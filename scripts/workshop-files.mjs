import { readFile, writeFile, mkdir, lstat, unlink } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { randomUUID } from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const features = ['priority', 'search', 'summary', 'handoff'];
const profiles = ['triage-reviewer', 'triage-coordinator', 'search-worker', 'summary-worker'];
const resources = ['SKILL.md', 'references/policy.md', 'scripts/inspect-fixtures.mjs'];
const allowed = new Set([
  ...features.map((name) => `src/features/${name}.mjs`),
  ...features.map((name) => `tests/features/${name}.test.mjs`),
  ...profiles.map((name) => `.github/agents/${name}.agent.md`),
  ...resources.map((resource) => `.github/skills/triage-policy/${resource}`)
]);

async function safePath(base, relative) {
  const parts = relative.split('/');
  let path = base;
  for (const part of parts) {
    if (!part || part === '.' || part === '..') throw new Error('Invalid workshop path.');
    path = join(path, part);
    try {
      if ((await lstat(path)).isSymbolicLink()) throw new Error(`Refusing a symbolic link: ${path}`);
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }
  }
  return path;
}

async function existing(path) {
  try { return await readFile(path, 'utf8'); }
  catch (error) { if (error.code === 'ENOENT') return null; throw error; }
}

export async function applyFiles(base, changes) {
  const seen = new Set();
  const originals = [];
  for (const change of changes) {
    if (!allowed.has(change.path) || seen.has(change.path) || (change.content !== null && typeof change.content !== 'string')) {
      throw new Error(`Invalid or duplicate workshop target: ${change.path}`);
    }
    seen.add(change.path);
    const target = await safePath(base, change.path);
    originals.push({ path: change.path, content: await existing(target) });
  }
  const id = `${Date.now()}-${randomUUID()}`;
  const backup = await safePath(base, `.workshop-backups/${id}`);
  await mkdir(backup, { recursive: true });
  await writeFile(join(backup, 'manifest.json'), JSON.stringify({ schemaVersion: 1, files: originals }, null, 2));
  console.log(`Backup saved: ${id}. Restore with npm run workshop:restore -- ${id}`);
  for (let index = 0; index < changes.length; index++) {
    const change = changes[index];
    const target = await safePath(base, change.path);
    if (await existing(target) !== originals[index].content) {
      throw new Error(`Concurrent edit detected at ${change.path}; stopped. Use the saved backup after resolving ownership.`);
    }
    if (change.content === null) {
      if (originals[index].content !== null) await unlink(target);
    } else {
      await mkdir(dirname(target), { recursive: true });
      await writeFile(target, change.content);
    }
    console.log(`${change.content === null ? 'Restored absence' : 'Wrote'}: ${change.path}`);
  }
  return id;
}

export async function restoreFiles(base, id) {
  if (!/^\d+-[a-f0-9-]{36}$/.test(id)) throw new Error('Use the exact backup ID printed by the workshop command.');
  const directory = await safePath(base, `.workshop-backups/${id}`);
  const manifest = JSON.parse(await readFile(join(directory, 'manifest.json'), 'utf8'));
  if (manifest.schemaVersion !== 1 || !Array.isArray(manifest.files)) throw new Error('Invalid backup manifest.');
  return applyFiles(base, manifest.files);
}

async function fromSource(source, target, transform = (content) => content) {
  return { path: target, content: transform(await readFile(join(root, ...source.split('/')), 'utf8')) };
}

async function featureChanges(names, starter = false) {
  const changes = [];
  for (const name of names) {
    changes.push(await fromSource(`workshop2/${starter ? 'starter' : 'solutions'}/features/${name}.mjs`, `src/features/${name}.mjs`));
    changes.push(starter
      ? { path: `tests/features/${name}.test.mjs`, content: null }
      : await fromSource(`workshop2/solutions/tests/${name}.test.mjs`, `tests/features/${name}.test.mjs`));
  }
  return changes;
}

async function customizationChanges(harness, template = false, onlyLab1 = false) {
  const changes = [];
  for (const profile of template || onlyLab1 ? ['triage-reviewer'] : profiles) {
    const source = template ? `workshop2/templates/${profile}.agent.md` : `workshop2/solutions/customizations/${harness}/${profile}.agent.md`;
    changes.push(await fromSource(source, `.github/agents/${profile}.agent.md`, (content) => template
      ? content.replace("tools: ['read', 'search']", `target: ${harness === 'local' ? 'vscode' : 'github-copilot'}\ntools: ['read', 'search']`)
        .replace('TODO: Add target: vscode for Local OR target: github-copilot for Copilot above.', 'The target is set for your selected harness; it does not switch the runtime.')
      : content));
  }
  for (const resource of resources) {
    changes.push(await fromSource(`workshop2/${template ? 'templates' : 'solutions/customizations'}/triage-policy/${resource}`, `.github/skills/triage-policy/${resource}`));
  }
  return changes;
}

async function main() {
  const [action, selection, extra] = process.argv.slice(2);
  if (extra) throw new Error('Too many arguments.');
  if (action === 'restore') {
    await restoreFiles(root, selection ?? '');
  } else if (action === 'starter' && !selection) {
    console.log('Restoring four starter modules and removing ONLY the four named exercise test files; all prior contents are backed up.');
    await applyFiles(root, await featureChanges(features, true));
  } else if (action === 'setup' && ['local', 'copilot'].includes(selection)) {
    await applyFiles(root, await customizationChanges(selection, true));
    console.log('Templates installed, NOT complete. Finish TODOs in Lab 1.');
  } else if (action === 'apply' && (features.includes(selection) || selection === 'all')) {
    await applyFiles(root, await featureChanges(selection === 'all' ? features : [selection]));
  } else if (action === 'apply' && ['lab1-local', 'lab1-copilot', 'agents-local', 'agents-copilot'].includes(selection)) {
    const harness = selection.endsWith('local') ? 'local' : 'copilot';
    await applyFiles(root, await customizationChanges(harness, false, selection.startsWith('lab1')));
  } else {
    throw new Error('Usage: workshop:setup -- local|copilot; workshop:apply -- priority|search|summary|handoff|all|lab1-local|lab1-copilot|agents-local|agents-copilot; workshop:restore -- <backup-id>; workshop:starter');
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  await main();
}

import { readFile, readdir, access } from 'node:fs/promises';
import { basename, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const requireLab1 = process.argv.includes('--require-lab1');
if (process.argv.slice(2).some((arg) => arg !== '--require-lab1')) throw new Error('Only --require-lab1 is supported.');

async function entries(path) {
  try { return await readdir(path, { withFileTypes: true }); }
  catch (error) { if (error.code === 'ENOENT') return []; throw error; }
}

function metadata(text, path) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) throw new Error(`${path}: frontmatter delimiters are required.`);
  const fields = {};
  for (const line of match[1].split(/\r?\n/)) {
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const field = line.match(/^([a-z][a-z-]*):\s*(.+)$/);
    if (!field || Object.hasOwn(fields, field[1])) throw new Error(`${path}: use the workshop's flat, unique frontmatter fields.`);
    fields[field[1]] = field[2].trim();
  }
  if (!text.slice(match[0].length).trim()) throw new Error(`${path}: instructions are empty.`);
  return fields;
}

function scalar(value) {
  return value?.replace(/^(['"])(.*)\1$/, '$2');
}

function list(value, path) {
  if (!value?.startsWith('[') || !value.endsWith(']')) throw new Error(`${path}: use a bracketed tools/agents/skills list.`);
  const inside = value.slice(1, -1).trim();
  if (!inside) return [];
  return inside.split(',').map((item) => scalar(item.trim()));
}

async function checkAgents(directory, active) {
  const names = [];
  for (const entry of await entries(directory)) {
    if (!entry.isFile() || !entry.name.endsWith('.agent.md')) continue;
    const path = join(directory, entry.name);
    const text = await readFile(path, 'utf8');
    const fields = metadata(text, path);
    const name = scalar(fields.name);
    if (!name || !scalar(fields.description)) throw new Error(`${path}: name and description are required for this workshop.`);
    if (names.includes(name)) throw new Error(`${path}: duplicate agent name.`);
    names.push(name);
    const target = scalar(fields.target);
    if (!['vscode', 'github-copilot'].includes(target)) throw new Error(`${path}: set an explicit workshop target.`);
    const unsupported = target === 'vscode'
      ? ['skills', 'mcp-servers']
      : ['agents', 'handoffs', 'argument-hint', 'advancedOptions'];
    for (const key of unsupported) if (fields[key]) throw new Error(`${path}: ${key} is unsupported for ${target}.`);
    const tools = list(fields.tools, path);
    for (const tool of tools) {
      if (!['read', 'search', 'edit', 'execute', 'agent', 'web', 'todo'].includes(tool)) {
        throw new Error(`${path}: unknown tool in the workshop subset: ${tool}`);
      }
    }
    if (fields.agents) list(fields.agents, path);
    if (fields.skills) list(fields.skills, path);
    if (name === 'Triage Reviewer' && JSON.stringify(tools) !== JSON.stringify(['read', 'search'])) {
      throw new Error(`${path}: Triage Reviewer must have only read/search tools.`);
    }
    if (active && /\bTODO\b|REPLACE_ME/.test(text)) throw new Error(`${path}: unfinished Lab 1 template.`);
  }
  return names;
}

async function checkSkill(directory, active) {
  const path = join(directory, 'SKILL.md');
  const text = await readFile(path, 'utf8');
  const fields = metadata(text, path);
  if (scalar(fields.name) !== basename(directory) || !scalar(fields.description)) {
    throw new Error(`${path}: name must match the folder and description must be present.`);
  }
  for (const resource of ['references/policy.md', 'scripts/inspect-fixtures.mjs']) {
    if (!text.includes(resource)) throw new Error(`${path}: link or name the bundled resource ${resource}.`);
    await access(join(directory, ...resource.split('/')));
  }
  const policy = await readFile(join(directory, 'references', 'policy.md'), 'utf8');
  if (active && /\bTODO\b|REPLACE_ME/.test(text + policy)) throw new Error(`${path}: unfinished skill or reference.`);
}

await access(join(root, '.github', 'copilot-instructions.md'));
for (const harness of ['local', 'copilot']) {
  const names = await checkAgents(join(root, 'workshop2', 'solutions', 'customizations', harness), false);
  if (names.length !== 4) throw new Error(`Expected four complete ${harness} instructor profiles.`);
}
await checkSkill(join(root, 'workshop2', 'solutions', 'customizations', 'triage-policy'), false);
const activeNames = await checkAgents(join(root, '.github', 'agents'), true);
const skillDirectory = join(root, '.github', 'skills', 'triage-policy');
const activeSkills = (await entries(skillDirectory)).some((entry) => entry.isFile() && entry.name === 'SKILL.md');
if (activeSkills) await checkSkill(skillDirectory, true);
if (requireLab1 && (!activeNames.includes('Triage Reviewer') || !activeSkills)) {
  throw new Error('Lab 1 requires an active Triage Reviewer agent and complete triage-policy skill.');
}
console.log(`Customization subset passed: 8 instructor profiles, complete instructor skill, ${activeNames.length} active agents, ${activeSkills ? 1 : 0} active workshop skills.`);
console.log('This is not a full YAML/schema validator or proof of runtime tool permissions. Verify in the selected harness.');

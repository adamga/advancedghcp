import { readdir } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const root = fileURLToPath(new URL('../', import.meta.url));

export async function testFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const groups = await Promise.all(entries.map((entry) => {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) return testFiles(path);
    return entry.name.endsWith('.test.mjs') ? [path] : [];
  }));
  return groups.flat().sort();
}

export function runTests(files, extraEnv = {}) {
  if (!files.length) throw new Error('No test files were found.');
  const result = spawnSync(process.execPath, ['--test', ...files], {
    cwd: root,
    env: { ...process.env, ...extraEnv },
    stdio: 'inherit'
  });
  if (result.error) throw result.error;
  if (result.signal) throw new Error(`Tests stopped by signal ${result.signal}.`);
  return result.status;
}

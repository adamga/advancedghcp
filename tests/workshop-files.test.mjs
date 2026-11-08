import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, writeFile, rm, access } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { applyFiles, restoreFiles } from '../scripts/workshop-files.mjs';

test('workshop restore preserves replaced files and removes only previously absent named files', async (t) => {
  const base = await mkdtemp(join(tmpdir(), 'triage-restore-'));
  t.after(() => rm(base, { recursive: true }));
  await mkdir(join(base, 'src', 'features'), { recursive: true });
  await writeFile(join(base, 'src', 'features', 'priority.mjs'), 'original');
  await writeFile(join(base, 'keep.txt'), 'unrelated');
  const id = await applyFiles(base, [
    { path: 'src/features/priority.mjs', content: 'solution' },
    { path: 'tests/features/priority.test.mjs', content: 'new test' }
  ]);
  const rescue = await restoreFiles(base, id);
  assert.equal(await readFile(join(base, 'src', 'features', 'priority.mjs'), 'utf8'), 'original');
  await assert.rejects(access(join(base, 'tests', 'features', 'priority.test.mjs')), { code: 'ENOENT' });
  assert.equal(await readFile(join(base, 'keep.txt'), 'utf8'), 'unrelated');
  await restoreFiles(base, rescue);
  assert.equal(await readFile(join(base, 'src', 'features', 'priority.mjs'), 'utf8'), 'solution');
});

test('workshop helpers reject unknown targets and invalid backup IDs', async (t) => {
  const base = await mkdtemp(join(tmpdir(), 'triage-targets-'));
  t.after(() => rm(base, { recursive: true }));
  await assert.rejects(applyFiles(base, [{ path: '../outside', content: 'bad' }]), /Invalid/);
  await assert.rejects(restoreFiles(base, '..'), /exact backup ID/);
  await assert.rejects(applyFiles(base, [{ path: 'package.json', content: '{}' }]), /Invalid/);
});

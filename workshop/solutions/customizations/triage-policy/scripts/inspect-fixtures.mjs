import assert from 'node:assert/strict';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const { issues } = await import(pathToFileURL(join(process.cwd(), 'src', 'data', 'issues.mjs')).href);
assert.equal(issues.length, 8);
assert.equal(new Set(issues.map((issue) => issue.id)).size, 8);
for (const issue of issues) {
  assert.ok(['open', 'in-progress', 'closed'].includes(issue.status));
  assert.ok(['high', 'medium', 'low'].includes(issue.impact));
  assert.equal(typeof issue.blocked, 'boolean');
  assert.ok(Number.isInteger(issue.affectedUsers) && issue.affectedUsers >= 0);
  assert.ok(Number.isInteger(issue.ageDays) && issue.ageDays >= 0);
}
console.log('Validated 8 synthetic issues; no files changed.');
console.table(issues.map(({ id, status, impact, blocked, affectedUsers, ageDays }) => ({
  id, status, impact, blocked, affectedUsers, ageDays
})));

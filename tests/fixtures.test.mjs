import test from 'node:test';
import assert from 'node:assert/strict';
import { issues } from '../src/data/issues.mjs';

test('fixtures contain eight unique, valid synthetic support issues', () => {
  assert.equal(issues.length, 8);
  assert.equal(new Set(issues.map((issue) => issue.id)).size, 8);
  for (const issue of issues) {
    assert.match(issue.id, /^ISS-\d{3}$/);
    for (const key of ['title', 'description', 'category']) assert.equal(typeof issue[key], 'string');
    assert.ok(['open', 'in-progress', 'closed'].includes(issue.status));
    assert.ok(['low', 'medium', 'high'].includes(issue.impact));
    assert.equal(typeof issue.blocked, 'boolean');
    assert.ok(Number.isInteger(issue.affectedUsers) && issue.affectedUsers >= 0);
    assert.ok(Number.isInteger(issue.ageDays) && issue.ageDays >= 0);
  }
});

test('fixtures and fixture records cannot be accidentally edited', () => {
  assert.ok(Object.isFrozen(issues));
  assert.ok(issues.every(Object.isFrozen));
  assert.throws(() => { issues[0].title = 'changed'; }, TypeError);
});

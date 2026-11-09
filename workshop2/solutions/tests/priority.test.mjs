import test from 'node:test';
import assert from 'node:assert/strict';
import { prioritizeIssue } from '../../src/features/priority.mjs';

test('owned priority tests: exact user-count threshold and closed override', () => {
  const issue = { status: 'open', impact: 'medium', blocked: false, affectedUsers: 99, ageDays: 0 };
  assert.equal(prioritizeIssue(issue).score, 30);
  assert.equal(prioritizeIssue({ ...issue, affectedUsers: 100 }).level, 'P2');
  assert.deepEqual(prioritizeIssue({ ...issue, status: 'closed', blocked: true }), {
    level: 'P3', score: 0, reasons: ['closed issue (0)']
  });
});

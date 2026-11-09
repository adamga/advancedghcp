import test from 'node:test';
import assert from 'node:assert/strict';
import { summarizeIssues } from '../../src/features/summary.mjs';

test('owned summary tests: closed blocked is not active blocked', () => {
  const issues = Object.freeze([
    Object.freeze({ category: 'search', status: 'closed', blocked: true }),
    Object.freeze({ category: 'accessibility', status: 'in-progress', blocked: true })
  ]);
  assert.deepEqual(summarizeIssues(issues), {
    available: true, total: 2, open: 1, blocked: 1, byCategory: { accessibility: 1, search: 1 }
  });
});

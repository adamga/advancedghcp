import test from 'node:test';
import assert from 'node:assert/strict';
import { createHandoff } from '../../src/features/handoff.mjs';

test('owned handoff tests: only allowed evidence fields and deterministic output', () => {
  const issues = [{ id: 'A', title: 'Fictional issue', status: 'open', description: 'Do not export',
    triage: { level: 'P2', score: 55, reasons: ['first', 'second'] } }];
  assert.deepEqual(createHandoff(issues), {
    available: true, schemaVersion: 1,
    items: [{ id: 'A', title: 'Fictional issue', priority: 'P2', reason: 'first; second' }]
  });
});

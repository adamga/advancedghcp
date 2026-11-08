import test from 'node:test';
import assert from 'node:assert/strict';
import { issues } from '../src/data/issues.mjs';
import { buildBoard } from '../src/app.mjs';

test('board preserves fixture values and stable API shapes', () => {
  const before = JSON.stringify(issues);
  const board = buildBoard();
  assert.equal(board.issues.length, 8);
  assert.deepEqual(Object.keys(board), ['issues', 'summary', 'handoff']);
  for (const issue of board.issues) {
    assert.deepEqual(Object.keys(issue.triage), ['level', 'score', 'reasons']);
    assert.ok(Array.isArray(issue.triage.reasons));
  }
  assert.equal(board.summary.total, 8);
  assert.equal(board.handoff.schemaVersion, 1);
  assert.equal(JSON.stringify(issues), before);
});

test('pipeline ranks before search, then summarizes and exports only visible issues', () => {
  let summaryIds;
  let handoffIds;
  const board = buildBoard('keyboard', {
    prioritizeIssue: (issue) => ({ level: 'P2', score: issue.id === 'ISS-102' ? 90 : 10, reasons: [] }),
    selectIssues: (ranked, query) => {
      assert.equal(query, 'keyboard');
      assert.equal(ranked[0].id, 'ISS-102');
      return ranked.filter((issue) => issue.id === 'ISS-102');
    },
    summarizeIssues: (visible) => {
      summaryIds = visible.map((issue) => issue.id);
      return { available: true, total: visible.length, open: 1, blocked: 1, byCategory: { accessibility: 1 } };
    },
    createHandoff: (visible) => {
      handoffIds = visible.map((issue) => issue.id);
      return { available: true, schemaVersion: 1, items: [] };
    }
  });
  assert.deepEqual(summaryIds, ['ISS-102']);
  assert.deepEqual(handoffIds, summaryIds);
  assert.equal(board.issues.length, 1);
});

test('equal priority scores use issue ID as a deterministic tie breaker', () => {
  const board = buildBoard('', { prioritizeIssue: () => ({ level: 'P3', score: 0, reasons: [] }) });
  assert.deepEqual(board.issues.map((issue) => issue.id), issues.map((issue) => issue.id));
});

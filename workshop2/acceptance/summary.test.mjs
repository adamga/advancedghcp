import test from 'node:test';
import assert from 'node:assert/strict';
import { issues } from '../../src/data/issues.mjs';
import { loadFeature } from './load-feature.mjs';
const { summarizeIssues } = await loadFeature('summary');

test('summary: all fixtures give eight total, six active, two active blocked', () => {
  assert.deepEqual(summarizeIssues(issues), {
    available: true, total: 8, open: 6, blocked: 2,
    byCategory: { accessibility: 2, payments: 2, reporting: 2, search: 2 }
  });
});

test('summary: an empty result is available and has zero counts', () => {
  assert.deepEqual(summarizeIssues([]), { available: true, total: 0, open: 0, blocked: 0, byCategory: {} });
});

test('summary: closed blocked issues count toward total and category, not active or blocked', () => {
  assert.deepEqual(summarizeIssues([issues[4]]), { available: true, total: 1, open: 0, blocked: 0, byCategory: { payments: 1 } });
});

test('summary: in-progress is active; only the supplied visible subset is counted', () => {
  assert.deepEqual(summarizeIssues([issues[3], issues[5]]), {
    available: true, total: 2, open: 2, blocked: 0, byCategory: { reporting: 1, search: 1 }
  });
});

test('summary: category keys have deterministic alphabetical insertion order', () => {
  assert.deepEqual(Object.keys(summarizeIssues([...issues].reverse()).byCategory), ['accessibility', 'payments', 'reporting', 'search']);
});

test('summary: input is not mutated and outputs are fresh objects', () => {
  const before = JSON.stringify(issues);
  const first = summarizeIssues(issues);
  const second = summarizeIssues(issues);
  assert.notEqual(first, second);
  assert.notEqual(first.byCategory, second.byCategory);
  assert.equal(JSON.stringify(issues), before);
});

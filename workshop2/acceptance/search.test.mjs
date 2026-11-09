import test from 'node:test';
import assert from 'node:assert/strict';
import { issues } from '../../src/data/issues.mjs';
import { loadFeature } from './load-feature.mjs';
const { selectIssues } = await loadFeature('search');
const ids = (selected) => selected.map((issue) => issue.id);

test('search: empty and whitespace queries return a new array of all issues', () => {
  for (const query of ['', '   ', '\t\n']) {
    const result = selectIssues(issues, query);
    assert.notEqual(result, issues);
    assert.deepEqual(result, issues);
  }
});

test('search: uppercase and mixed case match title and description', () => {
  assert.deepEqual(ids(selectIssues(issues, 'KEYBOARD')), ['ISS-102']);
  assert.deepEqual(ids(selectIssues(issues, 'bLuE')), ['ISS-104']);
});

test('search: category matching includes closed issues', () => {
  assert.deepEqual(ids(selectIssues(issues, 'PAYMENTS')), ['ISS-101', 'ISS-105']);
});

test('search: all whitespace-separated words must match, even across different fields', () => {
  assert.deepEqual(ids(selectIssues(issues, '  keyboard \t accessibility  ')), ['ISS-102']);
  assert.deepEqual(ids(selectIssues(issues, 'keyboard payments')), []);
});

test('search: unmatched and regular-expression-like strings are literal text', () => {
  assert.deepEqual(selectIssues(issues, 'no-such-issue'), []);
  assert.deepEqual(selectIssues(issues, '.*'), []);
});

test('search: preserves input order, objects, and fixture values', () => {
  const reversed = Object.freeze([...issues].reverse());
  const before = JSON.stringify(reversed);
  const result = selectIssues(reversed, 'search');
  assert.deepEqual(ids(result), ['ISS-108', 'ISS-104']);
  assert.equal(result[0], issues[7]);
  assert.equal(JSON.stringify(reversed), before);
});

import test from 'node:test';
import assert from 'node:assert/strict';
import { selectIssues } from '../../src/features/search.mjs';

test('owned search tests: AND matching, literal characters, and input order', () => {
  const issues = Object.freeze([
    Object.freeze({ id: 'A', title: 'Keyboard menu', description: 'Tab focus', category: 'accessibility' }),
    Object.freeze({ id: 'B', title: 'Chart', description: 'Legend', category: 'reporting' })
  ]);
  assert.deepEqual(selectIssues(issues, 'KEYBOARD accessibility'), [issues[0]]);
  assert.deepEqual(selectIssues(issues, 'keyboard reporting'), []);
  assert.deepEqual(selectIssues(issues, '.*'), []);
  assert.notEqual(selectIssues(issues, ''), issues);
});

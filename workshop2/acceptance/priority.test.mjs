import test from 'node:test';
import assert from 'node:assert/strict';
import { issues } from '../../src/data/issues.mjs';
import { loadFeature } from './load-feature.mjs';
const { prioritizeIssue } = await loadFeature('priority');
const sample = { ...issues[0], status: 'open', blocked: false, affectedUsers: 0, ageDays: 0 };

test('priority: all eight fixture scores and levels match the policy', () => {
  assert.deepEqual(issues.map((issue) => {
    const { score, level } = prioritizeIssue(issue);
    return [issue.id, score, level];
  }), [
    ['ISS-101', 100, 'P1'], ['ISS-102', 55, 'P2'], ['ISS-103', 15, 'P3'],
    ['ISS-104', 40, 'P2'], ['ISS-105', 0, 'P3'], ['ISS-106', 35, 'P3'],
    ['ISS-107', 10, 'P3'], ['ISS-108', 0, 'P3']
  ]);
});

test('priority: user-count boundary is exactly 100', () => {
  assert.equal(prioritizeIssue({ ...sample, impact: 'medium', affectedUsers: 99 }).score, 30);
  assert.equal(prioritizeIssue({ ...sample, impact: 'medium', affectedUsers: 100 }).score, 40);
  assert.equal(prioritizeIssue({ ...sample, impact: 'medium', affectedUsers: 100 }).level, 'P2');
});

test('priority: age boundary is exactly seven days', () => {
  assert.equal(prioritizeIssue({ ...sample, ageDays: 6 }).score, 60);
  assert.equal(prioritizeIssue({ ...sample, ageDays: 7 }).score, 65);
});

test('priority: the threshold at 80 separates reachable scores 75 and 85', () => {
  assert.deepEqual(prioritizeIssue({ ...sample, impact: 'high', blocked: false, affectedUsers: 100, ageDays: 7 }).level, 'P2');
  const p1 = prioritizeIssue({ ...sample, impact: 'high', blocked: true });
  assert.equal(p1.score, 85);
  assert.equal(p1.level, 'P1');
});

test('priority: closed issues always return zero, P3, and only the closed reason', () => {
  assert.deepEqual(prioritizeIssue(issues[4]), { level: 'P3', score: 0, reasons: ['closed issue (0)'] });
});

test('priority: result shape, reason ordering, and fixture immutability are exact', () => {
  const before = JSON.stringify(issues);
  assert.deepEqual(prioritizeIssue(issues[0]), {
    level: 'P1',
    score: 100,
    reasons: ['high impact (+60)', 'blocked workflow (+25)', '100+ affected users (+10)', '7+ days old (+5)']
  });
  assert.equal(JSON.stringify(issues), before);
  assert.throws(() => prioritizeIssue({ ...sample, impact: 'unknown' }), /Unknown impact/);
  assert.throws(() => prioritizeIssue({ ...sample, impact: 'constructor' }), /Unknown impact/);
});

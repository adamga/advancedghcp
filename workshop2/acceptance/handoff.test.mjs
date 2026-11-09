import test from 'node:test';
import assert from 'node:assert/strict';
import { issues } from '../../src/data/issues.mjs';
import { loadFeature } from './load-feature.mjs';
const { createHandoff } = await loadFeature('handoff');
const ranked = issues.map((issue) => ({ ...issue, triage: { level: 'P2', score: 50, reasons: ['sample reason', 'second reason'] } }));

test('handoff: output has exact schema and six active fixture items', () => {
  const report = createHandoff(ranked);
  assert.deepEqual(Object.keys(report), ['available', 'schemaVersion', 'items']);
  assert.equal(report.available, true);
  assert.equal(report.schemaVersion, 1);
  assert.equal(report.items.length, 6);
});

test('handoff: projects only id, title, priority, and joined evidence', () => {
  assert.deepEqual(createHandoff([ranked[0]]).items, [{
    id: 'ISS-101', title: issues[0].title, priority: 'P2', reason: 'sample reason; second reason'
  }]);
});

test('handoff: closed issues are excluded, including blocked closed issues', () => {
  assert.deepEqual(createHandoff([ranked[4], ranked[7]]).items, []);
});

test('handoff: preserves supplied ranked/filtered order without re-scoring', () => {
  assert.deepEqual(createHandoff([ranked[3], ranked[1]]).items.map((item) => item.id), ['ISS-104', 'ISS-102']);
});

test('handoff: empty result is available and deterministic with no timestamp', () => {
  assert.deepEqual(createHandoff([]), { available: true, schemaVersion: 1, items: [] });
  assert.equal(JSON.stringify(createHandoff(ranked)), JSON.stringify(createHandoff(ranked)));
  assert.doesNotMatch(JSON.stringify(createHandoff(ranked)), /timestamp|description|affectedUsers/);
});

test('handoff: input is not mutated and projected items do not alias issues', () => {
  const before = JSON.stringify(ranked);
  const report = createHandoff(ranked);
  assert.notEqual(report.items[0], ranked[0]);
  assert.equal(JSON.stringify(ranked), before);
});

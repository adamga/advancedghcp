import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { buildBoard } from '../../src/app.mjs';
import { createAppServer } from '../../src/http.mjs';
import { loadAllFeatures } from './load-feature.mjs';
const features = await loadAllFeatures();

test('integration: all solutions rank fixtures and agree on visible summary/export', () => {
  const board = buildBoard('', features);
  assert.deepEqual(board.issues.map((issue) => issue.id), ['ISS-101', 'ISS-102', 'ISS-104', 'ISS-106', 'ISS-103', 'ISS-107', 'ISS-105', 'ISS-108']);
  assert.equal(board.summary.open, 6);
  assert.equal(board.handoff.items.length, 6);
  const filtered = buildBoard('PAYMENTS', features);
  assert.deepEqual(filtered.issues.map((issue) => issue.id), ['ISS-101', 'ISS-105']);
  assert.deepEqual(filtered.summary, { available: true, total: 2, open: 1, blocked: 1, byCategory: { payments: 2 } });
  assert.equal(filtered.handoff.items.length, 1);
  assert.equal(filtered.handoff.items[0].priority, 'P1');
});

test('integration: real HTTP query filtering and evidence attachment work together', async (t) => {
  const server = createAppServer(features);
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  t.after(() => new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve())));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const board = await (await fetch(`${origin}/api/issues?q=KEYBOARD`)).json();
  assert.equal(board.issues.length, 1);
  assert.equal(board.summary.blocked, 1);
  assert.equal(board.handoffAvailable, true);
  const response = await fetch(`${origin}/api/handoff?q=KEYBOARD`);
  assert.equal(response.status, 200);
  assert.match(response.headers.get('content-disposition'), /attachment/);
  const report = await response.json();
  assert.deepEqual(report.items, [{
    id: 'ISS-102', title: 'Keyboard focus disappears in the menu', priority: 'P2',
    reason: 'medium impact (+30); blocked workflow (+25)'
  }]);
});

import test from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { createAppServer } from '../src/http.mjs';

async function serve(t, features = {}) {
  const server = createAppServer(features);
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  t.after(() => new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve())));
  return `http://127.0.0.1:${server.address().port}`;
}

test('health and issue HTTP contracts return local fixture data', async (t) => {
  const origin = await serve(t);
  const health = await fetch(`${origin}/api/health`);
  assert.deepEqual(await health.json(), { status: 'ok', fixtureCount: 8 });
  const response = await fetch(`${origin}/api/issues`);
  assert.equal(response.status, 200);
  const body = await response.json();
  assert.deepEqual(Object.keys(body), ['issues', 'summary', 'handoffAvailable']);
  assert.equal(body.issues.length, 8);
  assert.match(response.headers.get('content-type'), /application\/json/);
});

test('static assets have explicit types and self-only browser policy', async (t) => {
  const origin = await serve(t);
  for (const [path, type] of [['/', 'text/html'], ['/app.js', 'text/javascript'], ['/styles.css', 'text/css'], ['/favicon.svg', 'image/svg+xml']]) {
    const response = await fetch(`${origin}${path}`);
    assert.equal(response.status, 200);
    assert.ok(response.headers.get('content-type').startsWith(type));
    assert.equal(response.headers.get('x-content-type-options'), 'nosniff');
    assert.match(response.headers.get('content-security-policy'), /default-src 'self'/);
    assert.ok((await response.text()).length > 0);
  }
});

test('unknown paths and non-GET requests fail explicitly', async (t) => {
  const origin = await serve(t);
  assert.equal((await fetch(`${origin}/not-a-file`)).status, 404);
  assert.equal((await fetch(`${origin}/package.json`)).status, 404);
  const response = await fetch(`${origin}/api/issues`, { method: 'POST', body: '{}' });
  assert.equal(response.status, 405);
  assert.equal(response.headers.get('allow'), 'GET');
});

test('query length is bounded at the HTTP boundary', async (t) => {
  const origin = await serve(t);
  assert.equal((await fetch(`${origin}/api/issues?q=${'x'.repeat(200)}`)).status, 200);
  const response = await fetch(`${origin}/api/issues?q=${'x'.repeat(201)}`);
  assert.equal(response.status, 400);
  assert.match((await response.json()).error, /200/);
});

test('export route is unavailable until Lab 4, then returns a JSON attachment', async (t) => {
  const unavailable = await serve(t, { createHandoff: () => ({ available: false, schemaVersion: 1, items: [] }) });
  assert.equal((await fetch(`${unavailable}/api/handoff`)).status, 501);
  const enabled = await serve(t, { createHandoff: () => ({ available: true, schemaVersion: 1, items: [] }) });
  const response = await fetch(`${enabled}/api/handoff`);
  assert.equal(response.status, 200);
  assert.match(response.headers.get('content-disposition'), /triage-handoff\.json/);
  assert.deepEqual(await response.json(), { available: true, schemaVersion: 1, items: [] });
});

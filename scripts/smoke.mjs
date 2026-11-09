import assert from 'node:assert/strict';
import { once } from 'node:events';
import { createAppServer } from '../src/http.mjs';

const server = createAppServer();
server.listen(0, '127.0.0.1');
try {
  await once(server, 'listening');
  const origin = `http://127.0.0.1:${server.address().port}`;
  for (const path of ['/', '/styles.css', '/app.js', '/favicon.svg', '/api/health', '/api/issues']) {
    const response = await fetch(`${origin}${path}`);
    assert.equal(response.status, 200, path);
    assert.ok((await response.text()).length > 0, path);
  }
  const response = await fetch(`${origin}/api/issues`);
  const board = await response.json();
  assert.equal(board.issues.length, 8);
  const missing = await fetch(`${origin}/missing`);
  assert.equal(missing.status, 404);
  console.log('HTTP smoke passed: 6 routes, 8 fictional issues, and 404 handling.');
} finally {
  await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

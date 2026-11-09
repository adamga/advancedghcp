import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

test('page provides search labels, live status, an alert, and keyboard entry points', async () => {
  const html = await readFile(new URL('../public/index.html', import.meta.url), 'utf8');
  assert.match(html, /<html lang="en">/);
  assert.match(html, /<label for="query">/);
  assert.match(html, /role="status" aria-live="polite"/);
  assert.match(html, /role="alert"/);
  assert.match(html, /href="#issues"/);
  assert.match(html, /id="issues" tabindex="-1"/);
});

test('browser rendering treats issue content as text rather than HTML', async () => {
  const js = await readFile(new URL('../public/app.js', import.meta.url), 'utf8');
  assert.match(js, /textContent = text/);
  assert.doesNotMatch(js, /\.innerHTML\s*=/);
  assert.match(js, /encodeURIComponent\(query\)/);
  assert.match(js, /version !== requestVersion/);
});

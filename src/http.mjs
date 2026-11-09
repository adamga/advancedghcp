import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { buildBoard } from './app.mjs';

const assets = new Map([
  ['/', ['index.html', 'text/html; charset=utf-8']],
  ['/app.js', ['app.js', 'text/javascript; charset=utf-8']],
  ['/styles.css', ['styles.css', 'text/css; charset=utf-8']],
  ['/favicon.svg', ['favicon.svg', 'image/svg+xml']]
]);
const headers = {
  'Cache-Control': 'no-store',
  'X-Content-Type-Options': 'nosniff',
  'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
};

function sendJson(response, status, body) {
  response.writeHead(status, { ...headers, 'Content-Type': 'application/json; charset=utf-8' });
  response.end(JSON.stringify(body));
}

export function createAppServer(features = {}) {
  return createServer(async (request, response) => {
    try {
      const url = new URL(request.url, 'http://localhost');
      if (request.method !== 'GET') {
        response.setHeader('Allow', 'GET');
        sendJson(response, 405, { error: 'Only GET is supported.' });
        return;
      }
      if (url.pathname === '/api/health') {
        sendJson(response, 200, { status: 'ok', fixtureCount: 8 });
        return;
      }
      if (url.pathname === '/api/issues' || url.pathname === '/api/handoff') {
        const query = url.searchParams.get('q') ?? '';
        if (query.length > 200) {
          sendJson(response, 400, { error: 'Search must be 200 characters or fewer.' });
          return;
        }
        const board = buildBoard(query, features);
        if (url.pathname === '/api/handoff') {
          if (!board.handoff.available) {
            sendJson(response, 501, { error: 'Evidence export is a Lab 4 enhancement.' });
            return;
          }
          response.setHeader('Content-Disposition', 'attachment; filename="triage-handoff.json"');
          sendJson(response, 200, board.handoff);
          return;
        }
        sendJson(response, 200, { issues: board.issues, summary: board.summary, handoffAvailable: board.handoff.available });
        return;
      }
      const asset = assets.get(url.pathname);
      if (!asset) {
        sendJson(response, 404, { error: 'Not found.' });
        return;
      }
      const content = await readFile(new URL(`../public/${asset[0]}`, import.meta.url));
      response.writeHead(200, { ...headers, 'Content-Type': asset[1] });
      response.end(content);
    } catch (error) {
      console.error('Request failed:', error);
      if (!response.headersSent) sendJson(response, 500, { error: 'The request could not be completed.' });
      else response.destroy(error);
    }
  });
}

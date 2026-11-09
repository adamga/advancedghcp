import { createAppServer } from './http.mjs';
import { pathToFileURL } from 'node:url';

export function startServer(features = {}) {
  const port = Number(process.env.PORT ?? 3000);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error('PORT must be an integer between 1 and 65535.');
  }
  const server = createAppServer(features);
  server.on('error', (error) => {
    console.error('Server failed:', error.message);
    process.exitCode = 1;
  });
  server.listen(port, '127.0.0.1', () => {
    console.log(`Issue triage board: http://127.0.0.1:${port}`);
    console.log('Fictional, read-only data. Stop with Ctrl+C.');
  });
  return server;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) startServer();

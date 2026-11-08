import { join } from 'node:path';
import { root, runTests } from './run-tests.mjs';

const features = ['priority', 'search', 'summary', 'handoff'];
const selected = process.argv[2] ?? 'all';
if (process.argv.length > 3 || (selected !== 'all' && !features.includes(selected))) {
  throw new Error('Usage: npm run acceptance -- priority|search|summary|handoff|all');
}
const names = selected === 'all' ? features : [selected];
const files = names.map((name) => join(root, 'workshop', 'acceptance', `${name}.test.mjs`));
if (selected === 'all') files.push(join(root, 'workshop', 'acceptance', 'integration.test.mjs'));
process.exitCode = runTests(files);

import { join } from 'node:path';
import { root, runTests } from './run-tests.mjs';

const featureRoot = join(root, 'workshop', 'solutions', 'features');
for (const name of ['priority', 'search', 'summary', 'handoff']) {
  console.log(`\nInstructor solution: ${name}`);
  const status = runTests([join(root, 'workshop', 'acceptance', `${name}.test.mjs`)], { WORKSHOP_FEATURE_ROOT: featureRoot });
  if (status !== 0) {
    process.exitCode = status;
    break;
  }
}
if (!process.exitCode) {
  console.log('\nInstructor integration');
  process.exitCode = runTests([join(root, 'workshop', 'acceptance', 'integration.test.mjs')], { WORKSHOP_FEATURE_ROOT: featureRoot });
}

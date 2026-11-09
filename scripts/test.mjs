import { join } from 'node:path';
import { root, runTests, testFiles } from './run-tests.mjs';

process.exitCode = runTests(await testFiles(join(root, 'tests')));

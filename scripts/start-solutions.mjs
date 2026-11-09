import { startServer } from '../src/server.mjs';
import { prioritizeIssue } from '../workshop2/solutions/features/priority.mjs';
import { selectIssues } from '../workshop2/solutions/features/search.mjs';
import { summarizeIssues } from '../workshop2/solutions/features/summary.mjs';
import { createHandoff } from '../workshop2/solutions/features/handoff.mjs';

console.log('Instructor answers: loaded separately; starter files are not changed.');
startServer({ prioritizeIssue, selectIssues, summarizeIssues, createHandoff });

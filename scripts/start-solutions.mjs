import { startServer } from '../src/server.mjs';
import { prioritizeIssue } from '../workshop/solutions/features/priority.mjs';
import { selectIssues } from '../workshop/solutions/features/search.mjs';
import { summarizeIssues } from '../workshop/solutions/features/summary.mjs';
import { createHandoff } from '../workshop/solutions/features/handoff.mjs';

console.log('Instructor answers: loaded separately; starter files are not changed.');
startServer({ prioritizeIssue, selectIssues, summarizeIssues, createHandoff });

import { issues as fixtures } from './data/issues.mjs';
import { prioritizeIssue } from './features/priority.mjs';
import { selectIssues } from './features/search.mjs';
import { summarizeIssues } from './features/summary.mjs';
import { createHandoff } from './features/handoff.mjs';

export function buildBoard(query = '', features = {}) {
  const priority = features.prioritizeIssue ?? prioritizeIssue;
  const select = features.selectIssues ?? selectIssues;
  const summary = features.summarizeIssues ?? summarizeIssues;
  const handoff = features.createHandoff ?? createHandoff;
  const ranked = fixtures.map((issue) => ({ ...issue, triage: priority(issue) }));
  ranked.sort((a, b) => (b.triage.score ?? 0) - (a.triage.score ?? 0) || a.id.localeCompare(b.id));
  const visible = select(ranked, query);
  return { issues: visible, summary: summary(visible), handoff: handoff(visible) };
}

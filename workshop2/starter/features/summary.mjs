// Lab 3B replaces the unavailable counts; the UI already understands both states.
export function summarizeIssues(issues) {
  return { available: false, total: issues.length, open: null, blocked: null, byCategory: null };
}

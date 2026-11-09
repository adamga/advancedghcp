export function summarizeIssues(issues) {
  const categories = [...new Set(issues.map((issue) => issue.category))].sort();
  const byCategory = Object.fromEntries(categories.map((category) => [
    category, issues.filter((issue) => issue.category === category).length
  ]));
  const active = issues.filter((issue) => issue.status !== 'closed');
  return {
    available: true,
    total: issues.length,
    open: active.length,
    blocked: active.filter((issue) => issue.blocked).length,
    byCategory
  };
}

export function selectIssues(issues, query) {
  const tokens = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  return issues.filter((issue) => {
    const text = [issue.title, issue.description, issue.category].join(' ').toLowerCase();
    return tokens.every((token) => text.includes(token));
  });
}

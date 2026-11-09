export function createHandoff(issues) {
  return {
    available: true,
    schemaVersion: 1,
    items: issues.filter((issue) => issue.status !== 'closed').map((issue) => ({
      id: issue.id,
      title: issue.title,
      priority: issue.triage.level,
      reason: issue.triage.reasons.join('; ')
    }))
  };
}

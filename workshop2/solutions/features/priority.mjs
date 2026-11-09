export function prioritizeIssue(issue) {
  if (issue.status === 'closed') return { level: 'P3', score: 0, reasons: ['closed issue (0)'] };
  const weights = { high: 60, medium: 30, low: 10 };
  if (!Object.hasOwn(weights, issue.impact)) throw new TypeError(`Unknown impact: ${issue.impact}`);
  const base = weights[issue.impact];
  let score = base;
  const reasons = [`${issue.impact} impact (+${base})`];
  if (issue.blocked) {
    score += 25;
    reasons.push('blocked workflow (+25)');
  }
  if (issue.affectedUsers >= 100) {
    score += 10;
    reasons.push('100+ affected users (+10)');
  }
  if (issue.ageDays >= 7) {
    score += 5;
    reasons.push('7+ days old (+5)');
  }
  const level = score >= 80 ? 'P1' : score >= 40 ? 'P2' : 'P3';
  return { level, score, reasons };
}

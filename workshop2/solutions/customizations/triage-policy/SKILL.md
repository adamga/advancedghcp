---
name: triage-policy
description: Explain the fictional issue-triage scoring policy and derive acceptance cases when implementing priority.
---
# Triage policy

Use for issue-priority implementation, explanation, and acceptance-case design.
This is a deterministic workshop rule, not an AI model or real support SLA.

1. Read [the policy reference](references/policy.md); keep the frozen function
   contract and exact reason strings.
2. Inspect the synthetic input schema. From the repository root, an authorized
   writer or human may run
   `node .github/skills/triage-policy/scripts/inspect-fixtures.mjs`.
   The script reads fixtures and prints a schema check; it changes no files.
3. Derive cases for a high-impact blocked issue, a closed issue, 99/100 users,
   6/7 days, and the reachable scores either side of the P1 boundary.
4. Implement only the assigned priority module/test, or return findings if the
   role is read-only. Do not edit server, UI, fixtures, dependencies, or solutions.
5. Run `npm run acceptance -- priority` if execution is authorized; otherwise
   report that command as NOT RUN. Cite the policy and actual evidence.

The skill grants no tools, does not prove automatic selection, and does not
authorize network access, installations, or writes outside the assignment.

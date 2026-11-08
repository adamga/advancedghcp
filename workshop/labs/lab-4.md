# Lab 4 - review, quality gates, evidence handoff

**15 minutes | workshop clock 02:45-03:00**

Complete the small evidence export, review the integrated result, and produce a
truthful handoff. Prerequisite: priority, search, and summary integrated.
One writer owns `src/features/handoff.mjs` and `tests/features/handoff.test.mjs`.
Other roles are read-only until that writer stops.

## Steps and pacing

| Lab minutes | Action | Checkpoint |
|---|---|---|
| 0-4 | Implement minimal deterministic export | Only handoff and its owned test changed |
| 4-8 | Run final gates and inspect HTTP/browser output | Six export +26 combined acceptance tests |
| 8-11 | Read-only review; address in-scope findings | Evidence-based quality report |
| 11-13 | Human/agent handoff | Exact tests, limitations, ownership released |
| 13-15 | Retrospective | One improvement and one boundary you will keep |

### 1. Implement the final enhancement (4 min)

```text
Implement createHandoff(rankedVisibleIssues) only in src/features/handoff.mjs
and create tests/features/handoff.test.mjs. Read workshop/contracts.md v1.
Return exactly {available:true,schemaVersion:1,items}. Exclude closed issues.
Project exactly id,title,priority:triage.level,reason:triage.reasons.join('; ').
Preserve supplied order, do not re-score/mutate, and add no timestamp or extra
fields. Empty input returns an available empty report.
No server/UI/package/fixture/acceptance/solution/other-feature changes,
dependencies, network, pushes or PRs. Return actual validation or NOT RUN commands.
Stop and release ownership when ready for review.
```

The server and download link are already wired; do not add another endpoint.
This app's "handoff" is a JSON artifact, not a Local agent-transition button.

### 2. Final gates (4 min)

```text
npm run acceptance -- handoff
npm run acceptance -- all
npm test
npm run smoke
npm run check:customizations -- --require-lab1
```

Expected: six export checks and **26 combined feature/integration checks** pass.
Baseline plus your owned tests pass; customization check passes the completed
Lab 1 files. If you used fallback without active customizations, run the ordinary
check and explicitly record that runtime customization verification was skipped.

Restart `npm start` and refresh. Search `PAYMENTS`, then choose **Download evidence
JSON**. It contains one item, ISS-101, priorityP1, with four joined reasons.
It excludes closed ISS-105 and does not export descriptions, user counts, or
timestamps. Search `KEYBOARD`: ISS-102/P2, reason
`medium impact (+30); blocked workflow (+25)`. Empty results produce available
empty JSON. Verify keyboard access to search/clear/download and narrow-screen
layout; these are manual observations, not inferred from a source test.

### 3. Read-only integrated review (3 min)

```text
Use Triage Reviewer for one bounded integrated review.
Read the four src/features modules, the task-owned tests, and workshop/contracts.md.
Invariants: Node built-ins/synthetic-only, no mutation, frozen signatures,
no network/dependencies/shared-file edits; reviewer read/search only.
Check closed overrides, literal AND search, visible-summary consistency,
minimal export fields and truthful evidence. No terminal, edits, or delegation.
Return high-confidence findings with file/line impact, missing cases, suggested
checks marked NOT RUN, and limitations. Stop after report.
```

Inspect findings yourself. No second writer "fixes while reviewing." The integrator
assigns any fix to its owner, waits for release, then re-runs relevant gates.
If there are unresolved failures, say **not ready**, not "complete except tests".

### 4. Evidence-based handoff (2 min)

Use [the report template](../templates/task-report.md). Include objective,
changed owned paths, contract v1, exact commands/exit/pass counts, observed
query/download cases, remaining limitations, and release/next integration action.
Do not paste the whole chat or invent results. If a role only read code, its
report says NOT RUN; the actual executor supplies the test evidence.

Example wording after actually verifying it:

```text
Ready for integration review: four feature contracts preserved; all 26 final
acceptance checks passed. PAYMENTS returns two visible issues, summary2/1/1,
and one active export item ISS-101/P1. No package/shared-server/fixture changes.
All writer leases released. Limit: no persistence or real support workflow.
No push, PR, merge, or cloud deployment is authorized by this handoff.
```

Add your **actual** baseline/customization/manual results; the example is not
evidence by itself.

### 5. Two-minute retrospective

Tell a partner: What should have been a direct task instead of a subagent?
Which explicit context fact prevented a mistake? What was advisory versus
actually tool-restricted? Name one boundary you will preserve in your own repo.
Stop at the three-hour mark; [extensions](../extensions.md) are extra work.

## Measurable acceptance and hints

The minimal export shape, filtering/order, determinism and non-mutation pass all
six checks. The combined gate passes26; baseline/smoke pass; actual UI/HTTP
observations and customization/fallback limits are reported. Review findings
are resolved or explicitly block readiness. Handoff contains real evidence and
released ownership, not permission to merge.

1. The implementation is `filter` active items, then `map` only four fields.
2. Consume existing `triage`; do not import/re-run priority.
3. A timestamp makes snapshots nondeterministic and violates this contract.
4. Instructor catch-up: `npm run workshop:apply -- handoff`, then run final
   gates and explain why minimal evidence is safer than a raw fixture dump.

# Lab 3 - two safely orchestrated workstreams

**40 minutes | workshop clock 02:05-02:45**

Implement search and summary on **one repository** with separate contracts and
tests. Make ownership, dependency, and integration choices explicit. Worktrees
are one optional isolation tool, not the whole orchestration story.

Prerequisite: frozen [contracts](../contracts.md), passing baseline, completed
priority or its acknowledged catch-up. Choose one execution route below.

## Steps and pacing

| Lab minutes | Action | Checkpoint |
|---|---|---|
| 0-6 | Inspect diff; assign ownership and freeze contracts | Advisory board and clear integrator |
| 6-13 | Two bounded read-only research workstreams | Independent A/B reports; no writes |
| 13-27 | Implement under the chosen ownership route | A/B feature and owned tests only |
| 27-35 | Release workers, integrate, run independent and combined gates | Correct filtered counts and no shared-file collision |
| 35-40 | Inspect same-repo limits and hand off | Evidence, recovery plan, alternative explained |

### 1. Freeze the contract and assign advisory leases (6 min)

Inspect your working diff before starting. Copy the
[task-board template](../templates/task-board.md) into `.workshop-reports/` if
desired; one human integrator owns that shared board. Assign role labels, not
personal data. Document:

- A owns `src/features/search.mjs` and `tests/features/search.test.mjs`.
- B owns `src/features/summary.mjs` and `tests/features/summary.test.mjs`.
- The integrator owns shared server/UI/package/fixture changes **if needed**,
  final combined gates, board updates, and all shared Git index/branch operations.

A and B depend only on the frozen contract, **not each other**. Neither imports
the other's module. The starter already integrates both signatures; no shared
source edit is required. "Lease granted" means an agreement, not a lock, sandbox,
permission enforcement, or an automatic expiry. CODEOWNERS routes reviews;
it does not prevent edits. Tools capable of editing can still edit unowned paths.

Agree to stop if a signature or shared-file change seems necessary. Preserve both
workers' changes, then let only the integrator change the shared contract/file.
Never let parallel workers edit package files "just in case".

### 2. Two read-only research packets (7 min)

Ask the coordinator to obtain these reports before authorizing implementation.
It may run independent research concurrently if supported; otherwise sequential
research is fine. Local uses a fresh invocation for each report.

**A: search research**

```text
Use Triage Reviewer for read-only task A.
Goal: derive literal query-filter behavior and tests, no implementation.
Read workshop/contracts.md, src/features/search.mjs, src/app.mjs and the synthetic
fixture schema in src/data/issues.mjs. No workshop/solutions/.
Invariants: built-ins only, synthetic data, no mutations/network/dependencies,
frozen exports, no shared-file edits; read/search only, no terminal/edit/delegate.
Expected report: matching fields, AND token semantics, empty query, literal .*
case, order/object preservation, owned test cases, acceptance command NOT RUN,
evidence with file/line references, uncertainties. Stop after report.
```

**B: summary research**

```text
Use Triage Reviewer for read-only task B.
Goal: derive visible-summary behavior and tests, no implementation.
Read workshop/contracts.md, src/features/summary.mjs, src/app.mjs and the synthetic
fixture schema in src/data/issues.mjs. No workshop/solutions/.
Invariants: built-ins only, synthetic data, no mutations/network/dependencies,
frozen exports, no shared-file edits; read/search only, no terminal/edit/delegate.
Expected report: total/active/active-blocked/category definitions, empty subset,
closed-blocked case, alphabetical keys, owned tests, acceptance command NOT RUN,
evidence with file/line references, uncertainties. Do not depend on task A. Stop.
```

Check both reports against contracts. Record ready status before any implementation.
Subagent context is separate, but the filesystem may be shared.

### 3. Choose a safe implementation route (14 min)

**Route A - recommended: research first, single integration writer.**
After both read-only reports, one coordinator implements A and then B using
the task packets below. Workers are research-only. This minimizes write races
while keeping research contexts bounded and independent.

**Route B - optional same-checkout concurrent writers.**
Create/select **Search Worker** and **Summary Worker** custom profiles before the
freeze. Give each only read/search/edit (no execute, web, delegation or Git).
Use the instructor guide's field pattern. Start two independently prompted
sessions that **actually point to the same checkout**, or runtime worker
delegation if supported/configured. Register their separate ownership first.
A Local coordinator must explicitly allow any delegated worker in its `agents`
list; do not alter that shared profile while work is running. Copilot's named
worker request is advisory, not an `agents` allowlist.

If these are user-prompted sessions, call them **top-level sessions**, not subagents.
If the app creates independent worktrees by default, do not fight its supported
workflow: choose Route A or the worktree alternative below. Same checkout is not
required to use the app, and a UI label is not proof of filesystem location.

Route B workers cannot run tests with their tool list. The human/integrator runs
the independent checks only after each worker reports done. Their role instructions
constrain edits by agreement; they do not enforce path-level permissions.

**A implementation packet**

```text
Task A: implement selectIssues(issues, query) in src/features/search.mjs and create
tests/features/search.test.mjs. Only those files are yours.
Use workshop/contracts.md v1 and the accepted search report supplied here.
Trim/lowercase/split whitespace; every literal token must match joined title,
description or category. Empty query returns a new array; preserve input order
and object identity; include closed issues; .* is literal. No input mutation.
No shared server/UI/package/fixture/acceptance/solution/other-task edits,
no network/dependencies/Git/delegation. Do not import summary.
Return changed paths, boundary cases, and npm run acceptance -- search as NOT RUN
if no execution tool. Stop and release your lease before integration.
```

**B implementation packet**

```text
Task B: implement summarizeIssues(visibleIssues) in src/features/summary.mjs and
create tests/features/summary.test.mjs. Only those files are yours.
Use workshop/contracts.md v1 and the accepted summary report supplied here.
Return available:true,total,open,blocked,byCategory. Active/open means not closed
(including in-progress); blocked means active AND blocked; category counts all
supplied issues with alphabetically inserted keys. Empty gives 0/0/0/{}.
No input mutation or hidden fixtures; no dependency on search.
No shared server/UI/package/fixture/acceptance/solution/other-task edits,
no network/dependencies/Git/delegation. Return changed paths, boundary cases and
npm run acceptance -- summary as NOT RUN if no execution tool. Stop/release.
```

The integrator attaches each accepted report to its packet; do not rely on shared
parent history. Only a deliberately authorized integration writer may execute
validation. Do not turn on nested delegation, marketplace tools, or broad terminal
access merely to finish this small exercise.

### 4. Release, integrate, validate (8 min)

Wait for both writers to stop. Inspect their diff for ownership violations before
running global checks. One integrator performs Git staging/commits if desired;
concurrent `git add`, branch switches, or cherry-picks are forbidden by agreement.

```text
npm run acceptance -- search
npm run acceptance -- summary
npm test
npm run smoke
```

Expected: six search and six summary checks pass. Restart your local server,
refresh, and search `PAYMENTS`: two visible issues, one active, one active blocked,
payments count2. Search `KEYBOARD accessibility`: ISS-102 and counts1/1/1.
Search `keyboard payments`: empty board with available zero summary.
Clear search: eight total, six active, two active blocked, categories2 each.

Only the integrator changes shared wiring if a legitimate integration issue is
found. In the provided starter, no change should be needed. Re-run both relevant
feature gates after any shared edit. Passing each independent test alone does not
prove wiring correctness; HTTP and observed filtered counts are the combined check.

### 5. Limits, alternatives, handoff (5 min)

Explain what remains shared in a single checkout: source files, working tree,
Git index/branch, running processes, environment, and server ports. Read/search/edit
profiles remove terminal bypass for those workers, but still are not path locks.
Subagent context does not auto-create a sandbox or worktree.

**Portable no-preview fallback:** one chat, one writer. Obtain read-only A report,
then read-only B report. Freeze both contracts. Implement/test A, then B, then
integrate and run combined checks. The ownership/contract/dependency lesson is
the same; report that execution was sequential.

**Worktree branch-isolation alternative:** on clean committed checkpoints, the
integrator creates separate worktree branches for A and B. Each owns its files
and runs its tests in its own directory. Use different server ports. Commit
each task, then one integrator cherry-picks reviewed commits in dependency order
into an integration branch and runs the combined gates. Worktrees separate working
files/indexes, not repository-level collaboration or all external resources.

**PR alternative:** if your account/repo workflow permits it, separate branches
can become reviewed PRs; one integrator merges in dependency order and validates
the combined result. A PR/branch protects review/integration boundaries, not
parallel edits inside a shared checkout. Opening/pushing a PR is optional and
requires explicit permission; none is part of the mandatory lab.

Concrete safe worktree commands and collision recovery are in the
[instructor guide](../instructor-guide.md) and [restore guide](../restore.md).

## Measurable acceptance

Two explicit ownership records and a contract freeze exist. A/B research reports
are read-only and self-contained. Each task has its own implementation/test and
no cross-import or shared-file change. Six independent tests per task pass;
baseline/HTTP smoke and the three visible query/count cases pass. The integrator
records worker release, combined evidence, and the chosen actual execution route.

## Hint ladder

1. Search filters the supplied array; summary counts the supplied array. Neither
   should re-fetch/import fixtures or infer another task's behavior.
2. Search: `tokens.every(...)`; summary: active is `status !== 'closed'`.
3. For alphabetic category keys, collect/sort categories before creating counts.
   Closed blocked is a deliberate trap: it is not active blocked.
4. Instructor catch-up: apply `search` and `summary` separately with
   `npm run workshop:apply -- search` and `npm run workshop:apply -- summary`,
   then explain ownership and re-run integration checks. It is a rescue route,
   not permission for both writers to overwrite shared files.

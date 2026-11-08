# Lab 2 - bounded subagent, coordinator, priority

**35 minutes | workshop clock 01:30-02:05**

Use a restricted read-only specialist to derive a contract/test report, then
let one coordinator implement priority using the skill. Understand what was
delegated and what stayed in the parent. Prerequisite: Lab 1 customization
checkpoint, or the explicitly acknowledged instructor catch-up.

## Steps and pacing

| Lab minutes | Action | Checkpoint |
|---|---|---|
| 0-6 | Configure coordinator for chosen harness | Correct tools/fields; reviewer remains read-only |
| 6-14 | Delegate bounded policy research | Self-contained report with evidence, NOT RUN commands |
| 14-25 | Coordinator implements priority + owned tests using skill | Only two task-owned code/test files changed |
| 25-31 | Validate and request bounded review | Six priority checks and baseline pass |
| 31-35 | Inspect activity, handoff, explain distinctions | Honest role/context/tool report |

### 1. Build the coordinator (6 min)

Create `.github/agents/triage-coordinator.agent.md`. Use these verified fields
for your intended runtime; do not combine both examples.

**Copilot harness / app:**

```yaml
---
name: Triage Coordinator
description: Implement an assigned triage feature after bounded read-only research.
target: github-copilot
tools: ['read', 'search', 'edit', 'execute', 'agent']
skills: ['triage-policy']
---
```

**VS Code Local, selected explicitly in the session:**

```yaml
---
name: Triage Coordinator
description: Implement an assigned triage feature after bounded read-only research.
target: vscode
tools: ['read', 'search', 'edit', 'execute', 'agent']
agents: ['Triage Reviewer']
---
```

Add a body: restate ownership/contract; obtain a read-only report first; use the
skill explicitly; edit only priority and its test; run acceptance; obtain review;
report real evidence and stop. Local accepts the named-worker allowlist and no
`skills` field. Copilot accepts skill preloading and no `agents`/`handoffs`.
In Copilot, "only use this reviewer" in prose is an **advisory** choice, not a
Local-style enforced allowlist. Confirm actual available tools in either case.

Never rely on `include-custom-instructions` or `strict-tools-list` surviving
client conversion. Do not copy `agent/runSubagent` into a Copilot tool list:
Local uses that invocation reference; Copilot uses native delegation.

### 2. Delegate research only (8 min)

Select **Triage Coordinator**. Submit this complete task packet:

```text
Use Triage Reviewer as a read-only specialist for ONE policy research task.
Goal: derive priority implementation rules and boundary cases, not code changes.
Read workshop/contracts.md, src/data/issues.mjs, src/features/priority.mjs,
.github/skills/triage-policy/SKILL.md and its references/policy.md.
Do not read workshop/solutions/.
Explicit repo invariants: Node>=22 built-ins only, synthetic fixtures, no input
mutation, no network/dependencies, no shared server/UI/package/fixture edits.
Reviewer allowed actions: read/search only; no edits, terminal, web, or delegation.
Expected report: objective; exact contract with file/line evidence; ISS-101,
ISS-102 and closed ISS-105 worked cases; 99/100 users and 6/7 days; reason ordering;
commands to validate marked NOT RUN; uncertainties; stop after this report.
Do not implement yet. Return the specialist report for my inspection.
```

Verify a delegated tool call and the selected custom role actually appear.
In the VS Code Agents window, open the subagent indicator to inspect its
read-only chat; that lock means you cannot directly prompt that child chat,
not that the child's filesystem is sandboxed. If the UI is missing, inspect
ordinary chat activity or use the sequential fallback below.

Expected report: ISS-101=100/P1; ISS-102=55/P2; ISS-105=0/P3.
It cites policy paths and includes **NOT RUN** commands. It should not edit a
file or claim tests ran. A custom CLI subagent does not include repository
instructions by default, so the packet passes the necessary invariants directly.

### 3. Implement using the skill (11 min)

After inspecting the report, prompt the **coordinator**, not the read-only child:

```text
Use the triage-policy skill and accepted specialist findings to implement
prioritizeIssue(issue) in src/features/priority.mjs and create
tests/features/priority.test.mjs. Those are the only editable app/test paths.
Return fresh {level,score,reasons}; apply the closed override before additions.
Use exact rule/reason text from workshop/contracts.md. Cover user and age
boundaries, closed override, and non-mutation in the owned test.
Do not change exports, shared wiring, fixtures, package files, acceptance checks,
or other features. Do not read instructor solutions.
Run npm run acceptance -- priority and npm test if execution is authorized.
If blocked, stop editing and report exact NOT RUN commands for the human.
Stop after reporting changed paths and evidence; no pushes or PRs.
```

Check the skill/reference really appears in activity. Local uses explicit
discovery/invocation, not skills frontmatter. If preloading/discovery cannot be
verified, attach the installed skill/reference to this task and record the
fallback. A loaded skill does not expand the coordinator's tool permissions.

### 4. Run gates and review (6 min)

```text
npm run acceptance -- priority
npm test
```

Expected: six priority acceptance tests pass. All baseline checks pass; your
owned tests add to the baseline count. Restart `npm start` after a code change
(there is no watcher), then refresh. ISS-101 is P1 with four reasons; ISS-105
remains score0/P3 despite its high impact and blocked flag.

Ask for a **new bounded review** with the full current context:

```text
Use Triage Reviewer to read src/features/priority.mjs,
tests/features/priority.test.mjs and workshop/contracts.md.
Check closed override, inclusive 100-user/7-day boundaries, exact reason order,
fresh outputs, and no shared-file changes. Read/search only; no commands or edits.
Return file/line findings, missing cases, and NOT RUN suggested checks. Stop.
```

Local invocations are stateless: a new review is a new task, not a follow-up
message to the original child. In other runtimes use the supported mechanism,
but keep each task packet self-contained. The human/coordinator fixes in-scope
findings and reruns the actual gates.

### 5. Explain the boundaries (4 min)

Fill a short task report. Explain these differences to a partner:

| Concept | What it is | What it does NOT guarantee |
|---|---|---|
| Custom agent | Reusable role/tools definition | Separate session or file isolation |
| Subagent | Parent-delegated task in separate context, returning a report | Automatic full-history/repo-rule inheritance; filesystem isolation |
| Local handoff | Button to change the active agent in the same conversation; default send=false pre-fills | Background delegation or Copilot/app portability |
| Top-level session | Conversation the user independently prompts | Parent/child delegation simply because two chats exist |

Do not enable nested delegation or broad tools just to complete the lab.
More agents are not always better: a tiny edit usually needs a direct request.

## Measurable acceptance and fallback

Coordinator syntax matches the chosen harness. Effective reviewer tools remain
read/search only. The research task includes goal, paths, invariants, report,
and stop; activity shows real delegation **or** explicitly records simulation.
Only priority and its owned test changed for the feature. Six priority checks,
baseline, worked score/reason checks, and a truthful handoff pass.

**No-preview/no-delegation fallback:** run the research prompt in ordinary chat
with read-only tools if available, copy its report into the writer's task, then
perform the implementation/review sequentially. If you cannot restrict tools,
the human performs the read-only review. Record "manual/sequential role boundary",
not "enforced custom subagent". All feature/test outcomes stay the same.

## Hint ladder

1. Closed is an early return. Then base score, ordered additions, level, result.
2. Test 99/100 and 6/7, not just the seeded examples. Test 75/P2 versus85/P1;
   80 cannot be generated by this policy.
3. A reviewer cannot run tests. Let the human/writer execute and attach output.
4. Instructor catch-up: `npm run workshop:apply -- priority`. It installs the
   complete feature and owned test with a backup; rerun gates and explain the rule.
   Complete coordinator profiles are in the instructor guide for recovery.

If tests fail because the agent changed acceptance tests or shared files, preserve
the diff, stop that writer, and restore/reassign safely; do not weaken the gate.

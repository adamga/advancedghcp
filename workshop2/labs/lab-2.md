# Lab 2: Hire a coordinator and build the first feature (priority)

**35 minutes | workshop clock 01:30 - 02:05 | App changes: priority scoring (the first "missing piece")**

## Why this lab exists

**The problem.** Right now every card on the board says `untriaged`. Sam cannot
tell what to work on first. The feature that turns a pile of issues into a
ranked list, the **priority score**, is a placeholder that does nothing.

**A second, bigger problem.** You *could* just ask one agent "build priority".
But look at what that one agent would have to do all at once: learn the scoring
rule, find the edge cases, write the code, write the tests, and then grade its
own work. When one worker does everything, nobody checks the checker.

**The fix.** Split the work the way a good team would:

```text
          You (the human, in charge)
                   |
           Triage Coordinator      <- plans, delegates, writes the code
              |          |
   asks for research     implements
              v          v
     Triage Reviewer     src/features/priority.mjs
     (read-only)         tests/features/priority.test.mjs
```

The coordinator is like a **project lead**: it does not do all the thinking
alone. It sends the read-only reviewer off to *research and report back*, then
uses that report to write the code. At the end, a *fresh* review looks at the
finished work. You stay in charge: you read each report before the next step.

**The scenario.** Sam's rule is simple and written down (see
[the story](../01-the-story.md)). Your job is to get the coordinator to turn
that rule into working code **without inventing anything**, and to prove it
with tests, not with a confident-sounding message.

**What you will have at the end.** Every card shows a real score and `P1`/`P2`/`P3`
badge, the list is ranked, and you have evidence from tests. You will also be
able to explain the difference between a custom agent, a subagent, a handoff,
and a top-level session. That last part is the key concept of the day.

## Words to know

| Word | Plain meaning |
|---|---|
| **Coordinator** | The agent in charge of a task. It delegates and integrates. |
| **Subagent** | A helper the coordinator sends off with a self-contained brief. It works in its own separate "head" and returns a report. |
| **Task packet** | The brief you hand over: goal, files, rules, allowed actions, expected report, when to stop |
| **Gate** | A command that must pass before you call work done (here: `npm run acceptance -- priority`) |
| **Boundary case** | A value right at the edge of a rule (99 vs 100 users). Most bugs hide here. |

## Before you start

- Lab 1 is done, **or** you ran the catch-up: `npm run workshop:apply -- lab1-copilot`
  (or `lab1-local`).
- `npm run check:customizations -- --require-lab1` passes.
- Keep [contracts](../contracts.md) open. The scoring policy is there.
- Still in the same harness you chose in Lab 1. **Do not open `solutions/`.**

**Quick reminder of the rule you are implementing** (full version in the contracts):

```text
Active issue:  base = high 60 | medium 30 | low 10
               + 25 if blocked
               + 10 if affected users >= 100
               +  5 if open 7 or more days
Closed issue:  always score 0, level P3, only reason "closed issue (0)"
Level:         P1 if score >= 80 | P2 if score >= 40 | otherwise P3
```

## Time plan

| Minutes | Step | You will have |
|---|---|---|
| 0-3 | Read this introduction | The team picture and the rule |
| 3-8 | 1. Build the coordinator | A lead agent for your harness |
| 8-15 | 2. Delegate research only | A reviewer's report you can check |
| 15-25 | 3. Implement with the skill | Two changed files and a working score |
| 25-31 | 4. Run the gates and review | Test evidence and a fresh review |
| 31-35 | 5. Explain the boundaries | A clear picture of who did what |

---

## Step 1. Build the coordinator (5 min)

**What.** Create `.github/agents/triage-coordinator.agent.md` for **your**
harness.

**Why.** The coordinator is a new role: it needs to *edit and run* (the reviewer
could not), and it needs to be able to *call* the reviewer. Writing this as a
file, rather than repeating the setup in every chat, makes the role repeatable
and lets a teammate review it like any other code.

The two harnesses spell this slightly differently. **Use only the one you chose
in Lab 1. Do not mix them.**

**Copilot harness / Copilot app (recommended):**

```yaml
---
name: Triage Coordinator
description: Implement an assigned triage feature after bounded read-only research.
target: github-copilot
tools: ['read', 'search', 'edit', 'execute', 'agent']
skills: ['triage-policy']
---
```

**VS Code Local harness (only if you chose Local):**

```yaml
---
name: Triage Coordinator
description: Implement an assigned triage feature after bounded read-only research.
target: vscode
tools: ['read', 'search', 'edit', 'execute', 'agent']
agents: ['Triage Reviewer']
---
```

What each line means:

| Line | Meaning |
|---|---|
| `tools: [...'agent']` | It may read, search, edit, run commands, **and delegate to another agent**. The `agent` tool is what makes it a coordinator. |
| `skills: ['triage-policy']` (Copilot only) | Pre-loads the skill you wrote in Lab 1 |
| `agents: ['Triage Reviewer']` (Local only) | A **short list of who it may delegate to**. Anyone not named is refused. |

Why the difference? The two engines have different rulebooks. Copilot has
*native* delegation and can preload skills; it does not have the Local
allowlist. In Copilot, writing "only use the Triage Reviewer" in the body is an
**advisory request**, not an enforced list. Remember that distinction; it comes
up again in Step 5.

Below the second `---`, write the **body**: your coordinator's standing
instructions. Ask Copilot to draft it:

**Prompt:**

```text
Create .github/agents/triage-coordinator.agent.md using EXACTLY the frontmatter
for my chosen harness shown above. Write a short body that tells the coordinator to:
restate ownership and the contract; obtain a read-only specialist report first;
use the triage-policy skill explicitly; edit only the files the task names;
run the named acceptance gate; request a fresh review; report real evidence
(RAN vs NOT RUN) and stop. Do not add tools, fields, or other files.
```

*Why it is written this way:* it says **EXACTLY** (so the agent does not "improve"
the tool list), and the body describes a **process** (research, build, verify,
report) rather than vague hopes.

**You should see.**

- A new `.github/agents/triage-coordinator.agent.md` with your harness's fields.
- `npm run check:customizations -- --require-lab1` still passes.
- Start a **fresh chat**; **Triage Coordinator** now appears in the agent picker.

**If not.**

| Symptom | Fix |
|---|---|
| Both `skills` and `agents` appear | You mixed the two. Delete the one that does not belong to your harness. |
| It does not appear in the picker | Fresh chat, correct folder (`.github/agents/`), ends with `.agent.md`. |
| `agent/runSubagent` is in a Copilot file | Remove it. That reference is a Local-harness detail. Copilot uses native delegation. |

> **Reflect.** Why do we *not* give the coordinator permission to do absolutely
> everything "just in case"? (Think: the more it can do, the more a mistake can break.)

---

## Step 2. Delegate research only (7 min)

**What.** Select the Triage Coordinator and have it ask the Triage Reviewer for a
**read-only research report**. Nothing is built yet.

**Why.** Researching before building is cheaper than fixing afterwards. The
reviewer cannot change anything, so you get an *independent* reading of the
rules. If the reviewer and the coordinator later disagree, you have found a
misunderstanding **before** it became code.

There is one crucial fact to understand here:

> **A subagent starts with an empty head.** It does not see your conversation, and
> in some engines it does not even see your repository instructions. Whatever it
> needs to know must be **written into the brief**.

That is why the brief below looks long. Each line closes a gap the helper would
otherwise fill with guesses. This brief is called a **task packet**:

| Packet part | Why it is there |
|---|---|
| Goal | So it knows "research", not "build" |
| Files to read (and files *not* to read) | So it does not wander, and does not copy the answer from `solutions/` |
| Rules that always apply | The helper may not have inherited the repo instructions |
| Allowed actions | Read/search only; no edits, terminal, web, or delegation |
| Expected report | So the answer is complete and comparable |
| Stop | So it ends instead of carrying on to implement |

**How.** Select **Triage Coordinator** and send:

```text
Use Triage Reviewer as a read-only specialist for ONE policy research task.
Goal: derive priority implementation rules and boundary cases, not code changes.
Read workshop2/contracts.md, src/data/issues.mjs, src/features/priority.mjs,
.github/skills/triage-policy/SKILL.md and its references/policy.md.
Do not read workshop2/solutions/.
Explicit repo invariants: Node>=22 built-ins only, synthetic fixtures, no input
mutation, no network/dependencies, no shared server/UI/package/fixture edits.
Reviewer allowed actions: read/search only; no edits, terminal, web, or delegation.
Expected report: objective; exact contract with file/line evidence; ISS-101,
ISS-102 and closed ISS-105 worked cases; 99/100 users and 6/7 days; reason ordering;
commands to validate marked NOT RUN; uncertainties; stop after this report.
Do not implement yet. Return the specialist report for my inspection.
```

Then **look for proof that delegation really happened**: a delegated tool call
or a visible Triage Reviewer entry in the chat activity. In the VS Code Agents
window, the subagent appears as a separate chat with a **lock icon**. That lock
only means *you cannot type into that child chat*. It does not mean the child is
in a security sandbox.

**You should see.** A report that, in its own words:

- ISS-101 = **100 / P1** (high 60 + blocked 25 + 100+ users 10 + 7+ days 5)
- ISS-102 = **55 / P2** (medium 30 + blocked 25)
- ISS-105 = **0 / P3**, because it is closed, even though it is high-impact and blocked
- the **99 vs 100 users** and **6 vs 7 days** edges, and the order of the reasons
- commands to run, each marked **NOT RUN**
- file and line citations, and no files edited

**If not.**

| Symptom | Fix |
|---|---|
| No visible delegation | Use the **sequential fallback**: run the same prompt in ordinary chat with read-only tools (or have a human act as the reviewer), paste the report into Step 3, and record "manual/sequential role boundary" (not "enforced subagent"). The learning outcome is identical. |
| The reviewer started editing files | Stop it. Check the reviewer still has only `read` and `search`. Never fix by granting more access. |
| The report says "I ran the tests" | A read-only role cannot. Reject that and ask for NOT RUN labels. Wrongly claimed evidence is worse than no evidence. |
| The numbers are wrong | Compare with [contracts](../contracts.md); correct before using the report. |

> **Reflect.** The brief repeated rules that are already in the repo
> instructions. Why was repeating them worth it?

---

## Step 3. Implement priority using the skill (10 min)

**What.** Ask the **coordinator** (not the reviewer) to write the feature and
its test, touching **only two files**.

**Why.** Telling the agent *exactly which files it owns* is the main defense
against a helpful agent "improving" something nearby. With only two files in
play, the diff is small enough for you to review in minutes. Naming the skill
means the exact numbers come from the policy, not from the agent's imagination.

The two files:

```text
src/features/priority.mjs            <- the scoring function
tests/features/priority.test.mjs     <- the tests, which you also add
```

**How.** Read the specialist report first, then send:

```text
Use the triage-policy skill and accepted specialist findings to implement
prioritizeIssue(issue) in src/features/priority.mjs and create
tests/features/priority.test.mjs. Those are the only editable app/test paths.
Return fresh {level,score,reasons}; apply the closed override before additions.
Use exact rule/reason text from workshop2/contracts.md. Throw a TypeError whose
message starts with "Unknown impact" for any active impact other than
high/medium/low, even a name like "constructor". Cover user and age
boundaries, closed override, non-mutation, and the unknown impact in the owned test.
Do not change exports, shared wiring, fixtures, package files, acceptance checks,
or other features. Do not read instructor solutions.
Run npm run acceptance -- priority and npm test if execution is authorized.
If blocked, stop editing and report exact NOT RUN commands for the human.
Stop after reporting changed paths and evidence; no pushes or PRs.
```

Why each line matters:

| Line in the prompt | Reason |
|---|---|
| "Use the triage-policy skill" | Pulls the exact numbers from your Lab 1 recipe |
| "only editable paths" | Fences the change to two files |
| "closed override *before* additions" | A closed issue must be 0 even if high-impact and blocked. Checking it first avoids adding points and having to undo them. |
| "Return fresh {level,score,reasons}" | A new object each time. Changing the issue passed in would be a hidden bug. |
| "Throw a TypeError ... Unknown impact" | The contract says bad input must **fail loudly**. Without this line a typo such as `"urgent"` would quietly produce a wrong score, and the acceptance check looks for the error. |
| "Do not read instructor solutions" | You are here to build it, not copy it |
| "If blocked, stop and report NOT RUN" | Honest failure beats pretend success |

Now check **whether the skill was really used**. Look in the activity for the
skill being read. If it was not loaded automatically, attach the installed
`SKILL.md` and `policy.md` to the conversation and write down "manual fallback".
(The Local harness has no `skills` field; it relies on discovery or attaching.)
**A loaded skill never adds permissions**; it only supplies instructions.

**You should see.**

- Compared with before this step, exactly two files changed (check with `git status --short -uall`; files from Lab 1 may also be listed, so ignore those): `src/features/priority.mjs` and `tests/features/priority.test.mjs`.
- `priority.mjs` returns the three fields, checks `closed` first, uses `>=` for the 100-user and 7-day thresholds, and throws a `TypeError` for an unknown impact.
- The tests include **99/100** and **6/7** boundaries, a non-mutation check, and the unknown-impact error.

**If not.**

| Symptom | Fix |
|---|---|
| More than two files changed | Stop. Look at each extra file with `git diff -- <file>`. If it holds only the agent's stray edit and none of your own work, undo that one file with `git restore <file>` (for a brand-new file, delete just that file). `git restore` cannot be undone, so if you are unsure, ask your facilitator first. Then re-prompt and restate the fence. |
| Agent edited `acceptance/` tests | Preserve the diff, stop that writer, and restore. **Never weaken the gate.** |
| It could not run commands | Fine. It should list them as NOT RUN, and *you* run them in Step 4. |
| Ran out of time | Catch-up: `npm run workshop:apply -- priority` (it backs up first). Read the result and be ready to explain it. |

> **Reflect.** What went wrong in the old way of working that this "two files
> only" fence prevents?

---

## Step 4. Run the gates and request a fresh review (6 min)

**What.** Prove the feature works with commands, then get an independent review.

**Why.** An agent saying "all tests pass" is a *claim*. Running the command
yourself produces *evidence*. The review is a separate pair of eyes, but
reviewers cannot run tests, so **you** run them.

**How.** In a terminal:

```text
npm run acceptance -- priority
npm test
```

Then restart the app (there is no file watcher: press `Ctrl+C`, run `npm start`
again, refresh the page).

Next, request a **new** review. Because Local subagents are stateless, a second
review is a **new task**, not a follow-up message to the first reviewer.
Re-supply the context:

```text
Use Triage Reviewer to read src/features/priority.mjs,
tests/features/priority.test.mjs and workshop2/contracts.md.
Check closed override, inclusive 100-user/7-day boundaries, exact reason order,
fresh outputs, and no shared-file changes. Read/search only; no commands or edits.
Return file/line findings, missing cases, and NOT RUN suggested checks. Stop.
```

You (or the coordinator) fix any in-scope finding and rerun the gates.

**You should see.**

- Acceptance ends with `# tests 6`, `# pass 6`, `# fail 0`.
- `npm test` shows `# fail 0`. The total is 14 plus the tests *you* added. (If you
  used the catch-up, it is **15**.)
- In the browser: cards now show real badges. **ISS-101** is at the top, **P1**,
  with four "Why:" reasons. **ISS-105** (closed) is **P3** with only
  `closed issue (0)`, even though it is high-impact and blocked.
- The order is: 101, 102, 104, 106, 103, 107, then the two closed ones (105, 108).
- Summary and search are still **not** done; that is correct for now.

**If not.**

| Symptom | Fix |
|---|---|
| Acceptance shows `+ actual - expected` with `null`/`untriaged` | The starter file is still in place. Check you saved your edit and that the agent edited the right file. |
| Browser still shows `untriaged` | You did not restart the server. `Ctrl+C`, `npm start`, refresh. |
| One boundary test fails | Check `>=` vs `>`. The policy says "100 or more" and "7 or more". Also remember 80 is unreachable, so we test 75 (P2) and 85 (P1). |
| Reviewer says "tests pass" | It cannot know. Ask for NOT RUN labels. |

> **Reflect.** The reviewer found nothing, or found something. Either way, what
> did a *fresh* review give you that the coordinator's self-check could not?

---

## Step 5. Explain who did what (4 min)

**What.** Tell a neighbor, in your own words, how these four things differ.

**Why.** People often use these words interchangeably, which leads to wrong
expectations, such as assuming a subagent is sandboxed. Getting the vocabulary
right now makes the later labs and your real projects safer.

| Concept | What it is | What it does **not** guarantee |
|---|---|---|
| **Custom agent** | A reusable role + tool list in a file | A separate session or file isolation |
| **Subagent** | A task the parent hands off to a helper with its own context; it returns a report | The helper inheriting your history or repo rules, or being isolated from the filesystem |
| **Local handoff** | A button that switches the active agent in the *same* conversation | Background delegation, or portability to the Copilot app |
| **Top-level session** | A chat *you* prompt independently | Being a parent/child just because two chats exist |

Two more questions to talk through:

- When is it better to **skip** delegation entirely? (A tiny, obvious edit. More agents are not always better.)
- What was **enforced by tools** (the reviewer cannot edit) and what was only
  **advisory** (agreements in prose)?

Do not turn on nested delegation or broaden tools to "make it work" in this lab.

**You should see.** You can explain the table to someone without reading it.

**If not.** If one row still feels fuzzy, reread its right-hand column ("does
**not** guarantee"). That column is the part people most often get wrong. Ask
your facilitator for an example from your own session.

---

## Success checklist

- [ ] The coordinator uses **your** harness's fields only; the reviewer is still read/search only.
- [ ] The research task had a goal, files, rules, allowed actions, expected report, and stop, and you saw real delegation *or* wrote down "manual/sequential".
- [ ] Only `src/features/priority.mjs` and `tests/features/priority.test.mjs` changed.
- [ ] `npm run acceptance -- priority` shows 6 passing and `npm test` shows 0 failing.
- [ ] The browser shows ISS-101 = P1 with four reasons, ISS-105 = P3 with only the closed reason.
- [ ] You recorded whether the skill truly loaded, honestly.

## Reflect (one sentence each)

1. Why did we ask the reviewer to *research only* before any code was written?
2. Why is a task packet so detailed? What would break if it were one sentence?
3. Why is "all tests pass" from an agent weaker than the output of a command you ran?

## Hint ladder

1. Closed is an **early return**. Then the base score, then ordered additions,
   then the level.
2. Test the **edges**, not only the examples: 99/100 users and 6/7 days. Test 75
   (P2) versus 85 (P1); 80 cannot occur.
3. A reviewer cannot run tests. The human or the writer runs them and shares
   the output.
4. **Instructor catch-up:** `npm run workshop:apply -- priority`. It installs the
   finished feature and owned test (with a backup). Rerun the gates and explain
   the rule aloud. Complete coordinator profiles are in the
   [instructor guide](../instructor-guide.md).

If tests fail because the agent changed acceptance tests or shared files,
preserve the diff, stop that writer, restore (see [restore](../restore.md)),
and reassign. **Do not weaken the gate.**

**Fallback if delegation is unavailable:** run the research prompt in ordinary
chat with read-only tools, paste the report into the writer's task, then do the
build and review one after the other. If you cannot restrict tools, a human does
the read-only review. Label it "manual/sequential role boundary".

## Challenge (optional)

- Ask the reviewer: "Which inputs does the contract say must fail, and does a
  test prove each one?" Check its answer against `workshop2/contracts.md`.
- Add a one-sentence comment on the *why* of the closed-first rule. Keep it short.

## Where we are going next

The board now ranks issues. But Sam still cannot *search* it or see a *summary*.
In [Lab 3](lab-3.md) you build both **at the same time**, in the same
repository, so that two workers do not trample each other. That is the
orchestration problem at the heart of working with multiple agents.

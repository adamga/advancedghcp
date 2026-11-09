# Facilitator guide and complete answer key (workshop2)

**Audience:** people who just learned the basics of agents and skills.
**Time:** exactly 60 minutes presentation/demo + 120 minutes hands-on.
**Hands-on:** 30, 35, 40, and 15 minutes. There is no extra break outside those allocations.

This guide has two jobs: help you **teach the why** (not just the what), and give
you the **answer key** when a participant is stuck. Read the first two sections
before the day. Use the rest as a reference.

## Contents

1. [What workshop2 changed](#what-workshop2-changed)
2. [How to teach the why](#how-to-teach-the-why)
3. [Presentation and standalone lesson](#presentation-and-standalone-lesson)
4. [Timed slide map](#timed-slide-map---no-extra-minutes)
5. [Before class](#before-class)
6. [Presentation-to-lab bridge](#presentation-to-lab-bridge)
7. [Live pacing and rescue triggers](#live-pacing-and-rescue-triggers)
8. [Answer keys: Lab 1](#lab-1-answer-key), [Lab 2](#lab-2-answer-key), [Lab 3](#lab-3-answer-key), [Lab 4](#lab-4-answer-key)
9. [Rehearse and return to starter](#rehearse-the-full-answers-and-return-to-starter)
10. [Debrief rubric](#debrief-rubric)

## What workshop2 changed

Edition 1 gave participants the *what* in compact form. Workshop2 keeps the **same
app, the same frozen contracts, the same timings, and the same answers**, and adds
the **background, explanation, and reasoning** that make it understandable to people
of every level.

| Material | What it does | Who reads it, and when |
|---|---|---|
| [README](README.md) | Front door and route through the day | Everyone, first |
| [01 The story](01-the-story.md) | The app in plain words; what is missing; why it matters; what the labs fix | Everyone, **before the day** |
| [02 Concepts](02-concepts.md) | Every term explained with an everyday analogy | Everyone, before or during Lab 1 |
| [Preflight](preflight.md) | Setup with "what / why / you should see / if not" | Everyone, **before the day** (15-25 min) |
| [Labs 1-4](labs/lab-1.md) | Step-by-step labs; every step states *what, why, how, what you should see, what to do if not, and a reflection* | Participants, in the labs |
| [Contracts](contracts.md) | The authoritative reference for inputs, outputs, ownership, and HTTP | When a lab says "check the contract" |
| [Restore](restore.md) | Undo toolkit | Before Lab 1 (skim), and when needed |
| [Troubleshooting](troubleshooting.md) | Symptom, cause (why), safe action | When stuck |
| [Extensions](extensions.md) | Optional next steps after minute 180 | Early finishers |
| This guide | Facilitation, timing, answer keys | Facilitators only |

The original edition-1 `workshop/` folder was replaced by `workshop2/`. It remains
in the repository's git history and in the first pull request.

## How to teach the why

Every lab step follows the same six-part pattern. **Teach participants to look for
it**, and it becomes a habit they can use on any future task:

| Part | The question it answers |
|---|---|
| **What** | What am I doing right now? |
| **Why** | Why does this step exist? What goes wrong without it? |
| **How** | The exact actions to take |
| **You should see** | How will I *know* it worked? (real output, copied from a real run) |
| **If not** | What do I do when it did not? |
| **Reflect** | What did I just learn that applies beyond this app? |

**Three habits to model out loud, every time.**

1. **Say the purpose before the click.** "We are making the reviewer read-only
   *so that* a review cannot quietly change the code."
2. **Ask for a prediction.** Before running a command: "What do you expect to see?"
   Then compare. Being wrong is useful; it exposes a wrong mental model.
3. **Ask for evidence, not feelings.** "How do you know?" should be answered with
   a command and its result, or an honest `NOT RUN`.

**The one-sentence "why" for each lab.** If you only have time to say one thing:

| Lab | The why in one sentence |
|---|---|
| 1 | Rules, a role, and a recipe turn a general assistant into a *specialist that knows how your team works*. |
| 2 | Delegation works when the task is **bounded, read-only first, and checked** afterward; "done" is a claim, not proof. |
| 3 | Agents collide because they share **files, ports, and the git index**, not because they share a conversation. Prevent it with **ownership, a frozen contract, one integrator, and gates**. |
| 4 | A result is only as good as its **evidence**; an honest "not ready" beats a confident "done." |

**What to watch for when walking the room.**

- Someone skipping the **You should see** block. Ask them to read it aloud and compare.
- Someone treating a delegated answer as fact. Ask: "Which command proves that?"
- Someone widening a tool list "to get unstuck." Ask: "What would that let the
  reviewer do that you do not want?"

## Presentation and standalone lesson

Use the [42-slide editable PowerPoint](../deliverables/advanced-github-copilot-workshop.pptx)
and [printable PDF](../deliverables/advanced-github-copilot-workshop.pdf).
The supplied template's near-black/Arial/white/cyan/purple-blue language is adapted
with original workshop content; the original reference deck is not redistributed.

The [animated Coral MP4](../deliverables/advanced-github-copilot-explainer.mp4)
is **separate self-paced pre/post material**, not an extra segment in the live
180-minute agenda. It uses Microsoft Foundry `gpt-audio-1.5`, playful Coral voice,
24 fps explanatory motion graphics, on-screen captions and 42 embedded chapters.
Its [simpler video script](../deliverables/video-script.md) covers the same topics
through 126 teaching beats. It is not a recording of live Copilot UI.
Full slide speaker notes remain a long-form teaching reference,
**not text to read verbatim within the 60-minute talk/demo block**.

> **The video explains concepts; the lab steps live in the written labs.** The
> video was produced before workshop2's lab rewrite and covers the same concepts
> (agents, skills, delegation, safe orchestration). Where the video and a lab
> differ in detail, **the written lab in `workshop2/labs/` is the source of truth.**

Accessible and navigation editions:
[SRT](../deliverables/advanced-github-copilot-explainer.srt),
[WebVTT](../deliverables/advanced-github-copilot-explainer.vtt),
[transcript](../deliverables/explainer-transcript.md),
[audio-only](../deliverables/explainer-audio.m4a),
[chapter timestamps](../deliverables/video-chapters.txt), and
[timeline](../deliverables/video-timeline.json).
The [15-source ledger](../deliverables/source-ledger.md) records official facts
checked November 7, 2026 and their product/policy/preview limits. The workshop2
labs re-checked the key VS Code and Copilot facts on November 9, 2026.

Packaging/verification records:
[slide contact sheet](../deliverables/slide-contact-sheet.jpg),
[media verification](../deliverables/media-verification.json),
[text-fit adjustments](../deliverables/text-fit-adjustments.json), and
[content manifest](../deliverables/workshop-manifest.json).
The [narration manifest](../deliverables/narration-manifest.json) records verified
source passages and actual audio chunk timings.
The media verification covers complete audiovisual decode, 42 chapters,
caption coverage, actual illustration motion in every chapter, measured cadence,
and quieter encoded audio with safe peak headroom.
Use the [short preview](../deliverables/animated-explainer-preview.mp4) to check
laptop playback before an event. Hardware volume remains under the listener's control.
[Optional media rebuild instructions](../media/README.md) are outside attendee
preflight and all timed labs; the app remains zero-dependency Node.

## Timed slide map - no extra minutes

| Live clock | Slides | Talk/demo allocation | What to do |
|---|---|---|---|
| 00:00-00:15 | 1-10 | 11 min talk + 4 min app demo | Set expectations; **tell the app story (see [The story](01-the-story.md))**; show starter, four seams, and baseline |
| 00:15-00:35 | 11-23 | 10 min talk + 5 min demo1 + 5 min demo2 | Custom agent/skill, then bounded reviewer-to-writer delegation |
| 00:35-01:00 | 24-35 | 19 min talk + 6 min demo3 | Same-repo ownership/contracts, research-first integration, limits/fallback |
| Within 01:00-03:00 | 36-39 | Included in the four labs, not added | Lab launch/checkpoint/debrief prompts |
| Within 02:45-03:00 | 40-41 | Included in Lab4's 15 min | Recovery, evidence handoff, retrospective/closing |
| Reference whenever needed | 42 | No separate time allocation | Official-source pointers |

At minute 60 transition directly to the 30/35/40/15-minute lab schedule below.
Do not play the complete standalone video during the live agenda or turn full
narration notes into additional presentation time.

**When you present the app (slides 1-10),** use the three-sentence version from
[The story](01-the-story.md): what the app is (an issue triage board), what is
missing (four features that are stubs), and why it matters (they are four real
patterns: rules, delegation, safe parallel work, and honest evidence).

## Before class

**Two days before:** make sure everyone has done [preflight](preflight.md) and,
ideally, read [The story](01-the-story.md). People who did get far more from the labs.

**Check how people get the code.** Until the workshop pull request is merged, the
repository's default branch (`main`) is empty, so a plain `git clone` gives no
files. Tell attendees to use the `-b adamga-workshop-app-and-hands-on-labs`
command in [preflight](preflight.md), or merge the PR first. Keep an offline source ZIP
ready for people whose network blocks Git.

**Before you present,** use a clean starter checkout. Run:

```text
npm test
npm run smoke
npm run check:customizations
npm run verify:solutions
```

Expected starter baseline 14 tests; isolated solutions 6 tests each for priority,
search, summary, handoff plus 2 integration tests (26 total). No dependency install.
The ordinary customization check validates 8 inactive instructor profiles and
their skill, and reports 0 active exercise agents/skills in a fresh clone.
Acceptance against starter intentionally fails; never demonstrate "all green"
by completing all features before participants start.

Open the starter board at a narrow width and keyboard-tab through controls.
Check installed product availability, effective tools, and your account's
quota/policy beforehand. Have a manual/sequential route ready. Keep the Local
and Copilot profiles clearly separated; new VS Code sessions default to Copilot.
No Projects preview, marketplace, connector, experimental computer use, nested
subagent setting, MCP, cloud agent, or Azure service is needed.

Show the completed board **without changing starter files**:

```text
npm run start:solutions
```

The ordinary `npm start` uses participant source. `start:solutions` imports the
separate instructor modules into the same loopback HTTP server; it does not copy
or overwrite any app/test/customization. For side-by-side demos use separate
terminals and different ports. Windows: `$env:PORT = '3001'; npm run start:solutions`.
macOS/Linux: `PORT=3001 npm run start:solutions`. Keep only your own servers running.

Alternatively prepare a separate demo folder and install answers there with
`workshop:apply`; do not mutate attendee source behind the scenes. Worktrees/folders
still need distinct ports.

## Presentation-to-lab bridge

At minute 60, everyone should be able to distinguish:

| Concept | Beginner explanation | Boundary |
|---|---|---|
| Repository instructions | Shared rules for how this repo is worked on | Guidance; not automatic inheritance in every subagent |
| Custom agent | Reusable role with instructions and tools | Definition, not a separate session |
| Skill | Reusable procedure with optional reference/script resources | Context, not additional tool permission |
| Subagent | A delegated bounded task with separate context and report | Context isolation, not filesystem isolation |
| Local handoff | Change active role in the same conversation | Local-only; not delegation |
| Top-level session | A conversation the user prompts independently | Not a child merely because another chat exists |
| Worktree | Different working files/index for a branch | Does not eliminate shared-repo integration or port/service conflicts |

The participants' written version of this table is in [Concepts](02-concepts.md),
with an everyday analogy for each term.

Say: "We will use one small app and make ownership/contracts explicit. Two
read-only research streams followed by one writer is already useful orchestration."

## Live pacing and rescue triggers

Each lab opens with a short reading block and then five timed steps. The clock below
matches the **time plan table at the top of each lab**.

| Clock | Lab step | If a participant is behind |
|---|---|---|
| 01:00 | Lab 1 intro (3 min): rules, role, recipe | Use the analogy table; do not start Step 1 until it lands |
| 01:03 | Step 1: look before you leap (4 min) | Use the ordinary Chat view if the Agents window is missing |
| 01:07 | Step 2: write two rules (5 min) | Offer the two acceptable rules (answer key below) |
| 01:12 | Step 3: finish the reviewer (7 min) | Offer shared read/search profile fields; stress **read-only** |
| 01:19 | Step 4: finish the skill (7 min) | Use contract policy, not invented business rules |
| 01:26 | Step 5: check and try twice (4 min) | Complete answer installer only **after** explaining each missing piece |
| 01:30 | Lab 2 intro (3 min) | Draw the team picture on a board |
| 01:33 | Step 1: build the coordinator (5 min) | Show the harness-correct profile; keep Local and Copilot separate |
| 01:38 | Step 2: delegate research only (7 min) | Paste the complete research packet; preserve read-only tools |
| 01:45 | Step 3: implement priority (10 min) | Show the closed early-return hint |
| 01:55 | Step 4: gates and fresh review (6 min) | Apply the priority answer if needed; still require explanation and evidence |
| 02:01 | Step 5: who did what (4 min) | Use the four-row distinction table; no UI scavenger hunt |
| 02:05 | Lab 3 intro (3 min) | Default to single-writer Route A |
| 02:08 | Step 1: contract and ownership (5 min) | Provide the board template |
| 02:13 | Step 2: two research packets (7 min) | Provide A/B task packets; serialize if product availability differs |
| 02:20 | Step 3: implement under one route (12 min) | Separate feature installers rescue A and B independently |
| 02:32 | Step 4: release, integrate, validate (8 min) | Workers stop first; integrator gates and visible counts |
| 02:40 | Step 5: limits and alternatives (5 min) | Explain tradeoffs; do not spend class configuring worktrees |
| 02:45 | Lab 4 intro (1 min) and Step 1: export (3 min) | Show the filter-then-map hint |
| 02:49 | Step 2: final gates and download (4 min) | Apply handoff if needed; do not skip evidence checks |
| 02:53 | Step 3: one integrated review (3 min) | Reviewer stays read-only; unrun commands are `NOT RUN` |
| 02:56 | Step 4: truthful report (2 min) | Any unresolved failure is "not ready" |
| 02:58 | Step 5: retrospective (2 min) | One direct-task lesson and one boundary |
| 03:00 | Stop | Extensions are outside this agenda |

The small check-in/stretch moments live inside each lab checkpoint. Do not add
a surprise install, product migration, cloud setup, or account-policy exercise.

## Lab 1 answer key

Two acceptable repository-rule additions:

```markdown
For priority explanations, cite the installed triage-policy reference and give
one closed-issue case plus one exact boundary case.

In every handoff, distinguish commands actually executed from checks inspected
or suggested; mark unavailable execution NOT RUN with the responsible executor.
```

A complete reviewer must define scope, inputs, read/search only, findings with
file/line evidence, NOT RUN commands, and stop. It must not "borrow" execution
from a skill. The complete profiles are:

- [Local reviewer](solutions/customizations/local/triage-reviewer.agent.md)
- [Copilot/app reviewer](solutions/customizations/copilot/triage-reviewer.agent.md)

The real skill answer includes
[SKILL.md](solutions/customizations/triage-policy/SKILL.md),
[policy reference](solutions/customizations/triage-policy/references/policy.md),
and [fixture inspection script](solutions/customizations/triage-policy/scripts/inspect-fixtures.mjs).
The script reads only synthetic records and prints a schema check.
Folder name/metadata must agree, description must be specific, and both
resources must be referenced. Automatic selection is an observation, not a
pass/fail promise. Explicitly loaded/manual-context fallback is valid if labeled.

Catch-up for the chosen surface:

```text
npm run workshop:apply -- lab1-copilot
npm run check:customizations -- --require-lab1
```

Use `lab1-local` only with an explicitly selected Local session. Add the two
instruction rules manually and inspect runtime tools; the installer does not
substitute for either learning checkpoint. Save its backup ID.

**Why this lab matters (say it out loud).** Participants just learned the three
building blocks. The point is that each one has a *different job*: **rules** apply
always, a **role** is a specialist you can call, a **recipe** is a procedure loaded
when needed. The read-only reviewer teaches the habit of *limiting what an agent
can do* so that a review cannot silently become a change.

## Lab 2 answer key

Complete coordinator profiles:
[Local](solutions/customizations/local/triage-coordinator.agent.md) or
[Copilot/app](solutions/customizations/copilot/triage-coordinator.agent.md).
Local `agents` is an exact case-sensitive named-worker allowlist; explicit list
entries can override a worker's disable-model-invocation setting. Copilot does not
accept/forward that field. Copilot `skills` can preload available enabled skills;
Local uses explicit discovery/invocation. `target` changes interpretation, not runtime.

Repository instructions are not included in custom CLI subagents by default.
Task packets must explicitly pass constraints, paths, output, and stop.
Do not rely on `include-custom-instructions`, `strict-tools-list`, or other
conversion-sensitive fields to establish runtime restrictions. Check activity.
Local invocations are stateless; the reviewer cannot receive a later follow-up
as the same task. Further review needs a new complete invocation.

[Complete priority implementation](solutions/features/priority.mjs) and
[owned priority test](solutions/tests/priority.test.mjs).
Owned test answers are designed to be copied to `tests/features/`; their relative
imports refer to that destination, not direct execution in the answer folder.

| Issue | Arithmetic | Expected |
|---|---|---|
| ISS-101 | high 60 + blocked 25 + users 10 + age 5 | 100 / P1; four ordered reasons |
| ISS-102 | medium 30 + blocked 25 | 55 / P2; impact then blocked |
| ISS-103 | low 10 + age 5 | 15 / P3 |
| ISS-104 | medium 30 + users 10 | 40 / P2 |
| ISS-105 | closed override | 0 / P3; sole closed reason |
| ISS-106 | medium 30 + age 5 | 35 / P3 |
| ISS-107 | low 10 | 10 / P3 |
| ISS-108 | closed override | 0 / P3 |

P1 threshold >= 80, P2 >= 40. Nearest reachable P1 boundary values are 75/P2 and 85/P1:
do not invent an 80 fixture. Exact 99/100-user and 6/7-day checks matter.
Show why a closed high-impact blocked issue must short-circuit first.

Catch-up: `npm run workshop:apply -- priority`; validate with
`npm run acceptance -- priority` (6) and `npm test` (15).
Review common failures: closed handled last, > rather than >=, unordered reasons,
input mutation, or "sorting" implemented in the wrong shared file.
[Troubleshooting](troubleshooting.md#priority-lab-2) lists the symptom for each.

**Why this lab matters.** Delegation is not "ask another agent." It is *a bounded
task packet* (goal, context, files, output, stop) to a *read-only* specialist,
followed by *your own checks*. The scoring rule is deliberately small so attention
stays on the process, and the closed-issue override is the classic place where an
agent's confident answer is wrong.

## Lab 3 answer key

Recommended route: read-only A/B research, then one integration writer. Optional
concurrent write route uses disjoint feature/test ownership and read/search/edit
workers without terminal/Git/delegation. Their ownership remains advisory:
an edit tool is not a path sandbox.

Complete workers:
[Local search](solutions/customizations/local/search-worker.agent.md),
[Local summary](solutions/customizations/local/summary-worker.agent.md),
[Copilot search](solutions/customizations/copilot/search-worker.agent.md),
[Copilot summary](solutions/customizations/copilot/summary-worker.agent.md).
Installer `npm run workshop:apply -- agents-local` or `agents-copilot` copies the
four complete profiles for the chosen harness (**Triage Reviewer, Triage
Coordinator, Search Worker and Summary Worker**, not only the two workers) plus
the skill, for demo/catch-up. It backs up current customizations and overwrites
your attendees' Lab 1 and Lab 2 profiles with the complete versions. If delegating Local workers, update the coordinator allowlist
and body **before** freezing work. Do not edit this shared config mid-flight.

Answers:
[search](solutions/features/search.mjs) and
[search test](solutions/tests/search.test.mjs);
[summary](solutions/features/summary.mjs) and
[summary test](solutions/tests/summary.test.mjs).
Search uses trimmed whitespace tokens, literal lowercase text, and every-token
matching. It returns new arrays with existing input objects/order. Summary uses
only the passed visible subset; active = not closed; active blocked excludes
closed blocked. Categories include closed records and have sorted keys.

| Query | Visible IDs | Summary total/active/blocked | Category counts |
|---|---|---|---|
| empty | all 8 | 8/6/2 | accessibility 2, payments 2, reporting 2, search 2 |
| PAYMENTS | ISS-101, ISS-105 | 2/1/1 | payments 2 |
| KEYBOARD accessibility | ISS-102 | 1/1/1 | accessibility 1 |
| keyboard payments | none | 0/0/0 | {} |
| .* | none | 0/0/0 | {} |

No shared server/UI/package edit should be needed. A/B do not depend on one
another. Each owns a separate test; the integrator validates combined HTTP/UI
observations after both stop. Task-board leases and CODEOWNERS are advisory/review
routing; they do not enforce ownership. Shared Git index/branch and processes/
ports remain potential race points even with disjoint source files.

Catch-up each task separately: `workshop:apply -- search`, then
`workshop:apply -- summary`; six acceptance tests per task, baseline and smoke.
Run `npm run verify:solutions` in a clean starter to prove the isolated complete
answers without touching app source.

**Why this lab matters.** This is the heart of the workshop. Collisions come from
**shared files, shared ports, and the shared git index**, *not* from sharing a
conversation. The four techniques (**ownership, frozen contract, one integrator,
gates**) work in *any* tool. Worktrees are one useful layer, not the whole answer,
and they do not isolate ports, network, or secrets. Make participants say which
layer protects against which problem.

### Concrete optional worktree rehearsal

This is an alternative demonstration within the final discussion, or a later
extension, not required setup for the 40-minute lab. Begin from a clean committed
checkpoint; choose **unused branch names and destination folders**. One integrator
owns these operations. Never run a branch switch or staging concurrently with workers.

Windows PowerShell:

```powershell
git --no-pager status --short
git worktree add -b lab-search ..\advancedghcp-search
git worktree add -b lab-summary ..\advancedghcp-summary
```

macOS/Linux:

```bash
git --no-pager status --short
git worktree add -b lab-search ../advancedghcp-search
git worktree add -b lab-summary ../advancedghcp-summary
```

In each task directory implement only owned files, run its acceptance and
baseline, and commit only those paths. Give A PORT 3001 and B PORT 3002 if serving
simultaneously. Worker test files and contracts are already available.

Windows task A example:

```powershell
Set-Location ..\advancedghcp-search
npm run acceptance -- search
git add -- src\features\search.mjs tests\features\search.test.mjs
git commit -m "Implement search task"
git --no-pager log -1 --format=%H
```

macOS/Linux task A example:

```bash
cd ../advancedghcp-search
npm run acceptance -- search
git add -- src/features/search.mjs tests/features/search.test.mjs
git commit -m "Implement search task"
git --no-pager log -1 --format=%H
```

Repeat with summary-owned paths in B. Record both actual commit hashes. Back in
the clean integration checkout, the integrator creates a new integration branch,
then cherry-picks the two reviewed commits:

```text
git switch -c lab-integration
git cherry-pick <actual-search-commit>
git cherry-pick <actual-summary-commit>
npm run acceptance -- search
npm run acceptance -- summary
npm test
npm run smoke
```

Replace placeholders with actual hashes. A/B are independent, so either order
works here; changes with dependencies must integrate in dependency order.
If conflicts occur, preserve context and let the single integrator resolve.
Do not use force resets or delete worktrees to skip conflicts. Optional separate
PRs serve the same reviewed integration goal but require explicit push/PR
permission and final combined gates.

## Lab 4 answer key

[Complete export](solutions/features/handoff.mjs) and
[owned export test](solutions/tests/handoff.test.mjs) filter active issues,
project exactly four fields, preserve supplied order, and add no timestamp.
It consumes triage rather than recalculating it.

For KEYBOARD the downloaded object is exactly:

```json
{
  "available": true,
  "schemaVersion": 1,
  "items": [
    {
      "id": "ISS-102",
      "title": "Keyboard focus disappears in the menu",
      "priority": "P2",
      "reason": "medium impact (+30); blocked workflow (+25)"
    }
  ]
}
```

Full board exports 6 active items in ranked order; PAYMENTS exports only
ISS-101/P1. Closed issues still appear in the board/search but not in handoff.
The export is fictional issue evidence, not evidence that test commands ran.
Review that distinction before accepting a report.

Catch-up: `npm run workshop:apply -- handoff`.
Final gates: handoff 6; all 26; baseline plus owned tests (18 with all four
features); smoke; active customization subset and actual tools/loading
observations; manual keyboard/narrow-screen/search/download checks. If any
required check is unresolved, report not-ready. A successful handoff authorizes
no push, PR, merge, or deployment.

**Why this lab matters.** Finishing is not the same as being *ready*. The export is
tiny on purpose so the lesson is the **evidence habit**: what did you run, what
exited how, what did you not run, what are you unsure of. Reward the honest
"not ready" report over the confident wrong one.

## Rehearse the full answers and return to starter

```text
npm run workshop:apply -- all
npm run acceptance -- all
npm test
npm run smoke
```

Save the printed backup ID. Installing all four answers includes four owned
tests, so the provided baseline 14 plus owned 4 gives 18 passing tests.
Then `npm run workshop:restore -- <saved-id>` restores the prior feature/test
contents while first preserving current contents in a rescue snapshot.
Alternatively `npm run workshop:starter` explicitly resets only four features
and removes only four named owned tests, with a backup. Customizations and
unrelated work remain. Full details, with real output, are in [restore](restore.md).

Do not run installers while writers are editing. Their fixed-path backups and
change checks are recovery helpers, not enforced leases or an atomic transaction.

## Debrief rubric

Accept a task report only when it names the goal, explicit relevant context,
owned paths, frozen contract, actual command/exit/results or NOT RUN, uncertainty,
and a clear stop/release. Ask participants what they chose not to delegate.
Good outcomes are safe boundaries and trustworthy evidence, not an agent count.

**Ask these four "why" questions at the end** (two minutes, in Lab 4's retrospective):

1. Why did we freeze the contract *before* anyone wrote code?
2. Why was the reviewer read-only?
3. Why is a passing test not the same as "ready"?
4. What would you *not* delegate, and why?

A participant who can answer these has the *why*, which is the goal of workshop2.

Common misconceptions to correct: profile equals session; skill grants tools;
subagent context automatically isolates files; every harness accepts the same
frontmatter; a read-only chat lock means a filesystem sandbox; a task board or
CODEOWNERS enforces edits; worktrees remove all races; all-green unit tests alone
prove integrated UX. Use the no-preview sequential route without embarrassment.

After minute 180, use [extensions](extensions.md). Keep the app synthetic, local,
dependency-light, and without surprise cloud costs.

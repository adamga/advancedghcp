# Facilitator guide and complete answer key

**Audience:** people who just learned basic agents/skills.
**Time:** exactly 60 minutes presentation/demo + 120 hands-on.
**Hands-on:** 30, 35, 40, 15 minutes, no extra break outside those allocations.
Complete [preflight](preflight.md) before the session. The presentation/video are
separate workshop deliverables; this guide owns the app/lab facilitation.

## Presentation and standalone lesson

Use the [42-slide editable PowerPoint](../deliverables/advanced-github-copilot-workshop.pptx)
and [printable PDF](../deliverables/advanced-github-copilot-workshop.pdf).
The supplied template's near-black/Arial/white/cyan/purple-blue language is adapted
with original workshop content; the original reference deck is not redistributed.

The [GPT-audio Alloy MP4](../deliverables/advanced-github-copilot-explainer.mp4)
is **separate self-paced pre/post material**, not an extra segment in the live
180-minute agenda. It uses Microsoft Foundry `gpt-audio-1.5`, Alloy voice,
phrase-timed captions and 42 embedded chapters. It is a narrated slide lesson,
not a recording of live Copilot UI. Full speaker notes are standalone narration,
**not text to read verbatim within the 60-minute talk/demo block**.

Accessible and navigation editions:
[SRT](../deliverables/advanced-github-copilot-explainer.srt),
[WebVTT](../deliverables/advanced-github-copilot-explainer.vtt),
[transcript](../deliverables/explainer-transcript.md),
[audio-only](../deliverables/explainer-audio.m4a),
[chapter timestamps](../deliverables/video-chapters.txt), and
[timeline](../deliverables/video-timeline.json).
The [15-source ledger](../deliverables/source-ledger.md) records official facts
checked November 7, 2026 and their product/policy/preview limits.

Packaging/verification records:
[slide contact sheet](../deliverables/slide-contact-sheet.jpg),
[media verification](../deliverables/media-verification.json),
[text-fit adjustments](../deliverables/text-fit-adjustments.json), and
[content manifest](../deliverables/workshop-manifest.json).
The [narration manifest](../deliverables/narration-manifest.json) records verified
source passages and actual audio chunk timings; the original teaching text and
slide files are unchanged. The media verification covers complete audiovisual
decode, 42 chapters, caption coverage, frame alignment, and fitted PowerPoint text bounds.
[Optional media rebuild instructions](../media/README.md) are outside attendee
preflight and all timed labs; the app remains zero-dependency Node.

## Timed slide map - no extra minutes

| Live clock | Slides | Talk/demo allocation | What to do |
|---|---|---|---|
| 00:00-00:15 | 1-10 | 11 min talk + 4 min app demo | Set expectations; show starter, four seams, and baseline |
| 00:15-00:35 | 11-23 | 10 min talk + 5 min demo1 + 5 min demo2 | Custom agent/skill, then bounded reviewer-to-writer delegation |
| 00:35-01:00 | 24-35 | 19 min talk + 6 min demo3 | Same-repo ownership/contracts, research-first integration, limits/fallback |
| Within 01:00-03:00 | 36-39 | Included in the four labs, not added | Lab launch/checkpoint/debrief prompts |
| Within 02:45-03:00 | 40-41 | Included in Lab4's 15 min | Recovery, evidence handoff, retrospective/closing |
| Reference whenever needed | 42 | No separate time allocation | Official-source pointers |

At minute 60 transition directly to the 30/35/40/15-minute lab schedule below.
Do not play the complete standalone video during the live agenda or turn full
narration notes into additional presentation time.

## Before class

Use a clean starter checkout. Run:

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

At minute60, everyone should be able to distinguish:

| Concept | Beginner explanation | Boundary |
|---|---|---|
| Repository instructions | Shared rules for how this repo is worked on | Guidance; not automatic inheritance in every subagent |
| Custom agent | Reusable role with instructions and tools | Definition, not a separate session |
| Skill | Reusable procedure with optional reference/script resources | Context, not additional tool permission |
| Subagent | A delegated bounded task with separate context and report | Context isolation, not filesystem isolation |
| Local handoff | Change active role in the same conversation | Local-only; not delegation |
| Top-level session | A conversation the user prompts independently | Not a child merely because another chat exists |
| Worktree | Different working files/index for a branch | Does not eliminate shared-repo integration or port/service conflicts |

Say: "We will use one small app and make ownership/contracts explicit. Two
read-only research streams followed by one writer is already useful orchestration."

## Live pacing and rescue triggers

| Workshop clock | Facilitation | If a participant is behind |
|---|---|---|
| 01:00 | Lab1 begins; choose harness, inspect starter | Use ordinary Chat view if Agents window is missing |
| 01:10 | Ask for instruction diff and reviewer role | Offer shared read/search profile fields |
| 01:18 | Switch attention to actual skill resources | Use contract policy, not invented business rules |
| 01:26 | Run customization/fixture checks and two loading tests | Complete answer installer only after explaining each missing piece |
| 01:30 | Lab2 begins; coordinator and task packet | Paste complete research packet; preserve read-only tools |
| 01:44 | Research report accepted; start priority implementation | Show closed early-return hint |
| 01:55 | Run priority gate and review | Apply priority answer if needed; still require explanation/evidence |
| 02:01 | Debrief subagent/handoff/session distinction | Use the four-row distinction table, no UI scavenger hunt |
| 02:05 | Lab3 begins; ownership board and contract freeze | Default to single-writer RouteA |
| 02:18 | Research accepted; implementation | Provide A/B task packets; serialize if product availability differs |
| 02:32 | Workers stop; integrator gates and visible counts | Separate feature installers rescue A/B independently |
| 02:40 | Collision/branch alternatives and report | Explain tradeoffs; do not spend class configuring worktrees |
| 02:45 | Lab4 begins; small export | Show filter-then-map hint |
| 02:49 | Final gates and download | Apply handoff if needed; do not skip evidence checks |
| 02:56 | Report and review readiness | Any unresolved failure is "not ready" |
| 02:58 | Two-minute retrospective | One direct-task lesson and one boundary |
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
| ISS-101 | high60+blocked25+users10+age5 |100/P1; four ordered reasons |
| ISS-102 | medium30+blocked25 |55/P2; impact then blocked |
| ISS-103 | low10+age5 |15/P3 |
| ISS-104 | medium30+users10 |40/P2 |
| ISS-105 | closed override |0/P3; sole closed reason |
| ISS-106 | medium30+age5 |35/P3 |
| ISS-107 | low10 |10/P3 |
| ISS-108 | closed override |0/P3 |

P1 threshold>=80, P2>=40. Nearest reachable P1 boundary values are75/P2 and85/P1:
do not invent an80 fixture. Exact99/100-user and6/7-day checks matter.
Show why a closed high-impact blocked issue must short-circuit first.

Catch-up: `npm run workshop:apply -- priority`; validate with
`npm run acceptance -- priority` (6) and `npm test`.
Review common failures: closed handled last, > rather than >=, unordered reasons,
input mutation, or "sorting" implemented in the wrong shared file.

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
Installer `npm run workshop:apply -- agents-local` or `agents-copilot` copies all
four complete chosen profiles plus skill for demo/catch-up; it backs up current
customizations. If delegating Local workers, update the coordinator allowlist
and body **before** freezing work. Do not edit this shared config mid-flight.

Answers:
[search](solutions/features/search.mjs) and
[search test](solutions/tests/search.test.mjs);
[summary](solutions/features/summary.mjs) and
[summary test](solutions/tests/summary.test.mjs).
Search uses trimmed whitespace tokens, literal lowercase text, and every-token
matching. It returns new arrays with existing input objects/order. Summary uses
only the passed visible subset; active=not closed; active blocked excludes
closed blocked. Categories include closed records and have sorted keys.

| Query | Visible IDs | Summary total/active/blocked | Category counts |
|---|---|---|---|
| empty | all8 |8/6/2 | accessibility2,payments2,reporting2,search2 |
| PAYMENTS | ISS-101,ISS-105 |2/1/1 | payments2 |
| KEYBOARD accessibility | ISS-102 |1/1/1 | accessibility1 |
| keyboard payments | none |0/0/0 |{} |
| .* | none |0/0/0 |{} |

No shared server/UI/package edit should be needed. A/B do not depend on one
another. Each owns a separate test; the integrator validates combined HTTP/UI
observations after both stop. Task-board leases and CODEOWNERS are advisory/review
routing; they do not enforce ownership. Shared Git index/branch and processes/
ports remain potential race points even with disjoint source files.

Catch-up each task separately: `workshop:apply -- search`, then
`workshop:apply -- summary`; six acceptance tests per task, baseline and smoke.
Run `npm run verify:solutions` in a clean starter to prove the isolated complete
answers without touching app source.

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
baseline, and commit only those paths. Give A PORT3001 and B PORT3002 if serving
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

Full board exports6 active items in ranked order; PAYMENTS exports only
ISS-101/P1. Closed issues still appear in the board/search but not in handoff.
The export is fictional issue evidence, not evidence that test commands ran.
Review that distinction before accepting a report.

Catch-up: `npm run workshop:apply -- handoff`.
Final gates: handoff6; all26; baseline plus owned tests; smoke; active
customization subset and actual tools/loading observations; manual keyboard/
narrow-screen/search/download checks. If any required check is unresolved, report
not-ready. A successful handoff authorizes no push, PR, merge, or deployment.

## Rehearse the full answers and return to starter

```text
npm run workshop:apply -- all
npm run acceptance -- all
npm test
npm run smoke
```

Save the printed backup ID. Installing all four answers includes four owned
tests, so the provided baseline14 plus owned4 gives18 passing tests.
Then `npm run workshop:restore -- <saved-id>` restores the prior feature/test
contents while first preserving current contents in a rescue snapshot.
Alternatively `npm run workshop:starter` explicitly resets only four features
and removes only four named owned tests, with a backup. Customizations and
unrelated work remain. Full details are in [restore](restore.md).

Do not run installers while writers are editing. Their fixed-path backups and
change checks are recovery helpers, not enforced leases or an atomic transaction.

## Debrief rubric

Accept a task report only when it names the goal, explicit relevant context,
owned paths, frozen contract, actual command/exit/results or NOT RUN, uncertainty,
and a clear stop/release. Ask participants what they chose not to delegate.
Good outcomes are safe boundaries and trustworthy evidence, not an agent count.

Common misconceptions to correct: profile equals session; skill grants tools;
subagent context automatically isolates files; every harness accepts the same
frontmatter; a read-only chat lock means a filesystem sandbox; a task board or
CODEOWNERS enforces edits; worktrees remove all races; all-green unit tests alone
prove integrated UX. Use the no-preview sequential route without embarrassment.

After minute180, use [extensions](extensions.md). Keep the app synthetic, local,
dependency-light, and without surprise cloud costs.

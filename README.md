# Advanced GitHub Copilot: one repo, safer teamwork (Workshop 2)

A **3-hour workshop** for people who already know the basics of agents and skills:
60 minutes of presentation/demo, then **120 minutes of hands-on labs**. You will
practice custom agents, skills, bounded subagents, and safe orchestration in one
repository, using a small fictional **issue triage board**.

> **Workshop 2** is a full rewrite of the labs. Every step now explains **what to do
> and why**, in plain language, so people of all levels walk away understanding the
> *reasons*, not just the commands. The app, the frozen contracts, the timings, and
> the checks are the same as edition 1. Edition 1 is preserved in Git history
> (commit `8e5e291`) and in [pull request #1](https://github.com/adamga/advancedghcp/pull/1).

## Start here

**New to this? Read in this order:**

1. [The story](workshop2/01-the-story.md): what the app is, what is missing, why it
   matters, and what you will fix. (10 minutes)
2. [Concepts](workshop2/02-concepts.md): every term in plain English with everyday
   analogies. (10 minutes)
3. [Preflight](workshop2/preflight.md): get your computer ready **before** the session.
   (15-25 minutes, not part of the three hours. Reading the story and concepts plus
   preflight is about 35-45 minutes in total.)
4. [The workshop guide](workshop2/README.md): your route through the day, and how to
   read a lab step.

Facilitators: start with the [facilitator guide and answer key](workshop2/instructor-guide.md).

**Get the code** (the workshop lives on its own branch until the pull request is merged):

```text
git clone -b adamga-workshop-app-and-hands-on-labs https://github.com/adamga/advancedghcp.git advancedghcp-workshop
```

Quick start from the repository root:

```text
node --version
npm test
npm start
```

Open <http://127.0.0.1:3000> (stop the server with `Ctrl+C`). You should see **eight
fictional issues, every badge reading `untriaged`**. That is correct: the app is
*deliberately unfinished*, and finishing it is the workshop.

Do **not** run `npm install`: there are no package dependencies. No Azure
subscription, cloud-agent job, MCP server, marketplace, connector, experimental
computer use, or paid cloud resource is required. Copilot model usage and
subagents can still consume your plan's allowance.

## The exact agenda

| Workshop clock | Activity | Duration | What you walk away with |
|---|---|---:|---|
| 00:00-01:00 | Presentation and demos | 60 min | A shared mental model and the product workflow |
| 01:00-01:30 | [Lab 1: rules, a reviewer, and a skill](workshop2/labs/lab-1.md) | 30 min | An active read-only reviewer and a reusable policy skill |
| 01:30-02:05 | [Lab 2: delegate and prove (priority)](workshop2/labs/lab-2.md) | 35 min | A checked research report and a tested priority feature |
| 02:05-02:45 | [Lab 3: orchestrate safely (search + summary)](workshop2/labs/lab-3.md) | 40 min | Two features built without file collisions |
| 02:45-03:00 | [Lab 4: review and hand off (export)](workshop2/labs/lab-4.md) | 15 min | A JSON export, final gates, and an honest report |

Preflight and [extensions](workshop2/extensions.md) are outside the 180 minutes.
Short stretch and check-in moments are already inside each lab.

The [facilitator guide](workshop2/instructor-guide.md) contains a timed slide map:
slides 1-10 in the first 15 minutes (including a 4-minute app demo), slides 11-23 in
the next 20 (two 5-minute demos), slides 24-35 in the final 25 (6-minute orchestration
demo). Slides 36-39 are lab launch/debrief prompts within the 120-minute hands-on
block; slides 40-41 are recovery/closing within Lab 4; slide 42 is references with
no extra time.

## What the labs teach, in one line each

| Lab | The "why" |
|---|---|
| 1 | Rules, a role, and a recipe turn a general assistant into a specialist that knows how your team works. |
| 2 | Delegation works when the task is bounded, read-only first, and checked afterward. "Done" is a claim, not proof. |
| 3 | Agents collide because they share files, ports, and the git index, not because they share a conversation. Prevent it with ownership, a frozen contract, one integrator, and gates. |
| 4 | A result is only as good as its evidence. An honest "not ready" beats a confident "done." |

## Starter versus answers

The starter is intentionally usable but **not feature complete**. Eight fictional
issues render, health/static/API routes work, labels and keyboard focus are present,
and baseline tests pass. Four purposeful enhancements remain:

| Enhancement | Owner file | Baseline | Completed behavior |
|---|---|---|---|
| Priority, Lab 2 | `src/features/priority.mjs` | Explicit `untriaged`, null score | Deterministic P1/P2/P3 with reasons |
| Search, Lab 3A | `src/features/search.mjs` | Returns all issues | Literal case-insensitive AND matching |
| Summary, Lab 3B | `src/features/summary.mjs` | Counts marked unavailable | Visible totals, active/blocked/category counts |
| Evidence export, Lab 4 | `src/features/handoff.mjs` | Export HTTP 501; link hidden | Minimal deterministic JSON for active visible issues |

The shared server and UI are already wired to the frozen
[contracts](workshop2/contracts.md), so two workstreams never need to edit a
shared module or package file. Every task owns its own test file.

`workshop2/templates/` contains **unfinished** customization templates.
`workshop2/solutions/` contains complete **instructor answers**, never imported by
the starter. `workshop2/starter/` contains explicit restore snapshots.
No custom agent or skill is active in a fresh clone; Lab 1 creates them.
The repository-wide `.github/copilot-instructions.md` is active from the start.

## VS Code or the GitHub Copilot app

Choose either surface. The [preflight](workshop2/preflight.md) gives exact product
and policy checks, including the VS Code Agents window and an ordinary-chat fallback.
As checked against official docs on **November 9, 2026**, new VS Code sessions
default to the **Copilot harness**. Select **Local explicitly** only for the
Local-specific exercise.

Instructor profiles are split into `customizations/local/` and
`customizations/copilot/`. Local's `agents` allowlist and `handoffs` are **not**
portable to Copilot/app; Copilot's `skills` frontmatter is **not** accepted by
Local. `target` chooses editor schema, not session runtime. Verify the actual
tools in the intended harness. Skills do not grant tool permissions or guarantee
automatic loading. Do not rely on repository-instruction inheritance in custom
subagents; delegation prompts include the relevant invariants explicitly.

The app's Projects experience and customization marketplaces are preview features;
neither is required. If a newer UI or subagent feature is missing, use the documented
sequential fallback. Do not bypass an organization policy to match the demo.

## Commands and evidence

All commands run from the repository root and work without installing packages:

```text
npm test
npm run smoke
npm run check:customizations
npm run acceptance -- priority
npm run acceptance -- search
npm run acceptance -- summary
npm run acceptance -- handoff
npm run acceptance -- all
npm run verify:solutions
```

To show the fully completed board **without overwriting starter files**:

```text
npm run start:solutions
```

It uses the same loopback server and PORT option, importing only the separate
instructor feature implementations. Stop it with `Ctrl+C` before starting another
server on that port. The ordinary `npm start` always uses the current starter/
participant source, not hidden answers.

`npm test` covers baseline contracts, HTTP behavior, UI source safeguards, and
backup/restore. The starter has 14 baseline tests. The four feature acceptance
commands each run six tests; `all` also runs two integration tests (26 total).
**Acceptance failures before implementing the assigned feature are expected**;
they are not a broken starter and must not be weakened.
`verify:solutions` runs the isolated instructor features plus integration without
overwriting starter files. Static UI checks do not replace the manual keyboard,
narrow-screen, search, and download checks in the labs.

Instructor catch-up, **not the default attendee workflow**:

```text
npm run workshop:apply -- priority
npm run workshop:apply -- search
npm run workshop:apply -- summary
npm run workshop:apply -- handoff
```

Each command prints a backup ID **before** writing and includes the task's owned
test. [Restore instructions](workshop2/restore.md) preserve current contents before
undoing named files; no destructive Git reset/checkout commands are used.

## Deck, standalone video, and accessible editions

The **42-slide editable deck** adapts the supplied template's near-black background,
Arial typography, white text, cyan accents, and purple-blue palette with original
workshop content. The **animated GPT-audio Coral explainer** is separate self-paced
pre/post material; it is **not added to the 180-minute live agenda**.

| Material | Download |
|---|---|
| Editable presentation | [PowerPoint deck](deliverables/advanced-github-copilot-workshop.pptx) |
| Printable slide handout | [PDF slides](deliverables/advanced-github-copilot-workshop.pdf) |
| Complete narrated lesson | [Animated Coral MP4](deliverables/advanced-github-copilot-explainer.mp4) |
| Short playback sample | [Animated preview](deliverables/animated-explainer-preview.mp4) |
| External captions | [SRT](deliverables/advanced-github-copilot-explainer.srt) / [WebVTT](deliverables/advanced-github-copilot-explainer.vtt) |
| Accessible narration | [Full transcript](deliverables/explainer-transcript.md) / [audio-only M4A](deliverables/explainer-audio.m4a) |
| Navigation | [42 chapter timestamps](deliverables/video-chapters.txt) / [video timeline](deliverables/video-timeline.json) |
| Official facts and limits | [15-source ledger](deliverables/source-ledger.md), checked November 7, 2026 |
| Visual/verification records | [Slide overview](deliverables/slide-contact-sheet.jpg), [media verification](deliverables/media-verification.json), [text-fit adjustments](deliverables/text-fit-adjustments.json), [content manifest](deliverables/workshop-manifest.json) |

The video uses **Microsoft Foundry `gpt-audio-1.5`, playful Coral voice**, with a
measured quicker cadence, large on-screen captions and 42 embedded chapters. Its
[beginner-friendly script](deliverables/video-script.md) covers the same 42 topic
areas in 126 visual teaching beats. [Motion graphics](deliverables/animation-contact-sheet.jpg)
explain roles, shared files, dependencies, worktrees, code and worked triage examples.
It is an original animated lesson, **not a recording of live Copilot UI**.

> **The video explains the concepts; the written labs are the source of truth for
> the steps.** The video was produced for edition 1. It has **not** been re-narrated
> for the workshop2 lab rewrite. It covers the same concepts (agents, skills,
> delegation, safe orchestration), but where it differs in detail from
> [`workshop2/labs/`](workshop2/labs/lab-1.md), follow the written labs.

The [narration manifest](deliverables/narration-manifest.json) records voice
provenance, chunk transcripts and measured timings. The
[audio measurements](deliverables/audio-verification.json) document quieter
mastering around -22 LUFS, low-rumble reduction and a post-encoding true-peak
ceiling of -4 dBTP. No background music or effects compete with speech.
Long-form speaker notes are a teaching reference, not a verbatim live script.
[Media sources and rebuild instructions](media/README.md) are separate from the
dependency-free Node app; rebuilding media is optional and not part of attendee
preflight or lab time.

The application runs offline with **Node >=22, no dependencies, no authentication,
no AI integration, and no cloud services**. Copilot exercises need an online
Copilot-enabled account; the sample app itself does not.

## Repository map

| Path | Purpose |
|---|---|
| `workshop2/` | **The workshop**: story, concepts, preflight, four labs, contracts, restore, troubleshooting, extensions, facilitator guide |
| `workshop2/labs/` | Step-by-step labs: every step has what, why, how, what you should see, what to do if not, and a reflection |
| `workshop2/templates/` | Unfinished customization and report/task-board templates |
| `workshop2/solutions/` | Complete profiles, skill resources, feature implementations, owned tests (instructor answers) |
| `workshop2/starter/`, `workshop2/acceptance/` | Restore snapshots and feature acceptance checks used by the scripts |
| `src/data/issues.mjs` | Frozen synthetic fixtures |
| `src/app.mjs`, `src/http.mjs`, `src/server.mjs` | Single-writer pipeline and loopback HTTP server |
| `src/features/` | Four independently assigned exercise seams |
| `public/` | Accessible static board, safe text rendering, pre-wired controls |
| `tests/` | Always-on baseline checks; task-owned tests added during labs |
| `scripts/` | Portable runners, explicit feature acceptance, backup/restore, customization checks |
| `deliverables/` | All 21 final presentation/video/accessibility/verification outputs |
| `media/` | Original slide source, beginner storyboard, animation, Foundry narration and rebuild scripts |

This is a teaching sample, not a production support system. It has no persistent
storage or write API. File ownership and leases are **advisory**, not enforced
locks. Separate subagent contexts do **not** isolate the filesystem. Same-checkout
sessions share files, the Git index/branch, server ports, and running processes.
The workshop makes those risks visible rather than hiding them behind worktrees.

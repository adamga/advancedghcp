# Advanced GitHub Copilot: one repo, safer teamwork

A **3-hour workshop** for people who already know basic agents and skills:
60 minutes of presentation/demo, then **120 minutes of hands-on work**.
Practice custom agents, skill resources, bounded subagents, and safe orchestration
in one repository using a small fictional **issue triage board**.

## Deck, standalone video, and accessible editions

The **42-slide editable deck** adapts the supplied template's near-black background,
Arial typography, white text, cyan accents, and purple-blue palette with original
workshop content. The **GPT-audio Alloy narrated explainer** is separate self-paced pre/post
workshop material; it is **not added to the 180-minute live agenda**.

| Material | Download |
|---|---|
| Editable presentation | [PowerPoint deck](deliverables/advanced-github-copilot-workshop.pptx) |
| Printable slide handout | [PDF slides](deliverables/advanced-github-copilot-workshop.pdf) |
| Complete narrated lesson | [GPT-audio Alloy MP4](deliverables/advanced-github-copilot-explainer.mp4) |
| External captions | [SRT](deliverables/advanced-github-copilot-explainer.srt) / [WebVTT](deliverables/advanced-github-copilot-explainer.vtt) |
| Accessible narration | [Full transcript](deliverables/explainer-transcript.md) / [audio-only M4A](deliverables/explainer-audio.m4a) |
| Navigation | [42 chapter timestamps](deliverables/video-chapters.txt) / [video timeline](deliverables/video-timeline.json) |
| Official facts and limits | [15-source ledger](deliverables/source-ledger.md), checked November 7, 2026 |
| Visual/verification records | [Slide overview](deliverables/slide-contact-sheet.jpg), [media verification](deliverables/media-verification.json), [text-fit adjustments](deliverables/text-fit-adjustments.json), [content manifest](deliverables/workshop-manifest.json) |

The video uses **Microsoft Foundry `gpt-audio-1.5`, Alloy voice**, includes
phrase-timed captions and 42 embedded chapters, and explains all 42 topics.
The original teaching text and slide files are unchanged. Narration is generated
in short chunks, verified against the source, and loudness-normalized.
The [narration manifest](deliverables/narration-manifest.json) records voice
provenance, chunk transcripts and measured timings.
It is an original narrated slide lesson, **not a recording of live Copilot UI**.
Long-form speaker notes are standalone narration, not a verbatim live script.
The coordinator's verification record reports complete audiovisual decode,
source-content coverage, frame alignment and fitted PowerPoint text bounds.
[Media sources and rebuild instructions](media/README.md)
are separate from the dependency-free Node app; rebuilding media is optional and
not part of attendee preflight or lab time.

The application runs offline with **Node >=22, no dependencies, no authentication,
no AI integration, and no cloud services**. Copilot exercises need an online
Copilot-enabled account; the sample app itself does not.

## Start here

1. Complete [attendee preflight](workshop/preflight.md) **before** the timed workshop.
2. Run the starter from the repository root:

   ```text
   node --version
   npm test
   npm start
   ```

3. Open <http://127.0.0.1:3000>. Stop the server with Ctrl+C.
4. Follow [the hands-on route](workshop/README.md). Instructors start with
   [the facilitator guide and answer key](workshop/instructor-guide.md).

Do **not** run `npm install`: there are no package dependencies or lockfile to
coordinate. No Azure subscription, cloud-agent job, MCP server, marketplace,
connector, experimental computer use, or paid cloud resource is required.
Copilot model usage and subagents can still consume your plan's allowance.

## The exact agenda

| Workshop clock | Activity | Duration | Tangible outcome |
|---|---|---:|---|
| 00:00-01:00 | Presentation and demos | 60 min | Shared mental model and product workflow |
| 01:00-01:30 | [Lab 1: instructions, custom agent, real skill](workshop/labs/lab-1.md) | 30 min | Active reviewer and reusable policy skill |
| 01:30-02:05 | [Lab 2: bounded delegation and priority](workshop/labs/lab-2.md) | 35 min | Read-only specialist report and tested priority |
| 02:05-02:45 | [Lab 3: two owned workstreams](workshop/labs/lab-3.md) | 40 min | Search + summary integrated without shared-file races |
| 02:45-03:00 | [Lab 4: review and evidence handoff](workshop/labs/lab-4.md) | 15 min | JSON export, quality gate, retrospective |

Preflight and [extensions](workshop/extensions.md) are outside the 180 minutes.
Short stretch/check-in moments are already inside each lab, not extra agenda time.

The [instructor guide](workshop/instructor-guide.md) contains a timed slide map:
slides 1-10 in the first 15 minutes (including a 4-minute app demo), slides 11-23 in
the next 20 (two 5-minute demos), slides 24-35 in the final 25 (6-minute orchestration
demo). Slides 36-39 are lab launch/debrief prompts within the 120-minute hands-on
block; slides 40-41 are recovery/closing within Lab 4; slide 42 is references with
no extra time.

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
[contracts](workshop/contracts.md), so two workstreams never need to edit a
shared module or package file. Every task owns its own test file.

`workshop/templates/` contains **unfinished** customization templates.
`workshop/solutions/` contains complete **instructor answers**, never imported by
the starter. `workshop/starter/` contains explicit restore snapshots.
No custom agent or skill is active in a fresh clone; Lab 1 creates them.
The repository-wide `.github/copilot-instructions.md` is active from the start.

## VS Code or the GitHub Copilot app

Choose either surface. The [preflight](workshop/preflight.md) gives exact product
and policy checks, including the VS Code Agents window and an ordinary-chat fallback.
As checked against official docs on **November 7, 2026**, new VS Code sessions
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
instructor feature implementations. Stop it with Ctrl+C before starting another
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
test. [Restore instructions](workshop/restore.md) preserve current contents before
undoing named files; no destructive Git reset/checkout commands are used.

## Repository map

| Path | Purpose |
|---|---|
| `src/data/issues.mjs` | Frozen synthetic fixtures |
| `src/app.mjs`, `src/http.mjs`, `src/server.mjs` | Single-writer pipeline and loopback HTTP server |
| `src/features/` | Four independently assigned exercise seams |
| `public/` | Accessible static board, safe text rendering, pre-wired controls |
| `tests/` | Always-on baseline checks; task-owned tests added during labs |
| `scripts/` | Portable runners, explicit feature acceptance, backup/restore, customization checks |
| `workshop/labs/` | Prompts, steps, checkpoints, measurable criteria, hints |
| `workshop/templates/` | Unfinished customization and report/task-board templates |
| `workshop/solutions/` | Complete profiles, skill resources, feature implementations, owned tests |
| `workshop/instructor-guide.md` | Pacing, worked answers, recovery and debrief |
| `deliverables/` | All 15 final presentation/video/accessibility/verification outputs |
| `media/` | Original content source, optional Foundry narration and media rebuild scripts |

This is a teaching sample, not a production support system. It has no persistent
storage or write API. File ownership and leases are **advisory**, not enforced
locks. Separate subagent contexts do **not** isolate the filesystem. Same-checkout
sessions share files, the Git index/branch, server ports, and running processes.
The workshop makes those risks visible rather than hiding them behind worktrees.

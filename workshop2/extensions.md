# Extensions: where to go after the workshop

**What this is.** The four labs fit the 180-minute workshop exactly. This page is
a menu of **optional next steps** for when you finish early, or want to keep
learning afterward.

**Do not add these to the four timed labs.** Finish the core gates first
(`npm run acceptance -- all` passing, `npm test` showing 18 passing, and your
truthful report written). Extensions are for *after* that.

## The recipe for any extension

Every extension works best if you apply what the labs taught you. Before you
start, write down these four things, then hand the work to an agent:

1. **Ownership.** Which files may be changed, and which may not?
2. **A contract.** What exactly goes in and comes out? (Write examples.)
3. **Allowed tools.** Does it need to edit, or is reading enough?
4. **A stop condition.** How will you know it is done and correct? (A test you can run.)

*Why.* Agents are fast but literal. Clear boundaries and a way to check the
result are what turn "fast" into "correct."

## The menu

| Extension | Suggested time | What you will learn | Independent acceptance (how you know it is done) |
|---|---:|---|---|
| Status and category controls | 20 min | How to add a feature **without** breaking earlier ones | Combined filters keep AND search working, and the summary and export still match what is on screen |
| Additional accessibility review | 20 min | How to use a **read-only** reviewer on a real quality concern | Keyboard order, visible focus, 200% zoom, narrow viewport, and screen-reader labels are all documented |
| Compare direct versus delegated work | 15 min | When more agents help and when they do not | Same task, same model, same input. Report time, usage, quality, and your uncertainty. **Do not assume "more agents" wins.** |
| Worktree integration rehearsal | 25 min | What worktrees really isolate, hands on | Tasks committed separately, different ports, **one** integrator cherry-picks, combined gates pass |
| Local handoff button | 15 min | The difference between a **handoff** and a **subagent** | A Local-only planner pre-fills a writer prompt with `send: false` (see below) |
| Approved policy or hook experiment | 30 min | What controls can and cannot guarantee | The harness-specific schema is verified; harmless allowed, denied, and timeout cases are recorded; you make **no** claim of a complete sandbox |

## Notes on the trickier ones

### Local handoff button

A **handoff** is a button that moves *you* from one agent to another **inside the
same conversation**, with a prompt already typed for you to review. It is **not**
the same as a subagent, which does separate work in its own context and reports
back.

Use the documented `handoffs` setting with a `label`, an `agent`, a `prompt`, and
`send: false`. With `send: false`, the prompt is placed in the box but **not
sent**, so you can read and edit it first. **Inspect the pre-filled prompt before
you submit it.**

- This field is **Local only**. The Copilot harness and the app do not accept it.
- Do not put the example in both profiles.
- Do not describe a same-conversation transition as a separate worker context.

### Worktree integration rehearsal

Use the worked example in the instructor guide's
[concrete worktree rehearsal](instructor-guide.md#concrete-optional-worktree-rehearsal).
Do **not** delete working folders or force branches to "recover." If something
goes wrong, follow [Restore](restore.md).

### Approved policy or hook experiment

Use only **synthetic** paths and **approved** tools. Read the caution in
[Troubleshooting](troubleshooting.md#optional-advanced-controls-not-required):
a hook is useful, but it is not a complete sandbox, and a timeout does not mean
"blocked."

## Ground rules for every extension

The sample app must stay **small and dependency-light**. Do not add any of these:

- authentication or user accounts
- real customer data or secrets
- cloud services or cloud costs
- calls to external AI services from the app itself
- claims that it is ready for production

*Why.* The app is a **teaching tool**. Keeping it simple is what lets the lesson
stay visible. If you want to grow it into something real, do that in a separate
project.

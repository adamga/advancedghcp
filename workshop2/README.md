# Workshop 2: Advanced GitHub Copilot, agents, and skills

**Welcome.** This is the hands-on guide for a three-hour workshop. It is written
for people of **all levels**. You do not need to be an expert programmer. If you
already know the basics of Copilot agents and skills, this workshop takes you to
the next level: building a small team of agents, giving them rules and recipes,
splitting work between them without collisions, and checking what they tell you.

> **Workshop 2** is a rewrite of the original labs with much more background and
> a "why" behind every step. The application and the checks are the same. The
> original edition is preserved in Git history (commit `8e5e291`) and in pull
> request #1.

## What you will be able to do afterwards

You will be able to explain, **in your own words, why** you would:

1. Write project rules, a read-only reviewer agent, and a skill, and say which
   job each one does.
2. Delegate research to a helper agent with a self-contained brief, then let one
   agent build with proof.
3. Run several agents on one project without them overwriting each other.
4. Review agent work, demand evidence, and write an honest report.
5. Choose between the **GitHub Copilot app**, the **VS Code Agents window**, a
   worktree, or plain ownership rules, based on the situation.

## The route through the workshop

```text
BEFORE (35-45 min in total, optional but recommended)
   01-the-story.md  ->  02-concepts.md  ->  preflight.md
          |
SESSION (3 hours)
   Presentation and demo (60 min)   <- the slide deck
          |
   Lab 1  Customize the team        30 min  (rules, reviewer agent, skill)
   Lab 2  Delegate and prove        35 min  (feature: priority)
   Lab 3  Orchestrate safely        40 min  (features: search + summary)
   Lab 4  Review and hand off       15 min  (feature: export)
          |
AFTER
   extensions.md for ideas to keep practicing
```

| Step | Time | What you do |
|---|---:|---|
| Before: read the [story](01-the-story.md) and [concepts](02-concepts.md) | about 20 min | Learn the app, the scenario, and the vocabulary |
| Before: run the [preflight](preflight.md) | about 15-25 min | Make sure your computer is ready (the story and concepts reading above is the optional first step of preflight, so do not count it twice) |
| Presentation and demo | 60 min | Watch and ask questions |
| [Lab 1: Customize the team](labs/lab-1.md) | 30 min | Rules, read-only reviewer, skill |
| [Lab 2: Delegate and prove](labs/lab-2.md) | 35 min | Add priority with a helper agent |
| [Lab 3: Orchestrate safely](labs/lab-3.md) | 40 min | Add search and summary without collisions |
| [Lab 4: Review and hand off](labs/lab-4.md) | 15 min | Add export, final checks, honest report |

If you could not read the background ahead of time, skim the **"Why this lab
exists"** box at the top of each lab; it is enough to get started.

## How to read a lab step

Every step in every lab uses the same five parts. Once you know the pattern you
can move quickly.

| Part | What it tells you |
|---|---|
| **What** | The action, in one sentence |
| **Why** | The reason. This is the part to remember. |
| **How** | Exact commands and prompts to use |
| **You should see** | What success looks like, so you know whether to continue |
| **If not** | The most likely cause and the safest way to recover |

Look for these labels too:

- **Prompt** blocks are text you paste into Copilot. Each comes with a short
  "why it is written this way" so you can write your own next time.
- **Reflect** questions are for you, not the computer. They are how the lesson
  sticks. Jot down a sentence for each.
- **Challenge** items are optional extras for when you finish early.

## Choose your path before you start

| Path | Choose it when | What to do |
|---|---|---|
| **Copilot in VS Code or the app** (recommended) | You have a recent VS Code with the Agents window, or the GitHub Copilot app | Use the `copilot` profiles (`npm run workshop:setup -- copilot`) |
| **VS Code Local harness** | You deliberately select **Local** in your session | Use the `local` profiles (`npm run workshop:setup -- local`) |
| **No agents UI available** | Your organization or version does not show subagents | Use ordinary chat with one writer, playing each role in turn. Write down that delegation was *simulated*. |
| **Copilot unavailable** | Copilot is blocked by policy or network | Do the same steps by hand. The app and tests run offline. |

**Pick one and stay with it.** Changing the harness in the middle of a lab is the
most common way to get confusing results.

## Rules of the road

1. Everything is fictional and local. Never paste real customer data or secrets.
2. Do **not** run `npm install`. The app needs nothing extra.
3. Do not open the instructor solutions unless a hint or the facilitator says so.
4. If something goes wrong, use [restore](restore.md) or
   [troubleshooting](troubleshooting.md). Nothing here is permanent.
5. Do not give an agent more tools just to make a demo look automatic. If an
   agent cannot run a command, you run it and share the real output.

## What is in this folder

| File | Purpose |
|---|---|
| [01-the-story.md](01-the-story.md) | The app, what is missing, why it matters, and the scenario |
| [02-concepts.md](02-concepts.md) | Plain-English concepts, comparisons, and a glossary |
| [preflight.md](preflight.md) | Setup and "is my computer ready" checklist |
| [labs/lab-1.md](labs/lab-1.md) to [lab-4.md](labs/lab-4.md) | The four hands-on labs |
| [contracts.md](contracts.md) | The exact rules each feature must follow (your reference sheet) |
| [restore.md](restore.md) | How to undo, retry, or start fresh |
| [troubleshooting.md](troubleshooting.md) | Symptom, cause, fix |
| [extensions.md](extensions.md) | Optional challenges after the workshop |
| [instructor-guide.md](instructor-guide.md) | Timing, rescue tips, and answer keys for facilitators |
| `templates/` | Starting files for the labs and report formats |
| `starter/`, `solutions/`, `acceptance/` | Technical assets used by scripts and checks (instructor use) |

## Optional notes tools

Copy the [report template](templates/task-report.md) and the
[task-board template](templates/task-board.md) into a local `.workshop-reports`
folder if you want persistent notes. That folder is ignored by Git. The human
(you) owns the board; helper agents return reports and do not edit it.

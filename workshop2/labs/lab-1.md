# Lab 1: Customize the team (rules, a reviewer, and a recipe)

**30 minutes | workshop clock 01:00 - 01:30 | App changes: none (this lab builds the team)**

## Why this lab exists

**The problem.** Imagine hiring three helpful new colleagues on the same day and
handing each a task with no handbook, no job description, and no instructions for
the tricky parts. Each would guess. One would be too careful, another would
overstep, and you would repeat the same warnings to every one of them.

Agents are the same. Without guidance they guess, and every task needs you to
re-explain your project's rules from scratch.

**The fix.** Before we touch the app, we set up three small pieces of guidance.
Each solves a different problem:

| Piece | Comparison | The problem it solves | File you will edit |
|---|---|---|---|
| **Repository instructions** | The house rules poster | "Every agent should follow these rules, always" | `.github/copilot-instructions.md` |
| **A custom agent** (Triage Reviewer) | A job description | "I want a *reviewer* who can look but never touch" | `.github/agents/triage-reviewer.agent.md` |
| **A skill** (`triage-policy`) | A recipe card with a reference drawer | "Teach agents our scoring rule, with exact examples" | `.github/skills/triage-policy/` |

**The scenario.** Sam's team is about to let agents help finish the triage board.
Before any real work, Sam wants three things in place: ground rules, a safe
reviewer who can check work without changing it, and a written scoring policy
that agents can consult instead of guessing.

**What you will have at the end.** Three finished pieces of guidance, a script
that proves they are well formed, and, just as important, an honest note about
whether the agent *actually used* them. The app itself does not change in this
lab.

## Words to know

| Word | Plain meaning |
|---|---|
| **Harness** | The engine that runs your agent session (Copilot or Local). Pick one and keep it. |
| **Frontmatter** | The small settings block between `---` lines at the top of an agent or skill file |
| **Tools** | What an agent is allowed to do. The reviewer gets only `read` and `search`. |
| **Least privilege** | Give a role only the abilities it needs, nothing more |
| **Backup ID** | A label the setup script prints so you can undo with `restore` |

## Before you start

- [Preflight](../preflight.md) passes: `npm test` shows 14 passing tests.
- You decided on a path (see the [start page](../README.md#choose-your-path-before-you-start)).
  **Recommended: `copilot`.** Use `local` only if you deliberately chose the Local
  harness. Do not switch partway through the lab.
- Keep [contracts](../contracts.md) open in a tab. It is the "rulebook" for the app.
- Do **not** open `solutions/`. If you get stuck, use the [hint ladder](#hint-ladder).

## Time plan

| Minutes | Step | You will have |
|---|---|---|
| 0-3 | Read this introduction | The idea of rules, role, recipe |
| 3-7 | 1. Look before you leap | A working starter and a chosen harness |
| 7-12 | 2. Write two rules | Two testable rules in the instructions |
| 12-19 | 3. Finish the reviewer | A read-only agent with a clear job |
| 19-26 | 4. Finish the skill | A recipe with reference, examples, and a script |
| 26-30 | 5. Check it and try it twice | Evidence it works, or an honest "not sure" |

---

## Step 1. Look before you leap (4 min)

**What.** Run the starter app, read the two guidance files, and install the
*unfinished* templates for your chosen harness.

**Why.** You cannot improve what you have not seen. Running the app first shows
you the "before" picture: every issue says `untriaged`. Reading the existing
rules shows what agents already know. We install **templates with blanks**
(not answers) so *you* make the decisions. The script also makes a **backup**
first, so you can undo the agent and skill files it installs. (The backup covers
only those files. In Step 2 you will edit a different file, and that has its own
undo.)

**How.**

1. In a terminal, from the repository folder, run the tests and start the app:

   ```text
   npm test
   npm start
   ```

   Open <http://127.0.0.1:3000>. Leave the terminal running; open a second
   terminal tab for later commands. (Stop the app any time with `Ctrl+C`.)

2. Read `.github/copilot-instructions.md` and `workshop2/contracts.md`
   (just skim the headings of the second one).

3. Install the templates. Use **one** of these:

   ```text
   npm run workshop:setup -- copilot
   ```

   or, only if you deliberately chose the Local harness:

   ```text
   npm run workshop:setup -- local
   ```

4. **Write down the backup ID** the script prints (a long string starting with
   digits). It is your undo button.

**You should see.**

- `npm test` ends with `# pass 14` and `# fail 0`.
- The board shows eight cards, every badge reads `untriaged`, and the summary
  line says "8 visible issues. Detailed counts unlock in Lab 3."
- The setup script prints `Backup saved: ...` then four lines starting with
  `Wrote:` and the sentence `Templates installed, NOT complete. Finish TODOs in Lab 1.`

**If not.**

| Symptom | Likely cause and fix |
|---|---|
| `npm: command not found` | Node.js is not installed or not on your path. Redo the [preflight](../preflight.md). |
| "port already in use" | An earlier copy of the app is still running. Stop it with `Ctrl+C` and start again. |
| Fewer or more than 14 tests | You may have edited files already. Run `npm run workshop:starter` (it backs up first) and retry. |

> **Reflect.** The templates were *not* completed for you. Why would a workshop
> (or a team) choose to start from an unfinished template rather than a finished one?

---

## Step 2. Write two rules (5 min)

**What.** Add two short, specific rules to `.github/copilot-instructions.md`.

**Why.** This file is read by agents working in the project, so a rule written
here is a rule you rarely have to type again. (One caution you will meet in Lab
2: a custom helper agent may *not* inherit this file, so the most important rules
also get repeated in the brief you hand to a helper.) But the *quality* of the
rule is
what matters. A vague rule ("be careful") is ignored; a specific, checkable rule
("cite the reference file when you explain a score") changes behavior and can be
verified in a diff.

| Vague (avoid) | Specific and testable (prefer) |
|---|---|
| "Write good code." | "Add tests only in the task-owned test file." |
| "Be accurate." | "Policy explanations must cite `references/policy.md`." |
| "Report honestly." | "Every report lists commands as RAN (with result) or NOT RUN." |

**How.** Ask Copilot to propose the rules, then you decide.

**Prompt:**

```text
Read .github/copilot-instructions.md and workshop2/contracts.md.
Propose two precise contributor rules for this issue-triage exercise:
policy evidence and truthful validation reporting. Explain why each matters.
Edit only .github/copilot-instructions.md after identifying the exact additions.
Do not change app features, dependencies, fixtures, or instructor solutions.
```

*Why it is written this way:* it names the **files to read** (so the agent does
not wander), asks for **exactly two** rules (a small, reviewable change), gives
the **two themes** (so the rules are useful), says to **explain why** (so you can
judge them), and lists what **not** to touch (a boundary).

**You should see.** A small diff (open **Source Control** in VS Code or run
`git diff .github/copilot-instructions.md`) that adds about two short rules. Each
rule is something you could check by looking at a report or a diff.

**If not.**

| Symptom | Fix |
|---|---|
| The agent rewrote the whole file | Undo only this file with `git restore .github/copilot-instructions.md` (you had no changes of your own in it before this step), then re-run with "make the smallest possible addition". Do **not** use `workshop:restore` here: its backup is for the files from Step 1 and would remove your reviewer and skill templates. |
| The rules are vague ("be thorough") | Ask: "Rewrite each rule so a reviewer could check it with yes/no." |
| The agent changed other files | Review the diff and discard those changes. The prompt's last line exists to prevent this. |

> **Reflect.** A rule in this file is *guidance*, not a lock. Name one thing
> besides a rule that you would still check to be sure an agent followed it.
> (Hint: the diff, and the tests.)

---

## Step 3. Finish the Triage Reviewer (7 min)

**What.** Complete `.github/agents/triage-reviewer.agent.md` so it defines a
read-only reviewer.

**Why.** A reviewer's job is to give an *opinion*. If it can also edit files, it
can quietly "fix" things while you only asked for feedback, and you lose the
independent second look. **Least privilege** solves that: give the role only
`read` and `search`. Then it *cannot* change anything, no matter how it is
prompted. Later, in Lab 2 and Lab 3, this reviewer is the safe helper your
coordinator calls on.

**How.** First, understand the parts of an agent file:

```markdown
---
name: Triage Reviewer        # the name you pick from the dropdown. Keep exactly.
description: ...             # what it is for; agents and people both read this
target: github-copilot       # which rulebook the editor uses to check the file
tools: ['read', 'search']    # the ONLY abilities this role has. Keep exactly.
---
Plain-language instructions go here, below the second ---.
```

The `target:` line was added for you by the setup script. **It does not change
which harness your session runs in**; it only tells the editor which schema to
validate against. Leave it as installed.

Now ask Copilot to fill the blanks:

**Prompt:**

```text
Complete only .github/agents/triage-reviewer.agent.md from its starter template.
Role: read-only issue-triage contract and test reviewer.
Inputs: the task's named files and workshop2/contracts.md; read referenced policy
resources only when supplied. No instructor solutions.
Tools must remain read/search only. No edits, execution, web access, or delegation
by the reviewer. Report objective, file/line findings, boundary cases, suggested
commands marked NOT RUN, uncertainties, and the stop condition.
Use the installed target; do not add harness-incompatible fields.
```

*Why it is written this way:* it gives the agent a **role** and **inputs**, forces
the **tools to stay small**, specifies the **shape of the report** (so every
review looks alike and is easy to compare), and tells it to mark commands
**NOT RUN**, because a role that cannot run commands must never pretend it did.
It ends with a **stop condition** so the agent does not wander into extra work.

A finished reviewer's body should contain, in your own words:

1. **Task:** what it reviews.
2. **Inputs:** which files it may read.
3. **Checklist:** the invariants it checks (for example, "no input is mutated").
4. **Output fields:** objective, findings, boundary cases, suggested commands (NOT RUN), uncertainties.
5. **Limits:** "I cannot edit, run commands, use the network, or delegate."
6. **Stop:** what "finished" means.

**You should see.**

- The frontmatter (the block between the two `---` lines at the top of the file)
  still has `name: Triage Reviewer` and
  `tools: ['read', 'search']`; the word `TODO` is gone.
- Open your surface's **Customizations** view (in VS Code, run **Chat: Open
  Customizations**). Triage Reviewer appears, and hovering shows only read and
  search tools.

**If not.**

| Symptom | Fix |
|---|---|
| Agent not in the picker | Start a **fresh chat** (the list is read when a session starts). Check the file is in `.github/agents/`, ends in `.agent.md`, and the name is spelled exactly. |
| It shows `edit` or `execute` tools | Edit the `tools:` line back to `['read', 'search']`. Never "fix" a missing ability by adding tools. |
| Editor warns about an unsupported field | Remove *only* that field. Copilot files do not accept `agents`, `handoffs`, or `argument-hint`; Local files do not accept `skills`. |

> **Reflect.** Suppose a teammate says, "The reviewer would be more useful if it
> could run the tests itself." What is the benefit, what is the risk, and what
> would you do instead? (Hint: it returns commands marked NOT RUN and a human
> runs them.)

---

## Step 4. Finish the triage-policy skill (7 min)

**What.** Complete `.github/skills/triage-policy/SKILL.md` and
`references/policy.md`.

**Why.** The scoring rule (high 60, blocked +25, and so on) is exactly the kind
of thing an agent might *invent* if you do not tell it. A **skill** packages the
rule with how to use it. Compare the three pieces:

```text
.github/skills/triage-policy/
  SKILL.md                    <- the recipe card: when to use it, the steps
  references/policy.md        <- the drawer: exact rule, examples, boundaries
  scripts/inspect-fixtures.mjs <- a tool: checks the sample data is well formed
```

Agents typically see only each skill's **name and description** up front, then
open the full `SKILL.md` when the task matches, and open the reference only when
needed. This keeps their desk (context) tidy. That is why the exact numbers live
in a *reference* file instead of being pasted into every conversation.

A skill **teaches a procedure; it does not grant abilities.** If the script
needs a terminal and the agent has no terminal tool, the skill cannot change
that. In that case the agent should say "NOT RUN" and hand the command to you.

**How.**

**Prompt:**

```text
Complete the triage-policy skill and its policy reference in
.github/skills/triage-policy/. Use only workshop2/contracts.md for the policy.
Include exact scores, reasons, closed override, 99/100 users, 6/7 days,
and fresh outputs/no mutation. Reference the bundled inspect-fixtures script.
State that the script runs from the repo root only when execution is authorized,
and that a read-only reviewer must return NOT RUN commands instead.
Do not implement priority or any other application feature yet.
```

*Why it is written this way:* **"use only contracts.md"** stops the agent from
making up numbers; it lists the **boundary cases** (99 vs 100 users, 6 vs 7 days)
that cause real bugs; it says **do not implement priority yet**, keeping this lab
small and honest.

Then run the bundled script yourself and read what it says. First *open the
script and skim it* (about 15 lines): you should never run code you have not
glanced at.

Windows PowerShell:

```powershell
node .github\skills\triage-policy\scripts\inspect-fixtures.mjs
```

macOS or Linux:

```bash
node .github/skills/triage-policy/scripts/inspect-fixtures.mjs
```

**You should see.**

- `Validated 8 synthetic issues; no files changed.` and a table of the eight issues.
- In `SKILL.md`: a `name: triage-policy` that matches the folder name, a specific
  `description`, a short numbered procedure, and **links** to
  `references/policy.md` and `scripts/inspect-fixtures.mjs`.
- In `policy.md`: the closed-issue override, the point values, the P1/P2/P3
  thresholds, two worked examples (ISS-101 = 100/P1, ISS-102 = 55/P2), and the
  note that closed ISS-105 scores 0/P3.
- No `TODO` left.

**If not.**

| Symptom | Fix |
|---|---|
| The script says a module is missing | You are not in the repository root. `cd` there and run it again. |
| The skill is not found later | The folder name must equal `name:`. Check for typos. |
| The agent put the numbers wrong | Compare against [contracts](../contracts.md) and correct by hand; you are the final judge. |

> **Reflect.** Why is the policy kept in `references/policy.md` instead of
> inside `SKILL.md`? (Think: desk space, and "load it only when needed".)

---

## Step 5. Check it, then try it twice (4 min)

**What.** Run the automatic check, then test the skill two different ways and
record what actually happened.

**Why.** "It exists" is not the same as "it works". We separate three questions
on purpose, because people often blur them:

1. Is the file **well formed**? (the check script)
2. Can the agent **find** and **use** the skill when you ask for it by name?
   (**explicit** use)
3. Does the agent **choose** the skill **by itself** when the task fits?
   (**automatic** selection, which is *not guaranteed*)

**How.**

```text
npm run check:customizations -- --require-lab1
npm test
```

The first command checks a **small subset** of rules (names, tools, links, no
leftover TODO). It is not a full validator and cannot prove runtime permissions.
(If it fails, the first line after `Error:` is the useful part; the lines
starting `at ...` are noise.)

Then, in a **fresh chat** (so earlier conversation cannot influence the result),
try an **explicit** request:

```text
Use triage-policy to explain ISS-101 and ISS-105 and derive boundary test cases.
Read the installed skill and its reference. Do not change files.
If your role cannot run scripts, inspect them and report NOT RUN commands.
```

Then open **another fresh chat** and test **automatic** selection with a request
that does *not* name the skill:

```text
Explain the fictional issue-priority policy and derive tests for closed issues
and user-count boundaries. Do not edit files.
```

Look at the chat's activity. Record one of: **loaded**, **not selected**, or
**cannot verify**.

**You should see.**

- `Customization subset passed ...` from the check, and `# pass 14`, `# fail 0`.
- In the explicit chat: the answer cites the policy file and says ISS-101 scores
  100 (P1) and ISS-105 scores 0 (P3).
- In the automatic chat: *either* the skill was used, *or* it was not. **Both are
  acceptable outcomes.** The only wrong answer is claiming it loaded without
  looking.

**If not.**

| Symptom | Fix |
|---|---|
| Check says `unfinished Lab 1 template` | A `TODO` remains in an agent or skill file. Finish it; do not delete the check. |
| Skill does not appear for the explicit request | Confirm the folder is `.github/skills/triage-policy/`, start a fresh chat, and if it still fails, attach the `SKILL.md` and reference to the chat and record "manual fallback, not verified automatic loading". |
| The answer shows the wrong scores | The reference file has an error. Fix it; the policy is the single source of truth. |

> **Reflect.** If the skill was *not* selected automatically, what do you do in
> the next lab? (Hint: invoke or attach it explicitly. Do not pretend it loaded.)

---

## Success checklist

You are done when each box is true:

- [ ] Your diff shows **two** specific, checkable rules in the instructions.
- [ ] Triage Reviewer has the right name, a clear body, and **only** `read` and `search` tools.
- [ ] The skill has a matching name, a specific description, a policy reference with two worked examples, and links to the reference and the script.
- [ ] `npm run check:customizations -- --require-lab1` and `npm test` both pass.
- [ ] You wrote down, honestly: explicit use worked? automatic selection loaded / not selected / cannot verify?
- [ ] You did **not** implement any app feature (that starts in Lab 2).

## Reflect (write one sentence each)

1. Which of the three pieces (rules, agent, skill) would you reach for to say
   "never push to the main branch"? Which for "here is how we calculate
   discounts"? Which for "a reviewer who only reads"?
2. Why is a read-only reviewer *more trustworthy* than a reviewer who can also edit?
3. What is the difference between a skill being **available** and being **used**?

## Hint ladder

Try each rung in order. Do not skip to the last one.

1. **Which tool for which job?** Broad rules go in instructions. A reusable role
   goes in an agent. A procedure with reference material goes in a skill.
2. **Agent file.** Minimal fields: `name`, `description`, `tools`. The setup
   script already added the right `target`.
3. **Skill file.** Links are written relative to `SKILL.md`, and the folder name
   must match `name:`. A reviewer reads a script; it cannot silently gain the
   ability to run it.
4. **Instructor catch-up.** Run `npm run workshop:apply -- lab1-copilot` (or
   `lab1-local`). It installs finished reviewer and skill files and backs up
   yours first. You still need to add the two instruction rules and do the
   explicit/automatic checks yourself. Then read the finished files and explain
   each field.

**Stuck or went off the rails?** See [restore](../restore.md) to undo with your
backup ID, or [troubleshooting](../troubleshooting.md).

## Challenge (optional)

- Add a third boundary case to the reference and re-run the script.
- Write a one-line "description" for the reviewer that would help an agent
  decide *when* to call it. Is it specific enough?

## Where we are going next

You now have a **team of tools**: rules, a safe reviewer, and a recipe. In
[Lab 2](lab-2.md) you hire a **coordinator** who uses them: it delegates
research to the reviewer, then builds the first real feature, priority, and
proves it works.

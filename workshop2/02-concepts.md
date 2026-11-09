# Concepts in plain English

**Read this before the workshop (about 10 minutes), and keep it open during the
labs.** Every idea below is explained with an everyday comparison first and the
technical name second. If you only remember the comparisons, you can still
follow every lab.

## The big picture in one table

| Idea | Everyday comparison | One sentence |
|---|---|---|
| **Agent** | A helpful assistant who can *do* things, not just talk | It reads files, edits files, and runs commands to finish a goal you describe |
| **Custom instructions** | The house rules poster on the office wall | Short rules every agent in this project should follow |
| **Custom agent** | A job description for one role | A saved role with its own instructions and its own allowed tools |
| **Tools** | The assistant's hands | What an agent is *allowed* to do: read, search, edit, run commands |
| **Skill** | A recipe card with ingredients in the drawer | A folder of how-to steps, reference notes, and scripts an agent can pull out when needed |
| **Subagent** | Asking a colleague to research something and report back | A helper that works in its **own separate conversation** and returns a summary |
| **Context** | A desk | The limited space an agent can keep in view at one time |
| **Contract** | A plug and socket agreeing on a shape | A promise about what goes into and comes out of a piece of code |
| **Ownership** | A "reserved" sign on a desk | Who is allowed to change which files |
| **Worktree** | A separate desk with its own copy of the papers | A second folder for the same project, so changes cannot collide |
| **Integrator** | An editor-in-chief | The one person or agent who combines everyone's work |
| **Gate / test** | A checkpoint at the door | A command that must pass before work counts as done |
| **Evidence** | A receipt | Proof you can check: a command, its result, a screenshot |

## 1. Agents, and why we give them guidance

A normal chat answers questions. An **agent** takes a goal ("add search to the
board"), then decides on its own steps: it looks around the project, makes edits,
runs tests, reads the results, and tries again.

That power is useful and also risky, because an agent only knows what is in front
of it. If you do not tell it the rules, it guesses. Most of what you learn today
is *how to give agents the right guidance, the right limits, and the right
checks* so you can trust the result.

Remember this sentence for the whole workshop:

> **An agent is only as good as its instructions, its boundaries, and the proof
> you demand from it.**

## 2. The three ways to guide an agent

New users often mix these up. They solve three different problems:

| You want to... | Use | Comparison | Lives in |
|---|---|---|---|
| Set **project-wide rules** ("tests must pass before you say done") | **Custom instructions** | House rules poster | `.github/copilot-instructions.md` |
| Create a **reusable role** with limited abilities ("a reviewer who can only read") | **Custom agent** | Job description | `.github/agents/*.agent.md` |
| Teach a **procedure with reference material** ("how our scoring policy works") | **Skill** | Recipe card + drawer | `.github/skills/<name>/SKILL.md` |

Two easy mix-ups to avoid:

- **A skill does not give an agent new abilities.** A recipe card does not give
  you a stove. If an agent has no "run commands" tool, a skill that says "run
  this script" cannot make it run anything. Skills teach *what to do*; tools
  decide *what is allowed*.
- **Rules are advice, not locks.** Instructions and agent files *guide* behavior.
  They are not a security fence. This is why we also check results with real
  tests and why we say what an agent "must not do" *and* give it only the tools
  it needs.

## 3. Tools: giving the right hands to the right role

An agent can only do what its **tools** allow. The ones in this workshop:

| Tool | Lets the agent... | Risk |
|---|---|---|
| `read` | Open files | Low |
| `search` | Find text and files | Low |
| `edit` | Change files | Medium: it can break things |
| `execute` | Run terminal commands | Higher: it can do almost anything you can |
| `agent` | Ask a subagent for help | Adds cost and coordination |

**Least privilege** means giving each role only what it needs. A reviewer never
needs `edit`. If the reviewer cannot edit, it cannot accidentally "fix" things
while you only wanted an opinion. You will build exactly such a reviewer in Lab 1.

## 4. Subagents: a colleague with a clean desk

A **subagent** is a helper the main agent asks for help. The crucial detail is
that the subagent gets its **own separate conversation** ("a clean desk"). It
does the research, then hands back a short report. Your main conversation does not
fill up with every file it opened.

```text
 You ----> Main agent ----"please research X, read-only"----> Subagent
                |                                                 |
                | <------ short report: facts and file names -----+
                v
          decides and acts
```

Why this helps:

- **Focus:** the main agent keeps a tidy desk (context).
- **Safety:** you can give the subagent read-only tools.
- **Quality:** a fresh pair of eyes reviewing is less biased by how the code was
  written.

Three honest limits you should know:

1. **A subagent does not remember your conversation.** You must write a
   self-contained brief: the goal, the relevant files, the rules, what to return,
   and when to stop. We call this a *brief*, and we practice it.
2. **A separate conversation is not a separate copy of the files.** Two agents
   can still edit the same file at the same moment. Separate *thinking* is not
   separate *workspace*. That is the entire topic of Lab 3.
3. **A subagent adds cost and time.** For a tiny lookup, just ask directly.
   Delegate when the job is clear and you want to keep the main conversation clean.

## 5. Context: why a short, clear brief wins

An agent can only hold so much in view at once. Think of it as a desk. If you
pile on everything, the important page gets lost. This is why we:

- ask subagents to **return summaries**, not dumps of everything they read;
- **name the exact files** instead of saying "look around";
- write rules that are **short and testable** instead of long and vague.

"Be an expert and write great code" is vague. "Cite the reference file when you
explain a scoring rule" is testable. Prefer the second kind.

## 6. Working in one project without collisions

Imagine two cooks editing the same recipe on one sheet of paper at the same time.
One crosses out a line while the other writes on it. That is what happens when two
agents edit the same file. It is easy to do by accident, so you plan against it.

The techniques you will learn, from lightest to strongest:

| Technique | Comparison | What it does | What it does *not* do |
|---|---|---|---|
| **One owner per file** | Name tags on desks | Each file has exactly one allowed editor | Does not physically stop anyone; it is an agreement |
| **A frozen contract** | A plug-shape standard | Everyone agrees on inputs/outputs before building | Does not catch behavior mistakes by itself |
| **Read-only helpers + one writer** | Many researchers, one author | Only one agent changes files | A bit slower than everyone writing |
| **A task board with leases** | A sign-up sheet | Records who is working on what | A "lease" is a courtesy, not a lock |
| **One integrator for shared files** | An editor-in-chief | One agent combines work, serializes shared edits | Needs someone to do the integrating |
| **Gates (tests) after combining** | A checkpoint at the door | Proves the *combination* works | Only tests what the tests cover |
| **A separate worktree** | A separate desk with its own papers | Files and the staged-changes area are isolated | Does **not** isolate network ports, running servers, or secrets |
| **Branch + pull request review** | A review meeting before publishing | A human reviews before anything merges | Only catches what the reviewer notices |

> **Key idea:** There is no single magic fix. Worktrees are excellent, but they
> only separate *files*. Two copies of the app still fight over the same port
> number if both try to start a server on port 3000. Strong teams combine
> several techniques.

### What is a worktree, really?

Normally one project lives in one folder. A **Git worktree** gives the same
project a *second folder* on a separate branch. Each folder has its own files, so
an agent editing in folder B cannot overwrite your changes in folder A. Later, you
bring B's changes back through a normal Git merge or pull request.

Both the **GitHub Copilot app** and the **VS Code Agents window** can start a
session in its own worktree, depending on the version and your settings. Always
confirm the **session path and workspace** shown for each session before you
assume it is isolated. In this workshop we also learn the technique
that works when you cannot or do not want to use one: clear ownership plus one
integrator.

## 7. Where you do this work

There are two places to run agent sessions. They share the same ideas:

| Place | What it is | Good for |
|---|---|---|
| **GitHub Copilot app** | A desktop app for running agent sessions across your projects | Running several tasks side by side, often each in its own isolated copy (check the session path to be sure) |
| **VS Code Agents window** | An agent-first window inside VS Code (select **Open in Agents**, or run `code --agents`) | Directing agents while still having VS Code's editor and tools nearby |

Either works for every lab. Use whichever you already have installed.

### What is a harness?

A **harness** is the "engine room" that actually runs your agent session. In
VS Code you can choose between at least two:

| Harness | Name you may see | Notes for this workshop |
|---|---|---|
| **Copilot** | The newer default in VS Code and the GitHub Copilot app | Delegation to subagents is built in; skills can be preloaded into a custom agent with `skills` |
| **Local** | The VS Code built-in agent runtime | Uses the `agent` tool and an `agents` allow-list to name which helpers a coordinator may call; no `skills` field |

The two read slightly different agent files. We provide the right version for
each (`npm run workshop:setup -- copilot` or `-- local`). **Pick one and stay with
it for the whole workshop.** If you are unsure, choose `copilot`.

> **Beginner trap:** the file field `target: vscode` or `target: github-copilot`
> tells the *editor* which rules to use when checking your file. It does not
> change which harness your session runs in.

## 8. Proof beats promises

A modern agent writes fluent, confident sentences. Fluent is not the same as
correct. We use three habits throughout:

1. **Run the gate.** `npm test` and the lab's acceptance command must pass.
2. **Say what you did not run.** In reports, `NOT RUN` is a perfectly good
   answer. A false "all tests pass" is the only bad answer.
3. **Look at it.** After a change, refresh the board and see the result.

Even the reviewer agent obeys this: because it cannot run commands, it returns
commands marked `NOT RUN` for a human to run.

## Glossary

| Term | Meaning |
|---|---|
| **Acceptance test** | An automated check that says "this lab's feature behaves exactly as specified" |
| **Agent** | An AI assistant that can take actions toward a goal |
| **Backup ID** | A label printed by workshop scripts so you can undo a change with `npm run workshop:restore` |
| **Brief** | A self-contained task description for a subagent: goal, files, rules, output, stop |
| **Contract** | A written promise about what a function accepts and returns |
| **Coordinator** | An agent whose job is to split work and combine results |
| **Custom agent** | A saved role (`*.agent.md`) with its own instructions and tools |
| **Fixture** | Sample data used for tests; here, the eight made-up issues |
| **Frontmatter** | The small block of settings between `---` lines at the top of an agent or skill file |
| **Gate** | A check that must pass before moving on |
| **Handoff (export)** | In this app, a JSON file listing the urgent issues for engineers. (Not the VS Code "handoff button".) |
| **Harness** | The runtime engine for an agent session (Copilot or Local) |
| **Integrator** | The single role that combines parallel work and edits shared files |
| **JSON** | A plain-text format for structured data that programs can read |
| **Lease** | A courtesy claim that you are working on a task; not a lock |
| **Least privilege** | Give each role only the tools it needs |
| **Orchestration** | Planning and combining the work of several agents |
| **Read-only** | Able to look but not change anything |
| **Skill** | A folder with `SKILL.md`, references, and optional scripts that teach a procedure |
| **Subagent** | A helper that works in its own context and returns a report |
| **Triage** | Sorting problems by how urgent they are |
| **Worktree** | An extra working folder for the same Git repository |

## Next

Continue to the [preflight checklist](preflight.md), then back to the
[start page](README.md).

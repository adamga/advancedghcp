# Lab 3: Two features at once, without anyone trampling anyone

**40 minutes | workshop clock 02:05 - 02:45 | App changes: search (Task A) and summary (Task B)**

## Why this lab exists

**The problem.** Sam needs two more things from the board: a **search box** that
narrows the list, and a **summary line** that says how many issues are visible,
active, and blocked. They are independent: neither needs the other to be built
first. So it is tempting to give each one to a different agent and let them run
**at the same time**, which is faster.

**The danger.** Imagine two builders remodeling the same house at the same time
with no plan. One moves a wall while the other hangs a picture on it. Two
agents editing one repository can do the same:

- both edit the same file, and the second silently erases the first's work;
- one "helpfully" changes a shared file that the other relies on;
- both stage Git changes at once and mix their work together;
- both start a server on the same port and one crashes.

**The fix: orchestration.** Orchestration means *planning who touches what,
before anyone starts*. You will use four ideas from the [concepts guide](../02-concepts.md),
and the first three work in a single checkout. A worktree is only one extra option:

| Technique | Everyday comparison | What it does |
|---|---|---|
| **Ownership** | Reserved-desk signs | Each task gets *its own files*. Nobody else touches them. |
| **Frozen contract** | A standard plug shape | Agree the exact input/output of each piece first, so pieces fit without talking to each other. |
| **Integrator** | The editor-in-chief | One person owns shared things (the final check, Git, shared files) and puts the pieces together. |
| **Gates** | A quality inspection | Each piece must pass its own test *and* the combined test. |
| *(optional)* **Worktree** | Separate desks in separate rooms | A separate copy of the files for each worker. |

**The scenario.** You are the integrator. Two roles, **Search Worker (A)** and
**Summary Worker (B)**, each own two files. They must never import from each
other, because the contract already says how everything fits together. You
research, assign, build, release, integrate, and prove it.

**What you will have at the end.** A search box that filters the list (try
`payments`), a summary line with real counts, and a written ownership record.
And you can explain why parallel agents in one repository need **agreements**,
and how worktrees, branches, and pull requests each add a different safety.

## Words to know

| Word | Plain meaning |
|---|---|
| **Ownership / lease** | "These files are mine for this task." It is an **agreement**, not a lock. |
| **Contract** | The exact function inputs and outputs, written down and *frozen* (no changes mid-task) |
| **Integrator** | The one role that owns shared files, Git, and the final combined check |
| **Release** | A worker says "I'm done and stopped editing" before integration begins |
| **Race** | Two actions at once where the order changes the outcome (and one wins by accident) |

## Before you start

- Lab 2 is done (priority works), **or** you ran `npm run workshop:apply -- priority`.
- The baseline is green: `npm test` shows 0 failing.
- Open [contracts](../contracts.md) and find the **search** and **summary** sections.
- **Record your starting state.** Run `git status --short -uall` and keep that
  list. Expect your Lab 1 and Lab 2 files (the `.github/` files, `src/features/priority.mjs`
  and its test). If anything else is listed, sort that out before starting.
  (Optional tip: after a lab you can save it with `git add -A` and
  `git commit -m "Lab 2 done"`, so the next lab's list starts short.)
- **Choose your route now.** Route A in Step 3 is recommended and needs no extra
  setup. Route B (optional) needs two worker profiles that you create *before
  Step 1*; read Route B in Step 3 first if you want it.

## The two tasks at a glance

| | Task A: Search | Task B: Summary |
|---|---|---|
| Plain job | Narrow the list to issues that match what the user typed | Count what is on screen |
| Function | `selectIssues(issues, query)` | `summarizeIssues(visibleIssues)` |
| Owns | `src/features/search.mjs` and `tests/features/search.test.mjs` | `src/features/summary.mjs` and `tests/features/summary.test.mjs` |
| Rule in one line | Every typed word must appear (any case) in title, description or category | `open` = not closed; `blocked` = open **and** blocked; categories count everything shown |
| Gate | `npm run acceptance -- search` (6 checks) | `npm run acceptance -- summary` (6 checks) |
| Depends on | Only the frozen contract | Only the frozen contract (**not on A**) |

**Why the summary must not depend on search.** The app already runs the pipeline
*priority, then sort, then search, then summary*. The summary receives whatever
list is visible. It never needs to know *how* the list got narrowed. That is what
makes them independent, so safe to build in parallel.

## Time plan

| Minutes | Step | You will have |
|---|---|---|
| 0-3 | Read this introduction | The danger and the four techniques |
| 3-8 | 1. Freeze the contract and assign ownership | A written board; you as integrator |
| 8-15 | 2. Two read-only research packets | Two independent reports |
| 15-27 | 3. Implement under one route | Both features, only owned files changed |
| 27-35 | 4. Release, integrate, validate | 12 passing checks and the right counts on screen |
| 35-40 | 5. Limits and alternatives | A map of when to use worktrees, branches, PRs |

---

## Step 1. Freeze the contract and assign ownership (5 min)

**What.** Write down who owns which files, then agree that the contract is
frozen.

**Why.** Collisions are cheapest to prevent *before* work starts. A two-minute
written agreement removes the most common failure ("I thought that file was
mine"). You also decide in advance what happens if someone discovers the
contract needs to change: **everyone stops, and only the integrator edits
shared things.**

**How.**

1. Copy the [task-board template](../templates/task-board.md) to
   `.workshop-reports/task-board.md` (that folder is ignored by Git; make it if
   missing). **Only you, the integrator, edit this board.** Workers report; they
   do not write here. Use role labels, not personal names.
2. In the board, confirm:
   - **A** owns `src/features/search.mjs` + `tests/features/search.test.mjs`.
   - **B** owns `src/features/summary.mjs` + `tests/features/summary.test.mjs`.
   - **Integrator (you)** owns shared server/UI/package/fixture files, Git index
     and branch changes, final combined gates, and the board.
3. Write the stop rule on the board: *"If anyone thinks a signature or shared
   file must change, stop both writers, preserve both diffs, and let only the
   integrator change it."*
4. Set the states: A and B to `researching`, the integrator to `waiting`.

> **Important: what a "lease" is not.** A lease is **an agreement between
> humans and agents**. It is not a lock, a sandbox, or a permission. CODEOWNERS
> routes *review requests*; it does not stop edits. An agent whose tools can edit
> can still edit a file it does not own. That is why *you* check the diff before
> integrating (Step 4), and why the writers get the smallest possible tool list.

**You should see.** A board with two exclusive file sets, a named integrator,
a frozen contract note, and a stop rule. The starter already connects both
signatures to the app, so **no shared file needs to change.**

**If not.**

| Symptom | Fix |
|---|---|
| `.workshop-reports` does not exist | Create the folder. It is git-ignored on purpose. |
| Unsure who should be integrator | In a solo lab, it is you. In a pair, one person; do not share it. |

> **Reflect.** Why must A and B *not* import each other's module? What would go
> wrong if the summary called the search code directly?

---

## Step 2. Two read-only research packets (7 min)

**What.** Get two independent research reports **before** anyone writes code.

**Why.** Same reason as Lab 2: the reviewer cannot change anything, and a
second reading catches misunderstandings early. Doing A and B as *separate*
reports keeps each helper's head clear of the other's task. Subagent context is
separate, but **the filesystem is shared**. Separate heads, not separate rooms.

Ask the coordinator to obtain both reports. If it can run them at the same
time, good; one after the other is fine too. (With the Local harness, each
report is a fresh invocation.)

**Packet A, search research:**

```text
Use Triage Reviewer for read-only task A.
Goal: derive literal query-filter behavior and tests, no implementation.
Read workshop2/contracts.md, src/features/search.mjs, src/app.mjs and the synthetic
fixture schema in src/data/issues.mjs. No workshop2/solutions/.
Invariants: built-ins only, synthetic data, no mutations/network/dependencies,
frozen exports, no shared-file edits; read/search only, no terminal/edit/delegate.
Expected report: matching fields, AND token semantics, empty query, literal .*
case, order/object preservation, owned test cases, acceptance command NOT RUN,
evidence with file/line references, uncertainties. Stop after report.
```

**Packet B, summary research:**

```text
Use Triage Reviewer for read-only task B.
Goal: derive visible-summary behavior and tests, no implementation.
Read workshop2/contracts.md, src/features/summary.mjs, src/app.mjs and the synthetic
fixture schema in src/data/issues.mjs. No workshop2/solutions/.
Invariants: built-ins only, synthetic data, no mutations/network/dependencies,
frozen exports, no shared-file edits; read/search only, no terminal/edit/delegate.
Expected report: total/active/active-blocked/category definitions, empty subset,
closed-blocked case, alphabetical keys, owned tests, acceptance command NOT RUN,
evidence with file/line references, uncertainties. Do not depend on task A. Stop.
```

Two phrases deserve explanation:

- **"AND token semantics"**: if you type two words, an issue must contain *both*.
  `keyboard payments` finds nothing, because no single issue mentions both.
- **"literal `.*`"**: the text typed is matched as plain characters, not as a
  pattern. This is a safety choice: `.*` should match nothing, not everything.

**You should see.**

- **Report A:** search matches title + description + category; case-insensitive;
  trims spaces; empty query returns a *new* array in the *same order* with the
  *same objects*; closed issues are included; `.*` is literal.
- **Report B:** `total` = number supplied; `open` = not closed (so *in-progress
  counts*); `blocked` = open **and** blocked (closed-blocked ISS-105 does **not**
  count); categories count every supplied issue, keys in alphabetical order;
  empty input gives `0/0/0/{}`.
- Both: file/line evidence, commands marked NOT RUN, no edits.

Check both against [contracts](../contracts.md), then set A and B to `ready` on
your board.

**If not.**

| Symptom | Fix |
|---|---|
| Report B says closed-blocked counts as blocked | Wrong: the contract says *active* blocked. Correct it before implementing. This is a deliberate trap. |
| The two reports refer to each other | Re-run the one that drifted; they must be independent. |

> **Reflect.** Each report was checked by *you* against the contract before work
> started. What would have gone wrong if you had accepted both without reading?

---

## Step 3. Implement under one route (12 min)

**What.** Choose **one** route, then build both features with only owned files
changing.

**Why.** There are several valid ways to run this, and the best one depends on
your tools. Picking one *deliberately* is part of the lesson. The recommended
route is also the one with the lowest chance of a collision.

| Route | How it works | Collision risk | Choose it when |
|---|---|---|---|
| **A. Research first, one writer (recommended)** | Reviewer research is parallel; **one** coordinator writes A, then B | Lowest | Always a safe default; best for this lab |
| **B. Two workers in one checkout** | Two worker agents (read/search/edit only), each owning its files, run at once | Medium (shared tree) | Your tool supports it and you want to see the discipline |
| **C. Separate worktrees** | Each worker gets its own folder and branch | Low (files and index separated) | Real projects; see Step 5 |

> If the Copilot app or the Agents window **already gives each session its own
> worktree**, do not fight it. Use Route A, or treat that as Route C. A UI
> label is not proof of where files live.

### Route A: research first, one writer (recommended)

Send the coordinator these two tasks **in order**, attaching each accepted
report to its own task. (Do not rely on shared parent history; the packet must
carry what the writer needs.)

**Task A packet, search:**

```text
Task A: implement selectIssues(issues, query) in src/features/search.mjs and create
tests/features/search.test.mjs. Only those files are yours.
Use workshop2/contracts.md v1 and the accepted search report supplied here.
Trim/lowercase/split whitespace; every literal token must match joined title,
description or category. Empty query returns a new array; preserve input order
and object identity; include closed issues; .* is literal. No input mutation.
No shared server/UI/package/fixture/acceptance/solution/other-task edits,
no network/dependencies/Git/delegation. Do not import summary.
Return changed paths, boundary cases, and npm run acceptance -- search as NOT RUN
if no execution tool. Stop and release your lease before integration.
```

**Task B packet, summary:**

```text
Task B: implement summarizeIssues(visibleIssues) in src/features/summary.mjs and
create tests/features/summary.test.mjs. Only those files are yours.
Use workshop2/contracts.md v1 and the accepted summary report supplied here.
Return available:true,total,open,blocked,byCategory. Active/open means not closed
(including in-progress); blocked means active AND blocked; category counts all
supplied issues with alphabetically inserted keys. Empty gives 0/0/0/{}.
No input mutation or hidden fixtures; no dependency on search.
No shared server/UI/package/fixture/acceptance/solution/other-task edits,
no network/dependencies/Git/delegation. Return changed paths, boundary cases and
npm run acceptance -- summary as NOT RUN if no execution tool. Stop/release.
```

Why these packets are written this way:

| Phrase | Reason |
|---|---|
| "Only those files are yours" | The reserved-desk sign |
| "accepted ... report supplied here" | The writer has an empty head; give it the checked facts |
| "Do not import summary" / "no dependency on search" | Keeps A and B independent |
| "Return a *new* array" / "No input mutation" | Prevents hidden changes to data other code reads |
| "NOT RUN if no execution tool" | The truthful-reporting rule |
| "Stop and release your lease" | Tells you exactly when integration may begin |

### Route B: two workers in one checkout (optional)

Only if your tools support it. **Before Step 1**, as the integrator, create
**Search Worker** and **Summary Worker**
profiles (this is not a contract change, and no worker is running yet), each with only `read`, `search`, `edit`: no
`execute`, web, delegation, or Git (see the instructor guide for the exact
fields). Start two independently prompted sessions that **actually point to the
same checkout**, or use runtime worker delegation. Register both leases on the
board first.

- If these are chats *you* prompt yourself, call them **top-level sessions**, not
  subagents.
- In Local, the coordinator must name each worker in its `agents` list. Make
  that edit before work starts, then **do not edit that shared profile while
  work is running.** In Copilot, "use only this
  worker" is advisory.
- Workers cannot run tests (no `execute`). **You** run each independent check
  after the worker reports done.
- Their file ownership is by agreement. The tool list does not enforce paths.

**You should see (any route).**

- Compared with the starting list you recorded, `git status --short -uall` shows
  **exactly four new or changed files**: the two features and
  their two tests. Nothing in `src/app.mjs`, `public/`, `package.json`,
  `src/data/`, `workshop2/acceptance/`, or `workshop2/solutions/`.
- Neither feature file imports the other.
- Each worker's final message lists changed paths and **NOT RUN** (or real) commands.

**If not.**

| Symptom | Fix |
|---|---|
| A worker edited a shared file | Stop both. Keep both diffs. First save the shared file's change with `git diff --output=.workshop-reports/shared-edit.patch -- <file>` (use a new file name each time). Only the integrator then reverts it, and only if the file holds no change anyone wants (`git restore <file>`, for that shared file only). |
| Two writers changed the same file | That is a collision. Stop both, review the combined diff, pick *one* integration writer, redo the smaller piece. Never overwrite the other's work. |
| Out of time | Catch-up, each separately: `npm run workshop:apply -- search` then `npm run workshop:apply -- summary`. This is a rescue; it is not permission for two writers to overwrite shared files. |

> **Reflect.** Route A is slower than two workers in parallel. When would the
> speed-up be worth the extra risk, and what would you add to protect yourself?

---

## Step 4. Release, integrate, validate (8 min)

**What.** Make sure both writers have stopped, inspect the diff, then run the
checks one at a time and in the browser.

**Why.** Passing each feature's own test **does not prove** the app works
together. The wiring (which sends search results into the summary) is the thing
the combined checks and the browser prove. The order matters too: **release
first**, so nobody is editing while you test.

**How.**

1. **Confirm release.** Both workers have said "done"; mark A and B `released`
   on the board.
2. **Check ownership.** Run `git status --short -uall` and `git diff --stat`.
   Compared with your recorded starting list, only the four owned files should be
   new. If anything else changed, go back to the "If not"
   table in Step 3.
3. **Run the gates.**

   ```text
   npm run acceptance -- search
   npm run acceptance -- summary
   npm test
   npm run smoke
   ```

4. **Restart the app** (`Ctrl+C`, `npm start`), refresh the page, then try these
   four searches and compare:

   | You type | You should see |
   |---|---|
   | *(clear the box)* | **8 visible \| 6 active \| 2 active blocked \| Categories: accessibility 2, payments 2, reporting 2, search 2** |
   | `PAYMENTS` | Cards **ISS-101** and **ISS-105**; **2 visible \| 1 active \| 1 active blocked \| Categories: payments 2** |
   | `KEYBOARD accessibility` | Card **ISS-102** only; **1 visible \| 1 active \| 1 active blocked \| Categories: accessibility 1** |
   | `keyboard payments` | **No cards**; **0 visible \| 0 active \| 0 active blocked \| Categories: none** |

   Notice that `PAYMENTS` finds ISS-105 even though it is **closed**: search
   includes closed issues. The summary then reports 2 visible but only 1 active,
   because the closed one is not active. Seeing the numbers *disagree on purpose*
   is how you know the definitions are right.

**You should see.**

- `npm run acceptance -- search` ends `# pass 6`, `# fail 0`; `summary` likewise.
- `npm test` shows `# fail 0`. The total is 14 plus the tests you added.
  (With catch-up for priority, search, and summary it is **17**.)
- `npm run smoke` prints `HTTP smoke passed: 6 routes, 8 fictional issues, and 404 handling.`
- The four searches above behave exactly as shown.

**If not.**

| Symptom | Fix |
|---|---|
| Acceptance passes but the page shows "unlock in Lab 3" | The server was not restarted. `Ctrl+C`, `npm start`, refresh. |
| `PAYMENTS` shows only one card | The search is skipping closed issues. The contract includes them. |
| `Categories` appear in a strange order | Keys must be inserted alphabetically. |
| Counts differ in `KEYBOARD accessibility` | Check the AND rule: both words, any order. |
| A shared-file change seems necessary | **Stop.** Only the integrator changes shared wiring, then re-run *both* feature gates. In the supplied starter, no change should be needed. |

> **Reflect.** Both feature tests passed before you opened the browser. Name one
> bug that the browser check could still have caught that those tests could not.
> (Hint: wiring.)

---

## Step 5. Limits, alternatives, and a handoff note (5 min)

**What.** Understand what *a single shared checkout cannot protect*, and which
tool fills each gap.

**Why.** In real projects you will not always be able to rely on agreements
alone. Knowing what each safety layer actually protects tells you which one to
reach for.

**How.** Read this section; there is nothing to run. Then write your handoff
note at the end.

**What stays shared in one checkout:** the source files, the working tree, the
Git index and branch, running processes, environment variables, and server
ports. Giving workers `read/search/edit` only removes the terminal "back door",
but still does not lock paths. Subagent context does **not** create a sandbox
or a worktree.

| Safety layer | What it separates | What it does **not** separate |
|---|---|---|
| **Ownership + contract + integrator** (this lab) | *Decisions*: who changes what | Files (agreement only) |
| **Read/search/edit-only tools** | Terminal and Git actions | Which files may be edited |
| **Worktree** (own folder + branch per worker) | Working files and Git index | Ports, network, secrets, and shared services |
| **Pull request** | *Review and merge* | Edits inside a shared folder |
| **One writer, sequential** | Everything (nothing runs at once) | Nothing; it is just slower |

**Worktree alternative (do this later; it is *not* part of the 40 minutes).**
On a clean, committed checkpoint, the integrator creates one worktree per task,
each owner works and tests in its own folder on **different server ports**, each
commits, and then **one integrator** cherry-picks the commits in dependency order
into an integration branch and runs the combined gates. Worktrees separate
files and indexes; they do not separate ports, credentials, or the integration
step. See the [instructor guide](../instructor-guide.md#concrete-optional-worktree-rehearsal) for safe commands
and [restore](../restore.md) for recovery.

**Pull request alternative.** Where your repository workflow allows, separate
branches can become reviewed pull requests, and one integrator merges them in
dependency order. A PR protects review and integration boundaries; it does not
prevent two people from editing the *same checkout*. Opening or pushing a PR
needs explicit permission and is optional.

**Portable no-preview fallback (one chat, one writer).** Get the A report, then
the B report. Freeze both contracts. Implement and test A, then B, then
integrate and run the combined checks. The lesson (ownership, contract,
dependency) is identical. Just say the work was sequential.

**Write your handoff note** (three lines, in `.workshop-reports/`): who owned
what, the chosen route, and the final evidence (commands, counts, searches).

**You should see.** You can state, for each layer in the table, one thing it
prevents and one thing it does not. Your handoff note exists in `.workshop-reports/`.

**If not.** If a row is unclear, reread its right-hand column ("does **not**
separate"). If `.workshop-reports/` is missing, create it; it is git-ignored on purpose.

---

## Success checklist

- [ ] The board shows two exclusive file sets, a named integrator, a frozen-contract note, and a stop rule.
- [ ] Reports A and B were read-only, independent, and checked against the contract before any code.
- [ ] Only four files changed; neither feature imports the other; no shared file changed.
- [ ] `search` and `summary` each show 6 passing; `npm test` and `npm run smoke` pass.
- [ ] The four searches in Step 4 show exactly the cards and counts in the table.
- [ ] You recorded which route you used and when each worker released.

## Reflect (one sentence each)

1. In your own words, what does an **integrator** do that a worker does not?
2. Why can two tests both pass while the app is still wrong?
3. What does a worktree protect, and what does it leave exposed?
4. Why is "lease granted" *not* the same as "access denied to everyone else"?

## Hint ladder

1. Search **filters the list it is given**; summary **counts the list it is
   given**. Neither fetches fixtures or guesses the other's behavior.
2. Search: `tokens.every(...)`. Summary: open is `status !== 'closed'`.
3. For alphabetical category keys, collect and sort the category names before
   building the counts. **Closed-blocked is a deliberate trap**: it is *not*
   active blocked.
4. **Instructor catch-up:** `npm run workshop:apply -- search` and
   `npm run workshop:apply -- summary`, separately. Then explain the ownership
   story and re-run the integration checks.

## Challenge (optional)

- Add a one-line note to your board for how you would split a *third* feature.
  Which files would it own? Does it need anything from A or B?
- Try Route C for real after the workshop, on a scratch branch, using
  the instructor guide's commands.

## Where we are going next

You have a ranked, searchable, summarized board. One missing piece remains: a
**safe evidence export** that Sam can hand to a teammate. In [Lab 4](lab-4.md)
you build it, then do the final review and write an honest report.

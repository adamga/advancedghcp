# Troubleshooting: when something does not look right

**How to use this page.** Find the group that matches your problem, then the row
that matches your symptom. Every row has a **cause** (the *why*) and a **safe next
action**. Understanding the cause is the point: the same idea will explain
problems this page does not list.

> **The one rule.** If something is blocked (an approval, a policy, a missing
> permission), **do not work around it** by loosening security settings or by
> asking a different tool to do the same thing. Use the manual or sequential
> route the lab offers, and write down what happened. A blocked step is a normal
> thing to learn from, not a failure.

## First, three questions that solve most problems

1. **Did I restart the app?** The app has no "auto reload." After any code change,
   press `Ctrl+C` in the terminal, run `npm start` again, and refresh the page.
2. **Am I in the folder I think I am?** Run `pwd` (macOS/Linux) or `Get-Location`
   (PowerShell). Sessions in the Copilot app may use a **different worktree**
   (a separate copy of the folder).
3. **Which harness is my session on?** The Copilot harness and the Local harness
   read some settings differently (see [Concepts](02-concepts.md)).

## Setup and the app

| Symptom | Cause (why) | Safe next action |
|---|---|---|
| `npm` or `node` is not recognized, or Node is below 22 | Preflight is incomplete, or the terminal was opened before installing | Install Node 22+ with your approved installer **before** the timed agenda, then open a **new** terminal |
| PowerShell says `npm.ps1` cannot be loaded | A local policy blocks scripts | Use `npm.cmd` (for example `npm.cmd test`), or an approved terminal. **Do not lower the execution policy.** |
| Port 3000 is already in use | Another program owns it | Pick another port: PowerShell `$env:PORT='3001'; npm start`, macOS/Linux `PORT=3001 npm start`. **Never stop a process you did not start.** |
| The page still shows old behavior after I changed code | The plain server has no file watcher and loads code once | Stop *your own* server with `Ctrl+C`, run `npm start`, refresh |
| `npm install` is slow or fails | You do not need it. The app has **zero dependencies**. | Skip it. Run `npm test` directly. |
| `git clone` fails, or succeeds but the folder has no files | Network or access limit; or you cloned the default branch (`main`), which does not hold the workshop yet | Clone the workshop branch: `git clone -b adamga-workshop-app-and-hands-on-labs https://github.com/adamga/advancedghcp.git advancedghcp-workshop`. If it still fails, ask the facilitator for the offline ZIP |

## "Unfinished" behaviors that are **expected** (not bugs)

The starter is *meant* to be unfinished. Seeing these means your baseline is healthy.

| You see | It means | When it gets fixed |
|---|---|---|
| Every card says `untriaged` | The priority stub is still in place | After Lab 2 |
| Search always returns all eight | The search stub passes everything through | After Lab 3, Task A |
| The summary says "Detailed counts unlock in Lab 3" | The summary stub reports `available: false` | After Lab 3, Task B |
| No export link, or the export route returns `501` | The handoff stub reports `available: false` | After Lab 4 |
| `npm run acceptance -- priority` **fails** | The check is *supposed* to fail until the feature exists | After you build that feature |
| `check:customizations -- --require-lab1` fails with "Lab 1 requires an active Triage Reviewer agent and complete triage-policy skill." | You have not run `npm run workshop:setup -- local` (or `copilot`) yet, so the reviewer and skill are not installed | Run the setup command from Lab 1 Step 1 |
| `check:customizations -- --require-lab1` (or the plain check) fails with "unfinished Lab 1 template" | Setup has installed the templates, but they still contain `TODO` lines | Finish Lab 1. Until you do, the plain check fails as well, which is expected |

**Why they matter.** An honest unfinished state is better than a fake finished
one. If an app *pretends* to be complete, you cannot trust any check on it. **Do
not "fix" these by faking UI numbers or adding a second export route.**

## Agents and skills (Lab 1 and Lab 2)

| Symptom | Cause (why) | Safe next action |
|---|---|---|
| The active-template check fails | A `TODO`, `REPLACE_ME`, or a missing resource path is still in the file | Finish the agent/skill/reference as the lab says. **Do not weaken the validator.** |
| My agent does not appear in the picker | Wrong folder, wrong exact name, wrong harness, a stale session, or a policy | Confirm the file is in `.github/agents/`, the name matches exactly, you are on the intended harness, then start a **fresh** session and look at the real agent list |
| The Local agent errors on a `skills` field | Local and Copilot use **different** file schemas. Local rejects `skills`. | Remove `skills` from the Local file. Use the skill by explicit mention or link instead. |
| The Copilot agent errors on `agents` or `handoffs` | Those are Local-only fields | Use the Copilot version of the file. Do not claim the two have identical features. |
| I changed `target:` but nothing changed at runtime | `target:` only tells the *editor* how to read the file. It does not pick the engine. | Choose the intended harness yourself when you start the session |
| The skill did not load automatically | Automatic selection depends on relevance and is **not guaranteed** | Test **explicit** use first ("use the triage-policy skill"), then test automatic use separately, and record what you actually observed |
| My reviewer could not run a script or test | The read-only boundary is **working** | A person or the writer runs the command; the reviewer reports it as `NOT RUN` |
| A follow-up message cannot reach a Local subagent | A Local subagent call is **stateless**. It does not remember the earlier conversation. | Make a **new** bounded call that restates all the context it needs |
| The subagent ignored a project rule | Custom subagents do not always inherit repository instructions | Restate the key rules in your task packet |

## Delegation, parallel work, and worktrees (Lab 2 and Lab 3)

| Symptom | Cause (why) | Safe next action |
|---|---|---|
| An approval is blocked and nothing can click "allow" | The session has no approved action path (for example, unattended) | Run the approved command yourself or use the manual route. **Never bypass the approval with another tool.** |
| Two sessions see different edits | They are in different worktrees or checkouts, so they have **separate copies of the files** | Check each session's path. Use the one-writer route, or integrate branches on purpose. |
| A worker changed a file it did not own | A **scope breach**. Ownership rules are advisory; nothing blocks it automatically. | Stop all writers, preserve the diff, assign **one integrator** to reconcile, then re-run the dependent gates. See the [collision protocol](restore.md#collision-protocol). |
| Two workers' results do not fit together | The frozen contract was misread or silently changed | Re-read the feature in the [contract](contracts.md); the integrator fixes the seam |
| Two servers fight over a port | Worktrees isolate files, **not ports** | Give each session its own port, for example `PORT=3001` and `PORT=3002` |
| A restore stopped partway | A writer was still active, or the target was invalid | Keep the printed backup ID, stop all writers, inspect the state, and run it again. No destructive reset. |

## "My output does not match" clues

Compare what you see to the exact numbers below. The **likely mistake** column
points you at the cause quickly.

### Priority (Lab 2)

| You see | Likely mistake |
|---|---|
| ISS-105 is not `0 / P3` | The **closed override** runs too late. Closed must win before any bonus is added. |
| 99 users earns a bonus | The comparison should be `>= 100`, not `>`. 100 adds 10; 99 adds nothing. |
| 6 days old earns a bonus | The comparison should be `>= 7`. Seven days adds 5; six adds nothing. |
| The scores are right but the reasons are in a different order | **Reason order is part of the contract**: impact, blocked, users, age |
| You expected a score of exactly 80 to be P1 | A score of exactly 80 cannot occur under these additive rules. Test **75 (P2)** and **85 (P1)** instead. |

### Search (Lab 3, Task A)

| You see | Likely mistake |
|---|---|
| `keyboard payments` returns something | The match is acting like **OR**. It must be **AND**: every word must match. |
| `.*` matches everything | The query is being treated as a regular expression. It must be **plain text**. |
| Closed issues vanished from the results | Search should **not** hide closed matches. It only filters by words. |
| Capital letters change the result | The comparison must be case-insensitive |

### Summary (Lab 3, Task B)

| You see | Likely mistake |
|---|---|
| With the full board, blocked is **3** | A **closed** blocked issue was counted. The full board is **8 total / 6 active / 2 active blocked**. |
| After a search, the summary still says 8 | The summary used the full list instead of the **visible** (filtered) list |
| The categories do not sum to the total | Categories should count **everything visible**, closed or not |

### Export (Lab 4)

| You see | Likely mistake |
|---|---|
| Closed issues appear in the export | Only **active** visible issues belong in it |
| Extra fields or a timestamp | Exactly **four** fields per item, and **no** timestamp (the file must be the same every time) |
| The download works, so I stopped | A working download is **not** proof the tests pass. Record **both**. |

## Optional advanced controls (not required)

Hooks and organization policy can add extra controls, but this starter enables **no
hooks**. VS Code hooks are in preview, and event and schema details differ between
harnesses. Some important cautions, so you do not over-trust them:

- For Copilot command `preToolUse` hooks, an error can *deny* an action, but a
  **timeout falls through to normal permissions**. Do not call that "fail-closed."
- Terminal access can bypass controls that only watch file tools.
- A hook, a `CODEOWNERS` file, a task board, or a separate subagent context is **not
  a complete sandbox**.

Use the [official hooks documentation](https://code.visualstudio.com/docs/agent-customization/hooks)
only for an approved extension task **after** the workshop. Never disable a
warning, approval, or organization policy to make an exercise finish on its own.

## Still stuck?

1. Re-read the **"You should see"** block of the step you are on and compare it
   line by line to your screen.
2. Try the **hint ladder** at the bottom of your lab, one hint at a time.
3. Check [Restore](restore.md) if you think a file was changed by mistake.
4. Ask the facilitator. Bring the exact command you ran and the exact message you
   saw. That is far more useful than "it doesn't work."

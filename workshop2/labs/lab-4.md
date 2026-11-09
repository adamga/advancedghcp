# Lab 4: Ship it honestly (export, review, and a truthful report)

**15 minutes | workshop clock 02:45 - 03:00 | App changes: evidence export (the last missing piece)**

## Why this lab exists

**The problem.** Sam's board ranks, searches, and summarizes. But when Sam hands
work to a teammate, there is no way to take the *current view* with them. The
teammate does not need every detail; they need a short, trustworthy list of
what is active and why it ranks where it does. The **"Download evidence JSON"**
button is hidden because the export is still a placeholder.

**A second problem, bigger than the code.** At the end of any agent-assisted task
someone has to answer: *"Is this actually done?"* An agent will happily say
"Complete!" while a test is failing. A report that overstates its evidence is
the most expensive kind of mistake, because people stop checking.

**The fix.** Two things, both small:

1. Build the export with a **minimal, deterministic shape**: only four fields per
   item, no timestamps, no descriptions, no extras. *Less data is safer data*,
   and the same input always gives the same output.
2. Finish with a **truthful handoff report**. It lists what really ran (with
   results), what did *not* run, what is still limited, and what is *not*
   authorized. It does not say "done" unless the evidence says so.

**The scenario.** The export is the final piece. You will build it, run the
**complete** set of checks, get one last independent review of the *whole*
integrated app, and write the report as a teammate would want to read it.

**What you will have at the end.** A working **Download evidence JSON** button,
all 26 acceptance checks passing, an honest report, and a personal rule for how
you will use agents in your own work.

## Words to know

| Word | Plain meaning |
|---|---|
| **Deterministic** | Same input, same output, every time. No clock, no random values. |
| **Minimal export** | Only the fields a reader needs. Fewer fields = fewer surprises and leaks. |
| **Quality gate** | A check that must pass before something is called ready |
| **Handoff report** | A short, factual summary a teammate can act on without re-reading the chat |
| **Not ready** | The honest answer when any check fails. It is better than "done except the tests". |

## Before you start

- Priority, search, and summary all work (or you used the catch-up for each).
- `npm test` is green, and the app is running.
- A single writer owns `src/features/handoff.mjs` and `tests/features/handoff.test.mjs`.
  **Everyone else stays read-only until that writer stops.**
- The app's "handoff" is a **JSON file download**. It is *not* the Local harness's
  "handoff" button that switches agents. Same word, different thing.

## The export shape you are building

```json
{
  "available": true,
  "schemaVersion": 1,
  "items": [
    { "id": "ISS-101",
      "title": "Checkout stops on an empty basket",
      "priority": "P1",
      "reason": "high impact (+60); blocked workflow (+25); 100+ affected users (+10); 7+ days old (+5)" }
  ]
}
```

Rules: include **only active** issues (closed ones are left out), keep the order
the board shows, take `priority` from `triage.level` and `reason` from
`triage.reasons` joined with `"; "`, and add nothing else. An empty list gives
`{available:true, schemaVersion:1, items:[]}`.

## Time plan

| Minutes | Step | You will have |
|---|---|---|
| 0-1 | Read this introduction | Why export is minimal and honest |
| 1-4 | 1. Implement the export | Two new files (handoff and its test) |
| 4-8 | 2. Run the final gates and look at the result | 26 checks green; real downloaded JSON |
| 8-11 | 3. Get one integrated review | Findings from a read-only reviewer |
| 11-13 | 4. Write the handoff report | A truthful, evidence-based summary |
| 13-15 | 5. Retrospective | One lesson to keep |

---

## Step 1. Implement the export (3 min)

**What.** Ask your single writer to implement `createHandoff` in one file, with
its test in another.

**Why.** The server and the download link are **already wired**. All that is
missing is the function that decides *what goes in the file*. Keeping the
change this small means the review is quick. Choosing to add *nothing extra*
(no timestamp, no description) is a safety decision: a timestamp would make
the file different every time, and descriptions could leak more than the
reader needs.

**How.** Send:

```text
Implement createHandoff(rankedVisibleIssues) only in src/features/handoff.mjs
and create tests/features/handoff.test.mjs. Read workshop2/contracts.md v1.
Return exactly {available:true,schemaVersion:1,items}. Exclude closed issues.
Project exactly id,title,priority:triage.level,reason:triage.reasons.join('; ').
Preserve supplied order, do not re-score/mutate, and add no timestamp or extra
fields. Empty input returns an available empty report.
No server/UI/package/fixture/acceptance/solution/other-feature changes,
dependencies, network, pushes or PRs. Return actual validation or NOT RUN commands.
Stop and release ownership when ready for review.
```

Why it is written this way:

| Phrase | Reason |
|---|---|
| "Return **exactly** ..." | Locks the shape; extra fields would break the contract |
| "Exclude closed issues" | Closed work is finished; the handoff is about what is left |
| "do not re-score/mutate" | The score was already computed in Lab 2. Re-doing it risks a different answer. |
| "no timestamp or extra fields" | Deterministic and minimal |
| "Stop and release ownership" | Marks when review may begin |

**You should see.** Compared with before this step, only
`src/features/handoff.mjs` and `tests/features/handoff.test.mjs` are new or
changed (check with `git status --short -uall`; files from earlier labs may be
listed too, so ignore those). The implementation is a `filter`
(active only) then a `map` (four fields), and it reads the existing `triage`
rather than importing the priority code.

**If not.**

| Symptom | Fix |
|---|---|
| The agent added a `generatedAt` field | Remove it. It makes every export different, which breaks determinism. |
| A shared file was edited | Stop. Save the change with `git diff --output=.workshop-reports/shared-edit-lab4.patch -- <file>`, confirm the file holds nothing you want, then `git restore <file>` and restate the fence. |
| Out of time | Catch-up: `npm run workshop:apply -- handoff` (backs up first). Be ready to explain why minimal is safer than dumping the raw data. |

> **Reflect.** What could go wrong if the export included the full issue
> description and user counts? Who might see that file next?

---

## Step 2. Run the final gates and look at the result (4 min)

**What.** Run the complete set of checks, then try the download yourself.

**Why.** Each feature passed on its own earlier. The **combined** gate now runs
all four features *plus* two integration checks (do the pieces work together?).
After that, *you* look at what a real user would get. Tests tell you the logic
is right; the browser tells you the experience is right.

**How.**

```text
npm run acceptance -- handoff
npm run acceptance -- all
npm test
npm run smoke
npm run check:customizations -- --require-lab1
```

Restart the app (`Ctrl+C`, `npm start`) and refresh. Then:

1. Type `PAYMENTS` and press **Search**. The **Download evidence JSON** link
   appears. Click it.
2. Type `KEYBOARD` and download again.
3. Type `keyboard payments` and download again.

**You should see.**

- `npm run acceptance -- handoff` ends `# tests 6`, `# pass 6`, `# fail 0`.
- `npm run acceptance -- all` ends `# tests 26`, `# pass 26`, `# fail 0`.
  (24 feature checks plus 2 integration checks.)
- `npm test` ends `# fail 0`. With all four features installed it is
  **18 passing** (14 baseline + one owned test file per feature).
- `npm run smoke` prints `HTTP smoke passed: 6 routes, 8 fictional issues, and 404 handling.`
- The customization check passes.

The three downloads:

| You searched | The file contains |
|---|---|
| `PAYMENTS` | **One** item: `ISS-101`, `P1`, reason with **four** parts. ISS-105 is **not** there: it is closed. |
| `KEYBOARD` | **One** item: `ISS-102`, `P2`, reason `medium impact (+30); blocked workflow (+25)` |
| `keyboard payments` | `{"available":true,"schemaVersion":1,"items":[]}`: an empty but *valid* report |

None of them contain descriptions, user counts, or timestamps.

Also do three **manual** checks, because a source test cannot prove them: can you
reach Search, Clear, and Download using only the **Tab** and **Enter** keys; does
the focus outline stay visible; and does the page still read well when the
window is narrow? Write down what you *actually observed*.

**If not.**

| Symptom | Fix |
|---|---|
| The download link never appears | Server not restarted, or `available` is false. Restart and refresh. |
| Acceptance passes with 24, not 26 | You ran `-- handoff` instead of `-- all`. |
| `PAYMENTS` export contains ISS-105 | Closed issues must be excluded. Fix the filter. |
| Customization check fails | A `TODO` remains in a Lab 1 file. Finish it. If you are in fallback mode with no active customizations, the check will also fail while unfinished templates are installed: skip it and write "customization check NOT RUN (fallback mode)" in your report. |

> **Reflect.** The browser checks (keyboard, narrow screen) were manual. Why do
> we write "I observed this" instead of "tests prove this"?

---

## Step 3. Get one integrated, read-only review (3 min)

**What.** Ask the Triage Reviewer for one last look across the **whole** result.

**Why.** Earlier reviews each saw one feature. This one checks the *seams*
between them: does the search feed the summary correctly, and does the export
respect the same visible list? A fresh reviewer with no history of how the code
was written is the most useful kind of second opinion. And remember: **no second
writer "fixes while reviewing."** Mixing the roles brings back the collision
problem from Lab 3.

**How.** Send:

```text
Use Triage Reviewer for one bounded integrated review.
Read the four src/features modules, the task-owned tests, and workshop2/contracts.md.
Invariants: Node built-ins/synthetic-only, no mutation, frozen signatures,
no network/dependencies/shared-file edits; reviewer read/search only.
Check closed overrides, literal AND search, visible-summary consistency,
minimal export fields and truthful evidence. No terminal, edits, or delegation.
Return high-confidence findings with file/line impact, missing cases, suggested
checks marked NOT RUN, and limitations. Stop after report.
```

Read the findings yourself. Decide, as integrator:

- **A real in-scope problem?** Assign it to the owner of that file, wait for them
  to release, then re-run the relevant gate.
- **A suggestion outside the lab's scope?** Note it in the report as a follow-up.
- **Any unresolved failure?** The honest status is **"not ready"**, never
  "complete except for the tests".

**You should see.** A short report with file/line-cited findings (possibly none),
missing cases, and **NOT RUN** commands.

**If not.**

| Symptom | Fix |
|---|---|
| The reviewer says "all tests pass" | It cannot run them. Ignore the claim; rely on *your* output from Step 2. |
| It edits a file | Stop it; check its tools are still `read`, `search`. |

> **Reflect.** Why is it important that the reviewer is *not* the same agent that
> wrote the code?

---

## Step 4. Write the handoff report (2 min)

**What.** Fill in the [report template](../templates/task-report.md) using what
*actually happened*.

**Why.** The report is for the **next person**, who was not in your chat. It
should let them decide what to do without reading a transcript. Reports that
claim more than the evidence supports are how bad changes reach production.

**How.** Copy the template to `.workshop-reports/` and fill every heading with
facts. Be especially careful with **Validation**: write the exact command, its
result (exit code and passed count), and what you *observed* in the browser.
A role that only read code must write **NOT RUN**, and the person who actually
ran it supplies the evidence.

Here is an example of the *tone* to aim for, to use only **after you have
verified each claim yourself**:

```text
Ready for integration review: four feature contracts preserved; all 26 final
acceptance checks passed. PAYMENTS returns two visible issues, summary 2/1/1,
and one active export item ISS-101/P1. No package/shared-server/fixture changes.
All writer leases released. Limit: no persistence or real support workflow.
No push, PR, merge, or cloud deployment is authorized by this handoff.
```

The example is not evidence. Replace each number with **your** actual result.
Also list your honest limits: whether skill loading was verified, which route
you took in Lab 3, and which checks were manual.

**You should see.** A report with objective, owned files, contract version, the
exact commands and results, observed browser cases, known limits, and "no
push/PR/merge authorized".

**If not.**

| Symptom | Fix |
|---|---|
| You are tempted to paste the whole chat | Don't. Summarize the evidence; the reader wants facts, not a transcript. |
| A check failed | Write "not ready" with the exact failing command. That is a good report. |

> **Reflect.** What is the difference between *"all tests pass"* and *"I ran
> `npm run acceptance -- all` and it showed 26 pass, 0 fail"*?

---

## Step 5. Retrospective (2 min)

**What.** Talk to a partner for two minutes.

**Why.** Turning the day into *your own rule* is what makes it stick after the
workshop ends.

**How.** Discuss:

1. What should have been a **direct task** rather than a subagent?
2. Which fact, written explicitly into a brief, **prevented a mistake**?
3. What was **advisory** (an agreement) and what was **actually tool-restricted**?
4. Name **one boundary** you will keep in your own repository.

Write your answer to question 4 as one sentence, for example in
`.workshop-reports/`, so you can paste it into your own project's rules later.

**You should see.** One sentence you could actually use: a specific, checkable
boundary, not "be careful".

**If not.** If your sentence is vague, apply the Lab 1 test: could a reviewer
check it with a yes/no? If not, rewrite it until they could.

Stop at the three-hour mark. [Extensions](../extensions.md) are bonus work.

---

## Success checklist

- [ ] Compared with before Lab 4, only the handoff file and its test changed, and the export has exactly four fields per item.
- [ ] `npm run acceptance -- all` shows **26 pass, 0 fail**; baseline, smoke, and the customization check pass (or fallback limits are stated).
- [ ] `PAYMENTS`, `KEYBOARD`, and `keyboard payments` downloads match the table above.
- [ ] A read-only integrated review was done; findings were fixed by their owner or logged as follow-ups.
- [ ] Your report lists *real* commands and results, manual observations, limits, and the release of all ownership.
- [ ] Nothing was pushed, merged, or deployed without explicit permission.

## Hint ladder

1. The implementation is **filter** (active items) then **map** (four fields).
2. Use the existing `triage` value; do **not** import or re-run priority.
3. A timestamp makes the output different every run, which breaks the contract.
4. **Instructor catch-up:** `npm run workshop:apply -- handoff`. Then run the
   final gates and be ready to explain why a minimal export is safer than a raw
   dump of the fixtures.

## Challenge (optional)

- Ask: "What happens if `reasons` is missing on an item?" and decide whether the
  contract should specify it. Do not change the contract; note it for the next
  version.
- Rewrite your report in **five lines** for a busy manager.

## You did it

You started with an app that did not rank, search, summarize, or export. You
built the *team* (rules, reviewer, skill), delegated research, built features
under clear ownership, integrated them, and told the truth about the result.
The same habits (small contracts, bounded roles, evidence over claims) apply to
every agent-assisted project you will run next.

Next: [Extensions](../extensions.md) if you have time, or read the
[instructor guide](../instructor-guide.md) to teach this workshop yourself.

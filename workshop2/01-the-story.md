# The story: the app, what is missing, and why we care

**Read this before the workshop (about 10 minutes).** It explains the practice
application in plain language, what is missing from it on purpose, why that
matters, and what you will build in the four labs. You do not need to know
JavaScript to follow it. If a word is new, [the concepts guide](02-concepts.md)
has a plain-English definition.

## The 30-second version

You are given a small web page called the **Issue Triage Board**. A fictional
online shop uses it to look at problems that customers have reported. The page
*almost* works: it shows the reported problems. But four useful features were
removed on purpose. Over the next two hours you will put those four features
back, and you will do it the way a modern team does: by directing GitHub Copilot
agents, giving them clear rules, splitting work between them safely, and
checking their claims with real evidence.

The app is the **practice field**. The skill you take home is **how to work with
agents**, not how to write a sort function.

## The scenario: Monday morning at Harbor & Pine

Harbor & Pine is a made-up online shop. Over the weekend customers reported
eight problems. One says checkout breaks when the basket is empty. Another says
the keyboard cannot move through the menu. A few are small, like a typo in a
spreadsheet heading.

Sam, the support lead, has to answer one question before the 10 o'clock meeting:

> **"What should the engineers fix first?"**

Today Sam can only see a flat list of eight problems in the order they were
filed. Sam has to read each one, guess what is urgent, hunt for all the
payment-related ones by eye, count how many are blocked, and then type up a list
for the engineers by hand. That is slow, and it is easy to get wrong when you are
in a hurry.

Your job in this workshop is to finish the board so that Sam gets, in a few
clicks, a ranked list, a search box that works, a one-line summary, and a file
the engineers can use. Along the way you will learn the Copilot habits that let
you do that *safely and with proof*.

## The app in plain words

### What you see on the screen

When you start the app and open it in your browser (`http://127.0.0.1:3000`),
you see one page:

```text
Issue triage board
+--------------------------------------------------------------+
| Search title, description, or category                       |
| [ Try keyboard or payments          ] [Search] [Clear]       |
+--------------------------------------------------------------+
At a glance
  8 visible issues. Detailed counts unlock in Lab 3.     <- the summary line

Support issues
+--------------------------------------------------------------+
| ISS-101                                                      |
| Checkout stops on an empty basket                            |
| [untriaged] [open]                                           |
| A fictional demo store shows an error instead of a hint.     |
| payments | high impact | 140 sample users | 8 days           |
| Blocked workflow                                             |
+--------------------------------------------------------------+
| ISS-102 ...  (one card like this for each issue)             |
```

Each card is one customer-reported problem. The words on a card mean:

| On the card | What it means |
|---|---|
| **ISS-101** | The issue's ID, like a ticket number |
| **Title and description** | What the customer reported, in a sentence |
| **Badge such as `open`** | The status: `open`, `in-progress`, or `closed` (already fixed) |
| **Category** | The area of the shop: payments, accessibility, search, or reporting |
| **Impact** | How bad the problem is for people it hits: high, medium, or low |
| **Sample users** | How many (made-up) customers hit it |
| **Days** | How long it has been waiting |
| **Blocked workflow** | Customers cannot finish what they were doing at all |

### The eight issues

All data is **invented** for the workshop. Nothing is real, and nothing is sent
anywhere.

| ID | Title | Category | Status | Impact | Users | Blocked | Days |
|---|---|---|---|---|---|---|---|
| ISS-101 | Checkout stops on an empty basket | payments | open | high | 140 | yes | 8 |
| ISS-102 | Keyboard focus disappears in the menu | accessibility | open | medium | 45 | yes | 3 |
| ISS-103 | Export heading has a typo | reporting | open | low | 12 | no | 9 |
| ISS-104 | Search ignores uppercase words | search | in-progress | medium | 110 | no | 2 |
| ISS-105 | Receipt uses the wrong sample currency | payments | **closed** | high | 200 | yes | 14 |
| ISS-106 | Small-screen chart overlaps its legend | reporting | in-progress | medium | 80 | no | 7 |
| ISS-107 | Image alternative text is missing | accessibility | open | low | 25 | no | 1 |
| ISS-108 | Saved search loses its label | search | **closed** | low | 5 | no | 4 |

Six are still active. Two (ISS-105 and ISS-108) are **closed**, meaning someone
already fixed them. Remember those two: closed issues are a classic trap. A good
board must not tell engineers to fix something that is already fixed.

### What is under the hood (the "four small pieces")

The app is deliberately tiny. It uses only Node.js (a way to run JavaScript on
your computer), plain HTML, and no outside packages. There is nothing to install
and no account to sign in to.

Think of it as an **assembly line** with a station for each job. A request goes
in at one end (your page asks for the board) and a finished board comes out of
the other:

```text
 the 8 issues
      |
      v
 [1 PRIORITY]  gives every issue a rank:  "how urgent is this?"
      |
      v
 sort the issues from most to least urgent
      |
      v
 [2 SEARCH]    keeps only the issues that match what you typed
      |
      v
 [3 SUMMARY]   counts what is left: "how many, how many blocked?"
      |
      v
 [4 EXPORT]    packages the urgent ones into a file for engineers
      |
      v
 the board you see on screen
```

Each station is **one small file** with **one small job** in `src/features/`.
That design is on purpose. Small files with clear jobs are easy to explain to an
agent, easy to check, and — importantly for Lab 3 — easy to hand to *different*
agents at the same time without them getting in each other's way.

## What is missing, and why it matters

Four stations are in the app, but each one is a **placeholder** that does as
little as possible and says honestly that it is unfinished. This is what you see
today and what that costs Sam:

| Missing piece | What you see today | Why it matters in the real world |
|---|---|---|
| **1. Priority** | Every badge says `untriaged` and cards are in filing order | Without a ranking, a high-impact checkout failure sits next to a typo. People fix what is easy or loud instead of what is important. |
| **2. Search** | Typing in the box changes nothing; you always see all 8 | When there are 8 issues you can scan them. When there are 800 you cannot. Searching "payments" must find every payments issue quickly and reliably. |
| **3. Summary** | "8 visible issues. Detailed counts unlock in Lab 3." | A manager reads the summary line before anything else. "6 active, 2 blocked" tells them whether to worry before they read a single card. |
| **4. Export** | No download button; the export web address answers "not implemented" | Engineers do not live inside the board. They need a file they can attach to a ticket or feed to another tool. |

> **Why placeholders instead of empty files?** A feature that quietly returns
> nothing looks *finished* and is dangerous: it lies. Ours return an explicit
> "untriaged" / "unavailable" / "not implemented" so the app is always honest
> about what it can and cannot do. You will meet the same idea again in the labs:
> an agent that says "I did not run the tests" is more useful than one that
> pretends it did.

## What we will fix

| Lab | Time | We fix | The Copilot skill you practice |
|---|---|---|---|
| **Lab 1** | 30 min | Nothing in the app yet. You build the *team*. | Rules, a read-only reviewer agent, and a skill — the tools that make every later task safer |
| **Lab 2** | 35 min | **Priority** ("what first?") | Delegating: a research helper reads first, then one agent builds, with proof |
| **Lab 3** | 40 min | **Search** and **Summary** at the same time | Orchestration: two jobs in one project without agents trampling each other |
| **Lab 4** | 15 min | **Export** ("hand it to engineering") | Review, an honest report, and what to keep for next time |

When you finish, the board will have:

- cards sorted from most to least urgent, each with a **why** line;
- a search box that finds `PAYMENTS` (two issues) or `KEYBOARD` (one issue);
- a summary line such as `2 visible | 1 active | 1 active blocked | Categories: payments 2`;
- a **Download evidence JSON** button that exports just the urgent, active ones.

### The scoring rule (so it is not magic)

The ranking in Lab 2 is **not artificial intelligence**. It is a simple point
system. The reason to use plain arithmetic is that you can check it with a
calculator. When an agent claims "ISS-101 scores 100," you can verify that.

- Start with points for impact: **high 60, medium 30, low 10**.
- Add **25** if the issue is blocked (customers cannot continue).
- Add **10** if **100 or more** people are affected.
- Add **5** if it has waited **7 or more** days.
- Closed issues always score **0** (already fixed, so never urgent).
- **P1** (urgent) is 80 or more, **P2** (soon) is 40 or more, **P3** (later) is the rest.

Example, ISS-101: high impact 60 + blocked 25 + 140 users 10 + 8 days 5 = **100**,
so **P1**. Example, ISS-102: medium 30 + blocked 25 = **55**, so **P2**.

## The two stories running at the same time

Every lab tells two stories at once. Keep both in mind:

1. **The app story** — what we are building and why Sam needs it.
2. **The Copilot story** — what habit we are practicing and why it matters.

| Lab | App story | Copilot story |
|---|---|---|
| 1 | Prepare the team before the work starts | Give agents *rules*, *roles*, and *recipes* so you do not repeat yourself |
| 2 | Teach the board to rank issues | Hand off work cleanly: research first, build second, prove it third |
| 3 | Add search and summary together | Run several agents without collisions: contracts, ownership, one integrator |
| 4 | Create the engineering handoff | Trust but verify: honest reports beat confident ones |

## The ground rules (and the reason for each)

| Rule | Why |
|---|---|
| Everything is fictional and runs on your own machine | You can experiment without any risk to real data or systems |
| The app has no dependencies; do **not** run `npm install` | Fewer moving parts, nothing to download, nothing that can break the lesson |
| Do not read the instructor solutions until you are stuck | Struggling a little is how the habit sticks. Solutions are there for rescue, not for copying. |
| Never trust "done" without evidence | Agents can be wrong, confidently. A passing test and a visible result are evidence. A sentence is not. |
| When stuck, restore and keep going | Nothing here is permanent. [The restore guide](restore.md) puts you back safely. |

## What to do next

1. Skim [the concepts guide](02-concepts.md) so the vocabulary is familiar.
2. Work through [the preflight checklist](preflight.md) to make sure your
   computer is ready.
3. Return to the [workshop2 start page](README.md) for the schedule.

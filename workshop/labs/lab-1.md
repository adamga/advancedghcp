# Lab 1 - instructions, custom agent, real skill

**30 minutes | workshop clock 01:00-01:30**

Build a reusable read-only reviewer and a real policy skill with a reference and
script. This lab changes customizations, not the four application features.
Prerequisite: [preflight](../preflight.md) passes. Keep
[contracts](../contracts.md) and the [report template](../templates/task-report.md)
open. Do not read instructor solutions yet.

## Steps and pacing

| Lab minutes | Action | Checkpoint |
|---|---|---|
| 0-5 | Inspect starter and choose harness | Eight issues; features explicitly incomplete |
| 5-10 | Improve repository instructions | Two concrete, testable contributor rules added |
| 10-18 | Complete custom reviewer | Named agent, correct target, read/search only |
| 18-26 | Complete skill and reference | Procedure, two worked cases, real script/resource links |
| 26-30 | Validate and try two invocations | Syntax/resource check; explicit and automatic loading recorded separately |

### 1. Inspect, do not "finish everything" (5 min)

Run `npm test` and open the board. Read `.github/copilot-instructions.md` and
`workshop/contracts.md`. Identify the four deliberate incomplete features.
In your chosen surface inspect the **running harness**. For VS Code Copilot/app
choose `copilot`; for an explicitly selected VS Code Local session choose `local`.

Install **unfinished templates**, not solutions:

```text
npm run workshop:setup -- copilot
```

For an explicitly selected Local session use `npm run workshop:setup -- local`.
The command backs up named targets, sets the intended editor target, and creates:
the reviewer profile and the full `triage-policy` folder. It does **not** complete
their TODOs. Write down the printed backup ID. Do not change harness mid-lab.

### 2. Add repository-wide instructions (5 min)

Edit `.github/copilot-instructions.md` with two short, concrete rules. Example
goals: policy explanations must cite the reference; reports must distinguish
inspected checks from executed checks. Avoid vague "be an expert" instructions.

Prompt:

```text
Read .github/copilot-instructions.md and workshop/contracts.md.
Propose two precise contributor rules for this issue-triage exercise:
policy evidence and truthful validation reporting. Explain why each matters.
Edit only .github/copilot-instructions.md after identifying the exact additions.
Do not change app features, dependencies, fixtures, or instructor solutions.
```

Review the diff yourself. A repository rule is broad guidance, not an enforceable
filesystem permission or a guarantee of inheritance in every custom subagent.

### 3. Complete Triage Reviewer (8 min)

Edit `.github/agents/triage-reviewer.agent.md`. Keep `name: Triage Reviewer` and
`tools: ['read', 'search']`. Keep the target installed for your selected harness.
Define its task, input paths, invariant checklist, report fields, and stop.
It must **not** edit files, run terminal commands, use the network, or delegate.

Prompt:

```text
Complete only .github/agents/triage-reviewer.agent.md from its starter template.
Role: read-only issue-triage contract and test reviewer.
Inputs: the task's named files and workshop/contracts.md; read referenced policy
resources only when supplied. No instructor solutions.
Tools must remain read/search only. No edits, execution, web access, or delegation
by the reviewer. Report objective, file/line findings, boundary cases, suggested
commands marked NOT RUN, uncertainties, and the stop condition.
Use the installed target; do not add harness-incompatible fields.
```

Select the agent in a **fresh chat** or refresh discovery using your surface's
supported workflow. Check its actual tools. In VS Code use **Chat: Open
Customizations** if the newer Agents window is missing. `target: vscode` does
not switch the session into Local. Copilot does not accept `agents`/`handoffs`.

### 4. Complete the skill (8 min)

Edit `.github/skills/triage-policy/SKILL.md` and its `references/policy.md`.
Keep required `name: triage-policy` matching the folder and a specific
description. Define when to use it, a bounded procedure, two examples,
boundary cases, and what to do without execution tools. Link to both
`references/policy.md` and `scripts/inspect-fixtures.mjs`.

Use the frozen priority rule in `workshop/contracts.md`, not an invented SLA.
The bundled script is already runnable; inspect it before running it.

Prompt:

```text
Complete the triage-policy skill and its policy reference in
.github/skills/triage-policy/. Use only workshop/contracts.md for the policy.
Include exact scores, reasons, closed override, 99/100 users, 6/7 days,
and fresh outputs/no mutation. Reference the bundled inspect-fixtures script.
State that the script runs from the repo root only when execution is authorized,
and that a read-only reviewer must return NOT RUN commands instead.
Do not implement priority or any other application feature yet.
```

Human-run script, from the repository root:

Windows PowerShell:

```powershell
node .github\skills\triage-policy\scripts\inspect-fixtures.mjs
```

macOS/Linux:

```bash
node .github/skills/triage-policy/scripts/inspect-fixtures.mjs
```

Expected: `Validated 8 synthetic issues; no files changed.` and a fixture table.
A skill is a folder of procedure/resources, not just a clever prompt and not
permission to execute tools.

### 5. Check syntax and skill behavior (4 min)

```text
npm run check:customizations -- --require-lab1
npm test
```

The first check fails while TODOs remain; complete them rather than deleting
checks. It validates the workshop's **small syntax subset**, not every YAML
variant or runtime permission.

In a fresh suitable chat try an **explicit** skill request:

```text
Use triage-policy to explain ISS-101 and ISS-105 and derive boundary test cases.
Read the installed skill and its reference. Do not change files.
If your role cannot run scripts, inspect them and report NOT RUN commands.
```

If `/triage-policy` appears in your surface's slash menu, that is another explicit
invocation path. If discovery is unavailable, attach the installed skill/reference
and state this was a manual context fallback, not verified automatic loading.

In a second fresh chat test **automatic selection separately**:

```text
Explain the fictional issue-priority policy and derive tests for closed issues
and user-count boundaries. Do not edit files.
```

Inspect activity/resources. Record "loaded", "not selected", or "cannot verify".
Automatic selection is not guaranteed. If it was not selected, explicitly
invoke/link the skill for the next lab instead of pretending it loaded.

## Measurable acceptance

Two meaningful instruction additions appear in your diff. The active reviewer
has the correct name/target and **only read/search** tools. The skill has valid
name/description, a complete policy reference, both resource links, and a script
that validates eight synthetic issues. `check:customizations -- --require-lab1`
and `npm test` pass. Your report separately records explicit invocation,
automatic selection, and runtime tool observations. No app enhancement changed.

## Hint ladder

1. Put broad repo rules in instructions, the reusable role in an agent, and the
   domain procedure/resources in a skill. These solve different problems.
2. Minimal shared profile fields: name, description, tools. Add explicit
   `target: github-copilot` or `target: vscode` for the selected harness.
3. Use links relative to SKILL.md; the name must match the parent folder.
   A reviewer reads a script rather than secretly gaining execute tools.
4. Instructor catch-up: `npm run workshop:apply -- lab1-copilot` or
   `npm run workshop:apply -- lab1-local`, then explain each field/resource.
   This installs complete reviewer/skill answers and backs up your work; it does
   not make the human runtime checks or instruction additions unnecessary.

**Common recovery:** missing picker entry -> confirm folder, target, exact name,
fresh session, policy, and effective harness. Unsupported field -> remove only
the incompatible field; do not expand permissions. See
[troubleshooting](../troubleshooting.md). Take a brief stretch during the final
checkpoint; it is included in the 30 minutes.

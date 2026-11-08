# Hands-on route: 120 minutes

Start after the 60-minute presentation/demo. Have a working
[preflight](preflight.md), terminal, browser, and one Copilot-enabled surface.
Use only fictional fixtures. Keep [contracts](contracts.md) open throughout.

| Lab | Minutes | Minimum checkpoint before moving on |
|---|---:|---|
| [1: Customize](labs/lab-1.md) | 30 | Reviewer read/search only; complete skill + reference/script; two invocation checks |
| [2: Delegate](labs/lab-2.md) | 35 | Self-contained read-only report; priority six acceptance checks pass |
| [3: Orchestrate](labs/lab-3.md) | 40 | Two disjoint task records; search and summary six checks each pass; integration evidence |
| [4: Review and hand off](labs/lab-4.md) | 15 | Minimal JSON export; 26 final acceptance checks; truthful report and retrospective |

Choose a path before starting:

- **Copilot in VS Code/app:** use Copilot profiles and explicit delegation prompts.
  In VS Code, inspect subagent activity in the Agents window when available.
- **VS Code Local:** explicitly select Local and use the Local profiles/allowlist.
  Local invocations are stateless; a follow-up requires a new task with full context.
- **No newer UI/delegation:** ordinary chat with one writer and sequential role
  prompts. Record that delegation was simulated, not actually executed.
- **Copilot unavailable by policy/network:** perform the same implementation,
  contracts, tests, review, and handoff manually; the app remains offline.

Do not open the instructor solutions unless a hint or facilitator tells you to.
Ask the agent to avoid them in its task prompt. If an agent cannot execute, you
run the documented commands and attach their real output; never upgrade a
read-only role to broad tools just to make a demo look automatic.

Copy the [report template](templates/task-report.md) and
[task-board template](templates/task-board.md) into an ignored local
`.workshop-reports` folder if you want persistent exercise notes. The human
integrator owns that shared board; workers return reports rather than editing it.
Use [troubleshooting](troubleshooting.md) or [restore](restore.md) when needed.

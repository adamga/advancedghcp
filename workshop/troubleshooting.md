# Troubleshooting without expanding permissions

| Symptom | Likely cause | Safe next action |
|---|---|---|
| Starter feature acceptance fails | Enhancement intentionally incomplete | Run baseline `npm test`; implement only the assigned feature; keep acceptance checks |
| `npm` missing or Node<22 | Preflight incomplete | Use an approved Node>=22 install outside the timed agenda |
| PowerShell blocks npm.ps1 | Local policy | Use `npm.cmd` or an approved terminal; do not lower execution policy |
| Port 3000 occupied | Another process owns it | Use PORT=3001 in your OS syntax; never terminate unknown processes |
| UI still shows old feature behavior | Plain server has no watcher | Stop your own server with Ctrl+C, restart, refresh |
| Search always returns eight | Search stub remains | Complete Lab3A; starter behavior is expected |
| Summary says unavailable | Summary stub remains | Complete Lab3B; do not fake UI counts |
| Export501 or link hidden | Handoff stub remains | Complete Lab4; avoid adding duplicate endpoints |
| Active template check fails | TODOs/resource paths incomplete | Finish agent/skill/reference; do not weaken validator |
| Agent missing | Wrong folder/harness/name or discovery/policy | Confirm .github/agents, exact name, selected runtime, fresh session, actual inventory |
| Local agent fails on skills field | Mixed schemas | Local: remove skills; invoke/link resources explicitly |
| Copilot fails on agents/handoffs | Local-only fields | Use Copilot counterpart; no allowlist/handoff parity claim |
| target changed but runtime unchanged | target is editor interpretation | Start/select the intended harness explicitly |
| Skill not loaded automatically | Relevance selection is not guaranteed | Test explicit invocation/link separately; record observed result |
| Reviewer cannot run a script/test | Read-only restriction working | Human/writer runs command; reviewer reports NOT RUN |
| Tool approval blocked unattended | Session lacks approved action path | Run authorized command interactively/manually; do not bypass approval with another tool |
| Follow-up cannot reach Local subagent | Local invocation is stateless | New bounded invocation with current context |
| App sessions see different edits | Different worktrees/checkouts | Inspect paths; use single-writer route or intentional branch integration |
| Worker changed shared package/server | Scope breach | Stop writers, preserve diff, assign one integrator, review/reconcile and rerun dependent gates |
| Restore stops mid-operation | Concurrent write/invalid target | Keep printed backup, stop all writers, inspect state and snapshot; no destructive reset |

## Output mismatch clues

Priority ISS-105 must be 0/P3 even though blocked/high-impact. If it is urgent,
the closed override came too late. 99 users adds no bonus;100 adds10. Six days
adds none;seven adds5. Exact reason order is part of the output contract.

`keyboard payments` must return no issues: the query is AND, not OR.
`.*` is a literal string, not a regex. Search must retain closed matches.

Full summary is8 total/6 active/2 active blocked. If blocked is3, a closed blocked
issue was incorrectly counted. If filtered summary stays8, summary imported
fixtures or shared wiring passed the wrong subset.

Export should contain only active visible issues, four fields per item, and
no timestamp. A successful download is not proof of passing tests; record both.

## Optional advanced controls, not mandatory fixes

Hooks and policy can add controls, but this starter enables **no hooks**.
VS Code hooks are preview, and harness event/schema differences matter.
For Copilot command preToolUse hooks, errors can deny but timeouts fall through
normal permissions; do not call that fail-closed. Terminal access can bypass
file-tool-only ownership policies. A hook, CODEOWNERS file, task board, or separate
subagent context is not a complete sandbox.

Use the [official hooks documentation](https://code.visualstudio.com/docs/agent-customization/hooks)
only for an approved extension task after the workshop. Never disable a warning,
approval, or organization policy to make the exercise complete automatically.

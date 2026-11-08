# Extensions - outside the 180-minute workshop

Do not add these to the four timed labs. Pick one after the core gates pass.
Start with ownership, a contract, allowed tools, tests, and a stop condition.

| Extension | Suggested time | Independent acceptance |
|---|---:|---|
| Status/category controls | 20 min | Composed filters preserve AND search and visible-summary/export consistency |
| Additional accessibility review | 20 min | Keyboard order, focus visibility,200% zoom, narrow viewport, screen-reader labels documented |
| Compare direct versus delegated work | 15 min | Same task/model/input; report latency, usage, quality, and uncertainty without assuming "more agents" wins |
| Worktree integration rehearsal | 25 min | Disjoint task commits, different ports, single integrator cherry-pick, combined gates |
| Local handoff button | 15 min | Local-only planner profile pre-fills a writer prompt with send:false; clearly distinct from subagent delegation |
| Approved policy/hook experiment | 30 min | Harness-specific schema verified; harmless allowed/denied/timeout cases recorded; no claim of complete sandbox |

For the Local handoff extension use documented `handoffs` with label, agent,
prompt, and `send: false`; inspect the pre-filled prompt before submitting.
Copilot/app does not accept this Local field. Do not add the example to both
profiles or treat a same-conversation transition as a separate worker context.

For worktrees, do not delete working folders or force branches to recover.
For policy experiments, use synthetic paths and approved tools only. The starter
must remain dependency-light and must not acquire authentication, real customer
data, secrets, cloud costs, external AI calls, or production claims.

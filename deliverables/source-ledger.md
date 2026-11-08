# Source ledger and freshness review

Verified by direct fetch of official pages: **7 November 2026 (US Eastern)**.
This is a dated snapshot, not a guarantee of future UI or schema stability.
The source deck was used for visual formatting, not as a factual source.

| ID | Official source | Material supported | Caveat |
|---|---|---|---|
| S1 | [GitHub Copilot app](https://docs.github.com/en/copilot/concepts/copilot-surfaces/github-copilot-app) | GitHub Copilot app | All Copilot plans; organization app policy must be enabled. Modes are not tool permissions. |
| S2 | [App projects (public preview)](https://docs.github.com/en/copilot/how-tos/github-copilot-app/working-with-projects) | App projects (public preview) | Projects are public preview; core labs do not depend on them. |
| S3 | [App sessions, modes and permissions](https://docs.github.com/en/copilot/how-tos/github-copilot-app/agent-sessions) | App sessions, modes and permissions | Workspace choice controls file isolation; permissions and sandboxing are separate. |
| S4 | [VS Code Agents window](https://code.visualstudio.com/docs/agents/run/agents-window) | VS Code Agents window | Branch shares current folder; New Worktree starts from committed files. UI Commit/Create PR skip local hooks; run required checks explicitly. |
| S5 | [VS Code custom agent file reference](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference) | VS Code custom agent file reference | Copilot and Local schemas differ; target changes interpretation, not runtime. Copilot skills field vs Local agents/handoffs. |
| S6 | [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents) | VS Code custom agents | Local handoffs only. Instructions alone are not a permission boundary. |
| S7 | [VS Code subagents](https://code.visualstudio.com/docs/agents/run/subagents) | VS Code subagents | Local invocation stateless, not full-history inheritance. Separate context is not file isolation. Copilot lifecycle differs. |
| S8 | [VS Code agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) | VS Code agent skills | Automatic selection not guaranteed. Full directory needed. Name matches directory. Skills do not grant tools. |
| S9 | [GitHub custom agents and instruction inheritance](https://docs.github.com/en/copilot/concepts/customizations/custom-agents) | GitHub custom agents and instruction inheritance | Custom subagents in CLI do not include repo instructions by default; pass relevant constraints explicitly. |
| S10 | [GitHub delegation and /fleet](https://docs.github.com/en/copilot/concepts/agent-capabilities/choosing-and-delegating-agent-work/delegating-and-parallelizing-work-with-agents) | GitHub delegation and /fleet | /fleet can increase AI usage; delegation does not inherently create worktrees. |
| S11 | [VS Code hooks (preview)](https://code.visualstudio.com/docs/agent-customization/hooks) | VS Code hooks (preview) | VS Code experience preview; Copilot event schema differs from Local. preToolUse timeouts fall through normal permissions, not fail-closed. |
| S12 | [VS Code agent best practices](https://code.visualstudio.com/docs/agents/best-practices) | VS Code agent best practices | Use bounded tasks, relevant context, requirement-focused checks, review and measured usage. |
| S13 | [VS Code Universe releases, 28 October 2026](https://github.blog/changelog/2026-10-28-github-copilot-in-vs-code-universe-releases/) | VS Code Universe releases, 28 October 2026 | Published 28 October 2026. Documents new-session Copilot harness default. Marketplace/connectors preview, computer use experimental. |
| S14 | [Copilot customization compatibility](https://docs.github.com/en/copilot/reference/customization-cheat-sheet) | Copilot customization compatibility | Support differs by IDE/surface; recheck client and organization policy. |
| S15 | [VS Code overview and isolation limits](https://code.visualstudio.com/docs/agents/overview) | VS Code overview and isolation limits | Worktrees are not security boundaries. Host execution location differs from model hosting. |

## Before teaching again
1. Reopen all sources, record date/version, and compare agent fields and tool names.
2. Check installed app, VS Code, Copilot access, harness picker and organization policy.
3. Run the attendee preflight, baseline tests and all instructor solutions.
4. Rehearse all three demonstrations on the actual machine.
5. Keep sequential/manual fallback prompts available; do not replace missing features with claims of enforcement.

## Original workflow guidance
Task claims/leases, write-ownership matrices, one integration writer, contract freezes and changed-path review are teaching techniques, not claims of a built-in cross-agent filesystem lock.

## Media provenance
The editable deck carries the supplied theme and recreates its dark/cyan/purple visual treatment.
All teaching text, task diagrams and interface schematics are original. No presenter or GitHub Expert Services affiliation is implied.
The video uses Microsoft Foundry `gpt-audio-1.5` with the `coral` voice for speech synthesis. It is narrated instruction with code examples, not a recording of a live product demo.

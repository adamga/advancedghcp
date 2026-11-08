# Attendee preflight - outside the three-hour agenda

Allow 15-25 minutes before the session. No cloud account or resource is needed.
Ask the facilitator for an offline source ZIP if GitHub access is unavailable.

## Required access and tools

Use a currently supported VS Code with GitHub Copilot access, **or** the official
GitHub Copilot desktop app for your OS. Sign in with an account enabled for Copilot.
Organization policies, plan/model quotas, network controls, and staged product
availability may limit agents or tools. Check these before class rather than
spending lab time changing policy.

Install Node **22 or newer** with npm, Git, and a modern browser beforehand using
your organization's approved installer. You only need local file-write and local
terminal permissions. A fork or GitHub repository write access is optional:
all required exercises work in a local clone without pushing or creating a PR.

The sample application is offline and dependency-free. Copilot interactions
normally need network access and may consume plan/model allowances; subagents
add usage. Use a model already available within your approved plan and keep
delegation bounded. No Azure resources, hosted AI deployment, paid connector,
marketplace install, cloud-agent job, or MCP server is part of this workshop.

## Windows PowerShell

```powershell
git --version
node --version
npm --version
git clone https://github.com/adamga/advancedghcp.git advancedghcp-workshop
Set-Location .\advancedghcp-workshop
npm test
npm run smoke
npm run check:customizations
npm start
```

Open <http://127.0.0.1:3000>. Stop with Ctrl+C. If port 3000 is already occupied,
use a port you control rather than terminating somebody else's process:

```powershell
$env:PORT = '3001'
npm start
```

If policy blocks `npm.ps1`, use your approved terminal or `npm.cmd test` /
`npm.cmd start`; do not lower PowerShell execution policy for this workshop.

## macOS/Linux terminal

```bash
git --version
node --version
npm --version
git clone https://github.com/adamga/advancedghcp.git advancedghcp-workshop
cd advancedghcp-workshop
npm test
npm run smoke
npm run check:customizations
npm start
```

Open <http://127.0.0.1:3000>. Ctrl+C stops the server. For another port:

```bash
PORT=3001 npm start
```

Do not run `npm install`: this package has zero dependencies. If Node prints a
major version below 22, update it using your approved installation method before
the workshop. `engines` is documentation, not a guarantee your runtime is correct.

## Product availability check

Official documentation was checked **November 7, 2026**. UI labels can move.

**VS Code:** open the cloned folder. Confirm Copilot chat responds. New sessions
default to the **Copilot harness**; inspect the session's harness before selecting
a profile. If available, open the **Agents window** and find **Customizations**
in its sidebar. Otherwise use the ordinary Chat view and Command Palette
**Chat: Open Customizations**, then **Agents** or **Skills**. Local-specific lab
examples require a fresh session explicitly set to **Local**, not just a file
with `target: vscode`. That field changes editor interpretation, not runtime.

**GitHub Copilot app:** add/open your local repository using the supported app
workflow, verify the checkout shown in the session, and confirm you can run a
small read-only request. Use the Copilot profiles, not the Local allowlist/handoff
schema. Projects is public preview and is **optional**: ordinary repository
sessions are enough. Check whether a new session automatically creates a worktree;
for a same-checkout exercise do not assume all sessions see the same folder.

**Both:** confirm that you can see the effective tool inventory for the running
agent. The reviewer should have reading/search, not edit/terminal/network tools.
Approve only expected local exercise operations. If unattended approval is blocked,
run the command yourself or use the manual/sequential route.

**Fallback:** if the Agents window, custom-agent discovery, or native subagent
delegation is missing, use ordinary chat, paste the role instructions, and run
the task prompts sequentially with one writer. Explain that a pasted prompt
does not enforce a read-only tool boundary; disable write/terminal tools when
possible, otherwise keep the role task human-read-only. Do not label two
independent chats as subagent delegation.

## Success checklist

You should see eight fictional issues, untriaged badges, an explicit starter note,
and no export link. Search intentionally still shows all eight until Lab 3A.
Summary details are unavailable until Lab 3B. `npm test` passes 14 starter tests;
HTTP smoke passes; customization check reports zero active exercise agents/skills.
This is correct. Feature acceptance is expected to fail before implementation.

Confirm keyboard Tab reaches the search box, Search, and Clear; the skip link
appears when focused. At a narrow browser width, cards and controls should wrap.
Then stop your app until the live demo/labs, or leave only your own server running.

## Public references

- [GitHub Copilot app concepts](https://docs.github.com/copilot/concepts/agents/github-copilot-app)
- [VS Code Universe release, October 28, 2026](https://github.blog/changelog/2026-10-28-github-copilot-in-vs-code-universe-releases/)
- [VS Code custom-agent file reference](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference)
- [VS Code skills and verification](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [VS Code subagents and harness differences](https://code.visualstudio.com/docs/agents/run/subagents)
- [GitHub custom agents and instruction inheritance](https://docs.github.com/en/copilot/concepts/customizations/custom-agents)

Marketplace is preview, connectors are preview, and computer use is experimental;
none is required. A missing feature is a reason to use the fallback, not to bypass
your organization's restrictions.

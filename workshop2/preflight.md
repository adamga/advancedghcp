# Preflight: get ready before the workshop

**Allow 15-25 minutes, before the session starts. This is not part of the three hours.** (Add about 20 minutes if you also read the story and concepts first: about 35-45 minutes in total.)

Nothing here is difficult, but doing it ahead means the workshop's lab time goes
to *learning*, not to installing and troubleshooting. Each step says **what**
you do and **why**.

> **No cloud account, Azure resource, paid connector, marketplace install, cloud
> agent job, or MCP server is needed.** Everything runs on your own computer. No
> pushing to GitHub or opening a pull request is required either.

## Step 0. Read the story and concepts (10-20 min, optional but strongly recommended)

Read [The story](01-the-story.md) (about 10 min) and [Concepts](02-concepts.md)
(about 10 min; skim it if you are short on time). They explain
what the sample app is, what is missing, why it matters, and what the labs fix.
People who read first get far more from the labs.

## Step 1. Check your tools

**What you need.**

| Tool | Version | Why |
|---|---|---|
| **Node.js with npm** | 22 or newer | Runs the sample app and its tests |
| **Git** | any recent | Gets the code and shows what changed |
| **A modern browser** | current | Shows the triage board |
| **VS Code with GitHub Copilot** *or* the **GitHub Copilot app** | current | Where you will work with the agents |

Install any that are missing using **your organization's approved installer**.
You need local file-write and local terminal permission, nothing more.

**Also check your Copilot access.** Sign in with an account that has Copilot
enabled. Your organization's policies, your plan's model quota, network controls,
and staged product rollouts can limit agents or tools. It is far better to find
that out now than to spend lab time on it. Use a model already available in your
plan, and keep delegation bounded: subagents add usage.

## Step 2. Get the code and run the baseline

**What.** Clone the repository and run four commands.

**Why.** These prove your machine can run the app and its tests. "Baseline"
means the *starting* state, which is deliberately unfinished.

### Windows PowerShell

```powershell
git --version
node --version
npm --version
git clone -b adamga-workshop-app-and-hands-on-labs https://github.com/adamga/advancedghcp.git advancedghcp-workshop
Set-Location .\advancedghcp-workshop
npm test
npm run smoke
npm run check:customizations
npm start
```

### macOS or Linux

```bash
git --version
node --version
npm --version
git clone -b adamga-workshop-app-and-hands-on-labs https://github.com/adamga/advancedghcp.git advancedghcp-workshop
cd advancedghcp-workshop
npm test
npm run smoke
npm run check:customizations
npm start
```

**Do not run `npm install`.** This app has zero dependencies; there is nothing
to install, and skipping it avoids a long, unnecessary download.

**What each command does.**

| Command | Plain meaning |
|---|---|
| `git --version`, `node --version`, `npm --version` | "Are these tools installed, and which version?" Node must print **v22** or higher. |
| `git clone -b ... ` | Download a copy of the workshop from the workshop branch (`-b` picks the branch). The repository's default branch (`main`) does not hold the workshop yet; once the workshop pull request is merged, a plain `git clone <url>` also works. |
| `npm test` | Run the 14 starter tests |
| `npm run smoke` | Start the app briefly, ask it six questions over HTTP, and check the answers |
| `npm run check:customizations` | Check the (currently empty) agent and skill setup |
| `npm start` | Start the board at <http://127.0.0.1:3000>. Stop it with `Ctrl+C`. |

**You should see.**

- `node --version` prints `v22.x.x` or higher.
- `npm test` ends with `# tests 14`, `# pass 14`, `# fail 0`.
- `npm run smoke` prints `HTTP smoke passed: 6 routes, 8 fictional issues, and 404 handling.`
- `npm run check:customizations` prints `Customization subset passed: 8 instructor profiles, complete instructor skill, 0 active agents, 0 active workshop skills.` Zero is correct: *you* create the active ones in Lab 1.
- After `npm start`, <http://127.0.0.1:3000> shows **eight issue cards**, every
  badge reads `untriaged`, a note about the starter state, and **no** export link.
  Search shows all eight no matter what you type. The summary says details
  unlock in Lab 3.

**All of that is correct.** The app is *meant* to look unfinished. Feature
acceptance checks (`npm run acceptance -- priority`) are expected to **fail** at
this point; they pass only after you build each feature.

**If not.**

| Symptom | Safe fix |
|---|---|
| `npm` or `node` not found | Install Node 22+ with your approved installer, then open a **new** terminal |
| Node prints a version below 22 | Update it. The `engines` field in `package.json` is documentation, not a guarantee. |
| PowerShell says `npm.ps1` cannot be loaded | Use `npm.cmd test` and `npm.cmd start`, or an approved terminal. **Do not lower your execution policy.** |
| Port 3000 already in use | Use another port (below). **Do not stop a process you did not start.** |
| `git clone` fails, or the folder is empty | Check you used the `-b adamga-workshop-app-and-hands-on-labs` option (a plain clone of an empty `main` gives no files). Otherwise ask the facilitator for an offline source ZIP and unzip it instead |

### If port 3000 is taken

Windows PowerShell:

```powershell
$env:PORT = '3001'
npm start
```

macOS or Linux:

```bash
PORT=3001 npm start
```

Then open <http://127.0.0.1:3001>.

## Step 3. Check your Copilot surface

**What.** Open the cloned folder in your tool and confirm Copilot answers a tiny
question. Names and menus move around between releases (this was checked
**November 9, 2026**), so look for the *idea*, not the exact label.

**Why.** The labs use custom agents and skills. They are discovered from
`.github/`, and *which engine runs the session* matters, because the two engines
(harnesses) spell some settings differently.

### In VS Code

1. Open the cloned folder. Confirm Copilot chat responds.
2. New sessions default to the **Copilot harness**. **Look at which harness the
   session uses** before you pick an agent. (Why: a file's `target:` line only
   changes how the *editor reads the file*. It does **not** switch the runtime.)
3. If you have the **Agents window**, find **Customizations** in its sidebar.
   Otherwise use the normal Chat view and the Command Palette command
   **Chat: Open Customizations**, then look under **Agents** or **Skills**.
4. If you want the **Local** examples, start a **fresh session explicitly set to
   Local**.

### In the GitHub Copilot app

1. Add or open your local repository using the app's supported flow, and confirm
   the checkout shown in the session is the folder you cloned.
2. Confirm you can run a small **read-only** request.
3. Use the **Copilot** profile examples, not the Local allowlist/handoff schema.
4. The app's **Projects** feature (public preview) is **optional**; ordinary
   repository sessions are enough.
5. **Check whether a new session automatically creates a worktree.** If it does,
   different sessions may see different folders, so do not assume two sessions
   share one set of files. This matters in Lab 3.

### In both

- Confirm you can see the **tool list** of the running agent. A reviewer should
  have reading and search, and no edit, terminal, or network tools.
- Approve only the local operations the exercises call for. If unattended
  approval is blocked, run the command yourself or use the manual/sequential
  route in the labs.

### Fallback if something is missing

If the Agents window, custom-agent discovery, or native subagent delegation is
missing: use ordinary chat, paste the role instructions, and run the prompts one
at a time with **one writer**. Be honest about what that does and does not
prove: a pasted prompt **does not enforce** a read-only boundary. Turn off write
and terminal tools if you can; otherwise a human acts as the read-only reviewer.
**Do not label two separate chats "subagent delegation."** A missing feature is
a reason to use the fallback, **never a reason to bypass your organization's
restrictions.**

## Step 4. Two quick accessibility checks (2 min)

With the app running:

- Press **Tab**. You should reach the search box, **Search**, then **Clear**. A
  **skip link** appears when focused.
- Make the browser window narrow. Cards and controls should wrap and stay readable.

Then **stop your app** (`Ctrl+C`) until the live demo and labs, or leave running
only a server you started yourself.

## Preflight checklist

- [ ] Node 22+, npm, Git, a browser, and Copilot access all work
- [ ] `npm test` shows 14 passing
- [ ] `npm run smoke` passes
- [ ] The board loads at <http://127.0.0.1:3000> showing eight `untriaged` cards
- [ ] I know which **harness** my session uses (Copilot recommended)
- [ ] I read [The story](01-the-story.md) (optional)
- [ ] I know where the [troubleshooting](troubleshooting.md) page is

## Public references

- [GitHub Copilot app concepts](https://docs.github.com/copilot/concepts/agents/github-copilot-app)
- [VS Code Universe release, October 28, 2026](https://github.blog/changelog/2026-10-28-github-copilot-in-vs-code-universe-releases/)
- [VS Code custom-agent file reference](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference)
- [VS Code skills and verification](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [VS Code subagents and harness differences](https://code.visualstudio.com/docs/agents/run/subagents)
- [GitHub custom agents and instruction inheritance](https://docs.github.com/en/copilot/concepts/customizations/custom-agents)

Marketplace and connectors are preview, and computer use is experimental. **None
is required.**

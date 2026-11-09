"""A shorter, visual-first script covering the original workshop's 42 chapters."""

import json
from pathlib import Path

from workshop_content import SLIDES

CHAPTERS = []


def beat(headline, scene, labels, text, *, code="", variant=""):
    return dict(headline=headline, scene=scene, labels=labels, text=text, code=code, variant=variant)


def chapter(*beats):
    original = SLIDES[len(CHAPTERS)]
    CHAPTERS.append(dict(slide=len(CHAPTERS) + 1, title=original["title"].replace("\n", " "),
                         section=original["section"], sources=original["sources"], beats=list(beats)))


chapter(
    beat("Give every helper a job", "team", ["Coordinator", "Researcher", "Builder", "Reviewer"],
         "Welcome to your agent teamwork upgrade! No artificial intelligence doctorate required. Imagine a tiny support team: one person keeps the goal straight, another investigates, another builds, and another reviews. We will give Copilot similarly clear jobs, rather than asking a crowd of helpers to change everything at once."),
    beat("Small app. Real teamwork.", "board", ["Priority", "Search", "Summary", "Evidence"],
         "Our practice app is an issue triage board with fictional support tickets. It is deliberately small. We will add priority, search, a summary, and an evidence export. The interesting part is how we direct the work, protect shared files, and check that the final result actually works."),
    beat("Watch, pause, then try", "flow", ["Watch", "Pause", "Try", "Review"],
         "This is a visual lesson with an artificial intelligence generated voice, not a recording of live product clicks. Pause whenever you want to try an example. The live workshop still lasts three hours: one hour of presentation and demonstrations, followed by two hours of hands-on labs."),
)
chapter(
    beat("Role + recipe + task", "recipe", ["Agent = role", "Skill = recipe", "Prompt = task"],
         "Here is the whole workshop in three pieces. A custom agent is a reusable job description. A skill is a reusable recipe with supporting files. Your prompt is today's task: what to change, what to leave alone, and how to prove success. Different jobs need different tools, not bigger promises."),
    beat("A useful handoff", "brief", ["Goal", "Allowed files", "Checks", "Result"],
         "You will learn to give a helper a small, complete assignment. It needs the goal, the relevant context, the files it may edit, and the result to return. That result should contain evidence and unresolved questions. A confident sentence saying finished is not the same as a verified change."),
    beat("One repo, no collisions", "split", ["Worker A", "Shared file", "Worker B"],
         "You will also learn why two chats can collide in one repository. Separate conversations do not guarantee separate files. We will compare clear ownership, a single integration writer, dependency ordering, and separate worktrees. The best choice is the simplest workflow that keeps the changes understandable and safe."),
)
chapter(
    beat("The three-hour map", "flow", ["60 min together", "30 min lab", "35 min lab", "40 + 15 min"],
         "The event clock is simple: sixty minutes together, then four labs of thirty, thirty-five, forty, and fifteen minutes. Demonstrations are inside that first hour, not extra time. Short check-ins are inside the labs. This self-paced video's running time is separate from the live event schedule."),
    beat("Set up before the clock", "review", ["Node 22+", "Git", "Copilot access", "Passing starter"],
         "Complete the preflight before the workshop. Check Node, Git, your Copilot access, and the starter's tests. The app needs no database, secret keys, or package installation. If an organization blocks a newer feature, use the documented fallback rather than bypassing the policy. Setup should not consume your lab time."),
    beat("Four things to practice", "board", ["Create", "Delegate", "Coordinate", "Hand off"],
         "Lab one creates useful instructions, an agent, and a skill. Lab two delegates research and implements priority. Lab three coordinates search and summary without overlapping writers. Lab four reviews and exports evidence. Each lab has prompts, checkpoints, hints, and separate instructor answers, so you can recover without guessing."),
)
chapter(
    beat("The engine and control room", "flow", ["Model", "Harness", "Tools", "Result"],
         "A model proposes the next useful action. The harness is the control room around it: it supplies context, tools, permissions, and execution. A tool is an action such as reading a file or running a test. Changing the model does not automatically change the harness or its configuration format."),
    beat("A job is not a side quest", "team", ["Custom agent", "Main task", "Subagent", "Returned report"],
         "A custom agent is a definition of a specialist. A subagent is a helper doing delegated work in a separate context. You can select a specialist yourself, or a main agent can call it for a side task. Built-in helpers can be subagents too; you do not need a new profile for every task."),
    beat("Notes are not a workbench", "split", ["Context A", "Same checkout", "Context B"],
         "Context means the notes available to the helper. A session is an ongoing unit of work with its conversation and workspace. Two notebooks can sit on the same desk. Likewise, two separate contexts can still edit the same checkout. Keep the job definition, the delegated call, and the actual workspace separate in your thinking."),
)
chapter(
    beat("Two notebooks, one file", "split", ["Agent A", "shared.mjs", "Agent B"],
         "Here is our first collision. Two helpers have separate conversations, but both reach for the same file. One edit can overwrite the other. Subagents do not automatically get independent worktrees. A separate chat is useful for focus, but it is not evidence of filesystem isolation."),
    beat("Three different protections", "compare", ["Worktree: files", "Permissions: actions", "Sandbox: access"],
         "Three protections answer three different questions. A worktree separates working copies. Tool permissions control actions that need approval. A sandbox can restrict access to files, networks, or credentials. None is a substitute for the others. A worktree is another workbench, not a locked room around your computer."),
    beat("Check all shared resources", "brief", ["Files", "Git index", "Ports", "Outputs"],
         "Collisions are not limited to source code. Helpers in one checkout share its branch and Git index. Servers can fight over a port, and tests can overwrite a report directory. Before parallel writing, identify all the writable surfaces. If the boundaries are unclear, serialize the writes."),
)
chapter(
    beat("Current facts, dated honestly", "review", ["7 Nov 2026", "Official docs", "Actual client", "Recheck later"],
         "The workshop's product facts were checked against official GitHub and VS Code documentation on November seventh, twenty twenty-six. That is a snapshot, not a promise that interfaces never change. Before teaching it later, check the current clients, policy settings, and file references rather than trusting old examples."),
    beat("The default changed", "compare", ["New sessions", "Copilot harness", "Local examples"],
         "The October twenty-eighth VS Code release documents Copilot as the default harness for new sessions. Older examples often assume Local. That matters: some frontmatter fields and delegation tools are different. Always choose the intended harness before copying configuration, and then inspect the runtime behavior."),
    beat("Preview is not a prerequisite", "review", ["Projects: preview", "Marketplace: preview", "Core labs: portable"],
         "The Copilot app is documented for all Copilot plans, subject to organization policy. Its Projects experience is public preview. Marketplaces and connectors have preview limits, and computer use is experimental. Our core labs do not require these features, a cloud job, or external tools. Use the fallback when needed."),
)
chapter(
    beat("A home for agent work", "interface", ["Projects", "Active session", "Changes"],
         "The GitHub Copilot app is a desktop home for agent-driven development on Windows, macOS, and Linux. A Project can coordinate an ongoing goal; a session performs a bounded task. For this workshop, one repository and one small feature are enough. The diagram is an orientation sketch, not a screenshot of your build.", variant="app"),
    beat("Choose the workbench", "compare", ["New worktree", "Current checkout", "Verify path"],
         "When starting a session, choose the environment and workspace deliberately. New worktree gives a separate working copy. Current checkout uses the existing files and can overlap another writer. Read the selector and confirm the actual path. Do not assume the app's parallel sessions make every task independent."),
    beat("Mode and permission differ", "interface", ["Plan", "Interactive", "Autopilot"],
         "Plan lets you review an approach first. Interactive supports collaborative steering. Autopilot suits a clear task. Tool permissions are a separate choice: they decide which actions need approval. More autonomy does not remove your responsibility to inspect the changes and verify the outcome before integration.", variant="modes"),
)
chapter(
    beat("Start with one small plan", "brief", ["Outcome", "Constraints", "Acceptance", "No edits yet"],
         "For the app demonstration, ask for a plan to add one triage behavior. Include the expected result, allowed files, and existing test commands. Ask it not to edit yet. The useful output is a bounded plan with affected paths and checks, not a proposal to rebuild the application."),
    beat("Steer the same session", "interface", ["Correct session", "Small edit", "Complete diff"],
         "Review the plan. Reject surprise dependencies, databases, or unrelated improvements. Then allow the bounded implementation. Watch the changed files while it works. If it drifts, correct the same session with a concrete instruction. Confirm the active workspace before giving feedback; another conversation may be working on a different task.", variant="app"),
    beat("Finished is not proven", "review", ["Read diff", "Run checks", "Try behavior", "Integrate"],
         "When it finishes, read the complete relevant diff and run the checks. Try the actual behavior in the board. An agent's completion message is not the acceptance criterion. If the desktop app is unavailable, do the same plan, implement, and review loop in VS Code."),
)
chapter(
    beat("Open the Agents window", "interface", ["Sessions", "Conversation", "Files + Changes"],
         "VS Code's Agents window puts agent work first, beside the normal editor. Open it with the command Chat: Open Agents window, or code, double dash agents. The sidebar organizes sessions and customizations, the center holds the conversation, and the review pane shows files and changes. Actual controls may vary with your build.", variant="vscode"),
    beat("Select the active pane", "interface", ["Pane A", "Active pane B", "Commands land here"],
         "Several panes can be visible, but only one is active. Select the intended session before feedback, terminal commands, or browser checks. Branch mode uses the selected current folder. New Worktree starts from committed files in a separate directory. Separate panes alone do not isolate edits.", variant="active"),
    beat("Keep work in sync", "flow", ["Editor", "Same session", "Agents window", "Review"],
         "Supported sessions can continue between the editor and Agents window without starting over. Cloud and remote sessions have additional requirements; a remote host must remain available. We keep the core labs local, so you can see the paths, run the commands, and understand exactly where the changes go."),
)
chapter(
    beat("Same file, different rules", "compare", ["Copilot", "Local", "Check runtime"],
         "Sharing an agent filename does not guarantee identical behavior across harnesses. Copilot uses native task delegation and supports a skills field. Local uses the run subagent tool and supports a named agents allowlist and handoffs. These are different contracts. Check both the schema and actual available tools."),
    beat("The target is a label", "code", ["Editor schema", "Not runtime"],
         "The target field tells the editor how to interpret the file. Target vscode means Local interpretation; target github-copilot means Copilot interpretation. It does not switch your session's harness. Select the harness in the interface first. A completion suggestion is helpful, but it does not prove the runtime supports that tool.",
         code="target: vscode\n# Select Local in the session too.\n# target is not a runtime switch."),
    beat("Do not mix the fields", "compare", ["Copilot: skills", "Local: agents + handoffs", "Verify"],
         "Do not paste Local's agents list or handoffs into a Copilot example and expect enforcement. Do not paste Copilot's skills field into Local. The repository has separate examples. If native delegation is missing, run the same roles sequentially with a written handoff. The learning goal is reliable work, not a particular button."),
)
chapter(
    beat("Replace the wish with a brief", "brief", ["Goal", "Context", "Write set", "Checks"],
         "Make this smarter is a wish. Add this exact priority rule, preserve the issue shape, edit only this module and its tests, and run these checks is a task contract. The agent still chooses implementation details, but it no longer needs to invent your business requirements."),
    beat("Show what success looks like", "review", ["Positive", "Negative", "Boundary", "Expected output"],
         "Provide acceptance examples. One case should trigger the new behavior, one should remain unchanged, and one should test the exact boundary. Give the relevant files and existing commands. These examples are more useful than a long persona description or an instruction to be brilliant."),
    beat("Give it a stopping point", "brief", ["Return evidence", "Name unknowns", "Stop at scope"],
         "Finish the brief with the expected report and a stopping condition. Return changed paths, exact checks, results, and remaining risks. Stop when the assigned behavior passes, or report a specific blocker. Do not expand into unrelated cleanup. Small, self-contained briefs make delegation easier to evaluate."),
)
chapter(
    beat("Shared rules live together", "recipe", ["Repo instructions", "Scoped instructions", "Task prompt"],
         "Put durable repository rules in shared instructions: the runtime, test commands, fixture policy, and contract boundaries. The common Copilot file is dot github slash copilot instructions dot markdown. Path-specific instruction files can target selected areas. Keep them short enough to check and consistent with the task brief."),
    beat("Do not assume inheritance", "team", ["Main context", "Explicit brief", "Custom subagent"],
         "Instruction formats and activation differ by surface. AGENTS dot markdown is supported in some experiences, not identically everywhere. GitHub documents that custom subagents in Copilot CLI do not receive repository instructions by default. Pass important invariants explicitly. Do not rely on invisible inheritance to protect shared files."),
    beat("Guidance is not a lock", "split", ["Instruction", "Allowed tools", "Actual edits"],
         "Saying do not edit a file is guidance, not an operating-system lock. Combine instructions with appropriate tools, approvals, scope checks, and review. In lab one, you will write a small shared rule set and prove that your chosen agent and skill actually use the relevant guidance."),
)
chapter(
    beat("A reviewer with a small job", "team", ["Source + tests", "Reviewer", "Findings"],
         "Our first specialist is a reviewer. Its job is to find incorrect behavior and missing tests in the assigned files, then return actionable findings. It does not need to implement the fix. A focused role is easier to verify than a grand persona such as ultimate expert in everything."),
    beat("Tools match the job", "code", ["Read", "Search", "No shell"],
         "Give this reviewer reading and search tools, not editing or terminal execution. Define the report: file, problem, impact, and suggested fix or test. Check actual runtime activity because restrictions differ by harness. A read-only reviewer must not claim it ran tests; execution evidence comes from someone with execution tools.",
         code="name: Triage Reviewer\ndescription: Review assigned behavior\ntools: ['read', 'search']"),
    beat("Test the role, not the name", "review", ["Fresh chat", "Known files", "Check findings", "Check tools"],
         "Start a fresh session with the intended harness and a small file you understand. Ask for a review without repeating the role instructions. Inspect the findings against the source and look at tool activity and workspace changes. Listed in the picker is discovery, not proof that the agent behaves correctly."),
)
chapter(
    beat("A skill is a recipe folder", "recipe", ["SKILL.md", "references/", "scripts/"],
         "A skill is a folder containing a procedure and any supporting resources. Our triage-policy skill has a SKILL dot markdown file, a policy reference, and a fixture inspection script. Copy the whole folder, not just the headline file. Otherwise the recipe can point at missing ingredients."),
    beat("Tell it what and when", "code", ["Name matches folder", "Useful trigger"],
         "The skill needs a name and description in frontmatter. The lowercase, hyphenated name must match the directory. The description explains what it does and when to use it. Refer to supporting files with paths relative to SKILL dot markdown. Keep the steps concrete and tied to the repository.",
         code="name: triage-policy\ndescription: Apply the issue policy\n  when changing priority behavior."),
    beat("A recipe cannot grant tools", "review", ["Invoke", "Inspect activity", "Check output", "No permission grant"],
         "Verify explicit invocation, then test a matching ordinary request separately. Automatic selection is useful, not guaranteed. Check whether the agent read the resource and used the right command. A skill does not grant tools or credentials. A reader-only role can describe a check, but cannot truthfully execute it."),
)
chapter(
    beat("Available, selected, executed", "flow", ["Available", "Selected", "Executed", "Verified"],
         "These are four different checkpoints. A skill can exist on disk without discovery. It can be discovered without selection. It can be selected without successfully running its script. Do not collapse the whole chain into a green installed badge. Inspect the actual activity and the result."),
    beat("Three small probes", "review", ["Matching request", "Unrelated request", "Ambiguous request"],
         "Test a request that clearly matches the skill, one that should not use it, and one that is ambiguous. For triage policy, changing priority should load the policy. Explaining the page layout should not need to run priority checks. Refine the description when observed behavior is wrong."),
    beat("Trust the whole package", "recipe", ["Instructions", "Scripts", "Data access", "Publisher"],
         "Review scripts and resources before using an acquired skill. A skill supplies a recipe; an MCP connection exposes external tools. Approve and review those tools separately. Marketplace availability is not a trust guarantee. The report should distinguish passed, failed, and not run. Missing capability must not become a success-shaped answer."),
)
chapter(
    beat("Role plus recipe", "team", ["Implementer", "Triage policy", "Validation"],
         "Now combine the parts. The implementer is responsible for one change. The triage policy supplies a repeated procedure. The task brief supplies today's acceptance examples and allowed files. This is composition, not magic: each part has a clear responsibility that you can inspect."),
    beat("Copilot can preload skills", "code", ["Copilot harness", "Enabled skill"],
         "Copilot supports naming enabled skills in the agent's skills field. Use the exact skill name and confirm the inventory and actual loading. Preloading is not execution proof. The worker still needs appropriate tools and approvals, and the task still needs a narrow write set.",
         code="target: github-copilot\nskills: ['triage-policy']\ntools: ['read', 'search', 'edit']"),
    beat("Local uses a different path", "compare", ["Local: invoke/discover", "Copilot: skills field", "Same checks"],
         "Local does not accept that Copilot skills field. Use its supported discovery or explicit invocation instead. Do not give a researcher terminal access merely because an implementer uses a test procedure. Compose only what the role needs, then verify the behavior in the selected harness."),
)
chapter(
    beat("Demo: create the reviewer", "code", ["Small role", "Known input", "Read-only activity"],
         "In the live demonstration, create a workspace reviewer through Customizations, then inspect its file. Ask it to review a known small module. Look for useful findings and reading activity, not edits. If the report implies tests passed without execution, correct the role and repeat the small probe.",
         code=".github/agents/triage-reviewer.agent.md\n# Check the selected harness.\n# Inspect actual tool calls."),
    beat("Demo: create the recipe", "recipe", ["Create folder", "Add reference", "Invoke", "Inspect"],
         "Next, create the triage-policy skill with a real policy reference. Invoke it explicitly, inspect its resource use, then try a matching plain-language request. If automatic selection fails, refine the description rather than pretending installation guarantees use. Review the script before trusting its output."),
    beat("Not run is an honest result", "review", ["Passed", "Failed", "Not run"],
         "Finally, request a check that needs an unavailable tool. A good report says not run and explains why. It does not invent browser or test evidence. Lab one gives you time to create these files yourself and collect proof; the demonstration is inside the first hour."),
)
chapter(
    beat("Choose a useful side quest", "team", ["Main task", "Bounded research", "Useful report"],
         "Use a subagent when a separate context contains meaningful independent work. Research a module, implement one owned feature, or review a completed change. Do not split a tiny edit into a crowd of helpers. Delegation adds model usage, waiting, and coordination; it should earn its place."),
    beat("Dependencies still matter", "flow", ["Research", "Plan", "Implement", "Review"],
         "An orchestrator keeps the overall goal, identifies prerequisites, assigns context and tools, then combines results. Fleet mode in the app or CLI can delegate suitable tasks, but it does not make unsafe writes safe. Start with one read-only specialist, then add parallelism only when work is genuinely independent."),
    beat("Know your harness lifecycle", "compare", ["Local: new invocation", "Copilot: own lifecycle", "Pass context"],
         "Local subagent calls are stateless and do not inherit the full conversation. A further Local review needs a new invocation with updated context. Copilot has its own delegation lifecycle. Do not teach one harness's behavior as universal. Always give the worker the important constraints explicitly."),
)
chapter(
    beat("Pack a complete brief", "brief", ["Goal", "Contract", "Allowed actions", "Expected report"],
         "A research brief might say: locate triage behavior, read the contract and tests, do not edit or run commands, and return paths, patterns, and unknowns. Include the fictional-fixture rule and no-dependency constraint. The worker should not need to guess what happened earlier in your main conversation."),
    beat("Name the write boundary", "board", ["Owned module", "Owned tests", "Shared files reserved"],
         "For an implementation worker, replace read-only with the exact files it owns and acceptance examples. If it needs a shared contract change, it must stop and report that decision. Silent scope expansion is not helpful autonomy. The returned report should let the coordinator integrate without rereading every intermediate message."),
    beat("Update the context deliberately", "review", ["Findings", "Missing detail", "Updated brief", "Recheck"],
         "When a handoff is incomplete, identify the missing fact and supply it through the harness's supported lifecycle. For Local, start a new invocation with the relevant findings. Do not assume the earlier worker remembers a follow-up. A concise, self-contained brief is the portable fallback."),
)
chapter(
    beat("Local: one writer", "flow", ["Researcher", "Coordinator writes", "Reviewer", "Evidence"],
         "Our conservative Local pattern has two readers and one writer. The researcher reports, the coordinator implements and validates, and the reviewer inspects. Readers cannot collide with implementation edits. This is a useful first multi-agent design for a small, tightly connected repository."),
    beat("Allow only named workers", "code", ["Local only", "Exact names", "Agent tool"],
         "Local's coordinator can list exact worker names in its agents field. Include the agent tool set. Picker visibility is a separate control: hiding a helper does not automatically prevent model invocation. The Copilot harness does not accept this Local allowlist field. Inspect runtime calls rather than relying on a copied example.",
         code="target: vscode\ntools: ['agent', 'read', 'edit', 'execute']\nagents: ['Researcher', 'Reviewer']"),
    beat("Review, fix, review again", "review", ["Research", "Implement", "Validate", "Fresh review"],
         "The role describes a sequence, not a personality. Research first, implement within scope, validate, then request review. Fix actionable findings and provide updated context for another Local review invocation. At the checkpoint, inspect which files and tools actually changed, not only the frontmatter."),
)
chapter(
    beat("Copilot: same safe plan", "flow", ["Research", "Owned change", "Review", "Integrate"],
         "Keep the same safe plan in Copilot, but use its native delegation and compatible fields. Pass the skill procedure, repository constraints, and expected result explicitly. Naming preferred workers in prose is guidance, not an equivalent Local schema allowlist. One owner still controls shared writes."),
    beat("Do not smuggle Local fields", "code", ["Copilot", "Skill inventory", "No handoffs field"],
         "The Copilot profile can use the agent tool alias and preload triage-policy. Leave out Local's agents and handoffs fields. The target helps the editor interpret the file; the session picker chooses the actual harness. Confirm enabled tools and skill use in the fresh session.",
         code="target: github-copilot\ntools: ['agent', 'read', 'edit', 'execute']\nskills: ['triage-policy']"),
    beat("Fleet is not file isolation", "split", ["Fleet", "Same files?", "Ownership first"],
         "Fleet can help split suitable work, but each helper consumes usage and separate context does not create a private filesystem. If delegation is unavailable, run the roles sequentially with written handoffs. Success is still the correct behavior, intended file changes, honest evidence, and no unapproved scope expansion."),
)
chapter(
    beat("Handoff: switch the driver", "flow", ["Planner", "You review", "Implementer"],
         "A handoff changes the active agent in your conversation. Local can offer a button with a prefilled implementation prompt after planning. This is useful when you want to review a stage before continuing. It is not parallel delegation, and custom-agent handoffs are Local-only."),
    beat("Subagent: get a report back", "team", ["Main agent", "Side task", "Returned result"],
         "A subagent does a bounded side task and returns a result while the main agent keeps ownership. A separate session is independently tracked work with its own workspace choice. These are three different mechanisms. Choose a transition, delegated result, or independently tracked task based on your actual workflow."),
    beat("A manual handoff still works", "brief", ["Plan", "Files", "Checks", "Risks"],
         "A missing handoff button should not block learning. Paste a concise reviewed plan, affected files, checks, and remaining decisions into the next role. If using a Local handoff, send false lets you review the prompt before submission. Preserve the decision point rather than automating past it."),
)
chapter(
    beat("Add the points", "score", ["High 60", "Blocked +25", "Users +10", "Age +5"],
         "Let's make the priority example concrete. Active issues start at sixty points for high impact, thirty for medium, or ten for low. A blocked workflow adds twenty-five. At least one hundred affected users adds ten. At least seven days old adds five. Our first issue totals one hundred points.", variant="sum"),
    beat("Test the exact edge", "score", ["75 = P2", "80 threshold", "85 = P1"],
         "P one starts at eighty points, P two at forty, and lower scores are P three. This additive policy cannot produce exactly eighty, so test the nearest reachable scores: seventy-five is P two, eighty-five is P one. Also test ninety-nine versus one hundred users and six versus seven days.", variant="boundary"),
    beat("Closed beats every bonus", "score", ["Closed", "Score 0", "P3"],
         "Closed issues override the bonuses: zero points, P three, and only the closed-issue reason. Research the contract, implement one owned module, run those cases, then request review. This demo proves a requirement, not merely that an agent wrote code. Lab two supplies the complete specification.", variant="closed"),
)
chapter(
    beat("Spot the hot files", "board", ["Contract", "Package files", "UI wiring", "Fixtures"],
         "Before parallel writing, spot the hot files: shared contracts, package manifests, lockfiles, server wiring, and common fixtures. If two tasks need one hot file, assign it to an integrator or finish that prerequisite first. Asking both workers to be careful is not a coordination plan."),
    beat("The invisible shared stuff", "brief", ["Git index", "Ports", "Reports", "External state"],
         "Also reserve ports, output directories, databases, and external actions. In one checkout, concurrent stage-all commits can scoop up another worker's unfinished files. Different branches in the same folder do not give separate workspaces. Our offline sample removes databases and credentials so the remaining boundaries are easy to see."),
    beat("When unsure, queue the writes", "flow", ["Reader A + B", "Reports", "One writer", "Checks"],
         "If boundaries are uncertain, let readers investigate in parallel and keep a single implementation writer. That may feel less flashy than a swarm, but it is often faster overall because integration stays simple. Identify every writable surface, not only the source module named in the prompt."),
)
chapter(
    beat("Parallel research, single writer", "team", ["Research A", "Research B", "Integrator"],
         "One reader can study priority while another studies the filter controls. Each returns findings; neither changes the shared checkout. The coordinator combines the reports and performs the edit. This keeps useful specialization without overlapping writers or competing Git commits."),
    beat("Propose before applying", "flow", ["Patch proposal", "Check base", "Apply once", "Validate"],
         "Workers can also return proposed patches without applying them. The integrator checks the current file version and applies deliberately. If the base changed, regenerate or rebase the proposal. Do not paste an old whole-file replacement over newer work. A patch still needs review and behavior checks."),
    beat("Small can be sophisticated", "review", ["Useful scope", "Less duplication", "Clear integration"],
         "This pattern fits small repositories, coupled tasks, and newer teams. Two helpers examining one short file may only duplicate effort. Use separate contexts when their work is substantial enough to help. The advanced skill is choosing the workflow, not maximizing the agent count."),
)
chapter(
    beat("Agree on the contract first", "flow", ["Contract v1", "Worker A", "Worker B", "Integrator"],
         "A contract is the agreed input and output shape. Freeze that agreement before splitting work. For example, search and summary both consume the same issue shape. Neither changes it. File disjointness alone is not independence if one worker renames a field the other expects."),
    beat("Own the module and its tests", "board", ["A: search + tests", "B: summary + tests", "Integrator: shared files"],
         "Assign worker A the search module and its own tests, worker B the summary module and its tests, and the integrator the shared wiring and fixtures. Record acceptance checks and dependencies. If a worker needs another owner's file, it pauses and reports the decision rather than quietly expanding its territory."),
    beat("Ownership is an agreement", "review", ["Advisory", "Changed-path check", "Complete diff"],
         "The ownership board is a team convention, not a filesystem lock. Run changed-path scope checks and inspect the combined diff. They can detect an out-of-scope edit, not magically prevent every write. Keep one owner for the board itself, so coordination notes do not become another shared-file collision."),
)
chapter(
    beat("An arrow means wait", "flow", ["Contract", "A + B ready", "Integrate", "Retest"],
         "A dependency arrow means a prerequisite must finish first. If both features need the contract, agree and commit it before launching them. Then independent tasks can run together. List actual prerequisites; do not infer dependencies merely from the order tasks appear in a list."),
    beat("Serialize shared changes", "board", ["Shared config", "Single owner", "One commit sequence"],
         "Manifest, lockfile, shared configuration, and board updates belong to a serialized stage. Let one integrator change them once. Workers report progress back instead of competing to edit the same coordination document. Reserve a single writer for staging and integration in a shared checkout."),
    beat("Green plus green can fail", "review", ["Task A passes", "Task B passes", "Combined check"],
         "Two tasks can pass separately and fail together because their assumptions disagree. Retest the combined application and actual user flow after integration. If the dependency graph is mostly a chain, run it sequentially. Spend the saved attention on clear examples and review rather than artificial parallelism."),
)
chapter(
    beat("A claim is a sticky note", "board", ["Owner", "Paths", "Base revision", "Expiry"],
         "An advisory claim is a sticky note saying who owns which paths, from which base revision, and until when. The coordinator checks conflicts and acknowledges the assignment before writing. At handoff, the worker reports its changed files and releases the claim."),
    beat("Expiry is not overwrite permission", "split", ["Stale claim?", "Inspect state", "Coordinator decides"],
         "An expiry prevents a stale claim from blocking work forever. It does not authorize overwriting an active worker. Inspect the current state and resolve uncertainty. If a worker needs another path, request a new assignment. Markdown and chat claims are protocols, not operating-system mutexes."),
    beat("Combine the protections", "review", ["Claims", "Narrow tools", "Scope checks", "One integrator"],
         "For many small projects, combine advisory ownership, appropriate tools, scope checks, and one integrator. Use worktrees when separate working copies help. Actual locking requires an enforcement mechanism with defined failure behavior. Do not market a task board as a built-in cross-agent security boundary."),
)
chapter(
    beat("Checks have different jobs", "review", ["Detect edits", "Gate integration", "Route review"],
         "A scope check detects changed files outside an assignment. Required continuous integration can gate integration until tests pass. CODEOWNERS routes review to people; it does not lock local edits. These mechanisms are complementary. Be precise about whether a check prevents an action or detects it afterward."),
    beat("A shell is a powerful tool", "compare", ["Read/search", "Edit", "Terminal access"],
         "Give each role only needed capabilities, then inspect actual activity. Terminal execution is broad: a shell can write files even without a separate edit tool. A do-not-edit instruction alone is not a permission boundary. Keep approvals and machine access separate from repository ownership conventions."),
    beat("Hooks need failure tests", "flow", ["Before tool", "Decision", "Normal permissions", "Verify failure rules"],
         "Hooks can run checks before or after tools. VS Code's hooks experience is preview and harness formats differ. A post-tool hook cannot undo a completed action. Copilot command pre-tool errors deny, but timeouts fall through to normal permissions. Test failure behavior; our core labs do not need hooks."),
)
chapter(
    beat("A second workbench", "branch", ["Committed base", "Worktree A", "Worktree B"],
         "A Git worktree provides another working directory, normally on another branch. Independent workers edit separate copies. Start from an agreed committed baseline containing the contract and customizations. Uncommitted agent files, ignored dependencies, and local configuration do not automatically appear in a new worktree."),
    beat("Separate files, shared surroundings", "compare", ["Working copy", "Ports + services", "Sandbox separately"],
         "Worktrees separate working files and indices, not every part of Git or your machine. Give servers different ports and outputs separate locations. They do not protect credentials or external services by themselves. Sandboxing and permission controls address different risks."),
    beat("Commit, review, then integrate", "branch", ["Task commit", "Review", "Integrate", "Combined tests"],
         "A task commit remains on its task branch until you integrate it. Review the scope and evidence, then use your normal merge, cherry-pick, or pull-request workflow. Keep the worktree until integration is verified. Do not delete useful work just because the last response sounded successful.", variant="merge"),
)
chapter(
    beat("Give integration an owner", "flow", ["Review A", "Integrate A", "Integrate B", "Retest"],
         "Integration is a separate stage with one owner. Inspect each task's diff, scope, and test evidence. Integrate one task at a time. If shared assumptions changed, resolve them against the agreed contract before accepting another worker's result."),
    beat("Do not blindly choose a side", "split", ["Change A", "Conflict", "Change B"],
         "A conflict requires reasoning. Read both intentions and preserve the required behavior; do not blindly choose ours or theirs. Even a clean merge can be wrong if the features disagree on fields, filtering, or order. Combining text is not the same as combining correct behavior."),
    beat("Exercise the combined flow", "review", ["Whole suite", "Board behavior", "Expected evidence"],
         "Run the relevant combined checks and try the user flow. In our board, search, priority, summary, and export must agree on the visible issues. Document remaining risks honestly. A useful integration handoff is more than a merge commit or a collection of separate green test messages."),
)
chapter(
    beat("Compare the two patterns", "compare", ["Readers + one writer", "Separate worktrees", "Same checks"],
         "The third demo compares shared-checkout readers with one writer, and committed contracts with separate worktrees. Point out the actual paths and owners, not just separate tabs. Demonstrate a harmless scope violation caught before integration, then correct it rather than accepting an expanded write set."),
    beat("PAYMENTS gives two cards", "filter", ["PAYMENTS", "ISS-101 active", "ISS-105 closed"],
         "Now try the combined example. Searching uppercase PAYMENTS finds issues one hundred and one and one hundred and five. Search includes the closed issue because it matches the category. The visible summary is two total, one active, and one active blocked issue.", variant="payments"),
    beat("Evidence keeps the active issue", "filter", ["Visible: 2", "Export: ISS-101", "P1 evidence"],
         "Evidence export includes only the active visible issue, one hundred and one, with P one and its reasons. That proves all four behaviors agree. Rerun required checks explicitly: some UI commit and Create PR actions skip local Git hooks. The forty-minute orchestration lab gives you the hands-on practice.", variant="export"),
)
chapter(
    beat("Fictional data only", "review", ["Synthetic issues", "No secrets", "Known destination"],
         "Keep the sample fixtures fictional and never paste credentials into task context. If you later connect a tool, inspect its permissions and data destination. Repository text and outside documents are data, not authority to ignore the task's rules or ownership boundary."),
    beat("Review acquired capabilities", "recipe", ["Skill files", "Plugin scripts", "Hooks", "Tool access"],
         "Review acquired skills, plugins, and scripts before enabling them. Hooks may run without the model requesting the procedure. A marketplace listing is not a trust guarantee. Worktrees, sandboxing, and approval policies protect different things; none proves the generated code is correct."),
    beat("Review before external actions", "flow", ["Inspect diff", "Check destination", "Approval", "Action"],
         "Inspect the full diff before committing. Before an external action, confirm its destination and required approval. Our app is local and has no write API, so you can practice these habits without a database or cloud service. Optional media regeneration is separate from the attendee labs."),
)
chapter(
    beat("More helpers is not always better", "team", ["Small task", "Direct edit", "One useful specialist"],
         "Use a direct request for a small cohesive change. Delegate substantial independent work with a bounded result. Repeating the same investigation in several contexts costs more and may not improve the answer. A tiny team with clear jobs often beats an impressive-looking swarm."),
    beat("Bound the depth and cost", "flow", ["Scope", "Stop condition", "Available model", "Usage"],
         "Keep delegation depth bounded and include a stopping condition. Nesting has harness-specific support and is not a core lab requirement. Choose a model actually available to your account and suited to the task. Changing model and changing harness are different experiments."),
    beat("Measure usefulness", "review", ["Correct result", "Coordination effort", "Usage", "Refine"],
         "Measure whether the worker's result was useful and how much coordination it added. Lighter models may handle straightforward tasks. The app offers usage insights such as chronicle, but those are optional. Optimize the workflow, not the agent count, and respect your plan's usage allowance."),
)
chapter(
    beat("Eight fictional issues", "filter", ["8 total", "6 active", "2 active blocked"],
         "Our issue triage board has eight fictional issues, six active and two closed. Two active workflows are blocked. Accessibility, payments, reporting, and search each contain two issues. It runs with Node's built-in HTTP server, a static page, and the built-in test runner.", variant="all"),
    beat("Four deliberate gaps", "board", ["Priority", "Search", "Summary", "Evidence"],
         "The starter passes its baseline checks but intentionally lacks the four lab enhancements. Shared wiring already follows frozen contracts, so workers can own separate modules and tests. Instructor answers live separately and are not hidden inside the normal starter. Do not copy them before trying the exercise."),
    beat("Run the actual app", "code", ["No install", "Passing baseline", "Local browser"],
         "From the repository root, run npm test and npm start, then open the loopback page. No npm install, database, API keys, or Azure account is needed for the app. Use the exact paths and acceptance outputs in the lab files; these diagrams explain the workflow rather than replace the executable specification.",
         code="npm test\nnpm start\n# Open http://127.0.0.1:3000"),
)
chapter(
    beat("Lab one: build the toolkit", "recipe", ["Instructions", "Reviewer", "Policy skill"],
         "You have thirty minutes. Confirm the starter and harness, then write short repository instructions. Create a focused custom agent with only needed tools. Create a matching skill directory, name, description, and supporting resource. Test them on a known small task."),
    beat("Collect actual evidence", "review", ["Discovery", "Invocation", "Activity", "Honest limits"],
         "Show discovery separately from behavior. Inspect tool activity and compare output with the source. Record an explicit skill invocation and a matching plain-language request. Include an unavailable check reported honestly as not run. A listed file or a polished report is not sufficient proof."),
    beat("Explain your choices", "brief", ["Why this role?", "Why this recipe?", "Why these tools?"],
         "At the checkpoint, explain why each rule belongs in instructions, a role, or a skill. Use the hint ladder if you fall behind; the first hint is not the complete answer. The lab's measured outcome is a useful toolkit you can evaluate, not just more customization files."),
)
chapter(
    beat("Lab two: brief the researcher", "brief", ["Goal", "Contract", "Read-only", "Report"],
         "You have thirty-five minutes. Prepare a self-contained research brief with the contract, constraints, allowed actions, and expected report. Use a read-only specialist to find the priority behavior and existing test pattern. Review that report before implementation."),
    beat("Implement and check the edge", "score", ["Positive", "Negative", "Exact boundary"],
         "Keep one writer for the assigned priority module and tests. Use the policy skill to apply the exact rules. Check positive, negative, and boundary cases, including closed override. A nearby example is not proof of the real threshold. Supply test output as execution evidence.", variant="boundary"),
    beat("Get an honest review", "review", ["Source findings", "Actual test output", "Risks", "Scope"],
         "Ask the restricted reviewer to inspect the requirements and changed source. It must not claim command execution it could not perform. If native delegation is unavailable, run the roles sequentially. Hand off the outcome, changed paths, checks, and remaining uncertainty."),
)
chapter(
    beat("Lab three: split safely", "board", ["Contract agreed", "Search owner", "Summary owner", "Integrator"],
         "You have forty minutes. Read the shared contract and the search and summary tasks. Record owners, write sets, prerequisites, and reserved shared files. If both tasks need a contract change, complete it first. Do not send workers out with different assumptions."),
    beat("Claims are advisory", "split", ["Claim", "Scope check", "Conflict = pause"],
         "Compare the one-writer pattern with separate worktrees where available. Exercise claims and handoffs, then use the controlled scope-violation check. Explain whether it prevents a write or detects it later. Shared files, board updates, and Git integration remain with the integrator."),
    beat("Retest the whole board", "review", ["Integrate A", "Integrate B", "Combined checks", "User flow"],
         "Review and integrate one result at a time, then rerun the combined checks and try the board. Separate passing reports are not enough. At debrief, explain what could still collide and what you would do if a worker needed another owner's file."),
)
chapter(
    beat("Lab four: evidence and handoff", "review", ["Full diff", "Quality gates", "User flow", "JSON"],
         "You have fifteen minutes. Review the complete relevant diff and requirement coverage. Run the final checks and user flow, then create the minimal evidence export. Mark unavailable checks not run with a reason. Do not turn missing evidence into a success statement."),
    beat("Help the next developer", "brief", ["Outcome", "Paths", "Checks", "Risks"],
         "Write a handoff someone can use without reading the whole agent history. Include the outcome, changed paths, assumptions, exact checks and results, remaining risks, and next decisions. An evidence-based handoff is the final product, not an agent completion message."),
    beat("Reflect, then finish on time", "team", ["What helped?", "What collided?", "Simpler next time"],
         "Ask which tasks were truly independent, whether separate contexts helped, and where coordination cost more than a direct edit. The live workshop ends at three hours. Hooks, marketplace packaging, and cloud continuity are optional extensions afterward, not hidden extra requirements."),
)
chapter(
    beat("Recover from the actual state", "review", ["Pause", "Inspect", "Narrow", "Rerun"],
         "When work goes wrong, stop expanding the prompt. Inspect the actual files, changes, and evidence. If a customization is missing, check its path, frontmatter, harness, inventory, and committed worktree base. If tools differ, check the runtime rather than only the editor completion."),
    beat("Preserve useful work", "split", ["Writer A paused", "Inspect changes", "One integration owner"],
         "Pause overlapping writers and choose one integration owner. Preserve useful work and resolve the shared contract. Do not run a destructive reset simply to look clean. The lab provides named backup and restore operations that preserve current contents before undoing specific files."),
    beat("Stop is not undo", "flow", ["Stop request", "Completed actions remain", "Recover", "Recheck"],
         "Stopping does not undo completed commands or external actions. Checkpoints can restore some workspace and chat state, not every side effect. Use the appropriate Git or service recovery controls, then rerun affected checks. Recovery is complete when the required behavior is verified again."),
)
chapter(
    beat("Your reliable teamwork recipe", "recipe", ["Role", "Recipe", "Task contract"],
         "Your reliable teamwork recipe is a role, a reusable procedure, and a specific task contract. Choose narrow responsibilities and real acceptance examples. The agent owns a job, the skill supplies a process, and the prompt defines what success means today."),
    beat("The desk is what matters", "split", ["Separate context", "Actual workspace", "Explicit owners"],
         "Separate context does not mean separate files. Freeze contracts, assign owners, serialize shared changes, and use one integrator. Worktrees help separate working copies; permissions and sandboxing solve different problems. Advisory claims help coordination but do not enforce a lock."),
    beat("Evidence wins", "review", ["Read-only cannot run", "Target is not runtime", "Combined tests matter"],
         "Evidence beats confident prose. A read-only reviewer cannot claim it ran tests. Target vscode does not switch the harness. Two passing branches can fail together, so retest after integration. Keep the smallest workflow that reliably proves the outcome. That's the upgrade from agent user to orchestrator."),
)
chapter(
    beat("Keep the sources handy", "review", ["Official ledger", "Dated facts", "Actual versions"],
         "The full package includes the official source ledger, labs, instructor answers, captions, and this video's script. Product facts were checked on November seventh, twenty twenty-six. Recheck them before a later event. Preview features and organization policy can change what appears in your client."),
    beat("Illustrations, not hidden proof", "interface", ["Illustrated controls", "Live client may vary", "Verify tools"],
         "The animated interfaces and team diagrams are original teaching illustrations, not recordings of live Copilot activity. They show concepts; the labs show executable steps. Voice and animation are separate from the offline sample application, and they do not add time to the three-hour live schedule.", variant="vscode"),
    beat("Ready for your small task", "team", ["One goal", "Clear brief", "Useful help", "Proof"],
         "Start with one small task you understand. Give it a clear brief, use only the help it needs, and check the result. Then add one specialist or one independent workstream when it genuinely helps. Keep the controls visible and the evidence honest. You are directing the work, not surrendering it."),
)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("deliverables"))
    args = parser.parse_args()
    if len(CHAPTERS) != 42 or len(SLIDES) != 42:
        raise ValueError("Storyboard must cover all 42 workshop chapters.")
    args.out.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "style": "animated", "fps": 24, "width": 1280, "height": 720,
               "burned_captions": True, "chapters": CHAPTERS}
    (args.out / "storyboard.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    from video_source import write_script
    write_script(args.out, CHAPTERS)
    words = sum(len(item["text"].split()) for item in CHAPTERS for item in item["beats"])
    print(json.dumps({"chapters": len(CHAPTERS), "teaching_beats": sum(len(c["beats"]) for c in CHAPTERS),
                      "narration_words": words, "estimated_speech_minutes_at_155": round(words / 155, 1)}))


if __name__ == "__main__":
    main()

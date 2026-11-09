# Animated beginner-friendly video script

This script covers the original workshop topics with shorter visual teaching beats.
The PowerPoint's long-form speaker notes are a separate teaching reference.


## 01. From agent user to agent orchestrator


### Give every helper a job

Visual: team

Welcome to your agent teamwork upgrade! No artificial intelligence doctorate required. Imagine a tiny support team: one person keeps the goal straight, another investigates, another builds, and another reviews. We will give Copilot similarly clear jobs, rather than asking a crowd of helpers to change everything at once.


### Small app. Real teamwork.

Visual: board

Our practice app is an issue triage board with fictional support tickets. It is deliberately small. We will add priority, search, a summary, and an evidence export. The interesting part is how we direct the work, protect shared files, and check that the final result actually works.


### Watch, pause, then try

Visual: flow

This is a visual lesson with an artificial intelligence generated voice, not a recording of live product clicks. Pause whenever you want to try an example. The live workshop still lasts three hours: one hour of presentation and demonstrations, followed by two hours of hands-on labs.


## 02. What you will be able to do


### Role + recipe + task

Visual: recipe

Here is the whole workshop in three pieces. A custom agent is a reusable job description. A skill is a reusable recipe with supporting files. Your prompt is today's task: what to change, what to leave alone, and how to prove success. Different jobs need different tools, not bigger promises.


### A useful handoff

Visual: brief

You will learn to give a helper a small, complete assignment. It needs the goal, the relevant context, the files it may edit, and the result to return. That result should contain evidence and unresolved questions. A confident sentence saying finished is not the same as a verified change.


### One repo, no collisions

Visual: split

You will also learn why two chats can collide in one repository. Separate conversations do not guarantee separate files. We will compare clear ownership, a single integration writer, dependency ordering, and separate worktrees. The best choice is the simplest workflow that keeps the changes understandable and safe.


## 03. A realistic three-hour agenda


### The three-hour map

Visual: flow

The event clock is simple: sixty minutes together, then four labs of thirty, thirty-five, forty, and fifteen minutes. Demonstrations are inside that first hour, not extra time. Short check-ins are inside the labs. This self-paced video's running time is separate from the live event schedule.


### Set up before the clock

Visual: review

Complete the preflight before the workshop. Check Node, Git, your Copilot access, and the starter's tests. The app needs no database, secret keys, or package installation. If an organization blocks a newer feature, use the documented fallback rather than bypassing the policy. Setup should not consume your lab time.


### Four things to practice

Visual: board

Lab one creates useful instructions, an agent, and a skill. Lab two delegates research and implements priority. Lab three coordinates search and summary without overlapping writers. Lab four reviews and exports evidence. Each lab has prompts, checkpoints, hints, and separate instructor answers, so you can recover without guessing.


## 04. Five words that prevent confusion


### The engine and control room

Visual: flow

A model proposes the next useful action. The harness is the control room around it: it supplies context, tools, permissions, and execution. A tool is an action such as reading a file or running a test. Changing the model does not automatically change the harness or its configuration format.


### A job is not a side quest

Visual: team

A custom agent is a definition of a specialist. A subagent is a helper doing delegated work in a separate context. You can select a specialist yourself, or a main agent can call it for a side task. Built-in helpers can be subagents too; you do not need a new profile for every task.


### Notes are not a workbench

Visual: split

Context means the notes available to the helper. A session is an ongoing unit of work with its conversation and workspace. Two notebooks can sit on the same desk. Likewise, two separate contexts can still edit the same checkout. Keep the job definition, the delegated call, and the actual workspace separate in your thinking.


## 05. Separate context is not separate files


### Two notebooks, one file

Visual: split

Here is our first collision. Two helpers have separate conversations, but both reach for the same file. One edit can overwrite the other. Subagents do not automatically get independent worktrees. A separate chat is useful for focus, but it is not evidence of filesystem isolation.


### Three different protections

Visual: compare

Three protections answer three different questions. A worktree separates working copies. Tool permissions control actions that need approval. A sandbox can restrict access to files, networks, or credentials. None is a substitute for the others. A worktree is another workbench, not a locked room around your computer.


### Check all shared resources

Visual: brief

Collisions are not limited to source code. Helpers in one checkout share its branch and Git index. Servers can fight over a port, and tests can overwrite a report directory. Before parallel writing, identify all the writable surfaces. If the boundaries are unclear, serialize the writes.


## 06. Teach the documented product, not old defaults


### Current facts, dated honestly

Visual: review

The workshop's product facts were checked against official GitHub and VS Code documentation on November seventh, twenty twenty-six. That is a snapshot, not a promise that interfaces never change. Before teaching it later, check the current clients, policy settings, and file references rather than trusting old examples.


### The default changed

Visual: compare

The October twenty-eighth VS Code release documents Copilot as the default harness for new sessions. Older examples often assume Local. That matters: some frontmatter fields and delegation tools are different. Always choose the intended harness before copying configuration, and then inspect the runtime behavior.


### Preview is not a prerequisite

Visual: review

The Copilot app is documented for all Copilot plans, subject to organization policy. Its Projects experience is public preview. Marketplaces and connectors have preview limits, and computer use is experimental. Our core labs do not require these features, a cloud job, or external tools. Use the fallback when needed.


## 07. A desktop home for agent-driven work


### A home for agent work

Visual: interface

The GitHub Copilot app is a desktop home for agent-driven development on Windows, macOS, and Linux. A Project can coordinate an ongoing goal; a session performs a bounded task. For this workshop, one repository and one small feature are enough. The diagram is an orientation sketch, not a screenshot of your build.


### Choose the workbench

Visual: compare

When starting a session, choose the environment and workspace deliberately. New worktree gives a separate working copy. Current checkout uses the existing files and can overlap another writer. Read the selector and confirm the actual path. Do not assume the app's parallel sessions make every task independent.


### Mode and permission differ

Visual: interface

Plan lets you review an approach first. Interactive supports collaborative steering. Autopilot suits a clear task. Tool permissions are a separate choice: they decide which actions need approval. More autonomy does not remove your responsibility to inspect the changes and verify the outcome before integration.


## 08. Direct one small task, then inspect it


### Start with one small plan

Visual: brief

For the app demonstration, ask for a plan to add one triage behavior. Include the expected result, allowed files, and existing test commands. Ask it not to edit yet. The useful output is a bounded plan with affected paths and checks, not a proposal to rebuild the application.


### Steer the same session

Visual: interface

Review the plan. Reject surprise dependencies, databases, or unrelated improvements. Then allow the bounded implementation. Watch the changed files while it works. If it drifts, correct the same session with a concrete instruction. Confirm the active workspace before giving feedback; another conversation may be working on a different task.


### Finished is not proven

Visual: review

When it finishes, read the complete relevant diff and run the checks. Try the actual behavior in the board. An agent's completion message is not the acceptance criterion. If the desktop app is unavailable, do the same plan, implement, and review loop in VS Code.


## 09. An agent-first window beside your editor


### Open the Agents window

Visual: interface

VS Code's Agents window puts agent work first, beside the normal editor. Open it with the command Chat: Open Agents window, or code, double dash agents. The sidebar organizes sessions and customizations, the center holds the conversation, and the review pane shows files and changes. Actual controls may vary with your build.


### Select the active pane

Visual: interface

Several panes can be visible, but only one is active. Select the intended session before feedback, terminal commands, or browser checks. Branch mode uses the selected current folder. New Worktree starts from committed files in a separate directory. Separate panes alone do not isolate edits.


### Keep work in sync

Visual: flow

Supported sessions can continue between the editor and Agents window without starting over. Cloud and remote sessions have additional requirements; a remote host must remain available. We keep the core labs local, so you can see the paths, run the commands, and understand exactly where the changes go.


## 10. Select the harness before copying YAML


### Same file, different rules

Visual: compare

Sharing an agent filename does not guarantee identical behavior across harnesses. Copilot uses native task delegation and supports a skills field. Local uses the run subagent tool and supports a named agents allowlist and handoffs. These are different contracts. Check both the schema and actual available tools.


### The target is a label

Visual: code

The target field tells the editor how to interpret the file. Target vscode means Local interpretation; target github-copilot means Copilot interpretation. It does not switch your session's harness. Select the harness in the interface first. A completion suggestion is helpful, but it does not prove the runtime supports that tool.


### Do not mix the fields

Visual: compare

Do not paste Local's agents list or handoffs into a Copilot example and expect enforcement. Do not paste Copilot's skills field into Local. The repository has separate examples. If native delegation is missing, run the same roles sequentially with a written handoff. The learning goal is reliable work, not a particular button.


## 11. Write a task contract, not a wish


### Replace the wish with a brief

Visual: brief

Make this smarter is a wish. Add this exact priority rule, preserve the issue shape, edit only this module and its tests, and run these checks is a task contract. The agent still chooses implementation details, but it no longer needs to invent your business requirements.


### Show what success looks like

Visual: review

Provide acceptance examples. One case should trigger the new behavior, one should remain unchanged, and one should test the exact boundary. Give the relevant files and existing commands. These examples are more useful than a long persona description or an instruction to be brilliant.


### Give it a stopping point

Visual: brief

Finish the brief with the expected report and a stopping condition. Return changed paths, exact checks, results, and remaining risks. Stop when the assigned behavior passes, or report a specific blocker. Do not expand into unrelated cleanup. Small, self-contained briefs make delegation easier to evaluate.


## 12. Put shared rules where everyone can find them


### Shared rules live together

Visual: recipe

Put durable repository rules in shared instructions: the runtime, test commands, fixture policy, and contract boundaries. The common Copilot file is dot github slash copilot instructions dot markdown. Path-specific instruction files can target selected areas. Keep them short enough to check and consistent with the task brief.


### Do not assume inheritance

Visual: team

Instruction formats and activation differ by surface. AGENTS dot markdown is supported in some experiences, not identically everywhere. GitHub documents that custom subagents in Copilot CLI do not receive repository instructions by default. Pass important invariants explicitly. Do not rely on invisible inheritance to protect shared files.


### Guidance is not a lock

Visual: split

Saying do not edit a file is guidance, not an operating-system lock. Combine instructions with appropriate tools, approvals, scope checks, and review. In lab one, you will write a small shared rule set and prove that your chosen agent and skill actually use the relevant guidance.


## 13. A reviewer that can read, not write


### A reviewer with a small job

Visual: team

Our first specialist is a reviewer. Its job is to find incorrect behavior and missing tests in the assigned files, then return actionable findings. It does not need to implement the fix. A focused role is easier to verify than a grand persona such as ultimate expert in everything.


### Tools match the job

Visual: code

Give this reviewer reading and search tools, not editing or terminal execution. Define the report: file, problem, impact, and suggested fix or test. Check actual runtime activity because restrictions differ by harness. A read-only reviewer must not claim it ran tests; execution evidence comes from someone with execution tools.


### Test the role, not the name

Visual: review

Start a fresh session with the intended harness and a small file you understand. Ask for a review without repeating the role instructions. Inspect the findings against the source and look at tool activity and workspace changes. Listed in the picker is discovery, not proof that the agent behaves correctly.


## 14. A reusable recipe with a trigger


### A skill is a recipe folder

Visual: recipe

A skill is a folder containing a procedure and any supporting resources. Our triage-policy skill has a SKILL dot markdown file, a policy reference, and a fixture inspection script. Copy the whole folder, not just the headline file. Otherwise the recipe can point at missing ingredients.


### Tell it what and when

Visual: code

The skill needs a name and description in frontmatter. The lowercase, hyphenated name must match the directory. The description explains what it does and when to use it. Refer to supporting files with paths relative to SKILL dot markdown. Keep the steps concrete and tied to the repository.


### A recipe cannot grant tools

Visual: review

Verify explicit invocation, then test a matching ordinary request separately. Automatic selection is useful, not guaranteed. Check whether the agent read the resource and used the right command. A skill does not grant tools or credentials. A reader-only role can describe a check, but cannot truthfully execute it.


## 15. Discovery is not execution evidence


### Available, selected, executed

Visual: flow

These are four different checkpoints. A skill can exist on disk without discovery. It can be discovered without selection. It can be selected without successfully running its script. Do not collapse the whole chain into a green installed badge. Inspect the actual activity and the result.


### Three small probes

Visual: review

Test a request that clearly matches the skill, one that should not use it, and one that is ambiguous. For triage policy, changing priority should load the policy. Explaining the page layout should not need to run priority checks. Refine the description when observed behavior is wrong.


### Trust the whole package

Visual: recipe

Review scripts and resources before using an acquired skill. A skill supplies a recipe; an MCP connection exposes external tools. Approve and review those tools separately. Marketplace availability is not a trust guarantee. The report should distinguish passed, failed, and not run. Missing capability must not become a success-shaped answer.


## 16. Compose them without mixing harnesses


### Role plus recipe

Visual: team

Now combine the parts. The implementer is responsible for one change. The triage policy supplies a repeated procedure. The task brief supplies today's acceptance examples and allowed files. This is composition, not magic: each part has a clear responsibility that you can inspect.


### Copilot can preload skills

Visual: code

Copilot supports naming enabled skills in the agent's skills field. Use the exact skill name and confirm the inventory and actual loading. Preloading is not execution proof. The worker still needs appropriate tools and approvals, and the task still needs a narrow write set.


### Local uses a different path

Visual: compare

Local does not accept that Copilot skills field. Use its supported discovery or explicit invocation instead. Do not give a researcher terminal access merely because an implementer uses a test procedure. Compose only what the role needs, then verify the behavior in the selected harness.


## 17. Build and verify a role and a recipe


### Demo: create the reviewer

Visual: code

In the live demonstration, create a workspace reviewer through Customizations, then inspect its file. Ask it to review a known small module. Look for useful findings and reading activity, not edits. If the report implies tests passed without execution, correct the role and repeat the small probe.


### Demo: create the recipe

Visual: recipe

Next, create the triage-policy skill with a real policy reference. Invoke it explicitly, inspect its resource use, then try a matching plain-language request. If automatic selection fails, refine the description rather than pretending installation guarantees use. Review the script before trusting its output.


### Not run is an honest result

Visual: review

Finally, request a check that needs an unavailable tool. A good report says not run and explains why. It does not invent browser or test evidence. Lab one gives you time to create these files yourself and collect proof; the demonstration is inside the first hour.


## 18. Use a subagent for a bounded result


### Choose a useful side quest

Visual: team

Use a subagent when a separate context contains meaningful independent work. Research a module, implement one owned feature, or review a completed change. Do not split a tiny edit into a crowd of helpers. Delegation adds model usage, waiting, and coordination; it should earn its place.


### Dependencies still matter

Visual: flow

An orchestrator keeps the overall goal, identifies prerequisites, assigns context and tools, then combines results. Fleet mode in the app or CLI can delegate suitable tasks, but it does not make unsafe writes safe. Start with one read-only specialist, then add parallelism only when work is genuinely independent.


### Know your harness lifecycle

Visual: compare

Local subagent calls are stateless and do not inherit the full conversation. A further Local review needs a new invocation with updated context. Copilot has its own delegation lifecycle. Do not teach one harness's behavior as universal. Always give the worker the important constraints explicitly.


## 19. Give the worker enough context to succeed


### Pack a complete brief

Visual: brief

A research brief might say: locate triage behavior, read the contract and tests, do not edit or run commands, and return paths, patterns, and unknowns. Include the fictional-fixture rule and no-dependency constraint. The worker should not need to guess what happened earlier in your main conversation.


### Name the write boundary

Visual: board

For an implementation worker, replace read-only with the exact files it owns and acceptance examples. If it needs a shared contract change, it must stop and report that decision. Silent scope expansion is not helpful autonomy. The returned report should let the coordinator integrate without rereading every intermediate message.


### Update the context deliberately

Visual: review

When a handoff is incomplete, identify the missing fact and supply it through the harness's supported lifecycle. For Local, start a new invocation with the relevant findings. Do not assume the earlier worker remembers a follow-up. A concise, self-contained brief is the portable fallback.


## 20. Named workers, one implementation writer


### Local: one writer

Visual: flow

Our conservative Local pattern has two readers and one writer. The researcher reports, the coordinator implements and validates, and the reviewer inspects. Readers cannot collide with implementation edits. This is a useful first multi-agent design for a small, tightly connected repository.


### Allow only named workers

Visual: code

Local's coordinator can list exact worker names in its agents field. Include the agent tool set. Picker visibility is a separate control: hiding a helper does not automatically prevent model invocation. The Copilot harness does not accept this Local allowlist field. Inspect runtime calls rather than relying on a copied example.


### Review, fix, review again

Visual: review

The role describes a sequence, not a personality. Research first, implement within scope, validate, then request review. Fix actionable findings and provide updated context for another Local review invocation. At the checkpoint, inspect which files and tools actually changed, not only the frontmatter.


## 21. Same workflow, different runtime contract


### Copilot: same safe plan

Visual: flow

Keep the same safe plan in Copilot, but use its native delegation and compatible fields. Pass the skill procedure, repository constraints, and expected result explicitly. Naming preferred workers in prose is guidance, not an equivalent Local schema allowlist. One owner still controls shared writes.


### Do not smuggle Local fields

Visual: code

The Copilot profile can use the agent tool alias and preload triage-policy. Leave out Local's agents and handoffs fields. The target helps the editor interpret the file; the session picker chooses the actual harness. Confirm enabled tools and skill use in the fresh session.


### Fleet is not file isolation

Visual: split

Fleet can help split suitable work, but each helper consumes usage and separate context does not create a private filesystem. If delegation is unavailable, run the roles sequentially with written handoffs. Success is still the correct behavior, intended file changes, honest evidence, and no unapproved scope expansion.


## 22. Switching roles is not parallel delegation


### Handoff: switch the driver

Visual: flow

A handoff changes the active agent in your conversation. Local can offer a button with a prefilled implementation prompt after planning. This is useful when you want to review a stage before continuing. It is not parallel delegation, and custom-agent handoffs are Local-only.


### Subagent: get a report back

Visual: team

A subagent does a bounded side task and returns a result while the main agent keeps ownership. A separate session is independently tracked work with its own workspace choice. These are three different mechanisms. Choose a transition, delegated result, or independently tracked task based on your actual workflow.


### A manual handoff still works

Visual: brief

A missing handoff button should not block learning. Paste a concise reviewed plan, affected files, checks, and remaining decisions into the next role. If using a Local handoff, send false lets you review the prompt before submission. Preserve the decision point rather than automating past it.


## 23. Research -> implement -> prove -> review


### Add the points

Visual: score

Let's make the priority example concrete. Active issues start at sixty points for high impact, thirty for medium, or ten for low. A blocked workflow adds twenty-five. At least one hundred affected users adds ten. At least seven days old adds five. Our first issue totals one hundred points.


### Test the exact edge

Visual: score

P one starts at eighty points, P two at forty, and lower scores are P three. This additive policy cannot produce exactly eighty, so test the nearest reachable scores: seventy-five is P two, eighty-five is P one. Also test ninety-nine versus one hundred users and six versus seven days.


### Closed beats every bonus

Visual: score

Closed issues override the bonuses: zero points, P three, and only the closed-issue reason. Research the contract, implement one owned module, run those cases, then request review. This demo proves a requirement, not merely that an agent wrote code. Lab two supplies the complete specification.


## 24. Hot files and shared resources


### Spot the hot files

Visual: board

Before parallel writing, spot the hot files: shared contracts, package manifests, lockfiles, server wiring, and common fixtures. If two tasks need one hot file, assign it to an integrator or finish that prerequisite first. Asking both workers to be careful is not a coordination plan.


### The invisible shared stuff

Visual: brief

Also reserve ports, output directories, databases, and external actions. In one checkout, concurrent stage-all commits can scoop up another worker's unfinished files. Different branches in the same folder do not give separate workspaces. Our offline sample removes databases and credentials so the remaining boundaries are easy to see.


### When unsure, queue the writes

Visual: flow

If boundaries are uncertain, let readers investigate in parallel and keep a single implementation writer. That may feel less flashy than a swarm, but it is often faster overall because integration stays simple. Identify every writable surface, not only the source module named in the prompt.


## 25. Parallel readers, one integration writer


### Parallel research, single writer

Visual: team

One reader can study priority while another studies the filter controls. Each returns findings; neither changes the shared checkout. The coordinator combines the reports and performs the edit. This keeps useful specialization without overlapping writers or competing Git commits.


### Propose before applying

Visual: flow

Workers can also return proposed patches without applying them. The integrator checks the current file version and applies deliberately. If the base changed, regenerate or rebase the proposal. Do not paste an old whole-file replacement over newer work. A patch still needs review and behavior checks.


### Small can be sophisticated

Visual: review

This pattern fits small repositories, coupled tasks, and newer teams. Two helpers examining one short file may only duplicate effort. Use separate contexts when their work is substantial enough to help. The advanced skill is choosing the workflow, not maximizing the agent count.


## 26. Freeze the contract, then split the work


### Agree on the contract first

Visual: flow

A contract is the agreed input and output shape. Freeze that agreement before splitting work. For example, search and summary both consume the same issue shape. Neither changes it. File disjointness alone is not independence if one worker renames a field the other expects.


### Own the module and its tests

Visual: board

Assign worker A the search module and its own tests, worker B the summary module and its tests, and the integrator the shared wiring and fixtures. Record acceptance checks and dependencies. If a worker needs another owner's file, it pauses and reports the decision rather than quietly expanding its territory.


### Ownership is an agreement

Visual: review

The ownership board is a team convention, not a filesystem lock. Run changed-path scope checks and inspect the combined diff. They can detect an out-of-scope edit, not magically prevent every write. Keep one owner for the board itself, so coordination notes do not become another shared-file collision.


## 27. Parallelize ready tasks, not wishful tasks


### An arrow means wait

Visual: flow

A dependency arrow means a prerequisite must finish first. If both features need the contract, agree and commit it before launching them. Then independent tasks can run together. List actual prerequisites; do not infer dependencies merely from the order tasks appear in a list.


### Serialize shared changes

Visual: board

Manifest, lockfile, shared configuration, and board updates belong to a serialized stage. Let one integrator change them once. Workers report progress back instead of competing to edit the same coordination document. Reserve a single writer for staging and integration in a shared checkout.


### Green plus green can fail

Visual: review

Two tasks can pass separately and fail together because their assumptions disagree. Retest the combined application and actual user flow after integration. If the dependency graph is mostly a chain, run it sequentially. Spend the saved attention on clear examples and review rather than artificial parallelism.


## 28. A claim is a protocol, not a mutex


### A claim is a sticky note

Visual: board

An advisory claim is a sticky note saying who owns which paths, from which base revision, and until when. The coordinator checks conflicts and acknowledges the assignment before writing. At handoff, the worker reports its changed files and releases the claim.


### Expiry is not overwrite permission

Visual: split

An expiry prevents a stale claim from blocking work forever. It does not authorize overwriting an active worker. Inspect the current state and resolve uncertainty. If a worker needs another path, request a new assignment. Markdown and chat claims are protocols, not operating-system mutexes.


### Combine the protections

Visual: review

For many small projects, combine advisory ownership, appropriate tools, scope checks, and one integrator. Use worktrees when separate working copies help. Actual locking requires an enforcement mechanism with defined failure behavior. Do not market a task board as a built-in cross-agent security boundary.


## 29. Use checks and permissions, not slogans


### Checks have different jobs

Visual: review

A scope check detects changed files outside an assignment. Required continuous integration can gate integration until tests pass. CODEOWNERS routes review to people; it does not lock local edits. These mechanisms are complementary. Be precise about whether a check prevents an action or detects it afterward.


### A shell is a powerful tool

Visual: compare

Give each role only needed capabilities, then inspect actual activity. Terminal execution is broad: a shell can write files even without a separate edit tool. A do-not-edit instruction alone is not a permission boundary. Keep approvals and machine access separate from repository ownership conventions.


### Hooks need failure tests

Visual: flow

Hooks can run checks before or after tools. VS Code's hooks experience is preview and harness formats differ. A post-tool hook cannot undo a completed action. Copilot command pre-tool errors deny, but timeouts fall through to normal permissions. Test failure behavior; our core labs do not need hooks.


## 30. Separate working copies for independent tasks


### A second workbench

Visual: branch

A Git worktree provides another working directory, normally on another branch. Independent workers edit separate copies. Start from an agreed committed baseline containing the contract and customizations. Uncommitted agent files, ignored dependencies, and local configuration do not automatically appear in a new worktree.


### Separate files, shared surroundings

Visual: compare

Worktrees separate working files and indices, not every part of Git or your machine. Give servers different ports and outputs separate locations. They do not protect credentials or external services by themselves. Sandboxing and permission controls address different risks.


### Commit, review, then integrate

Visual: branch

A task commit remains on its task branch until you integrate it. Review the scope and evidence, then use your normal merge, cherry-pick, or pull-request workflow. Keep the worktree until integration is verified. Do not delete useful work just because the last response sounded successful.


## 31. A clean merge is not proof of correctness


### Give integration an owner

Visual: flow

Integration is a separate stage with one owner. Inspect each task's diff, scope, and test evidence. Integrate one task at a time. If shared assumptions changed, resolve them against the agreed contract before accepting another worker's result.


### Do not blindly choose a side

Visual: split

A conflict requires reasoning. Read both intentions and preserve the required behavior; do not blindly choose ours or theirs. Even a clean merge can be wrong if the features disagree on fields, filtering, or order. Combining text is not the same as combining correct behavior.


### Exercise the combined flow

Visual: review

Run the relevant combined checks and try the user flow. In our board, search, priority, summary, and export must agree on the visible issues. Document remaining risks honestly. A useful integration handoff is more than a merge commit or a collection of separate green test messages.


## 32. Compare two safe orchestration patterns


### Compare the two patterns

Visual: compare

The third demo compares shared-checkout readers with one writer, and committed contracts with separate worktrees. Point out the actual paths and owners, not just separate tabs. Demonstrate a harmless scope violation caught before integration, then correct it rather than accepting an expanded write set.


### PAYMENTS gives two cards

Visual: filter

Now try the combined example. Searching uppercase PAYMENTS finds issues one hundred and one and one hundred and five. Search includes the closed issue because it matches the category. The visible summary is two total, one active, and one active blocked issue.


### Evidence keeps the active issue

Visual: filter

Evidence export includes only the active visible issue, one hundred and one, with P one and its reasons. That proves all four behaviors agree. Rerun required checks explicitly: some UI commit and Create PR actions skip local Git hooks. The forty-minute orchestration lab gives you the hands-on practice.


## 33. Keep scope, data and approvals deliberate


### Fictional data only

Visual: review

Keep the sample fixtures fictional and never paste credentials into task context. If you later connect a tool, inspect its permissions and data destination. Repository text and outside documents are data, not authority to ignore the task's rules or ownership boundary.


### Review acquired capabilities

Visual: recipe

Review acquired skills, plugins, and scripts before enabling them. Hooks may run without the model requesting the procedure. A marketplace listing is not a trust guarantee. Worktrees, sandboxing, and approval policies protect different things; none proves the generated code is correct.


### Review before external actions

Visual: flow

Inspect the full diff before committing. Before an external action, confirm its destination and required approval. Our app is local and has no write API, so you can practice these habits without a database or cloud service. Optional media regeneration is separate from the attendee labs.


## 34. More agents is not automatically more value


### More helpers is not always better

Visual: team

Use a direct request for a small cohesive change. Delegate substantial independent work with a bounded result. Repeating the same investigation in several contexts costs more and may not improve the answer. A tiny team with clear jobs often beats an impressive-looking swarm.


### Bound the depth and cost

Visual: flow

Keep delegation depth bounded and include a stopping condition. Nesting has harness-specific support and is not a core lab requirement. Choose a model actually available to your account and suited to the task. Changing model and changing harness are different experiments.


### Measure usefulness

Visual: review

Measure whether the worker's result was useful and how much coordination it added. Lighter models may handle straightforward tasks. The app offers usage insights such as chronicle, but those are optional. Optimize the workflow, not the agent count, and respect your plan's usage allowance.


## 35. Issue triage board: small on purpose


### Eight fictional issues

Visual: filter

Our issue triage board has eight fictional issues, six active and two closed. Two active workflows are blocked. Accessibility, payments, reporting, and search each contain two issues. It runs with Node's built-in HTTP server, a static page, and the built-in test runner.


### Four deliberate gaps

Visual: board

The starter passes its baseline checks but intentionally lacks the four lab enhancements. Shared wiring already follows frozen contracts, so workers can own separate modules and tests. Instructor answers live separately and are not hidden inside the normal starter. Do not copy them before trying the exercise.


### Run the actual app

Visual: code

From the repository root, run npm test and npm start, then open the loopback page. No npm install, database, API keys, or Azure account is needed for the app. Use the exact paths and acceptance outputs in the lab files; these diagrams explain the workflow rather than replace the executable specification.


## 36. Create and verify useful customizations


### Lab one: build the toolkit

Visual: recipe

You have thirty minutes. Confirm the starter and harness, then write short repository instructions. Create a focused custom agent with only needed tools. Create a matching skill directory, name, description, and supporting resource. Test them on a known small task.


### Collect actual evidence

Visual: review

Show discovery separately from behavior. Inspect tool activity and compare output with the source. Record an explicit skill invocation and a matching plain-language request. Include an unavailable check reported honestly as not run. A listed file or a polished report is not sufficient proof.


### Explain your choices

Visual: brief

At the checkpoint, explain why each rule belongs in instructions, a role, or a skill. Use the hint ladder if you fall behind; the first hint is not the complete answer. The lab's measured outcome is a useful toolkit you can evaluate, not just more customization files.


## 37. Delegate a feature and collect proof


### Lab two: brief the researcher

Visual: brief

You have thirty-five minutes. Prepare a self-contained research brief with the contract, constraints, allowed actions, and expected report. Use a read-only specialist to find the priority behavior and existing test pattern. Review that report before implementation.


### Implement and check the edge

Visual: score

Keep one writer for the assigned priority module and tests. Use the policy skill to apply the exact rules. Check positive, negative, and boundary cases, including closed override. A nearby example is not proof of the real threshold. Supply test output as execution evidence.


### Get an honest review

Visual: review

Ask the restricted reviewer to inspect the requirements and changed source. It must not claim command execution it could not perform. If native delegation is unavailable, run the roles sequentially. Hand off the outcome, changed paths, checks, and remaining uncertainty.


## 38. Orchestrate two tasks without collisions


### Lab three: split safely

Visual: board

You have forty minutes. Read the shared contract and the search and summary tasks. Record owners, write sets, prerequisites, and reserved shared files. If both tasks need a contract change, complete it first. Do not send workers out with different assumptions.


### Claims are advisory

Visual: split

Compare the one-writer pattern with separate worktrees where available. Exercise claims and handoffs, then use the controlled scope-violation check. Explain whether it prevents a write or detects it later. Shared files, board updates, and Git integration remain with the integrator.


### Retest the whole board

Visual: review

Review and integrate one result at a time, then rerun the combined checks and try the board. Separate passing reports are not enough. At debrief, explain what could still collide and what you would do if a worker needed another owner's file.


## 39. Review, hand off and reflect


### Lab four: evidence and handoff

Visual: review

You have fifteen minutes. Review the complete relevant diff and requirement coverage. Run the final checks and user flow, then create the minimal evidence export. Mark unavailable checks not run with a reason. Do not turn missing evidence into a success statement.


### Help the next developer

Visual: brief

Write a handoff someone can use without reading the whole agent history. Include the outcome, changed paths, assumptions, exact checks and results, remaining risks, and next decisions. An evidence-based handoff is the final product, not an agent completion message.


### Reflect, then finish on time

Visual: team

Ask which tasks were truly independent, whether separate contexts helped, and where coordination cost more than a direct edit. The live workshop ends at three hours. Hooks, marketplace packaging, and cloud continuity are optional extensions afterward, not hidden extra requirements.


## 40. Stop, inspect, narrow and rerun


### Recover from the actual state

Visual: review

When work goes wrong, stop expanding the prompt. Inspect the actual files, changes, and evidence. If a customization is missing, check its path, frontmatter, harness, inventory, and committed worktree base. If tools differ, check the runtime rather than only the editor completion.


### Preserve useful work

Visual: split

Pause overlapping writers and choose one integration owner. Preserve useful work and resolve the shared contract. Do not run a destructive reset simply to look clean. The lab provides named backup and restore operations that preserve current contents before undoing specific files.


### Stop is not undo

Visual: flow

Stopping does not undo completed commands or external actions. Checkpoints can restore some workspace and chat state, not every side effect. Use the appropriate Git or service recovery controls, then rerun affected checks. Recovery is complete when the required behavior is verified again.


## 41. Reliable orchestration is an engineering skill


### Your reliable teamwork recipe

Visual: recipe

Your reliable teamwork recipe is a role, a reusable procedure, and a specific task contract. Choose narrow responsibilities and real acceptance examples. The agent owns a job, the skill supplies a process, and the prompt defines what success means today.


### The desk is what matters

Visual: split

Separate context does not mean separate files. Freeze contracts, assign owners, serialize shared changes, and use one integrator. Worktrees help separate working copies; permissions and sandboxing solve different problems. Advisory claims help coordination but do not enforce a lock.


### Evidence wins

Visual: review

Evidence beats confident prose. A read-only reviewer cannot claim it ran tests. Target vscode does not switch the harness. Two passing branches can fail together, so retest after integration. Keep the smallest workflow that reliably proves the outcome. That's the upgrade from agent user to orchestrator.


## 42. Official sources and availability


### Keep the sources handy

Visual: review

The full package includes the official source ledger, labs, instructor answers, captions, and this video's script. Product facts were checked on November seventh, twenty twenty-six. Recheck them before a later event. Preview features and organization policy can change what appears in your client.


### Illustrations, not hidden proof

Visual: interface

The animated interfaces and team diagrams are original teaching illustrations, not recordings of live Copilot activity. They show concepts; the labs show executable steps. Voice and animation are separate from the offline sample application, and they do not add time to the three-hour live schedule.


### Ready for your small task

Visual: team

Start with one small task you understand. Give it a clear brief, use only the help it needs, and check the result. Then add one specialist or one independent workstream when it genuinely helps. Keep the controls visible and the evidence honest. You are directing the work, not surrendering it.

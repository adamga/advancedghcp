# Complete explainer transcript

Original instruction covering all deck topics. Synthesized narration: Microsoft Foundry / gpt-audio-1.5 / alloy.
This is not a recording of a live product session. Captions are phrase-level estimates anchored to measured audio chunk durations where available; they are not word-level forced alignment.

## Slide 1: From agent user to agent orchestrator

Start: 00:00:00.000

Welcome. This workshop is for people who have already tried an agent and understand the basic idea of a skill. You do not need to be an artificial intelligence researcher, and you do not need to build a large application. We will move from asking one agent to make a change toward designing a reliable workflow that several agents can follow.
Our practice application is an issue triage board. Imagine a support team deciding which fictional issues deserve attention first. This is familiar enough to explain without a long business briefing, but gives us useful boundaries for rules, presentation, documentation, and tests.
The goal is not to create as many agents as possible. The goal is to know when a specialist helps, what information to give it, which tools it should have, and how to prove its result is correct. We will also see why two conversations can still overwrite the same file.
This is an original, narrated slide lesson, not a recording of a live Copilot session. The live workshop includes demonstrations and four hands-on labs. Pause the video whenever you want to inspect a code example or try a step yourself.


## Slide 2: What you will be able to do

Start: 00:01:19.000

By the end, you should be able to make four practical decisions. First, decide where a repeated instruction belongs. A rule that every change must follow is different from a specialist role, and both are different from a procedure used only for a particular task.
Second, write a delegated task that a subagent can understand on its own. It should know the goal, the relevant context, the files it may touch, and what result to return. A vague request to help is not enough.
Third, choose a coordination strategy for one repository. Sometimes separate worktrees are appropriate. Sometimes the simpler and safer choice is several readers and only one writer. Sometimes independent files can be assigned to separate writers, provided the shared contract is already fixed.
Fourth, check the result using the actual requirements. Passing a test suite matters, but it does not replace inspecting the user flow or checking that a priority rule behaves correctly at its boundary.
You will leave with a runnable starter, reusable examples, and lab solutions. Treat those solutions as an answer key, not as files to copy before attempting the exercise.


## Slide 3: A realistic three-hour agenda

Start: 00:02:37.500

The session has a hard three-hour boundary. The first hour includes explanation and demonstrations; it is not an hour of slides followed by extra demonstrations. The remaining two hours are hands-on.
Before the event, complete the attendee preflight. Install a supported Node version, check your Git and Copilot access, open the starter, and run its baseline checks. Downloading software and resolving organizational policy issues should happen before the clock starts.
For the first fifteen minutes we establish the vocabulary and tour the two interfaces. The next twenty minutes show how to create a useful custom agent and a skill, then delegate a real task. The final twenty-five minutes of the first hour concentrate on safe parallel work, integration, and review.
The four labs are timed at thirty, thirty-five, forty, and fifteen minutes. Their short checkpoints and debriefs are inside those allocations. There is no hidden additional break or setup period. If you need a break, take it during a lab work period and use the hint ladder to catch up.
The facilitator guide identifies the live demonstrations and optional extensions. Extensions are deliberately outside the three-hour core, so advanced participants can go deeper without making everyone else late.


## Slide 4: Five words that prevent confusion

Start: 00:04:06.500

Think of the model as the engine that proposes useful next steps. The harness is the machinery around that engine. It supplies context, exposes tools, handles approvals, and organizes execution. Changing the model does not automatically change the harness or its configuration format.
A custom agent is a definition. For example, a reviewer definition says what to review, which tools to use, and how to report findings. You can select that reviewer directly, or another agent can invoke it for a delegated task.
A subagent is the delegated execution, not necessarily another file you must author. Built-in agents can be subagents too. Separate context means the specialist can investigate without filling the main conversation with all its intermediate material.
A skill is closer to a reusable recipe. It may contain a checklist, a reference document, a script, or an example. The agent loads it when relevant or when you invoke it explicitly.
Finally, a session is the ongoing unit of work with its conversation and workspace. A top-level session, a custom agent definition, and a subagent call are not interchangeable. Keeping those concepts separate makes the user interfaces and the configuration examples much easier to understand.


## Slide 5: Separate context is not separate files

Start: 00:05:34.500

Here is the most important warning in the workshop. Separate conversations are not proof of separate files. If two agents use the same checkout and both edit the same module, one can overwrite the other's change.
Imagine two cooks with separate recipe cards but one cutting board. Their instructions are separate; their working surface is shared. Separate subagent context is like separate recipe cards. A worktree is more like giving each cook a separate preparation area, although they still share the kitchen's utilities.
Git worktrees separate working directories and normally branches. They do not automatically restrict access to your computer, credentials, network, or external services. Sandboxing and tool permissions address different parts of that problem.
There can also be shared resources beyond code. Two servers may try to use the same port. Tests may write the same report file. Concurrent Git commands in one checkout share its index. Different branches in the same folder are not a safe substitute for different worktrees.
Throughout the labs, we will identify the actual workspace, the allowed write set, and the shared resources before allowing parallel implementation. When you cannot establish safe boundaries, serialize the writes.


## Slide 6: Teach the documented product, not old defaults

Start: 00:06:59.000

These materials use live official GitHub and VS Code documentation checked on November seventh, twenty twenty-six, rather than treating a model's training data as a product reference.
An important example is the October twenty-eighth VS Code release. It documents the Copilot harness as the default for new sessions in both the editor and Agents window. Earlier examples often assume the older Local harness. That difference affects tool names, handoff support, and agent configuration.
We will label the harness for each runnable example. A target field helps the editor interpret a file, but it does not switch the session's actual harness. You must check both.
Availability is not uniform. The Copilot app is documented for all Copilot plans, subject to organizational policy. App Projects are public preview. The customization marketplace and connectors are preview experiences. Computer use is experimental and requires permission. None of those optional capabilities is necessary to finish our core labs.
Every product claim has a source identifier. The source ledger provides canonical links and caveats. Before teaching this workshop later, recheck the ledger and the versions attendees actually have. A verification date is an honest snapshot, not a promise that a fast-moving interface will never change.


## Slide 7: A desktop home for agent-driven work

Start: 00:08:32.500

The GitHub Copilot app is a desktop application built around agent-driven development. Its official documentation supports Windows, macOS, and Linux. Think of it as a place to direct work and review results, rather than only a code editor.
A Project is useful when a goal continues over time and may require several sessions or repositories. Projects are public preview. A session is the more concrete unit that works on a task. For this workshop, one repository and one bounded feature are enough.
When you start a session, choose where it runs and where it edits. A new worktree provides a separate working copy. Current checkout uses existing files and can therefore overlap other writers. Read the workspace selector rather than assuming isolation.
The app offers Plan, Interactive, and Autopilot modes. Plan allows you to review the approach before implementation. Interactive supports collaborative steering. Autopilot is appropriate for sufficiently clear tasks, but it does not remove the need to review the result.
Tool permission settings are a separate decision. A session can still need approval for a command or external action. Use the Changes view and the actual test output to decide whether the work is ready. The app's convenience does not make every completed agent response correct.


## Slide 8: Direct one small task, then inspect it

Start: 00:10:00.500

In the live demonstration, open the issue triage repository in the Copilot app. Before sending a prompt, point out the environment, workspace, mode, model, and permission settings. These controls answer different questions, so do not collapse them into one idea of autonomy.
Start with a planning request: explain how to add a triage rule, identify affected files, and return test cases without editing. The result should tell us where the work belongs and what evidence will prove it correct.
Next, review that plan. If it proposes a new framework, a database, or external credentials, redirect it. Our application is intentionally small and offline. We want practice with agents, not infrastructure troubleshooting.
Allow implementation only after the scope is clear. While the agent works, inspect whether its edits stay in the assigned files. If it expands the scope, steer the same session with a concrete correction.
At the end, open the complete diff and run the documented checks. A response saying all done is not our acceptance criterion. We need the rule's expected output, tests of its edge cases, and no unrelated edits.
If the desktop app is unavailable under your organization's policy, perform the same bounded workflow in VS Code. The safety pattern is portable even when the buttons differ.


## Slide 9: An agent-first window beside your editor

Start: 00:11:32.000

In VS Code, the Agents window is an agent-first interface alongside the regular editor. The documented command is Chat: Open Agents window. The command-line alternative is code, space, double dash agents.
The primary sidebar helps you organize sessions and open customizations. The central area is the conversation where you direct the task. The secondary sidebar exposes files, changes, search, and available validation tools.
The schematic on this slide is an original orientation diagram, not a screenshot of a particular build. Use the live interface in the demonstration and explain the actual labels attendees see.
When you create a session for a Git repository, Branch uses the selected current folder, while New Worktree starts from committed files in a separate working directory. A new worktree requires a repository with a commit, and it does not automatically contain uncommitted custom-agent files.
Multiple panes are useful for monitoring, but only one is active at a time. Check the active session before giving feedback, starting a terminal, or opening a browser.
The editor and Agents window can continue supported sessions without starting over. Remote and cloud execution have additional requirements. For our labs, local execution keeps the setup small and makes it easy to inspect exactly which files changed.


## Slide 10: Select the harness before copying YAML

Start: 00:13:00.500

A Markdown file can be discovered in two environments yet behave differently in each. This is why we label our examples.
For the Copilot harness, the current VS Code file reference documents built-in tool aliases including read, search, edit, execute, and agent. Native delegation uses the task tool. The skills field can name enabled skills to load into an agent's context.
For Local, delegation uses the VS Code run subagent tool. Local supports an agents list to limit which specialists a coordinator may invoke. Local also supports custom-agent handoffs.
Do not copy the Local agents list or handoffs into a Copilot-targeted example and expect the same effect. Conversely, Local does not accept the Copilot skills field. Local skills are discovered or explicitly invoked using supported mechanisms.
The target property tells the editor which schema to interpret: vscode for Local, or github-copilot for Copilot. It does not change the runtime you selected in the Session Target control.
For every example, first select the intended harness, then check discovery and actual tool activity. Editor completion is useful, but it is not proof that the runtime has a particular tool. Our fallback is always a self-contained prompt and a sequential workflow, not pretending unsupported fields are enforced.


## Slide 11: Write a task contract, not a wish

Start: 00:14:30.500

A strong task prompt is a compact contract. It says what success looks like and gives the agent enough information to find and verify the right change.
Compare make triage smarter with a specific request. Add deterministic priority classification for the fictional issue fixtures. Preserve the existing issue input shape. Do not add dependencies. Limit implementation to the priority module and its tests. Include a boundary case and a case that must remain unchanged.
The second version is more useful because it constrains both behavior and scope. The agent can still choose implementation details, but it does not have to invent your business requirements.
For delegation, add the allowed actions and the result format. A research worker should return paths, existing patterns, and unknowns without editing. An implementation worker should return changed files and validation evidence. A reviewer should not claim to have executed tests when it has only reading tools.
Include a stopping condition: stop after the assigned feature passes its checks, or report the specific blocker rather than expanding into unrelated work.
This is context engineering in practical terms. You are selecting the information the agent needs, not pasting the entire repository or an unrelated conversation into every call.


## Slide 12: Put shared rules where everyone can find them

Start: 00:16:01.000

Repository instructions hold durable conventions such as the test command, the supported runtime, and the rule that fixtures must be synthetic. Those should not be repeated differently in every specialist definition.
The repository-wide Copilot file is dot github slash copilot instructions dot markdown. Path-specific instructions can live in the instructions directory with an apply-to pattern, subject to the surface's support. AGENTS dot markdown is another supported instruction format in some experiences; do not assume identical activation across all clients.
For our small starter, keep the shared guidance short. Describe the application, the commands, the contract boundary, and the rule against adding dependencies or changing shared files without coordination.
There is an important inheritance caveat. GitHub's current custom-agent documentation says repository instructions are not included by default for custom subagents in Copilot CLI. Therefore, our delegated briefs explicitly include the critical invariants. An opt-in or client-specific conversion should not be your only defense.
Instructions guide behavior, but do not enforce file permissions. Saying do not edit a file is useful guidance, not a lock. Use tools, approvals, scope checks, and review alongside that guidance.
In the first lab, you will author and verify these instructions rather than turning them into a long document that nobody can evaluate.


## Slide 13: A reviewer that can read, not write

Start: 00:17:42.000

Here is a small custom-agent definition. The frontmatter gives it a name, explains when it is useful, and selects reading and search tools. The Markdown body tells it what decisions to make and how to report.
The restriction is deliberate. This reviewer does not need terminal execution, edits, or delegation. Removing those tools makes the role easier to reason about. Still, verify actual runtime activity, because tool restrictions can differ by harness and client.
The agent should report actionable behavior defects and missing tests with file references. It should explain the impact and suggest a fix. If it finds nothing, it should say so and identify checks it could not perform.
To verify it, select the intended harness and start a fresh chat. Attach one known source file and its tests, ask for a review, then inspect the findings against the code. Also inspect the tool calls and the working tree. A reviewer with read-only tools should not report that it ran the test suite.
Discovery is only the first checkpoint. A visible agent that produces vague advice is not yet a useful agent.
In the workshop repository, starter templates are separated from completed answers. You will adapt a role to a real recurring task, not just rename an expert persona.


## Slide 14: A reusable recipe with a trigger

Start: 00:19:10.500

A skill is a directory, not only a Markdown paragraph. The required SKILL dot markdown file starts with a name and a description. The name uses lowercase letters, numbers, and hyphens, and matches the parent directory. The description states both what the skill does and when to use it.
Our example is test changes. Its procedure identifies the tests covering a change, runs the documented commands, and reports passed, failed, and not-run checks. A reference file can explain the output format, and a supporting script can perform a deterministic check.
Keep paths relative to the skill file when referring to its resources. If you move only SKILL dot markdown and leave the script behind, you have not installed the complete skill.
Automatic relevance selection is useful but not guaranteed. Test explicit invocation and automatic selection separately. If a skill is available as a slash command, invoke it on a small known task and inspect whether its instructions and resources were actually used.
A skill does not grant permission to execute commands. The active agent still needs the relevant tools and approvals. Review every script before trusting it.
This is the first step toward reliable agent composition: give the specialist a repeatable procedure rather than hoping it remembers your preferred process.


## Slide 15: Discovery is not execution evidence

Start: 00:20:43.000

Skills help manage context because the agent can discover a concise description before loading the full procedure and its resources. This is often called progressive disclosure. It avoids putting every possible checklist into every conversation.
But you must evaluate the behavior. A skill can exist on disk without being discovered. It can be discovered without being selected. It can be selected without successfully executing its script.
Use three small probes. A positive request clearly matches the skill, such as validate the changed priority rule. A negative request, such as explain the application layout, should not unnecessarily run that procedure. An ambiguous request helps you see whether the description needs refinement.
Inspect the result and tool activity. Did it read the referenced report format? Did it run the expected command? Did it distinguish a skipped check from a passing one? A convincing-looking report is not proof.
Review scripts and data access before enabling a skill, especially one acquired from a marketplace or another repository. Skills can include executable code.
Avoid loading too many skills into a specialist. Give it the few procedures relevant to its role. If the role has only read tools, it can describe a verification plan, but it cannot truthfully claim to have run an execution-based skill.


## Slide 16: Compose them without mixing harnesses

Start: 00:22:15.500

Now we combine a role and a recipe. In the Copilot harness, the current VS Code reference supports a skills array in the custom-agent frontmatter. It names enabled skills to load into that agent's context.
For example, an implementer can have read, search, edit, and execute tools plus the test changes skill. Its body still specifies the allowed files, the behavior to implement, and the required handoff evidence. The skill supplies the repeatable validation procedure.
In Local, do not paste the Copilot skills field. Use supported skill discovery or explicit invocation and tell the worker to follow the relevant procedure. The repository includes harness-labelled examples so you can compare them without guessing.
Preloading a skill does not prove it ran, and a disabled or unavailable skill may still appear in editor inventories. Verify the skill's actual availability and use.
Also consider whether execute is necessary. A read-only researcher does not need it just because another specialist uses a test skill. Adding terminal access expands the worker's capabilities beyond a simple file editor.
For a beginner, the main lesson is composition: the agent answers who is responsible, the skill answers how a repeated task is performed, and the task brief answers what must be achieved this time.


## Slide 17: Build and verify a role and a recipe

Start: 00:23:46.500

For the live demonstration, begin with a fresh chat and the correct harness. Open Customizations, create a workspace reviewer, and show the generated file. Replace vague persona language with a focused output contract.
Ask it to inspect a small source file. Show the tool activity and explain why it should not execute tests. If the report implies tests passed, challenge it and refine the instructions.
Then create a test changes skill. Include a report template as a real resource in its directory. Invoke it explicitly using the interface supported by the selected harness, and ask it to validate the starter.
Inspect the command output. Next, use a plain-language request that matches the description and check whether automatic selection happens. If it does not, this is a useful demonstration of why discovery is not a guarantee.
Finally, supply a task that needs a browser check but do not grant browser tools. The correct report marks that check as not run, with a reason. It must not turn unavailable capability into success.
This demonstration is included in the first hour and is intentionally small. The lab gives you time to write your own files, test their behavior, and collect evidence. Do not use the demonstration as an excuse to skip verification in your own session.


## Slide 18: Use a subagent for a bounded result

Start: 00:25:15.500

Delegation is useful when a separate context can contain a meaningful amount of independent work. A research specialist can read a module and return its contract. A worker can implement one independently owned feature. A reviewer can inspect a completed change.
Delegation is not automatically an improvement. Splitting a tiny edit into several conversations can take longer and consume more AI usage than doing it directly. A task that depends on another unfinished result is not ready to run in parallel.
The current GitHub documentation describes an orchestrator that breaks down work, identifies dependencies, assigns context and tools, and combines results. The app and CLI offer fleet mode for suitable tasks, but fleet mode does not make an unsafe write set safe.
For our first delegated exercise, choose read-only research. It gives you practice with context and result contracts without introducing overlapping writers.
Remember that behavior varies by harness. Local subagent invocations are stateless and do not inherit the full conversation. Another Local review requires a new invocation with updated context. Copilot supports its own delegation lifecycle, so do not teach Local limitations as universal.
Start with one specialist and a clear stopping condition. Add parallelism only when the work genuinely benefits from it.


## Slide 19: Give the worker enough context to succeed

Start: 00:26:50.000

This slide is a worked delegation brief. We ask a researcher to find the priority behavior in the issue triage application. We provide the current contract and the repository constraints, then explicitly forbid edits and command execution.
The expected result is not an essay about best practices. It is a list of relevant paths, the current input and output shapes, existing test patterns, and unresolved questions that might affect implementation.
Make the request self-contained. If the main conversation established that all fixtures are synthetic or that dependencies must not change, include those facts. Do not assume the worker received earlier messages or repository instructions.
For an implementation worker, replace read-only with an exact write set and include acceptance examples. Ask it to stop and report if it needs to change a shared contract. That is better than silently expanding the assignment.
You should be able to evaluate the handoff without rereading all of the worker's intermediate conversation. The report should link evidence to the requested outcome.
If the worker's result is incomplete, provide the specific missing context appropriate to the harness's lifecycle. In Local that means a new invocation with the relevant findings, not pretending you can continue the earlier stateless call.


## Slide 20: Named workers, one implementation writer

Start: 00:28:17.500

This coordinator pattern is deliberately conservative. In a Local harness session, the coordinator lists the exact research and review agents it may use. Its tools include delegation, reading, searching, editing, and the required validation capability.
The researcher reads and reports. The coordinator implements. The reviewer reads the changed files and returns findings. There is only one implementation writer, so parallel research cannot overwrite code.
The agents allowlist is a Local-specific configuration. Include the agent tool set and use names that exactly match the worker definitions. Picker visibility is separate from model invocation: hiding a worker from the dropdown does not automatically prevent delegation.
The coordinator's instructions describe a sequence, not just a persona. Research first, implement from a reviewed plan, verify, then request review. If the review finds a defect, fix it and make a new Local review invocation with the updated context.
This is often a better first multi-agent design than two unrestricted general-purpose workers. It uses specialization without forcing difficult merge coordination.
In the lab, inspect the tools and files that actually changed. The YAML is useful configuration, but the evidence should show that the workflow followed the intended boundaries.


## Slide 21: Same workflow, different runtime contract

Start: 00:29:47.000

For the Copilot harness, keep the same safe workflow but do not copy Local-only fields. Use native delegation with the supported agent tool alias. A skill can be listed in Copilot frontmatter, but the delegated task still needs the relevant constraints and acceptance checks.
The conceptual coordinator remains responsible for the overall goal. It asks a researcher for a focused result, implements or assigns a bounded change, obtains a review, and integrates the evidence.
Without the Local agents allowlist field, an instruction naming preferred workers is guidance, not equivalent schema-level enforcement. Review the actual calls and the tools available to the workers.
Fleet mode in the app or CLI can analyze a larger prompt and parallelize appropriate subtasks. It may increase AI usage, and it does not automatically isolate files or remove dependencies. Use it only after you have defined safe task boundaries.
For this workshop, the portable fallback is to run the same roles sequentially and pass a written handoff between them. You still learn the contracts and quality gates even when native delegation or a newer interface is unavailable.
The result should be evaluated in the same way regardless of surface: the correct behavior, the intended file changes, honest validation evidence, and no unapproved expansion of scope.


## Slide 22: Switching roles is not parallel delegation

Start: 00:31:21.000

A handoff changes who is active in the conversation. Local custom agents can offer a button that switches to an implementation agent with a prefilled prompt. This is useful when you want to inspect a planning result before continuing.
A subagent is different. The main agent invokes a specialist and uses its returned result while retaining ownership of the larger task. You do not have to switch the active agent.
A separate session is different again. It is a tracked unit of work that you can direct independently. Its workspace choice determines whether it has separate files or shares an existing checkout.
Current VS Code documentation says custom-agent handoffs are supported only by Local, not by the Copilot harness. The example uses send false so that the user reviews the prefilled prompt before sending it.
Do not let a missing handoff button block the lab. A concise manual handoff containing the plan, affected files, checks, and remaining decisions achieves the learning objective without relying on that UI feature.
Choose the mechanism based on the workflow: transition when a human should review a stage, delegate when a specialist should return a bounded result, and open a separate session when independently tracked work is appropriate.


## Slide 23: Research -> implement -> prove -> review

Start: 00:32:43.500

In the live demonstration, use a small triage enhancement from the lab specification. Do not invent the rule during the demonstration. Read its acceptance examples aloud so participants can predict what should happen.
Ask a read-only researcher to identify the relevant contract, module, and tests. Review its report and show how the coordinator uses that result rather than repeating the entire investigation.
Next, implement the bounded change with one writer. Keep shared fixtures and server wiring unchanged unless the task explicitly assigns them. Use the validation skill to run the documented checks.
Here is the exact worked example. Active issues start with sixty points for high impact, thirty for medium, or ten for low. A blocked workflow adds twenty-five. One hundred or more affected users adds ten. Seven or more days of age adds five. P one begins at eighty points, and P two at forty. Fixture ISS one hundred and one totals one hundred points and is P one. Closed issues override all those additions and return zero, P three, with only the closed-issue reason.
Explain three categories of tests. A positive case must trigger the new behavior. A negative case must remain unchanged. A boundary case verifies the actual threshold. Eighty itself is unreachable under this fixed additive scoring policy, so compare the nearest reachable cases: seventy-five is P two, while eighty-five is P one. Test one hundred users versus ninety-nine and seven days versus six separately as well.
Then ask a restricted reviewer to inspect the change against the requirements. The reviewer can find reasoning defects, but it cannot truthfully claim execution without execution tools. The coordinator supplies the actual test evidence.
Finally, fix actionable findings or report what remains uncertain. This shows the full loop: researched context, bounded implementation, measured evidence, and independent review. It is much more useful than a demonstration that stops after the agent writes code.


## Slide 24: Hot files and shared resources

Start: 00:35:03.000

Before parallel implementation, look for hot files. These are files that several tasks are likely to touch: a shared type or contract, the package manifest, the lockfile, application wiring, generated artifacts, and common fixtures.
If both workers edit a hot file, merely asking them to be careful is not a reliable plan. Assign that file to one integrator, or complete the prerequisite change before starting independent tasks.
There are also shared resources that do not appear in a source diff. Two test commands can write the same report directory. Two servers can compete for port three thousand. A shared database can mix state. External services can receive duplicate requests.
In one checkout, Git's index and branch are shared. Do not let two agents independently stage all files and commit at the same time. One writer can accidentally include the other's unfinished work. Worktrees reduce that particular problem because they provide separate working copies and indices, but integration still requires care.
The practice app avoids databases, credentials, and external services to keep these issues manageable. Its task board still records file ownership and test output expectations.
The general lesson is to identify every writable surface, not only the source module named in the prompt.


## Slide 25: Parallel readers, one integration writer

Start: 00:36:35.000

When you are unsure about independent write boundaries, use parallel readers and one integration writer. Researchers can inspect separate questions concurrently, but they return findings rather than changing the shared checkout.
One researcher might explain the priority rules. Another might inspect the accessible filter controls. The coordinator uses both reports to plan a change. Only the integrator edits the shared source and wiring.
Another variation is patch proposals. A worker returns a diff or proposed implementation without applying it. The integrator checks it against the current file version and applies it deliberately. If the base changed, regenerate or rebase the proposal; do not paste an old replacement over new work.
This approach is slower than unrestricted parallel writing in some cases, but it greatly reduces coordination risk. It is a strong default for small repositories, tightly coupled tasks, or inexperienced teams.
Use separate specialists only when their work is substantial enough to justify the overhead. Two readers examining the same short file may simply duplicate effort.
In the lab, you will first exercise this safe pattern. Then you will compare it with disjoint writers and worktrees, so you learn to choose rather than assume one technique fits every task.


## Slide 26: Freeze the contract, then split the work

Start: 00:38:08.000

Disjoint ownership works when the tasks really are independent. Start by freezing the shared input and output contract. Then assign each worker a small set of files and its own tests.
For example, one worker may implement a search predicate while another implements a summary formatter. Both consume the same documented issue shape. Neither changes that shape or the shared server wiring. The integrator combines their results later.
The task board should record the owner, allowed files, dependencies, acceptance checks, and status. It should also say which shared files are reserved for the integrator.
A worker that discovers it needs another owner's file must stop and request a contract decision. Do not let it quietly edit outside the assignment. That small interruption prevents a much larger merge or behavior defect.
Remember that different source files can still be behaviorally coupled. If one worker renames a field that the other consumes, file disjointness does not make the tasks independent. The frozen contract is as important as the ownership list.
This is a team convention, not a built-in lock. We will add explicit scope checks and inspect the combined diff to detect violations rather than merely trusting the board.


## Slide 27: Parallelize ready tasks, not wishful tasks

Start: 00:39:34.000

A task graph helps you decide what can run now. If both feature tasks depend on a shared contract change, finish that change first. Only then are the feature tasks ready to run independently.
The graph on this slide has four stages. Define the contract, run two independent workers, integrate their output, then validate the combined application. The arrows represent actual prerequisites, not a preferred list order.
Shared configuration changes belong in a serialized stage. If a dependency must be added, let the integrator update the manifest and lockfile once. Do not ask every worker to solve installation separately.
Reserve one owner for the coordination board too. Multiple agents updating the same board can collide just as they can collide in code. Workers can report status to the coordinator, which updates the record.
Individual tests are necessary but insufficient. Two branches can pass independently and fail together because they make different assumptions about the contract or user flow. Run the combined suite and smoke checks after integration.
If the graph is mostly a chain, parallel execution adds little value. Use a sequential workflow and invest the saved attention in clearer acceptance examples and review.


## Slide 28: A claim is a protocol, not a mutex

Start: 00:41:01.000

You can improve shared-checkout coordination with an advisory claim protocol. Before writing, a worker states the paths it intends to own, the starting revision, and when the claim should expire. The coordinator checks for conflicts and acknowledges the assignment.
At handoff, the worker reports the changed files and releases its claim. If it needs another path, it pauses and requests a new assignment.
An expiry prevents a stale claim from blocking work forever, but expiry is not permission to overwrite an active worker. The coordinator must inspect the current state and resolve uncertainty.
This is similar to a team agreeing who edits a document section. It works only when participants follow the protocol. A Markdown file or chat message is not an operating-system mutex and does not stop a terminal command from writing elsewhere.
Actual locking requires an enforcement mechanism with defined failure behavior. In many coding workshops, the practical combination is advisory ownership, narrow tools, scope checks, and one integrator. Worktrees are another option when independent working copies are helpful.
Do not oversell claims as a product feature or security boundary. They are an original workflow technique in these materials, and the labs deliberately include a violation check so participants see the limitation.


## Slide 29: Use checks and permissions, not slogans

Start: 00:42:31.000

Guidance is valuable, but enforcement must be explicit. A changed-path scope check can fail when a task modifies files outside its assignment. Required continuous integration can block integration until tests pass. Review ownership can ensure the right people approve a change.
These mechanisms detect or gate different things. CODEOWNERS routes review; it does not prevent a local edit. A post-change scope check detects a violation after the write; it does not stop the initial write.
Tool restrictions reduce the capabilities available to a specialist. Be careful with terminal execution, because a shell can modify files even if a separate edit tool is absent.
Current Copilot hooks can inspect a pre-tool-use event and return a documented denial. VS Code's hooks experience is preview, and different harnesses use different event formats. A post-tool hook cannot undo an action already completed.
There is a subtle failure rule: documented command pre-tool-use errors deny a call, but timeouts fall through to normal permissions. Therefore, do not describe every hook as fail-closed.
The core labs do not enable hooks. They teach deterministic checks and manual review, with hooks as an optional extension. Before using a hook for enforcement, test valid, invalid, malformed, and timed-out cases in the actual execution environment.


## Slide 30: Separate working copies for independent tasks

Start: 00:44:06.000

A Git worktree gives one repository another working directory, usually on a different branch. This lets independent tasks edit separate copies without overwriting each other's working files.
Begin from a committed baseline. That baseline should include the contract and the customizations workers need. Uncommitted agent files do not magically appear in a newly created worktree. Ignored dependencies and local configuration are also absent by default.
The example creates two task worktrees from the same agreed base. The paths and branch names are examples; check your actual repository and use the platform-specific instructions in the lab.
Worktrees still share parts of Git's repository metadata and do not isolate external resources. Use different server ports and output directories, and do not let workers change shared credentials or external services.
When a task finishes, its commit is still on its task branch. It has not automatically reached the target branch. Review and integrate it deliberately, then retest the combined result.
Keep a worktree until integration and verification are complete. Do not remove it merely because the agent's last response sounded successful. If there is a conflict, resolve it based on the contract and intended behavior, not by blindly choosing one side.


## Slide 31: A clean merge is not proof of correctness

Start: 00:45:37.000

Integration is a separate stage with its own owner. First inspect each task's diff and evidence. Verify that the worker stayed within its assignment and that the tests cover the requested behavior rather than only implementation details.
Then integrate one task at a time. Your normal Git or pull-request workflow may use a merge, a cherry-pick of a reviewed commit, or a PR with required checks. These are integration choices, not reasons to skip review.
A conflict means the two changes need reasoning. Do not automatically choose ours or theirs. Read both intentions, check the shared contract, and preserve the required behavior.
Even a clean merge can be wrong. The changes may compile and pass their separate tests while disagreeing on a field name, filter semantics, or user-visible order. Run the complete relevant suite and exercise the combined flow.
For the issue triage app, that means opening the page, applying the new behavior, and checking the expected output against the fixture examples. A test success message alone is not enough if the feature never appears in the interface.
The lab answer key demonstrates the combined result and documents what remains intentionally out of scope. Good integration includes an honest handoff, not just a merge commit.


## Slide 32: Compare two safe orchestration patterns

Start: 00:47:05.000

The third live demonstration compares two patterns rather than declaring worktrees the only answer.
First, use the shared checkout with parallel read-only specialists. The coordinator receives their reports and performs the edit. Show the changed-file list so participants can see that only the assigned writer changed code.
Second, show two independent tasks from a committed contract in separate worktrees. Point out the actual paths and branches, not just separate conversation tabs.
Use the lab's scope-check mechanism to demonstrate a controlled violation. A proposed change to a shared file should fail the task's allowed-path check. Do not manufacture an unsafe destructive operation; the lesson is detection and correction.
Then review one task, integrate it, and repeat for the next. The concrete combined example is a case-insensitive search for PAYMENTS. It returns ISS one hundred and one and ISS one hundred and five. The summary shows two total issues, one active and one active blocked issue. Evidence export includes only the active issue, ISS one hundred and one, with its P one priority. This checks that search, summary, priority and handoff agree on the same visible issues.
Run the combined acceptance checks and inspect the page. Explain that commit actions in some UI workflows can skip local hooks, so required checks must be run explicitly and enforced by the normal integration policy.
Finally, ask participants which pattern they would choose if both tasks needed the same contract change. The correct first step is to serialize or assign that contract change, not to launch more agents.
This demonstration fits inside the first hour. The forty-minute orchestration lab provides the hands-on practice.


## Slide 33: Keep scope, data and approvals deliberate

Start: 00:49:08.000

Agent safety is not one switch. File isolation, tool permissions, sandboxing, and review each address different risks.
A worktree separates source changes. A sandbox can restrict filesystem, network, and credential access, depending on platform and configuration. Approval settings determine which tool actions require confirmation. None of them proves the generated code is correct.
The starter uses fictional issues and no external integration. Do not replace those fixtures with customer data or paste secrets into a prompt. If you later connect an MCP server or connector, inspect the permissions and the data destination.
Review acquired skills and plugins before enabling them. A skill directory may contain scripts, and hooks can run without the model asking for the procedure explicitly. Marketplace availability is not a trust guarantee.
Treat repository content and external text as data, not authoritative instructions to bypass the task's rules. If an issue asks the agent to ignore ownership boundaries, the worker should report that request rather than obey it.
Before committing, inspect the complete diff. Before any external action, verify the destination and required approval. The workshop focuses on local code precisely so you can learn these habits without creating avoidable cloud cost or data exposure.


## Slide 34: More agents is not automatically more value

Start: 00:50:43.000

The best agent workflow is often the smallest one that reliably completes the task. A direct request is appropriate for a small cohesive edit. A specialist is useful when the work needs substantial separate context or a recurring procedure.
Parallelism saves time only when tasks are independent enough that coordination costs do not exceed the benefit. Repeating the same investigation in several contexts can consume more usage without improving the result.
Bound delegation depth. Recursive delegation needs a stopping condition and has harness-specific support. It is not part of our core labs. A simple coordinator and one or two workers are enough to learn the principle.
Choose a model available to your account and suitable for the task. Do not copy a fixed model identifier from an old presentation and assume it is still offered. Keep model changes separate from harness changes so you know what affected the result.
Measure both quality and usage. Did the worker return a correct, usable result? How much extra context and waiting did coordination introduce? Did a lighter model suffice for a straightforward task?
In the Copilot app, current documentation also describes usage insights through chronicle. That is an optional way to reflect on patterns, not a requirement for the lab. The key habit is to optimize the workflow, not just increase the agent count.


## Slide 35: Issue triage board: small on purpose

Start: 00:52:18.000

The practice application is intentionally modest. It serves a static issue triage board using Node's built-in HTTP support and uses the built-in test runner. There is no database, authentication service, external AI call, or dependency-heavy framework to distract from the workflow.
The board shows eight fictional support issues: six active and two closed, with two active blocked workflows. Four categories have two issues each: accessibility, payments, reporting, and search. The exercises add priority scoring, case-insensitive search, summaries, and evidence export behind documented feature-module boundaries. That gives us a realistic reason to use skills, reviewers, and multiple task owners without building a production support platform.
Start with a passing baseline. A workshop should not require you to fix unrelated infrastructure before learning its topic. The missing lab features are intentional and described in the lab specifications.
The repository separates starter templates, attendee instructions, and instructor answers. The answer key can demonstrate one valid solution, but the acceptance checks evaluate behavior rather than requiring identical code.
Use the documented start and test commands from the README. Run the smoke check and inspect the page so you know the app works before asking agents to change it.
When you assign work, use the repository's actual module paths and contract. The generic diagrams in this deck illustrate the pattern; the lab files are the executable source of truth for exact features, fixtures, and allowed files.


## Slide 36: Create and verify useful customizations

Start: 00:54:08.000

The first lab takes thirty minutes. Use the first few minutes to confirm the passing starter and select the intended harness. Then write short repository instructions based on the existing commands and constraints.
Create a custom agent for a focused recurring role. It should have a useful description, only the tools it needs, and a result format you can evaluate. Do not simply call it senior expert and hope that defines its behavior.
Create a real skill directory with matching name and frontmatter. Include at least one supporting resource, and reference it from SKILL dot markdown. Verify that its commands and paths work in this repository.
Test discovery and behavior separately. A listed agent or skill is available, not necessarily correct. Use a small known request, inspect the activity, and compare the result with the source.
Record a positive invocation and a case that must be reported as not run or out of scope. This makes honesty part of the acceptance criteria.
The lab provides step-by-step actions, expected outputs, a hint ladder, and an answer key. If you fall behind, use the first hint before copying a complete solution.
At the checkpoint, you should be able to explain why each instruction belongs in its chosen file and why the specialist does not need unrestricted tools.


## Slide 37: Delegate a feature and collect proof

Start: 00:55:37.000

The second lab takes thirty-five minutes. Your first deliverable is a self-contained delegated brief. It includes the relevant contract, repository constraints, allowed actions, and expected report.
Use the read-only researcher to locate the behavior and existing test pattern. Check its report before implementation. If it assumes missing context, correct the brief.
Then use the coordinator workflow to implement the lab's exact enhancement. One implementation writer owns the assigned source and tests. The skill provides the repeatable validation procedure.
The acceptance criteria include positive, negative, and boundary cases. Do not accept a nearby example as proof of the actual threshold or precedence rule.
Ask the reviewer to inspect the changed code against the requirements. Supply the test output as evidence; do not let a read-only reviewer claim it executed commands.
If native delegation is unavailable, perform the roles sequentially with a concise manual handoff. You still need to produce the same behavior and evidence.
At the checkpoint, your report must show what changed, which checks ran, their results, and any remaining uncertainty. It must also identify the ownership boundary you preserved. The goal is a complete, verifiable loop, not merely a successful subagent call.


## Slide 38: Orchestrate two tasks without collisions

Start: 00:57:06.000

The third lab takes forty minutes and concentrates on one repository. Start by reading the shared contract and the two task specifications. Decide which files belong to each worker and which remain with the integrator.
Record the dependencies. If either task needs a contract change, perform that prerequisite before parallel work. Do not launch workers against different assumptions.
Exercise the shared-checkout safe pattern using readers and one writer, then compare the worktree option where available. The lab's fallback runs the same tasks sequentially without newer UI features.
Use the task board to record claims and handoffs. Treat the board as advisory. Run the changed-path scope check to catch a controlled violation and explain whether the check prevents a write or detects it afterward.
Review the worker results and integrate one at a time. Shared files, Git integration, and board updates belong to the integrator. Do not allow concurrent stage-all commits in one checkout.
Finally, rerun the combined checks and inspect the actual application. Separate green test reports are not sufficient.
At the debrief, explain which strategy you chose, what could still collide, and how you would handle a worker that needed an unassigned file. That reasoning is the main advanced skill this workshop aims to develop.


## Slide 39: Review, hand off and reflect

Start: 00:58:34.000

The final lab takes fifteen minutes. It is deliberately short because integration and validation have already happened in the previous exercises. Now consolidate the evidence and review the complete result.
Inspect the entire relevant diff, not only the last turn. Look for unrelated edits, changes to shared contracts, and tests that merely mirror the implementation without proving the requirement.
Run the final quality gates and the user-flow check described in the lab. If a check cannot run, mark it as not run with a reason. Do not present it as a success.
Write a handoff that another developer can use without reading the full agent history. Include the outcome, changed paths, contract version or assumptions, exact checks, results, risks, and next decisions.
Then reflect on orchestration. Which tasks were actually independent? Did separate contexts improve focus? Did coordination consume more effort than a direct edit would have? Would you use worktrees, one writer, or a sequential chain for the same task tomorrow?
The workshop ends at three hours. Optional extensions such as hook enforcement, marketplace packaging, or cloud continuity belong after the core session.
A good handoff is the final proof that you can direct agents as engineering collaborators rather than simply collect their completion messages.


## Slide 40: Stop, inspect, narrow and rerun

Start: 01:00:07.500

When a workflow goes wrong, recover from evidence rather than repeatedly issuing a broader prompt.
If an agent or skill is missing, check its path, frontmatter, selected harness, and enabled inventory. In a new worktree, confirm that the customization was committed in the base. A file that exists only in the original checkout is not present in the worktree.
If a worker has the wrong tools, compare the runtime activity with the harness-specific reference. Do not assume an editor completion guarantees availability or enforcement.
If two writers overlap, pause them and inspect the actual files and changes. Preserve useful work, identify the shared contract, and choose one integration owner. Do not run a destructive reset just to get back to a clean-looking state.
Stopping a request does not undo completed terminal commands or external actions. Checkpoints may restore certain workspace edits and chat state, but they are not a general rollback system. Use the documented non-destructive lab reset or normal Git recovery appropriate to the actual state.
After correction, rerun the checks affected by the change. A recovery is complete only when the required behavior is verified again.
These habits matter more than memorizing a particular button label, because the interfaces and defaults will continue to evolve.


## Slide 41: Reliable orchestration is an engineering skill

Start: 01:01:40.500

Let's finish with four ideas you can reuse immediately.
First, compose a role, a recipe, and a task contract. The custom agent defines responsibility. The skill supplies a repeated procedure. The prompt specifies this particular outcome and its constraints.
Second, distinguish context isolation from workspace isolation. Separate subagents or chats can still share files. A worktree separates working copies, while permissions and sandboxing address different risks.
Third, parallelize only genuinely independent work. Freeze contracts, assign explicit ownership, serialize shared-file changes, and use one integrator. Advisory claims help coordination but do not enforce a lock.
Fourth, trust evidence over confident prose. Review the source, run requirement-focused checks, inspect the actual user flow, and report skipped checks honestly.
Before you leave, test your understanding with three questions. Can a read-only reviewer claim it ran tests? No. Does target vscode switch the runtime to Local? No. Can two worktrees pass separately and fail after integration? Yes, which is why we retest the combined result.
The repository's labs, instructor answers, source ledger, captions, and transcript support repeating the workshop. Recheck the product sources before teaching it on a later date. The durable lesson is not a fixed interface: it is the discipline of directing bounded work and proving the result.


## Slide 42: Official sources and availability

Start: 01:03:24.500

This reference slide is an appendix, not extra time added to the live workshop. The complete source ledger contains the official URLs, what each source supports, and the caveats that affect our examples.
The materials were checked against live documentation on November seventh, twenty twenty-six, US Eastern time. VS Code pages fetched for the workshop displayed November fourth update dates where available, and the Universe release is dated October twenty-eighth.
Before a later delivery, verify the actual installed clients, organizational permissions, available harnesses, and customization syntax. Do not infer compatibility from a filename alone.
App Projects, customization marketplaces, connectors, and the VS Code hooks experience have preview limitations. Computer use is experimental. The core labs avoid needing those features or any external service.
The diagrams in this deck are original schematics for orientation. They are not captured product screenshots, and the video is narrated instruction rather than a live-session recording. The PowerPoint uses the visual language of the supplied reference deck without carrying forward its old teaching content or presenter affiliation.
Use the transcript and captions if you prefer reading or need an accessible alternative. Use the hands-on files for exact executable commands and acceptance outputs.

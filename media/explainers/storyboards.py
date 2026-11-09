"""Scripts and scene plans for the two workshop2 explainer videos.

Narration is written to be spoken exactly as typed (numbers spelled out, no
symbols), because the narration generator verifies the spoken transcript word
for word. Every ``cue`` is a phrase that must appear in that scene's narration;
the builder turns it into a time so visuals land when the words are said.
"""

CHAPTER_TAGS = {"attendee": "ATTENDEE GUIDE", "trainer": "TRAINER BRIEFING"}

ATTENDEE = {
    "key": "attendee",
    "title": "Workshop 2 Quick Start - Attendee Guide",
    "scenes": [
        {
            "id": "a01", "chapter": "Welcome", "kind": "title", "art": "hero",
            "narration": (
                "Hey there, and welcome! Today you are going to lead a team of friendly robot helpers "
                "through a real, messy problem. And you will learn why it works, not just which buttons "
                "to press. This is your quick start guide for workshop two. Grab a snack, and let's go!"
            ),
            "params": {
                "lines": ["Workshop 2", "Quick Start"],
                "sub": "Your friendly guide to the labs",
                "badge": "ATTENDEE GUIDE",
                "emojis": [
                    {"ch": "🤖", "cue": "friendly robot helpers"},
                    {"ch": "💡", "cue": "why it works"},
                    {"ch": "🚀", "cue": "let's go"},
                ],
            },
        },
        {
            "id": "a02", "chapter": "Meet Sam", "kind": "art", "art": "avalanche",
            "narration": (
                "First, meet Sam. Sam is the support lead at a little online shop called Harbor and Pine. "
                "It is Monday morning, ten minutes before the big ten o'clock meeting, and the inbox just "
                "exploded with bug reports. Sam has one question to answer: what should the engineers fix first?"
            ),
            "params": {
                "chips": [
                    {"text": "Meet Sam, the support lead", "emoji": "🙋", "color": "cyan", "cue": "meet Sam"},
                    {"text": "Harbor & Pine online shop", "emoji": "🛒", "color": "purple", "cue": "Harbor and Pine"},
                    {"text": "Monday, 9:50 am", "emoji": "⏰", "color": "orange", "cue": "ten minutes before"},
                    {"text": "What should engineers fix first?", "emoji": "❓", "color": "pink",
                     "cue": "what should the engineers fix first"},
                ],
                "motion": "in",
            },
        },
        {
            "id": "a03", "chapter": "The sample app", "kind": "board",
            "narration": (
                "To help Sam, there is a tiny website called the Issue Triage Board. It shows eight pretend "
                "bug reports, each with a title, a category, and a status. It is small on purpose: no "
                "database, nothing to install, just Node. But the board is unfinished, on purpose! Four "
                "things are missing. The priority badges all say untriaged, so nothing is ranked. The search "
                "box does nothing. The summary says detailed counts unlock in lab three. And there is no "
                "export button at all."
            ),
            "params": {
                "cues": {"drop": "eight pretend bug reports", "untriaged": "The priority badges"},
                "callouts": [
                    {"text": "No ranking yet", "target": "badge", "cue": "all say untriaged", "color": "orange"},
                    {"text": "Search does nothing", "target": "search", "cue": "The search box", "color": "pink"},
                    {"text": "Counts are locked", "target": "summary", "cue": "The summary says", "color": "purple"},
                    {"text": "No export button", "target": "export", "cue": "no export button", "color": "cyan"},
                ],
            },
        },
        {
            "id": "a04", "chapter": "Why it matters", "kind": "statement",
            "narration": (
                "So why does that matter? Without it, Sam is guessing. With it, Sam can say: here are the "
                "top problems, here is the proof, and here is what to fix first. Better answers, in "
                "minutes, not hours."
            ),
            "params": {
                "words": [
                    {"text": "GUESSING ✗", "color": "red", "cue": "Sam is guessing"},
                    {"text": "PROOF ✓", "color": "green", "cue": "here is the proof"},
                    {"text": "FIX FIRST 🎯", "color": "cyan", "cue": "what to fix first"},
                ],
                "sub": "Better answers, in minutes, not hours", "sub_cue": "Better answers",
            },
        },
        {
            "id": "a05", "chapter": "The team idea", "kind": "team", "hook": "One giant robot, or a whole team?",
            "narration": (
                "So how do we build it? Not with one giant robot doing everything. With a team! A "
                "coordinator robot makes the plan. A reviewer robot only reads and checks, and it is not "
                "allowed to change a thing. And builder robots each write one small piece. Specialists "
                "usually beat one overloaded generalist."
            ),
            "params": {
                "nodes": [
                    {"name": "Coordinator", "role": "Makes the plan", "color": "cyan", "prop": "clipboard",
                     "cue": "A coordinator robot"},
                    {"name": "Reviewer", "role": "Reads and checks only", "color": "purple", "prop": "magnifier",
                     "lock": True, "cue": "A reviewer robot"},
                    {"name": "Builder A", "role": "Writes one piece", "color": "green", "prop": "wrench",
                     "cue": "builder robots"},
                    {"name": "Builder B", "role": "Writes another piece", "color": "orange", "prop": "wrench",
                     "cue": "one small piece"},
                ],
                "footer": {"text": "Specialists usually beat one overloaded generalist",
                           "cue": "Specialists usually beat"},
            },
        },
        {
            "id": "a06", "chapter": "Three key words", "kind": "cards",
            "narration": (
                "Three words you will hear all day. An agent is a helper with a job description: its role, "
                "its instructions, and the tools it may use. A skill is a recipe card of know-how that a "
                "helper can read when needed. A recipe card gives knowledge, not new powers. And a subagent "
                "is a helper that your main agent hands a small job to, working in its own fresh context so "
                "the main chat stays tidy."
            ),
            "params": {
                "title": "Three words you will hear all day",
                "items": [
                    {"emoji": "🤖", "title": "Agent", "color": "cyan", "cue": "An agent is",
                     "body": "A helper with a job description: role, instructions and allowed tools."},
                    {"emoji": "📖", "title": "Skill", "color": "purple", "cue": "A skill is",
                     "body": "A recipe card of know-how. It gives knowledge, not new powers."},
                    {"emoji": "🧩", "title": "Subagent", "color": "green", "cue": "a subagent is",
                     "body": "A helper with its own fresh context, so the main chat stays tidy."},
                ],
            },
        },
        {
            "id": "a07", "chapter": "Too many cooks", "kind": "art", "art": "chaos",
            "narration": (
                "Now for the tricky part. What happens when several robots work in the same project at the "
                "same time? Chaos! They overwrite each other's work, and nobody knows whose version is right."
            ),
            "params": {
                "chips": [
                    {"text": "Same project, many robots", "emoji": "🤖", "color": "cyan",
                     "cue": "same project at the same time"},
                    {"text": "Work gets overwritten", "emoji": "💥", "color": "orange",
                     "cue": "overwrite each other's work"},
                    {"text": "Whose version is right?", "emoji": "🤷", "color": "pink",
                     "cue": "whose version is right"},
                ],
                "shake_cue": "Chaos", "motion": "out",
            },
        },
        {
            "id": "a08", "chapter": "Lanes and contracts", "kind": "lanes", "art": "harmony",
            "narration": (
                "The fix is lanes. Each robot owns its own files, and nobody else touches them. Shared "
                "rules, which we call frozen contracts, are agreed before anyone starts, so everyone builds "
                "to the same plan. Each robot can even work in its own worktree, which is a separate folder "
                "checkout of the same project. And one integrator robot puts all the pieces together at the "
                "end. One honest warning: worktrees separate files, but not ports or secrets, so two apps "
                "can still fight over the same port."
            ),
            "params": {
                "lanes": [
                    {"name": "Search Worker", "owns": "owns the search file", "color": "green"},
                    {"name": "Summary Worker", "owns": "owns the summary file", "color": "orange"},
                ],
                "integrator": "Integrator",
                "contracts_text": "Frozen contracts: agreed before anyone starts",
                "ports_chips": ["Same port?", "Same secrets?", "Shared services?"],
                "cues": {"lanes": "The fix is lanes", "contracts": "frozen contracts",
                         "worktrees": "its own worktree", "integrator": "one integrator robot",
                         "ports": "One honest warning"},
            },
        },
        {
            "id": "a09", "chapter": "How scoring works", "kind": "score",
            "narration": (
                "Here is how the board decides what is urgent. Take issue one oh one, the checkout bug. "
                "High impact is worth sixty points. It is blocked, so add twenty five. A hundred or more "
                "users are affected, add ten. It has waited a week or more, add five. Sixty plus twenty five "
                "plus ten plus five makes one hundred. And eighty or above is priority one: fix it first!"
            ),
            "params": {
                "issue": {"id": "ISS-101", "title": "Checkout stops on an empty basket", "category": "payments"},
                "rows": [
                    {"label": "High impact", "value": 60, "emoji": "🔥", "cue": "High impact is worth"},
                    {"label": "Blocked workflow", "value": 25, "emoji": "🚧", "cue": "It is blocked"},
                    {"label": "100+ users affected", "value": 10, "emoji": "👥", "cue": "A hundred or more users"},
                    {"label": "7+ days old", "value": 5, "emoji": "📅", "cue": "a week or more"},
                ],
                "total_cue": "Sixty plus twenty five", "badge": "P1", "badge_cue": "priority one",
            },
        },
        {
            "id": "a10", "chapter": "The four labs", "kind": "timeline", "art": "journey",
            "hook": "Four labs, two hours, one finished board",
            "narration": (
                "The rest of today is four hands-on labs, a hundred and twenty minutes in all. Lab one, "
                "thirty minutes: set the team's rules, and build a reviewer and a skill. Lab two, thirty five "
                "minutes: build the priority score. Lab three, forty minutes: add search and the summary at "
                "the same time. Lab four, fifteen minutes: add the export, run the final checks, and write an "
                "honest report."
            ),
            "params": {
                "title": "120 minutes of hands-on labs",
                "segments": [
                    {"label": "Lab 1", "minutes": 30, "sub": "Rules, reviewer, skill", "color": "cyan",
                     "emoji": "🛡️", "cue": "Lab one"},
                    {"label": "Lab 2", "minutes": 35, "sub": "Priority score", "color": "purple",
                     "emoji": "🏅", "cue": "Lab two"},
                    {"label": "Lab 3", "minutes": 40, "sub": "Search + summary", "color": "green",
                     "emoji": "🔎", "cue": "Lab three"},
                    {"label": "Lab 4", "minutes": 15, "sub": "Export + honest report", "color": "orange",
                     "emoji": "🚀", "cue": "Lab four"},
                ],
            },
        },
        {
            "id": "a11", "chapter": "Reading a lab step", "kind": "steps", "hook": "So you never feel lost",
            "narration": (
                "Every step in the lab guides follows the same pattern, so you never feel lost. What to do. "
                "Why you are doing it. How to do it. What you should see. What to try if you don't see it. "
                "And a quick question to reflect on. The why is the most important part, so don't skip it!"
            ),
            "params": {
                "title": "Every lab step has the same shape",
                "items": [
                    {"emoji": "🎯", "title": "What", "body": "What to do", "cue": "What to do"},
                    {"emoji": "💡", "title": "Why", "body": "Why it matters", "cue": "Why you are doing it"},
                    {"emoji": "🛠️", "title": "How", "body": "The exact steps", "cue": "How to do it"},
                    {"emoji": "👀", "title": "You should see", "body": "Your check that it worked",
                     "cue": "What you should see"},
                    {"emoji": "🧯", "title": "If not", "body": "What to try next", "cue": "What to try if"},
                    {"emoji": "🤔", "title": "Reflect", "body": "One quick question", "cue": "to reflect on"},
                ],
                "footer": {"text": "The why is the most important part!", "cue": "The why is the most"},
            },
        },
        {
            "id": "a12", "chapter": "Quick start", "kind": "terminal",
            "narration": (
                "Ready to start? Open a terminal, clone the workshop, and step inside. Run npm test, and "
                "you should see fourteen tests pass. Run npm run smoke for a quick health check. Then run "
                "npm start, and open the address it prints, on port three thousand, in your browser. You "
                "should see eight cards that all say untriaged. And please, do not run npm install. This "
                "project needs nothing extra."
            ),
            "params": {
                "title": "PowerShell",
                "lines": [
                    {"kind": "cmd", "cue": "clone the workshop",
                     "text": "git clone -b adamga-workshop-app-and-hands-on-labs https://github.com/adamga/advancedghcp.git advancedghcp-workshop"},
                    {"kind": "cmd", "cue": "step inside", "text": "cd advancedghcp-workshop"},
                    {"kind": "cmd", "cue": "Run npm test", "text": "npm test"},
                    {"kind": "ok", "cue": "fourteen tests pass", "text": "# tests 14   # pass 14   # fail 0"},
                    {"kind": "cmd", "cue": "Run npm run smoke", "text": "npm run smoke"},
                    {"kind": "ok", "cue": "quick health check", "text": "HTTP smoke passed: 6 routes, 8 fictional issues, and 404 handling."},
                    {"kind": "cmd", "cue": "run npm start", "text": "npm start"},
                    {"kind": "out", "cue": "address it prints", "text": "Issue triage board: http://127.0.0.1:3000"},
                ],
                "side": [
                    {"text": "Eight cards, all 'untriaged'", "emoji": "👀", "color": "green",
                     "cue": "eight cards that all say untriaged"},
                    {"text": "Never run npm install", "emoji": "🚫", "color": "red",
                     "cue": "do not run npm install"},
                ],
            },
        },
        {
            "id": "a13", "chapter": "Be honest", "kind": "stamps", "hook": "Say what really happened",
            "narration": (
                "One tip: be honest in your reports. If a check passed, say passed. If it failed, say "
                "failed. And if you did not run it, say not run. That is a perfectly good answer! Honest "
                "evidence is worth more than a green checkmark."
            ),
            "params": {
                "items": [
                    {"text": "PASSED", "color": "green", "cue": "say passed", "sub": "It ran and succeeded"},
                    {"text": "FAILED", "color": "red", "cue": "say failed", "sub": "It ran and did not"},
                    {"text": "NOT RUN", "color": "orange", "cue": "say not run", "sub": "A perfectly good answer"},
                ],
                "footer": {"text": "Honest evidence beats a green checkmark", "cue": "Honest evidence"},
            },
        },
        {
            "id": "a14", "chapter": "If you get stuck", "kind": "checklist", "art": "detective",
            "narration": (
                "Stuck? Ask yourself three things. Did I restart the app? Am I in the right folder? And "
                "which Copilot setup am I using? Made a mess? Workshop commands save a backup first, so you "
                "can restore. And still stuck? Raise your hand. Every helper in the room has been there."
            ),
            "params": {
                "title": "Stuck? Try this first",
                "items": [
                    {"text": "Did I restart the app?", "sub": "It has no auto-reload", "cue": "Did I restart the app"},
                    {"text": "Am I in the right folder?", "sub": "Check where your terminal is", "cue": "right folder"},
                    {"text": "Which Copilot setup am I using?", "sub": "Local or the Copilot harness",
                     "cue": "which Copilot setup"},
                    {"text": "Made a mess? Restore from backup", "sub": "Workshop commands print a backup ID first",
                     "cue": "Made a mess"},
                    {"text": "Still stuck? Raise your hand", "sub": "Everyone has been there", "cue": "Raise your hand"},
                ],
            },
        },
        {
            "id": "a15", "chapter": "Let's go!", "kind": "art", "art": "celebrate",
            "narration": (
                "That's it! You now know the story, the team, and the plan. By the end of today, Sam will "
                "have an answer, and you will know why it works. See you in lab one!"
            ),
            "params": {
                "chips": [
                    {"text": "You know the story", "emoji": "📖", "color": "cyan", "cue": "the story"},
                    {"text": "You know the team", "emoji": "🤖", "color": "purple", "cue": "the team"},
                    {"text": "You know the plan", "emoji": "🗺️", "color": "green", "cue": "the plan"},
                    {"text": "See you in Lab 1!", "emoji": "🚀", "color": "orange", "cue": "See you in lab one"},
                ],
                "confetti": True, "confetti_cue": "That's it", "motion": "in",
            },
        },
    ],
}

TRAINER = {
    "key": "trainer",
    "title": "Workshop 2 Trainer Briefing",
    "scenes": [
        {
            "id": "t01", "chapter": "Welcome, trainer", "kind": "title", "art": "classroom",
            "narration": (
                "Welcome, trainer! This is your complete briefing for workshop two, the advanced GitHub "
                "Copilot workshop. In a few minutes you will know the story, the approach, exactly how to "
                "get everything ready, what to check, and how to rescue the session when things go "
                "sideways. Let's get you confident."
            ),
            "params": {
                "lines": ["Workshop 2", "Trainer Briefing"],
                "sub": "Setup, approach, checks and rescues",
                "badge": "TRAINER BRIEFING",
                "emojis": [
                    {"ch": "🎓", "cue": "complete briefing"},
                    {"ch": "✅", "cue": "what to check"},
                    {"ch": "🛟", "cue": "rescue the session"},
                ],
            },
        },
        {
            "id": "t02", "chapter": "The story", "kind": "art", "art": "avalanche",
            "narration": (
                "Start with the story, because your attendees will remember it. Sam is the support lead at "
                "Harbor and Pine, a fictional shop. It is Monday, nine fifty. The ten o'clock meeting needs "
                "one answer: what should the engineers fix first? That single question is the scenario for "
                "all four labs."
            ),
            "params": {
                "chips": [
                    {"text": "Sam, support lead", "emoji": "🙋", "color": "cyan", "cue": "Sam is the support lead"},
                    {"text": "Harbor & Pine (fictional)", "emoji": "🛒", "color": "purple", "cue": "a fictional shop"},
                    {"text": "Monday, 9:50 am", "emoji": "⏰", "color": "orange", "cue": "nine fifty"},
                    {"text": "What should engineers fix first?", "emoji": "❓", "color": "pink",
                     "cue": "what should the engineers fix first"},
                ],
                "motion": "in",
            },
        },
        {
            "id": "t03", "chapter": "The sample app", "kind": "board",
            "narration": (
                "The sample app is the Issue Triage Board. It runs on Node twenty two or newer, with a "
                "built-in web server, zero dependencies, and port three thousand. It holds eight fictional "
                "issues, one oh one to one oh eight. Six are active, and two are closed. The workshop ships "
                "it unfinished, with four deliberate stubs: priority says untriaged, search passes "
                "everything through, the summary is locked, and export returns a five oh one with no "
                "download button. Your attendees finish those four pieces."
            ),
            "params": {
                "cues": {"drop": "eight fictional issues", "untriaged": "four deliberate stubs"},
                "callouts": [
                    {"text": "Priority: untriaged", "target": "badge", "cue": "priority says untriaged", "color": "orange"},
                    {"text": "Search: passthrough", "target": "search", "cue": "search passes everything through", "color": "pink"},
                    {"text": "Summary: locked", "target": "summary", "cue": "the summary is locked", "color": "purple"},
                    {"text": "Export: HTTP 501", "target": "export", "cue": "export returns a five oh one", "color": "cyan"},
                ],
            },
        },
        {
            "id": "t04", "chapter": "The real goal", "kind": "statement",
            "narration": (
                "Here is the real goal. Attendees should leave understanding why, not just what. Every lab "
                "step follows the same pattern: what, why, how, what you should see, what if not, and "
                "reflect. If you remember one thing to say out loud, it is this: the why is the lesson."
            ),
            "params": {
                "words": [
                    {"text": "NOT JUST WHAT 🛠️", "color": "orange", "cue": "not just what"},
                    {"text": "THE WHY 💡", "color": "cyan", "cue": "the why is the lesson"},
                ],
                "sub": "What - Why - How - You should see - If not - Reflect", "sub_cue": "Every lab step follows",
            },
        },
        {
            "id": "t05", "chapter": "Five myths to bust", "kind": "pairs",
            "narration": (
                "Five ideas trip people up, so teach them early. First, subagents give context isolation, "
                "not file isolation: a subagent has a fresh context, but it can still edit the same files. "
                "Second, skills grant no tools: a skill is a recipe card, and tools come from the agent. "
                "Third, a worktree isolates files, but not ports or secrets. Fourth, ownership and leases "
                "are advisory: they work because everyone agrees to follow them. Fifth, a local handoff is "
                "not delegation: two separate chats are not subagents."
            ),
            "params": {
                "title": "Myth  vs  Fact",
                "rows": [
                    {"myth": "Subagents keep my files safe", "fact": "Fresh context, same files", "cue": "First, subagents"},
                    {"myth": "A skill gives an agent new tools", "fact": "A recipe card. Tools come from the agent", "cue": "Second, skills"},
                    {"myth": "Worktrees isolate everything", "fact": "Files and index only, not ports or secrets", "cue": "Third, a worktree"},
                    {"myth": "Ownership locks the files", "fact": "It is advisory: a team agreement", "cue": "Fourth, ownership"},
                    {"myth": "Two chats are subagents", "fact": "A local handoff is not delegation", "cue": "Fifth, a local handoff"},
                ],
            },
        },
        {
            "id": "t06", "chapter": "The approach: a team", "kind": "team",
            "narration": (
                "The approach is a small team. A coordinator plans and delegates. A read-only reviewer "
                "checks the work and cannot edit. In lab three there are two workers, search and summary, "
                "and one integrator who merges the results and runs the gates. The default route is a "
                "single writer, which is the safest. The parallel route is the stretch goal, and it only "
                "works with frozen contracts and clear ownership."
            ),
            "params": {
                "nodes": [
                    {"name": "Coordinator", "role": "Plans and delegates", "color": "cyan", "prop": "clipboard",
                     "cue": "A coordinator plans"},
                    {"name": "Reviewer", "role": "Read-only checks", "color": "purple", "prop": "magnifier",
                     "lock": True, "cue": "A read-only reviewer"},
                    {"name": "Search Worker", "role": "Owns search", "color": "green", "prop": "wrench",
                     "cue": "two workers"},
                    {"name": "Summary Worker", "role": "Owns summary", "color": "orange", "prop": "wrench",
                     "cue": "search and summary"},
                    {"name": "Integrator", "role": "Merges + runs gates", "color": "pink", "prop": "hat",
                     "cue": "one integrator"},
                ],
                "footer": {"text": "Default: single writer.  Stretch: parallel with frozen contracts",
                           "cue": "The default route"},
            },
        },
        {
            "id": "t07", "chapter": "Why ownership matters", "kind": "art", "art": "chaos",
            "narration": (
                "Why bother with ownership? Because when two helpers edit the same file at the same time, "
                "one silently erases the other. Nobody notices until the tests fail, or worse, until they "
                "don't."
            ),
            "params": {
                "chips": [
                    {"text": "Two helpers, one file", "emoji": "👯", "color": "cyan", "cue": "two helpers edit the same file"},
                    {"text": "One silently erases the other", "emoji": "🫥", "color": "orange", "cue": "silently erases"},
                    {"text": "Worse: tests still pass", "emoji": "😬", "color": "pink", "cue": "or worse"},
                ],
                "shake_cue": "silently erases", "motion": "out",
            },
        },
        {
            "id": "t08", "chapter": "Four layers of protection", "kind": "lanes", "art": "harmony",
            "narration": (
                "The cure is layers of protection. Layer one: lanes. Each worker owns named files, like "
                "the search file or the summary file, and nobody else touches them. Layer two: frozen "
                "contracts, which are written agreements about function names and shapes, so workers can "
                "build in parallel without guessing. Layer three: one integrator, the only one who touches "
                "the shared wiring. Layer four: worktrees, separate checkouts for each worker. And "
                "remember the caveat: worktrees do not isolate ports, secrets, or shared services, so give "
                "each server its own port. When all else fails, drop to the safe route: one writer at a time."
            ),
            "params": {
                "lanes": [
                    {"name": "Search Worker", "owns": "owns the search file", "color": "green"},
                    {"name": "Summary Worker", "owns": "owns the summary file", "color": "orange"},
                ],
                "integrator": "Integrator",
                "contracts_text": "Frozen contracts: names + shapes, agreed first",
                "ports_chips": ["Own port each", "Own secrets", "Shared services"],
                "cues": {"lanes": "Layer one", "contracts": "Layer two", "integrator": "Layer three",
                         "worktrees": "Layer four", "ports": "remember the caveat"},
            },
        },
        {
            "id": "t09", "chapter": "Scoring rule", "kind": "score",
            "narration": (
                "Learn the scoring rule so you can check answers quickly. Issue one oh one is high impact, "
                "worth sixty. It is blocked, add twenty five. A hundred or more users, add ten. A week old "
                "or more, add five. That makes one hundred, and priority one starts at eighty. Priority two "
                "starts at forty. Everything else is priority three. Closed issues are always zero."
            ),
            "params": {
                "issue": {"id": "ISS-101", "title": "Checkout stops on an empty basket", "category": "payments"},
                "rows": [
                    {"label": "High impact", "value": 60, "emoji": "🔥", "cue": "high impact, worth sixty"},
                    {"label": "Blocked workflow", "value": 25, "emoji": "🚧", "cue": "It is blocked"},
                    {"label": "100+ users affected", "value": 10, "emoji": "👥", "cue": "A hundred or more users"},
                    {"label": "7+ days old", "value": 5, "emoji": "📅", "cue": "A week old"},
                ],
                "total_cue": "That makes one hundred", "badge": "P1", "badge_cue": "priority one starts",
                "legend": [
                    {"text": "P1 = 80 or more", "color": "red", "cue": "priority one starts"},
                    {"text": "P2 = 40 or more", "color": "orange", "cue": "Priority two"},
                    {"text": "P3 = the rest", "color": "green", "cue": "Everything else"},
                    {"text": "Closed = 0", "color": "muted", "cue": "Closed issues are always"},
                ],
            },
        },
        {
            "id": "t10", "chapter": "The answer key", "kind": "table",
            "narration": (
                "Here is the full answer key. Issue one oh one: one hundred, priority one. One oh two: "
                "fifty five, priority two. One oh three: fifteen, priority three. One oh four: forty, "
                "priority two, right on the line. One oh five is closed, so zero. One oh six: thirty five, "
                "priority three. One oh seven: ten, priority three. And one oh eight is closed, so zero."
            ),
            "params": {
                "title": "Expected priority for the eight issues",
                "headers": ["Issue", "Title", "Score", "Level"],
                "widths": [0.14, 0.52, 0.16, 0.18],
                "rows": [
                    {"cells": ["ISS-101", "Checkout stops on an empty basket", "100", "P1"], "tone": "red", "cue": "Issue one oh one"},
                    {"cells": ["ISS-102", "Keyboard focus disappears in the menu", "55", "P2"], "tone": "orange", "cue": "One oh two"},
                    {"cells": ["ISS-103", "Export heading has a typo", "15", "P3"], "tone": "green", "cue": "One oh three"},
                    {"cells": ["ISS-104", "Search ignores uppercase words", "40", "P2"], "tone": "orange", "cue": "One oh four"},
                    {"cells": ["ISS-105", "Receipt uses the wrong sample currency", "0 (closed)", "P3"], "tone": "muted", "cue": "One oh five"},
                    {"cells": ["ISS-106", "Small-screen chart overlaps its legend", "35", "P3"], "tone": "green", "cue": "One oh six"},
                    {"cells": ["ISS-107", "Image alternative text is missing", "10", "P3"], "tone": "green", "cue": "One oh seven"},
                    {"cells": ["ISS-108", "Saved search loses its label", "0 (closed)", "P3"], "tone": "muted", "cue": "one oh eight is closed"},
                ],
            },
        },
        {
            "id": "t11", "chapter": "What done looks like", "kind": "checklist",
            "narration": (
                "And here is what done looks like. Searching payments returns two cards, one oh one and one "
                "oh five. Searching keyboard returns one oh two. The summary shows eight total, six active, "
                "and two active blocked. The export button says download evidence JSON, and the file "
                "contains only issue one oh one."
            ),
            "params": {
                "title": "The finished board",
                "items": [
                    {"text": "Search PAYMENTS: two cards", "sub": "ISS-101 and ISS-105", "cue": "Searching payments"},
                    {"text": "Search KEYBOARD: one card", "sub": "ISS-102", "cue": "Searching keyboard"},
                    {"text": "Summary: 8 total, 6 active, 2 active blocked", "sub": "Two issues in each category",
                     "cue": "The summary shows"},
                    {"text": "'Download evidence JSON' button", "sub": "The file contains only ISS-101 (P1)",
                     "cue": "The export button"},
                ],
            },
        },
        {
            "id": "t12", "chapter": "Plan the clock", "kind": "timeline", "art": "journey",
            "narration": (
                "Plan the clock. The live session is three hours. Slides one to ten are the story and a "
                "demo, the first fifteen minutes. Slides eleven to twenty three cover agents and skills, "
                "with two demos, until thirty five minutes. Slides twenty four to thirty five cover "
                "ownership and contracts, with a third demo, until the one hour mark. Then two hours of "
                "labs: thirty, thirty five, forty, and fifteen minutes."
            ),
            "params": {
                "title": "The 180-minute plan",
                "segments": [
                    {"label": "Story", "minutes": 15, "sub": "Slides 1-10", "color": "blue", "emoji": "📖", "cue": "Slides one to ten"},
                    {"label": "Agents", "minutes": 20, "sub": "Slides 11-23", "color": "cyan", "emoji": "🤖", "cue": "Slides eleven to twenty three"},
                    {"label": "Ownership", "minutes": 25, "sub": "Slides 24-35", "color": "purple", "emoji": "🧭", "cue": "Slides twenty four"},
                    {"label": "Lab 1", "minutes": 30, "sub": "Rules + reviewer", "color": "green", "emoji": "🛡️", "cue": "Then two hours of labs"},
                    {"label": "Lab 2", "minutes": 35, "sub": "Priority", "color": "orange", "emoji": "🏅", "cue": "thirty five, forty"},
                    {"label": "Lab 3", "minutes": 40, "sub": "Search + summary", "color": "pink", "emoji": "🔎", "cue": "forty, and fifteen"},
                    {"label": "Lab 4", "minutes": 15, "sub": "Export + report", "color": "yellow", "emoji": "🚀", "cue": "and fifteen minutes"},
                ],
                "total_label": "60 min presenting + 120 min hands-on = 180 min",
            },
        },
        {
            "id": "t13", "chapter": "Lab by lab", "kind": "cards",
            "narration": (
                "Here is what each lab does. Lab one is the safe warm-up. Attendees write team rules, and "
                "build a read-only reviewer and a triage policy skill. They do not change the app at all. "
                "Lab two builds the priority feature, with a coordinator, read-only research, one builder, "
                "quality gates, and a fresh review. Lab three is the big one: search and summary in "
                "parallel. Route A, one writer, is the default. Route B uses two workers and frozen "
                "contracts. Lab four adds the evidence export, runs the final gates, and ends with a "
                "truthful report, where anything not run is marked not run, then a short retrospective."
            ),
            "params": {
                "title": "Four labs, four ideas",
                "items": [
                    {"emoji": "🛡️", "title": "Lab 1 · 30 min", "color": "cyan", "cue": "Lab one is the safe",
                     "body": "Warm-up. Team rules, a read-only reviewer, a triage policy skill. No app changes."},
                    {"emoji": "🏅", "title": "Lab 2 · 35 min", "color": "purple", "cue": "Lab two builds",
                     "body": "Priority. Coordinator, read-only research, one builder, gates, fresh review."},
                    {"emoji": "🔎", "title": "Lab 3 · 40 min", "color": "green", "cue": "Lab three is the big one",
                     "body": "Search + summary. Route A one writer (default). Route B two workers + contracts."},
                    {"emoji": "🚀", "title": "Lab 4 · 15 min", "color": "orange", "cue": "Lab four adds",
                     "body": "Evidence export, final gates, truthful report (NOT RUN where true), retrospective."},
                ],
            },
        },
        {
            "id": "t14", "chapter": "Two days before", "kind": "checklist",
            "narration": (
                "Two days before class, send attendees the preflight. It takes fifteen to twenty five "
                "minutes and is not part of the three hours. They need Node twenty two or newer, Git, a "
                "modern browser, VS Code with Copilot or the Copilot app, and a Copilot account. "
                "Optionally they can read the story and concepts docs, thirty five to forty five minutes in "
                "all. No cloud account, Azure, or MCP setup is needed. But policies, quota, and rollouts "
                "can limit agents, so ask people to check early."
            ),
            "params": {
                "title": "T-2 days: send the preflight",
                "items": [
                    {"text": "Preflight: 15-25 minutes", "sub": "Not part of the three hours", "cue": "send attendees the preflight"},
                    {"text": "Node 22+  and  Git", "sub": "Plus a modern browser", "cue": "They need Node"},
                    {"text": "VS Code + Copilot, or the Copilot app", "sub": "And a Copilot account", "cue": "VS Code with Copilot"},
                    {"text": "Optional: read the story + concepts docs", "sub": "35-45 minutes in all", "cue": "Optionally they can read"},
                    {"text": "No cloud account, Azure or MCP needed", "sub": "Policies, quota and rollouts can still limit agents", "cue": "No cloud account"},
                ],
            },
        },
        {
            "id": "t15", "chapter": "Getting the code", "kind": "terminal",
            "narration": (
                "Give them the code one of two ways. Online: clone with the dash b flag, naming the "
                "workshop branch. The remote main branch is empty, so a plain clone gives an empty folder, "
                "and that is the number one setup mistake. Offline: use the sample app and labs zip. It has "
                "no git history, so run git init and make a baseline commit before the worktree labs. And "
                "never run npm install. The app has zero dependencies."
            ),
            "params": {
                "title": "PowerShell",
                "lines": [
                    {"kind": "note", "cue": "Online", "text": "# Online: clone the workshop branch"},
                    {"kind": "cmd", "cue": "clone with the dash b flag",
                     "text": "git clone -b adamga-workshop-app-and-hands-on-labs https://github.com/adamga/advancedghcp.git advancedghcp-workshop"},
                    {"kind": "warn", "cue": "plain clone gives an empty folder", "text": "# Forgot -b?  main is empty, so the folder is empty!"},
                    {"kind": "note", "cue": "Offline", "text": "# Offline: unzip sample-app-and-labs.zip, then give it a baseline"},
                    {"kind": "cmd", "cue": "run git init", "text": "git init"},
                    {"kind": "cmd", "cue": "make a baseline commit", "text": "git add -A"},
                    {"kind": "cmd", "cue": "before the worktree labs", "text": "git commit -m \"workshop baseline\""},
                ],
                "side": [
                    {"text": "#1 setup mistake: forgetting -b", "emoji": "⚠️", "color": "orange", "cue": "number one setup mistake"},
                    {"text": "Never run npm install", "emoji": "🚫", "color": "red", "cue": "never run npm install"},
                ],
            },
        },
        {
            "id": "t16", "chapter": "Verify before class", "kind": "table",
            "narration": (
                "Before class, run four checks. Npm test should show fourteen passing tests. Npm run smoke "
                "should say HTTP smoke passed. Npm run check customizations should report zero active "
                "agents and zero active skills, which is correct, because lab one creates them. And npm run "
                "verify solutions runs twenty six tests against the instructor answers. Heads up: the "
                "acceptance checks, like npm run acceptance priority, are expected to fail on the starter. "
                "That is by design."
            ),
            "params": {
                "title": "Facilitator checks on a clean starter checkout",
                "headers": ["Command", "You should see", "Why"],
                "widths": [0.34, 0.38, 0.28],
                "rows": [
                    {"cells": ["npm test", "# tests 14, # pass 14, # fail 0", "Baseline is healthy"], "tone": "green", "cue": "Npm test should show"},
                    {"cells": ["npm run smoke", "HTTP smoke passed: 6 routes", "Server and routes work"], "tone": "green", "cue": "Npm run smoke"},
                    {"cells": ["npm run check:customizations", "0 active agents, 0 active skills", "Zero is right: Lab 1 creates them"], "tone": "green", "cue": "Npm run check customizations"},
                    {"cells": ["npm run verify:solutions", "26 tests pass", "Instructor answers are sound"], "tone": "green", "cue": "verify solutions runs"},
                    {"cells": ["npm run acceptance -- priority", "FAILS on the starter", "By design: the lab's finish line"], "tone": "orange", "cue": "acceptance checks"},
                ],
            },
        },
        {
            "id": "t17", "chapter": "Day-of prep", "kind": "checklist",
            "narration": (
                "On the day, prepare the room. Start from a clean starter checkout. Check the board at a "
                "narrow width, and with tab key navigation. Confirm that Copilot works and that quota is "
                "available. To show the finished board, run npm run start solutions on a different port, "
                "but never show an all-green board before attendees start. Stop only the servers you "
                "started. And have your manual, one-writer fallback ready."
            ),
            "params": {
                "title": "Day-of checklist",
                "items": [
                    {"text": "Start from a clean starter checkout", "sub": "Never mutate attendee source behind the scenes", "cue": "clean starter checkout"},
                    {"text": "Narrow width + keyboard tab navigation", "sub": "Check the board's responsive view", "cue": "narrow width"},
                    {"text": "Copilot works and quota is available", "sub": "Check policies for your account", "cue": "Confirm that Copilot works"},
                    {"text": "Demo: npm run start:solutions, different port", "sub": "Never show an all-green board before attendees start", "cue": "To show the finished board"},
                    {"text": "Stop only servers you started", "sub": "Keep your manual one-writer fallback ready", "cue": "Stop only the servers"},
                ],
            },
        },
        {
            "id": "t18", "chapter": "Surfaces and fallbacks", "kind": "cards",
            "narration": (
                "Check your surfaces and harnesses. Keep the Local profile and the Copilot profile "
                "separate. New VS Code sessions default to the Copilot harness, and Local needs an "
                "explicit fresh session. Check the agent's tool list, and check whether the Copilot app "
                "auto creates worktrees. If the Agents window or subagents are missing, fall back to "
                "ordinary chat with one writer. Never call two separate chats subagent delegation, and "
                "never bypass restrictions."
            ),
            "params": {
                "title": "Know what you actually have",
                "items": [
                    {"emoji": "🔀", "title": "Keep profiles apart", "color": "cyan", "cue": "Keep the Local profile",
                     "body": "Local and Copilot are different. New VS Code sessions default to Copilot; Local needs a fresh session."},
                    {"emoji": "🛠️", "title": "Check the tools", "color": "purple", "cue": "Check the agent's tool list",
                     "body": "Look at the agent's tool list. Does the Copilot app auto-create worktrees?"},
                    {"emoji": "🛟", "title": "Have a fallback", "color": "green", "cue": "If the Agents window",
                     "body": "No Agents window or subagents? Use ordinary chat, one writer. Never bypass restrictions."},
                ],
            },
        },
        {
            "id": "t19", "chapter": "Troubleshooting", "kind": "art", "art": "detective",
            "narration": (
                "Troubleshooting time. Three first questions solve most problems. Did I restart the app? "
                "Am I in the right folder? And which harness am I on? Also, expected unfinished behavior "
                "is not a bug. Untriaged badges and a five oh one on export are the starter working as "
                "designed."
            ),
            "params": {
                "chips": [
                    {"text": "Did I restart the app?", "emoji": "🔄", "color": "cyan", "cue": "Did I restart the app"},
                    {"text": "Am I in the right folder?", "emoji": "📂", "color": "purple", "cue": "right folder"},
                    {"text": "Which harness am I on?", "emoji": "🧭", "color": "green", "cue": "which harness"},
                    {"text": "Unfinished = by design, not a bug", "emoji": "🧪", "color": "orange", "cue": "not a bug"},
                ],
                "motion": "in",
            },
        },
        {
            "id": "t20", "chapter": "Common fixes", "kind": "table",
            "narration": (
                "Here are the common fixes. If the clone is empty, someone forgot the dash b. If port "
                "three thousand is busy, set a different port, then run npm start. If PowerShell blocks "
                "npm, use npm dot cmd. If an agent is missing from the picker, or approvals are blocked, "
                "use the manual route. And if two sessions see different edits, remember worktrees: each "
                "one has its own files."
            ),
            "params": {
                "title": "Symptom and fix",
                "headers": ["Symptom", "Fix"],
                "widths": [0.38, 0.62],
                "rows": [
                    {"cells": ["Clone is empty", "Clone again with -b adamga-workshop-app-and-hands-on-labs"], "tone": "orange", "cue": "the clone is empty"},
                    {"cells": ["Port 3000 is busy", "$env:PORT='3001'; npm start   (bash: PORT=3001 npm start)"], "tone": "orange", "cue": "port three thousand is busy"},
                    {"cells": ["PowerShell blocks npm.ps1", "Use npm.cmd instead"], "tone": "orange", "cue": "blocks npm"},
                    {"cells": ["Agent missing from the picker", "Check profile and harness; otherwise use the manual route"], "tone": "orange", "cue": "missing from the picker"},
                    {"cells": ["Approvals are blocked", "Use the manual route; never bypass restrictions"], "tone": "orange", "cue": "approvals are blocked"},
                    {"cells": ["Two sessions see different edits", "Worktrees: each one has its own files. That is normal"], "tone": "green", "cue": "see different edits"},
                ],
            },
        },
        {
            "id": "t21", "chapter": "Pacing rescues", "kind": "table",
            "narration": (
                "Watch the clock with the rescue table. At one hour seven minutes, if people are stuck on "
                "rules, offer the two acceptable rules. At one hour nineteen, use the contract policy, "
                "not invented business rules. At two oh five, default everyone to single writer Route A. "
                "At two twenty, the separate feature installers can rescue Route A and Route B "
                "independently. At two forty nine, apply the handoff if needed. At two fifty three, any "
                "command you did not run is marked not run. And at two fifty six, any unresolved failure "
                "is reported as not ready."
            ),
            "params": {
                "title": "Live pacing and rescue triggers",
                "headers": ["Clock", "Step", "Rescue"],
                "widths": [0.14, 0.40, 0.46],
                "rows": [
                    {"cells": ["1:07", "Lab 1 step 2: write two rules", "Offer the two acceptable rules"], "tone": "cyan", "cue": "At one hour seven minutes"},
                    {"cells": ["1:19", "Lab 1 step 4: finish the skill", "Use the contract policy, not invented rules"], "tone": "cyan", "cue": "At one hour nineteen"},
                    {"cells": ["2:05", "Lab 3 intro", "Default to single-writer Route A"], "tone": "purple", "cue": "At two oh five"},
                    {"cells": ["2:20", "Lab 3 step 3: implement", "Feature installers rescue A and B independently"], "tone": "purple", "cue": "At two twenty"},
                    {"cells": ["2:49", "Lab 4 step 2: final gates", "Apply the handoff if needed"], "tone": "orange", "cue": "At two forty nine"},
                    {"cells": ["2:53", "Lab 4 step 3: integrated review", "Unrun commands are NOT RUN"], "tone": "orange", "cue": "At two fifty three"},
                    {"cells": ["2:56", "Lab 4 step 4: truthful report", "Any unresolved failure is 'not ready'"], "tone": "orange", "cue": "at two fifty six"},
                ],
            },
        },
        {
            "id": "t22", "chapter": "If agents collide", "kind": "steps", "hook": "Don't panic: six calm steps",
            "narration": (
                "If agents collide, don't panic, and never use a destructive reset. Follow six steps. Stop "
                "all writers. Preserve the diff as a patch file. Name the lease owner. Assign one "
                "integrator. Re-run the gates. And write down what happened. To undo workshop changes, "
                "every workshop command prints a backup ID before it writes. Run npm run workshop restore "
                "with that exact ID. Restore saves a rescue backup first, and a partial ID is rejected."
            ),
            "params": {
                "title": "Collision protocol: six calm steps",
                "items": [
                    {"emoji": "🛑", "title": "Stop all writers", "body": "Pause every agent", "cue": "Stop all writers"},
                    {"emoji": "💾", "title": "Preserve the diff", "body": "Save it as a patch file", "cue": "Preserve the diff"},
                    {"emoji": "🏷️", "title": "Name the lease owner", "body": "Who owned those files?", "cue": "Name the lease owner"},
                    {"emoji": "👷", "title": "One integrator", "body": "Exactly one person merges", "cue": "Assign one integrator"},
                    {"emoji": "🚦", "title": "Re-run the gates", "body": "Tests, smoke, checks", "cue": "Re-run the gates"},
                    {"emoji": "📝", "title": "Write it down", "body": "What happened and why", "cue": "write down what happened"},
                ],
                "footer": {"text": "Undo: npm run workshop:restore -- <exact backup ID>", "cue": "backup ID before it writes"},
            },
        },
        {
            "id": "t23", "chapter": "Rehearse and debrief", "kind": "cards",
            "narration": (
                "Finally, rehearse. Install all four answers on a practice copy, check acceptance and "
                "tests, which should give eighteen passing tests, then restore to the starter. At the end "
                "of lab four, ask four why questions. Why did we freeze the contract before anyone wrote "
                "code? Why was the reviewer read-only? Why is a passing test not the same as ready? And "
                "what would you not delegate, and why? If attendees can answer, they have the why."
            ),
            "params": {
                "title": "Four closing 'why' questions",
                "pre": [
                    {"emoji": "🧪", "text": "Install all four answers", "color": "cyan", "cue": "Install all four answers"},
                    {"emoji": "✅", "text": "Check acceptance and tests", "color": "green", "cue": "check acceptance and tests"},
                    {"emoji": "🔢", "text": "Expect 18 passing tests", "color": "orange", "cue": "eighteen passing tests"},
                    {"emoji": "🔄", "text": "Restore to the starter", "color": "purple", "cue": "restore to the starter"},
                ],
                "items": [
                    {"emoji": "🧊", "title": "Why freeze the contract first?", "color": "cyan", "cue": "freeze the contract"},
                    {"emoji": "👓", "title": "Why was the reviewer read-only?", "color": "purple", "cue": "Why was the reviewer"},
                    {"emoji": "✅", "title": "Why isn't a passing test 'ready'?", "color": "green", "cue": "passing test not the same"},
                    {"emoji": "🙅", "title": "What would you not delegate, and why?", "color": "orange", "cue": "not delegate"},
                ],
                "footer": {"text": "Rehearse: apply all four answers, expect 18 passing tests, restore to starter",
                           "cue": "Finally, rehearse"},
            },
        },
        {
            "id": "t24", "chapter": "You've got this", "kind": "art", "art": "celebrate",
            "narration": (
                "That's the whole briefing! You know the story, the team approach, the setup, the checks, "
                "and the rescues. Go make your attendees' day, and remember: the why is the lesson. Have a "
                "fantastic workshop!"
            ),
            "params": {
                "chips": [
                    {"text": "Story, team and approach", "emoji": "🤖", "color": "cyan", "cue": "the story, the team approach"},
                    {"text": "Setup, checks and rescues", "emoji": "🧰", "color": "purple", "cue": "the setup, the checks"},
                    {"text": "The why is the lesson", "emoji": "💡", "color": "orange", "cue": "the why is the lesson"},
                ],
                "confetti": True, "confetti_cue": "That's the whole briefing", "motion": "in",
            },
        },
    ],
}

VIDEOS = {"attendee": ATTENDEE, "trainer": TRAINER}

---
name: Summary Worker
description: Implement only the frozen issue-summary feature and its owned tests.
target: vscode
tools: ['read', 'search', 'edit']
agents: []
---
Implement only src/features/summary.mjs and tests/features/summary.test.mjs.
Read workshop2/contracts.md and the supplied task. Do not edit any other file,
execute commands, use the network, delegate, or perform git operations.
Count only supplied issues; active means not closed; blocked means active and
blocked; category keys sort alphabetically. Do not import the search feature.
Return changed paths, rationale, acceptance cases, and NOT RUN commands.
Stop when the assigned implementation and tests are ready for human validation.

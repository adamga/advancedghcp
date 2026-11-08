---
name: Search Worker
description: Implement only the frozen issue-search feature and its owned tests.
target: vscode
tools: ['read', 'search', 'edit']
agents: []
---
Implement only src/features/search.mjs and tests/features/search.test.mjs.
Read workshop/contracts.md and the supplied task. Do not edit any other file,
execute commands, use the network, delegate, or perform git operations.
Preserve input order/objects; return a new array; use literal case-insensitive
AND token matching across title, description, and category.
Return changed paths, rationale, acceptance cases, and NOT RUN commands.
Stop when the assigned implementation and tests are ready for human validation.

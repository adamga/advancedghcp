# Lab 3 advisory task board

Only the human integrator edits this board. Workers report, not write here.
Store your exercise copy under `.workshop-reports` if desired.

**Contract:** workshop2/contracts.md v1; exports and shared wiring frozen.
**Integrator:** fill in a role label, not personal information.
**Review:** read-only research before any implementation.
**Shared resources:** package files, fixtures, server/UI, this board, Git
index/branch, server ports/processes. One designated owner; serialize changes.

| Task | Owner role | Exclusive files | Dependency | State | Lease/release | Acceptance |
|---|---|---|---|---|---|---|
| A search | Search Worker | src/features/search.mjs; tests/features/search.test.mjs | Contract frozen | unclaimed | not granted | npm run acceptance -- search |
| B summary | Summary Worker | src/features/summary.mjs; tests/features/summary.test.mjs | Contract frozen; not A | unclaimed | not granted | npm run acceptance -- summary |
| Integrate | Integrator | Shared wiring only if needed; final report/Git | A and B stopped, reports accepted | waiting | not granted | npm test; both acceptance; smoke |

Use states unclaimed -> researching -> ready -> writing -> validating ->
released -> integrated, or blocked with a reason. A "lease" is a human agreement,
not a lock, sandbox, permission boundary, or automatic timeout. On collision,
stop both writers, preserve both changes, reassign one integration writer, and
review the diff. Never overwrite another worker's current edit.

# Preserve, restore, or restart safely

Stop active writers first. A branch name does not protect uncommitted edits.
Do not use `git reset --hard`, `git checkout --`, broad recursive deletion,
or a force push to recover a workshop exercise.

## Before an experiment

Use a clean committed checkpoint or save your diff and copies of any untracked
files outside source. A patch alone does **not** include untracked files.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force .workshop-reports | Out-Null
git --no-pager diff --binary --output=.workshop-reports\before-experiment.patch
git --no-pager status --short
```

macOS/Linux:

```bash
mkdir -p .workshop-reports
git --no-pager diff --binary --output=.workshop-reports/before-experiment.patch
git --no-pager status --short
```

Copy any listed untracked work you want to preserve, or commit only the explicit
owned paths. Do not stage secrets or unrelated edits. Only the integrator uses
the shared Git index while tasks are active.

## Workshop backups

`workshop:setup`, `workshop:apply`, and `workshop:starter` write a snapshot of every
**named target's current content or absence** to `.workshop-backups/<id>/manifest.json`
before changing any file. The printed backup ID is your restore handle.
These ignored local backups can contain your exercise edits; do not publish them.

```text
npm run workshop:restore -- <exact-printed-backup-id>
```

Replace the placeholder with the actual ID; do not type angle brackets. Restore
first saves another **rescue backup of current contents**, then restores the
original snapshot. A file that was absent before setup is removed by exact name;
unrelated files are not touched. Backups stay available. Restore uses a fixed
allowlist, rejects invalid paths, and refuses symlink targets.

The operation is **not a multi-file lock or transaction**. It checks for changes
before each write but cannot prevent every race. Never run it while an agent or
editor is actively changing those targets. If it stops partway, the printed backup
exists: inspect both current state and snapshot before restoring again.
Undo multiple installs in reverse order to recover a previous complete checkpoint.
Empty resource directories may remain; they contain no active SKILL.md.

Example:

```text
npm run workshop:apply -- priority
# Save the printed ID.
npm run acceptance -- priority
npm run workshop:restore -- <that-id>
npm test
```

The restore may make priority acceptance fail again because you are intentionally
back at the starter. That is expected; baseline tests should pass.

## Reset only the named exercise features

```text
npm run workshop:starter
npm test
npm run smoke
```

This saves a backup, overwrites the **four named feature modules** from the explicit
starter snapshots, and removes only the four named task-owned
`tests/features/{priority,search,summary,handoff}.test.mjs` files. It leaves other
tests, repository instructions, active customizations, notes, and unrelated files
unchanged. Review that exact scope before running it. If other tests expect
completed features, preserve/reconcile those tests rather than deleting them.
Use the saved backup ID to undo the starter reset.

To undo Lab 1 customizations, use its original setup/apply backup ID. That
preserves current contents first and restores only the named installed resources.
Your manual instruction-file edits are not part of that installer snapshot:
keep their saved diff/commit and review them yourself.

## Start again without altering the current checkout

The safest full restart is a new clone/folder while keeping the current folder
intact. Choose a new, unused destination:

Windows PowerShell:

```powershell
git clone https://github.com/adamga/advancedghcp.git advancedghcp-workshop-fresh
Set-Location .\advancedghcp-workshop-fresh
npm test
```

macOS/Linux:

```bash
git clone https://github.com/adamga/advancedghcp.git advancedghcp-workshop-fresh
cd advancedghcp-workshop-fresh
npm test
```

No directory deletion is required. For an intentional committed mistake on your
own integration branch, inspect the commit and use a normal `git revert <commit>`
to produce a new undo commit. Resolve conflicts explicitly; do not force another
worker's state away.

## Collision protocol

Stop both writers, identify affected paths, preserve both patches/untracked
files, and appoint one integrator. Compare versions against contract v1, reconcile
the intended changes, and run both task gates plus combined HTTP observations.
Release/reassign advisory leases before resuming. A stale task-board entry is
not permission to overwrite a live edit.

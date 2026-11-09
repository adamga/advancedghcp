# Restore and recover: undo a mistake safely

**Why this page exists.** Working with agents means files change quickly, and
sometimes in a direction you did not want. This page is your **undo toolkit**.
The point is that you can try things boldly *because* you know how to get back.

> **Read this once before Lab 1.** You will probably never need it, but it is
> much calmer to read it *before* something goes wrong.

## Golden rules

1. **Stop the writers first.** Before restoring anything, make sure no agent or
   session is still editing files. A restore racing a writer is how you lose work.
2. **Save before you experiment.** The workshop commands make a backup for you.
   For your own risky experiments, save a patch (below).
3. **Never use these** to "fix" a workshop checkout. They throw work away with no
   way back:
   - `git reset --hard`
   - `git checkout -- .`
   - broad deletion (`Remove-Item -Recurse` or `rm -rf` on the project)
   - a force push
4. **Read the message before acting.** Every workshop command prints exactly what
   it wrote and what it backed up.

## What gets backed up automatically

The commands `workshop:setup`, `workshop:apply`, and `workshop:starter` change files
for you. Each one **first copies what it is about to overwrite** into
`.workshop-backups/<id>/`, then prints a line like:

```text
Backup saved: 1794230448093-63788737-df30-4265-9daf-ea52a3699bbf. Restore with npm run workshop:restore -- 1794230448093-63788737-df30-4265-9daf-ea52a3699bbf
```

That long **backup ID** is your undo ticket. **Copy it somewhere** if you think
you might want it. (`.workshop-backups/` and `.workshop-reports/` are
git-ignored, so they never end up in a commit.)

## Which situation are you in?

| What happened | Go to |
|---|---|
| I want to go back to the state before a workshop command | [Restore a backup](#restore-a-backup) |
| I want to wipe my four features back to the unfinished starter | [Reset the features to the starter](#reset-the-features-to-the-starter) |
| I want to undo Lab 1's templates | [Undo Lab 1](#undo-lab-1) |
| I am about to try something risky of my own | [Save a patch first](#save-a-patch-before-your-own-experiment) |
| Something is badly broken and I want to start over | [Fresh clone](#start-over-with-a-fresh-clone) |
| Two workers edited the same file | [Collision protocol](#collision-protocol) |
| I committed something I regret | [Undo a commit safely](#undo-a-commit-safely) |

## Restore a backup

**What.** Put your files back the way they were before a specific workshop command.

**Why.** It is a one-line undo that does not touch anything outside the
workshop's files.

```text
npm run workshop:restore -- <the exact backup ID>
```

**You should see.** A new `Backup saved:` line, then `Wrote:` lines for each file put
back. *Why a new backup?* Restore **backs up the current state first** (a "rescue"
backup), so even a restore can be undone. Example (after resetting to the
starter, then restoring):

```text
Backup saved: 1794230453742-986c6710-9877-4a4e-bdb3-10a00dec3d11. Restore with npm run workshop:restore -- 1794230453742-986c6710-9877-4a4e-bdb3-10a00dec3d11
Wrote: src/features/priority.mjs
Wrote: tests/features/priority.test.mjs
...
```

Run `npm test` afterward to confirm.

Two kinds of `Wrote:`-style lines can appear. `Wrote: <path>` means a file was put
back. `Restored absence: <path>` means the file **did not exist** when the backup
was taken, so the restore removed it (or confirmed it was already gone).

**Good to know.**

- Use the **exact** ID the command printed. A partial or wrong ID is rejected
  with `Use the exact backup ID printed by the workshop command.`
- It only touches a **fixed, known list** of workshop files, and refuses
  symbolic links. It cannot wander across your disk.
- It is **not a transaction**. If it is interrupted halfway (for example, a
  writer was still running), some files may be restored and some not. Keep the
  printed backup ID, stop all writers, look at the state, and run it again.
- Files that **did not exist** before the backed-up command are **removed** by the
  restore. That is correct: it returns you to the earlier state.

## Reset the features to the starter

**What.** Put the four feature files back to their unfinished 4-line starters,
and remove the four exercise test files, so you can redo a lab.

**Why.** Handy after a rehearsal, or if a lab went sideways and you want a clean
slate for the *features* only.

```text
npm run workshop:starter
```

**You should see.**

```text
Restoring four starter modules and removing ONLY the four named exercise test files; all prior contents are backed up.
Backup saved: <id>. Restore with npm run workshop:restore -- <id>
Wrote: src/features/priority.mjs
Restored absence: tests/features/priority.test.mjs
... (the same pair for search, summary, handoff)
```

Then `npm test` shows **14 passing** again (the original baseline).

**It does NOT touch** your `.github/` agents, skills, or instruction rules, your
notes in `.workshop-reports/`, or the app shell. That is deliberate: it cannot
delete things it does not own.

## Undo Lab 1

**What.** Lab 1's `workshop:setup` command copied templates into `.github/` and
printed a backup ID at the start.

**Why it is limited.** Restoring that ID returns the files the command touched
(only the reviewer template and the triage-policy skill files) to how they were.
It does **not** back up `.github/copilot-instructions.md`. **Edits you made by hand afterward** (for example, the two
rules you added to `copilot-instructions.md`) are **not** in that backup. If you
want those, save them yourself before restoring.

## Save a patch before your own experiment

**What.** Before something risky (for example, letting an agent loose on lots of
files), save a snapshot of your current uncommitted changes.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force .workshop-reports | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
git diff --binary --output=".workshop-reports\before-experiment-$stamp.patch"
```

macOS or Linux:

```bash
mkdir -p .workshop-reports
stamp=$(date +%Y%m%d-%H%M%S)
git diff --binary --output=".workshop-reports/before-experiment-$stamp.patch"
```

**Why the first line.** `git` will not create the folder for you, and fails with
`could not open ... for writing: No such file or directory` if it is missing.
(Lab 3 also creates this folder.) **Why the `$stamp` line.** It puts the date and
time in the file name, so saving a second patch later never overwrites the first.

**Why a patch.** A patch is a plain text record of *what changed*. If you hate the
result, you can see exactly what you had. If your working tree was clean, the
file is simply empty, which is fine.

> A patch captures changes to files git already tracks. New, never-added files
> are not in it. For those, copy the files themselves or commit first (below).

**Even safer:** make a **local commit** on your own branch before the experiment.
A commit is the strongest undo point and never leaves your machine.

## Start over with a fresh clone

**What.** Download a second copy next to your first one, and leave the first
alone.

**Why.** Cheaper and safer than trying to repair a confusing state. Your old
copy stays available so you can compare, or rescue a note from it.

```powershell
git clone -b adamga-workshop-app-and-hands-on-labs https://github.com/adamga/advancedghcp.git advancedghcp-workshop-fresh
Set-Location .\advancedghcp-workshop-fresh
npm test
```

(On macOS or Linux, the same commands work; use `cd` instead of `Set-Location`.
The `-b` option picks the workshop branch, because the repository's default
branch does not hold the workshop yet. After the workshop pull request is merged,
a plain `git clone <url>` works too.)

**You should see** 14 tests passing, and eight `untriaged` cards in the app.

## Collision protocol

A **collision** means two workers changed the same file, or one worker changed a
file it did not own (Lab 3 teaches how to prevent this). When you suspect one:

1. **Stop all writers.** No more edits from anyone.
2. **Preserve the evidence.** Save the diff with the same recipe as
   [Save a patch](#save-a-patch-before-your-own-experiment), using
   `collision-$stamp.patch` as the file name. Do **not** delete or overwrite anything yet.
3. **Name the owner.** Check the task board: who held the lease on that file?
4. **Assign one integrator** to reconcile. One person (or agent) merges the
   pieces. Do not have the workers "fix it themselves" in parallel; that is how
   it got worse.
5. **Re-run the gates** (`npm test`, the acceptance checks) after reconciling.
6. **Write down what happened** in your report: what collided, what you did, and
   what would have prevented it.

## Undo a commit safely

**What.** You already committed something you regret.

**Why `revert` and not `reset`.** `git revert` creates a **new** commit that
cancels the old one. History stays honest and nothing is destroyed. `reset
--hard` rewrites history and can erase work.

```text
git revert <the commit id>
```

If the commit was **pushed and shared**, `revert` is the only polite option. Never
force-push over other people's work.

## A note on worktrees

If you used a worktree (Lab 3, optional route), do **not** delete the folder or
force-delete the branch to "clean up" while it has uncommitted work. Commit or
patch first. A worktree is a normal folder plus a git branch; treat it with the
same care as any other working copy.

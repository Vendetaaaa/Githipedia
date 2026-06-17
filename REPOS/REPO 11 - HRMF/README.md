<div align="center">

![](https://capsule-render.vercel.app/api?type=blur&height=150&color=B91C1C&text=Git%20Hygiene%2C%20Reflog%20Fixing%20Mistakes&section=header&fontColor=FCA5A5&fontSize=24&fontAlignY=38&desc=The%20Undo%20Button%20For%20Git.&descAlignY=68)

[![Recovery](https://img.shields.io/badge/3_Safety_Nets-B91C1C?style=for-the-badge&labelColor=1a1a1a)](#the-three-safety-nets) [![No Data Lost](https://img.shields.io/badge/Nothing_Is_Ever_Truly_Gone-7F1D1D?style=for-the-badge&labelColor=1a1a1a)](#how-git-actually-stores-things)

</div>

---

## Table of Contents
[#table-of-contents](#table-of-contents)

- [What Is Git Hygiene?](#what-is-git-hygiene)
- [Why Should You Care?](#why-should-you-care)
- [How Git Actually Stores Things](#how-git-actually-stores-things)
- [The Three Safety Nets](#the-three-safety-nets)
  * [🔄 What is the Reflog?](#-what-is-the-reflog)
  * [🌱 What are Dangling Commits?](#-what-are-dangling-commits)
  * [🗑️ What is the Garbage Collector?](#️-what-is-the-garbage-collector)
- [Fixing Mistakes  A Field Guide](#fixing-mistakes--a-field-guide)
  * [😬 "I committed to the wrong branch"](#-i-committed-to-the-wrong-branch)
  * [✍️ "I need to change my last commit message"](#️-i-need-to-change-my-last-commit-message)
  * [📦 "I forgot to add a file to my last commit"](#-i-forgot-to-add-a-file-to-my-last-commit)
  * [⏪ "I want to undo my last commit but keep the changes"](#-i-want-to-undo-my-last-commit-but-keep-the-changes)
  * [💣 "I want to undo my last commit and discard the changes"](#-i-want-to-undo-my-last-commit-and-discard-the-changes)
  * [😱 "I ran a hard reset and lost commits"](#-i-ran-a-hard-reset-and-lost-commits)
  * [🌪️ "I force-pushed and broke a shared branch"](#️-i-force-pushed-and-broke-a-shared-branch)
  * [🗑️ "I deleted a branch by mistake"](#️-i-deleted-a-branch-by-mistake)
  * [🔥 "I committed a secret or sensitive file"](#-i-committed-a-secret-or-sensitive-file)
  * [🌀 "My merge/rebase is a disaster"](#-my-mergerebase-is-a-disaster)
- [`reset` vs `revert` vs `checkout` vs `restore`](#reset-vs-revert-vs-checkout-vs-restore)
- [Good Hygiene Habits](#good-hygiene-habits)
- [Useful Aliases for Your `.gitconfig`](#useful-aliases-for-your-gitconfig)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Useful Links](#useful-links)

---

## What Is Git Hygiene?
[#what-is-git-hygiene](#what-is-git-hygiene)

Git hygiene is the set of habits that keep a repository's history clean, readable, and recoverable: writing meaningful commit messages, committing in small logical chunks, not rewriting history other people depend on, and knowing how to clean up after yourself when something goes wrong.

It's not about perfection. It's about making sure that six months from now  or six minutes from now, after a panicked mistake  the history actually tells you what happened and gives you a way back.

> A repo with good hygiene is one where `git log` reads like a story. A repo without it reads like a crime scene.

---

## Why Should You Care?
[#why-should-you-care](#why-should-you-care)

Most people learn Git hygiene the hard way: by force-pushing over three days of a teammate's work, or running `git reset --hard` one commit too far and watching their afternoon disappear.

```
The good news: Git almost never actually deletes anything immediately.
Commits, branches, even "discarded" changes usually stick around in
the background for weeks before they're truly gone.

The bad news: if you don't know that, a scary error message or a
missing branch feels like a catastrophe  and panic is how a small
mistake turns into actual data loss.

```

Understanding how Git stores its history  and the recovery tools built into it  turns "I just lost a week of work" into "give me thirty seconds."

---

## How Git Actually Stores Things
[#how-git-actually-stores-things](#how-git-actually-stores-things)

Before any of the recovery tricks make sense, it helps to know what a "commit" really is under the hood. Branches are not containers that hold commits  they're just movable labels.

```
A commit is an object, identified by a SHA hash, stored in .git/objects
A branch is just a pointer  a named label  that points at one commit
HEAD is a pointer that points at "whatever branch you currently have checked out"

main  →  c3a91f2  →  8b7e0aa  →  4f1d220   (the commit chain main points to)
              ↑
            HEAD

```

When you "delete a branch," you're only deleting the label. The commits it pointed to don't vanish  they just become harder to find because nothing points at them anymore. That's the entire foundation of Git recovery: **the data usually outlives the pointer.**

---

## The Three Safety Nets
[#the-three-safety-nets](#the-three-safety-nets)

### 🔄 What is the Reflog?
[#-what-is-the-reflog](#-what-is-the-reflog)

The reflog ("reference log") is a local, private log of everywhere `HEAD` and your branches have pointed over the last 90 days or so. It records every commit, checkout, rebase, reset, and merge  even ones that are no longer reachable from any branch.

```
git reflog              →  show HEAD's history
git reflog show main    →  show a specific branch's history

```

A typical entry looks like this:

```
c3a91f2 HEAD@{0}: commit: add login validation
8b7e0aa HEAD@{1}: reset: moving to HEAD~1
4f1d220 HEAD@{2}: commit: fix typo in README
9e02ab1 HEAD@{3}: checkout: moving from feature/login to main

```

Each `HEAD@{n}` is a snapshot of where `HEAD` was at that point in time. If you ever reset, rebase, or delete a branch and the commits seem to vanish, the reflog almost always still has them  you just need to find the right entry and point a branch back at it.

> The reflog is **local only**. It is never pushed, never cloned, and lives entirely in your `.git` directory. It cannot save you from someone *else's* mistake on a shared branch  only your own, on your own machine.

### 🌱 What are Dangling Commits?
[#-what-are-dangling-commits](#-what-are-dangling-commits)

A dangling commit is a commit object that still physically exists in `.git/objects` but isn't reachable from any branch, tag, or other ref. This happens constantly  every amend, every rebase, every hard reset leaves the *old* commits behind as dangling objects.

```
git fsck --lost-found   →  list dangling commits and blobs

```

You can inspect any dangling commit the same way you'd inspect a normal one:

```
git show <sha>                    →  view the commit's content
git branch recovered-work <sha>   →  turn it back into a real branch

```

Dangling commits are the reason a "deleted" commit so rarely means a *gone* commit.

### 🗑️ What is the Garbage Collector?
[#️-what-is-the-garbage-collector](#️-what-is-the-garbage-collector)

Git's garbage collector (`git gc`) is the process that eventually cleans up dangling objects to keep the repository from growing forever. It runs automatically every so often, but it respects an expiry window first.

```
Reflog entries        →  expire after ~90 days by default (gc.reflogExpire)
Unreachable objects   →  expire after ~30 days by default (gc.pruneExpire)

```

This is the actual deadline on Git recovery: as long as `git gc` hasn't run *and* the relevant expiry window hasn't passed, the data is still sitting in `.git/objects` waiting to be found. In practice, for the vast majority of "I think I lost my work" situations, you have weeks, not minutes.

---

## Fixing Mistakes  A Field Guide
[#fixing-mistakes--a-field-guide](#fixing-mistakes--a-field-guide)

Real scenarios, in the order panic usually escalates.

### 😬 "I committed to the wrong branch"
[#-i-committed-to-the-wrong-branch](#-i-committed-to-the-wrong-branch)

```
git log -1                          # note the commit's SHA
git reset HEAD~1                    # undo the commit on this branch, keep the changes
git switch correct-branch
git add .
git commit -m "your message"

```

If you'd already moved on and the wrong commit is buried, `git cherry-pick <sha>` onto the correct branch works just as well, followed by removing it from the wrong one.

### ✍️ "I need to change my last commit message"
[#️-i-need-to-change-my-last-commit-message](#️-i-need-to-change-my-last-commit-message)

```
git commit --amend -m "the corrected message"

```

Only do this if the commit hasn't been pushed yet  amending rewrites the commit's SHA, which causes problems for anyone who already pulled it.

### 📦 "I forgot to add a file to my last commit"
[#-i-forgot-to-add-a-file-to-my-last-commit](#-i-forgot-to-add-a-file-to-my-last-commit)

```
git add forgotten-file.js
git commit --amend --no-edit

```

`--no-edit` keeps the original commit message untouched while folding the new file in.

### ⏪ "I want to undo my last commit but keep the changes"
[#-i-want-to-undo-my-last-commit-but-keep-the-changes](#-i-want-to-undo-my-last-commit-but-keep-the-changes)

```
git reset --soft HEAD~1    # keeps changes staged, ready to re-commit
git reset HEAD~1           # keeps changes unstaged, in your working directory

```

This is the move when the commit itself was wrong (bad message, wrong split, missing file) but the actual code is fine.

### 💣 "I want to undo my last commit and discard the changes"
[#-i-want-to-undo-my-last-commit-and-discard-the-changes](#-i-want-to-undo-my-last-commit-and-discard-the-changes)

```
git reset --hard HEAD~1

```
> This deletes uncommitted changes to tracked files permanently  they are not staged anywhere and the reflog cannot bring back data that was never committed. Double-check `git status` and `git diff` before running this.

### 😱 "I ran a hard reset and lost commits"
[#-i-ran-a-hard-reset-and-lost-commits](#-i-ran-a-hard-reset-and-lost-commits)

This is what the reflog exists for.

```
git reflog                          # find the entry just before the reset
git reset --hard HEAD@{1}           # or whichever index has your lost commit

```

If you're not sure which entry is right, `git show HEAD@{1}` lets you preview a snapshot before committing to resetting onto it.

### 🌪️ "I force-pushed and broke a shared branch"
[#️-i-force-pushed-and-broke-a-shared-branch](#️-i-force-pushed-and-broke-a-shared-branch)

```
Step 1 → Ask a teammate who pulled before the force-push for their local SHA
Step 2 → Or check the reflog on your own machine for the pre-push state
Step 3 → git push --force-with-lease origin branch-name  (restoring the good state)
Step 4 → Tell everyone on the branch to run: git fetch && git reset --hard origin/branch-name

```
> `--force-with-lease` instead of `--force` is the actual hygiene habit here  it refuses to push if someone else has added commits you haven't seen, instead of blindly overwriting them.

### 🗑️ "I deleted a branch by mistake"
[#️-i-deleted-a-branch-by-mistake](#️-i-deleted-a-branch-by-mistake)

```
git reflog                                    # find the last commit the branch pointed to
git branch recovered-branch-name <sha>        # recreate the branch at that commit

```

Deleted branches almost always leave a trail in the reflog under entries like `branch: Created from...` or the last `commit:` entry before the deletion. If the branch was merged before deletion, `git log --all` will usually still show its commits too.

### 🔥 "I committed a secret or sensitive file"
[#-i-committed-a-secret-or-sensitive-file](#-i-committed-a-secret-or-sensitive-file)

```
Not pushed yet  →  git reset --soft HEAD~1, remove the file, recommit
Already pushed  →  rotate/revoke the secret FIRST, then clean history

```
> Removing a secret from history does not undo the exposure if it's already been pushed  assume it's compromised and rotate it immediately. History rewriting only prevents *future* exposure, and tools like `git filter-repo` or BFG Repo-Cleaner are built for this rather than plain `rebase`.

### 🌀 "My merge/rebase is a disaster"
[#-my-mergerebase-is-a-disaster](#-my-mergerebase-is-a-disaster)

```
git merge --abort      # bail out of a merge in progress, back to pre-merge state
git rebase --abort     # bail out of a rebase in progress, back to pre-rebase state

```

Both commands only work *while the operation is still in progress* (i.e. you're mid-conflict). If you already finished and committed the result and it's wrong, the reflog entry from right before the merge/rebase started is your way back.

---

## `reset` vs `revert` vs `checkout` vs `restore`
[#reset-vs-revert-vs-checkout-vs-restore](#reset-vs-revert-vs-checkout-vs-restore)

These four commands get confused constantly because they all sound like "undo." They do very different things.

| Command | Rewrites History? | Safe on Shared Branches? | What It Actually Does |
| --- | --- | --- | --- |
| `git reset` | ✅ Yes | ❌ No | Moves the branch pointer backward, optionally touching staged/working files |
| `git revert` | ❌ No (adds a new commit) | ✅ Yes | Creates a *new* commit that undoes a previous one's changes |
| `git checkout <commit>` | ❌ No | ✅ Yes | Moves `HEAD` to look at a commit/branch/file, without changing the branch's history |
| `git restore <file>` | ❌ No | ✅ Yes | Restores a working-directory file from the index or a specific commit |

> The rule of thumb: if a branch is shared with anyone else, reach for `revert`, not `reset`. Reverting adds to history instead of rewriting it, so nobody else's clone gets out of sync.

---

## Good Hygiene Habits
[#good-hygiene-habits](#good-hygiene-habits)

```
Commit small, commit often    →  one logical change per commit, not "end of day" dumps
Write the "why," not the "what"  →  the diff already shows what changed
Never force-push to main/shared branches without --force-with-lease
Don't rewrite history that's already been pushed and pulled by others
Run git status before any reset --hard  know what you're about to discard
Tag before risky rewrites      →  git tag pre-rebase-backup gives you a free anchor
Keep .gitignore current        →  fewer accidental commits of secrets, builds, logs

```

The single highest-leverage habit on this list is the tag-before-rewrite trick: `git tag backup-before-rebase` takes one second and gives you a permanent, easy-to-find pointer back to exactly where you were  no digging through the reflog required.

---

## Useful Aliases for Your `.gitconfig`
[#useful-aliases-for-your-gitconfig](#useful-aliases-for-your-gitconfig)

A few aliases that make the safety nets faster to reach for in the moment you actually need them:

```
[alias]
    last      = log -1 HEAD
    undo      = reset --soft HEAD~1
    unstage   = restore --staged .
    graph     = log --oneline --graph --all --decorate
    lost      = reflog --date=relative

```

`git lost` in particular is worth memorizing  it's just the reflog with human-readable relative timestamps ("3 hours ago" instead of a raw date), which makes scanning for the right moment to roll back to much faster.

---

## Frequently Asked Questions
[#frequently-asked-questions](#frequently-asked-questions)

**Is anything in Git ever actually, permanently gone?**

Eventually, yes  but rarely quickly. Once `git gc` runs and an object is past its expiry window (commits you never committed in the first place are the one true exception; those were never stored at all), it's gone for good. For almost every real-world "oh no" moment, though, you're well inside that window.

**Does the reflog get pushed to GitHub/GitLab with the rest of my repo?**

No. The reflog is purely local, stored in `.git/logs`, and never transmitted anywhere. This means it can only rescue mistakes made on your own machine  it has no knowledge of, and no power over, what happens on the remote or in anyone else's clone.

**What's the difference between `git reset --hard` and `git clean`?**

`git reset --hard` affects tracked files  it can discard changes to files Git already knows about. `git clean` affects untracked files  new files you've never `git add`ed. Running `git clean -fd` deletes untracked files and directories with no recovery path at all, since Git never stored them as objects in the first place.

**I deleted a branch on GitHub through the website. Can I get it back?**

If it was recently deleted and your repository has an open pull request that was made from it, GitHub keeps a "restore branch" button on that closed/merged PR for a while. Otherwise, if anyone (including you) has a local clone with that branch, `git push origin local-branch-name` recreates it on the remote.

**Why does my team keep telling me to use `--force-with-lease` instead of `--force`?**

Because `--force` overwrites the remote branch unconditionally  even if someone pushed new commits to it five seconds before you. `--force-with-lease` checks that the remote hasn't changed since you last fetched, and refuses the push if it has. It's the difference between "overwrite no matter what" and "overwrite only if nothing's changed since I last looked."

---

## Useful Links
[#useful-links](#useful-links)

| Resource | What It Is |
| --- | --- |
| [Pro Git  Git Internals](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain) | The free official book's chapter on how Git actually stores data |
| [git-reflog documentation](https://git-scm.com/docs/git-reflog) | Official reference for every reflog subcommand and flag |
| [git-reset documentation](https://git-scm.com/docs/git-reset) | Official reference, including the soft/mixed/hard breakdown |
| [Oh Shit, Git!?!](https://ohshitgit.com/) | A blunt, practical cheat sheet for exactly this kind of situation |
| [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) | Faster alternative to `filter-branch` for purging secrets from history |
| [git-filter-repo](https://github.com/newren/git-filter-repo) | The modern, recommended tool for rewriting repo history |
| [GitHub Docs  Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | Official steps for purging committed secrets |

---

<div align="center">

![](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=Commit%20bravely.%20The%20reflog%20has%20your%20back.&fontSize=28&fontColor=FCA5A5&fontAlignY=65)

</div>

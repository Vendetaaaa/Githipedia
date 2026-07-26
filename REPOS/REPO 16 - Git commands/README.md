<div align="center">

[![](https://capsule-render.vercel.app/api?type=blur&height=250&color=B91C1C&text=Git%20Commands&section=header&fontColor=FCA5A5&fontAlign=34&desc=The%20Open%20Encyclopedia%20For%20Git.&descAlign=55)](https://capsule-render.vercel.app/api?type=blur&height=250&color=B91C1C&text=Git%20Commands&section=header&fontColor=FCA5A5&fontAlign=34&desc=The%20Open%20Encyclopedia%20For%20Git.&descAlign=55)

*Every Git command you'll actually use, where it came from, and why it works the way it does.*

</div>

---

## Table of Contents

- [What Is Git?](#what-is-git)
- [A Short History](#a-short-history)
- [Core Concepts You Need First](#core-concepts-you-need-first)
  * [What is a Repository?](#-what-is-a-repository)
  * [What is the Staging Area?](#-what-is-the-staging-area)
  * [What is a Commit?](#-what-is-a-commit)
  * [What is HEAD?](#-what-is-head)
- [Installing Git](#installing-git)
- [The Commands](#the-commands)
  * [Setup & Configuration](#setup--configuration)
  * [Starting a Repository](#starting-a-repository)
  * [Basic Snapshotting](#basic-snapshotting)
  * [Branching & Switching](#branching--switching)
  * [Merging & Rebasing](#merging--rebasing)
  * [Working With Remotes](#working-with-remotes)
  * [Inspecting History](#inspecting-history)
  * [Undoing Things](#undoing-things)
  * [Stashing](#stashing)
  * [Tags](#tags)
  * [Advanced & Situational](#advanced--situational)
- [Worked Examples](#worked-examples)
  * [Fixing your last commit message](#fixing-your-last-commit-message)
  * [Resolving a merge conflict](#resolving-a-merge-conflict)
  * [Squashing messy commits before a PR](#squashing-messy-commits-before-a-pr)
  * [Saving unfinished work with stash](#saving-unfinished-work-with-stash)
  * [Finding which commit broke something](#finding-which-commit-broke-something)
- [Git vs GitHub](#git-vs-github)
- [Support This Project](#support-this-project)
- [Resources & Further Reading](#resources--further-reading)
- [License](#license)

---

## What Is Git?

Git is a **distributed version control system**. It tracks changes to files over time, so you can see what changed, who changed it, and roll back to any earlier point without losing anything.

"Distributed" is the key word. Unlike older systems where one central server held the only full history, every Git clone carries the complete project history with it. Your laptop has just as much of the real repository as the server does.

> 💬 *Git tracks content, not files. Rename a file and change three lines inside it, and Git will usually still recognize it as the same file that moved.*

---

## A Short History

Git exists because of a licensing dispute. Up until 2005, the Linux kernel project used a proprietary tool called BitKeeper to manage its source code, donated for free use by its vendor. When that arrangement fell apart, Linus Torvalds needed a replacement fast, and nothing on the market moved at the speed a project with thousands of contributors required.

So he built one himself.

```
April 2005    → Torvalds starts writing Git
Days later    → Git manages its own source code
June 2005     → The Linux kernel 2.6.12 release is the first shipped with Git
2005 onward   → Junio Hamano takes over as lead maintainer, still holds the role today

```

The name is famously self-deprecating. Torvalds has said he names things after himself when he's feeling egotistical (Linux), and "git" is British slang for an unpleasant person. He also gave it a looser backronym: "Global Information Tracker."

GitHub, GitLab, and Bitbucket came later, as hosted platforms built around Git. Git itself has no company behind it and needs no internet connection to work. It ran fine in 2005 and it runs exactly the same way today.

---

## Core Concepts You Need First

A handful of ideas show up in nearly every command below. Get these straight first and the rest stops feeling like memorization.

### 🗂 What is a Repository?

A repository, or "repo," is a project folder plus its entire recorded history. That history lives in a hidden `.git` folder sitting right next to your files.

```
my-project/
├── .git/          ← the actual repository: history, config, everything
├── index.html
├── style.css
└── README.md

```

Delete `.git` and the folder stops being a repository. Your files stay, but every commit, branch, and past version is gone.

### 📥 What is the Staging Area?

Git splits saving a change into two steps instead of one. You **stage** the changes you want to include, then you **commit** the staged snapshot. This middle step is what lets you build one clean commit out of five files you edited, while leaving a sixth file's changes for later.

```
Working Directory  →  git add  →  Staging Area  →  git commit  →  Repository History

```

### 📸 What is a Commit?

A commit is a snapshot of your staged files at one point in time, plus a message explaining why. Each commit points back to the commit before it, which is how Git builds a full history out of a chain of snapshots.

Every commit gets a unique hash, something like `a3f9c2e`, generated from its content. Change one character in a file and the hash of every commit after it changes too.

### 🧭 What is HEAD?

HEAD is a pointer to whatever commit you currently have checked out. Almost always, that means it's pointing at the tip of whatever branch you're on. Move between branches or commits, and HEAD moves with you. Several commands below (`reset`, `checkout`) exist specifically to move HEAD around on purpose.

---

## Installing Git

```
# Windows: download the installer
https://git-scm.com/download/win

# macOS: via Homebrew
brew install git

# Debian / Ubuntu
sudo apt update && sudo apt install git

# Fedora
sudo dnf install git

# Verify it worked
git --version
```

First thing to do on any new machine, before anything else:

```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Every commit you make gets stamped with these two values. Get them wrong and every commit you've already pushed keeps the wrong author attached to it.

---

## The Commands

### Setup & Configuration

| Command | What It Does |
| --- | --- |
| `git config --global user.name "Name"` | Sets the name attached to your commits |
| `git config --global user.email "mail"` | Sets the email attached to your commits |
| `git config --global core.editor "code --wait"` | Sets which editor opens for commit messages |
| `git config --list` | Shows every active config value and where it came from |
| `git config --global alias.st status` | Creates a shortcut, `git st` now runs `git status` |

> 💡 **Tip:** Config set with `--global` applies to every repo on your machine. Drop the flag while inside a repo to override it for that project only, useful for a work email on a work repo.

---

### Starting a Repository

| Command | What It Does |
| --- | --- |
| `git init` | Turns the current folder into a new, empty Git repository |
| `git clone <url>` | Downloads a full copy of an existing repository, history included |
| `git clone <url> <folder>` | Same, but places it in a folder with a custom name |
| `git clone --depth 1 <url>` | Downloads only the latest commit, skipping the full history |

```
git init
# or
git clone https://github.com/user/repo.git
cd repo
```

> ⚠️ `--depth 1` clones are much faster on huge repos, but you lose access to old history until you run `git fetch --unshallow`.

---

### Basic Snapshotting

| Command | What It Does |
| --- | --- |
| `git status` | Shows what's changed, staged, and untracked |
| `git add <file>` | Stages a specific file |
| `git add .` | Stages every changed file in the current folder and below |
| `git add -p` | Stages changes interactively, chunk by chunk |
| `git commit -m "message"` | Commits everything currently staged |
| `git commit -am "message"` | Stages every tracked file's changes and commits in one step |
| `git diff` | Shows unstaged changes, line by line |
| `git diff --staged` | Shows what's staged and about to be committed |

```
git status
git add index.html style.css
git diff --staged
git commit -m "Add responsive navbar"
```

> 💡 **`git add -p` is worth learning early.** It walks through every changed block in a file and asks yes or no, so you can split a messy afternoon of edits into several clean, focused commits.

---

### Branching & Switching

| Command | What It Does |
| --- | --- |
| `git branch` | Lists local branches, marking the current one |
| `git branch <name>` | Creates a new branch, doesn't switch to it |
| `git branch -d <name>` | Deletes a branch, refuses if it has unmerged work |
| `git branch -D <name>` | Deletes a branch regardless, even if unmerged |
| `git switch <name>` | Switches to an existing branch |
| `git switch -c <name>` | Creates a branch and switches to it in one step |
| `git checkout -b <name>` | Older syntax for the same thing as `switch -c` |

```
git switch -c feature/dark-mode
# work happens here...
git add .
git commit -m "Add dark mode toggle"
git switch main
```

> 🌿 `switch` and `restore` are newer, split off from the old do-everything `checkout` command specifically to make each one's purpose obvious. Both syntaxes work, `switch` is just easier to reason about.

---

### Merging & Rebasing

| Command | What It Does |
| --- | --- |
| `git merge <branch>` | Combines another branch's history into your current one |
| `git rebase <branch>` | Replays your commits on top of another branch's tip |
| `git rebase -i HEAD~3` | Opens an interactive rebase for your last 3 commits |
| `git merge --abort` | Backs out of a merge that hit conflicts |
| `git rebase --abort` | Backs out of a rebase that hit conflicts |

```
git switch main
git pull
git switch feature/dark-mode
git rebase main
```

```
Merge:    keeps both histories, adds a merge commit joining them
Rebase:   rewrites your commits as if they started from main's latest tip

```

> ⚠️ Never rebase commits that are already pushed and that someone else might have pulled. Rebasing rewrites commit hashes, and anyone with the old versions ends up with a diverged history that's painful to fix.

---

### Working With Remotes

| Command | What It Does |
| --- | --- |
| `git remote -v` | Lists connected remotes and their URLs |
| `git remote add origin <url>` | Connects a local repo to a remote one, named `origin` |
| `git fetch` | Downloads new commits from a remote, doesn't merge them |
| `git pull` | Fetches and merges in one step |
| `git pull --rebase` | Fetches and rebases your local commits on top instead of merging |
| `git push` | Uploads your local commits to the remote |
| `git push -u origin <branch>` | Pushes and links your local branch to the remote one, so future `git push` needs no arguments |
| `git push --force-with-lease` | Force pushes, but refuses if someone else pushed first |

```
git remote add origin https://github.com/you/project.git
git push -u origin main
```

> ⚠️ Avoid plain `git push --force`. It overwrites the remote branch no matter what, even work you haven't seen yet. `--force-with-lease` checks first and refuses if it would delete someone else's commits.

---

### Inspecting History

| Command | What It Does |
| --- | --- |
| `git log` | Shows commit history, newest first |
| `git log --oneline` | Same, one line per commit |
| `git log --graph --all` | Shows history as a branching graph across every branch |
| `git show <hash>` | Shows exactly what a specific commit changed |
| `git blame <file>` | Shows who last touched each line, and in which commit |
| `git diff <hash1> <hash2>` | Shows what changed between two commits |

```
git log --oneline --graph --all
```

```
* a3f9c2e (HEAD -> main) Add dark mode toggle
* 1b8e4d1 Fix navbar spacing on mobile
| * 7c2a9f0 (feature/search) Add search bar
|/
* 0e5b3a2 Initial commit

```

> 💡 `git log --oneline --graph --all` is worth aliasing. It's the single fastest way to actually see what's going on across every branch at once.

---

### Undoing Things

| Command | What It Does |
| --- | --- |
| `git restore <file>` | Discards unstaged changes to a file |
| `git restore --staged <file>` | Unstages a file, keeps its changes in your working directory |
| `git commit --amend` | Rewrites your most recent commit instead of adding a new one |
| `git reset --soft HEAD~1` | Undoes the last commit, keeps changes staged |
| `git reset --mixed HEAD~1` | Undoes the last commit, keeps changes but unstages them |
| `git reset --hard HEAD~1` | Undoes the last commit and deletes the changes entirely |
| `git revert <hash>` | Creates a new commit that undoes a specific old commit |

```
Working Dir  ←──── reset --mixed (default)
Staged       ←──── reset --soft
History      ←──── reset --hard deletes it here too

```

> ⚠️ `reset --hard` deletes uncommitted work with no confirmation and no undo through normal means. `revert` is the safer choice on anything already pushed and shared, since it adds history instead of erasing it.

---

### Stashing

| Command | What It Does |
| --- | --- |
| `git stash` | Shelves your uncommitted changes, restores a clean working directory |
| `git stash list` | Shows every stashed set of changes |
| `git stash pop` | Reapplies the most recent stash and removes it from the list |
| `git stash apply` | Reapplies the most recent stash but keeps it in the list |
| `git stash drop` | Deletes a stash without applying it |

```
git stash
git switch main
git pull
git switch feature/dark-mode
git stash pop
```

---

### Tags

| Command | What It Does |
| --- | --- |
| `git tag` | Lists all tags |
| `git tag v1.0.0` | Creates a lightweight tag on the current commit |
| `git tag -a v1.0.0 -m "message"` | Creates an annotated tag, with a message and author |
| `git push origin v1.0.0` | Pushes a single tag to the remote |
| `git push --tags` | Pushes every local tag to the remote |

> 💡 Use annotated tags (`-a`) for anything meant to mark a real release. They store the tagger, date, and message, lightweight tags are just a label on a commit with nothing else attached.

---

### Advanced & Situational

| Command | What It Does |
| --- | --- |
| `git cherry-pick <hash>` | Applies one specific commit from another branch onto yours |
| `git bisect start` | Begins a binary search through history to find which commit introduced a bug |
| `git reflog` | Shows a log of everywhere HEAD has pointed, including "deleted" commits |
| `git submodule add <url>` | Embeds another repository inside yours, tracked at a fixed commit |
| `git worktree add ../path <branch>` | Checks out a branch into a separate folder without a second clone |
| `git clean -fd` | Deletes untracked files and folders, permanently |

> 🎯 **`git reflog` is a genuine safety net.** Even after `reset --hard` or a deleted branch, the commit usually still exists internally for a while. Reflog is often the fastest way back to it.

---

## Worked Examples

### Fixing your last commit message

Typo in the message, and you haven't pushed yet.

```
git commit --amend -m "Fix navbar spacing on mobile"
```

Forgot a file entirely.

```
git add forgotten-file.js
git commit --amend --no-edit
```

> ⚠️ Only amend commits that haven't been pushed. Amending a pushed commit changes its hash, and anyone who already pulled it now has a version that no longer matches yours.

### Resolving a merge conflict

```
git switch main
git pull
git switch feature/dark-mode
git merge main
```

Git stops and marks the conflicting sections directly in the file:

```
<<<<<<< HEAD
background-color: #1a1a1a;
=======
background-color: #121212;
>>>>>>> main
```

Pick the version you want, or write a new one that combines both, then delete the `<<<<<<<`, `=======`, and `>>>>>>>` markers by hand. Once every conflict in the file is resolved:

```
git add style.css
git commit
```

Git already knows this is a merge commit and pre-fills the message. You can accept it as is.

### Squashing messy commits before a PR

Five commits like "wip", "fix typo", "actually fix it" don't need to survive into the project's permanent history.

```
git rebase -i HEAD~5
```

Your editor opens with something like this:

```
pick a1b2c3d Add search bar
pick d4e5f6a wip
pick b7c8d9e fix typo
pick c1a2b3d actually fix it
pick e4f5a6b Add tests
```

Change every line except the first from `pick` to `squash` (or `s`), save, and Git will fold them into the first commit and prompt you for a combined commit message.

### Saving unfinished work with stash

Mid-feature, and an urgent bug needs a fix on `main` right now.

```
git stash push -m "half-done dark mode toggle"
git switch main
# fix the bug, commit, push
git switch feature/dark-mode
git stash pop
```

Everything comes back exactly where you left it.

### Finding which commit broke something

Something that worked a month ago is broken now, and forty commits happened in between.

```
git bisect start
git bisect bad                # current commit is broken
git bisect good v1.2.0        # this old tag was known to work
```

Git checks out a commit halfway between the two. Test it, then tell Git what you found.

```
git bisect good   # or
git bisect bad
```

Repeat. Git keeps narrowing the range in half until it lands on the exact commit that introduced the bug.

```
git bisect reset  # when you're done, returns you to where you started
```

---

## Git vs GitHub

These get used interchangeably in conversation, but they're not the same thing.

| | Git | GitHub |
| --- | --- | --- |
| **What it is** | A version control tool | A company that hosts Git repositories |
| **Runs where** | Locally, on your machine | On GitHub's servers |
| **Needs internet?** | No | Yes, to push, pull, or browse online |
| **Created by** | Linus Torvalds, 2005 | Tom Preston-Werner, Chris Wanstrath, PJ Hyett, Scott Chacon, 2008 |
| **Alternatives** | None really, Git is the standard | GitLab, Bitbucket, Codeberg, self-hosted Gitea |

You can use Git without ever touching GitHub. Plenty of teams run their own Git servers, or just push between each other's machines directly. GitHub adds the social and collaborative layer on top, pull requests, issues, actions, and everything else in this wiki's other guides.

---

## Support This Project

If this guide saved you a trip to Stack Overflow, or finally made rebasing make sense, a star helps other people find it too.

Found something outdated, unclear, or just plain wrong? Open an issue. Contributions are welcome, especially real-world examples from commands that didn't make the list yet.

---

## Resources & Further Reading

| Resource | What It Gets You |
| --- | --- |
| [Pro Git (free book)](https://git-scm.com/book/en/v2) | The complete, official reference, written by Scott Chacon and Ben Straub |
| [Git Documentation](https://git-scm.com/doc) | Official manual pages for every command |
| [Learn Git Branching](https://learngitbranching.js.org/) | Visual, interactive way to actually understand branching and rebasing |
| [Oh Shit, Git!?!](https://ohshitgit.com/) | Plain-language fixes for the most common ways people get stuck |
| [Git Cheat Sheet (GitHub)](https://education.github.com/git-cheat-sheet-education.pdf) | A printable one-page reference |
| [Explain Git With D3](https://onlywei.github.io/explain-git-with-d3/) | Animated visualizations of what each command actually does |
| [Conventional Commits](https://www.conventionalcommits.org/) | A standard format for writing useful commit messages |

---

## License

MIT License. Fork it, adapt it, translate it, share it freely.

<div align="center">

[![](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=More%20guides%20coming%20soon.&fontSize=28&fontColor=FCA5A5&animation=fadeIn&fontAlignY=65)](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=More%20guides%20coming%20soon.&fontSize=28&fontColor=FCA5A5&animation=fadeIn&fontAlignY=65)

</div>

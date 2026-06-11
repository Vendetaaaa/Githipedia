<div align="center">
  
<img src="https://capsule-render.vercel.app/api?type=blur&height=250&color=B91C1C&text=GitHub%20CLI&section=header&fontColor=FCA5A5&fontAlignY=34&desc=Everything%20you%20need%20to%20know%20about%20gh%20%E2%80%94%20the%20terminal%20that%20talks%20to%20GitHub.&descAlignY=55&descSize=18" width="100%" />

</div>

---

## Table of Contents

- [The Problem With Using GitHub in a Browser](#the-problem-with-using-github-in-a-browser)
- [Core Concepts You Need First](#core-concepts-you-need-first)
  * [What is a CLI?](#-what-is-a-cli)
  * [What is gh?](#-what-is-gh)
  * [How gh Differs From git](#-how-gh-differs-from-git)
  * [What is Authentication?](#-what-is-authentication)
- [Installation](#installation)
  * [Windows](#-windows)
  * [macOS](#-macos)
  * [Linux](#-linux)
- [Authentication - Connecting gh to Your Account](#authentication--connecting-gh-to-your-account)
- [The Command Structure](#the-command-structure)
- [The Commands](#the-commands)
  * [Quick Overview Table](#quick-overview-table)
  * [📁 gh repo - Repository Management](#-gh-repo--repository-management)
  * [🔀 gh pr - Pull Requests](#-gh-pr--pull-requests)
  * [🐛 gh issue - Issues](#-gh-issue--issues)
  * [⚙️ gh workflow & gh run - GitHub Actions](#️-gh-workflow--gh-run--github-actions)
  * [🔔 gh notify - Notifications](#-gh-notify--notifications)
  * [🔑 gh secret - Secrets Management](#-gh-secret--secrets-management)
  * [🌐 gh gist - Gists](#-gh-gist--gists)
  * [🔍 gh search - Search GitHub](#-gh-search--search-github)
  * [🔗 gh alias - Custom Shortcuts](#-gh-alias--custom-shortcuts)
  * [🧩 gh extension - Extending gh](#-gh-extension--extending-gh)
- [Combining gh With Other Tools](#combining-gh-with-other-tools)
- [Real Workflows You Can Steal](#real-workflows-you-can-steal)
- [The Full Command Reference](#the-full-command-reference)
- [Resources & Further Reading](#resources--further-reading)
- [License](#license)

---

## The Problem With Using GitHub in a Browser

Most developers use GitHub like this:

```
Write code in terminal
      ↓
Alt-Tab to browser
      ↓
Click through 4 pages to open a PR
      ↓
Alt-Tab back to terminal
      ↓
Make a change
      ↓
Repeat 12 times
```

Every context switch costs you focus. Every click through the UI is time you're not shipping.

Here's the uncomfortable part:
> *Everything you do on GitHub's website - creating repos, opening PRs, managing issues, triggering workflows - can be done in one line from your terminal. Most developers just don't know how.*

The GitHub CLI (`gh`) has been the official solution since 2020. It's maintained by GitHub, it's free, and it works on every platform. This guide covers everything it can do - from the basics through the workflows that will actually change how you work.

---

## Core Concepts You Need First

Before jumping into commands, four concepts will make everything else click immediately.

### 💻 What is a CLI?

A **CLI** (Command Line Interface) is a program you control entirely by typing commands into a terminal, rather than clicking through a graphical interface. Instead of navigating menus, you issue instructions directly.

```
GUI:  Find the repo button → click New → fill in the form → click Create
CLI:  gh repo create my-project --public --clone
```

Both do exactly the same thing. The CLI version takes about 3 seconds once it's in your muscle memory.

### 🐙 What is gh?

`gh` is GitHub's **official** command-line tool. It's not a third-party script someone put on npm - it's built and maintained by GitHub itself, released in 2020 after years of community demand.

It sits on top of GitHub's REST and GraphQL APIs and translates them into human-readable commands. Think of it as a remote control for your GitHub account that lives in your terminal.

```
gh is to GitHub
what git is to your local repo
```

The key distinction: `git` manages your code history. `gh` manages everything that happens *around* that code on GitHub - pull requests, issues, releases, Actions, notifications, and more.

### 🔀 How gh Differs From git

This trips up almost everyone when they first encounter `gh`. They sound similar and live in the same terminal, but they do completely different things.

<div align="center">
  
```
┌─────────────────────────────────────────────────────────────┐
│  git                          │  gh                         │
│  ─────────────────────────    │  ──────────────────────     │
│  Manages your code history    │  Manages GitHub features    │
│  Works offline                │  Requires internet          │
│  No GitHub account needed     │  Needs a GitHub account     │
│  Tracks commits & branches    │  Tracks PRs & issues        │
│  Created in 2005              │  Created in 2020            │
└─────────────────────────────────────────────────────────────┘
```

</div>

In practice you use both. `git commit`, `git push` - that's `git`. `gh pr create`, `gh issue list` - that's `gh`. They complement each other perfectly.

### 🔑 What is Authentication?

Before `gh` can talk to GitHub on your behalf, it needs to prove you are who you say you are. This is **authentication** - the one-time setup that connects the tool to your account.

`gh` handles this through a browser-based flow (the default) or a Personal Access Token. You do it once, and then every subsequent command just works.

---

## Installation

### 🪟 Windows

**Option 1 - winget (recommended):**
```
winget install --id GitHub.cli
```

**Option 2 - Scoop:**
```
scoop install gh
```

**Option 3 - MSI installer:**
Download directly from [cli.github.com](https://cli.github.com) - no package manager needed.

### 🍎 macOS

**Homebrew (recommended):**
```
brew install gh
```

**MacPorts:**
```
sudo port install gh
```

### 🐧 Linux

**Debian / Ubuntu:**
```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
&& sudo mkdir -p -m 755 /etc/apt/keyrings \
&& wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg \
   | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
   | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y
```

**Fedora / RHEL:**
```bash
sudo dnf install 'dnf-command(config-manager)'
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh --repo gh-cli
```

**Verify the installation worked:**
```
gh --version
# → gh version 2.x.x (yyyy-mm-dd)
```

---

## Authentication - Connecting gh to Your Account

Run this once after installation. You'll never need to think about it again.

```
gh auth login
```

You'll be guided through a short interactive flow:

```
? Where do you use GitHub?
  ▸ GitHub.com
    GitHub Enterprise Server

? What is your preferred protocol for Git operations?
  ▸ HTTPS
    SSH

? Authenticate Git with your GitHub credentials? (Y/n) Y

? How would you like to authenticate GitHub CLI?
  ▸ Login with a web browser
    Paste an authentication token
```

Select **Login with a web browser** - `gh` opens your browser, you approve, done. The token is stored securely in your system's credential store.

**Verify it worked:**
```
gh auth status
# → ✓ Logged in to github.com as YOUR-USERNAME
```

**Switching between accounts:**
```
gh auth login --hostname github.com   # add another account
gh auth switch                        # switch between them
gh auth logout                        # remove current account
```

> 🔒 `gh` never stores your password. It uses OAuth tokens, which can be revoked at any time from GitHub's Settings → Developer settings → Personal access tokens.

---

## The Command Structure

Every `gh` command follows the same logical pattern:

```
gh  [topic]  [action]  [target]  [flags]
 │      │        │         │         │
 │      │        │         │         └─ modifiers (--flag value)
 │      │        │         └─────────── what to act on
 │      │        └───────────────────── what to do
 │      └────────────────────────────── the GitHub feature area
 └───────────────────────────────────── the tool
```

**Examples:**
```
gh  repo    create   my-project  --public
gh  pr      merge    42          --squash
gh  issue   close    17          --comment "Fixed in #23"
gh  release create   v1.0.0      --generate-notes
```

Once this pattern clicks, you can guess most commands before looking them up. That's intentional - GitHub designed `gh` around discoverability.

> 💡 **When in doubt:** `gh [topic] --help` gives you the full command list for any topic. `gh help` lists all topics.

---

## The Commands

### Quick Overview Table

| Topic | What It Does | Key Commands |
|---|---|---|
| `gh repo` | Create, clone, fork, view repos | `create` `clone` `fork` `view` |
| `gh pr` | Full pull request lifecycle | `create` `list` `merge` `review` |
| `gh issue` | Create and manage issues | `create` `list` `close` `comment` |
| `gh workflow` | Trigger and inspect Actions | `run` `list` `view` |
| `gh run` | Monitor workflow runs | `list` `view` `watch` `download` |
| `gh release` | Create and manage releases | `create` `list` `upload` `download` |
| `gh gist` | Create and manage Gists | `create` `list` `view` `edit` |
| `gh secret` | Manage repo/org secrets | `set` `list` `delete` |
| `gh search` | Search GitHub from terminal | `repos` `issues` `prs` `code` |
| `gh alias` | Create custom command shortcuts | `set` `list` `delete` |
| `gh extension` | Add community-built commands | `install` `list` `upgrade` |

---

### 📁 gh repo - Repository Management

Everything you'd do on github.com/new or inside a repo's settings page, from the terminal.

#### Creating repositories

```bash
# Interactive - gh asks you everything
gh repo create

# Non-interactive - full control in one line
gh repo create my-project --public --clone
gh repo create my-project --private --description "Work in progress"
gh repo create org-name/my-project --public   # create inside an org
```

#### Cloning and forking

```bash
# Clone any repo (handles auth automatically)
gh repo clone owner/repo-name

# Fork a repo and clone your fork in one step
gh repo fork owner/repo-name --clone

# Fork and set up remote tracking of the upstream
gh repo fork owner/repo-name --clone --remote
```

The difference between `git clone` and `gh repo clone`:

```
git clone https://github.com/owner/repo.git
  → clones the repo, requires you to handle auth manually for private repos

gh repo clone owner/repo
  → clones the repo, handles auth automatically, works with private repos
    if your account has access
```

#### Viewing repo info

```bash
gh repo view                          # current repo
gh repo view owner/repo-name         # any repo
gh repo view owner/repo-name --web   # open in browser
```

#### Other useful repo commands

```bash
gh repo list                          # list your repos
gh repo list YOUR-USERNAME --limit 20
gh repo rename new-name               # rename current repo
gh repo archive                       # archive current repo
gh repo delete owner/repo-name        # delete (requires confirmation)
gh repo sync                          # sync fork with upstream
```

> ⚠️ `gh repo delete` is permanent. `gh` will ask you to type the repo name to confirm. There's no undo.

---

### 🔀 gh pr - Pull Requests

The single most-used part of `gh` for most developers. The entire PR lifecycle in one place.

#### Creating a pull request

```bash
# Interactive - gh fills in what it can, asks the rest
gh pr create

# Non-interactive
gh pr create --title "Fix login bug" --body "Resolves #42"

# Create as a draft
gh pr create --draft --title "WIP: new feature"

# Create targeting a specific base branch
gh pr create --base develop --title "Feature for develop"

# Create and immediately open in browser
gh pr create --web
```

When you run `gh pr create`, `gh` automatically:
- Detects your current branch
- Pushes it if it hasn't been pushed yet
- Pre-fills the title from your last commit message
- Links to issues mentioned in your commits

#### Listing and viewing PRs

```bash
gh pr list                            # open PRs in current repo
gh pr list --state closed             # closed PRs
gh pr list --author YOUR-USERNAME     # your PRs
gh pr list --label bug                # PRs with a specific label
gh pr list --assignee @me             # assigned to you

gh pr view 42                         # view PR #42
gh pr view 42 --web                   # open in browser
gh pr view                            # view PR for current branch
```

#### Checking out a PR locally

```bash
# Check out the branch for PR #42
gh pr checkout 42
```

This is genuinely one of the most useful commands in all of `gh`. Instead of:

```
# Old way
git fetch origin pull/42/head:pr-42
git checkout pr-42
```

You just type `gh pr checkout 42`. That's it.

#### Reviewing and merging

```bash
# Review
gh pr review 42 --approve
gh pr review 42 --request-changes --body "Please fix the edge case in line 47"
gh pr review 42 --comment --body "Looks good overall"

# Merge
gh pr merge 42                        # interactive - picks merge method
gh pr merge 42 --merge                # standard merge commit
gh pr merge 42 --squash               # squash into one commit
gh pr merge 42 --rebase               # rebase and merge
gh pr merge 42 --squash --delete-branch  # squash + clean up branch
```

#### Other PR commands

```bash
gh pr close 42                        # close without merging
gh pr reopen 42                       # reopen a closed PR
gh pr comment 42 --body "LGTM!"
gh pr ready 42                        # mark draft as ready for review
gh pr diff 42                         # show the diff
gh pr checks 42                       # show CI status
gh pr checks 42 --watch               # watch CI status live
```

> 💡 **Workflow tip:** `gh pr merge --squash --delete-branch` after a merge keeps your repo clean automatically. Combine it with an alias (covered later) and you'll never think about branch cleanup again.

---

### 🐛 gh issue - Issues

The complete issue management flow, no browser required.

#### Creating issues

```bash
# Interactive
gh issue create

# Non-interactive
gh issue create --title "Button broken on mobile" --body "Steps to reproduce..."

# With labels and assignees
gh issue create \
  --title "Add dark mode" \
  --body "Users have been requesting this for months." \
  --label "enhancement,good first issue" \
  --assignee YOUR-USERNAME

# Open browser to create (useful for complex formatting)
gh issue create --web
```

#### Listing and filtering

```bash
gh issue list                         # all open issues
gh issue list --state closed
gh issue list --assignee @me          # assigned to you
gh issue list --label "bug"
gh issue list --author YOUR-USERNAME
gh issue list --limit 50
gh issue list --milestone "v2.0"
```

#### Viewing and commenting

```bash
gh issue view 17                      # view issue #17
gh issue view 17 --web
gh issue comment 17 --body "I can reproduce this on macOS 14."
```

#### Closing and managing

```bash
gh issue close 17
gh issue close 17 --comment "Fixed in PR #42."
gh issue reopen 17
gh issue edit 17 --title "Updated title"
gh issue edit 17 --add-label "priority:high"
gh issue edit 17 --remove-label "needs triage"
gh issue edit 17 --add-assignee @me
```

#### Transferring and deleting

```bash
gh issue transfer 17 owner/other-repo
gh issue delete 17   # permanent - requires confirmation
```

---

### ⚙️ gh workflow & gh run - GitHub Actions

Trigger, monitor, and manage your CI/CD pipelines directly from the terminal.

#### Listing and viewing workflows

```bash
gh workflow list                      # all workflows in the repo
gh workflow view                      # view current/select a workflow
gh workflow view ci.yml
gh workflow view ci.yml --web
```

#### Triggering workflows manually

```bash
# Trigger a workflow_dispatch workflow
gh workflow run ci.yml

# With inputs
gh workflow run deploy.yml --field environment=production

# On a specific branch
gh workflow run ci.yml --ref develop
```

> ⚠️ `gh workflow run` only works for workflows that have a `workflow_dispatch` trigger. If your workflow only runs on `push` or `pull_request`, you can't trigger it manually with `gh`.

#### Enabling and disabling workflows

```bash
gh workflow enable ci.yml
gh workflow disable dependabot-updates.yml
```

#### Monitoring runs

```bash
gh run list                           # recent runs
gh run list --workflow ci.yml         # runs for a specific workflow
gh run list --branch main
gh run list --status failure          # only failed runs

gh run view 1234567890                # view a specific run
gh run view 1234567890 --log          # full logs
gh run view 1234567890 --log-failed   # only failed step logs
gh run watch 1234567890               # stream logs live
```

#### Cancelling and re-running

```bash
gh run cancel 1234567890
gh run rerun 1234567890               # rerun a failed run
gh run rerun 1234567890 --failed-only # only rerun failed jobs
```

#### Downloading artifacts

```bash
gh run download 1234567890            # download all artifacts
gh run download 1234567890 --name build-output  # specific artifact
gh run download 1234567890 --dir ./artifacts    # to a specific folder
```

---

### 🔔 gh notify - Notifications

Read and manage your GitHub notifications without leaving the terminal.

```bash
gh notify                             # interactive notification browser
gh notify --all                       # include already-read notifications
gh notify --participating             # only where you're participating
gh notify --repo owner/repo-name      # filter by repo
```

The interactive mode lets you navigate notifications with arrow keys, mark as read, open in browser, or filter on the fly. It's significantly faster than the GitHub notifications page for processing a full inbox.

---

### 🔑 gh secret - Secrets Management

Set and manage repository and organisation secrets without touching GitHub's UI.

```bash
# Set a secret (prompts for value - never pass secrets as arguments)
gh secret set MY_API_KEY

# Set from a file
gh secret set MY_CERT < cert.pem

# Set from stdin
echo "my-secret-value" | gh secret set MY_API_KEY

# List secrets (names only - values are never shown)
gh secret list

# Delete a secret
gh secret delete MY_API_KEY

# Organisation-level secrets
gh secret set MY_KEY --org my-org
gh secret set MY_KEY --org my-org --repos "repo1,repo2"

# Environment secrets
gh secret set MY_KEY --env production
```

> 🔒 **Always pipe secrets in or let `gh` prompt for them.** Never put a secret value directly in a command - it would appear in your shell history and be visible to anyone who can read it.

---

### 🌐 gh gist - Gists

Create, edit, and share Gists without opening a browser.

```bash
# Create a gist from a file
gh gist create script.sh

# Create a public gist with a description
gh gist create script.sh --public --desc "Useful backup script"

# Create from multiple files
gh gist create file1.py file2.py

# Create from stdin
echo "SELECT * FROM users;" | gh gist create --filename query.sql

# List your gists
gh gist list

# View a gist
gh gist view GIST-ID
gh gist view GIST-ID --raw
gh gist view GIST-ID --web

# Edit a gist
gh gist edit GIST-ID

# Delete a gist
gh gist delete GIST-ID
```

---

### 🔍 gh search - Search GitHub

Full GitHub search from the terminal, with filtering and formatting.

```bash
# Search repositories
gh search repos "cli tool" --language go --stars ">1000"
gh search repos "machine learning" --sort stars --limit 20

# Search issues and PRs
gh search issues "memory leak" --repo golang/go
gh search prs "fix auth" --state merged --author torvalds

# Search commits
gh search commits "fix race condition" --repo cli/cli

# Search code (returns file matches)
gh search code "gh.AuthTokenFromEnv" --repo cli/cli
```

**Useful search qualifiers:**

```
--language python         filter by programming language
--stars ">500"            minimum star count
--sort stars|forks|updated  sort order
--owner my-org            filter by owner
--state open|closed|merged  for issues/PRs
--limit 50                number of results (default 30)
--json fieldName          output as JSON for scripting
```

---

### 🔗 gh alias - Custom Shortcuts

Create your own commands that expand into longer `gh` commands.

```bash
# Create an alias
gh alias set co 'pr checkout'
# now: gh co 42  →  gh pr checkout 42

gh alias set prc 'pr create --draft'
# now: gh prc  →  gh pr create --draft

gh alias set mine 'issue list --assignee @me'
# now: gh mine  →  gh issue list --assignee @me

# Shell aliases (prefix with !)
gh alias set lpr '!gh pr list --author @me --state open'

# List all aliases
gh alias list

# Delete an alias
gh alias delete co
```

**Aliases with parameters:**

```bash
gh alias set newpr '!f() { gh pr create --title "$1" --body "$2"; }; f'
# usage: gh newpr "Fix the thing" "It was broken"
```

> 💡 **Best alias to start with:** `gh alias set done 'pr merge --squash --delete-branch'`. Then `gh done` closes and cleans up the current PR in one keystroke.

---

### 🧩 gh extension - Extending gh

The extension system lets the community add entirely new top-level commands to `gh`.

```bash
# Browse available extensions
gh ext search

# Install an extension
gh ext install dlvhdr/gh-dash         # a beautiful dashboard for PRs/issues
gh ext install meiji163/gh-notify     # enhanced notifications
gh ext install gennaro-tedesco/gh-f   # fuzzy-find anything on GitHub

# List installed extensions
gh ext list

# Upgrade extensions
gh ext upgrade --all
gh ext upgrade dlvhdr/gh-dash

# Remove an extension
gh ext remove dlvhdr/gh-dash
```

**Top extensions worth installing:**

| Extension | What It Does |
|---|---|
| `dlvhdr/gh-dash` | Full TUI dashboard - PRs, issues, and workflows in one view |
| `github/gh-copilot` | Ask Copilot for command suggestions from the terminal |
| `meiji163/gh-notify` | Better notification handling with filters |
| `gennaro-tedesco/gh-f` | Fuzzy-find repos, issues, and PRs interactively |
| `vilmibm/gh-screensaver` | Absolutely not useful. Completely necessary. |

> Anyone can write a `gh` extension - they're just shell scripts or Go binaries that follow a naming convention (`gh-*`). If `gh` is missing a command you need, you can build it.

---

## Combining gh With Other Tools

`gh` shines brightest when it's part of a pipeline rather than a standalone command.

#### JSON output for scripting

Almost every `gh` command supports `--json` followed by field names, plus `--jq` for inline filtering:

```bash
# Get the URL of your latest open PR
gh pr list --state open --json url --jq '.[0].url'

# Get all issue numbers with the "bug" label
gh issue list --label bug --json number --jq '.[].number'

# Count how many PRs you have open
gh pr list --author @me --json id --jq 'length'

# Get the run ID of the last failed workflow
gh run list --status failure --json databaseId --jq '.[0].databaseId'
```

#### Combining with fzf (fuzzy finder)

```bash
# Interactively pick a PR to check out
gh pr list --json number,title \
  --jq '.[] | "\(.number)\t\(.title)"' \
  | fzf | cut -f1 | xargs gh pr checkout

# Interactively pick an issue to view
gh issue list --json number,title \
  --jq '.[] | "\(.number)\t\(.title)"' \
  | fzf | cut -f1 | xargs gh issue view
```

#### Opening results in the browser

Any `gh` command that shows something supports `--web`:

```bash
gh pr view --web        # open current branch's PR in browser
gh repo view --web      # open repo in browser
gh run view --web       # open workflow run in browser
```

---

## Real Workflows You Can Steal

These are complete, copy-paste-ready workflows for common tasks.

#### The full PR lifecycle in 4 commands

```bash
# 1. Create a branch and do your work
git checkout -b fix/login-bug

# 2. Commit and push (git handles this)
git add . && git commit -m "Fix login redirect" && git push -u origin fix/login-bug

# 3. Open a PR
gh pr create --title "Fix login redirect on mobile" --body "Fixes #47"

# 4. After it's approved, merge and clean up
gh pr merge --squash --delete-branch
```

#### Quickly check in on your open work

```bash
# Everything assigned to you across issues and PRs
gh issue list --assignee @me
gh pr list --author @me
```

#### Trigger a deploy and watch it live

```bash
gh workflow run deploy.yml --field environment=production && \
  gh run watch $(gh run list --workflow deploy.yml --json databaseId --jq '.[0].databaseId')
```

#### Clone, set up, and open a repo in one shot

```bash
gh repo clone owner/repo-name && cd repo-name && gh repo view --web
```

#### Review all failing CI before merging

```bash
gh pr checks --watch   # stream live CI status for the current branch's PR
```

---

## The Full Command Reference
</br>
</br>
<details>
  <summary>Press here to look:</summary>

| Command | Description |
|---|---|
| `gh auth login` | Authenticate with GitHub |
| `gh auth logout` | Remove stored credentials |
| `gh auth status` | Show current auth state |
| `gh auth token` | Print the current auth token |
| `gh repo create` | Create a new repository |
| `gh repo clone` | Clone a repository |
| `gh repo fork` | Fork a repository |
| `gh repo view` | View repository information |
| `gh repo list` | List your repositories |
| `gh repo rename` | Rename a repository |
| `gh repo archive` | Archive a repository |
| `gh repo delete` | Delete a repository |
| `gh repo sync` | Sync a fork with upstream |
| `gh pr create` | Create a pull request |
| `gh pr list` | List pull requests |
| `gh pr view` | View a pull request |
| `gh pr checkout` | Check out a PR's branch |
| `gh pr merge` | Merge a pull request |
| `gh pr close` | Close a pull request |
| `gh pr reopen` | Reopen a pull request |
| `gh pr review` | Add a review to a PR |
| `gh pr comment` | Comment on a PR |
| `gh pr diff` | Show a PR's diff |
| `gh pr checks` | Show CI status for a PR |
| `gh pr ready` | Mark a draft PR as ready |
| `gh issue create` | Create an issue |
| `gh issue list` | List issues |
| `gh issue view` | View an issue |
| `gh issue close` | Close an issue |
| `gh issue reopen` | Reopen an issue |
| `gh issue comment` | Comment on an issue |
| `gh issue edit` | Edit an issue |
| `gh issue delete` | Delete an issue |
| `gh issue transfer` | Transfer an issue to another repo |
| `gh workflow list` | List workflows |
| `gh workflow run` | Trigger a workflow |
| `gh workflow view` | View a workflow |
| `gh workflow enable` | Enable a workflow |
| `gh workflow disable` | Disable a workflow |
| `gh run list` | List workflow runs |
| `gh run view` | View a workflow run |
| `gh run watch` | Stream a run's logs live |
| `gh run cancel` | Cancel a run |
| `gh run rerun` | Rerun a failed run |
| `gh run download` | Download run artifacts |
| `gh release create` | Create a release |
| `gh release list` | List releases |
| `gh release view` | View a release |
| `gh release upload` | Upload files to a release |
| `gh release download` | Download release assets |
| `gh release delete` | Delete a release |
| `gh secret set` | Set a secret |
| `gh secret list` | List secret names |
| `gh secret delete` | Delete a secret |
| `gh gist create` | Create a Gist |
| `gh gist list` | List your Gists |
| `gh gist view` | View a Gist |
| `gh gist edit` | Edit a Gist |
| `gh gist delete` | Delete a Gist |
| `gh search repos` | Search repositories |
| `gh search issues` | Search issues |
| `gh search prs` | Search pull requests |
| `gh search commits` | Search commits |
| `gh search code` | Search code |
| `gh alias set` | Create a command alias |
| `gh alias list` | List all aliases |
| `gh alias delete` | Delete an alias |
| `gh ext install` | Install an extension |
| `gh ext list` | List installed extensions |
| `gh ext upgrade` | Upgrade an extension |
| `gh ext remove` | Remove an extension |
| `gh ext search` | Search available extensions |

</details>
</br>
</br>

---

## Resources & Further Reading

| Resource | What It Gets You |
|---|---|
| [cli.github.com](https://cli.github.com) | Official site - installation and overview |
| [cli.github.com/manual](https://cli.github.com/manual) | The complete command reference |
| [github.com/cli/cli](https://github.com/cli/cli) | The open-source repo - report bugs, follow development |
| [github.com/cli/cli/releases](https://github.com/cli/cli/releases) | Release notes for every version |
| [GitHub Blog - gh announcement](https://github.blog/2020-09-17-github-cli-1-0-is-now-available/) | The original 1.0 launch post |
| [gh extension search](https://github.com/topics/gh-extension) | Browse all community extensions on GitHub |
| [dlvhdr/gh-dash](https://github.com/dlvhdr/gh-dash) | The best third-party extension - a full TUI dashboard |
| [GitHub Docs - gh](https://docs.github.com/en/github-cli) | Official documentation with examples |

---

## License

MIT License - fork it, adapt it, translate it, share it freely.

```
Stop clicking.
Start shipping.
```
<div align="center">
  
<img src="https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=More%20guides%20coming%20soon.&fontSize=28&fontColor=FCA5A5&fontAlignY=65" width="100%" />

</div>

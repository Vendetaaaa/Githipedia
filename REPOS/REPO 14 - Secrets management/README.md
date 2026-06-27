<div align="center">
  
[![](https://capsule-render.vercel.app/api?type=blur&height=250&color=B91C1C&text=Secrets%20and%20Environments&section=header&fontColor=FCA5A5&fontAlignY=34&desc=Protect%20your%20deploys.%20Lock%20down%20your%20secrets.&fontSize=18)](https://capsule-render.vercel.app/api?type=blur&height=250&color=B91C1C&text=Secrets%20%26%20Environments&section=header&fontColor=FCA5A5&fontAlignY=34&desc=Protect%20your%20deploys.%20Lock%20down%20your%20secrets.&fontSize=18)

[![CLI Friendly](https://img.shields.io/badge/CLI_Friendly-7F1D1D?style=for-the-badge&labelColor=1a1a1a)](https://img.shields.io/badge/CLI_Friendly-7F1D1D?style=for-the-badge&labelColor=1a1a1a) [![Last Updated](https://img.shields.io/badge/Last%20Updated-2026-991B1B?style=for-the-badge&labelColor=1a1a1a)](https://img.shields.io/badge/Last%20Updated-2026-991B1B?style=for-the-badge&labelColor=1a1a1a)

</div>

*Stop pasting API keys into Slack. Here's how GitHub actually wants you to gate deployments and store secrets.*

---

## Table of Contents
- [What Is This?](#what-is-this)
- [Core Concepts You Need First](#core-concepts-you-need-first)
  * [What is an Environment?](#-what-is-an-environment)
  * [What is a Deployment Job?](#-what-is-a-deployment-job)
  * [Why Not Just Use Repository Secrets For Everything?](#-why-not-just-use-repository-secrets-for-everything)
- [Environment Protection Rules](#environment-protection-rules)
  * [Required Reviewers](#-required-reviewers)
  * [Wait Timer](#-wait-timer)
  * [Deployment Branches and Tags](#-deployment-branches-and-tags)
  * [Setting It All Up](#setting-it-all-up)
  * [Approving a Deployment](#approving-a-deployment)
- [The Secrets Hierarchy](#the-secrets-hierarchy)
  * [The Three Levels](#the-three-levels)
  * [Precedence: Who Wins?](#precedence-who-wins)
  * [Choosing the Right Level](#choosing-the-right-level)
- [Syncing Secrets with the GitHub CLI](#syncing-secrets-with-the-github-cli)
  * [Setting a Single Secret](#-setting-a-single-secret)
  * [Bulk Syncing From a `.env` File](#-bulk-syncing-from-a-env-file)
  * [Syncing Across Repo, Org, and Environment](#-syncing-across-repo-org-and-environment)
  * [A Reusable Sync Script](#a-reusable-sync-script)
- [Common Pitfalls](#common-pitfalls)
- [Resources & Further Reading](#resources--further-reading)
- [License](#license)

---

## What Is This?

Every team eventually asks the same question: *"How do we stop a junior dev from accidentally pushing straight to production at 2 AM?"* GitHub's answer is **Environments** - and the protection rules and secret scoping that come with them.

This guide covers three things that almost always get tangled together in people's heads: how to gate a deployment behind a human approval, where a secret actually *should* live, and how to stop clicking through the web UI every time you need to update twelve API keys.

---

## Core Concepts You Need First

A few definitions before the good stuff - these get referenced constantly below.

### 🌐 What is an Environment?

An **environment** is a named deployment target inside a repository - things like `staging`, `production`, or `preview`. It's not a server or a URL by itself; it's a GitHub-side concept that a workflow job can *reference*, and which can carry its own rules and secrets.

```
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production   # ← this line is what ties the job to the environment
    steps:
      - run: ./deploy.sh
```

The moment a job references `environment: production`, GitHub checks whatever protection rules are attached to that environment **before** letting the job touch its secrets.

### 🚦 What is a Deployment Job?

Any job in a workflow that has an `environment:` key. That's it - that's the entire trigger condition for protection rules to apply.

```
Workflow triggers (push, PR, schedule...)
        ↓
Job references "environment: production"
        ↓
GitHub checks protection rules ──► not satisfied ──► job PAUSES
        ↓ satisfied
Job runs, environment secrets become available
```

> ⚠️ **Important nuance:** protection rules gate the *job*, not the whole workflow run. A workflow can have a `build` job that runs immediately and a `deploy` job that pauses - they don't block each other unless you say so with `needs:`.

### 🔐 Why Not Just Use Repository Secrets For Everything?

Because repository secrets have **no concept of approval**. The instant a workflow run starts, it can read every repository secret. If your production database password is a repository secret, *any* PR-triggered workflow on *any* branch can potentially reach it.

Environment secrets fix this: they're only available to workflow jobs that reference the environment, and if the environment requires approval, a job cannot access environment secrets until one of the required reviewers approves it. The secret is *physically* inaccessible until a human says yes.

---

## Environment Protection Rules

These are the guardrails you attach to an environment. There are three core ones, plus an extensible fourth for advanced setups.

| Rule | What It Does | Typical Use |
| --- | --- | --- |
| 👤 Required reviewers | Pauses the job until a person/team approves | Production deploys |
| ⏱️ Wait timer | Delays the job by a fixed number of minutes | "Cooling off" window before prod |
| 🌿 Deployment branches and tags | Restricts which branches/tags can deploy | Only `main` or `release/*` can hit prod |
| 🧩 Custom deployment protection rules | Gates deployment behind a third-party check (GitHub App) | Datadog/ServiceNow health checks |

### 👤 Required Reviewers

This is the "manual approval" feature people usually mean when they say that phrase. You enable required reviewers and add 1 to 6 individuals or teams. When a job targeting that environment runs, it pauses and a designated reviewer gets a notification - via email, GitHub notifications, and mobile push - and clicks approve or reject.

```
Job hits "environment: production"
            ↓
   🔔 Reviewer notified
            ↓
  ┌─────────┴─────────┐
  ▼                   ▼
Approved          Rejected
  ↓                   ↓
Deploy proceeds   Job fails, nothing deploys
```

There's also a **Prevent self-review** option - it prevents users from approving workflow runs that they triggered. Turn this on for production. Without it, the person who pushed the risky change can just rubber-stamp their own deploy.

> 💡 **Two-person rule:** combine a `workflow_dispatch` manual trigger with `environment: production` and required reviewers - now one human has to *start* the deploy, and a second human has to *approve* it.

### ⏱️ Wait Timer

A mandatory delay before the job is allowed to proceed, even with no reviewer involved. The time, in minutes, must be an integer between 1 and 43,200 - 30 days. Wait time doesn't count toward your billable minutes, so it's free insurance.

People use this as a "did we just break something obvious" buffer - long enough to catch an immediate failure in a downstream system, short enough not to annoy anyone.

### 🌿 Deployment Branches and Tags

Restricts which branches or tags are even allowed to reference the environment. The default option, protected branches only, means only branches with branch protection rules enabled can deploy - and if no branch protection rules exist anywhere in the repo, every branch can deploy.

In practice, most teams set a name pattern instead - `main`, `release/*` - so a random feature branch can't accidentally target production even if someone copy-pastes the wrong workflow file.

```
name: deploy
on: push
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v6
      - run: ./deploy.sh
# If the triggering branch doesn't match the environment's
# allowed branches/tags, this job simply fails before running.
```

### Setting It All Up

**1.** Go to your repo → **Settings → Environments → New environment**. Name it (`staging`, `production`, whatever matches your pipeline).

**2.** Under **Deployment protection rules**, toggle **Required reviewers**, pick up to 6 people or teams.

**3.** Optionally toggle **Wait timer** and set the minutes.

**4.** Under **Deployment branches and tags**, restrict to `main` or your release pattern.

**5.** Decide whether admins can bypass these rules. By default, administrators can bypass the protection rules and force deployments - you can disallow that for everyone if you want zero exceptions.

**6.** Click **Save protection rules**.

> ⚠️ **Plan limits matter here.** On GitHub Free, Pro, or Team plans, required reviewers and wait timers are only available for public repositories - private repos need GitHub Enterprise for those two specific controls. Branch restrictions and basic environment secrets still work on private repos with Pro/Team.

### Approving a Deployment

When a teammate's workflow run is sitting there waiting on you:

```
1. Open the Actions tab → click the waiting workflow run
2. You'll see a banner: "Review deployments"
3. Click it, select the environment(s) to approve or reject
4. Optionally leave a comment explaining your decision
5. Click "Approve and deploy" or "Reject"
```

This works from the GitHub Mobile app too - no laptop required to unblock a teammate's release.

---

## The Secrets Hierarchy

This is the part that trips up almost everyone the first time. There are **three levels** secrets can live at, and they don't stack the way most people assume.

### The Three Levels

```
🏢 Organization secrets
        │   shared across many repos, access controlled by policy
        ▼
📁 Repository secrets
        │   scoped to one repo, available to every workflow in it
        ▼
🔒 Environment secrets
        │   scoped to one environment, gated behind protection rules
        ▼
   Workflow job
```

| Level | Set By | Scope | Gated by Approval? |
| --- | --- | --- | --- |
| 🏢 Organization | Org owners/admins | Selected or all repos in the org | No |
| 📁 Repository | Repo admins/collaborators | The single repository | No |
| 🔒 Environment | Repo admins | Jobs referencing that environment | Yes, if reviewers are set |

A repository secret is available to **every** workflow in that repo, no matter which job or environment it touches. An organization secret lets you share credentials between multiple repositories, and updating it in one place takes effect everywhere that uses it - which is exactly why it's risky for anything truly sensitive: one compromised repo with org-secret access can be a back door into all of them.

### Precedence: Who Wins?

If the same secret *name* exists at more than one level, GitHub doesn't merge them or throw an error - it just picks one, silently, based on specificity. If a secret with the same name exists at multiple levels, the secret at the lowest level takes precedence.

```
        Organization secret: API_KEY = "org-value"
                    ↓ overridden by
         Repository secret: API_KEY = "repo-value"
                    ↓ overridden by
         Environment secret: API_KEY = "env-value"   ← this one wins
```

If an organization-level secret has the same name as a repository-level secret, the repository-level secret takes precedence. If an organization, repository, and environment all have a secret with the same name, the environment-level secret takes precedence.

> ⚠️ **The trap:** because there's no warning or error when this happens, it's easy to update an organization secret, see nothing change, and waste an hour debugging - only to discover a stale repository or environment secret with the same name has been silently winning the whole time. `gh secret list` at every level is your friend here.

There's a timing nuance too: organization and repository secrets are read when a workflow run is queued, while environment secrets are read when a job referencing the environment actually starts. So environment secrets reflect the *latest* value even if you update them mid-run; repo/org secrets are locked in at queue time.

### Choosing the Right Level

| If the secret is... | Put it at... |
| --- | --- |
| Shared by many repos (e.g. a shared npm registry token) | 🏢 Organization, with `--repos` restricted to the ones that need it |
| Specific to one project but used everywhere in it (e.g. a test API key) | 📁 Repository |
| Only relevant to one deployment target, and sensitive (e.g. prod DB credentials, signing keys) | 🔒 Environment, with required reviewers enabled |

> 🎯 **Rule of thumb:** the more damage a leaked secret could do, the lower it should live - and the more approval friction should sit in front of it. Production signing keys belong in an environment behind required reviewers, full stop.

---

## Syncing Secrets with the GitHub CLI

Clicking "New secret" in the web UI twelve times is how you end up with a typo in `DATBASE_URL` that costs you an afternoon. The `gh` CLI fixes this.

First, make sure you're authenticated:

```
gh auth login
gh auth status
```

### 🔑 Setting a Single Secret

```
# Interactive prompt - paste the value, repository-scoped
gh secret set API_KEY

# Read the value from a shell variable
gh secret set API_KEY --body "$API_KEY_VALUE"

# Read the value from a file
gh secret set CERTIFICATE_BASE64 < cert.base64

# Set it for a specific environment instead of the whole repo
gh secret set DATABASE_URL --env production

# Set it at the organization level, visible to all repos
gh secret set NPM_TOKEN --org my-org --visibility all

# Set it at the organization level, visible to specific repos only
gh secret set NPM_TOKEN --org my-org --repos repo1,repo2
```

> 💬 By default, GitHub CLI authenticates with the `repo` and `read:org` scopes - to manage organization secrets you must additionally authorize the `admin:org` scope.

### 📄 Bulk Syncing From a `.env` File

If you've got a `.env` full of values, you don't need to set them one by one. The cleanest built-in option is the `--env-file` flag:

```
gh secret set --env-file .env.production --env production --repo your-org/your-repo
```

This reads every `KEY=VALUE` line and creates or updates a matching secret in one shot.

If your `gh` version doesn't support `--env-file` yet, a short loop does the same job:

```
#!/bin/bash
# sync-secrets.sh - push every line of .env as a repo secret

if [ ! -f .env ]; then
  echo "No .env file found." && exit 1
fi

if ! gh auth status &>/dev/null; then
  echo "Not authenticated - run 'gh auth login' first." && exit 1
fi

while IFS='=' read -r key value; do
  # skip blank lines and comments
  [[ -z "$key" || "$key" == \#* ]] && continue
  echo "Syncing $key..."
  gh secret set "$key" --body "$value"
done < .env
```

> ⚠️ **Never commit `.env` to the repo it's syncing into.** If you're keeping a local `.env` for this purpose, add it to `.gitignore` before you do anything else.

### 🔀 Syncing Across Repo, Org, and Environment

Since the three levels use the same subcommand with different flags, scripting a full sync across all of them is straightforward:

```
# Org-wide secret, shared by everything
gh secret set NPM_TOKEN --org my-org --visibility all

# Repo-level secret, used by every workflow in this repo
gh secret set SENTRY_DSN --repo my-org/my-repo

# Environment-level secrets, one per deployment target
gh secret set DATABASE_URL --env staging    --repo my-org/my-repo
gh secret set DATABASE_URL --env production --repo my-org/my-repo
```

### A Reusable Sync Script

A slightly more complete version that handles all three environments from separate files, for a typical staging/production split:

```
#!/bin/bash
# sync-all-environments.sh
set -euo pipefail

REPO="my-org/my-repo"

sync_env() {
  local file=$1
  local environment=$2
  echo "── Syncing $file → environment: $environment ──"
  gh secret set --env-file "$file" --env "$environment" --repo "$REPO"
}

sync_env .env.staging    staging
sync_env .env.production production

echo "Done. Verifying..."
gh secret list --env staging    --repo "$REPO"
gh secret list --env production --repo "$REPO"
```

> 💡 **Drop this into CI itself** - a small workflow that runs `sync-all-environments.sh` whenever `.env.*.encrypted` changes in a release PR keeps secrets and code changes reviewed together, instead of someone updating one and forgetting the other.

To confirm anything actually landed where you expect:

```
gh secret list                          # repository secrets
gh secret list --env production         # one environment's secrets
gh secret list --org my-org             # organization secrets
```

To remove one:

```
gh secret delete SECRET_NAME
gh secret delete SECRET_NAME --env production
gh secret delete SECRET_NAME --org my-org
```

---

## Common Pitfalls

- **Forgetting environment secrets are gated by approval, not just by name.** A job can reference the right environment and still fail to read a secret if nobody's approved the run yet.
- **Assuming `--repos` defaults to "all."** Org secrets default to private-repo visibility unless you explicitly pass `--visibility all` or list repos.
- **Letting admins silently bypass protection rules.** If "Allow administrators to bypass configured protection rules" stays checked, your required-reviewer setup has a built-in skip button.
- **Same secret name, three different values, no warnings.** Covered above, but worth repeating - precedence failures are silent. `gh secret list` at every level before you assume a value took effect.
- **A 35-day ceiling on approvals.** A paused job holds a runner slot; GitHub Actions workflows have a maximum run time, and an unapproved deployment will eventually get cancelled rather than wait forever. Don't let approval requests rot - wire up a Slack/email ping for pending reviews.

---

## Resources & Further Reading

| Resource | What It Gets You |
| --- | --- |
| [GitHub Docs - Deployments and Environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) | The authoritative reference on protection rules |
| [GitHub Docs - Secrets Reference](https://docs.github.com/en/actions/reference/security/secrets) | Naming rules, limits, and the precedence behavior in full |
| [GitHub Docs - Using Secrets in GitHub Actions](https://docs.github.com/actions/security-guides/using-secrets-in-github-actions) | Step-by-step UI and `gh` CLI instructions for all three levels |
| [GitHub Docs - Reviewing Deployments](https://docs.github.com/actions/managing-workflow-runs/reviewing-deployments) | How approvals actually work from the reviewer's side |
| [GitHub CLI Manual - `gh secret`](https://cli.github.com/manual/gh_secret_set) | Every flag `gh secret set` supports, with examples |
| [trstringer/manual-approval](https://github.com/trstringer/manual-approval) | Issue-based manual approval for plans without native required reviewers |
| [Shields.io](https://shields.io) | Build custom badges for any README |
| [Capsule Render](https://github.com/kyechan99/capsule-render) | Header and footer banners like the one above |

---

## License

MIT - fork it, adapt it, share it freely.

<div align="center">

[![](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=Approve%20before%20you%20deploy.&fontSize=28&fontColor=FCA5A5&animation=fadeIn&fontAlignY=65)](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=Approve%20before%20you%20deploy.&fontSize=28&fontColor=FCA5A5&animation=fadeIn&fontAlignY=65)

</div>

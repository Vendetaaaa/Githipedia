<div align="center">

<img src="https://capsule-render.vercel.app/api?type=blur&height=250&color=B91C1C&text=GitHub+Security+Secrets&section=header&fontColor=FCA5A5&fontAlignY=34&desc=Stop+leaking+secrets.+Lock+your+repo+down.&descAlignY=55&descSize=18">

</div>

---

## Table of Contents

- [Why Security Keeps Tripping Developers Up](#why-security-keeps-tripping-developers-up)
- [GitHub Secrets: Hiding Passwords From Your Code](#github-secrets-hiding-passwords-from-your-code)
  - [What is a Secret?](#what-is-a-secret)
  - [How to Add a Secret](#how-to-add-a-secret)
  - [Using Secrets in a Workflow](#using-secrets-in-a-workflow)
  - [What Secrets Cannot Do](#what-secrets-cannot-do)
- [SSH Keys vs Personal Access Tokens](#ssh-keys-vs-personal-access-tokens)
  - [The Core Difference](#the-core-difference)
  - [Setting Up an SSH Key](#setting-up-an-ssh-key)
  - [Setting Up a Personal Access Token](#setting-up-a-personal-access-token)
  - [Which One Should You Use?](#which-one-should-you-use)
- [Branch Protection: Stopping Accidental Force-Pushes to Main](#branch-protection-stopping-accidental-force-pushes-to-main)
  - [What Branch Protection Does](#what-branch-protection-does)
  - [How to Turn It On](#how-to-turn-it-on)
  - [Recommended Settings](#recommended-settings)
- [Environments: Requiring Approval Before You Deploy](#environments-requiring-approval-before-you-deploy)
  - [What Environments Are](#what-environments-are)
  - [Setting Up a Production Environment](#setting-up-a-production-environment)
  - [Hooking an Environment Into a Workflow](#hooking-an-environment-into-a-workflow)
- [Quick Reference](#quick-reference)
- [License](#license)

---

## Why Security Keeps Tripping Developers Up

Most security mistakes on GitHub are not the result of carelessness. They happen because nothing warns you before you make them. You paste an API key into a file, push it, and it's gone. Scraped by bots that watch GitHub in real time, sometimes within seconds.

This guide covers four things that, once set up, prevent the most common problems from happening in the first place.

> *None of this requires advanced knowledge. If you can push code to GitHub, you can do all of this.*
> *To be secured, you must be aware of your surroundings*

---

## GitHub Secrets: Hiding Passwords From Your Code

### What is a Secret?

A secret is a way to store sensitive information, API keys, database passwords, tokens, inside GitHub so your code can use it without the value ever appearing in your files.

Instead of writing this in your code:

```yaml
# NEVER do this
- name: Deploy
  run: ./deploy.sh --token=sk_live_abc123supersecretkey
```

You store `sk_live_abc123supersecretkey` as a secret and reference it by name:

```yaml
- name: Deploy
  run: ./deploy.sh --token=${{ secrets.DEPLOY_TOKEN }}
```

The actual value never touches your files. It lives in GitHub's settings and gets injected when the workflow runs.

### How to Add a Secret

**1.** Go to your repository on GitHub.

**2.** Click **Settings** (you need to be the repo owner or have admin access).

**3.** In the left sidebar, click **Secrets and variables**, then **Actions**.

**4.** Click **New repository secret**.

**5.** Give it a clear name in capital letters , `DATABASE_URL`, `API_KEY`, `STRIPE_SECRET` , and paste the value in. Click **Add secret**.

That's it. The value is now encrypted and stored. Even GitHub staff cannot read it back.

### Using Secrets in a Workflow

Reference any secret with `${{ secrets.YOUR_SECRET_NAME }}` inside your workflow files:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Send to server
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: ./scripts/deploy.sh
```

The `env:` block makes each secret available as a normal environment variable for that step.

### What Secrets Cannot Do

There are a few things worth knowing upfront:

```
You cannot read a secret value back once it's saved.
If you lose it, you have to replace it with a new one.

Secrets are not available in pull requests from forks.
This is intentional , it stops strangers from writing
a workflow that prints your secrets to the logs.

Do not print secrets in logs, even accidentally.
GitHub will mask them if it recognizes the format,
but that is not something to rely on.
```

> ⚠️ **A common mistake:** Storing secrets directly in your `.env` file and committing it. Even if you delete it in the next commit, it lives forever in your Git history. If this happens to you, rotate the key immediately , do not just delete the file and hope for the best.

---

## SSH Keys vs Personal Access Tokens

Both of these let you authenticate with GitHub from your computer or from automated tools. They do the same job but work differently.

### The Core Difference

| | SSH Key | Personal Access Token (PAT) |
|---|---|---|
| What it looks like | A pair of files on your computer | A long string of characters |
| How it works | Proves who you are using math, no password | Acts like a password you paste in |
| Where it's used | Git operations (clone, push, pull) | Git operations and the GitHub API |
| How you set it up | Generate locally, add public half to GitHub | Generate on GitHub, copy and store it |
| If someone steals it | They need both files (harder to steal) | They can use it immediately |

### Setting Up an SSH Key

**1.** Open your terminal and generate a key pair:

```bash
ssh-keygen -t ed25519 -C "your@email.com"
```

Press Enter through the prompts. This creates two files in `~/.ssh/`:
- `id_ed25519` , your private key. Never share this.
- `id_ed25519.pub` , your public key. This is what you give to GitHub.

**2.** Copy your public key:

```bash
# Mac
pbcopy < ~/.ssh/id_ed25519.pub

# Linux
cat ~/.ssh/id_ed25519.pub
# then copy the output manually

# Windows (Git Bash)
clip < ~/.ssh/id_ed25519.pub
```

**3.** Go to **GitHub → Settings → SSH and GPG keys → New SSH key**. Give it a name, paste the public key in, and save.

**4.** Test that it worked:

```bash
ssh -T git@github.com
# You should see: Hi username! You've successfully authenticated.
```

From now on, clone repos using the SSH URL (`git@github.com:username/repo.git`) instead of the HTTPS one.

### Setting Up a Personal Access Token

**1.** Go to **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**.

**2.** Click **Generate new token (classic)**.

**3.** Give it a name that tells you what it's for , "Home laptop git access" or "CI deploy script".

**4.** Set an expiration date. Tokens that never expire are a risk if they end up somewhere they shouldn't.

**5.** Check the scopes you need. For basic Git operations, `repo` is enough.

**6.** Click **Generate token** and copy it immediately. You will not see it again.

**7.** When Git asks for your password, paste the token in instead.

> 💡 **Tip:** Store your token in your system's credential manager, not in a text file. On Mac that's Keychain, on Windows it's Credential Manager. Git can be set to use them automatically.

### Which One Should You Use?

Use SSH keys for everyday work on your own machine. They are more secure and you only have to set them up once per computer.

Use PATs when you need to authenticate from a script, a CI system, or somewhere you cannot use SSH , or when you need access to the GitHub API rather than just Git.

> ⚠️ **Never commit a PAT to a repo.** If you do, revoke it immediately at **Settings → Developer settings → Personal access tokens** and generate a new one.

---

## Branch Protection: Stopping Accidental Force-Pushes to Main

### What Branch Protection Does

Without branch protection, anyone with write access to your repo can push directly to `main` , including you, by accident. They can also force-push, which rewrites history and can permanently destroy work that was there before.

Branch protection rules let you say: "Before anything lands in `main`, it has to go through a pull request. And that pull request has to pass certain checks."

### How to Turn It On

**1.** Go to your repo and click **Settings**.

**2.** In the left sidebar, click **Branches**.

**3.** Under "Branch protection rules", click **Add rule**.

**4.** In the "Branch name pattern" box, type `main`.

**5.** Choose your settings (see below) and click **Create**.

### Recommended Settings

These are the ones most teams end up wishing they had turned on from the start:

**Require a pull request before merging**

Nobody can push directly to `main`. Changes have to come through a pull request. If you are working solo, you can set "Required number of approvals" to 0, which still forces the PR workflow without needing a second person.

**Require status checks to pass before merging**

If you have any automated tests or linters set up, this makes them a requirement. A PR cannot be merged if the tests are failing. Add your checks by name in the search box that appears after checking this option.

**Do not allow bypassing the above settings**

By default, repo admins can bypass protection rules. Checking this option makes the rules apply to everyone, including you.

**Block force pushes**

This prevents anyone from rewriting the history of `main` with a force push. You almost never want this on your main branch.

```
Result of turning these on:
Someone wants to change main
        ↓
They have to create a branch
        ↓
They open a pull request
        ↓
Automated checks run
        ↓
If checks pass, the PR can be merged
        ↓
main stays clean and auditable
```

> 💬 *Even on personal projects, this is worth doing. It forces you into a habit that will feel completely natural by the time you join a team where it is required.*

---

## Environments: Requiring Approval Before You Deploy

### What Environments Are

An environment in GitHub is a named deployment target , usually something like `staging` or `production` , that you can attach rules to.

The most useful rule is requiring a human to click "approve" before a workflow can deploy to that environment. This means no code reaches your live server without someone consciously saying "yes, this is ready."

### Setting Up a Production Environment

**1.** Go to **Settings → Environments → New environment**.

**2.** Name it `production` (or whatever you call your live server).

**3.** Under "Deployment protection rules", check **Required reviewers**.

**4.** Add yourself, a teammate, or a team as a required reviewer.

**5.** Click **Save protection rules**.

You can also add environment-specific secrets here , separate from your repo secrets , so that production credentials are only accessible when deploying to production specifically.

### Hooking an Environment Into a Workflow

Add `environment: production` to the job that does the actual deployment:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  deploy:
    needs: test          # only runs if tests pass
    runs-on: ubuntu-latest
    environment: production    # triggers the approval gate
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to server
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: ./deploy.sh
```

When this workflow runs, it will complete the `test` job and then pause. GitHub will notify the required reviewers. Only after someone approves does the `deploy` job continue.

```
Push to main
      ↓
Tests run automatically
      ↓
Deploy job is paused
      ↓
Reviewer gets notified and clicks Approve
      ↓
Code deploys to production
```

> 💡 **Why this matters:** The most common way deployments go wrong is someone merging something at the wrong moment , late at night, in a hurry, right before a deadline. A required approval forces a second of intention before the point of no return.

---

## Quick Reference

| Task | Where to Do It |
|---|---|
| Add a secret | Settings → Secrets and variables → Actions |
| Generate an SSH key | Terminal: `ssh-keygen -t ed25519 -C "you@email.com"` |
| Add SSH key to GitHub | Settings → SSH and GPG keys |
| Generate a PAT | Settings → Developer settings → Personal access tokens |
| Turn on branch protection | Settings → Branches → Add rule |
| Create a deployment environment | Settings → Environments → New environment |
| Add an approval requirement | Inside the environment settings, under "Deployment protection rules" |


---

## License

MIT: fork it, adapt it, share it freely.

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=Lock+it+down+from+day+one.&fontSize=36&fontColor=FCA5A5&animation=fadeIn&fontAlignY=65)

</div>

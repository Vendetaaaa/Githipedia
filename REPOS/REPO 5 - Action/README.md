<div align="center">

![GitHub Actions](https://capsule-render.vercel.app/api?type=blur&height=260&color=B91C1C&text=GitHub+Actions&section=header&fontColor=FCA5A5&fontAlignY=34&desc=Automate+everything.+Build%2C+test%2C+deploy%2C+and+more+%E2%80%94+straight+from+your+repo.+%E2%9A%99%EF%B8%8F&descAlignY=55&descSize=16)

![Beginner Friendly](https://img.shields.io/badge/Beginner_Friendly-B91C1C?style=flat-square&logoColor=white)
![Last Updated](https://img.shields.io/badge/Last%20Updated-2026-7F1D1D?style=flat-square)
![Full Reference](https://img.shields.io/badge/Full_Reference-EF4444?style=flat-square)

</div>

*Automate your builds, tests, and deployments without leaving GitHub. This guide covers everything from your first workflow to custom actions and matrix builds.*

---

## Table of Contents

- [What Is GitHub Actions?](#what-is-github-actions)
- [Things You Should Know First](#things-you-should-know-first)
  - [Workflows](#-what-is-a-workflow)
  - [Events](#-what-is-an-event)
  - [Jobs](#-what-is-a-job)
  - [Steps](#-what-is-a-step)
  - [Runners](#-what-is-a-runner)
  - [Actions](#-what-is-an-action)
- [Your First Workflow](#your-first-workflow)
- [Triggers - When Workflows Run](#triggers--when-workflows-run)
  - [Push and Pull Request](#push-and-pull-request)
  - [Schedule](#schedule)
  - [Manual Triggers](#manual-triggers)
  - [Other Events](#other-events)
- [Jobs](#jobs)
  - [Running Jobs in Parallel](#running-jobs-in-parallel)
  - [Running Jobs in Sequence](#running-jobs-in-sequence)
- [Steps and Shell Commands](#steps-and-shell-commands)
- [Using Actions](#using-actions)
  - [Official Actions](#official-actions)
  - [Community Actions](#community-actions)
  - [Pinning Action Versions](#pinning-action-versions)
- [Environment Variables and Secrets](#environment-variables-and-secrets)
  - [Environment Variables](#environment-variables)
  - [Secrets](#secrets)
  - [Environments](#environments)
- [Expressions and Contexts](#expressions-and-contexts)
- [Conditionals](#conditionals)
- [Matrix Builds](#matrix-builds)
- [Artifacts](#artifacts)
- [Caching Dependencies](#caching-dependencies)
- [Reusable Workflows](#reusable-workflows)
- [Custom Actions](#custom-actions)
  - [Composite Actions](#composite-actions)
  - [JavaScript Actions](#javascript-actions)
  - [Docker Actions](#docker-actions)
- [Permissions](#permissions)
- [Self-Hosted Runners](#self-hosted-runners)
- [Debugging and Troubleshooting](#debugging-and-troubleshooting)
- [Pricing and Limits](#pricing-and-limits)
- [Resources](#resources)
- [License](#license)

---

## What Is GitHub Actions?

GitHub Actions is GitHub's built-in automation platform. You write a YAML file, drop it in your repo, and GitHub runs it automatically whenever something happens, a push, a PR, a new release, a schedule, whatever you set it to.

The most common use is CI/CD. Every time someone pushes code, run the tests. Every time a PR opens, lint it. Every time you tag a release, build and deploy it. But Actions isn't limited to code either. You can use it to auto-label issues, send Slack notifications, generate docs, update a README with live data, basically anything that can be scripted.

It runs in the cloud by default on GitHub's infrastructure. You don't set up servers, you don't install anything. You write YAML and it runs.

```
You push code
    ↓
GitHub detects the event
    ↓
Your workflow file runs on a virtual machine in the cloud
    ↓
Results show up in the Actions tab of your repo
```

---

## Things You Should Know First

GitHub Actions has its own vocabulary and the docs assume you already know it. Read this once and the rest of the guide will make sense immediately.

### ⚙️ What is a Workflow?

A workflow is an automated process you define in a YAML file. It lives in `.github/workflows/` in your repo. You can have as many as you want, one for CI, one for deployment, one for issue triage, whatever you need.

```
your-repo/
└── .github/
    └── workflows/
        ├── ci.yml          ← runs tests on every push
        ├── deploy.yml      ← deploys on release
        └── label.yml       ← auto-labels issues
```

Each file is independent. They don't know about each other unless you explicitly set them up to interact.

### ⚡ What is an Event?

An event is what triggers a workflow to run. A push to main, a PR being opened, a new issue, a cron schedule, someone clicking a button. You define which events trigger your workflow at the top of the file.

```yaml
on: push          # runs on every push to any branch
on: [push, pull_request]   # runs on either
```

### 📦 What is a Job?

A job is a collection of steps that runs on a single machine. By default, jobs in the same workflow run in parallel. You can make them depend on each other if order matters.

Each job gets its own fresh virtual machine. Files from one job don't automatically carry over to another, you have to pass them explicitly using artifacts.

### 🔢 What is a Step?

A step is a single task inside a job. It's either a shell command or an action (a reusable piece of automation). Steps within a job run in order, one after another, on the same machine.

```yaml
steps:
  - name: Install dependencies
    run: npm install

  - name: Run tests
    run: npm test
```

### 💻 What is a Runner?

A runner is the virtual machine that actually executes your job. GitHub provides hosted runners running Ubuntu, Windows, and macOS. They're fresh machines spun up for each job and thrown away when it's done.

| Runner | Label |
|---|---|
| Ubuntu (latest) | `ubuntu-latest` |
| Ubuntu 22.04 | `ubuntu-22.04` |
| Windows (latest) | `windows-latest` |
| macOS (latest) | `macos-latest` |

You can also run jobs on your own machines. That's covered in [Self-Hosted Runners](#self-hosted-runners).

### 🧩 What is an Action?

An action is a reusable unit of automation. Instead of writing a bash script to checkout your code, set up Node, or upload a file to S3, someone's already written an action for that and you just reference it. Actions can be written by GitHub, the community, or you.

```yaml
- uses: actions/checkout@v4        # checks out your code
- uses: actions/setup-node@v4      # installs Node.js
```

---

## Your First Workflow

Here's a complete, working workflow that runs tests on every push. Drop this in `.github/workflows/ci.yml` and it will work for any Node.js project.

```yaml
name: CI

on: push

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test
```

What each part does:

```
name:        → the display name in the Actions tab
on:          → what triggers this workflow (push to any branch)
jobs:        → list of jobs to run
  test:      → name of this job (you choose it)
    runs-on: → which runner to use
    steps:   → list of things to do, in order
```

Push this file to your repo and go to the Actions tab. You'll see it running.

---

## Triggers - When Workflows Run

The `on:` key controls when your workflow runs. This is one of the most important things to get right.

### Push and Pull Request

```yaml
on:
  push:
    branches:
      - main
      - 'release/**'    # matches release/1.0, release/2.0, etc.
  pull_request:
    branches:
      - main
```

You can also filter by file paths. Useful when you only want CI to run if relevant files changed:

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'package.json'
```

And you can ignore paths:

```yaml
on:
  push:
    paths-ignore:
      - '**.md'        # don't run CI for documentation changes
```

### Schedule

Cron syntax. Runs your workflow on a timer regardless of any code activity.

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'    # every Monday at 9am UTC
```

```
┌───────── minute (0-59)
│ ┌───────── hour (0-23)
│ │ ┌───────── day of month (1-31)
│ │ │ ┌───────── month (1-12)
│ │ │ │ ┌───────── day of week (0-6, Sunday=0)
│ │ │ │ │
* * * * *
```

Common examples:

```yaml
'0 0 * * *'      # daily at midnight UTC
'0 9 * * 1-5'   # weekdays at 9am UTC
'*/15 * * * *'  # every 15 minutes
```

> ⚠️ Scheduled workflows only run on the default branch. If you add a schedule trigger to a workflow on a feature branch, it won't fire.

### Manual Triggers

`workflow_dispatch` lets you run a workflow manually from the Actions tab or via the API. You can add inputs so the person triggering it can pass values.

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy target'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
      debug:
        description: 'Enable debug logging'
        type: boolean
        default: false
```

Access the inputs in your steps:

```yaml
- name: Deploy
  run: ./deploy.sh ${{ inputs.environment }}
```

### Other Events

A few other useful ones:

```yaml
on:
  issues:
    types: [opened, labeled]        # when an issue is opened or labeled

  release:
    types: [published]              # when a release is published

  workflow_run:
    workflows: ['CI']
    types: [completed]              # when another workflow finishes

  repository_dispatch:              # triggered via API from outside GitHub
    types: [custom-event]
```

---

## Jobs

### Running Jobs in Parallel

By default, jobs run at the same time. This is fine when they're independent.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - run: npm run typecheck
```

`test`, `lint`, and `typecheck` all start simultaneously. Faster overall.

### Running Jobs in Sequence

Use `needs` to make a job wait for another to succeed first.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  build:
    needs: test           # only runs if test passes
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  deploy:
    needs: build          # only runs if build passes
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

You can depend on multiple jobs:

```yaml
  deploy:
    needs: [test, build, lint]    # all three must pass
```

---

## Steps and Shell Commands

The `run` key executes shell commands. By default it uses bash on Linux/macOS and PowerShell on Windows.

```yaml
steps:
  - name: Single command
    run: echo "hello"

  - name: Multiple commands
    run: |
      echo "first"
      echo "second"
      npm install

  - name: Use a specific shell
    shell: python
    run: |
      import os
      print(os.getcwd())
```

You can set a working directory for a step:

```yaml
  - name: Build frontend
    working-directory: ./frontend
    run: npm run build
```

Steps share the filesystem within a job. If step 1 creates a file, step 2 can read it.

---

## Using Actions

### Official Actions

GitHub maintains a set of official actions under the `actions/` namespace. These are the ones you'll use in almost every workflow.

| Action | What it does |
|---|---|
| `actions/checkout@v4` | Checks out your repository code |
| `actions/setup-node@v4` | Installs a specific version of Node.js |
| `actions/setup-python@v5` | Installs a specific version of Python |
| `actions/setup-java@v4` | Installs a specific version of Java |
| `actions/setup-go@v5` | Installs a specific version of Go |
| `actions/cache@v4` | Caches files between runs |
| `actions/upload-artifact@v4` | Saves files from a job |
| `actions/download-artifact@v4` | Retrieves saved files in another job |
| `actions/github-script@v7` | Runs JavaScript with access to the GitHub API |

### Community Actions

The GitHub Marketplace has thousands of community-built actions. Find them at [github.com/marketplace](https://github.com/marketplace?type=actions).

Some widely-used ones:

```yaml
- uses: docker/build-push-action@v5        # build and push Docker images
- uses: aws-actions/configure-aws-credentials@v4  # set up AWS credentials
- uses: codecov/codecov-action@v4          # upload coverage reports
- uses: slackapi/slack-github-action@v1    # send Slack notifications
- uses: softprops/action-gh-release@v2     # create GitHub releases
```

### Pinning Action Versions

Always pin to a specific version, not `@main` or `@master`. Using a floating ref means a third-party maintainer could change what runs in your workflow.

```yaml
# Bad - could change without warning
- uses: some-org/some-action@main

# Better - pinned to a tag
- uses: some-org/some-action@v2

# Best - pinned to a specific commit SHA
- uses: some-org/some-action@a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2
```

For official GitHub actions, pinning to a major version tag (`@v4`) is generally safe since they follow semantic versioning.

---

## Environment Variables and Secrets

### Environment Variables

Set variables at the workflow, job, or step level.

```yaml
env:
  NODE_ENV: production      # available to all jobs

jobs:
  build:
    env:
      APP_VERSION: '2.0'    # available to all steps in this job

    steps:
      - name: Print version
        env:
          DEBUG: 'true'     # available only to this step
        run: echo "$APP_VERSION"
```

GitHub also provides a set of built-in variables:

```yaml
${{ github.sha }}           # the commit SHA that triggered the workflow
${{ github.ref }}           # the branch or tag ref
${{ github.actor }}         # the username that triggered it
${{ github.repository }}    # owner/repo-name
${{ github.event_name }}    # push, pull_request, etc.
```

### Secrets

Secrets are encrypted values stored in your repo or org settings. Never put passwords, tokens, or API keys directly in your workflow file.

**Adding a secret:**

```
Repo → Settings → Secrets and variables → Actions → New repository secret
```

**Using a secret:**

```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.MY_API_KEY }}
    run: ./deploy.sh
```

Secrets are masked in logs. If a secret value accidentally appears in output, GitHub replaces it with `***`.

One secret is available automatically without you setting it up:

```yaml
${{ secrets.GITHUB_TOKEN }}    # auto-generated token with repo permissions
```

Use it to push commits, create releases, comment on PRs, and interact with the GitHub API from within your workflow.

### Environments

Environments let you group secrets, add protection rules, and require manual approval before a deployment runs.

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production     # uses secrets from the production environment
    steps:
      - run: ./deploy.sh
```

Set up environments under `Repo → Settings → Environments`. You can require specific reviewers to approve before the job runs, which is useful for production deployments.

---

## Expressions and Contexts

Expressions let you do logic inside your YAML using `${{ }}` syntax.

```yaml
${{ github.ref == 'refs/heads/main' }}    # true/false
${{ secrets.MY_SECRET }}                   # read a secret
${{ env.MY_VAR }}                          # read an env variable
${{ steps.my-step.outputs.result }}        # read output from a step
${{ matrix.node-version }}                 # read a matrix value
```

You can use operators inside expressions:

```yaml
${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
${{ contains(github.event.pull_request.labels.*.name, 'deploy') }}
${{ startsWith(github.ref, 'refs/tags/') }}
```

Contexts available:

| Context | What it contains |
|---|---|
| `github` | Event payload, repo info, actor, ref |
| `env` | Environment variables |
| `vars` | Repository/org variables (non-secret) |
| `secrets` | Encrypted secrets |
| `steps` | Outputs and results from previous steps |
| `jobs` | Outputs from other jobs |
| `runner` | Info about the current runner |
| `matrix` | Current matrix values |
| `inputs` | Inputs from workflow_dispatch or reusable workflows |

---

## Conditionals

Run or skip steps and jobs based on conditions.

```yaml
steps:
  - name: Only on main
    if: github.ref == 'refs/heads/main'
    run: ./deploy.sh

  - name: Only on PRs
    if: github.event_name == 'pull_request'
    run: ./preview-deploy.sh

  - name: Only if previous step succeeded
    if: success()
    run: echo "all good"

  - name: Always run this, even if something failed
    if: always()
    run: ./cleanup.sh

  - name: Only if something failed
    if: failure()
    run: ./notify-slack.sh
```

Status functions:

| Function | When it's true |
|---|---|
| `success()` | All previous steps succeeded |
| `failure()` | Any previous step failed |
| `cancelled()` | The workflow was cancelled |
| `always()` | No matter what happened |

You can use the same `if:` on jobs too:

```yaml
jobs:
  notify:
    needs: deploy
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - run: ./send-alert.sh
```

---

## Matrix Builds

Run the same job multiple times with different values. The most common use is testing across multiple language versions or operating systems.

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [18, 20, 22]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - run: npm test
```

This creates 9 jobs (3 OSes x 3 Node versions), all running in parallel.

**Excluding combinations:**

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node-version: [18, 20]
    exclude:
      - os: windows-latest
        node-version: 18    # skip this specific combination
```

**Including extra combinations:**

```yaml
strategy:
  matrix:
    node-version: [18, 20]
    include:
      - node-version: 20
        experimental: true    # adds an extra variable for this entry only
```

**Controlling failure behavior:**

```yaml
strategy:
  fail-fast: false    # don't cancel all jobs if one fails
  matrix:
    node-version: [18, 20, 22]
```

By default, if one matrix job fails, GitHub cancels the rest. `fail-fast: false` lets them all finish.

---

## Artifacts

Artifacts let you save files from a job and download them later, either manually or in another job.

**Uploading:**

```yaml
- name: Build
  run: npm run build

- name: Upload build output
  uses: actions/upload-artifact@v4
  with:
    name: build-files
    path: dist/
    retention-days: 7    # how long to keep it (default 90)
```

**Downloading in another job:**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-files
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-files
          path: dist/
      - run: ./deploy.sh dist/
```

You can also download artifacts manually from the Actions tab in your repo.

---

## Caching Dependencies

Caching saves time by reusing files from previous runs instead of re-downloading them every time.

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

How it works:

```
First run  → no cache found → install deps → save cache with key
Next run   → cache found, key matches → restore it → skip install
Lock file changes → key doesn't match → install fresh → save new cache
```

The `restore-keys` is a fallback. If the exact key isn't found, it looks for any cache starting with that prefix. Better than nothing.

Many setup actions have built-in caching you can enable with a flag:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'          # handles caching automatically
```

Same option exists for `setup-python` (with `pip`), `setup-java`, and others. Use that when it's available, it's simpler.

---

## Reusable Workflows

If you find yourself copy-pasting the same workflow across multiple repos, reusable workflows solve that. You define a workflow once and call it from others.

**The reusable workflow (in any repo):**

```yaml
# .github/workflows/deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh ${{ inputs.environment }}
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

**Calling it from another workflow:**

```yaml
# .github/workflows/production.yml
name: Production Deploy

on:
  push:
    branches: [main]

jobs:
  call-deploy:
    uses: your-org/your-repo/.github/workflows/deploy.yml@main
    with:
      environment: production
    secrets:
      DEPLOY_KEY: ${{ secrets.PROD_DEPLOY_KEY }}
```

Reusable workflows can be in the same repo or a different one. If they're in a different repo, that repo needs to be public or the calling repo needs access.

---

## Custom Actions

When no existing action does exactly what you need, you write your own. Three types: composite, JavaScript, and Docker.

### Composite Actions

The simplest kind. Just a sequence of steps packaged into a reusable action. Good for wrapping a few shell commands you use everywhere.

Create `action.yml` in a folder (or the root of a repo):

```yaml
name: 'Setup and Test'
description: 'Installs dependencies and runs tests'

inputs:
  node-version:
    description: 'Node.js version to use'
    required: false
    default: '20'

outputs:
  test-result:
    description: 'Whether tests passed'
    value: ${{ steps.run-tests.outputs.result }}

runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}

    - name: Install
      shell: bash
      run: npm ci

    - name: Test
      id: run-tests
      shell: bash
      run: |
        npm test
        echo "result=passed" >> $GITHUB_OUTPUT
```

Use it in a workflow:

```yaml
- uses: your-org/your-repo/path/to/action@v1
  with:
    node-version: '22'
```

### JavaScript Actions

More powerful than composite. Full access to the GitHub Actions toolkit. Good when you need to do something complex with the GitHub API or process data between steps.

Structure:

```
my-action/
├── action.yml
├── index.js
└── node_modules/    ← must be committed or bundled
```

```yaml
# action.yml
name: 'My JS Action'
description: 'Does something useful'

inputs:
  who-to-greet:
    description: 'Who to greet'
    required: true

outputs:
  random-number:
    description: 'A random number'

runs:
  using: 'node20'
  main: 'index.js'
```

```javascript
// index.js
const core = require('@actions/core');
const github = require('@actions/github');

try {
  const name = core.getInput('who-to-greet');
  console.log(`Hello, ${name}`);

  const randomNumber = Math.floor(Math.random() * 100);
  core.setOutput('random-number', randomNumber.toString());
} catch (error) {
  core.setFailed(error.message);
}
```

### Docker Actions

Run your action inside a Docker container. Useful when your action depends on specific tools or a specific OS environment.

```yaml
# action.yml
name: 'My Docker Action'
description: 'Runs in a container'

inputs:
  input-value:
    required: true

runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.input-value }}
```

```dockerfile
# Dockerfile
FROM alpine:3.19
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

Docker actions are slower to start than JS or composite actions because the container has to build or pull first.

---

## Permissions

By default, the `GITHUB_TOKEN` has read access to most things and write access to the contents of the repo. You can tighten this.

```yaml
permissions:
  contents: read       # read repo contents
  issues: write        # can create/edit issues
  pull-requests: write # can comment on PRs
  packages: write      # can push to GitHub Packages
```

Set it at the workflow level to apply to all jobs, or at the job level for finer control.

```yaml
jobs:
  deploy:
    permissions:
      contents: write      # this job needs to push
      id-token: write      # needed for OIDC auth with cloud providers
```

Available permission scopes:

| Scope | What it controls |
|---|---|
| `actions` | Manage workflow runs |
| `checks` | Create check runs |
| `contents` | Read/write repo contents |
| `deployments` | Manage deployments |
| `id-token` | Request OIDC tokens |
| `issues` | Read/write issues |
| `packages` | Push/pull packages |
| `pull-requests` | Read/write PRs |
| `security-events` | Upload SARIF results |
| `statuses` | Set commit statuses |

> 💡 For security, always use the minimum permissions your workflow actually needs. `read-all` or `write-all` is convenient but gives any compromised action in your workflow a lot of access.

---

## Self-Hosted Runners

GitHub's hosted runners cover most use cases, but sometimes you need your own machine. Common reasons: you need specific hardware, you need to access resources on a private network, or you're hitting the free tier limits.

**Adding a self-hosted runner:**

```
Repo → Settings → Actions → Runners → New self-hosted runner
```

Follow the instructions to install and register the runner agent on your machine. Then use it in your workflow:

```yaml
jobs:
  build:
    runs-on: self-hosted        # use any self-hosted runner

  deploy:
    runs-on: [self-hosted, linux, gpu]   # use a runner with specific labels
```

A few things to keep in mind if you go this route:

Self-hosted runners on public repos are a security risk. Any PR could run code on your machine. Only use them on private repos or repos where you fully control who can open PRs.

The runner agent needs to stay running. You'll probably want to run it as a service.

Runners don't get cleaned up automatically between jobs the way GitHub-hosted ones do. If you share state between jobs unintentionally, things get messy fast.

---

## Debugging and Troubleshooting

**Enable debug logging:**

Add these as secrets in your repo (not environment variables, they need to be secrets):

```
ACTIONS_RUNNER_DEBUG = true
ACTIONS_STEP_DEBUG = true
```

Re-run the failed workflow and you'll get verbose output.

**Print context to understand what's available:**

```yaml
- name: Dump context
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
```

**Set outputs from a step:**

```yaml
- name: Get version
  id: get-version
  run: echo "version=$(cat VERSION)" >> $GITHUB_OUTPUT

- name: Use version
  run: echo "Building ${{ steps.get-version.outputs.version }}"
```

**Common errors:**

```
Error: Resource not accessible by integration
→ Your GITHUB_TOKEN doesn't have the right permissions. Add a permissions: block.

Error: Process completed with exit code 1
→ A command failed. Look at the step output for the actual error.

Warning: No such file or directory
→ Check your working-directory setting and that previous steps ran successfully.

Error: Input required and not supplied
→ A required input for an action wasn't provided. Check the action's documentation.
```

**Re-running jobs:**

You can re-run a specific failed job without re-running the whole workflow from the Actions tab. Useful when a job fails due to a flaky test or a network timeout.

---

## Pricing and Limits

**Free tier (public repos):**

Everything is free on public repos. Unlimited minutes, unlimited storage for artifacts and caches.

**Free tier (private repos):**

| Plan | Minutes/month | Storage |
|---|---|---|
| Free | 2,000 | 500 MB |
| Pro | 3,000 | 1 GB |
| Team | 3,000 | 2 GB |
| Enterprise | 50,000 | 50 GB |

Minutes are multiplied based on runner type:

| Runner | Multiplier |
|---|---|
| Linux | 1x |
| Windows | 2x |
| macOS | 10x |

So 1 minute on macOS uses 10 minutes of your allowance. If you're running into limits, move things to Linux where possible.

**Other limits:**

```
Workflow run time:       6 hours maximum
Job run time:            6 hours maximum
Jobs per workflow:       255
Steps per job:           no hard limit (practical limit around 256)
Artifacts retention:     90 days (configurable down to 1)
Cache storage:           10 GB per repo (oldest evicted first)
Concurrent jobs:         varies by plan (20 for free, up to 500 for enterprise)
```

---

## Resources

<div align="center">

| Resource | What It Gets You |
|---|---|
| [GitHub Actions Docs](https://docs.github.com/en/actions) | The official reference, actually pretty good |
| [Workflow Syntax Reference](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) | Every single YAML key explained |
| [GitHub Marketplace - Actions](https://github.com/marketplace?type=actions) | Thousands of community actions |
| [actions/starter-workflows](https://github.com/actions/starter-workflows) | Official templates for common languages and tools |
| [act](https://github.com/nektos/act) | Run your workflows locally before pushing |
| [actionlint](https://github.com/rhysd/actionlint) | Static analysis for workflow files, catches mistakes before they run |
| [GitHub Actions Hero](https://github-actions-hero.vercel.app/) | Interactive playground for learning the syntax |
| [Awesome Actions](https://github.com/sdras/awesome-actions) | Curated list of useful community actions |
| [GitHub Security Lab - Actions](https://securitylab.github.com/research/github-actions-preventing-pwn-requests/) | How to avoid common Actions security pitfalls |

</div>

---

## License

MIT - fork it, adapt it, translate it, share it freely.

<div align="center">

[![](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=Automate+the+boring+stuff.&fontSize=28&fontColor=FCA5A5&fontAlignY=65)](https://github.com/Vendetaaaa/Githipedia)

</div>

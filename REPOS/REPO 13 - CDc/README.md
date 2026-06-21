<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=250&color=B91C1C&text=Codespaces%20and%20Devcontainers&fontColor=FCA5A5&fontSize=50&section=header" width="100%" />

![Setup Time](https://img.shields.io/badge/Setup%20Time-30%20min-B91C1C?style=for-the-badge&labelColor=1a1a1a)
![Level](https://img.shields.io/badge/Level-Beginner%20to%20Pro-7F1D1D?style=for-the-badge&labelColor=1a1a1a)

</div>

---

## What Is This?

Every contributor who opens your repo has to set up their machine before they can write a single line of code. Install the right Node version. Install the right Python version. Install some database. Set an environment variable nobody documented. Most people give up halfway through.

A devcontainer fixes this. It is a small config file that tells GitHub Codespaces, or VS Code, exactly what tools, extensions, and settings your project needs. The contributor clicks one button, waits a minute or two, and lands in a fully working environment. Same one every time. No setup guide needed.

This guide walks through what Codespaces and devcontainers actually are, how to write `devcontainer.json` from scratch, and how to make the one click experience feel polished.

---

## Table of Contents

- [Concepts You Need to Know First](#concepts-you-need-to-know-first)
  * [What is GitHub Codespaces](#what-is-github-codespaces)
  * [What is a Devcontainer](#what-is-a-devcontainer)
  * [How They Work Together](#how-they-work-together)
- [The Anatomy of devcontainer.json](#the-anatomy-of-devcontainerjson)
  * [Quick Overview](#quick-overview)
  * [Minimal Working Example](#minimal-working-example)
  * [Picking a Base Image](#picking-a-base-image)
  * [Features, the Easy Add-ons](#features-the-easy-add-ons)
  * [Forwarding Ports](#forwarding-ports)
  * [Lifecycle Commands](#lifecycle-commands)
  * [Editor Settings and Extensions](#editor-settings-and-extensions)
  * [Environment Variables and Secrets](#environment-variables-and-secrets)
- [Full Real World Examples](#full-real-world-examples)
  * [Node and React Project](#node-and-react-project)
  * [Python and Django Project](#python-and-django-project)
  * [Full Stack with a Database](#full-stack-with-a-database)
- [The One Click Badge](#the-one-click-badge)
- [Testing Your Setup Before Anyone Else Sees It](#testing-your-setup-before-anyone-else-sees-it)
- [Mistakes That Break the One Click Experience](#mistakes-that-break-the-one-click-experience)
- [The 30 Minute Setup Checklist](#the-30-minute-setup-checklist)
- [License](#license)

---

## Concepts You Need to Know First

Before touching any config file, lets get the basic words straight. Everything below builds on these three ideas.

### What is GitHub Codespaces

**Codespaces** is a cloud computer that GitHub spins up for you, with VS Code already running inside your browser or desktop app. You do not install anything locally. You click a button on a repo, and a few seconds or minutes later you have a terminal, a file editor, and a running project, all inside that cloud machine.

```
Normal way:
  clone repo -> install Node -> install the right version ->
  install dependencies -> set env vars -> hope it works

Codespaces way:
  click "Code" -> click "Create codespace" -> wait -> done
```

Think of it as borrowing a fully built laptop for a few hours, instead of building your own from parts every time.

### What is a Devcontainer

A **devcontainer** is the recipe for that cloud computer. It is a folder named `.devcontainer` sitting in your repo, holding a file called `devcontainer.json`. That file lists which programming languages to install, which VS Code extensions to add, which ports to open, and which commands to run after setup.

```
your-project/
├── .devcontainer/
│   └── devcontainer.json   <- the recipe
├── src/
├── package.json
└── README.md
```

Without this file, Codespaces still works, but it guesses a generic setup. With it, Codespaces builds exactly the environment your project needs, every single time, for every contributor.

### How They Work Together

```
You write devcontainer.json once
        |
        v
Contributor opens your repo on GitHub
        |
        v
Clicks "Create codespace on main"
        |
        v
GitHub reads devcontainer.json
        |
        v
Builds a container matching your recipe exactly
        |
        v
Contributor lands in a ready to code VS Code, in the browser
```

The same `devcontainer.json` file also works for local VS Code, through the Dev Containers extension. Write it once, and it powers both the cloud version and the local version.

---

## The Anatomy of devcontainer.json

### Quick Overview

| Field | What It Does | Required |
| --- | --- | --- |
| `name` | A friendly label shown in the Codespaces UI | No, but nice to have |
| `image` or `build` | The base container to start from | Yes, one of the two |
| `features` | Pre-made add-ons like Docker, AWS CLI, or extra languages | No |
| `forwardPorts` | Which ports get exposed so you can preview your app | No |
| `postCreateCommand` | Shell command that runs right after the container is built | No |
| `customizations` | VS Code settings and extensions to install automatically | No |
| `containerEnv` | Environment variables set inside the container | No |

> **Only `image` or `build` is truly required. Everything else is there to remove friction for whoever opens your repo next.**

### Minimal Working Example

This is the smallest devcontainer that actually does something useful:

```json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20"
}
```

Save that as `.devcontainer/devcontainer.json`, push it, and Codespaces already knows to give every contributor a Node 20 environment. That is the whole starting point. Everything past this is just adding convenience.

### Picking a Base Image

The base image is the operating system plus the language runtime that your container starts from. Microsoft maintains a large catalog of ready made ones, so you almost never need to build your own from scratch.

```
mcr.microsoft.com/devcontainers/javascript-node:20   -> Node.js 20
mcr.microsoft.com/devcontainers/python:3.12           -> Python 3.12
mcr.microsoft.com/devcontainers/go:1.22                -> Go 1.22
mcr.microsoft.com/devcontainers/java:17                -> Java 17
mcr.microsoft.com/devcontainers/universal:2             -> a bit of everything, heavier
```

| Approach | When To Use It |
| --- | --- |
| `image` with a premade tag | Your project uses one main language, this is the simplest path |
| `dockerFile` pointing to your own Dockerfile | You already maintain a Dockerfile and want full control |
| `dockerComposeFile` | Your project needs multiple containers, like an app plus a database |

For most repos, a premade image is enough. Save the custom Dockerfile route for when you genuinely need it.

### Features, the Easy Add-ons

**Features** are small, reusable installers you can bolt onto any base image, without writing any installation script yourself.

```json
{
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/aws-cli:1": {}
  }
}
```

Each entry in `features` adds one tool to the container. Want Docker available inside your codespace, plus the GitHub CLI, plus the AWS CLI. Three lines, no manual setup scripts, no figuring out install commands for a container you have never touched.

Browse the full list at [containers.dev/features](https://containers.dev/features) before writing a custom install step yourself. There is a very good chance someone already made the feature you need.

### Forwarding Ports

If your project runs a web server, Codespaces needs to know which port to expose so you, or the contributor, can actually open the running app in a browser tab.

```json
{
  "forwardPorts": [3000, 5432],
  "portsAttributes": {
    "3000": {
      "label": "Frontend",
      "onAutoForward": "openBrowser"
    },
    "5432": {
      "label": "Database",
      "onAutoForward": "silent"
    }
  }
}
```

`onAutoForward` controls what happens the moment that port becomes active. `openBrowser` pops a browser tab automatically. `silent` just forwards it quietly in the background, which is usually what you want for a database port.

### Lifecycle Commands

These are shell commands that run automatically at specific moments while the container is being built or started. They remove the need for a setup guide entirely.

```
onCreateCommand     -> runs once, when the container is first created
updateContentCommand -> runs when the container is created or rebuilt
postCreateCommand   -> runs once, right after the container is fully created
postStartCommand    -> runs every single time the container starts
postAttachCommand   -> runs every time a tool, like VS Code, attaches to it
```

```json
{
  "postCreateCommand": "npm install",
  "postStartCommand": "echo Welcome back to the project"
}
```

`postCreateCommand` is the one you will use the most. It is the perfect spot for `npm install`, `pip install -r requirements.txt`, database migrations, or anything else a contributor would normally have to remember to run by hand.

### Editor Settings and Extensions

This is where you make sure every contributor gets the same VS Code setup as you, down to the extensions and formatting rules.

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-python.python"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.tabSize": 2
      }
    }
  }
}
```

No more "wait, you don't have ESLint installed?" The extensions install themselves the moment the codespace opens. The settings apply automatically too, so formatting stays consistent across the whole team.

### Environment Variables and Secrets

Some projects need an API key or a database URL to actually run. Never put real secrets directly inside `devcontainer.json`, since that file gets committed to your repo and anyone can read it.

```json
{
  "containerEnv": {
    "NODE_ENV": "development"
  }
}
```

For anything sensitive, like API keys, use **Codespaces secrets** instead, set under your repository or organization settings on GitHub. Those get injected into the container at runtime, and never touch your committed files.

```
Repo settings -> Secrets and variables -> Codespaces -> New repository secret
```

> **Rule of thumb: plain config values go in devcontainer.json. Anything you would not want a stranger reading goes in Codespaces secrets.**

---

## Full Real World Examples

### Node and React Project

```json
{
  "name": "React App",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "forwardPorts": [3000],
  "postCreateCommand": "npm install",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ]
    }
  }
}
```

A contributor opens this repo, clicks one button, and within a minute has Node installed, dependencies already pulled in, ESLint and Prettier ready to go, and port 3000 ready to preview the running app.

### Python and Django Project

```json
{
  "name": "Django App",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "forwardPorts": [8000],
  "postCreateCommand": "pip install -r requirements.txt && python manage.py migrate",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  }
}
```

This one installs every Python dependency and runs your database migrations automatically, before the contributor even sees a terminal prompt.

### Full Stack with a Database

For projects needing more than one container, like an app plus a Postgres database, `dockerComposeFile` is the right tool.

```
.devcontainer/
├── devcontainer.json
└── docker-compose.yml
```

```json
{
  "name": "Full Stack App",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "forwardPorts": [3000, 5432],
  "postCreateCommand": "npm install"
}
```

```yaml
services:
  app:
    build: .
    volumes:
      - ..:/workspace:cached
    command: sleep infinity

  db:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD: devpassword
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

The `app` service is your actual coding environment. The `db` service runs alongside it automatically, fully networked together, no manual setup needed by the contributor at all.

---

## The One Click Badge

Drop this badge into your README so contributors see a literal one click button to launch a codespace, instead of having to dig through the green "Code" button menu themselves.

```
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/YOUR-USERNAME/YOUR-REPO)
```

Replace `YOUR-USERNAME/YOUR-REPO` with your actual repository path. The result looks like this:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/vscode)

You can also point the badge at a specific branch, or pass extra parameters, by appending them after a question mark:

```
https://codespaces.new/YOUR-USERNAME/YOUR-REPO?quickstart=1
```

> **Put this badge near the very top of your README. It is often the difference between someone trying your project right now, and someone closing the tab.**

---

## Testing Your Setup Before Anyone Else Sees It

Never assume your `devcontainer.json` works just because it looks correct. Always test the actual experience yourself first.

```
Step 1 -> Push your .devcontainer folder to your repo
Step 2 -> Open the repo on github.com
Step 3 -> Click the green "Code" button
Step 4 -> Click "Codespaces" tab, then "Create codespace on main"
Step 5 -> Wait for the build, watch the logs for any errors
Step 6 -> Once it opens, try running your project like a brand new contributor would
```

If you have VS Code installed locally, you can also test it without ever touching GitHub, using the **Dev Containers** extension. Open your project folder, run the command "Reopen in Container," and VS Code builds the exact same environment, locally.

> **If something fails inside the container build logs, fix it before telling anyone to try your repo. A broken one click experience is worse than no devcontainer at all.**

---

## Mistakes That Break the One Click Experience

| Mistake | Why It Hurts | The Fix |
| --- | --- | --- |
| Putting `devcontainer.json` in the wrong folder | Codespaces never finds it, falls back to a generic setup | Keep it inside a folder named exactly `.devcontainer` |
| Forgetting `postCreateCommand` | Contributor lands in an empty environment with no dependencies installed | Add the install command for your specific language |
| Hardcoding real API keys in the file | Secrets get committed to git history for anyone to see | Use Codespaces secrets in repository settings instead |
| Picking a huge universal image when you only need one language | Slower build times for everyone | Pick the smallest image that fits your actual stack |
| Never testing the build yourself | Contributors hit errors you never caught | Always build and open it yourself before sharing the repo |
| No forwarded ports on a web project | Contributor cannot preview the running app at all | Add `forwardPorts` for every port your app actually uses |
| Listing extensions nobody on the team uses | Bloats the container, slows down startup | Only include extensions the project genuinely needs |

---

## The 30 Minute Setup Checklist

Do this in one sitting, right after reading this guide.

```
THE BASICS  (do these first, they matter most)
──────────────────────────────────────────────────────────
[ ]  Create a folder named exactly .devcontainer in your repo root
[ ]  Add a devcontainer.json file inside it
[ ]  Pick a base image that matches your main language
[ ]  Add a postCreateCommand that installs your dependencies
[ ]  Add forwardPorts for any web server your project runs

THE POLISH  (adds convenience and saves contributors time)
──────────────────────────────────────────────────────────
[ ]  Add your team's must have VS Code extensions
[ ]  Add shared editor settings, like formatOnSave
[ ]  Move any real secrets into Codespaces secrets, never the file
[ ]  Add any useful features, like docker-in-docker or github-cli
[ ]  Push everything, then test it yourself in a fresh codespace
[ ]  Add the one click "Open in GitHub Codespaces" badge to your README
[ ]  Ask someone else to try it, and watch where they get stuck
```

---

## License

[#license](#license)

MIT, fork it, adapt it, share it freely.

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=7F1D1D&height=120&section=footer&fontColor=FCA5A5" width="100%" />

</div>

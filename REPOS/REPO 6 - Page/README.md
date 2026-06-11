<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=250&color=B91C1C&text=GitHub%20Pages%20Mastery&section=header&fontColor=FCA5A5&fontAlignY=34&desc=Turn%20Any%20Repo%20Into%20a%20Live%20Website.%20For%20Free.&fontSize=40&descSize=18&descAlignY=58&descColor=FCA5A5" width="100%" />

[![Setup Time](https://img.shields.io/badge/⏱_~1_Hour_Setup-B91C1C?style=for-the-badge&labelColor=1a1a1a)](.)
[![Level](https://img.shields.io/badge/🚀_Beginner_to_Pro-7F1D1D?style=for-the-badge&labelColor=1a1a1a)](.)
[![Free](https://img.shields.io/badge/💸_Completely_Free-B91C1C?style=for-the-badge&labelColor=1a1a1a)](.)

</div>

---

## Table of Contents

- [What is GitHub Pages?](#what-is-github-pages)
- [The 3 Types of Pages Sites](#the-3-types-of-pages-sites)
  * [User / Organization Site](#-user--organization-site)
  * [Project Site](#-project-site)
  * [Custom Domain Site](#-custom-domain-site)
- [Enabling GitHub Pages](#enabling-github-pages)
- [Your First Page - In 5 Minutes](#your-first-page--in-5-minutes)
- [Jekyll - The Built-In Site Generator](#jekyll--the-built-in-site-generator)
  * [What Jekyll Does](#what-jekyll-does)
  * [Built-in Themes](#built-in-themes)
  * [Front Matter](#front-matter)
- [Going Beyond Jekyll](#going-beyond-jekyll)
  * [React, Vue, and Static Frameworks](#react-vue-and-static-frameworks)
  * [Deploying with GitHub Actions](#deploying-with-github-actions)
- [Custom Domains](#custom-domains)
  * [Connecting Your Domain](#connecting-your-domain)
  * [Enforcing HTTPS](#enforcing-https)
- [The CNAME File](#the-cname-file)
- [License](#license)

---

## What is GitHub Pages?

GitHub Pages is a **free static hosting service** built directly into GitHub. You push files to a repository - HTML, CSS, JavaScript, Markdown - and GitHub publishes them as a live website at a public URL.

No server. No hosting bill. No deployment pipeline to configure. Just a repo and a branch.

> *If you have a GitHub repo, you are one settings toggle away from a live website.*

---

## The 3 Types of Pages Sites

### 👤 User / Organization Site

One special site tied to your GitHub account. It lives at `https://username.github.io` and is built from a repo named **exactly** `username.github.io`.

```
Repo name  →  username.github.io   (must match exactly)
URL        →  https://username.github.io
Branch     →  main  (default)
Limit      →  one per account
```

This is your **personal homepage** - portfolio, bio, dev blog, or landing page. It's the most visible Pages site you can own.

---

### 📁 Project Site

Every public repository can have its own Pages site - unlimited. They sit under a `/project-name` path on your user domain.

```
Repo name  →  any-project-name
URL        →  https://username.github.io/any-project-name
Branch     →  main, docs/, or gh-pages  (your choice)
Limit      →  one per repo, unlimited repos
```

Project sites are ideal for: documentation, demo pages, changelogs, and landing pages for your tools.

---

### 🌐 Custom Domain Site

Any Pages site - user or project - can be served from a domain you own instead of the default `github.io` URL.

```
Default  →  https://username.github.io
Custom   →  https://yourname.dev  (or any domain you own)
```

Both URLs remain active after the switch. GitHub handles the routing. See the [Custom Domains](#custom-domains) section for setup.

---

## Enabling GitHub Pages

```
Repository → Settings → Pages (left sidebar)

Source:
  - Deploy from a branch
      Branch: main    Folder: / (root)

  - GitHub Actions  (for custom build pipelines)

→ Click Save
→ Wait ~60 seconds
→ Your URL appears at the top of the Pages settings panel
```

> **Visibility note:** GitHub Pages is public by default for free accounts, even if the source repository is private. GitHub Pro, Team, and Enterprise plans can publish private repos to Pages privately.

---

## Your First Page - In 5 Minutes

No frameworks. No dependencies. Just a file.

**Step 1** - Create `index.html` in your repo root:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>My GitHub Page</title>
  <style>
    body { font-family: sans-serif; max-width: 700px; margin: 80px auto; padding: 0 20px; }
    h1   { color: #B91C1C; }
  </style>
</head>
<body>
  <h1>Hello from GitHub Pages 👋</h1>
  <p>This page is live at username.github.io</p>
</body>
</html>
```

**Step 2** - Commit and push to main.

**Step 3** - Enable Pages in Settings → Pages → Branch: main → Save.

That's it. Your site is live.

> **Markdown shortcut:** If you don't want to write HTML at all, create a `README.md` instead. GitHub Pages + Jekyll will automatically render it as a page.

---

## Jekyll - The Built-In Site Generator

Jekyll transforms Markdown and Liquid templates into a full HTML site. GitHub Pages runs it automatically - you never install or invoke it yourself.

### What Jekyll Does

```
Your files                Jekyll output
─────────────────         ─────────────────────────
index.md          →       index.html
_posts/           →       /2026/01/01/post-title/
_layouts/         →       applied to all pages
_includes/        →       reusable HTML partials
_config.yml       →       site-wide settings
```

### Built-in Themes

Skip all CSS and layout work by picking a supported theme in `_config.yml`:

```yaml
# _config.yml
theme: minima          # clean, minimal - the default
title: "My Site"
description: "A GitHub Pages site"
```

Supported themes include: `minima` · `cayman` · `slate` · `architect` · `tactile` · `midnight` · `hacker`

Browse them all at [pages.github.com/themes](https://pages.github.com/themes).

### Front Matter

Every Markdown file processed by Jekyll can have a **front matter block** - a YAML header between `---` lines that controls layout, title, and metadata.

```yaml
---
layout: post
title:  "My First Post"
date:   2026-01-15
---

Your page content starts here in Markdown.
```

Without front matter, Jekyll treats the file as a plain page with the default layout. With it, you get full control.

---

## Going Beyond Jekyll

### React, Vue, and Static Frameworks

Jekyll is optional. You can use any static site generator - Vite, Next.js (static export), Astro, Hugo - and deploy the built output to Pages.

```
Framework workflow:
  code (src/) → build → output (dist/ or out/) → deploy to Pages
```

The key: your Pages source must point to the **built output folder**, not your source files.

```
# For Vite / most frameworks
Source branch: gh-pages
Or: GitHub Actions deploying dist/ to gh-pages
```

### Deploying with GitHub Actions

For any framework that requires a build step, use a workflow:

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install & Build
        run: |
          npm ci
          npm run build

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

> This is the standard pattern for React, Vue, Astro, and any framework with a build step. Adjust `publish_dir` to wherever your framework outputs its built files.

---

## Custom Domains

### Connecting Your Domain

**Step 1** - Add a CNAME record at your DNS provider:

```
Type   Host          Value
─────────────────────────────────────
CNAME  www           username.github.io
```

For an apex domain (no `www`), add four A records instead:

```
Type   Host   Value
────────────────────────────
A      @      185.199.108.153
A      @      185.199.109.153
A      @      185.199.110.153
A      @      185.199.111.153
```

**Step 2** - Enter your domain in repository Settings → Pages → Custom domain → Save.

**Step 3** - Wait for DNS to propagate (anywhere from 1 minute to 48 hours depending on your provider).

### Enforcing HTTPS

```
Settings → Pages → Enforce HTTPS
```

GitHub provisions a free TLS certificate via Let's Encrypt automatically. The "Enforce HTTPS" checkbox only becomes available once DNS is verified - enable it as soon as it appears.

---

## The CNAME File

When you set a custom domain in Settings, GitHub automatically creates a file called `CNAME` in your repo root containing your domain name.

```
# CNAME file content (single line, no extras)
yoursite.dev
```

**Important:** if you ever delete this file, GitHub will remove your custom domain setting. Commit it into your repo and don't touch it.

If you're deploying via GitHub Actions, make sure your workflow copies the CNAME file into the published folder - otherwise it will be overwritten on each deploy:

```yaml
- name: Deploy
  uses: peaceiris/actions-gh-pages@v4
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./dist
    cname: yoursite.dev    # ← keeps the CNAME file intact
```

---

## License

MIT License - fork it, adapt it, translate it, share it freely.

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=7F1D1D&height=160&section=footer&text=Ship.%20Polish.%20Repeat.&fontSize=28&fontColor=FCA5A5&fontAlignY=65" width="100%" />

</div>

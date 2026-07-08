<div align="center">

![](https://capsule-render.vercel.app/api?type=blur&height=260&color=B91C1C&text=Building%20Your%20Info%20Hub&section=header&fontColor=FCA5A5&fontAlign=34&desc=Turning%20your%20org%20into%20a%20place%20people%20actually%20visit&descAlign=55&descSize=18)

[![Docs & Community](https://img.shields.io/badge/Docs_%26_Community-B91C1C?style=flat-square)](#) [![Last Updated](https://img.shields.io/badge/Last%20Updated-2026-B91C1C?style=flat-square)](#)

</div>

*Most orgs are just a pile of repos. Here's how to make yours a place people go to find answers.*

---

## Table of Contents

- [Why Bother With This?](#why-bother-with-this)
- [The Organization Profile README](#the-organization-profile-readme)
- [The .github Repository](#the-github-repository)
- [Using Discussions as a Knowledge Base](#using-discussions-as-a-knowledge-base)
- [Wikis vs Repos for Documentation](#wikis-vs-repos-for-documentation)
- [Pinned Repositories](#pinned-repositories)
- [Organization-Wide Issue and PR Templates](#organization-wide-issue-and-pr-templates)
- [Obscure but Useful Facts](#obscure-but-useful-facts)
- [Resources & Further Reading](#resources--further-reading)
- [License](#license)

---

## Why Bother With This?

An org with fifteen repos and no clear starting point makes people guess. New members poke around trying to figure out which repo is the "real" one, contributors don't know where to ask questions, and basic information ends up repeated in five different Slack channels because nobody could find where it was written down.

A little structure fixes almost all of that, and GitHub gives you more free tools for it than most people realize.

---

## The Organization Profile README

Every organization can have a special README that shows up right on its main page, above the list of repos. This is the first thing anyone sees when they land on your org, so it's worth treating like a homepage.

**1.** Create a new **public** repository inside your org, named exactly `.github` (yes, with the dot).

**2.** Inside it, create a `profile` folder.

**3.** Inside that folder, add a `README.md` file.

```
.github/
  profile/
    README.md   ← this is what shows on your org's homepage
```

**4.** Write it like an actual landing page: what the org does, links to the most important repos, how to get in touch, how to contribute if you're open-source.

> 💡 **Tip:** Keep it short and link out rather than trying to cram everything in. This README is a front door, not the whole house.

---

## The .github Repository

That same `.github` repo does more than hold your profile page. Anything you put at its root acts as an org-wide default that applies to every other repo that doesn't have its own version of the same file:

```
.github/
  profile/README.md          → your org's homepage
  CONTRIBUTING.md            → default contributing guide for all repos
  CODE_OF_CONDUCT.md         → default code of conduct for all repos
  ISSUE_TEMPLATE/            → default issue templates for all repos
  PULL_REQUEST_TEMPLATE.md   → default PR template for all repos
```

If an individual repo has its own `CONTRIBUTING.md`, that one wins for that specific repo. The org-wide version is just a fallback, which is exactly what you want, since it means new repos are covered automatically without anyone remembering to copy files around.

---

## Using Discussions as a Knowledge Base

GitHub Discussions is a forum-style feature you can enable per repo, but a lot of orgs use it differently: as a central place for questions, announcements, and decisions that don't belong in an issue tracker.

**1.** Pick (or create) one repo to act as the "hub" repo, could be your `.github` repo or a dedicated one like `community`.

**2.** Go to that repo's Settings and enable Discussions under the Features section.

**3.** Set up categories that match how your org actually communicates, common ones being **Announcements**, **Q&A**, **Ideas**, and **Show and tell**.

**4.** Pin the most useful threads, like an onboarding FAQ, so they stay at the top instead of getting buried.

Unlike issues, discussions don't need to resolve into a code change, which makes them a better fit for general questions and ongoing conversation.

---

## Wikis vs Repos for Documentation

GitHub gives every repo an optional wiki, but it's worth knowing when to use one versus just keeping docs as markdown files in the repo itself:

| | Wiki | Docs in the Repo |
| --- | --- | --- |
| Version controlled | Yes, but as its own separate git history | Yes, same history as the code |
| Reviewable via pull request | No, edits go live immediately | Yes, can require review like any other change |
| Good for | Loosely structured notes, FAQs edited by many people | Anything that should stay in sync with a specific code version |
| Discoverable in search | Weaker, wikis are indexed separately | Strong, shows up in normal repo search |

Most technical orgs are better off keeping documentation as markdown files inside a `docs/` folder in the actual repo, since it can be reviewed and stays version-locked to the code it describes. Wikis tend to work better for informal, frequently-edited pages like meeting notes or onboarding checklists where a PR review would just slow things down.

---

## Pinned Repositories

Your org page can pin up to six repos to the top, above the full list. This is one of the simplest, most overlooked ways to point people at what matters.

**1.** From your org's main page, look for **Customize pinned repositories**.

**2.** Choose the ones that matter most, usually your main product, your docs repo, and maybe a "start here" template repo.

**3.** Reorder them, the leftmost/topmost pin gets seen first.

If your org has forty repos and someone lands there for the first time, six pinned ones is the difference between "I have no idea where to start" and "oh, this is clearly the main thing."

---

## Organization-Wide Issue and PR Templates

Covered briefly above, but worth its own callout since it's easy to underuse. Templates placed in `.github/ISSUE_TEMPLATE/` at the org level apply automatically to any repo without its own templates.

A good starting set for most orgs:

```
.github/ISSUE_TEMPLATE/
  bug_report.md
  feature_request.md
  config.yml       ← controls template chooser behavior
```

The `config.yml` file lets you disable blank issues entirely, forcing people to pick a template, which keeps incoming issues far more consistent and easier to triage across every repo at once.

---

## Obscure but Useful Facts

* **The org profile README only shows to logged-out visitors if the org itself is public**, but organization members always see it regardless. If your profile page "isn't working," check the org's own visibility settings first.
* **The `.github` repo can itself be private**, but then its org-wide defaults (templates, contributing guide) only apply to other private repos in the org, not public ones. Public repos need the source repo to be public too for the fallback to apply.
* **Org-wide community health files don't override a repo that already has one, even an empty one.** An empty `CONTRIBUTING.md` in a repo will "win" over the org default and show nothing, which confuses people who assumed deleting the content would fall back automatically.
* **Discussions can be converted from issues and back isn't always clean.** Converting an issue into a discussion is one-way in most cases, so it's worth being deliberate about which repo has discussions enabled before people start filing things there.
* **Pinned repos are a personal, page-wide setting controlled by whoever has admin rights**, not something each visitor customizes. Everyone who lands on your org page sees the same six pins.
* **GitHub's org search indexing has a lag.** A new repo or a freshly written README might not show up in GitHub's search results immediately, so don't panic if something you just published seems to be "missing" for the first hour or so.

---

## Resources & Further Reading

| Resource | What It Gets You |
| --- | --- |
| [GitHub Docs — Organization Profile](https://docs.github.com/en/organizations) | Official steps for setting up your org's homepage |
| [GitHub Docs — About Discussions](https://docs.github.com/en/discussions) | Full reference on categories, moderation, and setup |
| [GitHub Docs — Creating a Default Community Health File](https://docs.github.com/en/communities) | How the `.github` repo fallback system actually works |
| [Shields.io](https://shields.io) | Build custom badges for your org's READMEs |
| [Capsule Render](https://github.com/kyechan99/capsule-render) | The header and footer banners used across this guide |

---

## License

MIT License, see [LICENSE](LICENSE) for full details. Fork it, adapt it, share it freely.

<div align="center">

![](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=That%27s%20the%20full%20set%2C%20for%20now.&fontSize=28&fontColor=FCA5A5&animation=fadeIn&fontAlignY=65)

</div>
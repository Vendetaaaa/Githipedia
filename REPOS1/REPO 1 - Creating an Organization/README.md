<div align="center">

![](https://capsule-render.vercel.app/api?type=blur&height=260&color=B91C1C&text=Creating%20an%20Organization&section=header&fontColor=FCA5A5&fontAlign=34&desc=Setting%20one%20up%20properly%2C%20the%20first%20time&descAlign=55&descSize=18)

[![Beginner Friendly](https://img.shields.io/badge/Beginner%20Friendly-B91C1C?style=flat-square)](#) [![Last Updated](https://img.shields.io/badge/Last%20Updated-2026-B91C1C?style=flat-square)](#)

</div>

*Everything to think about before, during, and right after you hit "Create organization."*

---

## Table of Contents

- [What Is an Organization, Actually?](#what-is-an-organization-actually)
- [Organization vs Personal Account](#organization-vs-personal-account)
- [Before You Create One](#before-you-create-one)
  * [Picking a Name](#picking-a-name)
  * [Picking a Plan](#picking-a-plan)
- [Step-by-Step: Creating the Organization](#step-by-step-creating-the-organization)
- [The First Week Checklist](#the-first-week-checklist)
- [Obscure but Useful Facts](#obscure-but-useful-facts)
- [Resources & Further Reading](#resources--further-reading)
- [License](#license)

---

## What Is an Organization, Actually?

A GitHub organization is a shared account that a group of people work out of together. Instead of a bunch of repos sitting under one person's username, they sit under a name that represents the team, company, or project. Nobody "owns" it the way a personal account is owned. Instead, people are added as members with different levels of access, and the organization keeps running even if the person who created it leaves.

Think of a personal account as your own desk, and an organization as the office building. Repos, teams, and permissions all live inside that building, and who gets which key is something you control from one place.

---

## Organization vs Personal Account

A lot of people start a project under their personal account and only move to an org once things get complicated. Here's the honest comparison:

| | Personal Account | Organization |
| --- | --- | --- |
| Who owns it | One person | Shared, with multiple owners possible |
| Repo ownership after you leave | Stays with you | Stays with the org |
| Team-based permissions | No, just collaborators | Yes, full team structure |
| SSO / SAML enforcement | Not available | Available on paid plans |
| Audit logs | Very limited | Full audit log |
| Billing | Personal | Centralized, one invoice |
| Good for | Solo projects, personal portfolios | Teams, companies, open-source projects with multiple maintainers |

If more than one person needs to be able to approve pull requests, manage settings, or the project needs to outlive any single contributor, it belongs in an org.

---

## Before You Create One

### Picking a Name

The org name becomes part of every URL under it, so it's worth a minute of thought:

* Keep it short. `github.com/your-really-long-company-name-inc` is painful to type and paste.
* Avoid trademarked names you don't have rights to. GitHub will take an org name down if there's a legitimate dispute.
* Check if the name is already taken as a personal username too, since org names and usernames share the same namespace.
* You can rename an org later, but old links (`github.com/oldname/repo`) will redirect only for a while, and some integrations break on rename. Get it right early if you can.

### Picking a Plan

GitHub offers a few org tiers, and the right one depends mostly on team size and whether you need advanced security controls:

| Plan | Roughly For | Notable Things You Get |
| --- | --- | --- |
| Free | Small teams, open-source | Unlimited public/private repos, basic team management |
| Team | Paid, growing teams | Draft PRs, required reviewers, scheduled reminders |
| Enterprise | Large companies | SAML SSO, audit log streaming, IP allow lists, advanced security |

You don't have to decide forever. Plans can be upgraded later without moving repos or losing history.

---

## Step-by-Step: Creating the Organization

**1.** Go to [github.com/account/organizations/new](https://github.com/account/organizations/new).

**2.** Pick a plan. Free is fine to start with, you can upgrade any time.

**3.** Enter the organization name, your contact email, and whether this belongs to a business or is for personal use. GitHub asks this mostly to route you to the right billing flow later.

**4.** GitHub will ask if you want to invite people right away. You can skip this and do it later, there's no rush.

**5.** Once it's created, you land on the org's dashboard. This is your control center from now on, accessible any time at:

```
github.com/orgs/YOUR-ORG-NAME/dashboard
```

**6.** Go to **Settings** and fill out the basics: profile picture, description, and location if relevant. This is the first thing anyone sees when they land on your org page.

> 💡 **Tip:** Use a square logo at least 200x200px for the org avatar. GitHub crops it into a rounded square across the site, so avoid designs with important details near the edges.

---

## The First Week Checklist

Once the org exists, a few things are worth doing before you start adding a lot of people or repos:

* **Set base permissions.** Under Settings → Member privileges, decide what a member can do by default (nothing, read, write, or admin on new repos). Most orgs should start this at "Read" or "No permission" and grant more per team.
* **Turn on two-factor authentication requirement.** Settings → Authentication security lets you require every member to have 2FA enabled. This alone prevents a huge share of account-compromise incidents.
* **Create your first team.** Even with three people, having a team called something like `core` makes it easier to manage permissions as a group instead of one by one.
* **Add a `.github` repository.** A special repo named exactly `.github` lets you set org-wide defaults like issue templates and a community health file that applies to every repo that doesn't have its own. Covered in more depth in the info hub guide.
* **Decide on repo visibility defaults.** Settings → Repository defaults controls whether new repos default to private or public. Get this right before someone accidentally creates a public repo with internal notes in it.

---

## Obscure but Useful Facts

A handful of things about org creation that don't come up until they matter:

* **You can convert a personal account into an org**, but not the other way around. If you started a project on a personal account and it's grown too big to manage alone, GitHub support can walk you through migrating it, though the personal account effectively becomes read-only under the new setup and you'll want a fresh personal account for yourself afterward.
* **An org can have zero repos and still be billed** if you have paid seats assigned. Seats are tied to members, not to repo count.
* **The person who creates the org isn't locked in as the sole owner.** Ownership can be fully transferred, and the creator can later be demoted to a regular member or removed entirely, as long as at least one other owner exists.
* **Org names are case-insensitive but case-preserving.** `github.com/MyOrg` and `github.com/myorg` point to the same place, but the org's display name keeps whatever casing you chose.
* **There's a soft limit on how many organizations a single user can create in a short period.** This exists to slow down spam and abuse, and it occasionally trips up legitimate users setting up several client orgs in one sitting. If you hit it, waiting a day usually clears it.
* **Verified domains aren't just a blue checkmark.** Once you verify a domain under Settings → Verified & approved domains, you can restrict organization membership visibility and even set default profile behavior for members with an email on that domain.

---

## Resources & Further Reading

| Resource | What It Gets You |
| --- | --- |
| [GitHub Docs — Creating a New Organization](https://docs.github.com/en/organizations) | The official step-by-step, kept current with UI changes |
| [GitHub Docs — Organization vs Personal Accounts](https://docs.github.com/en/get-started) | The reasoning behind account types, from GitHub itself |
| [GitHub Pricing](https://github.com/pricing) | Current plan breakdown and costs |
| [Shields.io](https://shields.io) | Build custom badges for your org's READMEs |
| [Capsule Render](https://github.com/kyechan99/capsule-render) | The header and footer banners used across this guide |

---

## License

MIT License, see [LICENSE](LICENSE) for full details. Fork it, adapt it, share it freely.

<div align="center">

![](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=Up%20next%3A%20maintaining%20it.&fontSize=28&fontColor=FCA5A5&animation=fadeIn&fontAlignY=65)

</div>
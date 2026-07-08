<div align="center">

![](https://capsule-render.vercel.app/api?type=blur&height=260&color=B91C1C&text=Maintaining%20and%20Managing&section=header&fontColor=FCA5A5&fontAlign=34&desc=Keeping%20an%20organization%20healthy%20long%20term&descAlign=55&descSize=18)

[![Ongoing](https://img.shields.io/badge/Ongoing%20Work-B91C1C?style=flat-square)](#) [![Last Updated](https://img.shields.io/badge/Last%20Updated-2026-B91C1C?style=flat-square)](#)

</div>

*Creating an org is the easy part. This is about not letting it turn into a mess six months later.*

---

## Table of Contents

- [Roles, Explained Properly](#roles-explained-properly)
- [Teams and Why You Should Use Them](#teams-and-why-you-should-use-them)
  * [Setting Up a Team Structure](#setting-up-a-team-structure)
  * [Nested Teams](#nested-teams)
- [Permissions Without the Headache](#permissions-without-the-headache)
- [Security Basics Every Org Needs](#security-basics-every-org-needs)
- [Billing and Seats](#billing-and-seats)
- [Offboarding People Properly](#offboarding-people-properly)
- [Obscure but Useful Facts](#obscure-but-useful-facts)
- [Resources & Further Reading](#resources--further-reading)
- [License](#license)

---

## Roles, Explained Properly

GitHub gives an organization a handful of roles, and mixing them up is one of the most common early mistakes:

| Role | Can Do | Typical Use |
| --- | --- | --- |
| **Owner** | Everything, including deleting the org | 1-3 trusted people, never more than needed |
| **Member** | Whatever their team permissions allow | Everyone else |
| **Billing manager** | Manage billing only, nothing else | Finance or ops people who don't touch code |
| **Moderator** (org-wide) | Block or unblock users, manage interaction limits | Community management on larger orgs |
| **Security manager** | View security alerts and settings across all repos, without full admin access | Security teams that shouldn't have owner rights |

The most common mistake is making everyone an owner "to keep things simple." Don't. Owners can delete the entire organization, remove other owners, and change billing. Keep that list as short as the org can reasonably function on.

> ⚠️ **Worth knowing:** if every owner leaves or is removed, GitHub has a recovery process, but it takes time and support involvement. Always keep at least two owners.

---

## Teams and Why You Should Use Them

Managing permissions repo by repo, person by person, works fine for three people. It falls apart at ten. Teams solve this by letting you grant access once, to a group, and add or remove people from that group instead of touching every repo.

### Setting Up a Team Structure

A reasonable starting structure for most orgs looks like this:

```
YOUR-ORG
├── core            → full write access to everything, small trusted group
├── engineering      → write access to code repos
├── design           → write access to design and docs repos, read on code
└── external         → read-only, for contractors or partners
```

**1.** Go to your org page, click **Teams**, then **New team**.

**2.** Name it something that describes function, not a person's name. `backend` ages better than `johns-team`.

**3.** Add members, then go to **Repositories** within the team page and assign it a permission level per repo (read, triage, write, maintain, or admin).

### Nested Teams

Teams can be nested inside parent teams. A parent team automatically includes everyone from its child teams, and any repo access given to the parent applies to everyone underneath it too.

```
engineering (parent)
  ├── backend (child)
  └── frontend (child)
```

Someone on `backend` is automatically treated as part of `engineering` for any permission granted at that level. This is useful for giving a whole department read access to shared resources without manually adding each sub-team.

---

## Permissions Without the Headache

GitHub's permission levels, from least to most access, are: **Read, Triage, Write, Maintain, Admin**. A quick way to think about each:

* **Read** — can view and clone, open issues, comment. Nothing else.
* **Triage** — Read, plus can manage issues and PRs (labels, assignees) without merging code.
* **Write** — Triage, plus can push code and merge PRs.
* **Maintain** — Write, plus can manage some repo settings, like protecting branches, without touching sensitive things like deleting the repo.
* **Admin** — full control of the repo, including deleting it and changing who has access.

A good rule most orgs land on eventually: default new members to no access or read-only, and grant Write or higher only through team membership tied to what they're actually working on. This keeps the blast radius small if an account gets compromised.

---

## Security Basics Every Org Needs

* **Require two-factor authentication.** This is Settings → Authentication security. If someone doesn't have 2FA on, they get removed from the org until they set it up. It sounds harsh, it isn't.
* **Turn on Dependabot alerts org-wide.** Settings → Code security lets you enable this as a default for every repo, so nobody has to remember to turn it on manually per project.
* **Set up branch protection on default branches.** At minimum, require a pull request before merging to `main`, and require at least one review on anything shared by more than one person.
* **Review the audit log periodically.** Settings → Audit log shows every meaningful action taken in the org: permission changes, new SSH keys, repo deletions. On paid plans this can be streamed to external tools for long-term retention.
* **Use SAML SSO if you're on Enterprise.** It ties org access directly to your company's identity provider, so removing someone from your company directory automatically cuts their GitHub access too.

---

## Billing and Seats

Paid orgs are billed per seat, where a seat is one member with paid-plan access. A few things that trip people up:

* Removing a member frees up their seat, but the change to your bill usually reflects on the next billing cycle, not instantly.
* Outside collaborators (people added to a single repo, not the whole org) can sometimes still count as billable depending on the plan, so check before assuming a "guest" is free.
* Billing managers can see and manage the invoice without being able to see any actual code, which is worth using if finance needs visibility but shouldn't have repo access.

---

## Offboarding People Properly

When someone leaves, removing their org access is not the same as revoking everything they touched. A proper offboarding pass includes:

**1.** Remove them from the organization (Settings → People → Remove).

**2.** Check if they had personal access tokens or SSH keys tied to org repos. Removing a member auto-revokes org-scoped tokens, but broader tokens might still work elsewhere if scoped loosely.

**3.** If they had admin on any specific repos outside team-based access, double check those are cleaned up too.

**4.** If they were an org owner, transfer or remove that role explicitly, don't assume removal from the org handles it (in most cases it does, but it's worth confirming in the audit log).

---

## Obscure but Useful Facts

* **Deleted teams don't delete history.** If you delete a team, past permission grants tied to it in the audit log stay intact, so you can still trace who had access to what and when.
* **A member can belong to an organization without being visible on the public member list**, depending on their own privacy setting for that org. This means "who's in this org" as seen from outside isn't always the full picture.
* **Org-level secrets exist separately from repo-level secrets**, and can be scoped to specific repos within the org. This is useful for shared API keys used by multiple projects, without copying the same secret into every repo's settings.
* **You can restrict who's allowed to create repositories at all**, down to specific teams, which is easy to miss since it's tucked away in Member privileges rather than in the repo settings themselves.
* **IP allow lists exist on Enterprise plans** and can block API and git access entirely from outside approved network ranges, independent of any individual user's login credentials.
* **Renaming a team doesn't break its `@org/team-name` mentions immediately**, GitHub keeps a redirect for a while, but old automation that hardcodes the slug can eventually stop resolving once the redirect expires.

---

## Resources & Further Reading

| Resource | What It Gets You |
| --- | --- |
| [GitHub Docs — Organizations](https://docs.github.com/en/organizations) | The official reference for every setting mentioned here |
| [GitHub Docs — Permission Levels](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories) | The exact breakdown of what each access level allows |
| [GitHub Docs — Security Overview](https://docs.github.com/en/code-security) | Org-wide security features and how to turn them on |
| [Shields.io](https://shields.io) | Build custom badges for your org's READMEs |
| [Capsule Render](https://github.com/kyechan99/capsule-render) | The header and footer banners used across this guide |

---

## License

MIT License, see [LICENSE](LICENSE) for full details. Fork it, adapt it, share it freely.

<div align="center">

![](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=Up%20next%3A%20building%20your%20hub.&fontSize=28&fontColor=FCA5A5&animation=fadeIn&fontAlignY=65)

</div>
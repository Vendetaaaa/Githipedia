<div align="center">

![GitHub Advisory Database](https://capsule-render.vercel.app/api?type=blur&height=260&color=B91C1C&text=GitHub+Advisory+Database&section=header&fontColor=FCA5A5&fontAlignY=34&desc=The+database+quietly+protecting+your+code+%E2%80%94+finally+explained+properly.&descAlignY=55&descSize=16)

![Security](https://img.shields.io/badge/Security-B91C1C?style=for-the-badge&labelColor=1a1a1a)
![25,000+ Advisories](https://img.shields.io/badge/25%2C000%2B_Advisories-7F1D1D?style=for-the-badge&labelColor=1a1a1a)
![13 Ecosystems](https://img.shields.io/badge/13_Ecosystems-991B1B?style=for-the-badge&labelColor=1a1a1a)
![Last Updated](https://img.shields.io/badge/Last%20Updated-2026-DC2626?style=for-the-badge&labelColor=1a1a1a)

</div>

*The database quietly protecting your code, finally explained properly.*

---

## Table of Contents

- [What Is This Thing?](#what-is-this-thing)
- [Why You Should Actually Care](#why-you-should-actually-care)
- [Core Concepts](#core-concepts)
  - [What is a Vulnerability?](#-what-is-a-vulnerability)
  - [What is a CVE?](#-what-is-a-cve)
  - [What is a GHSA ID?](#-what-is-a-ghsa-id)
  - [CVSS - Severity Explained](#-cvss--severity-explained)
  - [The OSV Format](#-the-osv-format)
- [The Three Types of Advisories](#the-three-types-of-advisories)
  - [✅ GitHub-Reviewed](#-github-reviewed)
  - [⏳ Unreviewed](#-unreviewed)
  - [☠️ Malware](#️-malware)
- [Where Does the Data Come From?](#where-does-the-data-come-from)
- [Supported Ecosystems](#supported-ecosystems)
- [What's Inside an Advisory](#whats-inside-an-advisory)
- [How It Connects to Dependabot](#how-it-connects-to-dependabot)
- [Searching the Database](#searching-the-database)
- [How to Contribute](#how-to-contribute)
- [The Numbers](#the-numbers)
- [FAQ](#faq)
- [Useful Links](#useful-links)

---

## What Is This Thing?

The GitHub Advisory Database is a free, publicly searchable database of known security vulnerabilities and malware in open-source packages. Think of it as a constantly-updated registry: "these versions of these packages have known problems, here's what they are, how bad they are, and how to fix them."

It covers 25,000+ advisories across 13 package ecosystems, npm, pip, Go, Rust, Maven, and more. Every entry links to affected versions, patched versions, and where possible a CVE identifier so you can cross-reference it elsewhere.

The whole thing is open source and lives at [github.com/github/advisory-database](https://github.com/github/advisory-database). Anyone can read it, use it, or contribute to it.

---

## Why You Should Actually Care

Modern software depends on code written by other people. Your `package.json`, `requirements.txt`, or `go.mod` is basically a list of trust relationships, and any one of those packages could have a vulnerability that ends up in your project.

```
Your app
  └── depends on library-x v2.1.0
        └── library-x v2.1.0 has a known SQL injection vulnerability
              └── your app now has a SQL injection vulnerability
```

The Advisory Database tracks these vulnerabilities so tools like Dependabot can warn you automatically, before someone exploits it.

You don't need to check it manually every day. But understanding how it works helps you read the alerts you get, figure out how serious they actually are, and decide when to update immediately versus when you can wait a sprint.

---

## Core Concepts

### 🔓 What is a Vulnerability?

A vulnerability is a flaw in software that could be exploited to cause harm. Data leaks, unauthorized access, system crashes. It's not always a traditional bug either; sometimes it's a design decision that turns out to be unsafe, or two features that interact in a dangerous way.

```
A vulnerability can damage:
  → Confidentiality  (data leaks, unauthorized access)
  → Integrity        (data tampering, code execution)
  → Availability     (denial of service, crashes)
```

A vulnerability that requires physical access to exploit is very different from one triggered by visiting a webpage. That difference is what severity scoring tries to capture.

### 🏷️ What is a CVE?

CVE stands for **Common Vulnerabilities and Exposures**. It's a standardised ID assigned to publicly known vulnerabilities, a universal reference number so that different databases, tools, and teams can all talk about the same issue without confusion.

```
Format:  CVE-YEAR-NUMBER
Example: CVE-2021-44228  ← Log4Shell, one of the most severe ever found
```

CVEs are assigned by organisations called CVE Numbering Authorities (CNAs). GitHub is one of them, which means it can assign CVE IDs directly for vulnerabilities in open-source projects hosted on GitHub. Not every vulnerability gets a CVE, but most significant ones do.

### 🪪 What is a GHSA ID?

Every advisory in the database gets its own unique identifier called a **GHSA ID**, regardless of whether a CVE exists.

```
Format:  GHSA-xxxx-xxxx-xxxx
Example: GHSA-jfh8-c2jp-hdpw
```

GHSA IDs are assigned the moment an advisory is created or imported. They're permanent and never reused. If you see one referenced anywhere, you can always look it up at `github.com/advisories/GHSA-xxxx-xxxx-xxxx`.

### 📊 CVSS - Severity Explained

CVSS (**Common Vulnerability Scoring System**) rates how serious a vulnerability is, on a scale from 0 to 10. The database supports both CVSS v3.1 and the newer v4.0.

| Severity | CVSS Score | What it actually means |
|---|---|---|
| 🟤 **Low** | 0.1-3.9 | Hard to exploit, limited impact, unusual conditions required |
| 🟡 **Medium** | 4.0-6.9 | Real risk, but usually needs specific conditions |
| 🟠 **High** | 7.0-8.9 | Serious, relatively easy to exploit. Patch soon |
| 🔴 **Critical** | 9.0-10.0 | Severe and easy to exploit. Patch immediately |

The score factors in attack complexity, whether authentication is required, whether it can be triggered remotely, and the kind of damage it causes.

A Critical advisory typically means something like: "an unauthenticated attacker can execute arbitrary code remotely with no user interaction required." If you see one, treat it urgently.

### 📄 The OSV Format

All advisories are stored as JSON files using the **Open Source Vulnerability (OSV) format**, an open standard so vulnerability data can be shared consistently across tools and databases.

This means the data is machine-readable and interoperable. Tools outside GitHub's ecosystem can pull from the same data.

```json
{
  "id": "GHSA-jfh8-c2jp-hdpw",
  "summary": "Remote code execution via unsafe deserialization",
  "severity": [{ "type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H" }],
  "affected": [{
    "package": { "ecosystem": "npm", "name": "example-package" },
    "ranges": [{ "type": "ECOSYSTEM", "events": [
      { "introduced": "1.0.0" },
      { "fixed": "1.2.3" }
    ]}]
  }]
}
```

---

## The Three Types of Advisories

### ✅ GitHub-Reviewed

The gold standard. A GitHub security analyst has manually examined the advisory, verified it's valid, confirmed affected and patched versions, and made sure the description is accurate.

```
Source   → CVE feed, community, or GitHub's own research
Review   → GitHub Security Curation team validates manually
Outcome  → Full description, accurate version ranges, ecosystem mapping
Dependabot → YES - triggers alerts if you're affected
```

This is the type that actually matters for most developers. When Dependabot alerts you, it's almost always based on a reviewed advisory. At launch the database had under 400 reviewed advisories; as of late 2024 that number had grown to over 20,000.

### ⏳ Unreviewed

These come straight from the National Vulnerability Database (NVD) feed, imported automatically without a manual review pass. That doesn't mean they're wrong; many have actually been looked at. But they haven't been through the full curation process.

```
Source   → NVD automatic feed
Review   → Not fully curated; may lack package mapping or version details
Dependabot → NO - Dependabot does not alert on unreviewed advisories
```

You can still browse unreviewed advisories at `github.com/advisories`, but don't expect automatic warnings from them.

### ☠️ Malware

A different category entirely. Not vulnerabilities in legitimate software; these are packages that are themselves malicious. Typosquats, backdoors, credential stealers, intentionally harmful packages published to public registries.

Search `type:malware` in the database. Worth knowing about, especially if you maintain open-source projects or work in supply-chain security.

**The most common type is typosquatting.** An attacker publishes a malicious package with a name very similar to a popular legitimate one, hoping developers install it by mistake.

```
Legitimate:  lodash        (200M+ weekly downloads)
Malicious:   1odash        (lowercase L instead of i)
             lodash-utils  (sounds plausible)
             iodash        (easy typo)
```

---

## Where Does the Data Come From?

```
National Vulnerability Database (NVD)  →  primary source for CVEs globally
GitHub Security Research               →  vulnerabilities found by GitHub's team
Community Contributions                →  PRs from developers worldwide
Package Registry Security Teams        →  e.g. npm security team for malware
CNA Partners                           →  other CVE Numbering Authorities
```

GitHub being a CNA means it can assign CVE IDs directly for vulnerabilities in open-source GitHub projects, without going through a third party.

---

## Supported Ecosystems

A GitHub-reviewed advisory is only possible for packages in a supported ecosystem:

| Ecosystem | Registry | Language(s) |
|---|---|---|
| `npm` | npmjs.com | JavaScript / TypeScript |
| `pip` | pypi.org | Python |
| `maven` | search.maven.org | Java / Kotlin |
| `rubygems` | rubygems.org | Ruby |
| `nuget` | nuget.org | .NET / C# |
| `composer` | packagist.org | PHP |
| `go` | pkg.go.dev | Go |
| `cargo` | crates.io | Rust |
| `swift` | swift.org / SPM | Swift |
| `pub` | pub.dev | Dart / Flutter |
| `hex` | hex.pm | Elixir / Erlang |
| `actions` | github.com/marketplace | GitHub Actions |
| `other` | - | Everything else |

> If your ecosystem isn't listed and you think it should be, you can open an issue at [github/advisory-database](https://github.com/github/advisory-database/issues).

---

## What's Inside an Advisory

Every advisory contains the same core fields:

```
GHSA ID         →  permanent unique identifier
CVE ID          →  cross-reference to global CVE database (if assigned)
Summary         →  one-line description
Description     →  full explanation of what's wrong and how it could be exploited
Severity        →  Low / Medium / High / Critical + raw CVSS score
Affected pkg    →  exactly which package is vulnerable
Ecosystem       →  which package registry
Affected vers.  →  the version range where the vulnerability exists
Patched vers.   →  the version(s) where it's been fixed
CWE IDs         →  classifies the type of flaw
References      →  links to CVE records, patches, blog posts, PoCs
Credits         →  who discovered and reported it
Published date  →  when first published
Last modified   →  when last updated
```

The **CWE ID** is useful when you want to understand *what kind* of vulnerability you're dealing with:

| CWE | What it means |
|---|---|
| CWE-79 | Cross-site scripting (XSS) |
| CWE-89 | SQL injection |
| CWE-22 | Path traversal |
| CWE-20 | Improper input validation |
| CWE-502 | Deserialization of untrusted data |
| CWE-400 | Uncontrolled resource consumption (DoS) |

---

## How It Connects to Dependabot

The Advisory Database and Dependabot are two halves of the same system. The database is the knowledge store; Dependabot is the engine that acts on it.

```
Step 1 → you add a dependency to your project
Step 2 → GitHub's dependency graph records it
Step 3 → a new GitHub-reviewed advisory is published for that package/version
Step 4 → Dependabot compares the advisory against your dependency graph
Step 5 → Dependabot opens an alert (and optionally a PR) on your repo
Step 6 → you review, update, and close the alert
```

Dependabot only triggers on **reviewed** advisories. Unreviewed ones haven't been validated for accuracy, so alerts based on them would generate a lot of noise.

**Enabling Dependabot alerts:**

```
Your repo → Settings → Security & analysis → Dependabot alerts → Enable
```

Or across your whole organisation:

```
Org settings → Code security → Dependabot alerts → Enable for all repositories
```

---

## Searching the Database

Browse and search at [github.com/advisories](https://github.com/advisories).

**Search filters:**

```
type:reviewed         →  GitHub-reviewed only
type:unreviewed       →  unreviewed only
type:malware          →  malware only

ecosystem:npm         →  filter by ecosystem
ecosystem:pip
ecosystem:go

severity:critical     →  filter by severity
severity:high
severity:medium
severity:low

CVE-2021-44228        →  search by CVE ID
GHSA-jfh8-c2jp-hdpw  →  search by GHSA ID
lodash                →  search by package name
```

**Via the GraphQL API:**

```graphql
query {
  securityAdvisories(first: 5, orderBy: {field: PUBLISHED_AT, direction: DESC}) {
    nodes {
      ghsaId
      summary
      severity
      publishedAt
      vulnerabilities(first: 3) {
        nodes {
          package { name ecosystem }
          vulnerableVersionRange
          firstPatchedVersion { identifier }
        }
      }
    }
  }
}
```

---

## How to Contribute

Two ways to get involved:

**Option 1 - Suggest improvements to an existing advisory**

On any advisory page at `github.com/advisories`, scroll to the bottom and click "Suggest improvements for this vulnerability." It opens a form where you can correct version ranges, add references, fix descriptions, or flag inaccurate info. Submitting automatically opens a PR.

**Option 2 - Submit a PR directly**

Clone the [advisory-database repo](https://github.com/github/advisory-database), find the advisory JSON you want to improve, make your changes, and open a PR. GitHub's Security Curation team reviews all contributions before merging.

Things worth contributing:

```
→ Missing or incorrect affected version ranges
→ Additional references (patches, blog posts, PoC links)
→ More accurate CWE classifications
→ Missing CVE links
→ Clearer or more complete descriptions
```

One limitation: community contributions are only accepted for advisories in supported ecosystems. The curation team needs to be able to properly assess each change, and that requires ecosystem familiarity.

---

## The Numbers

The database has grown a lot:

```
2019 (launch)  →  < 400 reviewed advisories
2024 (Oct)     →  > 20,000 reviewed advisories
2025-2026      →  25,000+ total across all types
```

2024 saw a 39% increase in advisories imported from external sources, driven by expanded ecosystem coverage and a major review push on older advisories predating the database's launch. It now supports CVSS v3.1 and v4.0.

---

## FAQ

**Why did I get a Dependabot alert for a package I'm not directly using?**

Dependabot covers both direct and transitive dependencies. A transitive dependency is a package that one of *your* dependencies depends on. You might never have heard of it, but it's running in your project. This is especially common in JavaScript, where dependency trees can be hundreds of packages deep.

**My package manager says I'm on a vulnerable version, but GitHub says it's patched. Who's right?**

Check the advisory's patched version carefully. Sometimes the fix exists in a minor release branch you haven't updated to, or the patch was backported to an older major version. If you can't reconcile it, the "Suggest improvements" link on the advisory page is the right place to flag the discrepancy.

**Can I use this data in my own tools?**

Yes, it's designed for this. The database is CC-BY 4.0 licensed, stored in OSV format, and fully queryable via GitHub's GraphQL API. Many commercial and open-source dependency scanners already pull from it.

**What's the difference between a GHSA ID and a CVE?**

A CVE is a global identifier assigned by the CVE Programme; it works across all databases and security tools. A GHSA ID is GitHub's own identifier, assigned to every advisory regardless of whether a CVE exists. An advisory can have both (they're linked), but GHSA IDs are assigned faster and exist even for vulnerabilities that haven't gone through the CVE process yet.

**Why don't unreviewed advisories trigger Dependabot alerts?**

Because they haven't been validated. They come straight from the NVD feed and may be incomplete, inaccurate, or not actually apply to a package in a supported ecosystem. Automatic alerts based on unreviewed data would generate significant noise: alerts for things that don't actually affect your project, missing version ranges, or advisories for entirely different packages with similar names.

---

## Useful Links

| Resource | What It Is |
|---|---|
| [github.com/advisories](https://github.com/advisories) | Browse and search the live database |
| [github/advisory-database](https://github.com/github/advisory-database) | The raw database repo - all OSV JSON files |
| [GitHub Docs - Advisory Database](https://docs.github.com/en/code-security/security-advisories/working-with-global-security-advisories-from-the-github-advisory-database/about-the-github-advisory-database) | Official documentation |
| [NIST National Vulnerability Database](https://nvd.nist.gov/) | The global CVE reference database |
| [OSV Schema](https://ossf.github.io/osv-schema/) | The open standard format advisories are stored in |
| [CVE Programme](https://www.cve.org/) | The global CVE numbering authority system |
| [About Dependabot alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts) | How Dependabot uses the database |

---

<div align="center">
  
[![](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=160&section=footer&text=Stay+patched.+Stay+safe.&fontSize=28&fontColor=FCA5A5&fontAlignY=65)](https://github.com/Vendetaaaa/Githipedia)

</div>
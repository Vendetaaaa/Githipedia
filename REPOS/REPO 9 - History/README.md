# The full story of GitHub, from a San Francisco apartment to 150 million developers.

---

## What is this platform?

GitHub did not appear out of nowhere. It was built to solve a real problem that developers were frustrated with every single day, and it grew into something much bigger than anyone who built it originally expected. This guide covers the full story: where it came from, how it grew, the controversies, the acquisitions, and where it stands today.

---

## Before GitHub: The Problem It Solved

To understand why GitHub mattered, you have to understand what collaboration looked like before it existed.

In the early 2000s, most teams used centralized version control systems like CVS or Subversion, usually called SVN. The model worked like this: there was one central server, and everyone pushed their code to it. If the server went down, work stopped. If two people edited the same file, the conflicts were a nightmare to sort out. Branching was so slow and painful that many teams just did not bother with it at all.

```
Old model (SVN):
   Dev A ──► Central Server ◄── Dev B
              (single point of failure)

Git model:
   Dev A ──► Local Repo ──► Remote Repo ◄── Dev B
              (every copy is a full backup)
```

Open source collaboration was especially awkward. If you found a bug in someone else's project and wanted to fix it, you had to email them a patch file and hope they noticed it. There was no standard way to propose a change, discuss it, and get it accepted. The whole process relied on mailing lists and goodwill.

GitHub changed all of that.

---

## The Timeline

### 2005 - Git Is Born

Before GitHub, there was Git, and without Git, GitHub would not exist.

Linus Torvalds, the creator of the Linux kernel, built Git in April 2005 in roughly ten days. He needed a distributed version control system for the Linux kernel after the project lost access to the tool it had been using. His goals were speed, simplicity, and the ability for thousands of contributors to work in parallel without a central server becoming a bottleneck.

```
April 3, 2005   --> Linus announces he is writing a new version control system
April 6, 2005   --> First commit to the Git source tree (made using Git itself)
April 7, 2005   --> Git is hosting its own source code
April 18, 2005  --> First successful merge of multiple branches
June 16, 2005   --> Linux kernel 2.6.12 becomes the first major project managed with Git
```

> 💡Fun fact: The name "Git" is British slang for an unpleasant person. Linus said he names his projects after himself. First Linux, then Git.

---

### 2007 to 2008 - GitHub Is Founded

Tom Preston-Werner and Chris Wanstrath met at a Ruby meetup in San Francisco in late 2007. Both of them were frustrated by how painful it was to share and collaborate on code with other developers. They started building GitHub as a weekend side project, something they genuinely wanted to exist for themselves.

P.J. Hyett joined shortly after. The three launched GitHub publicly on April 10, 2008, after a period of private beta testing. Scott Chacon came on board as one of the earliest employees, focusing on Git education and helping developers actually understand how to use the tool.

```
Late 2007    --> Preston-Werner and Wanstrath start building GitHub
January 2008 --> Private beta launches
April 10, 2008 --> GitHub goes public
End of 2008  --> GitHub is already hosting 46,000 public repositories
```

The original offer was simple: free for public repositories, paid for private ones. That model stayed in place for over a decade.

> 💡Fun fact: GitHub ran for two full years without any outside investment, funded entirely by subscription revenue from people who found it useful enough to pay for.

---

### 2009 to 2012 - Early Growth

Growth in the early years was quiet but surprisingly consistent. The Ruby and JavaScript communities adopted GitHub first, and the network effects kicked in fast. The more developers were on GitHub, the more reason there was for other developers to show up too.

| Year | Milestone |
|------|-----------|
| 2009 | 100,000 registered users |
| 2010 | 1,000,000 repositories hosted |
| 2011 | GitHub surpasses SourceForge and Google Code in total commits |
| 2012 | Series A funding, $100M raised from Andreessen Horowitz |
| 2012 | 1,000,000 registered users |

The $100M Series A in 2012 stood out because GitHub had been profitable without any outside investment for four years before accepting it. Andreessen Horowitz described it as one of the largest Series A checks the firm had ever written at the time.

---

### 2013 to 2015 - Going Mainstream

GitHub stopped being just a tool for developers and started becoming something closer to infrastructure that the whole world depended on.

Governments began using it to publish open data and legislation. Writers used it to version-control books. Scientists used it to collaborate on research papers. The phrase "GitHub for X" became shorthand for transparent, version-controlled collaboration in any field at all.

```
2013 --> 3,000,000 users and 5,000,000 repositories
2013 --> GitHub for Windows and GitHub for Mac released
2014 --> GitHub Enterprise hits $100M in annual recurring revenue
2015 --> GitHub reaches 9,000,000 users
2015 --> GitHub Education launches
```

> 💡Fun fact: GitHub Education gave millions of students free access to private repositories and professional tools. It became one of the most impactful free developer programs in the world and is still running today.

---

### 2016 to 2018 - Enterprise and the Microsoft Acquisition

By 2016, GitHub was the obvious home of open source. But internally the company was going through real turbulence, with leadership changes, documented culture problems, and growing competition from GitLab and Bitbucket putting pressure on the business.

Then came the announcement that changed everything.

On June 4, 2018, Microsoft announced it was acquiring GitHub for $7.5 billion in stock. It was the largest acquisition in GitHub's history and one of the biggest in the history of developer tools.

The reaction was immediate and split right down the middle. Thousands of developers moved their repositories to GitLab in the days after the announcement, worried that Microsoft would ruin what made GitHub worth using. Others pointed out that Microsoft had quietly become one of the largest contributors to open source anywhere in the world, and that the acquisition made a lot of sense once you looked at the numbers.

```
June 4, 2018     --> Microsoft acquisition announced at $7.5 billion
June 4 to 7, 2018 --> GitLab reports a 10x spike in repository imports
October 26, 2018 --> Acquisition officially closes
```

> 💡Fun fact: In the week after the announcement, GitLab went from importing around 100 repositories per hour to around 1,800 per hour. The panic was real. It was also, for most people, short-lived. GitHub's product kept getting better.

---

### 2019 to 2020 - Free Everything and the Arctic Vault

Microsoft's resources showed up quickly in GitHub's decisions.

On January 7, 2019, GitHub removed the limit on free private repositories. Before that day, private repos required a paid plan. Overnight, solo developers and small teams got unlimited private repositories at no cost. It was a direct challenge to Bitbucket, which had been the go-to option for free private hosting since GitHub charged for it.

Then GitHub did something that nobody saw coming.

In February 2020, GitHub photographed every active public repository onto archival film reels and transported them to a decommissioned coal mine deep inside a mountain in Svalbard, Norway. The facility sits 250 meters underground in permafrost designed to last for well over a thousand years.

```
Your public repo on GitHub
        |
        v
Photographed onto archival film
        |
        v
Shipped to Svalbard, Norway (78 degrees north latitude)
        |
        v
Stored 250 meters underground in Arctic permafrost
        |
        v
Preserved for 1,000 or more years
```

Every developer who had contributed to any active public repository before February 2, 2020 received the Arctic Code Vault Contributor badge on their profile. If you have it, a copy of your code is sitting under a Norwegian mountain right now.

---

### 2021 to 2023 - Copilot and the AI Era

On June 29, 2021, GitHub launched GitHub Copilot in technical preview. Built with OpenAI using a model called Codex, Copilot could autocomplete entire functions, suggest implementations based on comments, and write boilerplate from scratch. It felt genuinely different from anything developers had used before.

It was immediately controversial, because it was trained on public GitHub code and raised real questions about copyright and attribution that the industry is still working through today. It was also immediately popular.

```
June 2021     --> Copilot technical preview opens
June 2022     --> Copilot becomes generally available at $10 per month
March 2023    --> Copilot X announced, adding chat, voice, and PR summaries
November 2023 --> Copilot becomes free for verified students and open source maintainers
```

By 2023, GitHub Copilot had become the most widely used AI developer tool in the world. GitHub reported that in repositories where Copilot was enabled, it was generating close to 46% of the code being committed.

---

### 2024 to Present - 150 Million Developers

GitHub crossed 150 million registered developers in 2025, which makes it the largest software development platform in the world by nearly every measure you can use.

The platform has kept expanding its AI capabilities under the Copilot brand, adding coding agents, pull request automation, code review assistance, and deeper connections to development environments beyond VS Code. A free tier of Copilot on GitHub.com launched in 2025, making AI-assisted coding accessible to anyone with a GitHub account.

```
2024 --> GitHub Copilot Workspace announced
2024 --> Over 420 million public repositories on the platform
2025 --> 150 million registered developers
2025 --> Free Copilot tier launches on GitHub.com
```

The acquisitions of earlier years have been folded into the platform in ways that make GitHub feel less like a place to host code and more like a complete environment where software gets built from idea to deployment.

---

## Key Numbers at a Glance

| Metric | Number |
|--------|--------|
| Year founded | 2008 |
| Microsoft acquisition price | $7.5 billion |
| Registered developers in 2025 | 150 million+ |
| Public repositories | 420 million+ |
| Countries with active users | 200+ |
| Copilot subscribers | Millions |

---

## The Founders

| Person | Role | Known For |
|--------|------|-----------|
| Tom Preston-Werner | Co-founder | Initial architecture, created Semantic Versioning and Jekyll |
| Chris Wanstrath | Co-founder and CEO | Led GitHub through most of its independent years |
| P.J. Hyett | Co-founder | Early product and business direction |
| Scott Chacon | Co-founder and early employee | Git education, wrote the Pro Git book which is still free online |

> 💡Fun fact: Scott Chacon's Pro Git book is still the best free resource for learning Git properly. You can read the whole thing at git-scm.com/book.

---

## Notable Acquisitions and Products

| Year | Product or Company | What It Added |
|------|-------------------|---------------|
| 2016 | GitHub Pages expands | Free static site hosting for any public repository |
| 2018 | GitHub Actions launches | Native automation and CI/CD built directly into the platform |
| 2019 | Semmle | Code analysis and security scanning, which became CodeQL |
| 2020 | npm | The JavaScript package registry, home to over a million packages |
| 2021 | Copilot with OpenAI | AI-powered code completion that changed how developers write code |
| 2022 | Codespaces goes GA | Full cloud development environments that spin up in seconds |
| 2022 | Dependabot | Automated security updates for your dependencies |

---

## GitHub vs. The Alternatives

GitHub was not the only option. It competed with several serious challengers and outlasted most of them.

| Platform | Launched | Owned By | What Made It Different |
|----------|----------|----------|------------------------|
| GitHub | 2008 | Microsoft | Largest community, Copilot, Actions |
| Bitbucket | 2008 | Atlassian | Deep Jira integration, early free private repos |
| GitLab | 2011 | GitLab Inc. | Self-hostable, full DevOps platform in one product |
| SourceForge | 1999 | Slashdot Media | The standard before GitHub, declined sharply after 2010 |
| Google Code | 2006 | Google | Shut down in 2016, users migrated to GitHub |

> 💡Fun fact: Google Code shut down in January 2016. In their own announcement, Google acknowledged that GitHub had become the dominant platform for open source hosting and that continuing to run a competitor no longer made sense.

---

## License

MIT License, fork it, adapt it, translate it, share it freely.

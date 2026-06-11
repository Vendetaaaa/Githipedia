<div align="center">

![GitHub Profile Mastery](https://capsule-render.vercel.app/api?type=blur&height=260&color=B91C1C&text=GitHub+Profile+Mastery&section=header&fontColor=FCA5A5&fontAlignY=34&desc=Stop+having+a+bad+profile.+Start+today.&descAlignY=55&descSize=20)

![Setup Time](https://img.shields.io/badge/⏱_2_Hour_Setup-B91C1C?style=for-the-badge&labelColor=1a1a1a)
![Level](https://img.shields.io/badge/🚀_Beginner_to_Pro-7F1D1D?style=for-the-badge&labelColor=1a1a1a)

</div>

---

## Table of Contents

- [The Uncomfortable Truth](#the-uncomfortable-truth)
- [Before You Touch Anything](#before-you-touch-anything)
  - [What's a README?](#-whats-a-readme)
  - [What's Markdown?](#-whats-markdown)
  - [The Profile Trick Nobody Tells You About](#-the-profile-trick-nobody-tells-you-about)
  - [How People Actually Read Profiles](#-how-people-actually-read-profiles)
- [The 9 Elements](#the-9-elements)
  - [🖼️ Avatar & Identity](#️-avatar--identity)
  - [🎯 Bio](#-bio)
  - [📌 Pinned Repositories](#-pinned-repositories)
  - [📜 Profile README](#-profile-readme)
  - [📊 Stats Cards](#-stats-cards)
  - [🏷️ Tech Badges](#️-tech-badges)
  - [🐍 Contribution Graph & Snake](#-contribution-graph--snake)
  - [🔗 Social Links](#-social-links)
  - [🎨 Headers, Banners & Animations](#-headers-banners--animations)
- [What Kind of Profile Do You Need?](#what-kind-of-profile-do-you-need)
- [The Full Toolkit](#the-full-toolkit)
- [Things That Actually Kill Profiles](#things-that-actually-kill-profiles)
- [The 2-Hour Checklist](#the-2-hour-checklist)
- [License](#license)

---

## The Uncomfortable Truth

Most GitHub profiles look like this:

```
username: xX_coder_Xx
bio: (empty)
pinned repos: "test", "test2", "homework-2024", a fork they never touched
last commit: 8 months ago
```

That's not a portfolio. That's a liability.

Here's the uncomfortable part: a recruiter or collaborator who visits your profile is *already interested in you*. They looked you up on purpose. A bad profile is the only thing standing between that interest and an actual opportunity. And most developers have bad profiles, which means standing out is way easier than it sounds.

It takes a few focused hours. Not a redesign, not a new skill set. Just this guide.

---

## Before You Touch Anything

### 📄 What's a README?

A README is a file called `README.md` that GitHub automatically renders for anyone who visits. In a project repo it shows up below your file list. On your profile page, it *becomes* your front page. It's the first thing anyone sees.

No README means no context. A repo without one is basically a locked room. People look at the file names and leave.

```
my-project/
├── src/
├── tests/
├── package.json
└── README.md   ← GitHub shows this to everyone who visits
```

### ✍️ What's Markdown?

Markdown is the formatting language you use to write READMEs. Plain symbols become formatted output when GitHub renders them.

```
# Big Heading        →  large bold title
**bold**             →  bold text
*italic*             →  italic text
`code`               →  monospace highlight
- item               →  bullet point
[text](url)          →  clickable link
![alt](image-url)    →  embedded image
```

That covers most of what you'll actually use. The rest you can look up as you go.

### 🪄 The Profile Trick Nobody Tells You About

Create a repository with **your exact username** as the repo name, and GitHub treats its README as your profile page content. This is a real feature, not a hack.

```
→ github.com/new
→ Name it exactly your username (e.g. "janedoe")
→ ✓ Initialize with README
→ Create repository
→ Edit README.md → it now appears on your profile ✨
```

This is the single most important thing in this guide. Everything else builds on top of it.

### 👁️ How People Actually Read Profiles

Before you worry about design, understand what people actually look at and in what order:

```
0-2s   →  photo + name + bio        "who is this?"
2-5s   →  pinned repos              "what have they built?"
5-8s   →  contribution graph        "are they active?"
8-10s  →  README content            "can they communicate?"
```

If something feels off in the first five seconds, people leave. A beautiful README can't rescue empty pinned repos. **Get the substance right before touching the aesthetics.**

---

## The 9 Elements

| # | Element | Impact | Time | Difficulty |
|---|---|---|---|---|
| 1 | 🖼️ Avatar & Identity | High | 5 min | Trivial |
| 2 | 🎯 Bio | High | 10 min | Trivial |
| 3 | 📌 Pinned Repos | High | 30 min | Easy |
| 4 | 📜 Profile README | High | 1-2 hrs | Medium |
| 5 | 🔗 Social Links | Medium | 5 min | Trivial |
| 6 | 📊 Stats Cards | Medium | 10 min | Trivial |
| 7 | 🏷️ Tech Badges | Medium | 15 min | Easy |
| 8 | 🎨 Headers & Banners | Polish | 20 min | Easy |
| 9 | 🐍 Snake Animation | Polish | 45 min | Medium |

Do 1-3 first. Every time. The rest is polish on top of a foundation, and polish without a foundation is just decoration on nothing.

---

### 🖼️ Avatar & Identity

The first thing anyone sees. It sets the tone before they've read a single word.

**What works:**

| ✅ Good | ❌ Bad |
|---|---|
| Clear face photo, decent lighting | Default gray GitHub identicon |
| Consistent illustrated avatar | Blurry, dark, or heavily cropped |
| Same image across LinkedIn and GitHub | Random meme or in-joke |
| High contrast, centered | Heavily filtered selfie |

**Display name vs username:** Your username lives in every URL and is a pain to change. Your display name is flexible, so use it to show your real name so people can actually find and remember you.

```
Settings → Public profile → Name → Save
```

If your username is `xX_coder_Xx`, your display name should still say "Jane Doe." People search by name, not handle.

---

### 🎯 Bio

160 characters. One sentence. It's the most-read text on your whole profile.

**The formula:**

```
[what you do] + [what you're focused on] + [one hook]
```

**Examples:**

```
✅ "Backend dev building Go microservices · ex-@Stripe · shipping a
    side project in public"

✅ "CS junior @ uni · fascinated by compilers · looking for my first
    OSS contribution"

✅ "I make things that solve my own problems. Usually works out."

❌ "just a coder lol"
❌ "I like programming"
❌ (empty)
```

Also fill out the sidebar fields. They take two minutes and a lot of people just skip them:

```
🏢  Company    →  "@Freelance" or "@YourCompany" or "Open to work"
📍  Location   →  helps you appear in local developer searches
🔗  Website    →  portfolio, blog, or a project you're proud of
📧  Email      →  shows you're reachable; skip it if privacy matters
```

---

### 📌 Pinned Repositories

Your portfolio window. Six slots. Usually the first thing visitors actually click.

```
Profile page → "Customize your pins" (just below your bio) → select up to 6 → Save
```

**What to pin:**

```
✅ DEFINITELY PIN
   → your most complete, polished project (has a README, ideally a demo)
   → your primary-skill showcase
   → something that solves a real problem

✅ PROBABLY PIN
   → an OSS contribution you're proud of
   → a learning project with a write-up explaining what you learned

❌ NEVER PIN
   → repos named "test", "untitled", or "homework-2024"
   → repos with no description or README
   → forks you didn't meaningfully contribute to
   → anything your last commit on was over a year ago
```

Each card shows name, description, language, stars, and forks. The description is the most-read text on the card. Treat it like a one-line pitch.

```
Repository Settings → Edit repository details

✅  Description:  "CLI tool to batch-rename files using regex patterns"
✅  Topics:       cli, python, productivity, automation
✅  Website:      https://your-demo.com (if you have one)

❌  Description:  "my project" or (empty)
```

---

### 📜 Profile README

Your canvas. It can be a clean two-liner or a full showcase, but it needs to exist and it needs to feel like *you* wrote it, not like a template 10,000 other people are also using.

**The five parts that actually matter:**

**① Opening - who you are in two lines**

```markdown

## Hey, I'm Alex 👋

I build backend systems that don't fall over. Based in Bucharest,
currently obsessed with distributed tracing and Go generics.
```

**② The "right now" section - shows you're active and human**

```markdown
- 🔭 Currently shipping:  a personal finance API in Go
- 🌱 Learning:            Kubernetes, eBPF
- 🤝 Open to:             OSS collaboration on backend tooling
- 💬 Ask me about:        REST design, PostgreSQL, Docker
- ⚡ Fun fact:             I automate everything. Everything.
```

**③ Tech stack** - badges for what you actually know (see below)

**④ Stats** - contribution cards (see below)

**⑤ Contact - make it dead easy**

```html

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourname)
[![Email](https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:you@example.com)
[![Portfolio](https://img.shields.io/badge/Portfolio-B91C1C?style=for-the-badge&logo=vercel&logoColor=white)](https://yoursite.dev)

</div>
```

**On tone:** a 5-line README with a clear voice beats a 50-line wall of badges every time. Write it like a human, not like a resume.

---

### 📊 Stats Cards

[github-readme-stats](https://github.com/anuraghazra/github-readme-stats) generates live cards from your activity. Drop them in with a single image tag.

```markdown
<!-- Overall stats -->
![Stats](https://github-readme-stats.vercel.app/api?username=YOUR-USERNAME&show_icons=true&theme=dark&hide_border=true&bg_color=0d1117&icon_color=EF4444&title_color=FCA5A5)

<!-- Top languages -->
![Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=YOUR-USERNAME&layout=compact&theme=dark&hide_border=true&bg_color=0d1117&title_color=FCA5A5)

<!-- Streak -->
![Streak](https://streak-stats.demolab.com?user=YOUR-USERNAME&theme=dark&hide_border=true&ring=EF4444&fire=B91C1C&currStreakLabel=FCA5A5)
```

For a red palette: `dark` theme with `icon_color=EF4444` and `title_color=FCA5A5` gives you a clean dark base with red accents.

One honest caveat: stats cards measure quantity, not quality. "Mostly HTML" might just mean you have a lot of template files. Use stats as supporting evidence. Never as the headline.

---

### 🏷️ Tech Badges

[Shields.io](https://shields.io) + [Simple Icons](https://simpleicons.org) = a polished badge for any technology in about 30 seconds.

```markdown
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
```

**Style comparison:**

| Style | Best for |
|---|---|
| `flat-square` | Clean, modern - best for tech stacks |
| `for-the-badge` | Bold - good for social/contact links |
| `flat` | Slightly rounded, classic |
| `plastic` | Raised, retro profiles |

**Group them by category so they're readable:**

```markdown
### Languages
![Python] ![Go] ![TypeScript]

### Frameworks
![FastAPI] ![React] ![Gin]

### Infrastructure
![Docker] ![PostgreSQL] ![GitHub Actions]
```

One rule: if you'd be uncomfortable answering an interview question about it, don't badge it. A page full of badges for things you barely touched does more damage than good.

---

### 🐍 Contribution Graph & Snake

The green squares calendar is a passive signal of consistency. Two ways to make it work harder.

**Just keep it genuinely active.** Commits to personal projects, README edits, OSS contributions. Anything public shows up. Don't manufacture fake commits; experienced devs notice.

**Or add the snake animation.** It eats your contribution squares as a looping GIF. Subtle, memorable, and people always notice it.

**Step 1 - create the workflow:**

```yaml
# .github/workflows/snake.yml
name: Snake animation

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: Platane/snk@v3
        with:
          github_user_token: ${{ secrets.GITHUB_TOKEN }}
          outputs: |
            dist/github-snake.svg
            dist/github-snake-dark.svg?palette=github-dark
      - uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Step 2 - embed it in your README:**

```html
<div align="center">
  <img src="https://raw.githubusercontent.com/YOUR-USERNAME/YOUR-USERNAME/output/github-snake-dark.svg" />
</div>
```

---

### 🔗 Social Links

Two places to add these:

**GitHub's sidebar** - `Settings → Public profile → Social accounts`. At minimum: LinkedIn and your personal site.

**Inside your README** - raw URLs look unfinished; badge-style links look intentional.

```html
<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourname)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-B91C1C?style=for-the-badge&logo=safari&logoColor=white)](https://yoursite.dev)
[![Email](https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:you@email.com)

</div>

```

---

### 🎨 Headers, Banners & Animations

This is the finish layer. Apply it last, once everything beneath it is solid. A beautiful header on an empty profile is like putting a fancy frame on a blank canvas.

**Capsule Render** generates animated banners as simple image URLs, no design tools needed.

```html
<!-- Waving header -->
<img src="https://capsule-render.vercel.app/api?type=waving&height=250&color=B91C1C&text=Your%20Name&fontColor=FCA5A5&fontSize=60&section=header" width="100%" />

<!-- Blur style (used in this repo) -->
<img src="https://capsule-render.vercel.app/api?type=blur&height=250&color=B91C1C&text=Your%20Name&fontColor=FCA5A5&section=header" width="100%" />

<!-- Footer -->
<img src="https://capsule-render.vercel.app/api?type=waving&height=120&color=7F1D1D&section=footer" width="100%" />
```

Banner types: `wave` · `egg` · `shark` · `slice` · `rect` · `soft` · `blur` · `venom` · `cylinder`

**Typing animation** - one dynamic line that cycles through text:

```html
<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&pause=1000&color=EF4444&center=true&width=450&lines=Backend+Developer;Open+Source+Enthusiast;Always+shipping+something" />
</div>
```

**The rule on animations:**

One well-placed animation is memorable. Two is noisy. Three or more is unprofessional. Pick one and commit to it.

---

## What Kind of Profile Do You Need?

Your goal shapes your strategy. Pick the one that fits right now.

---

### 🎓 The Student

*Goal: show trajectory and potential, not experience you don't have yet*

Honest beats impressive here. Experienced people can tell when someone is being real with them. Don't fake depth. Show curiosity and momentum instead.

- Honest bio that names your path (bootcamp, CS degree, self-taught)
- 2-3 learning projects with READMEs explaining what you learned
- A visible "currently learning" stack
- One meaningful OSS contribution beats ten abandoned side projects

---

### 💼 The Job Seeker

*Goal: reduce the friction between someone visiting your profile and them sending a message*

Ask yourself: would you be comfortable sending this URL in a cold email to a company you want to work at? If not, fix it before applying anywhere.

- 2-3 polished, complete projects, deployed with live demos if possible
- LinkedIn link visible in the top half of your README
- Contribution graph active in the weeks before you start applying
- Bio: current status + primary skill + location (or "remote")

---

### 🔧 The OSS Contributor

*Goal: credibility, discoverability, and signaling you're welcoming to collaborators*

Consistency over time on the contribution graph matters more here than anywhere else. Maintainers want to see that you show up.

- Pin your most actively-maintained repos
- Signal openness: "PRs welcome", "good first issues labeled"
- Add a CONTRIBUTING.md to your major projects

---

### 🚀 The Builder in Public

*Goal: build an audience, attract collaborators, document your journey*

You're not just showing work here. You're showing how you think. That's what attracts people who want to build *with* you, not just use your code.

- Strong personality in the README; have a voice and use it
- A "what I'm building right now" section, updated at least monthly
- Links to your blog, newsletter, or dev log

---

## The Full Toolkit

| Tool | What It Does | Priority |
|---|---|---|
| [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) | Dynamic stat cards - stars, commits, languages | ⭐ Essential |
| [Shields.io](https://shields.io) | Custom badges for any tech or label | ⭐ Essential |
| [Simple Icons](https://simpleicons.org) | 3000+ brand logos as free SVGs | ⭐ Essential |
| [Capsule Render](https://github.com/kyechan99/capsule-render) | Animated header/footer banners | 🔴 Recommended |
| [Streak Stats](https://streak-stats.demolab.com) | Consecutive contribution streak card | 🔴 Recommended |
| [readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) | Animated typewriter text | 🔴 Recommended |
| [Platane/snk](https://github.com/Platane/snk) | Snake that eats your contribution graph | 🎨 Nice touch |
| [GitHub Profile Trophy](https://github.com/ryo-ma/github-profile-trophy) | Trophy badges from your stats | 🎨 Nice touch |
| [WakaTime](https://wakatime.com) | Real coding hours tracked by language | 🎨 Nice touch |
| [Profile README Generator](https://rahuldkjain.github.io/gh-profile-readme-generator/) | No-code starting point - heavily customize after | 🧰 Starter only |

---

## Things That Actually Kill Profiles

| Mistake | Why It Hurts | The Fix |
|---|---|---|
| Empty bio | Missed first impression in under a second | One sentence, the formula above |
| Pinned "test" or "untitled" repos | Signals you don't care about your own work | Delete or unpin them right now |
| Forked repos you never contributed to | Looks like padding | Only pin original or meaningful work |
| Default identicon avatar | Looks like an abandoned account | Upload literally any consistent image |
| Badges for everything you've touched | Dilutes your credibility | Only badge what you'd discuss in an interview |
| Stats card as the README centrepiece | Numbers do not equal quality | Stats support real work, they don't replace it |
| No contact method anywhere | Interested people give up and leave | At minimum, email or LinkedIn |
| README last updated years ago | "Currently learning Java" in 2022 | Review and refresh every 6 months |
| Copy-pasted template, unmodified | Looks like 10,000 other profiles | Templates are starting points |
| Multiple animations running at once | Visual chaos, slow load | One animation maximum |

---

## The 2-Hour Checklist

Do this in one sitting.

```
HOUR 1 - the foundation (do these first, they matter most)
──────────────────────────────────────────────────────────
□  Upload a clear, consistent avatar
□  Set display name to your real name
□  Write a bio: role + focus + one hook
□  Fill in location, website, one social link
□  Create the special username/username repository
□  Unpin all test / untitled / unfocused repos
□  Pin your 2-3 best projects
□  Add or improve the README on each pinned repo

HOUR 2 - the polish
──────────────────────────────────────────────────────────
□  Write your profile README (5-block structure above)
□  Add tech badges - grouped, only what you genuinely know
□  Add a stats card and streak card
□  Add social badge links in your README
□  Add a Capsule Render header or footer
□  Check: consistent colour palette throughout?
□  Check: can someone understand who you are in under 5s?
□  Send the URL to one person you trust and ask for honest feedback
```

---

## License

MIT - fork it, adapt it, translate it, share it freely.

```
Your code outlives your job title.
Your profile outlives your resume.
Build both like they matter.
```

<div align="center">
  
[![](https://capsule-render.vercel.app/api?type=waving&color=7F1D1D&height=160&section=footer&text=Ship.+Polish.+Repeat.&fontSize=28&fontColor=FCA5A5&fontAlignY=65)](https://github.com/Vendetaaaa/Githipedia)

</div>
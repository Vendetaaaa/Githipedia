<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=B91C1C&text=Profile%20Mastery%20and%20Hidden%20Markdown&fontColor=FCA5A5&fontSize=38&section=header" width="100%" />

<p align="center">
  <img alt="Depth" src="https://img.shields.io/badge/2_Deep_Dive-B91C1C?style=for-the-badge&labelColor=B91C1C&color=B91C1C" />
  <img alt="Level" src="https://img.shields.io/badge/Advanced_Tricks-B91C1C?style=for-the-badge&labelColor=B91C1C&color=B91C1C" />
</p>

</div>

---

## Table of Contents

- [Why This Deserves Its Own Deep Dive](#why-this-deserves-its-own-deep-dive)
- [Dynamic Stats Cards, Properly](#dynamic-stats-cards-properly)
- [Live-Updating Content](#live-updating-content)
  * [Pulling in your latest blog posts](#pulling-in-your-latest-blog-posts)
  * [Showing your currently-playing Spotify track](#showing-your-currently-playing-spotify-track)
- [Hidden HTML: The Accordion Trick](#hidden-html-the-accordion-trick)
- [The readme-generator, and When to Actually Use It](#the-readme-generator-and-when-to-actually-use-it)
- [Stacking All Four Without It Turning Into a Mess](#stacking-all-four-without-it-turning-into-a-mess)
- [Closing Note](#closing-note)

---

## Why This Deserves Its Own Deep Dive

Most guides stop at "add a stats card and a badge or two." That gets a profile from *empty* to *acceptable*. It does not get it to *unforgettable*.

The gap between those two is almost entirely made up of tricks that are not documented anywhere obvious: GitHub Actions quietly rewriting your README on a schedule, HTML tags that Markdown happens to pass through untouched, and generator tools that most people either misuse completely or dismiss without trying.

> *Nobody remembers a profile because it had a stats card. They remember it because something on it moved, updated, or surprised them.*

That's the thread connecting everything below.

---

## Dynamic Stats Cards, Properly

Everyone eventually finds [github-readme-stats](https://github.com/anuraghazra/github-readme-stats). Fewer people find its query parameters, which is where the actual customization lives.

```
<!-- The default everyone copies -->
![Stats](https://github-readme-stats.vercel.app/api?username=YOUR-USERNAME&show_icons=true)

<!-- The version worth shipping -->
![Stats](https://github-readme-stats.vercel.app/api?username=YOUR-USERNAME&show_icons=true&theme=tokyonight&hide_border=true&hide_rank=false&include_all_commits=true&count_private=true&card_width=440)
```

A few parameters most people never touch:

| Parameter | What it actually changes |
| --- | --- |
| `count_private=true` | Includes private repo activity in the count, not just public |
| `include_all_commits=true` | Uses full commit history instead of the last year only |
| `hide=stars,issues` | Removes specific stat rows you'd rather not show |
| `rank_icon=percentile` | Swaps the letter grade for a percentile ranking, which reads less like a school report card |
| `custom_title=` | Overrides the card's title text entirely |

<details>
<summary>Why "Mostly HTML" in your language card isn't a red flag (click to expand)</summary>

<br>

The top-languages card counts bytes, not effort. A single vendored HTML template can outweigh months of Python logic in raw byte count. If your language card doesn't match your actual skill set, that's normal, not a problem to fix. Treat stats cards as decoration that confirms activity, never as a resume replacement.

</details>

---

## Live-Updating Content

This is the category most profiles skip entirely, and it's the one that makes visitors do a double take, because a README that updates itself without you touching it reads as "this person automates things," which is exactly the impression a developer profile should give.

Both tricks below work the same way under the hood: a **GitHub Action runs on a schedule**, fetches fresh data, and rewrites a section of your README between two HTML comment markers.

### Pulling in your latest blog posts

Drop these two comment markers anywhere in your `README.md`:

```
<!-- BLOG-POST-LIST:START -->
<!-- BLOG-POST-LIST:END -->
```

Then add a workflow file at `.github/workflows/blog-post-workflow.yml`:

```yaml
name: Latest blog post workflow
on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:
jobs:
  update-readme-with-blog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gautamkrishnar/blog-post-workflow@v1
        with:
          feed_list: "https://your-blog-url.com/rss.xml"
```

Every six hours, the action fetches your RSS feed, formats the newest entries as Markdown links, and writes them straight between the comment markers. No manual edits, no forgetting to update it after a new post goes live.

### Showing your currently-playing Spotify track

This one needs a small piece of middleware since Spotify's API requires OAuth, but the setup is a one-time cost:

```
<div align="center">
  <img src="https://spotify-github-profile.vercel.app/api/view?uid=YOUR-SPOTIFY-ID&cover_image=true&theme=default&show_offline=false&background_color=121212" />
</div>
```

You authenticate once through the tool's hosted flow, get a `uid`, and drop it into the image URL above. The card then refreshes on its own whenever the badge is requested, showing whatever's actually playing.

> **Practical note:** set `show_offline=false` so the card simply omits itself when you're not listening to anything, rather than displaying a stale "last played" state that makes the whole README feel abandoned.

---

## Hidden HTML: The Accordion Trick

Markdown files render as HTML, which means any raw HTML tag GitHub doesn't explicitly strip just works. The most underused pair is `<details>` and `<summary>`, which gives you a native, no-JavaScript dropdown accordion.

```html
<details>
<summary>Click to see my full tech stack</summary>

### Languages
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)

### Tools
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

</details>
```

Rendered, this collapses into a single clickable line until someone chooses to expand it. Three places this earns its keep:

```
✅  Long badge lists   → keeps the top of the README scannable
✅  Detailed "about me" tangents → optional reading, not forced reading
✅  A changelog or "past projects" archive → history without clutter
❌  Your opening hook or contact links → these should never require a click
```

<details>
<summary>A second hidden trick worth knowing: comment-only lines</summary>

<br>

Standard HTML comments (`<!-- like this -->`) render as nothing at all in Markdown. Beyond hiding the workflow markers from earlier, they're also useful for leaving yourself notes directly in the source, such as `<!-- TODO: swap this banner once the new logo is done -->`, without a single visitor ever seeing them.

</details>

---

## The readme-generator, and When to Actually Use It

The [Profile README Generator](https://rahuldkjain.github.io/gh-profile-readme-generator/) is the tool most people either overuse or wrongly dismiss.

**Where it genuinely helps:** it exposes, in a form, roughly ninety percent of the tricks above (stats cards, badges, social links, a typing animation) without needing to memorize a single query parameter. For a first pass, it can take a blank README to something respectable in about ten minutes.

**Where it falls apart:** used as a final product instead of a starting point, it produces a README that looks like thousands of other README's, because everyone is pulling from the exact same generator defaults.

```
RIGHT WAY TO USE IT
1. Generate a base README with the tool
2. Strip out every section that doesn't apply to you
3. Rewrite the bio and "currently" section by hand, in your own voice
4. Swap the generic color scheme for one that's actually yours
5. Layer in one live-updating section (blog feed or stats) it doesn't offer by default

WRONG WAY TO USE IT
→ Generate it, copy the output, publish it unchanged
```

> The generator is scaffolding. The parts a visitor actually remembers, your bio, your voice, your "currently building" line, are the parts it can't write for you.

---

## Stacking All Four Without It Turning Into a Mess

Combining stats cards, a live feed, an accordion, and generator-built scaffolding in one README is easy to overdo. A rough order that keeps it readable:

| Order | Section | Why it goes there |
| --- | --- | --- |
| 1 | Banner and opening hook | First five seconds, no dropdowns allowed |
| 2 | "Currently" block | Human, scannable, still no dropdowns |
| 3 | Tech badges | Visible, but grouped |
| 4 | Live blog feed | Proves the automation works before anyone has to click anything |
| 5 | Stats and streak cards | Supporting evidence, not the headline |
| 6 | Everything else, archived work, extended bio, older badges | Behind a `<details>` accordion |

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=B91C1C&height=120&section=footer&fontColor=DBEAFE" width="100%" />

</div>

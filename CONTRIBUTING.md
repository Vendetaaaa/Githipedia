![Contributing Banner](https://capsule-render.vercel.app/api?type=blur&height=200&color=B91C1C&text=Contributing+to+Githipedia&section=header&fontColor=FCA5A5&fontSize=40&fontAlignY=50&desc=Help+us+build+the+open+encyclopedia+for+GitHub.&descAlignY=70&descSize=16)

> Everything matters, as small or big there is.

---

## Why Contribute?

Githipedia is a living organism. GitHub keeps evolving, and as so, should this repo also do. If you spotted something wrong, something missing, or just have a topic you think belongs here, you are already the right person to help.

No matter what you do, it is always welcomed!

---

## What You Can Contribute

### 1. **Documentation and guides**
- New REPO folders covering GitHub features not yet documented;
- Updates to existing guides when GitHub changes something;
- Better examples, clearer explanations, additional context;

### 2. **Corrections**
- Typos, broken links, outdated information;
- Inaccurate steps or screenshots that no longer match the current GitHub UI;

### 3. **Suggestions**
- Ideas for topics to cover, even if you are not writing them yourself;
- Feedback on how the content is structured or explained;

---

## Before You Start

A few things to check before opening a pull request:

1. Search the [open issues](https://github.com/Vendetaaaa/Githipedia/issues) and [existing REPOs](https://github.com/Vendetaaaa/Githipedia/tree/main/REPOS) to see if your topic or fix is already being worked on.
2. If you are adding a brand new REPO folder, open an issue first to discuss the scope. This helps avoid duplicate work.
3. Read the formatting conventions below so your content fits in naturally.

---

## How to Contribute

### Step 1: Fork the repo

Click the **Fork** button at the top of the [Githipedia repo page](https://github.com/Vendetaaaa/Githipedia). This creates your own copy to work on.

### Step 2: Clone your fork

```bash
git clone https://github.com/USERNAME/Githipedia.git
```

### Step 3: Create a branch

Give your branch a name that describes what you are doing:

```bash
git checkout -b add-github-actions-guide ( per exemple )
```

### Step 4: Make your changes

Write your content, fix your bug, update your guide. See the formatting section below for how things should look.

### Step 5: Commit and push

```bash
git add .
git commit -m "Add guide for GitHub Actions basics"
git push origin add-github-actions-guide
```

### Step 6: Open a pull request

Go to your fork on GitHub and click **Compare & pull request**. Fill in a short description of what you did and why, then submit it.

---

## Formatting Conventions

All content in Githipedia follows the same style so everything feels consistent.

**File structure**

Each REPO lives in its own folder under `/REPOS/` and must have a `README.md` + MIT LICENSE as its main files.

```
REPOS/
  REPO N - Topic Name/
    README.md
    LICENSE
    (extra files if needed)
```

**Headers**

Use a `capsule-render` banner at the top and bottom of every `README.md`, matching the red theme:

- Header: `color=B91C1C`, `fontColor=FCA5A5`
- Footer: `color=7F1D1D`, same font color

**Writing style**

> There is not a "special" writing type but it is recommended to follow these:

- Write like you are explaining something to a friend who knows what GitHub is but has not gone deep on this topic yet.
- Clear steps. No unknown jargon unless you explain it.

**Links**

Always link to the official GitHub docs when referencing something specific. Use descriptive link text, not "click here."

---

## Content Standards

To keep quality high across the board:

- Everything must be accurate as of the time of writing. If you are unsure, say so or link to the official source.
- No scraped or copy-pasted content from GitHub's documentation. Rewrite things in plain human language.
- If your guide includes steps, test them. Make sure they actually work.
- Avoid personal opinions unless clearly marked as a tip or note.

---

## Reporting Issues Instead of Contributing Directly

Not ready to write a fix yourself? That is completely fine.

[Open an issue](https://github.com/Vendetaaaa/Githipedia/issues/new) and describe:
- What is wrong or missing
- Where it is (link to the file or section)
- What it should say instead (if you know)

Someone will pick it up.

---

## Questions?

If you are unsure about anything, open an issue and ask. There are no silly questions here, only things that have not been documented yet.

---

![Footer Banner](https://capsule-render.vercel.app/api?type=blur&color=7F1D1D&height=120&section=footer&text=Thank+you+for+making+Githipedia+better.&fontColor=FCA5A5&fontSize=22&fontAlignY=55)

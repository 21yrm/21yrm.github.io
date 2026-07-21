# Apple-PI Personal Homepage Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Apple-π to the homepage News timeline and Selected Publications using the uploaded image and verified paper metadata.

**Architecture:** Extend the existing static markup in `_pages/about.md` with one news item and one publication card, following the neighboring S-Agent structure. Copy the supplied screenshot into `images/Apple-PI.png`; existing Jekyll and Sass behavior will render it without new styles or scripts.

**Tech Stack:** Jekyll, Markdown with inline HTML, Sass, static PNG assets

## Global Constraints

- Display the paper name as `Apple-π` and use `Apple-PI.png` for the asset filename.
- Preserve the full arXiv author order.
- Mark `Runmao Yao*` and `Kairui Hu*` as equal contributors; bold only `Runmao Yao*`.
- Reuse existing publication card styles without CSS changes.
- Link to the supplied arXiv, GitHub, and project URLs.

---

### Task 1: Add the Apple-PI image and homepage content

**Files:**
- Create: `images/Apple-PI.png`
- Modify: `_pages/about.md:96-174`

**Interfaces:**
- Consumes: Jekyll's existing relative image resolution and the existing `.news-item` and `.pub-card` markup contracts.
- Produces: A top-of-list 2026 News entry and top-of-list publication card that existing layout code renders automatically.

- [ ] **Step 1: Copy the uploaded image into the site assets**

Run:

```bash
cp '/Users/yaorunmao/Desktop/截屏2026-07-21 下午1.28.42.png' images/Apple-PI.png
```

Expected: `images/Apple-PI.png` exists and reports PNG format at 3112 × 1768 pixels.

- [ ] **Step 2: Add the News item at the top of the 2026 list**

Insert before the S-Agent item in `_pages/about.md`:

```html
<li class="news-item">
  <span class="news-date mono">Jul 17</span>
  <span class="news-text"><a href="https://arxiv.org/abs/2607.16401">Apple-π</a> is out &mdash; the first benchmark for evaluating law-grounded physical reasoning in video models.</span>
</li>
```

- [ ] **Step 3: Add the publication card before S-Agent**

Insert at the beginning of `#pub-masonry` in `_pages/about.md`:

```html
<article class="pub-card">
  <div class="pub-thumb">
    <img src="images/Apple-PI.png" alt="Apple-π" loading="lazy">
    <span class="pub-badge">arXiv 2026</span>
  </div>
  <div class="pub-info">
    <h3 class="pub-title">Apple-π: Benchmarking Thinking with Video Towards Law-Grounded Physical Intelligence</h3>
    <p class="pub-authors"><strong>Runmao Yao*</strong>, Kairui Hu*, Yukang Cao, Ruisi Wang, Shulin Tian, Ziang Cao, Weichen Fan, Ziqi Huang, Yuhao Dong, Hao Li, Zhaoxi Chen, Zhongang Cai, Lei Yang, Ziwei Liu</p>
    <div class="pub-links">
      <a href="https://arxiv.org/abs/2607.16401">Paper</a>
      <a href="https://github.com/21yrm/Apple-PI">Code</a>
      <a href="https://21yrm.github.io/Apple-PI-homepage/">Project</a>
    </div>
  </div>
</article>
```

- [ ] **Step 4: Run focused content assertions**

Run:

```bash
test -f images/Apple-PI.png
test "$(rg -c '2607\\.16401' _pages/about.md)" -eq 2
test "$(rg -c 'github\\.com/21yrm/Apple-PI' _pages/about.md)" -eq 1
test "$(rg -c '21yrm\\.github\\.io/Apple-PI-homepage/' _pages/about.md)" -eq 1
rg -F '<strong>Runmao Yao*</strong>, Kairui Hu*' _pages/about.md
```

Expected: all commands exit successfully and the last command prints the Apple-PI author line.

### Task 2: Validate the generated site and commit the implementation

**Files:**
- Verify: `_pages/about.md`
- Verify: `images/Apple-PI.png`

**Interfaces:**
- Consumes: The Jekyll project configuration in `_config.yml` and dependencies in `Gemfile.lock`.
- Produces: A generated `_site/index.html` containing the Apple-PI entry with a resolvable local image.

- [ ] **Step 1: Build the Jekyll site**

Run:

```bash
bundle exec jekyll build
```

Expected: exit code 0 and a generated `_site/index.html`.

- [ ] **Step 2: Verify generated markup and asset**

Run:

```bash
test -f _site/images/Apple-PI.png
test "$(rg -c '2607\\.16401' _site/index.html)" -eq 2
rg -F '<strong>Runmao Yao*</strong>, Kairui Hu*' _site/index.html
```

Expected: all commands exit successfully and the rendered author line is printed.

- [ ] **Step 3: Review the focused diff**

Run:

```bash
git diff --check
git diff -- _pages/about.md
git status --short
```

Expected: no whitespace errors; only `_pages/about.md`, `images/Apple-PI.png`, and this plan are new or modified after the earlier design commit.

- [ ] **Step 4: Commit the implementation**

Run:

```bash
git add _pages/about.md images/Apple-PI.png docs/superpowers/plans/2026-07-21-apple-pi-homepage.md
git commit -m "Add Apple-PI to homepage"
```

Expected: one commit containing the News item, publication card, image, and implementation plan.


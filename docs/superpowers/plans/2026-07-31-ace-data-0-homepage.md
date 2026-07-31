# ACE-Data-0 Homepage Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add ACE-Data-0 to the homepage News and Publications sections, use the supplied teaser image, and update the homepage research interests.

**Architecture:** Extend the existing static markup in `_pages/about.md` and add one local WebP asset. The new content follows the existing News and publication-card contracts, so the current Jekyll, Sass, and masonry JavaScript render it without structural or styling changes.

**Tech Stack:** Jekyll, Markdown with inline HTML, Sass, static WebP assets

## Global Constraints

- Change the `03` heading from `Selected Publications` to `Publications`.
- Place ACE-Data-0 first in the 2026 News list and first in Publications.
- Label the ACE-Data-0 publication card as `Technical Report`, not `arXiv 2026`.
- Preserve all 16 authors in paper order.
- Add `*` only to Yukang Cao, Haozhe Xie, and Beichen Wen.
- Bold only Runmao Yao in the ACE-Data-0 author list; do not add an asterisk to his name.
- Use the user-supplied `data-teaser.webp` image, available from the project page at `https://ace-data-engine.github.io/ACE-Data-0/assets/images/data-teaser.webp`.
- Order the hero tags and About research interests as Physical AI, Embodied AI, and World Models.
- Reuse the existing News and publication-card styles without CSS or JavaScript changes.

---

### Task 1: Add the ACE-Data-0 asset and homepage content

**Files:**
- Create: `images/ACE-Data-0.webp`
- Modify: `_pages/about.md:37-169`

**Interfaces:**
- Consumes: the existing `.tag`, `.news-item`, `.pub-card`, `.pub-thumb`, `.pub-authors`, and `.pub-links` markup contracts.
- Produces: updated research-interest copy, a regular top-of-list News entry, and a top-of-list publication card rendered by the existing page layout.

- [ ] **Step 1: Run the acceptance assertions and verify they fail**

Run:

```bash
test "$(rg -c '2607\\.28625' _pages/about.md 2>/dev/null || printf 0)" -eq 2
test "$(rg -c 'Embodied AI' _pages/about.md 2>/dev/null || printf 0)" -eq 1
test ! -f images/ACE-Data-0.webp
```

Expected: the first command exits 1 because the paper is absent. The second
command exits 1 because the `Embodied AI` hero tag is absent. The third command exits 0,
confirming that the image has not yet been added.

- [ ] **Step 2: Save the supplied teaser as a local site asset**

Run:

```bash
curl -L https://ace-data-engine.github.io/ACE-Data-0/assets/images/data-teaser.webp -o images/ACE-Data-0.webp
file images/ACE-Data-0.webp
```

Expected: the download succeeds and `file` reports a WebP image with dimensions
2000 × 1125.

- [ ] **Step 3: Update the research interests**

Replace the hero tags with:

```html
<span class="tag">Physical AI</span>
<span class="tag">Embodied AI</span>
<span class="tag">World Models</span>
```

Replace the research-highlight paragraph with:

```html
<p class="research-highlight">My research lies in <strong>physical AI</strong>, <strong>embodied AI</strong>, and <strong>world models</strong>.</p>
```

- [ ] **Step 4: Add the regular News item**

Insert this item before Apple-π in the 2026 News list:

```html
<li class="news-item">
  <span class="news-date mono">Jul 30</span>
  <span class="news-text"><a href="https://arxiv.org/abs/2607.28625">ACE-Data-0</a> is out &mdash; a large-scale, long-horizon, multimodal dataset for household human-object and human-scene interactions.</span>
</li>
```

- [ ] **Step 5: Rename the section and add the publication card**

Change only the heading text after the `03` span from `Selected Publications`
to `Publications`, preserving the citation badge.

Insert this card before Apple-π:

```html
<article class="pub-card">
  <div class="pub-thumb">
    <img src="images/ACE-Data-0.webp" alt="ACE-Data-0" loading="lazy">
    <span class="pub-badge">Technical Report</span>
  </div>
  <div class="pub-info">
    <h3 class="pub-title">ACE-Data-0: Human-Centric Ambient Capture as Embodied Data Engine</h3>
    <p class="pub-authors">Yukang Cao*, Haozhe Xie*, Beichen Wen*, <strong>Runmao Yao</strong>, Yinghao Liu, Yue Huang, Zhichao Liao, Yunxiang Wang, Haiheng Liu, Xingshun Tian, Dawei Su, Long Zhuo, Dacheng Tao, Xiaogang Wang, Liang Pan, Ziwei Liu</p>
    <div class="pub-links">
      <a href="https://arxiv.org/abs/2607.28625">Paper</a>
      <a href="https://huggingface.co/datasets/ACERobotics/ACE-Data-0">Dataset</a>
      <a href="https://ace-data-engine.github.io/ACE-Data-0/">Project</a>
    </div>
  </div>
</article>
```

- [ ] **Step 6: Run focused source assertions**

Run:

```bash
test -f images/ACE-Data-0.webp
file images/ACE-Data-0.webp | rg -F 'Web/P image'
file images/ACE-Data-0.webp | rg -F '2000x1125'
test "$(rg -c '2607\\.28625' _pages/about.md)" -eq 2
test "$(rg -c 'huggingface\\.co/datasets/ACERobotics/ACE-Data-0' _pages/about.md)" -eq 1
test "$(rg -c 'ace-data-engine\\.github\\.io/ACE-Data-0/' _pages/about.md)" -eq 1
rg -F 'Yukang Cao*, Haozhe Xie*, Beichen Wen*, <strong>Runmao Yao</strong>, Yinghao Liu, Yue Huang, Zhichao Liao, Yunxiang Wang, Haiheng Liu, Xingshun Tian, Dawei Su, Long Zhuo, Dacheng Tao, Xiaogang Wang, Liang Pan, Ziwei Liu' _pages/about.md
rg -U '<span class="tag">Physical AI</span>\\n[[:space:]]*<span class="tag">Embodied AI</span>\\n[[:space:]]*<span class="tag">World Models</span>' _pages/about.md
rg -F 'My research lies in <strong>physical AI</strong>, <strong>embodied AI</strong>, and <strong>world models</strong>.' _pages/about.md
rg -F '<span class="section-num mono">03</span>Publications ' _pages/about.md
rg -U '<img src="images/ACE-Data-0.webp" alt="ACE-Data-0" loading="lazy">\\n[[:space:]]*<span class="pub-badge">Technical Report</span>' _pages/about.md
! rg -F 'Video Generation' _pages/about.md
! rg -F 'Selected Publications' _pages/about.md
```

Expected: all commands exit 0; the exact complete author line, ordered tags,
About sentence, and renamed section heading are printed.

### Task 2: Validate the generated site and commit the update

**Files:**
- Verify: `_pages/about.md`
- Verify: `images/ACE-Data-0.webp`
- Verify: `docs/superpowers/plans/2026-07-31-ace-data-0-homepage.md`

**Interfaces:**
- Consumes: the Jekyll configuration and dependencies already pinned by the repository.
- Produces: a generated homepage containing the new content and a commit containing the implementation plan, homepage changes, and local teaser image.

- [ ] **Step 1: Build the Jekyll site**

Run:

```bash
BUNDLE_FORCE_RUBY_PLATFORM=true BUNDLE_PATH=/private/tmp/21yrm-bundle-native bundle exec jekyll build
```

Expected: Jekyll exits 0 and generates `_site/index.html`.

- [ ] **Step 2: Verify the generated homepage and copied asset**

Run:

```bash
test -f _site/images/ACE-Data-0.webp
test "$(rg -c '2607\\.28625' _site/index.html)" -eq 2
test "$(rg -c 'huggingface\\.co/datasets/ACERobotics/ACE-Data-0' _site/index.html)" -eq 1
rg -F 'Yukang Cao*, Haozhe Xie*, Beichen Wen*, <strong>Runmao Yao</strong>, Yinghao Liu, Yue Huang, Zhichao Liao, Yunxiang Wang, Haiheng Liu, Xingshun Tian, Dawei Su, Long Zhuo, Dacheng Tao, Xiaogang Wang, Liang Pan, Ziwei Liu' _site/index.html
rg -U '<span class="tag">Physical AI</span>\\n[[:space:]]*<span class="tag">Embodied AI</span>\\n[[:space:]]*<span class="tag">World Models</span>' _site/index.html
rg -F '<span class="section-num mono">03</span>Publications ' _site/index.html
rg -U '<img src="images/ACE-Data-0.webp" alt="ACE-Data-0" loading="lazy"[[:space:]]*/?>\\n[[:space:]]*<span class="pub-badge">Technical Report</span>' _site/index.html
! rg -F 'Video Generation' _site/index.html
! rg -F 'Selected Publications' _site/index.html
```

Expected: all commands exit 0 and the generated site contains the complete
author list, ordered interests, links, new section heading, and local image.

- [ ] **Step 3: Review the focused diff**

Run:

```bash
git diff --check
git diff -- _pages/about.md docs/superpowers/plans/2026-07-31-ace-data-0-homepage.md
git status --short
```

Expected: no whitespace errors. The only uncommitted changes are
`_pages/about.md`, `images/ACE-Data-0.webp`, and this implementation plan.

- [ ] **Step 4: Commit the implementation**

Run:

```bash
git add _pages/about.md images/ACE-Data-0.webp docs/superpowers/plans/2026-07-31-ace-data-0-homepage.md
git commit -m "Add ACE-Data-0 to homepage"
```

Expected: one commit containing the News item, publication card, teaser image,
research-interest updates, and implementation plan.

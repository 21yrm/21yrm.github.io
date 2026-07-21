# Apple-PI News Highlight Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Apple-π News timeline entry reuse the same highlight styling and animation as AnchoredDream.

**Architecture:** Change only the Apple-π News item's HTML state class in `_pages/about.md`. Existing Sass selectors for `.news-item.highlight` provide the bold accent date, animated timeline dot, and stronger text color without CSS or JavaScript changes.

**Tech Stack:** Jekyll, Markdown with inline HTML, Sass

## Global Constraints

- Keep AnchoredDream highlighted.
- Add the existing `highlight` class to Apple-π.
- Do not add or modify CSS or JavaScript.
- Preserve all News text, dates, and links.

---

### Task 1: Highlight the Apple-π News item

**Files:**
- Modify: `_pages/about.md:100`
- Verify: `assets/css/main.scss:970-1042`

**Interfaces:**
- Consumes: Existing `.news-item.highlight` Sass contract.
- Produces: Apple-π and AnchoredDream News entries that both opt into the existing highlight presentation.

- [ ] **Step 1: Verify the Apple-π highlight assertion currently fails**

Run:

```bash
rg -U '<li class="news-item highlight">\n[[:space:]]*<span class="news-date mono">Jul 17</span>' _pages/about.md
```

Expected: exit code 1 with no match.

- [ ] **Step 2: Add the existing highlight state**

Change the Apple-π opening element in `_pages/about.md` to:

```html
<li class="news-item highlight">
```

Do not change its date, copy, or arXiv link.

- [ ] **Step 3: Verify both highlighted entries and unchanged content**

Run:

```bash
test "$(rg -c 'class="news-item highlight"' _pages/about.md)" -eq 2
rg -U '<li class="news-item highlight">\n[[:space:]]*<span class="news-date mono">Jul 17</span>' _pages/about.md
rg -U '<li class="news-item highlight">\n[[:space:]]*<span class="news-date mono">Jan 23</span>' _pages/about.md
test "$(rg -c '2607\.16401' _pages/about.md)" -eq 2
```

Expected: all commands exit successfully; Apple-π and AnchoredDream are the two highlighted entries.

- [ ] **Step 4: Build and verify generated output**

Run:

```bash
BUNDLE_FORCE_RUBY_PLATFORM=true BUNDLE_PATH=/private/tmp/21yrm-bundle-native bundle exec jekyll build
test "$(rg -c 'class="news-item highlight"' _site/index.html)" -eq 2
git diff --check
```

Expected: Jekyll exits successfully, generated HTML contains exactly two highlighted News entries, and no whitespace errors are reported.

- [ ] **Step 5: Commit**

Run:

```bash
git add _pages/about.md
git commit -m "Highlight Apple-PI news item"
```

Expected: one commit changing a single HTML class.


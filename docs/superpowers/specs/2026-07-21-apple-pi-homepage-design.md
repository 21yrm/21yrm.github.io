# Apple-PI Personal Homepage Update

## Goal

Add the Apple-$\pi$ paper to both the News timeline and Selected Publications section of Runmao Yao's personal homepage, following the existing presentation used for recent 2026 papers.

## Content

### News

Insert a new item at the top of the 2026 timeline:

- Date: `Jul 17`
- Linked name: `Apple-π`
- Link: `https://arxiv.org/abs/2607.16401`
- Description: `the first benchmark for evaluating law-grounded physical reasoning in video models.`

The complete sentence is: `Apple-π is out — the first benchmark for evaluating law-grounded physical reasoning in video models.`

### Selected Publications

Insert a new publication card before S-Agent with:

- Image: `images/Apple-PI.png`, copied from the user-provided screenshot
- Image alt text: `Apple-π`
- Badge: `arXiv 2026`
- Title: `Apple-π: Benchmarking Thinking with Video Towards Law-Grounded Physical Intelligence`
- Authors, in arXiv order: `Runmao Yao*`, `Kairui Hu*`, `Yukang Cao`, `Ruisi Wang`, `Shulin Tian`, `Ziang Cao`, `Weichen Fan`, `Ziqi Huang`, `Yuhao Dong`, `Hao Li`, `Zhaoxi Chen`, `Zhongang Cai`, `Lei Yang`, `Ziwei Liu`
- Author styling: bold only `Runmao Yao*`; retain the asterisk on both Runmao Yao and Kairui Hu to indicate equal contribution
- Paper: `https://arxiv.org/abs/2607.16401`
- Code: `https://github.com/21yrm/Apple-PI`
- Project: `https://21yrm.github.io/Apple-PI-homepage/`

## Presentation

Reuse the existing publication-card markup and styles without introducing Apple-PI-specific CSS. Preserve the uploaded PNG as-is so the card uses the same responsive image behavior, masonry layout, hover treatment, and mobile breakpoints as the other publications.

## Validation

- Build the Jekyll site locally.
- Confirm the new News item is first in the 2026 list.
- Confirm the new publication card is first in Selected Publications.
- Confirm the image resolves and has meaningful alt text.
- Confirm both equal-contribution asterisks are present and only Runmao Yao's name is bold.
- Confirm the Paper, Code, and Project URLs are correct.
- Inspect the rendered page at desktop and mobile widths for layout regressions.

## Out of Scope

- Changes to the CV, biography, or project section.
- New card styles or special highlighting for Apple-PI.
- Changes to existing publication entries.

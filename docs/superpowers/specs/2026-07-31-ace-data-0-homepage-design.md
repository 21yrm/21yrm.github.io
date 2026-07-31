# ACE-Data-0 Homepage Update Design

## Goal

Update Runmao Yao's personal homepage to announce and list the newly released
paper, ACE-Data-0, while aligning the homepage research interests with the
current focus areas.

## Scope

The update is limited to `_pages/about.md` and one new local publication image.
Existing page structure, publication-card markup, masonry behavior, styling,
and citation-count behavior remain unchanged.

## News

Add a highlighted item at the top of the 2026 news list:

- Date: `Jul 30`
- Link: `https://arxiv.org/abs/2607.28625`
- Text: announce that ACE-Data-0 is out and describe it concisely as a
  large-scale, long-horizon, multimodal dataset for household human-object and
  human-scene interactions.

The date follows the paper's arXiv submission date and the item uses the
existing paper-announcement style.

## Publications

Change the section heading from `03 Selected Publications` to
`03 Publications`, preserving the Google Scholar citation badge.

Insert a new publication card before Apple-π with:

- Badge: `arXiv 2026`
- Title: `ACE-Data-0: Human-Centric Ambient Capture as Embodied Data Engine`
- Authors, in full and in paper order:
  `Yukang Cao*`, `Haozhe Xie*`, `Beichen Wen*`, **`Runmao Yao`**,
  `Yinghao Liu`, `Yue Huang`, `Zhichao Liao`, `Yunxiang Wang`,
  `Haiheng Liu`, `Xingshun Tian`, `Dawei Su`, `Long Zhuo`, `Dacheng Tao`,
  `Xiaogang Wang`, `Liang Pan`, and `Ziwei Liu`
- Equal-contribution marking: only the first three authors receive `*`
- Personal-author emphasis: `Runmao Yao` is bold and does not receive `*`
- Links:
  - Paper: `https://arxiv.org/abs/2607.28625`
  - Dataset: `https://huggingface.co/datasets/ACERobotics/ACE-Data-0`
  - Project: `https://ace-data-engine.github.io/ACE-Data-0/`

Copy the user-provided `data-teaser.webp` into the repository as
`images/ACE-Data-0.webp` and use it as the card image. Preserve the source
image without recompression; the existing publication thumbnail styling
controls its on-page crop and dimensions.

## Research Interests

Replace the hero tags, in order, with:

1. `Physical AI`
2. `Embodied AI`
3. `World Models`

Update the highlighted research sentence in `01 About` to name the same three
areas in the same order: physical AI, embodied AI, and world models.

## Verification

Before completion:

1. Assert that the new news item, publication title, full ordered author list,
   equal-contribution stars, links, heading, tags, and About sentence are
   present in the source.
2. Assert that `Video Generation` and `Selected Publications` no longer appear
   in the homepage source.
3. Confirm the local `images/ACE-Data-0.webp` asset matches the supplied image.
4. Build the Jekyll site successfully.
5. Inspect the generated homepage for the new content and image reference.

## Out of Scope

- Refactoring publications into a separate data file
- Changing publication-card styles or masonry layout
- Editing existing publication entries
- Adding a separate equal-contribution footnote to the page

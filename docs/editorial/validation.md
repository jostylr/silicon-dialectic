# Verification record — September 18, 2026

## Content integrity

- 31 original entries, 31 v1.5 entries, 31 v2 entries, and 31 separate critiques.
- All original `_posts` files match the recorded SHA-256 baseline and the starting Git revision `3c9070d`.
- Each of the 62 new edition entries preserves the original prompt block exactly, including source typos and the July 30 Novix attribution.
- Both closing reviews contain three strongest and three weakest selections, each with its own dialogue.
- Per-entry editorial and source-check notes are stored alongside this record; the JSON notes provide the detailed commit messages.

## Production builds

Built with Ruby 3.3.4, the GitHub Pages 232 dependency bundle, and Jekyll safe mode:

```sh
JEKYLL_ENV=production bundle exec jekyll build --safe
python3 scripts/validate_site.py
JEKYLL_ENV=production bundle exec jekyll build --safe --baseurl /silicon-dialectic --destination _site-project
python3 scripts/validate_site.py --site _site-project --baseurl /silicon-dialectic
```

Both builds passed. Each produced 134 HTML pages. Checks cover titles, duplicate IDs, unresolved Liquid, local links and anchors, same-origin absolute links, active edition links, previous/next navigation, the 31-entry edition indexes, all 124 table links, new-edition feeds, sitemap revision dates, and exclusion of private build/editorial files.

The dependency bundle emits a Faraday optional retry-middleware notice; it does not prevent either production build. No GitHub Pages deployment was performed.

## Browser checks

- Homepage inspected at desktop and 390-pixel mobile widths; edition cards stack on narrow screens.
- Edition index shows all 31 entries in reverse chronology, with start-of-month and closing-review entry points.
- Comparison index contains 31 rows and 124 links. Its table scrolls within the page at mobile width without widening the document.
- Closing comparison and final review inspected for readable layout and the active edition state.
- Search on v1.5 returns only the edited entry when searching for Claude. Enter on an empty result causes no console error.
- Temporary viewport override reset after responsive checks.

## Scope and limits

Original post URLs, CNAME, and recordings remain available. New writing does not claim that old recordings perform its new lyrics. Browser checks concern the local rendered site; external media were not played and all third-party destinations were not exhaustively tested. Fact-check sources and remaining editorial limitations are described in the per-entry notes and critiques.

All changes and local build dependencies are within this repository. Generated output and dependencies are ignored. No push or publishing-setting change was made.

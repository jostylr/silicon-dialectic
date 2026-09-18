# The Silicon Dialectic

A July 2025 AI-assisted daily blog, revisited in September 2026 as three complete editions and a comparative review.

- `/`: the experiment and reading routes
- `/v1/`: the original 31 entries (existing dated post URLs remain valid)
- `/v1.5/`: 31 edited entries
- `/v2/`: 31 new responses to the saved prompts
- `/entries/`: a table linking every version and critique
- `/critiques/`: 31 entry-specific comparisons
- `/final-review/`: the final assessment of the whole experiment

## Content and conventions

`_posts` is the untouched v1 archive. `_v1_5`, `_v2`, and `_critiques` are standard Jekyll collections. `_data/entries.json` maps a stable original filename to all four URLs, while `_data/editions.yml` describes the edition indexes. New documents have an `entry_id`, `date`, `version`, `title`, and `description`. The date is the original sequence date; the layouts disclose the September 2026 revision date.

The edited and fresh editions have separate Atom feeds at `/v1.5/feed.xml` and `/v2/feed.xml`; `/feed.xml` remains the original feed. New-edition metadata uses the September 2026 revision date, while indexes show original sequence dates.

Each essay keeps its original prompt verbatim. v1.5 edits the existing entry, including cases where the original wandered away from that prompt. v2 follows the prompt with fresh prose and original lyrics, preserving the dialogue/synthesis/reading-list conventions. Original recordings are not presented as recordings of the new lyrics. Editorial decisions and source checks are recorded in `docs/editorial/` and the per-entry commit messages.

The voices are literary roles. The comparison is an editorial experiment, not a controlled model benchmark; the new work was not blinded to the archive. See the About page for provenance and limitations.

## Local build

Use Ruby 3.3 and Bundler. The Gemfile uses the GitHub Pages dependency bundle, replacing the old reference to an absent theme gemspec. The TeXt theme itself is vendored in the repository.

```sh
bundle install
bundle exec jekyll serve
```

For a production build and checks:

```sh
JEKYLL_ENV=production bundle exec jekyll build --safe
python3 scripts/validate_site.py
```

The validator checks archive integrity, all four sets of entries, prompt preservation, generated internal links, edition navigation, and the index. It expects a complete `_site` build. To check source files alone, use `python3 scripts/validate_site.py --source-only`.

Check project-site paths as well as the custom-domain root:

```sh
JEKYLL_ENV=production bundle exec jekyll build --safe --baseurl /silicon-dialectic --destination _site-project
python3 scripts/validate_site.py --site _site-project --baseurl /silicon-dialectic
```

Local dependency caches and build output are ignored and excluded from publishing.

## GitHub Pages

The site uses standard Liquid, supported plugins, and output collections; there are no custom Jekyll plugins or client-side routing requirements. GitHub Pages can build it directly from the configured publishing branch. `CNAME` retains `silicon-dialectic.jostylr.com`, with an empty `baseurl` for that custom domain. All new internal links use `relative_url` so a project-path build also works.

This change does not push, alter repository publishing settings, or deploy anything. Once the commits are merged into the configured Pages source and pushed by the owner, the existing Pages publishing setup can build them.

## Attribution

Built on [TeXt Theme](https://github.com/kitian616/jekyll-TeXt-theme) by Tian Qi, under the repository’s MIT license. Article licensing follows `_config.yml` (CC BY-NC 4.0). Original prompts by James Taylor except where the archive explicitly attributes a prompt to Novix; original generated writing/lyrics credited in the entries. Some original recommendations retain affiliate links, disclosed on the site.

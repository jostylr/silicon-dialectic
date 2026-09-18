#!/usr/bin/env python3
"""Check the three-edition archive and the rendered GitHub Pages site.

Uses only the Python standard library. Run after a complete Jekyll build.
"""
import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []


def check(condition, message):
    if not condition:
        ERRORS.append(message)


def frontmatter(text):
    header = text.split('---', 2)[1]
    return dict((m.group(1), m.group(2).strip().strip('\"\''))
                for m in re.finditer(r'^([a-z_]+):\s*(.*)$', header, re.M))


def prompt(text):
    match = re.search(r'^[ \t]*[-*] \*\*TITLE:\*\*.*?(?=\n---|\n#{1,6} |\Z)', text, re.M | re.S)
    return match.group(0).rstrip('\n') if match else None


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.duplicate_ids = set()
        self.nav = []
        self.edition_targets = []
        self.listed_entries = []
        self.current = None
        self.title = ''
        self.in_title = False
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                self.duplicate_ids.add(attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'title':
            self.in_title = True
        if tag == 'nav':
            self.nav.append(attrs.get('aria-label', ''))
        if tag in ('a', 'link') and attrs.get('href'):
            self.links.append((attrs['href'], tag, attrs.get('rel', '')))
        if tag in ('img', 'script') and attrs.get('src'):
            self.links.append((attrs['src'], tag, ''))
        if tag == 'a':
            if self.nav and self.nav[-1] == 'Versions of this entry':
                self.edition_targets.append(attrs.get('href'))
                if attrs.get('aria-current') == 'page':
                    self.current = attrs.get('href')
            if 'read-entry' in attrs.get('class', '').split():
                self.listed_entries.append(attrs.get('href'))

    def handle_endtag(self, tag):
        if tag == 'nav' and self.nav:
            self.nav.pop()
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', default='_site')
    parser.add_argument('--baseurl', default='')
    parser.add_argument('--source-only', action='store_true')
    args = parser.parse_args()
    entries = json.loads((ROOT / '_data/entries.json').read_text())
    original_hashes = json.loads((ROOT / 'docs/editorial/original-sha256.json').read_text())
    check(len(entries) == 31, 'The entry manifest must contain 31 records.')
    check(len({entry['id'] for entry in entries}) == 31, 'Duplicate entry IDs in the manifest.')
    ids = {entry['id'] for entry in entries}
    for folder in ['_posts', '_v1_5', '_v2', '_critiques']:
        actual = {p.stem for p in (ROOT / folder).glob('*.md')}
        check(actual == ids, f'{folder}: missing {ids - actual}, extra {actual - ids}')
    for entry in entries:
        stem = entry['id']
        original = ROOT / '_posts' / (stem + '.md')
        if not original.exists():
            continue
        raw = original.read_bytes()
        check(hashlib.sha256(raw).hexdigest() == original_hashes.get(original.name), f'v1 changed: {original.name}')
        original_prompt = prompt(raw.decode())
        check(bool(original_prompt), f'{stem}: missing original prompt')
        for folder, version in [('_v1_5', 'v1.5'), ('_v2', 'v2'), ('_critiques', 'critique')]:
            path = ROOT / folder / original.name
            if not path.exists():
                continue
            text = path.read_text()
            check(text.startswith('---\n'), f'{path}: missing front matter')
            data = frontmatter(text)
            check(data.get('entry_id') == stem, f'{path}: wrong entry_id')
            check(data.get('version') == version, f'{path}: wrong version')
            check(data.get('date') == entry['date'], f'{path}: wrong date')
            check(bool(data.get('title')) and bool(data.get('description')), f'{path}: title/description missing')
            check(not re.search(r'\b(?:TODO|TBD|FIXME|lorem ipsum)\b', text, re.I), f'{path}: unfinished placeholder')
            if version != 'critique':
                check(prompt(text) == original_prompt, f'{path}: original prompt changed')
                check('<!--more-->' in text, f'{path}: excerpt marker missing')
                primary_voice = '**Novix AI:**' if version == 'v1.5' and '**Novix AI:**' in raw.decode() else '**James AI:**'
                check(primary_voice in text and '**Contra AI:**' in text, f'{path}: dialogue voices missing')
                check(re.search(r'Synthesis', text), f'{path}: synthesis missing')
                if '### Novix Prompt' in raw.decode():
                    check('### Novix Prompt' in text, f'{path}: original Novix prompt attribution changed')
            else:
                for key in ('v1', 'v15', 'v2'):
                    check(entry[key] in text, f'{path}: missing {key} comparison link')
    for folder in ('_v1_5', '_v2'):
        closing = ROOT / folder / '2025-07-31-silican-dialectic-a-review.md'
        if closing.exists():
            text = closing.read_text()
            check(len(re.findall(r'^#### [123]\. ', text, re.M)) == 6, f'{closing}: expected three strongest and three weakest dialogues')
    print(f'Source check: {len(entries)} entries × four versions; original hashes and saved prompts checked.')
    if not args.source_only:
        site = ROOT / args.site
        base = args.baseurl.rstrip('/')
        site_url = re.search(r'^url:\s*(\S+)', (ROOT / '_config.yml').read_text(), re.M).group(1)
        site_host = urlsplit(site_url).hostname
        pages = {p.relative_to(site).as_posix(): Page(p.read_text()) for p in site.rglob('*.html')}
        check(bool(pages), f'No rendered HTML in {site}; run the Jekyll build first.')

        def target(url):
            path = unquote(urlsplit(url).path)
            if base:
                if path == base:
                    path = '/'
                elif path.startswith(base + '/'):
                    path = path[len(base):]
                else:
                    return None
            name = path.lstrip('/')
            if not name or name.endswith('/'):
                name += 'index.html'
            if (site / name).is_dir():
                name += '/index.html'
            return name

        for filename, page in pages.items():
            check(bool(page.title.strip()), f'{filename}: empty title')
            check(not page.duplicate_ids, f'{filename}: duplicate IDs {page.duplicate_ids}')
            source_url = base + '/' + filename
            for href, tag, rel in page.links:
                parsed = urlsplit(href)
                if parsed.hostname == site_host and parsed.scheme in ('', 'http', 'https'):
                    # Original entries retain absolute custom-domain links. Map
                    # them to the equivalent local page in project-path builds.
                    path = parsed.path
                    if base and not (path == base or path.startswith(base + '/')):
                        path = base + path
                    resolved = path + ('#' + parsed.fragment if parsed.fragment else '')
                elif parsed.scheme or parsed.netloc or href.startswith('//'):
                    continue
                else:
                    resolved = urljoin(source_url, href)
                name = target(resolved)
                check(name is not None, f'{filename}: link escapes baseurl: {href}')
                if name is None:
                    continue
                check((site / name).exists(), f'{filename}: missing local target {href}')
                fragment = unquote(urlsplit(resolved).fragment)
                if fragment and name in pages:
                    check(fragment in pages[name].ids, f'{filename}: missing anchor {href}')
            rendered = (site / filename).read_text()
            check(not re.search(r'\{%|\{\{', rendered), f'{filename}: unrendered Liquid')

        for key in ['index.html', 'entries/index.html', 'critiques/index.html', 'final-review/index.html', 'v1/index.html', 'v1.5/index.html', 'v2/index.html']:
            check(key in pages, f'Missing destination page {key}')
        for index, entry in enumerate(entries):
            for version in ('v1', 'v15', 'v2', 'critique'):
                current_url = base + entry[version]
                name = target(current_url)
                check(name in pages, f'{version}: missing rendered page for {entry["id"]}: {name}')
                if name not in pages:
                    continue
                page = pages[name]
                check(page.current == current_url, f'{name}: wrong active edition')
                for key in ('v1', 'v15', 'v2', 'critique'):
                    check(base + entry[key] in page.edition_targets, f'{name}: missing {key} switcher link')
                for rel, neighbor in [('prev', index - 1), ('next', index + 1)]:
                    actual = [href for href, tag, link_rel in page.links if tag == 'a' and link_rel == rel]
                    expected = [base + entries[neighbor][version]] if 0 <= neighbor < len(entries) else []
                    check(actual == expected, f'{name}: incorrect {rel} sequence {actual} != {expected}')
        for key, folder in [('v1', 'v1'), ('v15', 'v1.5'), ('v2', 'v2')]:
            page = pages.get(folder + '/index.html')
            if page:
                expected = [base + entry[key] for entry in reversed(entries)]
                check(page.listed_entries == expected, f'{folder}: index mixes or omits entries or is not in reverse chronology')
        index = pages.get('entries/index.html')
        if index:
            links = {href for href, _, _ in index.links}
            for entry in entries:
                for key in ('v1', 'v15', 'v2', 'critique'):
                    check(base + entry[key] in links, f'Index missing {entry["id"]} {key}')
        atom = {'a': 'http://www.w3.org/2005/Atom'}
        for edition_path, key in [('v1.5', 'v15'), ('v2', 'v2')]:
            feed = site / edition_path / 'feed.xml'
            check(feed.exists(), f'Missing feed for {edition_path}')
            if feed.exists():
                try:
                    xml = ET.parse(feed)
                    items = xml.findall('a:entry', atom)
                    check(len(items) == 31, f'{edition_path}: expected 31 feed entries')
                    expected = ['https://silicon-dialectic.jostylr.com' + base + entry[key] for entry in reversed(entries)]
                    check([item.find('a:link', atom).get('href') for item in items] == expected, f'{edition_path}: feed contains wrong-edition links or order')
                    check(all(item.findtext('a:published', '', atom).startswith('2026-09-18') for item in items), f'{edition_path}: feed misdates new writing')
                except (ET.ParseError, AttributeError) as error:
                    check(False, f'{edition_path}: invalid Atom feed: {error}')
        sitemap = site / 'sitemap.xml'
        check(sitemap.exists(), 'Missing sitemap')
        if sitemap.exists():
            namespace = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            try:
                records = ET.parse(sitemap).findall('s:url', namespace)
                dates = {record.findtext('s:loc', '', namespace): record.findtext('s:lastmod', '', namespace) for record in records}
                new_urls = [entry[key] for entry in entries for key in ('v15', 'v2', 'critique')] + ['/final-review/']
                for url in new_urls:
                    check(dates.get(site_url + base + url, '').startswith('2026-09-18'), f'Sitemap misdates new writing: {url}')
            except ET.ParseError as error:
                check(False, f'Invalid sitemap: {error}')
        for excluded in ('scripts', 'docs', '.local', 'Gemfile', 'README.md'):
            check(not (site / excluded).exists(), f'Private build/editorial file published: {excluded}')
        print(f'Rendered check: {len(pages)} HTML pages; links, edition boundaries, chronological navigation, and baseurl {base or "/"} checked.')
    if ERRORS:
        print('\n'.join('ERROR: ' + error for error in ERRORS), file=sys.stderr)
        return 1
    print('All checks passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

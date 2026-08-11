"""Sync every article's "Other work" card (image + alt + title + category) to
match the homepage (index.html) card for that same article, so a case study
never shows different art or copy about itself depending on which page
you're looking from. Homepage is the single source of truth.
"""
import os
import re

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORK_CARD_RE = re.compile(
    r'<a href="(case-study-[^"]+\.html)"[^>]*class="work-card[^"]*"[^>]*>.*?'
    r'<img class="work-card-img" src="([^"]+)" alt="([^"]+)"[^>]*>.*?'
    r'<h3 class="work-card-title">([^<]+)</h3>\s*'
    r'<p class="work-card-cat">([^<]+)</p>',
    re.DOTALL,
)

OW_CARD_RE = re.compile(
    r'<a href="(case-study-[^"]+\.html)"([^>]*class="ow-card[^"]*"[^>]*)>\s*'
    r'<div class="ow-card-img-wrap">\s*'
    r'<img class="ow-card-img" src="[^"]+" alt="[^"]*"(\s*loading="lazy")?>\s*'
    r'</div>\s*'
    r'<div class="ow-card-info">\s*'
    r'<h3 class="ow-card-title">[^<]+</h3>\s*'
    r'<p class="ow-card-cat">[^<]+</p>\s*'
    r'</div>\s*'
    r'</a>'
)


def build_canonical_map():
    index_html = open(os.path.join(SITE_DIR, "index.html"), encoding="utf-8").read()
    mapping = {}
    for m in WORK_CARD_RE.finditer(index_html):
        href, src, alt, title, cat = m.groups()
        mapping[href] = {"src": src, "alt": alt, "title": title, "cat": cat}
    return mapping


def sync_file(path, mapping):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    changes = []

    def repl(m):
        href, attrs, lazy = m.group(1), m.group(2), m.group(3) or ""
        canonical = mapping.get(href)
        if not canonical:
            return m.group(0)
        new_block = (
            f'<a href="{href}"{attrs}>\n'
            f'      <div class="ow-card-img-wrap">\n'
            f'        <img class="ow-card-img" src="{canonical["src"]}" alt="{canonical["alt"]}"{lazy}>\n'
            f'      </div>\n'
            f'      <div class="ow-card-info">\n'
            f'        <h3 class="ow-card-title">{canonical["title"]}</h3>\n'
            f'        <p class="ow-card-cat">{canonical["cat"]}</p>\n'
            f'      </div>\n'
            f'    </a>'
        )
        if new_block.strip() != m.group(0).strip():
            changes.append(href)
        return new_block

    new_html = OW_CARD_RE.sub(repl, html)
    if changes:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
    return changes


if __name__ == "__main__":
    mapping = build_canonical_map()
    total = 0
    for fname in sorted(os.listdir(SITE_DIR)):
        if not fname.startswith("case-study-") or not fname.endswith(".html"):
            continue
        path = os.path.join(SITE_DIR, fname)
        changes = sync_file(path, mapping)
        for href in changes:
            print(f"{fname}: synced {href} card")
            total += 1
    print(f"\n{total} card(s) synced to canonical homepage source")

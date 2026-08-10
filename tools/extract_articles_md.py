"""Extract case study article text into clean editable Markdown files.
Pulls h1, intro paragraphs, meta table, process steps, outcome — skips nav/footer/CSS/JS.
Usage: python extract_articles_md.py
Writes one .md per case-study-*.html into articles-markdown/
"""
import os, re, glob
from bs4 import BeautifulSoup

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(SITE_DIR, "articles-markdown")
os.makedirs(OUT_DIR, exist_ok=True)

def clean_text(el):
    txt = el.get_text(" ", strip=True) if el else ""
    return txt.replace("­", "").replace("&shy;", "")

def extract(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    slug = os.path.splitext(os.path.basename(html_path))[0]
    lines = []

    h1 = soup.select_one(".case-header h1")
    title = clean_text(h1) if h1 else slug
    lines.append(f"# {title}")
    lines.append("")

    # Meta table
    meta_rows = soup.select(".case-meta-row")
    if meta_rows:
        lines.append("**Meta:**")
        for row in meta_rows:
            label = clean_text(row.select_one(".case-meta-label"))
            value = clean_text(row.select_one(".case-meta-value"))
            if label and value:
                lines.append(f"- {label}: {value}")
        lines.append("")

    # Intro paragraphs
    intro_ps = soup.select(".case-intro > p")
    if intro_ps:
        lines.append("## Intro")
        lines.append("")
        for p in intro_ps:
            lines.append(clean_text(p))
            lines.append("")

    # Case timeline (clickable jump-nav under h1, if present)
    ctl_rows = soup.select(".case-timeline .ctl-row")
    if ctl_rows:
        lines.append("## Timeline")
        lines.append("")
        for row in ctl_rows:
            label = clean_text(row.select_one(".ctl-label"))
            desc = clean_text(row.select_one(".ctl-desc"))
            if label:
                lines.append(f"- {label}: {desc}" if desc else f"- {label}")
        lines.append("")

    # Process steps
    steps = soup.select(".process-step")
    if steps:
        lines.append("## Process")
        lines.append("")
        for step in steps:
            h3 = clean_text(step.select_one("h3"))
            p = clean_text(step.select_one("p"))
            if h3:
                lines.append(f"### {h3}")
                lines.append("")
            if p:
                lines.append(p)
                lines.append("")

    # Outcome
    outcome_p = soup.select_one(".outcome p")
    if outcome_p:
        lines.append("## Outcome")
        lines.append("")
        lines.append(clean_text(outcome_p))
        lines.append("")

    # Image alt text (for reference — shows what each figure claims to depict)
    imgs = soup.select(".image-row img, .stacked-images img, .hero-widget img, .step-images img")
    if imgs:
        lines.append("## Figures (alt text reference)")
        lines.append("")
        for i, img in enumerate(imgs, 1):
            alt = img.get("alt", "").strip()
            src = img.get("src", "").strip()
            if alt:
                lines.append(f"{i}. `{os.path.basename(src)}` — {alt}")
        lines.append("")

    out_path = os.path.join(OUT_DIR, f"{slug}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_path, title

if __name__ == "__main__":
    html_files = sorted(glob.glob(os.path.join(SITE_DIR, "case-study-*.html")))
    print(f"Found {len(html_files)} case study pages\n")
    for hp in html_files:
        out_path, title = extract(hp)
        print(f"  {os.path.basename(hp):45s} -> {os.path.basename(out_path)}  ({title})")
    print(f"\nDone. Markdown files in: {OUT_DIR}")

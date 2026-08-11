"""One-time rollout: replace the old plain mailto Contact CTA with the new
"Yes, I want to know more" email-capture flow (shared contact-cta.css/js),
across every case-study article except reactive-vs-septic-arthritis
(already done by hand, this is the reference build).
"""
import os
import re
import sys

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP = {"case-study-reactive-vs-septic-arthritis.html"}

OLD_SECTION_RE = re.compile(
    r'<section class="contact fade-in">\s*'
    r'<h2>(.*?)</h2>\s*'
    r'<a href="mailto:steven\.oppong@gmail\.com" class="contact-icon"[^>]*>.*?</a>\s*'
    r'</section>',
    re.DOTALL,
)


def new_section(h2_html, slug):
    return f'''<section class="contact fade-in">
  <h2>{h2_html}</h2>
  <div class="contact-cta-stack">
    <div class="contact-cta-block">
      <button type="button" class="contact-icon partner-cta secondary" id="learnMoreYesBtn">Yes, I want to know more</button>
      <form class="contact-email-form" id="learnMoreForm" data-source="{slug}">
        <input type="email" id="learnMoreEmail" placeholder="you@email.com" required>
        <button type="submit">Send it to me</button>
      </form>
      <p class="contact-email-success" id="learnMoreSuccess">You're set. We'll send the full write-up to your inbox shortly.</p>
    </div>
  </div>
</section>'''


def process(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    if "contact-cta.css" in html:
        return "already done"

    m = OLD_SECTION_RE.search(html)
    if not m:
        return "SKIP: old contact section pattern not found"

    slug = os.path.basename(path).replace("case-study-", "").replace(".html", "")
    html = html[: m.start()] + new_section(m.group(1), slug) + html[m.end():]

    # head: add contact-cta.css right after global.css link
    if 'href="global.css"' not in html:
        return "SKIP: no global.css link found to anchor head insertion"
    html = html.replace(
        '<link rel="stylesheet" href="global.css">',
        '<link rel="stylesheet" href="global.css">\n<link rel="stylesheet" href="contact-cta.css">',
        1,
    )

    # body: add contact-cta.js before </body>, after other widget scripts if present,
    # otherwise right before the admin.js conditional loader / closing body tag
    if "admin.js" in html:
        html = html.replace(
            "<script>if (/[\\?&]edit\\b/.test(location.search))",
            '<script src="contact-cta.js"></script>\n<script>if (/[\\?&]edit\\b/.test(location.search))',
            1,
        )
    else:
        html = html.replace("</body>", '<script src="contact-cta.js"></script>\n</body>', 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return "updated"


if __name__ == "__main__":
    results = {}
    for fname in sorted(os.listdir(SITE_DIR)):
        if not fname.startswith("case-study-") or not fname.endswith(".html"):
            continue
        if fname in SKIP:
            results[fname] = "skipped (reference build)"
            continue
        path = os.path.join(SITE_DIR, fname)
        results[fname] = process(path)

    for fname, status in results.items():
        print(f"{status:45s} {fname}")

    updated = sum(1 for s in results.values() if s == "updated")
    print(f"\n{updated} files updated")
    problems = {k: v for k, v in results.items() if v.startswith("SKIP")}
    if problems:
        print("\nNeeds manual attention:")
        for k, v in problems.items():
            print(f"  {k}: {v}")

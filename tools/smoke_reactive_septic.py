"""Smoke test for case-study-reactive-vs-septic-arthritis.html: sticky outline,
captioned figures, gallery lightbox."""
import os
from playwright.sync_api import sync_playwright

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "file:///" + os.path.join(SITE_DIR, "case-study-reactive-vs-septic-arthritis.html").replace("\\", "/")
SCREENSHOT_DIR = os.path.join(SITE_DIR, "tools", "smoke_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

console_errors = []

def log_console(msg):
    if msg.type == "error":
        console_errors.append(msg.text)

results = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on("console", log_console)
    page.on("pageerror", lambda exc: console_errors.append(f"pageerror: {exc}"))

    page.goto(PAGE, wait_until="networkidle")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "rs_01_top.png"))

    intro_words = len(page.inner_text(".case-intro").split())
    results.append(("Intro is short (under 90 words)", intro_words < 90, f"{intro_words} words"))

    ctl_rows = page.query_selector_all(".case-timeline .ctl-row")
    results.append(("Outline has 6 stops", len(ctl_rows) == 6, f"found {len(ctl_rows)}"))

    outline_pos = page.eval_on_selector(".process-outline", "el => getComputedStyle(el).position")
    results.append(("Outline is sticky-positioned", outline_pos == "sticky", outline_pos))

    anchors = ["#ra-cleared", "#ra-mimicry", "#ra-enthesitis", "#ra-dgi", "#ra-fluid", "#ra-outcome"]
    for i, (row, anchor) in enumerate(zip(ctl_rows, anchors)):
        link = row.query_selector(".ctl-link")
        href = link.get_attribute("href")
        results.append((f"Outline link {i+1} href matches", href == anchor, f"{href} vs {anchor}"))
        link.click()
        page.wait_for_timeout(900)
        target = page.query_selector(anchor)
        in_view = False
        if target:
            box = target.bounding_box()
            in_view = box and 0 <= box["y"] <= 900
        results.append((f"Click '{anchor}' scrolls into view", in_view, ""))
        is_active = row.evaluate("el => el.classList.contains('active')")
        results.append((f"Row '{anchor}' gets active class", is_active, str(is_active)))

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "rs_02_after_scroll.png"))

    # Every process-step has imagery
    steps = page.query_selector_all(".process-step")
    for i, step in enumerate(steps):
        imgs_in_step = step.query_selector_all("img, video")
        results.append((f"Progression step {i+1} has imagery", len(imgs_in_step) > 0, f"{len(imgs_in_step)} images"))

    # No em dashes
    body_text = page.inner_text("body")
    has_em_dash = "—" in body_text
    results.append(("No em dashes in rendered text", not has_em_dash, "found em dash" if has_em_dash else "clean"))

    # All images load with nonzero natural width
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    all_imgs = page.query_selector_all("img:not(.lb-overlay img)")
    broken = []
    for im in all_imgs:
        w = page.evaluate("el => el.naturalWidth", im)
        if w == 0:
            broken.append(im.get_attribute("src"))
    results.append(("All images load (nonzero width)", len(broken) == 0, f"broken: {broken}" if broken else f"{len(all_imgs)} images ok"))

    # Lightbox on a process-step figure image
    img = page.query_selector(".process-step .step-figure img")
    if img:
        img.click()
        page.wait_for_timeout(400)
        overlay_open = page.eval_on_selector(".lb-overlay", "el => el.classList.contains('open')")
        results.append(("Lightbox opens on image click", overlay_open, str(overlay_open)))
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "rs_03_lightbox.png"))
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
    else:
        results.append(("Step figure has clickable img", False, "not found"))

    # Full-width closing video present, poster set
    full_video = page.query_selector("section.full-image video")
    poster_ok = False
    if full_video:
        poster = full_video.get_attribute("poster")
        poster_ok = bool(poster) and "reactive-septic-knee-01" in poster
    results.append(("Full-width closing video present with poster", full_video is not None and poster_ok, ""))

    # Compare slider (Figure 10) present and wired
    compare = page.query_selector(".compare-container")
    results.append(("Compare slider present", compare is not None, ""))
    if compare:
        handle = compare.query_selector(".compare-handle")
        results.append(("Compare slider has drag handle", handle is not None, ""))

    # Other work links to real pages
    ow_links = page.query_selector_all(".other-work-grid a")
    results.append(("Other work has 2 links", len(ow_links) == 2, f"found {len(ow_links)}"))

    # Mobile
    page.set_viewport_size({"width": 600, "height": 900})
    page.wait_for_timeout(300)
    mobile_cols = page.eval_on_selector(".case-header", "el => getComputedStyle(el).gridTemplateColumns")
    results.append(("Mobile: header collapses to single column", len(mobile_cols.split()) == 1, mobile_cols))
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "rs_04_mobile.png"))

    browser.close()

print("=" * 70)
print(f"SMOKE TEST: {PAGE}")
print("=" * 70)
passed = 0
for name, ok, detail in results:
    status = "PASS" if ok else "FAIL"
    if ok: passed += 1
    print(f"[{status}] {name}  ({detail})")
print("-" * 70)
print(f"{passed}/{len(results)} checks passed")
print(f"\nConsole errors: {len(console_errors)}")
for e in console_errors:
    print(f"  ERROR: {e}")
print(f"\nScreenshots: {SCREENSHOT_DIR}")

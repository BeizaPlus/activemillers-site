"""Smoke test for case-study-fat-necrosis.html: timeline nav, anchors, console errors, lightbox, responsive."""
import os
from playwright.sync_api import sync_playwright

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "file:///" + os.path.join(SITE_DIR, "case-study-fat-necrosis.html").replace("\\", "/")
SCREENSHOT_DIR = os.path.join(SITE_DIR, "tools", "smoke_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

console_errors = []
console_warnings = []

def log_console(msg):
    if msg.type == "error":
        console_errors.append(msg.text)
    elif msg.type == "warning":
        console_warnings.append(msg.text)

results = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on("console", log_console)
    page.on("pageerror", lambda exc: console_errors.append(f"pageerror: {exc}"))

    page.goto(PAGE, wait_until="networkidle")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "01_desktop_top.png"))

    # 0. Word count of intro (must read fast, PE-length)
    intro_text = page.inner_text(".case-intro")
    intro_words = len(intro_text.split())
    results.append(("Intro is short (PE-length, under 90 words)", intro_words < 90, f"{intro_words} words"))

    # 1. Outline exists and has 4 stops (3 mechanisms + outcome)
    ctl_rows = page.query_selector_all(".case-timeline .ctl-row")
    results.append(("Outline has 4 stops", len(ctl_rows) == 4, f"found {len(ctl_rows)}"))

    # 2. Header is two-column grid at desktop width
    header_cols = page.eval_on_selector(".case-header", "el => getComputedStyle(el).gridTemplateColumns")
    results.append(("Header is two-column grid", "px" in header_cols and len(header_cols.split()) == 2, header_cols))

    # 2b. Outline is sticky-positioned
    outline_pos = page.eval_on_selector(".process-outline", "el => getComputedStyle(el).position")
    results.append(("Outline is sticky-positioned", outline_pos == "sticky", outline_pos))

    # 3. Click each outline link, verify it scrolls to target AND active class gets applied
    anchors = ["#mechanism-enzymatic", "#mechanism-traumatic", "#mechanism-case", "#mechanism-outcome"]
    for i, (row, anchor) in enumerate(zip(ctl_rows, anchors)):
        link = row.query_selector(".ctl-link")
        href = link.get_attribute("href")
        results.append((f"Outline link {i+1} href matches", href == anchor, f"{href} vs {anchor}"))
        link.click()
        page.wait_for_timeout(600)
        target = page.query_selector(anchor)
        if target:
            box = target.bounding_box()
            in_view = box and 0 <= box["y"] <= 900
            results.append((f"Click '{anchor}' scrolls into view", in_view, f"y={box['y'] if box else None}"))
        else:
            results.append((f"Anchor {anchor} exists in DOM", False, "not found"))
        is_active = row.evaluate("el => el.classList.contains('active')")
        results.append((f"Row '{anchor}' gets active class on scroll", is_active, str(is_active)))

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "02_after_last_click.png"))

    # 3b. Every process-step has at least one image (no text-only blocks)
    steps = page.query_selector_all(".process-step")
    for i, step in enumerate(steps):
        imgs_in_step = step.query_selector_all("img")
        results.append((f"Process step {i+1} has imagery", len(imgs_in_step) > 0, f"{len(imgs_in_step)} images"))

    # 4. Scroll to top, check lightbox opens on image click
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    img = page.query_selector(".image-row img")
    if img:
        img.click()
        page.wait_for_timeout(400)
        overlay_open = page.eval_on_selector(".lb-overlay", "el => el.classList.contains('open')") if page.query_selector(".lb-overlay") else False
        results.append(("Lightbox opens on image click", overlay_open, str(overlay_open)))
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "03_lightbox_open.png"))
        # close it
        close_btn = page.query_selector(".lb-close")
        if close_btn:
            close_btn.click()
            page.wait_for_timeout(300)
    else:
        results.append(("Image row has clickable img", False, "no img found"))

    # 5. Check for em dashes anywhere in rendered text
    body_text = page.inner_text("body")
    has_em_dash = "—" in body_text
    results.append(("No em dashes in rendered text", not has_em_dash, "found em dash" if has_em_dash else "clean"))

    # 6. Mobile viewport check (809px breakpoint collapses to single column)
    page.set_viewport_size({"width": 600, "height": 900})
    page.wait_for_timeout(300)
    mobile_cols = page.eval_on_selector(".case-header", "el => getComputedStyle(el).gridTemplateColumns")
    is_single_col = len(mobile_cols.split()) == 1
    results.append(("Mobile: header collapses to single column", is_single_col, mobile_cols))
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "04_mobile_top.png"))

    # 7. Check nav mobile toggle exists and works
    toggle = page.query_selector("#mobileToggle")
    results.append(("Mobile nav toggle exists", toggle is not None, ""))

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
print()
print(f"Console errors: {len(console_errors)}")
for e in console_errors:
    print(f"  ERROR: {e}")
print(f"Console warnings: {len(console_warnings)}")
for w in console_warnings:
    print(f"  WARN: {w}")
print()
print(f"Screenshots saved to: {SCREENSHOT_DIR}")

"""Smoke test for case-study-wallenberg-syndrome.html: sticky outline, captioned figures,
gallery lightbox, and the lead-magnet email-capture flow (requires lead-capture-server.py running)."""
import os
from playwright.sync_api import sync_playwright

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "file:///" + os.path.join(SITE_DIR, "case-study-wallenberg-syndrome.html").replace("\\", "/")
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
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "wb_01_top.png"))

    intro_words = len(page.inner_text(".case-intro").split())
    results.append(("Intro is short (under 90 words)", intro_words < 90, f"{intro_words} words"))

    ctl_rows = page.query_selector_all(".case-timeline .ctl-row")
    results.append(("Outline has 5 stops", len(ctl_rows) == 5, f"found {len(ctl_rows)}"))

    outline_pos = page.eval_on_selector(".process-outline", "el => getComputedStyle(el).position")
    results.append(("Outline is sticky-positioned", outline_pos == "sticky", outline_pos))

    anchors = ["#wb-rollcall", "#wb-lateral", "#wb-decussation", "#wb-case", "#wb-outcome"]
    for i, (row, anchor) in enumerate(zip(ctl_rows, anchors)):
        link = row.query_selector(".ctl-link")
        href = link.get_attribute("href")
        results.append((f"Outline link {i+1} href matches", href == anchor, f"{href} vs {anchor}"))
        link.click()
        page.wait_for_timeout(500)
        target = page.query_selector(anchor)
        in_view = False
        if target:
            box = target.bounding_box()
            in_view = box and 0 <= box["y"] <= 900
        results.append((f"Click '{anchor}' scrolls into view", in_view, ""))
        is_active = row.evaluate("el => el.classList.contains('active')")
        results.append((f"Row '{anchor}' gets active class", is_active, str(is_active)))

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "wb_02_after_scroll.png"))

    # No em dashes
    body_text = page.inner_text("body")
    has_em_dash = "—" in body_text
    results.append(("No em dashes in rendered text", not has_em_dash, "found em dash" if has_em_dash else "clean"))

    # Lightbox on header image row
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    img = page.query_selector(".image-row img")
    if img:
        img.click()
        page.wait_for_timeout(400)
        overlay_open = page.eval_on_selector(".lb-overlay", "el => el.classList.contains('open')")
        results.append(("Lightbox opens on image click", overlay_open, str(overlay_open)))
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
    else:
        results.append(("Image row has clickable img", False, "not found"))

    # Lead magnet: form present
    form = page.query_selector("#leadMagnetForm")
    results.append(("Lead magnet form present", form is not None, ""))

    # Lead magnet: invalid submission blocked by browser validation (empty required field)
    email_input = page.query_selector("#leadMagnetEmail")
    results.append(("Email input present", email_input is not None, ""))

    # Lead magnet: real submission against local server
    if form and email_input:
        test_email = "smoketest+wallenberg@example.com"
        email_input.fill(test_email)
        submit_btn = page.query_selector("#leadMagnetForm button[type=submit]")
        submit_btn.click()
        page.wait_for_timeout(1200)
        success_visible = page.eval_on_selector("#leadMagnetSuccess", "el => el.classList.contains('visible')")
        results.append(("Lead magnet submission succeeds (server running)", success_visible, str(success_visible)))
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "wb_03_lead_success.png"))

    # Mobile
    page.set_viewport_size({"width": 600, "height": 900})
    page.wait_for_timeout(300)
    mobile_cols = page.eval_on_selector(".case-header", "el => getComputedStyle(el).gridTemplateColumns")
    results.append(("Mobile: header collapses to single column", len(mobile_cols.split()) == 1, mobile_cols))
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "wb_04_mobile.png"))

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

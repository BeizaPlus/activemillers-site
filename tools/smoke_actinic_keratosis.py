"""Smoke test for case-study-actinic-keratosis.html: sticky outline nav, captioned figures, gallery lightbox, hotspot annotations."""
import os
from playwright.sync_api import sync_playwright

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "file:///" + os.path.join(SITE_DIR, "case-study-actinic-keratosis.html").replace("\\", "/")
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
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "ak_01_desktop_top.png"))

    # 0. Word count of intro
    intro_text = page.inner_text(".case-intro")
    intro_words = len(intro_text.split())
    results.append(("Intro is short (under 90 words)", intro_words < 90, f"{intro_words} words"))

    # 1. Outline exists and has 4 stops
    ctl_rows = page.query_selector_all(".case-timeline .ctl-row")
    results.append(("Outline has 4 stops", len(ctl_rows) == 4, f"found {len(ctl_rows)}"))

    # 1b. Outline label is "Progression"
    outline_h2 = page.inner_text(".process-outline h2")
    results.append(("Outline heading reads 'Progression'", outline_h2.strip() == "Progression", outline_h2))

    # 2. Header is two-column grid
    header_cols = page.eval_on_selector(".case-header", "el => getComputedStyle(el).gridTemplateColumns")
    results.append(("Header is two-column grid", "px" in header_cols and len(header_cols.split()) == 2, header_cols))

    # 2b. Outline is sticky-positioned
    outline_pos = page.eval_on_selector(".process-outline", "el => getComputedStyle(el).position")
    results.append(("Outline is sticky-positioned", outline_pos == "sticky", outline_pos))

    # 3. Click each outline link, verify scroll + active class
    anchors = ["#ak-basal", "#ak-spinosum", "#ak-granulosum", "#ak-corneum"]
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

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "ak_02_after_last_click.png"))

    # 3b. Every process-step has imagery and a caption
    steps = page.query_selector_all(".process-step")
    for i, step in enumerate(steps):
        imgs_in_step = step.query_selector_all("img")
        caps_in_step = step.query_selector_all(".step-caption")
        results.append((f"Progression step {i+1} has imagery", len(imgs_in_step) > 0, f"{len(imgs_in_step)} images"))
        results.append((f"Progression step {i+1} has caption", len(caps_in_step) > 0, f"{len(caps_in_step)} captions"))

    # 4. Lightbox opens on image click, with fit-to-height sizing and rounded corners
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(300)
    img = page.query_selector(".image-row img")
    if img:
        img.click()
        page.wait_for_timeout(400)
        overlay_open = page.eval_on_selector(".lb-overlay", "el => el.classList.contains('open')") if page.query_selector(".lb-overlay") else False
        results.append(("Lightbox opens on image click", overlay_open, str(overlay_open)))
        box = page.eval_on_selector(".lb-overlay img", "el => ({h: el.clientHeight, radius: getComputedStyle(el).borderRadius})")
        results.append(("Lightbox image fits to ~92vh height", abs(box["h"] - 828) < 5, f"h={box['h']}"))
        results.append(("Lightbox image has rounded corners", box["radius"] == "16px", box["radius"]))
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "ak_03_lightbox_open.png"))
        close_btn = page.query_selector(".lb-close")
        if close_btn:
            close_btn.click()
            page.wait_for_timeout(300)
    else:
        results.append(("Image row has clickable img", False, "no img found"))

    # 4b. Lightbox caption works on a step-figure image (Figure 1)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(200)
    step_img = page.query_selector("#ak-basal .step-images img")
    if step_img:
        step_img.click()
        page.wait_for_timeout(400)
        info_visible = page.eval_on_selector(".lb-info", "el => el.classList.contains('visible')")
        results.append(("Info button visible for captioned figure", info_visible, str(info_visible)))
        info_btn = page.query_selector(".lb-info")
        info_btn.click()
        page.wait_for_timeout(300)
        cap_title = page.inner_text(".lb-caption-title")
        results.append(("Caption shows correct figure title", "TP53" in cap_title or "basal" in cap_title.lower(), cap_title))
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
    else:
        results.append(("Step-figure image found in Basal Layer section", False, "not found"))

    # 5. Hotspot pins still work (page-specific feature, must survive the rebuild)
    hotspot_pins = page.query_selector_all(".ak-pin")
    results.append(("Hotspot pins present", len(hotspot_pins) == 3, f"{len(hotspot_pins)} pins"))
    if hotspot_pins:
        hotspot_pins[0].click()
        page.wait_for_timeout(300)
        cap_text = page.inner_text("#ak-caption")
        results.append(("Hotspot click updates caption panel", "Capillary" in cap_text or "vessels" in cap_text.lower(), cap_text[:60]))

    # 6. No em dashes anywhere in rendered text
    body_text = page.inner_text("body")
    has_em_dash = "—" in body_text
    results.append(("No em dashes in rendered text", not has_em_dash, "found em dash" if has_em_dash else "clean"))

    # 7. Mobile viewport check
    page.set_viewport_size({"width": 600, "height": 900})
    page.wait_for_timeout(300)
    mobile_cols = page.eval_on_selector(".case-header", "el => getComputedStyle(el).gridTemplateColumns")
    is_single_col = len(mobile_cols.split()) == 1
    results.append(("Mobile: header collapses to single column", is_single_col, mobile_cols))
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "ak_04_mobile_top.png"))

    # 8. Mobile nav toggle exists
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

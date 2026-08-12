import sys
from playwright.sync_api import sync_playwright

URL = "file:///C:/Users/steve/Personal Assistant/Beiza/activemillers-site/index.html"

results = {}
console_errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})

    def on_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    page.on("console", on_console)
    page.on("pageerror", lambda exc: console_errors.append(str(exc)))

    page.goto(URL)
    page.wait_for_timeout(500)

    # Check 1: #mobileToggle visible
    toggle = page.locator("#mobileToggle")
    try:
        is_visible = toggle.is_visible()
        display = toggle.evaluate("el => getComputedStyle(el).display")
        results["1_toggle_visible"] = f"PASS (visible={is_visible}, display={display})" if is_visible and display != "none" else f"FAIL (visible={is_visible}, display={display})"
    except Exception as e:
        results["1_toggle_visible"] = f"FAIL (error: {e})"

    # Check 2: click toggle, #navLinks gains mobile-open, overlay visible
    try:
        toggle.click()
        page.wait_for_timeout(300)
        nav_links = page.locator("#navLinks")
        has_class = "mobile-open" in (nav_links.get_attribute("class") or "")
        nav_display = nav_links.evaluate("el => getComputedStyle(el).display")
        nav_opacity = nav_links.evaluate("el => getComputedStyle(el).opacity")
        results["2_nav_open"] = (
            f"PASS (mobile-open class={has_class}, display={nav_display}, opacity={nav_opacity})"
            if has_class and nav_display != "none" and float(nav_opacity) > 0
            else f"FAIL (mobile-open class={has_class}, display={nav_display}, opacity={nav_opacity})"
        )
    except Exception as e:
        results["2_nav_open"] = f"FAIL (error: {e})"

    # Check 3: search input visible/usable, type aspirin, exactly 1 .work-card without search-hidden
    try:
        search = page.locator("#caseSearch")
        search_visible = search.is_visible()
        search.click()
        search.fill("aspirin")
        page.wait_for_timeout(400)
        visible_cards = page.locator(".work-card:not(.search-hidden)")
        count = visible_cards.count()
        results["3_search"] = (
            f"PASS (input_visible={search_visible}, visible_cards={count})"
            if search_visible and count == 1
            else f"FAIL (input_visible={search_visible}, visible_cards={count})"
        )
    except Exception as e:
        results["3_search"] = f"FAIL (error: {e})"

    # Check 4: click a nav link (Experiments), confirm mobile-open removed
    try:
        # find nav link with text Experiments inside #navLinks
        link = page.locator("#navLinks a", has_text="Experiments").first
        link_count = page.locator("#navLinks a", has_text="Experiments").count()
        if link_count == 0:
            results["4_nav_link_close"] = "FAIL (no 'Experiments' link found in #navLinks)"
        else:
            link.click()
            page.wait_for_timeout(300)
            nav_links = page.locator("#navLinks")
            has_class_after = "mobile-open" in (nav_links.get_attribute("class") or "")
            results["4_nav_link_close"] = (
                f"PASS (mobile-open removed, class={nav_links.get_attribute('class')})"
                if not has_class_after
                else f"FAIL (mobile-open still present, class={nav_links.get_attribute('class')})"
            )
    except Exception as e:
        results["4_nav_link_close"] = f"FAIL (error: {e})"

    # Check 5: console errors
    results["5_console_errors"] = f"PASS (no errors)" if not console_errors else f"FAIL (errors: {console_errors})"

    browser.close()

for k in sorted(results.keys()):
    print(f"{k}: {results[k]}")

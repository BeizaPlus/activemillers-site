"""
Playwright test for the live-filter case search feature on index.html.
Run: python tools/test_case_search_playwright.py
"""
import pathlib
from playwright.sync_api import sync_playwright

FILE_PATH = pathlib.Path(r"C:\Users\steve\Personal Assistant\Beiza\activemillers-site\index.html")
URL = FILE_PATH.as_uri()

results = []
console_errors = []


def log(name, passed, detail=""):
    results.append((name, passed, detail))
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name} {('- ' + detail) if detail else ''}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ---------- DESKTOP ----------
        page = browser.new_page(viewport={"width": 1400, "height": 1000})
        page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda exc: console_errors.append(f"[pageerror] {exc}"))

        page.goto(URL)
        page.wait_for_load_state("networkidle")

        # Check 1: search input visible, Pathology link gone, Experiments present
        search_input = page.locator("#caseSearch")
        pathology_nav_link = page.locator("nav a[href='#pathology-anchor']")
        experiments_link = page.locator("nav a[href='#experiments-anchor']")
        try:
            input_visible = search_input.is_visible()
            pathology_count = pathology_nav_link.count()
            experiments_visible = experiments_link.first.is_visible()
            passed = input_visible and pathology_count == 0 and experiments_visible
            log("1. Search input visible, no Pathology link, Experiments present", passed,
                f"input_visible={input_visible} pathology_nav_link_count={pathology_count} experiments_visible={experiments_visible}")
        except Exception as e:
            log("1. Search input visible, no Pathology link, Experiments present", False, str(e))

        scroll_before = page.evaluate("window.scrollY")

        # Check 2: type "erythema"
        try:
            search_input.click()
            search_input.type("erythema", delay=30)
            page.wait_for_timeout(800)  # allow smooth scroll + filter
            visible_cards = page.locator(".work-card:not(.search-hidden)")
            visible_count = visible_cards.count()
            titles = []
            for i in range(visible_count):
                t = visible_cards.nth(i).locator(".work-card-title")
                titles.append(t.inner_text() if t.count() else "")
            scroll_after = page.evaluate("window.scrollY")
            scrolled = scroll_after > scroll_before
            is_erythema = any("erythema" in t.lower() for t in titles)
            passed = visible_count == 1 and is_erythema and scrolled
            log("2. 'erythema' filters to 1 card (Erythema Nodosum) + page scrolled", passed,
                f"visible_count={visible_count} titles={titles} scroll_before={scroll_before} scroll_after={scroll_after}")
        except Exception as e:
            log("2. 'erythema' filters to 1 card (Erythema Nodosum) + page scrolled", False, str(e))

        # Check 3: clear input
        try:
            total_cards = page.locator(".work-card").count()
            search_input.fill("")
            page.dispatch_event("#caseSearch", "input")
            page.wait_for_timeout(300)
            visible_cards = page.locator(".work-card:not(.search-hidden)")
            visible_count = visible_cards.count()
            no_results = page.locator("#workNoResults")
            no_results_visible_class = "visible" in (no_results.get_attribute("class") or "")
            passed = visible_count == total_cards and not no_results_visible_class
            log("3. Clearing input restores all cards, no-results hidden", passed,
                f"visible_count={visible_count} total_cards={total_cards} no_results_visible_class={no_results_visible_class}")
        except Exception as e:
            log("3. Clearing input restores all cards, no-results hidden", False, str(e))

        # Check 4: type "zzzznonexistent"
        try:
            search_input.fill("")
            search_input.type("zzzznonexistent", delay=20)
            page.wait_for_timeout(400)
            visible_cards = page.locator(".work-card:not(.search-hidden)")
            visible_count = visible_cards.count()
            no_results = page.locator("#workNoResults")
            has_visible_class = "visible" in (no_results.get_attribute("class") or "")
            is_rendered = no_results.is_visible()
            passed = visible_count == 0 and has_visible_class and is_rendered
            log("4. 'zzzznonexistent' -> 0 cards, #workNoResults visible+rendered", passed,
                f"visible_count={visible_count} has_visible_class={has_visible_class} is_rendered={is_rendered}")
        except Exception as e:
            log("4. 'zzzznonexistent' -> 0 cards, #workNoResults visible+rendered", False, str(e))

        # Check 5: type "dermatopathology" -> matches Erythema Nodosum + Actinic Keratosis
        try:
            search_input.fill("")
            search_input.type("dermatopathology", delay=20)
            page.wait_for_timeout(400)
            visible_cards = page.locator(".work-card:not(.search-hidden)")
            visible_count = visible_cards.count()
            titles = []
            for i in range(visible_count):
                t = visible_cards.nth(i).locator(".work-card-title")
                titles.append(t.inner_text() if t.count() else "")
            has_erythema = any("erythema" in t.lower() for t in titles)
            has_actinic = any("actinic" in t.lower() for t in titles)
            passed = has_erythema and has_actinic
            log("5. 'dermatopathology' matches Erythema Nodosum + Actinic Keratosis", passed,
                f"visible_count={visible_count} titles={titles}")
        except Exception as e:
            log("5. 'dermatopathology' matches Erythema Nodosum + Actinic Keratosis", False, str(e))

        # Check 6: console errors
        log("6. No console/page errors", len(console_errors) == 0, f"errors={console_errors}")

        page.close()

        # ---------- MOBILE ----------
        mobile_console_errors = []
        mpage = browser.new_page(viewport={"width": 390, "height": 844})
        mpage.on("console", lambda msg: mobile_console_errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
        mpage.on("pageerror", lambda exc: mobile_console_errors.append(f"[pageerror] {exc}"))
        mpage.goto(URL)
        mpage.wait_for_load_state("networkidle")

        try:
            toggle = mpage.locator("#mobileToggle")
            toggle_computed_display = mpage.eval_on_selector("#mobileToggle", "el => getComputedStyle(el).display")
            toggle_inline_style = mpage.eval_on_selector("#mobileToggle", "el => el.getAttribute('style')")
            toggle_clickable = toggle.is_visible()
            if toggle_clickable:
                toggle.click()
            else:
                # Hamburger button is not actually clickable (see bug note below);
                # force the nav open via JS so we can still evaluate the overlay itself.
                mpage.eval_on_selector("#navLinks", "el => el.classList.add('mobile-open')")
            mpage.wait_for_timeout(400)
            nav = mpage.locator("#navLinks")
            nav_class = nav.get_attribute("class") or ""
            mobile_open = "mobile-open" in nav_class

            m_search = mpage.locator("#caseSearch")
            m_visible = m_search.is_visible()
            box = m_search.bounding_box()
            viewport_width = 390
            not_clipped = False
            if box:
                not_clipped = (box["x"] >= 0) and (box["x"] + box["width"] <= viewport_width + 2)  # small tolerance

            # test usable: type into it
            usable = True
            try:
                m_search.click()
                m_search.type("test", delay=20)
                val = m_search.input_value()
                usable = (val == "test")
            except Exception:
                usable = False

            passed = toggle_clickable and mobile_open and m_visible and not_clipped and usable
            log("Mobile: search input in mobile nav overlay, visible, not clipped, usable", passed,
                f"toggle_button_clickable={toggle_clickable} toggle_computed_display={toggle_computed_display} "
                f"toggle_inline_style={toggle_inline_style} mobile_open={mobile_open} m_visible={m_visible} "
                f"box={box} not_clipped={not_clipped} usable={usable} mobile_console_errors={mobile_console_errors}")
        except Exception as e:
            log("Mobile: search input in mobile nav overlay, visible, not clipped, usable", False, str(e))

        mpage.close()
        browser.close()

    print("\n===== SUMMARY =====")
    for name, passed, detail in results:
        print(f"{'PASS' if passed else 'FAIL'}: {name}")


if __name__ == "__main__":
    main()

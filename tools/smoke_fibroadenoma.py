from pathlib import Path
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "case-study-fibroadenoma.html"


def run() -> None:
    assert PAGE.exists(), PAGE
    html = PAGE.read_text(encoding="utf-8")
    assert "—" not in html, "Em dash found in page source"
    for relative in (
        "videos/fibroadenoma-compressive-physics.mp4",
        "images/case-studies/fibroadenoma-compressive-physics-poster.jpg",
        "downloads/practical-pathology-case-001-fibroadenoma.pdf",
    ):
        assert (ROOT / relative).exists(), relative

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.goto(PAGE.as_uri(), wait_until="load")
        assert page.title() == "Fibroadenoma: Compressive Physics | Steven Oppong, MD"
        assert page.locator("video source").get_attribute("src") == "videos/fibroadenoma-compressive-physics.mp4"
        assert page.locator("a.download-button").get_attribute("href") == "downloads/practical-pathology-case-001-fibroadenoma.pdf"
        assert page.locator(".video-play-btn").is_visible()
        page.set_viewport_size({"width": 390, "height": 844})
        assert page.locator("h1").is_visible()
        browser.close()


if __name__ == "__main__":
    run()
    print("fibroadenoma smoke test passed")

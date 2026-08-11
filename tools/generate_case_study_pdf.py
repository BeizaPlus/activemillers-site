"""Standard case-study PDF packet generator.

This is the template for what gets emailed to someone who submits their
email through a case study's "Yes, I want to know more" CTA. One reusable
builder function (`build_case_study_pdf`) driven by a plain content dict,
so future articles just need a new CONFIG block, not a new script.

Structure (researched from lead-magnet PDF best practices: branded cover,
short-chunk body content backed by proof points, single closing CTA):
  1. Cover page - dark brand background, title, category, byline
  2. Content pages - condensed case narrative, 1-2 key images per page
  3. Closing CTA page - "Speak to a physician now" card

Demo: reactive-vs-septic-arthritis (run this file directly).
"""
import os
from fpdf import FPDF
from PIL import Image

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(SITE_DIR, "images", "case-studies")
OUT_DIR = os.path.join(SITE_DIR, "downloads")
IMG_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_pdf_img_cache")


def _compressed_image(path):
    """Downscale + JPEG-compress a source image for PDF embedding. A 4K PNG
    embedded at full resolution blows the packet up to 30MB+; a lead-magnet
    PDF needs to stay small enough to actually email."""
    os.makedirs(IMG_CACHE_DIR, exist_ok=True)
    cache_name = os.path.splitext(os.path.basename(path))[0] + ".jpg"
    cache_path = os.path.join(IMG_CACHE_DIR, cache_name)
    if os.path.exists(cache_path) and os.path.getmtime(cache_path) > os.path.getmtime(path):
        return cache_path
    img = Image.open(path).convert("RGB")
    max_w = 1000
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)
    img.save(cache_path, "JPEG", quality=78, optimize=True)
    return cache_path

BRAND_BG = (10, 10, 9)
BRAND_RED = (230, 0, 33)
INK = (20, 20, 20)
MUTED = (110, 110, 110)

PAGE_W = 210  # A4 mm


def _cover_page(pdf, title, category, byline):
    pdf.add_page()
    pdf.set_fill_color(*BRAND_BG)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_draw_color(*BRAND_RED)
    pdf.set_line_width(1.2)
    pdf.line(20, 90, 50, 90)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 30)
    pdf.set_xy(20, 100)
    pdf.multi_cell(170, 13, title, align="L")
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(*BRAND_RED)
    pdf.set_xy(20, pdf.get_y() + 4)
    pdf.cell(0, 8, category.upper(), ln=True)
    pdf.set_xy(20, 260)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(170, 6, byline, align="L")


def _section(pdf, heading, body, image_files=None):
    pdf.add_page()
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", "B", 17)
    pdf.set_xy(20, 20)
    pdf.multi_cell(170, 9, heading, align="L")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.set_x(20)
    pdf.multi_cell(170, 6.2, body, align="L")

    if image_files:
        pdf.ln(4)
        avail_w = 170
        gap = 6
        n = len(image_files)
        cell_w = (avail_w - gap * (n - 1)) / n
        x = 20
        y = pdf.get_y()
        max_h = 0
        for path, caption in image_files:
            full = os.path.join(IMG_DIR, path)
            if not os.path.exists(full):
                continue
            try:
                pdf.image(_compressed_image(full), x=x, y=y, w=cell_w)
                img_h = cell_w * 0.6
                max_h = max(max_h, img_h)
            except Exception:
                pass
            x += cell_w + gap
        pdf.set_y(y + max_h + 3)
        x = 20
        pdf.set_font("Helvetica", "I", 8.5)
        pdf.set_text_color(*MUTED)
        for path, caption in image_files:
            pdf.set_xy(x, pdf.get_y() - (max_h + 3) + max_h + 3)
            x += cell_w + gap
        # captions on one line under the row, left-aligned as a combined note
        pdf.set_x(20)
        pdf.multi_cell(170, 5, "  |  ".join(c for _, c in image_files), align="L")


def _cta_page(pdf, cta_title, cta_desc, cta_button, cta_note, contact_email):
    pdf.add_page()
    pdf.set_fill_color(*BRAND_RED)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_xy(25, 110)
    pdf.multi_cell(160, 10, cta_title, align="L")
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(255, 230, 230)
    pdf.set_x(25)
    pdf.multi_cell(160, 6.5, cta_desc, align="L")

    # pill button
    btn_y = pdf.get_y() + 8
    btn_w, btn_h = 80, 14
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(25, btn_y, btn_w, btn_h, "F", round_corners=True, corner_radius=7)
    pdf.set_text_color(*BRAND_RED)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(25, btn_y + 4.2)
    pdf.cell(btn_w, 6, cta_button, align="C")

    pdf.set_xy(25, btn_y + btn_h + 8)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(255, 210, 210)
    pdf.multi_cell(160, 5.5, cta_note, align="L")

    pdf.set_xy(25, 270)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(160, 5, f"activemillers.com  |  {contact_email}", align="L")


def build_case_study_pdf(config, out_path):
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    _cover_page(pdf, config["title"], config["category"], config["byline"])
    for section in config["sections"]:
        _section(pdf, section["heading"], section["body"], section.get("images"))
    _cta_page(
        pdf,
        config["cta"]["title"],
        config["cta"]["desc"],
        config["cta"]["button"],
        config["cta"]["note"],
        config["contact_email"],
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pdf.output(out_path)
    return out_path


# ---- Demo config: Reactive vs Septic Arthritis ----
REACTIVE_SEPTIC_CONFIG = {
    "title": "Reactive vs Septic Arthritis",
    "category": "Rheumatology / Infectious Disease",
    "byline": "Steven Oppong, MD - Medical Illustrator\nactivemillers.com",
    "contact_email": "steven.oppong@gmail.com",
    "sections": [
        {
            "heading": "Two joints, same presentation, opposite mechanisms",
            "body": (
                "A swollen, painful joint shows up the same way at the bedside whether it's "
                "reactive arthritis or disseminated gonococcal infection: migratory polyarthralgia, "
                "tenosynovitis, systemic symptoms. But inside the joint, the two conditions are "
                "mechanistically opposite. Reactive arthritis is sterile, a T-cell attack that "
                "outlives the infection that trained it. Disseminated gonococcal infection is a "
                "live bacterial invasion that seeded the joint through the bloodstream."
            ),
            "images": [
                ("reactive-septic-knee-baseplate.png", "Baseline joint capsule"),
            ],
        },
        {
            "heading": "Molecular mimicry: the case of mistaken identity",
            "body": (
                "HLA-B27 presents a fragment of the original organism to a T-cell, training that "
                "T-cell to attack it. The problem: a joint self-antigen looks close enough to that "
                "fragment that the same T-cell attacks the joint's own tissue instead. The joint "
                "fluid stays completely organism-free throughout. Every bit of the inflammation "
                "here is autoimmune, collateral damage in a fight that was actually won somewhere "
                "else entirely."
            ),
            "images": [
                ("reactive-septic-mech-02.png", "HLA-B27 presenting a self-antigen"),
                ("reactive-septic-mech-03.png", "T-cell attacking joint tissue directly"),
            ],
        },
        {
            "heading": "Still there: disseminated gonococcal infection",
            "body": (
                "Disseminated gonococcal infection runs the opposite path entirely. Neisseria "
                "gonorrhoeae breaches the mucosal barrier and gets directly into the bloodstream. "
                "Live bacteria, not primed T-cells, do the traveling. It develops in only 0.5 to "
                "3.0 percent of untreated gonococcal infections, but when it seeds a joint, it "
                "seeds it with the actual organism, and neutrophils flood in to fight a real, live "
                "infection."
            ),
            "images": [
                ("reactive-septic-knee-01.png", "Fully purulent joint fluid"),
            ],
        },
        {
            "heading": "The tap is what actually separates them",
            "body": (
                "Septic arthritis must be actively ruled out before reactive arthritis is "
                "diagnosed. That means a tap happens first, every time, even when the story sounds "
                "textbook for reactive arthritis. Gonococcal arthritis is the most common cause of "
                "septic arthritis in otherwise healthy young adults in the United States, and it's "
                "exactly the population that also gets reactive arthritis. The rule that holds "
                "regardless: assume septic until proven otherwise. Treating a sterile joint like "
                "it's infected costs a few unnecessary antibiotic days. Treating an infected joint "
                "like it's sterile costs cartilage, and sometimes the joint itself."
            ),
            "images": None,
        },
    ],
    "cta": {
        "title": "Have something specific to your case?",
        "desc": (
            "Get informed about your condition directly from a physician. "
            "No insurance required."
        ),
        "button": "Speak to a physician now",
        "note": (
            "This link will connect you with our telemedicine partner. "
            "(Placeholder in this demo build, pending final partner URL.)"
        ),
    },
}

if __name__ == "__main__":
    out = os.path.join(OUT_DIR, "reactive-vs-septic-arthritis-packet.pdf")
    path = build_case_study_pdf(REACTIVE_SEPTIC_CONFIG, out)
    print(f"Generated: {path}")
    print(f"Size: {os.path.getsize(path)} bytes")

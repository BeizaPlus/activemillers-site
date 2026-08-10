"""Generate the Wallenberg syndrome bibliography PDF, the free download offered
in exchange for an email address on case-study-wallenberg-syndrome.html.
"""
import os
from fpdf import FPDF

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(SITE_DIR, "downloads")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "wallenberg-bibliography.pdf")

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=20)

# Cover page
pdf.add_page()
pdf.set_fill_color(10, 10, 9)
pdf.rect(0, 0, 210, 297, "F")
pdf.set_text_color(255, 255, 255)
pdf.set_font("Helvetica", "B", 28)
pdf.set_xy(20, 100)
pdf.multi_cell(170, 12, "Wallenberg Syndrome", align="L")
pdf.set_font("Helvetica", "", 14)
pdf.set_xy(20, 130)
pdf.set_text_color(200, 200, 200)
pdf.multi_cell(170, 8, "Sources, Citations, and Rendering References", align="L")
pdf.set_xy(20, 260)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(150, 150, 150)
pdf.multi_cell(170, 6, "Steven Oppong, MD - Medical Illustrator\nactivemillers.com", align="L")

# Bibliography page
pdf.add_page()
pdf.set_text_color(20, 20, 20)
pdf.set_font("Helvetica", "B", 18)
pdf.cell(0, 12, "Bibliography and Source Citations", ln=True)
pdf.ln(4)

pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 8, "Anatomy and physiology reference", ln=True)
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 6,
    "Marieb, E. N. Human Anatomy & Physiology (Pearson, lecture edition, Chapter 8: The "
    "Nervous System). Cranial nerve nuclear locations in the medulla oblongata and pons; "
    "nucleus ambiguus as the shared motor nucleus for cranial nerves IX and X; ascending "
    "spinothalamic pathway crossing level.")
pdf.ln(4)

pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 8, "Documented clinical case", ln=True)
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 6,
    "\"Wallenberg Syndrome After Leg Day Training: A Case Report.\" PMC, 2026. "
    "PMC12634019. A previously healthy 40-year-old male developed right lateral "
    "medullary syndrome following a high-intensity resistance training session, with "
    "confirmed vertebral artery occlusion (V3 segment) on CT angiography and acute "
    "infarct of the right lateral medulla on MRI.")
pdf.ln(4)

pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 8, "Illustration 1: Lateral medullary cross-section", ln=True)
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 6,
    "Unreal Engine 5 photoreal cutaway render, built to the locked activemillers "
    "rendering standard (pure black background, no diagrammatic overlays, structures "
    "identifiable by real anatomical appearance and position). Depicts ischemic "
    "territory confined to the lateral medulla against healthy medial tissue.")
pdf.ln(4)

pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 8, "Illustration 2: Pyramidal decussation", ln=True)
pdf.set_font("Helvetica", "", 11)
pdf.multi_cell(0, 6,
    "Unreal Engine 5 photoreal render of the corticospinal tract crossing at the "
    "pyramidal decussation, showing the majority-crossed lateral corticospinal tract "
    "and minority-uncrossed anterior corticospinal tract, both terminating in spinal "
    "cord white matter only.")
pdf.ln(8)

pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(120, 120, 120)
pdf.multi_cell(0, 5,
    "This document is provided for educational reference alongside the case study "
    "published at activemillers.com. For questions or corrections, contact "
    "steven.oppong@gmail.com.")

pdf.output(OUT_PATH)
print(f"Generated: {OUT_PATH}")
print(f"Size: {os.path.getsize(OUT_PATH)} bytes")

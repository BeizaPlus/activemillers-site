# AGENTS.md — activemillers-site handoff (updated 2026-08-07)

## Deployment

```
cd C:\Users\steve\Personal Assistant\Beiza\activemillers-site
git add -A
git commit -m "message"
npx vercel --prod --yes
```

- **Branch:** `ceobranch`
- **GitHub:** `BeizaPlus/activemillers-site`
- **Vercel:** aliased to `https://www.activemillers.com`
- **Site:** static HTML files with embedded CSS + vanilla JS. No framework, no build step.
- `vercel.json` sets `framework: null`, static deploy.

## File structure (current)

```
Beiza/activemillers-site/
  global.css                                # SINGLE SOURCE: nav, footer, contact, cards, img border-radius, fade-in, responsive
  index.html                                # Homepage
  case-study-pulmonary-embolism.html        # PE case study
  case-study-pater-brown.html               # OB-GYN case study
  case-study-actinic-keratosis.html         # AK case study (2026-08-07)
  case-study-erythema-nodosum.html          # EN case study (2026-08-07)
  illustrated-pathology.html                # Book project page
  clean.html                                # old v2 static build, ignore
  vercel.json                               # static deploy config
  CNAME                                     # activemillers.com
  DEPLOY_HANDOFF.md                         # image map + deploy notes
  images/
    cross-section-anatomy.jpg               # hero bg + PE thumbnail
    the-dream.jpg                           # full-bleed between About+Experience
    HFtZcNIneFBJJZ7SfUHQJ1vsANc.png         # favicon
    crohn-crypt-abscess.jpg                 # Crohn's — crypt abscess neutrophil attack
    crohn-disease-3x3-grid.jpg              # Crohn's — 3x3 progression grid (not on page currently)
    erythema-nodosum-septal-panniculitis.png  # EN — wide tissue establishing shot
    erythema-nodosum-septal-infiltrate.png    # EN — tight septal infiltrate detail
    histiocyte-monocyte-extravasation.png     # not on page currently
    illustrated_pathology_book_cover.png      # not on page currently
    ischemic-colitis-watershed.jpg            # not on page currently
    kidney-sodium-calcium-stones.png          # Calcium stone formation card
    omega3-arachidonic-acid.jpg               # not on page currently
    prostacyclin-platelet-progression.jpg     # not on page currently
    actinic-keratosis/                        # 8 Immersa plates for AK case study
      01-establishing-skin-landscape.png      # Plate 8 (biopsy payoff) + homepage thumbnail
      02-dermal-epidermal-junction.png        # Plate 6 (solar elastosis)
      03-blood-interior-inflammation.png      # Plate 4 (granular layer thinning)
      04-keratinocyte-dysplasia.png           # Plate 2 (what the hand found)
      05-corneocyte-texture.png               # Plate 7 (the ones climbing)
      06-basal-layer-uv-damage.png            # Plate 3 (surface lies)
      07-mechanism-progression-grid.png       # Plate 5 (orderly rows broken)
      08-summit-sequence-grid.png             # Plate 1 (the skin — summit overview)
    case-studies/                             # illustrated-pathology chapter images
      chapter-aortic-dissection.png
      chapter-endocarditis.png
      chapter-sah.png
    pater-brown/                              # OB-GYN case images
      fetus-save-me.png
  videos/
    moon.mp4                                  # 7.3 MB, MoonSparse_v5
```

## Homepage card grid (current 2026-08-07)

2-column staggered (3 per column), matching Jonas Framer template rhythm:

| Left Column | Right Column (offset 60px) |
|---|---|
| Pulmonary Embolism (rect 5:3) | Actinic Keratosis (tall 3:4) |
| Erythema Nodosum (square 1:1) | OB-GYN Illustrations (square 1:1) |
| Calcium Stone Formation (square 1:1) | Crohn's Disease (square 1:1) |

**Card cards:** `border-radius: 16px`, card-title: 18px/600, card-cat: 14px/500. Gap: 40px, mobile: 16px single-column.

**Removed cards (2026-08-07):** Histiocyte Extravasation, Platelet Cascade, Ischemic Colitis, Omega-3 Pathway, Illustrated Pathology, duplicate Crohn's 3x3 grid.

## Key assets (quick lookup — outside activemillers-site)

| Asset | Absolute Path | Use |
|---|---|---|
| **Signature SVG** | `C:\Users\steve\Personal Assistant\assets\signature\signature-master.svg` | Steve's artist mark. Gold/tan #c7b191, calligraphic. Overlay on every finished medical illustration. |
| **Signature PNG** | `C:\Users\steve\Personal Assistant\assets\signature\signature-master.png` | Raster fallback. |
| **Signature style lock** | `C:\Users\steve\Personal Assistant\Beiza\activemillers-site\images\actinic-keratosis\18-final-block-silhouette-vessels.jpg` | Magnific style reference for all medical renders. |
| **Illustration ref area** | `C:\Users\steve\Personal Assistant\Beiza\activemillers-site\images\_ref_illustrations\` | Raw .ai / reference illustration files. |
| **Image rule** | `C:\Users\steve\Personal Assistant\.cursor\rules\immersa-medical-visuals.mdc` | Auto-applied on every image generation. Has signature + style sections. |

## Site sections (top to bottom)

1. **Nav** — fixed, mix-blend-mode: difference. Logo SVG inline. Links: "Pathology" (#pathology-anchor), "Experiments" (#experiments-anchor), "Contact"
2. **Hero** — full-viewport with `cross-section-anatomy.jpg` background at 85% opacity. H1: "I'm Steven, a medical illustrator that cares a great deal about first principles"
3. **Featured Work** grid (#experiments-anchor) — 2-column staggered grid. 6 cards (3 left, 3 right).
4. **About** — 4 paragraphs with bolded key phrases. Timeline: Artist, Doctor, Medical Illustrator, Pathology Residency (upcoming).
5. **Full-bleed image** — `the-dream.jpg`, 75vh.
6. **Experience** (#pathology-anchor) — 5 expandable accordion entries.
7. **Published Illustrations** — single column list (5 items).
8. **Contact CTA** — pill-shaped email button.
9. **Footer** — LinkedIn link, copyright 2026.

## Case study pages (standard structure)

Each case study follows the Jonas Framer template skeleton:
- Nav (same as homepage)
- Hero: title, subtitle, author credit
- Plates: alternating text/image pairs with thin dividers
- Closing: pathophysiology reference or outcome
- Other work: 2-card link grid
- Contact CTA + Footer

**AK page specific:** 8 plates, narrative patient-story format. 10-vertical-cross-section.png as full-width master plate after header.

## Design system

- **`global.css`** is the single source of truth for shared rules: nav (with blur gradient ::before), footer, contact CTA, `.ow-card`, `.fade-in`, `.img-wrap`, all responsive breakpoints, and **all image `border-radius: 16px`** via `img { border-radius: 16px; }`. Edit global.css once and the entire site updates.
- Dark theme: `#0a0a09` background, white text (`#e0ddd8` for case study body)
- Font: Inter (Google Fonts), system fallbacks
- Nav: fixed, transparent background. `::before` pseudo-element with `backdrop-filter: blur(16px)` gradient behind logo only (420px wide, fades right with mask-image)
- Section headings: 13px uppercase, opacity 0.5
- Responsive breakpoints: 1199px (tablet), 809px (mobile), 374px (small phone)
- Scroll fade-in: JS checks `window.innerHeight * 0.88`, adds `.visible` class
- Card hover: translateY(-4px)

## Writing rules (locked)

- **NO EM DASHES** anywhere. Use commas, periods, or colons.
- **Past tense** for completed-role bullets.
- **Pathology-relevant** filtering.
- **No fabrication** of names, programs, dates.

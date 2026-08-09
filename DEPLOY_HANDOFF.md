# Deploy Handoff — activemillers-site

Last updated: 2026-08-07

## Deploy command

```
cd "C:\Users\steve\Personal Assistant\Beiza\activemillers-site"
npx vercel --prod --yes
```

Aliased to: `https://www.activemillers.com`

## Key assets (quick lookup — same paths as AGENTS.md)

| Asset | Path | Use |
|---|---|---|
| **Signature SVG** | `assets/signature/signature-master.svg` | Steve artist mark. Gold/tan #c7b191. Overlay on finished illustrations. |
| **Signature PNG** | `assets/signature/signature-master.png` | Raster fallback. |
| **Illustration ref area** | `images/_ref_illustrations/` | Raw .ai ref files. |
| **Image rule** | `.cursor/rules/immersa-medical-visuals.mdc` | Auto-applied per generation. |

## Current page map

| Page | URL | Status |
|---|---|---|
| Homepage | `/index.html` | Live |
| PE case study | `/case-study-pulmonary-embolism.html` | Live |
| OB-GYN case study | `/case-study-pater-brown.html` | Live |
| Actinic Keratosis case study | `/case-study-actinic-keratosis.html` | Live (8 plates, 10 images) |
| Erythema Nodosum case study | `/case-study-erythema-nodosum.html` | Live (3 images, panniculitis narrative) |
| Illustrated Pathology book | `/illustrated-pathology.html` | Live (3D book mockup) |

## Homepage card grid (2026-08-07)

2-column staggered (3 left, 3 right):

| Left | Right |
|---|---|
| Pulmonary Embolism | Actinic Keratosis |
| Erythema Nodosum | OB-GYN Illustrations |
| Calcium Stone Formation | Crohn's Disease |

## Image sources

### Erythema Nodosum
| File | Source | Role |
|---|---|---|
| `erythema-nodosum-septal-panniculitis.png` | Magnific | Wide tissue establishing: fat lobules + inflamed septa |
| `erythema-nodosum-septal-infiltrate.png` | Magnific | Tight detail: neutrophilic infiltrate within septum |

### Crohn's Disease
| File | Source | Role |
|---|---|---|
| `crohn-crypt-abscess.jpg` | Magnific (`yiNmBaLPW9`) | Crypt abscess, neutrophil attack in intestinal crypt |

### Calcium Stone Formation
| File | Source | Role |
|---|---|---|
| `kidney-sodium-calcium-stones.png` | Magnific | Sodium-forcing-calcium precipitation, renal tubule crystals |

### Actinic Keratosis (8 Immersa plates)
All under `images/actinic-keratosis/`, copied from Downloads Magnific renders. See `AGENTS.md` for full plate mapping.

## Background color

- `#0a0a09` (black) — all pages

## Cards not yet live

These images exist in `images/` but are not on the homepage grid:

- `histiocyte-monocyte-extravasation.png` — removed (duplicate of erythema nodosum image)
- `prostacyclin-platelet-progression.jpg` — removed (not ready)
- `ischemic-colitis-watershed.jpg` — removed (wrong image, actually calcium stones)
- `omega3-arachidonic-acid.jpg` — removed (not ready)
- `illustrated_pathology_book_cover.png` — removed (book project on hold)
- `crohn-disease-3x3-grid.jpg` — kept off-grid (will go into Crohn's case study page)

## Pending

- **PE page:** `pe-progression-3.png` to be replaced with video later
- **Crohn's Disease**: case study page needed
- **Calcium Stone Formation**: case study page needed (Vitamin C, sodium-calcium correlation)

## Design system

- **`global.css`** — single source of truth for shared rules across all 6 pages. Nav (blur gradient behind logo), footer, contact CTA, `.ow-card`, `.fade-in`, `.img-wrap`, all responsive breakpoints, and `img { border-radius: 16px; }`. Edit once, entire site updates.
- All inline styles stripped of duplicated global rules (2026-08-07). Each page keeps only its layout-specific CSS.

# AGENTS.md — activemillers-site handoff

## Deployment

```
cd C:\Users\steve\Personal Assistant\Beiza\activemillers-site
git add index.html
git commit -m "message"
git push
npx vercel --prod --yes
```

- **Branch:** `ceobranch`
- **GitHub:** `BeizaPlus/activemillers-site`
- **Vercel:** aliased to `https://www.activemillers.com`
- **Site:** single static `index.html` with embedded CSS + vanilla JS. No framework, no build step.
- `vercel.json` sets `framework: null`, static deploy.

## File structure

```
Beiza/activemillers-site/
  index.html          # THE site (only file you edit)
  clean.html          # old v2 static build, ignore
  vercel.json         # static deploy config
  CNAME               # activemillers.com
  images/             # all assets
    cross-section-anatomy.jpg  # hero bg
    the-dream.jpg              # full-bleed image between About+Experience
    actinic-keratosis.jpg      # work grid card
    HFtZcNIneFBJJZ7SfUHQJ1vsANc.png  # favicon
    activemillers-logo.svg     # unused (logo embedded inline in nav)
  videos/
    moon.mp4           # 7.3 MB, MoonSparse_v5, linked via lightbox from About text
```

## Site sections (top to bottom)

1. **Nav** — fixed, mix-blend-mode: difference. Logo SVG inline. Links: "Pathology" (#pathology-anchor), "Experiments" (#experiments-anchor)
2. **Hero** — full-viewport with `cross-section-anatomy.jpg` background at 85% opacity. H1: "I'm Steven, a medical illustrator that cares a great deal about first principles"
3. **Featured Work** grid (#experiments-anchor) — 2-column masonry. Currently: Cross-Section Anatomy Study, Actinic Keratosis, plus Coming Soon placeholders. Dark cards on black bg.
4. **About** — 4 paragraphs with bolded key phrases. "decades of practice" is a clickable link → opens moon video in lightbox overlay.
5. **Full-bleed image** — `the-dream.jpg`, 75vh, no padding. Between About and Experience.
6. **Experience** (#pathology-anchor) — 5 expandable accordion entries (see below).
7. **Published Illustrations** — single column list (5 items).
8. **Contact CTA** — pill-shaped email button → steven.oppong@gmail.com
9. **Footer** — LinkedIn link only (kwabena-oppong-904a3440), copyright 2026

## Experience entries (current state)

All use bullet lists, identical styling. Chevron icon is absolutely positioned to the left so title text aligns with section headings. `exp-next` class on Pathology Residency dims it (opacity 0.6, italic subtitle).

1. **Atelier ActiveWorks** (2008–2025)
   Subtitle: Junior Creative Artist → Co-Founder & Creative Director
   Bullets: 2 (visual precision foundation, anatomy workbooks)

2. **Doctor of Medicine** (2012–2018)
   Subtitle: Kwame Nkrumah University of Science & Technology
   Bullets: 4 (MBChB, pathology rotations, 2 awards)
   Nested sub-entry: Pathology House Officer (2018–2020, Teaching Hospital Ghana) — 4 bullets

3. **Medical Illustrator** (2016–present)
   Subtitle: Freelance & Contract
   Bullets: 3 (translated concepts, appendicitis for Dept of Surgery KNUST, labor partograph for Ruma Fertility)

4. **Pathology Residency** (upcoming, no date)
   Subtitle: Next chapter: pursuing residency in Pathology (italic, dimmed)
   Bullets: 4 (forward-looking aspirational framing)

5. **Professional Associations** (no date)
   Subtitle: Memberships & Affiliations
   Bullets: 7 organizations

## Writing rules (locked)

- **NO EM DASHES** anywhere. Use commas, periods, or colons instead. Only exception: "Ghana Physician & Surgeons Foundation — North America" (proper name).
- **Past tense** for all completed-role bullets.
- **Pathology-relevant** filtering: every bullet should answer "why does this matter to a pathology program director."
- **No fabrication** of institution names, program names, or dates.

## Lightbox video

- "decades of practice" in About section links to `videos/moon.mp4`
- Opens in fullscreen dark overlay (`#videoLightbox`)
- X button OR clicking background closes lightbox AND pauses video
- JS functions: `openVideo(e)`, `closeVideo(e)`

## Design system

- Dark theme: `#0a0a09` background, white text
- Font: Inter (Google Fonts), system fallbacks
- Section headings: 13px uppercase, opacity 0.5
- Bullet lists: `list-style: disc`, `padding-left: 20px`, `opacity: 0.6`, `line-height: 1.8`
- Responsive breakpoints: 1199px (tablet), 809px (mobile), 374px (small phone)
- Scroll fade-in: JS checks `window.innerHeight * 0.85`, adds `.visible` class
- Max content width: 900px (exp-inner), 1000px (two-col-inner)

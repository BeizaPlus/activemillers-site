# activemillers-site — AGENTS.md

Static portfolio site for Steven Oppong, MD (Medical Illustrator).

## Repo & Deploy

| Detail | Value |
|---|---|
| Repo | `github.com/BeizaPlus/activemillers-site` |
| Live URL | `https://www.activemillers.com` |
| Hosting | Vercel (team: `beizas-projects`, user: `beizaplus`) |
| Domain | `activemillers.com` (Vercel DNS — CNAME → `cname.vercel-dns.com`) |
| Framework | None (static HTML/CSS/JS, no build step) |

## Deploying

**The reliable method — direct deploy from local files (not git push):**

```powershell
cd "C:\Users\steve\Personal Assistant\Beiza\activemillers-site"
npx vercel --prod --yes
```

This uploads the folder directly to Vercel (bypasses git). Always use this instead of relying on git-push auto-deploys, which have been unreliable for this project.

**If you want to push to both branches anyway:**

```powershell
git add -A
git commit -m "message"
git push origin main
git push origin ceobranch
```

But always follow with `npx vercel --prod --yes` to be sure.

## Local dev

```powershell
npx serve "C:\Users\steve\Personal Assistant\Beiza\activemillers-site" -l 3456 --no-clipboard
```

Then open `http://localhost:3456`.

## File structure

```
activemillers-site/
├── index.html              # Static single-page site (the rebuild)
├── index_framer_backup.html # Original Framer SPA (do not delete)
├── clean.html              # Same as index.html (dev copy)
├── images/                 # All image assets
│   ├── cross-section-anatomy.jpg  # Hero overlay + work card
│   ├── the-dream.jpg              # Work card + full-bleed section
│   ├── actinic-keratosis.jpg      # Work card
│   ├── activemillers-logo.svg     # Nav logo (red + white)
│   └── ...                        # Original Framer scraped images
├── sites/                  # Old Framer JS bundles (inert, kept for reference)
├── vercel.json             # { "framework": null, "outputDirectory": "." }
└── AGENTS.md               # This file
```

## Editing the site

The site is a single static HTML file. All styling is in a `<style>` block in the `<head>`. Sections are marked with `<!-- ===== NAME ===== -->` comments.

**Section order:**
1. NAV — fixed top nav with logo + Work/About/Contact links
2. HERO — headline + heart anatomy background image
3. WORK — two-column flex grid (Left: 3 cards, Right: 3 cards), dark theme
4. ABOUT — two-column grid (35/65), heading left, paragraphs right
5. FULL IMAGE — the-dream.jpg, full-bleed, 75vh
6. EXPERIENCE — vertically centered, 3 entries
7. SERVICES + CLIENTS — two-column flex list
8. CONTACT CTA — centered heading + email pill button
9. FOOTER — social links + copyright

**Responsive breakpoints:**
- Desktop: 1200px+
- Tablet: 810px–1199px
- Mobile: 375px–809px
- Small phone: ≤374px (iPhone SE)

**Colors:**
- Page background: `#0a0a09`
- Card backgrounds: `#141414`
- Text: white, dimmed at various opacities
- Red accent (logo): `#e60021`

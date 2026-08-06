# Deploy Handoff -- PE Case Study

## Command

```
cd "c:\Users\steve\Personal Assistant\Beiza\activemillers-site" && npx vercel --prod --yes
```

## Current image state (2026-08-05)

| Slot | File | Source |
|---|---|---|
| Two-image row left | `pe-panel-2.png` | Original |
| Two-image row right | `pe-rv-strain.png` | `Heart_Section_SVCfull-4K-v2.png` (Magnific 4K, v2) |
| Stacked 1 | `pe-progression-1.png` | Same as `pe-rv-strain` (v2 SVC heart) |
| Stacked 2 | `pe-progression-2.png` | Magnific 4K clean (no annotations) |
| Stacked 3 | `pe-progression-3.png` | `pe-progression-3-4K-v2.png` (fixed clot/SVC blend) |

## Pending

- **`pe-progression-3.png` will be replaced with a video later.** Do not overwrite with a static image when the video arrives; swap the `<img>` for a `<video>` element in the HTML.

## Color

- Both homepage and case study page: `#0a0a09` (black)

## Target

https://www.activemillers.com/case-study-pulmonary-embolism.html

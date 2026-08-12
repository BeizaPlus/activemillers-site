"""Crop pe-panel-2.png and pe-rv-strain.png to square, tight around the heart,
removing the dead black space Steve flagged in the image-row on the PE article.
Density-based bbox detection (not pure min/max) so faint background artifacts
(reflection planes, ambient occlusion) don't drag the crop wider than the
actual heart mass. Expands to a centered square, shrinking the side rather
than distorting if the padded box can't fit within the source dimensions."""
from PIL import Image
import numpy as np

SITE = r"C:\Users\steve\Personal Assistant\Beiza\activemillers-site"

JOBS = [
    ("images/case-studies/pe-panel-2.png", "images/case-studies/pe-panel-2-square.png", 0.16, 20, 0.01),
    ("images/case-studies/pe-rv-strain.png", "images/case-studies/pe-rv-strain-square.png", 0.05, 20, 0.01),
]


def density_bbox(mask, row_frac, col_frac):
    h, w = mask.shape
    row_density = mask.sum(axis=1) / w
    col_density = mask.sum(axis=0) / h
    rows = np.where(row_density > row_frac)[0]
    cols = np.where(col_density > col_frac)[0]
    return cols.min(), rows.min(), cols.max(), rows.max()


def crop_square(src, dst, pad_frac, threshold, density_frac):
    im = Image.open(src).convert("RGB")
    arr = np.asarray(im)
    luminance = arr.max(axis=2)
    mask = luminance > threshold

    x0, y0, x1, y1 = density_bbox(mask, density_frac, density_frac)
    w, h = x1 - x0, y1 - y0

    pad_x = int(w * pad_frac)
    pad_y = int(h * pad_frac)
    x0 -= pad_x; x1 += pad_x
    y0 -= pad_y; y1 += pad_y

    W, H = im.size
    side = min(max(x1 - x0, y1 - y0), W, H)
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2

    left = int(cx - side / 2)
    top = int(cy - side / 2)
    left = max(0, min(left, W - side))
    top = max(0, min(top, H - side))
    right = left + side
    bottom = top + side

    cropped = im.crop((left, top, right, bottom))
    cropped.save(dst)
    print(f"{src}: original {im.size}, bbox {(x0,y0,x1,y1)}, square side {side} at ({left},{top}) -> {cropped.size} -> {dst}")


for src, dst, pad, thr, dens in JOBS:
    crop_square(f"{SITE}/{src}", f"{SITE}/{dst}", pad, thr, dens)

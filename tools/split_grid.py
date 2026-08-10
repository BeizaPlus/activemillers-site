"""Split grid-composite images (2x2, 3x3, etc.) into individual cells.
Usage: python split_grid.py <input> <rows> <cols> [--output-dir <dir>] [--prefix <name>]
Example: python split_grid.py tb-scrofula-hero.jpg 2 2 --prefix tb-scrofula
"""
import os, sys
from PIL import Image

def split_grid(input_path, rows, cols, output_dir=None, prefix=None):
    img = Image.open(input_path)
    w, h = img.size
    cell_w, cell_h = w // cols, h // rows

    if output_dir is None:
        output_dir = os.path.dirname(input_path) or '.'
    if prefix is None:
        base = os.path.splitext(os.path.basename(input_path))[0]
        prefix = base

    ext = os.path.splitext(input_path)[1] or '.jpg'
    if ext.lower() == '.jpeg': ext = '.jpg'

    saved = []
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c + 1
            left, upper = c * cell_w, r * cell_h
            right, lower = left + cell_w, upper + cell_h
            cell = img.crop((left, upper, right, lower))
            fname = f"{prefix}-{idx:02d}{ext}"
            out_path = os.path.join(output_dir, fname)
            cell.save(out_path, quality=95)
            saved.append(out_path)
            print(f"  -> {fname}  ({cell.size[0]}x{cell.size[1]})")

    print(f"Split {os.path.basename(input_path)} ({w}x{h}) into {rows}x{cols} = {len(saved)} cells")
    return saved

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    rows = int(sys.argv[2])
    cols = int(sys.argv[3])
    output_dir = None
    prefix = None

    args = sys.argv[4:]
    i = 0
    while i < len(args):
        if args[i] == '--output-dir' and i+1 < len(args):
            output_dir = args[i+1]; i += 2
        elif args[i] == '--prefix' and i+1 < len(args):
            prefix = args[i+1]; i += 2
        else:
            i += 1

    split_grid(input_path, rows, cols, output_dir=output_dir, prefix=prefix)

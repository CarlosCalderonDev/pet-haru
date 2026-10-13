#!/usr/bin/env python3
"""Extract the populated cells from Haru's validated v2 atlas."""

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "assets" / "sprites" / "haru-urara-spritesheet.png"
OUTPUT = ROOT / "assets" / "frames"
CELL_W, CELL_H = 192, 208
ROWS = [
    ("idle", 6),
    ("running-right", 8),
    ("running-left", 8),
    ("waving", 4),
    ("jumping", 5),
    ("failed", 8),
    ("waiting", 6),
    ("running", 6),
    ("review", 6),
    ("look-a", 8),
    ("look-b", 8),
]


def main() -> None:
    with Image.open(ATLAS) as opened:
        atlas = opened.convert("RGBA")
        if atlas.size != (1536, 2288):
            raise SystemExit(f"Unexpected atlas size: {atlas.size}")
        for row, (state, count) in enumerate(ROWS):
            state_dir = OUTPUT / state
            state_dir.mkdir(parents=True, exist_ok=True)
            for col in range(count):
                box = (col * CELL_W, row * CELL_H, (col + 1) * CELL_W, (row + 1) * CELL_H)
                atlas.crop(box).save(state_dir / f"{col:02d}.png")


if __name__ == "__main__":
    main()


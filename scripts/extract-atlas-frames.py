#!/usr/bin/env python3
"""Extract populated cells from the canonical atlas."""

from PIL import Image

from generate_previews import extract_frames
from pet_config import sprite_settings


def main() -> None:
    atlas_path, _, _, cell_w, cell_h, counts = sprite_settings()
    with Image.open(atlas_path) as opened:
        extract_frames(opened.convert("RGBA"), cell_w, cell_h, counts)


if __name__ == "__main__":
    main()

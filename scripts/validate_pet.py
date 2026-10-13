#!/usr/bin/env python3
"""Validate the canonical atlas and emit a machine-readable QA report."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops

from pet_config import METADATA_PATH, ROOT, STATES, load_metadata, sprite_settings


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    return image.getchannel("A").getbbox()


def frame_digest(image: Image.Image) -> str:
    return hashlib.sha256(image.tobytes()).hexdigest()


def validate(update_metadata: bool = False) -> dict:
    atlas_path, width, height, cell_w, cell_h, frames_per_row = sprite_settings()
    metadata = load_metadata()
    errors: list[str] = []
    warnings: list[str] = []
    states: dict[str, dict] = {}

    raw = atlas_path.read_bytes()
    sha256 = hashlib.sha256(raw).hexdigest()
    stored_sprite = metadata["spritesheet"]
    if not update_metadata and stored_sprite.get("sha256") != sha256:
        errors.append("stored spritesheet SHA-256 does not match the canonical file")
    if not update_metadata and stored_sprite.get("file_size_bytes") != len(raw):
        errors.append("stored spritesheet size does not match the canonical file")
    if len(frames_per_row) != len(STATES):
        errors.append("frames_per_row does not match the number of declared states")

    with Image.open(atlas_path) as opened:
        atlas = opened.convert("RGBA")
        if atlas.size != (width, height):
            errors.append(f"atlas is {atlas.size}, expected {(width, height)}")
        columns = width // cell_w
        rows = height // cell_h
        seen: dict[str, str] = {}

        for row, (state, count) in enumerate(zip(STATES, frames_per_row)):
            boxes: list[tuple[int, int, int, int] | None] = []
            bottoms: list[int] = []
            duplicates: list[str] = []
            frames: list[Image.Image] = []
            for col in range(columns):
                box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
                frame = atlas.crop(box)
                bbox = alpha_bbox(frame)
                if col < count:
                    if bbox is None:
                        errors.append(f"{state}/{col:02d} is unexpectedly empty")
                        continue
                    boxes.append(bbox)
                    bottoms.append(bbox[3])
                    digest = frame_digest(frame)
                    label = f"{state}/{col:02d}"
                    if digest in seen:
                        duplicates.append(f"{label} duplicates {seen[digest]}")
                    else:
                        seen[digest] = label
                    frames.append(frame)
                    derived_path = ROOT / "assets" / "frames" / state / f"{col:02d}.png"
                    if not derived_path.exists():
                        errors.append(f"derived frame is missing: {derived_path.relative_to(ROOT)}")
                    else:
                        with Image.open(derived_path) as derived_opened:
                            derived = derived_opened.convert("RGBA")
                        if ImageChops.difference(frame, derived).getbbox() is not None:
                            errors.append(f"derived frame is stale: {derived_path.relative_to(ROOT)}")
                elif bbox is not None:
                    errors.append(f"unused cell row {row}, column {col} is not transparent")

            ground_spread = max(bottoms) - min(bottoms) if bottoms else 0
            if state not in {"jumping", "look-a", "look-b"} and ground_spread > 12:
                warnings.append(f"{state} ground line varies by {ground_spread}px")
            if duplicates:
                warnings.extend(duplicates)

            loop_delta = None
            if len(frames) > 1:
                histogram = ImageChops.difference(frames[0], frames[-1]).convert("L").histogram()
                loop_delta = round(sum(level * count for level, count in enumerate(histogram)) / (cell_w * cell_h), 2)

            states[state] = {
                "frames": count,
                "alpha_bounds": boxes,
                "ground_line_spread_px": ground_spread,
                "loop_endpoint_delta": loop_delta,
            }

    if update_metadata:
        sprite = metadata["spritesheet"]
        sprite["file_size_bytes"] = len(raw)
        sprite["sha256"] = sha256
        sprite["validated"] = not errors
        METADATA_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = {
        "valid": not errors,
        "file_size_bytes": len(raw),
        "sha256": sha256,
        "mime_type": "image/png",
        "width": width,
        "height": height,
        "sprite_version": metadata["spritesheet"]["version"],
        "cell_width": cell_w,
        "cell_height": cell_h,
        "frames_per_row": frames_per_row,
        "states": states,
        "warnings": warnings,
        "errors": errors,
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update-metadata", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "qa" / "validation.json")
    args = parser.parse_args()
    report = validate(update_metadata=args.update_metadata)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Validation: {'PASS' if report['valid'] else 'FAIL'}")
    print(f"Warnings: {len(report['warnings'])}; errors: {len(report['errors'])}")
    raise SystemExit(0 if report["valid"] else 1)


if __name__ == "__main__":
    main()

"""Shared project metadata loaded from docs/pet.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "docs" / "pet.json"


def load_metadata() -> dict:
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def sprite_settings() -> tuple[Path, int, int, int, int, list[int]]:
    metadata = load_metadata()
    sprite = metadata["spritesheet"]
    return (
        ROOT / sprite["path"],
        sprite["width"],
        sprite["height"],
        sprite["cell_width"],
        sprite["cell_height"],
        sprite["frames_per_row"],
    )


STATES = [
    "idle",
    "running-right",
    "running-left",
    "waving",
    "jumping",
    "failed",
    "waiting",
    "running",
    "review",
    "look-a",
    "look-b",
]

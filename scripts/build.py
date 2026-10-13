#!/usr/bin/env python3
"""Rebuild all derived assets and validate the canonical sprite sheet."""

from __future__ import annotations

import json

from generate_previews import main as generate_previews
from pet_config import ROOT
from validate_pet import validate


def main() -> None:
    generate_previews()
    report = validate(update_metadata=True)
    output = ROOT / "qa" / "validation.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Validation: {'PASS' if report['valid'] else 'FAIL'}")
    print(f"Warnings: {len(report['warnings'])}; errors: {len(report['errors'])}")
    if not report["valid"]:
        raise SystemExit(1)
    print("Build completed successfully.")


if __name__ == "__main__":
    main()

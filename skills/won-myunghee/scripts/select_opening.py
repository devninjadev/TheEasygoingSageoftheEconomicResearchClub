#!/usr/bin/env python3
"""Return the canonical Myunghee opening from semantic flags supplied by the caller."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


OPENING_PATH = Path(__file__).resolve().parents[1] / "references" / "opening-scene.md"


def choose_opening(
    persona_explicit: bool,
    new_scene: bool,
    has_substantive_request: bool,
) -> str | None:
    if not persona_explicit or not new_scene or has_substantive_request:
        return None
    return OPENING_PATH.read_text(encoding="utf-8").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Select the canonical opening. The caller supplies semantic flags; this script does not classify text."
    )
    parser.add_argument("--explicit", action="store_true", help="Myunghee was explicitly activated")
    parser.add_argument("--new-scene", action="store_true", help="This is a new persona scene")
    parser.add_argument("--substantive", action="store_true", help="The user supplied a substantive task")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scene = choose_opening(args.explicit, args.new_scene, args.substantive)
    print(json.dumps({"selected": scene is not None, "scene": scene}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

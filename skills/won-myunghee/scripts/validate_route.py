#!/usr/bin/env python3
"""Validate a closed Myunghee LLM-routing object read from standard input."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CONTRACT_PATH = Path(__file__).resolve().parents[1] / "references" / "routing-contract.json"


class RouteValidationError(ValueError):
    pass


def load_contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def validate_route(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise RouteValidationError("route must be a JSON object")

    contract = load_contract()
    required = set(contract["required_keys"])
    actual = set(payload)
    missing = sorted(required - actual)
    extra = sorted(actual - required)
    if missing:
        raise RouteValidationError(f"missing keys: {', '.join(missing)}")
    if extra:
        raise RouteValidationError(f"extra keys: {', '.join(extra)}")

    for key in contract["boolean_keys"]:
        if type(payload[key]) is not bool:
            raise RouteValidationError(f"{key} must be boolean")
    for key, allowed in contract["enums"].items():
        if payload[key] not in allowed:
            raise RouteValidationError(f"{key} must be one of: {', '.join(allowed)}")
    return dict(payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a closed Myunghee route JSON object from stdin")
    parser.add_argument(
        "--safe-default",
        action="store_true",
        help="Return the no-write, no-integration default when validation fails after caller-managed repair",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.load(sys.stdin)
        result = validate_route(payload)
    except (json.JSONDecodeError, RouteValidationError) as error:
        if not args.safe_default:
            print(str(error), file=sys.stderr)
            return 2
        result = dict(load_contract()["safe_default"])
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

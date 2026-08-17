from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "validate_route.py"
FIXTURES = json.loads((Path(__file__).parent / "fixtures" / "routing-cases.json").read_text(encoding="utf-8"))


def validate(
    test: unittest.TestCase,
    payload: object,
    *,
    safe_default: bool = False,
    missing_message: str = "closed routing validator absent: semantic route contract is not enforced",
) -> subprocess.CompletedProcess[str]:
    test.assertTrue(
        SCRIPT.is_file(),
        missing_message,
    )
    command = [sys.executable, str(SCRIPT)]
    if safe_default:
        command.append("--safe-default")
    return subprocess.run(
        command,
        input=json.dumps(payload, ensure_ascii=False),
        capture_output=True,
        text=True,
    )


class RoutingContractTests(unittest.TestCase):
    def test_valid_closed_route_round_trips(self) -> None:
        expected = FIXTURES["valid"]
        completed = validate(self, expected)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout), expected)

    def test_extra_key_and_unknown_enum_are_rejected(self) -> None:
        extra = {**FIXTURES["valid"], "reasoning": "hidden"}
        completed = validate(self, extra)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("extra keys", completed.stderr)

        unknown = {**FIXTURES["valid"], "conversation_mode": "urgent_alpha"}
        completed = validate(self, unknown)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("conversation_mode", completed.stderr)

    def test_remember_phrase_does_not_authorize_world_memory_write(self) -> None:
        fixture = FIXTURES["remember_only"]
        self.assertIn("기억해 둬", fixture["prompt"])
        completed = validate(
            self,
            fixture["route"],
            missing_message="World Memory write boundary absent: 기억해 둬 must keep write_intent none",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertFalse(result["needs_world_memory"])
        self.assertEqual(
            result["write_intent"],
            "none",
            "World Memory write boundary violated: 기억해 둬 is not explicit write authority",
        )

    def test_safe_default_disables_integrations_image_and_writes(self) -> None:
        completed = validate(self, {"broken": True}, safe_default=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertFalse(result["needs_world_memory"])
        self.assertFalse(result["needs_market_news"])
        self.assertFalse(result["needs_portfolio_advisor"])
        self.assertFalse(result["needs_image"])
        self.assertEqual(result["write_intent"], "none")


if __name__ == "__main__":
    unittest.main()

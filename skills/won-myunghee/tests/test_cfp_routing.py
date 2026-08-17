from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "validate_route.py"
FIXTURES = json.loads((Path(__file__).parent / "fixtures" / "routing-cases.json").read_text(encoding="utf-8"))


class CfpRoutingTests(unittest.TestCase):
    def validate(self, payload: object) -> dict[str, object]:
        self.assertTrue(
            SCRIPT.is_file(),
            "CFP route validator absent: freshness and jurisdiction cannot be enforced",
        )
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps(payload, ensure_ascii=False),
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def test_retirement_route_requires_current_korean_official_evidence(self) -> None:
        result = self.validate(FIXTURES["retirement"])
        self.assertEqual(result["request_class"], "retirement")
        self.assertEqual(result["jurisdiction"], "KR")
        self.assertEqual(result["freshness_requirement"], "official_current")

    def test_tax_route_requires_current_korean_official_evidence(self) -> None:
        result = self.validate(FIXTURES["tax"])
        self.assertEqual(result["request_class"], "tax")
        self.assertEqual(result["jurisdiction"], "KR")
        self.assertEqual(result["freshness_requirement"], "official_current")

    def test_insurance_route_requires_current_korean_official_evidence(self) -> None:
        result = self.validate(FIXTURES["insurance"])
        self.assertEqual(result["request_class"], "insurance")
        self.assertEqual(result["jurisdiction"], "KR")
        self.assertEqual(result["freshness_requirement"], "official_current")


if __name__ == "__main__":
    unittest.main()

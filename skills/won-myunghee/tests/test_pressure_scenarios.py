from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from types import ModuleType


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = json.loads((Path(__file__).parent / "pressure-scenarios.json").read_text(encoding="utf-8"))


def load_opening_module(test: unittest.TestCase) -> ModuleType:
    script = SKILL_ROOT / "scripts" / "select_opening.py"
    test.assertTrue(script.is_file(), "pressure contract failed: substantive request opening gate is absent")
    spec = importlib.util.spec_from_file_location("won_myunghee_pressure_opening", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PressureScenarioTests(unittest.TestCase):
    def test_fixture_covers_approved_red_pressure_scenarios(self) -> None:
        identifiers = {scenario["id"] for scenario in SCENARIOS}
        self.assertEqual(
            identifiers,
            {
                "explicit-toggle",
                "generic-finance-does-not-activate",
                "substantive-request-skips-opening",
                "remember-is-not-write-authority",
                "relationship-point-of-view",
                "signature-quotation-canon",
                "safe-default",
            },
        )

    def test_substantive_request_pressure_case_returns_no_opening(self) -> None:
        scenario = next(item for item in SCENARIOS if item["id"] == "substantive-request-skips-opening")
        self.assertIsNone(scenario["expected"]["opening"])
        module = load_opening_module(self)
        self.assertIsNone(module.choose_opening(True, True, True))

    def test_signature_pressure_case_keeps_persona_canons_disjoint(self) -> None:
        scenario = next(item for item in SCENARIOS if item["id"] == "signature-quotation-canon")
        self.assertEqual(scenario["expected"]["representative"], ["워런 버핏", "레이 달리오"])
        self.assertEqual(scenario["expected"]["not_representative"], ["조지 소로스", "스탠리 드러켄밀러"])
        registry = SKILL_ROOT / "references" / "source-registry.md"
        self.assertTrue(
            registry.is_file(),
            "pressure contract failed: Buffett+Dalio registry absent, so persona source separation is unenforced",
        )


if __name__ == "__main__":
    unittest.main()

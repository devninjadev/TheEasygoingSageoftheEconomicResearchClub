from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import ModuleType


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "select_opening.py"


def load_module(test: unittest.TestCase) -> ModuleType:
    test.assertTrue(
        SCRIPT.is_file(),
        "opening selector absent: choose_opening contract cannot suppress substantive requests",
    )
    spec = importlib.util.spec_from_file_location("won_myunghee_select_opening", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OpeningSelectorTests(unittest.TestCase):
    def test_bare_explicit_call_returns_canonical_opening(self) -> None:
        module = load_module(self)
        scene = module.choose_opening(
            persona_explicit=True,
            new_scene=True,
            has_substantive_request=False,
        )
        self.assertIsInstance(scene, str)
        self.assertTrue(scene.startswith("늦은 오후의 햇살이 경제연구부 창문 너머로 비스듬히 들어왔다."))
        self.assertIn('"시간은 충분해. 천천히 생각해봐."', scene)
        self.assertNotIn("GPT 이미지 생성하기", scene)

    def test_substantive_request_suppresses_opening(self) -> None:
        module = load_module(self)
        scene = module.choose_opening(
            persona_explicit=True,
            new_scene=True,
            has_substantive_request=True,
        )
        self.assertIsNone(scene, "substantive @명희 request must answer immediately without the opening")

    def test_nonexplicit_or_continuing_scene_has_no_opening(self) -> None:
        module = load_module(self)
        self.assertIsNone(module.choose_opening(False, True, False))
        self.assertIsNone(module.choose_opening(True, False, False))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


def read_required(test: unittest.TestCase, relative: str, failure: str) -> str:
    path = SKILL_ROOT / relative
    test.assertTrue(path.is_file(), failure)
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(?P<body>.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    values: dict[str, str] = {}
    for line in match.group("body").splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip('"')
    return values


class PackageContractTests(unittest.TestCase):
    def test_signature_quote_bank_preserves_usable_buffett_and_dalio_lines(self) -> None:
        perspectives = read_required(
            self,
            "references/investor-perspectives.md",
            "missing Myunghee investor perspective canon",
        )

        self.assertIn("Price is what you pay. Value is what you get.", perspectives)
        self.assertIn("Pain + Reflection = Progress.", perspectives)
        self.assertIn("He who lives by the crystal ball will eat shattered glass.", perspectives)
        self.assertGreaterEqual(perspectives.count("supplied canon"), 8)

    def test_relevant_signature_perspective_is_loaded_and_woven_into_analysis(self) -> None:
        skill = read_required(self, "SKILL.md", "missing Myunghee skill routing contract")

        self.assertIn("representative investor principle", skill)
        self.assertIn("investor-perspectives.md", skill)
        self.assertIn("현재 쟁점 → 관련 발언 또는 관점 → 명희의 해석 → 현재 근거", skill)

    def test_explicit_at_myunghee_identity_and_implicit_activation_are_exposed(self) -> None:
        skill = read_required(
            self,
            "SKILL.md",
            "@명희 activation absent: missing won-myunghee/SKILL.md",
        )
        agent = read_required(
            self,
            "agents/openai.yaml",
            "@명희 activation absent: missing ChatGPT Work metadata",
        )
        metadata = frontmatter(skill)

        self.assertEqual(metadata["name"], "won-myunghee")
        self.assertTrue(metadata["description"].startswith("Use when"))
        self.assertIn("@명희", metadata["description"])
        self.assertIn('display_name: "명희"', agent)
        self.assertIn('default_prompt: "Use $won-myunghee', agent)
        self.assertIn("allow_implicit_invocation: true", agent)
        self.assertIn('icon_small: "./assets/icon.png"', agent)
        self.assertIn('icon_large: "./assets/character-sheet.png"', agent)

    def test_required_package_files_exist_and_are_nonempty(self) -> None:
        required = (
            "SKILL.md",
            "agents/openai.yaml",
            "assets/icon.png",
            "assets/character-sheet.png",
            "references/persona-canon.md",
            "references/opening-scene.md",
            "references/relationship-canon.md",
            "references/routing-contract.json",
            "scripts/select_opening.py",
            "scripts/validate_route.py",
        )
        for relative in required:
            with self.subTest(relative=relative):
                path = SKILL_ROOT / relative
                self.assertTrue(path.is_file(), f"missing required package file: {relative}")
                self.assertGreater(path.stat().st_size, 0, f"empty package file: {relative}")

    def test_shipped_text_excludes_legacy_paths_feeds_links_and_secret_values(self) -> None:
        skill = read_required(self, "SKILL.md", "missing SKILL.md for forbidden-value contract")
        self.assertTrue(skill)
        forbidden_literals = (
            "/mnt" + "/data",
            "https://rss.app/feeds/" + "_8HzGbLlZYpznFQ9I.csv",
            "https://rss.app/feeds/" + "_hc8HiU0HyBWHfWoM.csv",
            "/Users/jundochang/" + "Desktop/",
            "chatgpt.com/" + "g/",
        )
        secret_value = re.compile(
            r"(?i)(oauth[_ -]?token|access[_ -]?token|cookie|client[_ -]?secret)\s*[:=]\s*[\"']?[^\s\"']+"
        )
        for path in sorted(SKILL_ROOT.rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".json", ".py", ".yaml"}:
                continue
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(SKILL_ROOT)):
                for literal in forbidden_literals:
                    self.assertNotIn(literal, text)
                self.assertIsNone(secret_value.search(text))


if __name__ == "__main__":
    unittest.main()

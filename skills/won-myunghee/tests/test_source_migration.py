from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
MIGRATION = SKILL_ROOT / "references" / "source-migration.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class SourceMigrationTests(unittest.TestCase):
    def load_migration(self) -> dict[str, object]:
        self.assertTrue(
            MIGRATION.is_file(),
            "source migration receipt absent: supplied persona, CFP, quotation, and image sources are uncovered",
        )
        return json.loads(MIGRATION.read_text(encoding="utf-8"))

    def test_migration_map_covers_every_supplied_source_domain(self) -> None:
        migration = self.load_migration()
        required = {
            "persona-and-opening",
            "relationship-stages",
            "cfp-framework",
            "buffett-dalio-canon",
            "saved-chatgpt-html",
            "icon",
            "character-sheet",
        }
        entries = {entry["id"]: entry for entry in migration["entries"]}
        self.assertEqual(set(entries), required)
        for identifier, entry in entries.items():
            with self.subTest(identifier=identifier):
                self.assertIn(entry["status"], {"preserved", "adapted", "excluded"})
                self.assertTrue(entry["destination"] or entry["reason"])

    def test_asset_hashes_match_migration_receipt(self) -> None:
        migration = self.load_migration()
        entries = {entry["id"]: entry for entry in migration["entries"]}
        for identifier, relative in {
            "icon": "assets/icon.png",
            "character-sheet": "assets/character-sheet.png",
        }.items():
            with self.subTest(identifier=identifier):
                asset = SKILL_ROOT / relative
                self.assertTrue(asset.is_file(), f"missing migrated asset: {relative}")
                self.assertEqual(sha256(asset), entries[identifier]["sha256"])


if __name__ == "__main__":
    unittest.main()

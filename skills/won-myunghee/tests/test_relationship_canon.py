from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


def read_required(test: unittest.TestCase, relative: str, failure: str) -> str:
    path = SKILL_ROOT / relative
    test.assertTrue(path.is_file(), failure)
    return path.read_text(encoding="utf-8")


class RelationshipCanonTests(unittest.TestCase):
    def test_objective_comprehensive_hayoung_and_subjective_faster_view_coexist(self) -> None:
        canon = read_required(
            self,
            "references/relationship-canon.md",
            "relationship canon absent: Hayoung objective/subjective distinction is not encoded",
        )
        self.assertIn("하영은 종합형", canon)
        self.assertIn("명희에게 속도형·전술형으로 보임", canon)
        self.assertNotIn("하영은 단타밖에 모른다", canon)
        self.assertNotIn("하영은 단기 투자자", canon)

    def test_signature_quotation_canon_is_buffett_and_dalio_only(self) -> None:
        registry = read_required(
            self,
            "references/source-registry.md",
            "signature quotation registry absent: Myunghee must use Buffett and Dalio, not Soros and Druckenmiller",
        )
        self.assertIn("대표 인용 정본은 워런 버핏과 레이 달리오", registry)
        self.assertIn("berkshirehathaway.com/letters/letters.html", registry)
        self.assertIn("principles.com", registry)
        self.assertNotIn("georgesoros.com", registry)
        self.assertNotIn("uscmarshallweb.s3-us-west-2.amazonaws.com", registry)


if __name__ == "__main__":
    unittest.main()

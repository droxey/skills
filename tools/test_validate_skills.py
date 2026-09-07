"""Unit tests for the deterministic skill-maturity validator."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import validate_skills as vs


class ParseFrontmatterTests(unittest.TestCase):
    def test_valid_frontmatter(self):
        text = "---\nname: x\ndescription: Use when doing x.\nmaturity: 2\n---\n\n# X\n"
        frontmatter, err = vs.parse_frontmatter(text)
        self.assertIsNone(err)
        self.assertEqual(frontmatter["name"], "x")
        self.assertEqual(frontmatter["maturity"], "2")

    def test_missing_closing_fence(self):
        _, err = vs.parse_frontmatter("---\nname: x\n")
        self.assertIsNotNone(err)


class CheckSkillTests(unittest.TestCase):
    BASE = ["name: demo-skill", "description: Use when demonstrating.", "maturity: 0"]

    @staticmethod
    def _full_body():
        return "\n\n".join("## " + aliases[0] for aliases in vs.CAPABILITIES.values())

    @staticmethod
    def _make_skill(frontmatter_lines, body):
        root = Path(tempfile.mkdtemp())
        (root / "SKILL.md").write_text(
            "---\n" + "\n".join(frontmatter_lines) + "\n---\n\n# Demo\n\n" + body,
            encoding="utf-8",
        )
        return root

    def test_level0_clean(self):
        body = self._full_body()
        skill = self._make_skill(self.BASE, body)
        name, maturity, problems = vs.check_skill(skill)
        self.assertEqual(name, "demo-skill")
        self.assertEqual(maturity, 0)
        self.assertEqual(problems, [])

    def test_missing_maturity_field(self):
        skill = self._make_skill(["name: demo-skill", "description: Use when demonstrating."], "")
        _, maturity, problems = vs.check_skill(skill)
        self.assertIsNone(maturity)
        self.assertTrue(any("maturity" in problem for problem in problems))

    def test_description_should_start_with_use_when(self):
        skill = self._make_skill(
            ["name: demo-skill", "description: does a thing.", "maturity: 0"], ""
        )
        _, _, problems = vs.check_skill(skill)
        self.assertTrue(any("Use when" in problem for problem in problems))

    def test_declared_level_two_requires_tests(self):
        body = self._full_body()
        skill = self._make_skill(
            ["name: demo-skill", "description: Use when demonstrating.", "maturity: 2"], body
        )
        _, maturity, problems = vs.check_skill(skill)
        self.assertEqual(maturity, 2)
        self.assertTrue(any("unit tests" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()

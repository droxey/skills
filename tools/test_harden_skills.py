"""Unit tests for the skill hardener."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import harden_skills as hs


class HardenSkillTests(unittest.TestCase):
    def test_replaces_entire_multiline_description(self):
        root = Path(tempfile.mkdtemp())
        skill = root / "humanize"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: humanize\ndescription: >\n  old description\n  continues here\n---\n\n# Humanize\n",
            encoding="utf-8",
        )

        hs.harden(skill, "humanize")

        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("description: " + hs.CURATED["humanize"]["desc"], text)
        self.assertNotIn("continues here", text)


if __name__ == "__main__":
    unittest.main()

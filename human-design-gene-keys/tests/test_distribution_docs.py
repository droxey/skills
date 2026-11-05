"""Static distribution-documentation checks, not a live Skillsync test."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DistributionDocumentationTests(unittest.TestCase):
    def test_skillsync_commands_and_primary_sources(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for expected in (
            "skl whoami",
            "skl skills upload ./human-design-gene-keys --dry-run",
            "skl skills upload ./human-design-gene-keys\n",
            'skl skills install "$SKILL_REF" --scope user',
            "https://skillsync.com/docs/skills",
            "https://skillsync.com/docs/cli-reference",
        ):
            self.assertIn(expected, text)
        self.assertNotIn("skillshare install", text)
        self.assertNotIn("skillshare sync", text)

    def test_private_scoped_verified_workflow(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for expected in (
            "private", "exact reference returned", "without overwriting", "never uploads",
            "No account upload, target installation, or workspace sync has been verified",
        ):
            self.assertIn(expected, text)
        self.assertNotIn(" --public", text)
        self.assertNotIn(" --force", text)
        self.assertNotIn("curl -", text)


if __name__ == "__main__":
    unittest.main()

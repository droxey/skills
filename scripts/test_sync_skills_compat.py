import subprocess
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("sync-skills.sh")


class SyncSkillsCompatTests(unittest.TestCase):
    def test_script_avoids_bash4_only_builtins(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertNotIn("readarray", source)
        self.assertNotIn("mapfile", source)

    def test_script_has_valid_bash_syntax(self):
        result = subprocess.run(
            ["bash", "-n", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_script_help_runs_without_network(self):
        result = subprocess.run(
            ["bash", str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Usage: scripts/sync-skills.sh [options]", result.stdout)


if __name__ == "__main__":
    unittest.main()

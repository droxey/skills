import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "sync-skills.sh"


def run(command, cwd):
    return subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)


class SyncSkillsTests(unittest.TestCase):
    def test_non_skill_file_change_triggers_reinstall(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source_repo = temp_path / "source"
            dest_root = temp_path / "dest"
            manifest_path = temp_path / "skills-manifest.json"

            source_repo.mkdir()
            run(["git", "init", "-b", "main"], cwd=source_repo)
            run(["git", "config", "user.name", "Test User"], cwd=source_repo)
            run(["git", "config", "user.email", "test@example.com"], cwd=source_repo)

            skill_dir = source_repo / "example-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "# Example Skill\n\n## Purpose\nValidate sync behavior.\n",
                encoding="utf-8",
            )
            (skill_dir / "prompts.md").write_text("first\n", encoding="utf-8")
            run(["git", "add", "."], cwd=source_repo)
            run(["git", "commit", "-m", "initial"], cwd=source_repo)

            manifest = {
                "repo": "local/test",
                "repo_url": str(source_repo),
                "ref": "main",
                "skills": [{"name": "example-skill", "path": "example-skill"}],
            }
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            first = subprocess.run(
                ["bash", str(SCRIPT_PATH), "--manifest", str(manifest_path), "--dest", str(dest_root), "--apply"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            installed_skill = dest_root / "example-skill"
            self.assertEqual((installed_skill / "prompts.md").read_text(encoding="utf-8"), "first\n")

            (skill_dir / "prompts.md").write_text("second\n", encoding="utf-8")
            run(["git", "add", "."], cwd=source_repo)
            run(["git", "commit", "-m", "update prompt"], cwd=source_repo)

            second = subprocess.run(
                ["bash", str(SCRIPT_PATH), "--manifest", str(manifest_path), "--dest", str(dest_root), "--apply"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("UPDATED example-skill", second.stdout)
            self.assertNotIn("UNCHANGED example-skill", second.stdout)
            self.assertEqual((installed_skill / "prompts.md").read_text(encoding="utf-8"), "second\n")
            marker = (installed_skill / ".skills-sync-source").read_text(encoding="utf-8")
            self.assertIn("skill_dir_sha256=", marker)
            self.assertNotIn("skill_md_sha256=", marker)


if __name__ == "__main__":
    unittest.main()

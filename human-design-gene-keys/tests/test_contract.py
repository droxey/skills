"""Offline package-contract checks; these do not evaluate a model's readings."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_SHA256 = "c6276381b5e5fb4f68b6cd121d170049c7ec511d55390d991e8b89a7e8a7b7c0"


class SkillContractTests(unittest.TestCase):
    def text(self, name: str) -> str:
        return (ROOT / name).read_text(encoding="utf-8")

    def test_frontmatter(self) -> None:
        text = self.text("SKILL.md")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertIn(f"name: {ROOT.name}", frontmatter)
        self.assertRegex(frontmatter, r"(?m)^description: Use when .+")
        self.assertRegex(frontmatter, r"(?m)^maturity: 0$")

    def test_required_contract_sections(self) -> None:
        headings = set(re.findall(r"(?m)^## (.+)$", self.text("SKILL.md")))
        self.assertTrue({"Purpose", "Inputs", "Outputs", "Example", "Success criteria", "Maturity", "Safety"} <= headings)

    def test_public_workflow_preserved(self) -> None:
        self.assertEqual(hashlib.sha256((ROOT / "references/research-workflow.md").read_bytes()).hexdigest(), WORKFLOW_SHA256)

    def test_relative_markdown_links_resolve(self) -> None:
        self.assertTrue((ROOT / "SKILL.md").is_file())
        for path in ROOT.rglob("*.md"):
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if re.match(r"[a-z][a-z0-9+.-]*:", link) or link.startswith("#"):
                    continue
                target = (path.parent / link.split("#", 1)[0]).resolve()
                self.assertTrue(target.is_relative_to(ROOT), f"Link escapes package: {path}: {link}")
                self.assertTrue(target.is_file(), f"Broken link: {path}: {link}")

    def test_tensions_contract(self) -> None:
        text = self.text("references/tensions.md").casefold()
        for literal in ("one short question", "source disagreement", "counterexample", "do not fit", "two chart features", "source support"):
            self.assertIn(literal, text)

    def test_subject_template_is_blank(self) -> None:
        text = self.text("templates/chart-input.md")
        for literal in ("{{subject}}", "{{source_id}}", "Displayed", "Derived", "Unverified", "Personality", "Gene Keys", "Unknown"):
            self.assertIn(literal, text)

    def test_private_profile_not_bundled(self) -> None:
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".json"}:
                continue
            text = path.read_text(encoding="utf-8").casefold()
            self.assertNotRegex(text, r"\b\d{4}-\d{2}-\d{2}\b", f"Concrete date in generic content: {path}")
            self.assertNotRegex(text, r"\bimg_\d+\.(?:png|jpe?g)\b", f"Private screenshot reference in {path}")
            self.assertNotIn("sandbox:/", text, f"Ephemeral dependency in {path}")
        for path in ROOT.rglob("*"):
            self.assertNotIn(path.suffix.lower(), {".pdf", ".jpeg", ".jpg", ".png"})

    def test_editing_sequence(self) -> None:
        text = self.text("SKILL.md")
        section = text.split("## Final editing", 1)[1].split("\n## ", 1)[0]
        self.assertLess(section.index("essence-doc"), section.index("i-have-adhd"))
        self.assertIn("unavailable", section)

    def test_eval_manifest_is_explicitly_unrun(self) -> None:
        data = json.loads(self.text("evals/cases.json"))
        self.assertEqual(data["execution_status"], "not_run")
        ids = [case["id"] for case in data["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 8)
        self.assertIn("tensions-discover", ids)
        self.assertIn("cross-subject-isolation", ids)
        for case in data["cases"]:
            self.assertTrue(case["prompt"])
            self.assertTrue(case["must"])
            self.assertTrue(case["must_not"])

    def test_source_privacy_and_no_false_scientific_claims(self) -> None:
        text = self.text("SKILL.md")
        for literal in ("primary sources", "scientific validity", "personal data", "publish", "read-only", "unverified"):
            self.assertIn(literal, text)


if __name__ == "__main__":
    unittest.main()

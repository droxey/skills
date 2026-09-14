import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted(ROOT.glob("*/SKILL.md"))


def body(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_every_checked_out_skill_is_nebula_upload_compatible() -> None:
    assert {path.parent.name for path in SKILLS} == {
        "dani-roxberrys-teaching-voice",
        "product-reverse-engineering",
    }

    for path in SKILLS:
        skill = body(path)
        frontmatter = skill.split("---", 2)[1]
        keys = re.findall(r"^([a-z][a-z-]*):", frontmatter, flags=re.MULTILINE)
        assert keys == ["name", "description"], path
        assert "Nebula" in skill, path
        assert "@skill:" in skill, path


def test_every_skill_is_self_contained_for_nebula_single_file_uploads() -> None:
    for path in SKILLS:
        skill = body(path)
        assert not re.search(
            r"(?i)(read|load|open) [`']?(references/|scripts/|assets/)", skill
        ), path


def test_every_skill_has_a_portable_delegation_contract() -> None:
    required = (
        "automatic delegation",
        "serial fallback",
        "at most three",
        "one owner per artifact",
        "parent",
        "review",
        "secrets",
        "consequential actions",
    )
    for path in SKILLS:
        skill = body(path).lower()
        for phrase in required:
            assert phrase in skill, (path, phrase)


def test_teaching_pipeline_preserves_order_and_parallelizes_only_safe_work() -> None:
    skill = body(ROOT / "dani-roxberrys-teaching-voice" / "SKILL.md")
    assert "examples.md → slides.md → speaker-notes.md" in skill
    assert "privacy, drift, and voice audits in parallel" in skill
    assert "severity, artifact, location, evidence, and proposed correction" in skill


def test_router_keeps_route_and_phase_gates_with_parent() -> None:
    skill = body(ROOT / "product-reverse-engineering" / "SKILL.md").lower()
    assert "route selection, authorization, dependency verification" in skill
    assert "never run separate pipeline phases in parallel" in skill
    assert "evidence partitions" in skill
    assert "resolve conflicts from source evidence" in skill

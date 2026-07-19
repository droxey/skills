from pathlib import Path

import pytest

from scripts.select_reasoning import TaskProfile, choose_reasoning, resolve_available


@pytest.mark.parametrize(
    ("profile", "expected"),
    [
        (
            TaskProfile(
                scope="bounded",
                uncertainty="low",
                consequence="low",
                verification="easy",
                entanglement="low",
            ),
            "medium",
        ),
        (
            TaskProfile(
                scope="cross-component",
                uncertainty="medium",
                consequence="moderate",
                verification="moderate",
                entanglement="medium",
            ),
            "high",
        ),
        (
            TaskProfile(
                scope="cross-component",
                uncertainty="high",
                consequence="high",
                verification="hard",
                entanglement="high",
                audit_required=True,
            ),
            "extra-high",
        ),
        (
            TaskProfile(
                scope="cross-component",
                uncertainty="high",
                consequence="high",
                verification="proof",
                entanglement="exceptional",
                repeated_failure=True,
            ),
            "max",
        ),
        (
            TaskProfile(
                scope="program",
                uncertainty="high",
                consequence="high",
                verification="hard",
                entanglement="high",
                judgment_dominant=True,
                framing_risk=True,
            ),
            "pro",
        ),
        (
            TaskProfile(
                scope="program",
                uncertainty="high",
                consequence="high",
                verification="hard",
                entanglement="high",
                independent_workstreams=4,
            ),
            "ultra",
        ),
    ],
)
def test_selects_expected_conceptual_mode(profile: TaskProfile, expected: str) -> None:
    assert choose_reasoning(profile) == expected


def test_pro_wins_over_max_when_problem_framing_is_the_primary_risk() -> None:
    profile = TaskProfile(
        scope="cross-component",
        uncertainty="high",
        consequence="high",
        verification="proof",
        entanglement="exceptional",
        repeated_failure=True,
        judgment_dominant=True,
        framing_risk=True,
    )
    assert choose_reasoning(profile) == "pro"


def test_ultra_requires_genuinely_independent_workstreams() -> None:
    profile = TaskProfile(
        scope="program",
        uncertainty="high",
        consequence="high",
        verification="hard",
        entanglement="high",
        independent_workstreams=2,
    )
    assert choose_reasoning(profile) == "extra-high"


@pytest.mark.parametrize(
    ("desired", "available", "expected"),
    [
        ("ultra", {"medium", "high", "extra-high", "pro"}, "pro"),
        ("ultra", {"medium", "high", "extra-high"}, "extra-high"),
        ("max", {"medium", "high", "extra-high", "pro"}, "extra-high"),
        ("pro", {"medium", "high", "extra-high"}, "extra-high"),
        ("extra-high", {"medium", "high"}, "high"),
        ("high", {"medium"}, "medium"),
    ],
)
def test_resolves_unavailable_modes(
    desired: str, available: set[str], expected: str
) -> None:
    assert resolve_available(desired, available) == expected


def test_rejects_unknown_profile_values() -> None:
    with pytest.raises(ValueError, match="scope"):
        TaskProfile(
            scope="enormous",
            uncertainty="low",
            consequence="low",
            verification="easy",
            entanglement="low",
        )


def test_skill_contract_uses_generic_examples_only() -> None:
    root = Path(__file__).resolve().parents[1]
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    readme = (root / "README.md").read_text(encoding="utf-8")
    combined = f"{skill}\n{readme}".lower()

    forbidden_specific_terms = {
        "dani",
        "cognee",
        "agentmemory",
        "episodes in ai",
        "mcp contract lab",
        "grain.com",
        "muse & machine",
    }
    assert not [term for term in forbidden_specific_terms if term in combined]


def test_skill_frontmatter_is_agentskills_compatible() -> None:
    root = Path(__file__).resolve().parents[1]
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\nname: reasoning-router\n")
    assert "\ndescription: Use when" in skill
    assert "\n---\n" in skill[4:]


def test_skill_documents_every_mode_and_lowest_sufficient_rule() -> None:
    root = Path(__file__).resolve().parents[1]
    skill = (root / "SKILL.md").read_text(encoding="utf-8").lower()
    readme = (root / "README.md").read_text(encoding="utf-8").lower()
    combined = f"{skill}\n{readme}"
    for mode in ("medium", "high", "extra high", "max", "pro", "ultra"):
        assert mode in combined
    assert "lowest sufficient" in combined
    assert "unavailable" in combined


def test_skill_stays_compact_enough_for_frequent_loading() -> None:
    root = Path(__file__).resolve().parents[1]
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    assert len(skill.split()) <= 650


def test_skill_trigger_applies_to_every_task() -> None:
    root = Path(__file__).resolve().parents[1]
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = skill.split("---", 2)[1]
    assert "description: Use when beginning any task" in frontmatter


def test_codex_global_instruction_enforces_router() -> None:
    root = Path(__file__).resolve().parents[1]
    instructions = (root / "integrations" / "codex" / "AGENTS.md").read_text(
        encoding="utf-8"
    )
    assert "Before every task" in instructions
    assert "reasoning-router" in instructions
    assert "lowest sufficient available" in instructions

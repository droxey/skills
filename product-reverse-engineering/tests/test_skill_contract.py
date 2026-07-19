import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "product-reverse-engineering"
SKILL = SKILL_DIR / "SKILL.md"
REFERENCE = SKILL_DIR / "references" / "routing-contract.md"

ROUTES = {
    "website-replication-skill": "https://github.com/leosssvip-dot/website-replication-skill",
    "reverse-engineer": "https://github.com/boshu2/agentops",
    "product-teardown": "https://github.com/Mehdibargach/claude-code-pm-skills",
    "clone-ui": "https://github.com/santowilem/skills",
    "code-to-prd": "https://github.com/alirezarezvani/claude-skills",
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_frontmatter_is_agentskills_compatible() -> None:
    skill = text(SKILL)
    assert skill.startswith("---\nname: product-reverse-engineering\n")
    frontmatter = skill.split("---", 2)[1]
    assert "\ndescription: Use when" in frontmatter


def test_exact_routes_are_documented() -> None:
    combined = text(SKILL) + text(REFERENCE)
    for name, source in ROUTES.items():
        assert name in combined
        assert source in combined


def test_compound_work_is_ordered_by_phase() -> None:
    combined = text(SKILL) + text(REFERENCE)
    assert "one atomic phase" in combined
    assert "website-replication-skill → clone-ui" in combined
    assert "reviewed artifacts" in combined


def test_missing_dependencies_fail_closed() -> None:
    combined = text(SKILL) + text(REFERENCE)
    assert "Never silently substitute" in combined
    assert "canonical source" in combined
    assert "claim the specialist ran" in combined


def test_handoff_uses_evidence_labels() -> None:
    combined = text(SKILL) + text(REFERENCE)
    for label in (
        "OBSERVED",
        "SOURCE-CONFIRMED",
        "INFERRED",
        "UNKNOWN",
        "BLOCKED",
    ):
        assert label in combined


def test_authorization_and_access_controls_are_explicit() -> None:
    combined = (text(SKILL) + text(REFERENCE)).lower()
    for phrase in (
        "explicit authorization",
        "never bypass",
        "mfa",
        "user-controlled browser",
        "rights-cleared",
    ):
        assert phrase in combined


def test_entry_skill_stays_compact() -> None:
    assert len(text(SKILL).split()) <= 650


def test_openai_interface_is_present() -> None:
    interface = text(SKILL_DIR / "agents" / "openai.yaml")
    assert 'display_name: "Product Reverse Engineering"' in interface
    assert "default_prompt:" in interface


def test_catalog_registration_is_additive() -> None:
    readme = text(ROOT / "README.md")
    manifest = json.loads(text(ROOT / "skills-manifest.json"))
    assert "## product-reverse-engineering" in readme
    assert {
        "name": "product-reverse-engineering",
        "path": "product-reverse-engineering",
    } in manifest["skills"]

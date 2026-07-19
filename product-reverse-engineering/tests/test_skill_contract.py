import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "product-reverse-engineering"
SKILL = SKILL_DIR / "SKILL.md"
REFERENCE = SKILL_DIR / "references" / "routing-contract.md"

ROUTE_DESTINATIONS = {
    "Observe and specify a live web product": "`website-replication-skill`",
    "Teardown an authorized repository or binary": "AgentOps `reverse-engineer`",
    "Analyze business model, market, growth, or moat": "`product-teardown`",
    "Rebuild a UI from a URL, screenshot, HTML/CSS, or Figma": "`clone-ui`",
    "Derive requirements or a PRD from source code": "`code-to-prd`",
}

DESTINATION_SOURCES = {
    "website-replication-skill": "https://github.com/leosssvip-dot/website-replication-skill",
    "reverse-engineer": "https://github.com/boshu2/agentops",
    "product-teardown": "https://github.com/Mehdibargach/claude-code-pm-skills",
    "clone-ui": "https://github.com/santowilem/skills",
    "code-to-prd": "https://github.com/alirezarezvani/claude-skills",
}

PREEXISTING_SKILL_NAMES = {
    "ah-devops-engineer",
    "chrome-mcp-web-fallback",
    "code",
    "code-review",
    "codespace-operator",
    "codespace-operator-v2",
    "dani-roxberrys-teaching-voice",
    "fleet-audit-patterns",
    "humanize",
    "intake-implementation-workflow",
    "linkedin-lead-gen-outreach",
    "markdown-mode-router",
    "meeting-to-action",
    "mobile-forensics",
    "model-cost-estimator",
    "musexmachine-mcp-codex-env",
    "nextjs-nebula-miniapp",
    "perceptis-manual-import-connector",
    "perceptyx-read-only-export-validation-and-scaffold",
    "product-clone-research",
    "prompt-technique-router",
    "repo-settings-bootstrap",
    "resume-ats-pdf-optimizer",
    "senior-devops",
    "web-scraper",
    "superpowers-brainstorming",
    "superpowers-dispatching-parallel-agents",
    "superpowers-executing-plans",
    "superpowers-finishing-a-development-branch",
    "superpowers-receiving-code-review",
    "superpowers-requesting-code-review",
    "superpowers-subagent-driven-development",
    "superpowers-systematic-debugging",
    "superpowers-test-driven-development",
    "superpowers-using-git-worktrees",
    "superpowers-using-superpowers",
    "superpowers-verification-before-completion",
    "superpowers-writing-plans",
    "superpowers-writing-skills",
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_frontmatter_is_agentskills_compatible() -> None:
    skill = text(SKILL)
    assert skill.startswith("---\nname: product-reverse-engineering\n")
    frontmatter = skill.split("---", 2)[1]
    assert "\ndescription: Use when" in frontmatter


def test_exact_route_to_destination_pairings_are_documented() -> None:
    skill = text(SKILL)
    for requested_work, destination in ROUTE_DESTINATIONS.items():
        assert f"| {requested_work} | {destination} |" in skill


def test_exact_destination_to_source_pairings_are_documented() -> None:
    reference = text(REFERENCE)
    for destination, source in DESTINATION_SOURCES.items():
        assert f"| `{destination}` | {source} |" in reference


def test_repository_to_prd_has_explicit_output_precedence() -> None:
    skill = text(SKILL)
    assert "a repository-to-PRD request routes to `code-to-prd`" in skill
    assert "a repository teardown routes to `reverse-engineer`" in skill


def test_compound_work_is_ordered_by_phase() -> None:
    combined = text(SKILL) + text(REFERENCE)
    assert "one atomic phase" in combined
    assert "website-replication-skill → clone-ui" in combined
    assert "reverse-engineer → code-to-prd" in combined
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
    skills = manifest["skills"]
    names = [entry["name"] for entry in skills]

    assert "## product-reverse-engineering" in readme
    assert {
        "name": "product-reverse-engineering",
        "path": "product-reverse-engineering",
    } in skills
    assert PREEXISTING_SKILL_NAMES <= set(names)
    assert names.count("product-reverse-engineering") == 1
    assert len(names) == len(set(names))

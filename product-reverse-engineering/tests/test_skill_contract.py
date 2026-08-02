import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "product-reverse-engineering"
SKILL = SKILL_DIR / "SKILL.md"
REFERENCE = SKILL_DIR / "references" / "routing-contract.md"
ROUTING_CASES = SKILL_DIR / "tests" / "routing-cases.jsonl"
SYNC_WORKFLOW = ROOT / ".github" / "workflows" / "skills-global-sync.yml"

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

DESTINATION_PROVENANCE = {
    "website-replication-skill": (
        "6f7ee0b2335069b6786dab2d4ced5b11def79141",
        "SKILL.md",
        "LICENSE (MIT)",
    ),
    "reverse-engineer": (
        "aceeb6f10f48e1c9d0919e947bed1e8e6de40578",
        "skills/reverse-engineer/SKILL.md",
        "LICENSE (Apache-2.0)",
    ),
    "product-teardown": (
        "ab21d7a398c92254c4b1d4fd17325bd09a17a538",
        "skills/product-teardown/SKILL.md",
        "README-only MIT claim; unverified",
    ),
    "clone-ui": (
        "2caf2e1dd0e58d974d8a72d803d7273f9f774ac5",
        "skills/clone-ui/SKILL.md",
        "README badge only; unverified",
    ),
    "code-to-prd": (
        "aa8d778811a557a2c28ccadda4cf3d0bd028a4cc",
        "product-team/code-to-prd/skills/code-to-prd/SKILL.md",
        "LICENSE (MIT)",
    ),
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


def jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in text(path).splitlines()
        if line.strip()
    ]


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
    assert "immutable" in combined
    assert "license" in combined.lower()
    assert "fail closed" in combined.lower()


def test_dependency_registry_pins_path_commit_and_license_evidence() -> None:
    reference = text(REFERENCE)
    for destination, (commit, path, license_evidence) in DESTINATION_PROVENANCE.items():
        row = next(
            line
            for line in reference.splitlines()
            if line.startswith("|") and f"`{destination}`" in line
        )
        assert commit in row
        assert path in row
        assert license_evidence in row


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


def test_high_risk_controls_are_always_loaded_by_the_router() -> None:
    skill = text(SKILL).lower()
    assert "read `references/routing-contract.md` before every route decision" in skill
    for phrase in (
        "static analysis is the default for binaries",
        "the pinned `reverse-engineer` destination is static-only",
        "disposable, sandboxed environment",
        "network disabled",
        "no secrets",
        "full visual and source surface",
        "differentiated composition, styles, code, embeds, branding, copy, and assets",
        "override any conflicting destination instructions",
        "a refusal or block selects no destination for execution",
        "route an independently useful allowed outcome",
        "personal data",
        "out of version control",
    ):
        assert phrase in skill


def test_entry_skill_stays_compact() -> None:
    assert len(text(SKILL).split()) <= 800


def test_openai_interface_is_present() -> None:
    interface = text(SKILL_DIR / "agents" / "openai.yaml")
    assert 'display_name: "Product Reverse Engineering"' in interface
    assert "$product-reverse-engineering" in interface


def test_sync_workflow_registers_skill_and_has_one_permissions_key() -> None:
    workflow = text(SYNC_WORKFLOW)
    assert "- 'product-reverse-engineering/**'" in workflow
    assert len(re.findall(r"^permissions:", workflow, flags=re.MULTILINE)) == 1


def test_machine_readable_cases_cover_routes_and_safety_boundaries() -> None:
    cases = jsonl(ROUTING_CASES)
    ids = {case["id"] for case in cases}
    assert len(ids) == len(cases)
    assert {
        "W1",
        "R1",
        "R2",
        "R3",
        "R4",
        "B1",
        "U1",
        "U2",
        "P1",
        "C1",
        "C2",
        "A1",
        "D1",
        "S1",
        "S2",
        "S3",
        "S4",
        "S5",
        "S6",
        "S7",
    } <= ids

    destinations = {
        destination
        for case in cases
        for destination in case["expected_destinations"]
    }
    assert destinations == set(DESTINATION_SOURCES)

    controls = {
        control
        for case in cases
        for control in case["required_controls"]
    }
    assert {
        "authorization-required",
        "static-only",
        "isolated-dynamic-analysis",
        "rights-ownership-required",
        "differentiated-clean-room",
        "pii-redaction",
        "prompt-injection-ignore",
        "immutable-provenance",
        "license-verified",
        "no-credentials-or-sessions",
        "consequential-action-confirmation",
    } <= controls

    by_id = {case["id"]: case for case in cases}
    assert by_id["R4"]["expected_decision"] == "block"
    assert by_id["R4"]["expected_destinations"] == []
    assert {
        "static-only",
        "isolated-dynamic-analysis",
    } <= set(by_id["R4"]["required_controls"])
    assert by_id["U2"]["expected_decision"] == "block"
    assert by_id["U2"]["expected_destinations"] == []
    assert by_id["S7"]["expected_decision"] == "route"
    assert by_id["S7"]["expected_destinations"] == ["clone-ui"]


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

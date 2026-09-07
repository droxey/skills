#!/usr/bin/env python3
"""Deterministic skill-maturity validator for the droxey/skills repository.

Standard library only; no network or model calls. Scans every top-level
first-party SKILL.md, checks its YAML frontmatter and the sections required by
`docs/skill-maturity-standard.md`, and reports each skill's declared versus
substantiated maturity level.

Exit code 0 means every skill is consistent with its declared level; 1 means at
least one skill is missing a required section or is declared at a level its
directory structure does not substantiate.
"""

import argparse
import re
import sys
from pathlib import Path

MATURITY_MIN = 0
MATURITY_MAX = 3

# Canonical capability -> accepted heading aliases (matched case-insensitively).
CAPABILITIES = {
    "purpose": ("purpose", "core rule", "intent", "what it does", "what this does"),
    "inputs": ("inputs", "preflight", "runtime model", "what it needs", "input"),
    "outputs": (
        "outputs",
        "what this skill produces",
        "what it produces",
        "handoff",
        "produces",
        "artifacts",
    ),
    "example": ("example", "examples", "worked example", "example invocation", "example run"),
    "success": (
        "success criteria",
        "definition of done",
        "validation standard",
        "done when",
        "good enough",
        "acceptance criteria",
    ),
    "maturity": ("maturity", "maturity level", "maturity note"),
}

SAFETY_HEADINGS = ("guardrails", "safety", "security", "authorization", "ethics", "approval")

SCRIPT_EXTS = {".py", ".sh", ".js", ".ts"}
STRUCTURED_EXTS = {".json", ".jsonl", ".yaml", ".yml"}


def parse_frontmatter(text):
    """Return (frontmatter dict, error string or None)."""
    if not text.startswith("---"):
        return {}, "missing opening `---`"
    end = text.find("\n---", 3)
    if end == -1:
        return {}, "missing closing `---`"
    block = text[3:end]
    fm = {}
    lines = block.splitlines()
    index = 0
    while index < len(lines):
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", lines[index])
        if not match:
            index += 1
            continue
        key, value = match.groups()
        if value in {">", ">-", ">+", "|", "|-", "|+"}:
            folded = []
            index += 1
            while index < len(lines) and (
                not lines[index].strip() or lines[index][0].isspace()
            ):
                folded.append(lines[index].strip())
                index += 1
            fm[key] = " ".join(part for part in folded if part)
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        fm[key] = value.strip()
        index += 1
    return fm, None


def extract_headings(body):
    """Return the set of normalized H2 heading names in body."""
    found = set()
    fence = None
    for line in body.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token[0]
            elif token[0] == fence:
                fence = None
            continue
        if fence:
            continue
        match = re.match(r"^#{2}\s+(.+?)\s*$", line)
        if match:
            found.add(match.group(1).strip().lower())
    return found


def _body(text):
    """Return the text after the frontmatter when present, else the full text."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def has_asset(skill_dir):
    """True when any runnable script or structured-output file lives under the skill."""
    exts = SCRIPT_EXTS | STRUCTURED_EXTS
    return any(
        p.is_file() and p.suffix.lower() in exts
        for p in skill_dir.rglob("*")
        if not any(part in {".git"} for part in p.parts)
    )


def has_tests(skill_dir):
    """True when tests/ contains at least one unit-test module."""
    tests = skill_dir / "tests"
    if not tests.is_dir():
        return False
    return any(
        p.is_file()
        and ((p.name.startswith("test_") and p.name.endswith(".py")) or p.name.endswith("_test.py"))
        for p in tests.iterdir()
    )


def has_agents_or_safety(skill_dir, headings):
    """True when agents/ interfaces exist or an explicit safety section is present."""
    if (skill_dir / "agents").is_dir():
        return True
    return any(h in SAFETY_HEADINGS for h in headings)


def check_skill(skill_dir):
    """Return (name, maturity_or_None, sorted_problem_list) for one skill directory."""
    problems = []
    skill_path = skill_dir / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")

    frontmatter, fm_err = parse_frontmatter(text)
    if fm_err:
        problems.append(fm_err)

    name = frontmatter.get("name", "") or skill_dir.name
    if not frontmatter.get("name"):
        problems.append("missing `name` in frontmatter")

    description = frontmatter.get("description", "")
    if not description:
        problems.append("missing `description` in frontmatter")
    elif not description.lower().startswith("use when"):
        problems.append("`description` should start with `Use when`")

    maturity = None
    maturity_raw = frontmatter.get("maturity")
    if maturity_raw is None:
        problems.append("missing `maturity` in frontmatter")
    else:
        try:
            maturity = int(maturity_raw)
        except ValueError:
            problems.append("`maturity` must be an integer, got %r" % maturity_raw)
            maturity = None
        else:
            if not MATURITY_MIN <= maturity <= MATURITY_MAX:
                problems.append(
                    "`maturity` %d outside %d-%d" % (maturity, MATURITY_MIN, MATURITY_MAX)
                )
                maturity = None

    headings = extract_headings(_body(text))

    for cap, aliases in CAPABILITIES.items():
        if not any(alias in headings for alias in aliases):
            problems.append("missing `## %s` section (aliases: %s)" % (cap, ", ".join(aliases)))

    if maturity is not None:
        if maturity >= 1 and not has_asset(skill_dir):
            problems.append("declared level >= 1 but no script or structured-output asset found")
        if maturity >= 2 and not has_tests(skill_dir):
            problems.append("declared level >= 2 but no unit tests under `tests/`")
        if maturity >= 3 and not has_agents_or_safety(skill_dir, headings):
            problems.append("declared level 3 but no `agents/` interface or safety section")

    return name, maturity, sorted(problems)


def discover_skills(root):
    return sorted(
        (p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").exists()),
        key=lambda p: p.name,
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root to scan (default: parent of tools/)",
    )
    args = parser.parse_args(argv)

    skills = discover_skills(args.root)
    if not skills:
        print("no SKILL.md files found under %s" % args.root)
        return 1

    failures = 0
    for skill_dir in skills:
        name, maturity, problems = check_skill(skill_dir)
        level = maturity if maturity is not None else "?"
        if problems:
            failures += 1
            print("[FAIL] %s (maturity %s)" % (name, level))
            for problem in problems:
                print("    - %s" % problem)
        else:
            print("[ok]   %s (maturity %s)" % (name, level))

    print("\n%d skills, %d with violations" % (len(skills), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

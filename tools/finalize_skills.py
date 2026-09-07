#!/usr/bin/env python3
"""Finalize: minimally harden the essence meta-skills, then validate all first-party skills."""
import argparse
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
ESSENCE_NAMES = ("essence", "essence-commit", "essence-doc", "essence-pr")

ALIASES = {
    "Purpose": ("purpose", "core rule", "intent", "what it does"),
    "Inputs": ("inputs", "preflight", "runtime model", "what it needs", "input"),
    "Outputs": ("outputs", "what this skill produces", "what it produces", "handoff", "produces", "artifacts"),
    "Example": ("example", "examples", "worked example", "example invocation"),
    "Success criteria": ("success criteria", "definition of done", "validation standard", "done when", "acceptance criteria"),
    "Maturity": ("maturity", "maturity level", "maturity note"),
}


def headings(body):
    return {m.group(1).strip().lower() for m in re.finditer(r"^#{2}\s+(.+?)\s*$", body, re.M)}


def has_section(h, title):
    return any(a in h for a in ALIASES[title])


def minimal_harden(path):
    text = path.read_text(encoding="utf-8")
    if "maturity:" in text.split("---", 2)[:2].__str__() is False and not re.search(r"(?m)^maturity:", text):
        pass
    # add maturity field before closing fence if absent
    if not re.search(r"(?m)^maturity:", text):
        text = text.replace("\n---", "\nmaturity: 0\n---", 1)
    body = text.split("---", 2)[2] if text.startswith("---") and text.count("---") >= 2 else text
    h = headings(body)
    if "maturity" not in h and not any(a in h for a in ALIASES["Maturity"]):
        text = text.rstrip("\n") + "\n\n## Maturity\n\nLevel 0 - Intent. Substantiated by the written contract only; the essence methodology is maintained in the droxey/skills repo.\n"
    path.write_text(text, encoding="utf-8")


def full_validate(path):
    """Return (name, maturity, missing_sections)."""
    text = path.read_text(encoding="utf-8")
    name = path.parent.name
    m = re.search(r"(?m)^maturity:\s*(\d+)", text)
    maturity = int(m.group(1)) if m else None
    body = text.split("---", 2)[2] if text.startswith("---") and text.count("---") >= 2 else text
    h = headings(body)
    missing = [t for t in ("Purpose", "Inputs", "Outputs", "Example", "Success criteria", "Maturity")
               if not has_section(h, t)]
    return name, maturity, missing


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=DEFAULT_ROOT,
        help="repository root to scan (default: parent of tools/)",
    )
    args = parser.parse_args(argv)
    essence = [args.root / name / "SKILL.md" for name in ESSENCE_NAMES]
    for p in essence:
        if p.exists():
            minimal_harden(p)
            print("[essence] %s -> maturity added" % p.parent.name)
        else:
            print("[essence] MISSING %s" % p)

    print("\n=== full validation ===")
    seen = {
        d.name: d
        for d in sorted(args.root.iterdir())
        if d.is_dir() and (d / "SKILL.md").exists()
    }
    if not seen:
        print("no SKILL.md files found under %s" % args.root, file=sys.stderr)
        return 1
    bad = 0
    for name in sorted(seen):
        n, maturity, missing = full_validate(seen[name] / "SKILL.md")
        if maturity is None or missing:
            bad += 1
            print("[FAIL] %-32s maturity=%s missing=%s" % (n, maturity, missing or "none"))
        else:
            print("[ok]   %-32s level %d" % (n, maturity))
    print("\n%d skills validated, %d with violations" % (len(seen), bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

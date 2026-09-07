#!/usr/bin/env python3
"""essence-doc protected-span guard.

essence-doc's actual rewrite is done by the invoking agent (it's a judgment call about
meaning, not a mechanical transform). This script's only job is the mechanical part:
extract code fences, inline code, URLs, and file-path-like tokens from the original file,
then confirm every one of them survives verbatim in the rewritten file. It does not
rewrite anything itself.
"""
import re
import sys

FENCE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]+`")
URL = re.compile(r"https?://[^\s)\]\"'>]+")
# path-like token: at least one slash, word/dot/dash chars, no whitespace either side
PATH = re.compile(r"(?<![\w/])(?:\.{1,2}/|~/)?(?:[\w.-]+/)+[\w.-]+")

# Order matters: match fences first so inline-code/URL/path patterns don't fire
# inside a code block; each match is masked before the next pattern runs.
PATTERNS = [FENCE, INLINE_CODE, URL, PATH]


TRAILING_PUNCT = ".,;:!?)"


def extract_protected(text):
    """Return protected literal substrings from text, masking each match so later
    patterns can't re-match inside a span already claimed by an earlier one."""
    spans = []
    working = text

    def _grab(match):
        raw = match.group(0)
        # Trailing sentence punctuation (the period ending a sentence a URL sits in,
        # etc.) isn't part of the URL/path itself -- don't force the rewrite to keep it.
        trimmed = raw.rstrip(TRAILING_PUNCT) or raw
        spans.append(trimmed)
        return " " * len(raw)

    for pattern in PATTERNS:
        working = pattern.sub(_grab, working)
    return spans


def validate(original_path, rewritten_path):
    with open(original_path, encoding="utf-8") as f:
        original = f.read()
    with open(rewritten_path, encoding="utf-8") as f:
        rewritten = f.read()

    protected = extract_protected(original)
    missing = [span for span in protected if span not in rewritten]

    if missing:
        print(f"FAIL: {len(missing)} of {len(protected)} protected span(s) missing or altered:")
        for span in missing:
            preview = span if len(span) <= 80 else span[:77] + "..."
            print(f"  - {preview!r}")
        return 1

    print(f"OK: all {len(protected)} protected span(s) preserved verbatim.")
    return 0


def main(argv):
    if len(argv) == 3 and argv[0] == "validate":
        return validate(argv[1], argv[2])
    if len(argv) == 2 and argv[0] == "extract":
        with open(argv[1], encoding="utf-8") as f:
            for span in extract_protected(f.read()):
                print(span)
        return 0
    print("usage: essence_doc.py validate <original> <rewritten>", file=sys.stderr)
    print("       essence_doc.py extract <file>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Run trigger evaluation for the `code` skill.

Compares expected trigger labels from `trigger-prompts.jsonl` against observed
router outcomes and writes a markdown report.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def safe_div(num: int, den: int) -> float:
    return (num / den) if den else 0.0


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate skill trigger precision/recall.")
    parser.add_argument(
        "--expected",
        default="code/evals/trigger-prompts.jsonl",
        help="Path to expected prompt labels JSONL (id, should_trigger).",
    )
    parser.add_argument(
        "--observed",
        required=True,
        help="Path to observed router outputs JSONL (id, triggered).",
    )
    parser.add_argument(
        "--out",
        default="",
        help="Output markdown path. Default: code/evals/results/YYYY-MM-DD-trigger-eval.md",
    )
    parser.add_argument("--precision-threshold", type=float, default=0.90)
    parser.add_argument("--recall-threshold", type=float, default=0.85)
    args = parser.parse_args()

    expected_path = Path(args.expected)
    observed_path = Path(args.observed)

    expected_rows = load_jsonl(expected_path)
    observed_rows = load_jsonl(observed_path)

    expected = {row["id"]: bool(row["should_trigger"]) for row in expected_rows}
    observed = {row["id"]: bool(row["triggered"]) for row in observed_rows}

    missing = sorted(set(expected) - set(observed))
    extra = sorted(set(observed) - set(expected))
    if missing or extra:
        print("ERROR: id mismatch between expected and observed files")
        if missing:
            print("Missing observed IDs:", ", ".join(missing))
        if extra:
            print("Unexpected observed IDs:", ", ".join(extra))
        return 2

    tp = fp = tn = fn = 0
    for prompt_id, should_trigger in expected.items():
        triggered = observed[prompt_id]
        if should_trigger and triggered:
            tp += 1
        elif should_trigger and not triggered:
            fn += 1
        elif not should_trigger and triggered:
            fp += 1
        else:
            tn += 1

    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    accuracy = safe_div(tp + tn, tp + tn + fp + fn)

    date_str = dt.date.today().isoformat()
    out_path = Path(args.out) if args.out else Path(f"code/evals/results/{date_str}-trigger-eval.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    status = "PASS" if (precision >= args.precision_threshold and recall >= args.recall_threshold) else "FAIL"

    lines = [
        "# Trigger Eval Report",
        "",
        f"- Date: {date_str}",
        f"- Expected file: `{expected_path}`",
        f"- Observed file: `{observed_path}`",
        f"- Precision threshold: {args.precision_threshold:.2f}",
        f"- Recall threshold: {args.recall_threshold:.2f}",
        f"- Status: **{status}**",
        "",
        "## Confusion Matrix",
        "",
        f"- TP: {tp}",
        f"- FP: {fp}",
        f"- TN: {tn}",
        f"- FN: {fn}",
        "",
        "## Metrics",
        "",
        f"- Precision: {precision:.4f}",
        f"- Recall: {recall:.4f}",
        f"- Accuracy: {accuracy:.4f}",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote report: {out_path}")
    print(f"Status: {status}")
    print(f"Precision: {precision:.4f} | Recall: {recall:.4f} | Accuracy: {accuracy:.4f}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

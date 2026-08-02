import json
import subprocess
import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
CASES = TEST_DIR / "routing-cases.jsonl"
RUNNER = TEST_DIR / "run_routing_eval.py"


def load_cases() -> list[dict]:
    return [
        json.loads(line)
        for line in CASES.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_observations(path: Path, cases: list[dict]) -> None:
    observations = [
        {
            "id": case["id"],
            "decision": case["expected_decision"],
            "destinations": case["expected_destinations"],
            "controls": case["required_controls"],
        }
        for case in cases
    ]
    path.write_text(
        "".join(json.dumps(item) + "\n" for item in observations),
        encoding="utf-8",
    )


def run_eval(observed: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--cases",
            str(CASES),
            "--observed",
            str(observed),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def test_accepts_complete_matching_observations(tmp_path: Path) -> None:
    observed = tmp_path / "observed.jsonl"
    cases = load_cases()
    write_observations(observed, cases)

    result = run_eval(observed)

    assert result.returncode == 0, result.stdout + result.stderr
    assert f"PASS {len(cases)}/{len(cases)}" in result.stdout


def test_rejects_wrong_route_and_missing_control(tmp_path: Path) -> None:
    observed = tmp_path / "observed.jsonl"
    cases = load_cases()
    write_observations(observed, cases)
    rows = [
        json.loads(line)
        for line in observed.read_text(encoding="utf-8").splitlines()
    ]
    rows[0]["destinations"] = ["clone-ui"]
    rows[1]["controls"] = []
    observed.write_text(
        "".join(json.dumps(item) + "\n" for item in rows),
        encoding="utf-8",
    )

    result = run_eval(observed)

    assert result.returncode == 1
    assert "W1: destinations" in result.stdout
    assert "R1: missing controls" in result.stdout


def test_rejects_missing_duplicate_and_unknown_case_ids(tmp_path: Path) -> None:
    observed = tmp_path / "observed.jsonl"
    cases = load_cases()
    write_observations(observed, cases[:-1])
    with observed.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "id": cases[0]["id"],
                    "decision": "route",
                    "destinations": [],
                    "controls": [],
                }
            )
            + "\n"
        )
        handle.write(
            json.dumps(
                {
                    "id": "UNKNOWN",
                    "decision": "route",
                    "destinations": [],
                    "controls": [],
                }
            )
            + "\n"
        )

    result = run_eval(observed)

    assert result.returncode == 1
    assert f"FAIL {len(cases) - 2}/{len(cases)}" in result.stdout
    assert "duplicate observation id" in result.stdout
    assert "missing observation ids" in result.stdout
    assert "unknown observation ids" in result.stdout


def test_rejects_unknown_control_tokens(tmp_path: Path) -> None:
    observed = tmp_path / "observed.jsonl"
    cases = load_cases()
    write_observations(observed, cases)
    rows = [
        json.loads(line)
        for line in observed.read_text(encoding="utf-8").splitlines()
    ]
    rows[0]["controls"].append("invented-control")
    observed.write_text(
        "".join(json.dumps(item) + "\n" for item in rows),
        encoding="utf-8",
    )

    result = run_eval(observed)

    assert result.returncode == 1
    assert "W1: unknown controls: invented-control" in result.stdout

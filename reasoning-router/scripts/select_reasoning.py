#!/usr/bin/env python3
"""Deterministic reference selector for the reasoning-router skill."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable

MODES = ("medium", "high", "extra-high", "max", "pro", "ultra")
SCOPES = {"bounded", "multi-step", "cross-component", "program"}
UNCERTAINTY = {"low", "medium", "high"}
CONSEQUENCE = {"low", "moderate", "high"}
VERIFICATION = {"easy", "moderate", "hard", "proof"}
ENTANGLEMENT = {"low", "medium", "high", "exceptional"}


@dataclass(frozen=True)
class TaskProfile:
    """Observable task characteristics used by the routing policy."""

    scope: str
    uncertainty: str
    consequence: str
    verification: str
    entanglement: str
    judgment_dominant: bool = False
    framing_risk: bool = False
    audit_required: bool = False
    security_or_concurrency: bool = False
    repeated_failure: bool = False
    independent_workstreams: int = 1

    def __post_init__(self) -> None:
        allowed = {
            "scope": (self.scope, SCOPES),
            "uncertainty": (self.uncertainty, UNCERTAINTY),
            "consequence": (self.consequence, CONSEQUENCE),
            "verification": (self.verification, VERIFICATION),
            "entanglement": (self.entanglement, ENTANGLEMENT),
        }
        for field, (value, choices) in allowed.items():
            if value not in choices:
                raise ValueError(f"invalid {field}: {value!r}; choose from {sorted(choices)}")
        if self.independent_workstreams < 1:
            raise ValueError("independent_workstreams must be at least 1")


def choose_reasoning(profile: TaskProfile) -> str:
    """Return the conceptual best mode before product availability fallbacks."""

    if profile.independent_workstreams >= 3:
        return "ultra"

    if profile.consequence == "high" and (
        profile.judgment_dominant or profile.framing_risk
    ):
        return "pro"

    if profile.entanglement == "exceptional" and (
        profile.verification == "proof" or profile.repeated_failure
    ):
        return "max"

    if (
        profile.audit_required
        or profile.security_or_concurrency
        or profile.consequence == "high"
        or profile.uncertainty == "high"
        or profile.verification in {"hard", "proof"}
        or profile.entanglement == "high"
        or profile.repeated_failure
    ):
        return "extra-high"

    if (
        profile.scope in {"multi-step", "cross-component", "program"}
        or profile.uncertainty == "medium"
        or profile.consequence == "moderate"
        or profile.verification == "moderate"
        or profile.entanglement == "medium"
    ):
        return "high"

    return "medium"


_FALLBACKS = {
    "ultra": ("ultra", "pro", "extra-high", "high", "medium"),
    "pro": ("pro", "extra-high", "high", "medium"),
    "max": ("max", "extra-high", "high", "medium"),
    "extra-high": ("extra-high", "high", "medium"),
    "high": ("high", "medium"),
    "medium": ("medium",),
}


def resolve_available(desired: str, available: Iterable[str]) -> str:
    """Resolve a conceptual mode against modes available in the active surface."""

    if desired not in MODES:
        raise ValueError(f"unknown desired mode: {desired!r}")
    available_set = set(available)
    unknown = available_set - set(MODES)
    if unknown:
        raise ValueError(f"unknown available modes: {sorted(unknown)}")
    if not available_set:
        raise ValueError("at least one available mode is required")

    for candidate in _FALLBACKS[desired]:
        if candidate in available_set:
            return candidate
    raise ValueError(
        f"no compatible fallback for {desired!r} in {sorted(available_set)}"
    )


def _parse_available(value: str) -> set[str]:
    return {item.strip().lower() for item in value.split(",") if item.strip()}


def _self_test() -> None:
    cases = [
        (TaskProfile("bounded", "low", "low", "easy", "low"), "medium"),
        (
            TaskProfile(
                "cross-component", "medium", "moderate", "moderate", "medium"
            ),
            "high",
        ),
        (
            TaskProfile(
                "cross-component",
                "high",
                "high",
                "hard",
                "high",
                audit_required=True,
            ),
            "extra-high",
        ),
        (
            TaskProfile(
                "cross-component",
                "high",
                "high",
                "proof",
                "exceptional",
                repeated_failure=True,
            ),
            "max",
        ),
        (
            TaskProfile(
                "program",
                "high",
                "high",
                "hard",
                "high",
                judgment_dominant=True,
                framing_risk=True,
            ),
            "pro",
        ),
        (
            TaskProfile(
                "program",
                "high",
                "high",
                "hard",
                "high",
                independent_workstreams=4,
            ),
            "ultra",
        ),
    ]
    for profile, expected in cases:
        actual = choose_reasoning(profile)
        if actual != expected:
            raise AssertionError(f"expected {expected}, got {actual}: {profile}")
    print(f"self-test passed: {len(cases)} routing cases")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Select the lowest sufficient GPT-5.6 reasoning mode."
    )
    parser.add_argument("--scope", choices=sorted(SCOPES))
    parser.add_argument("--uncertainty", choices=sorted(UNCERTAINTY))
    parser.add_argument("--consequence", choices=sorted(CONSEQUENCE))
    parser.add_argument("--verification", choices=sorted(VERIFICATION))
    parser.add_argument("--entanglement", choices=sorted(ENTANGLEMENT))
    parser.add_argument("--judgment-dominant", action="store_true")
    parser.add_argument("--framing-risk", action="store_true")
    parser.add_argument("--audit-required", action="store_true")
    parser.add_argument("--security-or-concurrency", action="store_true")
    parser.add_argument("--repeated-failure", action="store_true")
    parser.add_argument("--independent-workstreams", type=int, default=1)
    parser.add_argument(
        "--available",
        default=",".join(MODES),
        help="comma-separated modes available in the active product surface",
    )
    parser.add_argument("--self-test", action="store_true")
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0

    required = ("scope", "uncertainty", "consequence", "verification", "entanglement")
    missing = [name for name in required if getattr(args, name) is None]
    if missing:
        parser.error(
            "missing required arguments: "
            + ", ".join(f"--{name.replace('_', '-')}" for name in missing)
        )

    profile = TaskProfile(
        scope=args.scope,
        uncertainty=args.uncertainty,
        consequence=args.consequence,
        verification=args.verification,
        entanglement=args.entanglement,
        judgment_dominant=args.judgment_dominant,
        framing_risk=args.framing_risk,
        audit_required=args.audit_required,
        security_or_concurrency=args.security_or_concurrency,
        repeated_failure=args.repeated_failure,
        independent_workstreams=args.independent_workstreams,
    )
    desired = choose_reasoning(profile)
    selected = resolve_available(desired, _parse_available(args.available))
    print(
        json.dumps(
            {
                "desired": desired,
                "selected": selected,
                "fallback_used": desired != selected,
                "profile": asdict(profile),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

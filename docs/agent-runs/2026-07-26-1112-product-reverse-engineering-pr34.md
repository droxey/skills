# PR 34 Product Router Hardening

## Scope

Reviewed and hardened `droxey/skills` pull request 34 without merging it. The work preserved the five exact routes while fixing safety, dependency, registration, and behavioral-test blockers.

## Changes

- Made the routing reference always-loaded and pinned each dependency by origin, exact path, immutable commit, frontmatter identity, and license evidence.
- Defaulted binary analysis to static-only and blocked unsupported dynamic tracing from the pinned static-only specialist.
- Required full-surface rights for `clone-ui`; no-rights fidelity requests now block instead of repurposing that specialist.
- Added sensitive-evidence, credential/session, prompt-injection, consequential-action, and safe-method rules.
- Added a machine-readable 20-case suite, executable scorer, and scorer regression tests.
- Fixed the OpenAI default prompt, README sample, global-sync path registration, and duplicate workflow `permissions` key.

## Verification

- Product router tests: `19 passed`.
- Blind fresh-agent routing evaluation: `PASS 20/20`.
- Skill Creator validation: `Skill is valid!`.
- Manifest JSON, workflow YAML, Python compilation, shell syntax, sync smoke test, and `git diff --check`: passed.
- Branch-wide pytest with `PYTHONPATH=reasoning-router`: `48 passed, 1 failed`.
- `origin/main` with the same environment: `29 passed, 1 failed`.
- Both failures are `SyncSkillsCompatTests.test_script_avoids_bash4_only_builtins`, caused by the pre-existing `readarray` use. The tested script and compatibility test have identical blob IDs on `origin/main` and the PR head.
- Independent safety/dependency and tests/catalog reviews reported no remaining merge blockers after fixes.

No pull request merge was performed.

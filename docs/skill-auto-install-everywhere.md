# Auto-install skills across CLI, desktop app, and website

## Goal
Ensure every skill you create or update is installed predictably across all agent surfaces with minimal manual steps.

## Constraints
- Different surfaces may use different runtimes, update cadences, and local skill directories.
- You do not control every host directly (especially managed web environments).
- Silent drift is the biggest failure mode (skill source and installed copy diverge).

## Recommended baseline architecture

1. **Single source of truth**
   - Store skills in one GitHub repo (or mono-repo path).
   - Version every change with git tags (e.g. `skills-v2026.04.17.1`).

2. **Declarative manifest**
   - Keep a machine-readable manifest (`skills-manifest.json`) listing skill paths and a pinned ref/sha.
   - Treat the manifest as the deployment contract for all platforms.

3. **Idempotent installer entrypoint**
   - Standardize one install/sync command for all environments:
     - `./scripts/sync-skills.sh --repo <owner>/<repo> --ref <sha-or-tag>`
   - Never install from floating `main` in production workflows; pin versions.

4. **Platform adapters (thin wrappers)**
   - CLI: run installer at startup/login hook (or daily scheduled task).
   - Desktop app: run installer on launch/update event with local cache + rollback.
   - Website/hosted agent: run installer in environment bootstrapping job (image build or startup task).

5. **Drift detection + reconciliation**
   - Before install, compare installed `SKILL.md` checksum against manifest target.
   - If mismatch, reinstall and log result.
   - Emit a clear "installed/unchanged/failed" status per skill.

6. **Safe rollout model**
   - Promote versions through channels: `dev` -> `staging` -> `prod`.
   - Keep a one-command rollback to previous manifest ref.

## Practical workflow for every skill change

1. Edit skill files.
2. Run local validation checks (lint + smoke load).
3. Commit and push.
4. Update manifest to the new pinned ref.
5. Trigger platform install jobs.
6. Verify install receipts from each platform.
7. Promote to next channel after checks pass.

## Minimal controls that prevent 90% of failures

- **Pin versions** (no mutable refs in prod).
- **Use one installer implementation everywhere**.
- **Require install receipts** (timestamp, ref, skill name, result).
- **Alert on drift/failure** within minutes, not days.
- **Keep rollback manifest ready**.

## Starter manifest example

```json
{
  "version": "2026-04-17",
  "channel": "staging",
  "repo": "your-org/skills",
  "ref": "skills-v2026.04.17.1",
  "skills": [
    { "name": "skill-a", "path": "skills/skill-a" },
    { "name": "skill-b", "path": "skills/skill-b" }
  ]
}
```

## Implementation notes by surface

- **CLI**: easiest to keep current; use startup sync + manual `sync-skills` command.
- **Desktop**: prefer background sync with retry/backoff; avoid blocking UX on network failures.
- **Website**: treat skills as deployment artifact; sync during build/release, not per-request.

## Tradeoff summary

- **Fastest setup**: startup-time install from manifest (simple, slight startup latency).
- **Most reliable**: build-time baking + runtime drift check (more infra work, strongest consistency).
- **Most flexible**: per-user dynamic install (high complexity and governance overhead).

## Operational checklist

- [ ] Manifest is pinned to immutable ref.
- [ ] Installer is idempotent and logs receipts.
- [ ] Drift check runs on each platform.
- [ ] Rollback manifest tested at least once.
- [ ] Promotion gates are automated.

## True push + global sync pipeline (baseline)

1. In Codex, create/update a skill folder and `SKILL.md`.
2. Run a safe dry-run of branch/commit planning:
   - `./scripts/push-skill.sh --skill <skill-folder>`
3. Apply and open a PR:
   - `./scripts/push-skill.sh --skill <skill-folder> --apply --push --open-pr`
4. On merge to `main`, GitHub Actions runs `skills-global-sync`:
   - Cross-platform dry-run sync matrix (Ubuntu/macOS/Windows)
   - Optional apply step when repo variable `GLOBAL_SYNC_APPLY=true`

# AGENTS

This repository is a reusable skills catalog.

- Keep root docs concise.
- Add new skills in dedicated folders.
- Prefer additive docs over replacing existing files.
- Merge README changes instead of overwriting current sections.

- Load only the relevant `SKILL.md`; follow the [kickoff example](README.md#kickoff-prompt).
- Whenever adding a skill, install it and sync it to Skill Sync (`skillsync.com`)
  using the [skill workflow](README.md#skill-sync). Preview uploads, keep them
  private, and verify the remote result. Report blocked syncs as incomplete.
- Sync skill packages only. `skl sync` uploads conversation history and must not
  be used for skill synchronization. Skillshare is a different product.
- Before finishing a change, run `python tools/validate_skills.py` and
  `python -m pytest -q`; see [setup](README.md#validation). Report failures and
  checks not run. Hardening scripts modify files; they are not validation commands.

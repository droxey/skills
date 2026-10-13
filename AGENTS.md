# AGENTS

This repository is a reusable skills catalog.

- Keep root docs concise.
- Add new skills in dedicated folders.
- Prefer additive docs over replacing existing files.
- Merge README changes instead of overwriting current sections.

- Load only the relevant `SKILL.md`; follow the [kickoff example](README.md#kickoff-prompt).
- Use Skillshare for distribution; inspect source and targets with the
  [Skillshare checks](README.md#skillshare) before proposing sync changes.
- Before finishing a change, run `python tools/validate_skills.py` and
  `python -m pytest -q`; see [setup](README.md#validation). Report failures and
  checks not run. Hardening scripts modify files; they are not validation commands.

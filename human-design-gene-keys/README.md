# Human Design and Gene Keys skill

A generic, source-grounded reading workflow with placement, sequence, whole-chart, interview, and tension-discovery modes. Start with [SKILL.md](SKILL.md).

## Use

> Use human-design-gene-keys in tensions mode with the attached chart. Discover possible tensions first; do not assume they describe my experience.

Attach the subject's source materials or a separate private chart-input file. The [blank template](templates/chart-input.md) is optional. Personal profiles and uploaded PDFs are intentionally excluded from this package.

The [research workflow](references/research-workflow.md) preserves the supplied generic master prompt. The [tensions protocol](references/tensions.md) adds chart-first discovery, source-conflict classification, counterexamples, and one-question-at-a-time intake. Neither document is a substitute for opening and verifying original teachings during a reading.

## Installation

Use **Skillsync's `skl` CLI** on the machine where the skill should be installed. The primary documentation below is hosted at **skillsync.com**. Confirm the service and signed-in account before transferring files; this package does not configure or install the distribution tool.

Extract the ZIP without overwriting an existing folder. Work from the parent of `human-design-gene-keys`.

### Inspect before writing

```bash
skl whoami
skl skills upload --help
skl skills install --help
skl skills list --scope user --json
```

Stop if the account is wrong, the installed CLI lacks these commands, or the destination contains conflicting work. Sign in locally with `skl login` when needed; never paste passwords or authentication tokens into a chat. User-scope installation writes to both `~/.claude/skills` and `~/.agents/skills`; inspect existing copies and symlinks before proceeding. Use project scope only when that is the intended destination.

### Preview and upload privately

```bash
skl skills upload ./human-design-gene-keys --dry-run
```

Review the included files and identity. Only this generic skill folder belongs in the upload. Keep charts, private input records, transcripts, PDFs, and other personal material outside it. If the upload would update an existing remote skill, inspect that version and stop on unexpected differences.

After reviewing the preview:

```bash
skl skills upload ./human-design-gene-keys
```

Skills are private by default. Do not enable public visibility or workspace sharing. Record the exact reference returned by the upload; do not infer its owner from a GitHub username.

### Install the uploaded version

Paste the exact reference returned by the upload when prompted:

```bash
printf 'Uploaded skill reference: '
IFS= read -r SKILL_REF
if [ -n "$SKILL_REF" ]; then
  skl skills show "$SKILL_REF" &&
  skl skills install "$SKILL_REF" --scope user
else
  printf 'No reference supplied; installation skipped.\n' >&2
fi
```

Do not force replacement of an existing copy. Verify the installed record and compare this package's files with both target copies:

```bash
skl skills list --scope user --json
```

### Sync boundaries

`skl skills sync` compares workspace skills; a named sync pulls a workspace version and never uploads. Workspace synchronization requires the intended workspace and skill to be identified first. No workspace is selected by this package.

`skl sync` uploads chat sessions. It is not part of installing this skill and must not be run for this task. A private upload plus a local install does not establish synchronization across other machines or workspaces.

No account upload, target installation, or workspace sync has been verified by this package's offline checks. A local agent completing the task must report the remote reference, actual destinations, file comparisons, and any remaining gaps. Do not commit or push repository changes as part of this workflow.

Primary command references:

- https://skillsync.com/docs/skills
- https://skillsync.com/docs/cli-reference
- https://skillsync.com/docs/quickstart

## Validation

From this directory:

```bash
python -m unittest discover -s tests -v
python -m pytest -q
```

Tests verify the package contract and integrity of the bundled public workflow. They make no network, model, account, or installation calls. They do not prove chart interpretation quality, scientific validity, or successful installation.

The [behavioral cases](evals/cases.json) are explicitly unrun. Evaluate them separately with a named model, version, run date, outputs, source access, and pass/fail rationale before claiming behavioral coverage.

## Dependencies and privacy

During readings, load `essence-doc` followed by `i-have-adhd` from the available skills catalog. Do not install them automatically. Disclose unavailable dependencies and apply the stated output principles. This package does not copy third-party skill code or copyrighted reference books.

Keep chart records and interview state outside all reusable skill directories. Syncing a generic workflow must never silently sync a subject's birth data or private experiences.

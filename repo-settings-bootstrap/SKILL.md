# Skill: Repo Settings Bootstrap v2

## Purpose

Ensure any repository you create or modify has repo settings as code.

If `.github/settings.yml` is missing, generate it automatically.

In v2, also generate companion governance files when justified:

- `.github/settings.yml`
- `.github/CODEOWNERS`
- branch protection defaults in `settings.yml` when the repo warrants them
- org-inheritance hints when the repo is governed by an org-level settings system

This skill is designed for two cases:

1. **Existing repository**: infer from actual repo state
2. **New repository**: infer from the project plan

The skill must make the smallest safe change, avoid speculative admin policy, and preserve existing explicit choices.

---

## Primary rule

When a repo is created or modified and `.github/settings.yml` does not exist:

1. inspect the repo or plan first
2. generate `.github/settings.yml`
3. decide whether `.github/CODEOWNERS` is also required
4. decide whether default-branch protection belongs in the first pass
5. prefer inheritance over duplication when org-level policy already exists

---

## When to use

Use this skill when:

- creating a new repo from a plan
- scaffolding a project
- standardizing existing repos
- auditing repos for missing governance files
- preparing repos for Settings App or safe-settings style workflows
- migrating ad hoc repo configuration into versioned files

---

## Do not use when

Stop or switch to merge-only mode if:

- `.github/settings.yml` already exists and appears authoritative
- the repo is mirrored from upstream and policy must remain external
- repo settings are centrally enforced and repo-local overrides are prohibited
- the repo uses another settings-as-code system that would conflict

If management context is ambiguous, prefer a minimal audit note over policy changes.

---

## Required inputs

Provide one of:

### Mode A: Existing repo
- repo root contents, local path, or repo URL the agent can inspect

### Mode B: New repo
- project plan, scaffold spec, or creation brief

Optional inputs:

- owner or org
- desired visibility
- default branch name
- whether Issues, Wiki, Discussions, Projects should be enabled
- expected deployment environments
- labels
- CODEOWNERS intent
- review / merge posture
- org inheritance model

If details are missing, infer conservatively.

---

## Outputs

### Minimum

- `.github/settings.yml`

### Companion outputs when warranted

- `.github/CODEOWNERS`
- audit note describing what was inferred vs verified
- short rationale for nontrivial policy choices

Do not generate extra governance files unless they materially reduce risk.

---

## Decision flow

### 1. Detect management context

Check for:

- existing `.github/settings.yml`
- `.github/CODEOWNERS`
- `.github/` workflows or docs referencing repo-settings, settings app, or safe-settings
- admin/infrastructure repos that appear to be inheritance sources
- `_extends` or inheritance patterns in existing settings files
- references to central policy in README, docs, or workflows

Choose one mode:

- `create`: no file exists, repo-local settings allowed
- `merge`: file exists, preserve explicit settings
- `inherit`: repo should only carry thin overrides or references
- `stop`: repo-local settings should not be authored here

### 2. Classify repo type

Infer one of:

- library or package
- application or service
- website or docs site
- teaching/course material
- template/starter
- internal tooling or ops repo
- infra/policy repo

### 3. Infer baseline repository policy

Use the lean baseline unless repo evidence says otherwise:

```yaml
repository:
  has_issues: true
  has_wiki: false
  has_projects: false
  delete_branch_on_merge: true
  allow_squash_merge: true
  allow_merge_commit: false
  allow_rebase_merge: false
```

Adjust cautiously:

- **internal or infra repos**: may be `private: true` if the plan or repo clearly implies private use
- **docs/course/content repos**: usually no wiki, usually no projects
- **public libraries**: issues usually on, squash merge usually on
- **static sites**: issues may still be on, wiki usually off
- **templates**: do not invent unsupported template-specific keys

Do not flip visibility without explicit evidence.

### 4. Infer metadata

Populate only when confidence is high:

- `name`
- `description`
- `homepage`
- `topics`
- `private`

Rules:

- never invent URLs
- keep topics sparse and high-signal
- derive description from README title/subtitle or plan summary
- do not rename an existing repo unless the user explicitly asked

### 5. Decide whether CODEOWNERS is required

Generate `.github/CODEOWNERS` when any of these are true:

- the repo will be governed by settings-as-code
- branch protection will require code owner review
- the repo contains CI/CD, infra, or security-sensitive workflows
- the repo is multi-surface and ownership boundaries are clear
- the user or plan explicitly wants governance hardening

Baseline output when evidence is weak but protection is needed:

```txt
* @OWNER
.github/ @OWNER
```

Prefer more specific ownership only when you have actual ownership signals from the repo or plan.

### 6. Decide whether to emit branch protection

Only emit `branches` rules when the repo clearly benefits from them.

#### Emit branch protection by default for:

- production software repos
- infra or deployment repos
- shared libraries with active collaboration
- repos with CI workflows or release automation
- repos where CODEOWNERS is present or should be present

#### Usually omit on first pass for:

- personal scratch repos
- single-file notes/docs repos
- archived or mirror repos
- low-risk course/content repos unless the plan asks for review gates

Conservative default for the default branch:

- require pull request before merge
- require 1 approving review
- dismiss stale reviews only if that fits existing workflow signals
- require up-to-date branch only if CI exists
- require code owner review only if CODEOWNERS exists or is generated

Do not invent branch names. Infer from repo evidence or default to the plan’s chosen default branch.

### 7. Decide whether to use org inheritance

Prefer inheritance or thin overrides when:

- the org appears to manage settings centrally
- repos share a common baseline policy
- the repo should only define deltas from org standards

When inheritance is detected or clearly intended:

- keep repo-local `settings.yml` minimal
- include only repo-specific overrides
- avoid copying org-wide labels, teams, or branch rules into every repo

If the repo already uses `_extends` or a known inheritance mechanism, preserve it.

### 8. Merge behavior

When updating an existing file:

- preserve explicit values
- add only missing sections
- do not erase comments unless necessary
- avoid changing visibility, collaborators, teams, or environments unless directly requested
- preserve branch rules unless clearly broken or incomplete

---

## Authoring rules

### Rule 1: inspect before generating

Read the repo or plan first. No blind templates.

### Rule 2: minimal necessary config

Write only settings justified by evidence or low-risk defaults.

### Rule 3: no speculative admin actions

Do not add collaborators, teams, secrets, environments, required status checks, or exceptions without evidence.

### Rule 4: reversible first pass

Prefer settings that improve hygiene without blocking work.

### Rule 5: companion governance only when justified

Generate `CODEOWNERS` and branch protection only when they materially improve correctness or risk posture.

### Rule 6: respect inheritance

Do not duplicate org policy into every repo when the repo should inherit.

### Rule 7: stable YAML

Keep ordering predictable and the file compact.

---

## Existing repo inspection checklist

Inspect these before generating anything:

- repo name
- README title and summary
- license
- package or module metadata (`package.json`, `go.mod`, `pyproject.toml`, etc.)
- existing `.github/` files
- workflows and deployment jobs
- issue templates / PR templates / discussions config
- docs or site config
- branch names referenced in workflows/docs
- environment names referenced in workflows
- ownership hints from monorepo layout, CODEOWNERS, or plan docs

---

## New project plan inspection checklist

Extract these from the plan:

- project name
- one-line description
- public/private intent
- repo type
- whether issues should be enabled
- whether wiki/projects/discussions are wanted
- expected environments
- merge/review posture
- ownership expectations
- topics
- whether the repo is meant to inherit org policy

If the plan is incomplete, emit a lean first pass and record assumptions.

---

## Output contract

Return, in this order:

1. mode selected: `create`, `merge`, `inherit`, or `stop`
2. generated or updated `.github/settings.yml`
3. generated `.github/CODEOWNERS` if applicable
4. assumptions
5. validation notes

---

## Generation templates

### A. Lean baseline settings

```yaml
repository:
  has_issues: true
  has_wiki: false
  has_projects: false
  delete_branch_on_merge: true
  allow_squash_merge: true
  allow_merge_commit: false
  allow_rebase_merge: false
```

### B. Baseline CODEOWNERS

```txt
* @OWNER
.github/ @OWNER
```

### C. Baseline protected default branch

Use only when justified:

```yaml
branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 1
      enforce_admins: false
```

Replace `main` only when repo evidence shows a different default branch.

---

## Validation

Validate all outputs before claiming completion.

### Validate `.github/settings.yml`

Check:

- YAML parseability
- no duplicate keys
- no unresolved placeholders
- no unsupported or suspicious keys
- consistency with repo facts or plan
- no risky visibility/collaborator/team changes without evidence

### Validate `.github/CODEOWNERS`

Check:

- syntax is parseable line-by-line
- referenced owners are grounded in plan or repo context
- patterns are not over-broad unless using the intentional minimal baseline
- `.github/` is explicitly owned when settings-as-code is enabled

### Validate branch rules

Check:

- branch name exists or is the explicit planned default
- protections match repo maturity
- no required checks are named unless they are verified from CI
- code owner review is only required when CODEOWNERS exists

### Validate inheritance behavior

Check:

- repo-local file does not duplicate obvious org-wide policy
- `_extends` or equivalent inheritance mechanisms are preserved if already present
- repo-specific overrides are minimal and explainable

---

## Failure handling

If evidence is insufficient:

- emit the lean baseline only
- omit risky sections
- state assumptions clearly

If the repo appears centrally managed:

- switch to `inherit` or `stop`
- explain why
- do not generate conflicting local policy

If an existing file is malformed:

- repair only the broken portions
- preserve intent where recoverable
- note unverified sections

---

## Token-efficiency guidance

Optimize for agent reading:

- inspect only high-signal files first
- do not dump full repo trees unless needed
- emit compact YAML
- prefer a short assumptions block over long narrative
- avoid duplicate rationale across sections

---

## Success criteria

The skill succeeds when:

- a missing `.github/settings.yml` is added correctly
- the file reflects real repo or plan evidence
- `CODEOWNERS` is added only when justified
- branch protection is added only when justified
- inheritance is respected
- no speculative admin policy is introduced

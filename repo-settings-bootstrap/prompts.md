# Prompts for `Repo Settings Bootstrap v2`

## 1. Existing repo: create missing settings

```md
Inspect this repository.
If `.github/settings.yml` is missing, generate it.
Read the repo first:
- README
- package/module metadata
- license
- workflows
- existing `.github/` files
- branch references
Use the smallest safe settings file.
Also decide whether `.github/CODEOWNERS` is required.
Only add branch protection if the repo clearly warrants it.
Respect central inheritance if detected.
Return:
1. selected mode
2. `.github/settings.yml`
3. `.github/CODEOWNERS` if generated
4. assumptions
5. validation notes
```

## 2. New repo from plan

```md
Use this project plan to generate repo governance bootstrap files.
If `.github/settings.yml` is missing, create it from the plan.
Infer only conservative defaults when the plan is silent.
Also decide whether `.github/CODEOWNERS` belongs in v1.
Add protected default-branch rules only if the plan implies review gates.
If the repo should inherit org policy, keep the repo-local file minimal.
Return:
1. selected mode
2. `.github/settings.yml`
3. `.github/CODEOWNERS` if generated
4. assumptions
5. validation notes
```

## 3. Merge into existing settings file

```md
Inspect the existing `.github/settings.yml`.
Merge in only missing or clearly needed sections.
Preserve explicit values.
Do not change visibility, collaborators, teams, environments, or branch names unless directly supported.
If CODEOWNERS is missing, decide whether it is warranted.
Return the updated files and a concise change summary.
```

## 4. Strict repo-aware generation

```md
Generate repo settings only after inspecting repository evidence.
Use actual repo signals, not generic templates.
Prefer a lean baseline.
Do not invent URLs, owners, required checks, teams, or environment rules.
Require code owner review only if CODEOWNERS exists or is generated.
Validate YAML, CODEOWNERS, and branch rules before final output.
```

## 5. Inheritance-aware generation

```md
Inspect this repo for central settings management.
If the org appears to manage policy centrally, do not duplicate org-wide settings locally.
Preserve `_extends` or equivalent inheritance mechanisms if present.
Generate only repo-specific overrides.
If repo-local policy should not be authored, switch to stop mode and explain why.
```

## 6. CODEOWNERS decision pass

```md
Decide whether this repo needs `.github/CODEOWNERS`.
Generate it only if settings-as-code, branch protection, CI/CD, infra, or clear ownership boundaries justify it.
Use the narrowest correct ownership map.
If evidence is weak, use the minimal baseline only:
* @OWNER
.github/ @OWNER
Return the file and the reason it was or was not generated.
```

## 7. Branch protection decision pass

```md
Decide whether this repo should include default-branch protection in `.github/settings.yml`.
Only add it when the repo is a production software repo, infra repo, shared library, or otherwise needs review gates.
Never invent required status checks.
Require code owner review only if CODEOWNERS exists or will be generated.
Return the branch rule or explain why it was omitted.
```

## 8. Validation-only pass

```md
Validate these repo governance files:
- `.github/settings.yml`
- `.github/CODEOWNERS`
Check:
- YAML parseability
- duplicate keys
- unresolved placeholders
- unsupported or suspicious keys
- CODEOWNERS line validity
- mismatches with repo facts or plan
- risky or speculative governance changes
Return issues first, then corrected files if needed.
```

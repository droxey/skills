# Markdown Mode Router Prompts

Use these prompts to invoke the skill.

## Route a file

```md
Use markdown-mode-router.
repo: OWNER/REPO
file: path/to/file.md
goal: choose the correct markdown mode and normalize structure
```

## Apply general mode

```md
Use markdown-mode-router.
repo: OWNER/REPO
file: path/to/file.md
force_mode: general
goal: format this as a non-course markdown file
```

## Apply teaching mode

```md
Use markdown-mode-router.
repo: ACS-XXXX-Course-Repo
file: path/to/file.md
goal: keep teaching constraints and avoid non-course formatting drift
```

## TOC check

```md
Use markdown-mode-router.
repo: OWNER/REPO
file: path/to/file.md
goal: decide whether this file qualifies for a TOC
```

## Refactor an existing note

```md
Use markdown-mode-router.
repo: OWNER/REPO
file: path/to/file.md
goal: rewrite this note into the correct markdown strategy with the minimum necessary change
```

## Expected response contract

```md
Selected Mode
Why
TOC Decision
Heading Plan
Formatted Markdown
Assumptions
```

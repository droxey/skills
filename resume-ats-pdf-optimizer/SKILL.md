---
name: resume-ats-pdf-optimizer
description: Score and improve a resume PDF against a job description using ATS gap analysis and minimal, layout-preserving edits. Use this skill whenever the user asks to tailor a resume, score ATS compatibility, find missing JD keywords, or update a resume PDF without changing formatting or typography.
---

# Overview

Use this skill to run a repeatable ATS optimization workflow on a resume PDF and produce minimal-change edits that preserve visual fidelity.

Primary outputs:
1. ATS-style scorecard (0-100).
2. Gap report (keywords, skills, experience evidence, formatting risk).
3. Minimal edit plan for the existing PDF.
4. Updated PDF with unchanged layout/typography whenever technically possible.

Read `SOURCE.md` for the evidence base that drives scoring weights and priorities.

## Workflow

### 1) Collect inputs

Require:
- Resume PDF (source of truth for formatting/layout).
- Target job description text.

Optional:
- Target job title and seniority.
- Hard constraints (no fabrication, no metric invention, no date changes).

### 2) Build ATS scorecard

Score with these weighted dimensions (100 points total):
- **Keyword coverage (35 pts):** exact-match JD terms found in resume text.
- **Experience evidence alignment (35 pts):** JD requirements reflected in experience bullets.
- **Skills section alignment (15 pts):** required tools/certs/frameworks present verbatim.
- **Structure/parse safety (15 pts):** basic ATS readability risks (tables, columns, graphics-heavy blocks, nonstandard headers).

Default interpretation:
- 80+: strong match.
- 70-79: likely competitive but can improve.
- 50-69: moderate mismatch.
- <50: high risk for de-prioritization.

### 3) Run gap analysis

Produce these artifacts:
- **Missing keywords list:** JD terms absent from resume (exact strings).
- **Weak evidence list:** requirements mentioned in summary/skills but unsupported in experience bullets.
- **Section-level flags:** experience, skills, and parsing-risk issues.

Prioritize edits in this order:
1. Experience bullets (highest impact).
2. Skills section.
3. Summary/headline.
4. Formatting fixes only if parser risk exists.

### 4) Generate minimal edits

Rules:
- Keep every original section position and order unless user asks to reorder.
- Preserve line breaks, spacing rhythm, and bullet style when possible.
- Prefer substitutions over insertions.
- If inserting text, replace low-value phrasing first.
- Never add unsupported claims.

Edit style:
- Use JD-exact terms where true.
- Keep bullets concise and outcome-oriented.
- Maintain the user’s original voice and tense.

### 5) Choose PDF update method (layout-preserving first)

Use this decision order for "fewest visual changes":

1. **In-place text patching in PDF content streams** using `pikepdf` + targeted stream edits.
   - Best when edits are short and can fit existing text boxes.
   - Highest chance of preserving exact typography/layout.
   - Requires careful character-length and encoding handling.

2. **Overlay approach** (generate transparent overlay PDF and merge with original) using ReportLab + `pikepdf`/`qpdf`.
   - Best when replacing specific lines/blocks with strict coordinates.
   - Keeps original PDF untouched underneath.
   - Must match font, size, and coordinates precisely.

3. **DOCX round-trip fallback** only if source is clearly exported from editable DOCX and user accepts potential drift.
   - Higher risk of spacing reflow.
   - Not default for strict visual preservation.

Avoid as primary path:
- Full PDF re-render/conversion pipelines that reconstruct layout globally.

### 6) Verify output integrity

Before delivery, verify:
- Page count unchanged (unless explicitly requested).
- Non-edited regions visually unchanged.
- Fonts, margins, and section geometry preserved.
- Text remains selectable and parsable.
- ATS score improved vs baseline.

Return:
- Baseline score, updated score, delta.
- Exact list of edited lines/areas.
- Any unavoidable compromises (e.g., tiny kerning shifts).

## Guardrails

- Do not fabricate accomplishments, tools, or certifications.
- Do not claim ATS "pass" guarantees.
- Treat score as heuristic ranking, not employer truth.
- If PDF is image-only/scanned, run OCR first and report confidence limits.

## Response template

Use this structure when executing the skill:

1. **Goal**
2. **Constraints**
3. **Baseline scorecard**
4. **Top gaps (ranked by impact)**
5. **Minimal edit plan**
6. **PDF update method chosen + why**
7. **Post-edit scorecard + delta**
8. **Verification checks**
9. **Unverified edges / risks**

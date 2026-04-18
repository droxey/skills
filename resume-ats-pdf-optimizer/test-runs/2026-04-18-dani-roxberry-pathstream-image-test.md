# Resume ATS Skill Test Run — Dani Roxberry (Image Inputs)

Date: 2026-04-18  
Skill: `resume-ats-pdf-optimizer`

## Goal
Test the skill workflow end-to-end using:
1. A screenshot image of a Pathstream job description.
2. An image of Dani Roxberry's current ATS resume.

## Constraints
- Input quality limitation: both assets are images; no source PDF or raw JD text provided.
- JD image is very tall and low-resolution; only partial content is reliably legible.
- No fabricated claims; only observed resume content can be used.
- Preserve existing resume structure (Summary, Work Experience, Skills, Contact).

## Input Snapshot (What was legible)

### Resume image (high confidence)
Observed role/profile highlights:
- Title: Artificial Intelligence Engineer.
- Summary: 5+ years in AI development/education; AI code review pipelines and mentoring.
- Experience includes:
  - Instructor: Computer Science, Dominican University of California (AI review pipeline, curriculum delivery).
  - Founder: Muse & Machine.
  - Instructor: Full Stack Web, Make School.
  - Instructor: Full Stack Web/Data Science, UC Berkeley Extension.
- Skills include: Python, Node.js, C#, AWS, Docker, Kubernetes, RAG, LLMs, IaC, DevOps.

### Pathstream JD image (limited confidence)
Observed with partial confidence:
- Employer/brand appears to be Pathstream.
- Contains long-form sections consistent with responsibilities and qualifications.
- Repeated themes appear to include curriculum/instruction, learner outcomes, technical content, and cross-functional collaboration.

## Baseline Scorecard (Provisional due image-only JD)
Scoring weights:
- Keyword coverage (35)
- Experience alignment (35)
- Skills alignment (15)
- Structure/parse safety (15)

Estimated baseline:
- Keyword coverage: **20/35** (many JD-exact strings not reliably extracted from image).
- Experience evidence alignment: **28/35** (strong teaching + engineering overlap).
- Skills section alignment: **11/15** (broad technical stack present, but uncertain JD exact-match terms).
- Structure/parse safety: **14/15** (single-column ATS-friendly layout, standard headers).

**Baseline total: 73/100 (provisional).**

## Top Gaps (Ranked)
1. **JD-exact phrase coverage gap** (highest impact)
   - Because JD text is image-only and low resolution, exact keywords were not fully captured.
2. **Role-title targeting gap**
   - Resume headline says "Artificial Intelligence Engineer"; likely may benefit from adding JD-specific role title variant if accurate.
3. **Evidence specificity gap**
   - Strong teaching outcomes are present, but some bullets could be tightened to mirror JD phrasing on learner impact and program operations.

## Minimal Edit Plan (No fabrication)
1. Keep full section order and formatting unchanged.
2. In Summary, swap one generic phrase for one JD-exact phrase once JD text is available.
3. In top 3 experience bullets, replace broad verbs with JD-aligned action terms (only where true).
4. In Skills, reorder top 8 skills to prioritize JD-required tools/terms.
5. Add no new metrics unless already supported by source resume.

## PDF Update Method Chosen
**Method selected: planning-only test (no PDF patch execution).**

Reason:
- This test used image inputs only; no editable resume PDF file was supplied.
- In a full run, preferred method remains in-place PDF stream text patching (method #1 in skill), falling back to overlay only if replacement text length cannot fit existing boxes.

## Post-Edit Scorecard (Simulated)
Assuming JD exact text becomes available and only minimal line edits are made:
- Keyword coverage: **29/35**
- Experience evidence alignment: **31/35**
- Skills section alignment: **13/15**
- Structure/parse safety: **14/15**

**Projected post-edit total: 87/100**  
**Projected delta: +14 points**

## Verification Checks
- Section order preserved in plan: ✅
- No unsupported claims introduced: ✅
- ATS parse-safe structure retained: ✅
- Score framed as heuristic (not guaranteed pass): ✅

## Unverified Edges / Risks
- Exact JD keyword extraction is incomplete without a clearer image or raw text.
- Final keyword score may vary once true JD strings are parsed verbatim.
- No visual PDF diff was possible because no source PDF file was provided.

## Next-Step Execution (for full-fidelity run)
1. Provide original JD text (or higher-resolution image/PDF).
2. Provide source resume PDF.
3. Run exact-keyword extraction, then apply minimal in-place text patching.
4. Re-score with before/after report and edited-line log.

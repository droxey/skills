# Droxey Teaching Video System — Product and Skill Specification

**Status:** Design handoff  
**Owner:** Dani Roxberry  
**Namespace:** `droxey-`  
**Primary implementation targets:** reusable agent skills, Go CLI, Bubble Tea TUI  
**Source system:** Grain recordings and transcripts  

## 1. Purpose

Build a reliable system that turns Dani Roxberry's Grain archive into a searchable, resumable teaching-video pipeline that:

1. Archives every accessible recording and transcript.
2. Evaluates whether each recording is safe, valuable, current, and reusable.
3. Identifies useful teaching segments.
4. Supports deliberate clip extraction.
5. Converts approved material into distinctive, polished teaching videos.
6. Preserves Dani's teaching voice, production experience, privacy constraints, and sustainable workload.
7. Learns from publishing results over time.

The system must not collapse archival, content judgment, production, and publishing into one opaque workflow. Each stage must have a clear contract and must be independently testable.

---

## 2. Settled Product Decisions

The following decisions are locked unless Dani explicitly changes them.

### 2.1 Archive behavior

- Product mode: **archive + incremental sync**.
- First run exports all accessible Grain recordings.
- Later runs fetch only new or changed recordings and repair incomplete items.
- Quitting the TUI performs a **safe stop**; no background daemon in v1.
- Partial downloads must be preserved and resumed.
- macOS is the first supported platform.
- Authentication uses macOS Keychain.
- `GRAIN_API_TOKEN` is an explicit environment-variable override.

### 2.2 Per-recording archive bundle

Each recording archive must contain:

- Original media file
- Markdown transcript
- SRT captions
- Raw transcript JSON
- Metadata JSON

Recommended layout:

```text
grain-archive/
  YYYY/
    YYYY-MM-DD_recording-slug/
      recording.mp4
      transcript.md
      captions.srt
      transcript.json
      metadata.json
      analysis.json
      clips/
  manifest.jsonl
  manifest.csv
  failures.jsonl
```

All derivatives must reference the immutable source recording ID and source timestamps.

### 2.3 TUI model

Use **guided setup + focused dashboard**.

First run:

- Authenticate
- Select destination
- Confirm settings
- Begin sync

Subsequent runs open the sync dashboard directly.

Required dashboard signals:

- Total recordings
- Completed, queued, active, retrying, failed
- Current recording
- Current media progress
- Current analysis status
- Safe-stop state
- Latest error

Suggested controls:

```text
p  pause/resume
r  retry failed
x  review/extract clips
d  details
s  settings
q  quit safely
```

### 2.4 Analysis provider

- OpenAI is the sole semantic-analysis provider in v1.
- Deterministic local checks handle duration, file integrity, transcript statistics, audio metrics, and sampled-frame findings.
- Missing evidence must remain `UNKNOWN`; the model must never infer unavailable media quality.

### 2.5 Analysis timing

- Each successfully archived recording enters an independent analysis queue immediately.
- Archive failures must not corrupt or block analysis of other recordings.
- Analysis failures must not affect archive integrity.

### 2.6 Recording routes

The final recording route is one of:

- `DIRECT_USE`
- `REBUILD`
- `EXCLUDE`

`NEEDS_REVIEW` is a temporary workflow state, not a fourth final route.

Definitions:

- `DIRECT_USE`: usable after light editing only, such as trimming, captions, normalization, and branding.
- `REBUILD`: valuable material requiring rerecording, updated technical details, replacement visuals, or significant restructuring.
- `EXCLUDE`: weak, obsolete, student-heavy, sensitive, unauthorized, or fundamentally unusable material.
- `NEEDS_REVIEW`: evidence is incomplete, confidence is low, authorship is ambiguous, or another human decision is required.

### 2.7 Student and external-speaker handling

- Dani-led lectures may proceed when students are primarily listeners.
- Student presentations, breakout sessions, critiques, or student-heavy participation must be excluded automatically when confidence is high.
- Externally led webinars, guest talks, or meetings must route to `NEEDS_REVIEW`, not automatic reuse.
- The system must not use external speakers' material as Dani-authored source material without review.

### 2.8 Clip extraction

- The system proposes up to three candidate segments per recording.
- Extraction is **review-and-select**, never automatic by default.
- Candidate clips must not overlap or substantially duplicate one another.
- Every candidate must retain source recording ID, start time, end time, gate version, evidence, and checksum.
- Candidate clips inherit privacy, student-content, authorship, and technical-currency checks.
- `NEEDS_REVIEW` and externally led material cannot be auto-extracted.

### 2.9 Content scope

The system may identify any reusable Dani-led teaching or technical content, including:

- Programming
- AI engineering
- Agent systems
- Systems architecture
- Developer tooling
- Technical leadership
- Career mentoring
- Technical education

The system is not limited to Episodes in AI.

---

## 3. Canonical Recording Gate

The canonical skill is:

```text
droxey-recording-gate
```

It owns the versioned recording-evaluation contract used by the Teaching System and Go downloader.

### 3.1 Inputs

Canonical input uses Grain v2 recording and transcript structures plus a namespaced local evidence object:

```json
{
  "recording": {},
  "transcript": {},
  "analysis_evidence": {
    "duration_seconds": 0,
    "speaker_statistics": {},
    "audio_metrics": {},
    "sampled_frame_findings": {},
    "file_integrity": {},
    "user_settings": {}
  }
}
```

The skill may accept plain files or attachments interactively, but must normalize them into this structure before evaluation.

### 3.2 Eight-point gate

Each gate result must contain:

- `status`: `PASS`, `WARN`, `FAIL`, or `UNKNOWN`
- Evidence
- Confidence
- Relevant timestamps
- Routing effect

#### Gate 1 — Authorship and reuse rights

Determine whether Dani leads or materially owns the teaching content and whether reuse is permitted.

- Dani-led: may proceed.
- Externally led or ambiguous: `NEEDS_REVIEW`.
- Clearly unauthorized: `EXCLUDE`.

#### Gate 2 — Student, private, and sensitive content

- Dani-led lecture with students mostly listening: may proceed.
- Student-heavy session: `EXCLUDE` when confidence is high.
- Sensitive or private content: `EXCLUDE` when confidence is high.
- Ambiguous privacy status: `NEEDS_REVIEW`.

#### Gate 3 — Teaching value

The recording or segment must contain a clear, transferable lesson, explanation, method, demonstration, decision, or production insight.

No reusable teaching value may produce `EXCLUDE` when confidence is high.

#### Gate 4 — Originality

The content should include Dani's framing, experience, reasoning, examples, or distinctive explanation—not merely generic topic coverage.

Low originality alone should normally reduce priority or produce `REBUILD`, not automatic exclusion, unless the material has no meaningful value.

#### Gate 5 — Coherence and segmentability

The recording must work as a whole or contain up to three self-contained, understandable candidate segments.

Evidence should include timestamps and a concise segment thesis.

#### Gate 6 — Technical currency

- Current and accurate: may proceed.
- Valuable but fixable: `REBUILD`.
- Fundamentally obsolete premise: `EXCLUDE` when confidence is high.
- Uncertain currency: `NEEDS_REVIEW` or `WARN` depending on severity.

#### Gate 7 — Audio, delivery, and transcript quality

- Light-edit quality: supports `DIRECT_USE`.
- Strong content with poor production quality: `REBUILD`.
- Unavailable audio evidence: `UNKNOWN`; do not guess.

#### Gate 8 — Visual usefulness

- Clear, readable visuals: supports `DIRECT_USE`.
- Valuable transcript with poor or absent visuals: `REBUILD`.
- Unavailable visual evidence: `UNKNOWN`; do not guess.

### 3.3 Automatic exclusion policy

Automatic `EXCLUDE` is allowed only for high-confidence hard failures:

- Student-heavy or sensitive material
- No reusable teaching value
- Clearly unauthorized reuse
- Fundamentally obsolete premise
- Deterministic duration exclusion

Ambiguous cases must become `NEEDS_REVIEW`.

### 3.4 Output

The skill returns both:

1. Concise human-readable review
2. Strict versioned JSON

Required JSON fields:

```json
{
  "schema_version": "1.0.0",
  "gate_version": "1.0.0",
  "recording_id": "",
  "route": "DIRECT_USE",
  "workflow_state": "COMPLETE",
  "confidence": 0.0,
  "summary": "",
  "gates": [],
  "candidate_segments": [],
  "exclusion_reason": null,
  "review_reasons": [],
  "model": "",
  "analyzed_at": ""
}
```

Every downstream artifact must preserve `gate_version`.

---

## 4. Settings and Naming Contract

Settings names must describe domain behavior, not implementation mechanics. Avoid vague names such as `custom-minimum`, `custom-maximum`, `min`, or `max` without context.

### 4.1 Recommended YAML structure

```yaml
archive:
  destination_directory: ~/Movies/Grain Archive
  concurrent_downloads: 2
  verify_checksums: true

recording_filter:
  minimum_recording_duration: 30s

analysis:
  provider: openai
  model: null
  analyze_after_download: true
  maximum_candidate_segments_per_recording: 3

clip_candidates:
  duration_profile: teaching_clip
  minimum_candidate_duration: null
  maximum_candidate_duration: null

clip_extraction:
  mode: selected_only
  output_directory_name: clips
```

### 4.2 Duration parsing

Accepted user forms:

- `10s`
- `30s`
- `90s`
- `1m`
- `5m`
- `25m`

Reject unitless values.

Internally normalize to integer seconds.

### 4.3 Recording duration filter

```yaml
recording_filter:
  minimum_recording_duration: 30s
```

Rules:

- Default: `30s`
- `0s` disables the recording-duration filter.
- A recording is excluded only when `duration < threshold`.
- A recording exactly equal to the threshold passes.
- Exclusion reason: `DURATION_BELOW_MINIMUM`.
- This deterministic check runs before OpenAI analysis.

### 4.4 Candidate clip profiles

Profiles must remain in this order:

1. `teaching_clip` — default: `1m` to `5m`
2. `social_clip`: `30s` to `2m`
3. `mini_lesson`: `3m` to `15m`

The user may override profile bounds with:

```yaml
clip_candidates:
  minimum_candidate_duration: 45s
  maximum_candidate_duration: 8m
```

Safeguards:

- Absolute minimum candidate duration: `10s`
- Absolute maximum candidate duration: `25m`
- `minimum_candidate_duration` must be less than `maximum_candidate_duration`.
- Explicit overrides take precedence over profile defaults.
- Candidate segments should contain complete thoughts, not merely fill the target duration.

### 4.5 CLI flag names

Recommended flags:

```text
--minimum-recording-duration 30s
--clip-duration-profile teaching_clip
--minimum-candidate-duration 45s
--maximum-candidate-duration 8m
--maximum-candidate-segments 3
--clip-extraction-mode selected_only
```

Avoid aliases in v1 unless a clear ergonomic need appears. Descriptive flags are preferable to short ambiguous flags.

### 4.6 TUI profile help text

Present profiles in the required order:

#### Teaching clip · 1–5 minutes · Default

Best for LinkedIn, standard YouTube, Muse & Machine, or a course/LMS. Clips at or below three minutes may also be adapted into square or vertical YouTube Shorts.

#### Social clip · 30–120 seconds

Best for YouTube Shorts, Instagram Reels, TikTok, or LinkedIn. Prepare a vertical 9:16 version with readable captions.

#### Mini-lesson · 3–15 minutes

Best for standard YouTube, LinkedIn, Muse & Machine, a course/LMS, or X-Pilot source material.

Posting guidance is advisory. Selection or extraction must not publish, upload, crop, brand, or otherwise distribute a clip automatically.

---

## 5. Teaching-System Integration

The recording gate and Teaching System must not duplicate policy.

Recommended flow:

```text
Archive
  ↓
droxey-recording-gate
  ↓
DIRECT_USE / REBUILD / EXCLUDE / NEEDS_REVIEW
  ↓
Teaching System
  ↓
Teaching Voice → Social Learning → Write Like You Talk → Essence
```

Rules:

- `droxey-recording-gate` is canonical for source qualification.
- The Teaching System invokes it when source material includes recordings, transcripts, meetings, webinars, or classroom media.
- The Teaching System consumes the gate output; it must not reimplement the eight gates.
- Social Learning remains downstream. A source must not be excluded merely because its original lesson lacked social-learning mechanisms.
- Existing Teaching Voice rules remain responsible for transforming approved material into Dani's builder-teacher voice.

Existing skill names may be migrated separately. Do not rename existing skills as part of recording-gate implementation unless explicitly approved.

---

## 6. Teaching Video Production System

The production system converts qualified sources into distinctive videos. Its orchestration skill is:

```text
droxey-teaching-video-director
```

The director may compose these specialist capabilities:

- `droxey-teaching-video-format-research`
- `droxey-teaching-video-creative-director`
- `droxey-teaching-video-storyboard`
- `droxey-teaching-video-retention-review`
- `droxey-teaching-video-production-qc`
- `droxey-teaching-video-packager`
- `droxey-teaching-video-pattern-library`
- `droxey-technical-visual-designer`

These do not all need to be separate runtime invocations. Implementation agents should preserve logical boundaries and avoid unnecessary operational complexity.

### 6.1 Signature framework

The production system must combine all three approved concepts:

1. **Break it → Fix it → Prove it**
2. **What tutorials leave out**
3. **What stays human / what the system should do**

Recommended default narrative:

```text
Cold open
  ↓
Break It
  ↓
What Tutorials Leave Out
  ↓
Fix It
  ↓
Prove It
  ↓
What Stays Human
  ↓
Production Rule
```

This is a flexible grammar, not a mandatory visible heading sequence. A video may compress or reorder beats when justified, but it should preserve tension, technical clarity, proof, and a transferable conclusion.

### 6.2 Recurring branded teaching devices

Candidate devices:

- Hidden Assumption
- Reality Check
- System Map
- Proof
- Production Rule
- What I Would Actually Ship
- What Stays Human
- Do Not Do This

The creative-director skill must determine how these appear visually and when they are useful. Do not add every device to every video.

### 6.3 Teaching-video pattern library

Each pattern should include:

```yaml
name: delayed_reveal
purpose: create_curiosity
best_for:
  - technical_explanation
recommended_duration: 5s-15s
inputs: []
outputs: []
risks:
  - clickbait
  - delayed_value
examples: []
evidence: []
```

The pattern library must distinguish:

- Generalizable structural patterns
- Platform conventions
- Dani-specific signature patterns
- Creator-specific identity that must not be copied

Research should extract principles, not imitate another creator's brand, voice, wording, graphics, or persona.

### 6.4 Technical visual designer

Given an explanation, the visual designer chooses among:

- Camera
- Screen recording
- Terminal
- Code build
- Architecture diagram
- Timeline
- Flowchart
- Animated analogy
- Whiteboard
- Side-by-side comparison
- Zoom or focus treatment
- Typography-only emphasis

The goal is not maximal animation. The goal is showing the correct evidence or mental model at the correct moment.

### 6.5 Storyboard contract

A storyboard entry should support:

```yaml
start_time: 0s
end_time: 15s
spoken_content: ""
visual_content: ""
camera_framing: ""
screen_action: ""
diagram_or_animation: ""
text_overlay: ""
sound_cue: ""
source_recording_id: ""
source_start_time: null
source_end_time: null
technical_claims: []
proof: []
accessibility_notes: []
```

The storyboard must explicitly decide whether to:

- Keep original footage
- Trim original footage
- Rerecord narration
- Record direct-to-camera material
- Replace visuals
- Create diagrams or motion graphics
- Add proof or demonstration

### 6.6 Production quality review

The QA layer must verify:

- Technical correctness and currency
- Claims supported by visible proof
- Audio consistency
- Caption accuracy
- Mobile readability
- Contrast and non-color-only meaning
- Safe placement around platform interface overlays
- Motion clarity
- Rights and licenses
- Student and private-content removal
- Source traceability
- No automatic publishing

---

## 7. Unresolved Research Work

The following areas are intentionally not locked. Other agents should investigate these without reopening settled decisions.

### 7.1 Visual identity system

Not yet locked:

- Color system
- Typography
- Diagram grammar
- Thumbnail grammar
- Camera framing system
- Lower thirds
- Motion curves
- Transition vocabulary
- Sound palette
- Illustration style
- Code and terminal theme

Required output:

- A small, reusable design system
- Mobile-first readability rules
- Accessible contrast
- Remotion-compatible tokens and components
- At least three representative video-frame mockups
- Explicit anti-patterns

### 7.2 Hook taxonomy and selection process

Not yet locked:

- Canonical hook categories
- Selection rubric
- Number of hook variants generated
- Whether hooks are manually selected or scored
- Relationship between title, thumbnail, first frame, and first spoken line

Required output:

- Hook schema
- Evaluation rubric
- Examples adapted to Dani's topics
- Failure modes and anti-clickbait rules

### 7.3 On-camera performance direction

Not yet locked:

- Energy and pacing targets
- Gesture and eye-line guidance
- Camera distance
- Direct-to-camera versus voiceover rules
- Humor boundaries
- Rerecord triggers
- Performance self-review rubric

Required output:

- Practical coaching rubric
- Minimal setup requirements
- Examples for short, teaching, and mini-lesson profiles

### 7.4 Publishing strategy

Not yet locked:

- Primary platform
- Publication order
- Cadence
- Cross-platform adaptation rules
- Calls to action
- Community response boundaries
- What not to repurpose

Required output:

- Platform matrix
- Default release sequence
- Reuse rules
- No-auto-publish safeguards

### 7.5 Analytics and learning loop

Not yet locked:

- Canonical metrics
- Storage schema
- Platform data import method
- Success thresholds
- Experiment design
- Pattern-library update rules

At minimum evaluate:

- Click-through rate
- First-30-second retention
- Average percentage viewed
- Retention spikes and dips
- Saves
- Shares
- Comments
- Follows
- Search versus recommendation traffic
- Conversion into courses, newsletter, or products
- Performance by hook, topic, duration, and format

Required output:

- Versioned analytics schema
- Experiment contract
- Rules for updating production patterns
- Clear distinction between correlation and causation

### 7.6 Sustainable operating constraints

Known principles:

- Low friction
- ADHD-aware
- Protect home tasks and personal time
- Avoid audience-access obligations
- Publish rather than endlessly polish

Not yet locked:

- Maximum production hours per video
- Maximum active videos
- Release cadence
- Batch-recording limits
- Home-life cutoff
- Minimum acceptable production quality
- Comment and message boundaries

Required output:

- Explicit defaults
- Warning thresholds
- Stop conditions
- TUI settings and help text

### 7.7 Rights and release workflow

Not yet locked:

- Guest-speaker permission records
- Student consent records
- Music and visual-asset licensing
- Trademark handling
- Screenshot redaction
- Source attribution
- Expiration and takedown policy

Required output:

- Evidence model
- Review states
- Hard-stop conditions
- Audit trail requirements

---

## 8. Go CLI and Bubble Tea Architecture

Recommended CLI name is not yet locked. Do not assume `grain-archive` is final.

Suggested command surface:

```text
<cli> setup
<cli> sync
<cli> analyze
<cli> review
<cli> clips list
<cli> clips extract
<cli> status
<cli> doctor
<cli> config show
<cli> config edit
```

### 8.1 Core components

```text
cmd/
internal/config
internal/keychain
internal/grain
internal/archive
internal/manifest
internal/download
internal/transcript
internal/analyze
internal/gate
internal/clips
internal/checksum
internal/tui
```

### 8.2 State model

Each recording should move through independently persisted states:

```text
DISCOVERED
QUEUED
DOWNLOADING
ARCHIVED
ANALYZING
ANALYZED
NEEDS_REVIEW
CLIP_CANDIDATES_READY
COMPLETE
FAILED_RETRYABLE
FAILED_PERMANENT
EXCLUDED
```

A process crash must not require rescanning or redownloading completed work.

### 8.3 Manifest requirements

The manifest must record:

- Grain recording ID
- Source update timestamp
- Local paths
- File sizes
- Checksums
- Download state
- Retry count
- Transcript state
- Analysis state
- Gate version
- Final route
- Candidate segments
- Extracted clips
- Last error
- Last successful update

Use a durable local store appropriate for resumability. SQLite is preferred unless the implementation agent proves a simpler format can safely support concurrent state transitions, migrations, queries, and recovery.

### 8.4 Safety requirements

- Write downloads to temporary or partial paths.
- Promote files atomically after successful validation.
- Never overwrite a valid archive with a partial response.
- Respect HTTP range support where available.
- Retry with bounded exponential backoff and jitter.
- Preserve exact error causes.
- Rate-limit Grain and OpenAI requests independently.
- Redact tokens from logs.
- Do not store plaintext PATs in config files.
- Do not publish, upload, delete remote recordings, or modify Grain data.

---

## 9. Testing Contract

### 9.1 Recording-gate behavioral tests

Required fixtures:

- Dani-led lecture with strong audio and visuals → `DIRECT_USE`
- Strong transcript with poor visuals → `REBUILD`
- Student presentation → `EXCLUDE`
- External webinar → `NEEDS_REVIEW`
- Outdated but fixable technical lesson → `REBUILD`
- Fundamentally obsolete premise → `EXCLUDE`
- Missing audio and visual evidence → no guessed values; `UNKNOWN` gates
- Recording shorter than threshold → deterministic `EXCLUDE`
- Recording exactly equal to threshold → passes duration filter
- Duration filter set to `0s` → disabled
- Ambiguous privacy status → `NEEDS_REVIEW`
- Three non-overlapping candidate segments maximum

### 9.2 Downloader tests

- Resume interrupted download
- Skip valid completed file
- Repair corrupted file
- Handle changed source recording
- Preserve source after analysis failure
- Safe quit during active downloads
- Keychain unavailable
- Environment token override
- API pagination
- Rate limiting
- Partial network failure
- Disk full
- Destination removed
- Invalid duration settings
- Schema migration

### 9.3 TUI tests

- First-run setup flow
- Existing configuration startup
- Pause/resume
- Retry failure
- Safe quit
- Settings validation
- Clip-profile help text order
- Screen-reader-friendly labels where supported
- Narrow terminal layout

### 9.4 Skill tests

Each skill must include pressure tests showing that it:

- Does not invent missing evidence
- Does not reopen locked product decisions
- Does not copy another creator's identity
- Preserves Dani's teaching voice
- Separates production recommendations from publishing actions
- Does not auto-publish
- Does not bypass rights or privacy review

---

## 10. Acceptance Criteria

The first usable release is complete when:

1. All 568 currently accessible Grain recordings can be discovered through pagination.
2. An interrupted archive run resumes without redownloading completed valid files.
3. Every completed recording has the full portable bundle.
4. The duration filter works with `s` and `m` units and defaults to `30s`.
5. OpenAI analysis runs independently after each completed archive.
6. The eight-point gate produces human and strict JSON output.
7. Unknown media evidence remains unknown.
8. High-confidence hard failures may be excluded; ambiguous cases require review.
9. Up to three candidate segments are proposed without overlap.
10. Clip extraction occurs only after explicit user selection.
11. Clip-profile settings use descriptive names and enforce the `10s` to `25m` safeguards.
12. The TUI presents the three profiles in the required order with posting guidance.
13. Tokens never appear in config files or logs.
14. Safe quit leaves the archive resumable.
15. No remote Grain content is modified or deleted.

---

## 11. Agent Handoff Rules

An agent receiving this specification must:

1. Treat Section 2 as settled requirements.
2. Ask questions only when ambiguity materially changes behavior.
3. Research only the unresolved areas in Section 7 unless implementation exposes a contradiction.
4. Preserve the `droxey-` namespace for all new skill names.
5. Keep archival, analysis, production, and publishing as separate bounded systems.
6. Never add automatic publishing without explicit approval.
7. Never weaken student, privacy, authorship, or rights safeguards.
8. Version all machine-readable contracts.
9. Record assumptions and unresolved edges.
10. Return evidence for recommendations, especially for current platform behavior and video-format trends.

### Suggested handoff prompt

```text
Use this specification as the canonical product model. Do not reopen settled decisions in Sections 2–6. Investigate only the unresolved area assigned to you from Section 7. Produce a concrete proposal with evidence, tradeoffs, defaults, schemas/settings where relevant, tests, risks, and exact changes required to integrate your proposal into the canonical system. Preserve the droxey- namespace and all safety boundaries.
```

---

## 12. Recommended Work Order

1. Implement and test `droxey-recording-gate`.
2. Integrate the gate into the existing Teaching System without duplicating rules.
3. Finalize CLI name and Go architecture.
4. Implement archive + resumable sync.
5. Implement analysis queue and strict gate-result persistence.
6. Implement review and candidate-clip extraction.
7. Research and lock the visual identity.
8. Build `droxey-teaching-video-director` and specialist skills.
9. Build production templates and Remotion-compatible assets.
10. Define publishing and analytics feedback loops.

---

## 13. Explicit Non-Goals for v1

- Background daemon
- Windows or Linux support
- Automatic publishing
- Automatic extraction of every candidate clip
- Automated student or guest consent collection
- Full nonlinear video editor
- Generic AI avatar as the primary presentation style
- Replacing Dani's voice or teaching identity
- Deleting or modifying Grain recordings
- Multi-provider semantic analysis

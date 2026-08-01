---
doc_type: spec
version: v1
status: review
authority: proposed
---

# Droxey Recording Gate Design Specification

**Date:** 2026-08-01  
**Canonical skill:** `droxey-recording-gate`

## 1. Purpose

`droxey-recording-gate` determines whether a Grain recording contains reusable teaching material, explains the decision, and proposes reviewable clip boundaries. It is the single policy authority for recording qualification.

The same versioned policy, vocabulary, result schema, and conformance fixtures must govern:

1. the standalone recording-gate skill;
2. the conditional recording-gate step used by the downstream Teaching System skill; and
3. the future Go and Bubble Tea archive application.

This prevents the skill and application from making different decisions about the same recording.

## 2. Goals

- Evaluate every eligible recording against eight explicit gates.
- Produce a concise human report and strict machine-readable JSON.
- Produce a final `DIRECT_USE`, `REBUILD`, or `EXCLUDE` route, or require review before choosing a route.
- Propose no more than three useful, coherent clip candidates.
- Fail closed when privacy, reuse rights, or required evidence is uncertain.
- Make every decision reproducible through versioning and fingerprints.
- Minimize OpenAI calls without reducing safety.
- Provide a language-neutral conformance suite reusable by the skill and Go application.

## 3. Non-goals

The canonical gate does not:

- discover or download Grain recordings;
- edit, trim, transcode, extract, delete, or publish media;
- automatically select proposed clips;
- manage API credentials;
- define the archive application's complete TUI or synchronization behavior;
- support multiple model providers in version 1; or
- replace legal, institutional, or human review when reuse rights or student privacy are uncertain.

`EXCLUDE` is a content-use decision. It never deletes the archived source.

## 4. System boundary and ownership

| Component | Owns | Does not own |
| --- | --- | --- |
| `droxey-recording-gate` | Normative policy, closed-set reason codes, schemas, routing reducer, clip proposals, conformance fixtures | Downloading, extraction, publishing, credential storage |
| Downstream Teaching System skill | Teaching transformation after an eligible gate result | Copies of gate rules |
| Downstream Social Learning skill | Social-learning design after content qualification | Recording qualification |
| Go + Bubble Tea application | Grain archive, resumability, credentials, OpenAI invocation, caching, selection, extraction, TUI | Independent policy interpretations |

The downstream order is:

1. Archive the Grain source.
2. Run `droxey-recording-gate`.
3. Resolve a `NEEDS_REVIEW` decision state when necessary.
4. Route accepted material through the appropriate teaching workflow.
5. Extract only clips explicitly selected by the user.

The Teaching System skill invokes the canonical gate conditionally when its input is an unevaluated recording. It references the canonical policy version rather than duplicating the policy. Social Learning, `write-like-you-talk`, and `essence` remain downstream transformations. Final downstream skill names are confirmed during their separate integration design; this specification commits only to `droxey-recording-gate`.

### 4.1 Existing package assessment

The reviewed Teaching Voice and Social Learning packages are compatible downstream inputs but do not implement the recording gate. Teaching value is strongly covered; student/privacy, originality, coherence, audio/transcript, and visual usefulness are partial; authorship/reuse rights and technical currency are missing. The standalone gate owns those rules. Teaching System integration invokes it; Social Learning remains unchanged downstream.

## 5. Canonical vocabulary

### 5.1 Gate statuses

Every gate returns exactly one status:

- `PASS`: evidence supports use without substantive remediation for this gate.
- `WARN`: useful material remains, but a known and fixable problem requires remediation.
- `FAIL`: evidence establishes that the gate is not satisfied.
- `UNKNOWN`: required evidence is absent or insufficient. The system must not guess.

Each gate also returns `HIGH`, `MEDIUM`, or `LOW` confidence; `SUFFICIENT`, `PARTIAL`, or `INSUFFICIENT` evidence sufficiency; a concise explanation; and evidence references. Confidence and evidence sufficiency are independent. A gate cannot pass when required evidence is partial or missing.

### 5.2 Decision status

- `FINAL`: `decision.route` contains a final content disposition.
- `NEEDS_REVIEW`: evidence or confidence must be resolved before a route can be chosen; `decision.route` is `null`.

`NEEDS_REVIEW` is a completed policy decision, not an operational failure and not a content route.

### 5.3 Recording routes

- `DIRECT_USE`: the recording can be used with only light trimming, captions, normalization, or branding. It does not require re-recording, replacement visuals, or substantive rewriting.
- `REBUILD`: worthwhile teaching content survives, but the presentation, structure, currency, audio, visuals, or privacy treatment requires substantive reconstruction.
- `EXCLUDE`: the recording must not enter the production pipeline.

### 5.4 Candidate clip

A candidate clip is a proposed time range containing one complete teaching idea. A proposal is not an extracted file and is never automatically selected.

## 6. Inputs

### 6.1 Required Grain input

The adapter must normalize the Grain v2 recording and transcript into:

- Grain recording ID;
- title;
- recording timestamp;
- source URL;
- duration in integer milliseconds;
- known participants and speakers;
- transcript segments containing speaker, `start_ms`, `end_ms`, and text; and
- source API version.

A missing or unusable transcript is an operational input error, not a gate decision.

### 6.2 Optional analysis evidence

The input may contain a namespaced `analysis_evidence` object with independently obtained facts or measurements:

- verified presenter and reuse-rights assertions;
- speaker-time distribution;
- audio measurements and delivery findings;
- sampled-frame or screen-activity findings;
- sourced technical-currentness verification for time-sensitive claims; and
- evidence provenance.

Evidence must identify its source and collection time. The model may interpret evidence but may not invent absent measurements. Missing audio or visual evidence produces `UNKNOWN` for the affected gate and ordinarily sets the decision status to `NEEDS_REVIEW`. Time-sensitive technical claims cannot receive a high-confidence currency pass from model memory alone.

Raw video is not required by the canonical gate contract. Collection of audio and frame evidence belongs to the consuming application.

## 7. Canonical configuration

The default YAML is:

```yaml
config_version: 1

recording_selection:
  minimum_recording_duration: 30s

candidate_clips:
  duration_range:
    preset: teaching-clip
  maximum_clips_per_recording: 3
```

An explicit clip range replaces the preset:

```yaml
config_version: 1

recording_selection:
  minimum_recording_duration: 30s

candidate_clips:
  duration_range:
    minimum: 45s
    maximum: 8m
  maximum_clips_per_recording: 3
```

### 7.1 Recording selection

- `recording_selection.minimum_recording_duration` defaults to `30s`.
- `0s` disables duration-based recording exclusion.
- A recording is excluded only when `duration < minimum_recording_duration`.
- A recording exactly equal to the threshold passes preflight.
- Duration exclusion is deterministic and must not call OpenAI.

### 7.2 Candidate clip profiles

Profiles remain in this order in configuration help and the TUI:

| Preset | Range | UI help: appropriate destinations |
| --- | --- | --- |
| `teaching-clip` | 1m–5m | LinkedIn, standard YouTube, Muse & Machine, course/LMS |
| `social-clip` | 30s–2m | YouTube Shorts, Instagram Reels, TikTok, LinkedIn |
| `mini-lesson` | 3m–15m | YouTube, LinkedIn, Muse & Machine, course/LMS, X-Pilot source |

This help is advisory. The gate does not crop, caption, brand, upload, or publish media.

An explicit custom duration range has no inferred platform guidance. Its `recommended_destinations` value is an empty array unless a future consumer-owned editorial setting supplies guidance separately.

### 7.3 Duration syntax and invariants

- Accept whole-second Go-style values using `s`, `m`, or a combination such as `1m30s`.
- Reject unitless, fractional, negative, hour, and millisecond values.
- Explicit ranges require both `minimum` and `maximum`.
- `preset` and explicit `minimum`/`maximum` are mutually exclusive.
- An explicit range is inclusive and must satisfy `minimum < maximum`.
- Candidate clip durations have code-level safeguards of `10s` minimum and `25m` maximum.
- These safeguards are invariants, not editable configuration.
- `candidate_clips.maximum_clips_per_recording` counts proposals, not extracted files. It defaults to `3` and accepts `1`, `2`, or `3` in version 1.
- `0s` is valid only for `recording_selection.minimum_recording_duration`.

### 7.4 Future Go CLI names

The consuming application uses descriptive kebab-case flags corresponding to snake-case YAML fields:

- `--minimum-recording-duration`
- `--clip-duration-preset`
- `--minimum-clip-duration`
- `--maximum-clip-duration`
- `--maximum-clips-per-recording`
- `--clip-extraction-mode`

Version 1 provides no abbreviated aliases. Flags override configuration. A preset flag replaces the entire configured duration range. Explicit duration overrides require both minimum and maximum flags and replace the range atomically. Invalid combinations fail before work begins. Clip extraction mode belongs to the Go application; version 1 extracts selected clips only.

## 8. Deterministic preflight

Preflight runs before any OpenAI request:

1. Validate the configuration version and all configuration invariants.
2. Validate required normalized Grain fields and transcript structure.
3. Confirm transcript timestamps are ordered and fall within recording duration.
4. Apply `minimum_recording_duration`.
5. Compute canonical input and configuration fingerprints.

Invalid configuration or malformed required input returns an operational error and no assessment. When `recording.duration_ms < minimum_recording_duration`, emit `FINAL`/`EXCLUDE` with reason code `RECORDING_BELOW_MINIMUM_DURATION`, set `semantic_evaluation.status` to `SKIPPED`, set `gates` to `null`, emit no candidates, and make no OpenAI request. Equality passes preflight. Skipped gates must not be mislabeled `UNKNOWN`; `UNKNOWN` means an evaluation ran but required evidence was insufficient.

## 9. Eight-gate assessment

| Gate ID | Question | Required behavior |
| --- | --- | --- |
| `authorship_and_reuse_rights` | Did Dani create, lead, or obtain permission to reuse the material? | Prohibited use may be `FAIL`; ambiguous rights or an externally led recording requires review. |
| `student_and_private_content` | Is reuse safe with respect to students, private information, and confidential material? | Student-heavy sessions and established unsafe private content fail. Isolated removable content warns and requires rebuilding. A Dani-led lecture where students mostly listen may proceed when the evidence supports it. |
| `teaching_value` | Does the recording teach a useful concept, method, decision, or demonstration? | No meaningful teaching value fails. |
| `originality` | Does Dani add experience, framing, judgment, delivery, or explanation worth preserving? | Generic treatment may require rebuilding; lack of both originality and surviving value may exclude. Similar public topics do not make Dani's experience-driven treatment non-original. |
| `coherence_and_segmentability` | Does the recording or a segment contain a complete, understandable idea? | No complete extractable idea fails. |
| `technical_currency` | Are the claims, APIs, tools, and recommendations still accurate enough to teach? | Current material may pass; fixable outdated details require rebuilding; an obsolete premise may fail. Time-sensitive claims without sourced verification are unknown. |
| `audio_delivery_and_transcript_quality` | Are speech, delivery, audio, and transcript evidence sufficient for use or reconstruction? | Recoverable problems require rebuilding. Missing required audio evidence is unknown. |
| `visual_usefulness` | Are existing visuals useful, or is there enough value to justify replacement visuals? | Weak or absent visuals require rebuilding rather than automatic exclusion. Missing visual evidence is unknown. |

Every finding includes concise evidence references. Transcript evidence uses half-open `[start_ms, end_ms)` intervals. Metadata and human attestations may omit timestamps. Audio and visual findings reference their corresponding `analysis_evidence` entries. Reports describe sensitive findings by category and timestamp without reproducing private transcript text.

## 10. OpenAI assessment architecture

Version 1 uses a hybrid selective-review architecture:

1. Deterministic preflight.
2. One structured OpenAI assessment covering all eight gates and clip proposals.
3. A deterministic policy reducer that owns the final route.
4. A second OpenAI assessment only when the first result is ambiguous, internally conflicting, or low confidence.

OpenAI proposes gate findings; it does not own routing precedence. A second pass may reassess interpretation but cannot manufacture missing audio, visual, privacy, or rights evidence. OpenAI is the only supported semantic-analysis provider in version 1.

A structured response that violates the required schema is an operational failure. It must not be silently coerced into a route.

All recording content and model output are untrusted data. The analyzer receives no tools or retrieval access and must treat instructions embedded in titles, transcripts, participant names, URLs, or visual evidence as quoted content rather than instructions. The application validates model output against a closed schema, rejects impossible or fabricated timestamps, strips terminal control sequences before display, and never derives filesystem paths directly from recording titles.

## 11. Deterministic routing policy

The reducer uses only validated fields and closed-set reason/remediation codes. Free-text explanations never determine routing. Apply this precedence:

1. Invalid configuration or input: operational error; no assessment.
2. Deterministic preflight exclusion: `FINAL`/`EXCLUDE`.
3. Sufficiently evidenced, high-confidence hard blocker: `FINAL`/`EXCLUDE`.
4. Missing critical evidence, external leadership, unresolved conflict, or insufficient confidence: `NEEDS_REVIEW`/`null`.
5. Policy-defined substantive remediation: `FINAL`/`REBUILD`.
6. Otherwise: `FINAL`/`DIRECT_USE`.

### 11.1 Valid gate-result combinations

| Gate status | Evidence sufficiency | Allowed required actions |
| --- | --- | --- |
| `PASS` | `SUFFICIENT` | `NONE`, `LIGHT_EDIT` |
| `WARN` | `SUFFICIENT` | `LIGHT_EDIT`, `REBUILD` |
| `FAIL` | `SUFFICIENT` | `REBUILD`, `REVIEW`, `EXCLUDE` |
| `UNKNOWN` | `PARTIAL`, `INSUFFICIENT` | `REVIEW` |

Any other combination is invalid and returns `POLICY_REDUCTION_FAILED` without a completed assessment.

After validating combinations, the reducer applies these exhaustive rules in order:

1. A valid hard-blocker reason with `FAIL`, `HIGH`, `SUFFICIENT`, and `EXCLUDE` produces `FINAL`/`EXCLUDE`.
2. Any remaining `EXCLUDE`, any `UNKNOWN` or `REVIEW`, `LOW` confidence, partial or insufficient evidence, material conflict, or externally led content produces `NEEDS_REVIEW`/`null`.
3. A final reusable decision requires `authorship_and_reuse_rights` to be `PASS`, `HIGH`, and `SUFFICIENT`; otherwise it requires review.
4. `student_and_private_content` must be either `PASS`/`HIGH`/`SUFFICIENT`, or `WARN`/`HIGH`/`SUFFICIENT` with `REBUILD` and `PRIVATE_CONTENT_REMOVABLE`. Any other non-excluded privacy result requires review.
5. Any remaining `REBUILD` action produces `FINAL`/`REBUILD`.
6. Any remaining `LIGHT_EDIT` action, or all `PASS`/`NONE` results, produces `FINAL`/`DIRECT_USE`.

`MEDIUM` confidence is permitted only for non-rights and non-privacy gates with sufficient evidence. Final decision confidence is the lowest confidence among gate results that contributed to the decision.

### 11.2 Closed-set policy reason codes

| Outcome class | Applicable gate or reducer | Allowed reason codes |
| --- | --- | --- |
| Preflight exclude | Preflight | `RECORDING_BELOW_MINIMUM_DURATION` |
| Hard exclude | `authorship_and_reuse_rights` | `REUSE_PROHIBITED` |
| Hard exclude | `student_and_private_content` | `STUDENT_HEAVY`, `PRIVATE_CONTENT_UNSAFE` |
| Hard exclude | `teaching_value` | `NO_TEACHING_VALUE` |
| Hard exclude | `originality` | `NO_ORIGINAL_VALUE` |
| Hard exclude | `coherence_and_segmentability` | `NO_COHERENT_IDEA` |
| Hard exclude | `technical_currency` | `OBSOLETE_PREMISE` |
| Needs review | `authorship_and_reuse_rights` | `REUSE_RIGHTS_UNRESOLVED`, `EXTERNALLY_LED` |
| Needs review | `student_and_private_content` | `PRIVACY_UNRESOLVED` |
| Needs review | `audio_delivery_and_transcript_quality` | `AUDIO_EVIDENCE_MISSING` |
| Needs review | `visual_usefulness` | `VISUAL_EVIDENCE_MISSING` |
| Needs review | `technical_currency` | `TECHNICAL_CURRENCY_UNVERIFIED` |
| Needs review | Reducer | `FINDINGS_CONFLICT`, `CONFIDENCE_INSUFFICIENT` |
| Rebuild | `student_and_private_content` | `PRIVATE_CONTENT_REMOVABLE` |
| Rebuild | `originality` | `ORIGINALITY_REBUILD_REQUIRED` |
| Rebuild | `coherence_and_segmentability` | `STRUCTURE_REBUILD_REQUIRED` |
| Rebuild | `technical_currency` | `OUTDATED_DETAILS_FIXABLE` |
| Rebuild | `audio_delivery_and_transcript_quality` | `AUDIO_OR_TRANSCRIPT_REBUILD_REQUIRED` |
| Rebuild | `visual_usefulness` | `VISUAL_REBUILD_REQUIRED` |
| Direct-use edit | Any evaluated gate | `LIGHT_EDIT_ONLY` |

A non-`NONE` gate action requires at least one allowed gate reason code; `NONE` requires an empty gate reason-code list. Preflight and reducer reason codes appear only on the decision. A reason code used by the wrong gate or with the wrong outcome/action is invalid and returns `POLICY_REDUCTION_FAILED`. Summaries may explain details but cannot introduce routing semantics outside this catalog. Adding, removing, or changing a reason code requires a policy-version change.

### 11.3 Exclude

Automatically choose `FINAL`/`EXCLUDE` only for:

- deterministic recording-duration exclusion; or
- a high-confidence hard failure with sufficient evidence.

Hard failures include prohibited reuse, unsafe student/private content, no teaching value, no coherent idea, an obsolete premise, or no remaining value after originality is considered. A student-heavy session or recording containing private education, health, accommodation, disciplinary, financial, or personally identifying information excludes only when sufficient evidence establishes the failure. Ambiguous identity, consent, classroom context, privacy, or rights evidence requires review. Externally led or ambiguous-rights recordings are not automatically excluded.

### 11.4 Needs review

Choose `NEEDS_REVIEW` with a null route when no exclusion is established and any of the following applies:

- rights, presenter identity, or privacy is unresolved;
- required audio or visual evidence is missing;
- gate findings materially conflict;
- a potentially hard failure has insufficient confidence; or
- the second pass cannot resolve an ambiguity.

Model-reported confidence alone cannot upgrade `UNKNOWN`. The reducer may downgrade confidence based on evidence sufficiency but may not upgrade missing evidence. If a second pass fails operationally, the manifest becomes `PAUSED` for a retryable failure or `FAILED` for a permanent failure, and no completed assessment artifacts are created. The validated first pass may remain in a private checkpoint for retry but is not a gate decision.

### 11.5 Rebuild

Choose `FINAL`/`REBUILD` when useful content survives known, fixable problems such as:

- removable private references;
- generic framing that can gain value from Dani's experience;
- outdated but correctable technical details;
- weak structure;
- recoverable audio, delivery, or transcript problems; or
- weak or absent visuals.

### 11.6 Direct use

Choose `FINAL`/`DIRECT_USE` when every gate passes or has a validated `WARN`/`LIGHT_EDIT` result and remaining work is limited to light trimming, captions, normalization, or branding.

## 12. Candidate clip policy

- Propose no more than `candidate_clips.maximum_clips_per_recording` candidates.
- Each candidate must contain one complete idea and fit the effective duration range.
- Candidate intervals are half-open `[start_ms, end_ms)`. Adjacent intervals are allowed; overlap is prohibited.
- Candidate timestamps must be within the recording and satisfy `start_ms < end_ms`.
- Never propose candidates for a final `EXCLUDE` decision.
- A `NEEDS_REVIEW` assessment may contain proposals only when privacy and reuse-rights gates both pass with high confidence and sufficient evidence.
- Recheck privacy, rights, technical currency, and production requirements at candidate scope.
- Each proposal has its own `FINAL`/`DIRECT_USE`, `FINAL`/`REBUILD`, or `NEEDS_REVIEW`/`null` decision. Omit excluded segments rather than proposing them.
- Extraction requires explicit user selection and occurs as a separate derivative step. The final interval, including padding or handles, must pass privacy and rights checks before extraction.
- A proposal awaiting review is not extractable. A `REBUILD` proposal may be extracted only as source material for reconstruction and must not be labeled publishable.

Recommended destinations are copied from the active duration profile for UI guidance. They are not publishing instructions.

## 13. Result contract

Each completed assessment produces two sibling artifacts inside the recording bundle:

- `recording-assessment.json`: strict machine-readable result;
- `recording-assessment.md`: concise human report.

### 13.1 JSON sections

| Field | Required contents |
| --- | --- |
| `schema_version` | Assessment schema version |
| `policy_version` | Canonical recording-gate policy version |
| `assessment_id` | Unique assessment identifier |
| `created_at` | UTC RFC 3339 timestamp |
| `recording` | Grain ID, title, date, source URL, duration |
| `reproducibility` | Input, configuration, policy, and model fingerprints plus effective configuration |
| `preflight` | Completed checks and deterministic decisions |
| `semantic_evaluation` | `COMPLETED` or `SKIPPED`, with a closed-set reason when skipped |
| `gates` | Exactly eight gate results after semantic evaluation; `null` after deterministic preflight exclusion |
| `decision` | Status, nullable route, confidence, reason codes, summary, triggering gates, review reasons |
| `candidate_clips` | Zero to three proposals |
| `analysis_provenance` | Provider, model, response identifiers, timestamps, usage, and second-pass status |

Wall-clock timestamps—including `created_at`, recording time, evidence collection time, and provider request times—use UTC RFC 3339 strings. Media offsets and durations use integer milliseconds. Configuration retains human-readable whole-second duration strings. Gate evidence contains short findings and references, not private chain-of-thought or hidden model reasoning.

For deterministic preflight exclusion, `analysis_provenance` records a pass count of zero and null provider, model, response, usage, and cost fields.

### 13.2 Gate result

Each entry in `gates` contains:

- `gate_id`;
- `status`;
- `confidence`;
- `evidence_sufficiency`;
- closed-set `reason_codes`;
- a closed-set `required_action` of `NONE`, `LIGHT_EDIT`, `REBUILD`, `REVIEW`, or `EXCLUDE`;
- `summary`;
- zero or more typed evidence references; and
- an optional `review_reason`.

The schema requires every gate ID exactly once.

### 13.3 Decision

`decision` contains:

- `status`, either `FINAL` or `NEEDS_REVIEW`;
- `route`, either `DIRECT_USE`, `REBUILD`, `EXCLUDE`, or `null`;
- `confidence`;
- closed-set `reason_codes`;
- a concise human-readable `summary`;
- `triggering_gate_ids`; and
- `review_reasons`.

The reducer, not the OpenAI response, creates this object.

### 13.4 Candidate clip

Each candidate contains:

- stable `candidate_id`;
- one-based `ordinal`;
- `start_ms`, `end_ms`, and derived `duration_ms`;
- `duration_range_source`, either a preset name or `custom`;
- `working_title`;
- `complete_idea_summary`;
- `selection_rationale`;
- ordered `recommended_destinations`; and
- `required_edits`; and
- an independent `decision` using the same status/nullable-route structure.

Candidate selection state belongs to the Go application's resumable manifest and is not written back into the immutable assessment result. Generate `assessment_id` once and preserve it across resume. Derive candidate IDs from the assessment ID and normalized boundaries; reassessment creates a new assessment and new candidate IDs.

### 13.5 Human report

`recording-assessment.md` presents, in order:

1. decision status, nullable final route, and confidence;
2. concise rationale;
3. the eight-gate status table when semantic evaluation ran, or the preflight skip reason otherwise;
4. required review or remediation;
5. proposed clip table; and
6. analysis provenance without secrets or transcript dumps.

## 14. Operational error contract

Operational failures never masquerade as `EXCLUDE` or `NEEDS_REVIEW`. The gate returns a typed error to the consuming workflow and does not create a completed assessment result.

Canonical error classes include:

- `INVALID_CONFIGURATION`
- `INVALID_INPUT`
- `MISSING_TRANSCRIPT`
- `OPENAI_AUTHENTICATION_FAILED`
- `OPENAI_RATE_LIMITED`
- `OPENAI_TIMEOUT`
- `OPENAI_SERVICE_UNAVAILABLE`
- `OPENAI_SCHEMA_VIOLATION`
- `OPENAI_REQUEST_REFUSED`
- `CLOUD_PROCESSING_NOT_AUTHORIZED`
- `SENSITIVE_PAYLOAD_REQUIRES_REVIEW`
- `POLICY_REDUCTION_FAILED`

Allow at most four OpenAI requests for one assessment, including transport retries and the optional semantic second pass. Retry connection failures, timeouts, rate limits, and temporary service failures using full-jitter exponential backoff with a one-second base and 30-second cap. Honor server retry guidance up to 60 seconds. Do not retry invalid input or configuration, authentication or authorization failures, request refusals, schema-invalid model output, or reducer failures.

Grain acquisition errors are owned by the Go application because they occur before normalized gate input exists.

The Go manifest, not the immutable assessment result, owns lifecycle state: `PENDING`, `IN_PROGRESS`, `PAUSED`, `COMPLETE`, `BLOCKED`, or `FAILED`. Only `COMPLETE` creates assessment artifacts. Cancellation, retry exhaustion, and provider or schema failures never become gate decisions.

## 15. Privacy, credentials, and diagnostics

- Secrets never appear in YAML, result artifacts, or logs.
- The macOS application stores Grain and OpenAI credentials in Keychain.
- `GRAIN_API_TOKEN` and `OPENAI_API_KEY` are explicit environment overrides.
- Cloud-processing authorization is independent of authorship, consent to recording, and reuse rights.
- Before any OpenAI request containing recording content, authorization must be `GRANTED`. `DENIED` or `UNKNOWN` makes no cloud request, sets the manifest lifecycle to `BLOCKED`, and returns `CLOUD_PROCESSING_NOT_AUTHORIZED` without creating assessment artifacts.
- Before the first cloud analysis, the TUI explains exactly what recording data leaves the device and requires confirmation.
- By default, send only a pseudonymized transcript, essential metadata, and locally derived evidence. Pseudonymization preserves verified roles such as Dani or student while replacing personal names.
- Version 1 never sends original audio, video, or frames to OpenAI. Supporting raw-media transmission later requires a separate privacy design and policy version.
- A local secret scan blocks transmission when the selected payload appears to contain credentials, API keys, or other secrets. It makes zero OpenAI requests, sets the manifest lifecycle to `BLOCKED`, returns `SENSITIVE_PAYLOAD_REQUIRES_REVIEW`, and creates no assessment artifacts.
- Default logs include IDs, stages, durations, usage, and error codes—not transcript text.
- Raw prompts and responses are excluded from normal artifacts.
- Diagnostic capture requires an explicit setting, a clear privacy warning, and restrictive local file permissions.
- Missing privacy or reuse-rights evidence fails closed to `NEEDS_REVIEW`.
- A Dani-led lecture may proceed only when reuse rights pass. Every proposed final interval must omit student speech, names, faces, chat, submissions, grades, notifications, and private screen content unless explicit rights and privacy evidence permits that exact content.
- No gate outcome deletes or modifies the archived source.

This design is a technical safeguard, not a claim of legal or institutional compliance.

## 16. Caching, cost, and resumability

Cache identity is SHA-256 over canonicalized normalized input and evidence, effective configuration, policy version, assessment schema version, analyzer and prompt versions, requested model identifier, and non-secret opaque Grain/OpenAI account identifiers. Record requested and returned model identifiers, provider system fingerprint when supplied, response IDs, pass count, token usage, and nullable estimated cost.

Cache only schema-valid completed assessments. Validate entries on read, write atomically with owner-only permissions, lock concurrent writers, and invalidate resumed stages when any fingerprint changes. An unchanged recording reuses its completed assessment unless the user explicitly requests reassessment.

The normal cost is one OpenAI assessment. The second assessment runs only under the conditions in Section 10. Record token usage and estimated cost when the API response and configured pricing data make an estimate possible; label estimates as estimates.

The Go application checkpoints archive and analysis stages separately. Closing the TUI requests a safe stop, completes or cancels the active bounded operation, persists the checkpoint, and exits. Version 1 does not run a daemon. Restarting resumes from the last valid checkpoint.

## 17. Go archive integration constraints

The later Go and Bubble Tea design must preserve these already approved constraints:

- macOS-first turnkey application;
- guided first-run setup and focused dashboard;
- Grain personal access token in Keychain with environment override;
- portable recording bundles containing original media, Markdown transcript, SRT, raw transcript JSON, and metadata JSON;
- analysis begins as soon as an individual recording bundle is complete;
- archive synchronization is incremental and resumable;
- closing the TUI safely checkpoints work;
- proposed clips are extracted only after explicit selection; and
- the gate contract and conformance fixtures are consumed without reinterpretation.

The complete downloader, TUI, manifest, and extraction design remains a separate design cycle.

## 18. Verification strategy

While frontmatter is `status: review` and `authority: proposed`, this document is the planning authority but not yet executable implementation authority. Final approval changes it to `status: approved` and `authority: current`. Implementation must then add `droxey-recording-gate/schemas/recording-assessment-v1.schema.json`. The approved policy specification owns semantics and that JSON Schema owns structure; language-neutral conformance fixtures are executable examples and do not independently define or override either authority. Both the skill and Go implementation must pass the same fixtures before release.

### 18.1 Fixture coverage

Fixtures cover:

- duration parsing, defaults, exact-threshold behavior, bounds, and invalid combinations;
- all gate statuses and routing precedence;
- missing evidence and fail-closed review;
- student-heavy, Dani-led, private-content, and reuse-rights cases;
- current, fixably outdated, and obsolete technical content;
- direct-use versus rebuild boundaries;
- malformed and incomplete OpenAI responses;
- candidate count, range, timestamps, overlap, and route eligibility;
- private or identifying data in titles, participant metadata, chat, notifications, frames, or screens despite a clean transcript;
- minors, grades, accommodations, health information, student IDs, credentials, and API keys;
- missing diarization, incorrect diarization, and truncated or misaligned transcripts;
- Dani-led lectures containing brief student questions;
- padding or handles that capture a student name, voice, face, or private screen;
- prompt injection in transcripts, malicious URLs, terminal escapes, and path traversal strings;
- invalid enums, unexpected fields, and impossible timestamps;
- denied or unknown cloud authorization proving zero OpenAI calls;
- retry exhaustion, ambiguous timeouts, cancellation at every stage, corrupt or partial caches, changed inputs, concurrent runs, and cross-account cache isolation;
- canary scans proving logs, reports, filenames, and cache entries do not contain secret or private fixture values;
- cross-implementation comparison of policy outcomes; and
- schema versioning and enum stability.

Fixtures use synthetic or anonymized material. Real student recordings and identifiable student transcripts must not be committed.

### 18.2 Test layers

- Table-driven reducer and validation fixtures run deterministically in CI.
- OpenAI responses are mocked for ordinary automated tests.
- A manual live-model evaluation detects prompt and model behavior changes.
- Skill development follows red-green-refactor: capture baseline failures without the skill, apply the skill, rerun the same scenarios, and close observed loopholes.
- Adversarial scenarios test pressure to guess missing evidence, overlook privacy, exceed clip limits, or reinterpret `EXCLUDE` as deletion.
- The critical safety subset reruns whenever the model, prompt, schema, or policy changes.

### 18.3 Release gates

- 100% of critical privacy, rights, duration, and deletion-safety cases pass.
- 100% assessment-schema validity and clip-boundary compliance.
- At least 90% exact decision-status and route agreement on a Dani-labeled set covering every route and gate, reported separately for each final route and `NEEDS_REVIEW`.
- At least 80% of proposed clips are rated usable or usable with only a small boundary adjustment.
- Any critical false-safe result blocks release.

Decision agreement means both status and nullable route match Dani's label; matching `REBUILD` when the label is `DIRECT_USE` does not qualify. A usable clip contains the intended complete idea and needs no boundary change; a small adjustment changes either boundary by no more than five seconds without adding unsafe content. A rejected idea, major reconstruction of boundaries, or privacy/rights problem does not qualify.

A critical false-safe is any reusable or extractable result when privacy or rights should be `FAIL` or `UNKNOWN`, any cloud transmission without granted authorization, or any source mutation or deletion. One critical false-safe blocks release even when aggregate targets pass.

Live-model scores are recorded with the model identifier, policy version, prompt version, fixture-set version, and evaluation date.

## 19. Versioning and change control

- Version 1 starts with `config_version: 1`, `schema_version: "1.0.0"`, and `policy_version: "1.0.0"`.
- `config_version` versions accepted configuration shape.
- `schema_version` versions result shape and semantics.
- `policy_version` versions gate definitions, routing, and clip policy.
- Conformance fixtures declare the policy and schema versions they test.
- A breaking field or semantic change requires a new schema version.
- A changed routing outcome for the same evidence requires a new policy version.
- Implementations reject unsupported major versions rather than guessing.
- The policy specification owns semantics and the JSON Schema owns structure. A conflict between them blocks release until both artifacts are reconciled under an appropriate version change.

## 20. Deliberately deferred choices

These choices belong to later implementation planning and do not alter the canonical behavior:

- exact OpenAI model and model settings;
- audio measurement and frame-sampling implementation;
- physical package layout for shared conformance fixtures;
- TUI screen composition and key bindings;
- downloader concurrency and bandwidth controls;
- media container and codec choices for extracted derivatives; and
- publishing integrations.

All eventual renamed first-party skills use the `droxey-` prefix. The exact Teaching System suffix remains part of its separate integration design.

Any later choice that changes a gate, route, invariant, privacy boundary, or result field must return to design review and version the affected contract.

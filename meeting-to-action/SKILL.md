---
name: meeting-to-action
description: Use when converting meeting notes or transcripts into summaries, decisions, and action items.
  and action items with owners and due dates. Use when a user asks to turn a meeting
  recording, transcript, or notes into a follow-up plan.
created_at: '2026-05-15T06:39:52.080801+00:00'
updated_at: '2026-05-15T06:39:52.080801+00:00'
maturity: 0
---

# Meeting to Action

## Goal
Transform meeting content into an actionable follow-up package with clear ownership and deadlines.

## Best fit
- Use when the user provides a transcript or detailed notes.
- Use when the user needs action items, decisions, and next steps.
- Use when a concise recap email or message is required.

## Not fit
- Avoid when the user wants tasks or calendar invites created automatically.
- Avoid when the transcript is missing and cannot be summarized reliably.
- Avoid when sensitive content should not be shared.

## Quick orientation
- Identify decisions, action items, owners, due dates, and unresolved questions.
- Confirm ambiguous ownership or dates rather than presenting inferences as facts.
- Produce drafts only; preserve confidentiality and do not access integrations.

## Required inputs
- Transcript or notes.
- Participant list and roles (if available).
- Preferred due date format and timezone.
- Audience for the recap (internal or external).

## Expected output
- Short summary and key decisions.
- Action items with owners, due dates, and status.
- Open questions or risks.
- Draft follow-up message or email.

## Operational notes
- Mark any inferred owners or due dates as tentative.
- Use clear, consistent action verbs.
- Deliver drafts only; do not send or update systems.

## Security notes
- Treat meeting content as confidential.
- Avoid sharing outputs outside the user context.

## Safe mode
- Summarize and draft action items only.
- Do not create tasks, invites, or messages automatically.

## Sensitive ops
- Creating tasks, calendar events, or sending messages is out of scope.

## Maturity

Level 0 - Intent. Substantiated by the written contract only; no runnable asset or tests yet.

## Purpose

Turn meeting material into a summary, decisions, and tracked actions.

## Inputs

Meeting notes or a transcript.

## Outputs

Summary, decisions, and owner-tagged action items.

## Example

From a transcript, extract decisions and produce action items each with an owner and due date.

## Success criteria

Every decision and action is captured with an owner so nothing actionable is lost.
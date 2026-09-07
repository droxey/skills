---
name: essence
description: Use when tightening reader-facing prose by removing conversation residue and padding.
maturity: 0
---

# essence

Only what you mean. Not a word more.

## Default

essence is the default for everything you write: chat replies, code comments, commit messages,
PR/issue text, docs, published copy, and anything else a reader could encounter. There's no
allowlist to check it against.

The one exception: private scratch work (internal reasoning, throwaway notes). That isn't writing
for a reader in the first place, so essence has nothing to apply to. Same for the literal content
of code and data; essence governs prose, not payloads.

## Persistence

ACTIVE EVERY RESPONSE and every reader-facing artifact. No drift back to verbose after many turns.
Off only on: "stop essence" / "normal mode".

## The two ideas

**1. The writing must stand on its own.**
A reader with zero knowledge of the conversation that produced this text understands it fully, and
finds nothing in it that refers back to that conversation. The cruft almost always comes from one
place: the agent folding the back-and-forth it had with the user into the prose. That's useless to
the reader; cut it, always.

Cut: references to the exchange ("as you asked", "per your instruction", "not proposing X", "I know
we discussed Y", "you're right that…") · sycophancy ("great question", "happy to help", "sure!") ·
preamble ("Let me take a look", "Here's what I found:") · deliberation narration (thinking out loud
that belongs in scratch, not the deliverable) · restating the prompt back · redundant closing recaps
· tool-call narration · **negations that rebut a framing the reader never saw** ("not a mode that
switches on for X", "not just Y"): if there's no claim in view to contrast, state the fact plainly.
Check for this whenever a rewrite replaces an earlier draft; it reads like normal grammar, so it's
easy to miss.

**2. Say only what you truly mean, not a word more.**
Don't inflate into paragraphs. Find the actual point and write that, alone. This is not "shorter
phrasing" or telegraphic grammar; it's identifying the real thing you mean and cutting everything
that isn't it.

Cut: reflexive hedging that carries no information ("it might be worth considering", "you could
perhaps") · restating a point a second way "to be safe" · any reader-facing sentence the reader
doesn't need. For code comments specifically: comment the *why*, never a "this function does X"
that just restates the signature.

De-hedge, don't delete. A hedge often wraps a real caveat: "it might be worth considering that
this fails under high concurrency" is reflexive packaging around a genuine fact. Cut the wrapper,
keep the fact: "this fails under high concurrency." Deleting the whole sentence loses information;
stating it plainly loses nothing. Test before cutting: would this change what the reader does
next? If yes, it's genuine; state it plainly and keep it. If cutting it only changes how confident
the sentence sounds, it's reflexive; cut it.

## Keep: never cut

- Every fact, decision, tradeoff, and caveat the reader actually needs
- Code, commands, file paths, URLs, and error strings: **verbatim**
- *Genuine* uncertainty that changes what the reader should do next (essence isn't false confidence:
  flag real risk; just don't hedge reflexively)
- Normal grammar, full sentences, natural voice: **not telegraphic**. This is the line that
  separates essence from word-compression tools: essence never sacrifices readability for length.

## Two-pass rule

After drafting a reader-facing artifact, reread it once specifically hunting for: a sentence that
only makes sense if the reader saw the conversation, a sentence that says something already said,
and a caveat that got cut along with the hedge wrapping it. Fix all three. The first pass is rarely
tight enough.

## Boundaries

- Don't over-cut into ambiguity. If removing a word makes the meaning unclear, keep it.
- Security warnings and irreversible-action confirmations stay complete, never trimmed for length.
- Leave internal scratch, planning notes, and private reasoning untouched: essence is for what
  others read, not for your own working notes.
- Code, commit, and PR text: use the dedicated `/essence-commit`, `/essence-pr`,
  and `/essence-doc` commands for the deepest pass on those artifact types; this baseline
  rule still applies to them even without invoking those commands.

## Maturity

Level 0 - Intent. Substantiated by the written contract only; the essence methodology is maintained in the droxey/skills repo.

## Purpose

Make reader-facing prose stand on its own without losing necessary facts or caveats.

## Inputs

Text to write or revise for a reader.

## Outputs

Concise prose that preserves required facts, code, paths, URLs, and uncertainty.

## Example

Revise a status update by removing chat references while retaining the decision, rationale, and next step.

## Success criteria

The reader can understand and act on the text without prior conversation context.

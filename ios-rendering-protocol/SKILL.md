---
name: ios-rendering-protocol
description: "iOS text rendering protocol for Nebula chat: use MarkDownRenderer for
  all body text, DataTable for tables, Callout for banners, Steps for sequences. READ
  before composing any reply on iOS."
maturity: 0
---

## When to use

Every reply composed from an iOS device. This protocol ensures all text is selectable DOM and no components overflow or overlap.

## Component compliance matrix

Tested on iOS Safari, confirmed results per component:

### Selectable (safe to use)

| Component | Notes |
|---|---|
| MarkDownRenderer | All body text + fenced code blocks (monospaced, selectable) |
| DataTable | No overflow, handles column alignment |
| Callout | No overlap |
| Steps | Each line individually selectable (cross-step is a DOM limitation) |
| Card + CardHeader | Selectable |
| StatCard | Selectable |
| TagBlock | Selectable |

### Avoid (broken on iOS)

| Component | Issue |
|---|---|
| TextContent | Overlapping text near bottom of viewport |
| CodeBlock | Text is NOT selectable |
| Plain text outside openui | Text is NOT selectable |
| Buttons | Overlaps preceding text on iOS -- same root cause as FollowUpBlock |
| FollowUpBlock | Overlaps preceding text on iOS -- same root cause as Buttons |

## Rendering rules

1.  **MarkDownRenderer** for all body text and code blocks (fenced triple-backticks inside for monospaced selectable code).
2.  **DataTable** for tabular data -- never markdown tables inside MarkDownRenderer (they overflow the container on iOS).
3.  **Callout** for info/success/warning/error banners.
4.  **Steps** for ordered sequences; each StepsItem must be a pre-defined named variable, not inlined.
5.  **Card** for elevated containers (sparingly).
6.  **Never use TextContent** -- causes overlapping-layout bug near bottom of screen.
7.  **FollowUpBlock and Buttons overlap** the text above them on iOS. Workaround: insert an explicit spacer MarkDownRenderer before the button row:
    `spacer = MarkDownRenderer("&nbsp;")` then `root = Stack([body, spacer, buttons])`
8.  **Never use CodeBlock** -- use a fenced code block inside MarkDownRenderer instead.
9.  **Never use plain text outside the openui block.**
10. **Every valid URI** must be a clickable markdown link so mobile users can tap to open.

## Template

```openui
root = Stack([content])
content = MarkDownRenderer("Your markdown body here.")
```

For replies with both prose and a table:

```openui
root = Stack([prose, tbl])
prose = MarkDownRenderer("Analysis text above the table.")
tbl = DataTable(
  [{"key": "col1", "label": "Column 1"}, {"key": "col2", "label": "Column 2"}],
  [{"col1": "val1", "col2": "val2"}],
  "optional caption",
  10
)
```

For replies ending with FollowUpBlock (iOS workaround):

```openui
root = Stack([body, spacer, followUp])
body = MarkDownRenderer("Your analysis text here.")
spacer = MarkDownRenderer("&nbsp;")
followUp = FollowUpBlock([FollowUpItem("Show the steps"), FollowUpItem("Explain step 1")])
```

## Pitfalls

- TextContent causes overlapping text near the bottom on iOS -- never use it.
- CodeBlock renders text that is NOT selectable -- use a fenced code block inside MarkDownRenderer instead.
- Markdown tables inside MarkDownRenderer overflow the container on iOS -- always use DataTable instead.
- StepsItem and array children must be pre-defined named variables, not inline expressions.
- FollowUpBlock and Buttons overlap the preceding text element on iOS (pill-shaped buttons bleed into body text). Insert an explicit spacer MarkDownRenderer with a single non-breaking space between the body text and the button row to force gap.
- Untested components (Accordion, Carousel, ImageGallery, Modal, MermaidBlock, DiffView, KanbanBoard, Timeline, Tabs, SectionBlock, ListBlock, TreeView, ActivityFeed, HeatMap, AgentCard, SearchResult, AppCard, AppIcon, Icon, TweetCard, UserCard, Form) have unknown iOS behavior -- test before using for user-facing replies.

## Maturity

Level 0 - Intent. Substantiated by the written contract only; no runnable asset or tests yet.

## Purpose

Apply the iOS text-rendering protocol in Nebula chat output.

## Inputs

Content to render plus the intended component shape.

## Outputs

Rendering decisions and content shaped for the iOS surface.

## Example

Choose MarkDownRenderer over raw markdown for a chat block so iOS renders it correctly.

## Success criteria

Every renderable block uses the protocol-appropriate component for iOS.


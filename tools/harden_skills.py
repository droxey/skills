#!/usr/bin/env python3
"""Batch-harden first-party skills to the incremental maturity methodology.

Deterministic; standard library only. Adds a computed `maturity` field to each
SKILL.md's frontmatter and ensures the required body sections (Purpose, Inputs,
Outputs, Example, Success criteria, Maturity) exist using curated content drawn
from each skill's own description. Runs in place over the live install dirs.
"""
import argparse
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent

# name -> dict(desc, purpose, inputs, outputs, example, success). desc is a
# "Use when ..." single-line replacement for the frontmatter description.
CURATED = {
    "ah-devops-engineer": dict(
        desc="Use when extending or maintaining modern CI/CD, infrastructure-as-code, and cloud automation workflows.",
        purpose="Act as a senior DevOps engineer for infrastructure, CI/CD, and automation work.",
        inputs="Infrastructure, pipelines, or deployment config plus the operator's objective.",
        outputs="Hardened configuration, runbooks, and fixes with an explanation of tradeoffs.",
        example="Given a broken deploy pipeline, diagnose the failing stage and patch the workflow with a rollback path.",
        success="The pipeline or infra change is applied, verified, and documented; nothing is left in a broken state.",
    ),
    "chrome-mcp-web-fallback": dict(
        desc="Use when a web retrieval task fails from blocking or bot protection and needs a browser-driven retry.",
        purpose="Recover failed web retrieval by retrying once through chrome-mcp.",
        inputs="The failing URL, the retrieval error, and the original extraction goal.",
        outputs="The recovered page content or a clear 'still blocked' result.",
        example="A curl fetch returns a 403; retry the same page through chrome-mcp and return the rendered content.",
        success="The page is retrieved via the browser, or the failure is reported without further silent retries.",
    ),
    "code-review": dict(
        desc="Use when reviewing code for security, performance, maintainability, and correctness issues.",
        purpose="Produce a systematic code review across security, performance, and maintainability.",
        inputs="A diff, patch, or repository plus the review's risk context.",
        outputs="Prioritized findings with file-level references and concrete fix guidance.",
        example="Review a PR's diff and order findings by severity with a specific fix for each.",
        success="Every finding is actionable, referenced to code, and free of speculative claims.",
    ),
    "code": dict(
        desc="Use when writing or refactoring non-trivial code with quality gates and regression resistance.",
        purpose="Drive code changes through discuss, spec, test-first, review, and mutation-testing stages.",
        inputs="A problem statement, the existing code, and acceptance criteria.",
        outputs="Spec, tests, implementation, and a review record that passes the gates.",
        example="Implement a feature by first capturing a short spec, writing failing tests, then the code, then a second-pass review.",
        success="Tests pass, the review gates are met, and the change resists mutation testing.",
    ),
    "codespace-operator-v2": dict(
        desc="Use when selecting the lightest GitHub workspace mode for a given job.",
        purpose="Choose the cheapest sufficient GitHub workspace mode for the work at hand.",
        inputs="The task's runtime, isolation, and tooling requirements.",
        outputs="A validated execution plan naming the workspace mode to use.",
        example="Pick a Codespace only when the task needs a runtime; otherwise use a lighter mode and return the plan.",
        success="The chosen mode is the lightest one that satisfies the task's actual requirements.",
    ),
    "dani-roxberrys-teaching-voice": dict(
        desc="Use when generating lesson assets in Dani Roxberry's builder-teacher voice from a plan or outline.",
        purpose="Produce lesson materials that read in Dani Roxberry's teaching voice without a live transcript.",
        inputs="A lesson plan, topic outline, or course materials.",
        outputs="Examples, slides, and speaker notes in the precomputed teaching voice.",
        example="Generate examples, then slides and speaker notes for a topic outline in the builder-teacher voice.",
        success="The output stays on-voice and aligns with the plan without requesting a transcript.",
    ),
    "fleet-audit-patterns": dict(
        desc="Use when auditing a fleet of agents for toolkit overlap, duplication, and coverage gaps.",
        purpose="Run a consistent fleet audit covering overlap, duplication, and gaps.",
        inputs="The agent roster and each agent's toolkits, prompts, and usage.",
        outputs="An audit report listing overlaps, gaps, and consolidation recommendations.",
        example="Compare all agents' toolkits and flag any pair with redundant coverage plus any capability nobody owns.",
        success="Every overlap, gap, and redundant-toolkit case in the fleet is named with a recommendation.",
    ),
    "humanize": dict(
        desc="Use when removing recognizable AI writing patterns from text.",
        purpose="Strip AI-typical vocabulary and structure so the text reads human.",
        inputs="Draft text to humanize plus the target tone and audience.",
        outputs="Rewritten text with AI fingerprints removed.",
        example="Rewrite a generated paragraph to drop hedge phrases and formulaic transitions while keeping the meaning.",
        success="The rewrite reads naturally and no longer matches AI-writing detection patterns.",
    ),
    "intake-implementation-workflow": dict(
        desc="Use when resuming Intake product implementation or onboarding a new engineer to its canonical plan.",
        purpose="Provide the canonical planning context for implementing the Intake product.",
        inputs="The current Intake task or the engineer's onboarding need.",
        outputs="The implementation steps and context needed to proceed.",
        example="Hand a new engineer the Intake planning context so implementation resumes without re-deriving decisions.",
        success="The engineer or run has the canonical context and the next implementation step.",
    ),
    "linkedin-lead-gen-outreach": dict(
        desc="Use when researching LinkedIn prospects and running lightweight outreach.",
        purpose="Guide LinkedIn prospecting, research, and outreach from one source of truth.",
        inputs="Target accounts or roles, plus any compliance bounds on outreach.",
        outputs="A prospect list with tailored, compliant outreach messages.",
        example="Research a target account's decision-makers and draft an outreach sequence for them.",
        success="Prospects are researched and the outreach is accurate, tailored, and within stated bounds.",
    ),
    "markdown-mode-router": dict(
        desc="Use when routing Markdown work to teaching versus general formatting mode.",
        purpose="Route Markdown edits to the right mode with minimal structural change.",
        inputs="The Markdown content and the intended outcome.",
        outputs="A mode decision and the normalized Markdown.",
        example="Decide whether a document edit needs teaching mode or general formatting, then normalize it.",
        success="The edit lands in the correct mode with no unnecessary restructuring.",
    ),
    "meeting-to-action": dict(
        desc="Use when converting meeting notes or transcripts into summaries, decisions, and action items.",
        purpose="Turn meeting material into a summary, decisions, and tracked actions.",
        inputs="Meeting notes or a transcript.",
        outputs="Summary, decisions, and owner-tagged action items.",
        example="From a transcript, extract decisions and produce action items each with an owner and due date.",
        success="Every decision and action is captured with an owner so nothing actionable is lost.",
    ),
    "mobile-forensics": dict(
        desc="Use when carving mobile artifacts, databases, and plists from forensic images.",
        purpose="Apply mobile forensics techniques to extract and interpret device artifacts.",
        inputs="A forensic image, database, or filesystem extract plus the investigation question.",
        outputs="Carved artifacts and their interpretation with evidence provenance.",
        example="Recover and reconstruct records from a device database and report what they show.",
        success="Artifacts are extracted with intact provenance and interpreted without overstating findings.",
    ),
    "model-cost-estimator": dict(
        desc="Use when projecting model usage costs from tokens, model pricing, and scenario inputs.",
        purpose="Estimate model usage cost from token and pricing assumptions.",
        inputs="Token assumptions, model pricing, and the scenario (or scenario comparison) to price.",
        outputs="A cost projection or comparison with the assumptions shown.",
        example="Estimate monthly cost for a traffic estimate at a given model's per-token price and note assumptions.",
        success="Every estimate states its token, pricing, and rate assumptions explicitly.",
    ),
    "nextjs-nebula-miniapp": dict(
        desc="Use when building, reviewing, or optimizing a Next.js miniapp in the Nebula sandbox.",
        purpose="Apply Next.js and Nebula-miniapp best practices to build or review an app.",
        inputs="A Next.js miniapp (or its code) plus the production concern to address.",
        outputs="Compliant code/config and a production-readiness checklist result.",
        example="Review a miniapp's component architecture, data fetching, and checklist before deploy.",
        success="The app meets the design, performance, and production-checklist standards.",
    ),
    "product-clone-research": dict(
        desc="Use when capturing a product's routes, flows, and screenshots for clone planning.",
        purpose="Run authenticated reconnaissance to inform a product clone plan.",
        inputs="A target domain and the scope of flows/sections to capture.",
        outputs="Route/flow capture, screenshots, and a handoff prompt for clone planning.",
        example="Map a site's auth and core flows with screenshots, then summarize into a clone-planning handoff.",
        success="The captured artifacts cover the stated scope and produce a usable handoff prompt.",
    ),
    "prompt-technique-router": dict(
        desc="Use when choosing and applying the best-fit prompting technique for a task.",
        purpose="Select and apply the right prompting technique for the task.",
        inputs="The task, its complexity, and any output-quality constraints.",
        outputs="A technique choice and the framed prompt applying it.",
        example="Classify a task's ambiguity and apply the matching technique to the actual prompt.",
        success="A specific technique is chosen and applied, not left as generic advice.",
    ),
    "repo-settings-bootstrap": dict(
        desc="Use when bootstrapping repository settings-as-code with minimal safe changes.",
        purpose="Scaffold repository settings-as-code and governance defaults.",
        inputs="A repository and the governance defaults to establish.",
        outputs="Settings-as-code files (e.g. .github/settings.yml) applied minimally.",
        example="Add a .github/settings.yml with branch protection defaults and no unrelated edits.",
        success="Governance defaults are in place with the smallest diff that achieves them.",
    ),
    "resume-ats-pdf-optimizer": dict(
        desc="Use when scoring and improving a resume PDF against a job description.",
        purpose="Score a resume against a job description and improve it without breaking layout.",
        inputs="A resume PDF and the target job description.",
        outputs="An ATS gap analysis plus minimal, layout-preserving edits.",
        example="Score a resume, list missing keywords, and apply the smallest edits that raise the match.",
        success="Keyword gaps are addressed with edits that preserve the PDF's formatting.",
    ),
    "senior-devops": dict(
        desc="Use when handling CI/CD, infra automation, containerization, and cloud operations.",
        purpose="Provide comprehensive DevOps coverage across CI/CD, containers, and cloud.",
        inputs="The infrastructure or deployment problem and the target environment.",
        outputs="Robust configuration, automation, and operational guidance.",
        example="Design and apply a containerized deployment pipeline with health checks for a service.",
        success="The delivered change is production-safe, reproducible, and documented.",
    ),
    "web-scraper": dict(
        desc="Use when scraping and extracting content from web pages with a multi-strategy approach.",
        purpose="Scrape arbitrary pages with multiple extraction strategies and fallbacks.",
        inputs="Target URLs and what to extract.",
        outputs="Extracted content or structured data with the strategy used.",
        example="Extract article text from a page, falling back from static HTML to rendered content when needed.",
        success="The requested content is extracted and the strategy that worked is reported.",
    ),
    "ai-writing-detection": dict(
        desc="Use when analyzing text for AI authorship or understanding detection patterns.",
        purpose="Detect AI writing via vocabulary, structure, and model fingerprints.",
        inputs="A text sample plus the detection question.",
        outputs="A likelihood assessment citing the specific patterns observed.",
        example="Analyze an essay and identify which AI-writing patterns, if any, it exhibits.",
        success="Findings cite concrete patterns and avoid over-claiming where evidence is weak.",
    ),
    "go-defensive": dict(
        desc="Use when hardening Go code at API boundaries and reviewing for robustness.",
        purpose="Harden Go code for defensive correctness at boundaries.",
        inputs="Go source or a review target.",
        outputs="Fixes or findings for copying, cleanup, and bounds-checking issues.",
        example="Audit a handler and add slice/map copies and defer cleanup where untrusted input crosses a boundary.",
        success="Identified robustness issues are fixed or clearly reported with a rationale.",
    ),
    "improve": dict(
        desc="Use when surveying a codebase for senior-level, prioritized implementation plans.",
        purpose="Produce prioritized, self-contained implementation plans for other executors.",
        inputs="A codebase plus the improvement goal.",
        outputs="Prioritized, self-contained plans for other agents to execute.",
        example="Survey a repo and emit ranked implementation plans, each with enough detail to execute independently.",
        success="Each plan is self-contained, prioritized, and ready for another executor to run.",
    ),
    "owasp-top-10": dict(
        desc="Use when auditing for OWASP Top 10 vulnerabilities or reviewing secure code.",
        purpose="Detect and remediate OWASP Top 10 security issues.",
        inputs="The code, config, or system to audit.",
        outputs="Findings mapped to OWASP categories with remediation steps.",
        example="Audit an app for injection and broken access control and map each finding to its OWASP category.",
        success="Every finding is mapped to an OWASP category with a remediation path.",
    ),
    "qmd": dict(
        desc="Use when bootstrapping QMD search instructions to query indexed local markdown.",
        purpose="Bootstrap QMD search from the installed CLI for indexed markdown retrieval.",
        inputs="A question about local notes/wiki content.",
        outputs="Search instructions and retrieved results from the index.",
        example="Convert a question into QMD search instructions and return matching indexed notes.",
        success="The query is translated into a working QMD search and results are grounded in the index.",
    ),
    "tdd-workflows-tdd-cycle": dict(
        desc="Use when following the TDD cycle within TDD workflows.",
        purpose="Apply the red-green-refactor TDD cycle.",
        inputs="A behavior to implement and its expected behavior.",
        outputs="Failing test, passing implementation, and a refactor.",
        example="Write the failing test, make it pass minimally, then refactor while keeping tests green.",
        success="Each change is driven by a previously failing test that now passes.",
    ),
    "teaching-lesson-plan": dict(
        desc="Use when designing a structured lesson plan for any subject, audience, or format.",
        purpose="Design complete lesson plans with objectives, activities, and assessment.",
        inputs="Subject, audience, format, and duration.",
        outputs="A lesson plan with objectives, activities, timing, and assessment.",
        example="Build a workshop plan with learning objectives, timed activities, and a closing assessment.",
        success="The plan includes objectives, activities, timing, and assessment for the stated audience.",
    ),
    "ios-rendering-protocol": dict(
        desc="Use when deciding how to render text and components on the Nebula iOS client.",
        purpose="Apply the iOS text-rendering protocol in Nebula chat output.",
        inputs="Content to render plus the intended component shape.",
        outputs="Rendering decisions and content shaped for the iOS surface.",
        example="Choose MarkDownRenderer over raw markdown for a chat block so iOS renders it correctly.",
        success="Every renderable block uses the protocol-appropriate component for iOS.",
    ),
    "skill-router-v2": dict(
        desc="Use when routing among globally installed skills to pick the right one for a task.",
        purpose="Route a task to the correct installed skill via a decision tree.",
        inputs="The task and the set of installed skills.",
        outputs="A single best-fit skill selection.",
        example="Classify a request and traverse the router to select the one skill that covers it.",
        success="Exactly one skill is selected and it demonstrably covers the request.",
    ),
}


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, 0, 0
    end = text.find("\n---", 3)
    if end == -1:
        return None, 0, 0
    return text[: end + 4], 4, end + 4


def headings(body):
    return {m.group(1).strip().lower() for m in re.finditer(r"^#{2}\s+(.+?)\s*$", body, re.M)}


def has_asset(d):
    return any(
        p.is_file() and p.suffix.lower() in {".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml"}
        for p in d.rglob("*")
        if not any(part == ".git" for part in p.parts)
    )


def has_tests(d):
    t = d / "tests"
    return t.is_dir() and any(
        p.is_file() and (p.name.startswith("test_") and p.name.endswith(".py")) or p.name.endswith("_test.py")
        for p in t.rglob("*.py")
    )


def has_agents(d):
    return (d / "agents").is_dir()


def compute_level(d):
    if has_agents(d) and has_tests(d):
        return 3
    if has_tests(d):
        return 2
    if has_asset(d):
        return 1
    return 0


def level_label(n):
    return {0: "Intent", 1: "Determinism", 2: "Stability", 3: "Safety and Scale"}[n]


ALIASES = {
    "Purpose": ("purpose", "core rule", "intent", "what it does"),
    "Inputs": ("inputs", "preflight", "runtime model", "what it needs", "input"),
    "Outputs": ("outputs", "what this skill produces", "what it produces", "handoff", "produces", "artifacts"),
    "Example": ("example", "examples", "worked example", "example invocation"),
    "Success criteria": ("success criteria", "definition of done", "validation standard", "done when", "acceptance criteria"),
    "Maturity": ("maturity", "maturity level", "maturity note"),
}


def section_lines(title, body):
    return "## %s\n\n%s\n" % (title, body)


def harden(skill_dir, name):
    path = skill_dir / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    cur = CURATED.get(name)
    if not cur:
        return None

    fm, fm_start, body_start = parse_frontmatter(text)
    if fm is None:
        return "no frontmatter"

    body = text[body_start:]
    h = headings(body)

    # 1. normalized frontmatter metadata
    level = compute_level(skill_dir)
    if re.search(r"(?m)^description:", fm):
        fm = re.sub(r"(?m)^description:.*$", "description: %s" % cur["desc"], fm, count=1)
    else:
        fm = fm.replace("\n---", "\ndescription: %s\n---" % cur["desc"], 1)
    if re.search(r"(?m)^maturity:", fm):
        fm = re.sub(r"(?m)^maturity:.*$", "maturity: %d" % level, fm, count=1)
    else:
        fm = fm.replace("\n---", "\nmaturity: %d\n---" % level, 1)

    # 3. required sections
    additions = []
    if "maturity" not in h and not any(a in h for a in ALIASES["Maturity"]):
        additions.append(section_lines("Maturity", "Level %d - %s. Substantiated by %s." % (
            level, level_label(level),
            "agents/ interface" if level == 3 else "unit tests under tests/" if level == 2 else "a runnable script/structured asset" if level == 1 else "the written contract only; no runnable asset or tests yet",
        )))
    for title in ("Purpose", "Inputs", "Outputs", "Example", "Success criteria"):
        if any(a in h for a in ALIASES[title]):
            continue
        body_text = {
            "Purpose": cur["purpose"],
            "Inputs": cur["inputs"],
            "Outputs": cur["outputs"],
            "Example": cur["example"],
            "Success criteria": cur["success"],
        }[title]
        additions.append(section_lines(title, body_text))

    new_body = body.rstrip("\n")
    if additions:
        new_body = new_body + "\n\n" + "\n".join(additions) + "\n"

    path.write_text(fm + "\n\n" + new_body.lstrip("\n"), encoding="utf-8")
    return (name, level, len(additions))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=DEFAULT_ROOT,
        help="repository root to scan (default: parent of tools/)",
    )
    args = parser.parse_args(argv)

    seen = {
        d.name: d
        for d in sorted(args.root.iterdir())
        if d.is_dir() and (d / "SKILL.md").exists() and d.name in CURATED
    }
    if not seen:
        print("no curated SKILL.md files found under %s" % args.root, file=sys.stderr)
        return 1

    total = 0
    for name, d in sorted(seen.items()):
        res = harden(d, name)
        if res is None:
            print("[skip] %s" % name)
            continue
        n, level, added = res
        total += 1
        print("[ok]   %-32s -> level %d (%d sections added)" % (n, level, added))
    print("\n%d skills hardened" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())

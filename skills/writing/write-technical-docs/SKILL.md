---
name: write-technical-docs
description: Draft, review, and rewrite clear technical documentation in US English or French for France. Use for Markdown or plain-text procedures, API guides, concepts, reference material, troubleshooting, and other technical content that needs consistent terminology, direct instructions, or advisory style checks. Do not use as a translation workflow or as proof of ASD-STE100 compliance.
---

# Write Technical Docs

Produce accurate, usable technical documentation without changing its technical intent.

## Load the rules

1. Read [references/general-rules.md](references/general-rules.md) in full for every English or French task.
2. Read [references/french-rules.md](references/french-rules.md) in full when writing or reviewing French.
3. Apply a supplied project glossary before the bundled lexicon and general preferences.
4. For French, combine this skill with `no-slop-fr`. Keep its precision, concrete language, and no-fluff guidance. Let this skill take priority for technical lists, repeated structures, non-human grammatical subjects, interface fragments, and useful passive constructions.

## Establish the task

- Determine whether to draft, review, or rewrite.
- Confirm the language from the request or source; require one language per checker run.
- Identify the passage type: procedure, concept, API reference, troubleshooting, safety notice, or mixed content.
- Identify the audience, prerequisite knowledge, product terminology, and required tone from available context.
- Request missing facts only when guessing could change safety, behavior, or the documented contract.

Do not translate between English and French as part of this skill. Apply these rules to source text or to a target text produced through a separate translation workflow.

## Draft

1. Extract verified facts, prerequisites, expected results, warnings, and exact product terms.
2. Choose one preferred term for each concept; record project-specific choices before drafting.
3. Organize content around the reader's task or question.
4. Write with the loaded rules and the conventions already established in the surrounding documentation.
5. Run the checker when a file or complete passage is available.
6. Review every finding in context before changing the draft.

## Review

1. Read the complete passage before evaluating individual sentences.
2. Run the checker, if available, to collect advisory findings.
3. Discard findings that conflict with the project glossary, source facts, document conventions, or an intentional exception.
4. Group the remaining findings by impact: technical ambiguity first, task failure risk second, style improvement last.
5. Explain the reason for each recommended change and provide a concrete alternative.
6. Leave acceptable text unchanged. Never derive a compliance score from the number of findings.

## Rewrite

1. Rewrite only when the user requests a revision or approves proposed changes.
2. Preserve technical meaning, scope, conditions, sequence, units, error behavior, and security or safety constraints.
3. Preserve code, commands, identifiers, API names, UI labels, links, and file paths unless the user explicitly asks to change them.
4. Preserve the force and capitalization of normative keywords such as `MUST`, `SHOULD`, and `MAY`.
5. Re-run the checker and inspect the result; do not chase a finding when its suggested change makes the text less exact.

## Use the checker as an adviser

Resolve paths relative to this `SKILL.md`. Use Python 3.10 or later.

```text
python scripts/check_technical_writing.py INPUT --lang en --format json
python scripts/check_technical_writing.py INPUT --lang fr --format text --glossary PROJECT.jsonl
```

Pass `-` as `INPUT` for standard input. Add `--min-confidence low|medium|high` when the user wants fewer or more findings.

- Treat exit code `0` as a completed analysis, including when findings exist.
- Treat exit code `2` as an input, configuration, or missing-model error.
- If the checker cannot run, state the limitation and continue with a manual review. Do not install dependencies without permission.
- Treat confidence as diagnostic certainty, not as severity or proof that a change is required.
- Inspect the original location and surrounding paragraph for every finding.
- Never modify a document automatically from checker output.

## Protect exact technical content

Keep fenced and inline code, configuration keys, commands, identifiers, URLs, link targets, placeholders, and generated output exact. Preserve valid Markdown structure. Change protected content only under an explicit request that names it.

Treat headings, table cells, UI labels, status text, and parameter descriptions as valid fragments when their format makes the meaning clear. Allow repeated syntax in steps and reference entries when parallel structure improves scanning.

## State limitations accurately

Present the checker as non-authoritative writing assistance. Never claim that this skill, its lexicons, or its checker provides ASD approval, certification, authorization, or ASD-STE100 compliance.

Keep the guidance independently authored and general-purpose. Do not copy, adapt, or translate the ASD-STE100 dictionary, rules, or examples into this skill. The copyright notice in [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf) restricts reproduction without written authority, subject to the document's stated special usage rights. The official [Tools for STE](https://www.asd-ste100.org/STEsoftware.html) page also states that ASD and STEMG do not endorse, certify, or authorize checking tools and that writers must evaluate tool feedback.

## Deliver

- For drafting, return the requested document plus only the assumptions that affect its use.
- For review, return prioritized findings with locations, reasons, and optional revisions.
- For rewriting, return the revised text and flag any unresolved technical ambiguity.
- Never label the output as compliant or certified.

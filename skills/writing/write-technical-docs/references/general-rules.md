# General technical-writing rules

Apply these independently authored rules to US English and French technical documentation for France. Treat every uppercase identifier below as a stable interface shared by the skill, checker, tests, and review output. Do not rename an identifier without migrating every consumer.

Use the rules as advice. Prefer technical truth and established project terminology over a mechanical rewrite.

## Contents

- [Terminology](#terminology)
- [Project glossary](#project-glossary)
- [Meaning and normative force](#meaning-and-normative-force)
- [Sentences and actions](#sentences-and-actions)
- [Procedures](#procedures)
- [References and cohesion](#references-and-cohesion)
- [Information structure](#information-structure)
- [Protected content and exceptions](#protected-content-and-exceptions)
- [Review and delivery](#review-and-delivery)
- [Independence and limits](#independence-and-limits)

## Terminology

### `TERM_DISCOURAGED` — Replace a discouraged term when the context matches

- Look up the term's meaning, part of speech, and context before recommending an alternative.
- Prefer the bundled lexicon's preferred term unless a project glossary overrides it.
- Keep a discouraged form when it is an official name, literal UI label, quotation, code element, or required domain term.
- Offer a suggestion instead of treating the occurrence as an error.

### `TERM_INCONSISTENT` — Use one preferred term for one concept

- Map each concept to one preferred term within a document or documentation set.
- Avoid switching between synonyms when readers could infer different meanings.
- Allow distinct terms for distinct concepts, even when everyday language treats them as synonyms.
- Let the project glossary define preferred, allowed, and discouraged variants.

## Project glossary

Pass a JSONL glossary with `--glossary`. Put one JSON object on each nonblank line and use the same schema as `lexicon-en.jsonl` and `lexicon-fr.jsonl`:

- Use string fields `id`, `concept_id`, `language`, `part_of_speech`, `meaning`, `preferred`, and `note`.
- Set `part_of_speech` to `adjective`, `adverb`, `modal`, `noun`, `phrase`, `pronoun`, or `verb`.
- Use non-empty string arrays `allowed_forms`, `discouraged_forms`, and `suggestions`.
- Set `language` to `en` or `fr` and `confidence` to `low`, `medium`, or `high`.
- Include `preferred` in `allowed_forms`.
- Give equivalent English and French entries the same `concept_id` when they represent the same concept.
- Put approved project spellings in `allowed_forms`; put alternatives to flag in `discouraged_forms`.
- Keep each `id` unique and each `(language, concept_id)` pair unique; encode the file as UTF-8.

Let project entries override bundled preferences for the matching language and concept. Preserve exact product terms even when they differ from the bundled lexicon.

## Meaning and normative force

### `MEANING_PRESERVE` — Preserve the technical contract

- Preserve actors, objects, conditions, negation, sequence, ranges, units, defaults, side effects, and failure behavior.
- Preserve distinctions such as required versus optional, synchronous versus asynchronous, and local versus remote.
- Do not invent missing behavior or simplify away an exception.
- Ask for clarification when a stylistic change would require choosing between plausible meanings.

### `NORMATIVE_KEYWORD_PRESERVE` — Keep requirement strength exact

- Preserve normative keywords such as `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` when they carry defined force.
- Do not downgrade an obligation to advice or upgrade a recommendation to a requirement.
- Preserve capitalization when the document uses it to mark normative meaning.
- Apply the same principle to project-defined French equivalents.

## Sentences and actions

### `SENTENCE_FOCUSED` — Give each sentence one clear purpose

- Keep the main relation between actor, action, and object easy to identify.
- Separate background, condition, action, and result when combining them creates ambiguity.
- Retain a longer sentence when splitting it would break a necessary logical relation.

### `SENTENCE_LONG` — Review long sentences, do not reject them automatically

- Suggest a review above 25 words in English or 30 words in French.
- Exclude code, URLs, identifiers, and other protected spans from the useful word count.
- Consider lists, parenthetical text, abbreviations, and domain terms before proposing a split.
- Keep a long sentence when it remains the clearest exact expression.

### `ACTIONS_MULTIPLE` — Keep procedural steps focused

- Prefer one main user action per numbered step.
- Separate independent actions that can fail, require confirmation, or need their own result.
- Keep tightly coupled actions together when separating them would make the procedure harder to follow.
- Do not count conditions, results, or short supporting clauses as separate user actions by default.

### `PASSIVE_AMBIGUOUS` — Flag passive voice only when it hides useful responsibility

- Name the actor when the reader must know who or what performs the action.
- Keep passive voice when the actor is unknown, irrelevant, already established, or less important than the resulting state.
- Allow a component or system as the grammatical subject when it performs the documented behavior.
- Recommend a rewrite only when it clarifies responsibility, sequence, or cause.

### `NOUN_GROUP_COMPLEX` — Unpack hard-to-parse noun groups

- Review long chains of nouns or modifiers that permit more than one attachment or scope.
- Introduce a preposition, relative clause, or defined term when it makes relationships explicit.
- Keep established multi-word product names and domain terms intact.
- Check the project glossary before breaking apart a technical term.

## Procedures

### `PROCEDURE_DIRECT` — Make every step executable

- Start each step with the action in the chosen procedural mood.
- Put prerequisites and safety conditions before the action they constrain.
- Put the expected result after the action and identify how to verify it.
- Name the target precisely; avoid generic instructions such as “handle the issue.”
- Preserve repeated step structure when it helps readers scan equivalent operations.

## References and cohesion

### `REFERENCE_VAGUE` — Make references resolve to one antecedent

- Replace vague pronouns or pointers when two or more antecedents are plausible.
- Name the component, value, step, section, or result instead of relying on “it,” “this,” “that,” “above,” or “below.”
- Keep a short reference when the antecedent is adjacent and unmistakable.
- Prefer stable section names or link text over page-relative directions.

### `LINK_PRESERVE` — Preserve destinations and make labels useful

- Keep URL and Markdown link destinations exact unless the user requests an update.
- Improve visible link text only when doing so preserves the destination and surrounding grammar.
- Avoid using a bare “here” when a destination name would help readers predict the target.

## Information structure

### `STRUCTURE_TASK` — Organize around reader needs

- Put prerequisites before procedures and verification after the relevant action.
- Use headings that identify the task, concept, or reference subject.
- Use numbered lists for ordered actions, bullets for unordered choices, and tables for repeated fields.
- Keep warnings next to the action or condition they govern.
- Allow parallel repetition in API entries, parameter lists, and troubleshooting patterns.

## Protected content and exceptions

### `CODE_PRESERVE` — Keep machine-significant content exact

- Exclude frontmatter, fenced code, inline code, command output, URLs, and link destinations from prose rewrites.
- Preserve identifiers, API fields, option names, file paths, placeholders, version strings, and literal UI labels.
- Do not change case, punctuation, Unicode, spacing, or quoting inside protected content.
- Treat fragments in headings, tables, labels, and reference fields as valid when the container supplies their role.
- Report no high-confidence prose finding solely from an ignored or protected span.

## Review and delivery

### `REVIEW_CONTEXTUALIZE` — Apply human judgment to every finding

- Read the full sentence and surrounding paragraph before recommending a change.
- Check the source facts, project glossary, document type, audience, and intentional exceptions.
- Discard false positives and lower confidence when context remains incomplete.
- Prioritize ambiguity and task risk over cosmetic consistency.
- Explain how a suggestion improves the text; keep the original when it is clearer or more exact.
- Produce no global score, compliance claim, certification claim, or automatic edit.

## Independence and limits

Keep these rules independent from ASD-STE100. Do not reproduce or translate its rules, dictionary entries, or examples. Consult the official [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf) for its copyright notice and stated usage rights. Follow the official [Tools for STE](https://www.asd-ste100.org/STEsoftware.html) guidance that checking tools are aids, can produce inaccurate feedback, and are not endorsed, certified, or authorized by ASD or STEMG.

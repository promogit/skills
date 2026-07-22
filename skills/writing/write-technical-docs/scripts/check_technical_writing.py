#!/usr/bin/env python3
"""Give non-blocking technical-writing advice for English or French text.

The checker is deliberately advisory: findings never change the input and never
make the process fail.  Exit status 2 is reserved for input and configuration
errors, including an unavailable NLP runtime or language model.
"""

from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, TextIO, Tuple


PYTHON_MINIMUM = (3, 10)
SPACY_VERSION = "3.8.14"
MODEL_VERSIONS = {"en": ("en_core_web_sm", "3.8.0"), "fr": ("fr_core_news_sm", "3.8.0")}
CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}
SUPPORTED_SUFFIXES = {".md", ".txt"}
RULE_IDS = {
    "TERM_DISCOURAGED",
    "TERM_INCONSISTENT",
    "SENTENCE_LONG",
    "ACTIONS_MULTIPLE",
    "PASSIVE_AMBIGUOUS",
    "REFERENCE_VAGUE",
    "NOUN_GROUP_COMPLEX",
}

REQUIRED_LEXICON_FIELDS = {
    "id",
    "concept_id",
    "language",
    "part_of_speech",
    "meaning",
    "preferred",
    "allowed_forms",
    "discouraged_forms",
    "suggestions",
    "confidence",
    "note",
}
STRING_LEXICON_FIELDS = {
    "id",
    "concept_id",
    "language",
    "part_of_speech",
    "meaning",
    "preferred",
    "confidence",
    "note",
}
LIST_LEXICON_FIELDS = {"allowed_forms", "discouraged_forms", "suggestions"}
LEXICON_PARTS_OF_SPEECH = {
    "adjective",
    "adverb",
    "modal",
    "noun",
    "phrase",
    "pronoun",
    "verb",
}

SKILL_ROOT = Path(__file__).resolve().parents[1]
BUILTIN_LEXICONS = {
    "en": SKILL_ROOT / "references" / "lexicon-en.jsonl",
    "fr": SKILL_ROOT / "references" / "lexicon-fr.jsonl",
}


class CheckerError(Exception):
    """A user-facing input or configuration error."""


@dataclass(frozen=True)
class LexiconEntry:
    id: str
    concept_id: str
    language: str
    part_of_speech: str
    meaning: str
    preferred: str
    allowed_forms: Tuple[str, ...]
    discouraged_forms: Tuple[str, ...]
    suggestions: Tuple[str, ...]
    confidence: str
    note: str


@dataclass(frozen=True)
class MaskedText:
    text: str
    protected: Tuple[bool, ...]


@dataclass(frozen=True)
class Finding:
    rule_id: str
    file: str
    line: int
    column: int
    excerpt: str
    level: str
    confidence: str
    message: str
    suggestions: Tuple[str, ...] = field(default_factory=tuple)
    offset: int = field(default=0, compare=False, repr=False)

    def as_dict(self) -> Dict[str, Any]:
        """Return only the stable public JSON fields."""

        return {
            "rule_id": self.rule_id,
            "file": self.file,
            "line": self.line,
            "column": self.column,
            "excerpt": self.excerpt,
            "level": self.level,
            "confidence": self.confidence,
            "message": self.message,
            "suggestions": list(self.suggestions),
        }


def _mark_range(marks: List[bool], start: int, end: int) -> None:
    start = max(0, start)
    end = min(len(marks), end)
    if start < end:
        marks[start:end] = [True] * (end - start)


def _range_is_clear(marks: Sequence[bool], start: int, end: int) -> bool:
    return not any(marks[start:end])


def mask_markdown_with_map(text: str) -> MaskedText:
    """Mask non-prose Markdown while retaining every original character offset."""

    marks = [False] * len(text)

    # YAML frontmatter is recognized only at the beginning of the document.
    frontmatter = re.match(
        r"\A(?:\ufeff)?---[ \t]*\r?\n.*?^(?:---|\.\.\.)[ \t]*(?:\r?\n|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if frontmatter:
        _mark_range(marks, frontmatter.start(), frontmatter.end())

    lines = text.splitlines(keepends=True)
    line_offsets: List[int] = []
    running_offset = 0
    for line in lines:
        line_offsets.append(running_offset)
        running_offset += len(line)

    # Headings are fragments, not prose sentences. Mask both ATX headings and
    # setext heading pairs so they cannot distort tagging in the next paragraph.
    for index, line in enumerate(lines):
        line_body = line.rstrip("\r\n")
        start = line_offsets[index]
        if re.match(r"^[ \t]{0,3}#{1,6}(?:[ \t]+|$)", line_body):
            _mark_range(marks, start, start + len(line))
        if index + 1 < len(lines) and line_body.strip():
            underline = lines[index + 1].rstrip("\r\n")
            if re.match(r"^[ \t]{0,3}(?:=+|-+)[ \t]*$", underline):
                _mark_range(marks, start, start + len(line))
                underline_start = line_offsets[index + 1]
                _mark_range(marks, underline_start, underline_start + len(lines[index + 1]))

    # Parse fences line by line so that the closer may contain more fence chars.
    offset = 0
    fence_start: Optional[int] = None
    fence_char = ""
    fence_size = 0
    for line in lines:
        line_body = line.rstrip("\r\n")
        if fence_start is None:
            opener = re.match(r"^[ \t]{0,3}(`{3,}|~{3,})", line_body)
            if opener and _range_is_clear(marks, offset, offset + len(line)):
                fence_start = offset
                fence_char = opener.group(1)[0]
                fence_size = len(opener.group(1))
        else:
            closer = re.match(
                rf"^[ \t]{{0,3}}({re.escape(fence_char)}{{{fence_size},}})[ \t]*$",
                line_body,
            )
            if closer:
                _mark_range(marks, fence_start, offset + len(line))
                fence_start = None
                fence_char = ""
                fence_size = 0
        offset += len(line)
    if fence_start is not None:
        _mark_range(marks, fence_start, len(text))

    # CommonMark indented code uses four columns beyond its container. Track
    # list content indentation so ordinary four-space list continuations remain
    # prose while code nested under a list is still protected.
    list_stack: List[Tuple[int, int]] = []
    for index, line in enumerate(lines):
        line_body = line.rstrip("\r\n")
        if not line_body.strip():
            continue
        leading = re.match(r"^[ \t]*", line_body).group(0)
        indent = len(leading.expandtabs(4))
        list_item = re.match(
            r"^(?P<indent>[ \t]*)(?P<marker>(?:[-+*]|\d{1,9}[.)]))(?P<gap>[ \t]+)",
            line_body,
        )
        if list_item:
            marker_indent = len(list_item.group("indent").expandtabs(4))
            while list_stack and marker_indent <= list_stack[-1][0]:
                list_stack.pop()
            is_list_item = (
                marker_indent <= 3
                if not list_stack
                else list_stack[-1][1] <= marker_indent < list_stack[-1][1] + 4
            )
            if is_list_item:
                gap = min(4, max(1, len(list_item.group("gap").expandtabs(4))))
                content_indent = marker_indent + len(list_item.group("marker")) + gap
                list_stack.append((marker_indent, content_indent))
                continue
        while list_stack and indent < list_stack[-1][1]:
            list_stack.pop()
        code_indent = list_stack[-1][1] + 4 if list_stack else 4
        if indent >= code_indent:
            start = line_offsets[index]
            if _range_is_clear(marks, start, start + len(line)):
                _mark_range(marks, start, start + len(line))

    # CommonMark code spans may cross line boundaries. Require an exact backtick
    # run on both sides so a longer run cannot close a shorter delimiter.
    for match in re.finditer(r"(?<!`)(`+)(?!`)([\s\S]*?)(?<!`)\1(?!`)", text):
        if _range_is_clear(marks, match.start(), match.end()):
            _mark_range(marks, match.start(), match.end())

    # Keep reader-visible link labels available for prose review. Mask the image
    # marker, Markdown punctuation, destinations, and reference identifiers.
    inline_link = re.compile(
        r"(?P<image>!?)\[(?P<label>[^\]\r\n]*)\]\((?P<destination>[^\)\r\n]*(?:\)[^\)\r\n]*)?)\)",
        flags=re.IGNORECASE,
    )
    reference_link = re.compile(
        r"(?P<image>!?)\[(?P<label>[^\]\r\n]*)\]\[(?P<reference>[^\]\r\n]*)\]",
        flags=re.IGNORECASE,
    )
    for pattern in (inline_link, reference_link):
        for match in pattern.finditer(text):
            label_start, label_end = match.span("label")
            if _range_is_clear(marks, match.start(), label_start):
                _mark_range(marks, match.start(), label_start)
            if _range_is_clear(marks, label_end, match.end()):
                _mark_range(marks, label_end, match.end())

    # Autolinks have no separate reader-visible label.
    for match in re.finditer(r"<(?:(?:https?|mailto):)[^>\r\n]+>", text, flags=re.IGNORECASE):
        if _range_is_clear(marks, match.start(), match.end()):
            _mark_range(marks, match.start(), match.end())

    # Bare URLs can contain punctuation; trim common prose terminators.
    for match in re.finditer(r"(?i)\b(?:https?://|www\.)[^\s<>]+", text):
        end = match.end()
        while end > match.start() and text[end - 1] in ".,;:!?)]}":
            end -= 1
        if _range_is_clear(marks, match.start(), end):
            _mark_range(marks, match.start(), end)

    # Preserve code-like identifiers, CLI options, paths, and qualified names.
    identifier_patterns = (
        r"(?<!\w)--?[A-Za-z][A-Za-z0-9_-]*\b",
        r"(?<!\w)[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+\b",
        r"(?<!\w)[a-z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*\b",
        r"(?<!\w)[A-Za-z_$][\w$]*(?:(?:::|\.)[A-Za-z_$][\w$]*)+\b",
        r"(?<!\w)[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b",
        r"(?<!\w)(?:\.{0,2}/|/)[^\s<>]+",
        r"(?<!\w)[A-Za-z0-9_-]+\.(?:py|js|ts|tsx|jsx|java|go|rs|rb|php|sh|yaml|yml|json|toml|ini|md|txt)\b",
    )
    for pattern in identifier_patterns:
        for match in re.finditer(pattern, text):
            if _range_is_clear(marks, match.start(), match.end()):
                _mark_range(marks, match.start(), match.end())

    masked = "".join(
        char if not marks[index] or char in "\r\n" else " "
        for index, char in enumerate(text)
    )
    return MaskedText(masked, tuple(marks))


def mask_markdown(text: str) -> str:
    """Convenience API returning only the offset-preserving masked text."""

    return mask_markdown_with_map(text).text


def normalize_for_match(text: str) -> str:
    """Normalize Unicode and typography for case-insensitive term matching."""

    normalized, _ = _normalize_with_offsets(text)
    return normalized


def _normalize_with_offsets(text: str) -> Tuple[str, Tuple[int, ...]]:
    characters: List[str] = []
    offsets: List[int] = []
    apostrophes = {"’", "‘", "‛", "ʼ", "＇", "`"}
    dashes = {"‐", "‑", "‒", "–", "—", "―", "−"}
    for index, original in enumerate(text):
        char = "'" if original in apostrophes else "-" if original in dashes else original
        # NFKD is applied character by character so every output code point keeps
        # an exact mapping to its source position, including ligature expansion.
        chunk = unicodedata.normalize("NFKD", char).casefold()
        if original.isspace() and original not in "\r\n":
            chunk = " "
        for item in chunk:
            characters.append(item)
            offsets.append(index)
    return "".join(characters), tuple(offsets)


def _form_regex(normalized_form: str) -> re.Pattern[str]:
    parts = re.split(r"\s+", normalized_form.strip())
    body = r"\s+".join(re.escape(part) for part in parts if part)
    if not body:
        return re.compile(r"(?!x)x")
    prefix = r"(?<!\w)" if normalized_form[0].isalnum() else ""
    suffix = r"(?!\w)" if normalized_form[-1].isalnum() else ""
    return re.compile(prefix + body + suffix)


def find_form_occurrences(
    text: str, form: str, protected: Optional[Sequence[bool]] = None
) -> List[Tuple[int, int]]:
    """Find a term with Unicode normalization and return original offsets."""

    normalized_text, offsets = _normalize_with_offsets(text)
    normalized_form = normalize_for_match(form)
    if not normalized_form.strip() or not offsets:
        return []
    occurrences: List[Tuple[int, int]] = []
    for match in _form_regex(normalized_form).finditer(normalized_text):
        start = offsets[match.start()]
        end = offsets[match.end() - 1] + 1
        if protected is not None and any(protected[start:end]):
            continue
        occurrences.append((start, end))
    return occurrences


def _require_string_list(value: Any, field_name: str, location: str) -> Tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise CheckerError(f"{location}: '{field_name}' must be an array of strings")
    return tuple(value)


def validate_lexicon_record(
    record: Any, location: str, expected_language: Optional[str] = None
) -> LexiconEntry:
    """Validate and convert one JSONL lexicon record."""

    if not isinstance(record, dict):
        raise CheckerError(f"{location}: each JSONL line must contain an object")
    missing = REQUIRED_LEXICON_FIELDS - set(record)
    extra = set(record) - REQUIRED_LEXICON_FIELDS
    if missing:
        raise CheckerError(f"{location}: missing fields: {', '.join(sorted(missing))}")
    if extra:
        raise CheckerError(f"{location}: unsupported fields: {', '.join(sorted(extra))}")
    for name in STRING_LEXICON_FIELDS:
        if not isinstance(record[name], str):
            raise CheckerError(f"{location}: '{name}' must be a string")
    for name in ("id", "concept_id", "language", "part_of_speech", "meaning", "preferred"):
        if not record[name].strip():
            raise CheckerError(f"{location}: '{name}' must not be empty")
    if record["language"] not in MODEL_VERSIONS:
        raise CheckerError(f"{location}: 'language' must be 'en' or 'fr'")
    if expected_language and record["language"] != expected_language:
        raise CheckerError(
            f"{location}: expected language '{expected_language}', got '{record['language']}'"
        )
    if record["confidence"] not in CONFIDENCE_RANK:
        raise CheckerError(f"{location}: 'confidence' must be low, medium, or high")
    if record["part_of_speech"] not in LEXICON_PARTS_OF_SPEECH:
        allowed = ", ".join(sorted(LEXICON_PARTS_OF_SPEECH))
        raise CheckerError(f"{location}: 'part_of_speech' must be one of: {allowed}")
    lists = {name: _require_string_list(record[name], name, location) for name in LIST_LEXICON_FIELDS}
    if any(not values for values in lists.values()):
        raise CheckerError(f"{location}: form and suggestion arrays must not be empty")
    if any(not item.strip() for values in lists.values() for item in values):
        raise CheckerError(f"{location}: form and suggestion strings must not be empty")
    preferred = normalize_for_match(record["preferred"])
    if preferred not in {normalize_for_match(form) for form in lists["allowed_forms"]}:
        raise CheckerError(f"{location}: 'preferred' must also occur in 'allowed_forms'")
    return LexiconEntry(
        id=record["id"],
        concept_id=record["concept_id"],
        language=record["language"],
        part_of_speech=record["part_of_speech"],
        meaning=record["meaning"],
        preferred=record["preferred"],
        allowed_forms=lists["allowed_forms"],
        discouraged_forms=lists["discouraged_forms"],
        suggestions=lists["suggestions"],
        confidence=record["confidence"],
        note=record["note"],
    )


def load_lexicon(path: Path, expected_language: Optional[str] = None) -> List[LexiconEntry]:
    """Load a strict UTF-8 JSONL lexicon."""

    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise CheckerError(f"cannot read lexicon '{path}': {exc}") from exc
    entries: List[LexiconEntry] = []
    ids = set()
    concepts = set()
    for line_number, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        location = f"{path}:{line_number}"
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CheckerError(f"{location}: invalid JSON: {exc.msg}") from exc
        entry = validate_lexicon_record(record, location, expected_language)
        if entry.id in ids:
            raise CheckerError(f"{location}: duplicate id '{entry.id}'")
        concept_key = (entry.language, entry.concept_id)
        if concept_key in concepts:
            raise CheckerError(
                f"{location}: duplicate concept_id '{entry.concept_id}' for language '{entry.language}'"
            )
        ids.add(entry.id)
        concepts.add(concept_key)
        entries.append(entry)
    if not entries:
        raise CheckerError(f"lexicon '{path}' contains no records")
    return entries


def merge_lexicons(
    builtin: Sequence[LexiconEntry], project: Sequence[LexiconEntry], language: str
) -> List[LexiconEntry]:
    """Apply language-specific project entries as concept-level overrides."""

    local = [entry for entry in project if entry.language == language]
    overridden_ids = {entry.id for entry in local}
    overridden_concepts = {entry.concept_id for entry in local}
    authorized = {
        normalize_for_match(form)
        for entry in local
        for form in (entry.preferred, *entry.allowed_forms)
    }
    merged: List[LexiconEntry] = []
    for entry in builtin:
        if entry.id in overridden_ids or entry.concept_id in overridden_concepts:
            continue
        discouraged = tuple(
            form for form in entry.discouraged_forms if normalize_for_match(form) not in authorized
        )
        merged.append(replace(entry, discouraged_forms=discouraged))
    merged.extend(local)
    return merged


def _line_column(text: str, offset: int) -> Tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    previous_newline = text.rfind("\n", 0, offset)
    return line, offset - previous_newline


def _excerpt(text: str, start: int, end: Optional[int] = None, limit: int = 180) -> str:
    end = start + 1 if end is None else max(start + 1, end)
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    value = text[line_start:line_end].strip()
    if len(value) <= limit:
        return value
    relative = max(0, start - line_start)
    window_start = max(0, min(relative - limit // 3, len(value) - limit))
    clipped = value[window_start : window_start + limit]
    return ("…" if window_start else "") + clipped + ("…" if window_start + limit < len(value) else "")


def _make_finding(
    rule_id: str,
    source: str,
    original: str,
    start: int,
    end: int,
    level: str,
    confidence: str,
    message: str,
    suggestions: Sequence[str] = (),
) -> Finding:
    line, column = _line_column(original, start)
    return Finding(
        rule_id=rule_id,
        file=source,
        line=line,
        column=column,
        excerpt=_excerpt(original, start, end),
        level=level,
        confidence=confidence,
        message=message,
        suggestions=tuple(suggestions),
        offset=start,
    )


MESSAGES = {
    "en": {
        "discouraged": "Consider replacing '{found}' with the preferred term '{preferred}'.",
        "inconsistent": "Use one term consistently for this concept; prefer '{preferred}'.",
        "long": "This sentence has {count} words; consider splitting it into focused sentences.",
        "actions": "This sentence appears to contain multiple actions; consider one action per step.",
        "passive": "Review this passive construction: the responsible actor may be unclear.",
        "vague": "Replace the potentially vague reference '{found}' with an explicit name.",
        "noun": "Consider unpacking this dense noun group into a clearer phrase.",
    },
    "fr": {
        "discouraged": "Envisagez de remplacer « {found} » par le terme privilégié « {preferred} ».",
        "inconsistent": "Utilisez un seul terme pour ce concept ; privilégiez « {preferred} ».",
        "long": "Cette phrase contient {count} mots ; envisagez de la scinder en phrases ciblées.",
        "actions": "Cette phrase semble contenir plusieurs actions ; envisagez une action par étape.",
        "passive": "Vérifiez cette tournure passive : le responsable de l'action peut être ambigu.",
        "vague": "Remplacez la référence potentiellement vague « {found} » par un nom explicite.",
        "noun": "Envisagez de décomposer ce groupe nominal dense pour le rendre plus clair.",
    },
}


def detect_terminology(
    original: str,
    masked: MaskedText,
    source: str,
    language: str,
    entries: Sequence[LexiconEntry],
    doc: Any = None,
) -> List[Finding]:
    findings: List[Finding] = []
    messages = MESSAGES[language]
    allowed_by_form: Dict[str, set] = {}
    for candidate in entries:
        for form in (candidate.preferred, *candidate.allowed_forms):
            allowed_by_form.setdefault(normalize_for_match(form), set()).add(candidate.concept_id)

    try:
        doc_tokens = list(doc) if doc is not None else []
    except TypeError:
        doc_tokens = []

    def context_matches(entry: LexiconEntry, start: int, end: int, form: str) -> bool:
        """Use local POS context to avoid homograph advice."""

        other_concepts = allowed_by_form.get(normalize_for_match(form), set()) - {entry.concept_id}
        expected = {
            "noun": {"NOUN", "PROPN"},
            "verb": {"VERB"},
            "adjective": {"ADJ"},
            "adverb": {"ADV"},
            "modal": {"AUX", "VERB"},
            "pronoun": {"PRON"},
        }.get(entry.part_of_speech)
        overlapping = [
            token
            for token in doc_tokens
            if _token_start(token) < end
            and _token_start(token) + len(str(_attr(token, "text", ""))) > start
        ]
        if expected is not None and overlapping:
            return any(_attr(token, "pos_") in expected for token in overlapping)
        if other_concepts:
            # Suppression is safer than a context-blind false positive when the
            # same spelling is explicitly accepted for another concept.
            return False
        return True

    for entry in entries:
        preferred_occurrences: List[Tuple[int, int]] = []
        for form in (entry.preferred, *entry.allowed_forms):
            preferred_occurrences.extend(
                find_form_occurrences(masked.text, form, masked.protected)
            )
        discouraged_occurrences: List[Tuple[int, int]] = []
        for form in entry.discouraged_forms:
            for start, end in find_form_occurrences(masked.text, form, masked.protected):
                if not context_matches(entry, start, end, form):
                    continue
                discouraged_occurrences.append((start, end))
                found = original[start:end]
                suggestions = entry.suggestions or (entry.preferred,)
                findings.append(
                    _make_finding(
                        "TERM_DISCOURAGED",
                        source,
                        original,
                        start,
                        end,
                        "advice",
                        entry.confidence,
                        messages["discouraged"].format(found=found, preferred=entry.preferred),
                        suggestions,
                    )
                )
        # Different inflections in allowed_forms are intentionally equivalent.
        # Report inconsistency only when an accepted label and a discouraged
        # competing label both occur for the same concept.
        if preferred_occurrences and discouraged_occurrences:
            for start, end in discouraged_occurrences:
                findings.append(
                    _make_finding(
                        "TERM_INCONSISTENT",
                        source,
                        original,
                        start,
                        end,
                        "advice",
                        "medium",
                        messages["inconsistent"].format(preferred=entry.preferred),
                        (entry.preferred,),
                    )
                )
    return findings


def _tokens(span: Any) -> List[Any]:
    try:
        return list(span)
    except TypeError:
        return []


def _attr(token: Any, name: str, default: Any = "") -> Any:
    return getattr(token, name, default)


def _token_lower(token: Any) -> str:
    value = _attr(token, "lower_", None)
    return value if value is not None else str(_attr(token, "text", "")).casefold()


def _token_start(token: Any, fallback: int = 0) -> int:
    return int(_attr(token, "idx", fallback))


def _span_bounds(span: Any) -> Tuple[int, int]:
    start = int(_attr(span, "start_char", 0))
    end = int(_attr(span, "end_char", start + len(str(_attr(span, "text", "")))))
    return start, end


def _is_word(token: Any) -> bool:
    is_alpha = _attr(token, "is_alpha", None)
    if is_alpha is not None:
        return bool(is_alpha)
    return bool(re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ]", str(_attr(token, "text", ""))))


def _sentences(doc: Any) -> List[Any]:
    try:
        return list(doc.sents)
    except (AttributeError, TypeError, ValueError):
        return []


def detect_sentence_length(
    doc: Any, original: str, source: str, language: str
) -> List[Finding]:
    threshold = 25 if language == "en" else 30
    findings: List[Finding] = []
    for sentence in _sentences(doc):
        words = [token for token in _tokens(sentence) if _is_word(token)]
        if len(words) <= threshold:
            continue
        start, end = _span_bounds(sentence)
        start = _token_start(words[0], start) if words else start
        findings.append(
            _make_finding(
                "SENTENCE_LONG",
                source,
                original,
                start,
                end,
                "advice",
                "high",
                MESSAGES[language]["long"].format(count=len(words)),
                (),
            )
        )
    return findings


def detect_multiple_actions(
    doc: Any, original: str, source: str, language: str
) -> List[Finding]:
    connectors = {"en": {"and", "then"}, "fr": {"et", "puis", "ensuite"}}[language]
    findings: List[Finding] = []
    for sentence in _sentences(doc):
        tokens = _tokens(sentence)
        verbs = [
            token
            for token in tokens
            if _attr(token, "pos_") == "VERB"
            and _attr(token, "dep_") not in {"aux", "aux:pass", "auxpass"}
        ]
        coordinated = any(_attr(token, "dep_") == "conj" for token in verbs) or any(
            _token_lower(token) in connectors for token in tokens
        )
        word_tokens = [token for token in tokens if _is_word(token)]
        first_word = word_tokens[0] if word_tokens else None
        first_is_action = first_word in verbs if first_word is not None else False
        if first_word is not None and first_is_action:
            morph = str(_attr(first_word, "morph", ""))
            first_is_action = (
                "Mood=Imp" in morph
                or "VerbForm=Inf" in morph
                or _attr(first_word, "dep_") == "ROOT"
                or _attr(first_word, "tag_") in {"VB", "VERB__Inf"}
            )
        if len(verbs) < 2 or not coordinated or not first_is_action:
            continue
        start, end = _span_bounds(sentence)
        start = _token_start(verbs[0], start)
        findings.append(
            _make_finding(
                "ACTIONS_MULTIPLE",
                source,
                original,
                start,
                end,
                "review",
                "medium",
                MESSAGES[language]["actions"],
                (),
            )
        )
    return findings


def _looks_like_french_passive(tokens: Sequence[Any], index: int) -> bool:
    token = tokens[index]
    lemma = str(_attr(token, "lemma_", "")).casefold()
    if lemma not in {"être", "etre"}:
        return False
    for candidate in tokens[index + 1 : index + 4]:
        if _attr(candidate, "pos_") not in {"VERB", "ADJ"}:
            continue
        morph = str(_attr(candidate, "morph", ""))
        tag = str(_attr(candidate, "tag_", ""))
        if "Part" in morph or "Past" in morph or tag in {"VERB__Part", "VPP"}:
            return True
    return False


def detect_ambiguous_passive(
    doc: Any, original: str, source: str, language: str
) -> List[Finding]:
    findings: List[Finding] = []
    for sentence in _sentences(doc):
        tokens = _tokens(sentence)
        passive_tokens = [
            token
            for token in tokens
            if _attr(token, "dep_") in {"auxpass", "aux:pass", "nsubjpass", "nsubj:pass"}
        ]
        if language == "fr" and not passive_tokens:
            passive_tokens = [
                token for index, token in enumerate(tokens) if _looks_like_french_passive(tokens, index)
            ]
        if not passive_tokens:
            continue
        explicit_agent = any(
            _attr(token, "dep_") in {"agent", "obl:agent"} for token in tokens
        )
        agent_marker = "by" if language == "en" else "par"
        if not explicit_agent:
            for index, token in enumerate(tokens[:-1]):
                if _token_lower(token) == agent_marker and _attr(tokens[index + 1], "pos_") in {
                    "NOUN",
                    "PROPN",
                    "PRON",
                    "DET",
                }:
                    explicit_agent = True
                    break
        if explicit_agent:
            continue
        start, end = _span_bounds(sentence)
        start = _token_start(passive_tokens[0], start)
        findings.append(
            _make_finding(
                "PASSIVE_AMBIGUOUS",
                source,
                original,
                start,
                end,
                "review",
                "medium",
                MESSAGES[language]["passive"],
                (),
            )
        )
    return findings


def detect_vague_references(
    doc: Any, original: str, source: str, language: str
) -> List[Finding]:
    demonstratives = {
        "en": {"this", "that", "these", "those"},
        "fr": {"ceci", "cela", "ça", "ca", "celui-ci", "celle-ci"},
    }[language]
    pronouns = {"en": {"it"}, "fr": {"il", "elle", "ils", "elles"}}[language]
    spatial = {
        "en": {"above", "below", "previous", "following", "aforementioned"},
        "fr": {"ci-dessus", "ci-dessous", "précédent", "précédente", "suivant", "suivante"},
    }[language]
    findings: List[Finding] = []
    sentences = _sentences(doc)
    for sentence_index, sentence in enumerate(sentences):
        tokens = _tokens(sentence)
        for index, token in enumerate(tokens):
            lower = _token_lower(token)
            vague = False
            confidence = "medium"
            if lower in demonstratives:
                # English "that" is often a complementizer rather than a
                # reference (for example, "Verify that the service is ready").
                if _attr(token, "pos_") not in {"DET", "PRON"}:
                    continue
                next_nominal = next(
                    (
                        candidate
                        for candidate in tokens[index + 1 : index + 5]
                        if _is_word(candidate) and _attr(candidate, "pos_") in {"NOUN", "PROPN"}
                    ),
                    None,
                )
                # A demonstrative determiner governing a nearby named noun is
                # explicit enough, including when an adjective intervenes.
                vague = not (_attr(token, "pos_") == "DET" and next_nominal is not None)
            elif lower in pronouns:
                vague = _attr(token, "dep_") in {"nsubj", "nsubj:pass", "nsubjpass"}
                if not _attr(token, "dep_"):
                    vague = index == 0
                if _attr(token, "dep_") == "expl":
                    vague = False
                # A single named entity in the immediately preceding sentence
                # is a reasonable local antecedent. Remaining pronoun cases are
                # deliberately low-confidence and hidden by the default filter.
                if vague and sentence_index:
                    previous_nominals = [
                        candidate
                        for candidate in _tokens(sentences[sentence_index - 1])
                        if _attr(candidate, "pos_") in {"NOUN", "PROPN"}
                    ]
                    if len(previous_nominals) == 1:
                        vague = False
                confidence = "low"
            elif lower in spatial:
                next_token = next(
                    (candidate for candidate in tokens[index + 1 :] if _is_word(candidate)), None
                )
                vague = not (
                    _attr(token, "pos_") in {"ADJ", "DET"}
                    and next_token is not None
                    and _attr(next_token, "pos_") in {"NOUN", "PROPN"}
                )
            if not vague:
                continue
            start = _token_start(token, _span_bounds(sentence)[0])
            token_text = str(_attr(token, "text", lower))
            findings.append(
                _make_finding(
                    "REFERENCE_VAGUE",
                    source,
                    original,
                    start,
                    start + len(token_text),
                    "review",
                    confidence,
                    MESSAGES[language]["vague"].format(found=token_text),
                    (),
                )
            )
    return findings


def detect_complex_noun_groups(
    doc: Any,
    original: str,
    source: str,
    language: str,
    entries: Sequence[LexiconEntry] = (),
) -> List[Finding]:
    try:
        chunks = list(doc.noun_chunks)
    except (AttributeError, TypeError, ValueError):
        return []
    findings: List[Finding] = []
    authorized_forms = {
        normalize_for_match(form).strip()
        for entry in entries
        for form in (entry.preferred, *entry.allowed_forms)
        if len(normalize_for_match(form).split()) >= 2
    }
    for chunk in chunks:
        tokens = [token for token in _tokens(chunk) if _is_word(token)]
        content = [token for token in tokens if _attr(token, "pos_") not in {"DET", "ADP", "CCONJ"}]
        nominals = [token for token in content if _attr(token, "pos_") in {"NOUN", "PROPN"}]
        if not (len(tokens) >= 8 or (len(tokens) >= 5 and len(nominals) >= 3)):
            continue
        # Do not advise writers to unpack a glossary-approved multiword term.
        # Ignore leading determiners for this exact-term comparison, but do not
        # suppress a larger noun group that merely contains an approved term.
        term_tokens = [token for token in tokens if _attr(token, "pos_") != "DET"]
        term_text = normalize_for_match(
            " ".join(str(_attr(token, "text", "")) for token in term_tokens)
        ).strip()
        if term_text in authorized_forms:
            continue
        start, end = _span_bounds(chunk)
        findings.append(
            _make_finding(
                "NOUN_GROUP_COMPLEX",
                source,
                original,
                start,
                end,
                "review",
                "medium",
                MESSAGES[language]["noun"],
                (),
            )
        )
    return findings


def analyze_text(
    original: str,
    source: str,
    language: str,
    nlp: Any,
    entries: Sequence[LexiconEntry],
    min_confidence: str = "medium",
) -> List[Finding]:
    """Analyze text without changing it."""

    masked = mask_markdown_with_map(original)
    try:
        doc = nlp(masked.text)
    except Exception as exc:  # spaCy pipeline failures are configuration errors.
        raise CheckerError(f"NLP analysis failed: {exc}") from exc
    findings = detect_terminology(original, masked, source, language, entries, doc)
    findings.extend(detect_sentence_length(doc, original, source, language))
    findings.extend(detect_multiple_actions(doc, original, source, language))
    findings.extend(detect_ambiguous_passive(doc, original, source, language))
    findings.extend(detect_vague_references(doc, original, source, language))
    findings.extend(detect_complex_noun_groups(doc, original, source, language, entries))

    minimum = CONFIDENCE_RANK[min_confidence]
    unique: Dict[Tuple[str, int], Finding] = {}
    for finding in findings:
        if CONFIDENCE_RANK[finding.confidence] < minimum:
            continue
        unique.setdefault((finding.rule_id, finding.offset), finding)
    return sorted(unique.values(), key=lambda item: (item.offset, item.rule_id))


def load_nlp(language: str) -> Any:
    """Load the pinned spaCy runtime and model, with actionable failures."""

    if sys.version_info < PYTHON_MINIMUM:
        current = ".".join(str(value) for value in sys.version_info[:3])
        raise CheckerError(f"Python 3.10 or later is required (current: {current})")
    try:
        spacy = importlib.import_module("spacy")
    except ImportError as exc:
        raise CheckerError(
            "spaCy 3.8.14 is not installed; install requirements-nlp.txt in a Python 3.10+ environment"
        ) from exc
    except Exception as exc:
        raise CheckerError(f"cannot import spaCy {SPACY_VERSION}: {exc}") from exc
    actual_spacy = str(getattr(spacy, "__version__", "unknown"))
    if actual_spacy != SPACY_VERSION:
        raise CheckerError(f"spaCy {SPACY_VERSION} is required (current: {actual_spacy})")
    model, expected_version = MODEL_VERSIONS[language]
    try:
        nlp = spacy.load(model)
    except (ImportError, OSError) as exc:
        raise CheckerError(
            f"spaCy model {model} {expected_version} is not installed; install requirements-nlp.txt"
        ) from exc
    except Exception as exc:
        raise CheckerError(f"cannot load spaCy model {model} {expected_version}: {exc}") from exc
    actual_model = str(getattr(nlp, "meta", {}).get("version", "unknown"))
    if actual_model != expected_version:
        raise CheckerError(
            f"spaCy model {model} {expected_version} is required (current: {actual_model})"
        )
    # Markdown fragments and whitespace can make the statistical parser create
    # surprising boundaries. A rule-based first pass stabilizes punctuation
    # boundaries; the dependency parser then respects those preset starts.
    pipe_names = tuple(getattr(nlp, "pipe_names", ()))
    if "sentencizer" not in pipe_names and hasattr(nlp, "add_pipe"):
        position = {"before": "parser"} if "parser" in pipe_names else {"first": True}
        try:
            nlp.add_pipe("sentencizer", config={"overwrite": True}, **position)
        except Exception as exc:
            raise CheckerError(f"cannot configure sentence segmentation for {model}: {exc}") from exc
    return nlp


def read_input(value: str, stdin: TextIO) -> Tuple[str, str]:
    """Read a supported UTF-8 input and return text plus its output label."""

    if value == "-":
        try:
            return stdin.read(), "-"
        except (OSError, UnicodeError) as exc:
            raise CheckerError(f"cannot read stdin: {exc}") from exc
    path = Path(value)
    if path.suffix.casefold() not in SUPPORTED_SUFFIXES:
        raise CheckerError("input must be a .md or .txt file, or '-' for stdin")
    if not path.is_file():
        raise CheckerError(f"input file does not exist or is not a file: '{path}'")
    try:
        return path.read_text(encoding="utf-8"), str(path)
    except (OSError, UnicodeError) as exc:
        raise CheckerError(f"cannot read input '{path}': {exc}") from exc


def format_text(findings: Sequence[Finding], source: str, language: str) -> str:
    if not findings:
        return f"{source}: no advice.\n" if language == "en" else f"{source} : aucun conseil.\n"
    lines = []
    for finding in findings:
        line = (
            f"{finding.file}:{finding.line}:{finding.column} "
            f"[{finding.level}/{finding.confidence}] {finding.rule_id} {finding.message}"
        )
        if finding.suggestions:
            label = "Suggestions" if language == "en" else "Suggestions"
            line += f" {label}: {', '.join(finding.suggestions)}"
        lines.append(line)
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Give advisory technical-writing feedback without modifying the input."
    )
    parser.add_argument("input", metavar="INPUT", help="a .md/.txt file, or - for stdin")
    parser.add_argument("--lang", choices=("en", "fr"), required=True, help="document language")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    parser.add_argument("--glossary", type=Path, help="project JSONL glossary")
    parser.add_argument(
        "--min-confidence", choices=("low", "medium", "high"), default="medium"
    )
    return parser


def main(
    argv: Optional[Sequence[str]] = None,
    *,
    stdin: Optional[TextIO] = None,
    stdout: Optional[TextIO] = None,
    stderr: Optional[TextIO] = None,
    nlp_loader: Any = load_nlp,
) -> int:
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    args = build_parser().parse_args(argv)
    try:
        original, source = read_input(args.input, stdin)
        builtin = load_lexicon(BUILTIN_LEXICONS[args.lang], expected_language=args.lang)
        project: List[LexiconEntry] = []
        if args.glossary is not None:
            if args.glossary.suffix.casefold() != ".jsonl":
                raise CheckerError("project glossary must be a .jsonl file")
            project = load_lexicon(args.glossary)
        entries = merge_lexicons(builtin, project, args.lang)
        nlp = nlp_loader(args.lang)
        findings = analyze_text(
            original,
            source,
            args.lang,
            nlp,
            entries,
            min_confidence=args.min_confidence,
        )
    except CheckerError as exc:
        stderr.write(f"error: {exc}\n")
        return 2

    if args.output_format == "json":
        json.dump([finding.as_dict() for finding in findings], stdout, ensure_ascii=False, indent=2)
        stdout.write("\n")
    else:
        stdout.write(format_text(findings, source, args.lang))
    # Findings are advice, not failures.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

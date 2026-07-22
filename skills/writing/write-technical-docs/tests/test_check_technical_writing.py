import importlib.util
import io
import json
import re
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "check_technical_writing.py"
SPEC = importlib.util.spec_from_file_location("write_technical_docs_checker", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)


class FakeToken:
    def __init__(
        self,
        text,
        idx,
        pos="NOUN",
        dep="",
        lemma=None,
        morph="",
        tag="",
        is_alpha=None,
    ):
        self.text = text
        self.idx = idx
        self.pos_ = pos
        self.dep_ = dep
        self.lemma_ = text.casefold() if lemma is None else lemma
        self.lower_ = text.casefold()
        self.morph = morph
        self.tag_ = tag
        self.is_alpha = bool(re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ]", text)) if is_alpha is None else is_alpha


class FakeSpan:
    def __init__(self, original, tokens):
        self._tokens = list(tokens)
        self.start_char = self._tokens[0].idx if self._tokens else 0
        if self._tokens:
            last = self._tokens[-1]
            self.end_char = last.idx + len(last.text)
        else:
            self.end_char = self.start_char
        self.text = original[self.start_char : self.end_char]

    def __iter__(self):
        return iter(self._tokens)


class FakeDoc:
    def __init__(self, tokens=(), sentences=(), noun_chunks=()):
        self._tokens = list(tokens)
        self.sents = list(sentences)
        self.noun_chunks = list(noun_chunks)

    def __iter__(self):
        return iter(self._tokens)


class EmptyNLP:
    def __call__(self, _text):
        return FakeDoc()


def fake_span(original, specs, start_at=0):
    """Build a span from (text, pos, dep, morph, tag) token specs."""

    tokens = []
    cursor = start_at
    for spec in specs:
        word = spec[0]
        index = original.find(word, cursor)
        if index < 0:
            raise AssertionError("token {!r} not found after {} in {!r}".format(word, cursor, original))
        values = list(spec[1:]) + [""] * 4
        pos, dep, morph, tag = values[:4]
        tokens.append(FakeToken(word, index, pos=pos, dep=dep, morph=morph, tag=tag))
        cursor = index + len(word)
    return FakeSpan(original, tokens)


def entry_record(**updates):
    record = {
        "id": "TEST-001",
        "concept_id": "use",
        "language": "en",
        "part_of_speech": "verb",
        "meaning": "Employ something for a purpose.",
        "preferred": "use",
        "allowed_forms": ["use", "uses", "used", "using"],
        "discouraged_forms": ["utilize", "utilizes"],
        "suggestions": ["Use 'use' when the meaning is unchanged."],
        "confidence": "high",
        "note": "Keep specialized measurement terms where needed.",
    }
    record.update(updates)
    return record


def make_entry(**updates):
    return checker.validate_lexicon_record(entry_record(**updates), "test")


class LexiconTests(unittest.TestCase):
    def test_built_in_lexicons_have_fifty_valid_records_each(self):
        for language, path in checker.BUILTIN_LEXICONS.items():
            entries = checker.load_lexicon(path, expected_language=language)
            self.assertEqual(50, len(entries), path)
            self.assertEqual(50, len({item.id for item in entries}))
            self.assertEqual(50, len({item.concept_id for item in entries}))

    def test_schema_requires_exact_fields_and_types(self):
        missing = entry_record()
        del missing["meaning"]
        with self.assertRaisesRegex(checker.CheckerError, "missing fields: meaning"):
            checker.validate_lexicon_record(missing, "memory:1")

        extra = entry_record(extra="value")
        with self.assertRaisesRegex(checker.CheckerError, "unsupported fields: extra"):
            checker.validate_lexicon_record(extra, "memory:1")

        invalid_pos = entry_record(part_of_speech="gerund")
        with self.assertRaisesRegex(checker.CheckerError, "part_of_speech"):
            checker.validate_lexicon_record(invalid_pos, "memory:1")
        pronoun = checker.validate_lexicon_record(
            entry_record(part_of_speech="pronoun"), "memory:1"
        )
        self.assertEqual("pronoun", pronoun.part_of_speech)

        no_suggestions = entry_record(suggestions=[])
        with self.assertRaisesRegex(checker.CheckerError, "must not be empty"):
            checker.validate_lexicon_record(no_suggestions, "memory:1")

        preferred_missing = entry_record(preferred="operate")
        with self.assertRaisesRegex(checker.CheckerError, "preferred.*allowed_forms"):
            checker.validate_lexicon_record(preferred_missing, "memory:1")

    def test_loader_rejects_duplicate_ids_and_concepts(self):
        first = entry_record()
        duplicate_id = entry_record(concept_id="operate")
        duplicate_concept = entry_record(id="TEST-002")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicates.jsonl"
            path.write_text(
                json.dumps(first) + "\n" + json.dumps(duplicate_id) + "\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(checker.CheckerError, "duplicate id"):
                checker.load_lexicon(path)
            path.write_text(
                json.dumps(first) + "\n" + json.dumps(duplicate_concept) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(checker.CheckerError, "duplicate concept_id"):
                checker.load_lexicon(path)

    def test_project_entry_overrides_a_builtin_concept_and_authorizes_terms(self):
        builtin = [make_entry()]
        project = [
            make_entry(
                id="PROJECT-001",
                preferred="utilize",
                allowed_forms=["utilize", "utilizes"],
                discouraged_forms=["leverage"],
                suggestions=["Use 'utilize' for this project's defined operation."],
            )
        ]
        merged = checker.merge_lexicons(builtin, project, "en")
        self.assertEqual(["PROJECT-001"], [item.id for item in merged])
        masked = checker.mask_markdown_with_map("Utilize this operation.")
        findings = checker.detect_terminology(
            "Utilize this operation.", masked, "input.md", "en", merged, FakeDoc()
        )
        self.assertEqual([], findings)


class MaskingAndPositionTests(unittest.TestCase):
    def test_unicode_normalization_handles_apostrophes_dashes_and_decomposition(self):
        self.assertEqual(
            checker.normalize_for_match("L’utilisateur — configuré"),
            checker.normalize_for_match("l'utilisateur - configure\u0301"),
        )
        self.assertEqual([(0, 13)], checker.find_form_occurrences("L’utilisateur", "l'utilisateur"))

    def test_masking_preserves_length_newlines_and_protected_zones(self):
        text = (
            "---\nterm: utilize\n---\n"
            "# Utilize in a heading\n"
            "Utilize setext heading\n=======================\n"
            "`utilize` [utilize](https://example.test/utilize)\n"
            "https://example.test/utilize foo_utilize client.utilize --utilize\n"
            "```python\nutilize()\n```\n"
            "Please utilize this feature.\n"
        )
        masked = checker.mask_markdown_with_map(text)
        self.assertEqual(len(text), len(masked.text))
        self.assertEqual(text.count("\n"), masked.text.count("\n"))
        # The reader-visible link label and the final prose occurrence remain.
        self.assertEqual(2, masked.text.count("utilize"))
        link_label = text.index("[utilize]") + 1
        self.assertFalse(any(masked.protected[link_label : link_label + len("utilize")]))
        visible = text.rfind("utilize")
        self.assertFalse(any(masked.protected[visible : visible + len("utilize")]))

    def test_indented_and_multiline_code_are_masked_with_exact_offsets(self):
        text = (
            "    Please utilize indented code.\n"
            "`Please\nutilize multiline code.`\n"
            "```text\nutilize fenced code\n`~~\nstill utilize fenced code\n```\n"
            "Please utilize prose.\n"
        )
        masked = checker.mask_markdown_with_map(text)
        self.assertEqual(len(text), len(masked.text))
        self.assertEqual(text.count("\n"), masked.text.count("\n"))
        self.assertEqual(1, masked.text.count("utilize"))
        visible = text.rfind("utilize")
        self.assertFalse(any(masked.protected[visible : visible + len("utilize")]))

    def test_list_continuation_remains_prose_but_nested_indented_code_is_masked(self):
        text = (
            "- First item\n"
            "    Please utilize this continuation.\n"
            "\n"
            "      utilize_nested_code()\n"
            "      - utilize literal code\n"
        )
        masked = checker.mask_markdown_with_map(text)
        continuation = text.index("utilize")
        nested_code = [match.start() for match in re.finditer("utilize", text)][1:]
        self.assertFalse(
            any(masked.protected[continuation : continuation + len("utilize")])
        )
        for offset in nested_code:
            self.assertTrue(any(masked.protected[offset : offset + len("utilize")]))

    def test_link_labels_remain_visible_but_destinations_and_references_do_not(self):
        text = (
            "[Please utilize this feature](https://example.test/utilize) and "
            "[use this reference][utilize-reference]."
        )
        findings = checker.analyze_text(
            text, "guide.md", "en", EmptyNLP(), [make_entry()], min_confidence="medium"
        )
        discouraged = [item for item in findings if item.rule_id == "TERM_DISCOURAGED"]
        self.assertEqual(1, len(discouraged))
        self.assertIn("Please utilize this feature", discouraged[0].excerpt)

    def test_findings_keep_original_line_and_column(self):
        text = "First line.\nPlease utilize this feature.\n"
        findings = checker.analyze_text(
            text, "guide.md", "en", EmptyNLP(), [make_entry()], min_confidence="medium"
        )
        discouraged = [item for item in findings if item.rule_id == "TERM_DISCOURAGED"]
        self.assertEqual(1, len(discouraged))
        self.assertEqual((2, 8), (discouraged[0].line, discouraged[0].column))
        self.assertIn("Please utilize", discouraged[0].excerpt)

    def test_no_high_confidence_term_finding_comes_from_masked_markdown(self):
        text = "---\nterm: utilize\n---\n`utilize`\n[use](https://x.test/utilize)\n"
        findings = checker.analyze_text(
            text, "guide.md", "en", EmptyNLP(), [make_entry()], min_confidence="low"
        )
        self.assertEqual([], findings)


class TerminologyTests(unittest.TestCase):
    def test_allowed_inflections_are_not_inconsistent(self):
        text = "Use the client. The service uses the same client."
        findings = checker.detect_terminology(
            text,
            checker.mask_markdown_with_map(text),
            "guide.md",
            "en",
            [make_entry()],
            FakeDoc(),
        )
        self.assertNotIn("TERM_INCONSISTENT", {item.rule_id for item in findings})

    def test_accepted_and_discouraged_labels_are_inconsistent(self):
        text = "Use the client; do not utilize the legacy wrapper."
        findings = checker.detect_terminology(
            text,
            checker.mask_markdown_with_map(text),
            "guide.md",
            "en",
            [make_entry()],
            FakeDoc(),
        )
        self.assertEqual(
            {"TERM_DISCOURAGED", "TERM_INCONSISTENT"}, {item.rule_id for item in findings}
        )

    def test_context_sensitive_backup_is_not_flagged_as_a_noun(self):
        entries = checker.load_lexicon(checker.BUILTIN_LEXICONS["en"], expected_language="en")
        entries = [item for item in entries if item.concept_id in {"backup-noun", "back-up-verb"}]

        noun_text = "Create a backup."
        noun_span = fake_span(
            noun_text,
            [("Create", "VERB", "ROOT"), ("a", "DET", "det"), ("backup", "NOUN", "obj")],
        )
        noun_doc = FakeDoc(list(noun_span), [noun_span])
        noun_findings = checker.detect_terminology(
            noun_text,
            checker.mask_markdown_with_map(noun_text),
            "guide.md",
            "en",
            entries,
            noun_doc,
        )
        self.assertNotIn("TERM_DISCOURAGED", {item.rule_id for item in noun_findings})

        verb_text = "Backup the files."
        verb_span = fake_span(
            verb_text,
            [("Backup", "VERB", "ROOT"), ("the", "DET", "det"), ("files", "NOUN", "obj")],
        )
        verb_doc = FakeDoc(list(verb_span), [verb_span])
        verb_findings = checker.detect_terminology(
            verb_text,
            checker.mask_markdown_with_map(verb_text),
            "guide.md",
            "en",
            entries,
            verb_doc,
        )
        self.assertIn("TERM_DISCOURAGED", {item.rule_id for item in verb_findings})

    def test_pos_gate_suppresses_rollback_noun_for_verb_entry(self):
        entries = checker.load_lexicon(checker.BUILTIN_LEXICONS["en"], expected_language="en")
        entries = [item for item in entries if item.concept_id == "roll-back-verb"]
        text = "Perform a rollback."
        span = fake_span(
            text,
            [("Perform", "VERB", "ROOT"), ("a", "DET", "det"), ("rollback", "NOUN", "obj")],
        )
        findings = checker.detect_terminology(
            text,
            checker.mask_markdown_with_map(text),
            "guide.md",
            "en",
            entries,
            FakeDoc(list(span), [span]),
        )
        self.assertNotIn("TERM_DISCOURAGED", {item.rule_id for item in findings})

    def test_pos_gate_suppresses_french_identifier_used_as_a_verb(self):
        entries = checker.load_lexicon(checker.BUILTIN_LEXICONS["fr"], expected_language="fr")
        entries = [item for item in entries if item.concept_id == "identifier"]
        text = "Identifier la cause."
        span = fake_span(
            text,
            [("Identifier", "VERB", "ROOT"), ("la", "DET", "det"), ("cause", "NOUN", "obj")],
        )
        findings = checker.detect_terminology(
            text,
            checker.mask_markdown_with_map(text),
            "guide.md",
            "fr",
            entries,
            FakeDoc(list(span), [span]),
        )
        self.assertNotIn("TERM_DISCOURAGED", {item.rule_id for item in findings})


class HeuristicTests(unittest.TestCase):
    def test_sentence_length_thresholds_are_strictly_greater_than_limits(self):
        for language, limit in (("en", 25), ("fr", 30)):
            at_limit = " ".join(["word"] * limit)
            span = fake_span(at_limit, [("word", "NOUN", "") for _ in range(limit)])
            self.assertEqual(
                [],
                checker.detect_sentence_length(
                    FakeDoc(list(span), [span]), at_limit, "input.txt", language
                ),
            )

            over_limit = " ".join(["word"] * (limit + 1))
            span = fake_span(over_limit, [("word", "NOUN", "") for _ in range(limit + 1)])
            findings = checker.detect_sentence_length(
                FakeDoc(list(span), [span]), over_limit, "input.txt", language
            )
            self.assertEqual(1, len(findings))
            self.assertEqual("SENTENCE_LONG", findings[0].rule_id)

    def test_multiple_actions_only_flags_probable_procedure_steps(self):
        procedure = "Open the panel and select the profile."
        procedure_span = fake_span(
            procedure,
            [
                ("Open", "VERB", "ROOT", "Mood=Imp", "VB"),
                ("the", "DET", "det"),
                ("panel", "NOUN", "obj"),
                ("and", "CCONJ", "cc"),
                ("select", "VERB", "conj"),
                ("the", "DET", "det"),
                ("profile", "NOUN", "obj"),
            ],
        )
        findings = checker.detect_multiple_actions(
            FakeDoc(list(procedure_span), [procedure_span]), procedure, "guide.md", "en"
        )
        self.assertEqual(["ACTIONS_MULTIPLE"], [item.rule_id for item in findings])

        description = "The service validates and stores the token."
        description_span = fake_span(
            description,
            [
                ("The", "DET", "det"),
                ("service", "NOUN", "nsubj"),
                ("validates", "VERB", "ROOT"),
                ("and", "CCONJ", "cc"),
                ("stores", "VERB", "conj"),
                ("the", "DET", "det"),
                ("token", "NOUN", "obj"),
            ],
        )
        self.assertEqual(
            [],
            checker.detect_multiple_actions(
                FakeDoc(list(description_span), [description_span]),
                description,
                "guide.md",
                "en",
            ),
        )

    def test_passive_without_actor_is_advice_but_explicit_agent_is_not(self):
        ambiguous = "The token was stored."
        ambiguous_span = fake_span(
            ambiguous,
            [
                ("The", "DET", "det"),
                ("token", "NOUN", "nsubjpass"),
                ("was", "AUX", "auxpass"),
                ("stored", "VERB", "ROOT"),
            ],
        )
        findings = checker.detect_ambiguous_passive(
            FakeDoc(list(ambiguous_span), [ambiguous_span]), ambiguous, "guide.md", "en"
        )
        self.assertEqual(["PASSIVE_AMBIGUOUS"], [item.rule_id for item in findings])

        explicit = "The token was stored by the service."
        explicit_span = fake_span(
            explicit,
            [
                ("The", "DET", "det"),
                ("token", "NOUN", "nsubjpass"),
                ("was", "AUX", "auxpass"),
                ("stored", "VERB", "ROOT"),
                ("by", "ADP", "agent"),
                ("the", "DET", "det"),
                ("service", "NOUN", "pobj"),
            ],
        )
        self.assertEqual(
            [],
            checker.detect_ambiguous_passive(
                FakeDoc(list(explicit_span), [explicit_span]), explicit, "guide.md", "en"
            ),
        )

    def test_subject_pronoun_is_low_confidence_but_standalone_demonstrative_is_medium(self):
        text = "It is unclear. This is ambiguous."
        first = fake_span(
            text,
            [("It", "PRON", "nsubj"), ("is", "AUX", "ROOT"), ("unclear", "ADJ", "acomp")],
        )
        second_start = text.index("This")
        second = fake_span(
            text,
            [("This", "PRON", "nsubj"), ("is", "AUX", "ROOT"), ("ambiguous", "ADJ", "acomp")],
            start_at=second_start,
        )
        doc = FakeDoc(list(first) + list(second), [first, second])
        findings = checker.detect_vague_references(doc, text, "guide.md", "en")
        by_word = {text[item.offset : item.offset + (2 if item.offset == 0 else 4)]: item for item in findings}
        self.assertEqual("low", by_word["It"].confidence)
        self.assertEqual("medium", by_word["This"].confidence)

    def test_complementizer_and_explicit_demonstrative_noun_phrase_are_not_vague(self):
        text = "Verify that the service is ready. Use that preferred label."
        first = fake_span(
            text,
            [
                ("Verify", "VERB", "ROOT"),
                ("that", "SCONJ", "mark"),
                ("the", "DET", "det"),
                ("service", "NOUN", "nsubj"),
                ("is", "AUX", "ccomp"),
                ("ready", "ADJ", "acomp"),
            ],
        )
        second_start = text.index("Use")
        second = fake_span(
            text,
            [
                ("Use", "VERB", "ROOT"),
                ("that", "DET", "det"),
                ("preferred", "ADJ", "amod"),
                ("label", "NOUN", "obj"),
            ],
            start_at=second_start,
        )
        doc = FakeDoc(list(first) + list(second), [first, second])
        self.assertEqual([], checker.detect_vague_references(doc, text, "guide.md", "en"))

    def test_complex_noun_group_is_detected(self):
        text = "The distributed session cache retention policy configuration value is optional."
        chunk = fake_span(
            text,
            [
                ("The", "DET", "det"),
                ("distributed", "ADJ", "amod"),
                ("session", "NOUN", "compound"),
                ("cache", "NOUN", "compound"),
                ("retention", "NOUN", "compound"),
                ("policy", "NOUN", "compound"),
                ("configuration", "NOUN", "compound"),
                ("value", "NOUN", "ROOT"),
            ],
        )
        doc = FakeDoc(list(chunk), [chunk], [chunk])
        findings = checker.detect_complex_noun_groups(doc, text, "guide.md", "en")
        self.assertEqual(["NOUN_GROUP_COMPLEX"], [item.rule_id for item in findings])

    def test_glossary_approved_noun_group_is_not_unpacked(self):
        text = "The quantum stream routing policy bundle is active."
        chunk = fake_span(
            text,
            [
                ("The", "DET", "det"),
                ("quantum", "NOUN", "compound"),
                ("stream", "NOUN", "compound"),
                ("routing", "NOUN", "compound"),
                ("policy", "NOUN", "compound"),
                ("bundle", "NOUN", "ROOT"),
            ],
        )
        entry = make_entry(
            id="PROJECT-TERM-001",
            concept_id="quantum-policy-bundle",
            part_of_speech="noun",
            meaning="A project-defined routing policy bundle.",
            preferred="quantum stream routing policy bundle",
            allowed_forms=["quantum stream routing policy bundle"],
            discouraged_forms=["routing package"],
            suggestions=["Use the approved project term."],
        )
        doc = FakeDoc(list(chunk), [chunk], [chunk])
        self.assertEqual(
            [], checker.detect_complex_noun_groups(doc, text, "guide.md", "en", [entry])
        )

    def test_minimum_confidence_filters_advice(self):
        low = checker.Finding(
            "REFERENCE_VAGUE", "x", 1, 1, "It", "review", "low", "message", (), 0
        )
        high = checker.Finding(
            "SENTENCE_LONG", "x", 1, 1, "Long", "advice", "high", "message", (), 1
        )
        # Exercise the public rank contract directly; analyze_text uses this same filter.
        kept = [
            finding
            for finding in (low, high)
            if checker.CONFIDENCE_RANK[finding.confidence] >= checker.CONFIDENCE_RANK["medium"]
        ]
        self.assertEqual([high], kept)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.lexicon = Path(self.temp.name) / "lexicon-en.jsonl"
        self.lexicon.write_text(json.dumps(entry_record(), ensure_ascii=False) + "\n", encoding="utf-8")

    def run_main(self, argv, input_text="", loader=None):
        stdout = io.StringIO()
        stderr = io.StringIO()
        lexicons = {"en": self.lexicon, "fr": self.lexicon}
        with mock.patch.object(checker, "BUILTIN_LEXICONS", lexicons):
            code = checker.main(
                argv,
                stdin=io.StringIO(input_text),
                stdout=stdout,
                stderr=stderr,
                nlp_loader=(lambda _language: EmptyNLP()) if loader is None else loader,
            )
        return code, stdout.getvalue(), stderr.getvalue()

    def test_stdin_json_output_has_exact_public_fields_and_findings_exit_zero(self):
        code, output, error = self.run_main(
            ["-", "--lang", "en", "--format", "json"], "Please utilize this feature."
        )
        self.assertEqual(0, code)
        self.assertEqual("", error)
        payload = json.loads(output)
        self.assertGreaterEqual(len(payload), 1)
        self.assertEqual(
            {
                "rule_id",
                "file",
                "line",
                "column",
                "excerpt",
                "level",
                "confidence",
                "message",
                "suggestions",
            },
            set(payload[0]),
        )
        self.assertEqual("-", payload[0]["file"])

    def test_text_output_and_no_findings_exit_zero(self):
        code, output, error = self.run_main(["-", "--lang", "en"], "Use this feature.")
        self.assertEqual(0, code)
        self.assertEqual("", error)
        self.assertEqual("-: no advice.\n", output)
        self.assertNotIn("score", output.casefold())
        self.assertNotIn("compliance", output.casefold())

    def test_unsupported_input_and_bad_glossary_return_two(self):
        code, _, error = self.run_main(["manual.pdf", "--lang", "en"])
        self.assertEqual(2, code)
        self.assertIn(".md or .txt", error)

        glossary = Path(self.temp.name) / "bad.jsonl"
        glossary.write_text("not-json\n", encoding="utf-8")
        code, _, error = self.run_main(
            ["-", "--lang", "en", "--glossary", str(glossary)], "Use this."
        )
        self.assertEqual(2, code)
        self.assertIn("invalid JSON", error)

    def test_missing_model_cli_path_returns_two_with_clear_message(self):
        fake_spacy = types.SimpleNamespace(__version__="3.8.14")

        def missing_model(_name):
            raise OSError("model unavailable")

        fake_spacy.load = missing_model
        with mock.patch.object(checker.sys, "version_info", (3, 10, 0)), mock.patch.object(
            checker.importlib, "import_module", return_value=fake_spacy
        ):
            code, output, error = self.run_main(
                ["-", "--lang", "en"], "Use this feature.", loader=checker.load_nlp
            )
        self.assertEqual(2, code)
        self.assertEqual("", output)
        self.assertIn("en_core_web_sm 3.8.0 is not installed", error)

    def test_nlp_configuration_failures_return_two_without_tracebacks(self):
        cases = []

        def broken_import(_name):
            raise OSError("broken binary dependency")

        cases.append((broken_import, "cannot import spaCy"))

        broken_load_spacy = types.SimpleNamespace(__version__="3.8.14")

        def broken_load(_name):
            raise ValueError("invalid model configuration")

        broken_load_spacy.load = broken_load
        cases.append((lambda _name: broken_load_spacy, "cannot load spaCy model"))

        class BrokenPipeline:
            meta = {"version": "3.8.0"}
            pipe_names = ("parser",)

            def add_pipe(self, *_args, **_kwargs):
                raise RuntimeError("pipeline is locked")

        broken_pipe_spacy = types.SimpleNamespace(
            __version__="3.8.14", load=lambda _name: BrokenPipeline()
        )
        cases.append((lambda _name: broken_pipe_spacy, "cannot configure sentence segmentation"))

        for importer, expected in cases:
            with self.subTest(expected=expected), mock.patch.object(
                checker.sys, "version_info", (3, 10, 0)
            ), mock.patch.object(checker.importlib, "import_module", side_effect=importer):
                code, output, error = self.run_main(
                    ["-", "--lang", "en"], "Use this feature.", loader=checker.load_nlp
                )
            self.assertEqual(2, code)
            self.assertEqual("", output)
            self.assertIn(expected, error)
            self.assertNotIn("Traceback", error)

    def test_markdown_and_text_file_inputs_are_analyzed_without_modification(self):
        for suffix in (".md", ".txt"):
            path = Path(self.temp.name) / ("guide" + suffix)
            original = "Please utilize this feature.\n"
            path.write_text(original, encoding="utf-8")
            code, output, error = self.run_main(
                [str(path), "--lang", "en", "--format", "json"]
            )
            self.assertEqual(0, code)
            self.assertEqual("", error)
            payload = json.loads(output)
            self.assertEqual(str(path), payload[0]["file"])
            self.assertEqual(original, path.read_text(encoding="utf-8"))

    def test_high_confidence_filter_hides_medium_findings(self):
        entry = entry_record(confidence="medium")
        self.lexicon.write_text(json.dumps(entry) + "\n", encoding="utf-8")
        code, output, _ = self.run_main(
            ["-", "--lang", "en", "--format", "json", "--min-confidence", "high"],
            "Please utilize this feature.",
        )
        self.assertEqual(0, code)
        self.assertEqual([], json.loads(output))


class IntegrationContractTests(unittest.TestCase):
    def test_every_emitted_rule_id_is_documented_in_references(self):
        reference_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (SKILL_ROOT / "references").glob("*.md")
        )
        for rule_id in checker.RULE_IDS:
            self.assertIn(rule_id, reference_text)

    def test_fixture_set_covers_languages_markdown_and_forward_samples(self):
        fixture_dir = Path(__file__).parent / "fixtures"
        expected = {
            "valid-en.md",
            "problematic-en.md",
            "valid-fr.md",
            "problematic-fr.md",
            "api-en.md",
            "procedure-fr.md",
            "domain-terms.md",
            "project-glossary.jsonl",
        }
        self.assertTrue(expected.issubset({path.name for path in fixture_dir.iterdir()}))
        combined = "\n".join(path.read_text(encoding="utf-8") for path in fixture_dir.glob("*.md"))
        self.assertIn("```", combined)
        self.assertIn("| --- |", combined)
        self.assertIn("https://", combined)
        self.assertIn("l’API", combined)

    def test_requirements_pin_runtime_and_both_models(self):
        requirements = (SKILL_ROOT / "requirements-nlp.txt").read_text(encoding="utf-8")
        self.assertIn("Python 3.10", requirements)
        self.assertIn("spacy==3.8.14", requirements)
        self.assertIn("click==8.3.1", requirements)
        self.assertIn("en_core_web_sm-3.8.0", requirements)
        self.assertIn("fr_core_news_sm-3.8.0", requirements)


if __name__ == "__main__":
    unittest.main()

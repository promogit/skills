"""Optional tests that run when the pinned spaCy runtime and models are present."""

import importlib.util
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "check_technical_writing.py"
MODULE_NAME = "write_technical_docs_checker_integration"
SPEC = importlib.util.spec_from_file_location(MODULE_NAME, SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
sys.modules[MODULE_NAME] = checker
SPEC.loader.exec_module(checker)


class SpacyIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.nlp_en = checker.load_nlp("en")
            cls.nlp_fr = checker.load_nlp("fr")
        except checker.CheckerError as exc:
            raise unittest.SkipTest(str(exc))
        cls.lexicon_en = checker.load_lexicon(
            checker.BUILTIN_LEXICONS["en"], expected_language="en"
        )
        cls.lexicon_fr = checker.load_lexicon(
            checker.BUILTIN_LEXICONS["fr"], expected_language="fr"
        )

    def analyze_fixture(self, name, language):
        text = (Path(__file__).parent / "fixtures" / name).read_text(encoding="utf-8")
        nlp = self.nlp_en if language == "en" else self.nlp_fr
        lexicon = self.lexicon_en if language == "en" else self.lexicon_fr
        return checker.analyze_text(text, name, language, nlp, lexicon, "medium")

    def test_real_english_pipeline_finds_representative_advice(self):
        rule_ids = {item.rule_id for item in self.analyze_fixture("problematic-en.md", "en")}
        self.assertTrue(
            {"TERM_DISCOURAGED", "SENTENCE_LONG", "ACTIONS_MULTIPLE"}.issubset(rule_ids),
            rule_ids,
        )

    def test_real_french_pipeline_finds_representative_advice(self):
        rule_ids = {item.rule_id for item in self.analyze_fixture("problematic-fr.md", "fr")}
        self.assertTrue(
            {"TERM_DISCOURAGED", "SENTENCE_LONG", "ACTIONS_MULTIPLE"}.issubset(rule_ids),
            rule_ids,
        )

    def test_real_pos_tagging_suppresses_rollback_noun(self):
        text = "Perform a rollback."
        entries = [item for item in self.lexicon_en if item.concept_id == "roll-back-verb"]
        findings = checker.analyze_text(text, "input.txt", "en", self.nlp_en, entries, "low")
        self.assertNotIn("TERM_DISCOURAGED", {item.rule_id for item in findings})

    def test_real_pos_tagging_suppresses_identifier_verb(self):
        text = "Identifier la cause."
        entries = [item for item in self.lexicon_fr if item.concept_id == "identifier"]
        findings = checker.analyze_text(text, "input.txt", "fr", self.nlp_fr, entries, "low")
        self.assertNotIn("TERM_DISCOURAGED", {item.rule_id for item in findings})

    def test_valid_fixtures_stay_quiet_at_default_confidence(self):
        for name, language in (("valid-en.md", "en"), ("valid-fr.md", "fr")):
            findings = self.analyze_fixture(name, language)
            self.assertEqual([], findings, (name, [item.as_dict() for item in findings]))

    def test_forward_api_and_procedure_fixtures_stay_quiet(self):
        for name, language in (("api-en.md", "en"), ("procedure-fr.md", "fr")):
            findings = self.analyze_fixture(name, language)
            self.assertEqual([], findings, (name, [item.as_dict() for item in findings]))

    def test_forward_domain_fixture_honors_the_project_glossary(self):
        fixture_dir = Path(__file__).parent / "fixtures"
        text = (fixture_dir / "domain-terms.md").read_text(encoding="utf-8")
        project = checker.load_lexicon(fixture_dir / "project-glossary.jsonl")
        entries = checker.merge_lexicons(self.lexicon_en, project, "en")
        findings = checker.analyze_text(
            text, "domain-terms.md", "en", self.nlp_en, entries, "medium"
        )
        terminology = [item for item in findings if item.rule_id == "TERM_DISCOURAGED"]
        self.assertEqual(1, len(terminology), [item.as_dict() for item in findings])
        self.assertEqual(5, terminology[0].line)
        self.assertIn("flux capsule", terminology[0].message)


if __name__ == "__main__":
    unittest.main()

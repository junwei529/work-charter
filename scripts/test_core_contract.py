#!/usr/bin/env python3
"""Focused verifier and installer-inventory regression tests; no installation."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

core = load("tested_core", ROOT / "scripts/check_source_contract.py")
repo = load("tested_repository", ROOT / "scripts/check_repository.py")
install = load("tested_inventory", ROOT / "scripts/manage_install.py")

class CoreAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = core.load_json(core.SPEC)
        cls.witness = core.load_json(ROOT / "evals/core-protections/witness-charter.json")

    def outcome(self, witness):
        return core.assess(self.spec, "charter", ROOT, witness)["result"]

    def test_empty_case_inventory_is_rejected(self):
        spec = copy.deepcopy(self.spec)
        for rule in spec["rules"]:
            rule["cases"] = []
        with self.assertRaises(ValueError):
            core.expected_cases(spec, "charter")

    def test_duplicate_scenario_id_is_rejected(self):
        spec = copy.deepcopy(self.spec)
        spec["rules"][0]["cases"][1]["id"] = spec["rules"][0]["cases"][0]["id"]
        with self.assertRaises(ValueError):
            core.expected_cases(spec, "charter")

    def test_missing_component_cannot_reduce_coverage(self):
        spec = copy.deepcopy(self.spec)
        spec["rules"][0]["locations"].pop("charter")
        with self.assertRaises(ValueError):
            core.expected_cases(spec, "charter")

    def test_real_independent_assessment_is_bound(self):
        self.assertEqual(self.outcome(self.witness), "PASS")

    def test_contradictory_action_is_rejected(self):
        witness = copy.deepcopy(self.witness)
        answer = next(a for a in witness["answers"] if a["case_id"] == "CP01-N")
        answer["decision"] = "ALLOW_SCOPED"
        self.assertEqual(self.outcome(witness), "FAIL")

    def test_unread_scenario_cannot_pass(self):
        witness = copy.deepcopy(self.witness)
        witness["answers"].pop()
        self.assertEqual(self.outcome(witness), "FAIL")

    def test_duplicate_answer_cannot_replace_missing_coverage(self):
        witness = copy.deepcopy(self.witness)
        witness["answers"][-1] = copy.deepcopy(witness["answers"][0])
        self.assertEqual(self.outcome(witness), "FAIL")

    def test_fabricated_source_excerpt_is_rejected(self):
        witness = copy.deepcopy(self.witness)
        witness["answers"][0]["evidence"]["quote"] = "This rule permits publication of all credentials."
        self.assertEqual(self.outcome(witness), "FAIL")

    def test_changed_clause_requests_reassessment_not_wording_failure(self):
        witness = copy.deepcopy(self.witness)
        witness["answers"][0]["clause_bindings"][0]["sha256"] = "0" * 64
        self.assertEqual(self.outcome(witness), "REASSESS")

    def test_changed_scenario_spec_requests_reassessment(self):
        witness = copy.deepcopy(self.witness)
        witness["spec_sha256"] = "0" * 64
        self.assertEqual(self.outcome(witness), "REASSESS")

    def test_paragraph_wrapping_does_not_change_clause_identity(self):
        with self.temp() as folder:
            root = Path(folder)
            path = root / "rules.md"
            location = {"path": "rules.md", "heading": "Contract"}
            path.write_text("# Contract\n\nContinue authorized work.\n", encoding="utf-8")
            before = core.section(root, location)
            path.write_text("# Contract\n\nContinue\n  authorized   work.\n", encoding="utf-8")
            self.assertEqual(core.section(root, location), before)

    def test_duplicate_json_keys_are_rejected(self):
        with self.temp() as folder:
            path = Path(folder) / "input.json"
            path.write_text('{"decision":"BLOCK","decision":"ALLOW_SCOPED"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                core.load_json(path)

    def test_unsafe_relative_input_is_rejected(self):
        with self.assertRaises(ValueError):
            core.safe_file(ROOT, "../outside.md")

    def test_conditional_reference_is_reachable(self):
        with self.temp() as folder:
            root = Path(folder)
            (root / "references").mkdir()
            entry = root / "SKILL.md"
            entry.write_text("[branch](references/a.md)\n", encoding="utf-8")
            (root / "references/a.md").write_text("[detail](b.md#detail)\n", encoding="utf-8")
            (root / "references/b.md").write_text("# Detail\n[return](../SKILL.md)\n", encoding="utf-8")
            (root / "references/orphan.md").write_text("# Orphan\n", encoding="utf-8")
            reached = repo.reachable_package_markdown(root, entry)
            self.assertIn((root / "references/b.md").resolve(), reached)
            self.assertEqual(len(reached), 3)
            self.assertNotIn((root / "references/orphan.md").resolve(), reached)

    @staticmethod
    def temp():
        output = ROOT / ".eval-runs"
        output.mkdir(exist_ok=True)
        return tempfile.TemporaryDirectory(prefix="work-charter-core-", dir=output)

class InventoryTests(unittest.TestCase):
    def test_old_and_current_shapes_remain_accepted(self):
        for shape in [install.LEGACY_PACKAGE_FILES, install.V06_PACKAGE_FILES, install.EXPECTED_FILES]:
            with self.subTest(size=len(shape)):
                self.assertEqual(install.validate_package_file_set(list(shape), "test"), shape)
        self.assertEqual(len(install.EXPECTED_FILES), 8)

    def test_unknown_file_is_rejected(self):
        with self.assertRaises(install.LifecycleError):
            install.validate_package_file_set(list(install.EXPECTED_FILES) + ["extra.txt"], "test")

    def test_duplicate_file_is_rejected(self):
        values = list(install.EXPECTED_FILES)
        with self.assertRaises(install.LifecycleError):
            install.validate_package_file_set(values + values[:1], "test")

    def test_count_mismatch_is_rejected(self):
        metadata = {"package": {"path": "skills/work-charter", "files": list(install.EXPECTED_FILES), "file_count": 7}}
        with self.assertRaises(install.LifecycleError):
            install.candidate_file_set(metadata)

    def test_current_candidate_matches_actual_package(self):
        metadata = install.candidate_metadata(ROOT, "0.12.0")
        _, files, tree = install.package_files(ROOT, metadata, metadata["package"]["tree"])
        self.assertEqual(set(files), install.EXPECTED_FILES)
        self.assertEqual(tree, metadata["package"]["tree"])

    def test_old_descriptors_still_parse(self):
        for version in ["0.11.1", "0.11.0"]:
            self.assertEqual(install.candidate_metadata(ROOT, version)["package"]["file_count"], 6)

if __name__ == "__main__":
    unittest.main()

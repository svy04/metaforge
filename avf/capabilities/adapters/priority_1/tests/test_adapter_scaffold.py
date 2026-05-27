from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from avf.capabilities.adapters.priority_1 import adapter_contracts
from avf.capabilities.adapters.priority_1.evidence_mapping import build_evidence_entries
from avf.capabilities.adapters.priority_1.record_normalizers import normalize_repo_local_fixture
from avf.capabilities.adapters.priority_1.repo_local_validation_harness import (
    load_valid_fixture_map,
    run_repo_local_validation,
    validation_summary,
)


class AdapterScaffoldTests(unittest.TestCase):
    def test_adapter_module_flags_block_protected_actions(self) -> None:
        self.assertFalse(adapter_contracts.CANDIDATE_TOOL_IMPORT_ALLOWED)
        self.assertFalse(adapter_contracts.DEPENDENCY_INSTALL_ALLOWED)
        self.assertFalse(adapter_contracts.EXTERNAL_FETCH_ALLOWED)
        self.assertFalse(adapter_contracts.RUNTIME_INTEGRATION_ALLOWED)
        self.assertTrue(adapter_contracts.PROVIDER_NEUTRAL)
        self.assertTrue(adapter_contracts.DEPENDENCY_FREE)

    def test_normalizes_four_fixture_types(self) -> None:
        fixture_map = load_valid_fixture_map(ROOT)
        normalized = run_repo_local_validation(fixture_map)
        self.assertEqual(4, len(normalized))
        self.assertEqual(
            ["eval_case", "redteam_case", "rag_metric", "governance_gate"],
            [record["normalized_record_type"] for record in normalized],
        )
        self.assertEqual(
            "eval_case",
            normalize_repo_local_fixture("eval-case-contract", fixture_map["eval-case-contract"])["normalized_record_type"],
        )

    def test_evidence_entries_preserve_boundaries(self) -> None:
        normalized = run_repo_local_validation(load_valid_fixture_map(ROOT))
        entries = build_evidence_entries(normalized)
        self.assertEqual(4, len(entries))
        self.assertTrue(all(entry["validation_result"] == "PASS" for entry in entries))
        self.assertTrue(all(entry["candidate_tool_import_allowed"] is False for entry in entries))
        self.assertTrue(all(entry["dependency_install_allowed"] is False for entry in entries))
        self.assertTrue(all(entry["external_fetch_allowed"] is False for entry in entries))
        self.assertTrue(all(entry["runtime_integration_allowed"] is False for entry in entries))

    def test_harness_summary_blocks_external_actions(self) -> None:
        summary = validation_summary(run_repo_local_validation(load_valid_fixture_map(ROOT)))
        self.assertEqual(4, summary["normalized_record_count"])
        self.assertTrue(summary["repo_local_source_only"])
        self.assertEqual(0, summary["candidate_tool_import_allowed_count"])
        self.assertEqual(0, summary["dependency_install_allowed_count"])
        self.assertEqual(0, summary["external_fetch_allowed_count"])
        self.assertEqual(0, summary["runtime_integration_allowed_count"])


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AdapterScaffoldTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print("LOCAL_ADAPTER_SCAFFOLD_TESTS_RESULT=PASS")
        print(f"LOCAL_ADAPTER_SCAFFOLD_TEST_COUNT={suite.countTestCases()}")
        return 0
    print("LOCAL_ADAPTER_SCAFFOLD_TESTS_RESULT=FAIL")
    print(f"LOCAL_ADAPTER_SCAFFOLD_TEST_COUNT={suite.countTestCases()}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

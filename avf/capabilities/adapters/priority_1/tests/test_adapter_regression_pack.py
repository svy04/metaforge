from __future__ import annotations

import json
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
)


INVALID_FIXTURE_URIS = {
    "eval-case-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_eval_case_contract.invalid.fixture.json",
    "redteam-case-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_redteam_case_contract.invalid.fixture.json",
    "rag-metric-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_rag_metric_contract.invalid.fixture.json",
    "governance-gate-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_governance_gate_contract.invalid.fixture.json",
}


def read_fixture(uri: str) -> dict:
    return json.loads((ROOT / uri).read_text(encoding="utf-8"))


class AdapterRegressionPackTests(unittest.TestCase):
    def test_rejects_eval_case_missing_claim_boundary(self) -> None:
        with self.assertRaisesRegex(ValueError, "claim_boundary"):
            normalize_repo_local_fixture("eval-case-contract", read_fixture(INVALID_FIXTURE_URIS["eval-case-contract"]))

    def test_rejects_redteam_case_bad_evidence_basis_type(self) -> None:
        with self.assertRaisesRegex(ValueError, "evidence_basis"):
            normalize_repo_local_fixture("redteam-case-contract", read_fixture(INVALID_FIXTURE_URIS["redteam-case-contract"]))

    def test_rejects_rag_metric_unexpected_runtime_hint(self) -> None:
        with self.assertRaisesRegex(ValueError, "unexpected_runtime_hint"):
            normalize_repo_local_fixture("rag-metric-contract", read_fixture(INVALID_FIXTURE_URIS["rag-metric-contract"]))

    def test_rejects_governance_gate_bad_risk_tier(self) -> None:
        with self.assertRaisesRegex(ValueError, "risk_tier"):
            normalize_repo_local_fixture("governance-gate-contract", read_fixture(INVALID_FIXTURE_URIS["governance-gate-contract"]))

    def test_boundary_flags_remain_false_after_valid_normalization(self) -> None:
        records = run_repo_local_validation(load_valid_fixture_map(ROOT))
        self.assertEqual(4, len(records))
        for record in records:
            self.assertFalse(record["candidate_tool_import_allowed"])
            self.assertFalse(record["dependency_install_allowed"])
            self.assertFalse(record["external_fetch_allowed"])
            self.assertFalse(record["runtime_integration_allowed"])
        self.assertFalse(adapter_contracts.CANDIDATE_TOOL_IMPORT_ALLOWED)
        self.assertFalse(adapter_contracts.DEPENDENCY_INSTALL_ALLOWED)
        self.assertFalse(adapter_contracts.EXTERNAL_FETCH_ALLOWED)
        self.assertFalse(adapter_contracts.RUNTIME_INTEGRATION_ALLOWED)

    def test_evidence_mapping_has_no_action_drift(self) -> None:
        entries = build_evidence_entries(run_repo_local_validation(load_valid_fixture_map(ROOT)))
        self.assertEqual(4, len(entries))
        for entry in entries:
            self.assertEqual("PASS", entry["validation_result"])
            self.assertFalse(entry["candidate_tool_import_allowed"])
            self.assertFalse(entry["dependency_install_allowed"])
            self.assertFalse(entry["external_fetch_allowed"])
            self.assertFalse(entry["runtime_integration_allowed"])


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AdapterRegressionPackTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print("LOCAL_ADAPTER_REGRESSION_PACK_RESULT=PASS")
        print(f"LOCAL_ADAPTER_REGRESSION_TEST_COUNT={suite.countTestCases()}")
        return 0
    print("LOCAL_ADAPTER_REGRESSION_PACK_RESULT=FAIL")
    print(f"LOCAL_ADAPTER_REGRESSION_TEST_COUNT={suite.countTestCases()}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

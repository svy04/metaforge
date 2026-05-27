from __future__ import annotations

import copy
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


VALID_FIXTURE_URIS = {
    "eval-case-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_eval_case_contract.valid.fixture.json",
    "redteam-case-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_redteam_case_contract.valid.fixture.json",
    "rag-metric-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_rag_metric_contract.valid.fixture.json",
    "governance-gate-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_governance_gate_contract.valid.fixture.json",
}


def read_fixture(contract_id: str) -> dict:
    return json.loads((ROOT / VALID_FIXTURE_URIS[contract_id]).read_text(encoding="utf-8"))


class AdapterBehaviorExpansionTests(unittest.TestCase):
    def test_rejects_eval_case_public_claim_boundary(self) -> None:
        record = copy.deepcopy(read_fixture("eval-case-contract"))
        record["claim_boundary"] = "public_release_claim"

        with self.assertRaisesRegex(ValueError, "claim_boundary"):
            normalize_repo_local_fixture("eval-case-contract", record)

    def test_rejects_redteam_case_empty_evidence_basis(self) -> None:
        record = copy.deepcopy(read_fixture("redteam-case-contract"))
        record["evidence_basis"] = []

        with self.assertRaisesRegex(ValueError, "evidence_basis"):
            normalize_repo_local_fixture("redteam-case-contract", record)

    def test_rejects_rag_metric_runtime_positive_boundary(self) -> None:
        record = copy.deepcopy(read_fixture("rag-metric-contract"))
        record["interpretation_boundary"] = "start evaluator runtime now"

        with self.assertRaisesRegex(ValueError, "interpretation_boundary"):
            normalize_repo_local_fixture("rag-metric-contract", record)

    def test_rejects_governance_gate_missing_publish_block(self) -> None:
        record = copy.deepcopy(read_fixture("governance-gate-contract"))
        record["blocked_actions"] = ["dependency_install", "runtime_integration", "deploy"]

        with self.assertRaisesRegex(ValueError, "blocked_actions"):
            normalize_repo_local_fixture("governance-gate-contract", record)

    def test_normalized_records_include_behavior_requirement_trace(self) -> None:
        records = run_repo_local_validation(load_valid_fixture_map(ROOT))
        self.assertEqual(4, len(records))
        for record in records:
            self.assertIn("behavior_requirement_ids", record)
            self.assertIn(record["source_contract_id"], adapter_contracts.BEHAVIOR_REQUIREMENTS_BY_CONTRACT)
            self.assertEqual(
                adapter_contracts.BEHAVIOR_REQUIREMENTS_BY_CONTRACT[record["source_contract_id"]],
                tuple(record["behavior_requirement_ids"]),
            )

    def test_evidence_entries_include_behavior_requirement_trace(self) -> None:
        records = run_repo_local_validation(load_valid_fixture_map(ROOT))
        entries = build_evidence_entries(records)
        self.assertEqual(4, len(entries))
        for entry in entries:
            self.assertIn("source_behavior_requirement_ids", entry)
            self.assertEqual(
                adapter_contracts.BEHAVIOR_REQUIREMENTS_BY_CONTRACT[entry["source_contract_id"]],
                tuple(entry["source_behavior_requirement_ids"]),
            )
            self.assertFalse(entry["candidate_tool_import_allowed"])
            self.assertFalse(entry["dependency_install_allowed"])
            self.assertFalse(entry["external_fetch_allowed"])
            self.assertFalse(entry["runtime_integration_allowed"])


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AdapterBehaviorExpansionTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print("LOCAL_ADAPTER_BEHAVIOR_EXPANSION_RESULT=PASS")
        print(f"LOCAL_ADAPTER_BEHAVIOR_EXPANSION_TEST_COUNT={suite.countTestCases()}")
        return 0
    print("LOCAL_ADAPTER_BEHAVIOR_EXPANSION_RESULT=FAIL")
    print(f"LOCAL_ADAPTER_BEHAVIOR_EXPANSION_TEST_COUNT={suite.countTestCases()}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

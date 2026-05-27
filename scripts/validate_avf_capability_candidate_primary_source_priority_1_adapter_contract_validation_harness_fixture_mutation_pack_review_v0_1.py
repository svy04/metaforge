from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1.py"
MUTATION_PACK_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_gate.json"
MUTATION_PACK_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_PACK_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_runner_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_HARNESS_FIXTURE_MUTATION_PACK_REVIEWED"
REVIEW_STATUS = "adapter_contract_validation_harness_fixture_mutation_pack_validated_ready_for_mutation_runner"

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "hardening_area_count": 5,
    "fixture_mutation_plan_count": 5,
    "mutation_fixture_count": 5,
    "reviewed_mutation_fixture_count": 5,
    "mutation_fixture_expected_invalid_count": 5,
    "mutation_fixture_actual_invalid_count": 5,
    "mutation_fixture_result_matched_expected_count": 5,
    "reviewed_mutation_fixture_result_count": 5,
    "blocked_action_count": 10,
    "reviewed_blocked_action_count": 10,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_contract_validation_harness_fixture_mutation_runner_count": 1,
}

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "automated_scraping_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "runtime_export_performed",
    "collector_started",
    "telemetry_export_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    MUTATION_PACK_GATE,
    MUTATION_PACK_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    REVIEW_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "reviewed_mutation_fixture_count=5",
    "reviewed_mutation_fixture_result_count=5",
    "mutation_fixture_result_matched_expected_count=5",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "provider_neutral=true",
    "dependency_free=true",
    "candidate_tool_import_allowed=false",
    "dependency_install_allowed=false",
    "external_fetch_allowed=false",
    "runtime_integration_allowed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-runner",
    "owner_approval_required_before_execution: false",
    "Create a repo-local mutation runner that executes the reviewed mutation fixtures through the no-install harness boundary",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Pack Review v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_previous_pack() -> dict:
    pack = read_json(MUTATION_PACK_GATE)
    if pack.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("fixture mutation pack gate goal_id mismatch")
    if pack.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("fixture mutation pack gate must point to this review goal")
    if pack.get("ready_for_adapter_contract_validation_harness_fixture_mutation_pack_review_count") != 1:
        fail("fixture mutation pack must be ready for review")
    for key, value in {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "mutation_fixture_result_matched_expected_count": 5,
        "review_blocker_count": 0,
    }.items():
        if pack.get(key) != value:
            fail(f"fixture mutation pack {key} mismatch")
    for uri in pack.get("mutation_fixture_uris", []):
        if not (ROOT / uri).is_file():
            fail(f"fixture mutation file missing: {uri}")
    require_false_flags(pack.get("claim_boundary", {}), "fixture mutation pack claim boundary")
    require_text_markers(
        MUTATION_PACK_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-pack",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return pack


def reviewed_results(pack: dict) -> list[dict]:
    results = []
    for result in pack.get("mutation_fixture_validation_results", []):
        item = {
            **result,
            "review_status": "reviewed_mutation_fixture_invalid_outcome_matches_expected",
            "mutation_fixture_contract_validated": True,
        }
        results.append(item)
    return results


def require_reviewed_result(item: dict, source_by_id: dict[str, dict]) -> None:
    fixture_id = item.get("mutation_fixture_id", "<missing>")
    if fixture_id not in source_by_id:
        fail(f"reviewed mutation fixture result {fixture_id} missing matching source result")
    source = source_by_id[fixture_id]
    for key, value in source.items():
        if item.get(key) != value:
            fail(f"reviewed mutation fixture result {fixture_id} changed source field {key}")
    if item.get("review_status") != "reviewed_mutation_fixture_invalid_outcome_matches_expected":
        fail(f"reviewed mutation fixture result {fixture_id} review_status mismatch")
    if item.get("mutation_fixture_contract_validated") is not True:
        fail(f"reviewed mutation fixture result {fixture_id} contract validation flag mismatch")


def require_review_record(record: dict, label: str, pack: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("mutation_fixture_uris") != pack.get("mutation_fixture_uris"):
        fail(f"{label} mutation fixture uri mismatch")
    if record.get("reviewed_blocked_actions") != pack.get("reviewed_blocked_actions"):
        fail(f"{label} reviewed blocked actions mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("adapter_contract_validation_harness_fixture_mutation_pack_gate") != MUTATION_PACK_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input mutation pack gate uri mismatch")
    source_by_id = {
        item["mutation_fixture_id"]: item
        for item in pack.get("mutation_fixture_validation_results", [])
    }
    reviewed = record.get("reviewed_mutation_fixture_validation_results", [])
    if len(reviewed) != EXPECTED_COUNTS["reviewed_mutation_fixture_result_count"]:
        fail(f"{label} reviewed mutation fixture result count mismatch")
    for item in reviewed:
        require_reviewed_result(item, source_by_id)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(pack: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-fixture-mutation-pack-review-gate-v0-1":
        fail("fixture mutation pack review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("fixture mutation pack review gate status must be PASS")
    require_review_record(gate, "fixture mutation pack review gate", pack)


def require_validation_result(pack: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", pack)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    pack = require_previous_pack()
    require_review_record(read_json(REVIEW_GATE), "fixture mutation pack review", pack)
    require_gate(pack)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(REVIEW_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(pack)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Harness Fixture Mutation Pack Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_fixture_mutation_pack_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("provider_neutral=true")
    print("dependency_free=true")
    print("candidate_tool_import_allowed=false")
    print("dependency_install_allowed=false")
    print("external_fetch_allowed=false")
    print("runtime_integration_allowed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

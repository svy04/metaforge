from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1.py"
FIXTURE_PACK_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_gate.json"
FIXTURE_PACK_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_FIXTURE_PACK_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_plan_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_FIXTURE_PACK_REVIEWED"
REVIEW_STATUS = "adapter_contract_validation_fixture_pack_validated_ready_for_validation_harness_plan"

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "validation_fixture_count": 8,
    "reviewed_validation_fixture_count": 8,
    "passing_fixture_count": 4,
    "failing_fixture_count": 4,
    "fixture_validation_result_matched_expected_count": 8,
    "provider_neutral_fixture_count": 8,
    "dependency_free_fixture_count": 8,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_contract_validation_harness_plan_count": 1,
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
    FIXTURE_PACK_GATE,
    FIXTURE_PACK_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    REVIEW_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "source_schema_artifact_count=4",
    "validation_fixture_count=8",
    "reviewed_validation_fixture_count=8",
    "passing_fixture_count=4",
    "failing_fixture_count=4",
    "fixture_validation_result_matched_expected_count=8",
    "provider_neutral_fixture_count=8",
    "dependency_free_fixture_count=8",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "review_blocker_count=0",
    "ready_for_adapter_contract_validation_harness_plan_count=1",
    "provider_neutral=true",
    "dependency_free=true",
    "candidate_tool_import_allowed=false",
    "dependency_install_allowed=false",
    "runtime_integration_allowed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-validation-harness-plan",
    "owner_approval_required_before_execution: false",
    "Create a repo-local no-install adapter contract validation harness plan",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Fixture Pack Review v0.1 validation")
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


def require_previous_fixture_pack() -> dict:
    fixture_pack = read_json(FIXTURE_PACK_GATE)
    if fixture_pack.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("adapter contract validation fixture pack gate goal_id mismatch")
    if fixture_pack.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("adapter contract validation fixture pack gate must point to this review goal")
    if fixture_pack.get("ready_for_adapter_contract_validation_fixture_pack_review_count") != 1:
        fail("adapter contract validation fixture pack must be ready for review")
    if fixture_pack.get("provider_neutral") is not True:
        fail("adapter contract validation fixture pack must remain provider-neutral")
    if fixture_pack.get("dependency_free") is not True:
        fail("adapter contract validation fixture pack must remain dependency-free")
    if fixture_pack.get("candidate_tool_import_allowed") is not False:
        fail("adapter contract validation fixture pack must not allow candidate tool import")
    if fixture_pack.get("dependency_install_allowed") is not False:
        fail("adapter contract validation fixture pack must not allow dependency install")
    if fixture_pack.get("runtime_integration_allowed") is not False:
        fail("adapter contract validation fixture pack must not allow runtime integration")
    for key, value in {
        "source_schema_artifact_count": 4,
        "validation_fixture_count": 8,
        "passing_fixture_count": 4,
        "failing_fixture_count": 4,
        "fixture_validation_result_matched_expected_count": 8,
        "provider_neutral_fixture_count": 8,
        "dependency_free_fixture_count": 8,
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
    }.items():
        if fixture_pack.get(key) != value:
            fail(f"adapter contract validation fixture pack gate {key} mismatch")
    for fixture in fixture_pack.get("validation_fixtures", []):
        if fixture.get("validation_result_matched_expected") is not True:
            fail(f"fixture {fixture.get('fixture_id')} validation result must match expected")
        if fixture.get("provider_neutral") is not True:
            fail(f"fixture {fixture.get('fixture_id')} must be provider-neutral")
        if fixture.get("dependency_free") is not True:
            fail(f"fixture {fixture.get('fixture_id')} must be dependency-free")
        if fixture.get("candidate_tool_import_allowed") is not False:
            fail(f"fixture {fixture.get('fixture_id')} must not allow candidate tool import")
        if fixture.get("dependency_install_allowed") is not False:
            fail(f"fixture {fixture.get('fixture_id')} must not allow dependency install")
        if fixture.get("runtime_integration_allowed") is not False:
            fail(f"fixture {fixture.get('fixture_id')} must not allow runtime integration")
        fixture_uri = fixture.get("fixture_uri")
        if not fixture_uri or not (ROOT / fixture_uri).is_file():
            fail(f"fixture {fixture.get('fixture_id')} fixture_uri missing")
    require_false_flags(fixture_pack.get("claim_boundary", {}), "adapter contract validation fixture pack claim boundary")
    require_text_markers(
        FIXTURE_PACK_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-fixture-pack",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return fixture_pack


def require_reviewed_fixture(item: dict, source_by_id: dict[str, dict]) -> None:
    fixture_id = item.get("fixture_id", "<missing>")
    if fixture_id not in source_by_id:
        fail(f"reviewed fixture {fixture_id} missing matching source fixture")
    source = source_by_id[fixture_id]
    for key, value in source.items():
        if item.get(key) != value:
            fail(f"reviewed fixture {fixture_id} changed source field {key}")
    if item.get("review_status") != "reviewed_fixture_validation_result_matches_expected":
        fail(f"reviewed fixture {fixture_id} review_status mismatch")
    if item.get("fixture_contract_validated") is not True:
        fail(f"reviewed fixture {fixture_id} fixture_contract_validated must be true")


def require_review_record(record: dict, label: str, fixture_pack: dict) -> None:
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

    input_uris = record.get("input_uris", {})
    if input_uris.get("adapter_contract_validation_fixture_pack_gate") != FIXTURE_PACK_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input fixture pack gate uri mismatch")

    reviewed_fixtures = record.get("reviewed_validation_fixtures", [])
    if len(reviewed_fixtures) != EXPECTED_COUNTS["reviewed_validation_fixture_count"]:
        fail(f"{label} reviewed fixture count mismatch")
    source_by_id = {
        item["fixture_id"]: item
        for item in fixture_pack.get("validation_fixtures", [])
    }
    for item in reviewed_fixtures:
        require_reviewed_fixture(item, source_by_id)

    if record.get("source_schema_artifacts") != fixture_pack.get("source_schema_artifacts"):
        fail(f"{label} source schema artifacts mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(fixture_pack: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-fixture-pack-review-gate-v0-1":
        fail("adapter contract validation fixture pack review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("adapter contract validation fixture pack review gate status must be PASS")
    require_review_record(gate, "adapter contract validation fixture pack review gate", fixture_pack)


def require_validation_result(fixture_pack: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", fixture_pack)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    fixture_pack = require_previous_fixture_pack()
    require_review_record(read_json(REVIEW_GATE), "adapter contract validation fixture pack review", fixture_pack)
    require_gate(fixture_pack)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(REVIEW_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(fixture_pack)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Fixture Pack Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("provider_neutral=true")
    print("dependency_free=true")
    print("candidate_tool_import_allowed=false")
    print("runtime_integration_allowed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

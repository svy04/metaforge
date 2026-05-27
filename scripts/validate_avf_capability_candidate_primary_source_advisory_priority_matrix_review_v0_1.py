from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_advisory_priority_matrix_review_v0_1.py"
PRIORITY_MATRIX = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix.json"
PRIORITY_MATRIX_GATE = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_gate.json"
PRIORITY_MATRIX_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ADVISORY_PRIORITY_MATRIX_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_v0_1"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ADVISORY_PRIORITY_MATRIX_REVIEWED"
REVIEW_STATUS = "advisory_priority_matrix_validated_ready_for_priority_1_deep_research_plan"
MATRIX_STATUS = "advisory_priority_matrix_created_non_executable"
MATRIX_MODEL = "evidence_tier_plus_integration_risk_placeholder_v0_1"

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "priority_matrix_candidate_count": 7,
    "reviewed_priority_item_count": 7,
    "priority_1_candidate_count": 1,
    "priority_2_candidate_count": 5,
    "priority_3_candidate_count": 1,
    "selection_allowed_count": 0,
    "dependency_adoption_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_priority_1_deep_research_plan_count": 1,
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
    PRIORITY_MATRIX,
    PRIORITY_MATRIX_GATE,
    PRIORITY_MATRIX_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_advisory_priority_matrix_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "priority_matrix_scope_confirmed=advisory_non_executable_internal_planning",
    "priority_matrix_not_selection_gate=true",
    "priority_1_deep_research_plan_candidate_count=1",
    "priority_1_candidate_id=cap-eval-redteam-promptfoo-ragas",
    "selection_allowed=false",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-priority-1-deep-research-plan",
    "owner_approval_required_before_execution: false",
    "Create a repo-local deep research plan for the priority 1 candidate",
    "Do not select, adopt, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Advisory Priority Matrix Review v0.1 validation")
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


def require_priority_item(item: dict, label: str) -> None:
    candidate_id = item.get("candidate_id", "<missing>")
    if item.get("matrix_scope") != "advisory_non_executable_internal_planning":
        fail(f"{label} {candidate_id} matrix scope mismatch")
    if item.get("integration_risk_placeholder") != "requires_future_license_security_architecture_review":
        fail(f"{label} {candidate_id} integration risk placeholder mismatch")
    if item.get("priority_matrix_review_required") is not True:
        fail(f"{label} {candidate_id} review required flag mismatch")
    if item.get("selection_allowed") is not False:
        fail(f"{label} {candidate_id} selection must be blocked")
    if item.get("dependency_adoption_allowed") is not False:
        fail(f"{label} {candidate_id} dependency adoption must be blocked")
    if item.get("runtime_integration_allowed") is not False:
        fail(f"{label} {candidate_id} runtime integration must be blocked")
    if item.get("advisory_priority") not in {1, 2, 3}:
        fail(f"{label} {candidate_id} advisory priority mismatch")


def require_previous_inputs() -> tuple[dict, dict]:
    matrix = read_json(PRIORITY_MATRIX)
    gate = read_json(PRIORITY_MATRIX_GATE)
    if matrix.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("priority matrix goal_id mismatch")
    if matrix.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("priority matrix must point to this review goal")
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-advisory-priority-matrix-gate-v0-1":
        fail("priority matrix gate id mismatch")
    if gate.get("status") != "PASS":
        fail("priority matrix gate status must be PASS")
    for record, label in [(matrix, "priority matrix"), (gate, "priority matrix gate")]:
        if record.get("matrix_status") != MATRIX_STATUS:
            fail(f"{label} status mismatch")
        if record.get("matrix_model") != MATRIX_MODEL:
            fail(f"{label} model mismatch")
        if record.get("matrix_scope") != "advisory_non_executable_internal_planning":
            fail(f"{label} scope mismatch")
        if record.get("selection_allowed") is not False:
            fail(f"{label} selection must be blocked")
        if record.get("dependency_adoption_allowed") is not False:
            fail(f"{label} dependency adoption must be blocked")
        if record.get("runtime_integration_allowed") is not False:
            fail(f"{label} runtime integration must be blocked")
        for key in [
            "candidate_count",
            "priority_matrix_candidate_count",
            "priority_1_candidate_count",
            "priority_2_candidate_count",
            "priority_3_candidate_count",
            "selection_allowed_count",
            "dependency_adoption_allowed_count",
            "runtime_integration_allowed_count",
        ]:
            if record.get(key) != EXPECTED_COUNTS[key]:
                fail(f"{label} {key} mismatch")
        for item in record.get("priority_items", []):
            require_priority_item(item, label)
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        PRIORITY_MATRIX_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-advisory-priority-matrix",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return matrix, gate


def require_reviewed_item(item: dict, matrix_by_id: dict[str, dict], label: str) -> None:
    candidate_id = item.get("candidate_id", "<missing>")
    if candidate_id not in matrix_by_id:
        fail(f"{label} unexpected candidate {candidate_id}")
    source = matrix_by_id[candidate_id]
    copied = [
        "evidence_strength_score",
        "evidence_strength_tier",
        "source_count",
        "claim_summary_count",
        "advisory_priority",
        "integration_risk_placeholder",
    ]
    for key in copied:
        if item.get(key) != source.get(key):
            fail(f"{label} {candidate_id} {key} mismatch")
    if item.get("review_status") != "reviewed_advisory_priority_validated":
        fail(f"{label} {candidate_id} review status mismatch")
    expected_deep_plan_required = source.get("advisory_priority") == 1
    if item.get("priority_1_deep_research_plan_required") is not expected_deep_plan_required:
        fail(f"{label} {candidate_id} deep research plan flag mismatch")
    if item.get("selection_allowed") is not False:
        fail(f"{label} {candidate_id} selection must be blocked")
    if item.get("dependency_adoption_allowed") is not False:
        fail(f"{label} {candidate_id} dependency adoption must be blocked")
    if item.get("runtime_integration_allowed") is not False:
        fail(f"{label} {candidate_id} runtime integration must be blocked")


def require_review_record(record: dict, label: str, matrix: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "priority_matrix_scope_confirmed": "advisory_non_executable_internal_planning",
        "priority_matrix_not_selection_gate": True,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("priority_1_candidate_ids") != ["cap-eval-redteam-promptfoo-ragas"]:
        fail(f"{label} priority 1 candidate ids mismatch")
    reviewed = record.get("reviewed_priority_items", [])
    if len(reviewed) != EXPECTED_COUNTS["reviewed_priority_item_count"]:
        fail(f"{label} reviewed item count mismatch")
    matrix_by_id = {item["candidate_id"]: item for item in matrix.get("priority_items", [])}
    for item in reviewed:
        require_reviewed_item(item, matrix_by_id, label)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_review_gate(matrix: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-advisory-priority-matrix-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", matrix)


def require_validation_result(matrix: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_advisory_priority_matrix_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", matrix)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    matrix, _ = require_previous_inputs()
    require_review_gate(matrix)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(matrix)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Advisory Priority Matrix Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_advisory_priority_matrix_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("priority_matrix_scope_confirmed=advisory_non_executable_internal_planning")
    print("priority_matrix_not_selection_gate=true")
    print("priority_1_candidate_id=cap-eval-redteam-promptfoo-ragas")
    print("selection_allowed=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("dependency_install_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

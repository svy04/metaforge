from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_advisory_priority_matrix_v0_1.py"
SCORECARD_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_gate.json"
SCORECARD_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_next_action.yml"
PRIORITY_MATRIX = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix.json"
PRIORITY_MATRIX_GATE = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_gate.json"
PRIORITY_MATRIX_REPORT = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ADVISORY_PRIORITY_MATRIX_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_review_v0_1"
MATRIX_STATUS = "advisory_priority_matrix_created_non_executable"
MATRIX_MODEL = "evidence_tier_plus_integration_risk_placeholder_v0_1"

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "priority_matrix_candidate_count": 7,
    "priority_1_candidate_count": 1,
    "priority_2_candidate_count": 5,
    "priority_3_candidate_count": 1,
    "selection_allowed_count": 0,
    "dependency_adoption_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "ready_for_priority_matrix_review_count": 1,
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
    SCORECARD_REVIEW_GATE,
    SCORECARD_REVIEW_NEXT_ACTION,
    PRIORITY_MATRIX,
    PRIORITY_MATRIX_GATE,
    PRIORITY_MATRIX_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_advisory_priority_matrix_v0_1=true",
    f"matrix_status={MATRIX_STATUS}",
    f"matrix_model={MATRIX_MODEL}",
    "matrix_scope=advisory_non_executable_internal_planning",
    "priority_matrix_candidate_count=7",
    "priority_1_candidate_count=1",
    "priority_2_candidate_count=5",
    "priority_3_candidate_count=1",
    "selection_allowed_count=0",
    "dependency_adoption_allowed_count=0",
    "runtime_integration_allowed_count=0",
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
    "action_id: review-capability-candidate-primary-source-advisory-priority-matrix",
    "owner_approval_required_before_execution: false",
    "Review the advisory priority matrix",
    "Do not select, adopt, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Advisory Priority Matrix v0.1 validation")
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


def priority_for_tier(tier: str) -> int:
    if tier == "strong":
        return 1
    if tier == "moderate":
        return 2
    return 3


def require_previous_input() -> dict:
    review = read_json(SCORECARD_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("scorecard review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("scorecard review gate must point to this matrix goal")
    if review.get("ready_for_advisory_priority_matrix_count") != 1:
        fail("scorecard review gate must be ready for priority matrix")
    if review.get("scorecard_not_selection_gate") is not True:
        fail("scorecard review must confirm non-selection boundary")
    if review.get("dependency_adoption_allowed") is not False:
        fail("scorecard review dependency adoption must remain blocked")
    if review.get("runtime_integration_allowed") is not False:
        fail("scorecard review runtime integration must remain blocked")
    require_false_flags(review.get("claim_boundary", {}), "scorecard review claim boundary")
    require_text_markers(
        SCORECARD_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-advisory-priority-matrix",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_priority_item(item: dict, review_by_id: dict[str, dict], label: str) -> None:
    candidate_id = item.get("candidate_id", "<missing>")
    if candidate_id not in review_by_id:
        fail(f"{label} unexpected candidate {candidate_id}")
    source = review_by_id[candidate_id]
    expected_priority = priority_for_tier(source["evidence_strength_tier"])
    expected = {
        "evidence_strength_score": source["evidence_strength_score"],
        "evidence_strength_tier": source["evidence_strength_tier"],
        "source_count": source["source_count"],
        "claim_summary_count": source["claim_summary_count"],
        "integration_risk_placeholder": "requires_future_license_security_architecture_review",
        "advisory_priority": expected_priority,
        "matrix_scope": "advisory_non_executable_internal_planning",
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "priority_matrix_review_required": True,
    }
    for key, value in expected.items():
        if item.get(key) != value:
            fail(f"{label} {candidate_id} {key} mismatch")


def require_matrix_record(record: dict, label: str, review: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "matrix_status": MATRIX_STATUS,
        "matrix_model": MATRIX_MODEL,
        "matrix_scope": "advisory_non_executable_internal_planning",
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
    if record.get("source_required_candidate_ids") != review.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    items = record.get("priority_items", [])
    if len(items) != EXPECTED_COUNTS["priority_matrix_candidate_count"]:
        fail(f"{label} priority item count mismatch")
    review_by_id = {item["candidate_id"]: item for item in review.get("reviewed_scorecard_candidates", [])}
    priorities = {1: 0, 2: 0, 3: 0}
    for item in items:
        require_priority_item(item, review_by_id, label)
        priorities[item["advisory_priority"]] += 1
    if priorities[1] != EXPECTED_COUNTS["priority_1_candidate_count"]:
        fail(f"{label} priority 1 count mismatch")
    if priorities[2] != EXPECTED_COUNTS["priority_2_candidate_count"]:
        fail(f"{label} priority 2 count mismatch")
    if priorities[3] != EXPECTED_COUNTS["priority_3_candidate_count"]:
        fail(f"{label} priority 3 count mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_priority_matrix(review: dict) -> None:
    matrix = read_json(PRIORITY_MATRIX)
    if matrix.get("matrix_id") != "avf-capability-candidate-primary-source-advisory-priority-matrix-v0-1":
        fail("priority matrix id mismatch")
    require_matrix_record(matrix, "priority matrix", review)


def require_priority_matrix_gate(review: dict) -> None:
    gate = read_json(PRIORITY_MATRIX_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-advisory-priority-matrix-gate-v0-1":
        fail("priority matrix gate id mismatch")
    if gate.get("status") != "PASS":
        fail("priority matrix gate status must be PASS")
    require_matrix_record(gate, "priority matrix gate", review)


def require_validation_result(review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_advisory_priority_matrix_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_matrix_record(result, "validation result", review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review = require_previous_input()
    require_priority_matrix(review)
    require_priority_matrix_gate(review)
    require_text_markers(PRIORITY_MATRIX_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Advisory Priority Matrix v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_advisory_priority_matrix_v0_1=true")
    print(f"matrix_status={MATRIX_STATUS}")
    print(f"matrix_model={MATRIX_MODEL}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("matrix_scope=advisory_non_executable_internal_planning")
    print("selection_allowed=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

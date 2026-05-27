from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1.py"
QUALITY_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_quality_review_gate.json"
QUALITY_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_quality_review_next_action.yml"
RECOMMENDATION = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation.json"
RECOMMENDATION_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_gate.json"
RECOMMENDATION_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_EVIDENCE_BACKED_CAPABILITY_RECOMMENDATION_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_quality_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
RECOMMENDATION_DECISION = "RECOMMEND_CONDITIONAL_NO_INSTALL_ADAPTER_PLANNING"
RECOMMENDATION_STATUS = "evidence_backed_candidate_fit_recommended_without_dependency_adoption"

EXPECTED_COUNTS = {
    "reviewed_evidence_record_count": 7,
    "recommendation_count": 1,
    "candidate_fit_signal_count": 4,
    "required_later_review_count": 2,
    "adoption_authorized_count": 0,
    "dependency_install_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "ready_for_no_install_adapter_plan_count": 1,
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
    QUALITY_REVIEW_GATE,
    QUALITY_REVIEW_NEXT_ACTION,
    RECOMMENDATION,
    RECOMMENDATION_GATE,
    RECOMMENDATION_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"recommendation_decision={RECOMMENDATION_DECISION}",
    f"recommendation_status={RECOMMENDATION_STATUS}",
    "adoption_authorized=false",
    "dependency_install_allowed=false",
    "runtime_integration_allowed=false",
    "reviewed_evidence_record_count=7",
    "recommendation_count=1",
    "candidate_fit_signal_count=4",
    "required_later_review_count=2",
    "adoption_authorized_count=0",
    "ready_for_no_install_adapter_plan_count=1",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "dependency_install_performed=false",
    "runtime_integration_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-priority-1-no-install-adapter-plan",
    "owner_approval_required_before_execution: false",
    "Plan a no-install adapter boundary from the evidence-backed recommendation",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Evidence-Backed Capability Recommendation v0.1 validation")
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


def require_previous_quality_review() -> dict:
    review = read_json(QUALITY_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("quality review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("quality review gate must point to this recommendation goal")
    if review.get("ready_for_evidence_backed_recommendation_count") != 1:
        fail("quality review must be ready for recommendation")
    if review.get("adoption_authorized") is not False:
        fail("quality review must not authorize adoption")
    require_false_flags(review.get("claim_boundary", {}), "quality review claim boundary")
    require_text_markers(
        QUALITY_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-evidence-backed-recommendation",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_recommendation_record(record: dict, label: str, quality_review: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "recommendation_decision": RECOMMENDATION_DECISION,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommended_next_implementation_mode": "no_install_adapter_plan_only",
        "adoption_authorized": False,
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
    if input_uris.get("manual_evidence_quality_review_gate") != QUALITY_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input quality review gate uri mismatch")
    if len(record.get("candidate_fit_signals", [])) != EXPECTED_COUNTS["candidate_fit_signal_count"]:
        fail(f"{label} candidate fit signal count mismatch")
    if len(record.get("required_later_reviews", [])) != EXPECTED_COUNTS["required_later_review_count"]:
        fail(f"{label} required later review count mismatch")
    if len(quality_review.get("reviewed_evidence_records", [])) != record.get("reviewed_evidence_record_count"):
        fail(f"{label} reviewed evidence count mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(quality_review: dict) -> None:
    gate = read_json(RECOMMENDATION_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-evidence-backed-capability-recommendation-gate-v0-1":
        fail("recommendation gate id mismatch")
    if gate.get("status") != "PASS":
        fail("recommendation gate status must be PASS")
    require_recommendation_record(gate, "recommendation gate", quality_review)


def require_validation_result(quality_review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_recommendation_record(result, "validation result", quality_review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    quality_review = require_previous_quality_review()
    recommendation = read_json(RECOMMENDATION)
    require_recommendation_record(recommendation, "recommendation", quality_review)
    require_gate(quality_review)
    require_text_markers(RECOMMENDATION_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(quality_review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Evidence-Backed Capability Recommendation v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"recommendation_decision={RECOMMENDATION_DECISION}")
    print(f"recommendation_status={RECOMMENDATION_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("adoption_authorized=false")
    print("dependency_install_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

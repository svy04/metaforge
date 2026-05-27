from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1.py"
CLAIM_MAP = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map.json"
SCORECARD = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard.json"
SCORECARD_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_gate.json"
SCORECARD_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_STRENGTH_SCORECARD_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_v0_1"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_STRENGTH_SCORECARD_REVIEWED"
REVIEW_STATUS = "advisory_scorecard_validated_ready_for_priority_matrix"
SCORING_MODEL = "advisory_source_kind_diversity_v0_1"

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "scorecard_candidate_count": 7,
    "reviewed_scorecard_candidate_count": 7,
    "source_claim_count": 16,
    "strong_evidence_candidate_count": 1,
    "moderate_evidence_candidate_count": 5,
    "early_evidence_candidate_count": 1,
    "dependency_adopted_score_count": 0,
    "runtime_integrated_score_count": 0,
    "review_blocker_count": 0,
    "ready_for_advisory_priority_matrix_count": 1,
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
    CLAIM_MAP,
    SCORECARD,
    SCORECARD_GATE,
    SCORECARD_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "scorecard_scope_confirmed=advisory_internal_design_evidence_only",
    "scorecard_not_selection_gate=true",
    "ready_for_advisory_priority_matrix_count=1",
    "reviewed_scorecard_candidate_count=7",
    "dependency_adopted_score_count=0",
    "runtime_integrated_score_count=0",
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
    "action_id: create-capability-candidate-primary-source-advisory-priority-matrix",
    "owner_approval_required_before_execution: false",
    "Create an advisory priority matrix from the reviewed scorecard",
    "Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Evidence Strength Scorecard Review v0.1 validation")
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


def require_scorecard_candidate(candidate: dict, label: str) -> None:
    candidate_id = candidate.get("candidate_id", "<missing>")
    if candidate.get("scorecard_scope") != "advisory_internal_design_evidence_only":
        fail(f"{label} {candidate_id} scorecard scope mismatch")
    if candidate.get("dependency_adoption_allowed") is not False:
        fail(f"{label} {candidate_id} dependency adoption must be blocked")
    if candidate.get("runtime_integration_allowed") is not False:
        fail(f"{label} {candidate_id} runtime integration must be blocked")
    if candidate.get("scorecard_review_required") is not True:
        fail(f"{label} {candidate_id} review required flag mismatch")
    if candidate.get("evidence_strength_tier") not in {"strong", "moderate", "early"}:
        fail(f"{label} {candidate_id} tier mismatch")
    if not isinstance(candidate.get("evidence_strength_score"), int):
        fail(f"{label} {candidate_id} score must be int")


def require_previous_inputs() -> tuple[dict, dict]:
    scorecard = read_json(SCORECARD)
    gate = read_json(SCORECARD_GATE)
    if scorecard.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("scorecard goal_id mismatch")
    if scorecard.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("scorecard must point to this review goal")
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-evidence-strength-scorecard-gate-v0-1":
        fail("scorecard gate id mismatch")
    if gate.get("status") != "PASS":
        fail("scorecard gate status must be PASS")
    for record, label in [(scorecard, "scorecard"), (gate, "scorecard gate")]:
        if record.get("scorecard_scope") != "advisory_internal_design_evidence_only":
            fail(f"{label} scope mismatch")
        if record.get("scoring_model") != SCORING_MODEL:
            fail(f"{label} scoring model mismatch")
        if record.get("dependency_adoption_allowed") is not False:
            fail(f"{label} dependency adoption must be blocked")
        if record.get("runtime_integration_allowed") is not False:
            fail(f"{label} runtime integration must be blocked")
        for key, value in EXPECTED_COUNTS.items():
            if key in record and record.get(key) != value:
                fail(f"{label} {key} mismatch")
        for candidate in record.get("candidate_scorecards", []):
            require_scorecard_candidate(candidate, label)
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        SCORECARD_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-evidence-strength-scorecard",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return scorecard, gate


def require_reviewed_candidate(item: dict, score_by_id: dict[str, dict], label: str) -> None:
    candidate_id = item.get("candidate_id", "<missing>")
    if candidate_id not in score_by_id:
        fail(f"{label} unexpected candidate {candidate_id}")
    source = score_by_id[candidate_id]
    copied = [
        "evidence_strength_score",
        "evidence_strength_tier",
        "source_count",
        "claim_summary_count",
    ]
    for key in copied:
        if item.get(key) != source.get(key):
            fail(f"{label} {candidate_id} {key} mismatch")
    if item.get("review_status") != "reviewed_scorecard_validated":
        fail(f"{label} {candidate_id} review status mismatch")
    if item.get("priority_matrix_allowed") is not True:
        fail(f"{label} {candidate_id} priority matrix transition must be allowed")
    if item.get("selection_allowed") is not False:
        fail(f"{label} {candidate_id} selection must be blocked")
    if item.get("dependency_adoption_allowed") is not False:
        fail(f"{label} {candidate_id} dependency adoption must be blocked")
    if item.get("runtime_integration_allowed") is not False:
        fail(f"{label} {candidate_id} runtime integration must be blocked")


def require_review_record(record: dict, label: str, scorecard: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "scorecard_scope_confirmed": "advisory_internal_design_evidence_only",
        "scorecard_not_selection_gate": True,
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
    if record.get("source_required_candidate_ids") != scorecard.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    reviewed = record.get("reviewed_scorecard_candidates", [])
    if len(reviewed) != EXPECTED_COUNTS["reviewed_scorecard_candidate_count"]:
        fail(f"{label} reviewed candidate count mismatch")
    score_by_id = {item["candidate_id"]: item for item in scorecard.get("candidate_scorecards", [])}
    for item in reviewed:
        require_reviewed_candidate(item, score_by_id, label)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_review_gate(scorecard: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-evidence-strength-scorecard-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", scorecard)


def require_validation_result(scorecard: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", scorecard)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    scorecard, _ = require_previous_inputs()
    require_review_gate(scorecard)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(scorecard)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Evidence Strength Scorecard Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("scorecard_scope_confirmed=advisory_internal_design_evidence_only")
    print("scorecard_not_selection_gate=true")
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

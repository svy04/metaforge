from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1.py"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_gate.json"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_next_action.yml"
CAPTURE_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan.json"
CAPTURE_FIELD_SPEC = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_field_spec.json"
CAPTURE_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_gate.json"
CAPTURE_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_SOURCE_EVIDENCE_CAPTURE_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CAPTURE_PLAN_STATUS = "source_evidence_capture_plan_created_non_executable"
CAPTURE_PLAN_SCOPE = "capture_field_schema_and_target_plan_only"

EXPECTED_COUNTS = {
    "source_target_count": 7,
    "capture_field_count": 14,
    "required_capture_field_count": 14,
    "target_capture_plan_count": 7,
    "source_fetch_allowed_count": 0,
    "source_fetch_performed_count": 0,
    "oss_clone_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_capture_plan_review_count": 1,
}

REQUIRED_CAPTURE_FIELDS = {
    "source_target_id",
    "candidate_id",
    "source_kind",
    "source_uri",
    "retrieval_mode",
    "capture_scope",
    "claim_to_extract",
    "exact_locator",
    "evidence_summary",
    "quote_limit_policy",
    "license_or_terms_note",
    "security_or_supply_chain_note",
    "adoption_boundary",
    "capture_status",
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
    REVIEW_GATE,
    REVIEW_NEXT_ACTION,
    CAPTURE_PLAN,
    CAPTURE_FIELD_SPEC,
    CAPTURE_PLAN_GATE,
    CAPTURE_PLAN_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"capture_plan_status={CAPTURE_PLAN_STATUS}",
    f"capture_plan_scope={CAPTURE_PLAN_SCOPE}",
    "source_target_count=7",
    "capture_field_count=14",
    "required_capture_field_count=14",
    "target_capture_plan_count=7",
    "source_fetch_allowed_count=0",
    "source_fetch_performed_count=0",
    "oss_clone_allowed_count=0",
    "dependency_install_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "dependency_install_performed=false",
    "runtime_integration_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-priority-1-source-evidence-capture-plan",
    "owner_approval_required_before_execution: false",
    "Review the repo-local source evidence capture plan",
    "Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Source Evidence Capture Plan v0.1 validation")
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


def require_previous_input() -> dict:
    review = read_json(REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("deep research plan review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("deep research plan review gate must point to this capture plan goal")
    if review.get("ready_for_source_evidence_capture_plan_count") != 1:
        fail("deep research plan review must be ready for capture plan")
    if review.get("deep_research_plan_not_source_fetch_gate") is not True:
        fail("deep research plan review must confirm source-fetch boundary")
    if review.get("external_fetch_performed") is not False:
        fail("review gate external fetch must be false")
    if review.get("dependency_adoption_allowed") is not False:
        fail("review gate dependency adoption must remain blocked")
    if review.get("runtime_integration_allowed") is not False:
        fail("review gate runtime integration must remain blocked")
    require_false_flags(review.get("claim_boundary", {}), "deep research plan review claim boundary")
    require_text_markers(
        REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-source-evidence-capture-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_capture_field(field: dict, label: str) -> None:
    field_name = field.get("field_name", "<missing>")
    if field_name not in REQUIRED_CAPTURE_FIELDS:
        fail(f"{label} unexpected capture field {field_name}")
    if field.get("required") is not True:
        fail(f"{label} {field_name} must be required")
    if not field.get("description"):
        fail(f"{label} {field_name} description required")
    if field.get("capture_boundary") != "planning_only_not_collected":
        fail(f"{label} {field_name} capture boundary mismatch")


def require_target_capture_plan(item: dict, source_by_id: dict[str, dict], label: str) -> None:
    source_target_id = item.get("source_target_id", "<missing>")
    if source_target_id not in source_by_id:
        fail(f"{label} unexpected source target {source_target_id}")
    source = source_by_id[source_target_id]
    for key in ["candidate_id", "source_kind", "source_uri", "inspection_focus"]:
        if item.get(key) != source.get(key):
            fail(f"{label} {source_target_id} {key} mismatch")
    if item.get("retrieval_mode") != "future_owner_approved_manual_or_connector_capture":
        fail(f"{label} {source_target_id} retrieval mode mismatch")
    if item.get("capture_scope") != "claim_boundary_evidence_only":
        fail(f"{label} {source_target_id} capture scope mismatch")
    if item.get("capture_status") != "planned_not_collected":
        fail(f"{label} {source_target_id} capture status mismatch")
    if item.get("source_fetch_allowed") is not False:
        fail(f"{label} {source_target_id} source fetch must be blocked")
    if item.get("external_fetch_performed") is not False:
        fail(f"{label} {source_target_id} external fetch must be false")
    if item.get("oss_clone_allowed") is not False:
        fail(f"{label} {source_target_id} clone must be blocked")
    if item.get("dependency_install_allowed") is not False:
        fail(f"{label} {source_target_id} dependency install must be blocked")
    if item.get("runtime_integration_allowed") is not False:
        fail(f"{label} {source_target_id} runtime integration must be blocked")


def require_capture_record(record: dict, label: str, review: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "capture_plan_status": CAPTURE_PLAN_STATUS,
        "capture_plan_scope": CAPTURE_PLAN_SCOPE,
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
    fields = record.get("capture_fields", [])
    if len(fields) != EXPECTED_COUNTS["capture_field_count"]:
        fail(f"{label} capture field count mismatch")
    seen_fields = set()
    for field in fields:
        require_capture_field(field, label)
        seen_fields.add(field["field_name"])
    if seen_fields != REQUIRED_CAPTURE_FIELDS:
        fail(f"{label} capture field set mismatch")
    source_by_id = {target["source_target_id"]: target for target in review.get("reviewed_source_targets", [])}
    plans = record.get("target_capture_plans", [])
    if len(plans) != EXPECTED_COUNTS["target_capture_plan_count"]:
        fail(f"{label} target capture plan count mismatch")
    for item in plans:
        require_target_capture_plan(item, source_by_id, label)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_field_spec(review: dict) -> None:
    spec = read_json(CAPTURE_FIELD_SPEC)
    require_capture_record(spec, "capture field spec", review)


def require_plan_gate(review: dict) -> None:
    gate = read_json(CAPTURE_PLAN_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-source-evidence-capture-plan-gate-v0-1":
        fail("capture plan gate id mismatch")
    if gate.get("status") != "PASS":
        fail("capture plan gate status must be PASS")
    require_capture_record(gate, "capture plan gate", review)


def require_validation_result(review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_capture_record(result, "validation result", review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review = require_previous_input()
    plan = read_json(CAPTURE_PLAN)
    require_capture_record(plan, "capture plan", review)
    require_field_spec(review)
    require_plan_gate(review)
    require_text_markers(CAPTURE_PLAN_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Source Evidence Capture Plan v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"capture_plan_status={CAPTURE_PLAN_STATUS}")
    print(f"capture_plan_scope={CAPTURE_PLAN_SCOPE}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

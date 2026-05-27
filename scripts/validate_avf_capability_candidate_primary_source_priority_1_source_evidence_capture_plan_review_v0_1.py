from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1.py"
CAPTURE_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan.json"
CAPTURE_FIELD_SPEC = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_field_spec.json"
CAPTURE_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_gate.json"
CAPTURE_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_SOURCE_EVIDENCE_CAPTURE_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_SOURCE_EVIDENCE_CAPTURE_PLAN_REVIEWED"
REVIEW_STATUS = "source_evidence_capture_plan_validated_ready_for_manual_evidence_workspace"
CAPTURE_PLAN_SCOPE = "capture_field_schema_and_target_plan_only"

EXPECTED_COUNTS = {
    "source_target_count": 7,
    "capture_field_count": 14,
    "reviewed_capture_field_count": 14,
    "target_capture_plan_count": 7,
    "reviewed_target_capture_plan_count": 7,
    "planned_not_collected_target_count": 7,
    "source_fetch_allowed_count": 0,
    "source_fetch_performed_count": 0,
    "oss_clone_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "review_blocker_count": 0,
    "ready_for_manual_evidence_workspace_count": 1,
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
    CAPTURE_PLAN,
    CAPTURE_FIELD_SPEC,
    CAPTURE_PLAN_GATE,
    CAPTURE_PLAN_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    f"capture_plan_scope_confirmed={CAPTURE_PLAN_SCOPE}",
    "capture_plan_not_evidence_collection_gate=true",
    "capture_field_count=14",
    "reviewed_capture_field_count=14",
    "target_capture_plan_count=7",
    "reviewed_target_capture_plan_count=7",
    "planned_not_collected_target_count=7",
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
    "action_id: create-capability-candidate-primary-source-priority-1-manual-evidence-workspace",
    "owner_approval_required_before_execution: false",
    "Create a repo-local manual evidence workspace",
    "Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Source Evidence Capture Plan Review v0.1 validation")
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


def require_capture_field(field: dict, label: str) -> None:
    field_name = field.get("field_name", "<missing>")
    if field.get("required") is not True:
        fail(f"{label} {field_name} must be required")
    if field.get("capture_boundary") != "planning_only_not_collected":
        fail(f"{label} {field_name} boundary mismatch")
    if not field.get("description"):
        fail(f"{label} {field_name} description required")


def require_target_plan(item: dict, label: str) -> None:
    target_id = item.get("source_target_id", "<missing>")
    if item.get("candidate_id") != CANDIDATE_ID:
        fail(f"{label} {target_id} candidate mismatch")
    if item.get("retrieval_mode") != "future_owner_approved_manual_or_connector_capture":
        fail(f"{label} {target_id} retrieval mode mismatch")
    if item.get("capture_scope") != "claim_boundary_evidence_only":
        fail(f"{label} {target_id} capture scope mismatch")
    if item.get("capture_status") != "planned_not_collected":
        fail(f"{label} {target_id} capture status mismatch")
    if item.get("adoption_boundary") != "evidence_capture_is_not_selection_or_dependency_adoption":
        fail(f"{label} {target_id} adoption boundary mismatch")
    if item.get("source_fetch_allowed") is not False:
        fail(f"{label} {target_id} source fetch must be blocked")
    if item.get("external_fetch_performed") is not False:
        fail(f"{label} {target_id} external fetch must be false")
    if item.get("oss_clone_allowed") is not False:
        fail(f"{label} {target_id} oss clone must be blocked")
    if item.get("dependency_install_allowed") is not False:
        fail(f"{label} {target_id} dependency install must be blocked")
    if item.get("runtime_integration_allowed") is not False:
        fail(f"{label} {target_id} runtime integration must be blocked")


def require_previous_input() -> dict:
    plan = read_json(CAPTURE_PLAN)
    field_spec = read_json(CAPTURE_FIELD_SPEC)
    gate = read_json(CAPTURE_PLAN_GATE)
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("capture plan goal_id mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("capture plan must point to this review goal")
    if gate.get("status") != "PASS":
        fail("capture plan gate status must be PASS")
    for record, label in [(plan, "capture plan"), (field_spec, "capture field spec"), (gate, "capture plan gate")]:
        if record.get("candidate_id") != CANDIDATE_ID:
            fail(f"{label} candidate mismatch")
        if record.get("capture_plan_scope") != CAPTURE_PLAN_SCOPE:
            fail(f"{label} scope mismatch")
        for key in [
            "source_target_count",
            "capture_field_count",
            "target_capture_plan_count",
            "source_fetch_allowed_count",
            "source_fetch_performed_count",
            "oss_clone_allowed_count",
            "dependency_install_allowed_count",
            "runtime_integration_allowed_count",
        ]:
            if record.get(key) != EXPECTED_COUNTS[key]:
                fail(f"{label} {key} mismatch")
        if record.get("external_fetch_performed") is not False:
            fail(f"{label} external fetch must be false")
        if record.get("oss_clone_performed") is not False:
            fail(f"{label} oss clone must be false")
        if record.get("dependency_install_performed") is not False:
            fail(f"{label} dependency install must be false")
        if record.get("runtime_integration_performed") is not False:
            fail(f"{label} runtime integration must be false")
        for field in record.get("capture_fields", []):
            require_capture_field(field, label)
        for item in record.get("target_capture_plans", []):
            require_target_plan(item, label)
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        CAPTURE_PLAN_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-source-evidence-capture-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return plan


def require_reviewed_field(field: dict, field_by_name: dict[str, dict], label: str) -> None:
    field_name = field.get("field_name", "<missing>")
    if field_name not in field_by_name:
        fail(f"{label} unexpected reviewed field {field_name}")
    source = field_by_name[field_name]
    for key in ["required", "description", "capture_boundary"]:
        if field.get(key) != source.get(key):
            fail(f"{label} {field_name} {key} mismatch")
    if field.get("review_status") != "reviewed_capture_field_validated":
        fail(f"{label} {field_name} review status mismatch")


def require_reviewed_target(item: dict, plan_by_id: dict[str, dict], label: str) -> None:
    target_id = item.get("source_target_id", "<missing>")
    if target_id not in plan_by_id:
        fail(f"{label} unexpected reviewed target {target_id}")
    source = plan_by_id[target_id]
    for key in ["candidate_id", "source_kind", "source_uri", "capture_scope", "claim_to_extract", "capture_status"]:
        if item.get(key) != source.get(key):
            fail(f"{label} {target_id} {key} mismatch")
    if item.get("review_status") != "reviewed_target_capture_plan_validated":
        fail(f"{label} {target_id} review status mismatch")
    require_target_plan(item, label)


def require_review_record(record: dict, label: str, plan: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "capture_plan_scope_confirmed": CAPTURE_PLAN_SCOPE,
        "capture_plan_not_evidence_collection_gate": True,
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
    fields = record.get("reviewed_capture_fields", [])
    if len(fields) != EXPECTED_COUNTS["reviewed_capture_field_count"]:
        fail(f"{label} reviewed capture field count mismatch")
    field_by_name = {field["field_name"]: field for field in plan.get("capture_fields", [])}
    for field in fields:
        require_reviewed_field(field, field_by_name, label)
    reviewed_targets = record.get("reviewed_target_capture_plans", [])
    if len(reviewed_targets) != EXPECTED_COUNTS["reviewed_target_capture_plan_count"]:
        fail(f"{label} reviewed target count mismatch")
    plan_by_id = {item["source_target_id"]: item for item in plan.get("target_capture_plans", [])}
    for item in reviewed_targets:
        require_reviewed_target(item, plan_by_id, label)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_review_gate(plan: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-source-evidence-capture-plan-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", plan)


def require_validation_result(plan: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", plan)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    plan = require_previous_input()
    require_review_gate(plan)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(plan)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Source Evidence Capture Plan Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("capture_plan_not_evidence_collection_gate=true")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

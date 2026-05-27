from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1.py"
CAPTURE_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_gate.json"
CAPTURE_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_next_action.yml"
WORKSPACE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace.json"
RECORD_TEMPLATES = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_record_templates.json"
WORKSPACE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_gate.json"
WORKSPACE_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_MANUAL_EVIDENCE_WORKSPACE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
WORKSPACE_STATUS = "manual_evidence_workspace_created_empty_templates_only"
WORKSPACE_SCOPE = "repo_local_empty_evidence_templates_only"

EXPECTED_COUNTS = {
    "source_target_count": 7,
    "evidence_record_template_count": 7,
    "required_capture_field_count": 14,
    "empty_template_count": 7,
    "filled_evidence_record_count": 0,
    "source_fetch_performed_count": 0,
    "oss_clone_performed_count": 0,
    "dependency_install_performed_count": 0,
    "runtime_integration_performed_count": 0,
    "review_blocker_count": 0,
    "ready_for_manual_workspace_review_count": 1,
}

EMPTY_FIELDS = [
    "exact_locator",
    "evidence_summary",
    "license_or_terms_note",
    "security_or_supply_chain_note",
]

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
    CAPTURE_REVIEW_GATE,
    CAPTURE_REVIEW_NEXT_ACTION,
    WORKSPACE,
    RECORD_TEMPLATES,
    WORKSPACE_GATE,
    WORKSPACE_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"workspace_status={WORKSPACE_STATUS}",
    f"workspace_scope={WORKSPACE_SCOPE}",
    "evidence_record_template_count=7",
    "empty_template_count=7",
    "filled_evidence_record_count=0",
    "source_fetch_performed_count=0",
    "oss_clone_performed_count=0",
    "dependency_install_performed_count=0",
    "runtime_integration_performed_count=0",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "dependency_install_performed=false",
    "runtime_integration_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-priority-1-manual-evidence-workspace",
    "owner_approval_required_before_execution: false",
    "Review the repo-local manual evidence workspace",
    "Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Manual Evidence Workspace v0.1 validation")
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
    review = read_json(CAPTURE_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("capture plan review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("capture plan review gate must point to this workspace goal")
    if review.get("ready_for_manual_evidence_workspace_count") != 1:
        fail("capture plan review must be ready for manual evidence workspace")
    if review.get("capture_plan_not_evidence_collection_gate") is not True:
        fail("capture plan review must confirm non-collection boundary")
    if review.get("external_fetch_performed") is not False:
        fail("capture plan review external fetch must be false")
    require_false_flags(review.get("claim_boundary", {}), "capture plan review claim boundary")
    require_text_markers(
        CAPTURE_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-manual-evidence-workspace",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_template(item: dict, source_by_id: dict[str, dict], label: str) -> None:
    template_id = item.get("evidence_record_template_id", "<missing>")
    source_target_id = item.get("source_target_id", "<missing>")
    if source_target_id not in source_by_id:
        fail(f"{label} {template_id} unexpected source target")
    source = source_by_id[source_target_id]
    for key in ["candidate_id", "source_kind", "source_uri", "claim_to_extract", "capture_scope", "adoption_boundary"]:
        if item.get(key) != source.get(key):
            fail(f"{label} {template_id} {key} mismatch")
    if item.get("capture_status") != "empty_template_not_collected":
        fail(f"{label} {template_id} capture status mismatch")
    for field_name in EMPTY_FIELDS:
        if item.get(field_name) != "":
            fail(f"{label} {template_id} {field_name} must be empty")
    if item.get("source_fetch_performed") is not False:
        fail(f"{label} {template_id} source fetch must be false")
    if item.get("external_fetch_performed") is not False:
        fail(f"{label} {template_id} external fetch must be false")
    if item.get("oss_clone_performed") is not False:
        fail(f"{label} {template_id} oss clone must be false")
    if item.get("dependency_install_performed") is not False:
        fail(f"{label} {template_id} dependency install must be false")
    if item.get("runtime_integration_performed") is not False:
        fail(f"{label} {template_id} runtime integration must be false")


def require_workspace_record(record: dict, label: str, review: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "workspace_status": WORKSPACE_STATUS,
        "workspace_scope": WORKSPACE_SCOPE,
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
    templates = record.get("evidence_record_templates", [])
    if len(templates) != EXPECTED_COUNTS["evidence_record_template_count"]:
        fail(f"{label} template count mismatch")
    source_by_id = {item["source_target_id"]: item for item in review.get("reviewed_target_capture_plans", [])}
    for item in templates:
        require_template(item, source_by_id, label)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_workspace_gate(review: dict) -> None:
    gate = read_json(WORKSPACE_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-manual-evidence-workspace-gate-v0-1":
        fail("workspace gate id mismatch")
    if gate.get("status") != "PASS":
        fail("workspace gate status must be PASS")
    require_workspace_record(gate, "workspace gate", review)


def require_validation_result(review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_workspace_record(result, "validation result", review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review = require_previous_input()
    workspace = read_json(WORKSPACE)
    require_workspace_record(workspace, "manual evidence workspace", review)
    templates = read_json(RECORD_TEMPLATES)
    require_workspace_record(templates, "record templates", review)
    require_workspace_gate(review)
    require_text_markers(WORKSPACE_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Manual Evidence Workspace v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"workspace_status={WORKSPACE_STATUS}")
    print(f"workspace_scope={WORKSPACE_SCOPE}")
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

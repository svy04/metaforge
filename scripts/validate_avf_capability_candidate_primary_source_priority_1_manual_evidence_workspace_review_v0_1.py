from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1.py"
WORKSPACE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace.json"
RECORD_TEMPLATES = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_record_templates.json"
WORKSPACE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_gate.json"
WORKSPACE_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_next_action.yml"
WORKSPACE_VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1.validation_result.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_MANUAL_EVIDENCE_WORKSPACE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_MANUAL_EVIDENCE_WORKSPACE_REVIEWED"
REVIEW_STATUS = "manual_evidence_workspace_validated_ready_for_evidence_collection_authorization_packet"
WORKSPACE_SCOPE = "repo_local_empty_evidence_templates_only"

EXPECTED_COUNTS = {
    "source_target_count": 7,
    "evidence_record_template_count": 7,
    "reviewed_evidence_record_template_count": 7,
    "empty_template_count": 7,
    "filled_evidence_record_count": 0,
    "source_fetch_performed_count": 0,
    "oss_clone_performed_count": 0,
    "dependency_install_performed_count": 0,
    "runtime_integration_performed_count": 0,
    "review_blocker_count": 0,
    "ready_for_evidence_collection_authorization_packet_count": 1,
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
    WORKSPACE,
    RECORD_TEMPLATES,
    WORKSPACE_GATE,
    WORKSPACE_NEXT_ACTION,
    WORKSPACE_VALIDATION_RESULT,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "manual_workspace_not_evidence_collection_gate=true",
    "source_target_count=7",
    "evidence_record_template_count=7",
    "reviewed_evidence_record_template_count=7",
    "empty_template_count=7",
    "filled_evidence_record_count=0",
    "source_fetch_performed_count=0",
    "oss_clone_performed_count=0",
    "dependency_install_performed_count=0",
    "runtime_integration_performed_count=0",
    "ready_for_evidence_collection_authorization_packet_count=1",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "dependency_install_performed=false",
    "runtime_integration_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-priority-1-evidence-collection-authorization-packet",
    "owner_approval_required_before_execution: false",
    "Create an owner authorization packet for primary-source evidence collection",
    "Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Manual Evidence Workspace Review v0.1 validation")
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


def require_empty_template(item: dict, label: str) -> None:
    template_id = item.get("evidence_record_template_id", "<missing>")
    if item.get("capture_status") != "empty_template_not_collected":
        fail(f"{label} {template_id} capture_status mismatch")
    for field_name in EMPTY_FIELDS:
        if item.get(field_name) != "":
            fail(f"{label} {template_id} {field_name} must be empty")
    for flag in [
        "source_fetch_performed",
        "external_fetch_performed",
        "oss_clone_performed",
        "dependency_install_performed",
        "runtime_integration_performed",
    ]:
        if item.get(flag) is not False:
            fail(f"{label} {template_id} {flag} must be false")


def require_previous_workspace() -> dict:
    workspace = read_json(WORKSPACE)
    if workspace.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("manual evidence workspace goal_id mismatch")
    if workspace.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("manual evidence workspace must point to this review goal")
    if workspace.get("workspace_scope") != WORKSPACE_SCOPE:
        fail("manual evidence workspace scope mismatch")
    if workspace.get("filled_evidence_record_count") != 0:
        fail("manual evidence workspace must have no filled evidence records")
    if workspace.get("empty_template_count") != EXPECTED_COUNTS["empty_template_count"]:
        fail("manual evidence workspace empty template count mismatch")
    require_false_flags(workspace.get("claim_boundary", {}), "manual evidence workspace claim boundary")
    for item in workspace.get("evidence_record_templates", []):
        require_empty_template(item, "manual evidence workspace")

    record_templates = read_json(RECORD_TEMPLATES)
    if record_templates != workspace:
        fail("record templates file must match manual evidence workspace")

    gate = read_json(WORKSPACE_GATE)
    if gate.get("status") != "PASS":
        fail("manual evidence workspace gate must be PASS")

    validation_result = read_json(WORKSPACE_VALIDATION_RESULT)
    if validation_result.get("status") != "PASS":
        fail("manual evidence workspace validation result must be PASS")

    require_text_markers(
        WORKSPACE_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-manual-evidence-workspace",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return workspace


def require_reviewed_template(item: dict, template_by_id: dict[str, dict]) -> None:
    template_id = item.get("evidence_record_template_id", "<missing>")
    if template_id not in template_by_id:
        fail(f"reviewed template {template_id} missing matching input template")
    template = template_by_id[template_id]
    for key, value in template.items():
        if item.get(key) != value:
            fail(f"reviewed template {template_id} changed input field {key}")
    if item.get("review_status") != "reviewed_empty_evidence_template_validated":
        fail(f"reviewed template {template_id} review_status mismatch")
    require_empty_template(item, "reviewed template")


def require_review_record(record: dict, label: str, workspace: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "workspace_scope_confirmed": WORKSPACE_SCOPE,
        "manual_workspace_not_evidence_collection_gate": True,
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
    if input_uris.get("manual_evidence_workspace") != WORKSPACE.relative_to(ROOT).as_posix():
        fail(f"{label} input manual evidence workspace uri mismatch")
    if input_uris.get("manual_evidence_record_templates") != RECORD_TEMPLATES.relative_to(ROOT).as_posix():
        fail(f"{label} input record templates uri mismatch")

    reviewed = record.get("reviewed_evidence_record_templates", [])
    if len(reviewed) != EXPECTED_COUNTS["reviewed_evidence_record_template_count"]:
        fail(f"{label} reviewed evidence template count mismatch")
    template_by_id = {
        item["evidence_record_template_id"]: item
        for item in workspace.get("evidence_record_templates", [])
    }
    for item in reviewed:
        require_reviewed_template(item, template_by_id)

    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_review_gate(workspace: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-manual-evidence-workspace-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", workspace)


def require_validation_result(workspace: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", workspace)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    workspace = require_previous_workspace()
    require_review_gate(workspace)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(workspace)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Manual Evidence Workspace Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("manual_workspace_not_evidence_collection_gate=true")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

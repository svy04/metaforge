from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_v0_1.py"
COMPLETION_GUIDE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_gate.json"
COMPLETION_GUIDE_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_next_action.yml"
TEMPLATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template.yml"
TEMPLATE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_gate.json"
TEMPLATE_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_RUNTIME_INTEGRATION_OWNER_FILLED_AUTHORIZATION_PACKET_TEMPLATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
TEMPLATE_DECISION = "OWNER_FILLED_AUTHORIZATION_PACKET_TEMPLATE_READY_UNFILLED_RUNTIME_ACTIONS_BLOCKED"
TEMPLATE_STATUS = "template_unfilled_authorization_not_granted"

AUTHORIZATION_FIELDS = [
    "authorization_statement",
    "authorized_by",
    "authorized_at",
    "authorization_expires_at",
    "authorized_actions",
    "scope_boundaries",
    "sandbox_plan_uri",
    "license_review_uri",
    "security_review_uri",
    "rollback_plan_uri",
    "revocation_note",
]

EXPECTED_COUNTS = {
    "runtime_preflight_check_count": 8,
    "authorization_item_count": 6,
    "required_authorization_field_count": 11,
    "authorization_field_completed_count": 0,
    "owner_filled_authorization_item_template_count": 6,
    "owner_filled_authorization_item_completed_count": 0,
    "authorization_item_not_granted_count": 6,
    "protected_action_required_count": 6,
    "owner_input_required_count": 1,
    "sandbox_plan_required_count": 1,
    "license_review_required_count": 1,
    "security_review_required_count": 1,
    "runtime_integration_allowed_count": 0,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "action_allowed_count": 0,
    "template_blocker_count": 0,
    "ready_for_runtime_integration_owner_filled_authorization_packet_template_review_count": 1,
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
    COMPLETION_GUIDE_GATE,
    COMPLETION_GUIDE_NEXT_ACTION,
    TEMPLATE,
    TEMPLATE_GATE,
    TEMPLATE_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEMPLATE_MARKERS = [
    "packet_id: avf-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-filled-authorization-packet-template-v0-1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"template_decision: {TEMPLATE_DECISION}",
    f"template_status: {TEMPLATE_STATUS}",
    "authorization_packet_completed: false",
    "owner_authorization_granted: false",
    "authorization_statement:",
    "authorized_by:",
    "authorized_at:",
    "authorization_expires_at:",
    "authorized_actions: []",
    "scope_boundaries: []",
    "sandbox_plan_uri:",
    "license_review_uri:",
    "security_review_uri:",
    "rollback_plan_uri:",
    "revocation_note:",
    "decision: unfilled",
    "authorization_status: not_granted",
    "action_allowed: false",
    "protected_action_required: true",
    "No candidate tool import",
    "No dependency install",
    "No external fetch",
    "No runtime integration",
    "No runtime export",
    "No external service call",
    "No deploy",
    "No publish",
    "No release readiness claim",
    "No production readiness claim",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_v0_1=true",
    "owner_filled_authorization_packet_template_created=true",
    "owner_filled_authorization_packet_template_gate_created=true",
    f"candidate_id={CANDIDATE_ID}",
    f"template_decision={TEMPLATE_DECISION}",
    f"template_status={TEMPLATE_STATUS}",
    "authorization_packet_completed=false",
    "owner_authorization_granted=false",
    "runtime_preflight_check_count=8",
    "authorization_item_count=6",
    "required_authorization_field_count=11",
    "authorization_field_completed_count=0",
    "owner_filled_authorization_item_template_count=6",
    "owner_filled_authorization_item_completed_count=0",
    "authorization_item_not_granted_count=6",
    "protected_action_required_count=6",
    "owner_input_required_count=1",
    "sandbox_plan_required_count=1",
    "license_review_required_count=1",
    "security_review_required_count=1",
    "runtime_integration_allowed_count=0",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "action_allowed_count=0",
    "template_blocker_count=0",
    "ready_for_runtime_integration_owner_filled_authorization_packet_template_review_count=1",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-filled-authorization-packet-template",
    "owner_approval_required_before_execution: false",
    "Review the unfilled owner-filled authorization packet template before accepting any owner authorization",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Owner-Filled Authorization Packet Template v0.1 validation")
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


def require_completion_guide_gate() -> dict:
    gate = read_json(COMPLETION_GUIDE_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("completion guide gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("completion guide gate must point to this template goal")
    if gate.get("ready_for_runtime_integration_owner_filled_authorization_packet_template_count") != 1:
        fail("completion guide gate must be ready for owner-filled template")
    for key, value in {
        "candidate_id": CANDIDATE_ID,
        "owner_authorization_granted": False,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "completion_guide_blocker_count": 0,
    }.items():
        if gate.get(key) != value:
            fail(f"completion guide gate {key} mismatch")
    if gate.get("required_authorization_fields") != AUTHORIZATION_FIELDS:
        fail("completion guide required authorization fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "completion guide gate claim boundary")
    require_text_markers(
        COMPLETION_GUIDE_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-filled-authorization-packet-template",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_template_item(item: dict) -> None:
    item_id = item.get("authorization_item_id", "<missing>")
    expected = {
        "decision": "unfilled",
        "authorization_status": "not_granted",
        "protected_action_required": True,
        "action_allowed": False,
        "owner_authorization_granted": False,
    }
    for key, value in expected.items():
        if item.get(key) != value:
            fail(f"template item {item_id} {key} mismatch")
    for key in AUTHORIZATION_FIELDS:
        value = item.get(key)
        if key in ["authorized_actions", "scope_boundaries"]:
            if value != []:
                fail(f"template item {item_id} {key} must be empty list")
        elif value != "":
            fail(f"template item {item_id} {key} must be empty")


def require_template_record(record: dict, label: str, source: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "template_decision": TEMPLATE_DECISION,
        "template_status": TEMPLATE_STATUS,
        "authorization_packet_completed": False,
        "owner_authorization_granted": False,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "runtime_integration_performed": False,
        "runtime_export_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("adapter_runtime_integration_owner_input_completion_guide_gate") != COMPLETION_GUIDE_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} completion guide gate input uri mismatch")
    if record.get("required_authorization_fields") != AUTHORIZATION_FIELDS:
        fail(f"{label} required authorization fields mismatch")
    if record.get("source_reviewed_owner_input_authorization_items") != source.get("source_reviewed_owner_input_authorization_items"):
        fail(f"{label} source reviewed owner input items mismatch")
    items = record.get("owner_filled_authorization_item_templates", [])
    if len(items) != EXPECTED_COUNTS["owner_filled_authorization_item_template_count"]:
        fail(f"{label} template item count mismatch")
    for item in items:
        require_template_item(item)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(source: dict) -> None:
    gate = read_json(TEMPLATE_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-filled-authorization-packet-template-gate-v0-1":
        fail("template gate id mismatch")
    if gate.get("status") != "PASS":
        fail("template gate status must be PASS")
    require_template_record(gate, "template gate", source)


def require_validation_result(source: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_template_record(result, "validation result", source)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    source = require_completion_guide_gate()
    require_text_markers(TEMPLATE, TEMPLATE_MARKERS)
    require_gate(source)
    require_text_markers(TEMPLATE_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(source)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Owner-Filled Authorization Packet Template v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_v0_1=true")
    print("owner_filled_authorization_packet_template_created=true")
    print("owner_filled_authorization_packet_template_gate_created=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"template_decision={TEMPLATE_DECISION}")
    print(f"template_status={TEMPLATE_STATUS}")
    print("authorization_packet_completed=false")
    print("owner_authorization_granted=false")
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

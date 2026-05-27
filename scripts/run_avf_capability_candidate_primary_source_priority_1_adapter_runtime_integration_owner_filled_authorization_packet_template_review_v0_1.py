from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

TEMPLATE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_RUNTIME_INTEGRATION_OWNER_FILLED_AUTHORIZATION_PACKET_TEMPLATE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_supplied_authorization_packet_template_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_RUNTIME_INTEGRATION_OWNER_FILLED_AUTHORIZATION_PACKET_TEMPLATE_REVIEWED"
REVIEW_STATUS = "owner_filled_authorization_template_reviewed_unfilled_authorization_not_granted"

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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def false_boundary() -> dict:
    return {
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "automated_scraping_performed": False,
        "scraping_performed": False,
        "posting_automation_performed": False,
        "dependency_install_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "package_install_performed": False,
        "runtime_integration_performed": False,
        "runtime_export_performed": False,
        "collector_started": False,
        "telemetry_export_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_template_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("template gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("template gate must point to this review goal")
    if gate.get("ready_for_runtime_integration_owner_filled_authorization_packet_template_review_count") != 1:
        raise SystemExit("template gate must be ready for review")
    if gate.get("authorization_packet_completed") is not False:
        raise SystemExit("authorization packet template must remain incomplete")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("owner authorization must remain not granted")
    if gate.get("required_authorization_fields") != AUTHORIZATION_FIELDS:
        raise SystemExit("template gate required authorization fields mismatch")
    for key in [
        "candidate_tool_import_allowed",
        "dependency_install_allowed",
        "external_fetch_allowed",
        "runtime_integration_allowed",
        "runtime_integration_performed",
        "runtime_export_performed",
        "external_fetch_performed",
        "oss_clone_performed",
        "dependency_install_performed",
    ]:
        if gate.get(key) is not False:
            raise SystemExit(f"template gate {key} must be false")


def reviewed_template_items(gate: dict) -> list[dict]:
    return [
        {
            **item,
            "review_status": "reviewed_owner_filled_template_item_remains_unfilled_not_granted",
        }
        for item in gate["owner_filled_authorization_item_templates"]
    ]


def counts(gate: dict) -> dict:
    return {
        "runtime_preflight_check_count": gate["runtime_preflight_check_count"],
        "authorization_item_count": gate["authorization_item_count"],
        "required_authorization_field_count": gate["required_authorization_field_count"],
        "authorization_field_completed_count": gate["authorization_field_completed_count"],
        "owner_filled_authorization_item_template_count": gate["owner_filled_authorization_item_template_count"],
        "reviewed_owner_filled_authorization_item_template_count": len(reviewed_template_items(gate)),
        "owner_filled_authorization_item_completed_count": gate["owner_filled_authorization_item_completed_count"],
        "authorization_item_not_granted_count": gate["authorization_item_not_granted_count"],
        "protected_action_required_count": gate["protected_action_required_count"],
        "owner_input_required_count": gate["owner_input_required_count"],
        "sandbox_plan_required_count": gate["sandbox_plan_required_count"],
        "license_review_required_count": gate["license_review_required_count"],
        "security_review_required_count": gate["security_review_required_count"],
        "runtime_integration_allowed_count": 0,
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "action_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_runtime_integration_owner_supplied_authorization_packet_template_count": 1,
    }


def base_review_record(gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
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
        "required_authorization_fields": AUTHORIZATION_FIELDS,
        "source_owner_filled_authorization_item_templates": gate["owner_filled_authorization_item_templates"],
        "reviewed_owner_filled_authorization_item_templates": reviewed_template_items(gate),
        "input_uris": {
            "adapter_runtime_integration_owner_filled_authorization_packet_template_gate": rel(TEMPLATE_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        **counts(gate),
        "claim_boundary": false_boundary(),
    }


def build_gate(gate: dict) -> dict:
    return {
        **base_review_record(gate),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-filled-authorization-packet-template-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Unfilled owner-filled authorization packet template reviewed; authorization remains not granted",
    }


def build_validation_result(gate: dict) -> dict:
    return {
        **base_review_record(gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(TEMPLATE_GATE),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(REVIEW_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-supplied-authorization-packet-template
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local owner-supplied authorization packet template without granting authorization
  - Keep it structurally separate from the unfilled template and still blocked by default
  - Require a later owner-supplied packet review before any protected action can be accepted
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(gate).items())
    item_lines = "\n".join(
        "- {authorization_item_id}: review_status=reviewed_owner_filled_template_item_remains_unfilled_not_granted, decision=unfilled, authorization_status=not_granted, protected_action_required=true, action_allowed=false".format(
            **item
        )
        for item in reviewed_template_items(gate)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Owner-Filled Authorization Packet Template Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_review_v0_1=true

## Review summary

- candidate_id={CANDIDATE_ID}
- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- authorization_packet_completed=false
- owner_authorization_granted=false
- provider_neutral=true
- dependency_free=true
- candidate_tool_import_allowed=false
- dependency_install_allowed=false
- external_fetch_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false
- runtime_export_performed=false

## Counts

{count_lines}

## Reviewed owner-filled authorization item templates

{item_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    gate = read_json(TEMPLATE_GATE)
    require_template_gate(gate)

    write_json(REVIEW_GATE, build_gate(gate))
    report = build_report(gate)
    write_text(REVIEW_REPORT, report)
    write_text(REVIEW_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Owner-Filled Authorization Packet Template Review v0.1")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    print("authorization_packet_completed=false")
    print("owner_authorization_granted=false")
    for key, value in counts(gate).items():
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

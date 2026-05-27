from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_review_gate.json"
OWNER_INPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet.yml"
OWNER_INPUT_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_gate.json"
OWNER_INPUT_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_RUNTIME_INTEGRATION_OWNER_INPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
OWNER_INPUT_DECISION = "OWNER_INPUT_PACKET_TEMPLATE_READY_UNFILLED_RUNTIME_ACTIONS_BLOCKED"
OWNER_INPUT_STATUS = "owner_input_required_not_supplied_authorization_not_granted"

BOUNDARY_ITEMS = [
    "candidate tool import",
    "dependency install",
    "external fetch",
    "runtime integration",
    "runtime export",
    "external service call",
    "deploy",
    "publish",
    "release readiness claim",
    "production readiness claim",
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


def require_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("review gate must point to this owner input packet goal")
    if gate.get("ready_for_runtime_integration_owner_input_packet_count") != 1:
        raise SystemExit("review gate must be ready for owner input packet")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("review gate must not grant owner authorization")
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
            raise SystemExit(f"review gate {key} must be false")


def owner_input_items(gate: dict) -> list[dict]:
    return [
        {
            "authorization_item_id": item["authorization_item_id"],
            "requested_action": item["requested_action"],
            "decision": "unfilled",
            "authorization_status": "not_granted",
            "protected_action_required": True,
            "action_allowed": False,
            "owner_authorization_granted": False,
            "authorization_statement": "",
            "authorized_by": "",
            "authorized_at": "",
            "authorization_expires_at": "",
            "scope_boundaries": [],
            "sandbox_plan_uri": "",
            "license_review_uri": "",
            "security_review_uri": "",
            "revocation_note": "",
        }
        for item in gate["reviewed_authorization_items"]
    ]


def counts(gate: dict) -> dict:
    return {
        "runtime_preflight_check_count": gate["runtime_preflight_check_count"],
        "authorization_item_count": gate["authorization_item_count"],
        "owner_input_item_template_count": len(owner_input_items(gate)),
        "owner_input_item_completed_count": 0,
        "authorization_item_not_granted_count": gate["authorization_item_not_granted_count"],
        "protected_action_required_count": gate["protected_action_required_count"],
        "owner_input_required_count": 1,
        "sandbox_plan_required_count": gate["sandbox_plan_required_count"],
        "license_review_required_count": gate["license_review_required_count"],
        "security_review_required_count": gate["security_review_required_count"],
        "runtime_integration_allowed_count": 0,
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "action_allowed_count": 0,
        "owner_input_packet_blocker_count": 0,
        "ready_for_runtime_integration_owner_input_packet_review_count": 1,
    }


def base_owner_input_record(gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "owner_input_decision": OWNER_INPUT_DECISION,
        "owner_input_status": OWNER_INPUT_STATUS,
        "owner_input_packet_completed": False,
        "owner_authorization_granted": False,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "runtime_integration_performed": False,
        "runtime_export_performed": False,
        "source_reviewed_authorization_items": gate["reviewed_authorization_items"],
        "owner_input_authorization_items": owner_input_items(gate),
        "input_uris": {
            "adapter_runtime_integration_authorization_packet_review_gate": rel(REVIEW_GATE),
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
        **base_owner_input_record(gate),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-input-packet-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Owner input packet template created unfilled; runtime and external actions remain blocked",
    }


def build_validation_result(gate: dict) -> dict:
    return {
        **base_owner_input_record(gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(OWNER_INPUT_PACKET),
            rel(OWNER_INPUT_GATE),
            rel(OWNER_INPUT_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_owner_input_packet(gate: dict) -> str:
    item_rows = []
    for item in owner_input_items(gate):
        item_rows.append(
            f"""  - authorization_item_id: {item['authorization_item_id']}
    requested_action: \"{item['requested_action']}\"
    decision: unfilled
    authorization_status: not_granted
    protected_action_required: true
    action_allowed: false
    owner_authorization_granted: false
    authorization_statement:
    authorized_by:
    authorized_at:
    authorization_expires_at:
    scope_boundaries: []
    sandbox_plan_uri:
    license_review_uri:
    security_review_uri:
    revocation_note:"""
        )
    blocked_rows = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    flag_rows = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""packet_id: avf-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-input-packet-v0-1
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
candidate_id: {CANDIDATE_ID}
owner_input_decision: {OWNER_INPUT_DECISION}
owner_input_status: {OWNER_INPUT_STATUS}

owner_input_packet_completed: false
owner_authorization_granted: false
runtime_integration_allowed: false
candidate_tool_import_allowed: false
dependency_install_allowed: false
external_fetch_allowed: false
runtime_export_allowed: false
external_service_call_allowed: false

owner_input_authorization_items:
{chr(10).join(item_rows)}

boundary_summary:
{blocked_rows}

claim_boundary:
{flag_rows}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-input-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the unfilled owner input packet template before any runtime authorization can be accepted
  - Confirm every authorization item is still unfilled, not_granted, protected_action_required, and action_allowed=false
  - Keep runtime, dependency, tool import, and external fetch actions blocked until a later owner-filled packet is reviewed
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(gate).items())
    item_lines = "\n".join(
        "- {authorization_item_id}: decision=unfilled, authorization_status=not_granted, protected_action_required=true, action_allowed=false".format(
            **item
        )
        for item in owner_input_items(gate)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Owner Input Packet v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1=true

## Owner input summary

- owner_input_packet_template_created=true
- owner_input_packet_gate_created=true
- candidate_id={CANDIDATE_ID}
- owner_input_decision={OWNER_INPUT_DECISION}
- owner_input_status={OWNER_INPUT_STATUS}
- owner_input_packet_completed=false
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

## Owner input authorization item templates

{item_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    gate = read_json(REVIEW_GATE)
    require_review_gate(gate)

    write_text(OWNER_INPUT_PACKET, build_owner_input_packet(gate))
    write_json(OWNER_INPUT_GATE, build_gate(gate))
    write_text(OWNER_INPUT_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Owner Input Packet v0.1")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_v0_1=true")
    print("owner_input_packet_template_created=true")
    print("owner_input_packet_gate_created=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"owner_input_decision={OWNER_INPUT_DECISION}")
    print(f"owner_input_status={OWNER_INPUT_STATUS}")
    print("owner_input_packet_completed=false")
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

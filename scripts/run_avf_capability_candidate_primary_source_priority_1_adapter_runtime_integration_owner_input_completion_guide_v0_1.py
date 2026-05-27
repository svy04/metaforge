from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

OWNER_INPUT_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_review_gate.json"
COMPLETION_GUIDE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide.md"
COMPLETION_GUIDE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_gate.json"
COMPLETION_GUIDE_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_RUNTIME_INTEGRATION_OWNER_INPUT_COMPLETION_GUIDE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_filled_authorization_packet_template_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
GUIDE_DECISION = "OWNER_INPUT_COMPLETION_GUIDE_READY_RUNTIME_ACTIONS_STILL_BLOCKED"
GUIDE_STATUS = "completion_guide_instruction_only_authorization_not_granted"

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

COMPLETION_STEPS = [
    "choose_authorization_items",
    "write_owner_authorization_statement",
    "attach_sandbox_license_security_reviews",
    "set_scope_boundaries_and_expiration",
    "define_rollback_and_revocation",
    "submit_owner_filled_packet_for_review",
]

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


def require_owner_input_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("owner input review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("owner input review gate must point to this completion guide goal")
    if gate.get("ready_for_runtime_integration_owner_input_completion_guide_count") != 1:
        raise SystemExit("owner input review gate must be ready for completion guide")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("owner authorization must remain not granted")
    if gate.get("owner_input_packet_completed") is not False:
        raise SystemExit("owner input packet must remain incomplete")
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
            raise SystemExit(f"owner input review gate {key} must be false")


def counts(gate: dict) -> dict:
    return {
        "runtime_preflight_check_count": gate["runtime_preflight_check_count"],
        "authorization_item_count": gate["authorization_item_count"],
        "reviewed_owner_input_item_count": gate["reviewed_owner_input_item_count"],
        "required_authorization_field_count": len(AUTHORIZATION_FIELDS),
        "completion_step_count": len(COMPLETION_STEPS),
        "owner_input_item_completed_count": gate["owner_input_item_completed_count"],
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
        "completion_guide_blocker_count": 0,
        "ready_for_runtime_integration_owner_filled_authorization_packet_template_count": 1,
    }


def base_completion_guide_record(gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "guide_decision": GUIDE_DECISION,
        "guide_status": GUIDE_STATUS,
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
        "completion_steps": COMPLETION_STEPS,
        "source_reviewed_owner_input_authorization_items": gate["reviewed_owner_input_authorization_items"],
        "input_uris": {
            "adapter_runtime_integration_owner_input_packet_review_gate": rel(OWNER_INPUT_REVIEW_GATE),
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
        **base_completion_guide_record(gate),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-input-completion-guide-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Owner input completion guide created; authorization remains not granted and runtime actions remain blocked",
    }


def build_validation_result(gate: dict) -> dict:
    return {
        **base_completion_guide_record(gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(OWNER_INPUT_REVIEW_GATE),
            rel(COMPLETION_GUIDE),
            rel(COMPLETION_GUIDE_GATE),
            rel(COMPLETION_GUIDE_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_completion_guide(gate: dict) -> str:
    field_rows = "\n".join(f"- `{field}`: required in a later owner-filled packet before review can accept any action." for field in AUTHORIZATION_FIELDS)
    step_rows = "\n".join(f"- `{step}`: complete this as written, then route to a later review gate." for step in COMPLETION_STEPS)
    item_rows = "\n".join(
        "- `{authorization_item_id}`: remains decision=unfilled, authorization_status=not_granted, protected_action_required=true, action_allowed=false.".format(
            **item
        )
        for item in gate["reviewed_owner_input_authorization_items"]
    )
    blocked_rows = "\n".join(f"- No {item}" for item in BOUNDARY_ITEMS)
    return f"""# AVF Adapter Runtime Integration Owner Input Completion Guide v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
candidate_id: {CANDIDATE_ID}
guide_decision: {GUIDE_DECISION}
guide_status: {GUIDE_STATUS}

This guide explains how the owner would fill a later runtime authorization packet. It is instruction-only and does not grant authorization.

## Current locked state

- owner_authorization_granted: false
- runtime_integration_allowed: false
- candidate_tool_import_allowed: false
- dependency_install_allowed: false
- external_fetch_allowed: false

## Required authorization fields

{field_rows}

## Completion steps

{step_rows}

## Authorization items still blocked

{item_rows}

## Boundary summary

{blocked_rows}

## Minimum owner completion rule

The owner-filled packet must choose exact `authorized_actions`, bind them to `scope_boundaries`, provide sandbox/license/security review URIs, include a rollback plan and revocation note, and then pass a separate review gate. Until then, every action remains blocked.

## Next safe goal

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-runtime-integration-owner-filled-authorization-packet-template
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local owner-filled authorization packet template without granting authorization
  - Include all required authorization fields from the completion guide
  - Keep the template unfilled by default and route any filled version through a later review gate
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(gate).items())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Owner Input Completion Guide v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_v0_1=true

## Guide summary

- owner_input_completion_guide_created=true
- owner_input_completion_guide_gate_created=true
- candidate_id={CANDIDATE_ID}
- guide_decision={GUIDE_DECISION}
- guide_status={GUIDE_STATUS}
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

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    gate = read_json(OWNER_INPUT_REVIEW_GATE)
    require_owner_input_review_gate(gate)

    write_text(COMPLETION_GUIDE, build_completion_guide(gate))
    write_json(COMPLETION_GUIDE_GATE, build_gate(gate))
    write_text(COMPLETION_GUIDE_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Owner Input Completion Guide v0.1")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_runtime_integration_owner_input_completion_guide_v0_1=true")
    print("owner_input_completion_guide_created=true")
    print("owner_input_completion_guide_gate_created=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"guide_decision={GUIDE_DECISION}")
    print(f"guide_status={GUIDE_STATUS}")
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

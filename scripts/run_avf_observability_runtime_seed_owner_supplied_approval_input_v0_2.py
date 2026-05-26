from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
GOALS = ROOT / "docs" / "goals"

PREVIOUS_RETRY_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_gate.json"
OWNER_INPUT_PACKET = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_v0_2.yml"
OWNER_INPUT_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_v0_2_gate.json"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_v0_2_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_v0_2.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_SUPPLIED_APPROVAL_INPUT_V0_2_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_v0_2"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_review_v0_2"
CREATED_AT = "2026-05-27T00:00:00Z"
INPUT_DECISION = "OWNER_SUPPLIED_APPROVAL_INPUT_V0_2_CREATED_EMPTY_NOT_AUTHORIZED"
OWNER_INPUT_STATUS = "not_supplied"

REQUIRED_OWNER_FIELDS = [
    "owner_name",
    "reviewed_packet_id",
    "approval_decision",
    "approved_actions",
    "approval_valid_after_review",
    "approval_notes",
    "reviewed_at",
]

REQUIRED_APPROVAL_ACTIONS = [
    "collector_start",
    "telemetry_export",
    "runtime_backend_integration",
    "dependency_adoption",
]

FALSE_FLAGS = {
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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def false_boundary() -> dict:
    return dict(FALSE_FLAGS)


def require_previous_retry_gate() -> None:
    gate = read_json(PREVIOUS_RETRY_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous retry gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous retry gate must point to this v0.2 input goal")
    if gate.get("retry_status") != "awaiting_owner_supplied_approval":
        raise SystemExit("previous retry gate must be awaiting owner approval")
    if gate.get("owner_approval_granted") is not False:
        raise SystemExit("previous retry gate must not grant approval")
    if gate.get("owner_supplied_fields_count") != 0:
        raise SystemExit("previous retry gate owner supplied field count must be zero")
    if gate.get("missing_required_owner_fields") != REQUIRED_OWNER_FIELDS:
        raise SystemExit("previous retry gate missing fields mismatch")
    if gate.get("codex_must_not_fill_owner_approval") is not True:
        raise SystemExit("previous retry gate must forbid Codex-filled approval")
    if gate.get("owner_must_supply_approval") is not True:
        raise SystemExit("previous retry gate must require owner-supplied approval")
    for key in ["collector_start_allowed", "telemetry_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            raise SystemExit(f"previous retry gate {key} must remain false")


def build_owner_input_packet() -> str:
    fields = "\n".join(f"  - {field}" for field in REQUIRED_OWNER_FIELDS)
    actions = "\n".join(f"  - {action}" for action in REQUIRED_APPROVAL_ACTIONS)
    boundary = "\n".join(f"  {key}: false" for key in FALSE_FLAGS)
    return f"""packet_id: avf-observability-runtime-seed-owner-supplied-approval-input-v0-2
schema_version: 0.2
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
input_decision: {INPUT_DECISION}
owner_input_status: {OWNER_INPUT_STATUS}

owner_approval_record_present: false
owner_approval_granted: false
owner_supplied_fields_count: 0
missing_required_owner_fields_count: {len(REQUIRED_OWNER_FIELDS)}
missing_required_owner_fields:
{fields}

actions_requiring_owner_approval:
{actions}

owner_name: null
reviewed_packet_id: null
approval_decision: null
approved_actions: []
approval_valid_after_review: false
approval_notes: null
reviewed_at: null

collector_start_allowed: false
telemetry_export_allowed: false
runtime_integration_allowed: false
dependency_adoption_allowed: false
codex_fabricated_owner_approval: false
codex_must_not_fill_owner_approval: true
owner_must_supply_approval: true

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_owner_input_gate() -> dict:
    return {
        "gate_id": "avf-observability-runtime-seed-owner-supplied-approval-input-v0-2-gate",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "input_decision": INPUT_DECISION,
        "owner_input_status": OWNER_INPUT_STATUS,
        "owner_approval_record_present": False,
        "owner_approval_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_owner_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "actions_requiring_owner_approval": REQUIRED_APPROVAL_ACTIONS,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_fabricated_owner_approval": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
        "owner_input_packet_uri": rel(OWNER_INPUT_PACKET),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-observability-runtime-seed-owner-supplied-approval-input-v0-2
owner_input_status: {OWNER_INPUT_STATUS}
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the v0.2 owner-supplied approval input packet
  - Review must keep runtime actions blocked when owner input is empty
  - Confirm Codex did not fabricate owner approval
  - Do not start collectors, export telemetry, integrate runtime backends, adopt dependencies, deploy, publish, or claim readiness

owner_approval_record_present: false
collector_start_allowed: false
telemetry_export_allowed: false
runtime_integration_allowed: false
dependency_adoption_allowed: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_observability_runtime_seed_owner_supplied_approval_input_v0_2",
        "status": "PASS",
        "input_decision": INPUT_DECISION,
        "owner_input_status": OWNER_INPUT_STATUS,
        "owner_approval_record_present": False,
        "owner_approval_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_owner_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "actions_requiring_owner_approval": REQUIRED_APPROVAL_ACTIONS,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_fabricated_owner_approval": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    missing = "\n".join(f"- {field}" for field in REQUIRED_OWNER_FIELDS)
    return f"""# AVF Observability Runtime Seed Owner-Supplied Approval Input v0.2 Report

RESULT: PASS
observability_runtime_seed_owner_supplied_approval_input_v0_2=true

## Commands

- python scripts\\run_avf_observability_runtime_seed_owner_supplied_approval_input_v0_2.py
- python scripts\\validate_avf_observability_runtime_seed_owner_supplied_approval_input_v0_2.py

## Input summary

- input_decision={INPUT_DECISION}
- owner_input_status={OWNER_INPUT_STATUS}
- owner_approval_record_present=false
- owner_approval_granted=false
- owner_supplied_fields_count=0
- missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}
- collector_start_allowed=false
- telemetry_export_allowed=false
- runtime_integration_allowed=false
- dependency_adoption_allowed=false
- codex_fabricated_owner_approval=false
- codex_must_not_fill_owner_approval=true
- owner_must_supply_approval=true

## Missing required owner fields

{missing}

## Generated artifacts

- {rel(OWNER_INPUT_PACKET)}
- {rel(OWNER_INPUT_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_retry_gate()

    write_text(OWNER_INPUT_PACKET, build_owner_input_packet())
    write_json(OWNER_INPUT_GATE, build_owner_input_gate())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Observability Runtime Seed Owner-Supplied Approval Input v0.2")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_supplied_approval_input_v0_2=true")
    print(f"input_decision={INPUT_DECISION}")
    print("owner_input_status=not_supplied")
    print("owner_approval_record_present=false")
    print("owner_approval_granted=false")
    print("owner_supplied_fields_count=0")
    print(f"missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    print("collector_start_allowed=false")
    print("telemetry_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print("codex_fabricated_owner_approval=false")
    print("codex_must_not_fill_owner_approval=true")
    print("owner_must_supply_approval=true")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("automated_scraping_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("runtime_export_performed=false")
    print("collector_started=false")
    print("telemetry_export_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

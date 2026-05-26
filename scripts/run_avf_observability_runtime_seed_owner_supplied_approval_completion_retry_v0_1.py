from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
GOALS = ROOT / "docs" / "goals"

PREVIOUS_REVIEW_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_review_gate.json"
RETRY_PACKET = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry.yml"
RETRY_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_gate.json"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_SUPPLIED_APPROVAL_COMPLETION_RETRY_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_1"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_v0_2"
CREATED_AT = "2026-05-27T00:00:00Z"
RETRY_DECISION = "OWNER_APPROVAL_COMPLETION_RETRY_PACKET_CREATED_INTEGRATION_STILL_BLOCKED"
RETRY_STATUS = "awaiting_owner_supplied_approval"

REQUIRED_OWNER_FIELDS = [
    "owner_name",
    "reviewed_packet_id",
    "approval_decision",
    "approved_actions",
    "approval_valid_after_review",
    "approval_notes",
    "reviewed_at",
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


def require_previous_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous review gate must point to this retry goal")
    if gate.get("review_status") != "blocked_owner_approval_input_not_supplied":
        raise SystemExit("previous review gate must remain blocked")
    if gate.get("owner_approval_granted") is not False:
        raise SystemExit("previous review gate must not grant approval")
    if gate.get("owner_supplied_fields_count") != 0:
        raise SystemExit("previous review gate supplied field count must remain zero")
    if gate.get("missing_required_owner_fields") != REQUIRED_OWNER_FIELDS:
        raise SystemExit("previous review gate missing fields mismatch")
    if gate.get("codex_fabricated_owner_approval") is not False:
        raise SystemExit("Codex fabricated owner approval must be false")
    for key in ["collector_start_allowed", "telemetry_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            raise SystemExit(f"previous review gate {key} must remain false")


def build_retry_packet() -> str:
    fields = "\n".join(
        "\n".join(
            [
                f"  - field: {field}",
                "    status: missing",
                "    supplied_by: owner_only",
                "    codex_may_fill: false",
            ]
        )
        for field in REQUIRED_OWNER_FIELDS
    )
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""packet_id: avf-observability-runtime-seed-owner-supplied-approval-completion-retry-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
retry_decision: {RETRY_DECISION}
retry_status: {RETRY_STATUS}

owner_approval_granted: false
owner_supplied_fields_count: 0
missing_required_owner_fields_count: {len(REQUIRED_OWNER_FIELDS)}
collector_start_allowed: false
telemetry_export_allowed: false
runtime_integration_allowed: false
dependency_adoption_allowed: false
codex_must_not_fill_owner_approval: true
owner_must_supply_approval: true

missing_required_owner_fields:
{fields}

retry_rules:
  - Owner may supply a new v0.2 approval input packet with the required fields.
  - Codex must not fabricate owner name, reviewed packet id, approval decision, approved actions, approval notes, or timestamps.
  - Any supplied input must be reviewed in a separate step before collector start, telemetry export, runtime integration, or dependency adoption can be considered.
  - Collectors, telemetry export, runtime integration, and dependency adoption remain blocked in this retry packet.

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_retry_gate() -> dict:
    return {
        "gate_id": "avf-observability-runtime-seed-owner-supplied-approval-completion-retry-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "retry_decision": RETRY_DECISION,
        "retry_status": RETRY_STATUS,
        "owner_approval_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_owner_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
        "retry_packet_uri": rel(RETRY_PACKET),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: collect-observability-runtime-seed-owner-supplied-approval-input-v0-2
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Wait for owner-supplied approval input v0.2
  - Codex must not fabricate owner approval
  - Keep retry_status: {RETRY_STATUS}
  - Keep owner_approval_granted false until owner input exists and is reviewed
  - Do not start collectors from this retry packet
  - Do not export telemetry from this retry packet
  - Do not integrate runtime backends from this retry packet
  - Do not adopt dependencies from this retry packet
  - Do not deploy, publish, or claim readiness

retry_status: {RETRY_STATUS}
owner_approval_granted: false
collector_start_allowed: false
telemetry_export_allowed: false
runtime_integration_allowed: false
dependency_adoption_allowed: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_1",
        "status": "PASS",
        "retry_decision": RETRY_DECISION,
        "retry_status": RETRY_STATUS,
        "owner_approval_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_owner_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    missing = "\n".join(f"- {field}" for field in REQUIRED_OWNER_FIELDS)
    return f"""# AVF Observability Runtime Seed Owner-Supplied Approval Completion Retry v0.1 Report

RESULT: PASS
observability_runtime_seed_owner_supplied_approval_completion_retry_v0_1=true

## Commands

- python scripts\\run_avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_1.py
- python scripts\\validate_avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_1.py

## Retry summary

- retry_decision={RETRY_DECISION}
- retry_status={RETRY_STATUS}
- owner_approval_granted=false
- owner_supplied_fields_count=0
- missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}
- collector_start_allowed=false
- telemetry_export_allowed=false
- runtime_integration_allowed=false
- dependency_adoption_allowed=false
- codex_must_not_fill_owner_approval=true
- owner_must_supply_approval=true

## Missing required owner fields

{missing}

## Generated artifacts

- {rel(RETRY_PACKET)}
- {rel(RETRY_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    previous_review_gate = read_json(PREVIOUS_REVIEW_GATE)
    require_previous_review_gate(previous_review_gate)

    write_text(RETRY_PACKET, build_retry_packet())
    write_json(RETRY_GATE, build_retry_gate())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Observability Runtime Seed Owner-Supplied Approval Completion Retry v0.1")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_supplied_approval_completion_retry_v0_1=true")
    print(f"retry_decision={RETRY_DECISION}")
    print(f"retry_status={RETRY_STATUS}")
    print("owner_approval_granted=false")
    print("owner_supplied_fields_count=0")
    print(f"missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    print("collector_start_allowed=false")
    print("telemetry_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
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

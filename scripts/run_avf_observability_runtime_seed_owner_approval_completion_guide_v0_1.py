from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PREVIOUS_REVIEW_GATE = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_review_gate.json"
COMPLETION_GUIDE = OBS_GENERATED / "observability_runtime_seed_owner_approval_record_completion_guide.md"
COMPLETION_GUIDE_GATE = OBS_GENERATED / "observability_runtime_seed_owner_approval_record_completion_guide_gate.json"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_approval_record_completion_guide_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_approval_record_completion_guide_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_APPROVAL_COMPLETION_GUIDE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_approval_completion_guide_v0_1"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
GUIDE_DECISION = "OWNER_APPROVAL_COMPLETION_GUIDE_CREATED_NO_RUNTIME_AUTHORIZATION_GRANTED"
PREVIOUS_REVIEW_STATUS = "blocked_missing_owner_approval_record"

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


def require_previous_review_gate() -> None:
    gate = read_json(PREVIOUS_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous review gate must point to this completion guide goal")
    if gate.get("review_status") != PREVIOUS_REVIEW_STATUS:
        raise SystemExit("previous review gate status mismatch")
    if gate.get("owner_approval_record_present") is not False:
        raise SystemExit("previous review gate must not contain owner approval")
    if gate.get("missing_required_owner_fields") != REQUIRED_OWNER_FIELDS:
        raise SystemExit("previous review gate missing owner fields mismatch")
    for key in ["collector_start_allowed", "telemetry_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            raise SystemExit(f"previous review gate {key} must remain false")


def build_completion_guide() -> str:
    required = "\n".join(f"- `{field}`" for field in REQUIRED_OWNER_FIELDS)
    actions = "\n".join(f"- `{action}`" for action in REQUIRED_APPROVAL_ACTIONS)
    boundary = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    return f"""# AVF Observability Runtime Seed Owner Approval Record Completion Guide v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
guide_decision: {GUIDE_DECISION}

owner_approval_record_present: false
collector_start_allowed: false
telemetry_export_allowed: false
runtime_integration_allowed: false
dependency_adoption_allowed: false
codex_must_not_fill_owner_approval: true
owner_must_supply_approval: true
missing_required_owner_fields_count: {len(REQUIRED_OWNER_FIELDS)}

## Required Owner-Supplied Fields

{required}

## Actions Requiring Owner Approval

{actions}

## Completion Rules

- The owner must supply these fields manually before any future runtime observability integration can be reviewed.
- Codex must not fabricate owner identity, approval decision, approved actions, review timestamp, or approval notes.
- A completed owner-supplied record still requires a separate review step before any collector startup, telemetry export, runtime backend integration, or dependency adoption can be considered.
- This guide does not grant approval and does not execute any runtime action.

## Protected Action Boundary

{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_completion_gate() -> dict:
    return {
        "gate_id": "avf-observability-runtime-seed-owner-approval-completion-guide-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "owner_approval_record_present": False,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
        "required_owner_fields": REQUIRED_OWNER_FIELDS,
        "actions_requiring_owner_approval": REQUIRED_APPROVAL_ACTIONS,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "completion_guide_uri": rel(COMPLETION_GUIDE),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: collect-observability-runtime-seed-owner-supplied-approval-input
owner_approval_record_present: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Wait for owner-supplied approval input
  - Codex must not fabricate owner approval
  - Keep all runtime actions blocked until owner input exists and is separately reviewed
  - Do not start collectors, export telemetry, integrate runtime backends, install dependencies, deploy, publish, or claim readiness

owner_approval_record_present: false
collector_start_allowed: false
telemetry_export_allowed: false
runtime_integration_allowed: false
dependency_adoption_allowed: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_observability_runtime_seed_owner_approval_completion_guide_v0_1",
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "owner_approval_record_present": False,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_approval": True,
        "required_owner_fields": REQUIRED_OWNER_FIELDS,
        "actions_requiring_owner_approval": REQUIRED_APPROVAL_ACTIONS,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    return f"""# AVF Observability Runtime Seed Owner Approval Completion Guide v0.1 Report

RESULT: PASS
observability_runtime_seed_owner_approval_completion_guide_v0_1=true

## Commands

- python scripts\\run_avf_observability_runtime_seed_owner_approval_completion_guide_v0_1.py
- python scripts\\validate_avf_observability_runtime_seed_owner_approval_completion_guide_v0_1.py

## Guide summary

- guide_decision={GUIDE_DECISION}
- owner_approval_record_present=false
- collector_start_allowed=false
- telemetry_export_allowed=false
- runtime_integration_allowed=false
- dependency_adoption_allowed=false
- codex_must_not_fill_owner_approval=true
- owner_must_supply_approval=true
- missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}

## Generated artifacts

- {rel(COMPLETION_GUIDE)}
- {rel(COMPLETION_GUIDE_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> int:
    require_previous_review_gate()

    write_text(COMPLETION_GUIDE, build_completion_guide())
    write_json(COMPLETION_GUIDE_GATE, build_completion_gate())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Observability Runtime Seed Owner Approval Completion Guide v0.1")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_approval_completion_guide_v0_1=true")
    print(f"guide_decision={GUIDE_DECISION}")
    print("owner_approval_record_present=false")
    print("collector_start_allowed=false")
    print("telemetry_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print("codex_must_not_fill_owner_approval=true")
    print("owner_must_supply_approval=true")
    print(f"missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

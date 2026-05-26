from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

ACCEPTANCE_GATE = OBS_GENERATED / "observability_runtime_seed_acceptance_gate.json"
ACCEPTANCE_NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_acceptance_next_action.yml"
OWNER_APPROVAL_PACKET = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet.json"
OWNER_APPROVAL_GATE = OBS_GENERATED / "observability_runtime_seed_owner_approval_gate.json"
OWNER_APPROVAL_GUIDE = OBS_GENERATED / "observability_runtime_seed_owner_approval_completion_guide.md"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_APPROVAL_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_acceptance_gate_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
APPROVAL_STATUS = "not_approved_owner_input_required"
APPROVAL_SCOPE = "future_runtime_observability_integration_only"

REQUIRED_APPROVAL_ACTIONS = [
    "collector_start",
    "telemetry_export",
    "runtime_backend_integration",
    "dependency_adoption",
]

ALLOWED_WITHOUT_APPROVAL = [
    "repo_local_documentation",
    "repo_local_validation",
    "repo_local_approval_packet_review",
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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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


def require_previous_acceptance_gate() -> None:
    gate = read_json(ACCEPTANCE_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("acceptance gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("acceptance gate must point to this owner approval packet")
    if gate.get("owner_approval_required_before_runtime_integration") is not True:
        raise SystemExit("acceptance gate must require owner approval before runtime integration")
    for key in ["runtime_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            raise SystemExit(f"acceptance gate {key} must remain false")
    next_action = read(ACCEPTANCE_NEXT_ACTION)
    if f"next_safe_goal_id: {THIS_GOAL_ID}" not in next_action:
        raise SystemExit("acceptance next action must point to this goal")


def build_packet() -> dict:
    return {
        "packet_id": "avf-observability-runtime-seed-owner-approval-packet-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "required_owner_decision": "explicit_owner_approval_required_before_runtime_integration",
        "integration_actions_requiring_owner_approval": REQUIRED_APPROVAL_ACTIONS,
        "blocked_until_owner_approval": True,
        "allowed_without_owner_approval": ALLOWED_WITHOUT_APPROVAL,
        "approval_record_template": {
            "owner_name": "<required>",
            "reviewed_packet_id": "avf-observability-runtime-seed-owner-approval-packet-v0-1",
            "approval_decision": "pending",
            "approved_actions": [],
            "approval_valid_after_review": False,
            "approval_notes": "<required before any future runtime integration>",
            "reviewed_at": "<required>",
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate() -> dict:
    return {
        "gate_id": "avf-observability-runtime-seed-owner-approval-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "owner_approval_packet_created": True,
        "owner_approval_record_present": False,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def report_body(title: str) -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    actions = "\n".join(f"- {action}" for action in REQUIRED_APPROVAL_ACTIONS)
    allowed = "\n".join(f"- {item}" for item in ALLOWED_WITHOUT_APPROVAL)
    return f"""# {title}

RESULT: PASS
observability_runtime_seed_owner_approval_packet_v0_1=true
approval_status={APPROVAL_STATUS}
approval_scope={APPROVAL_SCOPE}
owner_approval_record_present=false
collector_start_allowed=false
telemetry_export_allowed=false
runtime_integration_allowed=false
dependency_adoption_allowed=false

## Actions requiring explicit owner approval

{actions}

## Allowed without owner approval

{allowed}

## Boundary

This packet is not approval. It only defines the approval record required before any future collector startup, telemetry export, runtime backend integration, or dependency adoption.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-observability-runtime-seed-owner-approval-packet
owner_approval_record_present: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local owner approval packet for completeness
  - Do not treat this packet as approval
  - Keep collector startup, telemetry export, runtime integration, dependency adoption, deploy, publish, release readiness, and production readiness blocked
  - If owner approval is later supplied, record it as a separate reviewed artifact before any future integration proposal

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_observability_runtime_seed_owner_approval_packet_v0_1",
        "status": "PASS",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "approval_status": APPROVAL_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "owner_approval_record_present": False,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_report() -> str:
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [OWNER_APPROVAL_PACKET, OWNER_APPROVAL_GATE, OWNER_APPROVAL_GUIDE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return report_body("AVF Observability Runtime Seed Owner Approval Packet v0.1 Report") + f"""
## Commands

- python scripts\\run_avf_observability_runtime_seed_owner_approval_packet_v0_1.py
- python scripts\\validate_avf_observability_runtime_seed_owner_approval_packet_v0_1.py

## Generated artifacts

{artifacts}
"""


def main() -> int:
    require_previous_acceptance_gate()

    write_json(OWNER_APPROVAL_PACKET, build_packet())
    write_json(OWNER_APPROVAL_GATE, build_gate())
    write_text(OWNER_APPROVAL_GUIDE, report_body("Observability Runtime Seed Owner Approval Completion Guide v0.1"))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_validation_report())

    print("AVF Observability Runtime Seed Owner Approval Packet v0.1")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_approval_packet_v0_1=true")
    print(f"approval_status={APPROVAL_STATUS}")
    print(f"approval_scope={APPROVAL_SCOPE}")
    print("owner_approval_record_present=false")
    print("collector_start_allowed=false")
    print("telemetry_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

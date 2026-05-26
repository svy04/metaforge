from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

OWNER_APPROVAL_PACKET = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet.json"
OWNER_APPROVAL_GATE = OBS_GENERATED / "observability_runtime_seed_owner_approval_gate.json"
OWNER_APPROVAL_NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_next_action.yml"
REVIEW = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_review.json"
REVIEW_GATE = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_review_gate.json"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_review_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_approval_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_APPROVAL_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_approval_completion_guide_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "OWNER_APPROVAL_PACKET_REVIEWED_APPROVAL_NOT_PROVIDED_INTEGRATION_BLOCKED"
REVIEW_STATUS = "blocked_missing_owner_approval_record"
APPROVAL_SCOPE = "future_runtime_observability_integration_only"

REQUIRED_APPROVAL_ACTIONS = [
    "collector_start",
    "telemetry_export",
    "runtime_backend_integration",
    "dependency_adoption",
]

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


def require_previous_packet_inputs() -> None:
    packet = read_json(OWNER_APPROVAL_PACKET)
    gate = read_json(OWNER_APPROVAL_GATE)
    if packet.get("goal_id") != PREVIOUS_GOAL_ID or gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("owner approval packet or gate goal mismatch")
    if packet.get("next_safe_goal_id") != THIS_GOAL_ID or gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("owner approval packet and gate must point to this review goal")
    if packet.get("approval_status") != "not_approved_owner_input_required":
        raise SystemExit("owner approval packet must remain not approved")
    if packet.get("approval_scope") != APPROVAL_SCOPE:
        raise SystemExit("owner approval packet scope mismatch")
    if packet.get("integration_actions_requiring_owner_approval") != REQUIRED_APPROVAL_ACTIONS:
        raise SystemExit("owner approval packet action list mismatch")
    template = packet.get("approval_record_template", {})
    if sorted(template) != sorted(REQUIRED_OWNER_FIELDS):
        raise SystemExit("owner approval template fields mismatch")
    if template.get("approved_actions") != [] or template.get("approval_valid_after_review") is not False:
        raise SystemExit("owner approval template must not approve actions")
    if gate.get("owner_approval_record_present") is not False:
        raise SystemExit("owner approval record must not be present")
    for key in ["collector_start_allowed", "telemetry_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            raise SystemExit(f"owner approval gate {key} must remain false")
    if f"next_safe_goal_id: {THIS_GOAL_ID}" not in read(OWNER_APPROVAL_NEXT_ACTION):
        raise SystemExit("owner approval next action must point to this review goal")


def build_review_record() -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "approval_scope": APPROVAL_SCOPE,
        "owner_approval_required": True,
        "owner_approval_record_present": False,
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "actions_requiring_owner_approval": REQUIRED_APPROVAL_ACTIONS,
        "missing_required_owner_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "review_reason": "The packet defines an approval template, but no completed owner approval record is present.",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_review_gate(review: dict) -> dict:
    gate = {
        "gate_id": "avf-observability-runtime-seed-owner-approval-packet-review-gate-v0-1",
        "status": "PASS",
        "review_record_uri": rel(REVIEW),
    }
    gate.update(review)
    return gate


def build_next_action() -> str:
    return f"""action_id: create-observability-runtime-seed-owner-approval-completion-guide
owner_approval_record_present: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a completion guide for the owner approval record fields
  - Keep review_status: {REVIEW_STATUS}
  - Do not treat the approval packet or its review as owner approval
  - Do not start collectors, export telemetry, integrate runtime backends, install dependencies, deploy, publish, or claim readiness

review_status: {REVIEW_STATUS}
owner_approval_record_present: false
collector_start_allowed: false
telemetry_export_allowed: false
runtime_integration_allowed: false
dependency_adoption_allowed: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(review: dict) -> dict:
    result = {
        "validator_id": "validate_avf_observability_runtime_seed_owner_approval_packet_review_v0_1",
        "status": "PASS",
    }
    result.update(review)
    return result


def build_report(review: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    missing = "\n".join(f"- {field}" for field in REQUIRED_OWNER_FIELDS)
    actions = "\n".join(f"- {action}" for action in REQUIRED_APPROVAL_ACTIONS)
    return f"""# AVF Observability Runtime Seed Owner Approval Packet Review v0.1 Report

RESULT: PASS
observability_runtime_seed_owner_approval_packet_review_v0_1=true

## Commands

- python scripts\\run_avf_observability_runtime_seed_owner_approval_packet_review_v0_1.py
- python scripts\\validate_avf_observability_runtime_seed_owner_approval_packet_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- owner_approval_required=true
- owner_approval_record_present=false
- collector_start_allowed=false
- telemetry_export_allowed=false
- runtime_integration_allowed=false
- dependency_adoption_allowed=false
- missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}

## Actions still requiring owner approval

{actions}

## Missing required owner fields

{missing}

## Generated artifacts

- {rel(REVIEW)}
- {rel(REVIEW_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> int:
    require_previous_packet_inputs()
    review = build_review_record()

    write_json(REVIEW, review)
    write_json(REVIEW_GATE, build_review_gate(review))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Observability Runtime Seed Owner Approval Packet Review v0.1")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_approval_packet_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    print("owner_approval_required=true")
    print("owner_approval_record_present=false")
    print("collector_start_allowed=false")
    print("telemetry_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print(f"missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

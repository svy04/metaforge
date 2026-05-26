from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

OWNER_INPUT_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_gate.json"
REVIEW = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_review.json"
REVIEW_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_review_gate.json"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_review_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_input_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_OWNER_SUPPLIED_APPROVAL_INPUT_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_review_v0_1"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_input_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "OWNER_SUPPLIED_APPROVAL_INPUT_REVIEWED_EMPTY_INTEGRATION_BLOCKED"
REVIEW_STATUS = "blocked_owner_approval_input_not_supplied"

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


def require_owner_input_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("owner input gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("owner input gate must point to this review goal")
    if gate.get("owner_input_status") != "not_supplied":
        raise SystemExit("owner input status must be not_supplied")
    if gate.get("owner_approval_record_present") is not False:
        raise SystemExit("owner approval record must not be present")
    if gate.get("owner_supplied_fields_count") != 0:
        raise SystemExit("owner supplied fields must be zero")
    if gate.get("missing_required_owner_fields") != REQUIRED_OWNER_FIELDS:
        raise SystemExit("owner input missing fields mismatch")
    if gate.get("codex_fabricated_owner_approval") is not False:
        raise SystemExit("Codex fabricated owner approval must be false")
    if gate.get("codex_must_not_fill_owner_approval") is not True:
        raise SystemExit("Codex must not fill owner approval")
    if gate.get("owner_must_supply_approval") is not True:
        raise SystemExit("owner must supply approval")
    for key in ["collector_start_allowed", "telemetry_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if gate.get(key) is not False:
            raise SystemExit(f"owner input gate {key} must remain false")


def build_review_record() -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "owner_input_status": "not_supplied",
        "owner_approval_record_present": False,
        "owner_approval_granted": False,
        "owner_supplied_fields_count": 0,
        "missing_required_owner_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_owner_fields_count": len(REQUIRED_OWNER_FIELDS),
        "collector_start_allowed": False,
        "telemetry_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "codex_fabricated_owner_approval": False,
        "review_reason": "owner-supplied approval input is empty, so collectors, telemetry export, runtime integration, and dependency adoption remain blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_review_gate(review: dict) -> dict:
    gate = {
        "gate_id": "avf-observability-runtime-seed-owner-supplied-approval-input-review-gate-v0-1",
        "status": "PASS",
        "review_record_uri": rel(REVIEW),
    }
    gate.update(review)
    return gate


def build_next_action() -> str:
    return f"""action_id: create-observability-runtime-seed-owner-supplied-approval-completion-retry
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a completion retry guide that lists the missing owner approval fields
  - Keep review_status: {REVIEW_STATUS}
  - Do not start collectors from this blocked input review
  - Do not export telemetry from this blocked input review
  - Do not integrate runtime backends from this blocked input review
  - Do not fabricate owner approval
  - Do not install dependencies, deploy, publish, or claim readiness

review_status: {REVIEW_STATUS}
owner_approval_granted: false
collector_start_allowed: false
telemetry_export_allowed: false
runtime_integration_allowed: false
dependency_adoption_allowed: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(review: dict) -> dict:
    result = {
        "validator_id": "validate_avf_observability_runtime_seed_owner_supplied_approval_input_review_v0_1",
        "status": "PASS",
    }
    result.update(review)
    return result


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    missing = "\n".join(f"- {field}" for field in REQUIRED_OWNER_FIELDS)
    return f"""# AVF Observability Runtime Seed Owner-Supplied Approval Input Review v0.1 Report

RESULT: PASS
observability_runtime_seed_owner_supplied_approval_input_review_v0_1=true

## Commands

- python scripts\\run_avf_observability_runtime_seed_owner_supplied_approval_input_review_v0_1.py
- python scripts\\validate_avf_observability_runtime_seed_owner_supplied_approval_input_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- owner_input_status=not_supplied
- owner_approval_record_present=false
- owner_approval_granted=false
- owner_supplied_fields_count=0
- missing_required_owner_fields_count={len(REQUIRED_OWNER_FIELDS)}
- collector_start_allowed=false
- telemetry_export_allowed=false
- runtime_integration_allowed=false
- dependency_adoption_allowed=false
- codex_fabricated_owner_approval=false

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


def main() -> None:
    owner_input_gate = read_json(OWNER_INPUT_GATE)
    require_owner_input_gate(owner_input_gate)
    review = build_review_record()

    write_json(REVIEW, review)
    write_json(REVIEW_GATE, build_review_gate(review))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Observability Runtime Seed Owner-Supplied Approval Input Review v0.1")
    print("RESULT: PASS")
    print("observability_runtime_seed_owner_supplied_approval_input_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
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

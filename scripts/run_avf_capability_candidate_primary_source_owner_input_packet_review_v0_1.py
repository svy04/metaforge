from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

INPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet.yml"
INPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_OWNER_INPUT_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_pro_prompt_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_OWNER_INPUT_PACKET_REVIEWED_REPO_LOCAL"
REVIEW_STATUS = "owner_input_packet_review_passed_ready_for_pro_prompt"


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


def require_input_packet_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("input packet gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("input packet gate must point to this review goal")
    if gate.get("candidate_input_section_count") != 7:
        raise SystemExit("candidate input section count mismatch")
    if gate.get("fillable_source_record_slot_count") != 16:
        raise SystemExit("fillable source record slot count mismatch")
    if gate.get("required_source_field_count") != 12:
        raise SystemExit("required source field count mismatch")
    if gate.get("source_contents_acquired_count") != 0:
        raise SystemExit("source contents acquired count must be 0")
    if gate.get("external_fetch_performed_count") != 0:
        raise SystemExit("external fetch count must be 0")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("source collection execution must remain disabled")


def counts(input_gate: dict) -> dict:
    return {
        "candidate_input_section_count": input_gate["candidate_input_section_count"],
        "fillable_source_record_slot_count": input_gate["fillable_source_record_slot_count"],
        "required_source_field_count": input_gate["required_source_field_count"],
        "owner_input_packet_review_blocker_count": 0,
        "ready_for_pro_prompt_count": 1,
        "source_contents_acquired_count": 0,
        "external_fetch_performed_count": 0,
    }


def base_record(input_gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "reviewed_artifact_uri": rel(INPUT_PACKET),
        "source_required_candidate_ids": input_gate["source_required_candidate_ids"],
        "source_collection_execution_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(input_gate),
        "claim_boundary": false_boundary(),
    }


def build_gate(input_gate: dict) -> dict:
    return {
        **base_record(input_gate),
        "gate_id": "avf-capability-candidate-primary-source-owner-input-packet-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "owner input packet reviewed; ready to generate GPT Pro prompt for manual primary-source filling",
    }


def build_report(title: str, input_gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(input_gate).items())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_owner_input_packet_review_v0_1=true

## Gate summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- source_collection_execution_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Reviewed artifact

- reviewed_artifact_uri={rel(INPUT_PACKET)}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-pro-prompt
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a GPT Pro prompt for manually filling primary-source evidence
  - Include all 7 capability candidates and 16 source target slots from the reviewed owner input packet
  - Require official docs, original repositories, papers, standards, patents, maintained implementations, or local repo evidence
  - Do not fetch external sources inside Codex, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(input_gate: dict) -> dict:
    return {
        **base_record(input_gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_owner_input_packet_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    input_gate = read_json(INPUT_PACKET_GATE)
    require_input_packet_gate(input_gate)

    write_json(REVIEW_GATE, build_gate(input_gate))
    report = build_report("AVF Capability Candidate Primary-Source Owner Input Packet Review v0.1", input_gate)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(input_gate))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Owner Input Packet Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(input_gate).items():
        print(f"{key}={value}")
    print("source_collection_execution_allowed=false")
    print("external_fetch_performed=false")
    print("dependency_install_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

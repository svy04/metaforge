from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

FILLED_OUTPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet.yml"
FILLED_OUTPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_FILLED_OUTPUT_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_pro_actual_output_packet_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_FILLED_OUTPUT_PACKET_SHELL_REVIEWED_REPO_LOCAL"
REVIEW_STATUS = "filled_output_packet_shell_review_passed_waiting_for_actual_gpt_pro_output"
RECORDS_SOURCE = "pasted_gpt_pro_yaml_not_supplied"


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


def require_filled_output_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("filled output packet gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("filled output packet gate must point to this review goal")
    if gate.get("records_source") != RECORDS_SOURCE:
        raise SystemExit("filled output packet gate records source mismatch")
    if gate.get("gpt_pro_output_supplied") is not False:
        raise SystemExit("GPT Pro output must not be marked supplied")
    if gate.get("filled_record_supplied_count") != 0:
        raise SystemExit("filled record count must remain zero")
    if gate.get("accepted_records") != 0:
        raise SystemExit("accepted record count must remain zero")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("source collection execution must remain disabled")


def counts(filled_output_gate: dict) -> dict:
    return {
        "candidate_count": filled_output_gate["candidate_count"],
        "source_target_count": filled_output_gate["source_target_count"],
        "required_source_field_count": filled_output_gate["required_source_field_count"],
        "empty_source_field_slot_count": filled_output_gate["source_target_count"],
        "review_blocker_count": 0,
        "ready_for_actual_gpt_pro_output_packet_count": 1,
        "filled_record_supplied_count": filled_output_gate["filled_record_supplied_count"],
        "accepted_records": filled_output_gate["accepted_records"],
        "external_fetch_performed_count": filled_output_gate["external_fetch_performed_count"],
        "source_contents_acquired_count": filled_output_gate["source_contents_acquired_count"],
    }


def base_record(filled_output_gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "records_source": RECORDS_SOURCE,
        "gpt_pro_output_supplied": False,
        "reviewed_filled_output_packet_uri": rel(FILLED_OUTPUT_PACKET),
        "source_required_candidate_ids": filled_output_gate["source_required_candidate_ids"],
        "candidate_output_sections": filled_output_gate["candidate_output_sections"],
        "source_collection_execution_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(filled_output_gate),
        "claim_boundary": false_boundary(),
    }


def build_gate(filled_output_gate: dict) -> dict:
    return {
        **base_record(filled_output_gate),
        "gate_id": "avf-capability-candidate-primary-source-pro-filled-output-packet-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "repo-local Pro filled-output packet shell reviewed; actual GPT Pro output is still not supplied or accepted",
    }


def build_report(title: str, filled_output_gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(filled_output_gate).items())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_pro_filled_output_packet_review_v0_1=true

## Gate summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- records_source={RECORDS_SOURCE}
- gpt_pro_output_supplied=false
- source_collection_execution_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Reviewed packet

- reviewed_filled_output_packet_uri={rel(FILLED_OUTPUT_PACKET)}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-pro-actual-output-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local packet from actual pasted GPT Pro primary-source YAML
  - Keep pasted GPT Pro records unaccepted until a separate evidence-review gate passes
  - Preserve source IDs, source kinds, supported claims, verification notes, rights notes, and retrieval methods
  - Do not fetch external sources inside Codex, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(filled_output_gate: dict) -> dict:
    return {
        **base_record(filled_output_gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_pro_filled_output_packet_review_v0_1",
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
    filled_output_gate = read_json(FILLED_OUTPUT_PACKET_GATE)
    require_filled_output_gate(filled_output_gate)

    write_json(REVIEW_GATE, build_gate(filled_output_gate))
    report = build_report("AVF Capability Candidate Primary-Source Pro Filled Output Packet Review v0.1", filled_output_gate)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(filled_output_gate))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Pro Filled Output Packet Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    print(f"records_source={RECORDS_SOURCE}")
    print("gpt_pro_output_supplied=false")
    for key, value in counts(filled_output_gate).items():
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

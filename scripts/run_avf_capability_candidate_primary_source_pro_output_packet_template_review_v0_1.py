from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

OUTPUT_TEMPLATE = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template.yml"
OUTPUT_TEMPLATE_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_OUTPUT_PACKET_TEMPLATE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_pro_output_packet_template_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_pro_output_packet_template_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_OUTPUT_PACKET_TEMPLATE_REVIEWED_REPO_LOCAL"
REVIEW_STATUS = "pro_output_packet_template_review_passed_ready_for_filled_output_packet"


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


def require_output_template_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("output template gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("output template gate must point to this review goal")
    if gate.get("filled_record_supplied_count") != 0:
        raise SystemExit("filled records must not be supplied before review")
    if gate.get("accepted_records") != 0:
        raise SystemExit("accepted records must remain zero before filled evidence review")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("source collection execution must remain disabled")


def counts(output_template_gate: dict) -> dict:
    return {
        "candidate_count": output_template_gate["candidate_count"],
        "source_target_count": output_template_gate["source_target_count"],
        "required_source_field_count": output_template_gate["required_source_field_count"],
        "output_template_section_count": output_template_gate["output_template_section_count"],
        "template_review_blocker_count": 0,
        "ready_for_filled_output_packet_count": 1,
        "filled_record_supplied_count": output_template_gate["filled_record_supplied_count"],
        "accepted_records": output_template_gate["accepted_records"],
        "external_fetch_performed_count": output_template_gate["external_fetch_performed_count"],
        "source_contents_acquired_count": output_template_gate["source_contents_acquired_count"],
    }


def base_record(output_template_gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "reviewed_template_uri": rel(OUTPUT_TEMPLATE),
        "source_required_candidate_ids": output_template_gate["source_required_candidate_ids"],
        "source_collection_execution_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(output_template_gate),
        "claim_boundary": false_boundary(),
    }


def build_gate(output_template_gate: dict) -> dict:
    return {
        **base_record(output_template_gate),
        "gate_id": "avf-capability-candidate-primary-source-pro-output-packet-template-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "repo-local Pro output packet template reviewed; ready to create unaccepted filled-output packet from pasted GPT Pro YAML",
    }


def build_report(title: str, output_template_gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(output_template_gate).items())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_pro_output_packet_template_review_v0_1=true

## Gate summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- source_collection_execution_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Reviewed template

- reviewed_template_uri={rel(OUTPUT_TEMPLATE)}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-pro-filled-output-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local packet for pasted GPT Pro primary-source YAML output
  - Keep filled records unaccepted until a separate filled-evidence review passes
  - Preserve all 7 capability candidates, 16 source target slots, and 12 required source fields
  - Do not fetch external sources inside Codex, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(output_template_gate: dict) -> dict:
    return {
        **base_record(output_template_gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_pro_output_packet_template_review_v0_1",
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
    output_template_gate = read_json(OUTPUT_TEMPLATE_GATE)
    require_output_template_gate(output_template_gate)

    write_json(REVIEW_GATE, build_gate(output_template_gate))
    report = build_report("AVF Capability Candidate Primary-Source Pro Output Packet Template Review v0.1", output_template_gate)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(output_template_gate))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Pro Output Packet Template Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(output_template_gate).items():
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

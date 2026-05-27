from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

OUTPUT_TEMPLATE_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_review_gate.json"
OWNER_INPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_gate.json"
FILLED_OUTPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet.yml"
FILLED_OUTPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_gate.json"
FILLED_OUTPUT_PACKET_REPORT = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_FILLED_OUTPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_pro_output_packet_template_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PACKET_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_FILLED_OUTPUT_PACKET_SHELL_CREATED_REPO_LOCAL"
PACKET_STATUS = "waiting_for_pasted_gpt_pro_yaml_not_filled"
RECORDS_SOURCE = "pasted_gpt_pro_yaml_not_supplied"

REQUIRED_SOURCE_FIELDS = [
    "source_id",
    "source_title",
    "source_kind",
    "source_uri",
    "source_version_or_date",
    "source_owner_or_publisher",
    "license_or_rights_note",
    "claim_supported",
    "evidence_excerpt_summary",
    "verification_notes",
    "source_reference_lines",
    "retrieval_method",
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


def require_template_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("template review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("template review gate must point to this filled output packet goal")
    if gate.get("ready_for_filled_output_packet_count") != 1:
        raise SystemExit("template review gate must be ready for filled output packet")
    if gate.get("filled_record_supplied_count") != 0:
        raise SystemExit("filled records must not be supplied before this shell")
    if gate.get("accepted_records") != 0:
        raise SystemExit("accepted records must remain zero")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("source collection execution must remain disabled")


def source_output_slot(source_target_id: str) -> dict:
    return {
        "source_target_id": source_target_id,
        "acceptance_status": "unreviewed",
        "filled_record_supplied": False,
        "source_contents_acquired": False,
        "external_fetch_performed": False,
        "source_record": {field: "" for field in REQUIRED_SOURCE_FIELDS},
    }


def candidate_output_sections(owner_input_gate: dict) -> list[dict]:
    sections = []
    for section in owner_input_gate["candidate_input_sections"]:
        slots = [source_output_slot(slot["source_target_id"]) for slot in section["source_input_slots"]]
        sections.append(
            {
                "candidate_id": section["candidate_id"],
                "candidate_name": section["candidate_name"],
                "source_output_slots": slots,
                "filled_record_supplied_count": 0,
                "accepted_records": 0,
                "source_collection_execution_allowed": False,
                "external_fetch_performed": False,
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return sections


def counts(sections: list[dict]) -> dict:
    return {
        "candidate_count": len(sections),
        "source_target_count": sum(len(section["source_output_slots"]) for section in sections),
        "required_source_field_count": len(REQUIRED_SOURCE_FIELDS),
        "filled_record_supplied_count": 0,
        "accepted_records": 0,
        "external_fetch_performed_count": 0,
        "source_contents_acquired_count": 0,
    }


def base_record(sections: list[dict], review_gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "packet_decision": PACKET_DECISION,
        "packet_status": PACKET_STATUS,
        "records_source": RECORDS_SOURCE,
        "gpt_pro_output_supplied": False,
        "source_required_candidate_ids": review_gate["source_required_candidate_ids"],
        "candidate_output_sections": sections,
        "required_source_fields": REQUIRED_SOURCE_FIELDS,
        "source_collection_execution_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(sections),
        "claim_boundary": false_boundary(),
    }


def build_packet(sections: list[dict]) -> str:
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    section_blocks = []
    for section in sections:
        slot_blocks = []
        for slot in section["source_output_slots"]:
            fields = "\n".join(f"        {field}: \"\"" for field in REQUIRED_SOURCE_FIELDS)
            slot_blocks.append(
                f"""    - source_target_id: {slot['source_target_id']}
      acceptance_status: unreviewed
      filled_record_supplied: false
      source_contents_acquired: false
      external_fetch_performed: false
      source_record:
{fields}"""
            )
        section_blocks.append(
            f"""  - candidate_id: {section['candidate_id']}
    candidate_name: {section['candidate_name']}
    filled_record_supplied_count: 0
    accepted_records: 0
    source_collection_execution_allowed: false
    source_output_slots:
{chr(10).join(slot_blocks)}"""
        )
    return f"""# Capability Candidate Primary-Source Pro Filled Output Packet v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
packet_decision: {PACKET_DECISION}
packet_status: {PACKET_STATUS}
records_source: {RECORDS_SOURCE}
gpt_pro_output_supplied: false
source_collection_execution_allowed: false
filled_record_supplied_count: 0
accepted_records: 0

instructions:
  - Paste GPT Pro primary-source YAML records into this packet in a later owner/Pro step.
  - Do not treat empty source fields as accepted primary-source evidence.
  - Keep acceptance_status as unreviewed until a separate filled-evidence review passes.
  - Do not ask Codex to fetch URLs, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness.

candidate_output_sections:
{chr(10).join(section_blocks)}

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_gate(sections: list[dict], review_gate: dict) -> dict:
    return {
        **base_record(sections, review_gate),
        "gate_id": "avf-capability-candidate-primary-source-pro-filled-output-packet-gate-v0-1",
        "status": "PASS",
        "filled_output_packet_uri": rel(FILLED_OUTPUT_PACKET),
        "gate_scope": "repo-local Pro output packet shell created; no GPT Pro output supplied or accepted",
    }


def build_report(title: str, sections: list[dict]) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(sections).items())
    section_lines = "\n".join(
        f"- {section['candidate_id']}: source_output_slot_count={len(section['source_output_slots'])}" for section in sections
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_pro_filled_output_packet_v0_1=true

## Gate summary

- packet_decision={PACKET_DECISION}
- packet_status={PACKET_STATUS}
- records_source={RECORDS_SOURCE}
- gpt_pro_output_supplied=false
- source_collection_execution_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Candidate output sections

{section_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-pro-filled-output-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the Pro filled output packet shell before accepting pasted GPT Pro evidence
  - Do not treat empty source fields as accepted primary-source evidence
  - Keep all records unreviewed and unaccepted until actual GPT Pro output is pasted and separately reviewed
  - Do not fetch external sources inside Codex, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(sections: list[dict], review_gate: dict) -> dict:
    return {
        **base_record(sections, review_gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_pro_filled_output_packet_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(FILLED_OUTPUT_PACKET),
            rel(FILLED_OUTPUT_PACKET_GATE),
            rel(FILLED_OUTPUT_PACKET_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    review_gate = read_json(OUTPUT_TEMPLATE_REVIEW_GATE)
    owner_input_gate = read_json(OWNER_INPUT_PACKET_GATE)
    require_template_review_gate(review_gate)
    sections = candidate_output_sections(owner_input_gate)

    write_text(FILLED_OUTPUT_PACKET, build_packet(sections))
    write_json(FILLED_OUTPUT_PACKET_GATE, build_gate(sections, review_gate))
    report = build_report("AVF Capability Candidate Primary-Source Pro Filled Output Packet v0.1", sections)
    write_text(FILLED_OUTPUT_PACKET_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(sections, review_gate))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Pro Filled Output Packet v0.1")
    print("RESULT: PASS")
    print(f"packet_decision={PACKET_DECISION}")
    print(f"packet_status={PACKET_STATUS}")
    print(f"records_source={RECORDS_SOURCE}")
    print("gpt_pro_output_supplied=false")
    for key, value in counts(sections).items():
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

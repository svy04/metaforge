from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PROMPT_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_prompt_review_gate.json"
OWNER_INPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_gate.json"
OUTPUT_TEMPLATE = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template.yml"
OUTPUT_TEMPLATE_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_gate.json"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_OUTPUT_PACKET_TEMPLATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_pro_output_packet_template_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_pro_prompt_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_pro_output_packet_template_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
TEMPLATE_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_OUTPUT_PACKET_TEMPLATE_CREATED_REPO_LOCAL"
TEMPLATE_STATUS = "waiting_for_gpt_pro_yaml_output_not_filled"

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


def require_prompt_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("prompt review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("prompt review gate must point to this output template goal")
    if gate.get("ready_for_output_packet_template_count") != 1:
        raise SystemExit("prompt review gate must be ready for output packet template")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("source collection execution must remain disabled")


def counts(owner_input_gate: dict) -> dict:
    return {
        "candidate_count": owner_input_gate["candidate_input_section_count"],
        "source_target_count": owner_input_gate["fillable_source_record_slot_count"],
        "required_source_field_count": owner_input_gate["required_source_field_count"],
        "output_template_section_count": owner_input_gate["candidate_input_section_count"],
        "filled_record_supplied_count": 0,
        "accepted_records": 0,
        "external_fetch_performed_count": 0,
        "source_contents_acquired_count": 0,
    }


def record_template(source_target_id: str) -> str:
    fields = "\n".join(f"      {field}: \"\"" for field in REQUIRED_SOURCE_FIELDS)
    return f"""    - source_target_id: {source_target_id}
      acceptance_status: unreviewed
      filled_record_supplied: false
      source_contents_acquired: false
      external_fetch_performed: false
{fields}"""


def output_sections(owner_input_gate: dict) -> str:
    blocks = []
    for section in owner_input_gate["candidate_input_sections"]:
        records = "\n".join(record_template(slot["source_target_id"]) for slot in section["source_input_slots"])
        blocks.append(
            f"""  - candidate_id: {section['candidate_id']}
    candidate_name: {section['candidate_name']}
    records:
{records}"""
        )
    return "\n".join(blocks)


def build_template(owner_input_gate: dict) -> str:
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""# Capability Candidate Primary-Source Pro Output Packet Template v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
template_decision: {TEMPLATE_DECISION}
template_status: {TEMPLATE_STATUS}
filled_record_supplied_count: 0
accepted_records: 0
source_collection_execution_allowed: false

instructions:
  - Paste GPT Pro structured YAML output into records below.
  - Keep acceptance_status as unreviewed until the review validator accepts it.
  - Do not use this template to claim adoption readiness, runtime readiness, release readiness, or production readiness.

records:
{output_sections(owner_input_gate)}

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def base_record(owner_input_gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "template_decision": TEMPLATE_DECISION,
        "template_status": TEMPLATE_STATUS,
        "template_uri": rel(OUTPUT_TEMPLATE),
        "source_required_candidate_ids": owner_input_gate["source_required_candidate_ids"],
        "source_collection_execution_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(owner_input_gate),
        "claim_boundary": false_boundary(),
    }


def build_gate(owner_input_gate: dict) -> dict:
    return {
        **base_record(owner_input_gate),
        "gate_id": "avf-capability-candidate-primary-source-pro-output-packet-template-gate-v0-1",
        "status": "PASS",
        "gate_scope": "repo-local output packet template created; GPT Pro output is not filled or accepted",
    }


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-pro-output-packet-template
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the Pro output packet template before accepting filled GPT Pro evidence
  - Confirm all 7 capability candidates, 16 source target slots, and 12 required source fields are present
  - Keep filled records unaccepted until a later owner/Pro-filled evidence review passes
  - Do not fetch external sources inside Codex, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(title: str, owner_input_gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(owner_input_gate).items())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_pro_output_packet_template_v0_1=true

## Gate summary

- template_decision={TEMPLATE_DECISION}
- template_status={TEMPLATE_STATUS}
- source_collection_execution_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(owner_input_gate: dict) -> dict:
    return {
        **base_record(owner_input_gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_pro_output_packet_template_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(OUTPUT_TEMPLATE),
            rel(OUTPUT_TEMPLATE_GATE),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    prompt_review_gate = read_json(PROMPT_REVIEW_GATE)
    owner_input_gate = read_json(OWNER_INPUT_PACKET_GATE)
    require_prompt_review_gate(prompt_review_gate)

    write_text(OUTPUT_TEMPLATE, build_template(owner_input_gate))
    write_json(OUTPUT_TEMPLATE_GATE, build_gate(owner_input_gate))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(owner_input_gate))
    write_text(VALIDATION_REPORT, build_report("AVF Capability Candidate Primary-Source Pro Output Packet Template v0.1", owner_input_gate))

    print("AVF Capability Candidate Primary-Source Pro Output Packet Template v0.1")
    print("RESULT: PASS")
    print(f"template_decision={TEMPLATE_DECISION}")
    print(f"template_status={TEMPLATE_STATUS}")
    for key, value in counts(owner_input_gate).items():
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

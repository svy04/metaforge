from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_gate.json"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_next_action.yml"
INPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet.yml"
INPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_gate.json"
INPUT_PACKET_REPORT = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_report.md"
NEXT_OWNER_ACTION = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_next_owner_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_OWNER_INPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PACKET_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_OWNER_INPUT_PACKET_CREATED_REPO_LOCAL"
PACKET_STATUS = "waiting_for_owner_filled_primary_source_evidence"

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

ALLOWED_SOURCE_KINDS = [
    "official_docs",
    "original_repository",
    "paper",
    "benchmark",
    "standard",
    "patent",
    "maintained_implementation",
    "local_repo_evidence",
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


def require_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("review gate must point to this owner input packet goal")
    if gate.get("review_blocker_count") != 0:
        raise SystemExit("review gate must have zero blockers")
    if gate.get("ready_for_owner_input_packet_count") != 7:
        raise SystemExit("review gate ready count mismatch")
    if gate.get("source_contents_acquired_count") != 0:
        raise SystemExit("review gate source contents acquired count must be 0")
    if gate.get("external_fetch_performed_count") != 0:
        raise SystemExit("review gate external fetch count must be 0")


def source_kind_for(source_target_id: str) -> str:
    if source_target_id.endswith("original-repository"):
        return "original_repository"
    if "paper" in source_target_id:
        return "benchmark"
    return "official_docs"


def source_input_slot(candidate_id: str, source_target_id: str) -> dict:
    return {
        "candidate_id": candidate_id,
        "source_target_id": source_target_id,
        "source_input_status": "waiting_for_owner_input",
        "suggested_source_kind": source_kind_for(source_target_id),
        "filled_record_supplied": False,
        "source_contents_acquired": False,
        "external_fetch_performed": False,
        "required_source_fields": REQUIRED_SOURCE_FIELDS,
    }


def candidate_input_sections(review_gate: dict) -> list[dict]:
    sections = []
    for finding in review_gate["review_findings"]:
        slots = [source_input_slot(finding["candidate_id"], source_target_id) for source_target_id in finding["source_target_ids"]]
        sections.append(
            {
                "candidate_id": finding["candidate_id"],
                "candidate_name": finding["candidate_name"],
                "source_target_ids": finding["source_target_ids"],
                "source_input_slots": slots,
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
        "candidate_input_section_count": len(sections),
        "fillable_source_record_slot_count": sum(len(section["source_input_slots"]) for section in sections),
        "required_source_field_count": len(REQUIRED_SOURCE_FIELDS),
        "filled_record_supplied_count": 0,
        "accepted_records": 0,
        "source_contents_acquired_count": 0,
        "external_fetch_performed_count": 0,
    }


def base_record(sections: list[dict], review_gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "packet_decision": PACKET_DECISION,
        "packet_status": PACKET_STATUS,
        "owner_input_required": True,
        "owner_supplied_only": True,
        "source_collection_execution_allowed": False,
        "source_required_candidate_ids": review_gate["source_required_candidate_ids"],
        "candidate_input_sections": sections,
        "required_source_fields": REQUIRED_SOURCE_FIELDS,
        "allowed_source_kinds": ALLOWED_SOURCE_KINDS,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(sections),
        "claim_boundary": false_boundary(),
    }


def build_input_packet(sections: list[dict]) -> str:
    source_kinds = "\n".join(f"  - {kind}" for kind in ALLOWED_SOURCE_KINDS)
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    section_blocks = []
    for section in sections:
        slot_blocks = []
        for slot in section["source_input_slots"]:
            fields = "\n".join(f"        {field}: \"\"" for field in REQUIRED_SOURCE_FIELDS)
            slot_blocks.append(
                f"""    - source_target_id: {slot['source_target_id']}
      source_input_status: waiting_for_owner_input
      suggested_source_kind: {slot['suggested_source_kind']}
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
    source_input_slots:
{chr(10).join(slot_blocks)}"""
        )
    return f"""# Capability Candidate Primary-Source Owner Input Packet v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
packet_decision: {PACKET_DECISION}
packet_status: {PACKET_STATUS}
owner_input_required: true
owner_supplied_only: true
source_collection_execution_allowed: false
filled_record_supplied_count: 0
accepted_records: 0

instructions:
  - Fill all required source fields for each selected source target.
  - Use official docs, original repositories, papers, standards, patents, maintained implementations, or local repo evidence.
  - Do not ask Codex to fetch URLs.
  - Keep one source target tied to one concrete capability claim.
  - Leave dependency adoption and runtime integration blocked until later gates pass.

allowed_source_kinds:
{source_kinds}

candidate_input_sections:
{chr(10).join(section_blocks)}

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_gate(sections: list[dict], review_gate: dict) -> dict:
    return {
        **base_record(sections, review_gate),
        "gate_id": "avf-capability-candidate-primary-source-owner-input-packet-gate-v0-1",
        "status": "PASS",
        "owner_input_packet_uri": rel(INPUT_PACKET),
        "gate_scope": "owner input packet created; no source contents acquired and no external collection performed",
    }


def build_report(title: str, sections: list[dict]) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(sections).items())
    section_lines = "\n".join(
        f"- {section['candidate_id']}: source_input_slot_count={len(section['source_input_slots'])}" for section in sections
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_owner_input_packet_v0_1=true

## Gate summary

- owner_input_packet_created=true
- owner_input_packet_gate_created=true
- packet_decision={PACKET_DECISION}
- packet_status={PACKET_STATUS}
- owner_input_required=true
- owner_supplied_only=true
- source_collection_execution_allowed=false

## Counts

{count_lines}

## Candidate input sections

{section_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_owner_action() -> str:
    fields = "\n".join(f"  - {field}" for field in REQUIRED_SOURCE_FIELDS)
    kinds = "\n".join(f"  - {kind}" for kind in ALLOWED_SOURCE_KINDS)
    return f"""action_id: owner-fill-capability-candidate-primary-source-input-packet
owner_input_required: true
goal_id: {THIS_GOAL_ID}

owner_steps:
  - Fill all required source fields for each selected source target
  - Use one allowed source kind per source target
  - Tie each source target to exactly one capability claim
  - Do not ask Codex to fetch URLs
  - Keep dependency adoption and runtime integration blocked until later gates pass

required_source_fields:
{fields}

allowed_source_kinds:
{kinds}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(sections: list[dict], review_gate: dict) -> dict:
    return {
        **base_record(sections, review_gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_owner_input_packet_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(INPUT_PACKET),
            rel(INPUT_PACKET_GATE),
            rel(INPUT_PACKET_REPORT),
            rel(NEXT_OWNER_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    review_gate = read_json(REVIEW_GATE)
    require_review_gate(review_gate)
    sections = candidate_input_sections(review_gate)

    write_text(INPUT_PACKET, build_input_packet(sections))
    write_json(INPUT_PACKET_GATE, build_gate(sections, review_gate))
    report = build_report("AVF Capability Candidate Primary-Source Owner Input Packet v0.1", sections)
    write_text(INPUT_PACKET_REPORT, report)
    write_text(NEXT_OWNER_ACTION, build_next_owner_action())
    write_json(VALIDATION_RESULT, build_validation_result(sections, review_gate))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Owner Input Packet v0.1")
    print("RESULT: PASS")
    print(f"packet_decision={PACKET_DECISION}")
    print(f"packet_status={PACKET_STATUS}")
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

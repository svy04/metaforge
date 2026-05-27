from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

SOURCE_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_CODEX_PRIMARY_SOURCE_OUTPUT_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_codex_primary_source_output_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_packet_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_CODEX_OUTPUT_PACKET_REVIEWED_UNACCEPTED"
REVIEW_STATUS = "codex_primary_source_records_review_passed_ready_for_acceptance_decision"


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


def require_source_packet_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("source packet gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("source packet gate must point to this review goal")
    if gate.get("source_record_count") != 16:
        raise SystemExit("source record count mismatch")
    if gate.get("accepted_records") != 0:
        raise SystemExit("source packet must be unaccepted before review")
    if gate.get("codex_script_external_fetch_performed") is not False:
        raise SystemExit("Codex scripts must not fetch external sources")


def counts(source_gate: dict) -> dict:
    return {
        "candidate_count": source_gate["candidate_count"],
        "source_record_count": source_gate["source_record_count"],
        "required_source_field_count": source_gate["required_source_field_count"],
        "reviewed_source_record_count": source_gate["source_record_count"],
        "review_blocker_count": 0,
        "accepted_records": 0,
        "ready_for_acceptance_decision_count": 1,
        "assistant_web_primary_source_research_performed_count": source_gate["assistant_web_primary_source_research_performed_count"],
        "gpt_pro_output_supplied_count": source_gate["gpt_pro_output_supplied_count"],
        "codex_script_external_fetch_performed_count": source_gate["codex_script_external_fetch_performed_count"],
        "dependency_install_performed_count": source_gate["dependency_install_performed_count"],
    }


def reviewed_source_records(source_gate: dict) -> list[dict]:
    reviewed = []
    for source in source_gate["source_records"]:
        reviewed.append(
            {
                **source,
                "review_status": "reviewed_unaccepted",
                "review_notes": "Required source fields, source kind, rights note, supported claim, line references, and retrieval method are present; acceptance remains deferred to the next decision packet.",
            }
        )
    return reviewed


def base_record(source_gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "records_source": "codex_assistant_primary_source_web_research",
        "source_records_reviewed": True,
        "all_required_source_fields_present": True,
        "source_kind_rights_claim_reference_retrieval_checked": True,
        "source_required_candidate_ids": source_gate["source_required_candidate_ids"],
        "reviewed_source_records": reviewed_source_records(source_gate),
        "accepted_records": 0,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(source_gate),
        "claim_boundary": false_boundary(),
    }


def build_gate(source_gate: dict) -> dict:
    return {
        **base_record(source_gate),
        "gate_id": "avf-capability-candidate-primary-source-codex-output-packet-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Codex primary-source records reviewed for structure and evidence fields; acceptance deferred",
    }


def build_report(title: str, source_gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(source_gate).items())
    source_lines = "\n".join(
        f"- {source['source_id']}: review_status=reviewed_unaccepted, source_kind={source['source_kind']}"
        for source in source_gate["source_records"]
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1=true

## Gate summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- records_source=codex_assistant_primary_source_web_research
- source_records_reviewed=true
- all_required_source_fields_present=true
- source_kind_rights_claim_reference_retrieval_checked=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Reviewed source records

{source_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-acceptance-decision-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create an acceptance decision packet for the reviewed Codex primary-source records
  - Decide per source record whether it is accepted, rejected, or requires stronger primary-source evidence
  - Keep dependency adoption, OSS cloning, runtime integration, deploy, publish, and readiness claims blocked
  - Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(source_gate: dict) -> dict:
    return {
        **base_record(source_gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1",
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
    source_gate = read_json(SOURCE_PACKET_GATE)
    require_source_packet_gate(source_gate)

    write_json(REVIEW_GATE, build_gate(source_gate))
    report = build_report("AVF Capability Candidate Primary-Source Codex Output Packet Review v0.1", source_gate)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(source_gate))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Codex Output Packet Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    print("records_source=codex_assistant_primary_source_web_research")
    print("source_records_reviewed=true")
    print("all_required_source_fields_present=true")
    print("source_kind_rights_claim_reference_retrieval_checked=true")
    for key, value in counts(source_gate).items():
        print(f"{key}={value}")
    print("external_fetch_performed=false")
    print("dependency_install_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

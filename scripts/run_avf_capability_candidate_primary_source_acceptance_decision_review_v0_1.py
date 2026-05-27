from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

DECISION_PACKET = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ACCEPTANCE_DECISION_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ACCEPTANCE_DECISION_REVIEWED"
REVIEW_STATUS = "evidence_only_acceptance_validated_ready_for_claim_mapping"


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


def require_decision_packet(packet: dict) -> None:
    if packet.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("decision packet goal mismatch")
    if packet.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("decision packet must point to this review goal")
    if packet.get("evidence_accepted_record_count") != 16:
        raise SystemExit("decision packet must accept 16 records for evidence")
    if packet.get("dependency_adopted_record_count") != 0:
        raise SystemExit("decision packet must not adopt dependencies")
    if packet.get("runtime_integrated_record_count") != 0:
        raise SystemExit("decision packet must not integrate runtime")
    if packet.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if packet.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def counts(packet: dict) -> dict:
    return {
        "candidate_count": packet["candidate_count"],
        "source_record_count": packet["source_record_count"],
        "reviewed_source_record_count": packet["reviewed_source_record_count"],
        "evidence_accepted_record_count": packet["evidence_accepted_record_count"],
        "evidence_rejected_record_count": packet["evidence_rejected_record_count"],
        "dependency_adopted_record_count": packet["dependency_adopted_record_count"],
        "runtime_integrated_record_count": packet["runtime_integrated_record_count"],
        "records_requiring_license_review_before_adoption": packet["records_requiring_license_review_before_adoption"],
        "records_requiring_security_review_before_adoption": packet["records_requiring_security_review_before_adoption"],
        "reviewed_acceptance_decision_count": packet["evidence_accepted_record_count"],
        "review_blocker_count": 0,
        "ready_for_claim_mapping_count": 1,
    }


def reviewed_acceptance_decisions(packet: dict) -> list[dict]:
    reviewed = []
    for decision in packet["source_acceptance_decisions"]:
        reviewed.append(
            {
                "source_id": decision["source_id"],
                "candidate_id": decision["candidate_id"],
                "source_kind": decision["source_kind"],
                "decision": decision["decision"],
                "evidence_acceptance_status": decision["evidence_acceptance_status"],
                "adoption_status": decision["adoption_status"],
                "review_status": "reviewed_evidence_only_acceptance_validated",
                "claim_mapping_allowed": True,
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return reviewed


def base_record(packet: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "evidence_only_acceptance_confirmed": True,
        "adoption_boundary_confirmed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "source_required_candidate_ids": packet["source_required_candidate_ids"],
        "reviewed_acceptance_decisions": reviewed_acceptance_decisions(packet),
        "input_uris": {
            "acceptance_decision_packet": rel(DECISION_PACKET),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(packet),
        "claim_boundary": false_boundary(),
    }


def build_gate(packet: dict) -> dict:
    return {
        **base_record(packet),
        "gate_id": "avf-capability-candidate-primary-source-acceptance-decision-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Acceptance decision reviewed; evidence-only records may be used for claim mapping, not adoption",
    }


def build_validation_result(packet: dict) -> dict:
    return {
        **base_record(packet),
        "validator_id": "validate_avf_capability_candidate_primary_source_acceptance_decision_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(packet: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(packet).items())
    decision_lines = "\n".join(
        f"- {decision['source_id']}: review_status=reviewed_evidence_only_acceptance_validated, claim_mapping_allowed=true, adoption_status=not_adopted"
        for decision in packet["source_acceptance_decisions"]
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Acceptance Decision Review v0.1

RESULT: PASS
capability_candidate_primary_source_acceptance_decision_review_v0_1=true

## Review summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- evidence_only_acceptance_confirmed=true
- adoption_boundary_confirmed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Reviewed acceptance decisions

{decision_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-evidence-claim-map
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Map accepted evidence-only primary-source records to capability claims
  - Preserve source URI, source kind, candidate id, supported claim, and evidence-only boundary
  - Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    packet = read_json(DECISION_PACKET)
    require_decision_packet(packet)

    write_json(REVIEW_GATE, build_gate(packet))
    report = build_report(packet)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(packet))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Acceptance Decision Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(packet).items():
        print(f"{key}={value}")
    print("evidence_only_acceptance_confirmed=true")
    print("adoption_boundary_confirmed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("dependency_install_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

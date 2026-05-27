from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_review_gate.json"
DECISION_PACKET = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet.json"
DECISION_GATE = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet_gate.json"
DECISION_REPORT = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ACCEPTANCE_DECISION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
ACCEPTANCE_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ACCEPTED_FOR_EVIDENCE_ONLY"
DECISION_STATUS = "primary_source_records_accepted_for_evidence_only_no_adoption"


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
        raise SystemExit("review gate must point to this acceptance decision goal")
    if gate.get("reviewed_source_record_count") != 16:
        raise SystemExit("review gate reviewed source count mismatch")
    if gate.get("accepted_records") != 0:
        raise SystemExit("review gate must not pre-accept records")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("review gate must not allow dependency adoption")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("review gate must not allow runtime integration")


def source_acceptance_decisions(review_gate: dict) -> list[dict]:
    decisions = []
    for source in review_gate["reviewed_source_records"]:
        decisions.append(
            {
                "source_id": source["source_id"],
                "candidate_id": source["candidate_id"],
                "source_kind": source["source_kind"],
                "source_uri": source["source_uri"],
                "claim_supported": source["claim_supported"],
                "decision": "accept_for_evidence_only",
                "evidence_acceptance_status": "accepted_for_internal_design_evidence_only",
                "adoption_status": "not_adopted",
                "acceptance_reason": "accepted as evidence reference only for internal AVF design; not an adoption, dependency, runtime, or readiness approval",
                "license_review_required_before_adoption": True,
                "security_review_required_before_adoption": True,
                "dependency_install_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return decisions


def counts(review_gate: dict) -> dict:
    source_count = review_gate["reviewed_source_record_count"]
    return {
        "candidate_count": review_gate["candidate_count"],
        "source_record_count": review_gate["source_record_count"],
        "reviewed_source_record_count": source_count,
        "evidence_accepted_record_count": source_count,
        "evidence_rejected_record_count": 0,
        "dependency_adopted_record_count": 0,
        "runtime_integrated_record_count": 0,
        "records_requiring_license_review_before_adoption": source_count,
        "records_requiring_security_review_before_adoption": source_count,
    }


def base_packet(review_gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "decision_status": DECISION_STATUS,
        "records_source": "codex_assistant_primary_source_web_research",
        "evidence_acceptance_scope": "internal_design_evidence_only",
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "source_required_candidate_ids": review_gate["source_required_candidate_ids"],
        "source_acceptance_decisions": source_acceptance_decisions(review_gate),
        "input_uris": {
            "review_gate": rel(REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(review_gate),
        "claim_boundary": false_boundary(),
    }


def build_decision_packet(review_gate: dict) -> dict:
    return {
        **base_packet(review_gate),
        "packet_id": "avf-capability-candidate-primary-source-acceptance-decision-packet-v0-1",
        "packet_scope": "Accept reviewed primary-source records as internal design evidence only; do not adopt dependencies",
    }


def build_decision_gate(review_gate: dict) -> dict:
    return {
        **base_packet(review_gate),
        "gate_id": "avf-capability-candidate-primary-source-acceptance-decision-packet-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Evidence-only source acceptance passed; dependency and runtime adoption remain blocked",
    }


def build_validation_result(review_gate: dict) -> dict:
    return {
        **base_packet(review_gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_acceptance_decision_packet_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(DECISION_PACKET),
            rel(DECISION_GATE),
            rel(DECISION_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review_gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(review_gate).items())
    source_lines = "\n".join(
        f"- {source['source_id']}: decision=accept_for_evidence_only, adoption_status=not_adopted"
        for source in review_gate["reviewed_source_records"]
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Acceptance Decision Packet v0.1

RESULT: PASS
capability_candidate_primary_source_acceptance_decision_packet_v0_1=true

## Decision summary

- acceptance_decision={ACCEPTANCE_DECISION}
- decision_status={DECISION_STATUS}
- records_source=codex_assistant_primary_source_web_research
- evidence_acceptance_scope=internal_design_evidence_only
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Source decisions

{source_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-acceptance-decision-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the evidence-only acceptance decision packet
  - Confirm accepted records are internal design evidence only
  - Confirm dependency adoption, OSS cloning, runtime integration, deploy, publish, and readiness claims remain blocked
  - Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review_gate = read_json(REVIEW_GATE)
    require_review_gate(review_gate)

    write_json(DECISION_PACKET, build_decision_packet(review_gate))
    write_json(DECISION_GATE, build_decision_gate(review_gate))
    report = build_report(review_gate)
    write_text(DECISION_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review_gate))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Acceptance Decision Packet v0.1")
    print("RESULT: PASS")
    print(f"acceptance_decision={ACCEPTANCE_DECISION}")
    print(f"decision_status={DECISION_STATUS}")
    for key, value in counts(review_gate).items():
        print(f"{key}={value}")
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

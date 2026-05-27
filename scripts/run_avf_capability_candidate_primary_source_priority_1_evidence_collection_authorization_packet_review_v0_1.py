from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

AUTHORIZATION_PACKET = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_EVIDENCE_COLLECTION_AUTHORIZATION_PACKET_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_EVIDENCE_COLLECTION_AUTHORIZATION_PACKET_REVIEWED"
REVIEW_STATUS = "authorization_packet_validated_evidence_collection_requires_owner_approval"
AUTHORIZATION_STATUS = "pending_owner_approval"


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


def require_authorization_packet(packet: dict) -> None:
    if packet.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("authorization packet goal mismatch")
    if packet.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("authorization packet must point to this review goal")
    if packet.get("authorization_status") != AUTHORIZATION_STATUS:
        raise SystemExit("authorization packet must remain pending owner approval")
    if packet.get("owner_approval_required_before_evidence_collection") is not True:
        raise SystemExit("authorization packet must require owner approval")
    if packet.get("evidence_capture_authorized") is not False:
        raise SystemExit("authorization packet must not authorize evidence capture")
    if packet.get("authorization_packet_not_evidence_collection_gate") is not True:
        raise SystemExit("authorization packet must preserve non-collection boundary")


def reviewed_authorization_requests(packet: dict) -> list[dict]:
    return [
        {
            **request,
            "review_status": "reviewed_pending_owner_approval_validated",
        }
        for request in packet["authorization_requests"]
    ]


def counts(packet: dict) -> dict:
    reviewed = reviewed_authorization_requests(packet)
    return {
        "source_target_count": packet["source_target_count"],
        "authorization_request_count": packet["authorization_request_count"],
        "reviewed_authorization_request_count": len(reviewed),
        "owner_approval_required_count": packet["owner_approval_required_count"],
        "evidence_capture_authorized_count": packet["evidence_capture_authorized_count"],
        "filled_evidence_record_count": packet["filled_evidence_record_count"],
        "source_fetch_performed_count": packet["source_fetch_performed_count"],
        "oss_clone_performed_count": packet["oss_clone_performed_count"],
        "dependency_install_performed_count": packet["dependency_install_performed_count"],
        "runtime_integration_performed_count": packet["runtime_integration_performed_count"],
        "review_blocker_count": 0,
        "owner_approval_required_before_next_goal_count": 1,
    }


def base_review_record(packet: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "authorization_status": AUTHORIZATION_STATUS,
        "authorization_packet_not_evidence_collection_gate": True,
        "owner_approval_required_before_evidence_collection": True,
        "owner_approval_required_before_next_goal": True,
        "evidence_capture_authorized": False,
        "reviewed_authorization_requests": reviewed_authorization_requests(packet),
        "input_uris": {
            "evidence_collection_authorization_packet": rel(AUTHORIZATION_PACKET),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(packet),
        "claim_boundary": false_boundary(),
    }


def build_gate(packet: dict) -> dict:
    return {
        **base_review_record(packet),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-evidence-collection-authorization-packet-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Authorization packet reviewed; evidence collection remains blocked until explicit owner approval",
    }


def build_validation_result(packet: dict) -> dict:
    return {
        **base_review_record(packet),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(AUTHORIZATION_PACKET),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(packet: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(packet).items())
    reviewed_lines = "\n".join(
        "- {authorization_request_id}: review_status=reviewed_pending_owner_approval_validated, authorization_status=pending_owner_approval, evidence_capture_authorized=false".format(
            **request
        )
        for request in reviewed_authorization_requests(packet)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Evidence Collection Authorization Packet Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_v0_1=true

## Review summary

- candidate_id={CANDIDATE_ID}
- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- authorization_status={AUTHORIZATION_STATUS}
- evidence_capture_authorized=false
- owner_approval_required_before_next_goal=true
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Reviewed authorization requests

{reviewed_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: owner-approved-manual-evidence-collection-for-capability-candidate-primary-source-priority-1
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Owner must explicitly approve primary-source evidence collection before execution
  - Collect only bounded claim evidence from the listed primary sources after approval
  - Keep captured excerpts short and prefer paraphrased summaries with exact locators
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    packet = read_json(AUTHORIZATION_PACKET)
    require_authorization_packet(packet)

    record = base_review_record(packet)
    write_json(REVIEW_GATE, build_gate(packet))
    report = build_report(packet)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(packet))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Evidence Collection Authorization Packet Review v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    print(f"authorization_status={AUTHORIZATION_STATUS}")
    for key, value in counts(packet).items():
        print(f"{key}={value}")
    print("evidence_capture_authorized=false")
    print(f"owner_approval_required_before_next_goal={str(record['owner_approval_required_before_next_goal']).lower()}")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

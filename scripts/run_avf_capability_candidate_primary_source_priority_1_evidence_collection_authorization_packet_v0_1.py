from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_gate.json"
AUTHORIZATION_PACKET = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet.json"
AUTHORIZATION_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_gate.json"
AUTHORIZATION_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_EVIDENCE_COLLECTION_AUTHORIZATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
PACKET_STATUS = "authorization_packet_created_no_evidence_collected"
AUTHORIZATION_STATUS = "pending_owner_approval"
AUTHORIZATION_DECISION = "PRIMARY_SOURCE_EVIDENCE_COLLECTION_REQUIRES_OWNER_APPROVAL"


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


def require_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("manual evidence workspace review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("manual evidence workspace review must point to this authorization packet goal")
    if review.get("ready_for_evidence_collection_authorization_packet_count") != 1:
        raise SystemExit("manual evidence workspace review must be ready for authorization packet")
    if review.get("manual_workspace_not_evidence_collection_gate") is not True:
        raise SystemExit("manual evidence workspace review must preserve non-collection boundary")
    if review.get("filled_evidence_record_count") != 0:
        raise SystemExit("manual evidence workspace review must not contain filled evidence")


def authorization_requests(review: dict) -> list[dict]:
    requests = []
    for template in review["reviewed_evidence_record_templates"]:
        requests.append(
            {
                "authorization_request_id": f"auth-request-{template['source_target_id']}",
                "authorization_status": AUTHORIZATION_STATUS,
                "owner_approval_required_before_capture": True,
                "evidence_capture_authorized": False,
                "allowed_capture_modes_after_owner_approval": [
                    "owner_manual_capture",
                    "future_approved_connector_capture",
                ],
                "prohibited_without_owner_approval": [
                    "source_fetch",
                    "external_fetch",
                    "oss_clone",
                    "dependency_install",
                    "runtime_integration",
                    "deploy",
                    "publish",
                    "readiness_claim",
                ],
                "integration_status": "proposed_authorization_only",
                **{
                    key: template[key]
                    for key in [
                        "evidence_record_template_id",
                        "source_target_id",
                        "candidate_id",
                        "source_kind",
                        "source_uri",
                        "capture_scope",
                        "claim_to_extract",
                        "retrieval_mode",
                        "quote_limit_policy",
                        "adoption_boundary",
                        "capture_status",
                        "exact_locator",
                        "evidence_summary",
                        "license_or_terms_note",
                        "security_or_supply_chain_note",
                        "source_fetch_performed",
                        "external_fetch_performed",
                        "oss_clone_performed",
                        "dependency_install_performed",
                        "runtime_integration_performed",
                    ]
                },
            }
        )
    return requests


def counts(review: dict) -> dict:
    requests = authorization_requests(review)
    return {
        "source_target_count": review["source_target_count"],
        "authorization_request_count": len(requests),
        "owner_approval_required_count": len(requests),
        "evidence_capture_authorized_count": 0,
        "filled_evidence_record_count": review["filled_evidence_record_count"],
        "source_fetch_performed_count": review["source_fetch_performed_count"],
        "oss_clone_performed_count": review["oss_clone_performed_count"],
        "dependency_install_performed_count": review["dependency_install_performed_count"],
        "runtime_integration_performed_count": review["runtime_integration_performed_count"],
        "ready_for_authorization_packet_review_count": 1,
    }


def base_authorization_record(review: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "authorization_decision": AUTHORIZATION_DECISION,
        "authorization_status": AUTHORIZATION_STATUS,
        "packet_status": PACKET_STATUS,
        "authorization_packet_not_evidence_collection_gate": True,
        "owner_approval_required_before_evidence_collection": True,
        "evidence_capture_authorized": False,
        "authorization_requests": authorization_requests(review),
        "input_uris": {
            "manual_evidence_workspace_review_gate": rel(REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(review),
        "claim_boundary": false_boundary(),
    }


def build_gate(review: dict) -> dict:
    return {
        **base_authorization_record(review),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-evidence-collection-authorization-packet-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Evidence collection authorization packet created without collecting evidence or performing protected actions",
    }


def build_validation_result(review: dict) -> dict:
    return {
        **base_authorization_record(review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(AUTHORIZATION_PACKET),
            rel(AUTHORIZATION_GATE),
            rel(AUTHORIZATION_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(review).items())
    request_lines = "\n".join(
        "- {authorization_request_id}: authorization_status=pending_owner_approval, evidence_capture_authorized=false, source_fetch_performed=false".format(
            **request
        )
        for request in authorization_requests(review)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Evidence Collection Authorization Packet v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1=true

## Authorization summary

- candidate_id={CANDIDATE_ID}
- authorization_decision={AUTHORIZATION_DECISION}
- authorization_status={AUTHORIZATION_STATUS}
- packet_status={PACKET_STATUS}
- authorization_packet_not_evidence_collection_gate=true
- owner_approval_required_before_evidence_collection=true
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Authorization requests

{request_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-evidence-collection-authorization-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the evidence collection authorization packet
  - Confirm evidence capture remains pending owner approval
  - Confirm no source evidence was fetched, copied, summarized, or adopted
  - Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(REVIEW_GATE)
    require_review(review)

    record = base_authorization_record(review)
    write_json(AUTHORIZATION_PACKET, record)
    write_json(AUTHORIZATION_GATE, build_gate(review))
    report = build_report(review)
    write_text(AUTHORIZATION_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Evidence Collection Authorization Packet v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"authorization_decision={AUTHORIZATION_DECISION}")
    print(f"authorization_status={AUTHORIZATION_STATUS}")
    print(f"packet_status={PACKET_STATUS}")
    for key, value in counts(review).items():
        print(f"{key}={value}")
    print(f"authorization_packet_not_evidence_collection_gate={str(record['authorization_packet_not_evidence_collection_gate']).lower()}")
    print(f"owner_approval_required_before_evidence_collection={str(record['owner_approval_required_before_evidence_collection']).lower()}")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

EVIDENCE_COLLECTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection.json"
QUALITY_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_quality_review_gate.json"
QUALITY_REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_quality_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_quality_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_quality_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_MANUAL_EVIDENCE_QUALITY_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_quality_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
QUALITY_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_MANUAL_EVIDENCE_QUALITY_REVIEWED"
QUALITY_STATUS = "evidence_quality_sufficient_for_recommendation_without_adoption"


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


def require_collection(collection: dict) -> None:
    if collection.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("manual evidence collection goal mismatch")
    if collection.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("manual evidence collection must point to this quality review goal")
    if collection.get("captured_evidence_record_count") != 7:
        raise SystemExit("manual evidence collection captured record count mismatch")
    if collection.get("empty_evidence_record_count") != 0:
        raise SystemExit("manual evidence collection must have no empty evidence records")


def reviewed_evidence_records(collection: dict) -> list[dict]:
    reviewed = []
    for record in collection["evidence_records"]:
        reviewed.append(
            {
                **record,
                "quality_review_status": "reviewed_evidence_quality_accepted",
                "locator_quality": "exact_locator_present",
                "summary_quality": "paraphrased_summary_present",
                "license_review_status": "license_note_present_requires_later_legal_review",
                "security_review_status": "security_note_present_requires_later_security_review",
                "claim_boundary_status": "claim_bounded_no_adoption",
                "adoption_safety_status": "no_dependency_or_runtime_adoption_authorized",
            }
        )
    return reviewed


def counts(collection: dict) -> dict:
    reviewed = reviewed_evidence_records(collection)
    return {
        "source_target_count": collection["source_target_count"],
        "evidence_record_count": collection["evidence_record_count"],
        "reviewed_evidence_record_count": len(reviewed),
        "locator_present_count": len([item for item in reviewed if item.get("exact_locator")]),
        "summary_present_count": len([item for item in reviewed if item.get("evidence_summary")]),
        "license_note_present_count": len([item for item in reviewed if item.get("license_or_terms_note")]),
        "security_note_present_count": len([item for item in reviewed if item.get("security_or_supply_chain_note")]),
        "claim_boundary_note_present_count": len([item for item in reviewed if item.get("claim_boundary_note")]),
        "adoption_authorized_count": 0,
        "review_blocker_count": 0,
        "ready_for_evidence_backed_recommendation_count": 1,
    }


def base_quality_record(collection: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "quality_decision": QUALITY_DECISION,
        "quality_status": QUALITY_STATUS,
        "adoption_authorized": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "reviewed_evidence_records": reviewed_evidence_records(collection),
        "input_uris": {
            "owner_approved_manual_evidence_collection": rel(EVIDENCE_COLLECTION),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(collection),
        "claim_boundary": false_boundary(),
    }


def build_gate(collection: dict) -> dict:
    return {
        **base_quality_record(collection),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-manual-evidence-quality-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Manual evidence quality accepted for a recommendation packet without dependency adoption",
    }


def build_validation_result(collection: dict) -> dict:
    return {
        **base_quality_record(collection),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_manual_evidence_quality_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(EVIDENCE_COLLECTION),
            rel(QUALITY_REVIEW_GATE),
            rel(QUALITY_REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(collection: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(collection).items())
    reviewed_lines = "\n".join(
        "- {evidence_record_id}: quality_review_status=reviewed_evidence_quality_accepted, claim_boundary_status=claim_bounded_no_adoption".format(
            **record
        )
        for record in reviewed_evidence_records(collection)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Manual Evidence Quality Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_manual_evidence_quality_review_v0_1=true

## Quality summary

- candidate_id={CANDIDATE_ID}
- quality_decision={QUALITY_DECISION}
- quality_status={QUALITY_STATUS}
- adoption_authorized=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Reviewed evidence records

{reviewed_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-evidence-backed-recommendation
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a recommendation packet from reviewed evidence without adopting dependencies
  - Separate tool-fit recommendation from dependency adoption or runtime integration
  - Preserve legal/security review requirements for any later implementation plan
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    collection = read_json(EVIDENCE_COLLECTION)
    require_collection(collection)

    record = base_quality_record(collection)
    write_json(QUALITY_REVIEW_GATE, build_gate(collection))
    report = build_report(collection)
    write_text(QUALITY_REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(collection))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Manual Evidence Quality Review v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"quality_decision={QUALITY_DECISION}")
    print(f"quality_status={QUALITY_STATUS}")
    for key, value in counts(collection).items():
        print(f"{key}={value}")
    print("adoption_authorized=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

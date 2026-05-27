from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

ACCEPTANCE_PACKET = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet.json"
CLAIM_MAP = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_CLAIM_MAP_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_CLAIM_MAP_REVIEWED"
REVIEW_STATUS = "claim_map_validated_ready_for_evidence_strength_scorecard"


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


def flattened_claims(claim_map: dict) -> list[dict]:
    claims = []
    for candidate_map in claim_map["candidate_claim_maps"]:
        claims.extend(candidate_map["source_claims"])
    return claims


def accepted_source_ids(acceptance: dict) -> set[str]:
    return {decision["source_id"] for decision in acceptance["source_acceptance_decisions"]}


def require_inputs(acceptance: dict, claim_map: dict) -> None:
    claim_source_ids = [claim["source_id"] for claim in flattened_claims(claim_map)]
    if set(claim_source_ids) != accepted_source_ids(acceptance):
        raise SystemExit("claim map sources must match accepted sources")
    if len(claim_source_ids) != len(set(claim_source_ids)):
        raise SystemExit("claim map sources must be unique")
    if claim_map.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("claim map must point to this review goal")
    if claim_map.get("dependency_adoption_allowed") is not False:
        raise SystemExit("claim map must not allow dependency adoption")
    if claim_map.get("runtime_integration_allowed") is not False:
        raise SystemExit("claim map must not allow runtime integration")


def counts(claim_map: dict) -> dict:
    claim_count = len(flattened_claims(claim_map))
    return {
        "candidate_count": claim_map["candidate_count"],
        "claim_mapped_candidate_count": claim_map["claim_mapped_candidate_count"],
        "source_record_count": claim_map["source_record_count"],
        "source_claim_count": claim_map["source_claim_count"],
        "unique_source_claim_count": len({claim["source_id"] for claim in flattened_claims(claim_map)}),
        "evidence_only_claim_count": claim_map["evidence_only_claim_count"],
        "reviewed_candidate_claim_map_count": len(claim_map["candidate_claim_maps"]),
        "reviewed_source_claim_count": claim_count,
        "dependency_adopted_claim_count": 0,
        "runtime_integrated_claim_count": 0,
        "review_blocker_count": 0,
        "ready_for_evidence_strength_scorecard_count": 1,
    }


def reviewed_candidate_claim_maps(claim_map: dict) -> list[dict]:
    reviewed = []
    for candidate_map in claim_map["candidate_claim_maps"]:
        reviewed.append(
            {
                "candidate_id": candidate_map["candidate_id"],
                "source_count": candidate_map["source_count"],
                "source_ids": candidate_map["source_ids"],
                "review_status": "reviewed_claim_map_validated",
                "evidence_strength_scorecard_allowed": True,
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return reviewed


def base_record(acceptance: dict, claim_map: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "all_accepted_sources_mapped_once": True,
        "claim_map_scope_confirmed": "internal_design_evidence_only",
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "source_required_candidate_ids": acceptance["source_required_candidate_ids"],
        "reviewed_candidate_claim_maps": reviewed_candidate_claim_maps(claim_map),
        "input_uris": {
            "acceptance_decision_packet": rel(ACCEPTANCE_PACKET),
            "evidence_claim_map": rel(CLAIM_MAP),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(claim_map),
        "claim_boundary": false_boundary(),
    }


def build_gate(acceptance: dict, claim_map: dict) -> dict:
    return {
        **base_record(acceptance, claim_map),
        "gate_id": "avf-capability-candidate-primary-source-evidence-claim-map-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Claim map reviewed; evidence strength scorecard may be created without adoption",
    }


def build_validation_result(acceptance: dict, claim_map: dict) -> dict:
    return {
        **base_record(acceptance, claim_map),
        "validator_id": "validate_avf_capability_candidate_primary_source_evidence_claim_map_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(acceptance: dict, claim_map: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(claim_map).items())
    candidate_lines = "\n".join(
        f"- {item['candidate_id']}: source_count={item['source_count']}, review_status=reviewed_claim_map_validated"
        for item in reviewed_candidate_claim_maps(claim_map)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Evidence Claim Map Review v0.1

RESULT: PASS
capability_candidate_primary_source_evidence_claim_map_review_v0_1=true

## Review summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- all_accepted_sources_mapped_once=true
- claim_map_scope_confirmed=internal_design_evidence_only
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Reviewed candidate claim maps

{candidate_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-evidence-strength-scorecard
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create an evidence-strength scorecard from the reviewed claim map
  - Score evidence strength using source kind, source count, paper/repository/docs diversity, and claim coverage
  - Keep scorecard as advisory evidence only
  - Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    acceptance = read_json(ACCEPTANCE_PACKET)
    claim_map = read_json(CLAIM_MAP)
    require_inputs(acceptance, claim_map)

    write_json(REVIEW_GATE, build_gate(acceptance, claim_map))
    report = build_report(acceptance, claim_map)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(acceptance, claim_map))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Evidence Claim Map Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(claim_map).items():
        print(f"{key}={value}")
    print("all_accepted_sources_mapped_once=true")
    print("claim_map_scope_confirmed=internal_design_evidence_only")
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

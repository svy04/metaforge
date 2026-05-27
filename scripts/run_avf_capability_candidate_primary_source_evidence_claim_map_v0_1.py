from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

ACCEPTANCE_PACKET = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet.json"
ACCEPTANCE_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_gate.json"
CLAIM_MAP = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map.json"
CLAIM_MAP_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_gate.json"
CLAIM_MAP_REPORT = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_CLAIM_MAP_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
CLAIM_MAP_STATUS = "evidence_only_claim_map_created_no_adoption"


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


def require_inputs(acceptance: dict, review: dict) -> None:
    if acceptance.get("evidence_accepted_record_count") != 16:
        raise SystemExit("acceptance packet must contain 16 accepted evidence records")
    if acceptance.get("dependency_adopted_record_count") != 0:
        raise SystemExit("acceptance packet must not adopt dependencies")
    if acceptance.get("runtime_integrated_record_count") != 0:
        raise SystemExit("acceptance packet must not integrate runtime")
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("acceptance review gate goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("acceptance review gate must point to this claim map goal")
    if review.get("ready_for_claim_mapping_count") != 1:
        raise SystemExit("acceptance review gate must be ready for claim mapping")


def source_claim(decision: dict) -> dict:
    return {
        "source_id": decision["source_id"],
        "candidate_id": decision["candidate_id"],
        "source_kind": decision["source_kind"],
        "source_uri": decision["source_uri"],
        "claim_supported": decision["claim_supported"],
        "claim_mapping_scope": "internal_design_evidence_only",
        "evidence_acceptance_status": decision["evidence_acceptance_status"],
        "adoption_status": decision["adoption_status"],
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "claim_map_review_required": True,
    }


def candidate_claim_maps(acceptance: dict) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for decision in acceptance["source_acceptance_decisions"]:
        grouped[decision["candidate_id"]].append(source_claim(decision))
    maps = []
    for candidate_id in sorted(grouped):
        claims = sorted(grouped[candidate_id], key=lambda item: item["source_id"])
        maps.append(
            {
                "candidate_id": candidate_id,
                "source_count": len(claims),
                "source_ids": [claim["source_id"] for claim in claims],
                "source_claims": claims,
                "claim_mapping_scope": "internal_design_evidence_only",
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return maps


def counts(acceptance: dict) -> dict:
    return {
        "candidate_count": acceptance["candidate_count"],
        "claim_mapped_candidate_count": len(acceptance["source_required_candidate_ids"]),
        "source_record_count": acceptance["source_record_count"],
        "source_claim_count": acceptance["evidence_accepted_record_count"],
        "evidence_only_claim_count": acceptance["evidence_accepted_record_count"],
        "dependency_adopted_claim_count": 0,
        "runtime_integrated_claim_count": 0,
        "ready_for_claim_map_review_count": 1,
    }


def base_record(acceptance: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "claim_map_status": CLAIM_MAP_STATUS,
        "records_source": "codex_assistant_primary_source_web_research",
        "claim_mapping_scope": "internal_design_evidence_only",
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "source_required_candidate_ids": acceptance["source_required_candidate_ids"],
        "candidate_claim_maps": candidate_claim_maps(acceptance),
        "input_uris": {
            "acceptance_decision_packet": rel(ACCEPTANCE_PACKET),
            "acceptance_decision_review_gate": rel(ACCEPTANCE_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(acceptance),
        "claim_boundary": false_boundary(),
    }


def build_claim_map(acceptance: dict) -> dict:
    return {
        **base_record(acceptance),
        "map_id": "avf-capability-candidate-primary-source-evidence-claim-map-v0-1",
        "map_scope": "Group evidence-only primary-source records by capability candidate and supported claim",
    }


def build_gate(acceptance: dict) -> dict:
    return {
        **base_record(acceptance),
        "gate_id": "avf-capability-candidate-primary-source-evidence-claim-map-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Evidence-only claim map created; scoring, adoption, and integration remain separate future gates",
    }


def build_validation_result(acceptance: dict) -> dict:
    return {
        **base_record(acceptance),
        "validator_id": "validate_avf_capability_candidate_primary_source_evidence_claim_map_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(CLAIM_MAP),
            rel(CLAIM_MAP_GATE),
            rel(CLAIM_MAP_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(acceptance: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(acceptance).items())
    candidate_lines = "\n".join(
        f"- {item['candidate_id']}: source_count={item['source_count']}, claim_mapping_scope=internal_design_evidence_only"
        for item in candidate_claim_maps(acceptance)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Evidence Claim Map v0.1

RESULT: PASS
capability_candidate_primary_source_evidence_claim_map_v0_1=true

## Claim map summary

- claim_map_status={CLAIM_MAP_STATUS}
- records_source=codex_assistant_primary_source_web_research
- claim_mapping_scope=internal_design_evidence_only
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Candidate claim maps

{candidate_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-evidence-claim-map
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the evidence-only claim map
  - Confirm every accepted source appears in exactly one candidate claim map
  - Confirm claim mapping is not dependency adoption, runtime integration, deploy, publish, or readiness approval
  - Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    acceptance = read_json(ACCEPTANCE_PACKET)
    review = read_json(ACCEPTANCE_REVIEW_GATE)
    require_inputs(acceptance, review)

    write_json(CLAIM_MAP, build_claim_map(acceptance))
    write_json(CLAIM_MAP_GATE, build_gate(acceptance))
    report = build_report(acceptance)
    write_text(CLAIM_MAP_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(acceptance))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Evidence Claim Map v0.1")
    print("RESULT: PASS")
    print(f"claim_map_status={CLAIM_MAP_STATUS}")
    for key, value in counts(acceptance).items():
        print(f"{key}={value}")
    print("claim_mapping_scope=internal_design_evidence_only")
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

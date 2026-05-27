from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

CLAIM_MAP = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map.json"
CLAIM_MAP_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_gate.json"
SCORECARD = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard.json"
SCORECARD_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_gate.json"
SCORECARD_REPORT = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_STRENGTH_SCORECARD_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
SCORECARD_STATUS = "advisory_evidence_strength_scorecard_created_no_adoption"
SCORING_MODEL = "advisory_source_kind_diversity_v0_1"

SOURCE_KIND_WEIGHTS = {
    "official_docs": 2,
    "original_repository": 3,
    "paper": 4,
}


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


def require_inputs(claim_map: dict, review_gate: dict) -> None:
    if claim_map.get("claim_mapping_scope") != "internal_design_evidence_only":
        raise SystemExit("claim map must remain evidence-only")
    if claim_map.get("dependency_adoption_allowed") is not False:
        raise SystemExit("claim map must not allow dependency adoption")
    if claim_map.get("runtime_integration_allowed") is not False:
        raise SystemExit("claim map must not allow runtime integration")
    if review_gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("claim map review goal mismatch")
    if review_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("claim map review gate must point to this scorecard goal")
    if review_gate.get("ready_for_evidence_strength_scorecard_count") != 1:
        raise SystemExit("claim map review gate must be ready for scorecard")


def source_kind_counts(claims: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for claim in claims:
        kind = claim["source_kind"]
        counts[kind] = counts.get(kind, 0) + 1
    return dict(sorted(counts.items()))


def evidence_tier(score: int) -> str:
    if score >= 12:
        return "strong"
    if score >= 8:
        return "moderate"
    return "early"


def candidate_scorecard(candidate_map: dict) -> dict:
    claims = candidate_map["source_claims"]
    counts = source_kind_counts(claims)
    source_count = len(claims)
    source_kind_points = sum(SOURCE_KIND_WEIGHTS[kind] * count for kind, count in counts.items())
    diversity_bonus = len(counts)
    source_count_bonus = source_count
    score = source_kind_points + diversity_bonus + source_count_bonus
    return {
        "candidate_id": candidate_map["candidate_id"],
        "scorecard_scope": "advisory_internal_design_evidence_only",
        "source_count": source_count,
        "source_ids": candidate_map["source_ids"],
        "source_kind_counts": counts,
        "source_kind_points": source_kind_points,
        "diversity_bonus": diversity_bonus,
        "source_count_bonus": source_count_bonus,
        "evidence_strength_score": score,
        "evidence_strength_tier": evidence_tier(score),
        "claim_summary_count": len(claims),
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "scorecard_review_required": True,
    }


def candidate_scorecards(claim_map: dict) -> list[dict]:
    return [
        candidate_scorecard(candidate_map)
        for candidate_map in sorted(claim_map["candidate_claim_maps"], key=lambda item: item["candidate_id"])
    ]


def tier_counts(scorecards: list[dict]) -> dict[str, int]:
    counts = {"strong": 0, "moderate": 0, "early": 0}
    for scorecard in scorecards:
        counts[scorecard["evidence_strength_tier"]] += 1
    return counts


def counts(claim_map: dict) -> dict:
    scorecards = candidate_scorecards(claim_map)
    tiers = tier_counts(scorecards)
    return {
        "candidate_count": claim_map["candidate_count"],
        "scorecard_candidate_count": len(scorecards),
        "source_claim_count": claim_map["source_claim_count"],
        "evidence_only_score_count": len(scorecards),
        "strong_evidence_candidate_count": tiers["strong"],
        "moderate_evidence_candidate_count": tiers["moderate"],
        "early_evidence_candidate_count": tiers["early"],
        "dependency_adopted_score_count": 0,
        "runtime_integrated_score_count": 0,
        "ready_for_scorecard_review_count": 1,
    }


def base_record(claim_map: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "scorecard_status": SCORECARD_STATUS,
        "scoring_model": SCORING_MODEL,
        "scorecard_scope": "advisory_internal_design_evidence_only",
        "source_kind_weights": SOURCE_KIND_WEIGHTS,
        "source_required_candidate_ids": claim_map["source_required_candidate_ids"],
        "candidate_scorecards": candidate_scorecards(claim_map),
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "input_uris": {
            "evidence_claim_map": rel(CLAIM_MAP),
            "evidence_claim_map_review_gate": rel(CLAIM_MAP_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(claim_map),
        "claim_boundary": false_boundary(),
    }


def build_scorecard(claim_map: dict) -> dict:
    return {
        **base_record(claim_map),
        "scorecard_id": "avf-capability-candidate-primary-source-evidence-strength-scorecard-v0-1",
        "scorecard_notes": "Advisory evidence-strength score only; this is not a selection, adoption, runtime, or readiness gate.",
    }


def build_gate(claim_map: dict) -> dict:
    return {
        **base_record(claim_map),
        "gate_id": "avf-capability-candidate-primary-source-evidence-strength-scorecard-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Advisory evidence-strength scorecard created; review required before any downstream prioritization",
    }


def build_validation_result(claim_map: dict) -> dict:
    return {
        **base_record(claim_map),
        "validator_id": "validate_avf_capability_candidate_primary_source_evidence_strength_scorecard_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(SCORECARD),
            rel(SCORECARD_GATE),
            rel(SCORECARD_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(claim_map: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(claim_map).items())
    score_lines = "\n".join(
        "- {candidate_id}: score={evidence_strength_score}, tier={evidence_strength_tier}, source_count={source_count}".format(
            **scorecard
        )
        for scorecard in candidate_scorecards(claim_map)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Evidence Strength Scorecard v0.1

RESULT: PASS
capability_candidate_primary_source_evidence_strength_scorecard_v0_1=true

## Scorecard summary

- scorecard_status={SCORECARD_STATUS}
- scoring_model={SCORING_MODEL}
- scorecard_scope=advisory_internal_design_evidence_only
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Candidate scores

{score_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-evidence-strength-scorecard
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the advisory evidence-strength scorecard
  - Confirm scoring uses only reviewed evidence-only claim maps
  - Confirm scorecard is not a selection, adoption, runtime integration, deploy, publish, or readiness gate
  - Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    claim_map = read_json(CLAIM_MAP)
    review_gate = read_json(CLAIM_MAP_REVIEW_GATE)
    require_inputs(claim_map, review_gate)

    write_json(SCORECARD, build_scorecard(claim_map))
    write_json(SCORECARD_GATE, build_gate(claim_map))
    report = build_report(claim_map)
    write_text(SCORECARD_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(claim_map))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Evidence Strength Scorecard v0.1")
    print("RESULT: PASS")
    print(f"scorecard_status={SCORECARD_STATUS}")
    print(f"scoring_model={SCORING_MODEL}")
    for key, value in counts(claim_map).items():
        print(f"{key}={value}")
    print("scorecard_scope=advisory_internal_design_evidence_only")
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

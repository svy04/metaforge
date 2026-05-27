from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_evidence_strength_scorecard_v0_1.py"
CLAIM_MAP = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map.json"
CLAIM_MAP_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_gate.json"
CLAIM_MAP_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_next_action.yml"
SCORECARD = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard.json"
SCORECARD_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_gate.json"
SCORECARD_REPORT = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_STRENGTH_SCORECARD_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1"
SCORECARD_STATUS = "advisory_evidence_strength_scorecard_created_no_adoption"
SCORING_MODEL = "advisory_source_kind_diversity_v0_1"

SOURCE_KIND_WEIGHTS = {
    "official_docs": 2,
    "original_repository": 3,
    "paper": 4,
}

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "scorecard_candidate_count": 7,
    "source_claim_count": 16,
    "evidence_only_score_count": 7,
    "strong_evidence_candidate_count": 1,
    "moderate_evidence_candidate_count": 5,
    "early_evidence_candidate_count": 1,
    "dependency_adopted_score_count": 0,
    "runtime_integrated_score_count": 0,
    "ready_for_scorecard_review_count": 1,
}

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "automated_scraping_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "runtime_export_performed",
    "collector_started",
    "telemetry_export_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    CLAIM_MAP,
    CLAIM_MAP_REVIEW_GATE,
    CLAIM_MAP_REVIEW_NEXT_ACTION,
    SCORECARD,
    SCORECARD_GATE,
    SCORECARD_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_evidence_strength_scorecard_v0_1=true",
    f"scorecard_status={SCORECARD_STATUS}",
    f"scoring_model={SCORING_MODEL}",
    "scorecard_scope=advisory_internal_design_evidence_only",
    "scorecard_candidate_count=7",
    "source_claim_count=16",
    "strong_evidence_candidate_count=1",
    "moderate_evidence_candidate_count=5",
    "early_evidence_candidate_count=1",
    "dependency_adopted_score_count=0",
    "runtime_integrated_score_count=0",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-evidence-strength-scorecard",
    "owner_approval_required_before_execution: false",
    "Review the advisory evidence-strength scorecard",
    "Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Evidence Strength Scorecard v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def flattened_claims(candidate_map: dict) -> list[dict]:
    return candidate_map.get("source_claims", [])


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


def require_previous_inputs() -> dict:
    claim_map = read_json(CLAIM_MAP)
    review_gate = read_json(CLAIM_MAP_REVIEW_GATE)
    if claim_map.get("goal_id") != "avf_capability_candidate_primary_source_evidence_claim_map_v0_1":
        fail("claim map goal_id mismatch")
    if review_gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("claim map review gate goal_id mismatch")
    if review_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("claim map review gate must point to this scorecard goal")
    if review_gate.get("ready_for_evidence_strength_scorecard_count") != 1:
        fail("claim map review gate must be ready for scorecard")
    if review_gate.get("dependency_adoption_allowed") is not False:
        fail("claim map review gate dependency adoption must remain blocked")
    if review_gate.get("runtime_integration_allowed") is not False:
        fail("claim map review gate runtime integration must remain blocked")
    require_false_flags(claim_map.get("claim_boundary", {}), "claim map claim boundary")
    require_false_flags(review_gate.get("claim_boundary", {}), "claim map review claim boundary")
    require_text_markers(
        CLAIM_MAP_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-evidence-strength-scorecard",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return claim_map


def require_scorecard_candidate(candidate_score: dict, source_map: dict, label: str) -> None:
    candidate_id = source_map["candidate_id"]
    if candidate_score.get("candidate_id") != candidate_id:
        fail(f"{label} candidate id mismatch")
    claims = flattened_claims(source_map)
    counts = source_kind_counts(claims)
    source_count = len(claims)
    source_kind_points = sum(SOURCE_KIND_WEIGHTS[kind] * count for kind, count in counts.items())
    diversity_bonus = len(counts)
    source_count_bonus = source_count
    expected_score = source_kind_points + diversity_bonus + source_count_bonus
    expected_tier = evidence_tier(expected_score)

    expected = {
        "scorecard_scope": "advisory_internal_design_evidence_only",
        "source_count": source_count,
        "source_kind_counts": counts,
        "source_kind_points": source_kind_points,
        "diversity_bonus": diversity_bonus,
        "source_count_bonus": source_count_bonus,
        "evidence_strength_score": expected_score,
        "evidence_strength_tier": expected_tier,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "scorecard_review_required": True,
    }
    for key, value in expected.items():
        if candidate_score.get(key) != value:
            fail(f"{label} {candidate_id} {key} mismatch")
    if candidate_score.get("source_ids") != source_map.get("source_ids"):
        fail(f"{label} {candidate_id} source ids mismatch")
    if candidate_score.get("claim_summary_count") != len(source_map.get("source_claims", [])):
        fail(f"{label} {candidate_id} claim summary count mismatch")


def require_scorecard_record(record: dict, label: str, claim_map: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "scorecard_status": SCORECARD_STATUS,
        "scoring_model": SCORING_MODEL,
        "scorecard_scope": "advisory_internal_design_evidence_only",
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("source_required_candidate_ids") != claim_map.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    if record.get("source_kind_weights") != SOURCE_KIND_WEIGHTS:
        fail(f"{label} source kind weights mismatch")
    scorecards = record.get("candidate_scorecards", [])
    if len(scorecards) != EXPECTED_COUNTS["scorecard_candidate_count"]:
        fail(f"{label} candidate scorecard count mismatch")
    source_maps = {item["candidate_id"]: item for item in claim_map.get("candidate_claim_maps", [])}
    tiers = {"strong": 0, "moderate": 0, "early": 0}
    for candidate_score in scorecards:
        candidate_id = candidate_score.get("candidate_id")
        if candidate_id not in source_maps:
            fail(f"{label} unexpected candidate scorecard {candidate_id}")
        require_scorecard_candidate(candidate_score, source_maps[candidate_id], label)
        tiers[candidate_score["evidence_strength_tier"]] += 1
    if tiers["strong"] != EXPECTED_COUNTS["strong_evidence_candidate_count"]:
        fail(f"{label} strong tier count mismatch")
    if tiers["moderate"] != EXPECTED_COUNTS["moderate_evidence_candidate_count"]:
        fail(f"{label} moderate tier count mismatch")
    if tiers["early"] != EXPECTED_COUNTS["early_evidence_candidate_count"]:
        fail(f"{label} early tier count mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_scorecard(claim_map: dict) -> None:
    scorecard = read_json(SCORECARD)
    if scorecard.get("scorecard_id") != "avf-capability-candidate-primary-source-evidence-strength-scorecard-v0-1":
        fail("scorecard id mismatch")
    require_scorecard_record(scorecard, "scorecard", claim_map)


def require_scorecard_gate(claim_map: dict) -> None:
    gate = read_json(SCORECARD_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-evidence-strength-scorecard-gate-v0-1":
        fail("scorecard gate id mismatch")
    if gate.get("status") != "PASS":
        fail("scorecard gate status must be PASS")
    require_scorecard_record(gate, "scorecard gate", claim_map)


def require_validation_result(claim_map: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_evidence_strength_scorecard_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_scorecard_record(result, "validation result", claim_map)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    claim_map = require_previous_inputs()
    require_scorecard(claim_map)
    require_scorecard_gate(claim_map)
    require_text_markers(SCORECARD_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(claim_map)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Evidence Strength Scorecard v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_evidence_strength_scorecard_v0_1=true")
    print(f"scorecard_status={SCORECARD_STATUS}")
    print(f"scoring_model={SCORING_MODEL}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("scorecard_scope=advisory_internal_design_evidence_only")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

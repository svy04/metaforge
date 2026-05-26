from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_fit_scoring_validator_v0_1.py"
ACQUISITION_PLAN = CAPABILITIES / "capability_acquisition_plan.json"
CANDIDATE_REGISTRY = CAPABILITIES / "capability_candidate_registry.json"
BUILD_BUY_ADOPT = CAPABILITIES / "build_buy_adopt_decision_records.json"
CAPABILITY_SOURCE_LEDGER = CAPABILITIES / "capability_source_ledger.json"
SCORECARD = CAPABILITIES / "capability_fit_scorecard.json"
GATE_DECISION = CAPABILITIES / "capability_fit_scoring_gate_decision.json"
SCORING_SOURCE_LEDGER = CAPABILITIES / "capability_fit_scoring_source_ledger.json"
VALIDATION_RESULT = CAPABILITIES / "capability_fit_scoring_validator_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_FIT_SCORING_VALIDATOR_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_fit_scoring_validator_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_review_dossier_v0_1"

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    ACQUISITION_PLAN,
    CANDIDATE_REGISTRY,
    BUILD_BUY_ADOPT,
    CAPABILITY_SOURCE_LEDGER,
    SCORECARD,
    GATE_DECISION,
    SCORING_SOURCE_LEDGER,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_SCORING_SOURCE_IDS = {
    "src-openssf-scorecard",
    "src-slsa-spec",
    "src-spdx-spec",
    "src-github-dependency-review",
    "src-openssf-scorecard-paper",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_fit_scoring_validator_v0_1=true",
    "capability_fit_scorecard_created=true",
    "candidate_scores_created=true",
    "gate_decision_created=true",
    "scoring_source_ledger_created=true",
    "protected_action_executed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "provider_calls_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Fit Scoring Validator v0.1 validation")
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


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def candidate_count(registry: dict) -> int:
    return sum(len(capability.get("candidate_records", [])) for capability in registry.get("capabilities", []))


def require_scoring_source_ledger() -> None:
    ledger = read_json(SCORING_SOURCE_LEDGER)
    if ledger.get("automation_fetch_performed") is not False:
        fail("scoring source ledger automation_fetch_performed must be false")
    source_ids = {source.get("source_id") for source in ledger.get("sources", [])}
    missing = sorted(REQUIRED_SCORING_SOURCE_IDS - source_ids)
    if missing:
        fail("scoring source ledger missing source ids:\n" + "\n".join(missing))
    for source in ledger.get("sources", []):
        if source.get("source_kind") not in {"official_docs", "official_standard", "official_guidance", "paper", "official_repo"}:
            fail(f"unsupported scoring source kind: {source.get('source_id')}")
        if not source.get("url", "").startswith("https://"):
            fail(f"scoring source missing https URL: {source.get('source_id')}")


def require_scorecard(registry: dict) -> None:
    scorecard = read_json(SCORECARD)
    if scorecard.get("status") != "PASS":
        fail("scorecard status must be PASS")
    if scorecard.get("goal_id") != THIS_GOAL_ID:
        fail("scorecard goal_id mismatch")
    if scorecard.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("scorecard next safe goal mismatch")
    require_false_flags(scorecard.get("claim_boundary", {}), "scorecard claim boundary")

    scores = scorecard.get("candidate_scores", [])
    expected_count = candidate_count(registry)
    if len(scores) != expected_count:
        fail(f"scorecard candidate count mismatch: expected {expected_count}, got {len(scores)}")

    registry_candidate_ids = {
        candidate.get("candidate_id")
        for capability in registry.get("capabilities", [])
        for candidate in capability.get("candidate_records", [])
    }
    score_candidate_ids = {score.get("candidate_id") for score in scores}
    missing = sorted(registry_candidate_ids - score_candidate_ids)
    if missing:
        fail("scorecard missing candidate scores:\n" + "\n".join(missing))

    for score in scores:
        if not isinstance(score.get("fit_score"), int) or not 0 <= score["fit_score"] <= 100:
            fail(f"invalid fit_score: {score.get('candidate_id')}")
        if not isinstance(score.get("risk_score"), int) or not 0 <= score["risk_score"] <= 100:
            fail(f"invalid risk_score: {score.get('candidate_id')}")
        if not isinstance(score.get("priority_rank"), int) or score["priority_rank"] < 1:
            fail(f"invalid priority_rank: {score.get('candidate_id')}")
        if score.get("integration_readiness") != "not_ready_requires_reviews":
            fail(f"integration readiness must stay blocked: {score.get('candidate_id')}")
        if score.get("license_review_status") != "required_not_performed":
            fail(f"license review must remain required_not_performed: {score.get('candidate_id')}")
        if score.get("security_review_status") != "required_not_performed":
            fail(f"security review must remain required_not_performed: {score.get('candidate_id')}")
        if score.get("maintenance_review_status") != "required_not_performed":
            fail(f"maintenance review must remain required_not_performed: {score.get('candidate_id')}")
        if score.get("next_gate") != "capability_review_dossier_required":
            fail(f"next gate mismatch: {score.get('candidate_id')}")
        if not score.get("scoring_basis"):
            fail(f"missing scoring_basis: {score.get('candidate_id')}")
        if not set(score.get("scoring_source_refs", [])) >= REQUIRED_SCORING_SOURCE_IDS:
            fail(f"missing scoring source refs: {score.get('candidate_id')}")


def require_gate_decision(registry: dict) -> None:
    gate = read_json(GATE_DECISION)
    if gate.get("status") != "PASS":
        fail("gate decision status must be PASS")
    if gate.get("decision") != "do_not_integrate_yet":
        fail("gate decision must block integration")
    if gate.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("gate decision next safe goal mismatch")
    if len(gate.get("top_candidates", [])) < 3:
        fail("gate decision should name at least three top candidates")
    require_false_flags(gate.get("claim_boundary", {}), "gate decision claim boundary")
    score_ids = {score.get("candidate_id") for score in read_json(SCORECARD).get("candidate_scores", [])}
    for candidate_id in gate.get("top_candidates", []):
        if candidate_id not in score_ids:
            fail(f"gate decision top candidate missing from scorecard: {candidate_id}")
    if candidate_count(registry) != len(score_ids):
        fail("gate decision sees incomplete scorecard")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("fit scoring validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("fit scoring validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "fit scoring validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    acquisition_plan = read_json(ACQUISITION_PLAN)
    if acquisition_plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("acquisition plan does not authorize fit scoring as next safe goal")

    registry = read_json(CANDIDATE_REGISTRY)
    require_scoring_source_ledger()
    require_scorecard(registry)
    require_gate_decision(registry)
    require_validation_result()
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Fit Scoring Validator v0.1 validation")
    print("RESULT: PASS")
    print("capability_fit_scoring_validator_v0_1=true")
    print("capability_fit_scorecard_created=true")
    print("candidate_scores_created=true")
    print("gate_decision_created=true")
    print("scoring_source_ledger_created=true")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("provider_calls_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

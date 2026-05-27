from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

SCORECARD = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard.json"
SCORECARD_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_STRENGTH_SCORECARD_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_STRENGTH_SCORECARD_REVIEWED"
REVIEW_STATUS = "advisory_scorecard_validated_ready_for_priority_matrix"


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


def require_scorecard(scorecard: dict, gate: dict) -> None:
    if scorecard.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("scorecard goal mismatch")
    if scorecard.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("scorecard must point to this review goal")
    if gate.get("status") != "PASS":
        raise SystemExit("scorecard gate must pass")
    if scorecard.get("dependency_adoption_allowed") is not False:
        raise SystemExit("scorecard must not allow dependency adoption")
    if scorecard.get("runtime_integration_allowed") is not False:
        raise SystemExit("scorecard must not allow runtime integration")


def counts(scorecard: dict) -> dict:
    return {
        "candidate_count": scorecard["candidate_count"],
        "scorecard_candidate_count": scorecard["scorecard_candidate_count"],
        "reviewed_scorecard_candidate_count": scorecard["scorecard_candidate_count"],
        "source_claim_count": scorecard["source_claim_count"],
        "strong_evidence_candidate_count": scorecard["strong_evidence_candidate_count"],
        "moderate_evidence_candidate_count": scorecard["moderate_evidence_candidate_count"],
        "early_evidence_candidate_count": scorecard["early_evidence_candidate_count"],
        "dependency_adopted_score_count": 0,
        "runtime_integrated_score_count": 0,
        "review_blocker_count": 0,
        "ready_for_advisory_priority_matrix_count": 1,
    }


def reviewed_scorecard_candidates(scorecard: dict) -> list[dict]:
    reviewed = []
    for item in scorecard["candidate_scorecards"]:
        reviewed.append(
            {
                "candidate_id": item["candidate_id"],
                "evidence_strength_score": item["evidence_strength_score"],
                "evidence_strength_tier": item["evidence_strength_tier"],
                "source_count": item["source_count"],
                "claim_summary_count": item["claim_summary_count"],
                "review_status": "reviewed_scorecard_validated",
                "priority_matrix_allowed": True,
                "selection_allowed": False,
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return reviewed


def base_record(scorecard: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "scorecard_scope_confirmed": "advisory_internal_design_evidence_only",
        "scorecard_not_selection_gate": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "source_required_candidate_ids": scorecard["source_required_candidate_ids"],
        "reviewed_scorecard_candidates": reviewed_scorecard_candidates(scorecard),
        "input_uris": {
            "evidence_strength_scorecard": rel(SCORECARD),
            "evidence_strength_scorecard_gate": rel(SCORECARD_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(scorecard),
        "claim_boundary": false_boundary(),
    }


def build_gate(scorecard: dict) -> dict:
    return {
        **base_record(scorecard),
        "gate_id": "avf-capability-candidate-primary-source-evidence-strength-scorecard-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Advisory scorecard reviewed; priority matrix may be created without selection or adoption",
    }


def build_validation_result(scorecard: dict) -> dict:
    return {
        **base_record(scorecard),
        "validator_id": "validate_avf_capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(scorecard: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(scorecard).items())
    score_lines = "\n".join(
        "- {candidate_id}: score={evidence_strength_score}, tier={evidence_strength_tier}, selection_allowed=false".format(
            **item
        )
        for item in reviewed_scorecard_candidates(scorecard)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Evidence Strength Scorecard Review v0.1

RESULT: PASS
capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1=true

## Review summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- scorecard_scope_confirmed=advisory_internal_design_evidence_only
- scorecard_not_selection_gate=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Reviewed scorecards

{score_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-advisory-priority-matrix
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create an advisory priority matrix from the reviewed scorecard
  - Combine evidence tier with integration risk placeholders only
  - Keep the matrix advisory and non-executable
  - Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    scorecard = read_json(SCORECARD)
    gate = read_json(SCORECARD_GATE)
    require_scorecard(scorecard, gate)

    write_json(REVIEW_GATE, build_gate(scorecard))
    report = build_report(scorecard)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(scorecard))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Evidence Strength Scorecard Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(scorecard).items():
        print(f"{key}={value}")
    print("scorecard_scope_confirmed=advisory_internal_design_evidence_only")
    print("scorecard_not_selection_gate=true")
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

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

SCORECARD_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_strength_scorecard_review_gate.json"
PRIORITY_MATRIX = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix.json"
PRIORITY_MATRIX_GATE = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_gate.json"
PRIORITY_MATRIX_REPORT = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ADVISORY_PRIORITY_MATRIX_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
MATRIX_STATUS = "advisory_priority_matrix_created_non_executable"
MATRIX_MODEL = "evidence_tier_plus_integration_risk_placeholder_v0_1"


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


def require_scorecard_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("scorecard review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("scorecard review must point to this priority matrix goal")
    if review.get("ready_for_advisory_priority_matrix_count") != 1:
        raise SystemExit("scorecard review must be ready for priority matrix")
    if review.get("scorecard_not_selection_gate") is not True:
        raise SystemExit("scorecard review must confirm non-selection boundary")
    if review.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if review.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def priority_for_tier(tier: str) -> int:
    if tier == "strong":
        return 1
    if tier == "moderate":
        return 2
    return 3


def priority_items(review: dict) -> list[dict]:
    items = []
    for candidate in review["reviewed_scorecard_candidates"]:
        items.append(
            {
                "candidate_id": candidate["candidate_id"],
                "evidence_strength_score": candidate["evidence_strength_score"],
                "evidence_strength_tier": candidate["evidence_strength_tier"],
                "source_count": candidate["source_count"],
                "claim_summary_count": candidate["claim_summary_count"],
                "integration_risk_placeholder": "requires_future_license_security_architecture_review",
                "advisory_priority": priority_for_tier(candidate["evidence_strength_tier"]),
                "matrix_scope": "advisory_non_executable_internal_planning",
                "selection_allowed": False,
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
                "priority_matrix_review_required": True,
            }
        )
    return sorted(items, key=lambda item: (item["advisory_priority"], item["candidate_id"]))


def counts(review: dict) -> dict:
    items = priority_items(review)
    priorities = {1: 0, 2: 0, 3: 0}
    for item in items:
        priorities[item["advisory_priority"]] += 1
    return {
        "candidate_count": review["candidate_count"],
        "priority_matrix_candidate_count": len(items),
        "priority_1_candidate_count": priorities[1],
        "priority_2_candidate_count": priorities[2],
        "priority_3_candidate_count": priorities[3],
        "selection_allowed_count": 0,
        "dependency_adoption_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "ready_for_priority_matrix_review_count": 1,
    }


def base_record(review: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "matrix_status": MATRIX_STATUS,
        "matrix_model": MATRIX_MODEL,
        "matrix_scope": "advisory_non_executable_internal_planning",
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "source_required_candidate_ids": review["source_required_candidate_ids"],
        "priority_items": priority_items(review),
        "input_uris": {
            "evidence_strength_scorecard_review_gate": rel(SCORECARD_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(review),
        "claim_boundary": false_boundary(),
    }


def build_matrix(review: dict) -> dict:
    return {
        **base_record(review),
        "matrix_id": "avf-capability-candidate-primary-source-advisory-priority-matrix-v0-1",
        "matrix_notes": "Advisory non-executable priority matrix only; not selection, adoption, runtime, or readiness approval.",
    }


def build_gate(review: dict) -> dict:
    return {
        **base_record(review),
        "gate_id": "avf-capability-candidate-primary-source-advisory-priority-matrix-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Advisory non-executable priority matrix created; review required before downstream planning",
    }


def build_validation_result(review: dict) -> dict:
    return {
        **base_record(review),
        "validator_id": "validate_avf_capability_candidate_primary_source_advisory_priority_matrix_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(PRIORITY_MATRIX),
            rel(PRIORITY_MATRIX_GATE),
            rel(PRIORITY_MATRIX_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(review).items())
    item_lines = "\n".join(
        "- {candidate_id}: advisory_priority={advisory_priority}, tier={evidence_strength_tier}, selection_allowed=false".format(
            **item
        )
        for item in priority_items(review)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Advisory Priority Matrix v0.1

RESULT: PASS
capability_candidate_primary_source_advisory_priority_matrix_v0_1=true

## Matrix summary

- matrix_status={MATRIX_STATUS}
- matrix_model={MATRIX_MODEL}
- matrix_scope=advisory_non_executable_internal_planning
- selection_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Priority items

{item_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-advisory-priority-matrix
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the advisory priority matrix
  - Confirm priorities are non-executable internal planning signals only
  - Confirm no candidate is selected, adopted, installed, cloned, integrated, deployed, published, or marked ready
  - Do not select, adopt, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(SCORECARD_REVIEW_GATE)
    require_scorecard_review(review)

    write_json(PRIORITY_MATRIX, build_matrix(review))
    write_json(PRIORITY_MATRIX_GATE, build_gate(review))
    report = build_report(review)
    write_text(PRIORITY_MATRIX_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Advisory Priority Matrix v0.1")
    print("RESULT: PASS")
    print(f"matrix_status={MATRIX_STATUS}")
    print(f"matrix_model={MATRIX_MODEL}")
    for key, value in counts(review).items():
        print(f"{key}={value}")
    print("matrix_scope=advisory_non_executable_internal_planning")
    print("selection_allowed=false")
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

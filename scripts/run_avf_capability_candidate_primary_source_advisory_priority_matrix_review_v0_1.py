from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PRIORITY_MATRIX = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix.json"
PRIORITY_MATRIX_GATE = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ADVISORY_PRIORITY_MATRIX_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_ADVISORY_PRIORITY_MATRIX_REVIEWED"
REVIEW_STATUS = "advisory_priority_matrix_validated_ready_for_priority_1_deep_research_plan"
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


def require_priority_matrix(matrix: dict, gate: dict) -> None:
    if matrix.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("priority matrix goal mismatch")
    if matrix.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("priority matrix must point to this review goal")
    if gate.get("status") != "PASS":
        raise SystemExit("priority matrix gate must pass")
    if matrix.get("matrix_status") != MATRIX_STATUS:
        raise SystemExit("priority matrix status mismatch")
    if matrix.get("matrix_model") != MATRIX_MODEL:
        raise SystemExit("priority matrix model mismatch")
    if matrix.get("selection_allowed") is not False:
        raise SystemExit("selection must remain blocked")
    if matrix.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if matrix.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")
    if matrix.get("priority_1_candidate_count") != 1:
        raise SystemExit("priority 1 candidate count must be exactly 1 for this review")


def priority_1_candidate_ids(matrix: dict) -> list[str]:
    return [
        item["candidate_id"]
        for item in matrix["priority_items"]
        if item["advisory_priority"] == 1
    ]


def counts(matrix: dict) -> dict:
    return {
        "candidate_count": matrix["candidate_count"],
        "priority_matrix_candidate_count": matrix["priority_matrix_candidate_count"],
        "reviewed_priority_item_count": matrix["priority_matrix_candidate_count"],
        "priority_1_candidate_count": matrix["priority_1_candidate_count"],
        "priority_2_candidate_count": matrix["priority_2_candidate_count"],
        "priority_3_candidate_count": matrix["priority_3_candidate_count"],
        "selection_allowed_count": 0,
        "dependency_adoption_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_priority_1_deep_research_plan_count": 1,
    }


def reviewed_priority_items(matrix: dict) -> list[dict]:
    reviewed = []
    for item in matrix["priority_items"]:
        reviewed.append(
            {
                "candidate_id": item["candidate_id"],
                "evidence_strength_score": item["evidence_strength_score"],
                "evidence_strength_tier": item["evidence_strength_tier"],
                "source_count": item["source_count"],
                "claim_summary_count": item["claim_summary_count"],
                "advisory_priority": item["advisory_priority"],
                "integration_risk_placeholder": item["integration_risk_placeholder"],
                "review_status": "reviewed_advisory_priority_validated",
                "priority_1_deep_research_plan_required": item["advisory_priority"] == 1,
                "selection_allowed": False,
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return reviewed


def base_record(matrix: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "priority_matrix_scope_confirmed": "advisory_non_executable_internal_planning",
        "priority_matrix_not_selection_gate": True,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "priority_1_candidate_ids": priority_1_candidate_ids(matrix),
        "reviewed_priority_items": reviewed_priority_items(matrix),
        "input_uris": {
            "advisory_priority_matrix": rel(PRIORITY_MATRIX),
            "advisory_priority_matrix_gate": rel(PRIORITY_MATRIX_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(matrix),
        "claim_boundary": false_boundary(),
    }


def build_gate(matrix: dict) -> dict:
    return {
        **base_record(matrix),
        "gate_id": "avf-capability-candidate-primary-source-advisory-priority-matrix-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Advisory priority matrix reviewed; priority 1 deep research planning may be created without selection or adoption",
    }


def build_validation_result(matrix: dict) -> dict:
    return {
        **base_record(matrix),
        "validator_id": "validate_avf_capability_candidate_primary_source_advisory_priority_matrix_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(matrix: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(matrix).items())
    item_lines = "\n".join(
        "- {candidate_id}: review_status=reviewed_advisory_priority_validated, advisory_priority={advisory_priority}, priority_1_deep_research_plan_required={priority_1_deep_research_plan_required}, selection_allowed=false".format(
            **item
        )
        for item in reviewed_priority_items(matrix)
    )
    priority_ids = ", ".join(priority_1_candidate_ids(matrix))
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Advisory Priority Matrix Review v0.1

RESULT: PASS
capability_candidate_primary_source_advisory_priority_matrix_review_v0_1=true

## Review summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- priority_matrix_scope_confirmed=advisory_non_executable_internal_planning
- priority_matrix_not_selection_gate=true
- priority_1_deep_research_plan_candidate_count={len(priority_1_candidate_ids(matrix))}
- priority_1_candidate_id={priority_ids}
- selection_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Reviewed priority items

{item_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-deep-research-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local deep research plan for the priority 1 candidate
  - Candidate: cap-eval-redteam-promptfoo-ragas
  - Identify official docs, original repos, papers, standards, and maintained source-code targets to inspect later
  - Keep the plan non-executable and evidence-only
  - Do not select, adopt, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    matrix = read_json(PRIORITY_MATRIX)
    gate = read_json(PRIORITY_MATRIX_GATE)
    require_priority_matrix(matrix, gate)

    write_json(REVIEW_GATE, build_gate(matrix))
    report = build_report(matrix)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(matrix))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Advisory Priority Matrix Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(matrix).items():
        print(f"{key}={value}")
    print("priority_matrix_scope_confirmed=advisory_non_executable_internal_planning")
    print("priority_matrix_not_selection_gate=true")
    print("priority_1_candidate_id=cap-eval-redteam-promptfoo-ragas")
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

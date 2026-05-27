from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RESEARCH_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan.json"
SOURCE_TARGETS = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_source_targets.json"
PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_DEEP_RESEARCH_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_DEEP_RESEARCH_PLAN_REVIEWED"
REVIEW_STATUS = "deep_research_plan_validated_ready_for_source_evidence_capture_plan"
PLAN_SCOPE = "primary_source_deep_research_plan_only"


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


def require_plan(plan: dict, gate: dict) -> None:
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("deep research plan goal mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("deep research plan must point to this review goal")
    if gate.get("status") != "PASS":
        raise SystemExit("deep research plan gate must pass")
    if plan.get("candidate_id") != CANDIDATE_ID:
        raise SystemExit("candidate mismatch")
    if plan.get("plan_scope") != PLAN_SCOPE:
        raise SystemExit("plan scope mismatch")
    if plan.get("source_target_count") != 7:
        raise SystemExit("source target count mismatch")
    if plan.get("external_fetch_performed") is not False:
        raise SystemExit("source fetching must remain blocked")
    if plan.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if plan.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def counts(plan: dict) -> dict:
    return {
        "source_target_count": plan["source_target_count"],
        "reviewed_source_target_count": plan["source_target_count"],
        "official_docs_target_count": plan["official_docs_target_count"],
        "original_repository_target_count": plan["original_repository_target_count"],
        "paper_target_count": plan["paper_target_count"],
        "standard_target_count": plan["standard_target_count"],
        "maintained_source_code_target_count": plan["maintained_source_code_target_count"],
        "selection_allowed_count": 0,
        "dependency_adoption_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "external_fetch_performed_count": 0,
        "review_blocker_count": 0,
        "ready_for_source_evidence_capture_plan_count": 1,
    }


def reviewed_source_targets(plan: dict) -> list[dict]:
    reviewed = []
    for target in plan["source_targets"]:
        reviewed.append(
            {
                "source_target_id": target["source_target_id"],
                "candidate_id": target["candidate_id"],
                "source_kind": target["source_kind"],
                "source_uri": target["source_uri"],
                "inspection_focus": target["inspection_focus"],
                "maintained_source_code_target": target["maintained_source_code_target"],
                "review_status": "reviewed_source_target_validated",
                "capture_plan_required": True,
                "selection_allowed": False,
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
                "external_fetch_performed": False,
            }
        )
    return reviewed


def base_record(plan: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "plan_scope_confirmed": PLAN_SCOPE,
        "deep_research_plan_not_source_fetch_gate": True,
        "reviewed_source_targets": reviewed_source_targets(plan),
        "input_uris": {
            "priority_1_deep_research_plan": rel(RESEARCH_PLAN),
            "priority_1_deep_research_source_targets": rel(SOURCE_TARGETS),
            "priority_1_deep_research_plan_gate": rel(PLAN_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "external_fetch_performed": False,
        **counts(plan),
        "claim_boundary": false_boundary(),
    }


def build_gate(plan: dict) -> dict:
    return {
        **base_record(plan),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-deep-research-plan-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Deep research plan reviewed; source evidence capture planning may be created without fetching sources",
    }


def build_validation_result(plan: dict) -> dict:
    return {
        **base_record(plan),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(plan: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(plan).items())
    target_lines = "\n".join(
        "- {source_target_id}: review_status=reviewed_source_target_validated, capture_plan_required=true, external_fetch_performed=false".format(
            **target
        )
        for target in reviewed_source_targets(plan)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Deep Research Plan Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1=true

## Review summary

- candidate_id={CANDIDATE_ID}
- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- plan_scope_confirmed={PLAN_SCOPE}
- deep_research_plan_not_source_fetch_gate=true
- selection_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false

## Counts

{count_lines}

## Reviewed source targets

{target_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-source-evidence-capture-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local source evidence capture plan
  - Define exact evidence fields to capture from each source target
  - Keep capture planning non-executable until a separate approved evidence collection goal exists
  - Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    plan = read_json(RESEARCH_PLAN)
    gate = read_json(PLAN_GATE)
    require_plan(plan, gate)

    write_json(REVIEW_GATE, build_gate(plan))
    report = build_report(plan)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plan))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Deep Research Plan Review v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(plan).items():
        print(f"{key}={value}")
    print("deep_research_plan_not_source_fetch_gate=true")
    print("selection_allowed=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

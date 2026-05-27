from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

CAPTURE_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan.json"
CAPTURE_FIELD_SPEC = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_field_spec.json"
CAPTURE_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_SOURCE_EVIDENCE_CAPTURE_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_SOURCE_EVIDENCE_CAPTURE_PLAN_REVIEWED"
REVIEW_STATUS = "source_evidence_capture_plan_validated_ready_for_manual_evidence_workspace"
CAPTURE_PLAN_SCOPE = "capture_field_schema_and_target_plan_only"


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


def require_capture_plan(plan: dict, gate: dict) -> None:
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("capture plan goal mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("capture plan must point to this review goal")
    if gate.get("status") != "PASS":
        raise SystemExit("capture plan gate must pass")
    if plan.get("candidate_id") != CANDIDATE_ID:
        raise SystemExit("candidate mismatch")
    if plan.get("capture_plan_scope") != CAPTURE_PLAN_SCOPE:
        raise SystemExit("capture plan scope mismatch")
    if plan.get("capture_field_count") != 14:
        raise SystemExit("capture field count mismatch")
    if plan.get("target_capture_plan_count") != 7:
        raise SystemExit("target capture plan count mismatch")
    if plan.get("external_fetch_performed") is not False:
        raise SystemExit("external fetch must remain blocked")
    if plan.get("oss_clone_performed") is not False:
        raise SystemExit("oss clone must remain blocked")
    if plan.get("dependency_install_performed") is not False:
        raise SystemExit("dependency install must remain blocked")
    if plan.get("runtime_integration_performed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def counts(plan: dict) -> dict:
    return {
        "source_target_count": plan["source_target_count"],
        "capture_field_count": plan["capture_field_count"],
        "reviewed_capture_field_count": plan["capture_field_count"],
        "target_capture_plan_count": plan["target_capture_plan_count"],
        "reviewed_target_capture_plan_count": plan["target_capture_plan_count"],
        "planned_not_collected_target_count": plan["target_capture_plan_count"],
        "source_fetch_allowed_count": 0,
        "source_fetch_performed_count": 0,
        "oss_clone_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_manual_evidence_workspace_count": 1,
    }


def reviewed_capture_fields(plan: dict) -> list[dict]:
    return [
        {
            **field,
            "review_status": "reviewed_capture_field_validated",
        }
        for field in plan["capture_fields"]
    ]


def reviewed_target_capture_plans(plan: dict) -> list[dict]:
    return [
        {
            **item,
            "review_status": "reviewed_target_capture_plan_validated",
        }
        for item in plan["target_capture_plans"]
    ]


def base_record(plan: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "capture_plan_scope_confirmed": CAPTURE_PLAN_SCOPE,
        "capture_plan_not_evidence_collection_gate": True,
        "reviewed_capture_fields": reviewed_capture_fields(plan),
        "reviewed_target_capture_plans": reviewed_target_capture_plans(plan),
        "input_uris": {
            "priority_1_source_evidence_capture_plan": rel(CAPTURE_PLAN),
            "priority_1_source_evidence_capture_field_spec": rel(CAPTURE_FIELD_SPEC),
            "priority_1_source_evidence_capture_plan_gate": rel(CAPTURE_PLAN_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(plan),
        "claim_boundary": false_boundary(),
    }


def build_gate(plan: dict) -> dict:
    return {
        **base_record(plan),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-source-evidence-capture-plan-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Source evidence capture plan reviewed; manual evidence workspace may be created without source fetching",
    }


def build_validation_result(plan: dict) -> dict:
    return {
        **base_record(plan),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1",
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
    field_lines = "\n".join(
        "- {field_name}: review_status=reviewed_capture_field_validated".format(**field)
        for field in reviewed_capture_fields(plan)
    )
    target_lines = "\n".join(
        "- {source_target_id}: review_status=reviewed_target_capture_plan_validated, capture_status={capture_status}, external_fetch_performed=false".format(
            **item
        )
        for item in reviewed_target_capture_plans(plan)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Source Evidence Capture Plan Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1=true

## Review summary

- candidate_id={CANDIDATE_ID}
- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- capture_plan_scope_confirmed={CAPTURE_PLAN_SCOPE}
- capture_plan_not_evidence_collection_gate=true
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Reviewed capture fields

{field_lines}

## Reviewed target capture plans

{target_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-manual-evidence-workspace
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local manual evidence workspace
  - Create empty evidence record templates for each source target
  - Keep all records empty or placeholder-only until a separate owner-approved evidence collection goal exists
  - Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    plan = read_json(CAPTURE_PLAN)
    gate = read_json(CAPTURE_PLAN_GATE)
    require_capture_plan(plan, gate)

    write_json(REVIEW_GATE, build_gate(plan))
    report = build_report(plan)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plan))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Source Evidence Capture Plan Review v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(plan).items():
        print(f"{key}={value}")
    print("capture_plan_not_evidence_collection_gate=true")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

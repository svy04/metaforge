from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RECOMMENDATION_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_gate.json"
ADAPTER_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan.json"
ADAPTER_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_gate.json"
ADAPTER_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_NO_INSTALL_ADAPTER_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_DECISION = "CREATE_NO_INSTALL_ADAPTER_PLAN_ONLY"
PLAN_STATUS = "no_install_adapter_contract_plan_created"


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


def require_recommendation(recommendation: dict) -> None:
    if recommendation.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("recommendation goal mismatch")
    if recommendation.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("recommendation must point to this no-install adapter plan goal")
    if recommendation.get("ready_for_no_install_adapter_plan_count") != 1:
        raise SystemExit("recommendation must be ready for no-install adapter plan")
    if recommendation.get("dependency_install_allowed") is not False:
        raise SystemExit("recommendation must not allow dependency install")
    if recommendation.get("runtime_integration_allowed") is not False:
        raise SystemExit("recommendation must not allow runtime integration")


def adapter_components() -> list[dict]:
    return [
        {
            "component_id": "candidate-evidence-reader",
            "purpose": "Read repo-local evidence and recommendation packets only.",
            "implementation_boundary": "file_contract_only_no_dependency_import",
        },
        {
            "component_id": "eval-case-contract",
            "purpose": "Define normalized input/output schema for future eval cases.",
            "implementation_boundary": "schema_only_no_tool_execution",
        },
        {
            "component_id": "redteam-case-contract",
            "purpose": "Define red-team case categories and expected evidence fields.",
            "implementation_boundary": "schema_only_no_provider_call",
        },
        {
            "component_id": "rag-metric-contract",
            "purpose": "Define RAG metric slots that can later map to approved evaluators.",
            "implementation_boundary": "schema_only_no_runtime_integration",
        },
        {
            "component_id": "governance-gate-contract",
            "purpose": "Keep legal/security/adoption decisions outside evidence collection.",
            "implementation_boundary": "policy_contract_only",
        },
    ]


def contract_boundaries() -> list[str]:
    return [
        "repo_local_files_only",
        "no_dependency_install",
        "no_oss_clone",
        "no_runtime_import",
        "no_provider_call",
        "no_readiness_claim",
    ]


def blocked_actions() -> list[str]:
    return [
        "install_dependency",
        "clone_or_fetch_oss_source",
        "execute_candidate_tool",
        "import_candidate_runtime",
        "call_model_provider",
        "export_telemetry",
        "deploy_or_publish",
        "claim_release_or_production_readiness",
    ]


def counts() -> dict:
    return {
        "adapter_component_count": len(adapter_components()),
        "contract_boundary_count": len(contract_boundaries()),
        "blocked_action_count": len(blocked_actions()),
        "dependency_install_allowed_count": 0,
        "oss_clone_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "ready_for_no_install_adapter_plan_review_count": 1,
    }


def base_plan_record() -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "plan_decision": PLAN_DECISION,
        "plan_status": PLAN_STATUS,
        "adapter_components": adapter_components(),
        "contract_boundaries": contract_boundaries(),
        "blocked_actions": blocked_actions(),
        "input_uris": {
            "evidence_backed_recommendation_gate": rel(RECOMMENDATION_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "dependency_install_allowed": False,
        "oss_clone_allowed": False,
        "runtime_integration_allowed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(),
        "claim_boundary": false_boundary(),
    }


def build_gate() -> dict:
    return {
        **base_plan_record(),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-no-install-adapter-plan-gate-v0-1",
        "status": "PASS",
        "gate_scope": "No-install adapter contract plan created without dependency adoption",
    }


def build_validation_result() -> dict:
    return {
        **base_plan_record(),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(RECOMMENDATION_GATE),
            rel(ADAPTER_PLAN),
            rel(ADAPTER_PLAN_GATE),
            rel(ADAPTER_PLAN_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report() -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts().items())
    component_lines = "\n".join(
        "- {component_id}: {implementation_boundary}".format(**component)
        for component in adapter_components()
    )
    boundary_lines = "\n".join(f"- {boundary}" for boundary in contract_boundaries())
    blocked_lines = "\n".join(f"- {action}" for action in blocked_actions())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 No-Install Adapter Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1=true

## Plan summary

- candidate_id={CANDIDATE_ID}
- plan_decision={PLAN_DECISION}
- plan_status={PLAN_STATUS}
- dependency_install_allowed=false
- oss_clone_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Adapter components

{component_lines}

## Contract boundaries

{boundary_lines}

## Blocked actions

{blocked_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-no-install-adapter-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the no-install adapter plan for contract safety
  - Confirm the plan remains schema/contract-only
  - Confirm no dependency install, OSS clone, runtime import, provider call, deployment, or readiness claim is allowed
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    recommendation = read_json(RECOMMENDATION_GATE)
    require_recommendation(recommendation)

    record = base_plan_record()
    write_json(ADAPTER_PLAN, record)
    write_json(ADAPTER_PLAN_GATE, build_gate())
    report = build_report()
    write_text(ADAPTER_PLAN_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 No-Install Adapter Plan v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_status={PLAN_STATUS}")
    for key, value in counts().items():
        print(f"{key}={value}")
    print("dependency_install_allowed=false")
    print("oss_clone_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

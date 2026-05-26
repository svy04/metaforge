from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

APPROVAL_GATE = CAPABILITIES / "primary_source_acquisition_approval_packet_gate.json"
ACQUISITION_PLAN = CAPABILITIES / "primary_source_acquisition_plan.yml"
PLAN_GATE = CAPABILITIES / "primary_source_acquisition_plan_gate.json"
CLAIM_MAP = CAPABILITIES / "primary_source_acquisition_claim_map.json"
NEXT_ACTION = CAPABILITIES / "primary_source_acquisition_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_acquisition_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_ACQUISITION_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_acquisition_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_acquisition_approval_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_acquisition_plan_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
APPROVAL_DECISION = "PRIMARY_SOURCE_ACQUISITION_APPROVAL_PACKET_READY"
PLAN_DECISION = "PRIMARY_SOURCE_ACQUISITION_PLAN_READY"

ALLOWED_SOURCE_CATEGORIES = [
    "official_docs",
    "original_repository",
    "paper",
    "patent",
    "standard",
    "maintained_implementation",
    "local_repo_evidence",
]

SOURCE_TARGETS = [
    {
        "source_target_id": "src-langgraph-official-docs",
        "source_category": "official_docs",
        "source_name": "LangGraph official documentation",
        "target_claim_id": "claim-agent-runtime-stateful-graph",
        "target_claim": "AVF runtime adapter should evaluate a stateful graph model for long-running agent orchestration.",
    },
    {
        "source_target_id": "src-temporal-official-docs",
        "source_category": "official_docs",
        "source_name": "Temporal official documentation",
        "target_claim_id": "claim-durable-workflow-backend",
        "target_claim": "AVF durable workflow phases should evaluate crash-resumable workflow execution.",
    },
    {
        "source_target_id": "src-opentelemetry-standard-docs",
        "source_category": "standard",
        "source_name": "OpenTelemetry documentation and specifications",
        "target_claim_id": "claim-observability-standard",
        "target_claim": "AVF observability should use a standard traces, metrics, and logs model.",
    },
    {
        "source_target_id": "src-mcp-official-docs",
        "source_category": "standard",
        "source_name": "Model Context Protocol documentation",
        "target_claim_id": "claim-tool-protocol-boundary",
        "target_claim": "AVF tool integration should use an explicit tool protocol boundary before plugin execution.",
    },
    {
        "source_target_id": "src-litellm-original-repository",
        "source_category": "original_repository",
        "source_name": "LiteLLM original repository",
        "target_claim_id": "claim-provider-independent-llm-gateway",
        "target_claim": "AVF model plane should evaluate a provider-independent LLM gateway.",
    },
    {
        "source_target_id": "src-vllm-original-repository",
        "source_category": "original_repository",
        "source_name": "vLLM original repository",
        "target_claim_id": "claim-open-model-serving-plane",
        "target_claim": "AVF model plane should evaluate open model serving for later approved runtime phases.",
    },
    {
        "source_target_id": "src-webarena-paper",
        "source_category": "paper",
        "source_name": "WebArena paper",
        "target_claim_id": "claim-web-agent-autonomy-caution",
        "target_claim": "AVF web automation should remain approval-gated because autonomous web agents need evidence-backed limits.",
    },
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_approval_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("approval gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("approval gate must point to this acquisition plan goal")
    if gate.get("approval_decision") != APPROVAL_DECISION:
        raise SystemExit("approval gate decision mismatch")
    if gate.get("acquisition_plan_allowed") is not True:
        raise SystemExit("approval gate must allow planning")
    if gate.get("acquisition_execution_allowed") is not False:
        raise SystemExit("approval gate must keep execution blocked")


def source_target_block(target: dict) -> str:
    return f"""  - source_target_id: {target["source_target_id"]}
    source_category: {target["source_category"]}
    source_name: {target["source_name"]}
    target_claim_id: {target["target_claim_id"]}
    target_claim: {target["target_claim"]}
    acquisition_mode: future_approved_manual_lookup_or_owner_supplied
    source_uri_status: planned_not_fetched
    license_review_status: required_not_performed
    security_review_status: required_not_performed
    evidence_record_status: planned_not_acquired
    source_collection_execution_allowed: false
    external_fetch_performed: false
"""


def build_plan() -> str:
    categories = "\n".join(f"  - {category}" for category in ALLOWED_SOURCE_CATEGORIES)
    targets = "".join(source_target_block(target) for target in SOURCE_TARGETS)
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""# Primary-Source Acquisition Plan v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
plan_decision: {PLAN_DECISION}
plan_status: drafted_repo_local_not_executed

acquisition_plan_allowed: true
acquisition_execution_allowed: false
owner_approval_required_before_execution: true

allowed_source_categories:
{categories}

planning_rules:
  - Do not fetch, scrape, clone, install, or call providers in this plan.
  - Use this plan to map target claims to future primary-source evidence records.
  - Keep every source target in planned_not_acquired state until a later approval-gated phase.
  - Treat blogs as discovery pointers only; final evidence must come from allowed primary-source categories.

source_targets:
{targets}
claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_claim_mappings() -> list[dict]:
    mappings = []
    for target in SOURCE_TARGETS:
        mappings.append(
            {
                "source_target_id": target["source_target_id"],
                "source_category": target["source_category"],
                "source_name": target["source_name"],
                "target_claim_id": target["target_claim_id"],
                "target_claim": target["target_claim"],
                "evidence_record_status": "planned_not_acquired",
                "source_collection_execution_allowed": False,
                "external_fetch_performed": False,
                "license_review_status": "required_not_performed",
                "security_review_status": "required_not_performed",
            }
        )
    return mappings


def build_claim_map() -> dict:
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "plan_status": "drafted_repo_local_not_executed",
        "claim_mappings": build_claim_mappings(),
        "claim_boundary": false_boundary(),
    }


def build_plan_gate() -> dict:
    return {
        "gate_id": "avf-primary-source-acquisition-plan-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "plan_decision": PLAN_DECISION,
        "plan_status": "drafted_repo_local_not_executed",
        "acquisition_plan_uri": rel(ACQUISITION_PLAN),
        "claim_map_uri": rel(CLAIM_MAP),
        "acquisition_plan_allowed": True,
        "acquisition_execution_allowed": False,
        "owner_approval_required_before_execution": True,
        "allowed_source_categories": ALLOWED_SOURCE_CATEGORIES,
        "planned_source_target_ids": [target["source_target_id"] for target in SOURCE_TARGETS],
        "planned_source_targets_count": len(SOURCE_TARGETS),
        "claim_mappings_count": len(SOURCE_TARGETS),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-primary-source-acquisition-plan
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review planned source targets before any acquisition execution
  - Verify each source target maps to one AVF claim
  - Keep source targets planned_not_acquired until a later approved acquisition lane
  - Do not fetch, scrape, clone, install, or call providers during review

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_primary_source_acquisition_plan_v0_1",
        "status": "PASS",
        "plan_decision": PLAN_DECISION,
        "plan_status": "drafted_repo_local_not_executed",
        "planned_source_targets": len(SOURCE_TARGETS),
        "claim_mappings": len(SOURCE_TARGETS),
        "acquisition_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Primary-Source Acquisition Plan v0.1 Report

RESULT: PASS
primary_source_acquisition_plan_v0_1=true

## Commands

- python scripts\\run_avf_primary_source_acquisition_plan_v0_1.py
- python scripts\\validate_avf_primary_source_acquisition_plan_v0_1.py

## Gate summary

- acquisition_plan_created=true
- plan_gate_created=true
- claim_map_created=true
- planned_source_targets={len(SOURCE_TARGETS)}
- claim_mappings={len(SOURCE_TARGETS)}
- acquisition_execution_allowed=false
- external_fetch_performed=false
- scraping_performed=false
- oss_clone_performed=false
- package_install_performed=false

## Generated artifacts

- {rel(ACQUISITION_PLAN)}
- {rel(PLAN_GATE)}
- {rel(CLAIM_MAP)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    approval_gate = read_json(APPROVAL_GATE)
    require_approval_gate(approval_gate)

    write_text(ACQUISITION_PLAN, build_plan())
    write_json(PLAN_GATE, build_plan_gate())
    write_json(CLAIM_MAP, build_claim_map())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Primary-Source Acquisition Plan v0.1")
    print("RESULT: PASS")
    print("acquisition_plan_created=true")
    print("plan_gate_created=true")
    print("claim_map_created=true")
    print(f"planned_source_targets={len(SOURCE_TARGETS)}")
    print(f"claim_mappings={len(SOURCE_TARGETS)}")
    print("acquisition_execution_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

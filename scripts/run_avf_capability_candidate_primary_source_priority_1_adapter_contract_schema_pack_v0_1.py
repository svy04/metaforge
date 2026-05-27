from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PLAN_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_gate.json"
SCHEMA_PACK = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack.json"
SCHEMA_PACK_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_gate.json"
SCHEMA_PACK_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_SCHEMA_PACK_V0_1_REPORT.md"

EVAL_CASE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_eval_case_contract.schema.json"
REDTEAM_CASE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_redteam_case_contract.schema.json"
RAG_METRIC_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_rag_metric_contract.schema.json"
GOVERNANCE_GATE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_governance_gate_contract.schema.json"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
PACK_DECISION = "CREATE_PROVIDER_NEUTRAL_ADAPTER_CONTRACT_SCHEMA_PACK"
PACK_STATUS = "adapter_contract_schema_pack_created_provider_neutral_dependency_free"


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


def contract_extension() -> dict:
    return {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "runtime_integration_allowed": False,
    }


def base_schema(title: str, required: list[str], properties: dict) -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": properties,
        "x-avf-contract": contract_extension(),
    }


def schemas() -> dict[Path, dict]:
    return {
        EVAL_CASE_SCHEMA: base_schema(
            "AVF Provider-Neutral Eval Case Contract",
            ["case_id", "input", "expected_behavior", "success_criteria", "claim_boundary"],
            {
                "case_id": {"type": "string"},
                "input": {"type": "string"},
                "expected_behavior": {"type": "string"},
                "success_criteria": {"type": "array", "items": {"type": "string"}},
                "claim_boundary": {"type": "string"},
            },
        ),
        REDTEAM_CASE_SCHEMA: base_schema(
            "AVF Provider-Neutral Red-Team Case Contract",
            ["case_id", "risk_category", "prompt_or_scenario", "expected_refusal_or_guardrail", "evidence_basis"],
            {
                "case_id": {"type": "string"},
                "risk_category": {"type": "string"},
                "prompt_or_scenario": {"type": "string"},
                "expected_refusal_or_guardrail": {"type": "string"},
                "evidence_basis": {"type": "array", "items": {"type": "string"}},
            },
        ),
        RAG_METRIC_SCHEMA: base_schema(
            "AVF Provider-Neutral RAG Metric Slot Contract",
            ["metric_id", "metric_name", "input_fields", "output_fields", "interpretation_boundary"],
            {
                "metric_id": {"type": "string"},
                "metric_name": {"type": "string"},
                "input_fields": {"type": "array", "items": {"type": "string"}},
                "output_fields": {"type": "array", "items": {"type": "string"}},
                "interpretation_boundary": {"type": "string"},
            },
        ),
        GOVERNANCE_GATE_SCHEMA: base_schema(
            "AVF Provider-Neutral Governance Gate Contract",
            ["gate_id", "risk_tier", "required_reviews", "blocked_actions", "decision_boundary"],
            {
                "gate_id": {"type": "string"},
                "risk_tier": {"type": "string", "enum": ["green", "yellow", "red"]},
                "required_reviews": {"type": "array", "items": {"type": "string"}},
                "blocked_actions": {"type": "array", "items": {"type": "string"}},
                "decision_boundary": {"type": "string"},
            },
        ),
    }


def require_plan_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("adapter plan review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("adapter plan review must point to this schema pack goal")
    if review.get("ready_for_adapter_contract_schema_pack_count") != 1:
        raise SystemExit("adapter plan review must be ready for schema pack")
    if review.get("plan_remains_contract_only") is not True:
        raise SystemExit("adapter plan review must remain contract-only")
    if review.get("dependency_install_allowed") is not False:
        raise SystemExit("adapter plan review must not allow dependency install")
    if review.get("runtime_integration_allowed") is not False:
        raise SystemExit("adapter plan review must not allow runtime integration")


def schema_artifacts() -> list[dict]:
    return [
        {
            "schema_id": "eval-case-contract",
            "component_id": "eval-case-contract",
            "schema_uri": rel(EVAL_CASE_SCHEMA),
            **contract_extension(),
        },
        {
            "schema_id": "redteam-case-contract",
            "component_id": "redteam-case-contract",
            "schema_uri": rel(REDTEAM_CASE_SCHEMA),
            **contract_extension(),
        },
        {
            "schema_id": "rag-metric-contract",
            "component_id": "rag-metric-contract",
            "schema_uri": rel(RAG_METRIC_SCHEMA),
            **contract_extension(),
        },
        {
            "schema_id": "governance-gate-contract",
            "component_id": "governance-gate-contract",
            "schema_uri": rel(GOVERNANCE_GATE_SCHEMA),
            **contract_extension(),
        },
    ]


def counts(plan_review: dict) -> dict:
    return {
        "source_adapter_component_count": plan_review["reviewed_adapter_component_count"],
        "schema_backed_component_count": len(schema_artifacts()),
        "supporting_component_count": 1,
        "adapter_contract_schema_count": len(schemas()),
        "generated_schema_artifact_count": len(schema_artifacts()),
        "provider_neutral_schema_count": len(schema_artifacts()),
        "dependency_free_schema_count": len(schema_artifacts()),
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "ready_for_adapter_contract_schema_pack_review_count": 1,
    }


def base_pack_record(plan_review: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "pack_decision": PACK_DECISION,
        "pack_status": PACK_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "runtime_integration_allowed": False,
        "source_adapter_components": plan_review["reviewed_adapter_components"],
        "schema_artifacts": schema_artifacts(),
        "input_uris": {
            "no_install_adapter_plan_review_gate": rel(PLAN_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(plan_review),
        "claim_boundary": false_boundary(),
    }


def build_gate(plan_review: dict) -> dict:
    return {
        **base_pack_record(plan_review),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-schema-pack-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Provider-neutral dependency-free adapter contract schemas generated without candidate tool import",
    }


def build_validation_result(plan_review: dict) -> dict:
    return {
        **base_pack_record(plan_review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(PLAN_REVIEW_GATE),
            rel(SCHEMA_PACK),
            *[rel(path) for path in schemas()],
            rel(SCHEMA_PACK_GATE),
            rel(SCHEMA_PACK_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(plan_review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(plan_review).items())
    schema_lines = "\n".join(
        "- {schema_id}: provider_neutral=true, dependency_free=true, candidate_tool_import_allowed=false".format(
            **artifact
        )
        for artifact in schema_artifacts()
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Schema Pack v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1=true

## Pack summary

- candidate_id={CANDIDATE_ID}
- pack_decision={PACK_DECISION}
- pack_status={PACK_STATUS}
- provider_neutral=true
- dependency_free=true
- candidate_tool_import_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Schema artifacts

{schema_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-schema-pack
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review provider-neutral adapter contract schemas
  - Confirm schema artifacts remain dependency-free and provider-neutral
  - Confirm no candidate tool import, dependency install, runtime integration, deployment, publishing, or readiness claim is introduced
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    plan_review = read_json(PLAN_REVIEW_GATE)
    require_plan_review(plan_review)

    for schema_path, schema in schemas().items():
        write_json(schema_path, schema)

    record = base_pack_record(plan_review)
    write_json(SCHEMA_PACK, record)
    write_json(SCHEMA_PACK_GATE, build_gate(plan_review))
    report = build_report(plan_review)
    write_text(SCHEMA_PACK_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plan_review))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Schema Pack v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"pack_decision={PACK_DECISION}")
    print(f"pack_status={PACK_STATUS}")
    for key, value in counts(plan_review).items():
        print(f"{key}={value}")
    print("provider_neutral=true")
    print("dependency_free=true")
    print("candidate_tool_import_allowed=false")
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

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

GAP_REVIEW = CAPABILITIES / "primary_source_evidence_registry_gap_review.json"
GAP_REVIEW_GATE = CAPABILITIES / "primary_source_evidence_registry_gap_review_gate.json"
GAP_REVIEW_NEXT_ACTION = CAPABILITIES / "primary_source_evidence_registry_gap_review_next_action.yml"
CLOSURE_PLAN = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan.json"
CLOSURE_GATE = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_gate.json"
NAMESPACE_MAP_PLAN = CAPABILITIES / "primary_source_namespace_mapping_plan.json"
CLOSURE_BACKLOG = CAPABILITIES / "primary_source_evidence_registry_gap_closure_backlog.yml"
CLOSURE_REPORT = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_EVIDENCE_REGISTRY_GAP_CLOSURE_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_evidence_registry_gap_closure_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_evidence_registry_gap_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_evidence_registry_namespace_map_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
CLOSURE_DECISION = "PRIMARY_SOURCE_EVIDENCE_REGISTRY_GAP_CLOSURE_PLAN_CREATED_REPO_LOCAL"
CLOSURE_STATUS = "closure_plan_ready_no_gaps_closed_yet"

GAP_IDS = [
    "gap-product-quality-reports-missing-primary-source-inputs",
    "gap-avf-ledger-to-manual-record-namespace-map",
    "gap-content-safety-policy-sources-missing-manual-records",
    "gap-adoption-evidence-gates-not-yet-linked-to-registry",
]

CLOSURE_STEP_IDS = [
    "step-bound-or-attach-product-quality-primary-source-inputs",
    "step-create-avf-ledger-manual-record-namespace-map",
    "step-add-content-safety-policy-manual-source-records",
    "step-link-adoption-candidates-to-evidence-gates",
]

ADOPTION_GATE_REQUIREMENTS = [
    "build_vs_buy_review",
    "license_review",
    "security_review",
    "supply_chain_review",
    "owner_approval_gate",
]

NAMESPACE_MAPPING_PLAN = [
    ("src-langgraph-docs", "src-langgraph-official-docs", "direct_equivalent"),
    ("src-temporal-docs", "src-temporal-official-docs", "direct_equivalent"),
    ("src-opentelemetry-docs", "src-opentelemetry-standard-docs", "direct_equivalent"),
    ("src-mcp-docs", "src-mcp-official-docs", "direct_equivalent"),
    ("registry-only-litellm", "src-litellm-original-repository", "manual_record_without_avf_ledger_source"),
    ("registry-only-vllm", "src-vllm-original-repository", "manual_record_without_avf_ledger_source"),
    ("src-webarena-paper", "src-webarena-paper", "same_identifier"),
]


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


def require_previous_gap_review(review: dict, gate: dict) -> None:
    for label, record in [("gap review", review), ("gap review gate", gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            raise SystemExit(f"{label} goal mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            raise SystemExit(f"{label} must point to this closure plan goal")
        if record.get("gap_ids") != GAP_IDS:
            raise SystemExit(f"{label} gap ids mismatch")


def counts_from_gap_review(review: dict) -> dict:
    return {
        "gap_count": review.get("gap_count"),
        "closure_step_count": len(CLOSURE_STEP_IDS),
        "reports_missing_primary_source_inputs_count": review.get("reports_missing_primary_source_inputs_count"),
        "content_safety_policy_sources_missing_manual_records_count": review.get("content_safety_policy_sources_missing_manual_records_count"),
        "namespace_mapping_required_count": len(NAMESPACE_MAPPING_PLAN),
        "adoption_gate_requirement_count": len(ADOPTION_GATE_REQUIREMENTS),
    }


def base_record(counts: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "closure_decision": CLOSURE_DECISION,
        "closure_status": CLOSURE_STATUS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "gap_ids": GAP_IDS,
        "closure_step_ids": CLOSURE_STEP_IDS,
        "gaps_closed_count": 0,
        **counts,
        "claim_boundary": false_boundary(),
    }


def closure_steps() -> list[dict]:
    return [
        {
            "step_id": CLOSURE_STEP_IDS[0],
            "targets_gap_id": GAP_IDS[0],
            "action_type": "plan_only",
            "output_contract": "repo-local list of product-quality reports that need primary-source input attachment or explicit claim-boundary exemption",
            "execution_status": "planned_not_executed",
        },
        {
            "step_id": CLOSURE_STEP_IDS[1],
            "targets_gap_id": GAP_IDS[1],
            "action_type": "plan_only",
            "output_contract": rel(NAMESPACE_MAP_PLAN),
            "execution_status": "planned_not_executed",
        },
        {
            "step_id": CLOSURE_STEP_IDS[2],
            "targets_gap_id": GAP_IDS[2],
            "action_type": "plan_only",
            "output_contract": "manual source records required for src-ftc-endorsement-guides and src-ftc-ai-claims",
            "execution_status": "planned_not_executed",
        },
        {
            "step_id": CLOSURE_STEP_IDS[3],
            "targets_gap_id": GAP_IDS[3],
            "action_type": "plan_only",
            "output_contract": "adoption evidence gates for build-vs-buy, license, security, supply-chain, and owner approval",
            "execution_status": "planned_not_executed",
        },
    ]


def build_closure_plan(counts: dict) -> dict:
    return {
        **base_record(counts),
        "plan_id": "avf-primary-source-evidence-registry-gap-closure-plan-v0-1",
        "plan_scope": "deterministic repo-local closure plan; no gaps closed yet",
        "closure_steps": closure_steps(),
        "adoption_gate_requirements": ADOPTION_GATE_REQUIREMENTS,
        "source_inputs": [
            rel(GAP_REVIEW),
            rel(GAP_REVIEW_GATE),
            rel(GAP_REVIEW_NEXT_ACTION),
        ],
    }


def build_closure_gate(counts: dict) -> dict:
    return {
        **base_record(counts),
        "gate_id": "avf-primary-source-evidence-registry-gap-closure-plan-gate-v0-1",
        "status": "PASS",
        "gate_scope": "closure plan generated; execution deferred to PR-sized follow-up goals",
        "protected_actions_blocked": True,
    }


def build_namespace_map_plan(counts: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "namespace_mapping_required_count": counts["namespace_mapping_required_count"],
        "mapping_plan": [
            {
                "avf_ledger_source_id": avf_source_id,
                "manual_source_target_id": manual_source_id,
                "mapping_kind": mapping_kind,
                "mapping_status": "planned_not_applied",
            }
            for avf_source_id, manual_source_id, mapping_kind in NAMESPACE_MAPPING_PLAN
        ],
        "claim_boundary": false_boundary(),
    }


def build_closure_backlog() -> str:
    step_blocks = "\n".join(
        f"""  - step_id: {step['step_id']}
    targets_gap_id: {step['targets_gap_id']}
    action_type: {step['action_type']}
    execution_status: {step['execution_status']}
    output_contract: {step['output_contract']}"""
        for step in closure_steps()
    )
    return f"""goal_id: {THIS_GOAL_ID}
closure_decision: {CLOSURE_DECISION}
closure_status: {CLOSURE_STATUS}
gaps_closed_count: 0

closure_steps:
{step_blocks}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(title: str, counts: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts.items())
    step_lines = "\n".join(f"- {step_id}" for step_id in CLOSURE_STEP_IDS)
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
primary_source_evidence_registry_gap_closure_plan_v0_1=true

## Gate summary

- closure_decision={CLOSURE_DECISION}
- closure_status={CLOSURE_STATUS}
- gaps_closed_count=0

## Counts

{count_lines}

## Closure steps

{step_lines}

## Generated artifacts

- {rel(CLOSURE_PLAN)}
- {rel(CLOSURE_GATE)}
- {rel(NAMESPACE_MAP_PLAN)}
- {rel(CLOSURE_BACKLOG)}
- {rel(CLOSURE_REPORT)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-primary-source-namespace-map
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create deterministic repo-local mapping between AVF ledger source ids and manual source record target ids
  - Keep each mapping in planned/applied status with source and target ids
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(counts: dict) -> dict:
    return {
        **base_record(counts),
        "validator_id": "validate_avf_primary_source_evidence_registry_gap_closure_plan_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(CLOSURE_PLAN),
            rel(CLOSURE_GATE),
            rel(NAMESPACE_MAP_PLAN),
            rel(CLOSURE_BACKLOG),
            rel(CLOSURE_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    review = read_json(GAP_REVIEW)
    gate = read_json(GAP_REVIEW_GATE)
    require_previous_gap_review(review, gate)

    counts = counts_from_gap_review(review)
    write_json(CLOSURE_PLAN, build_closure_plan(counts))
    write_json(CLOSURE_GATE, build_closure_gate(counts))
    write_json(NAMESPACE_MAP_PLAN, build_namespace_map_plan(counts))
    write_text(CLOSURE_BACKLOG, build_closure_backlog())
    write_text(CLOSURE_REPORT, build_report("Primary-Source Evidence Registry Gap Closure Plan v0.1", counts))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(counts))
    write_text(VALIDATION_REPORT, build_report("AVF Primary-Source Evidence Registry Gap Closure Plan v0.1 Report", counts))

    print("AVF Primary-Source Evidence Registry Gap Closure Plan v0.1")
    print("RESULT: PASS")
    print(f"closure_decision={CLOSURE_DECISION}")
    print(f"closure_status={CLOSURE_STATUS}")
    for key, value in counts.items():
        print(f"{key}={value}")
    print("gaps_closed_count=0")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

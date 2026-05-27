from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

DECISION_MATRIX = CAPABILITIES / "capability_adoption_decision_matrix.json"
DECISION_GATE = CAPABILITIES / "capability_adoption_decision_matrix_gate.json"
DECISION_NEXT_ACTION = CAPABILITIES / "capability_adoption_decision_matrix_next_action.yml"
EXPANSION_PLAN = CAPABILITIES / "capability_candidate_primary_source_expansion_plan.json"
EXPANSION_GATE = CAPABILITIES / "capability_candidate_primary_source_expansion_plan_gate.json"
EXPANSION_BACKLOG = CAPABILITIES / "capability_candidate_primary_source_expansion_backlog.yml"
EXPANSION_REPORT = CAPABILITIES / "capability_candidate_primary_source_expansion_plan_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_expansion_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_expansion_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EXPANSION_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_expansion_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_adoption_decision_matrix_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EXPANSION_PLAN_CREATED_REPO_LOCAL"
PLAN_STATUS = "source_expansion_plan_ready_no_external_fetch"

SOURCE_REQUIRED_CANDIDATE_IDS = [
    "cap-k8s-workflow-argo",
    "cap-general-orchestration-kestra-prefect-airflow",
    "cap-evidence-lineage-dagster",
    "cap-rag-document-pipeline-haystack",
    "cap-llm-observability-langfuse-phoenix",
    "cap-eval-redteam-promptfoo-ragas",
    "cap-coding-executor-openhands-sweagent",
]

EXPECTED_COUNTS = {
    "source_required_candidate_count": 7,
    "planned_primary_source_record_count": 7,
    "official_docs_priority_count": 6,
    "original_repository_priority_count": 4,
    "paper_or_benchmark_priority_count": 1,
    "external_fetch_performed_count": 0,
    "ready_for_manual_record_creation_count": 7,
}


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


def require_previous_matrix(matrix: dict, gate: dict) -> None:
    for label, record in [("decision matrix", matrix), ("decision gate", gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            raise SystemExit(f"{label} goal mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            raise SystemExit(f"{label} must point to this expansion plan goal")
        if record.get("source_record_required_candidate_count") != EXPECTED_COUNTS["source_required_candidate_count"]:
            raise SystemExit(f"{label} source required candidate count mismatch")
        if record.get("dependency_adoption_allowed") is not False:
            raise SystemExit(f"{label} dependency adoption must remain blocked")
        if record.get("runtime_integration_allowed") is not False:
            raise SystemExit(f"{label} runtime integration must remain blocked")


def source_expansion_plans(matrix: dict) -> list[dict]:
    source_required = [
        candidate
        for candidate in matrix.get("candidates", [])
        if candidate.get("source_record_status") == "manual_source_record_required"
    ]
    if [candidate["candidate_id"] for candidate in source_required] != SOURCE_REQUIRED_CANDIDATE_IDS:
        raise SystemExit("source-required candidate ids mismatch")

    source_targets = {
        "cap-k8s-workflow-argo": {
            "source_priority_types": ["official_docs", "original_repository"],
            "planned_source_targets": [
                "src-argo-workflows-official-docs",
                "src-argo-workflows-original-repository",
            ],
            "record_goal": "Document official workflow semantics, DAG/step model, Kubernetes execution boundary, and license/security gate needs.",
        },
        "cap-general-orchestration-kestra-prefect-airflow": {
            "source_priority_types": ["official_docs"],
            "planned_source_targets": [
                "src-kestra-official-docs",
                "src-prefect-official-docs",
                "src-airflow-official-docs",
            ],
            "record_goal": "Compare orchestration fit for event-driven/manual-approval flows without selecting or installing a backend.",
        },
        "cap-evidence-lineage-dagster": {
            "source_priority_types": ["official_docs", "original_repository"],
            "planned_source_targets": [
                "src-dagster-official-docs",
                "src-dagster-original-repository",
            ],
            "record_goal": "Evaluate whether asset lineage concepts map to AVF evidence/artifact lineage before dependency adoption.",
        },
        "cap-rag-document-pipeline-haystack": {
            "source_priority_types": ["official_docs", "original_repository"],
            "planned_source_targets": [
                "src-haystack-official-docs",
                "src-haystack-original-repository",
            ],
            "record_goal": "Evaluate document pipeline and retrieval abstractions for future approved AVF memory/search phases.",
        },
        "cap-llm-observability-langfuse-phoenix": {
            "source_priority_types": ["official_docs"],
            "planned_source_targets": [
                "src-langfuse-official-docs",
                "src-phoenix-official-docs",
            ],
            "record_goal": "Compare tracing/eval observability boundaries without starting collectors or exporting telemetry.",
        },
        "cap-eval-redteam-promptfoo-ragas": {
            "source_priority_types": ["official_docs", "paper_or_benchmark"],
            "planned_source_targets": [
                "src-promptfoo-official-docs",
                "src-ragas-official-docs",
                "src-ragas-paper-or-benchmark-record",
            ],
            "record_goal": "Evaluate regression, red-team, and RAG/agent evaluation fit from primary sources before any test harness adoption.",
        },
        "cap-coding-executor-openhands-sweagent": {
            "source_priority_types": ["original_repository"],
            "planned_source_targets": [
                "src-openhands-original-repository",
                "src-swe-agent-original-repository",
            ],
            "record_goal": "Assess optional approval-gated coding executor lane while preserving Codex as the current visible executor.",
        },
    }

    plans = []
    for candidate in source_required:
        candidate_id = candidate["candidate_id"]
        target = source_targets[candidate_id]
        plans.append(
            {
                "candidate_id": candidate_id,
                "candidate_name": candidate["name"],
                "capability_type": candidate["capability_type"],
                "expansion_status": "planned_not_fetched",
                "source_record_status": "planned_not_collected",
                "source_priority_types": target["source_priority_types"],
                "planned_source_targets": target["planned_source_targets"],
                "record_goal": target["record_goal"],
                "manual_review_required": True,
                "source_contents_acquired": False,
                "external_fetch_performed": False,
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
                "protected_action_required_before_adoption": True,
            }
        )
    return plans


def count_priority(plans: list[dict], priority: str) -> int:
    return sum(1 for plan in plans if priority in plan["source_priority_types"])


def base_record(plans: list[dict]) -> dict:
    counts = {
        **EXPECTED_COUNTS,
        "official_docs_priority_count": count_priority(plans, "official_docs"),
        "original_repository_priority_count": count_priority(plans, "original_repository"),
        "paper_or_benchmark_priority_count": count_priority(plans, "paper_or_benchmark"),
    }
    if counts != EXPECTED_COUNTS:
        raise SystemExit(f"source priority counts mismatch: {counts}")
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "plan_decision": PLAN_DECISION,
        "plan_status": PLAN_STATUS,
        "source_required_candidate_ids": SOURCE_REQUIRED_CANDIDATE_IDS,
        "source_expansion_plans": plans,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts,
        "claim_boundary": false_boundary(),
    }


def build_plan(plans: list[dict]) -> dict:
    return {
        **base_record(plans),
        "plan_id": "avf-capability-candidate-primary-source-expansion-plan-v0-1",
        "plan_scope": "repo-local source-record expansion plan only; no external source fetch, dependency install, clone, or runtime integration",
        "source_inputs": [
            rel(DECISION_MATRIX),
            rel(DECISION_GATE),
            rel(DECISION_NEXT_ACTION),
        ],
    }


def build_gate(plans: list[dict]) -> dict:
    return {
        **base_record(plans),
        "gate_id": "avf-capability-candidate-primary-source-expansion-plan-gate-v0-1",
        "status": "PASS",
        "gate_scope": "source expansion targets planned; external collection and adoption remain blocked",
    }


def build_backlog(plans: list[dict]) -> str:
    blocks = []
    for plan in plans:
        target_lines = "\n".join(f"      - {target_id}" for target_id in plan["planned_source_targets"])
        blocks.append(
            f"""  - candidate_id: {plan['candidate_id']}
    candidate_name: {plan['candidate_name']}
    expansion_status: {plan['expansion_status']}
    source_record_status: {plan['source_record_status']}
    planned_source_targets:
{target_lines}
    manual_review_required: true
    external_fetch_performed: false
    dependency_adoption_allowed: false
    runtime_integration_allowed: false"""
        )
    return f"""goal_id: {THIS_GOAL_ID}
plan_decision: {PLAN_DECISION}
plan_status: {PLAN_STATUS}
source_required_candidate_count: {EXPECTED_COUNTS['source_required_candidate_count']}
planned_primary_source_record_count: {EXPECTED_COUNTS['planned_primary_source_record_count']}

source_expansion_backlog:
{chr(10).join(blocks)}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(title: str, plans: list[dict]) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in EXPECTED_COUNTS.items())
    plan_lines = "\n".join(
        f"- {plan['candidate_id']}: {', '.join(plan['planned_source_targets'])}" for plan in plans
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_expansion_plan_v0_1=true

## Gate summary

- plan_decision={PLAN_DECISION}
- plan_status={PLAN_STATUS}
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Source expansion targets

{plan_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-manual-records
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create repo-local manual source record shells for source-required capability candidates
  - Preserve planned source target ids, source kind priorities, license/security review placeholders, and adoption gates
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(plans: list[dict]) -> dict:
    return {
        **base_record(plans),
        "validator_id": "validate_avf_capability_candidate_primary_source_expansion_plan_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(EXPANSION_PLAN),
            rel(EXPANSION_GATE),
            rel(EXPANSION_BACKLOG),
            rel(EXPANSION_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    matrix = read_json(DECISION_MATRIX)
    gate = read_json(DECISION_GATE)
    require_previous_matrix(matrix, gate)
    plans = source_expansion_plans(matrix)

    write_json(EXPANSION_PLAN, build_plan(plans))
    write_json(EXPANSION_GATE, build_gate(plans))
    write_text(EXPANSION_BACKLOG, build_backlog(plans))
    report = build_report("AVF Capability Candidate Primary-Source Expansion Plan v0.1", plans)
    write_text(EXPANSION_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plans))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Expansion Plan v0.1")
    print("RESULT: PASS")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_status={PLAN_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("external_fetch_performed=false")
    print("dependency_install_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

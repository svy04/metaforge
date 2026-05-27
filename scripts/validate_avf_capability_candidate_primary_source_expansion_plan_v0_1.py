from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_expansion_plan_v0_1.py"
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

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "automated_scraping_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "runtime_export_performed",
    "collector_started",
    "telemetry_export_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    DECISION_MATRIX,
    DECISION_GATE,
    DECISION_NEXT_ACTION,
    EXPANSION_PLAN,
    EXPANSION_GATE,
    EXPANSION_BACKLOG,
    EXPANSION_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_expansion_plan_v0_1=true",
    f"plan_decision={PLAN_DECISION}",
    f"plan_status={PLAN_STATUS}",
    "source_required_candidate_count=7",
    "planned_primary_source_record_count=7",
    "official_docs_priority_count=6",
    "original_repository_priority_count=4",
    "paper_or_benchmark_priority_count=1",
    "external_fetch_performed_count=0",
    "ready_for_manual_record_creation_count=7",
    "cap-k8s-workflow-argo",
    "cap-general-orchestration-kestra-prefect-airflow",
    "cap-evidence-lineage-dagster",
    "cap-rag-document-pipeline-haystack",
    "cap-llm-observability-langfuse-phoenix",
    "cap-eval-redteam-promptfoo-ragas",
    "cap-coding-executor-openhands-sweagent",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "runtime_export_performed=false",
    "collector_started=false",
    "telemetry_export_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-manual-records",
    "owner_approval_required_before_execution: false",
    "Create repo-local manual source record shells for source-required capability candidates",
    "Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Expansion Plan v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_previous_matrix() -> None:
    for label, record in [("decision matrix", read_json(DECISION_MATRIX)), ("decision gate", read_json(DECISION_GATE))]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            fail(f"{label} goal_id mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            fail(f"{label} must point to this expansion plan goal")
        if record.get("source_record_required_candidate_count") != EXPECTED_COUNTS["source_required_candidate_count"]:
            fail(f"{label} source required candidate count mismatch")
        if record.get("dependency_adoption_allowed") is not False:
            fail(f"{label} dependency adoption must remain blocked")
        if record.get("runtime_integration_allowed") is not False:
            fail(f"{label} runtime integration must remain blocked")
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        DECISION_NEXT_ACTION,
        [
            "action_id: plan-capability-candidate-primary-source-expansion",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )


def require_plan_record(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "plan_decision": PLAN_DECISION,
        "plan_status": PLAN_STATUS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("source_required_candidate_ids") != SOURCE_REQUIRED_CANDIDATE_IDS:
        fail(f"{label} source-required candidate ids mismatch")
    plans = record.get("source_expansion_plans")
    if not isinstance(plans, list) or len(plans) != EXPECTED_COUNTS["planned_primary_source_record_count"]:
        fail(f"{label} source expansion plan count mismatch")
    for plan in plans:
        if plan.get("expansion_status") != "planned_not_fetched":
            fail(f"{label} expansion status must be planned_not_fetched")
        if plan.get("external_fetch_performed") is not False:
            fail(f"{label} must not fetch external sources")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate() -> None:
    gate = read_json(EXPANSION_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-expansion-plan-gate-v0-1":
        fail("expansion plan gate id mismatch")
    if gate.get("status") != "PASS":
        fail("expansion plan gate status must be PASS")
    require_plan_record(gate, "expansion plan gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_expansion_plan_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_plan_record(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_matrix()
    require_plan_record(read_json(EXPANSION_PLAN), "expansion plan")
    require_gate()
    require_text_markers(EXPANSION_BACKLOG, SOURCE_REQUIRED_CANDIDATE_IDS)
    require_text_markers(EXPANSION_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Expansion Plan v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_expansion_plan_v0_1=true")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_status={PLAN_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("automated_scraping_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("runtime_export_performed=false")
    print("collector_started=false")
    print("telemetry_export_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

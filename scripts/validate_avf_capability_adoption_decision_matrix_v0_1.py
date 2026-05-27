from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOCS_AVF = ROOT / "docs" / "avf"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_adoption_decision_matrix_v0_1.py"
FINAL_REVIEW = CAPABILITIES / "primary_source_registry_gap_closure_final_review.json"
FINAL_GATE = CAPABILITIES / "primary_source_registry_gap_closure_final_review_gate.json"
FINAL_NEXT_ACTION = CAPABILITIES / "primary_source_registry_gap_closure_final_review_next_action.yml"
ADOPTION_LINKS = CAPABILITIES / "primary_source_adoption_evidence_gate_links.json"
MANUAL_RECORDS = CAPABILITIES / "primary_source_manual_records.json"
OSS_MAP = DOCS_AVF / "OPEN_SOURCE_EXPANSION_MAP.md"
DECISION_MATRIX = CAPABILITIES / "capability_adoption_decision_matrix.json"
DECISION_GATE = CAPABILITIES / "capability_adoption_decision_matrix_gate.json"
DECISION_REPORT = CAPABILITIES / "capability_adoption_decision_matrix_report.md"
NEXT_ACTION = CAPABILITIES / "capability_adoption_decision_matrix_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_adoption_decision_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_ADOPTION_DECISION_MATRIX_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_adoption_decision_matrix_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_registry_gap_closure_final_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_expansion_plan_v0_1"
MATRIX_DECISION = "CAPABILITY_ADOPTION_DECISION_MATRIX_CREATED_REPO_LOCAL"
MATRIX_STATUS = "planning_only_all_adoption_blocked"

CANDIDATE_IDS = [
    "cap-agent-runtime-langgraph",
    "cap-durable-workflow-temporal",
    "cap-k8s-workflow-argo",
    "cap-general-orchestration-kestra-prefect-airflow",
    "cap-evidence-lineage-dagster",
    "cap-llm-gateway-litellm",
    "cap-local-open-model-serving-ollama-vllm",
    "cap-rag-document-pipeline-haystack",
    "cap-llm-observability-langfuse-phoenix",
    "cap-eval-redteam-promptfoo-ragas",
    "cap-tool-protocol-mcp",
    "cap-telemetry-standard-opentelemetry",
    "cap-coding-executor-openhands-sweagent",
]

GATE_IDS = [
    "gate-build-vs-buy-review",
    "gate-license-review",
    "gate-security-review",
    "gate-supply-chain-review",
    "gate-owner-approval",
]

EXPECTED_COUNTS = {
    "candidate_count": 13,
    "source_backed_candidate_count": 6,
    "source_record_required_candidate_count": 7,
    "manual_primary_source_record_count": 7,
    "gate_requirement_count": 5,
    "ready_for_adoption_count": 0,
    "blocked_candidate_count": 13,
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
    FINAL_REVIEW,
    FINAL_GATE,
    FINAL_NEXT_ACTION,
    ADOPTION_LINKS,
    MANUAL_RECORDS,
    OSS_MAP,
    DECISION_MATRIX,
    DECISION_GATE,
    DECISION_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_adoption_decision_matrix_v0_1=true",
    f"matrix_decision={MATRIX_DECISION}",
    f"matrix_status={MATRIX_STATUS}",
    "candidate_count=13",
    "source_backed_candidate_count=6",
    "source_record_required_candidate_count=7",
    "manual_primary_source_record_count=7",
    "gate_requirement_count=5",
    "ready_for_adoption_count=0",
    "blocked_candidate_count=13",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "all_candidates_blocked_until_gates_satisfied=true",
    "cap-agent-runtime-langgraph",
    "cap-durable-workflow-temporal",
    "cap-llm-gateway-litellm",
    "cap-tool-protocol-mcp",
    "cap-telemetry-standard-opentelemetry",
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
    "action_id: plan-capability-candidate-primary-source-expansion",
    "owner_approval_required_before_execution: false",
    "Create repo-local primary-source expansion plan for capability candidates without manual source records",
    "Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Adoption Decision Matrix v0.1 validation")
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


def require_previous_final_review() -> None:
    for label, record in [("final review", read_json(FINAL_REVIEW)), ("final gate", read_json(FINAL_GATE))]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            fail(f"{label} goal_id mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            fail(f"{label} must point to this decision matrix goal")
        if record.get("remaining_gap_count") != 0:
            fail(f"{label} must have remaining_gap_count=0")
        if record.get("dependency_adoption_allowed") is not False:
            fail(f"{label} dependency adoption must remain blocked")
        if record.get("runtime_integration_allowed") is not False:
            fail(f"{label} runtime integration must remain blocked")
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        FINAL_NEXT_ACTION,
        [
            "action_id: create-capability-adoption-decision-matrix",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )


def require_matrix_record(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "matrix_decision": MATRIX_DECISION,
        "matrix_status": MATRIX_STATUS,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "all_candidates_blocked_until_gates_satisfied": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("candidate_ids") != CANDIDATE_IDS:
        fail(f"{label} candidate ids mismatch")
    if record.get("gate_ids") != GATE_IDS:
        fail(f"{label} gate ids mismatch")
    candidates = record.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != EXPECTED_COUNTS["candidate_count"]:
        fail(f"{label} candidate count mismatch")
    for candidate in candidates:
        if candidate.get("adoption_status") != "blocked_until_gates_satisfied":
            fail(f"{label} candidate adoption status must stay blocked")
        if candidate.get("dependency_adoption_allowed") is not False:
            fail(f"{label} candidate dependency adoption must stay blocked")
        if candidate.get("runtime_integration_allowed") is not False:
            fail(f"{label} candidate runtime integration must stay blocked")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate() -> None:
    gate = read_json(DECISION_GATE)
    if gate.get("gate_id") != "avf-capability-adoption-decision-matrix-gate-v0-1":
        fail("decision matrix gate id mismatch")
    if gate.get("status") != "PASS":
        fail("decision matrix gate status must be PASS")
    require_matrix_record(gate, "decision matrix gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_adoption_decision_matrix_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_matrix_record(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_final_review()
    require_matrix_record(read_json(DECISION_MATRIX), "decision matrix")
    require_gate()
    require_text_markers(DECISION_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Adoption Decision Matrix v0.1 validation")
    print("RESULT: PASS")
    print("capability_adoption_decision_matrix_v0_1=true")
    print(f"matrix_decision={MATRIX_DECISION}")
    print(f"matrix_status={MATRIX_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("all_candidates_blocked_until_gates_satisfied=true")
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

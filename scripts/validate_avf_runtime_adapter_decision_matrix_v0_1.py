from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_runtime_adapter_decision_matrix_v0_1.py"
MANUAL_RECORDS = CAPABILITIES / "primary_source_manual_records.json"
INTEGRATION_REVIEW_GATE = CAPABILITIES / "primary_source_claim_integration_review_gate.json"
DECISION_MATRIX = CAPABILITIES / "runtime_adapter_decision_matrix.json"
DECISION_MATRIX_MD = CAPABILITIES / "runtime_adapter_decision_matrix.md"
GATE = CAPABILITIES / "runtime_adapter_decision_matrix_gate.json"
NEXT_ACTION = CAPABILITIES / "runtime_adapter_decision_matrix_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "runtime_adapter_decision_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_RUNTIME_ADAPTER_DECISION_MATRIX_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_runtime_adapter_decision_matrix_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_claim_integration_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_runtime_adapter_contract_skeletons_v0_1"
MATRIX_DECISION = "RUNTIME_ADAPTER_DECISION_MATRIX_READY_FOR_CONTRACT_SKELETONS"
MATRIX_SCOPE = "planning_and_contract_selection_only"

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
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

SOURCE_TARGET_IDS = [
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
]

EXPECTED_CANDIDATES = [
    ("langgraph-agent-runtime-adapter", "agent_runtime_plane", "primary_contract_candidate"),
    ("temporal-durable-workflow-backend", "durable_workflow_plane", "defer_until_runtime_state_machine"),
    ("opentelemetry-observability-standard", "observability_eval_plane", "design_contract_now"),
    ("mcp-tool-protocol-boundary", "tool_registry_plane", "design_contract_now"),
    ("litellm-provider-gateway", "model_tool_plane", "later_gateway_candidate"),
    ("vllm-open-model-serving", "model_serving_plane", "later_serving_candidate"),
    ("webarena-web-autonomy-caution", "safety_eval_plane", "cautionary_benchmark_only"),
]

REQUIRED_FILES = [
    RUNNER,
    MANUAL_RECORDS,
    INTEGRATION_REVIEW_GATE,
    DECISION_MATRIX,
    DECISION_MATRIX_MD,
    GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "runtime_adapter_decision_matrix_v0_1=true",
    f"matrix_decision={MATRIX_DECISION}",
    f"matrix_scope={MATRIX_SCOPE}",
    "decision_records=7",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "LangGraph",
    "Temporal",
    "OpenTelemetry",
    "MCP",
    "LiteLLM",
    "vLLM",
    "WebArena",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-runtime-adapter-contract-skeletons",
    "owner_approval_required_before_execution: true",
    "Generate adapter contract skeletons only",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Runtime Adapter Decision Matrix v0.1 validation")
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


def require_inputs() -> dict:
    records = read_json(MANUAL_RECORDS)
    if records.get("goal_id") != "avf_primary_source_manual_records_v0_1":
        fail("manual records goal mismatch")
    if records.get("manual_primary_source_review_performed") is not True:
        fail("manual primary-source review must be true")
    if records.get("source_contents_acquired") is not True:
        fail("source contents must have been acquired before matrix planning")
    source_records = records.get("source_records")
    if not isinstance(source_records, list) or len(source_records) != len(SOURCE_TARGET_IDS):
        fail("manual records must contain seven source records")
    if [entry.get("source_target_id") for entry in source_records] != SOURCE_TARGET_IDS:
        fail("manual record source ids mismatch")
    require_false_flags(records.get("claim_boundary", {}), "manual records")

    gate = read_json(INTEGRATION_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("integration review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("integration review gate must point to this matrix goal")
    if gate.get("implementation_planning_allowed") is not True:
        fail("implementation planning must be allowed by previous gate")
    if gate.get("dependency_adoption_allowed") is not False:
        fail("dependency adoption must remain blocked by previous gate")
    if gate.get("runtime_integration_allowed") is not False:
        fail("runtime integration must remain blocked by previous gate")
    require_false_flags(gate.get("claim_boundary", {}), "integration review gate")
    return records


def require_decision_matrix() -> None:
    matrix = read_json(DECISION_MATRIX)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "matrix_decision": MATRIX_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if matrix.get(key) != value:
            fail(f"decision matrix {key} mismatch")
    if matrix.get("source_target_ids") != SOURCE_TARGET_IDS:
        fail("decision matrix source ids mismatch")
    require_false_flags(matrix.get("claim_boundary", {}), "decision matrix")

    records = matrix.get("decision_records")
    if not isinstance(records, list) or len(records) != len(EXPECTED_CANDIDATES):
        fail("decision matrix must contain seven decision records")
    for record, (candidate_id, plane, recommendation) in zip(records, EXPECTED_CANDIDATES):
        if record.get("candidate_id") != candidate_id:
            fail(f"candidate_id mismatch for {candidate_id}")
        if record.get("plane") != plane:
            fail(f"plane mismatch for {candidate_id}")
        if record.get("recommendation") != recommendation:
            fail(f"recommendation mismatch for {candidate_id}")
        if record.get("source_target_id") not in SOURCE_TARGET_IDS:
            fail(f"source_target_id missing for {candidate_id}")
        if record.get("adoption_status") != "not_adopted_contract_planning_only":
            fail(f"adoption status must remain planning-only for {candidate_id}")
        if record.get("dependency_install_allowed") is not False:
            fail(f"dependency install must be false for {candidate_id}")
        if record.get("runtime_integration_allowed") is not False:
            fail(f"runtime integration must be false for {candidate_id}")
        if record.get("owner_approval_required_before_adoption") is not True:
            fail(f"owner approval gate missing for {candidate_id}")
        for key in [
            "primary_source_claim",
            "fit_for_avf",
            "defer_or_adopt_reason",
            "required_next_contract",
            "risk_notes",
        ]:
            if not record.get(key):
                fail(f"{candidate_id} missing {key}")


def require_gate() -> None:
    gate = read_json(GATE)
    expected = {
        "gate_id": "avf-runtime-adapter-decision-matrix-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "matrix_decision": MATRIX_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "decision_records": len(EXPECTED_CANDIDATES),
        "implementation_planning_allowed": True,
        "contract_skeleton_generation_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_runtime_adapter_decision_matrix_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("matrix_decision") != MATRIX_DECISION:
        fail("validation result decision mismatch")
    if result.get("decision_records") != len(EXPECTED_CANDIDATES):
        fail("validation result record count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_inputs()
    require_decision_matrix()
    require_text_markers(DECISION_MATRIX_MD, TEXT_MARKERS)
    require_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, TEXT_MARKERS + [
        "RESULT: PASS",
        "protected_action_executed=false",
        "provider_calls_performed=false",
        "live_model_calls_performed=false",
        "external_service_calls_performed=false",
        "dependency_install_performed=false",
        "external_fetch_performed=false",
        "oss_clone_performed=false",
        "runtime_integration_performed=false",
        "deploy_performed=false",
        "publish_performed=false",
        "release_ready=false",
        "production_ready=false",
    ])

    print("AVF Runtime Adapter Decision Matrix v0.1 validation")
    print("RESULT: PASS")
    print("runtime_adapter_decision_matrix_v0_1=true")
    print(f"matrix_decision={MATRIX_DECISION}")
    print(f"matrix_scope={MATRIX_SCOPE}")
    print("decision_records=7")
    print("implementation_planning_allowed=true")
    print("contract_skeleton_generation_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
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
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

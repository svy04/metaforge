from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_runtime_adapter_contract_skeletons_v0_1.py"
DECISION_MATRIX = CAPABILITIES / "runtime_adapter_decision_matrix.json"
DECISION_MATRIX_GATE = CAPABILITIES / "runtime_adapter_decision_matrix_gate.json"
MANIFEST = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_manifest.json"
GATE = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_RUNTIME_ADAPTER_CONTRACT_SKELETONS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_runtime_adapter_contract_skeletons_v0_1"
PREVIOUS_GOAL_ID = "avf_runtime_adapter_decision_matrix_v0_1"
NEXT_SAFE_GOAL_ID = "avf_runtime_adapter_contract_review_v0_1"
SKELETON_DECISION = "RUNTIME_ADAPTER_CONTRACT_SKELETONS_READY_FOR_REVIEW"
SKELETON_SCOPE = "repo_local_contract_skeletons_only"

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

EXPECTED_CONTRACTS = [
    ("langgraph-agent-runtime-adapter", ROOT / "avf" / "runtime" / "agent_graph_adapter_contract.md"),
    ("temporal-durable-workflow-backend", ROOT / "avf" / "runtime" / "durable_workflow_adapter_contract.md"),
    ("opentelemetry-observability-standard", ROOT / "avf" / "observability" / "telemetry_event_contract.md"),
    ("mcp-tool-protocol-boundary", ROOT / "avf" / "integrations" / "mcp_tool_registry_contract.md"),
    ("litellm-provider-gateway", ROOT / "avf" / "integrations" / "llm_gateway_contract.md"),
    ("vllm-open-model-serving", ROOT / "avf" / "integrations" / "open_model_serving_contract.md"),
    ("webarena-web-autonomy-caution", ROOT / "avf" / "evals" / "web_autonomy_safety_eval_contract.md"),
]

REQUIRED_FILES = [
    RUNNER,
    DECISION_MATRIX,
    DECISION_MATRIX_GATE,
    MANIFEST,
    GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
    *[path for _, path in EXPECTED_CONTRACTS],
]

CONTRACT_MARKERS = [
    "contract_status: skeleton_only",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "provider_calls_performed=false",
    "external_service_calls_performed=false",
    "protected_action_executed=false",
    "release_ready=false",
    "production_ready=false",
    "## Purpose",
    "## Contract Inputs",
    "## Contract Outputs",
    "## Safety Gates",
    "## Evidence Hooks",
    "## Non-goals",
    "## Next Review Gate",
]

TEXT_MARKERS = [
    "runtime_adapter_contract_skeletons_v0_1=true",
    f"skeleton_decision={SKELETON_DECISION}",
    f"skeleton_scope={SKELETON_SCOPE}",
    "contract_skeletons_created=7",
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
    "action_id: review-runtime-adapter-contract-skeletons",
    "owner_approval_required_before_execution: true",
    "Review the generated contract skeletons",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Runtime Adapter Contract Skeletons v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{rel(path)} missing markers:\n" + "\n".join(missing))


def require_previous_matrix() -> dict:
    matrix = read_json(DECISION_MATRIX)
    if matrix.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("decision matrix goal mismatch")
    if matrix.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("decision matrix must point to this contract skeleton goal")
    if matrix.get("contract_skeleton_generation_allowed") is not True:
        fail("contract skeleton generation must be allowed")
    if matrix.get("dependency_adoption_allowed") is not False:
        fail("dependency adoption must remain blocked")
    if matrix.get("runtime_integration_allowed") is not False:
        fail("runtime integration must remain blocked")
    records = matrix.get("decision_records")
    if not isinstance(records, list) or len(records) != len(EXPECTED_CONTRACTS):
        fail("decision matrix must contain seven decision records")
    require_false_flags(matrix.get("claim_boundary", {}), "decision matrix")

    gate = read_json(DECISION_MATRIX_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("decision matrix gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("decision matrix gate must point to this contract skeleton goal")
    if gate.get("contract_skeleton_generation_allowed") is not True:
        fail("previous gate must allow contract skeleton generation")
    require_false_flags(gate.get("claim_boundary", {}), "decision matrix gate")
    return matrix


def require_contracts(matrix: dict) -> None:
    matrix_records = {record["candidate_id"]: record for record in matrix["decision_records"]}
    manifest = read_json(MANIFEST)
    if manifest.get("goal_id") != THIS_GOAL_ID:
        fail("manifest goal mismatch")
    if manifest.get("previous_goal_id") != PREVIOUS_GOAL_ID:
        fail("manifest previous goal mismatch")
    if manifest.get("skeleton_decision") != SKELETON_DECISION:
        fail("manifest decision mismatch")
    if manifest.get("skeleton_scope") != SKELETON_SCOPE:
        fail("manifest scope mismatch")
    if manifest.get("contract_skeletons_created") != len(EXPECTED_CONTRACTS):
        fail("manifest contract count mismatch")
    if manifest.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("manifest next safe goal mismatch")
    require_false_flags(manifest.get("claim_boundary", {}), "manifest")

    contracts = manifest.get("contracts")
    if not isinstance(contracts, list) or len(contracts) != len(EXPECTED_CONTRACTS):
        fail("manifest must list seven contracts")

    for manifest_entry, (candidate_id, path) in zip(contracts, EXPECTED_CONTRACTS):
        if manifest_entry.get("candidate_id") != candidate_id:
            fail(f"manifest candidate mismatch for {candidate_id}")
        if manifest_entry.get("contract_uri") != rel(path):
            fail(f"manifest contract_uri mismatch for {candidate_id}")
        if manifest_entry.get("contract_status") != "skeleton_only":
            fail(f"manifest contract status mismatch for {candidate_id}")
        if manifest_entry.get("source_target_id") != matrix_records[candidate_id]["source_target_id"]:
            fail(f"manifest source target mismatch for {candidate_id}")
        if manifest_entry.get("dependency_adoption_allowed") is not False:
            fail(f"manifest dependency install must be false for {candidate_id}")
        if manifest_entry.get("runtime_integration_allowed") is not False:
            fail(f"manifest runtime integration must be false for {candidate_id}")

        require_text_markers(path, CONTRACT_MARKERS)
        require_text_markers(path, [
            f"candidate_id: {candidate_id}",
            f"source_target_id: {matrix_records[candidate_id]['source_target_id']}",
            f"primary_source_uri: {matrix_records[candidate_id]['primary_source_uri']}",
            f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
        ])


def require_gate() -> None:
    gate = read_json(GATE)
    expected = {
        "gate_id": "avf-runtime-adapter-contract-skeletons-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "skeleton_decision": SKELETON_DECISION,
        "skeleton_scope": SKELETON_SCOPE,
        "contract_skeletons_created": len(EXPECTED_CONTRACTS),
        "contract_review_allowed": True,
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
    if result.get("validator_id") != "validate_avf_runtime_adapter_contract_skeletons_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("skeleton_decision") != SKELETON_DECISION:
        fail("validation result decision mismatch")
    if result.get("contract_skeletons_created") != len(EXPECTED_CONTRACTS):
        fail("validation result contract count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    matrix = require_previous_matrix()
    require_contracts(matrix)
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

    print("AVF Runtime Adapter Contract Skeletons v0.1 validation")
    print("RESULT: PASS")
    print("runtime_adapter_contract_skeletons_v0_1=true")
    print(f"skeleton_decision={SKELETON_DECISION}")
    print(f"skeleton_scope={SKELETON_SCOPE}")
    print("contract_skeletons_created=7")
    print("contract_review_allowed=true")
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

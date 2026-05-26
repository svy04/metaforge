from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_runtime_adapter_contract_review_v0_1.py"
MANIFEST = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_manifest.json"
SKELETON_GATE = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_gate.json"
REVIEW_GATE = RUNTIME_GENERATED / "runtime_adapter_contract_review_gate.json"
REVIEW_REPORT = RUNTIME_GENERATED / "runtime_adapter_contract_review_report.md"
NEXT_ACTION = RUNTIME_GENERATED / "runtime_adapter_contract_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "runtime_adapter_contract_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_RUNTIME_ADAPTER_CONTRACT_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_runtime_adapter_contract_review_v0_1"
PREVIOUS_GOAL_ID = "avf_runtime_adapter_contract_skeletons_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_adapter_stub_v0_1"
REVIEW_DECISION = "CONTRACT_SKELETONS_REVIEWED_AGENT_GRAPH_ADAPTER_SELECTED_FOR_STUB"
REVIEW_SCOPE = "review_and_first_stub_selection_only"
SELECTED_CANDIDATE_ID = "langgraph-agent-runtime-adapter"
SELECTED_CONTRACT_URI = "avf/runtime/agent_graph_adapter_contract.md"

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

REQUIRED_FILES = [
    RUNNER,
    MANIFEST,
    SKELETON_GATE,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "runtime_adapter_contract_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_scope={REVIEW_SCOPE}",
    "contracts_reviewed=7",
    f"selected_candidate_id={SELECTED_CANDIDATE_ID}",
    f"selected_contract_uri={SELECTED_CONTRACT_URI}",
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
    "action_id: create-agent-graph-adapter-stub",
    "owner_approval_required_before_execution: true",
    "Create a repo-local agent graph adapter stub",
    "Do not install LangGraph or any runtime dependency",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Runtime Adapter Contract Review v0.1 validation")
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


def require_previous_skeletons() -> dict:
    manifest = read_json(MANIFEST)
    if manifest.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("manifest goal mismatch")
    if manifest.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("manifest must point to this review goal")
    if manifest.get("contract_skeletons_created") != 7:
        fail("manifest must contain seven contract skeletons")
    if manifest.get("dependency_adoption_allowed") is not False:
        fail("dependency adoption must remain blocked")
    if manifest.get("runtime_integration_allowed") is not False:
        fail("runtime integration must remain blocked")
    require_false_flags(manifest.get("claim_boundary", {}), "manifest")

    gate = read_json(SKELETON_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("skeleton gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("skeleton gate must point to this review goal")
    if gate.get("contract_review_allowed") is not True:
        fail("contract review must be allowed")
    require_false_flags(gate.get("claim_boundary", {}), "skeleton gate")
    return manifest


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    expected = {
        "gate_id": "avf-runtime-adapter-contract-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "contracts_reviewed": 7,
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "selected_contract_uri": SELECTED_CONTRACT_URI,
        "stub_creation_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_runtime_adapter_contract_review_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
    if result.get("selected_candidate_id") != SELECTED_CANDIDATE_ID:
        fail("validation result selected candidate mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_skeletons()
    require_review_gate()
    require_text_markers(REVIEW_REPORT, TEXT_MARKERS)
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

    print("AVF Runtime Adapter Contract Review v0.1 validation")
    print("RESULT: PASS")
    print("runtime_adapter_contract_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print("contracts_reviewed=7")
    print(f"selected_candidate_id={SELECTED_CANDIDATE_ID}")
    print(f"selected_contract_uri={SELECTED_CONTRACT_URI}")
    print("stub_creation_allowed=true")
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

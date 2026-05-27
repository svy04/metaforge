from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1.py"
ACCEPTANCE_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_gate.json"
ACCEPTANCE_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_next_action.yml"
IMPLEMENTATION_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan.json"
IMPLEMENTATION_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan_report.md"
IMPLEMENTATION_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_IMPLEMENTATION_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_harness_acceptance_gate_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PLAN_DECISION = "CREATE_REPO_LOCAL_NO_INSTALL_ADAPTER_IMPLEMENTATION_PLAN_FROM_REVIEWED_ACCEPTANCE_GATE"
PLAN_STATUS = "planned_for_repo_local_adapter_scaffold_not_runtime_or_dependency_ready"

EXPECTED_COUNTS = {
    "source_schema_artifact_count": 4,
    "baseline_fixture_result_count": 8,
    "mutation_runner_result_count": 5,
    "all_fixture_result_count": 13,
    "all_fixture_result_matched_expected_count": 13,
    "reviewed_acceptance_criteria_count": 6,
    "reviewed_acceptance_criteria_passed_count": 6,
    "source_contract_count": 4,
    "implementation_task_count": 7,
    "planned_file_target_count": 4,
    "validation_command_count": 3,
    "blocked_action_count": 10,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "plan_blocker_count": 0,
    "ready_for_adapter_scaffold_count": 1,
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
    ACCEPTANCE_REVIEW_GATE,
    ACCEPTANCE_REVIEW_NEXT_ACTION,
    IMPLEMENTATION_PLAN,
    IMPLEMENTATION_PLAN_REPORT,
    IMPLEMENTATION_PLAN_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

SOURCE_CONTRACT_IDS = [
    "eval-case-contract",
    "redteam-case-contract",
    "rag-metric-contract",
    "governance-gate-contract",
]

IMPLEMENTATION_TASK_IDS = [
    "adapter-contract-boundary-module",
    "eval-case-record-normalizer",
    "redteam-case-record-normalizer",
    "rag-metric-record-normalizer",
    "governance-gate-record-normalizer",
    "repo-local-validation-harness-entrypoint",
    "evidence-ledger-v2-mapping",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"plan_decision={PLAN_DECISION}",
    f"plan_status={PLAN_STATUS}",
    "source_contract_count=4",
    "implementation_task_count=7",
    "planned_file_target_count=4",
    "validation_command_count=3",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "plan_blocker_count=0",
    "ready_for_adapter_scaffold_count=1",
    "provider_neutral=true",
    "dependency_free=true",
    "candidate_tool_import_allowed=false",
    "dependency_install_allowed=false",
    "external_fetch_allowed=false",
    "runtime_integration_allowed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-scaffold",
    "owner_approval_required_before_execution: false",
    "Create a repo-local adapter scaffold from the implementation plan without importing candidate tools",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Implementation Plan v0.1 validation")
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


def require_acceptance_review_gate() -> dict:
    gate = read_json(ACCEPTANCE_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("acceptance review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("acceptance review gate must point to this implementation plan goal")
    if gate.get("ready_for_adapter_implementation_plan_count") != 1:
        fail("acceptance review gate must be ready for implementation plan")
    for key, value in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "review_blocker_count": 0,
    }.items():
        if gate.get(key) != value:
            fail(f"acceptance review gate {key} mismatch")
    for key, value in {
        "source_schema_artifact_count": 4,
        "all_fixture_result_count": 13,
        "all_fixture_result_matched_expected_count": 13,
        "reviewed_acceptance_criteria_count": 6,
        "reviewed_acceptance_criteria_passed_count": 6,
    }.items():
        if gate.get(key) != value:
            fail(f"acceptance review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "acceptance review gate claim boundary")
    require_text_markers(
        ACCEPTANCE_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-implementation-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_source_contract(item: dict) -> None:
    for key in ["contract_id", "schema_uri", "valid_fixture_uri", "invalid_fixture_uri", "implementation_scope"]:
        if not item.get(key):
            fail(f"source contract missing {key}")
    if item.get("contract_id") not in SOURCE_CONTRACT_IDS:
        fail(f"unexpected source contract {item.get('contract_id')}")
    for key in ["candidate_tool_import_allowed", "dependency_install_allowed", "external_fetch_allowed", "runtime_integration_allowed"]:
        if item.get(key) is not False:
            fail(f"source contract {item.get('contract_id')} must keep {key}=false")


def require_implementation_task(item: dict) -> None:
    for key in ["task_id", "goal", "acceptance_criteria", "planned_file_targets", "validation_commands", "claim_boundary"]:
        if not item.get(key):
            fail(f"implementation task missing {key}")
    if item.get("task_id") not in IMPLEMENTATION_TASK_IDS:
        fail(f"unexpected implementation task {item.get('task_id')}")
    for key in ["candidate_tool_import_allowed", "dependency_install_allowed", "external_fetch_allowed", "runtime_integration_allowed"]:
        if item.get(key) is not False:
            fail(f"implementation task {item.get('task_id')} must keep {key}=false")


def require_plan_record(record: dict, label: str, gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "plan_decision": PLAN_DECISION,
        "plan_status": PLAN_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("adapter_contract_validation_harness_acceptance_gate_review_gate") != ACCEPTANCE_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} acceptance review gate input uri mismatch")
    if record.get("reviewed_acceptance_criteria") != gate.get("reviewed_acceptance_criteria"):
        fail(f"{label} reviewed acceptance criteria mismatch")
    source_contracts = record.get("source_contracts", [])
    if len(source_contracts) != EXPECTED_COUNTS["source_contract_count"]:
        fail(f"{label} source contract count mismatch")
    for item in source_contracts:
        require_source_contract(item)
    tasks = record.get("implementation_tasks", [])
    if len(tasks) != EXPECTED_COUNTS["implementation_task_count"]:
        fail(f"{label} implementation task count mismatch")
    for item in tasks:
        require_implementation_task(item)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_plan_record(result, "validation result", gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    gate = require_acceptance_review_gate()
    require_plan_record(read_json(IMPLEMENTATION_PLAN), "implementation plan", gate)
    require_text_markers(IMPLEMENTATION_PLAN_REPORT, REPORT_MARKERS)
    require_text_markers(IMPLEMENTATION_PLAN_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Implementation Plan v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_status={PLAN_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("provider_neutral=true")
    print("dependency_free=true")
    print("candidate_tool_import_allowed=false")
    print("dependency_install_allowed=false")
    print("external_fetch_allowed=false")
    print("runtime_integration_allowed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
ADAPTER_ROOT = ROOT / "avf" / "capabilities" / "adapters" / "priority_1"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1.py"
IMPLEMENTATION_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan.json"
IMPLEMENTATION_PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan_next_action.yml"
ADAPTER_CONTRACTS = ADAPTER_ROOT / "adapter_contracts.py"
RECORD_NORMALIZERS = ADAPTER_ROOT / "record_normalizers.py"
REPO_LOCAL_VALIDATION_HARNESS = ADAPTER_ROOT / "repo_local_validation_harness.py"
EVIDENCE_MAPPING = ADAPTER_ROOT / "evidence_mapping.py"
SCAFFOLD_VALIDATION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_validation.json"
SCAFFOLD_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_report.md"
SCAFFOLD_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_SCAFFOLD_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
SCAFFOLD_DECISION = "CREATE_REPO_LOCAL_ADAPTER_SCAFFOLD_FROM_IMPLEMENTATION_PLAN"
SCAFFOLD_STATUS = "repo_local_adapter_scaffold_created_not_runtime_or_dependency_ready"

EXPECTED_COUNTS = {
    "source_contract_count": 4,
    "implementation_task_count": 7,
    "adapter_module_count": 4,
    "normalized_record_count": 4,
    "evidence_entry_count": 4,
    "validation_command_count": 3,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "scaffold_blocker_count": 0,
    "ready_for_adapter_scaffold_review_count": 1,
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
    IMPLEMENTATION_PLAN,
    IMPLEMENTATION_PLAN_NEXT_ACTION,
    ADAPTER_CONTRACTS,
    RECORD_NORMALIZERS,
    REPO_LOCAL_VALIDATION_HARNESS,
    EVIDENCE_MAPPING,
    SCAFFOLD_VALIDATION,
    SCAFFOLD_REPORT,
    SCAFFOLD_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"scaffold_decision={SCAFFOLD_DECISION}",
    f"scaffold_status={SCAFFOLD_STATUS}",
    "source_contract_count=4",
    "implementation_task_count=7",
    "adapter_module_count=4",
    "normalized_record_count=4",
    "evidence_entry_count=4",
    "validation_command_count=3",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "scaffold_blocker_count=0",
    "ready_for_adapter_scaffold_review_count=1",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-scaffold",
    "owner_approval_required_before_execution: false",
    "Review the repo-local adapter scaffold before expanding it into executable local tests",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Scaffold v0.1 validation")
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


def require_implementation_plan() -> dict:
    plan = read_json(IMPLEMENTATION_PLAN)
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("implementation plan goal_id mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("implementation plan must point to this scaffold goal")
    if plan.get("ready_for_adapter_scaffold_count") != 1:
        fail("implementation plan must be ready for adapter scaffold")
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
        "plan_blocker_count": 0,
    }.items():
        if plan.get(key) != value:
            fail(f"implementation plan {key} mismatch")
    if len(plan.get("source_contracts", [])) != EXPECTED_COUNTS["source_contract_count"]:
        fail("implementation plan source contract count mismatch")
    if len(plan.get("implementation_tasks", [])) != EXPECTED_COUNTS["implementation_task_count"]:
        fail("implementation plan task count mismatch")
    require_false_flags(plan.get("claim_boundary", {}), "implementation plan claim boundary")
    require_text_markers(
        IMPLEMENTATION_PLAN_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-scaffold",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return plan


def require_imported_modules() -> tuple[object, object, object, object]:
    sys.path.insert(0, str(ROOT))
    contracts = importlib.import_module("avf.capabilities.adapters.priority_1.adapter_contracts")
    normalizers = importlib.import_module("avf.capabilities.adapters.priority_1.record_normalizers")
    harness = importlib.import_module("avf.capabilities.adapters.priority_1.repo_local_validation_harness")
    evidence = importlib.import_module("avf.capabilities.adapters.priority_1.evidence_mapping")
    for module, name in [
        (contracts, "adapter_contracts"),
        (normalizers, "record_normalizers"),
        (harness, "repo_local_validation_harness"),
        (evidence, "evidence_mapping"),
    ]:
        if getattr(module, "CANDIDATE_TOOL_IMPORT_ALLOWED", None) is not False:
            fail(f"{name} must keep candidate tool import blocked")
        if getattr(module, "DEPENDENCY_INSTALL_ALLOWED", None) is not False:
            fail(f"{name} must keep dependency install blocked")
        if getattr(module, "EXTERNAL_FETCH_ALLOWED", None) is not False:
            fail(f"{name} must keep external fetch blocked")
        if getattr(module, "RUNTIME_INTEGRATION_ALLOWED", None) is not False:
            fail(f"{name} must keep runtime integration blocked")
    return contracts, normalizers, harness, evidence


def require_scaffold_record(record: dict, label: str, plan: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "scaffold_decision": SCAFFOLD_DECISION,
        "scaffold_status": SCAFFOLD_STATUS,
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
    if input_uris.get("adapter_implementation_plan") != IMPLEMENTATION_PLAN.relative_to(ROOT).as_posix():
        fail(f"{label} implementation plan input uri mismatch")
    if record.get("source_contracts") != plan.get("source_contracts"):
        fail(f"{label} source contracts mismatch")
    normalized = record.get("normalized_records", [])
    if len(normalized) != EXPECTED_COUNTS["normalized_record_count"]:
        fail(f"{label} normalized record count mismatch")
    evidence_entries = record.get("evidence_entries", [])
    if len(evidence_entries) != EXPECTED_COUNTS["evidence_entry_count"]:
        fail(f"{label} evidence entry count mismatch")
    for item in normalized:
        for key in ["source_contract_id", "record_id", "normalized_record_type", "claim_boundary"]:
            if not item.get(key):
                fail(f"{label} normalized record missing {key}")
        for key in ["candidate_tool_import_allowed", "dependency_install_allowed", "external_fetch_allowed", "runtime_integration_allowed"]:
            if item.get(key) is not False:
                fail(f"{label} normalized record {item.get('record_id')} must keep {key}=false")
    for item in evidence_entries:
        for key in ["artifact_id", "source_contract_id", "claim", "claim_boundary", "validation_method", "validation_result"]:
            if not item.get(key):
                fail(f"{label} evidence entry missing {key}")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(plan: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_scaffold_record(result, "validation result", plan)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    plan = require_implementation_plan()
    _, normalizers, harness, evidence = require_imported_modules()
    fixture_map = harness.load_valid_fixture_map(ROOT)
    normalized_records = harness.run_repo_local_validation(fixture_map)
    if len(normalized_records) != EXPECTED_COUNTS["normalized_record_count"]:
        fail("runtime harness normalized record count mismatch")
    if normalizers.normalize_repo_local_fixture("eval-case-contract", fixture_map["eval-case-contract"]).get("normalized_record_type") != "eval_case":
        fail("eval case normalizer contract mismatch")
    if len(evidence.build_evidence_entries(normalized_records)) != EXPECTED_COUNTS["evidence_entry_count"]:
        fail("evidence mapping entry count mismatch")
    require_scaffold_record(read_json(SCAFFOLD_VALIDATION), "scaffold validation", plan)
    require_text_markers(SCAFFOLD_REPORT, REPORT_MARKERS)
    require_text_markers(SCAFFOLD_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(plan)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Scaffold v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"scaffold_decision={SCAFFOLD_DECISION}")
    print(f"scaffold_status={SCAFFOLD_STATUS}")
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

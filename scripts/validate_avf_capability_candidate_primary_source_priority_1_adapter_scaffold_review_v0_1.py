from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1.py"
SCAFFOLD_VALIDATION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_validation.json"
SCAFFOLD_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_SCAFFOLD_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_local_tests_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_SCAFFOLD_REVIEWED"
REVIEW_STATUS = "adapter_scaffold_reviewed_ready_for_executable_local_tests"

EXPECTED_COUNTS = {
    "source_contract_count": 4,
    "implementation_task_count": 7,
    "adapter_module_count": 4,
    "reviewed_adapter_module_count": 4,
    "normalized_record_count": 4,
    "reviewed_normalized_record_count": 4,
    "evidence_entry_count": 4,
    "reviewed_evidence_entry_count": 4,
    "validation_command_count": 3,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "scaffold_blocker_count": 0,
    "review_blocker_count": 0,
    "ready_for_adapter_scaffold_review_count": 1,
    "ready_for_adapter_local_tests_count": 1,
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
    SCAFFOLD_VALIDATION,
    SCAFFOLD_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    REVIEW_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "adapter_module_count=4",
    "reviewed_adapter_module_count=4",
    "normalized_record_count=4",
    "reviewed_normalized_record_count=4",
    "evidence_entry_count=4",
    "reviewed_evidence_entry_count=4",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "runtime_integration_allowed_count=0",
    "review_blocker_count=0",
    "ready_for_adapter_local_tests_count=1",
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
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-local-tests",
    "owner_approval_required_before_execution: false",
    "Create executable repo-local tests for the adapter scaffold without candidate tool imports",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Scaffold Review v0.1 validation")
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


def require_scaffold_validation() -> dict:
    scaffold = read_json(SCAFFOLD_VALIDATION)
    if scaffold.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("scaffold validation goal_id mismatch")
    if scaffold.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("scaffold validation must point to this review goal")
    if scaffold.get("ready_for_adapter_scaffold_review_count") != 1:
        fail("scaffold validation must be ready for review")
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
        "scaffold_blocker_count": 0,
    }.items():
        if scaffold.get(key) != value:
            fail(f"scaffold validation {key} mismatch")
    for key, value in {
        "adapter_module_count": 4,
        "normalized_record_count": 4,
        "evidence_entry_count": 4,
    }.items():
        if scaffold.get(key) != value:
            fail(f"scaffold validation {key} mismatch")
    require_false_flags(scaffold.get("claim_boundary", {}), "scaffold validation claim boundary")
    require_text_markers(
        SCAFFOLD_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-adapter-scaffold",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return scaffold


def require_review_record(record: dict, label: str, scaffold: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
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
    if input_uris.get("adapter_scaffold_validation") != SCAFFOLD_VALIDATION.relative_to(ROOT).as_posix():
        fail(f"{label} scaffold validation input uri mismatch")
    if record.get("adapter_module_uris") != scaffold.get("adapter_module_uris"):
        fail(f"{label} adapter module uris mismatch")
    if record.get("normalized_records") != scaffold.get("normalized_records"):
        fail(f"{label} normalized records mismatch")
    if record.get("evidence_entries") != scaffold.get("evidence_entries"):
        fail(f"{label} evidence entries mismatch")
    if len(record.get("reviewed_adapter_modules", [])) != EXPECTED_COUNTS["reviewed_adapter_module_count"]:
        fail(f"{label} reviewed adapter module count mismatch")
    for module in record.get("reviewed_adapter_modules", []):
        if module.get("review_status") != "reviewed_adapter_module_preserves_repo_local_boundary":
            fail(f"{label} reviewed adapter module status mismatch")
        for key in ["candidate_tool_import_allowed", "dependency_install_allowed", "external_fetch_allowed", "runtime_integration_allowed"]:
            if module.get(key) is not False:
                fail(f"{label} reviewed adapter module must keep {key}=false")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(scaffold: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", scaffold)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    scaffold = require_scaffold_validation()
    require_review_record(read_json(REVIEW_GATE), "review gate", scaffold)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(REVIEW_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(scaffold)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Scaffold Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
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

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GOAL_GENERATED = ROOT / "avf" / "goals" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"

RUNNER = ROOT / "scripts" / "run_avf_active_objective_completion_matrix_v0_1.py"
MATRIX = GOAL_GENERATED / "active_objective_completion_matrix_v0_1.json"
NEXT_CODEX_TASK = GOAL_GENERATED / "active_objective_completion_matrix_next_codex_task_packet.yml"
VALIDATION_RESULT = GOAL_GENERATED / "active_objective_completion_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_ACTIVE_OBJECTIVE_COMPLETION_MATRIX_V0_1_REPORT.md"
PROTECTED_BOUNDARY = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_review_protected_action_required_boundary.json"

THIS_GOAL_ID = "avf_active_objective_completion_matrix_v0_1"
NEXT_SAFE_GOAL_ID = "avf_local_primary_source_evidence_acceptance_harness_v0_1"
TERMINAL_CONDITION = "ACTIVE_OBJECTIVE_NOT_COMPLETE_PROTECTED_ACTION_REQUIRED_FOR_SOURCE_COLLECTION"
OBJECTIVE_TEXT = "그럼 끝내지 말고 오픈소스 쓸거 다 쓰고 논문 인용할꺼 다 쓰고 1차 자료 다 써서 구현하고 완성 되고 완벽해질때까지 끝내지마"

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

REQUIREMENT_IDS = [
    "REQ-001-preserve-full-objective",
    "REQ-002-use-validated-open-source",
    "REQ-003-cite-papers",
    "REQ-004-use-primary-sources",
    "REQ-005-implement-toward-factory-infrastructure",
    "REQ-006-prove-completion-requirement-by-requirement",
    "REQ-007-respect-protected-action-boundaries",
    "REQ-008-avoid-production-or-release-claims",
]

REQUIRED_FILES = [
    RUNNER,
    MATRIX,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
    PROTECTED_BOUNDARY,
]

NEXT_TASK_MARKERS = [
    "task_id: avf-local-primary-source-evidence-acceptance-harness-v0-1",
    "owner-supplied primary-source evidence",
    "No source collection execution",
    "No provider calls",
    "No live model calls",
    "No external service calls",
    "No automated scraping",
    "No OSS clone",
    "No package install",
    "No dependency install",
    "No runtime integration",
    "No deploy",
    "No publish",
    "No release readiness claim",
    "No production readiness claim",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "active_objective_completion_matrix_v0_1=true",
    f"terminal_condition={TERMINAL_CONDITION}",
    "objective_completion_proven=false",
    "foundation_ready_scope=repo_local_internal_only",
    "requirements_total=8",
    "requirements_proven=4",
    "requirements_partial=2",
    "requirements_blocked=1",
    "requirements_unproven=1",
    "source_collection_terminal_condition=PROTECTED_ACTION_REQUIRED",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Active Objective Completion Matrix v0.1 validation")
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


def require_protected_boundary() -> None:
    boundary = read_json(PROTECTED_BOUNDARY)
    if boundary.get("terminal_condition") != "PROTECTED_ACTION_REQUIRED":
        fail("source collection boundary must be PROTECTED_ACTION_REQUIRED")
    if boundary.get("owner_input_required") is not True:
        fail("source collection boundary must require owner input")
    if boundary.get("collection_execution_allowed") is not False:
        fail("source collection boundary must keep collection blocked")
    require_false_flags(boundary.get("claim_boundary", {}), "source collection boundary")


def require_matrix() -> None:
    matrix = read_json(MATRIX)
    if matrix.get("matrix_id") != THIS_GOAL_ID:
        fail("matrix_id mismatch")
    if matrix.get("objective") != OBJECTIVE_TEXT:
        fail("objective text mismatch")
    if matrix.get("terminal_condition") != TERMINAL_CONDITION:
        fail("terminal condition mismatch")
    if matrix.get("objective_completion_proven") is not False:
        fail("matrix must not prove full objective completion")
    if matrix.get("foundation_ready_scope") != "repo_local_internal_only":
        fail("foundation ready scope mismatch")
    if matrix.get("source_collection_terminal_condition") != "PROTECTED_ACTION_REQUIRED":
        fail("source collection terminal condition mismatch")
    if matrix.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("next safe goal mismatch")
    require_false_flags(matrix.get("claim_boundary", {}), "matrix")

    requirements = matrix.get("requirements", [])
    if [item.get("id") for item in requirements] != REQUIREMENT_IDS:
        fail("requirement ids mismatch")
    counts = matrix.get("requirement_counts", {})
    expected_counts = {
        "total": 8,
        "proven": 4,
        "partial": 2,
        "blocked": 1,
        "unproven": 1,
    }
    if counts != expected_counts:
        fail(f"requirement counts mismatch: {counts}")
    statuses = {item["id"]: item["status"] for item in requirements}
    expected_statuses = {
        "REQ-001-preserve-full-objective": "PROVEN",
        "REQ-002-use-validated-open-source": "PARTIAL",
        "REQ-003-cite-papers": "PARTIAL",
        "REQ-004-use-primary-sources": "BLOCKED_OWNER_ACTION_FOR_EXTERNAL_COLLECTION",
        "REQ-005-implement-toward-factory-infrastructure": "PROVEN",
        "REQ-006-prove-completion-requirement-by-requirement": "PROVEN",
        "REQ-007-respect-protected-action-boundaries": "PROVEN",
        "REQ-008-avoid-production-or-release-claims": "UNPROVEN_FOR_FULL_OBJECTIVE",
    }
    if statuses != expected_statuses:
        fail(f"requirement statuses mismatch: {statuses}")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_active_objective_completion_matrix_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("objective_completion_proven") is not False:
        fail("validation result must not prove full objective completion")
    if result.get("terminal_condition") != TERMINAL_CONDITION:
        fail("validation result terminal condition mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_protected_boundary()
    require_matrix()
    require_text_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Active Objective Completion Matrix v0.1 validation")
    print("RESULT: PASS")
    print("active_objective_completion_matrix_v0_1=true")
    print(f"terminal_condition={TERMINAL_CONDITION}")
    print("objective_completion_proven=false")
    print("foundation_ready_scope=repo_local_internal_only")
    print("requirements_total=8")
    print("requirements_proven=4")
    print("requirements_partial=2")
    print("requirements_blocked=1")
    print("requirements_unproven=1")
    print("source_collection_terminal_condition=PROTECTED_ACTION_REQUIRED")
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

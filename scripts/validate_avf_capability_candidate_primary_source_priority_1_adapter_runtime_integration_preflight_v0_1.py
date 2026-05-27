from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1.py"
BEHAVIOR_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_gate.json"
BEHAVIOR_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_next_action.yml"
PREFLIGHT_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_gate.json"
PREFLIGHT_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_report.md"
PREFLIGHT_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_RUNTIME_INTEGRATION_PREFLIGHT_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PREFLIGHT_DECISION = "RUNTIME_INTEGRATION_REQUIRES_OWNER_AUTHORIZATION_AND_SEPARATE_SANDBOX_PLAN"
PREFLIGHT_STATUS = "repo_local_preflight_passed_runtime_integration_still_blocked"

EXPECTED_COUNTS = {
    "adapter_module_count": 4,
    "behavior_requirement_count": 6,
    "reviewed_behavior_requirement_count": 6,
    "runtime_preflight_check_count": 8,
    "runtime_preflight_check_pass_count": 8,
    "runtime_preflight_check_fail_count": 0,
    "owner_authorization_required_count": 1,
    "sandbox_plan_required_count": 1,
    "license_review_required_count": 1,
    "security_review_required_count": 1,
    "runtime_integration_allowed_count": 0,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "preflight_blocker_count": 0,
    "ready_for_runtime_integration_authorization_packet_count": 1,
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
    BEHAVIOR_REVIEW_GATE,
    BEHAVIOR_REVIEW_NEXT_ACTION,
    PREFLIGHT_GATE,
    PREFLIGHT_REPORT,
    PREFLIGHT_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PREFLIGHT_CHECK_IDS = [
    "candidate-tool-import-remains-blocked",
    "dependency-install-remains-blocked",
    "external-fetch-remains-blocked",
    "runtime-integration-remains-blocked",
    "runtime-export-remains-blocked",
    "owner-authorization-required-before-runtime",
    "sandbox-plan-required-before-runtime",
    "license-and-security-review-required-before-runtime",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"preflight_decision={PREFLIGHT_DECISION}",
    f"preflight_status={PREFLIGHT_STATUS}",
    "runtime_preflight_check_count=8",
    "runtime_preflight_check_pass_count=8",
    "runtime_preflight_check_fail_count=0",
    "owner_authorization_required_count=1",
    "sandbox_plan_required_count=1",
    "license_review_required_count=1",
    "security_review_required_count=1",
    "runtime_integration_allowed_count=0",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "preflight_blocker_count=0",
    "ready_for_runtime_integration_authorization_packet_count=1",
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
    "action_id: create-capability-candidate-primary-source-priority-1-adapter-runtime-integration-authorization-packet",
    "owner_approval_required_before_execution: false",
    "Create an owner authorization packet before any runtime, tool, dependency, or external fetch step",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Preflight v0.1 validation")
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


def require_behavior_review_gate() -> dict:
    gate = read_json(BEHAVIOR_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("behavior review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("behavior review gate must point to this preflight goal")
    if gate.get("ready_for_runtime_integration_preflight_count") != 1:
        fail("behavior review gate must be ready for runtime integration preflight")
    for key, value in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "review_blocker_count": 0,
    }.items():
        if gate.get(key) != value:
            fail(f"behavior review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "behavior review gate claim boundary")
    require_text_markers(
        BEHAVIOR_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-runtime-integration-preflight",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_preflight_check(item: dict) -> None:
    for key in ["check_id", "status", "runtime_action_allowed", "evidence"]:
        if key not in item:
            fail(f"preflight check missing {key}")
    if item["check_id"] not in PREFLIGHT_CHECK_IDS:
        fail(f"unexpected preflight check {item['check_id']}")
    if item["status"] != "PASS":
        fail(f"preflight check {item['check_id']} must pass")
    if item["runtime_action_allowed"] is not False:
        fail(f"preflight check {item['check_id']} must not allow runtime action")


def require_preflight_record(record: dict, label: str, source: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "preflight_decision": PREFLIGHT_DECISION,
        "preflight_status": PREFLIGHT_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "runtime_integration_performed": False,
        "runtime_export_performed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("adapter_behavior_expansion_review_gate") != BEHAVIOR_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} behavior review gate input uri mismatch")
    if record.get("reviewed_behavior_requirements") != source.get("reviewed_behavior_requirements"):
        fail(f"{label} reviewed behavior requirements mismatch")
    checks = record.get("runtime_preflight_checks", [])
    if len(checks) != EXPECTED_COUNTS["runtime_preflight_check_count"]:
        fail(f"{label} runtime preflight check count mismatch")
    for item in checks:
        require_preflight_check(item)
    if sorted(item["check_id"] for item in checks) != sorted(PREFLIGHT_CHECK_IDS):
        fail(f"{label} runtime preflight check ids mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(source: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_preflight_record(result, "validation result", source)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    source = require_behavior_review_gate()
    require_preflight_record(read_json(PREFLIGHT_GATE), "preflight gate", source)
    require_text_markers(PREFLIGHT_REPORT, REPORT_MARKERS)
    require_text_markers(PREFLIGHT_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(source)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Preflight v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"preflight_decision={PREFLIGHT_DECISION}")
    print(f"preflight_status={PREFLIGHT_STATUS}")
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

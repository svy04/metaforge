from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1.py"
PREFLIGHT_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_gate.json"
PREFLIGHT_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_next_action.yml"
AUTH_PACKET = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet.json"
AUTH_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_report.md"
AUTH_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_RUNTIME_INTEGRATION_AUTHORIZATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
AUTHORIZATION_DECISION = "REQUEST_OWNER_AUTHORIZATION_FOR_FUTURE_RUNTIME_INTEGRATION_ONLY"
AUTHORIZATION_STATUS = "owner_authorization_required_not_granted"

EXPECTED_COUNTS = {
    "runtime_preflight_check_count": 8,
    "authorization_item_count": 6,
    "authorization_item_not_granted_count": 6,
    "protected_action_required_count": 6,
    "owner_input_required_count": 1,
    "sandbox_plan_required_count": 1,
    "license_review_required_count": 1,
    "security_review_required_count": 1,
    "runtime_integration_allowed_count": 0,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "external_fetch_allowed_count": 0,
    "authorization_blocker_count": 0,
    "ready_for_runtime_integration_authorization_packet_review_count": 1,
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
    PREFLIGHT_GATE,
    PREFLIGHT_NEXT_ACTION,
    AUTH_PACKET,
    AUTH_REPORT,
    AUTH_NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

AUTHORIZATION_ITEM_IDS = [
    "authorize-candidate-tool-import",
    "authorize-dependency-install",
    "authorize-external-source-fetch",
    "authorize-runtime-integration",
    "authorize-runtime-export",
    "authorize-external-service-call",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"authorization_decision={AUTHORIZATION_DECISION}",
    f"authorization_status={AUTHORIZATION_STATUS}",
    "owner_authorization_granted=false",
    "runtime_preflight_check_count=8",
    "authorization_item_count=6",
    "authorization_item_not_granted_count=6",
    "protected_action_required_count=6",
    "owner_input_required_count=1",
    "sandbox_plan_required_count=1",
    "license_review_required_count=1",
    "security_review_required_count=1",
    "runtime_integration_allowed_count=0",
    "candidate_tool_import_allowed_count=0",
    "dependency_install_allowed_count=0",
    "external_fetch_allowed_count=0",
    "authorization_blocker_count=0",
    "ready_for_runtime_integration_authorization_packet_review_count=1",
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
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-runtime-integration-authorization-packet",
    "owner_approval_required_before_execution: false",
    "Review the repo-local authorization packet before asking the owner to approve any protected action",
    "Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Authorization Packet v0.1 validation")
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


def require_preflight_gate() -> dict:
    gate = read_json(PREFLIGHT_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("preflight gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("preflight gate must point to this authorization packet goal")
    if gate.get("ready_for_runtime_integration_authorization_packet_count") != 1:
        fail("preflight gate must be ready for authorization packet")
    for key, value in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "preflight_blocker_count": 0,
    }.items():
        if gate.get(key) != value:
            fail(f"preflight gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "preflight gate claim boundary")
    require_text_markers(
        PREFLIGHT_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-runtime-integration-authorization-packet",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_authorization_item(item: dict) -> None:
    for key in ["authorization_item_id", "requested_action", "authorization_status", "protected_action_required", "action_allowed"]:
        if key not in item:
            fail(f"authorization item missing {key}")
    if item["authorization_item_id"] not in AUTHORIZATION_ITEM_IDS:
        fail(f"unexpected authorization item {item['authorization_item_id']}")
    if item["authorization_status"] != "not_granted":
        fail(f"authorization item {item['authorization_item_id']} must remain not_granted")
    if item["protected_action_required"] is not True:
        fail(f"authorization item {item['authorization_item_id']} must require protected action approval")
    if item["action_allowed"] is not False:
        fail(f"authorization item {item['authorization_item_id']} must not allow action")


def require_authorization_record(record: dict, label: str, source: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "authorization_decision": AUTHORIZATION_DECISION,
        "authorization_status": AUTHORIZATION_STATUS,
        "owner_authorization_granted": False,
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
    if input_uris.get("adapter_runtime_integration_preflight_gate") != PREFLIGHT_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} preflight gate input uri mismatch")
    if record.get("runtime_preflight_checks") != source.get("runtime_preflight_checks"):
        fail(f"{label} runtime preflight checks mismatch")
    items = record.get("authorization_items", [])
    if len(items) != EXPECTED_COUNTS["authorization_item_count"]:
        fail(f"{label} authorization item count mismatch")
    for item in items:
        require_authorization_item(item)
    if sorted(item["authorization_item_id"] for item in items) != sorted(AUTHORIZATION_ITEM_IDS):
        fail(f"{label} authorization item ids mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_validation_result(source: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_authorization_record(result, "validation result", source)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    source = require_preflight_gate()
    require_authorization_record(read_json(AUTH_PACKET), "authorization packet", source)
    require_text_markers(AUTH_REPORT, REPORT_MARKERS)
    require_text_markers(AUTH_NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(source)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Authorization Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"authorization_decision={AUTHORIZATION_DECISION}")
    print(f"authorization_status={AUTHORIZATION_STATUS}")
    print("owner_authorization_granted=false")
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

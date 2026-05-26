from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_acquisition_approval_packet_v0_1.py"
PREVIOUS_REVIEW_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_review_gate.json"
APPROVAL_PACKET = CAPABILITIES / "primary_source_acquisition_approval_packet.yml"
APPROVAL_GATE = CAPABILITIES / "primary_source_acquisition_approval_packet_gate.json"
NEXT_ACTION = CAPABILITIES / "primary_source_acquisition_approval_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_acquisition_approval_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_ACQUISITION_APPROVAL_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_acquisition_approval_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_owner_input_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_acquisition_plan_v0_1"
PREVIOUS_REVIEW_DECISION = "OWNER_INPUT_PACKET_REJECTED_EMPTY_SOURCE_RECORD"
APPROVAL_DECISION = "PRIMARY_SOURCE_ACQUISITION_APPROVAL_PACKET_READY"

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

ALLOWED_SOURCE_CATEGORIES = [
    "official_docs",
    "original_repository",
    "paper",
    "patent",
    "standard",
    "maintained_implementation",
    "local_repo_evidence",
]

DENIED_ACTIONS = [
    "bulk_scraping",
    "credentialed_account_access",
    "private_data_collection",
    "package_install",
    "dependency_install",
    "oss_clone",
    "runtime_integration",
    "provider_call",
    "live_model_call",
    "deploy",
    "publish",
    "production_readiness_claim",
    "release_readiness_claim",
]

REQUIRED_FILES = [
    RUNNER,
    PREVIOUS_REVIEW_GATE,
    APPROVAL_PACKET,
    APPROVAL_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

APPROVAL_PACKET_MARKERS = [
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"approval_decision: {APPROVAL_DECISION}",
    "approval_status: planning_only_not_approved_for_execution",
    "acquisition_plan_allowed: true",
    "acquisition_execution_allowed: false",
    "external_fetch_allowed: false",
    "scraping_allowed: false",
    "provider_calls_allowed: false",
    "clone_or_install_allowed: false",
    "official_docs",
    "original_repository",
    "paper",
    "patent",
    "standard",
    "maintained_implementation",
    "local_repo_evidence",
    "bulk_scraping",
    "credentialed_account_access",
    "private_data_collection",
    "package_install",
    "runtime_integration",
    "protected_action_executed: false",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: draft-primary-source-acquisition-plan",
    "owner_approval_required_before_execution: true",
    "Plan source acquisition without fetching, scraping, cloning, installing, or calling providers",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_acquisition_approval_packet_v0_1=true",
    "approval_packet_created=true",
    "approval_gate_created=true",
    "approval_status=planning_only_not_approved_for_execution",
    "acquisition_plan_allowed=true",
    "acquisition_execution_allowed=false",
    "external_fetch_allowed=false",
    "scraping_allowed=false",
    "provider_calls_allowed=false",
    "clone_or_install_allowed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "dependency_install_performed=false",
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
    print("AVF Primary-Source Acquisition Approval Packet v0.1 validation")
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


def require_previous_review_gate() -> None:
    gate = read_json(PREVIOUS_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous review gate must point to this approval packet goal")
    if gate.get("review_decision") != PREVIOUS_REVIEW_DECISION:
        fail("previous review gate decision mismatch")
    if gate.get("source_collection_execution_allowed") is not False:
        fail("previous review gate must keep source collection blocked")
    require_false_flags(gate.get("claim_boundary", {}), "previous review gate")


def require_approval_gate() -> None:
    gate = read_json(APPROVAL_GATE)
    expected = {
        "gate_id": "avf-primary-source-acquisition-approval-packet-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "approval_decision": APPROVAL_DECISION,
        "approval_status": "planning_only_not_approved_for_execution",
        "acquisition_plan_allowed": True,
        "acquisition_execution_allowed": False,
        "external_fetch_allowed": False,
        "scraping_allowed": False,
        "provider_calls_allowed": False,
        "clone_or_install_allowed": False,
        "owner_approval_required_before_execution": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"approval gate {key} mismatch")
    if gate.get("allowed_source_categories") != ALLOWED_SOURCE_CATEGORIES:
        fail("approval gate allowed source categories mismatch")
    if gate.get("denied_actions") != DENIED_ACTIONS:
        fail("approval gate denied actions mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "approval gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_acquisition_approval_packet_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("approval_decision") != APPROVAL_DECISION:
        fail("validation result approval decision mismatch")
    if result.get("acquisition_execution_allowed") is not False:
        fail("validation result must keep acquisition execution blocked")
    if result.get("owner_approval_required_before_execution") is not True:
        fail("validation result must require owner approval before execution")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_review_gate()
    require_text_markers(APPROVAL_PACKET, APPROVAL_PACKET_MARKERS)
    require_approval_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Acquisition Approval Packet v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_acquisition_approval_packet_v0_1=true")
    print("approval_packet_created=true")
    print("approval_gate_created=true")
    print("approval_status=planning_only_not_approved_for_execution")
    print("acquisition_plan_allowed=true")
    print("acquisition_execution_allowed=false")
    print("external_fetch_allowed=false")
    print("scraping_allowed=false")
    print("provider_calls_allowed=false")
    print("clone_or_install_allowed=false")
    print("owner_approval_required_before_execution=true")
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

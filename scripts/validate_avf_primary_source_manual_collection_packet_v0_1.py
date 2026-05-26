from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_manual_collection_packet_v0_1.py"
SKELETONS = CAPABILITIES / "primary_source_record_skeletons.json"
SKELETONS_REVIEW_GATE = CAPABILITIES / "primary_source_record_skeletons_review_gate.json"
PACKET = CAPABILITIES / "primary_source_manual_collection_packet.json"
PACKET_MARKDOWN = CAPABILITIES / "primary_source_manual_collection_packet.md"
PACKET_GATE = CAPABILITIES / "primary_source_manual_collection_packet_gate.json"
NEXT_ACTION = CAPABILITIES / "primary_source_manual_collection_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_manual_collection_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_MANUAL_COLLECTION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_manual_collection_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_record_skeletons_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_manual_records_v0_1"
REVIEW_DECISION = "PRIMARY_SOURCE_RECORD_SKELETONS_REVIEWED_COLLECTION_BLOCKED"
PACKET_DECISION = "PRIMARY_SOURCE_MANUAL_COLLECTION_PACKET_READY_NOT_EXECUTED"

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

REQUIRED_SOURCE_FIELDS = [
    "source_id",
    "source_title",
    "source_kind",
    "source_uri",
    "source_version_or_date",
    "source_owner_or_publisher",
    "license_or_rights_note",
    "claim_supported",
    "evidence_excerpt_summary",
    "verification_notes",
]

REQUIRED_FILES = [
    RUNNER,
    SKELETONS,
    SKELETONS_REVIEW_GATE,
    PACKET,
    PACKET_MARKDOWN,
    PACKET_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    f"packet_decision={PACKET_DECISION}",
    "collection_tasks=7",
    "manual_collection_execution_status=not_executed",
    "source_contents_acquired=false",
    "external_fetch_performed=false",
    "automated_scraping_performed=false",
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
    "source_uri: to_be_filled_during_manual_collection",
    "evidence_excerpt_summary: to_be_filled_during_manual_collection",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-primary-source-manual-records",
    "owner_approval_required_before_execution: true",
    "Create manual primary-source records from official docs, original repositories, standards, and papers",
    "Do not automate scraping, clone repositories, install packages, deploy, publish, or call providers",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_manual_collection_packet_v0_1=true",
    f"packet_decision={PACKET_DECISION}",
    "collection_tasks=7",
    "manual_collection_execution_status=not_executed",
    "all_tasks_planned_not_acquired=true",
    "source_contents_acquired=false",
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
    print("AVF Primary-Source Manual Collection Packet v0.1 validation")
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


def require_skeleton_review_gate() -> None:
    gate = read_json(SKELETONS_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("skeleton review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("skeleton review gate must point to this packet goal")
    if gate.get("review_decision") != REVIEW_DECISION:
        fail("skeleton review gate decision mismatch")
    if gate.get("reviewed_source_target_ids") != SOURCE_TARGET_IDS:
        fail("skeleton review gate source target ids mismatch")
    if gate.get("collection_remains_blocked") is not True:
        fail("skeleton review gate must keep collection blocked")
    require_false_flags(gate.get("claim_boundary", {}), "skeleton review gate")


def require_packet() -> None:
    packet = read_json(PACKET)
    if packet.get("goal_id") != THIS_GOAL_ID:
        fail("packet goal_id mismatch")
    if packet.get("previous_goal_id") != PREVIOUS_GOAL_ID:
        fail("packet previous_goal_id mismatch")
    if packet.get("packet_decision") != PACKET_DECISION:
        fail("packet decision mismatch")
    if packet.get("manual_collection_execution_status") != "not_executed":
        fail("manual collection must remain not_executed")
    tasks = packet.get("collection_tasks")
    if not isinstance(tasks, list) or len(tasks) != len(SOURCE_TARGET_IDS):
        fail("packet must contain seven collection tasks")
    if [task.get("source_target_id") for task in tasks] != SOURCE_TARGET_IDS:
        fail("collection task source target ids mismatch")
    for task in tasks:
        if task.get("evidence_record_status") != "planned_not_acquired":
            fail("collection task status must remain planned_not_acquired")
        if task.get("source_contents_acquired") is not False:
            fail("collection task source contents must be false")
        if task.get("automated_collection_allowed") is not False:
            fail("automated collection must remain blocked")
        if task.get("external_fetch_performed") is not False:
            fail("collection task external_fetch_performed must be false")
        if task.get("required_source_fields") != REQUIRED_SOURCE_FIELDS:
            fail("collection task required fields mismatch")
        if task.get("source_uri") != "to_be_filled_during_manual_collection":
            fail("collection task source_uri placeholder mismatch")
        if task.get("evidence_excerpt_summary") != "to_be_filled_during_manual_collection":
            fail("collection task evidence summary placeholder mismatch")
    require_false_flags(packet.get("claim_boundary", {}), "manual collection packet")


def require_packet_gate() -> None:
    gate = read_json(PACKET_GATE)
    expected = {
        "gate_id": "avf-primary-source-manual-collection-packet-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "packet_decision": PACKET_DECISION,
        "collection_tasks": len(SOURCE_TARGET_IDS),
        "manual_collection_execution_status": "not_executed",
        "all_tasks_planned_not_acquired": True,
        "source_contents_acquired": False,
        "automated_collection_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"packet gate {key} mismatch")
    if gate.get("source_target_ids") != SOURCE_TARGET_IDS:
        fail("packet gate source target ids mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "packet gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_manual_collection_packet_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("packet_decision") != PACKET_DECISION:
        fail("validation result packet decision mismatch")
    if result.get("manual_collection_execution_status") != "not_executed":
        fail("validation result must keep collection not_executed")
    if result.get("collection_tasks") != len(SOURCE_TARGET_IDS):
        fail("validation result collection task count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_skeleton_review_gate()
    require_packet()
    require_text_markers(PACKET_MARKDOWN, PACKET_MARKERS)
    require_packet_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Manual Collection Packet v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_manual_collection_packet_v0_1=true")
    print(f"packet_decision={PACKET_DECISION}")
    print("collection_tasks=7")
    print("manual_collection_execution_status=not_executed")
    print("all_tasks_planned_not_acquired=true")
    print("source_contents_acquired=false")
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

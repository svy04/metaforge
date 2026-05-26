from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_manual_records_v0_1.py"
PACKET_GATE = CAPABILITIES / "primary_source_manual_collection_packet_gate.json"
RECORDS = CAPABILITIES / "primary_source_manual_records.json"
RECORDS_MARKDOWN = CAPABILITIES / "primary_source_manual_records.md"
RECORDS_GATE = CAPABILITIES / "primary_source_manual_records_gate.json"
NEXT_ACTION = CAPABILITIES / "primary_source_manual_records_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_manual_records_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_MANUAL_RECORDS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_manual_records_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_manual_collection_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_records_review_v0_1"
PACKET_DECISION = "PRIMARY_SOURCE_MANUAL_COLLECTION_PACKET_READY_NOT_EXECUTED"
RECORD_DECISION = "PRIMARY_SOURCE_MANUAL_RECORDS_CREATED_FROM_PRIMARY_SOURCES"

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

REQUIRED_RECORD_FIELDS = [
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
    "source_reference_lines",
    "retrieval_method",
]

REQUIRED_FILES = [
    RUNNER,
    PACKET_GATE,
    RECORDS,
    RECORDS_MARKDOWN,
    RECORDS_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

RECORD_MARKERS = [
    f"record_decision={RECORD_DECISION}",
    "source_records=7",
    "manual_primary_source_review_performed=true",
    "source_contents_acquired=true",
    "automated_collection_allowed=false",
    "external_fetch_performed=false",
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
    "https://docs.langchain.com/oss/python/langgraph/overview",
    "https://docs.temporal.io/",
    "https://opentelemetry.io/docs/what-is-opentelemetry/",
    "https://modelcontextprotocol.io/docs/getting-started/intro",
    "https://github.com/BerriAI/litellm",
    "https://github.com/vllm-project/vllm",
    "https://arxiv.org/abs/2307.13854",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-primary-source-manual-records",
    "owner_approval_required_before_execution: true",
    "Review manually recorded primary-source evidence before integrating claims",
    "Do not install, clone, deploy, publish, or call providers",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_manual_records_v0_1=true",
    f"record_decision={RECORD_DECISION}",
    "source_records=7",
    "manual_primary_source_review_performed=true",
    "source_contents_acquired=true",
    "all_records_have_primary_source_uris=true",
    "all_records_have_evidence_summaries=true",
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
    print("AVF Primary-Source Manual Records v0.1 validation")
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


def require_packet_gate() -> None:
    gate = read_json(PACKET_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("manual collection packet gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("manual collection packet gate must point to this records goal")
    if gate.get("packet_decision") != PACKET_DECISION:
        fail("manual collection packet gate decision mismatch")
    if gate.get("source_target_ids") != SOURCE_TARGET_IDS:
        fail("manual collection packet gate source target ids mismatch")
    if gate.get("manual_collection_execution_status") != "not_executed":
        fail("manual collection packet must remain not_executed")
    require_false_flags(gate.get("claim_boundary", {}), "manual collection packet gate")


def require_records() -> None:
    data = read_json(RECORDS)
    if data.get("goal_id") != THIS_GOAL_ID:
        fail("records goal_id mismatch")
    if data.get("previous_goal_id") != PREVIOUS_GOAL_ID:
        fail("records previous_goal_id mismatch")
    if data.get("record_decision") != RECORD_DECISION:
        fail("record decision mismatch")
    if data.get("manual_primary_source_review_performed") is not True:
        fail("manual primary-source review must be true")
    records = data.get("source_records")
    if not isinstance(records, list) or len(records) != len(SOURCE_TARGET_IDS):
        fail("records must contain seven source records")
    if [record.get("source_target_id") for record in records] != SOURCE_TARGET_IDS:
        fail("source record ids mismatch")
    for record in records:
        if record.get("source_record_status") != "manual_primary_source_record_created":
            fail("source record status mismatch")
        if record.get("source_contents_acquired") is not True:
            fail("source record contents must be acquired")
        if record.get("automated_collection_allowed") is not False:
            fail("automated collection must remain blocked")
        if record.get("external_fetch_performed") is not False:
            fail("record external_fetch_performed must be false")
        source_record = record.get("source_record", {})
        for field in REQUIRED_RECORD_FIELDS:
            if field not in source_record:
                fail(f"source record missing field {field}")
            value = source_record[field]
            if isinstance(value, str) and not value.strip():
                fail(f"source record field {field} must not be blank")
            if isinstance(value, str) and "to_be_filled" in value:
                fail(f"source record field {field} must be filled")
        if not source_record["source_uri"].startswith("https://"):
            fail("source_uri must be https primary source")
        if len(source_record["evidence_excerpt_summary"]) < 40:
            fail("evidence summary must be substantive")
        if "Manual primary-source review" not in source_record["verification_notes"]:
            fail("verification notes must identify manual primary-source review")
    require_false_flags(data.get("claim_boundary", {}), "manual source records")


def require_records_gate() -> None:
    gate = read_json(RECORDS_GATE)
    expected = {
        "gate_id": "avf-primary-source-manual-records-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "record_decision": RECORD_DECISION,
        "source_records": len(SOURCE_TARGET_IDS),
        "manual_primary_source_review_performed": True,
        "source_contents_acquired": True,
        "all_records_have_primary_source_uris": True,
        "all_records_have_evidence_summaries": True,
        "automated_collection_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"records gate {key} mismatch")
    if gate.get("source_target_ids") != SOURCE_TARGET_IDS:
        fail("records gate source target ids mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "records gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_manual_records_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("record_decision") != RECORD_DECISION:
        fail("validation result record decision mismatch")
    if result.get("source_records") != len(SOURCE_TARGET_IDS):
        fail("validation result record count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_packet_gate()
    require_records()
    require_text_markers(RECORDS_MARKDOWN, RECORD_MARKERS)
    require_records_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Manual Records v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_manual_records_v0_1=true")
    print(f"record_decision={RECORD_DECISION}")
    print("source_records=7")
    print("manual_primary_source_review_performed=true")
    print("source_contents_acquired=true")
    print("all_records_have_primary_source_uris=true")
    print("all_records_have_evidence_summaries=true")
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

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_codex_primary_source_output_packet_v0_1.py"
PREVIOUS_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_review_gate.json"
OUTPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet.yml"
OUTPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_gate.json"
OUTPUT_PACKET_REPORT = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_CODEX_PRIMARY_SOURCE_OUTPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_codex_primary_source_output_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_review_v0_1"
SUPERSEDED_GOAL_ID = "avf_capability_candidate_primary_source_pro_actual_output_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1"
PACKET_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_CODEX_PRIMARY_SOURCE_OUTPUT_PACKET_CREATED"
PACKET_STATUS = "codex_primary_source_records_supplied_unaccepted"

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "source_record_count": 16,
    "required_source_field_count": 12,
    "filled_record_supplied_count": 16,
    "accepted_records": 0,
    "assistant_web_primary_source_research_performed_count": 1,
    "gpt_pro_output_supplied_count": 0,
    "codex_script_external_fetch_performed_count": 0,
    "dependency_install_performed_count": 0,
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
    "source_reference_lines",
    "retrieval_method",
]

REQUIRED_FILES = [
    RUNNER,
    PREVIOUS_REVIEW_GATE,
    OUTPUT_PACKET,
    OUTPUT_PACKET_GATE,
    OUTPUT_PACKET_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_SOURCE_IDS = [
    "src-argo-workflows-official-docs",
    "src-argo-workflows-original-repository",
    "src-kestra-official-docs",
    "src-prefect-official-docs",
    "src-airflow-official-docs",
    "src-dagster-official-docs",
    "src-dagster-original-repository",
    "src-haystack-official-docs",
    "src-haystack-original-repository",
    "src-langfuse-official-docs",
    "src-phoenix-official-docs",
    "src-promptfoo-official-docs",
    "src-ragas-official-docs",
    "src-ragas-paper-or-benchmark-record",
    "src-openhands-original-repository",
    "src-swe-agent-original-repository",
]

PACKET_MARKERS = [
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"supersedes_missing_input_goal_id: {SUPERSEDED_GOAL_ID}",
    f"packet_decision: {PACKET_DECISION}",
    f"packet_status: {PACKET_STATUS}",
    "records_source: codex_assistant_primary_source_web_research",
    "gpt_pro_output_supplied: false",
    "assistant_web_primary_source_research_performed: true",
    "codex_script_external_fetch_performed: false",
    "accepted_records: 0",
    "acceptance_status: unreviewed",
    "retrieval_method:",
    "source_reference_lines:",
    "protected_action_executed: false",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_codex_primary_source_output_packet_v0_1=true",
    f"packet_decision={PACKET_DECISION}",
    f"packet_status={PACKET_STATUS}",
    "records_source=codex_assistant_primary_source_web_research",
    "assistant_web_primary_source_research_performed=true",
    "gpt_pro_output_supplied=false",
    "codex_script_external_fetch_performed=false",
    "candidate_count=7",
    "source_record_count=16",
    "required_source_field_count=12",
    "filled_record_supplied_count=16",
    "accepted_records=0",
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
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-codex-primary-source-output-packet",
    "owner_approval_required_before_execution: false",
    "Review Codex-collected primary-source records before accepting them as evidence",
    "Keep all source records unaccepted until the review gate verifies every source field",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Codex Output Packet v0.1 validation")
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


def require_previous_review_gate() -> dict:
    gate = read_json(PREVIOUS_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != SUPERSEDED_GOAL_ID:
        fail("previous review gate next safe goal mismatch")
    if gate.get("gpt_pro_output_supplied") is not False:
        fail("previous review gate must not claim GPT Pro output supplied")
    require_false_flags(gate.get("claim_boundary", {}), "previous review gate claim boundary")
    return gate


def require_source_records(record: dict, label: str) -> None:
    records = record.get("source_records")
    if not isinstance(records, list) or len(records) != EXPECTED_COUNTS["source_record_count"]:
        fail(f"{label} source record count mismatch")
    seen = []
    for source in records:
        source_id = source.get("source_id")
        seen.append(source_id)
        if source.get("acceptance_status") != "unreviewed":
            fail(f"{label} {source_id} must remain unreviewed")
        if source.get("filled_record_supplied") is not True:
            fail(f"{label} {source_id} must be marked supplied")
        for field in REQUIRED_SOURCE_FIELDS:
            if not source.get(field):
                fail(f"{label} {source_id} missing {field}")
        if source.get("retrieval_method") != "codex_assistant_web_open_primary_source_current_turn":
            fail(f"{label} {source_id} retrieval method mismatch")
    if sorted(seen) != sorted(REQUIRED_SOURCE_IDS):
        fail(f"{label} source ids mismatch")


def require_packet_record(record: dict, label: str, previous_gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "supersedes_missing_input_goal_id": SUPERSEDED_GOAL_ID,
        "packet_decision": PACKET_DECISION,
        "packet_status": PACKET_STATUS,
        "records_source": "codex_assistant_primary_source_web_research",
        "assistant_web_primary_source_research_performed": True,
        "gpt_pro_output_supplied": False,
        "codex_script_external_fetch_performed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("source_required_candidate_ids") != previous_gate.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    require_source_records(record, label)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(previous_gate: dict) -> None:
    gate = read_json(OUTPUT_PACKET_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-codex-output-packet-gate-v0-1":
        fail("output packet gate id mismatch")
    if gate.get("status") != "PASS":
        fail("output packet gate status must be PASS")
    if gate.get("output_packet_uri") != OUTPUT_PACKET.relative_to(ROOT).as_posix():
        fail("output packet uri mismatch")
    require_packet_record(gate, "output packet gate", previous_gate)


def require_validation_result(previous_gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_codex_primary_source_output_packet_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_packet_record(result, "validation result", previous_gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    previous_gate = require_previous_review_gate()
    require_text_markers(OUTPUT_PACKET, PACKET_MARKERS)
    require_gate(previous_gate)
    require_text_markers(OUTPUT_PACKET_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(previous_gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Codex Output Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_codex_primary_source_output_packet_v0_1=true")
    print(f"packet_decision={PACKET_DECISION}")
    print(f"packet_status={PACKET_STATUS}")
    print("records_source=codex_assistant_primary_source_web_research")
    print("assistant_web_primary_source_research_performed=true")
    print("gpt_pro_output_supplied=false")
    print("codex_script_external_fetch_performed=false")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

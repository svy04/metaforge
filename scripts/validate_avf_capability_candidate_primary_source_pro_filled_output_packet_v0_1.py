from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_pro_filled_output_packet_v0_1.py"
OUTPUT_TEMPLATE_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_review_gate.json"
OUTPUT_TEMPLATE_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_pro_output_packet_template_review_next_action.yml"
OWNER_INPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_gate.json"
FILLED_OUTPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet.yml"
FILLED_OUTPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_gate.json"
FILLED_OUTPUT_PACKET_REPORT = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_FILLED_OUTPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_pro_output_packet_template_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_review_v0_1"
PACKET_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_FILLED_OUTPUT_PACKET_SHELL_CREATED_REPO_LOCAL"
PACKET_STATUS = "waiting_for_pasted_gpt_pro_yaml_not_filled"

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "source_target_count": 16,
    "required_source_field_count": 12,
    "filled_record_supplied_count": 0,
    "accepted_records": 0,
    "external_fetch_performed_count": 0,
    "source_contents_acquired_count": 0,
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
    OUTPUT_TEMPLATE_REVIEW_GATE,
    OUTPUT_TEMPLATE_REVIEW_NEXT_ACTION,
    OWNER_INPUT_PACKET_GATE,
    FILLED_OUTPUT_PACKET,
    FILLED_OUTPUT_PACKET_GATE,
    FILLED_OUTPUT_PACKET_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"packet_decision: {PACKET_DECISION}",
    f"packet_status: {PACKET_STATUS}",
    "records_source: pasted_gpt_pro_yaml_not_supplied",
    "gpt_pro_output_supplied: false",
    "source_collection_execution_allowed: false",
    "filled_record_supplied_count: 0",
    "accepted_records: 0",
    "cap-k8s-workflow-argo",
    "cap-general-orchestration-kestra-prefect-airflow",
    "cap-evidence-lineage-dagster",
    "cap-rag-document-pipeline-haystack",
    "cap-llm-observability-langfuse-phoenix",
    "cap-eval-redteam-promptfoo-ragas",
    "cap-coding-executor-openhands-sweagent",
    "src-argo-workflows-official-docs",
    "src-airflow-official-docs",
    "src-ragas-paper-or-benchmark-record",
    "source_id:",
    "source_title:",
    "source_kind:",
    "source_uri:",
    "source_version_or_date:",
    "source_owner_or_publisher:",
    "license_or_rights_note:",
    "claim_supported:",
    "evidence_excerpt_summary:",
    "verification_notes:",
    "source_reference_lines:",
    "retrieval_method:",
    "acceptance_status: unreviewed",
    "filled_record_supplied: false",
    "external_fetch_performed: false",
    "protected_action_executed: false",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-pro-filled-output-packet",
    "owner_approval_required_before_execution: false",
    "Review the Pro filled output packet shell before accepting pasted GPT Pro evidence",
    "Do not treat empty source fields as accepted primary-source evidence",
    "Do not fetch external sources inside Codex, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_pro_filled_output_packet_v0_1=true",
    f"packet_decision={PACKET_DECISION}",
    f"packet_status={PACKET_STATUS}",
    "records_source=pasted_gpt_pro_yaml_not_supplied",
    "gpt_pro_output_supplied=false",
    "candidate_count=7",
    "source_target_count=16",
    "required_source_field_count=12",
    "filled_record_supplied_count=0",
    "accepted_records=0",
    "external_fetch_performed_count=0",
    "source_contents_acquired_count=0",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "runtime_export_performed=false",
    "collector_started=false",
    "telemetry_export_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Pro Filled Output Packet v0.1 validation")
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


def require_previous_template_review_gate() -> dict:
    gate = read_json(OUTPUT_TEMPLATE_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("output template review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("output template review gate must point to this filled output packet goal")
    if gate.get("ready_for_filled_output_packet_count") != 1:
        fail("output template review gate must be ready for filled output packet shell")
    for key, value in EXPECTED_COUNTS.items():
        if key in gate and gate.get(key) != value:
            fail(f"output template review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "output template review gate claim boundary")
    require_text_markers(
        OUTPUT_TEMPLATE_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-pro-filled-output-packet",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return gate


def require_packet_record(record: dict, label: str, review_gate: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "packet_decision": PACKET_DECISION,
        "packet_status": PACKET_STATUS,
        "records_source": "pasted_gpt_pro_yaml_not_supplied",
        "gpt_pro_output_supplied": False,
        "source_collection_execution_allowed": False,
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
    if record.get("source_required_candidate_ids") != review_gate.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    sections = record.get("candidate_output_sections")
    if not isinstance(sections, list) or len(sections) != EXPECTED_COUNTS["candidate_count"]:
        fail(f"{label} candidate output section count mismatch")
    slot_count = sum(len(section.get("source_output_slots", [])) for section in sections)
    if slot_count != EXPECTED_COUNTS["source_target_count"]:
        fail(f"{label} source output slot count mismatch")
    for section in sections:
        if section.get("filled_record_supplied_count") != 0:
            fail(f"{label} section must not contain filled records")
        if section.get("accepted_records") != 0:
            fail(f"{label} section must not contain accepted records")
        for slot in section.get("source_output_slots", []):
            if slot.get("acceptance_status") != "unreviewed":
                fail(f"{label} slot acceptance status mismatch")
            if slot.get("filled_record_supplied") is not False:
                fail(f"{label} slot must not be filled yet")
            if slot.get("source_contents_acquired") is not False:
                fail(f"{label} slot must not contain acquired source contents")
            if slot.get("external_fetch_performed") is not False:
                fail(f"{label} slot must not fetch externally")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(review_gate: dict) -> None:
    gate = read_json(FILLED_OUTPUT_PACKET_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-pro-filled-output-packet-gate-v0-1":
        fail("filled output packet gate id mismatch")
    if gate.get("status") != "PASS":
        fail("filled output packet gate status must be PASS")
    if gate.get("filled_output_packet_uri") != FILLED_OUTPUT_PACKET.relative_to(ROOT).as_posix():
        fail("filled output packet gate uri mismatch")
    require_packet_record(gate, "filled output packet gate", review_gate)


def require_validation_result(review_gate: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_pro_filled_output_packet_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_packet_record(result, "validation result", review_gate)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    review_gate = require_previous_template_review_gate()
    require_text_markers(FILLED_OUTPUT_PACKET, PACKET_MARKERS)
    require_gate(review_gate)
    require_text_markers(FILLED_OUTPUT_PACKET_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(review_gate)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Pro Filled Output Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_pro_filled_output_packet_v0_1=true")
    print(f"packet_decision={PACKET_DECISION}")
    print(f"packet_status={PACKET_STATUS}")
    print("records_source=pasted_gpt_pro_yaml_not_supplied")
    print("gpt_pro_output_supplied=false")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("source_collection_execution_allowed=false")
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
    print("runtime_export_performed=false")
    print("collector_started=false")
    print("telemetry_export_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

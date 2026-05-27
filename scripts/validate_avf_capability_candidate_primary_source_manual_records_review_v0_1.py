from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_manual_records_review_v0_1.py"
MANUAL_RECORDS = CAPABILITIES / "capability_candidate_primary_source_manual_records.json"
MANUAL_RECORDS_GATE = CAPABILITIES / "capability_candidate_primary_source_manual_records_gate.json"
MANUAL_RECORDS_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_manual_records_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_MANUAL_RECORDS_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_v0_1"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_MANUAL_RECORD_SHELLS_REVIEWED_REPO_LOCAL"
REVIEW_STATUS = "manual_record_shells_review_passed_no_source_contents_acquired"

EXPECTED_COUNTS = {
    "manual_record_shell_count": 7,
    "planned_source_target_count": 16,
    "source_contents_acquired_count": 0,
    "external_fetch_performed_count": 0,
    "review_blocker_count": 0,
    "ready_for_owner_input_packet_count": 7,
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
    MANUAL_RECORDS,
    MANUAL_RECORDS_GATE,
    MANUAL_RECORDS_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_manual_records_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "manual_record_shell_count=7",
    "planned_source_target_count=16",
    "source_contents_acquired_count=0",
    "external_fetch_performed_count=0",
    "review_blocker_count=0",
    "ready_for_owner_input_packet_count=7",
    "cap-k8s-workflow-argo",
    "cap-general-orchestration-kestra-prefect-airflow",
    "cap-evidence-lineage-dagster",
    "cap-rag-document-pipeline-haystack",
    "cap-llm-observability-langfuse-phoenix",
    "cap-eval-redteam-promptfoo-ragas",
    "cap-coding-executor-openhands-sweagent",
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

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-owner-input-packet",
    "owner_approval_required_before_execution: false",
    "Create a repo-local owner input packet for filling primary-source evidence manually",
    "Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Manual Records Review v0.1 validation")
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


def require_previous_manual_records() -> dict:
    for label, record in [("manual records", read_json(MANUAL_RECORDS)), ("manual records gate", read_json(MANUAL_RECORDS_GATE))]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            fail(f"{label} goal_id mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            fail(f"{label} must point to this review goal")
        for key, value in EXPECTED_COUNTS.items():
            if key in record and key != "review_blocker_count" and key != "ready_for_owner_input_packet_count":
                if record.get(key) != value:
                    fail(f"{label} {key} mismatch")
        if record.get("source_contents_acquired_count") != 0:
            fail(f"{label} source contents must remain unacquired")
        if record.get("external_fetch_performed_count") != 0:
            fail(f"{label} external fetch count must be 0")
        if record.get("dependency_adoption_allowed") is not False:
            fail(f"{label} dependency adoption must remain blocked")
        if record.get("runtime_integration_allowed") is not False:
            fail(f"{label} runtime integration must remain blocked")
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        MANUAL_RECORDS_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-manual-records",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return read_json(MANUAL_RECORDS)


def require_review_record(record: dict, label: str, manual_records: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("source_required_candidate_ids") != manual_records.get("source_required_candidate_ids"):
        fail(f"{label} source-required candidate ids mismatch")
    findings = record.get("review_findings")
    if not isinstance(findings, list) or len(findings) != EXPECTED_COUNTS["manual_record_shell_count"]:
        fail(f"{label} review finding count mismatch")
    for finding in findings:
        if finding.get("review_result") != "PASS":
            fail(f"{label} finding review result must be PASS")
        if finding.get("source_contents_acquired") is not False:
            fail(f"{label} finding must not acquire source contents")
        if finding.get("external_fetch_performed") is not False:
            fail(f"{label} finding must not fetch externally")
        if finding.get("ready_for_owner_input_packet") is not True:
            fail(f"{label} finding must be ready for owner input packet")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(manual_records: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-manual-records-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", manual_records)


def require_validation_result(manual_records: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_manual_records_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", manual_records)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    manual_records = require_previous_manual_records()
    require_gate(manual_records)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(manual_records)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Manual Records Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_manual_records_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
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

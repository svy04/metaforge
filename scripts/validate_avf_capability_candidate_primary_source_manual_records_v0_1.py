from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_manual_records_v0_1.py"
EXPANSION_PLAN = CAPABILITIES / "capability_candidate_primary_source_expansion_plan.json"
EXPANSION_GATE = CAPABILITIES / "capability_candidate_primary_source_expansion_plan_gate.json"
EXPANSION_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_expansion_plan_next_action.yml"
MANUAL_RECORDS = CAPABILITIES / "capability_candidate_primary_source_manual_records.json"
MANUAL_RECORDS_MD = CAPABILITIES / "capability_candidate_primary_source_manual_records.md"
MANUAL_RECORDS_GATE = CAPABILITIES / "capability_candidate_primary_source_manual_records_gate.json"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_manual_records_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_manual_records_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_MANUAL_RECORDS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_expansion_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_review_v0_1"
RECORD_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_MANUAL_RECORD_SHELLS_CREATED_REPO_LOCAL"
RECORD_STATUS = "manual_record_shells_ready_no_source_contents_acquired"

SOURCE_REQUIRED_CANDIDATE_IDS = [
    "cap-k8s-workflow-argo",
    "cap-general-orchestration-kestra-prefect-airflow",
    "cap-evidence-lineage-dagster",
    "cap-rag-document-pipeline-haystack",
    "cap-llm-observability-langfuse-phoenix",
    "cap-eval-redteam-promptfoo-ragas",
    "cap-coding-executor-openhands-sweagent",
]

EXPECTED_COUNTS = {
    "manual_record_shell_count": 7,
    "planned_source_target_count": 16,
    "source_contents_acquired_count": 0,
    "external_fetch_performed_count": 0,
    "license_review_required_count": 7,
    "security_review_required_count": 7,
    "ready_for_owner_manual_research_count": 7,
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
    EXPANSION_PLAN,
    EXPANSION_GATE,
    EXPANSION_NEXT_ACTION,
    MANUAL_RECORDS,
    MANUAL_RECORDS_MD,
    MANUAL_RECORDS_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_manual_records_v0_1=true",
    f"record_decision={RECORD_DECISION}",
    f"record_status={RECORD_STATUS}",
    "manual_record_shell_count=7",
    "planned_source_target_count=16",
    "source_contents_acquired_count=0",
    "external_fetch_performed_count=0",
    "license_review_required_count=7",
    "security_review_required_count=7",
    "ready_for_owner_manual_research_count=7",
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
    "action_id: review-capability-candidate-primary-source-manual-records",
    "owner_approval_required_before_execution: false",
    "Review repo-local manual source record shells before any owner-filled source evidence is accepted",
    "Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Manual Records v0.1 validation")
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


def planned_target_count(shells: list[dict]) -> int:
    return sum(len(shell.get("planned_source_records", [])) for shell in shells)


def require_previous_plan() -> list[dict]:
    for label, record in [("expansion plan", read_json(EXPANSION_PLAN)), ("expansion gate", read_json(EXPANSION_GATE))]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            fail(f"{label} goal_id mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            fail(f"{label} must point to this manual records goal")
        if record.get("source_required_candidate_ids") != SOURCE_REQUIRED_CANDIDATE_IDS:
            fail(f"{label} source-required candidate ids mismatch")
        if record.get("planned_primary_source_record_count") != EXPECTED_COUNTS["manual_record_shell_count"]:
            fail(f"{label} planned source record count mismatch")
        if record.get("external_fetch_performed_count") != 0:
            fail(f"{label} external fetch count must be 0")
        if record.get("dependency_adoption_allowed") is not False:
            fail(f"{label} dependency adoption must remain blocked")
        if record.get("runtime_integration_allowed") is not False:
            fail(f"{label} runtime integration must remain blocked")
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        EXPANSION_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-manual-records",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return read_json(EXPANSION_PLAN)["source_expansion_plans"]


def require_records(record: dict, label: str, expansion_plans: list[dict]) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "record_decision": RECORD_DECISION,
        "record_status": RECORD_STATUS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("source_required_candidate_ids") != SOURCE_REQUIRED_CANDIDATE_IDS:
        fail(f"{label} source-required candidate ids mismatch")
    shells = record.get("manual_record_shells")
    if not isinstance(shells, list) or len(shells) != EXPECTED_COUNTS["manual_record_shell_count"]:
        fail(f"{label} manual record shell count mismatch")
    if planned_target_count(shells) != EXPECTED_COUNTS["planned_source_target_count"]:
        fail(f"{label} planned source target count mismatch")
    expansion_by_candidate = {plan["candidate_id"]: plan for plan in expansion_plans}
    for shell in shells:
        candidate_id = shell.get("candidate_id")
        if candidate_id not in expansion_by_candidate:
            fail(f"{label} shell has unexpected candidate id {candidate_id}")
        expected_plan = expansion_by_candidate[candidate_id]
        if shell.get("manual_record_shell_status") != "created_shell_not_filled":
            fail(f"{label} shell status must be created_shell_not_filled")
        if shell.get("source_target_ids") != expected_plan.get("planned_source_targets"):
            fail(f"{label} source target ids mismatch for {candidate_id}")
        if shell.get("source_priority_types") != expected_plan.get("source_priority_types"):
            fail(f"{label} source priority types mismatch for {candidate_id}")
        if shell.get("source_contents_acquired") is not False:
            fail(f"{label} shell must not acquire source contents")
        if shell.get("external_fetch_performed") is not False:
            fail(f"{label} shell must not fetch external sources")
        if shell.get("dependency_adoption_allowed") is not False:
            fail(f"{label} shell dependency adoption must remain blocked")
        if shell.get("runtime_integration_allowed") is not False:
            fail(f"{label} shell runtime integration must remain blocked")
        if shell.get("license_review_status") != "required_not_performed":
            fail(f"{label} shell license review status mismatch")
        if shell.get("security_review_status") != "required_not_performed":
            fail(f"{label} shell security review status mismatch")
        source_records = shell.get("planned_source_records")
        if not isinstance(source_records, list) or len(source_records) != len(expected_plan.get("planned_source_targets", [])):
            fail(f"{label} planned source records mismatch for {candidate_id}")
        for planned_source in source_records:
            if planned_source.get("source_contents_acquired") is not False:
                fail(f"{label} planned source record must not contain source contents")
            if planned_source.get("external_fetch_performed") is not False:
                fail(f"{label} planned source record must not fetch externally")
            if planned_source.get("manual_review_status") != "required_not_performed":
                fail(f"{label} planned source record manual review status mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(expansion_plans: list[dict]) -> None:
    gate = read_json(MANUAL_RECORDS_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-manual-records-gate-v0-1":
        fail("manual records gate id mismatch")
    if gate.get("status") != "PASS":
        fail("manual records gate status must be PASS")
    require_records(gate, "manual records gate", expansion_plans)


def require_validation_result(expansion_plans: list[dict]) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_manual_records_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_records(result, "validation result", expansion_plans)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    expansion_plans = require_previous_plan()
    require_records(read_json(MANUAL_RECORDS), "manual records", expansion_plans)
    require_text_markers(MANUAL_RECORDS_MD, REPORT_MARKERS)
    require_gate(expansion_plans)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(expansion_plans)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Manual Records v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_manual_records_v0_1=true")
    print(f"record_decision={RECORD_DECISION}")
    print(f"record_status={RECORD_STATUS}")
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

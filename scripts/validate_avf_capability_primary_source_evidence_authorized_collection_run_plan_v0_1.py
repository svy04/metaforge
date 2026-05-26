from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_primary_source_evidence_authorized_collection_run_plan_v0_1.py"
AUTH_PACKET = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_packet.yml"
AUTH_GATE = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_gate.json"
RUN_PLAN = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan.yml"
RUN_PLAN_GATE = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_AUTHORIZED_COLLECTION_RUN_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_run_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_collection_authorization_review_v0_1"
RUN_PLAN_DECISION = "PLAN_READY_EXECUTION_BLOCKED_PENDING_EXPLICIT_AUTHORIZATION"
AUTHORIZATION_DECISION = "BLOCKED_PENDING_EXPLICIT_COLLECTION_AUTHORIZATION"

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

AUTHORIZATION_FIELDS = [
    "owner_authorization_statement",
    "authorized_by",
    "authorized_at",
    "authorization_expires_at",
    "authorized_collection_modes",
    "authorized_source_families",
    "authorized_candidate_ids",
    "authorized_source_slot_ids",
    "max_records_to_collect",
    "collection_boundaries",
    "revocation_note",
]

REQUIRED_FILES = [
    RUNNER,
    AUTH_PACKET,
    AUTH_GATE,
    RUN_PLAN,
    RUN_PLAN_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

RUN_PLAN_MARKERS = [
    "plan_id: avf-capability-primary-source-evidence-authorized-collection-run-plan-v0-1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    f"run_plan_decision: {RUN_PLAN_DECISION}",
    "authorization_required: true",
    "authorization_present: false",
    "collection_execution_allowed: false",
    "source_records_planned: 35",
    "source_records_executable: 0",
    "trusted_sources_by_default: false",
    "ingested_sources_by_default: false",
    "integrated_sources_by_default: false",
    "authorization_review_required_before_execution: true",
    "execution_modes:",
    "execution_steps:",
    "source_collection_tasks:",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

NEXT_TASK_MARKERS = [
    "task_id: avf-capability-primary-source-evidence-collection-authorization-review-v0-1",
    "No collection execution before explicit authorization review passes",
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
    "capability_primary_source_evidence_authorized_collection_run_plan_v0_1=true",
    "authorized_collection_run_plan_created=true",
    "authorized_collection_run_plan_gate_created=true",
    "source_records_planned=35",
    "source_records_executable=0",
    "collection_execution_allowed=false",
    "authorization_present=false",
    "authorization_review_required_before_execution=true",
    "trusted_sources_by_default=false",
    "ingested_sources_by_default=false",
    "integrated_sources_by_default=false",
    "integration_decision=blocked",
    f"run_plan_decision={RUN_PLAN_DECISION}",
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
    print("AVF Capability Primary-Source Evidence Authorized Collection Run Plan v0.1 validation")
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


def require_authorized_collection_gate() -> None:
    gate = read_json(AUTH_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("authorized collection gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("authorized collection gate must point to this run plan goal")
    if gate.get("authorization_decision") != AUTHORIZATION_DECISION:
        fail("authorized collection gate authorization decision mismatch")
    if gate.get("collection_authorization_status") != "not_authorized":
        fail("authorized collection gate must remain not_authorized")
    if gate.get("owner_authorization_granted") is not False:
        fail("owner authorization must remain false")
    if gate.get("integration_decision") != "blocked":
        fail("authorized collection gate must keep integration blocked")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_targeted") != 35:
        fail("authorized collection gate source target count mismatch")
    if counts.get("source_records_authorized") != 0:
        fail("authorized collection gate must not authorize records")
    require_false_flags(gate.get("claim_boundary", {}), "authorized collection gate")


def require_run_plan_gate() -> None:
    gate = read_json(RUN_PLAN_GATE)
    expected = {
        "gate_id": "avf-capability-primary-source-evidence-authorized-collection-run-plan-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "run_plan_decision": RUN_PLAN_DECISION,
        "authorization_decision": AUTHORIZATION_DECISION,
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"run plan gate {key} mismatch")

    required_bools = {
        "authorization_required": True,
        "authorization_present": False,
        "authorization_review_required_before_execution": True,
        "collection_execution_allowed": False,
        "manual_owner_collection_executable": False,
        "pro_manual_collection_executable": False,
        "codex_assisted_link_opening_executable": False,
        "automated_collection_executable": False,
    }
    for key, value in required_bools.items():
        if gate.get(key) is not value:
            fail(f"run plan gate {key} mismatch")

    if gate.get("authorization_fields_required") != AUTHORIZATION_FIELDS:
        fail("run plan gate authorization fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "run plan gate")

    counts = gate.get("source_entry_counts", {})
    expected_counts = {
        "source_records_planned": 35,
        "source_records_executable": 0,
        "trusted_source_records": 0,
        "ingested_source_records": 0,
        "integrated_source_records": 0,
    }
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            fail(f"run plan count {key} mismatch")

    execution_modes = gate.get("execution_modes", [])
    if len(execution_modes) != 4:
        fail("run plan gate must list four execution modes")
    for mode in execution_modes:
        if mode.get("execution_allowed") is not False:
            fail(f"{mode.get('mode_id')} execution must be blocked")
        if mode.get("authorization_required") is not True:
            fail(f"{mode.get('mode_id')} must require authorization")

    execution_steps = gate.get("execution_steps", [])
    if len(execution_steps) < 5:
        fail("run plan gate must include execution steps")
    for step in execution_steps:
        if step.get("status") != "blocked_pending_explicit_authorization":
            fail(f"{step.get('step_id')} execution step status mismatch")

    source_tasks = gate.get("source_collection_tasks", [])
    if len(source_tasks) != 35:
        fail("run plan gate must include 35 source collection tasks")
    for task in source_tasks:
        if task.get("execution_status") != "blocked_pending_explicit_authorization":
            fail(f"{task.get('source_slot_id')} execution status mismatch")
        for key in [
            "collection_execution_allowed",
            "trusted_source",
            "accepted_for_ingestion",
            "accepted_for_integration",
            "integration_allowed_from_record",
        ]:
            if task.get(key) is not False:
                fail(f"{task.get('source_slot_id')} {key} must be false")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("validator_id") != "validate_avf_capability_primary_source_evidence_authorized_collection_run_plan_v0_1":
        fail("validation result validator_id mismatch")
    if validation.get("status") != "PASS":
        fail("validation result must be PASS")
    if validation.get("run_plan_decision") != RUN_PLAN_DECISION:
        fail("validation result run plan decision mismatch")
    if validation.get("source_records_executable") != 0:
        fail("validation result must not make source records executable")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_authorized_collection_gate()
    require_text_markers(RUN_PLAN, RUN_PLAN_MARKERS + AUTHORIZATION_FIELDS)
    require_run_plan_gate()
    require_text_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Primary-Source Evidence Authorized Collection Run Plan v0.1 validation")
    print("RESULT: PASS")
    print("capability_primary_source_evidence_authorized_collection_run_plan_v0_1=true")
    print("authorized_collection_run_plan_created=true")
    print("authorized_collection_run_plan_gate_created=true")
    print("source_records_planned=35")
    print("source_records_executable=0")
    print("collection_execution_allowed=false")
    print("authorization_present=false")
    print("authorization_review_required_before_execution=true")
    print("trusted_sources_by_default=false")
    print("ingested_sources_by_default=false")
    print("integrated_sources_by_default=false")
    print("integration_decision=blocked")
    print(f"run_plan_decision={RUN_PLAN_DECISION}")
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

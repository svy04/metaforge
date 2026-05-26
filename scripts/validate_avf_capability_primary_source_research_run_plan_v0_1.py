from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_primary_source_research_run_plan_v0_1.py"
AUTHORIZATION_GATE = CAPABILITIES / "capability_external_primary_source_research_authorization_gate.json"
RESEARCH_PACKET = CAPABILITIES / "capability_primary_source_research_packet.yml"
RUN_PLAN = CAPABILITIES / "capability_primary_source_research_run_plan.yml"
RUN_PLAN_GATE = CAPABILITIES / "capability_primary_source_research_run_plan_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_research_run_plan_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_research_run_plan_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_RESEARCH_RUN_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_research_run_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_external_primary_source_research_authorization_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_capture_workspace_v0_1"
RUN_PLAN_DECISION = "PLAN_READY_EXECUTION_BLOCKED_PENDING_OWNER_AUTHORIZATION"

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

PRIMARY_SOURCE_FAMILIES = [
    "official_docs",
    "official_repository",
    "license_file",
    "security_advisory",
    "maintenance_signal",
    "architecture_spec",
    "supply_chain_standard",
    "paper",
    "patent",
    "standard",
]

REQUIRED_FILES = [
    RUNNER,
    AUTHORIZATION_GATE,
    RESEARCH_PACKET,
    RUN_PLAN,
    RUN_PLAN_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

RUN_PLAN_MARKERS = [
    "packet_id: avf-capability-primary-source-research-run-plan-v0-1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    "source_collection_mode: planned_owner_or_pro_manual_only",
    "owner_authorization_required: true",
    "owner_authorization_granted: false",
    "research_execution_allowed: false",
    "external_primary_source_research_executed: false",
    "manual_evidence_capture_steps:",
    "record_source_uri",
    "record_source_type",
    "record_short_verbatim_excerpt",
    "compute_sha256_snapshot_hash",
    "record_license_note",
    "record_security_note",
    "record_maintenance_note",
    "record_architecture_fit_note",
    "record_supply_chain_note",
    "mark_untrusted_until_ingestion_gate",
    "candidate-opentelemetry",
    "candidate-litellm-proxy",
    "candidate-temporal-workflow",
    "candidate-langgraph-runtime",
    "candidate-mcp-tool-registry",
    "no_fetch_no_scrape_no_clone_no_install_no_integration",
    "release_ready: false",
    "production_ready: false",
]

NEXT_TASK_MARKERS = [
    "task_id: avf-capability-primary-source-evidence-capture-workspace-v0-1",
    "No external research execution",
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
    "capability_primary_source_research_run_plan_v0_1=true",
    "primary_source_research_run_plan_created=true",
    "primary_source_families_bounded=true",
    "manual_evidence_capture_steps_created=true",
    "target_source_slots_planned=35",
    "owner_authorization_required=true",
    "owner_authorization_granted=false",
    "research_execution_allowed=false",
    "external_primary_source_research_executed=false",
    f"run_plan_decision={RUN_PLAN_DECISION}",
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
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Primary-Source Research Run Plan v0.1 validation")
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


def require_authorization_gate() -> None:
    gate = read_json(AUTHORIZATION_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("authorization gate previous goal mismatch")
    if gate.get("status") != "PASS":
        fail("authorization gate must be PASS")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("authorization gate must point to this run plan goal")
    if gate.get("owner_authorization_required") is not True:
        fail("authorization gate must require owner authorization")
    if gate.get("owner_authorization_granted") is not False:
        fail("authorization gate owner authorization must remain false")
    if gate.get("external_research_allowed") is not False:
        fail("authorization gate external research allowance must remain false")
    if gate.get("automated_collection_allowed") is not False:
        fail("authorization gate automated collection allowance must remain false")
    if gate.get("allowed_future_source_families_after_authorization") != PRIMARY_SOURCE_FAMILIES:
        fail("authorization gate source families mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "authorization gate claim boundary")


def require_research_packet() -> None:
    text = read(RESEARCH_PACKET)
    if "source_collection_mode: manual_owner_or_pro" not in text:
        fail("research packet must remain manual owner or PRO collection")
    if "integration_allowed: false" not in text:
        fail("research packet integration must remain blocked")
    if "automated_scraping_allowed: false" not in text:
        fail("research packet automated scraping must remain blocked")
    if "oss_clone_allowed: false" not in text:
        fail("research packet OSS clone must remain blocked")
    if text.count("source_slot_id:") != 35:
        fail("research packet must still expose 35 source slots")


def require_run_plan_gate() -> None:
    gate = read_json(RUN_PLAN_GATE)
    expected = {
        "gate_id": "avf-capability-primary-source-research-run-plan-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "run_plan_decision": RUN_PLAN_DECISION,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"run plan gate {key} mismatch")

    expected_bools = {
        "primary_source_families_bounded": True,
        "manual_evidence_capture_steps_created": True,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "research_execution_allowed": False,
        "external_primary_source_research_executed": False,
    }
    for key, value in expected_bools.items():
        if gate.get(key) is not value:
            fail(f"run plan gate {key} mismatch")

    if gate.get("target_source_slots_planned") != 35:
        fail("run plan gate target slot count mismatch")
    if gate.get("source_families") != PRIMARY_SOURCE_FAMILIES:
        fail("run plan gate source families mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "run plan gate claim boundary")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("validator_id") != "validate_avf_capability_primary_source_research_run_plan_v0_1":
        fail("validation result validator_id mismatch")
    if validation.get("status") != "PASS":
        fail("validation result must be PASS")
    if validation.get("run_plan_decision") != RUN_PLAN_DECISION:
        fail("validation result run plan decision mismatch")
    if validation.get("research_execution_allowed") is not False:
        fail("validation result research execution allowance must remain false")
    if validation.get("external_primary_source_research_executed") is not False:
        fail("validation result external research execution must remain false")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "validation result claim boundary")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_authorization_gate()
    require_research_packet()
    require_text_markers(RUN_PLAN, RUN_PLAN_MARKERS + PRIMARY_SOURCE_FAMILIES)
    require_run_plan_gate()
    require_text_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Primary-Source Research Run Plan v0.1 validation")
    print("RESULT: PASS")
    print("capability_primary_source_research_run_plan_v0_1=true")
    print("primary_source_research_run_plan_created=true")
    print("primary_source_families_bounded=true")
    print("manual_evidence_capture_steps_created=true")
    print("target_source_slots_planned=35")
    print("owner_authorization_required=true")
    print("owner_authorization_granted=false")
    print("research_execution_allowed=false")
    print("external_primary_source_research_executed=false")
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

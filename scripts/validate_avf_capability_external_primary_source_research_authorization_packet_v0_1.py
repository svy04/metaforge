from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_external_primary_source_research_authorization_packet_v0_1.py"
PREVIOUS_REVIEW_GATE = CAPABILITIES / "capability_owner_completed_source_evidence_review_gate.json"
AUTHORIZATION_PACKET = CAPABILITIES / "capability_external_primary_source_research_authorization_packet.yml"
AUTHORIZATION_GATE = CAPABILITIES / "capability_external_primary_source_research_authorization_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_external_primary_source_research_authorization_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_external_primary_source_research_authorization_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_EXTERNAL_PRIMARY_SOURCE_RESEARCH_AUTHORIZATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_external_primary_source_research_authorization_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_owner_completed_source_evidence_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_research_run_plan_v0_1"
AUTHORIZATION_DECISION = "BLOCKED_PENDING_OWNER_AUTHORIZATION"

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
    PREVIOUS_REVIEW_GATE,
    AUTHORIZATION_PACKET,
    AUTHORIZATION_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

PACKET_MARKERS = [
    "packet_id: avf-capability-external-primary-source-research-authorization-packet-v0-1",
    f"goal_id: {THIS_GOAL_ID}",
    f"previous_goal_id: {PREVIOUS_GOAL_ID}",
    "owner_authorization_required: true",
    "owner_authorization_granted: false",
    "external_primary_source_research_allowed: false",
    "automated_scraping_allowed: false",
    "oss_clone_allowed: false",
    "dependency_install_allowed: false",
    "runtime_integration_allowed: false",
    "deploy_allowed: false",
    "publish_allowed: false",
    "release_ready: false",
    "production_ready: false",
    "owner_manual_browser_research",
    "pro_manual_primary_source_research",
    "codex_link_opening_only_after_explicit_authorization",
    "enabled: false",
]

NEXT_TASK_MARKERS = [
    "task_id: avf-capability-primary-source-research-run-plan-v0-1",
    "No external research execution without explicit owner authorization",
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
    "capability_external_primary_source_research_authorization_packet_v0_1=true",
    "owner_authorization_required=true",
    "owner_authorization_granted=false",
    "external_primary_source_research_allowed=false",
    "automated_collection_allowed=false",
    "integration_decision=blocked",
    f"authorization_decision={AUTHORIZATION_DECISION}",
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
    print("AVF Capability External Primary-Source Research Authorization Packet v0.1 validation")
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


def require_previous_gate() -> None:
    previous_gate = read_json(PREVIOUS_REVIEW_GATE)
    if previous_gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous review gate goal_id mismatch")
    if previous_gate.get("status") != "PASS":
        fail("previous review gate must be PASS")
    if previous_gate.get("review_decision") != "BLOCKED_OWNER_EVIDENCE_NOT_COMPLETED":
        fail("previous review gate decision mismatch")
    if previous_gate.get("integration_decision") != "blocked":
        fail("previous review gate must keep integration blocked")
    if previous_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous review gate must point to this authorization packet goal")
    counts = previous_gate.get("source_entry_counts", {})
    if counts.get("completed_source_records") != 0:
        fail("previous review gate completed source records must be zero")
    if counts.get("accepted_source_records") != 0:
        fail("previous review gate accepted source records must be zero")


def require_authorization_gate() -> None:
    gate = read_json(AUTHORIZATION_GATE)
    expected = {
        "gate_id": "avf-capability-external-primary-source-research-authorization-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "authorization_decision": AUTHORIZATION_DECISION,
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"authorization gate {key} mismatch")

    required_bools = {
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "external_research_allowed": False,
        "automated_collection_allowed": False,
    }
    for key, value in required_bools.items():
        if gate.get(key) is not value:
            fail(f"authorization gate {key} mismatch")

    if gate.get("allowed_future_source_families_after_authorization") != PRIMARY_SOURCE_FAMILIES:
        fail("authorization gate allowed future source families mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "authorization gate claim boundary")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("validator_id") != "validate_avf_capability_external_primary_source_research_authorization_packet_v0_1":
        fail("validation result validator_id mismatch")
    if validation.get("status") != "PASS":
        fail("validation result must be PASS")
    if validation.get("authorization_decision") != AUTHORIZATION_DECISION:
        fail("validation result authorization decision mismatch")
    if validation.get("owner_authorization_granted") is not False:
        fail("validation result owner authorization must remain false")
    if validation.get("external_primary_source_research_allowed") is not False:
        fail("validation result external research allowance must remain false")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "validation result claim boundary")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_gate()
    require_text_markers(AUTHORIZATION_PACKET, PACKET_MARKERS + PRIMARY_SOURCE_FAMILIES)
    require_authorization_gate()
    require_text_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability External Primary-Source Research Authorization Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_external_primary_source_research_authorization_packet_v0_1=true")
    print("owner_authorization_required=true")
    print("owner_authorization_granted=false")
    print("external_primary_source_research_allowed=false")
    print("automated_collection_allowed=false")
    print("integration_decision=blocked")
    print(f"authorization_decision={AUTHORIZATION_DECISION}")
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

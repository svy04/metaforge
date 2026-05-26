from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_primary_source_evidence_population_gate_v0_1.py"
WORKSPACE = CAPABILITIES / "capability_primary_source_evidence_capture_workspace.yml"
WORKSPACE_GATE = CAPABILITIES / "capability_primary_source_evidence_capture_workspace_gate.json"
POPULATION_GATE = CAPABILITIES / "capability_primary_source_evidence_population_gate.json"
POPULATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_population_validation_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_population_gate_next_codex_task_packet.yml"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_POPULATION_GATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_population_gate_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_capture_workspace_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_owner_primary_source_evidence_population_packet_v0_1"
POPULATION_DECISION = "BLOCKED_NO_POPULATED_SOURCE_EVIDENCE"

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

REQUIRED_EVIDENCE_FIELDS = [
    "source_uri",
    "source_type",
    "quoted_excerpt",
    "source_snapshot_hash",
    "license_note",
    "security_note",
    "maintenance_note",
    "architecture_fit_note",
    "supply_chain_note",
    "reviewer",
    "reviewed_at",
]

REQUIRED_FILES = [
    RUNNER,
    WORKSPACE,
    WORKSPACE_GATE,
    POPULATION_GATE,
    POPULATION_RESULT,
    NEXT_CODEX_TASK,
    VALIDATION_REPORT,
]

NEXT_TASK_MARKERS = [
    "task_id: avf-capability-owner-primary-source-evidence-population-packet-v0-1",
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
    "capability_primary_source_evidence_population_gate_v0_1=true",
    "population_gate_created=true",
    "workspace_records_reviewed=35",
    "empty_source_records=35",
    "partial_source_records=0",
    "complete_source_records=0",
    "accepted_source_records=0",
    "integration_decision=blocked",
    f"population_decision={POPULATION_DECISION}",
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
    print("AVF Capability Primary-Source Evidence Population Gate v0.1 validation")
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


def require_workspace_gate() -> None:
    gate = read_json(WORKSPACE_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("workspace gate previous goal mismatch")
    if gate.get("status") != "PASS":
        fail("workspace gate must be PASS")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("workspace gate must point to this population gate goal")
    if gate.get("target_source_slots_available") != 35:
        fail("workspace gate source slot count mismatch")
    if gate.get("captured_source_records") != 0:
        fail("workspace gate captured source records must be zero")
    if gate.get("trusted_source_records") != 0:
        fail("workspace gate trusted source records must be zero")
    if gate.get("accepted_source_records") != 0:
        fail("workspace gate accepted source records must be zero")
    if gate.get("required_evidence_fields") != REQUIRED_EVIDENCE_FIELDS:
        fail("workspace gate required evidence fields mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "workspace gate claim boundary")


def require_workspace_text() -> None:
    text = read(WORKSPACE)
    if text.count("source_slot_id:") != 35:
        fail("workspace must still contain 35 source slots")
    if text.count("record_status: empty_untrusted") != 35:
        fail("workspace records must remain empty and untrusted")
    if text.count("source_uri: \"\"") != 35:
        fail("workspace source URI fields must remain empty")
    if text.count("quoted_excerpt: \"\"") != 35:
        fail("workspace excerpt fields must remain empty")
    if text.count("accepted_for_ingestion: false") != 35:
        fail("workspace must block ingestion for all empty records")


def require_population_gate() -> None:
    gate = read_json(POPULATION_GATE)
    expected = {
        "gate_id": "avf-capability-primary-source-evidence-population-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "population_decision": POPULATION_DECISION,
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"population gate {key} mismatch")

    expected_counts = {
        "workspace_records_reviewed": 35,
        "empty_source_records": 35,
        "partial_source_records": 0,
        "complete_source_records": 0,
        "accepted_source_records": 0,
    }
    for key, value in expected_counts.items():
        if gate.get(key) != value:
            fail(f"population gate {key} mismatch")

    if gate.get("required_evidence_fields") != REQUIRED_EVIDENCE_FIELDS:
        fail("population gate required evidence fields mismatch")
    reviews = gate.get("record_reviews", [])
    if len(reviews) != 35:
        fail("population gate must include 35 record reviews")
    for review in reviews:
        if review.get("review_status") != "empty_record_blocked":
            fail(f"{review.get('source_slot_id')} review status mismatch")
        if review.get("missing_required_fields") != REQUIRED_EVIDENCE_FIELDS:
            fail(f"{review.get('source_slot_id')} missing fields mismatch")
        if review.get("accepted_for_ingestion") is not False:
            fail(f"{review.get('source_slot_id')} must remain blocked")
        if review.get("accepted_for_integration") is not False:
            fail(f"{review.get('source_slot_id')} must not allow integration")
    require_false_flags(gate.get("claim_boundary", {}), "population gate claim boundary")


def require_population_result() -> None:
    result = read_json(POPULATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_primary_source_evidence_population_gate_v0_1":
        fail("population result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("population result must be PASS")
    if result.get("population_decision") != POPULATION_DECISION:
        fail("population result decision mismatch")
    if result.get("accepted_source_records") != 0:
        fail("population result accepted source records must be zero")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("population result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "population result claim boundary")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_workspace_gate()
    require_workspace_text()
    require_population_gate()
    require_population_result()
    require_text_markers(NEXT_CODEX_TASK, NEXT_TASK_MARKERS)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Primary-Source Evidence Population Gate v0.1 validation")
    print("RESULT: PASS")
    print("capability_primary_source_evidence_population_gate_v0_1=true")
    print("population_gate_created=true")
    print("workspace_records_reviewed=35")
    print("empty_source_records=35")
    print("partial_source_records=0")
    print("complete_source_records=0")
    print("accepted_source_records=0")
    print("integration_decision=blocked")
    print(f"population_decision={POPULATION_DECISION}")
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

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_source_evidence_acceptance_gate_v0_1.py"
FIXTURE_MANIFEST = CAPABILITIES / "capability_source_evidence_fixture_template_manifest.json"
INGESTION_RULES = CAPABILITIES / "capability_source_evidence_ingestion_rules.json"
INGESTION_DRY_RUN = CAPABILITIES / "capability_source_evidence_ingestion_dry_run_result.json"
ACCEPTANCE_GATE = CAPABILITIES / "capability_source_evidence_acceptance_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_source_evidence_acceptance_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_source_evidence_acceptance_gate_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_SOURCE_EVIDENCE_ACCEPTANCE_GATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_source_evidence_acceptance_gate_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_source_evidence_ingestion_validator_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_research_packet_v0_1"
GATE_DECISION = "BLOCKED_NO_ACCEPTED_INGESTED_SOURCE_EVIDENCE"

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
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

REQUIRED_EVIDENCE_CATEGORIES = [
    "authenticity",
    "license",
    "security",
    "maintenance",
    "architecture_fit",
    "supply_chain_risk",
    "owner_approval",
]

REQUIRED_FILES = [
    RUNNER,
    FIXTURE_MANIFEST,
    INGESTION_RULES,
    INGESTION_DRY_RUN,
    ACCEPTANCE_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_GATE_FIELDS = {
    "gate_id",
    "created_at",
    "goal_id",
    "status",
    "input_uris",
    "source_entry_counts",
    "gate_decision",
    "integration_decision",
    "owner_approval_required",
    "required_evidence_categories_before_integration_proposal",
    "categories_passed",
    "candidate_acceptance_records",
    "future_integration_prerequisites",
    "next_safe_goal_id",
    "claim_boundary",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_source_evidence_acceptance_gate_v0_1=true",
    "acceptance_gate_created=true",
    "accepted_entries=0",
    "integration_decision=blocked",
    f"gate_decision={GATE_DECISION}",
    "owner_approval_required=true",
    "all_evidence_categories_required=true",
    "protected_action_executed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Source Evidence Acceptance Gate v0.1 validation")
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


def require_inputs() -> tuple[dict, dict, dict]:
    manifest = read_json(FIXTURE_MANIFEST)
    ingestion_rules = read_json(INGESTION_RULES)
    dry_run = read_json(INGESTION_DRY_RUN)
    if manifest.get("next_safe_goal_id") != PREVIOUS_GOAL_ID:
        fail("fixture manifest must point to ingestion validator before acceptance gate")
    if ingestion_rules.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("ingestion rules must point to this acceptance gate")
    if dry_run.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("ingestion dry run must point to this acceptance gate")
    if dry_run.get("accepted_entries") != 0:
        fail("ingestion dry run accepted entries must remain zero for this gate")
    if dry_run.get("integration_decision") != "blocked":
        fail("ingestion dry run integration decision must remain blocked")
    require_false_flags(ingestion_rules.get("claim_boundary", {}), "ingestion rules claim boundary")
    require_false_flags(dry_run.get("claim_boundary", {}), "ingestion dry run claim boundary")
    return manifest, ingestion_rules, dry_run


def require_acceptance_gate(manifest: dict, dry_run: dict) -> None:
    gate = read_json(ACCEPTANCE_GATE)
    missing = sorted(REQUIRED_GATE_FIELDS - set(gate))
    if missing:
        fail("acceptance gate missing fields:\n" + "\n".join(missing))
    if gate.get("status") != "PASS":
        fail("acceptance gate status must be PASS")
    if gate.get("goal_id") != THIS_GOAL_ID:
        fail("acceptance gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("acceptance gate next safe goal mismatch")
    if gate.get("gate_decision") != GATE_DECISION:
        fail("acceptance gate decision mismatch")
    if gate.get("integration_decision") != "blocked":
        fail("acceptance gate integration decision must remain blocked")
    if gate.get("owner_approval_required") is not True:
        fail("owner approval must be required")
    if gate.get("required_evidence_categories_before_integration_proposal") != REQUIRED_EVIDENCE_CATEGORIES:
        fail("required evidence categories mismatch")
    if gate.get("categories_passed") != []:
        fail("no evidence categories may pass when accepted entries are zero")
    require_false_flags(gate.get("claim_boundary", {}), "acceptance gate claim boundary")

    source_counts = gate.get("source_entry_counts", {})
    manifest_entries = manifest.get("candidate_template_records", [])
    candidate_ids = sorted({entry["candidate_id"] for entry in manifest_entries})
    if source_counts.get("template_entries_checked") != len(manifest_entries):
        fail("acceptance gate template entry count mismatch")
    if source_counts.get("candidate_count") != len(candidate_ids):
        fail("acceptance gate candidate count mismatch")
    if source_counts.get("accepted_entries") != dry_run.get("accepted_entries"):
        fail("acceptance gate accepted entry count mismatch")
    if source_counts.get("rejected_entries") != dry_run.get("rejected_entries"):
        fail("acceptance gate rejected entry count mismatch")
    if source_counts.get("accepted_entries") != 0:
        fail("acceptance gate accepted entries must be zero")

    records = gate.get("candidate_acceptance_records", [])
    if len(records) != len(candidate_ids):
        fail("candidate acceptance records must aggregate every candidate")
    for record in records:
        if record.get("candidate_id") not in candidate_ids:
            fail(f"unexpected candidate record {record.get('candidate_id')}")
        if record.get("accepted_source_entries") != 0:
            fail(f"{record.get('candidate_id')} accepted source entries must be zero")
        if record.get("acceptance_status") != "blocked_no_accepted_ingested_source_evidence":
            fail(f"{record.get('candidate_id')} acceptance status mismatch")
        if record.get("integration_proposal_allowed") is not False:
            fail(f"{record.get('candidate_id')} integration proposal must be blocked")
        if record.get("owner_approval_required") is not True:
            fail(f"{record.get('candidate_id')} owner approval must be required")
        if record.get("required_evidence_categories_missing") != REQUIRED_EVIDENCE_CATEGORIES:
            fail(f"{record.get('candidate_id')} missing categories mismatch")

    prerequisites = gate.get("future_integration_prerequisites", [])
    for category in REQUIRED_EVIDENCE_CATEGORIES:
        if not any(category in item for item in prerequisites):
            fail(f"future integration prerequisites missing {category}")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("acceptance validation result must be PASS")
    if validation.get("validator_id") != "validate_avf_capability_source_evidence_acceptance_gate_v0_1":
        fail("acceptance validation result validator_id mismatch")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("acceptance validation result next safe goal mismatch")
    if validation.get("gate_decision") != GATE_DECISION:
        fail("acceptance validation result gate decision mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "acceptance validation result")


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    manifest, _ingestion_rules, dry_run = require_inputs()
    require_acceptance_gate(manifest, dry_run)
    require_validation_result()
    require_markers(
        NEXT_CODEX_TASK,
        [
            "task_id: avf-capability-primary-source-research-packet-v0-1",
            "No provider calls",
            "No live model calls",
            "No external service calls",
            "No scraping automation",
            "No package install",
            "No dependency install",
            "No OSS clone",
            "No runtime integration",
            "next_safe_goal_id: avf_capability_primary_source_research_packet_v0_1",
        ],
    )
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Source Evidence Acceptance Gate v0.1 validation")
    print("RESULT: PASS")
    print("capability_source_evidence_acceptance_gate_v0_1=true")
    print("acceptance_gate_created=true")
    print("accepted_entries=0")
    print("integration_decision=blocked")
    print(f"gate_decision={GATE_DECISION}")
    print("owner_approval_required=true")
    print("all_evidence_categories_required=true")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

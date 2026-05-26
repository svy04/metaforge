from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_source_evidence_fixture_template_v0_1.py"
SOURCE_EVIDENCE_EVALUATION_PACKET = CAPABILITIES / "capability_source_evidence_evaluation_packet.json"
SOURCE_EVIDENCE_EVALUATION_GATE = CAPABILITIES / "capability_source_evidence_evaluation_preflight_gate.json"
SOURCE_EVIDENCE_FIXTURE_TEMPLATE = CAPABILITIES / "capability_source_evidence_fixture_template.yml"
SOURCE_EVIDENCE_FIXTURE_TEMPLATE_MANIFEST = CAPABILITIES / "capability_source_evidence_fixture_template_manifest.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_source_evidence_fixture_template_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_source_evidence_fixture_template_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_SOURCE_EVIDENCE_FIXTURE_TEMPLATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_source_evidence_fixture_template_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_source_evidence_ingestion_validator_v0_1"

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

REQUIRED_FILES = [
    RUNNER,
    SOURCE_EVIDENCE_EVALUATION_PACKET,
    SOURCE_EVIDENCE_EVALUATION_GATE,
    SOURCE_EVIDENCE_FIXTURE_TEMPLATE,
    SOURCE_EVIDENCE_FIXTURE_TEMPLATE_MANIFEST,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_TEMPLATE_MARKERS = [
    "template_id: avf-capability-source-evidence-fixture-template-v0-1",
    "goal_id: avf_capability_source_evidence_fixture_template_v0_1",
    "evidence_status: owner_to_fill",
    "evidence_trusted: false",
    "evidence_verified: false",
    "accepted_for_integration: false",
    "source_uri:",
    "source_type:",
    "quoted_excerpt:",
    "source_snapshot_hash:",
    "license_note:",
    "security_note:",
    "maintenance_note:",
    "architecture_fit_note:",
    "supply_chain_note:",
    "reviewer:",
    "reviewed_at:",
    "Evidence remains untrusted until evaluated by the source evidence ingestion validator.",
]

REQUIRED_MANIFEST_FIELDS = {
    "manifest_id",
    "goal_id",
    "status",
    "template_uri",
    "source_evidence_evaluation_packet_uri",
    "candidate_template_records",
    "template_contract",
    "next_safe_goal_id",
    "claim_boundary",
}

REQUIRED_ENTRY_FIELDS = {
    "candidate_id",
    "candidate_name",
    "capability_id",
    "source_slot_id",
    "slot_type",
    "target_uri",
    "template_fields",
    "trusted_by_default",
    "verified_by_default",
    "accepted_for_integration",
    "claim_boundary",
}

REQUIRED_TEMPLATE_FIELDS = {
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
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_source_evidence_fixture_template_v0_1=true",
    "source_evidence_fixture_template_created=true",
    "source_evidence_fixture_manifest_created=true",
    "template_fields_created=true",
    "evidence_remains_untrusted_until_evaluated=true",
    "integration_remains_blocked=true",
    "protected_action_executed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "provider_calls_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Source Evidence Fixture Template v0.1 validation")
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


def require_inputs() -> dict:
    packet = read_json(SOURCE_EVIDENCE_EVALUATION_PACKET)
    gate = read_json(SOURCE_EVIDENCE_EVALUATION_GATE)
    if packet.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("source evidence evaluation packet must point to fixture template as next safe goal")
    if gate.get("gate_decision") != "BLOCKED_NO_ACCEPTED_SOURCE_EVIDENCE":
        fail("source evidence evaluation gate must remain blocked before fixture template")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("source evidence evaluation gate must point to fixture template as next safe goal")
    return packet


def require_template_file() -> None:
    text = read(SOURCE_EVIDENCE_FIXTURE_TEMPLATE)
    missing = [marker for marker in REQUIRED_TEMPLATE_MARKERS if marker not in text]
    if missing:
        fail("fixture template missing markers:\n" + "\n".join(missing))


def require_manifest(evaluation_packet: dict) -> None:
    manifest = read_json(SOURCE_EVIDENCE_FIXTURE_TEMPLATE_MANIFEST)
    missing = sorted(REQUIRED_MANIFEST_FIELDS - set(manifest))
    if missing:
        fail("fixture manifest missing fields:\n" + "\n".join(missing))
    if manifest.get("status") != "PASS":
        fail("fixture manifest status must be PASS")
    if manifest.get("goal_id") != THIS_GOAL_ID:
        fail("fixture manifest goal_id mismatch")
    if manifest.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("fixture manifest next safe goal mismatch")
    if manifest.get("template_uri") != "avf/capabilities/generated/capability_source_evidence_fixture_template.yml":
        fail("fixture manifest template URI mismatch")
    require_false_flags(manifest.get("claim_boundary", {}), "fixture manifest claim boundary")

    expected_entries = sum(
        len(candidate.get("evidence_evaluation_records", []))
        for candidate in evaluation_packet.get("candidate_evaluation_records", [])
    )
    entries = manifest.get("candidate_template_records", [])
    if len(entries) != expected_entries:
        fail("fixture manifest entry count must match evaluation evidence records")
    for entry in entries:
        missing_entry_fields = sorted(REQUIRED_ENTRY_FIELDS - set(entry))
        if missing_entry_fields:
            fail(f"{entry.get('source_slot_id', '<unknown>')} missing entry fields:\n" + "\n".join(missing_entry_fields))
        if set(entry.get("template_fields", [])) != REQUIRED_TEMPLATE_FIELDS:
            fail(f"{entry.get('source_slot_id')} template fields mismatch")
        if entry.get("trusted_by_default") is not False:
            fail(f"{entry.get('source_slot_id')} trusted_by_default must be false")
        if entry.get("verified_by_default") is not False:
            fail(f"{entry.get('source_slot_id')} verified_by_default must be false")
        if entry.get("accepted_for_integration") is not False:
            fail(f"{entry.get('source_slot_id')} accepted_for_integration must be false")
        require_false_flags(entry.get("claim_boundary", {}), f"{entry.get('source_slot_id')} claim boundary")

    contract = manifest.get("template_contract", {})
    if contract.get("evidence_trusted_until_evaluated") is not False:
        fail("template contract must keep evidence untrusted until evaluated")
    if contract.get("automated_fetch_allowed") is not False:
        fail("automated fetch must remain false")
    if contract.get("automated_scraping_allowed") is not False:
        fail("automated scraping must remain false")
    if contract.get("integration_allowed_from_template") is not False:
        fail("template must not allow integration")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("fixture template validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("fixture template validation next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "fixture template validation result")


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    evaluation_packet = require_inputs()
    require_template_file()
    require_manifest(evaluation_packet)
    require_validation_result()
    require_markers(NEXT_CODEX_TASK, ["task_id: avf-capability-source-evidence-ingestion-validator-v0-1", "forbidden_changes:", "validation_commands:", f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}"])
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Source Evidence Fixture Template v0.1 validation")
    print("RESULT: PASS")
    print("capability_source_evidence_fixture_template_v0_1=true")
    print("source_evidence_fixture_template_created=true")
    print("source_evidence_fixture_manifest_created=true")
    print("template_fields_created=true")
    print("evidence_remains_untrusted_until_evaluated=true")
    print("integration_remains_blocked=true")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("provider_calls_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

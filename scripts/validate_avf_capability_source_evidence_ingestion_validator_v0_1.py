from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_source_evidence_ingestion_validator_v0_1.py"
FIXTURE_TEMPLATE = CAPABILITIES / "capability_source_evidence_fixture_template.yml"
FIXTURE_MANIFEST = CAPABILITIES / "capability_source_evidence_fixture_template_manifest.json"
INGESTION_RULES = CAPABILITIES / "capability_source_evidence_ingestion_rules.json"
INGESTION_DRY_RUN = CAPABILITIES / "capability_source_evidence_ingestion_dry_run_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_source_evidence_ingestion_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_source_evidence_ingestion_validator_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_SOURCE_EVIDENCE_INGESTION_VALIDATOR_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_source_evidence_ingestion_validator_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_source_evidence_acceptance_gate_v0_1"

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
    FIXTURE_TEMPLATE,
    FIXTURE_MANIFEST,
    INGESTION_RULES,
    INGESTION_DRY_RUN,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_FIELDS = {
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

REQUIRED_RULE_FIELDS = {
    "rule_id",
    "goal_id",
    "status",
    "fixture_template_uri",
    "fixture_manifest_uri",
    "required_fields",
    "field_rules",
    "default_decision",
    "rejection_decision",
    "candidate_ingestion_rules",
    "next_safe_goal_id",
    "claim_boundary",
}

REQUIRED_DRY_RUN_FIELDS = {
    "dry_run_id",
    "goal_id",
    "status",
    "template_entries_checked",
    "accepted_entries",
    "rejected_entries",
    "candidate_ingestion_results",
    "integration_decision",
    "next_safe_goal_id",
    "claim_boundary",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_source_evidence_ingestion_validator_v0_1=true",
    "source_evidence_ingestion_rules_created=true",
    "source_evidence_ingestion_dry_run_created=true",
    "missing_or_partial_evidence_rejected=true",
    "hashes_reviewer_excerpts_and_notes_required=true",
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
    print("AVF Capability Source Evidence Ingestion Validator v0.1 validation")
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
    manifest = read_json(FIXTURE_MANIFEST)
    if manifest.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("fixture manifest must point to ingestion validator as next safe goal")
    contract = manifest.get("template_contract", {})
    if contract.get("integration_allowed_from_template") is not False:
        fail("fixture template must not allow integration")
    if set(contract.get("required_fields_before_ingestion", [])) != REQUIRED_FIELDS:
        fail("fixture manifest required fields mismatch")
    if "Evidence remains untrusted until evaluated by the source evidence ingestion validator." not in read(FIXTURE_TEMPLATE):
        fail("fixture template must warn that evidence remains untrusted until evaluated")
    return manifest


def require_ingestion_rules(manifest: dict) -> None:
    rules = read_json(INGESTION_RULES)
    missing = sorted(REQUIRED_RULE_FIELDS - set(rules))
    if missing:
        fail("ingestion rules missing fields:\n" + "\n".join(missing))
    if rules.get("status") != "PASS":
        fail("ingestion rules status must be PASS")
    if rules.get("goal_id") != THIS_GOAL_ID:
        fail("ingestion rules goal_id mismatch")
    if rules.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("ingestion rules next safe goal mismatch")
    if set(rules.get("required_fields", [])) != REQUIRED_FIELDS:
        fail("ingestion rules required fields mismatch")
    if rules.get("default_decision") != "reject_until_all_required_fields_present":
        fail("ingestion rules default decision must reject")
    if rules.get("rejection_decision") != "blocked_missing_required_owner_supplied_evidence":
        fail("ingestion rules rejection decision mismatch")
    require_false_flags(rules.get("claim_boundary", {}), "ingestion rules claim boundary")

    field_rules = rules.get("field_rules", {})
    for field in REQUIRED_FIELDS:
        rule = field_rules.get(field)
        if not rule:
            fail(f"missing field rule for {field}")
        if rule.get("required_before_ingestion") is not True:
            fail(f"{field} must be required before ingestion")
        if rule.get("empty_value_decision") != "reject":
            fail(f"{field} empty value decision must reject")
    if field_rules["source_snapshot_hash"].get("hash_algorithm") != "sha256":
        fail("source snapshot hash must require sha256")
    if field_rules["quoted_excerpt"].get("must_be_verbatim_excerpt") is not True:
        fail("quoted excerpt must be marked as verbatim")

    manifest_entries = manifest.get("candidate_template_records", [])
    candidate_rules = rules.get("candidate_ingestion_rules", [])
    if len(candidate_rules) != len(manifest_entries):
        fail("candidate ingestion rules must match fixture manifest entries")
    for rule in candidate_rules:
        if rule.get("ingestion_decision") != "reject_until_required_fields_present":
            fail(f"{rule.get('source_slot_id')} ingestion decision must reject")
        if rule.get("evidence_trusted_after_ingestion") is not False:
            fail(f"{rule.get('source_slot_id')} evidence must remain untrusted after ingestion")
        if rule.get("evidence_verified_after_ingestion") is not False:
            fail(f"{rule.get('source_slot_id')} evidence must remain unverified after ingestion")
        if rule.get("accepted_for_integration") is not False:
            fail(f"{rule.get('source_slot_id')} must not be accepted for integration")
        if set(rule.get("required_fields", [])) != REQUIRED_FIELDS:
            fail(f"{rule.get('source_slot_id')} required fields mismatch")
        require_false_flags(rule.get("claim_boundary", {}), f"{rule.get('source_slot_id')} claim boundary")


def require_dry_run(manifest: dict) -> None:
    dry_run = read_json(INGESTION_DRY_RUN)
    missing = sorted(REQUIRED_DRY_RUN_FIELDS - set(dry_run))
    if missing:
        fail("ingestion dry run missing fields:\n" + "\n".join(missing))
    if dry_run.get("status") != "PASS":
        fail("ingestion dry run status must be PASS")
    if dry_run.get("goal_id") != THIS_GOAL_ID:
        fail("ingestion dry run goal_id mismatch")
    if dry_run.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("ingestion dry run next safe goal mismatch")
    entry_count = len(manifest.get("candidate_template_records", []))
    if dry_run.get("template_entries_checked") != entry_count:
        fail("ingestion dry run checked count mismatch")
    if dry_run.get("accepted_entries") != 0:
        fail("ingestion dry run accepted entries must be zero")
    if dry_run.get("rejected_entries") != entry_count:
        fail("ingestion dry run rejected entries must match template entry count")
    if dry_run.get("integration_decision") != "blocked":
        fail("ingestion dry run integration decision must remain blocked")
    require_false_flags(dry_run.get("claim_boundary", {}), "ingestion dry run claim boundary")
    for result in dry_run.get("candidate_ingestion_results", []):
        if result.get("ingestion_status") != "rejected_missing_required_fields":
            fail(f"{result.get('source_slot_id')} dry-run ingestion status must reject")
        if set(result.get("missing_required_fields", [])) != REQUIRED_FIELDS:
            fail(f"{result.get('source_slot_id')} missing required fields mismatch")
        if result.get("accepted_for_evaluation") is not False:
            fail(f"{result.get('source_slot_id')} accepted_for_evaluation must be false")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("ingestion validator validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("ingestion validator validation next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "ingestion validator validation result")


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    manifest = require_inputs()
    require_ingestion_rules(manifest)
    require_dry_run(manifest)
    require_validation_result()
    require_markers(NEXT_CODEX_TASK, ["task_id: avf-capability-source-evidence-acceptance-gate-v0-1", "forbidden_changes:", "validation_commands:", f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}"])
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Source Evidence Ingestion Validator v0.1 validation")
    print("RESULT: PASS")
    print("capability_source_evidence_ingestion_validator_v0_1=true")
    print("source_evidence_ingestion_rules_created=true")
    print("source_evidence_ingestion_dry_run_created=true")
    print("missing_or_partial_evidence_rejected=true")
    print("hashes_reviewer_excerpts_and_notes_required=true")
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

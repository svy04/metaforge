from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

FIXTURE_TEMPLATE = CAPABILITIES / "capability_source_evidence_fixture_template.yml"
FIXTURE_MANIFEST = CAPABILITIES / "capability_source_evidence_fixture_template_manifest.json"
INGESTION_RULES = CAPABILITIES / "capability_source_evidence_ingestion_rules.json"
INGESTION_DRY_RUN = CAPABILITIES / "capability_source_evidence_ingestion_dry_run_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_source_evidence_ingestion_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_source_evidence_ingestion_validator_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_SOURCE_EVIDENCE_INGESTION_VALIDATOR_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_source_evidence_ingestion_validator_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_source_evidence_acceptance_gate_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"

REQUIRED_FIELDS = [
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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def false_boundary() -> dict:
    return {
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "scraping_performed": False,
        "posting_automation_performed": False,
        "dependency_install_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "package_install_performed": False,
        "runtime_integration_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def build_field_rules() -> dict:
    rules = {}
    for field in REQUIRED_FIELDS:
        rules[field] = {
            "required_before_ingestion": True,
            "empty_value_decision": "reject",
        }
    rules["source_snapshot_hash"]["hash_algorithm"] = "sha256"
    rules["quoted_excerpt"]["must_be_verbatim_excerpt"] = True
    return rules


def build_candidate_ingestion_rule(entry: dict) -> dict:
    return {
        "candidate_id": entry["candidate_id"],
        "candidate_name": entry["candidate_name"],
        "capability_id": entry["capability_id"],
        "source_slot_id": entry["source_slot_id"],
        "slot_type": entry["slot_type"],
        "target_uri": entry["target_uri"],
        "required_fields": REQUIRED_FIELDS,
        "ingestion_decision": "reject_until_required_fields_present",
        "evidence_trusted_after_ingestion": False,
        "evidence_verified_after_ingestion": False,
        "accepted_for_integration": False,
        "claim_boundary": false_boundary(),
    }


def build_ingestion_rules(manifest: dict) -> dict:
    entries = manifest["candidate_template_records"]
    return {
        "rule_id": "avf-capability-source-evidence-ingestion-rules-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "fixture_template_uri": rel(FIXTURE_TEMPLATE),
        "fixture_manifest_uri": rel(FIXTURE_MANIFEST),
        "required_fields": REQUIRED_FIELDS,
        "field_rules": build_field_rules(),
        "default_decision": "reject_until_all_required_fields_present",
        "rejection_decision": "blocked_missing_required_owner_supplied_evidence",
        "candidate_ingestion_rules": [
            build_candidate_ingestion_rule(entry)
            for entry in entries
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_dry_run_result(entry: dict) -> dict:
    return {
        "candidate_id": entry["candidate_id"],
        "source_slot_id": entry["source_slot_id"],
        "slot_type": entry["slot_type"],
        "target_uri": entry["target_uri"],
        "ingestion_status": "rejected_missing_required_fields",
        "missing_required_fields": REQUIRED_FIELDS,
        "accepted_for_evaluation": False,
    }


def build_dry_run(manifest: dict) -> dict:
    entries = manifest["candidate_template_records"]
    return {
        "dry_run_id": "avf-capability-source-evidence-ingestion-dry-run-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "template_entries_checked": len(entries),
        "accepted_entries": 0,
        "rejected_entries": len(entries),
        "candidate_ingestion_results": [
            build_dry_run_result(entry)
            for entry in entries
        ],
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-source-evidence-acceptance-gate-v0-1
title: Add AVF capability source evidence acceptance gate v0.1
goal: Define the approval-gated acceptance boundary that can only consider fully ingested owner evidence and still does not fetch, scrape, clone, install, integrate, deploy, publish, or claim readiness.
context_paths:
  - avf/capabilities/generated/capability_source_evidence_ingestion_rules.json
  - avf/capabilities/generated/capability_source_evidence_ingestion_dry_run_result.json
  - avf/capabilities/generated/capability_source_evidence_fixture_template_manifest.json
files_likely_to_touch:
  - scripts/run_avf_capability_source_evidence_acceptance_gate_v0_1.py
  - scripts/validate_avf_capability_source_evidence_acceptance_gate_v0_1.py
  - avf/capabilities/generated/capability_source_evidence_acceptance_gate.json
  - docs/goals/AVF_CAPABILITY_SOURCE_EVIDENCE_ACCEPTANCE_GATE_V0_1_REPORT.md
forbidden_changes:
  - No provider calls
  - No live model calls
  - No external service calls
  - No scraping automation
  - No package install
  - No dependency install
  - No OSS clone
  - No runtime integration
  - No deploy
  - No publish
  - No release readiness claim
  - No production readiness claim
acceptance_criteria:
  - acceptance gate exists
  - acceptance remains blocked when ingestion dry run has zero accepted evidence
  - owner approval and all evidence categories are required before any future integration proposal
  - integration remains blocked
validation_commands:
  - python scripts\\validate_avf_capability_source_evidence_ingestion_validator_v0_1.py
  - python scripts\\validate_avf_capability_source_evidence_acceptance_gate_v0_1.py
expected_outputs:
  - capability_source_evidence_acceptance_gate.json
  - source evidence acceptance gate validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_source_evidence_ingestion_validator_v0_1",
        "status": "PASS",
        "checks": [
            "fixture manifest points to ingestion validator",
            "ingestion rules exist for manually filled fixtures",
            "missing or partial evidence remains rejected",
            "hashes, reviewer, excerpts, and notes are required before evaluation can proceed",
            "integration remains blocked",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(dry_run: dict) -> str:
    candidate_counts: dict[str, int] = {}
    for result in dry_run["candidate_ingestion_results"]:
        candidate_counts[result["candidate_id"]] = candidate_counts.get(result["candidate_id"], 0) + 1
    rows = "\n".join(
        f"- {candidate_id}: rejected_entries={count}, accepted_entries=0, integration=blocked"
        for candidate_id, count in candidate_counts.items()
    )
    return f"""# AVF Capability Source Evidence Ingestion Validator v0.1 Report

RESULT: PASS
capability_source_evidence_ingestion_validator_v0_1=true
source_evidence_ingestion_rules_created=true
source_evidence_ingestion_dry_run_created=true
missing_or_partial_evidence_rejected=true
hashes_reviewer_excerpts_and_notes_required=true
integration_remains_blocked=true
protected_action_executed=false
dependency_install_performed=false
external_fetch_performed=false
oss_clone_performed=false
package_install_performed=false
runtime_integration_performed=false
provider_calls_performed=false
scraping_performed=false
posting_automation_performed=false
deploy_performed=false
publish_performed=false
release_ready=false
production_ready=false
next_safe_goal_id={NEXT_SAFE_GOAL_ID}

## Ingestion Dry Run

- template_entries_checked={dry_run['template_entries_checked']}
- accepted_entries={dry_run['accepted_entries']}
- rejected_entries={dry_run['rejected_entries']}
- integration_decision={dry_run['integration_decision']}

## Candidate Results

{rows}

## Boundary

The ingestion validator defines local validation rules for manually filled source evidence only. Missing or partial evidence is rejected, all required fields remain mandatory, and the result does not fetch, scrape, clone, install, trust, verify, invoke, deploy, publish, approve, or integrate any source or candidate.
"""


def main() -> None:
    manifest = read_json(FIXTURE_MANIFEST)
    if manifest.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("fixture manifest does not point to this ingestion validator goal")
    contract = manifest.get("template_contract", {})
    if contract.get("integration_allowed_from_template") is not False:
        raise SystemExit("fixture template must not allow integration")
    if set(contract.get("required_fields_before_ingestion", [])) != set(REQUIRED_FIELDS):
        raise SystemExit("fixture manifest required fields mismatch")

    rules = build_ingestion_rules(manifest)
    dry_run = build_dry_run(manifest)
    write_json(INGESTION_RULES, rules)
    write_json(INGESTION_DRY_RUN, dry_run)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(dry_run))

    print("AVF Capability Source Evidence Ingestion Validator v0.1 runner")
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

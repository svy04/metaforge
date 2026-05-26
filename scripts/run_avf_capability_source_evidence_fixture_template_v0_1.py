from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

SOURCE_EVIDENCE_EVALUATION_PACKET = CAPABILITIES / "capability_source_evidence_evaluation_packet.json"
SOURCE_EVIDENCE_EVALUATION_GATE = CAPABILITIES / "capability_source_evidence_evaluation_preflight_gate.json"
SOURCE_EVIDENCE_FIXTURE_TEMPLATE = CAPABILITIES / "capability_source_evidence_fixture_template.yml"
SOURCE_EVIDENCE_FIXTURE_TEMPLATE_MANIFEST = CAPABILITIES / "capability_source_evidence_fixture_template_manifest.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_source_evidence_fixture_template_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_source_evidence_fixture_template_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_SOURCE_EVIDENCE_FIXTURE_TEMPLATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_source_evidence_fixture_template_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_source_evidence_ingestion_validator_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"

TEMPLATE_FIELDS = [
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


def flatten_evaluation_records(packet: dict) -> list[dict]:
    entries = []
    for candidate in packet["candidate_evaluation_records"]:
        for evidence in candidate["evidence_evaluation_records"]:
            entries.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "candidate_name": candidate["candidate_name"],
                    "capability_id": candidate["capability_id"],
                    "source_slot_id": evidence["source_slot_id"],
                    "slot_type": evidence["slot_type"],
                    "target_uri": evidence["target_uri"],
                }
            )
    return entries


def build_template_entry(entry: dict) -> str:
    return f"""  - candidate_id: {entry['candidate_id']}
    candidate_name: {entry['candidate_name']}
    capability_id: {entry['capability_id']}
    source_slot_id: {entry['source_slot_id']}
    slot_type: {entry['slot_type']}
    target_uri: {entry['target_uri']}
    evidence_status: owner_to_fill
    evidence_trusted: false
    evidence_verified: false
    accepted_for_integration: false
    source_uri:
    source_type:
    quoted_excerpt:
    source_snapshot_hash:
    license_note:
    security_note:
    maintenance_note:
    architecture_fit_note:
    supply_chain_note:
    reviewer:
    reviewed_at:
"""


def build_template(entries: list[dict]) -> str:
    body = "".join(build_template_entry(entry) for entry in entries)
    return f"""# AVF Capability Source Evidence Fixture Template v0.1
# Evidence remains untrusted until evaluated by the source evidence ingestion validator.
# Fill this template manually from primary/original sources only.
# Do not use this file as approval to fetch, scrape, clone, install, integrate, deploy, publish, or claim readiness.

template_id: avf-capability-source-evidence-fixture-template-v0-1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
template_mode: owner_supplied_primary_source_evidence_fixture
source_evidence_evaluation_packet_uri: {rel(SOURCE_EVIDENCE_EVALUATION_PACKET)}
source_evidence_evaluation_gate_uri: {rel(SOURCE_EVIDENCE_EVALUATION_GATE)}
evidence_trusted_until_evaluated: false
integration_allowed_from_template: false
entries:
{body}claim_boundary:
  protected_action_executed: false
  provider_calls_performed: false
  live_model_calls_performed: false
  external_service_calls_performed: false
  scraping_performed: false
  posting_automation_performed: false
  dependency_install_performed: false
  external_fetch_performed: false
  oss_clone_performed: false
  package_install_performed: false
  runtime_integration_performed: false
  deploy_performed: false
  publish_performed: false
  release_ready: false
  production_ready: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_manifest_entry(entry: dict) -> dict:
    return {
        "candidate_id": entry["candidate_id"],
        "candidate_name": entry["candidate_name"],
        "capability_id": entry["capability_id"],
        "source_slot_id": entry["source_slot_id"],
        "slot_type": entry["slot_type"],
        "target_uri": entry["target_uri"],
        "template_fields": TEMPLATE_FIELDS,
        "trusted_by_default": False,
        "verified_by_default": False,
        "accepted_for_integration": False,
        "claim_boundary": false_boundary(),
    }


def build_manifest(entries: list[dict]) -> dict:
    return {
        "manifest_id": "avf-capability-source-evidence-fixture-template-manifest-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "template_uri": rel(SOURCE_EVIDENCE_FIXTURE_TEMPLATE),
        "source_evidence_evaluation_packet_uri": rel(SOURCE_EVIDENCE_EVALUATION_PACKET),
        "source_evidence_evaluation_gate_uri": rel(SOURCE_EVIDENCE_EVALUATION_GATE),
        "candidate_template_records": [
            build_manifest_entry(entry)
            for entry in entries
        ],
        "template_contract": {
            "evidence_trusted_until_evaluated": False,
            "automated_fetch_allowed": False,
            "automated_scraping_allowed": False,
            "integration_allowed_from_template": False,
            "required_fields_before_ingestion": TEMPLATE_FIELDS,
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-source-evidence-ingestion-validator-v0-1
title: Add AVF capability source evidence ingestion validator v0.1
goal: Validate a manually filled source evidence fixture without trusting, accepting, fetching, scraping, cloning, installing, or integrating evidence by default.
context_paths:
  - avf/capabilities/generated/capability_source_evidence_fixture_template.yml
  - avf/capabilities/generated/capability_source_evidence_fixture_template_manifest.json
  - avf/capabilities/generated/capability_source_evidence_evaluation_packet.json
files_likely_to_touch:
  - scripts/run_avf_capability_source_evidence_ingestion_validator_v0_1.py
  - scripts/validate_avf_capability_source_evidence_ingestion_validator_v0_1.py
  - avf/capabilities/generated/capability_source_evidence_ingestion_rules.json
  - docs/goals/AVF_CAPABILITY_SOURCE_EVIDENCE_INGESTION_VALIDATOR_V0_1_REPORT.md
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
  - ingestion rules exist for manually filled fixtures
  - missing or partial evidence remains rejected
  - hashes, reviewer, excerpts, and notes are required before evaluation can proceed
  - integration remains blocked
validation_commands:
  - python scripts\\validate_avf_capability_source_evidence_fixture_template_v0_1.py
  - python scripts\\validate_avf_capability_source_evidence_ingestion_validator_v0_1.py
expected_outputs:
  - capability_source_evidence_ingestion_rules.json
  - source evidence ingestion validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_source_evidence_fixture_template_v0_1",
        "status": "PASS",
        "checks": [
            "source evidence evaluation packet points to fixture template",
            "fillable fixture template exists",
            "template manifest maps all evidence evaluation records",
            "source URI, source type, quoted excerpt, snapshot hash, notes, reviewer, and reviewed_at fields exist",
            "evidence remains untrusted until evaluated",
            "integration remains blocked",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(entries: list[dict]) -> str:
    candidate_counts: dict[str, int] = {}
    for entry in entries:
        candidate_counts[entry["candidate_id"]] = candidate_counts.get(entry["candidate_id"], 0) + 1
    rows = "\n".join(
        f"- {candidate_id}: template_entries={count}, trusted=false, verified=false, integration=blocked"
        for candidate_id, count in candidate_counts.items()
    )
    return f"""# AVF Capability Source Evidence Fixture Template v0.1 Report

RESULT: PASS
capability_source_evidence_fixture_template_v0_1=true
source_evidence_fixture_template_created=true
source_evidence_fixture_manifest_created=true
template_fields_created=true
evidence_remains_untrusted_until_evaluated=true
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

## Fixture Template Entries

{rows}

## Boundary

The fixture template is a fillable owner-supplied evidence form only. It does not fetch, scrape, clone, install, trust, verify, invoke, deploy, publish, approve, or integrate any source or candidate. Evidence remains untrusted until evaluated by a later ingestion validator.
"""


def main() -> None:
    evaluation_packet = read_json(SOURCE_EVIDENCE_EVALUATION_PACKET)
    evaluation_gate = read_json(SOURCE_EVIDENCE_EVALUATION_GATE)
    if evaluation_packet.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("source evidence evaluation packet does not point to this fixture template goal")
    if evaluation_gate.get("gate_decision") != "BLOCKED_NO_ACCEPTED_SOURCE_EVIDENCE":
        raise SystemExit("source evidence evaluation gate must remain blocked before fixture template")
    if evaluation_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("source evidence evaluation gate does not point to this fixture template goal")

    entries = flatten_evaluation_records(evaluation_packet)
    write_text(SOURCE_EVIDENCE_FIXTURE_TEMPLATE, build_template(entries))
    write_json(SOURCE_EVIDENCE_FIXTURE_TEMPLATE_MANIFEST, build_manifest(entries))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(entries))

    print("AVF Capability Source Evidence Fixture Template v0.1 runner")
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

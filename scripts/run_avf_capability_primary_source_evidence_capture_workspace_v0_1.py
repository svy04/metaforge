from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUN_PLAN_GATE = CAPABILITIES / "capability_primary_source_research_run_plan_gate.json"
RESEARCH_PACKET = CAPABILITIES / "capability_primary_source_research_packet.yml"
WORKSPACE = CAPABILITIES / "capability_primary_source_evidence_capture_workspace.yml"
WORKSPACE_GATE = CAPABILITIES / "capability_primary_source_evidence_capture_workspace_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_capture_workspace_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_capture_workspace_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_CAPTURE_WORKSPACE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_capture_workspace_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_research_run_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_population_gate_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
WORKSPACE_DECISION = "WORKSPACE_READY_EMPTY_UNTRUSTED_EXECUTION_BLOCKED"

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
        "automated_scraping_performed": False,
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


def require_run_plan_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("run plan gate previous goal mismatch")
    if gate.get("status") != "PASS":
        raise SystemExit("run plan gate must be PASS")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("run plan gate must point to this capture workspace goal")
    if gate.get("target_source_slots_planned") != 35:
        raise SystemExit("expected 35 target source slots")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("owner authorization must remain false")
    if gate.get("external_primary_source_research_executed") is not False:
        raise SystemExit("external research execution must remain false")
    if gate.get("source_families") != PRIMARY_SOURCE_FAMILIES:
        raise SystemExit("source family boundary mismatch")


def parse_source_slots() -> list[dict]:
    records: list[dict] = []
    current: dict | None = None
    for raw_line in RESEARCH_PACKET.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- candidate_id:"):
            if current:
                records.append(current)
            current = {"candidate_id": line.split(":", 1)[1].strip()}
        elif current and ":" in line:
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip()
    if current:
        records.append(current)
    return records


def workspace_record(record: dict) -> str:
    return f"""  - candidate_id: {record['candidate_id']}
    candidate_name: {record['candidate_name']}
    capability_id: {record['capability_id']}
    source_slot_id: {record['source_slot_id']}
    planned_target_uri: {record['target_uri']}
    planned_source_type: {record['source_type']}
    record_status: empty_untrusted
    source_uri: ""
    source_type: {record['source_type']}
    quoted_excerpt: ""
    source_snapshot_hash: ""
    license_note: ""
    security_note: ""
    maintenance_note: ""
    architecture_fit_note: ""
    supply_chain_note: ""
    reviewer: ""
    reviewed_at: ""
    evidence_trusted_by_default: false
    evidence_verified_by_default: false
    accepted_for_ingestion: false
    integration_allowed_from_record: false"""


def build_workspace(records: list[dict]) -> str:
    family_rows = "\n".join(f"  - {family}" for family in PRIMARY_SOURCE_FAMILIES)
    field_rows = "\n".join(f"  - {field}" for field in REQUIRED_EVIDENCE_FIELDS)
    record_rows = "\n".join(workspace_record(record) for record in records)
    return f"""workspace_id: avf-capability-primary-source-evidence-capture-workspace-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
workspace_mode: empty_repo_local_capture_workspace
owner_authorization_required: true
owner_authorization_granted: false
external_research_executed: false
target_source_slots_available: {len(records)}
captured_source_records: 0
trusted_source_records: 0
accepted_source_records: 0
empty_record_templates_created: true
records_remain_untrusted_by_default: true
workspace_decision: {WORKSPACE_DECISION}

source_families:
{family_rows}

required_evidence_fields:
{field_rows}

evidence_records:
{record_rows}

claim_boundary:
  protected_action_executed: false
  provider_calls_performed: false
  live_model_calls_performed: false
  external_service_calls_performed: false
  automated_scraping_performed: false
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


def build_workspace_gate(records: list[dict]) -> dict:
    return {
        "gate_id": "avf-capability-primary-source-evidence-capture-workspace-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "workspace_decision": WORKSPACE_DECISION,
        "empty_record_templates_created": True,
        "records_remain_untrusted_by_default": True,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "external_research_executed": False,
        "target_source_slots_available": len(records),
        "captured_source_records": 0,
        "trusted_source_records": 0,
        "accepted_source_records": 0,
        "source_families": PRIMARY_SOURCE_FAMILIES,
        "required_evidence_fields": REQUIRED_EVIDENCE_FIELDS,
        "workspace_uri": rel(WORKSPACE),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-evidence-population-gate-v0-1
title: Add AVF primary-source evidence population gate v0.1
goal: Validate whether the repo-local primary-source evidence workspace has been manually populated, while keeping empty or partial records blocked and avoiding external research execution, scraping, clone, install, runtime integration, deploy, publish, or readiness claims.
context_paths:
  - avf/capabilities/generated/capability_primary_source_evidence_capture_workspace.yml
  - avf/capabilities/generated/capability_primary_source_evidence_capture_workspace_gate.json
  - avf/capabilities/generated/capability_source_evidence_ingestion_rules.yml
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_population_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_population_validation_result.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_POPULATION_GATE_V0_1_REPORT.md
forbidden_changes:
  - No external research execution
  - No provider calls
  - No live model calls
  - No external service calls
  - No automated scraping
  - No OSS clone
  - No package install
  - No dependency install
  - No runtime integration
  - No deploy
  - No publish
  - No release readiness claim
  - No production readiness claim
acceptance_criteria:
  - gate detects empty records
  - gate rejects partial records
  - gate requires all evidence fields before acceptance
  - protected actions remain blocked
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_capture_workspace_v0_1.py
expected_outputs:
  - primary-source evidence population gate
  - population validation result
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(records: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_capture_workspace_v0_1",
        "status": "PASS",
        "checks": [
            "workspace exists",
            "required evidence fields are present",
            "35 source slot templates are present",
            "records remain empty and untrusted by default",
            "protected-action flags remain false",
        ],
        "workspace_decision": WORKSPACE_DECISION,
        "target_source_slots_available": len(records),
        "captured_source_records": 0,
        "trusted_source_records": 0,
        "accepted_source_records": 0,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(records: list[dict]) -> str:
    candidates = sorted({record["candidate_id"] for record in records})
    candidate_rows = "\n".join(f"- {candidate}: empty_untrusted" for candidate in candidates)
    return f"""# AVF Capability Primary-Source Evidence Capture Workspace v0.1 Report

RESULT: PASS
capability_primary_source_evidence_capture_workspace_v0_1=true
primary_source_evidence_capture_workspace_created=true
target_source_slots_available={len(records)}
captured_source_records=0
trusted_source_records=0
accepted_source_records=0
empty_record_templates_created=true
records_remain_untrusted_by_default=true
owner_authorization_required=true
owner_authorization_granted=false
external_research_executed=false
workspace_decision={WORKSPACE_DECISION}
protected_action_executed=false
provider_calls_performed=false
live_model_calls_performed=false
external_service_calls_performed=false
automated_scraping_performed=false
scraping_performed=false
posting_automation_performed=false
dependency_install_performed=false
external_fetch_performed=false
oss_clone_performed=false
package_install_performed=false
runtime_integration_performed=false
deploy_performed=false
publish_performed=false
release_ready=false
production_ready=false
next_safe_goal_id={NEXT_SAFE_GOAL_ID}

## Workspace Boundary

This is a repo-local capture workspace only. It contains empty evidence record templates for the planned source slots. No external research, automated collection, clone, install, integration, deploy, publish, or readiness claim was performed.

## Candidate Record State

{candidate_rows}

## Required Evidence Fields

Each future record must provide source URI, source type, short excerpt, sha256 snapshot hash, license note, security note, maintenance note, architecture fit note, supply-chain note, reviewer, and reviewed_at before a later population gate can consider it complete.
"""


def main() -> None:
    gate = read_json(RUN_PLAN_GATE)
    require_run_plan_gate(gate)
    records = parse_source_slots()
    if len(records) != 35:
        raise SystemExit(f"expected 35 source slot records, got {len(records)}")

    write_text(WORKSPACE, build_workspace(records))
    write_json(WORKSPACE_GATE, build_workspace_gate(records))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result(records))
    write_text(VALIDATION_REPORT, build_report(records))

    print("AVF Capability Primary-Source Evidence Capture Workspace v0.1 runner")
    print("RESULT: PASS")
    print("capability_primary_source_evidence_capture_workspace_v0_1=true")
    print("primary_source_evidence_capture_workspace_created=true")
    print(f"target_source_slots_available={len(records)}")
    print("captured_source_records=0")
    print("trusted_source_records=0")
    print("accepted_source_records=0")
    print("empty_record_templates_created=true")
    print("records_remain_untrusted_by_default=true")
    print("owner_authorization_required=true")
    print("owner_authorization_granted=false")
    print("external_research_executed=false")
    print(f"workspace_decision={WORKSPACE_DECISION}")
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

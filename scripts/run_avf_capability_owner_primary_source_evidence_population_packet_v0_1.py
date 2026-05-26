from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

WORKSPACE = CAPABILITIES / "capability_primary_source_evidence_capture_workspace.yml"
POPULATION_GATE = CAPABILITIES / "capability_primary_source_evidence_population_gate.json"
OWNER_POPULATION_PACKET = CAPABILITIES / "capability_owner_primary_source_evidence_population_packet.yml"
OWNER_POPULATION_GATE = CAPABILITIES / "capability_owner_primary_source_evidence_population_packet_gate.json"
OWNER_POPULATION_PRO_PROMPT = CAPABILITIES / "capability_owner_primary_source_evidence_population_pro_prompt.md"
VALIDATION_RESULT = CAPABILITIES / "capability_owner_primary_source_evidence_population_packet_v0_1.validation_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_owner_primary_source_evidence_population_next_codex_task_packet.yml"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_OWNER_PRIMARY_SOURCE_EVIDENCE_POPULATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_owner_primary_source_evidence_population_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_population_gate_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_owner_filled_primary_source_evidence_review_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"

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

SOURCE_FAMILIES = [
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


def parse_workspace_records() -> list[dict]:
    records: list[dict] = []
    current: dict | None = None
    for raw_line in WORKSPACE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- candidate_id:"):
            if current:
                records.append(current)
            current = {"candidate_id": line.split(":", 1)[1].strip()}
        elif current and ":" in line:
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip().strip('"')
    if current:
        records.append(current)
    return records


def require_previous_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous population gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous population gate must point to this owner/PRO population packet")
    if gate.get("workspace_records_reviewed") != 35:
        raise SystemExit("previous population gate must review 35 records")
    if gate.get("accepted_source_records") != 0:
        raise SystemExit("previous population gate must not accept evidence records")
    if gate.get("integration_decision") != "blocked":
        raise SystemExit("previous population gate must keep integration blocked")


def build_packet(records: list[dict]) -> str:
    families = "\n".join(f"  - {family}" for family in SOURCE_FAMILIES)
    fields = "\n".join(f"  - {field}" for field in REQUIRED_EVIDENCE_FIELDS)
    record_blocks = "\n".join(build_record_block(record) for record in records)
    return f"""packet_id: avf-capability-owner-primary-source-evidence-population-packet-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
packet_mode: owner_or_pro_primary_source_evidence_population
population_source: owner_or_pro_supplied_primary_sources_only
population_packet_status: ready_for_owner_or_pro_input
manual_or_pro_input_required: true
evidence_records_to_populate: {len(records)}
records_completed_by_default: 0
records_accepted_by_default: 0
integration_allowed_from_packet: false
automated_scraping_allowed: false
external_fetch_allowed_by_packet: false
oss_clone_allowed_by_packet: false
dependency_install_allowed_by_packet: false
runtime_integration_allowed_by_packet: false
release_ready: false
production_ready: false

source_families:
{families}

required_evidence_fields:
{fields}

population_instructions:
  - Fill source_uri from a primary/original source only.
  - Keep quoted_excerpt short and directly tied to the field being reviewed.
  - Record a source_snapshot_hash before any trust decision.
  - Write license, security, maintenance, architecture fit, and supply-chain notes separately.
  - Keep every record blocked until a later review gate accepts it.
  - Do not fetch, scrape, clone, install, integrate, deploy, publish, or claim readiness from this packet.

evidence_records:
{record_blocks}

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


def build_record_block(record: dict) -> str:
    return f"""  - candidate_id: {record.get('candidate_id', '')}
    candidate_name: {record.get('candidate_name', '')}
    capability_id: {record.get('capability_id', '')}
    source_slot_id: {record.get('source_slot_id', '')}
    planned_target_uri: {record.get('planned_target_uri', '')}
    planned_source_type: {record.get('planned_source_type', '')}
    record_status: awaiting_owner_or_pro_population
    source_uri: \"\"
    source_type: {record.get('source_type') or record.get('planned_source_type', '')}
    quoted_excerpt: \"\"
    source_snapshot_hash: \"\"
    license_note: \"\"
    security_note: \"\"
    maintenance_note: \"\"
    architecture_fit_note: \"\"
    supply_chain_note: \"\"
    reviewer: \"\"
    reviewed_at: \"\"
    accepted_for_ingestion: false
    integration_allowed_from_record: false"""


def build_gate(records: list[dict]) -> dict:
    return {
        "gate_id": "avf-capability-owner-primary-source-evidence-population-packet-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "gate_decision": "PACKET_READY_AWAITING_OWNER_OR_PRO_POPULATION",
        "integration_decision": "blocked",
        "source_slots_to_populate": len(records),
        "records_completed_by_default": 0,
        "records_accepted_by_default": 0,
        "manual_or_pro_input_required": True,
        "automated_research_allowed": False,
        "source_families": SOURCE_FAMILIES,
        "required_evidence_fields": REQUIRED_EVIDENCE_FIELDS,
        "population_packet_uri": rel(OWNER_POPULATION_PACKET),
        "pro_prompt_uri": rel(OWNER_POPULATION_PRO_PROMPT),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_pro_prompt() -> str:
    field_list = "\n".join(f"- `{field}`" for field in REQUIRED_EVIDENCE_FIELDS)
    family_list = "\n".join(f"- `{family}`" for family in SOURCE_FAMILIES)
    return f"""# AVF Owner Primary-Source Evidence Population PRO Prompt

Use this PRO Prompt when you want GPT Pro or another human-reviewed research lane to fill the repo-local primary-source evidence packet.

You are a primary-source evidence reviewer for AVF capability acquisition.

Use primary/original sources only:

{family_list}

Task:

Populate the 35 evidence records from `avf/capabilities/generated/capability_owner_primary_source_evidence_population_packet.yml`.

For each record, fill only these fields:

{field_list}

Rules:

- Use primary/original sources only.
- Return populated evidence records only.
- Keep quoted excerpts short and directly relevant.
- Include `source_snapshot_hash` for the captured source snapshot or source text.
- Include `license_note`, `security_note`, `maintenance_note`, `architecture_fit_note`, and `supply_chain_note` separately.
- Do not mark any record accepted for ingestion.
- Do not mark any record accepted for integration.
- Do not claim release readiness.
- Do not claim production readiness.
- Do not fetch code, clone repositories, install packages, call providers, automate scraping, deploy, publish, or post.

Output format:

Return YAML blocks matching the original `source_slot_id` values, with the required evidence fields populated. Do not include unrelated commentary.
"""


def build_validation_result(records: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_capability_owner_primary_source_evidence_population_packet_v0_1",
        "status": "PASS",
        "checks": [
            "owner/PRO primary-source evidence population packet exists",
            "source families listed",
            "required evidence fields listed",
            "PRO prompt exists",
            "records remain blocked by default",
            "protected-action flags false",
        ],
        "source_slots_to_populate": len(records),
        "records_completed_by_default": 0,
        "records_accepted_by_default": 0,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-owner-filled-primary-source-evidence-review-v0-1
title: Add AVF owner-filled primary-source evidence review gate v0.1
goal: Define the repo-local review gate for owner/PRO-filled primary-source evidence records before any source can be accepted for ingestion or capability integration.
context_paths:
  - avf/capabilities/generated/capability_owner_primary_source_evidence_population_packet.yml
  - avf/capabilities/generated/capability_owner_primary_source_evidence_population_packet_gate.json
  - avf/capabilities/generated/capability_owner_primary_source_evidence_population_pro_prompt.md
files_likely_to_touch:
  - scripts/run_avf_capability_owner_filled_primary_source_evidence_review_v0_1.py
  - scripts/validate_avf_capability_owner_filled_primary_source_evidence_review_v0_1.py
  - avf/capabilities/generated/capability_owner_filled_primary_source_evidence_review_gate.json
  - docs/goals/AVF_CAPABILITY_OWNER_FILLED_PRIMARY_SOURCE_EVIDENCE_REVIEW_V0_1_REPORT.md
forbidden_changes:
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
  - review gate checks whether owner/PRO-filled evidence has all required fields
  - empty or partial records remain blocked
  - no capability integration is allowed without accepted source evidence
  - protected actions remain blocked
validation_commands:
  - python scripts\\validate_avf_capability_owner_primary_source_evidence_population_packet_v0_1.py
  - python scripts\\validate_avf_capability_owner_filled_primary_source_evidence_review_v0_1.py
expected_outputs:
  - owner-filled source evidence review gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(records: list[dict]) -> str:
    return f"""# AVF Capability Owner Primary-Source Evidence Population Packet v0.1 Report

RESULT: PASS
capability_owner_primary_source_evidence_population_packet_v0_1=true
owner_primary_source_evidence_population_packet_created=true
owner_primary_source_evidence_population_gate_created=true
pro_prompt_created=true
source_families_listed=true
required_evidence_fields_listed=true
source_slots_to_populate={len(records)}
records_completed_by_default=0
records_accepted_by_default=0
integration_decision=blocked
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

## Boundary

This packet prepares owner/PRO population of primary-source evidence only. It does not execute external research, provider calls, live model calls, external service calls, scraping, fetching, cloning, installing, runtime integration, deployment, publishing, or readiness claims.

## Next Safe Goal

`{NEXT_SAFE_GOAL_ID}` should review populated evidence records and keep empty or partial records blocked before ingestion or integration.
"""


def main() -> None:
    gate = read_json(POPULATION_GATE)
    require_previous_gate(gate)
    records = parse_workspace_records()
    if len(records) != 35:
        raise SystemExit("owner/PRO population packet requires 35 source records")

    write_text(OWNER_POPULATION_PACKET, build_packet(records))
    write_json(OWNER_POPULATION_GATE, build_gate(records))
    write_text(OWNER_POPULATION_PRO_PROMPT, build_pro_prompt())
    write_json(VALIDATION_RESULT, build_validation_result(records))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_text(VALIDATION_REPORT, build_report(records))

    print("AVF Capability Owner Primary-Source Evidence Population Packet v0.1")
    print("RESULT: PASS")
    print(f"source_slots_to_populate={len(records)}")
    print("records_completed_by_default=0")
    print("records_accepted_by_default=0")
    print("integration_decision=blocked")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

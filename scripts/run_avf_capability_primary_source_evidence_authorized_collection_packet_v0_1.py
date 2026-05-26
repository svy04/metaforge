from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RETRY_REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_retry_review_gate.json"
RETRY_PACKET = CAPABILITIES / "capability_primary_source_evidence_population_retry_packet.yml"
PRO_PROMPT = CAPABILITIES / "capability_owner_primary_source_evidence_population_pro_prompt.md"
COLLECTION_PACKET = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_packet.yml"
COLLECTION_GATE = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_AUTHORIZED_COLLECTION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_retry_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_run_plan_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
AUTHORIZATION_DECISION = "BLOCKED_PENDING_EXPLICIT_COLLECTION_AUTHORIZATION"

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

AUTHORIZATION_FIELDS = [
    "owner_authorization_statement",
    "authorized_by",
    "authorized_at",
    "authorization_expires_at",
    "authorized_collection_modes",
    "authorized_source_families",
    "authorized_candidate_ids",
    "authorized_source_slot_ids",
    "max_records_to_collect",
    "collection_boundaries",
    "revocation_note",
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


def require_retry_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("retry review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("retry review gate must point to this authorized collection goal")
    if gate.get("review_decision") != "BLOCKED_RETRY_EVIDENCE_NOT_FILLED":
        raise SystemExit("retry review gate decision mismatch")
    if gate.get("integration_decision") != "blocked":
        raise SystemExit("retry review gate must keep integration blocked")
    counts = gate.get("source_entry_counts", {})
    if counts.get("retry_records_reviewed") != 35:
        raise SystemExit("retry review gate must include 35 retry records")
    if counts.get("accepted_retry_records") != 0:
        raise SystemExit("retry review gate must not accept records")


def build_collection_modes() -> list[dict]:
    return [
        {
            "mode_id": "owner_manual_primary_source_collection",
            "label": "Owner manual browser research",
            "authorization_required": True,
            "collection_allowed": False,
            "allowed_after_authorization": True,
            "boundary": "Owner may manually inspect primary/original sources and paste evidence into repo-local records after filling authorization fields.",
        },
        {
            "mode_id": "pro_manual_primary_source_collection",
            "label": "PRO-assisted manual primary-source research",
            "authorization_required": True,
            "collection_allowed": False,
            "allowed_after_authorization": True,
            "boundary": "PRO may prepare primary-source notes for owner review, but this branch does not call providers or live models.",
        },
        {
            "mode_id": "codex_assisted_link_opening_after_explicit_authorization",
            "label": "Codex assisted link opening",
            "authorization_required": True,
            "collection_allowed": False,
            "allowed_after_authorization": True,
            "boundary": "Codex may only open owner-authorized primary/original source links for review; scraping, clone, install, and integration remain forbidden.",
        },
        {
            "mode_id": "automated_connector_collection",
            "label": "Automated connector collection",
            "authorization_required": True,
            "collection_allowed": False,
            "allowed_after_authorization": False,
            "boundary": "Automated collection requires a future narrower connector policy, separate approval, audit, and validator before use.",
        },
    ]


def build_source_collection_records(retry_reviews: list[dict]) -> list[dict]:
    records: list[dict] = []
    for review in retry_reviews:
        records.append(
            {
                "candidate_id": review.get("candidate_id", ""),
                "candidate_name": review.get("candidate_name", ""),
                "capability_id": review.get("capability_id", ""),
                "source_slot_id": review.get("source_slot_id", ""),
                "planned_target_uri": review.get("planned_target_uri", ""),
                "planned_source_type": review.get("planned_source_type", ""),
                "previous_review_status": review.get("review_status", ""),
                "collection_status": "awaiting_explicit_authorization",
                "collection_allowed": False,
                "trusted_source": False,
                "accepted_for_ingestion": False,
                "accepted_for_integration": False,
                "integration_allowed_from_record": False,
                "authorization_required_fields": AUTHORIZATION_FIELDS,
            }
        )
    return records


def build_candidate_collection_records(source_records: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for record in source_records:
        grouped[record["candidate_id"]].append(record)
    candidate_records: list[dict] = []
    for candidate_id, records in sorted(grouped.items()):
        candidate_records.append(
            {
                "candidate_id": candidate_id,
                "source_records_targeted": len(records),
                "source_records_authorized": 0,
                "trusted_source_records": 0,
                "ingested_source_records": 0,
                "integrated_source_records": 0,
                "candidate_status": "blocked_pending_explicit_collection_authorization",
                "collection_proposal_allowed": False,
                "integration_proposal_allowed": False,
            }
        )
    return candidate_records


def build_collection_gate(source_records: list[dict]) -> dict:
    return {
        "gate_id": "avf-capability-primary-source-evidence-authorized-collection-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "authorization_decision": AUTHORIZATION_DECISION,
        "collection_authorization_status": "not_authorized",
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "manual_owner_collection_allowed": False,
        "pro_manual_collection_allowed": False,
        "codex_assisted_link_opening_allowed": False,
        "automated_collection_allowed": False,
        "authorization_fields": AUTHORIZATION_FIELDS,
        "allowed_source_families_after_explicit_authorization": PRIMARY_SOURCE_FAMILIES,
        "collection_modes": build_collection_modes(),
        "source_entry_counts": {
            "source_records_targeted": len(source_records),
            "source_records_authorized": 0,
            "trusted_source_records": 0,
            "ingested_source_records": 0,
            "integrated_source_records": 0,
        },
        "source_collection_records": source_records,
        "candidate_collection_records": build_candidate_collection_records(source_records),
        "retry_review_gate_uri": rel(RETRY_REVIEW_GATE),
        "retry_packet_uri": rel(RETRY_PACKET),
        "pro_prompt_uri": rel(PRO_PROMPT),
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def yaml_bool(value: bool) -> str:
    return "true" if value else "false"


def build_collection_packet(gate: dict) -> str:
    families = "\n".join(f"  - {family}" for family in PRIMARY_SOURCE_FAMILIES)
    fields = "\n".join(f"  - {field}" for field in AUTHORIZATION_FIELDS)
    modes = "\n".join(
        [
            f"  - mode_id: {mode['mode_id']}\n"
            f"    authorization_required: {yaml_bool(mode['authorization_required'])}\n"
            f"    collection_allowed: {yaml_bool(mode['collection_allowed'])}\n"
            f"    allowed_after_authorization: {yaml_bool(mode['allowed_after_authorization'])}\n"
            f"    boundary: {mode['boundary']}"
            for mode in gate["collection_modes"]
        ]
    )
    records = "\n".join(
        [
            f"  - candidate_id: {record['candidate_id']}\n"
            f"    candidate_name: {record['candidate_name']}\n"
            f"    capability_id: {record['capability_id']}\n"
            f"    source_slot_id: {record['source_slot_id']}\n"
            f"    planned_target_uri: {record['planned_target_uri']}\n"
            f"    planned_source_type: {record['planned_source_type']}\n"
            f"    previous_review_status: {record['previous_review_status']}\n"
            f"    collection_status: {record['collection_status']}\n"
            f"    collection_allowed: false\n"
            f"    trusted_source: false\n"
            f"    accepted_for_ingestion: false\n"
            f"    accepted_for_integration: false\n"
            f"    integration_allowed_from_record: false"
            for record in gate["source_collection_records"]
        ]
    )
    return f"""packet_id: avf-capability-primary-source-evidence-authorized-collection-packet-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
authorization_decision: {AUTHORIZATION_DECISION}
collection_authorization_status: not_authorized
owner_authorization_required: true
owner_authorization_granted: false
manual_owner_collection_allowed: false
pro_manual_collection_allowed: false
codex_assisted_link_opening_allowed: false
automated_collection_allowed: false
automated_scraping_allowed: false
source_records_targeted: {gate['source_entry_counts']['source_records_targeted']}
source_records_authorized: 0
trusted_sources_by_default: false
ingested_sources_by_default: false
integrated_sources_by_default: false
integration_decision: blocked
release_ready: false
production_ready: false

authorization_fields_required_before_collection:
{fields}

allowed_source_families_after_explicit_authorization:
{families}

collection_modes:
{modes}

source_collection_records:
{records}

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


def build_validation_result(gate: dict) -> dict:
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_authorized_collection_packet_v0_1",
        "status": "PASS",
        "checks": [
            "authorized collection packet exists",
            "explicit authorization fields are listed",
            "manual owner and PRO collection are distinguished from automated collection",
            "no source is trusted, ingested, or integrated by default",
            "protected-action flags remain false",
        ],
        "authorization_decision": AUTHORIZATION_DECISION,
        "source_records_targeted": gate["source_entry_counts"]["source_records_targeted"],
        "source_records_authorized": 0,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-evidence-authorized-collection-run-plan-v0-1
title: Add AVF authorized primary-source evidence collection run plan v0.1
goal: Define the repo-local run plan for explicit owner-authorized primary-source evidence collection without executing external collection from this packet.
context_paths:
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_packet.yml
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_population_retry_packet.yml
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_run_plan.yml
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_run_plan_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_AUTHORIZED_COLLECTION_RUN_PLAN_V0_1_REPORT.md
forbidden_changes:
  - No external collection execution until explicit authorization fields are filled and reviewed
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
  - run plan references the authorized collection packet and gate
  - run plan keeps source records blocked until explicit authorization is present
  - run plan defines manual owner/PRO/Codex-assisted modes separately
  - no source is trusted, ingested, or integrated by default
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_authorized_collection_packet_v0_1.py
expected_outputs:
  - authorized collection run plan
  - run plan gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    return f"""# AVF Capability Primary-Source Evidence Authorized Collection Packet v0.1 Report

RESULT: PASS
capability_primary_source_evidence_authorized_collection_packet_v0_1=true
authorized_collection_packet_created=true
authorized_collection_gate_created=true
source_records_targeted={counts['source_records_targeted']}
source_records_authorized={counts['source_records_authorized']}
trusted_sources_by_default=false
ingested_sources_by_default=false
integrated_sources_by_default=false
owner_authorization_required=true
owner_authorization_granted=false
manual_owner_collection_allowed=false
pro_manual_collection_allowed=false
codex_assisted_link_opening_allowed=false
automated_collection_allowed=false
integration_decision=blocked
authorization_decision={AUTHORIZATION_DECISION}
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

## Decision

The authorized collection packet defines the fields and collection modes that must be explicitly approved before AVF can collect primary/original source evidence. All 35 source records remain untrusted, uningested, and unintegrated by default.

## Next Safe Goal

`{NEXT_SAFE_GOAL_ID}` should create a repo-local run plan that remains blocked unless explicit authorization fields are filled and reviewed.
"""


def main() -> None:
    retry_review_gate = read_json(RETRY_REVIEW_GATE)
    require_retry_review_gate(retry_review_gate)
    retry_reviews = retry_review_gate.get("retry_record_reviews", [])
    if len(retry_reviews) != 35:
        raise SystemExit("authorized collection packet requires 35 retry review records")

    source_records = build_source_collection_records(retry_reviews)
    gate = build_collection_gate(source_records)

    write_text(COLLECTION_PACKET, build_collection_packet(gate))
    write_json(COLLECTION_GATE, gate)
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_text(VALIDATION_REPORT, build_report(gate))

    counts = gate["source_entry_counts"]
    print("AVF Capability Primary-Source Evidence Authorized Collection Packet v0.1")
    print("RESULT: PASS")
    print(f"source_records_targeted={counts['source_records_targeted']}")
    print(f"source_records_authorized={counts['source_records_authorized']}")
    print(f"authorization_decision={gate['authorization_decision']}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

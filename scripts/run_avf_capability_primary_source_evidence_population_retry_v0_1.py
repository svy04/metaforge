from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

REVIEW_GATE = CAPABILITIES / "capability_owner_filled_primary_source_evidence_review_gate.json"
RETRY_PACKET = CAPABILITIES / "capability_primary_source_evidence_population_retry_packet.yml"
RETRY_GATE = CAPABILITIES / "capability_primary_source_evidence_population_retry_gate.json"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_population_retry_v0_1.validation_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_population_retry_next_codex_task_packet.yml"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_POPULATION_RETRY_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_population_retry_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_owner_filled_primary_source_evidence_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_retry_review_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
RETRY_DECISION = "RETRY_PACKET_READY_AWAITING_OWNER_OR_PRO_EVIDENCE"

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


def require_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous review gate must point to this retry goal")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_slots_reviewed") != 35:
        raise SystemExit("previous review gate must review 35 records")
    if counts.get("empty_source_records") != 35:
        raise SystemExit("previous review gate must expose 35 empty records")
    if counts.get("accepted_source_records") != 0:
        raise SystemExit("previous review gate must not accept source records")
    if gate.get("integration_decision") != "blocked":
        raise SystemExit("previous review gate must keep integration blocked")


def build_retry_packet(blocked_reviews: list[dict]) -> str:
    fields = "\n".join(f"  - {field}" for field in REQUIRED_EVIDENCE_FIELDS)
    records = "\n".join(build_retry_record(review) for review in blocked_reviews)
    return f"""packet_id: avf-capability-primary-source-evidence-population-retry-packet-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
retry_attempt: 1
retry_reason: previous_review_gate_blocked_empty_records
retry_source_records: {len(blocked_reviews)}
empty_records_to_retry: {len(blocked_reviews)}
records_accepted_by_default: 0
integration_allowed_from_retry: false
manual_or_pro_input_required: true
external_fetch_allowed_by_packet: false
automated_scraping_allowed: false
oss_clone_allowed_by_packet: false
dependency_install_allowed_by_packet: false
runtime_integration_allowed_by_packet: false
release_ready: false
production_ready: false

required_evidence_fields:
{fields}

retry_instructions:
  - Fill only primary/original source evidence fields.
  - Preserve source_slot_id so the retry review can map evidence back to the blocked record.
  - Keep accepted_for_ingestion false until a later ingestion validator accepts the record.
  - Keep integration_allowed_from_record false until evidence and owner approval gates pass.
  - Do not fetch, scrape, clone, install, integrate, deploy, publish, or claim readiness from this packet.

retry_records:
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


def build_retry_record(review: dict) -> str:
    return f"""  - candidate_id: {review.get('candidate_id', '')}
    candidate_name: {review.get('candidate_name', '')}
    capability_id: {review.get('capability_id', '')}
    source_slot_id: {review.get('source_slot_id', '')}
    planned_target_uri: {review.get('planned_target_uri', '')}
    planned_source_type: {review.get('planned_source_type', '')}
    previous_review_status: {review.get('review_status', '')}
    retry_status: awaiting_owner_or_pro_population
    missing_required_fields: {', '.join(review.get('missing_required_fields', []))}
    source_uri: \"\"
    source_type: \"\"
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


def build_retry_gate(blocked_reviews: list[dict]) -> dict:
    return {
        "gate_id": "avf-capability-primary-source-evidence-population-retry-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "retry_decision": RETRY_DECISION,
        "integration_decision": "blocked",
        "retry_source_records": len(blocked_reviews),
        "empty_records_to_retry": len(blocked_reviews),
        "records_accepted_by_default": 0,
        "manual_or_pro_input_required": True,
        "required_evidence_fields": REQUIRED_EVIDENCE_FIELDS,
        "retry_packet_uri": rel(RETRY_PACKET),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(blocked_reviews: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_population_retry_v0_1",
        "status": "PASS",
        "checks": [
            "previous owner-filled review gate was read",
            "blocked empty source records were preserved",
            "retry packet preserves required evidence fields",
            "no record accepted by default",
            "protected-action flags false",
        ],
        "retry_source_records": len(blocked_reviews),
        "empty_records_to_retry": len(blocked_reviews),
        "records_accepted_by_default": 0,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-evidence-retry-review-v0-1
title: Add AVF primary-source evidence retry review gate v0.1
goal: Review any owner/PRO-filled retry evidence records before accepting them for ingestion or capability integration.
context_paths:
  - avf/capabilities/generated/capability_primary_source_evidence_population_retry_packet.yml
  - avf/capabilities/generated/capability_primary_source_evidence_population_retry_gate.json
  - avf/capabilities/generated/capability_owner_filled_primary_source_evidence_review_gate.json
files_likely_to_touch:
  - scripts/run_avf_capability_primary_source_evidence_retry_review_v0_1.py
  - scripts/validate_avf_capability_primary_source_evidence_retry_review_v0_1.py
  - avf/capabilities/generated/capability_primary_source_evidence_retry_review_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_RETRY_REVIEW_V0_1_REPORT.md
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
  - retry review checks every required evidence field
  - empty or partial retry records remain blocked
  - completed records are still not integrated without later acceptance and owner approval gates
  - protected actions remain blocked
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_population_retry_v0_1.py
expected_outputs:
  - primary-source evidence retry review gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(blocked_reviews: list[dict]) -> str:
    return f"""# AVF Capability Primary-Source Evidence Population Retry v0.1 Report

RESULT: PASS
capability_primary_source_evidence_population_retry_v0_1=true
primary_source_evidence_population_retry_packet_created=true
primary_source_evidence_population_retry_gate_created=true
retry_source_records={len(blocked_reviews)}
empty_records_to_retry={len(blocked_reviews)}
records_accepted_by_default=0
integration_decision=blocked
retry_decision={RETRY_DECISION}
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

The retry packet preserves the 35 empty source records blocked by the owner-filled evidence review gate. It provides another owner/PRO population surface without trusting, ingesting, integrating, fetching, scraping, cloning, installing, deploying, publishing, or claiming readiness.
"""


def main() -> None:
    review_gate = read_json(REVIEW_GATE)
    require_review_gate(review_gate)
    blocked_reviews = [
        review
        for review in review_gate.get("source_record_reviews", [])
        if review.get("review_status") == "empty_record_blocked"
    ]
    if len(blocked_reviews) != 35:
        raise SystemExit("retry packet requires 35 empty blocked source records")

    write_text(RETRY_PACKET, build_retry_packet(blocked_reviews))
    write_json(RETRY_GATE, build_retry_gate(blocked_reviews))
    write_json(VALIDATION_RESULT, build_validation_result(blocked_reviews))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_text(VALIDATION_REPORT, build_report(blocked_reviews))

    print("AVF Capability Primary-Source Evidence Population Retry v0.1")
    print("RESULT: PASS")
    print(f"retry_source_records={len(blocked_reviews)}")
    print(f"empty_records_to_retry={len(blocked_reviews)}")
    print("records_accepted_by_default=0")
    print("integration_decision=blocked")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

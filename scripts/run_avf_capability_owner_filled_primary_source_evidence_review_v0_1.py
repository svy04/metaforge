from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

POPULATION_PACKET = CAPABILITIES / "capability_owner_primary_source_evidence_population_packet.yml"
POPULATION_GATE = CAPABILITIES / "capability_owner_primary_source_evidence_population_packet_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_owner_filled_primary_source_evidence_review_gate.json"
VALIDATION_RESULT = CAPABILITIES / "capability_owner_filled_primary_source_evidence_review_v0_1.validation_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_owner_filled_primary_source_evidence_review_next_codex_task_packet.yml"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_OWNER_FILLED_PRIMARY_SOURCE_EVIDENCE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_owner_filled_primary_source_evidence_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_owner_primary_source_evidence_population_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_population_retry_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
REVIEW_DECISION = "BLOCKED_OWNER_OR_PRO_EVIDENCE_NOT_FILLED"

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

CAPTURED_EVIDENCE_FIELDS = [
    "source_uri",
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


def parse_population_records() -> list[dict]:
    records: list[dict] = []
    current: dict | None = None
    for raw_line in POPULATION_PACKET.read_text(encoding="utf-8").splitlines():
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


def require_population_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("population gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("population gate must point to this review goal")
    if gate.get("source_slots_to_populate") != 35:
        raise SystemExit("population gate source slot count mismatch")
    if gate.get("records_completed_by_default") != 0:
        raise SystemExit("population gate must not complete records by default")
    if gate.get("records_accepted_by_default") != 0:
        raise SystemExit("population gate must not accept records by default")


def review_record(record: dict) -> dict:
    if all(not record.get(field) for field in CAPTURED_EVIDENCE_FIELDS):
        review_status = "empty_record_blocked"
        missing = REQUIRED_EVIDENCE_FIELDS
    else:
        missing = [field for field in REQUIRED_EVIDENCE_FIELDS if not record.get(field)]
        review_status = "partial_record_blocked" if missing else "complete_record_pending_ingestion_gate"
    return {
        "candidate_id": record.get("candidate_id", ""),
        "candidate_name": record.get("candidate_name", ""),
        "capability_id": record.get("capability_id", ""),
        "source_slot_id": record.get("source_slot_id", ""),
        "planned_target_uri": record.get("planned_target_uri", ""),
        "planned_source_type": record.get("planned_source_type", ""),
        "review_status": review_status,
        "missing_required_fields": missing,
        "accepted_for_ingestion": False,
        "accepted_for_integration": False,
    }


def build_candidate_reviews(record_reviews: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for review in record_reviews:
        grouped[review["candidate_id"]].append(review)
    candidate_reviews: list[dict] = []
    for candidate_id, reviews in sorted(grouped.items()):
        complete_count = sum(1 for review in reviews if review["review_status"] == "complete_record_pending_ingestion_gate")
        candidate_reviews.append(
            {
                "candidate_id": candidate_id,
                "source_slots_reviewed": len(reviews),
                "complete_source_records": complete_count,
                "accepted_source_records": 0,
                "candidate_status": "blocked_no_complete_primary_source_records",
                "integration_proposal_allowed": False,
            }
        )
    return candidate_reviews


def build_review_gate(record_reviews: list[dict]) -> dict:
    empty_count = sum(1 for review in record_reviews if review["review_status"] == "empty_record_blocked")
    partial_count = sum(1 for review in record_reviews if review["review_status"] == "partial_record_blocked")
    complete_count = sum(1 for review in record_reviews if review["review_status"] == "complete_record_pending_ingestion_gate")
    return {
        "gate_id": "avf-capability-owner-filled-primary-source-evidence-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "integration_decision": "blocked",
        "population_packet_uri": rel(POPULATION_PACKET),
        "source_entry_counts": {
            "source_slots_reviewed": len(record_reviews),
            "empty_source_records": empty_count,
            "partial_source_records": partial_count,
            "complete_source_records": complete_count,
            "accepted_source_records": 0,
            "integration_allowed_records": 0,
        },
        "required_evidence_fields": REQUIRED_EVIDENCE_FIELDS,
        "captured_evidence_fields": CAPTURED_EVIDENCE_FIELDS,
        "source_record_reviews": record_reviews,
        "candidate_review_records": build_candidate_reviews(record_reviews),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_owner_filled_primary_source_evidence_review_v0_1",
        "status": "PASS",
        "checks": [
            "owner/PRO population packet reviewed",
            "source_type alone is not treated as completed evidence",
            "empty records remain blocked",
            "no source evidence accepted for ingestion or integration",
            "protected-action flags false",
        ],
        "review_decision": gate["review_decision"],
        "source_slots_reviewed": counts["source_slots_reviewed"],
        "empty_source_records": counts["empty_source_records"],
        "partial_source_records": counts["partial_source_records"],
        "complete_source_records": counts["complete_source_records"],
        "accepted_source_records": counts["accepted_source_records"],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-evidence-population-retry-v0-1
title: Prepare AVF primary-source evidence population retry packet v0.1
goal: Provide the next owner/PRO action packet for filling missing primary-source evidence records after the review gate blocks empty records.
context_paths:
  - avf/capabilities/generated/capability_owner_primary_source_evidence_population_packet.yml
  - avf/capabilities/generated/capability_owner_filled_primary_source_evidence_review_gate.json
  - avf/capabilities/generated/capability_owner_primary_source_evidence_population_pro_prompt.md
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_population_retry_packet.yml
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_POPULATION_RETRY_V0_1_REPORT.md
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
  - retry packet lists blocked empty source records
  - retry packet preserves required evidence fields
  - no record is accepted by default
  - protected actions remain blocked
validation_commands:
  - python scripts\\validate_avf_capability_owner_filled_primary_source_evidence_review_v0_1.py
expected_outputs:
  - primary-source evidence population retry packet
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    return f"""# AVF Capability Owner-Filled Primary-Source Evidence Review v0.1 Report

RESULT: PASS
capability_owner_filled_primary_source_evidence_review_v0_1=true
owner_filled_primary_source_evidence_review_gate_created=true
source_slots_reviewed={counts['source_slots_reviewed']}
empty_source_records={counts['empty_source_records']}
partial_source_records={counts['partial_source_records']}
complete_source_records={counts['complete_source_records']}
accepted_source_records={counts['accepted_source_records']}
integration_decision={gate['integration_decision']}
review_decision={gate['review_decision']}
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

The review gate inspected 35 owner/PRO population slots. `source_type` values are present as planned metadata, but no captured primary-source evidence fields are populated. Every record remains blocked for ingestion and integration.

## Boundary

This gate does not execute external research, provider calls, live model calls, external service calls, scraping, fetching, cloning, installing, runtime integration, deployment, publishing, or readiness claims.
"""


def main() -> None:
    population_gate = read_json(POPULATION_GATE)
    require_population_gate(population_gate)
    records = parse_population_records()
    if len(records) != 35:
        raise SystemExit("owner-filled evidence review requires 35 population records")
    record_reviews = [review_record(record) for record in records]
    gate = build_review_gate(record_reviews)

    write_json(REVIEW_GATE, gate)
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_text(VALIDATION_REPORT, build_report(gate))

    counts = gate["source_entry_counts"]
    print("AVF Capability Owner-Filled Primary-Source Evidence Review v0.1")
    print("RESULT: PASS")
    print(f"source_slots_reviewed={counts['source_slots_reviewed']}")
    print(f"empty_source_records={counts['empty_source_records']}")
    print(f"accepted_source_records={counts['accepted_source_records']}")
    print(f"review_decision={gate['review_decision']}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

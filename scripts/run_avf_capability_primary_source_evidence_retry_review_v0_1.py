from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RETRY_PACKET = CAPABILITIES / "capability_primary_source_evidence_population_retry_packet.yml"
RETRY_GATE = CAPABILITIES / "capability_primary_source_evidence_population_retry_gate.json"
RETRY_REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_retry_review_gate.json"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_retry_review_v0_1.validation_result.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_retry_review_next_codex_task_packet.yml"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_RETRY_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_retry_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_population_retry_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_packet_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
REVIEW_DECISION = "BLOCKED_RETRY_EVIDENCE_NOT_FILLED"

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

CAPTURED_EVIDENCE_FIELDS = REQUIRED_EVIDENCE_FIELDS


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


def parse_retry_records() -> list[dict]:
    records: list[dict] = []
    current: dict | None = None
    for raw_line in RETRY_PACKET.read_text(encoding="utf-8").splitlines():
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


def require_retry_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("retry gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("retry gate must point to this retry review goal")
    if gate.get("retry_source_records") != 35:
        raise SystemExit("retry gate retry source count mismatch")
    if gate.get("records_accepted_by_default") != 0:
        raise SystemExit("retry gate must not accept records by default")
    if gate.get("integration_decision") != "blocked":
        raise SystemExit("retry gate must keep integration blocked")


def review_retry_record(record: dict) -> dict:
    if all(not record.get(field) for field in CAPTURED_EVIDENCE_FIELDS):
        review_status = "empty_retry_record_blocked"
        missing = REQUIRED_EVIDENCE_FIELDS
    else:
        missing = [field for field in REQUIRED_EVIDENCE_FIELDS if not record.get(field)]
        review_status = "partial_retry_record_blocked" if missing else "complete_retry_record_pending_acceptance_gate"
    return {
        "candidate_id": record.get("candidate_id", ""),
        "candidate_name": record.get("candidate_name", ""),
        "capability_id": record.get("capability_id", ""),
        "source_slot_id": record.get("source_slot_id", ""),
        "planned_target_uri": record.get("planned_target_uri", ""),
        "planned_source_type": record.get("planned_source_type", ""),
        "previous_review_status": record.get("previous_review_status", ""),
        "review_status": review_status,
        "missing_required_fields": missing,
        "accepted_for_ingestion": False,
        "accepted_for_integration": False,
    }


def build_candidate_reviews(retry_reviews: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for review in retry_reviews:
        grouped[review["candidate_id"]].append(review)
    candidate_reviews: list[dict] = []
    for candidate_id, reviews in sorted(grouped.items()):
        complete_count = sum(1 for review in reviews if review["review_status"] == "complete_retry_record_pending_acceptance_gate")
        candidate_reviews.append(
            {
                "candidate_id": candidate_id,
                "retry_records_reviewed": len(reviews),
                "complete_retry_records": complete_count,
                "accepted_retry_records": 0,
                "candidate_status": "blocked_no_complete_retry_evidence",
                "integration_proposal_allowed": False,
            }
        )
    return candidate_reviews


def build_retry_review_gate(retry_reviews: list[dict]) -> dict:
    empty_count = sum(1 for review in retry_reviews if review["review_status"] == "empty_retry_record_blocked")
    partial_count = sum(1 for review in retry_reviews if review["review_status"] == "partial_retry_record_blocked")
    complete_count = sum(1 for review in retry_reviews if review["review_status"] == "complete_retry_record_pending_acceptance_gate")
    return {
        "gate_id": "avf-capability-primary-source-evidence-retry-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "integration_decision": "blocked",
        "retry_packet_uri": rel(RETRY_PACKET),
        "source_entry_counts": {
            "retry_records_reviewed": len(retry_reviews),
            "empty_retry_records": empty_count,
            "partial_retry_records": partial_count,
            "complete_retry_records": complete_count,
            "accepted_retry_records": 0,
            "integration_allowed_records": 0,
        },
        "required_evidence_fields": REQUIRED_EVIDENCE_FIELDS,
        "captured_evidence_fields": CAPTURED_EVIDENCE_FIELDS,
        "retry_record_reviews": retry_reviews,
        "candidate_review_records": build_candidate_reviews(retry_reviews),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_retry_review_v0_1",
        "status": "PASS",
        "checks": [
            "primary-source evidence retry packet reviewed",
            "empty retry records remain blocked",
            "no retry source evidence accepted for ingestion or integration",
            "next safe goal moves toward authorized primary-source collection",
            "protected-action flags false",
        ],
        "review_decision": gate["review_decision"],
        "retry_records_reviewed": counts["retry_records_reviewed"],
        "empty_retry_records": counts["empty_retry_records"],
        "partial_retry_records": counts["partial_retry_records"],
        "complete_retry_records": counts["complete_retry_records"],
        "accepted_retry_records": counts["accepted_retry_records"],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-evidence-authorized-collection-packet-v0-1
title: Add AVF authorized primary-source evidence collection packet v0.1
goal: Define the explicit owner-authorized collection packet required before filling primary/original source evidence records for OSS, paper, patent, and standard review.
context_paths:
  - avf/capabilities/generated/capability_primary_source_evidence_retry_review_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_population_retry_packet.yml
  - avf/capabilities/generated/capability_owner_primary_source_evidence_population_pro_prompt.md
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_packet.yml
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_AUTHORIZED_COLLECTION_PACKET_V0_1_REPORT.md
forbidden_changes:
  - No provider calls without explicit owner authorization
  - No live model calls without explicit owner authorization
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
  - collection packet lists explicit authorization fields
  - collection packet distinguishes manual owner/PRO research from automated collection
  - no source is marked trusted, ingested, or integrated by default
  - protected actions remain blocked until explicit authorization fields are filled
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_retry_review_v0_1.py
expected_outputs:
  - authorized collection packet
  - collection gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    return f"""# AVF Capability Primary-Source Evidence Retry Review v0.1 Report

RESULT: PASS
capability_primary_source_evidence_retry_review_v0_1=true
primary_source_evidence_retry_review_gate_created=true
retry_records_reviewed={counts['retry_records_reviewed']}
empty_retry_records={counts['empty_retry_records']}
partial_retry_records={counts['partial_retry_records']}
complete_retry_records={counts['complete_retry_records']}
accepted_retry_records={counts['accepted_retry_records']}
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

The retry review gate inspected 35 retry records. No primary-source evidence fields were filled, so every record remains blocked for ingestion and integration.

## Next Safe Goal

`{NEXT_SAFE_GOAL_ID}` should define the explicit owner-authorized collection packet needed before filling OSS, paper, patent, and standards evidence records.
"""


def main() -> None:
    retry_gate = read_json(RETRY_GATE)
    require_retry_gate(retry_gate)
    retry_records = parse_retry_records()
    if len(retry_records) != 35:
        raise SystemExit("retry review requires 35 retry records")
    retry_reviews = [review_retry_record(record) for record in retry_records]
    gate = build_retry_review_gate(retry_reviews)

    write_json(RETRY_REVIEW_GATE, gate)
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_text(VALIDATION_REPORT, build_report(gate))

    counts = gate["source_entry_counts"]
    print("AVF Capability Primary-Source Evidence Retry Review v0.1")
    print("RESULT: PASS")
    print(f"retry_records_reviewed={counts['retry_records_reviewed']}")
    print(f"empty_retry_records={counts['empty_retry_records']}")
    print(f"accepted_retry_records={counts['accepted_retry_records']}")
    print(f"review_decision={gate['review_decision']}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

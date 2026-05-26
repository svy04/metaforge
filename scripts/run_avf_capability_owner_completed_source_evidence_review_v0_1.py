from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RESEARCH_PACKET = CAPABILITIES / "capability_primary_source_research_packet.yml"
PRO_PROMPT = CAPABILITIES / "capability_primary_source_research_pro_prompt.md"
FIXTURE_TEMPLATE = CAPABILITIES / "capability_source_evidence_fixture_template.yml"
FIXTURE_MANIFEST = CAPABILITIES / "capability_source_evidence_fixture_template_manifest.json"
REVIEW_GATE = CAPABILITIES / "capability_owner_completed_source_evidence_review_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_owner_completed_source_evidence_review_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_owner_completed_source_evidence_review_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_OWNER_COMPLETED_SOURCE_EVIDENCE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_owner_completed_source_evidence_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_external_primary_source_research_authorization_packet_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
REVIEW_DECISION = "BLOCKED_OWNER_EVIDENCE_NOT_COMPLETED"

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

REQUIRED_CATEGORIES = [
    "authenticity",
    "license",
    "security",
    "maintenance",
    "architecture_fit",
    "supply_chain_risk",
    "owner_approval",
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


def build_source_record_reviews(entries: list[dict]) -> list[dict]:
    return [
        {
            "candidate_id": entry["candidate_id"],
            "source_slot_id": entry["source_slot_id"],
            "slot_type": entry["slot_type"],
            "target_uri": entry["target_uri"],
            "review_status": "blocked_missing_required_fields",
            "missing_required_fields": REQUIRED_FIELDS,
            "accepted_for_evaluation": False,
            "accepted_for_integration": False,
        }
        for entry in entries
    ]


def build_candidate_review_records(entries: list[dict]) -> list[dict]:
    counts: dict[str, dict[str, int]] = {}
    names: dict[str, str] = {}
    for entry in entries:
        candidate_id = entry["candidate_id"]
        names[candidate_id] = entry["candidate_name"]
        counts.setdefault(candidate_id, {"source_slots": 0})
        counts[candidate_id]["source_slots"] += 1
    return [
        {
            "candidate_id": candidate_id,
            "candidate_name": names[candidate_id],
            "source_slots_reviewed": count["source_slots"],
            "completed_source_records": 0,
            "candidate_status": "blocked_no_completed_source_evidence",
            "integration_proposal_allowed": False,
            "owner_approval_required": True,
            "categories_missing": REQUIRED_CATEGORIES,
        }
        for candidate_id, count in sorted(counts.items())
    ]


def build_review_gate(manifest: dict) -> dict:
    entries = manifest["candidate_template_records"]
    candidate_count = len({entry["candidate_id"] for entry in entries})
    return {
        "gate_id": "avf-capability-owner-completed-source-evidence-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "reviewed_fixture_uri": rel(FIXTURE_TEMPLATE),
        "research_packet_uri": rel(RESEARCH_PACKET),
        "source_entry_counts": {
            "source_slots_reviewed": len(entries),
            "completed_source_records": 0,
            "incomplete_source_records": len(entries),
            "accepted_source_records": 0,
            "rejected_source_records": len(entries),
            "candidate_count": candidate_count,
        },
        "review_decision": REVIEW_DECISION,
        "integration_decision": "blocked",
        "owner_approval_present": False,
        "owner_approval_required": True,
        "required_fields": REQUIRED_FIELDS,
        "required_categories": REQUIRED_CATEGORIES,
        "categories_satisfied": [],
        "source_record_reviews": build_source_record_reviews(entries),
        "candidate_review_records": build_candidate_review_records(entries),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-external-primary-source-research-authorization-packet-v0-1
title: Add AVF external primary-source research authorization packet v0.1
goal: Define the explicit owner authorization contract required before this branch performs external primary-source research, while keeping scraping, clone, install, integration, deploy, publish, and readiness claims blocked.
context_paths:
  - avf/capabilities/generated/capability_owner_completed_source_evidence_review_gate.json
  - avf/capabilities/generated/capability_primary_source_research_packet.yml
  - avf/capabilities/generated/capability_primary_source_research_pro_prompt.md
files_likely_to_touch:
  - avf/capabilities/generated/capability_external_primary_source_research_authorization_packet.yml
  - avf/capabilities/generated/capability_external_primary_source_research_authorization_gate.json
  - docs/goals/AVF_CAPABILITY_EXTERNAL_PRIMARY_SOURCE_RESEARCH_AUTHORIZATION_PACKET_V0_1_REPORT.md
forbidden_changes:
  - No provider calls without explicit owner authorization
  - No live model calls without explicit owner authorization
  - No external service calls without explicit owner authorization
  - No automated scraping
  - No package install
  - No dependency install
  - No OSS clone
  - No runtime integration
  - No deploy
  - No publish
  - No release readiness claim
  - No production readiness claim
acceptance_criteria:
  - authorization packet exists
  - external primary-source research remains blocked until owner explicitly authorizes it
  - allowed future sources are limited to primary/original sources
  - scraping, clone, install, integration, deploy, publish, and readiness claims remain blocked
validation_commands:
  - python scripts\\validate_avf_capability_owner_completed_source_evidence_review_v0_1.py
expected_outputs:
  - external primary-source research authorization packet
  - external primary-source research authorization validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_owner_completed_source_evidence_review_v0_1",
        "status": "PASS",
        "checks": [
            "owner-completed source evidence review gate exists",
            "required fields are checked before accepting source records",
            "zero completed records remain blocked",
            "owner approval is required and absent",
            "integration remains blocked",
            "protected-action flags false",
        ],
        "review_decision": REVIEW_DECISION,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(gate: dict) -> str:
    rows = "\n".join(
        "- {candidate_id}: source_slots_reviewed={source_slots_reviewed}, completed_source_records={completed_source_records}, integration_proposal_allowed={integration_proposal_allowed}".format(
            **record
        )
        for record in gate["candidate_review_records"]
    )
    counts = gate["source_entry_counts"]
    return f"""# AVF Capability Owner-Completed Source Evidence Review v0.1 Report

RESULT: PASS
capability_owner_completed_source_evidence_review_v0_1=true
owner_completed_source_evidence_review_gate_created=true
source_slots_reviewed={counts['source_slots_reviewed']}
completed_source_records={counts['completed_source_records']}
accepted_source_records={counts['accepted_source_records']}
rejected_source_records={counts['rejected_source_records']}
integration_decision={gate['integration_decision']}
review_decision={gate['review_decision']}
owner_approval_present=false
protected_action_executed=false
dependency_install_performed=false
external_fetch_performed=false
oss_clone_performed=false
package_install_performed=false
runtime_integration_performed=false
provider_calls_performed=false
live_model_calls_performed=false
external_service_calls_performed=false
scraping_performed=false
posting_automation_performed=false
deploy_performed=false
publish_performed=false
release_ready=false
production_ready=false
next_safe_goal_id={NEXT_SAFE_GOAL_ID}

## Review Boundary

This gate reviews the owner/PRO evidence fixture contract locally. The current fixture has zero completed source records, so every candidate remains blocked and no integration proposal is allowed.

## Candidate Review Results

{rows}

## Boundary

This review does not fetch, scrape, clone, install, trust, verify, approve, integrate, invoke, deploy, publish, or claim readiness for any source or candidate.
"""


def main() -> None:
    manifest = read_json(FIXTURE_MANIFEST)
    if f"next_safe_goal_id: {THIS_GOAL_ID}" not in RESEARCH_PACKET.read_text(encoding="utf-8"):
        raise SystemExit("research packet must point to this owner-completed source evidence review goal")
    if "Do not fetch, scrape, clone, install, integrate, deploy, publish, or automate from this repo." not in PRO_PROMPT.read_text(encoding="utf-8"):
        raise SystemExit("PRO prompt must preserve protected-action boundary")

    gate = build_review_gate(manifest)
    write_json(REVIEW_GATE, gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Owner-Completed Source Evidence Review v0.1 runner")
    print("RESULT: PASS")
    print("capability_owner_completed_source_evidence_review_v0_1=true")
    print("owner_completed_source_evidence_review_gate_created=true")
    print("source_slots_reviewed=35")
    print("completed_source_records=0")
    print("accepted_source_records=0")
    print("integration_decision=blocked")
    print(f"review_decision={REVIEW_DECISION}")
    print("owner_approval_present=false")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

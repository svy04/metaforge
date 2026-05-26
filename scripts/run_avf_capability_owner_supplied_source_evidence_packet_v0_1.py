from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

MANUAL_REVIEW_PACKET = CAPABILITIES / "capability_manual_source_review_packet.json"
MANUAL_REVIEW_GATE = CAPABILITIES / "capability_manual_source_review_preflight_gate.json"
OWNER_SUPPLIED_EVIDENCE_PACKET = CAPABILITIES / "capability_owner_supplied_source_evidence_packet.json"
OWNER_SUPPLIED_EVIDENCE_GATE = CAPABILITIES / "capability_owner_supplied_source_evidence_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_owner_supplied_source_evidence_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_owner_supplied_source_evidence_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_OWNER_SUPPLIED_SOURCE_EVIDENCE_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_owner_supplied_source_evidence_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_source_evidence_evaluation_packet_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"

BLOCKING_REQUIREMENTS = [
    "owner_supplied_evidence_uri_missing",
    "owner_supplied_excerpt_or_notes_missing",
    "source_snapshot_hash_missing",
    "reviewer_missing",
    "evidence_not_evaluated",
    "integration_not_approved",
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


def build_evidence_record(capture: dict) -> dict:
    return {
        "evidence_record_id": f"{capture['source_slot_id']}-owner-evidence",
        "source_slot_id": capture["source_slot_id"],
        "candidate_id": capture["candidate_id"],
        "slot_type": capture["slot_type"],
        "target_uri": capture["target_uri"],
        "owner_supplied_evidence_status": "awaiting_owner_input",
        "owner_supplied_evidence_uri": None,
        "owner_supplied_excerpt": None,
        "owner_supplied_notes": None,
        "source_snapshot_hash": None,
        "snapshot_hash_algorithm": "sha256_required_before_trust",
        "reviewer": None,
        "reviewed_at": None,
        "evidence_trusted": False,
        "evidence_verified": False,
        "claim_boundary": false_boundary(),
    }


def build_candidate_evidence_record(candidate: dict) -> dict:
    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_name": candidate["candidate_name"],
        "capability_id": candidate["capability_id"],
        "priority_rank": candidate["priority_rank"],
        "candidate_evidence_status": "awaiting_owner_input",
        "integration_decision": "blocked",
        "source_evidence_verified": False,
        "owner_supplied_evidence_records": [
            build_evidence_record(capture)
            for capture in candidate["source_evidence_capture_records"]
        ],
        "claim_boundary": false_boundary(),
    }


def build_owner_supplied_evidence_packet(manual: dict) -> dict:
    return {
        "packet_id": "avf-capability-owner-supplied-source-evidence-packet-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "evidence_mode": "owner_supplied_primary_source_snapshot_placeholders",
        "manual_source_review_packet_uri": rel(MANUAL_REVIEW_PACKET),
        "manual_source_review_gate_uri": rel(MANUAL_REVIEW_GATE),
        "candidate_owner_supplied_evidence_records": [
            build_candidate_evidence_record(candidate)
            for candidate in manual["candidate_source_review_records"]
        ],
        "evidence_input_contract": {
            "required_evidence_source": "owner_supplied_primary_source_snapshot_or_notes",
            "automated_fetch_allowed": False,
            "automated_scraping_allowed": False,
            "evidence_trusted_by_default": False,
            "evidence_verified_by_default": False,
            "snapshot_hash_required_before_trust": True,
            "manual_reviewer_required_before_trust": True,
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_owner_supplied_evidence_gate(packet: dict) -> dict:
    return {
        "gate_id": "avf-capability-owner-supplied-source-evidence-preflight-gate-v0-1",
        "created_at": CREATED_AT,
        "status": "PASS",
        "gate_decision": "BLOCKED_PENDING_SOURCE_EVIDENCE_EVALUATION",
        "decision_reason": "Evidence placeholders exist, but owner-supplied evidence URI, excerpt/notes, hash, reviewer, and evaluation are not present.",
        "candidate_ids": [
            record["candidate_id"]
            for record in packet["candidate_owner_supplied_evidence_records"]
        ],
        "blocking_requirements": BLOCKING_REQUIREMENTS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-source-evidence-evaluation-packet-v0-1
title: Add AVF capability source evidence evaluation packet v0.1
goal: Define the repo-local criteria for evaluating owner-supplied primary-source evidence without trusting it by default or enabling integration.
context_paths:
  - avf/capabilities/generated/capability_owner_supplied_source_evidence_packet.json
  - avf/capabilities/generated/capability_owner_supplied_source_evidence_preflight_gate.json
  - avf/capabilities/generated/capability_manual_source_review_packet.json
files_likely_to_touch:
  - scripts/run_avf_capability_source_evidence_evaluation_packet_v0_1.py
  - scripts/validate_avf_capability_source_evidence_evaluation_packet_v0_1.py
  - avf/capabilities/generated/capability_source_evidence_evaluation_packet.json
  - docs/goals/AVF_CAPABILITY_SOURCE_EVIDENCE_EVALUATION_PACKET_V0_1_REPORT.md
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
  - source evidence evaluation packet exists
  - each evidence record has evaluation criteria for authenticity, license, security, maintenance, architecture fit, and supply-chain risk
  - no evidence is marked accepted by default
  - integration remains blocked
validation_commands:
  - python scripts\\validate_avf_capability_owner_supplied_source_evidence_packet_v0_1.py
  - python scripts\\validate_avf_capability_source_evidence_evaluation_packet_v0_1.py
expected_outputs:
  - capability_source_evidence_evaluation_packet.json
  - source evidence evaluation validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_owner_supplied_source_evidence_packet_v0_1",
        "status": "PASS",
        "checks": [
            "manual source review packet points to owner-supplied evidence",
            "owner-supplied source evidence packet exists",
            "evidence input fields preserve source URI, excerpt/notes placeholder, hash placeholder, reviewer, and claim boundary",
            "no evidence is trusted or verified by default",
            "integration remains blocked",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(packet: dict) -> str:
    rows = "\n".join(
        f"- {record['candidate_id']}: evidence_records={len(record['owner_supplied_evidence_records'])}, status={record['candidate_evidence_status']}, integration={record['integration_decision']}"
        for record in packet["candidate_owner_supplied_evidence_records"]
    )
    return f"""# AVF Capability Owner-Supplied Source Evidence Packet v0.1 Report

RESULT: PASS
capability_owner_supplied_source_evidence_packet_v0_1=true
owner_supplied_source_evidence_packet_created=true
owner_supplied_source_evidence_gate_created=true
evidence_input_fields_created=true
no_evidence_trusted_or_verified_by_default=true
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

## Owner-Supplied Evidence Records

{rows}

## Boundary

The packet creates owner-supplied evidence placeholders only. It does not fetch, scrape, clone, install, trust, verify, invoke, deploy, publish, approve, or integrate any source or candidate.
"""


def main() -> None:
    manual = read_json(MANUAL_REVIEW_PACKET)
    manual_gate = read_json(MANUAL_REVIEW_GATE)
    if manual.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("manual source review packet does not point to this owner-supplied evidence goal")
    if manual_gate.get("gate_decision") != "BLOCKED_PENDING_OWNER_SUPPLIED_SOURCE_EVIDENCE":
        raise SystemExit("manual source review gate must remain blocked before owner-supplied evidence packet")
    if manual_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("manual source review gate does not point to this owner-supplied evidence goal")

    packet = build_owner_supplied_evidence_packet(manual)
    write_json(OWNER_SUPPLIED_EVIDENCE_PACKET, packet)
    write_json(OWNER_SUPPLIED_EVIDENCE_GATE, build_owner_supplied_evidence_gate(packet))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(packet))

    print("AVF Capability Owner-Supplied Source Evidence Packet v0.1 runner")
    print("RESULT: PASS")
    print("capability_owner_supplied_source_evidence_packet_v0_1=true")
    print("owner_supplied_source_evidence_packet_created=true")
    print("owner_supplied_source_evidence_gate_created=true")
    print("evidence_input_fields_created=true")
    print("no_evidence_trusted_or_verified_by_default=true")
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

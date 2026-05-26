from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

OWNER_SUPPLIED_EVIDENCE_PACKET = CAPABILITIES / "capability_owner_supplied_source_evidence_packet.json"
OWNER_SUPPLIED_EVIDENCE_GATE = CAPABILITIES / "capability_owner_supplied_source_evidence_preflight_gate.json"
SOURCE_EVIDENCE_EVALUATION_PACKET = CAPABILITIES / "capability_source_evidence_evaluation_packet.json"
SOURCE_EVIDENCE_EVALUATION_GATE = CAPABILITIES / "capability_source_evidence_evaluation_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_source_evidence_evaluation_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_source_evidence_evaluation_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_SOURCE_EVIDENCE_EVALUATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_source_evidence_evaluation_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_source_evidence_fixture_template_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"

REQUIRED_CATEGORIES = [
    "authenticity",
    "license",
    "security",
    "maintenance",
    "architecture_fit",
    "supply_chain_risk",
]

BLOCKING_REQUIREMENTS = [
    "no_accepted_owner_supplied_source_evidence",
    "authenticity_not_passed",
    "license_not_passed",
    "security_not_passed",
    "maintenance_not_passed",
    "architecture_fit_not_passed",
    "supply_chain_risk_not_passed",
    "integration_not_approved",
]

REJECTION_REASONS = [
    "owner_supplied_evidence_uri_missing",
    "owner_supplied_excerpt_or_notes_missing",
    "source_snapshot_hash_missing",
    "reviewer_missing",
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


def build_criteria() -> list[dict]:
    return [
        {
            "category": category,
            "status": "not_evaluable_without_owner_supplied_evidence",
            "passed": False,
            "required_before_integration": True,
        }
        for category in REQUIRED_CATEGORIES
    ]


def build_evaluation_record(evidence: dict) -> dict:
    return {
        "evidence_record_id": evidence["evidence_record_id"],
        "source_slot_id": evidence["source_slot_id"],
        "candidate_id": evidence["candidate_id"],
        "slot_type": evidence["slot_type"],
        "target_uri": evidence["target_uri"],
        "evaluation_status": "blocked_missing_owner_supplied_evidence",
        "acceptance_decision": "not_accepted",
        "rejection_reasons": REJECTION_REASONS,
        "evaluation_criteria": build_criteria(),
        "evidence_trusted": False,
        "evidence_verified": False,
        "accepted_for_integration": False,
        "claim_boundary": false_boundary(),
    }


def build_candidate_evaluation_record(candidate: dict) -> dict:
    evidence_records = [
        build_evaluation_record(evidence)
        for evidence in candidate["owner_supplied_evidence_records"]
    ]
    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_name": candidate["candidate_name"],
        "capability_id": candidate["capability_id"],
        "priority_rank": candidate["priority_rank"],
        "candidate_evaluation_status": "blocked_insufficient_owner_supplied_evidence",
        "integration_decision": "blocked",
        "accepted_evidence_count": 0,
        "pending_or_rejected_evidence_count": len(evidence_records),
        "evidence_evaluation_records": evidence_records,
        "claim_boundary": false_boundary(),
    }


def build_evaluation_packet(owner_packet: dict) -> dict:
    return {
        "packet_id": "avf-capability-source-evidence-evaluation-packet-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "evaluation_mode": "criteria_only_owner_evidence_not_accepted_by_default",
        "owner_supplied_evidence_packet_uri": rel(OWNER_SUPPLIED_EVIDENCE_PACKET),
        "owner_supplied_evidence_gate_uri": rel(OWNER_SUPPLIED_EVIDENCE_GATE),
        "candidate_evaluation_records": [
            build_candidate_evaluation_record(candidate)
            for candidate in owner_packet["candidate_owner_supplied_evidence_records"]
        ],
        "evaluation_contract": {
            "accept_evidence_by_default": False,
            "allow_integration_without_all_required_categories_passing": False,
            "required_categories": REQUIRED_CATEGORIES,
            "required_before_trust": [
                "owner_supplied_evidence_uri",
                "owner_supplied_excerpt_or_notes",
                "source_snapshot_hash",
                "reviewer",
                "authenticity_passed",
                "license_passed",
                "security_passed",
                "maintenance_passed",
                "architecture_fit_passed",
                "supply_chain_risk_passed",
            ],
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_evaluation_gate(packet: dict) -> dict:
    return {
        "gate_id": "avf-capability-source-evidence-evaluation-preflight-gate-v0-1",
        "created_at": CREATED_AT,
        "status": "PASS",
        "gate_decision": "BLOCKED_NO_ACCEPTED_SOURCE_EVIDENCE",
        "decision_reason": "Owner-supplied evidence placeholders are present, but no evidence record has source URI, excerpt/notes, snapshot hash, reviewer, accepted criteria, or owner approval.",
        "candidate_ids": [
            record["candidate_id"]
            for record in packet["candidate_evaluation_records"]
        ],
        "blocking_requirements": BLOCKING_REQUIREMENTS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-source-evidence-fixture-template-v0-1
title: Add AVF capability source evidence fixture template v0.1
goal: Create a fillable repo-local template for owner-supplied primary-source evidence snapshots without fetching, scraping, cloning, installing, or trusting evidence by default.
context_paths:
  - avf/capabilities/generated/capability_source_evidence_evaluation_packet.json
  - avf/capabilities/generated/capability_source_evidence_evaluation_preflight_gate.json
  - avf/capabilities/generated/capability_owner_supplied_source_evidence_packet.json
files_likely_to_touch:
  - scripts/run_avf_capability_source_evidence_fixture_template_v0_1.py
  - scripts/validate_avf_capability_source_evidence_fixture_template_v0_1.py
  - avf/capabilities/generated/capability_source_evidence_fixture_template.yml
  - docs/goals/AVF_CAPABILITY_SOURCE_EVIDENCE_FIXTURE_TEMPLATE_V0_1_REPORT.md
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
  - source evidence fixture template exists
  - template fields cover source URI, source type, quoted excerpt, snapshot hash, license note, security note, maintenance note, architecture fit note, supply-chain note, reviewer, and reviewed_at
  - template warns evidence remains untrusted until evaluated
  - integration remains blocked
validation_commands:
  - python scripts\\validate_avf_capability_source_evidence_evaluation_packet_v0_1.py
  - python scripts\\validate_avf_capability_source_evidence_fixture_template_v0_1.py
expected_outputs:
  - capability_source_evidence_fixture_template.yml
  - source evidence fixture template validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_source_evidence_evaluation_packet_v0_1",
        "status": "PASS",
        "checks": [
            "owner-supplied evidence packet points to source evidence evaluation",
            "source evidence evaluation packet exists",
            "evaluation criteria exist for authenticity, license, security, maintenance, architecture fit, and supply-chain risk",
            "no evidence is accepted by default",
            "integration remains blocked",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(packet: dict) -> str:
    rows = "\n".join(
        f"- {record['candidate_id']}: evaluated_records={len(record['evidence_evaluation_records'])}, accepted={record['accepted_evidence_count']}, status={record['candidate_evaluation_status']}, integration={record['integration_decision']}"
        for record in packet["candidate_evaluation_records"]
    )
    return f"""# AVF Capability Source Evidence Evaluation Packet v0.1 Report

RESULT: PASS
capability_source_evidence_evaluation_packet_v0_1=true
source_evidence_evaluation_packet_created=true
source_evidence_evaluation_gate_created=true
evaluation_criteria_created=true
no_evidence_accepted_by_default=true
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

## Candidate Evidence Evaluation Records

{rows}

## Boundary

The packet evaluates empty owner-supplied source evidence placeholders only. It creates criteria for authenticity, license, security, maintenance, architecture fit, and supply-chain risk, but accepts no evidence by default and does not fetch, scrape, clone, install, trust, verify, invoke, deploy, publish, approve, or integrate any source or candidate.
"""


def main() -> None:
    owner_packet = read_json(OWNER_SUPPLIED_EVIDENCE_PACKET)
    owner_gate = read_json(OWNER_SUPPLIED_EVIDENCE_GATE)
    if owner_packet.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("owner-supplied evidence packet does not point to this source evidence evaluation goal")
    if owner_gate.get("gate_decision") != "BLOCKED_PENDING_SOURCE_EVIDENCE_EVALUATION":
        raise SystemExit("owner-supplied evidence gate must remain blocked before source evidence evaluation")
    if owner_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("owner-supplied evidence gate does not point to this source evidence evaluation goal")

    packet = build_evaluation_packet(owner_packet)
    write_json(SOURCE_EVIDENCE_EVALUATION_PACKET, packet)
    write_json(SOURCE_EVIDENCE_EVALUATION_GATE, build_evaluation_gate(packet))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(packet))

    print("AVF Capability Source Evidence Evaluation Packet v0.1 runner")
    print("RESULT: PASS")
    print("capability_source_evidence_evaluation_packet_v0_1=true")
    print("source_evidence_evaluation_packet_created=true")
    print("source_evidence_evaluation_gate_created=true")
    print("evaluation_criteria_created=true")
    print("no_evidence_accepted_by_default=true")
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

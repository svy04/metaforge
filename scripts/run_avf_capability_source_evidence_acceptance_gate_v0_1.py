from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

FIXTURE_MANIFEST = CAPABILITIES / "capability_source_evidence_fixture_template_manifest.json"
INGESTION_RULES = CAPABILITIES / "capability_source_evidence_ingestion_rules.json"
INGESTION_DRY_RUN = CAPABILITIES / "capability_source_evidence_ingestion_dry_run_result.json"
ACCEPTANCE_GATE = CAPABILITIES / "capability_source_evidence_acceptance_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_source_evidence_acceptance_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_source_evidence_acceptance_gate_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_SOURCE_EVIDENCE_ACCEPTANCE_GATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_source_evidence_acceptance_gate_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_source_evidence_ingestion_validator_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_research_packet_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
GATE_DECISION = "BLOCKED_NO_ACCEPTED_INGESTED_SOURCE_EVIDENCE"

REQUIRED_EVIDENCE_CATEGORIES = [
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


def count_by_candidate(dry_run: dict) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for result in dry_run.get("candidate_ingestion_results", []):
        candidate_id = result["candidate_id"]
        if candidate_id not in counts:
            counts[candidate_id] = {"accepted": 0, "rejected": 0}
        if result.get("accepted_for_evaluation") is True:
            counts[candidate_id]["accepted"] += 1
        else:
            counts[candidate_id]["rejected"] += 1
    return counts


def build_candidate_records(dry_run: dict) -> list[dict]:
    records = []
    for candidate_id, counts in sorted(count_by_candidate(dry_run).items()):
        records.append(
            {
                "candidate_id": candidate_id,
                "accepted_source_entries": counts["accepted"],
                "rejected_source_entries": counts["rejected"],
                "acceptance_status": "blocked_no_accepted_ingested_source_evidence",
                "integration_proposal_allowed": False,
                "owner_approval_required": True,
                "required_evidence_categories_missing": REQUIRED_EVIDENCE_CATEGORIES,
            }
        )
    return records


def build_acceptance_gate(manifest: dict, dry_run: dict) -> dict:
    manifest_entries = manifest["candidate_template_records"]
    candidate_ids = {entry["candidate_id"] for entry in manifest_entries}
    return {
        "gate_id": "avf-capability-source-evidence-acceptance-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "input_uris": {
            "fixture_manifest": rel(FIXTURE_MANIFEST),
            "ingestion_rules": rel(INGESTION_RULES),
            "ingestion_dry_run": rel(INGESTION_DRY_RUN),
        },
        "source_entry_counts": {
            "template_entries_checked": len(manifest_entries),
            "candidate_count": len(candidate_ids),
            "accepted_entries": dry_run["accepted_entries"],
            "rejected_entries": dry_run["rejected_entries"],
        },
        "gate_decision": GATE_DECISION,
        "integration_decision": "blocked",
        "owner_approval_required": True,
        "required_evidence_categories_before_integration_proposal": REQUIRED_EVIDENCE_CATEGORIES,
        "categories_passed": [],
        "candidate_acceptance_records": build_candidate_records(dry_run),
        "future_integration_prerequisites": [
            "authenticity: owner-supplied source URI, source type, quoted excerpt, and sha256 snapshot hash must be present",
            "license: owner-supplied license note must be present and reviewed",
            "security: owner-supplied security note must be present and reviewed",
            "maintenance: owner-supplied maintenance note must be present and reviewed",
            "architecture_fit: owner-supplied architecture fit note must be present and reviewed",
            "supply_chain_risk: owner-supplied supply-chain note must be present and reviewed",
            "owner_approval: explicit owner approval is required before any future integration proposal",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-research-packet-v0-1
title: Add AVF capability primary-source research packet v0.1
goal: Create a repo-local PRO/owner research packet for manually collecting primary-source evidence before any future capability integration proposal.
context_paths:
  - avf/capabilities/generated/capability_source_evidence_acceptance_gate.json
  - avf/capabilities/generated/capability_source_evidence_fixture_template.yml
  - avf/capabilities/generated/capability_source_evidence_fixture_template_manifest.json
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_research_packet.yml
  - avf/capabilities/generated/capability_primary_source_research_packet.validation_result.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_RESEARCH_PACKET_V0_1_REPORT.md
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
  - primary-source research packet exists
  - packet instructs PRO/owner to collect only official docs, repositories, license files, security advisories, maintenance signals, architecture specs, and supply-chain standards
  - packet requires source URI, source type, verbatim excerpt, sha256 snapshot hash, license/security/maintenance/architecture/supply-chain notes, reviewer, and reviewed_at
  - packet does not fetch, scrape, clone, install, integrate, deploy, publish, or claim readiness
validation_commands:
  - python scripts\\validate_avf_capability_source_evidence_acceptance_gate_v0_1.py
expected_outputs:
  - capability_primary_source_research_packet.yml
  - primary-source research packet validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(gate: dict) -> dict:
    return {
        "validator_id": "validate_avf_capability_source_evidence_acceptance_gate_v0_1",
        "status": "PASS",
        "checks": [
            "acceptance gate exists",
            "accepted entries remain zero",
            "integration remains blocked",
            "owner approval required",
            "all evidence categories required before integration proposal",
            "protected-action flags false",
        ],
        "gate_decision": gate["gate_decision"],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(gate: dict) -> str:
    rows = "\n".join(
        "- {candidate_id}: accepted_source_entries={accepted_source_entries}, rejected_source_entries={rejected_source_entries}, integration_proposal_allowed={integration_proposal_allowed}".format(
            **record
        )
        for record in gate["candidate_acceptance_records"]
    )
    return f"""# AVF Capability Source Evidence Acceptance Gate v0.1 Report

RESULT: PASS
capability_source_evidence_acceptance_gate_v0_1=true
acceptance_gate_created=true
accepted_entries={gate['source_entry_counts']['accepted_entries']}
rejected_entries={gate['source_entry_counts']['rejected_entries']}
candidate_count={gate['source_entry_counts']['candidate_count']}
integration_decision={gate['integration_decision']}
gate_decision={gate['gate_decision']}
owner_approval_required=true
all_evidence_categories_required=true
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

## Acceptance Boundary

The acceptance gate blocks future integration proposals because the ingestion dry run has zero accepted source evidence entries. A candidate can only move toward a future integration proposal after all required evidence categories are present and explicit owner approval is recorded.

## Candidate Gate Results

{rows}

## Required Categories Before Future Integration Proposal

- authenticity
- license
- security
- maintenance
- architecture_fit
- supply_chain_risk
- owner_approval

## Boundary

This gate does not fetch, scrape, clone, install, trust, verify, approve, integrate, invoke, deploy, publish, or claim readiness for any source or candidate.
"""


def main() -> None:
    manifest = read_json(FIXTURE_MANIFEST)
    ingestion_rules = read_json(INGESTION_RULES)
    dry_run = read_json(INGESTION_DRY_RUN)

    if manifest.get("next_safe_goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("fixture manifest must point to ingestion validator")
    if ingestion_rules.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("ingestion rules must point to acceptance gate")
    if dry_run.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("ingestion dry run must point to acceptance gate")
    if dry_run.get("accepted_entries") != 0:
        raise SystemExit("acceptance gate requires zero accepted entries for this blocked dry run")
    if dry_run.get("integration_decision") != "blocked":
        raise SystemExit("ingestion dry run must keep integration blocked")

    gate = build_acceptance_gate(manifest, dry_run)
    write_json(ACCEPTANCE_GATE, gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Source Evidence Acceptance Gate v0.1 runner")
    print("RESULT: PASS")
    print("capability_source_evidence_acceptance_gate_v0_1=true")
    print("acceptance_gate_created=true")
    print("accepted_entries=0")
    print("integration_decision=blocked")
    print(f"gate_decision={GATE_DECISION}")
    print("owner_approval_required=true")
    print("all_evidence_categories_required=true")
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

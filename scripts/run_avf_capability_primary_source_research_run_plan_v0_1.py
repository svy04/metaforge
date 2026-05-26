from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

AUTHORIZATION_GATE = CAPABILITIES / "capability_external_primary_source_research_authorization_gate.json"
RESEARCH_PACKET = CAPABILITIES / "capability_primary_source_research_packet.yml"
RUN_PLAN = CAPABILITIES / "capability_primary_source_research_run_plan.yml"
RUN_PLAN_GATE = CAPABILITIES / "capability_primary_source_research_run_plan_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_research_run_plan_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_research_run_plan_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_RESEARCH_RUN_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_research_run_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_external_primary_source_research_authorization_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_capture_workspace_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
RUN_PLAN_DECISION = "PLAN_READY_EXECUTION_BLOCKED_PENDING_OWNER_AUTHORIZATION"

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

CANDIDATES = [
    "candidate-opentelemetry",
    "candidate-litellm-proxy",
    "candidate-temporal-workflow",
    "candidate-langgraph-runtime",
    "candidate-mcp-tool-registry",
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


def require_authorization_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("authorization gate previous goal mismatch")
    if gate.get("status") != "PASS":
        raise SystemExit("authorization gate must be PASS")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("authorization gate must point to this run plan goal")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("owner authorization must remain false")
    if gate.get("external_research_allowed") is not False:
        raise SystemExit("external research allowance must remain false")
    if gate.get("automated_collection_allowed") is not False:
        raise SystemExit("automated collection allowance must remain false")
    if gate.get("allowed_future_source_families_after_authorization") != PRIMARY_SOURCE_FAMILIES:
        raise SystemExit("source family boundary mismatch")


def source_slot_count() -> int:
    return RESEARCH_PACKET.read_text(encoding="utf-8").count("source_slot_id:")


def build_run_plan(slot_count: int) -> str:
    source_family_rows = "\n".join(f"  - {family}" for family in PRIMARY_SOURCE_FAMILIES)
    candidate_rows = "\n".join(
        f"  - candidate_id: {candidate}\n"
        "    collection_status: planned_not_executed\n"
        "    evidence_capture_required: true\n"
        "    integration_allowed_from_plan: false"
        for candidate in CANDIDATES
    )
    return f"""packet_id: avf-capability-primary-source-research-run-plan-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
source_collection_mode: planned_owner_or_pro_manual_only
owner_authorization_required: true
owner_authorization_granted: false
research_execution_allowed: false
external_primary_source_research_executed: false
target_source_slots_planned: {slot_count}
run_plan_decision: {RUN_PLAN_DECISION}

source_families:
{source_family_rows}

candidate_prioritization:
{candidate_rows}

manual_evidence_capture_steps:
  - step_id: record_source_uri
    result_required: source URI copied into the evidence workspace by owner or PRO after explicit authorization.
  - step_id: record_source_type
    result_required: source type selected from bounded primary/original source families.
  - step_id: record_short_verbatim_excerpt
    result_required: short excerpt captured for review without copying full documents.
  - step_id: compute_sha256_snapshot_hash
    result_required: sha256 snapshot hash recorded for the reviewed source material.
  - step_id: record_license_note
    result_required: license compatibility note captured before any build/buy/adopt decision.
  - step_id: record_security_note
    result_required: security advisory or security posture note captured before any integration proposal.
  - step_id: record_maintenance_note
    result_required: maintenance signal note captured before any integration proposal.
  - step_id: record_architecture_fit_note
    result_required: architecture fit note captured against AVF control-plane, runtime, data, model/tool, observability, and studio planes.
  - step_id: record_supply_chain_note
    result_required: supply-chain note captured before any dependency or runtime decision.
  - step_id: mark_untrusted_until_ingestion_gate
    result_required: every source remains untrusted until the ingestion and acceptance gates pass.

blocked_execution_rules:
  - no_fetch_no_scrape_no_clone_no_install_no_integration
  - no_provider_calls
  - no_live_model_calls
  - no_external_service_calls
  - no_deploy
  - no_publish
  - no_release_readiness_claim
  - no_production_readiness_claim

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


def build_run_plan_gate(slot_count: int) -> dict:
    return {
        "gate_id": "avf-capability-primary-source-research-run-plan-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "run_plan_decision": RUN_PLAN_DECISION,
        "primary_source_families_bounded": True,
        "manual_evidence_capture_steps_created": True,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "research_execution_allowed": False,
        "external_primary_source_research_executed": False,
        "target_source_slots_planned": slot_count,
        "source_families": PRIMARY_SOURCE_FAMILIES,
        "run_plan_uri": rel(RUN_PLAN),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-evidence-capture-workspace-v0-1
title: Add AVF primary-source evidence capture workspace v0.1
goal: Create a repo-local workspace for owner/PRO captured primary-source evidence records without executing external research, automated scraping, OSS clone, install, runtime integration, deploy, publish, or readiness claims.
context_paths:
  - avf/capabilities/generated/capability_primary_source_research_run_plan.yml
  - avf/capabilities/generated/capability_primary_source_research_run_plan_gate.json
  - avf/capabilities/generated/capability_source_evidence_fixture_template.yml
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_capture_workspace.yml
  - avf/capabilities/generated/capability_primary_source_evidence_capture_workspace_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_CAPTURE_WORKSPACE_V0_1_REPORT.md
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
  - evidence capture workspace exists
  - workspace includes required evidence fields for all source families
  - records remain empty and untrusted by default
  - protected actions remain blocked
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_research_run_plan_v0_1.py
expected_outputs:
  - primary-source evidence capture workspace
  - workspace gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(slot_count: int) -> dict:
    return {
        "validator_id": "validate_avf_capability_primary_source_research_run_plan_v0_1",
        "status": "PASS",
        "checks": [
            "run plan exists",
            "primary/original source families remain bounded",
            "manual evidence capture steps are explicit",
            "external research execution remains blocked",
            "protected-action flags remain false",
        ],
        "run_plan_decision": RUN_PLAN_DECISION,
        "target_source_slots_planned": slot_count,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "research_execution_allowed": False,
        "external_primary_source_research_executed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(slot_count: int) -> str:
    families = "\n".join(f"- {family}" for family in PRIMARY_SOURCE_FAMILIES)
    candidates = "\n".join(f"- {candidate}: planned_not_executed" for candidate in CANDIDATES)
    return f"""# AVF Capability Primary-Source Research Run Plan v0.1 Report

RESULT: PASS
capability_primary_source_research_run_plan_v0_1=true
primary_source_research_run_plan_created=true
primary_source_families_bounded=true
manual_evidence_capture_steps_created=true
target_source_slots_planned={slot_count}
owner_authorization_required=true
owner_authorization_granted=false
research_execution_allowed=false
external_primary_source_research_executed=false
run_plan_decision={RUN_PLAN_DECISION}
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

## Run Plan Boundary

This is a repo-local plan only. It prepares manual primary/original source evidence capture after explicit owner authorization, but it does not execute external research.

## Source Families

{families}

## Candidate Plan

{candidates}

## Manual Evidence Capture

Each future evidence record must include source URI, source type, short excerpt, sha256 snapshot hash, license note, security note, maintenance note, architecture fit note, supply-chain note, reviewer, and reviewed_at before any later ingestion or acceptance gate can consider it.
"""


def main() -> None:
    gate = read_json(AUTHORIZATION_GATE)
    require_authorization_gate(gate)
    slot_count = source_slot_count()
    if slot_count != 35:
        raise SystemExit(f"expected 35 source slots, got {slot_count}")

    write_text(RUN_PLAN, build_run_plan(slot_count))
    write_json(RUN_PLAN_GATE, build_run_plan_gate(slot_count))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result(slot_count))
    write_text(VALIDATION_REPORT, build_report(slot_count))

    print("AVF Capability Primary-Source Research Run Plan v0.1 runner")
    print("RESULT: PASS")
    print("capability_primary_source_research_run_plan_v0_1=true")
    print("primary_source_research_run_plan_created=true")
    print("primary_source_families_bounded=true")
    print("manual_evidence_capture_steps_created=true")
    print(f"target_source_slots_planned={slot_count}")
    print("owner_authorization_required=true")
    print("owner_authorization_granted=false")
    print("research_execution_allowed=false")
    print("external_primary_source_research_executed=false")
    print(f"run_plan_decision={RUN_PLAN_DECISION}")
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

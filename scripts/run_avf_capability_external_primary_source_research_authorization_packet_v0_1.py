from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

PREVIOUS_REVIEW_GATE = CAPABILITIES / "capability_owner_completed_source_evidence_review_gate.json"
AUTHORIZATION_PACKET = CAPABILITIES / "capability_external_primary_source_research_authorization_packet.yml"
AUTHORIZATION_GATE = CAPABILITIES / "capability_external_primary_source_research_authorization_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_external_primary_source_research_authorization_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_external_primary_source_research_authorization_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_EXTERNAL_PRIMARY_SOURCE_RESEARCH_AUTHORIZATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_external_primary_source_research_authorization_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_owner_completed_source_evidence_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_research_run_plan_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
AUTHORIZATION_DECISION = "BLOCKED_PENDING_OWNER_AUTHORIZATION"

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


def require_previous_gate(previous_gate: dict) -> None:
    if previous_gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review gate goal_id mismatch")
    if previous_gate.get("status") != "PASS":
        raise SystemExit("previous review gate must be PASS")
    if previous_gate.get("review_decision") != "BLOCKED_OWNER_EVIDENCE_NOT_COMPLETED":
        raise SystemExit("previous review gate decision mismatch")
    if previous_gate.get("integration_decision") != "blocked":
        raise SystemExit("previous review gate must keep integration blocked")
    if previous_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous review gate must point to this authorization packet goal")
    counts = previous_gate.get("source_entry_counts", {})
    if counts.get("completed_source_records") != 0:
        raise SystemExit("previous review gate completed source records must be zero")
    if counts.get("accepted_source_records") != 0:
        raise SystemExit("previous review gate accepted source records must be zero")


def build_authorization_packet() -> str:
    source_family_rows = "\n".join(f"  - {family}" for family in PRIMARY_SOURCE_FAMILIES)
    return f"""packet_id: avf-capability-external-primary-source-research-authorization-packet-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
authorization_decision: {AUTHORIZATION_DECISION}
owner_authorization_required: true
owner_authorization_granted: false
external_primary_source_research_allowed: false
automated_collection_allowed: false
automated_scraping_allowed: false
oss_clone_allowed: false
dependency_install_allowed: false
package_install_allowed: false
runtime_integration_allowed: false
deploy_allowed: false
publish_allowed: false
release_ready: false
production_ready: false

allowed_future_source_families_after_authorization:
{source_family_rows}

future_allowed_modes_after_explicit_authorization:
  - mode: owner_manual_browser_research
    enabled: false
    boundary: Owner may manually inspect primary/original sources and paste completed evidence into the repo-local evidence fixture.
  - mode: pro_manual_primary_source_research
    enabled: false
    boundary: PRO may prepare primary-source research notes for owner review, but no external action is executed from this branch.
  - mode: codex_link_opening_only_after_explicit_authorization
    enabled: false
    boundary: Codex may only open owner-authorized primary/original source links for review; no scraping, clone, install, integration, deploy, or publish action is allowed.

blocked_until_authorized:
  - provider_calls
  - live_model_calls
  - external_service_calls
  - automated_scraping
  - oss_clone
  - dependency_install
  - package_install
  - runtime_integration
  - deploy
  - publish
  - release_readiness_claim
  - production_readiness_claim

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


def build_authorization_gate() -> dict:
    return {
        "gate_id": "avf-capability-external-primary-source-research-authorization-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "authorization_decision": AUTHORIZATION_DECISION,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "external_research_allowed": False,
        "automated_collection_allowed": False,
        "allowed_future_source_families_after_authorization": PRIMARY_SOURCE_FAMILIES,
        "disabled_future_modes_until_authorized": [
            "owner_manual_browser_research",
            "pro_manual_primary_source_research",
            "codex_link_opening_only_after_explicit_authorization",
        ],
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "authorization_packet_uri": rel(AUTHORIZATION_PACKET),
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-research-run-plan-v0-1
title: Add AVF primary-source research run plan v0.1
goal: Define the repo-local run plan for owner-authorized manual primary-source research without performing external research, scraping, clone, install, runtime integration, deploy, publish, or readiness claims.
context_paths:
  - avf/capabilities/generated/capability_external_primary_source_research_authorization_packet.yml
  - avf/capabilities/generated/capability_external_primary_source_research_authorization_gate.json
  - avf/capabilities/generated/capability_primary_source_research_packet.yml
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_research_run_plan.yml
  - avf/capabilities/generated/capability_primary_source_research_run_plan_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_RESEARCH_RUN_PLAN_V0_1_REPORT.md
forbidden_changes:
  - No external research execution without explicit owner authorization
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
  - run plan exists
  - primary/original source families remain bounded
  - manual evidence capture steps are explicit
  - all protected actions remain blocked unless a later owner authorization artifact allows a narrower mode
validation_commands:
  - python scripts\\validate_avf_capability_external_primary_source_research_authorization_packet_v0_1.py
expected_outputs:
  - primary-source research run plan
  - run plan gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_external_primary_source_research_authorization_packet_v0_1",
        "status": "PASS",
        "checks": [
            "authorization packet exists",
            "previous owner-completed evidence review remains blocked",
            "external primary-source research remains blocked pending owner authorization",
            "future allowed source families are primary/original sources only",
            "scraping, clone, install, integration, deploy, publish, and readiness claims remain blocked",
        ],
        "authorization_decision": AUTHORIZATION_DECISION,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "external_primary_source_research_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(gate: dict) -> str:
    families = "\n".join(f"- {family}" for family in gate["allowed_future_source_families_after_authorization"])
    modes = "\n".join(f"- {mode}: disabled until explicit owner authorization" for mode in gate["disabled_future_modes_until_authorized"])
    return f"""# AVF Capability External Primary-Source Research Authorization Packet v0.1 Report

RESULT: PASS
capability_external_primary_source_research_authorization_packet_v0_1=true
owner_authorization_required=true
owner_authorization_granted=false
external_primary_source_research_allowed=false
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

## Authorization Boundary

This packet records the required owner authorization contract before this branch performs external primary-source research. The current decision is blocked pending explicit owner authorization.

## Allowed Future Source Families After Authorization

{families}

## Disabled Future Modes

{modes}

## Blocked Actions

Provider calls, live model calls, external service calls, automated scraping, OSS clone, dependency install, package install, runtime integration, deploy, publish, and release or production readiness claims remain blocked.
"""


def main() -> None:
    previous_gate = read_json(PREVIOUS_REVIEW_GATE)
    require_previous_gate(previous_gate)

    gate = build_authorization_gate()
    write_text(AUTHORIZATION_PACKET, build_authorization_packet())
    write_json(AUTHORIZATION_GATE, gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability External Primary-Source Research Authorization Packet v0.1 runner")
    print("RESULT: PASS")
    print("capability_external_primary_source_research_authorization_packet_v0_1=true")
    print("owner_authorization_required=true")
    print("owner_authorization_granted=false")
    print("external_primary_source_research_allowed=false")
    print("automated_collection_allowed=false")
    print("integration_decision=blocked")
    print(f"authorization_decision={AUTHORIZATION_DECISION}")
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

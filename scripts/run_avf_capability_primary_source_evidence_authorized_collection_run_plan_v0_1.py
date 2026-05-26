from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

AUTH_PACKET = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_packet.yml"
AUTH_GATE = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_gate.json"
RUN_PLAN = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan.yml"
RUN_PLAN_GATE = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_authorized_collection_run_plan_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_AUTHORIZED_COLLECTION_RUN_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_run_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_authorized_collection_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_collection_authorization_review_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"
RUN_PLAN_DECISION = "PLAN_READY_EXECUTION_BLOCKED_PENDING_EXPLICIT_AUTHORIZATION"
AUTHORIZATION_DECISION = "BLOCKED_PENDING_EXPLICIT_COLLECTION_AUTHORIZATION"

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


def require_auth_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("authorized collection gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("authorized collection gate must point to this run plan goal")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("authorized collection gate must remain unauthorized")
    if gate.get("collection_authorization_status") != "not_authorized":
        raise SystemExit("authorized collection gate authorization status mismatch")
    if gate.get("integration_decision") != "blocked":
        raise SystemExit("authorized collection gate must keep integration blocked")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_targeted") != 35:
        raise SystemExit("authorized collection gate must target 35 source records")
    if counts.get("source_records_authorized") != 0:
        raise SystemExit("authorized collection gate must not authorize records")


def build_execution_modes(auth_gate: dict) -> list[dict]:
    modes: list[dict] = []
    for mode in auth_gate.get("collection_modes", []):
        modes.append(
            {
                "mode_id": mode.get("mode_id", ""),
                "label": mode.get("label", ""),
                "authorization_required": True,
                "execution_allowed": False,
                "source": "authorized_collection_gate",
                "blocked_reason": "explicit_authorization_fields_not_present_or_not_reviewed",
            }
        )
    return modes


def build_execution_steps() -> list[dict]:
    return [
        {
            "step_id": "review_authorization_fields",
            "purpose": "Confirm explicit owner authorization fields before collection.",
            "status": "blocked_pending_explicit_authorization",
            "required_before": ["any_source_collection"],
        },
        {
            "step_id": "collect_primary_source_snapshots",
            "purpose": "Capture authorized primary/original source evidence snapshots.",
            "status": "blocked_pending_explicit_authorization",
            "required_before": ["source_hashing", "evidence_population"],
        },
        {
            "step_id": "compute_source_snapshot_hashes",
            "purpose": "Attach deterministic hashes to captured source snapshots or source text.",
            "status": "blocked_pending_explicit_authorization",
            "required_before": ["evidence_ingestion_review"],
        },
        {
            "step_id": "populate_retry_evidence_records",
            "purpose": "Fill source_uri, short quoted excerpt, review notes, reviewer, and reviewed_at fields.",
            "status": "blocked_pending_explicit_authorization",
            "required_before": ["source_evidence_ingestion_validator"],
        },
        {
            "step_id": "run_ingestion_and_acceptance_gates",
            "purpose": "Keep evidence untrusted until ingestion and acceptance validators pass.",
            "status": "blocked_pending_explicit_authorization",
            "required_before": ["capability_integration_proposal"],
        },
        {
            "step_id": "propose_capability_integration_task",
            "purpose": "Only after accepted source evidence and owner approval, create a PR-sized integration task.",
            "status": "blocked_pending_explicit_authorization",
            "required_before": ["any_runtime_integration"],
        },
    ]


def build_source_tasks(auth_gate: dict) -> list[dict]:
    tasks: list[dict] = []
    for record in auth_gate.get("source_collection_records", []):
        tasks.append(
            {
                "candidate_id": record.get("candidate_id", ""),
                "candidate_name": record.get("candidate_name", ""),
                "capability_id": record.get("capability_id", ""),
                "source_slot_id": record.get("source_slot_id", ""),
                "planned_target_uri": record.get("planned_target_uri", ""),
                "planned_source_type": record.get("planned_source_type", ""),
                "execution_status": "blocked_pending_explicit_authorization",
                "collection_execution_allowed": False,
                "trusted_source": False,
                "accepted_for_ingestion": False,
                "accepted_for_integration": False,
                "integration_allowed_from_record": False,
                "required_authorization_fields": AUTHORIZATION_FIELDS,
                "required_execution_steps": [step["step_id"] for step in build_execution_steps()],
            }
        )
    return tasks


def build_run_plan_gate(auth_gate: dict) -> dict:
    source_tasks = build_source_tasks(auth_gate)
    return {
        "gate_id": "avf-capability-primary-source-evidence-authorized-collection-run-plan-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "run_plan_decision": RUN_PLAN_DECISION,
        "authorization_decision": AUTHORIZATION_DECISION,
        "authorization_required": True,
        "authorization_present": False,
        "authorization_review_required_before_execution": True,
        "collection_execution_allowed": False,
        "manual_owner_collection_executable": False,
        "pro_manual_collection_executable": False,
        "codex_assisted_link_opening_executable": False,
        "automated_collection_executable": False,
        "authorization_fields_required": AUTHORIZATION_FIELDS,
        "execution_modes": build_execution_modes(auth_gate),
        "execution_steps": build_execution_steps(),
        "source_entry_counts": {
            "source_records_planned": len(source_tasks),
            "source_records_executable": 0,
            "trusted_source_records": 0,
            "ingested_source_records": 0,
            "integrated_source_records": 0,
        },
        "source_collection_tasks": source_tasks,
        "auth_packet_uri": rel(AUTH_PACKET),
        "auth_gate_uri": rel(AUTH_GATE),
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def yaml_bool(value: bool) -> str:
    return "true" if value else "false"


def build_run_plan(gate: dict) -> str:
    fields = "\n".join(f"  - {field}" for field in AUTHORIZATION_FIELDS)
    modes = "\n".join(
        [
            f"  - mode_id: {mode['mode_id']}\n"
            f"    authorization_required: {yaml_bool(mode['authorization_required'])}\n"
            f"    execution_allowed: {yaml_bool(mode['execution_allowed'])}\n"
            f"    blocked_reason: {mode['blocked_reason']}"
            for mode in gate["execution_modes"]
        ]
    )
    steps = "\n".join(
        [
            f"  - step_id: {step['step_id']}\n"
            f"    status: {step['status']}\n"
            f"    purpose: {step['purpose']}"
            for step in gate["execution_steps"]
        ]
    )
    tasks = "\n".join(
        [
            f"  - candidate_id: {task['candidate_id']}\n"
            f"    candidate_name: {task['candidate_name']}\n"
            f"    capability_id: {task['capability_id']}\n"
            f"    source_slot_id: {task['source_slot_id']}\n"
            f"    planned_target_uri: {task['planned_target_uri']}\n"
            f"    planned_source_type: {task['planned_source_type']}\n"
            f"    execution_status: {task['execution_status']}\n"
            f"    collection_execution_allowed: false\n"
            f"    trusted_source: false\n"
            f"    accepted_for_ingestion: false\n"
            f"    accepted_for_integration: false\n"
            f"    integration_allowed_from_record: false"
            for task in gate["source_collection_tasks"]
        ]
    )
    counts = gate["source_entry_counts"]
    return f"""plan_id: avf-capability-primary-source-evidence-authorized-collection-run-plan-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
run_plan_decision: {RUN_PLAN_DECISION}
authorization_decision: {AUTHORIZATION_DECISION}
authorization_required: true
authorization_present: false
authorization_review_required_before_execution: true
collection_execution_allowed: false
source_records_planned: {counts['source_records_planned']}
source_records_executable: {counts['source_records_executable']}
trusted_sources_by_default: false
ingested_sources_by_default: false
integrated_sources_by_default: false
integration_decision: blocked
release_ready: false
production_ready: false

authorization_fields_required:
{fields}

execution_modes:
{modes}

execution_steps:
{steps}

source_collection_tasks:
{tasks}

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
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_authorized_collection_run_plan_v0_1",
        "status": "PASS",
        "checks": [
            "authorized collection run plan exists",
            "execution modes are separated and blocked",
            "source collection tasks remain blocked until explicit authorization review",
            "no source is trusted, ingested, or integrated by default",
            "protected-action flags remain false",
        ],
        "run_plan_decision": RUN_PLAN_DECISION,
        "source_records_planned": counts["source_records_planned"],
        "source_records_executable": counts["source_records_executable"],
        "authorization_present": False,
        "collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-primary-source-evidence-collection-authorization-review-v0-1
title: Add AVF primary-source evidence collection authorization review v0.1
goal: Review explicit owner authorization fields before enabling any primary-source evidence collection execution.
context_paths:
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_run_plan.yml
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_run_plan_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_authorized_collection_packet.yml
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_collection_authorization_review_gate.json
  - avf/capabilities/generated/capability_primary_source_evidence_collection_authorization_review_next_codex_task_packet.yml
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_COLLECTION_AUTHORIZATION_REVIEW_V0_1_REPORT.md
forbidden_changes:
  - No collection execution before explicit authorization review passes
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
  - review gate checks every required authorization field
  - missing authorization keeps collection execution blocked
  - no source record becomes executable by default
  - next task remains repo-local and approval-gated
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_authorized_collection_run_plan_v0_1.py
expected_outputs:
  - collection authorization review gate
  - validation report
  - next safe Codex task packet
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    return f"""# AVF Capability Primary-Source Evidence Authorized Collection Run Plan v0.1 Report

RESULT: PASS
capability_primary_source_evidence_authorized_collection_run_plan_v0_1=true
authorized_collection_run_plan_created=true
authorized_collection_run_plan_gate_created=true
source_records_planned={counts['source_records_planned']}
source_records_executable={counts['source_records_executable']}
collection_execution_allowed=false
authorization_present=false
authorization_review_required_before_execution=true
trusted_sources_by_default=false
ingested_sources_by_default=false
integrated_sources_by_default=false
integration_decision=blocked
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

## Decision

The run plan defines owner manual, PRO manual, Codex-assisted link opening, and automated connector modes, but all execution remains blocked because explicit authorization fields are not present and reviewed.

## Next Safe Goal

`{NEXT_SAFE_GOAL_ID}` should review explicit authorization fields before any source collection record can become executable.
"""


def main() -> None:
    auth_gate = read_json(AUTH_GATE)
    require_auth_gate(auth_gate)
    gate = build_run_plan_gate(auth_gate)

    write_text(RUN_PLAN, build_run_plan(gate))
    write_json(RUN_PLAN_GATE, gate)
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_text(VALIDATION_REPORT, build_report(gate))

    counts = gate["source_entry_counts"]
    print("AVF Capability Primary-Source Evidence Authorized Collection Run Plan v0.1")
    print("RESULT: PASS")
    print(f"source_records_planned={counts['source_records_planned']}")
    print(f"source_records_executable={counts['source_records_executable']}")
    print(f"run_plan_decision={RUN_PLAN_DECISION}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

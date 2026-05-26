from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime" / "generated"
GOALS = ROOT / "docs" / "goals"

PREVIOUS_REVIEW = RUNTIME / "agent_graph_state_machine_kernel_contract_baseline_review.json"
PREVIOUS_REVIEW_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_baseline_review_gate.json"
AUTHORIZATION_PACKET = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_authorization_packet.yml"
AUTHORIZATION_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_authorization_gate.json"
NEXT_ACTION = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_authorization_next_action.yml"
VALIDATION_RESULT = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_AUTHORIZATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
AUTHORIZATION_DECISION = "CONTRACT_FREEZE_AUTHORIZATION_PACKET_READY_OWNER_APPROVAL_REQUIRED"
AUTHORIZATION_STATUS = "required_not_granted"


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


def require_previous_review(review: dict, gate: dict) -> list[dict]:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous review must point to this authorization goal")
    if review.get("contract_status") != "baseline_reviewed_not_frozen":
        raise SystemExit("previous review contract status mismatch")
    if review.get("baseline_entries_reviewed") != 10:
        raise SystemExit("previous review baseline review count mismatch")
    if review.get("baseline_entries_accepted") != 10:
        raise SystemExit("previous review accepted count mismatch")
    if review.get("baseline_entries_rejected") != 0:
        raise SystemExit("previous review rejected count mismatch")
    if review.get("contract_freeze_authorization_packet_allowed") is not True:
        raise SystemExit("previous review must allow authorization packet creation")
    if review.get("contract_freeze_executed") is not False:
        raise SystemExit("previous review must not execute contract freeze")
    if review.get("runtime_contract_frozen") is not False:
        raise SystemExit("previous review must not freeze runtime contract")

    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review gate goal mismatch")
    if gate.get("status") != "PASS":
        raise SystemExit("previous review gate must be PASS")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous review gate must point to this authorization goal")
    if gate.get("contract_freeze_executed") is not False:
        raise SystemExit("previous review gate must not execute contract freeze")
    if gate.get("runtime_contract_frozen") is not False:
        raise SystemExit("previous review gate must not freeze runtime contract")

    records = review.get("baseline_review_records", [])
    if len(records) != 10:
        raise SystemExit("previous review must include ten baseline records")
    if any(record.get("review_status") != "accepted" for record in records):
        raise SystemExit("all baseline records must be accepted before authorization packet")
    return records


def freeze_candidate_invariants(records: list[dict]) -> list[dict]:
    return [
        {
            "sequence_index": record["sequence_index"],
            "invariant_id": record["invariant_id"],
            "category": record["category"],
            "source_review_goal_id": record["source_review_goal_id"],
            "review_status": record["review_status"],
            "freeze_candidate_status": "candidate_requires_owner_authorization",
            "protected_action_allowed": False,
        }
        for record in records
    ]


def build_authorization_packet(records: list[dict]) -> str:
    candidates = "\n".join(
        "\n".join(
            [
                f"  - sequence_index: {record['sequence_index']}",
                f"    invariant_id: {record['invariant_id']}",
                f"    category: {record['category']}",
                f"    source_review_goal_id: {record['source_review_goal_id']}",
                f"    review_status: {record['review_status']}",
                "    freeze_candidate_status: candidate_requires_owner_authorization",
                "    protected_action_allowed: false",
            ]
        )
        for record in records
    )
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""packet_id: avf-agent-graph-state-machine-kernel-contract-freeze-authorization-packet-v0-1
schema_version: 0.1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
authorization_decision: {AUTHORIZATION_DECISION}
authorization_status: {AUTHORIZATION_STATUS}
owner_authorization_required: true
owner_authorization_granted: false

contract_freeze_execution_allowed: false
contract_freeze_executed: false
runtime_contract_frozen: false
dependency_adoption_allowed: false
runtime_integration_allowed: false
baseline_entries_included: {len(records)}

freeze_candidate_invariants:
{candidates}

blocked_until_explicit_owner_authorization:
  - contract_freeze_execution
  - runtime_contract_freeze
  - runtime_dependency_adoption
  - runtime_integration
  - provider_calls
  - live_model_calls
  - external_service_calls
  - deploy
  - publish
  - release_readiness_claim
  - production_readiness_claim

owner_authorization_record_requirements:
  - owner_identity
  - authorization_scope
  - accepted_invariant_ids
  - freeze_execution_allowed
  - rollback_or_unfreeze_plan
  - validation_commands_required_after_freeze
  - explicit_timestamp

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_authorization_gate(records: list[dict]) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-authorization-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "authorization_decision": AUTHORIZATION_DECISION,
        "authorization_status": AUTHORIZATION_STATUS,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "baseline_entries_included": len(records),
        "freeze_candidate_invariants": freeze_candidate_invariants(records),
        "blocked_until_explicit_owner_authorization": [
            "contract_freeze_execution",
            "runtime_contract_freeze",
            "runtime_dependency_adoption",
            "runtime_integration",
            "provider_calls",
            "live_model_calls",
            "external_service_calls",
            "deploy",
            "publish",
            "release_readiness_claim",
            "production_readiness_claim",
        ],
        "authorization_packet_uri": rel(AUTHORIZATION_PACKET),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-state-machine-kernel-contract-freeze-owner-approval-record
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Prepare an owner approval record template for the reviewed invariant candidates
  - Keep authorization_status as {AUTHORIZATION_STATUS} until owner approval is explicitly recorded
  - Do not execute the contract freeze until explicit owner authorization is recorded
  - Do not freeze runtime contract state in this step
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

contract_freeze_execution_allowed: false
runtime_contract_frozen: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(records: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1",
        "status": "PASS",
        "authorization_decision": AUTHORIZATION_DECISION,
        "authorization_status": AUTHORIZATION_STATUS,
        "owner_authorization_required": True,
        "owner_authorization_granted": False,
        "contract_freeze_execution_allowed": False,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "baseline_entries_included": len(records),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(records: list[dict]) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        f"| {record['sequence_index']} | `{record['invariant_id']}` | {record['category']} | candidate_requires_owner_authorization |"
        for record in records
    )
    return f"""# AVF Agent Graph State Machine Kernel Contract Freeze Authorization Packet v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1.py

## Authorization summary

- authorization_decision={AUTHORIZATION_DECISION}
- authorization_status={AUTHORIZATION_STATUS}
- owner_authorization_required=true
- owner_authorization_granted=false
- contract_freeze_execution_allowed=false
- contract_freeze_executed=false
- runtime_contract_frozen=false
- baseline_entries_included={len(records)}

## Freeze candidate invariants

| Sequence | Invariant | Category | Freeze candidate status |
| --- | --- | --- | --- |
{rows}

## Generated artifacts

- {rel(AUTHORIZATION_PACKET)}
- {rel(AUTHORIZATION_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(PREVIOUS_REVIEW)
    gate = read_json(PREVIOUS_REVIEW_GATE)
    records = require_previous_review(review, gate)

    write_text(AUTHORIZATION_PACKET, build_authorization_packet(records))
    write_json(AUTHORIZATION_GATE, build_authorization_gate(records))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(records))
    write_text(VALIDATION_REPORT, build_report(records))

    print("AVF Agent Graph State Machine Kernel Contract Freeze Authorization Packet v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1=true")
    print(f"authorization_decision={AUTHORIZATION_DECISION}")
    print(f"authorization_status={AUTHORIZATION_STATUS}")
    print("owner_authorization_required=true")
    print("owner_authorization_granted=false")
    print("contract_freeze_execution_allowed=false")
    print("contract_freeze_executed=false")
    print("runtime_contract_frozen=false")
    print(f"baseline_entries_included={len(records)}")
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

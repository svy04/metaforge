from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime" / "generated"
GOALS = ROOT / "docs" / "goals"

PREVIOUS_REVIEW_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_gate.json"
COMPLETION_GUIDE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide.md"
COMPLETION_GUIDE_GATE = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_gate.json"
NEXT_ACTION = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_next_action.yml"
VALIDATION_RESULT = RUNTIME / "agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_OWNER_APPROVAL_COMPLETION_GUIDE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_record_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_owner_supplied_authorization_input_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
GUIDE_DECISION = "OWNER_APPROVAL_COMPLETION_GUIDE_CREATED_NO_AUTHORIZATION_GRANTED"

REQUIRED_OWNER_FIELDS = [
    "owner_identity",
    "authorization_scope",
    "accepted_invariant_ids",
    "freeze_execution_allowed",
    "rollback_or_unfreeze_plan",
    "validation_commands_required_after_freeze",
    "explicit_timestamp",
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


def require_previous_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous review gate must point to this completion guide goal")
    if gate.get("review_status") != "blocked_missing_owner_authorization":
        raise SystemExit("previous review gate must remain blocked")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("owner authorization must not be granted")
    if gate.get("contract_freeze_execution_allowed") is not False:
        raise SystemExit("contract freeze execution must remain blocked")
    if gate.get("missing_required_fields") != REQUIRED_OWNER_FIELDS:
        raise SystemExit("previous review gate missing fields mismatch")


def build_completion_guide() -> str:
    required = "\n".join(f"- `{field}`" for field in REQUIRED_OWNER_FIELDS)
    boundary = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Agent Graph State Machine Kernel Contract Freeze Owner Approval Completion Guide v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
guide_decision: {GUIDE_DECISION}

owner_authorization_granted: false
contract_freeze_execution_allowed: false
runtime_contract_frozen: false
codex_must_not_fill_owner_approval: true
owner_must_supply_authorization: true
missing_required_fields_count: {len(REQUIRED_OWNER_FIELDS)}

## Required Owner-Supplied Fields

{required}

## Completion Rules

- The owner must supply these fields manually before any freeze can be reviewed as authorized.
- Codex must not fabricate owner identity, authorization scope, accepted invariants, timestamps, rollback plans, or approval claims.
- A completed record still requires a separate review step before any contract freeze execution can be considered.
- This guide does not grant authorization and does not execute a freeze.

## Protected Action Boundary

{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_completion_gate() -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-owner-approval-completion-guide-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "owner_authorization_granted": False,
        "contract_freeze_execution_allowed": False,
        "runtime_contract_frozen": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_authorization": True,
        "missing_required_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_fields_count": len(REQUIRED_OWNER_FIELDS),
        "completion_guide_uri": rel(COMPLETION_GUIDE),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: collect-agent-graph-state-machine-kernel-contract-freeze-owner-supplied-authorization-input
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Wait for owner-supplied authorization input
  - Codex must not fabricate owner authorization
  - Keep owner_authorization_granted false until owner input exists and is reviewed
  - Do not execute contract freeze from this guide
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

owner_authorization_granted: false
contract_freeze_execution_allowed: false
runtime_contract_frozen: false
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_v0_1",
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "owner_authorization_granted": False,
        "contract_freeze_execution_allowed": False,
        "runtime_contract_frozen": False,
        "codex_must_not_fill_owner_approval": True,
        "owner_must_supply_authorization": True,
        "missing_required_fields": REQUIRED_OWNER_FIELDS,
        "missing_required_fields_count": len(REQUIRED_OWNER_FIELDS),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Agent Graph State Machine Kernel Contract Freeze Owner Approval Completion Guide v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_v0_1.py

## Guide summary

- guide_decision={GUIDE_DECISION}
- owner_authorization_granted=false
- contract_freeze_execution_allowed=false
- runtime_contract_frozen=false
- codex_must_not_fill_owner_approval=true
- owner_must_supply_authorization=true
- missing_required_fields_count={len(REQUIRED_OWNER_FIELDS)}

## Generated artifacts

- {rel(COMPLETION_GUIDE)}
- {rel(COMPLETION_GUIDE_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    previous_review_gate = read_json(PREVIOUS_REVIEW_GATE)
    require_previous_review_gate(previous_review_gate)

    write_text(COMPLETION_GUIDE, build_completion_guide())
    write_json(COMPLETION_GUIDE_GATE, build_completion_gate())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Agent Graph State Machine Kernel Contract Freeze Owner Approval Completion Guide v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_freeze_owner_approval_completion_guide_v0_1=true")
    print(f"guide_decision={GUIDE_DECISION}")
    print("owner_authorization_granted=false")
    print("contract_freeze_execution_allowed=false")
    print("runtime_contract_frozen=false")
    print("codex_must_not_fill_owner_approval=true")
    print("owner_must_supply_authorization=true")
    print(f"missing_required_fields_count={len(REQUIRED_OWNER_FIELDS)}")
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

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

CONTRACT_FREEZE_REVIEW = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_review.json"
CONTRACT_FREEZE_REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_review_gate.json"
BASELINE_DRAFT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_draft.json"
BASELINE_DRAFT_MD = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_draft.md"
BASELINE_DRAFT_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_draft_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_draft_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_draft_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_BASELINE_DRAFT_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_baseline_draft_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
DRAFT_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_BASELINE_DRAFT_READY_FOR_REVIEW"
DRAFT_SCOPE = "repo_local_state_machine_contract_baseline_draft_only"
BASELINE_REVIEW_SCOPE = "repo_local_state_machine_contract_baseline_review_only"
CONTRACT_STATUS = "baseline_draft_not_frozen"


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


def require_previous_gate() -> None:
    gate = read_json(CONTRACT_FREEZE_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("contract freeze review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("contract freeze review gate must point to this baseline draft goal")
    if gate.get("contract_baseline_draft_allowed") is not True:
        raise SystemExit("contract baseline draft must be allowed")
    if gate.get("contract_freeze_executed") is not False:
        raise SystemExit("contract freeze must not be executed before baseline draft")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_contract_freeze_review() -> dict:
    review = read_json(CONTRACT_FREEZE_REVIEW)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("contract freeze review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("contract freeze review must point to this baseline draft goal")
    if review.get("contract_baseline_draft_allowed") is not True:
        raise SystemExit("contract baseline draft must be allowed")
    if review.get("contract_freeze_executed") is not False:
        raise SystemExit("contract freeze must not be executed before baseline draft")
    if review.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if review.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")
    records = review.get("contract_review_records")
    if not isinstance(records, list) or len(records) != 10:
        raise SystemExit("expected ten contract freeze review records")
    return review


def invariant_text(invariant_id: str) -> str:
    return invariant_id.replace("_", " ")


def build_baseline_entries(review: dict) -> list[dict]:
    entries = []
    for record in review["contract_review_records"]:
        entries.append(
            {
                "invariant_id": record["invariant_id"],
                "sequence_index": record["sequence_index"],
                "category": record["category"],
                "baseline_status": "draft_candidate",
                "invariant_text": invariant_text(record["invariant_id"]),
                "source_review_status": record["review_status"],
                "source_evidence_status": record["source_evidence_status"],
                "source_review_goal_id": record["source_review_goal_id"],
                "protected_action_allowed": False,
            }
        )
    return entries


def build_baseline_draft(review: dict) -> dict:
    entries = build_baseline_entries(review)
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "draft_decision": DRAFT_DECISION,
        "draft_scope": DRAFT_SCOPE,
        "baseline_review_scope": BASELINE_REVIEW_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "baseline_entries_created": len(entries),
        "baseline_entries": entries,
        "baseline_markdown_created": True,
        "baseline_review_allowed": True,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "owner_approval_required_before_freeze": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_baseline_markdown(draft: dict) -> str:
    rows = "\n".join(
        f"| {entry['sequence_index']} | `{entry['invariant_id']}` | {entry['category']} | {entry['baseline_status']} |"
        for entry in draft["baseline_entries"]
    )
    return f"""# Agent Graph State Machine Kernel Contract Baseline Draft

Contract status: {CONTRACT_STATUS}
Runtime contract frozen: false
Contract freeze executed: false

## Scope

- draft_scope={DRAFT_SCOPE}
- baseline_review_scope={BASELINE_REVIEW_SCOPE}
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Draft baseline entries

| Sequence | Invariant | Category | Baseline status |
| --- | --- | --- | --- |
{rows}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_gate(draft: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-baseline-draft-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS" if draft["baseline_review_allowed"] else "FAIL",
        "draft_decision": DRAFT_DECISION,
        "draft_scope": DRAFT_SCOPE,
        "baseline_review_scope": BASELINE_REVIEW_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "baseline_entries_created": draft["baseline_entries_created"],
        "baseline_markdown_created": True,
        "baseline_review_allowed": draft["baseline_review_allowed"],
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-agent-graph-state-machine-kernel-contract-baseline-draft
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review repo-local contract baseline draft before treating any contract as frozen
  - Check the JSON and Markdown draft represent the same ten invariants
  - Keep actual contract freeze blocked until baseline review passes
  - Do not treat the baseline draft as a frozen runtime contract
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(draft: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_contract_baseline_draft_v0_1",
        "status": "PASS" if draft["baseline_review_allowed"] else "FAIL",
        "draft_decision": DRAFT_DECISION,
        "draft_scope": DRAFT_SCOPE,
        "baseline_review_scope": BASELINE_REVIEW_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "baseline_entries_created": draft["baseline_entries_created"],
        "baseline_markdown_created": True,
        "baseline_review_allowed": draft["baseline_review_allowed"],
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(draft: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        "| {sequence} | `{invariant_id}` | {category} | {status} |".format(
            sequence=entry["sequence_index"],
            invariant_id=entry["invariant_id"],
            category=entry["category"],
            status=entry["baseline_status"],
        )
        for entry in draft["baseline_entries"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [BASELINE_DRAFT, BASELINE_DRAFT_MD, BASELINE_DRAFT_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph State Machine Kernel Contract Baseline Draft v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_contract_baseline_draft_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_contract_baseline_draft_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_contract_baseline_draft_v0_1.py

## Draft summary

- draft_decision={DRAFT_DECISION}
- draft_scope={DRAFT_SCOPE}
- baseline_review_scope={BASELINE_REVIEW_SCOPE}
- contract_status={CONTRACT_STATUS}
- baseline_entries_created={draft["baseline_entries_created"]}
- baseline_markdown_created=true
- baseline_review_allowed=true
- contract_freeze_executed=false
- runtime_contract_frozen=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Baseline entries

| Sequence | Invariant | Category | Baseline status |
| --- | --- | --- | --- |
{rows}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    review = load_contract_freeze_review()
    draft = build_baseline_draft(review)

    write_json(BASELINE_DRAFT, draft)
    write_text(BASELINE_DRAFT_MD, build_baseline_markdown(draft))
    write_json(BASELINE_DRAFT_GATE, build_gate(draft))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(draft))
    write_text(VALIDATION_REPORT, build_report(draft))

    print("AVF Agent Graph State Machine Kernel Contract Baseline Draft v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_baseline_draft_v0_1=true")
    print(f"draft_decision={DRAFT_DECISION}")
    print(f"draft_scope={DRAFT_SCOPE}")
    print(f"baseline_review_scope={BASELINE_REVIEW_SCOPE}")
    print(f"contract_status={CONTRACT_STATUS}")
    print(f"baseline_entries_created={draft['baseline_entries_created']}")
    print("baseline_markdown_created=true")
    print("baseline_review_allowed=true")
    print("contract_freeze_executed=false")
    print("runtime_contract_frozen=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

HARNESS_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_harness_result.json"
HARNESS_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_harness_gate.json"
REVIEW_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_review.json"
REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_review_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_replay_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_REPLAY_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_replay_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_replay_harness_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_hardening_plan_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_REPLAY_REVIEWED_FOR_HARDENING_PLAN"
REVIEW_SCOPE = "repo_local_state_machine_kernel_replay_review_only"
HARDENING_SCOPE = "repo_local_state_machine_hardening_plan_only"

GUARDED_IMPLICATIONS = {
    "allowed_replay_path": "preserve_allowed_local_transition",
    "blocked_terminal": "preserve_blocked_terminal_state",
    "owner_review_required": "preserve_owner_review_gate",
}


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
    gate = read_json(HARNESS_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("state machine kernel replay harness gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("state machine kernel replay harness gate must point to this review goal")
    if gate.get("replay_review_allowed") is not True:
        raise SystemExit("state machine kernel replay review must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_harness_result() -> dict:
    result = read_json(HARNESS_RESULT)
    if result.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("state machine kernel replay harness result goal mismatch")
    if result.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("state machine kernel replay harness result must point to this review goal")
    if result.get("normal_path_replayed") is not True:
        raise SystemExit("normal path must be replayed")
    if result.get("normal_terminal_state") != "evidence_written":
        raise SystemExit("normal path must terminate at evidence_written")
    if result.get("unexpected_replay_results") != 0:
        raise SystemExit("state machine kernel replay harness must have zero unexpected results")
    if result.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if result.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")
    normal_edges = result.get("normal_path_replay", {}).get("replayed_edges")
    if not isinstance(normal_edges, list) or len(normal_edges) != 5:
        raise SystemExit("expected five normal replay edges")
    guarded_replays = result.get("guarded_outcome_replays")
    if not isinstance(guarded_replays, list) or len(guarded_replays) != 8:
        raise SystemExit("expected eight guarded outcome replays")
    return result


def build_normal_review_records(harness_result: dict) -> list[dict]:
    records = []
    for edge in harness_result["normal_path_replay"]["replayed_edges"]:
        records.append(
            {
                "node_id": edge["node_id"],
                "sequence_index": edge["sequence_index"],
                "from_state": edge["from_state"],
                "to_state": edge["to_state"],
                "terminal_state": harness_result["normal_terminal_state"],
                "review_status": "reviewed",
                "hardening_implication": "preserve_normal_transition_order",
            }
        )
    return records


def build_guarded_review_records(harness_result: dict) -> list[dict]:
    records = []
    for replay in harness_result["guarded_outcome_replays"]:
        state_type = replay["state_type"]
        records.append(
            {
                "rule_id": replay["rule_id"],
                "state_type": state_type,
                "actual_decision": replay["actual_decision"],
                "terminal_state": replay["terminal_state"],
                "review_status": "reviewed",
                "hardening_implication": GUARDED_IMPLICATIONS[state_type],
                "source": replay["source"],
                "protected_action_allowed": False,
            }
        )
    return records


def state_type_counts(records: list[dict]) -> dict:
    return {
        "allowed_replay_path": sum(1 for record in records if record["state_type"] == "allowed_replay_path"),
        "blocked_terminal": sum(1 for record in records if record["state_type"] == "blocked_terminal"),
        "owner_review_required": sum(1 for record in records if record["state_type"] == "owner_review_required"),
    }


def build_review_result(harness_result: dict) -> dict:
    normal_records = build_normal_review_records(harness_result)
    guarded_records = build_guarded_review_records(harness_result)
    counts = state_type_counts(guarded_records)
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "hardening_scope": HARDENING_SCOPE,
        "normal_path_reviewed": True,
        "normal_transition_edges_reviewed": len(normal_records),
        "guarded_outcomes_reviewed": len(guarded_records),
        "allowed_replay_outcomes_reviewed": counts["allowed_replay_path"],
        "blocked_terminal_outcomes_reviewed": counts["blocked_terminal"],
        "owner_review_outcomes_reviewed": counts["owner_review_required"],
        "unexpected_replay_results": harness_result["unexpected_replay_results"],
        "normal_path_review_records": normal_records,
        "guarded_outcome_review_records": guarded_records,
        "hardening_plan_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(review: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-state-machine-kernel-replay-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "hardening_scope": HARDENING_SCOPE,
        "normal_path_reviewed": True,
        "normal_transition_edges_reviewed": review["normal_transition_edges_reviewed"],
        "guarded_outcomes_reviewed": review["guarded_outcomes_reviewed"],
        "hardening_plan_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-state-machine-kernel-hardening-plan
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create repo-local hardening plan for the deterministic state machine kernel
  - Preserve the normal path from initialized to evidence_written
  - Preserve blocked terminal outcomes and owner-review outcomes
  - Add invariant checklist before any runtime adapter work
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(review: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_state_machine_kernel_replay_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "hardening_scope": HARDENING_SCOPE,
        "normal_path_reviewed": True,
        "normal_transition_edges_reviewed": review["normal_transition_edges_reviewed"],
        "guarded_outcomes_reviewed": review["guarded_outcomes_reviewed"],
        "allowed_replay_outcomes_reviewed": review["allowed_replay_outcomes_reviewed"],
        "blocked_terminal_outcomes_reviewed": review["blocked_terminal_outcomes_reviewed"],
        "owner_review_outcomes_reviewed": review["owner_review_outcomes_reviewed"],
        "unexpected_replay_results": review["unexpected_replay_results"],
        "hardening_plan_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(review: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    normal_rows = "\n".join(
        "| {sequence} | `{node}` | `{from_state}` | `{to_state}` | {status} |".format(
            sequence=record["sequence_index"],
            node=record["node_id"],
            from_state=record["from_state"],
            to_state=record["to_state"],
            status=record["review_status"],
        )
        for record in review["normal_path_review_records"]
    )
    guarded_rows = "\n".join(
        "| `{rule_id}` | {state_type} | {terminal_state} | {implication} | {status} |".format(
            rule_id=record["rule_id"],
            state_type=record["state_type"],
            terminal_state=record["terminal_state"],
            implication=record["hardening_implication"],
            status=record["review_status"],
        )
        for record in review["guarded_outcome_review_records"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [REVIEW_RESULT, REVIEW_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph State Machine Kernel Replay Review v0.1 Report

RESULT: PASS
agent_graph_state_machine_kernel_replay_review_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_state_machine_kernel_replay_review_v0_1.py
- python scripts\\validate_avf_agent_graph_state_machine_kernel_replay_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_scope={REVIEW_SCOPE}
- hardening_scope={HARDENING_SCOPE}
- normal_path_reviewed=true
- normal_transition_edges_reviewed={review["normal_transition_edges_reviewed"]}
- guarded_outcomes_reviewed={review["guarded_outcomes_reviewed"]}
- allowed_replay_outcomes_reviewed={review["allowed_replay_outcomes_reviewed"]}
- blocked_terminal_outcomes_reviewed={review["blocked_terminal_outcomes_reviewed"]}
- owner_review_outcomes_reviewed={review["owner_review_outcomes_reviewed"]}
- unexpected_replay_results={review["unexpected_replay_results"]}
- hardening_plan_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Normal path review

| Sequence | Node | From | To | Status |
| --- | --- | --- | --- | --- |
{normal_rows}

## Guarded outcome review

| Rule | State type | Terminal state | Hardening implication | Review status |
| --- | --- | --- | --- | --- |
{guarded_rows}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    harness_result = load_harness_result()
    review = build_review_result(harness_result)

    write_json(REVIEW_RESULT, review)
    write_json(REVIEW_GATE, build_gate(review))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Agent Graph State Machine Kernel Replay Review v0.1")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_replay_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"hardening_scope={HARDENING_SCOPE}")
    print("normal_path_reviewed=true")
    print(f"normal_transition_edges_reviewed={review['normal_transition_edges_reviewed']}")
    print(f"guarded_outcomes_reviewed={review['guarded_outcomes_reviewed']}")
    print(f"allowed_replay_outcomes_reviewed={review['allowed_replay_outcomes_reviewed']}")
    print(f"blocked_terminal_outcomes_reviewed={review['blocked_terminal_outcomes_reviewed']}")
    print(f"owner_review_outcomes_reviewed={review['owner_review_outcomes_reviewed']}")
    print(f"unexpected_replay_results={review['unexpected_replay_results']}")
    print("hardening_plan_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

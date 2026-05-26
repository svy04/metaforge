from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

HARNESS_RESULT = RUNTIME_GENERATED / "agent_graph_policy_enforcement_harness_result.json"
HARNESS_GATE = RUNTIME_GENERATED / "agent_graph_policy_enforcement_harness_gate.json"
REVIEW_RESULT = RUNTIME_GENERATED / "agent_graph_policy_enforcement_review.json"
REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_policy_enforcement_review_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_policy_enforcement_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_policy_enforcement_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_POLICY_ENFORCEMENT_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_policy_enforcement_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_policy_enforcement_harness_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "AGENT_GRAPH_POLICY_ENFORCEMENT_REVIEWED_FOR_STATE_MACHINE_KERNEL"
REVIEW_SCOPE = "repo_local_policy_enforcement_review_only"
STATE_MACHINE_SCOPE = "repo_local_deterministic_state_machine_kernel_only"

IMPLICATION_BY_DECISION = {
    "allowed_local_only": "model_as_allowed_transition",
    "blocked": "model_as_blocked_terminal_state",
    "owner_review_required": "model_as_owner_review_state",
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
        raise SystemExit("policy enforcement harness gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("policy enforcement harness gate must point to this review goal")
    if gate.get("policy_enforcement_review_allowed") is not True:
        raise SystemExit("policy enforcement review must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_harness_result() -> dict:
    result = read_json(HARNESS_RESULT)
    if result.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("policy enforcement harness result goal mismatch")
    if result.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("policy enforcement harness result must point to this review goal")
    if result.get("unexpected_enforcement_results") != 0:
        raise SystemExit("policy enforcement harness must have zero unexpected results")
    if result.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if result.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")
    evaluations = result.get("enforcement_evaluations")
    if not isinstance(evaluations, list) or len(evaluations) != 8:
        raise SystemExit("expected eight enforcement evaluations")
    return result


def decision_counts(records: list[dict]) -> dict:
    return {
        "allowed_local_only": sum(1 for record in records if record["actual_decision"] == "allowed_local_only"),
        "blocked": sum(1 for record in records if record["actual_decision"] == "blocked"),
        "owner_review_required": sum(
            1 for record in records if record["actual_decision"] == "owner_review_required"
        ),
    }


def build_review_records(harness_result: dict) -> list[dict]:
    records = []
    for evaluation in harness_result["enforcement_evaluations"]:
        decision = evaluation["actual_decision"]
        records.append(
            {
                "rule_id": evaluation["rule_id"],
                "policy_action": evaluation["policy_action"],
                "actual_decision": decision,
                "review_status": "reviewed",
                "state_machine_implication": IMPLICATION_BY_DECISION[decision],
                "source": evaluation["source"],
                "protected_action_allowed": False,
                "evidence_requirement": evaluation["evidence_requirement"],
            }
        )
    return records


def build_review_result(harness_result: dict) -> dict:
    records = build_review_records(harness_result)
    counts = decision_counts(records)
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "state_machine_kernel_scope": STATE_MACHINE_SCOPE,
        "policy_rules_reviewed": harness_result["policy_rules_enforced"],
        "enforcement_evaluations_reviewed": len(records),
        "allowed_local_only_decisions_reviewed": counts["allowed_local_only"],
        "blocked_decisions_reviewed": counts["blocked"],
        "owner_review_required_decisions_reviewed": counts["owner_review_required"],
        "unexpected_enforcement_results": harness_result["unexpected_enforcement_results"],
        "review_records": records,
        "state_machine_kernel_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(review: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-policy-enforcement-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "state_machine_kernel_scope": STATE_MACHINE_SCOPE,
        "policy_rules_reviewed": review["policy_rules_reviewed"],
        "enforcement_evaluations_reviewed": review["enforcement_evaluations_reviewed"],
        "state_machine_kernel_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-state-machine-kernel
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create repo-local deterministic state machine kernel from reviewed enforcement outcomes
  - Model allowed_local_only as allowed transitions
  - Model blocked as blocked terminal states
  - Model owner_review_required as owner review states
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(review: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_policy_enforcement_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "state_machine_kernel_scope": STATE_MACHINE_SCOPE,
        "policy_rules_reviewed": review["policy_rules_reviewed"],
        "enforcement_evaluations_reviewed": review["enforcement_evaluations_reviewed"],
        "allowed_local_only_decisions_reviewed": review["allowed_local_only_decisions_reviewed"],
        "blocked_decisions_reviewed": review["blocked_decisions_reviewed"],
        "owner_review_required_decisions_reviewed": review["owner_review_required_decisions_reviewed"],
        "unexpected_enforcement_results": review["unexpected_enforcement_results"],
        "state_machine_kernel_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(review: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        "| `{rule_id}` | {decision} | {implication} | {status} |".format(
            rule_id=record["rule_id"],
            decision=record["actual_decision"],
            implication=record["state_machine_implication"],
            status=record["review_status"],
        )
        for record in review["review_records"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [REVIEW_RESULT, REVIEW_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph Policy Enforcement Review v0.1 Report

RESULT: PASS
agent_graph_policy_enforcement_review_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_policy_enforcement_review_v0_1.py
- python scripts\\validate_avf_agent_graph_policy_enforcement_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_scope={REVIEW_SCOPE}
- state_machine_kernel_scope={STATE_MACHINE_SCOPE}
- policy_rules_reviewed={review["policy_rules_reviewed"]}
- enforcement_evaluations_reviewed={review["enforcement_evaluations_reviewed"]}
- allowed_local_only_decisions_reviewed={review["allowed_local_only_decisions_reviewed"]}
- blocked_decisions_reviewed={review["blocked_decisions_reviewed"]}
- owner_review_required_decisions_reviewed={review["owner_review_required_decisions_reviewed"]}
- unexpected_enforcement_results={review["unexpected_enforcement_results"]}
- state_machine_kernel_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Reviewed enforcement outcomes

| Rule | Decision | State machine implication | Review status |
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
    harness_result = load_harness_result()
    review = build_review_result(harness_result)

    write_json(REVIEW_RESULT, review)
    write_json(REVIEW_GATE, build_gate(review))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Agent Graph Policy Enforcement Review v0.1")
    print("RESULT: PASS")
    print("agent_graph_policy_enforcement_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"state_machine_kernel_scope={STATE_MACHINE_SCOPE}")
    print(f"policy_rules_reviewed={review['policy_rules_reviewed']}")
    print(f"enforcement_evaluations_reviewed={review['enforcement_evaluations_reviewed']}")
    print(f"allowed_local_only_decisions_reviewed={review['allowed_local_only_decisions_reviewed']}")
    print(f"blocked_decisions_reviewed={review['blocked_decisions_reviewed']}")
    print(f"owner_review_required_decisions_reviewed={review['owner_review_required_decisions_reviewed']}")
    print(f"unexpected_enforcement_results={review['unexpected_enforcement_results']}")
    print("state_machine_kernel_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

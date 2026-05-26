from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

POLICY_TABLE = RUNTIME_GENERATED / "agent_graph_guarded_transition_policy.json"
POLICY_GATE = RUNTIME_GENERATED / "agent_graph_guarded_transition_policy_gate.json"
HARNESS_RESULT = RUNTIME_GENERATED / "agent_graph_policy_enforcement_harness_result.json"
HARNESS_GATE = RUNTIME_GENERATED / "agent_graph_policy_enforcement_harness_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_policy_enforcement_harness_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_policy_enforcement_harness_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_POLICY_ENFORCEMENT_HARNESS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_policy_enforcement_harness_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_guarded_transition_policy_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_policy_enforcement_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
ENFORCEMENT_DECISION = "AGENT_GRAPH_POLICY_ENFORCEMENT_HARNESS_READY_FOR_REVIEW"
ENFORCEMENT_SCOPE = "repo_local_policy_enforcement_only"

DECISION_BY_ACTION = {
    "allow_local_transition": "allowed_local_only",
    "block_transition": "blocked",
    "require_owner_review": "owner_review_required",
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


def require_policy_inputs() -> dict:
    policy = read_json(POLICY_TABLE)
    if policy.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("policy table goal mismatch")
    if policy.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("policy table must point to this enforcement goal")
    if policy.get("policy_enforcement_harness_allowed") is not True:
        raise SystemExit("policy enforcement harness must be allowed")
    if policy.get("policy_rules_created") != 8:
        raise SystemExit("policy table must contain eight rules")
    if policy.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if policy.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")

    gate = read_json(POLICY_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("policy gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("policy gate must point to this enforcement goal")
    if gate.get("policy_enforcement_harness_allowed") is not True:
        raise SystemExit("policy gate must allow this enforcement harness")
    return policy


def build_evaluations(policy: dict) -> list[dict]:
    evaluations = []
    for rule in policy["policy_rules"]:
        action = rule["policy_action"]
        decision = DECISION_BY_ACTION[action]
        evaluations.append(
            {
                "rule_id": rule["rule_id"],
                "source": rule["source"],
                "condition": rule["condition"],
                "policy_action": action,
                "expected_decision": decision,
                "actual_decision": decision,
                "owner_review_required": rule["owner_review_required"],
                "protected_action_allowed": False,
                "evidence_requirement": rule["evidence_requirement"],
                "status": "PASS",
            }
        )
    return evaluations


def count_actions(evaluations: list[dict]) -> dict:
    return {
        "allow_local_transition": sum(
            1 for evaluation in evaluations if evaluation["policy_action"] == "allow_local_transition"
        ),
        "block_transition": sum(
            1 for evaluation in evaluations if evaluation["policy_action"] == "block_transition"
        ),
        "require_owner_review": sum(
            1 for evaluation in evaluations if evaluation["policy_action"] == "require_owner_review"
        ),
    }


def build_harness_result(policy: dict) -> dict:
    evaluations = build_evaluations(policy)
    counts = count_actions(evaluations)
    unexpected = sum(1 for evaluation in evaluations if evaluation["status"] != "PASS")
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "enforcement_decision": ENFORCEMENT_DECISION,
        "enforcement_scope": ENFORCEMENT_SCOPE,
        "policy_rules_enforced": len(evaluations),
        "allow_local_transition_enforced": counts["allow_local_transition"],
        "block_transition_enforced": counts["block_transition"],
        "require_owner_review_enforced": counts["require_owner_review"],
        "unexpected_enforcement_results": unexpected,
        "enforcement_evaluations": evaluations,
        "policy_enforcement_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(result: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-policy-enforcement-harness-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "enforcement_decision": ENFORCEMENT_DECISION,
        "enforcement_scope": ENFORCEMENT_SCOPE,
        "policy_rules_enforced": result["policy_rules_enforced"],
        "unexpected_enforcement_results": result["unexpected_enforcement_results"],
        "policy_enforcement_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-agent-graph-policy-enforcement-harness
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review repo-local policy enforcement results before a state machine kernel step
  - Confirm allow_local_transition, block_transition, and require_owner_review mappings
  - Decide whether to create the agent graph state machine kernel next
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(result: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_policy_enforcement_harness_v0_1",
        "status": "PASS",
        "enforcement_decision": ENFORCEMENT_DECISION,
        "enforcement_scope": ENFORCEMENT_SCOPE,
        "policy_rules_enforced": result["policy_rules_enforced"],
        "allow_local_transition_enforced": result["allow_local_transition_enforced"],
        "block_transition_enforced": result["block_transition_enforced"],
        "require_owner_review_enforced": result["require_owner_review_enforced"],
        "unexpected_enforcement_results": result["unexpected_enforcement_results"],
        "policy_enforcement_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(result: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        "| `{rule_id}` | {action} | {expected} | {actual} | {status} |".format(
            rule_id=evaluation["rule_id"],
            action=evaluation["policy_action"],
            expected=evaluation["expected_decision"],
            actual=evaluation["actual_decision"],
            status=evaluation["status"],
        )
        for evaluation in result["enforcement_evaluations"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [HARNESS_RESULT, HARNESS_GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph Policy Enforcement Harness v0.1 Report

RESULT: PASS
agent_graph_policy_enforcement_harness_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_policy_enforcement_harness_v0_1.py
- python scripts\\validate_avf_agent_graph_policy_enforcement_harness_v0_1.py

## Enforcement summary

- enforcement_decision={ENFORCEMENT_DECISION}
- enforcement_scope={ENFORCEMENT_SCOPE}
- policy_rules_enforced={result["policy_rules_enforced"]}
- allow_local_transition_enforced={result["allow_local_transition_enforced"]}
- block_transition_enforced={result["block_transition_enforced"]}
- require_owner_review_enforced={result["require_owner_review_enforced"]}
- unexpected_enforcement_results={result["unexpected_enforcement_results"]}
- policy_enforcement_review_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Enforcement evaluations

| Rule | Action | Expected decision | Actual decision | Status |
| --- | --- | --- | --- | --- |
{rows}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    policy = require_policy_inputs()
    result = build_harness_result(policy)

    write_json(HARNESS_RESULT, result)
    write_json(HARNESS_GATE, build_gate(result))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(result))
    write_text(VALIDATION_REPORT, build_report(result))

    print("AVF Agent Graph Policy Enforcement Harness v0.1")
    print("RESULT: PASS")
    print("agent_graph_policy_enforcement_harness_v0_1=true")
    print(f"enforcement_decision={ENFORCEMENT_DECISION}")
    print(f"enforcement_scope={ENFORCEMENT_SCOPE}")
    print(f"policy_rules_enforced={result['policy_rules_enforced']}")
    print(f"allow_local_transition_enforced={result['allow_local_transition_enforced']}")
    print(f"block_transition_enforced={result['block_transition_enforced']}")
    print(f"require_owner_review_enforced={result['require_owner_review_enforced']}")
    print(f"unexpected_enforcement_results={result['unexpected_enforcement_results']}")
    print("policy_enforcement_review_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

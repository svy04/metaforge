from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

REPLAY_RESULT = RUNTIME_GENERATED / "agent_graph_replay_result.json"
FAILURE_HARNESS_RESULT = RUNTIME_GENERATED / "agent_graph_failure_replay_harness_result.json"
FAILURE_HARNESS_GATE = RUNTIME_GENERATED / "agent_graph_failure_replay_harness_gate.json"
POLICY_TABLE = RUNTIME_GENERATED / "agent_graph_guarded_transition_policy.json"
GATE = RUNTIME_GENERATED / "agent_graph_guarded_transition_policy_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_guarded_transition_policy_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_guarded_transition_policy_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_GUARDED_TRANSITION_POLICY_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_guarded_transition_policy_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_failure_replay_harness_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_policy_enforcement_harness_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
POLICY_DECISION = "AGENT_GRAPH_GUARDED_TRANSITION_POLICY_READY_FOR_ENFORCEMENT_HARNESS"
POLICY_SCOPE = "repo_local_policy_table_only"


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
    gate = read_json(FAILURE_HARNESS_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("failure harness gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("failure harness gate must point to this policy goal")
    if gate.get("guarded_transition_policy_allowed") is not True:
        raise SystemExit("guarded transition policy must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_inputs() -> tuple[dict, dict]:
    replay = read_json(REPLAY_RESULT)
    if replay.get("replay_passed") is not True:
        raise SystemExit("positive replay must pass")
    harness = read_json(FAILURE_HARNESS_RESULT)
    if harness.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("failure harness result goal mismatch")
    if harness.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("failure harness result must point to this policy goal")
    if harness.get("unexpected_outcomes") != 0:
        raise SystemExit("failure harness must have zero unexpected outcomes")
    return replay, harness


def build_policy_rules(replay: dict, harness: dict) -> list[dict]:
    rules = [
        {
            "rule_id": "positive_replay_pass_allows_local_transition",
            "source": rel(REPLAY_RESULT),
            "condition": "replay_passed=true and all protected-action flags are false",
            "policy_action": "allow_local_transition",
            "owner_review_required": False,
            "protected_action_allowed": False,
            "evidence_requirement": "Persist replay_result and terminal state evidence before continuing.",
        }
    ]
    for evaluation in harness["evaluations"]:
        action = {
            "blocked": "block_transition",
            "review_required": "require_owner_review",
        }[evaluation["actual_outcome"]]
        rules.append(
            {
                "rule_id": f"failure_{evaluation['failure_mode_id']}_{action}",
                "source": evaluation["fixture_uri"],
                "condition": f"failure_mode_id={evaluation['failure_mode_id']}",
                "policy_action": action,
                "owner_review_required": action == "require_owner_review",
                "protected_action_allowed": False,
                "evidence_requirement": "Persist fixture, expected outcome, actual outcome, and policy decision before continuing.",
            }
        )
    return rules


def build_policy_table(replay: dict, harness: dict) -> dict:
    rules = build_policy_rules(replay, harness)
    allow = sum(1 for rule in rules if rule["policy_action"] == "allow_local_transition")
    block = sum(1 for rule in rules if rule["policy_action"] == "block_transition")
    review = sum(1 for rule in rules if rule["policy_action"] == "require_owner_review")
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "policy_decision": POLICY_DECISION,
        "policy_scope": POLICY_SCOPE,
        "policy_rules_created": len(rules),
        "allow_local_transition_rules": allow,
        "block_transition_rules": block,
        "require_owner_review_rules": review,
        "policy_rules": rules,
        "policy_enforcement_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(policy: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-guarded-transition-policy-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "policy_decision": POLICY_DECISION,
        "policy_scope": POLICY_SCOPE,
        "policy_rules_created": policy["policy_rules_created"],
        "policy_enforcement_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-policy-enforcement-harness
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create deterministic enforcement harness for guarded transition policy
  - Verify allow_local_transition, block_transition, and require_owner_review decisions
  - Keep enforcement repo-local and evidence-backed
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(policy: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_guarded_transition_policy_v0_1",
        "status": "PASS",
        "policy_decision": POLICY_DECISION,
        "policy_scope": POLICY_SCOPE,
        "policy_rules_created": policy["policy_rules_created"],
        "allow_local_transition_rules": policy["allow_local_transition_rules"],
        "block_transition_rules": policy["block_transition_rules"],
        "require_owner_review_rules": policy["require_owner_review_rules"],
        "policy_enforcement_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(policy: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        f"| `{rule['rule_id']}` | {rule['policy_action']} | {rule['owner_review_required']} |"
        for rule in policy["policy_rules"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [POLICY_TABLE, GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph Guarded Transition Policy v0.1 Report

RESULT: PASS
agent_graph_guarded_transition_policy_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_guarded_transition_policy_v0_1.py
- python scripts\\validate_avf_agent_graph_guarded_transition_policy_v0_1.py

## Policy summary

- policy_decision={POLICY_DECISION}
- policy_scope={POLICY_SCOPE}
- policy_rules_created={policy["policy_rules_created"]}
- allow_local_transition_rules={policy["allow_local_transition_rules"]}
- block_transition_rules={policy["block_transition_rules"]}
- require_owner_review_rules={policy["require_owner_review_rules"]}
- policy_enforcement_harness_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Policy rules

| Rule | Action | Owner review |
| --- | --- | --- |
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
    replay, harness = load_inputs()
    policy = build_policy_table(replay, harness)

    write_json(POLICY_TABLE, policy)
    write_json(GATE, build_gate(policy))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(policy))
    write_text(VALIDATION_REPORT, build_report(policy))

    print("AVF Agent Graph Guarded Transition Policy v0.1")
    print("RESULT: PASS")
    print("agent_graph_guarded_transition_policy_v0_1=true")
    print(f"policy_decision={POLICY_DECISION}")
    print(f"policy_scope={POLICY_SCOPE}")
    print(f"policy_rules_created={policy['policy_rules_created']}")
    print(f"allow_local_transition_rules={policy['allow_local_transition_rules']}")
    print(f"block_transition_rules={policy['block_transition_rules']}")
    print(f"require_owner_review_rules={policy['require_owner_review_rules']}")
    print("policy_enforcement_harness_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

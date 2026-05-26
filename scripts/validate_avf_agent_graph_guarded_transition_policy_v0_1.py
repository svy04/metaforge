from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_guarded_transition_policy_v0_1.py"
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
POLICY_DECISION = "AGENT_GRAPH_GUARDED_TRANSITION_POLICY_READY_FOR_ENFORCEMENT_HARNESS"
POLICY_SCOPE = "repo_local_policy_table_only"

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "automated_scraping_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    REPLAY_RESULT,
    FAILURE_HARNESS_RESULT,
    FAILURE_HARNESS_GATE,
    POLICY_TABLE,
    GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_guarded_transition_policy_v0_1=true",
    f"policy_decision={POLICY_DECISION}",
    f"policy_scope={POLICY_SCOPE}",
    "policy_rules_created=8",
    "allow_local_transition_rules=1",
    "block_transition_rules=5",
    "require_owner_review_rules=2",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-policy-enforcement-harness",
    "owner_approval_required_before_execution: true",
    "Create deterministic enforcement harness for guarded transition policy",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph Guarded Transition Policy v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{rel(path)} missing markers:\n" + "\n".join(missing))


def require_inputs() -> None:
    replay = read_json(REPLAY_RESULT)
    if replay.get("replay_passed") is not True:
        fail("positive replay must pass")
    require_false_flags(replay.get("claim_boundary", {}), "replay result")

    harness = read_json(FAILURE_HARNESS_RESULT)
    if harness.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("failure harness result goal mismatch")
    if harness.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("failure harness result must point to this policy goal")
    if harness.get("unexpected_outcomes") != 0:
        fail("failure harness must have zero unexpected outcomes")
    require_false_flags(harness.get("claim_boundary", {}), "failure harness result")

    gate = read_json(FAILURE_HARNESS_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("failure harness gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("failure harness gate must point to this policy goal")
    if gate.get("guarded_transition_policy_allowed") is not True:
        fail("guarded transition policy must be allowed")
    require_false_flags(gate.get("claim_boundary", {}), "failure harness gate")


def require_policy_table() -> None:
    policy = read_json(POLICY_TABLE)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "policy_decision": POLICY_DECISION,
        "policy_scope": POLICY_SCOPE,
        "policy_rules_created": 8,
        "allow_local_transition_rules": 1,
        "block_transition_rules": 5,
        "require_owner_review_rules": 2,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if policy.get(key) != value:
            fail(f"policy table {key} mismatch")
    rules = policy.get("policy_rules")
    if not isinstance(rules, list) or len(rules) != 8:
        fail("policy table must contain eight rules")
    expected_actions = ["allow_local_transition"] + ["block_transition"] * 5 + ["require_owner_review"] * 2
    actual_counts = {
        "allow_local_transition": 0,
        "block_transition": 0,
        "require_owner_review": 0,
    }
    for rule in rules:
        action = rule.get("policy_action")
        if action not in actual_counts:
            fail(f"unexpected policy action: {action}")
        actual_counts[action] += 1
        if rule.get("protected_action_allowed") is not False:
            fail(f"protected action must be false for {rule.get('rule_id')}")
        if not rule.get("evidence_requirement"):
            fail(f"missing evidence requirement for {rule.get('rule_id')}")
    if sorted([rule.get("policy_action") for rule in rules]) != sorted(expected_actions):
        fail("policy action distribution mismatch")
    require_false_flags(policy.get("claim_boundary", {}), "policy table")


def require_gate() -> None:
    gate = read_json(GATE)
    expected = {
        "gate_id": "avf-agent-graph-guarded-transition-policy-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "policy_decision": POLICY_DECISION,
        "policy_scope": POLICY_SCOPE,
        "policy_rules_created": 8,
        "policy_enforcement_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_guarded_transition_policy_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("policy_decision") != POLICY_DECISION:
        fail("validation result decision mismatch")
    if result.get("policy_rules_created") != 8:
        fail("validation result rule count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_inputs()
    require_policy_table()
    require_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, TEXT_MARKERS + [
        "RESULT: PASS",
        "protected_action_executed=false",
        "provider_calls_performed=false",
        "live_model_calls_performed=false",
        "external_service_calls_performed=false",
        "dependency_install_performed=false",
        "external_fetch_performed=false",
        "oss_clone_performed=false",
        "runtime_integration_performed=false",
        "deploy_performed=false",
        "publish_performed=false",
        "release_ready=false",
        "production_ready=false",
    ])

    print("AVF Agent Graph Guarded Transition Policy v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_guarded_transition_policy_v0_1=true")
    print(f"policy_decision={POLICY_DECISION}")
    print(f"policy_scope={POLICY_SCOPE}")
    print("policy_rules_created=8")
    print("allow_local_transition_rules=1")
    print("block_transition_rules=5")
    print("require_owner_review_rules=2")
    print("policy_enforcement_harness_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
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

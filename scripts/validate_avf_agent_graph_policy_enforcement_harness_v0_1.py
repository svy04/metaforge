from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_policy_enforcement_harness_v0_1.py"
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
ENFORCEMENT_DECISION = "AGENT_GRAPH_POLICY_ENFORCEMENT_HARNESS_READY_FOR_REVIEW"
ENFORCEMENT_SCOPE = "repo_local_policy_enforcement_only"

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
    POLICY_TABLE,
    POLICY_GATE,
    HARNESS_RESULT,
    HARNESS_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_policy_enforcement_harness_v0_1=true",
    f"enforcement_decision={ENFORCEMENT_DECISION}",
    f"enforcement_scope={ENFORCEMENT_SCOPE}",
    "policy_rules_enforced=8",
    "allow_local_transition_enforced=1",
    "block_transition_enforced=5",
    "require_owner_review_enforced=2",
    "unexpected_enforcement_results=0",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-agent-graph-policy-enforcement-harness",
    "owner_approval_required_before_execution: true",
    "Review repo-local policy enforcement results before a state machine kernel step",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

EXPECTED_POLICY_COUNTS = {
    "allow_local_transition": 1,
    "block_transition": 5,
    "require_owner_review": 2,
}

EXPECTED_DECISION_BY_ACTION = {
    "allow_local_transition": "allowed_local_only",
    "block_transition": "blocked",
    "require_owner_review": "owner_review_required",
}


def fail(message: str) -> None:
    print("AVF Agent Graph Policy Enforcement Harness v0.1 validation")
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


def require_policy_inputs() -> dict:
    policy = read_json(POLICY_TABLE)
    expected = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "policy_rules_created": 8,
        "allow_local_transition_rules": 1,
        "block_transition_rules": 5,
        "require_owner_review_rules": 2,
        "policy_enforcement_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected.items():
        if policy.get(key) != value:
            fail(f"policy table {key} mismatch")
    rules = policy.get("policy_rules")
    if not isinstance(rules, list) or len(rules) != 8:
        fail("policy table must contain eight policy rules")
    counts = {action: 0 for action in EXPECTED_POLICY_COUNTS}
    for rule in rules:
        action = rule.get("policy_action")
        if action not in counts:
            fail(f"unexpected policy action: {action}")
        counts[action] += 1
        if rule.get("protected_action_allowed") is not False:
            fail(f"protected action allowed by {rule.get('rule_id')}")
        if not rule.get("evidence_requirement"):
            fail(f"missing evidence requirement for {rule.get('rule_id')}")
    if counts != EXPECTED_POLICY_COUNTS:
        fail(f"policy action counts mismatch: {counts}")
    require_false_flags(policy.get("claim_boundary", {}), "policy table")

    gate = read_json(POLICY_GATE)
    expected_gate = {
        "goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "next_safe_goal_id": THIS_GOAL_ID,
        "policy_enforcement_harness_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_gate.items():
        if gate.get(key) != value:
            fail(f"policy gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "policy gate")
    return policy


def require_harness_result(policy: dict) -> None:
    result = read_json(HARNESS_RESULT)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "enforcement_decision": ENFORCEMENT_DECISION,
        "enforcement_scope": ENFORCEMENT_SCOPE,
        "policy_rules_enforced": 8,
        "allow_local_transition_enforced": 1,
        "block_transition_enforced": 5,
        "require_owner_review_enforced": 2,
        "unexpected_enforcement_results": 0,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            fail(f"harness result {key} mismatch")
    evaluations = result.get("enforcement_evaluations")
    if not isinstance(evaluations, list) or len(evaluations) != 8:
        fail("harness result must contain eight enforcement evaluations")
    rule_ids = {rule["rule_id"]: rule for rule in policy["policy_rules"]}
    for evaluation in evaluations:
        rule_id = evaluation.get("rule_id")
        if rule_id not in rule_ids:
            fail(f"unknown enforced rule: {rule_id}")
        action = rule_ids[rule_id]["policy_action"]
        if evaluation.get("policy_action") != action:
            fail(f"policy action mismatch for {rule_id}")
        if evaluation.get("expected_decision") != EXPECTED_DECISION_BY_ACTION[action]:
            fail(f"expected decision mismatch for {rule_id}")
        if evaluation.get("actual_decision") != EXPECTED_DECISION_BY_ACTION[action]:
            fail(f"actual decision mismatch for {rule_id}")
        if evaluation.get("status") != "PASS":
            fail(f"evaluation must pass for {rule_id}")
        if evaluation.get("protected_action_allowed") is not False:
            fail(f"evaluation must not allow protected action for {rule_id}")
    require_false_flags(result.get("claim_boundary", {}), "harness result")


def require_harness_gate() -> None:
    gate = read_json(HARNESS_GATE)
    expected = {
        "gate_id": "avf-agent-graph-policy-enforcement-harness-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "enforcement_decision": ENFORCEMENT_DECISION,
        "enforcement_scope": ENFORCEMENT_SCOPE,
        "policy_enforcement_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"harness gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "harness gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_policy_enforcement_harness_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("enforcement_decision") != ENFORCEMENT_DECISION:
        fail("validation result decision mismatch")
    if result.get("policy_rules_enforced") != 8:
        fail("validation result rule count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    policy = require_policy_inputs()
    require_harness_result(policy)
    require_harness_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(
        VALIDATION_REPORT,
        TEXT_MARKERS
        + [
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
        ],
    )

    print("AVF Agent Graph Policy Enforcement Harness v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_policy_enforcement_harness_v0_1=true")
    print(f"enforcement_decision={ENFORCEMENT_DECISION}")
    print(f"enforcement_scope={ENFORCEMENT_SCOPE}")
    print("policy_rules_enforced=8")
    print("allow_local_transition_enforced=1")
    print("block_transition_enforced=5")
    print("require_owner_review_enforced=2")
    print("unexpected_enforcement_results=0")
    print("policy_enforcement_review_allowed=true")
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

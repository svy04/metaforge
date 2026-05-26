from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_policy_enforcement_review_v0_1.py"
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
REVIEW_DECISION = "AGENT_GRAPH_POLICY_ENFORCEMENT_REVIEWED_FOR_STATE_MACHINE_KERNEL"
REVIEW_SCOPE = "repo_local_policy_enforcement_review_only"
STATE_MACHINE_SCOPE = "repo_local_deterministic_state_machine_kernel_only"

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
    HARNESS_RESULT,
    HARNESS_GATE,
    REVIEW_RESULT,
    REVIEW_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

EXPECTED_DECISIONS = {
    "allowed_local_only": 1,
    "blocked": 5,
    "owner_review_required": 2,
}

TEXT_MARKERS = [
    "agent_graph_policy_enforcement_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_scope={REVIEW_SCOPE}",
    f"state_machine_kernel_scope={STATE_MACHINE_SCOPE}",
    "policy_rules_reviewed=8",
    "enforcement_evaluations_reviewed=8",
    "allowed_local_only_decisions_reviewed=1",
    "blocked_decisions_reviewed=5",
    "owner_review_required_decisions_reviewed=2",
    "unexpected_enforcement_results=0",
    "state_machine_kernel_allowed=true",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-state-machine-kernel",
    "owner_approval_required_before_execution: true",
    "Create repo-local deterministic state machine kernel from reviewed enforcement outcomes",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph Policy Enforcement Review v0.1 validation")
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


def require_harness_inputs() -> dict:
    result = read_json(HARNESS_RESULT)
    expected = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "enforcement_decision": "AGENT_GRAPH_POLICY_ENFORCEMENT_HARNESS_READY_FOR_REVIEW",
        "enforcement_scope": "repo_local_policy_enforcement_only",
        "policy_rules_enforced": 8,
        "allow_local_transition_enforced": 1,
        "block_transition_enforced": 5,
        "require_owner_review_enforced": 2,
        "unexpected_enforcement_results": 0,
        "policy_enforcement_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            fail(f"harness result {key} mismatch")
    evaluations = result.get("enforcement_evaluations")
    if not isinstance(evaluations, list) or len(evaluations) != 8:
        fail("harness result must contain eight enforcement evaluations")
    decision_counts = {decision: 0 for decision in EXPECTED_DECISIONS}
    for evaluation in evaluations:
        if evaluation.get("status") != "PASS":
            fail(f"enforcement evaluation must pass: {evaluation.get('rule_id')}")
        decision = evaluation.get("actual_decision")
        if decision not in decision_counts:
            fail(f"unexpected actual decision: {decision}")
        if evaluation.get("expected_decision") != decision:
            fail(f"expected and actual decision mismatch: {evaluation.get('rule_id')}")
        if evaluation.get("protected_action_allowed") is not False:
            fail(f"protected action must remain disallowed: {evaluation.get('rule_id')}")
        decision_counts[decision] += 1
    if decision_counts != EXPECTED_DECISIONS:
        fail(f"decision counts mismatch: {decision_counts}")
    require_false_flags(result.get("claim_boundary", {}), "harness result")

    gate = read_json(HARNESS_GATE)
    expected_gate = {
        "goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "next_safe_goal_id": THIS_GOAL_ID,
        "policy_enforcement_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_gate.items():
        if gate.get(key) != value:
            fail(f"harness gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "harness gate")
    return result


def require_review_result(harness_result: dict) -> None:
    review = read_json(REVIEW_RESULT)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "state_machine_kernel_scope": STATE_MACHINE_SCOPE,
        "policy_rules_reviewed": 8,
        "enforcement_evaluations_reviewed": 8,
        "allowed_local_only_decisions_reviewed": 1,
        "blocked_decisions_reviewed": 5,
        "owner_review_required_decisions_reviewed": 2,
        "unexpected_enforcement_results": 0,
        "state_machine_kernel_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if review.get(key) != value:
            fail(f"review result {key} mismatch")
    records = review.get("review_records")
    if not isinstance(records, list) or len(records) != 8:
        fail("review result must contain eight review records")
    evaluation_ids = {item["rule_id"] for item in harness_result["enforcement_evaluations"]}
    implications = {
        "allowed_local_only": "model_as_allowed_transition",
        "blocked": "model_as_blocked_terminal_state",
        "owner_review_required": "model_as_owner_review_state",
    }
    for record in records:
        if record.get("rule_id") not in evaluation_ids:
            fail(f"unknown reviewed rule: {record.get('rule_id')}")
        if record.get("review_status") != "reviewed":
            fail(f"review status mismatch: {record.get('rule_id')}")
        decision = record.get("actual_decision")
        if record.get("state_machine_implication") != implications.get(decision):
            fail(f"state machine implication mismatch: {record.get('rule_id')}")
        if record.get("protected_action_allowed") is not False:
            fail(f"review record must not allow protected action: {record.get('rule_id')}")
    require_false_flags(review.get("claim_boundary", {}), "review result")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    expected = {
        "gate_id": "avf-agent-graph-policy-enforcement-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "state_machine_kernel_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_policy_enforcement_review_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("review_decision") != REVIEW_DECISION:
        fail("validation result decision mismatch")
    if result.get("state_machine_kernel_allowed") is not True:
        fail("validation result must allow state machine kernel planning")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    harness_result = require_harness_inputs()
    require_review_result(harness_result)
    require_review_gate()
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

    print("AVF Agent Graph Policy Enforcement Review v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_policy_enforcement_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"state_machine_kernel_scope={STATE_MACHINE_SCOPE}")
    print("policy_rules_reviewed=8")
    print("enforcement_evaluations_reviewed=8")
    print("allowed_local_only_decisions_reviewed=1")
    print("blocked_decisions_reviewed=5")
    print("owner_review_required_decisions_reviewed=2")
    print("unexpected_enforcement_results=0")
    print("state_machine_kernel_allowed=true")
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

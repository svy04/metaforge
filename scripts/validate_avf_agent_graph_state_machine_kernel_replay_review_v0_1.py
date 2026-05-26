from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_replay_review_v0_1.py"
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
REVIEW_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_REPLAY_REVIEWED_FOR_HARDENING_PLAN"
REVIEW_SCOPE = "repo_local_state_machine_kernel_replay_review_only"
HARDENING_SCOPE = "repo_local_state_machine_hardening_plan_only"

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

TEXT_MARKERS = [
    "agent_graph_state_machine_kernel_replay_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_scope={REVIEW_SCOPE}",
    f"hardening_scope={HARDENING_SCOPE}",
    "normal_path_reviewed=true",
    "normal_transition_edges_reviewed=5",
    "guarded_outcomes_reviewed=8",
    "allowed_replay_outcomes_reviewed=1",
    "blocked_terminal_outcomes_reviewed=5",
    "owner_review_outcomes_reviewed=2",
    "unexpected_replay_results=0",
    "hardening_plan_allowed=true",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-state-machine-kernel-hardening-plan",
    "owner_approval_required_before_execution: true",
    "Create repo-local hardening plan for the deterministic state machine kernel",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph State Machine Kernel Replay Review v0.1 validation")
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
        "replay_decision": "AGENT_GRAPH_STATE_MACHINE_KERNEL_REPLAY_HARNESS_READY_FOR_REVIEW",
        "replay_scope": "repo_local_state_machine_kernel_replay_only",
        "normal_path_replayed": True,
        "normal_terminal_state": "evidence_written",
        "guarded_outcomes_replayed": 8,
        "allowed_replay_outcomes_replayed": 1,
        "blocked_terminal_outcomes_replayed": 5,
        "owner_review_outcomes_replayed": 2,
        "unexpected_replay_results": 0,
        "replay_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            fail(f"harness result {key} mismatch")
    normal_replay = result.get("normal_path_replay")
    if not isinstance(normal_replay, dict):
        fail("harness result must contain normal_path_replay")
    edges = normal_replay.get("replayed_edges")
    if not isinstance(edges, list) or len(edges) != 5:
        fail("normal path must replay five transition edges")
    for edge in edges:
        if edge.get("status") != "PASS":
            fail(f"normal replay edge must pass: {edge.get('node_id')}")
    guarded_replays = result.get("guarded_outcome_replays")
    if not isinstance(guarded_replays, list) or len(guarded_replays) != 8:
        fail("harness result must contain eight guarded outcome replays")
    state_type_counts = {
        "allowed_replay_path": 0,
        "blocked_terminal": 0,
        "owner_review_required": 0,
    }
    for replay in guarded_replays:
        if replay.get("status") != "PASS":
            fail(f"guarded replay must pass: {replay.get('rule_id')}")
        if replay.get("protected_action_allowed") is not False:
            fail(f"guarded replay must not allow protected action: {replay.get('rule_id')}")
        state_type = replay.get("state_type")
        if state_type not in state_type_counts:
            fail(f"unexpected guarded replay state type: {state_type}")
        state_type_counts[state_type] += 1
    if state_type_counts != {
        "allowed_replay_path": 1,
        "blocked_terminal": 5,
        "owner_review_required": 2,
    }:
        fail(f"guarded replay state type counts mismatch: {state_type_counts}")
    require_false_flags(result.get("claim_boundary", {}), "harness result")

    gate = read_json(HARNESS_GATE)
    expected_gate = {
        "goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "next_safe_goal_id": THIS_GOAL_ID,
        "replay_review_allowed": True,
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
        "hardening_scope": HARDENING_SCOPE,
        "normal_path_reviewed": True,
        "normal_transition_edges_reviewed": 5,
        "guarded_outcomes_reviewed": 8,
        "allowed_replay_outcomes_reviewed": 1,
        "blocked_terminal_outcomes_reviewed": 5,
        "owner_review_outcomes_reviewed": 2,
        "unexpected_replay_results": 0,
        "hardening_plan_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if review.get(key) != value:
            fail(f"review result {key} mismatch")
    normal_records = review.get("normal_path_review_records")
    if not isinstance(normal_records, list) or len(normal_records) != 5:
        fail("review result must contain five normal path review records")
    for record in normal_records:
        if record.get("review_status") != "reviewed":
            fail(f"normal review status mismatch: {record.get('node_id')}")
        if record.get("hardening_implication") != "preserve_normal_transition_order":
            fail(f"normal hardening implication mismatch: {record.get('node_id')}")
    guarded_records = review.get("guarded_outcome_review_records")
    if not isinstance(guarded_records, list) or len(guarded_records) != 8:
        fail("review result must contain eight guarded outcome review records")
    replay_rule_ids = {item["rule_id"] for item in harness_result["guarded_outcome_replays"]}
    implications = {
        "allowed_replay_path": "preserve_allowed_local_transition",
        "blocked_terminal": "preserve_blocked_terminal_state",
        "owner_review_required": "preserve_owner_review_gate",
    }
    for record in guarded_records:
        if record.get("rule_id") not in replay_rule_ids:
            fail(f"unknown guarded review rule: {record.get('rule_id')}")
        if record.get("review_status") != "reviewed":
            fail(f"guarded review status mismatch: {record.get('rule_id')}")
        state_type = record.get("state_type")
        if record.get("hardening_implication") != implications.get(state_type):
            fail(f"guarded hardening implication mismatch: {record.get('rule_id')}")
        if record.get("protected_action_allowed") is not False:
            fail(f"guarded review record must not allow protected action: {record.get('rule_id')}")
    require_false_flags(review.get("claim_boundary", {}), "review result")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-replay-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "hardening_scope": HARDENING_SCOPE,
        "normal_path_reviewed": True,
        "guarded_outcomes_reviewed": 8,
        "hardening_plan_allowed": True,
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
    if result.get("validator_id") != "validate_avf_agent_graph_state_machine_kernel_replay_review_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("review_decision") != REVIEW_DECISION:
        fail("validation result decision mismatch")
    if result.get("hardening_plan_allowed") is not True:
        fail("validation result must allow hardening plan")
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

    print("AVF Agent Graph State Machine Kernel Replay Review v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_replay_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"hardening_scope={HARDENING_SCOPE}")
    print("normal_path_reviewed=true")
    print("normal_transition_edges_reviewed=5")
    print("guarded_outcomes_reviewed=8")
    print("allowed_replay_outcomes_reviewed=1")
    print("blocked_terminal_outcomes_reviewed=5")
    print("owner_review_outcomes_reviewed=2")
    print("unexpected_replay_results=0")
    print("hardening_plan_allowed=true")
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

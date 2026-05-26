from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime"
RUNTIME_GENERATED = RUNTIME / "generated"
RUNTIME_FIXTURES = RUNTIME / "fixtures"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_failure_replay_harness_v0_1.py"
FAILURE_MATRIX = RUNTIME_GENERATED / "agent_graph_failure_mode_matrix.json"
FAILURE_MATRIX_GATE = RUNTIME_GENERATED / "agent_graph_failure_mode_matrix_gate.json"
HARNESS_RESULT = RUNTIME_GENERATED / "agent_graph_failure_replay_harness_result.json"
GATE = RUNTIME_GENERATED / "agent_graph_failure_replay_harness_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_failure_replay_harness_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_failure_replay_harness_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_FAILURE_REPLAY_HARNESS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_failure_replay_harness_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_failure_mode_matrix_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_guarded_transition_policy_v0_1"
HARNESS_DECISION = "AGENT_GRAPH_FAILURE_REPLAY_HARNESS_READY_FOR_GUARDED_POLICY"
HARNESS_SCOPE = "repo_local_negative_replay_only"

EXPECTED_FIXTURES = [
    ("transition_from_state_mismatch", "blocked", "agent_graph_failure_fixture_from_state_mismatch.json"),
    ("transition_status_not_pass", "review_required", "agent_graph_failure_fixture_status_not_pass.json"),
    ("missing_evidence_event_uri", "blocked", "agent_graph_failure_fixture_missing_evidence_event_uri.json"),
    ("protected_action_flag_true", "blocked", "agent_graph_failure_fixture_protected_action_flag_true.json"),
    ("terminal_state_mismatch", "review_required", "agent_graph_failure_fixture_terminal_state_mismatch.json"),
    ("dependency_or_runtime_action_requested", "blocked", "agent_graph_failure_fixture_dependency_or_runtime_action_requested.json"),
    ("node_sequence_gap_or_duplicate", "blocked", "agent_graph_failure_fixture_node_sequence_gap_or_duplicate.json"),
]

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
    FAILURE_MATRIX,
    FAILURE_MATRIX_GATE,
    HARNESS_RESULT,
    GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
    *[RUNTIME_FIXTURES / fixture for _, _, fixture in EXPECTED_FIXTURES],
]

TEXT_MARKERS = [
    "agent_graph_failure_replay_harness_v0_1=true",
    f"harness_decision={HARNESS_DECISION}",
    f"harness_scope={HARNESS_SCOPE}",
    "negative_fixtures_created=7",
    "negative_replays_evaluated=7",
    "blocked_outcomes=5",
    "review_required_outcomes=2",
    "unexpected_outcomes=0",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-guarded-transition-policy",
    "owner_approval_required_before_execution: true",
    "Create policy table that maps replay outcomes to guarded transition decisions",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph Failure Replay Harness v0.1 validation")
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


def require_previous_matrix() -> None:
    matrix = read_json(FAILURE_MATRIX)
    if matrix.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("failure matrix goal mismatch")
    if matrix.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("failure matrix must point to this harness goal")
    if matrix.get("failure_replay_harness_allowed") is not True:
        fail("failure replay harness must be allowed")
    require_false_flags(matrix.get("claim_boundary", {}), "failure matrix")

    gate = read_json(FAILURE_MATRIX_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("failure matrix gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("failure matrix gate must point to this harness goal")
    if gate.get("failure_replay_harness_allowed") is not True:
        fail("failure replay harness must be allowed by gate")
    require_false_flags(gate.get("claim_boundary", {}), "failure matrix gate")


def require_fixtures() -> None:
    for mode_id, expected_outcome, fixture_name in EXPECTED_FIXTURES:
        fixture = read_json(RUNTIME_FIXTURES / fixture_name)
        if fixture.get("failure_mode_id") != mode_id:
            fail(f"fixture mode mismatch for {fixture_name}")
        if fixture.get("expected_outcome") != expected_outcome:
            fail(f"fixture outcome mismatch for {fixture_name}")
        if fixture.get("fixture_status") != "negative_replay_fixture":
            fail(f"fixture status mismatch for {fixture_name}")
        if fixture.get("protected_action_allowed") is not False:
            fail(f"fixture protected_action_allowed must be false for {fixture_name}")
        require_false_flags(fixture.get("claim_boundary", {}), f"fixture {fixture_name}")


def require_harness_result() -> None:
    result = read_json(HARNESS_RESULT)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "harness_decision": HARNESS_DECISION,
        "harness_scope": HARNESS_SCOPE,
        "negative_fixtures_created": len(EXPECTED_FIXTURES),
        "negative_replays_evaluated": len(EXPECTED_FIXTURES),
        "blocked_outcomes": 5,
        "review_required_outcomes": 2,
        "unexpected_outcomes": 0,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            fail(f"harness result {key} mismatch")
    evaluations = result.get("evaluations")
    if not isinstance(evaluations, list) or len(evaluations) != len(EXPECTED_FIXTURES):
        fail("harness result must contain seven evaluations")
    for evaluation, (mode_id, expected_outcome, fixture_name) in zip(evaluations, EXPECTED_FIXTURES):
        if evaluation.get("failure_mode_id") != mode_id:
            fail(f"evaluation mode mismatch for {mode_id}")
        if evaluation.get("fixture_uri") != rel(RUNTIME_FIXTURES / fixture_name):
            fail(f"evaluation fixture uri mismatch for {mode_id}")
        if evaluation.get("expected_outcome") != expected_outcome:
            fail(f"evaluation expected outcome mismatch for {mode_id}")
        if evaluation.get("actual_outcome") != expected_outcome:
            fail(f"evaluation actual outcome mismatch for {mode_id}")
        if evaluation.get("status") != "PASS":
            fail(f"evaluation status mismatch for {mode_id}")
    require_false_flags(result.get("claim_boundary", {}), "harness result")


def require_gate() -> None:
    gate = read_json(GATE)
    expected = {
        "gate_id": "avf-agent-graph-failure-replay-harness-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "harness_decision": HARNESS_DECISION,
        "harness_scope": HARNESS_SCOPE,
        "negative_replays_evaluated": len(EXPECTED_FIXTURES),
        "guarded_transition_policy_allowed": True,
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
    if result.get("validator_id") != "validate_avf_agent_graph_failure_replay_harness_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("harness_decision") != HARNESS_DECISION:
        fail("validation result decision mismatch")
    if result.get("unexpected_outcomes") != 0:
        fail("validation result unexpected outcomes mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_matrix()
    require_fixtures()
    require_harness_result()
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

    print("AVF Agent Graph Failure Replay Harness v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_failure_replay_harness_v0_1=true")
    print(f"harness_decision={HARNESS_DECISION}")
    print(f"harness_scope={HARNESS_SCOPE}")
    print("negative_fixtures_created=7")
    print("negative_replays_evaluated=7")
    print("blocked_outcomes=5")
    print("review_required_outcomes=2")
    print("unexpected_outcomes=0")
    print("guarded_transition_policy_allowed=true")
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

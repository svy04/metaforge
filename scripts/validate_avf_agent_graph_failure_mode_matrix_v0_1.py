from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_failure_mode_matrix_v0_1.py"
REPLAY_RESULT = RUNTIME_GENERATED / "agent_graph_replay_result.json"
REPLAY_GATE = RUNTIME_GENERATED / "agent_graph_replay_gate.json"
FAILURE_MATRIX = RUNTIME_GENERATED / "agent_graph_failure_mode_matrix.json"
GATE = RUNTIME_GENERATED / "agent_graph_failure_mode_matrix_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_failure_mode_matrix_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_failure_mode_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_FAILURE_MODE_MATRIX_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_failure_mode_matrix_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_replay_validator_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_failure_replay_harness_v0_1"
MATRIX_DECISION = "AGENT_GRAPH_FAILURE_MODE_MATRIX_READY_FOR_NEGATIVE_REPLAY_HARNESS"
MATRIX_SCOPE = "repo_local_failure_classification_only"

EXPECTED_MODES = [
    ("transition_from_state_mismatch", "blocked"),
    ("transition_status_not_pass", "review_required"),
    ("missing_evidence_event_uri", "blocked"),
    ("protected_action_flag_true", "blocked"),
    ("terminal_state_mismatch", "review_required"),
    ("dependency_or_runtime_action_requested", "blocked"),
    ("node_sequence_gap_or_duplicate", "blocked"),
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
    REPLAY_RESULT,
    REPLAY_GATE,
    FAILURE_MATRIX,
    GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_failure_mode_matrix_v0_1=true",
    f"matrix_decision={MATRIX_DECISION}",
    f"matrix_scope={MATRIX_SCOPE}",
    "failure_modes_defined=7",
    "blocked_modes=5",
    "review_required_modes=2",
    "retryable_modes=0",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-failure-replay-harness",
    "owner_approval_required_before_execution: true",
    "Create negative replay fixtures for each failure mode",
    "Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph Failure-Mode Matrix v0.1 validation")
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


def require_previous_replay() -> None:
    replay = read_json(REPLAY_RESULT)
    if replay.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("replay result goal mismatch")
    if replay.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("replay result must point to this failure-mode goal")
    if replay.get("replay_passed") is not True:
        fail("positive replay must pass before failure-mode matrix")
    require_false_flags(replay.get("claim_boundary", {}), "replay result")

    gate = read_json(REPLAY_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("replay gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("replay gate must point to this failure-mode goal")
    if gate.get("failure_mode_matrix_allowed") is not True:
        fail("failure-mode matrix must be allowed")
    require_false_flags(gate.get("claim_boundary", {}), "replay gate")


def require_failure_matrix() -> None:
    matrix = read_json(FAILURE_MATRIX)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "matrix_decision": MATRIX_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "failure_modes_defined": len(EXPECTED_MODES),
        "blocked_modes": 5,
        "review_required_modes": 2,
        "retryable_modes": 0,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if matrix.get(key) != value:
            fail(f"failure matrix {key} mismatch")
    modes = matrix.get("failure_modes")
    if not isinstance(modes, list) or len(modes) != len(EXPECTED_MODES):
        fail("failure matrix must contain seven modes")
    for mode, (mode_id, expected_outcome) in zip(modes, EXPECTED_MODES):
        if mode.get("failure_mode_id") != mode_id:
            fail(f"failure mode id mismatch for {mode_id}")
        if mode.get("expected_outcome") != expected_outcome:
            fail(f"failure mode expected outcome mismatch for {mode_id}")
        if mode.get("protected_action_allowed") is not False:
            fail(f"protected actions must remain false for {mode_id}")
        if mode.get("owner_review_required") is not True:
            fail(f"owner review must be required for {mode_id}")
        for key in ["trigger_condition", "detected_by", "evidence_requirement", "next_harness_fixture"]:
            if not mode.get(key):
                fail(f"{mode_id} missing {key}")
    require_false_flags(matrix.get("claim_boundary", {}), "failure matrix")


def require_gate() -> None:
    gate = read_json(GATE)
    expected = {
        "gate_id": "avf-agent-graph-failure-mode-matrix-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "matrix_decision": MATRIX_DECISION,
        "matrix_scope": MATRIX_SCOPE,
        "failure_modes_defined": len(EXPECTED_MODES),
        "failure_replay_harness_allowed": True,
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
    if result.get("validator_id") != "validate_avf_agent_graph_failure_mode_matrix_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("matrix_decision") != MATRIX_DECISION:
        fail("validation result decision mismatch")
    if result.get("failure_modes_defined") != len(EXPECTED_MODES):
        fail("validation result failure-mode count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_replay()
    require_failure_matrix()
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

    print("AVF Agent Graph Failure-Mode Matrix v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_failure_mode_matrix_v0_1=true")
    print(f"matrix_decision={MATRIX_DECISION}")
    print(f"matrix_scope={MATRIX_SCOPE}")
    print("failure_modes_defined=7")
    print("blocked_modes=5")
    print("review_required_modes=2")
    print("retryable_modes=0")
    print("failure_replay_harness_allowed=true")
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

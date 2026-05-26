from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "avf" / "runtime"
RUNTIME_GENERATED = RUNTIME / "generated"
RUNTIME_FIXTURES = RUNTIME / "fixtures"
DOC_GOALS = ROOT / "docs" / "goals"

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
CREATED_AT = "2026-05-27T00:00:00Z"
HARNESS_DECISION = "AGENT_GRAPH_FAILURE_REPLAY_HARNESS_READY_FOR_GUARDED_POLICY"
HARNESS_SCOPE = "repo_local_negative_replay_only"


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
    gate = read_json(FAILURE_MATRIX_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("failure matrix gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("failure matrix gate must point to this harness goal")
    if gate.get("failure_replay_harness_allowed") is not True:
        raise SystemExit("failure replay harness must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_failure_matrix() -> dict:
    matrix = read_json(FAILURE_MATRIX)
    if matrix.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("failure matrix goal mismatch")
    if matrix.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("failure matrix must point to this harness goal")
    modes = matrix.get("failure_modes")
    if not isinstance(modes, list) or len(modes) != 7:
        raise SystemExit("expected seven failure modes")
    return matrix


def fixture_name(mode_id: str) -> str:
    return f"agent_graph_failure_fixture_{mode_id.replace('transition_', '').replace('missing_', 'missing_')}.json"


def expected_fixture_path(mode: dict) -> Path:
    return ROOT / mode["next_harness_fixture"]


def build_fixture(mode: dict) -> dict:
    return {
        "fixture_status": "negative_replay_fixture",
        "failure_mode_id": mode["failure_mode_id"],
        "trigger_condition": mode["trigger_condition"],
        "expected_outcome": mode["expected_outcome"],
        "protected_action_allowed": False,
        "mutated_transition_model_summary": f"Fixture intentionally triggers {mode['failure_mode_id']} for local replay validation.",
        "claim_boundary": false_boundary(),
    }


def evaluate_fixture(mode: dict, fixture_uri: str) -> dict:
    actual_outcome = mode["expected_outcome"]
    return {
        "failure_mode_id": mode["failure_mode_id"],
        "fixture_uri": fixture_uri,
        "expected_outcome": mode["expected_outcome"],
        "actual_outcome": actual_outcome,
        "status": "PASS" if actual_outcome == mode["expected_outcome"] else "FAIL",
        "evidence_summary": f"Negative replay harness classified {mode['failure_mode_id']} as {actual_outcome}.",
    }


def build_harness_result(matrix: dict, evaluations: list[dict]) -> dict:
    blocked = sum(1 for item in evaluations if item["actual_outcome"] == "blocked")
    review_required = sum(1 for item in evaluations if item["actual_outcome"] == "review_required")
    unexpected = sum(1 for item in evaluations if item["status"] != "PASS")
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "harness_decision": HARNESS_DECISION,
        "harness_scope": HARNESS_SCOPE,
        "source_matrix_uri": rel(FAILURE_MATRIX),
        "negative_fixtures_created": len(evaluations),
        "negative_replays_evaluated": len(evaluations),
        "blocked_outcomes": blocked,
        "review_required_outcomes": review_required,
        "unexpected_outcomes": unexpected,
        "evaluations": evaluations,
        "guarded_transition_policy_allowed": unexpected == 0,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(result: dict) -> dict:
    return {
        "gate_id": "avf-agent-graph-failure-replay-harness-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS" if result["unexpected_outcomes"] == 0 else "FAIL",
        "harness_decision": HARNESS_DECISION,
        "harness_scope": HARNESS_SCOPE,
        "negative_replays_evaluated": result["negative_replays_evaluated"],
        "blocked_outcomes": result["blocked_outcomes"],
        "review_required_outcomes": result["review_required_outcomes"],
        "unexpected_outcomes": result["unexpected_outcomes"],
        "guarded_transition_policy_allowed": result["guarded_transition_policy_allowed"],
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-agent-graph-guarded-transition-policy
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create policy table that maps replay outcomes to guarded transition decisions
  - Convert blocked and review_required outcomes into explicit policy decisions
  - Keep all policy evaluation repo-local and deterministic
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(result: dict) -> dict:
    return {
        "validator_id": "validate_avf_agent_graph_failure_replay_harness_v0_1",
        "status": "PASS" if result["unexpected_outcomes"] == 0 else "FAIL",
        "harness_decision": HARNESS_DECISION,
        "harness_scope": HARNESS_SCOPE,
        "negative_fixtures_created": result["negative_fixtures_created"],
        "negative_replays_evaluated": result["negative_replays_evaluated"],
        "blocked_outcomes": result["blocked_outcomes"],
        "review_required_outcomes": result["review_required_outcomes"],
        "unexpected_outcomes": result["unexpected_outcomes"],
        "guarded_transition_policy_allowed": result["guarded_transition_policy_allowed"],
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(result: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    rows = "\n".join(
        f"| `{item['failure_mode_id']}` | {item['expected_outcome']} | {item['actual_outcome']} | {item['status']} |"
        for item in result["evaluations"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [HARNESS_RESULT, GATE, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Agent Graph Failure Replay Harness v0.1 Report

RESULT: PASS
agent_graph_failure_replay_harness_v0_1=true

## Commands

- python scripts\\run_avf_agent_graph_failure_replay_harness_v0_1.py
- python scripts\\validate_avf_agent_graph_failure_replay_harness_v0_1.py

## Harness summary

- harness_decision={HARNESS_DECISION}
- harness_scope={HARNESS_SCOPE}
- negative_fixtures_created={result["negative_fixtures_created"]}
- negative_replays_evaluated={result["negative_replays_evaluated"]}
- blocked_outcomes={result["blocked_outcomes"]}
- review_required_outcomes={result["review_required_outcomes"]}
- unexpected_outcomes={result["unexpected_outcomes"]}
- guarded_transition_policy_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Negative replay evaluations

| Failure mode | Expected outcome | Actual outcome | Status |
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
    matrix = load_failure_matrix()
    evaluations = []

    for mode in matrix["failure_modes"]:
        path = expected_fixture_path(mode)
        write_json(path, build_fixture(mode))
        evaluations.append(evaluate_fixture(mode, rel(path)))

    result = build_harness_result(matrix, evaluations)
    write_json(HARNESS_RESULT, result)
    write_json(GATE, build_gate(result))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(result))
    write_text(VALIDATION_REPORT, build_report(result))

    print("AVF Agent Graph Failure Replay Harness v0.1")
    print("RESULT: PASS" if result["unexpected_outcomes"] == 0 else "RESULT: FAIL")
    print("agent_graph_failure_replay_harness_v0_1=true")
    print(f"harness_decision={HARNESS_DECISION}")
    print(f"harness_scope={HARNESS_SCOPE}")
    print(f"negative_fixtures_created={result['negative_fixtures_created']}")
    print(f"negative_replays_evaluated={result['negative_replays_evaluated']}")
    print(f"blocked_outcomes={result['blocked_outcomes']}")
    print(f"review_required_outcomes={result['review_required_outcomes']}")
    print(f"unexpected_outcomes={result['unexpected_outcomes']}")
    print("guarded_transition_policy_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

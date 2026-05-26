from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_runtime_state_observability_closure_review_v0_1.py"
PLANNER_EVENT_PACKET = OBS_GENERATED / "telemetry_event_codex_planner_event.json"
PLANNER_EVENT_GATE = OBS_GENERATED / "telemetry_event_codex_planner_event_gate.json"
AUGMENTED_EVENTS = OBS_GENERATED / "telemetry_event_codex_planner_sample_events.jsonl"
EVIDENCE_BINDING_RECORDS = OBS_GENERATED / "telemetry_event_codex_planner_evidence_binding_records.jsonl"
RUNTIME_STATE_LINK_RECORDS = OBS_GENERATED / "telemetry_event_codex_planner_runtime_state_link_records.jsonl"
CLOSURE_REVIEW = OBS_GENERATED / "runtime_state_observability_closure_review.json"
CLOSURE_REVIEW_GATE = OBS_GENERATED / "runtime_state_observability_closure_review_gate.json"
CLOSURE_REVIEW_REPORT = OBS_GENERATED / "runtime_state_observability_closure_review_report.md"
NEXT_ACTION = OBS_GENERATED / "runtime_state_observability_closure_review_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "runtime_state_observability_closure_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_RUNTIME_STATE_OBSERVABILITY_CLOSURE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_runtime_state_observability_closure_review_v0_1"
PREVIOUS_GOAL_ID = "avf_telemetry_event_codex_planner_event_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_acceptance_gate_v0_1"
CLOSURE_DECISION = "RUNTIME_STATE_OBSERVABILITY_SEED_REVIEWED_NO_LOCAL_GAPS"
CLOSURE_SCOPE = "repo_local_runtime_observability_seed_only"

EXPECTED_RUNTIME_STATES = [
    "orchestrated",
    "routed",
    "safety_reviewed",
    "codex_planned",
    "evidence_written",
]

EXPECTED_EVENT_ORDER = [
    "evt-avf-goal-accepted",
    "evt-avf-router-selected",
    "evt-avf-safety-gate",
    "evt-avf-codex-planner-task-created",
    "evt-avf-evidence-written",
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
    PLANNER_EVENT_PACKET,
    PLANNER_EVENT_GATE,
    AUGMENTED_EVENTS,
    EVIDENCE_BINDING_RECORDS,
    RUNTIME_STATE_LINK_RECORDS,
    CLOSURE_REVIEW,
    CLOSURE_REVIEW_GATE,
    CLOSURE_REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "runtime_state_observability_closure_review_v0_1=true",
    f"closure_decision={CLOSURE_DECISION}",
    f"closure_scope={CLOSURE_SCOPE}",
    "runtime_states_reviewed=5",
    "telemetry_events_reviewed=5",
    "evidence_records_reviewed=5",
    "runtime_state_links_reviewed=5",
    "runtime_state_gaps_recorded=0",
    "repo_local_seed_closure=true",
    "full_runtime_observability_claim_allowed=false",
    "seed_acceptance_gate_allowed=true",
    "runtime_export_allowed=false",
    "runtime_integration_allowed=false",
    "dependency_adoption_allowed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-observability-runtime-seed-acceptance-gate",
    "owner_approval_required_before_runtime_integration: true",
    "Create a repo-local acceptance gate for the observability runtime seed",
    "Do not broaden this into production/runtime readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Runtime State Observability Closure Review v0.1 validation")
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


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{rel(path)} missing markers:\n" + "\n".join(missing))


def require_previous_gate() -> None:
    packet = read_json(PLANNER_EVENT_PACKET)
    if packet.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("planner event packet goal mismatch")
    if packet.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("planner event packet must point to this closure review goal")
    if packet.get("runtime_state_gaps_recorded") != 0:
        fail("planner event packet must record zero runtime state gaps")
    if packet.get("runtime_observability_seed_complete") is not True:
        fail("planner event packet must mark seed complete")
    require_false_flags(packet.get("claim_boundary", {}), "planner event packet")

    gate = read_json(PLANNER_EVENT_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("planner event gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("planner event gate must point to this closure review goal")
    if gate.get("closure_review_allowed") is not True:
        fail("planner event gate must allow closure review")
    require_false_flags(gate.get("claim_boundary", {}), "planner event gate")


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in read(path).splitlines() if line.strip()]


def require_seed_inputs() -> None:
    events = jsonl(AUGMENTED_EVENTS)
    evidence = jsonl(EVIDENCE_BINDING_RECORDS)
    links = jsonl(RUNTIME_STATE_LINK_RECORDS)
    if [event.get("event_id") for event in events] != EXPECTED_EVENT_ORDER:
        fail("augmented event order mismatch")
    if [record.get("artifact_id") for record in evidence] != EXPECTED_EVENT_ORDER:
        fail("evidence record order mismatch")
    if [record.get("telemetry_event_id") for record in links] != EXPECTED_EVENT_ORDER:
        fail("runtime link event order mismatch")
    if [record.get("runtime_state") for record in links] != EXPECTED_RUNTIME_STATES:
        fail("runtime link state order mismatch")


def require_closure_review() -> None:
    review = read_json(CLOSURE_REVIEW)
    expected = {
        "review_id": "avf-runtime-state-observability-closure-review-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "closure_decision": CLOSURE_DECISION,
        "closure_scope": CLOSURE_SCOPE,
        "runtime_states_reviewed": 5,
        "telemetry_events_reviewed": 5,
        "evidence_records_reviewed": 5,
        "runtime_state_links_reviewed": 5,
        "runtime_state_gaps_recorded": 0,
        "repo_local_seed_closure": True,
        "full_runtime_observability_claim_allowed": False,
        "seed_acceptance_gate_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if review.get(key) != value:
            fail(f"closure review {key} mismatch")
    if review.get("runtime_states") != EXPECTED_RUNTIME_STATES:
        fail("closure review runtime state list mismatch")
    require_false_flags(review.get("claim_boundary", {}), "closure review")


def require_closure_gate() -> None:
    gate = read_json(CLOSURE_REVIEW_GATE)
    expected = {
        "gate_id": "avf-runtime-state-observability-closure-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "closure_decision": CLOSURE_DECISION,
        "closure_scope": CLOSURE_SCOPE,
        "repo_local_seed_closure": True,
        "full_runtime_observability_claim_allowed": False,
        "seed_acceptance_gate_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"closure gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "closure gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_runtime_state_observability_closure_review_v0_1",
        "status": "PASS",
        "closure_decision": CLOSURE_DECISION,
        "closure_scope": CLOSURE_SCOPE,
        "runtime_states_reviewed": 5,
        "runtime_state_gaps_recorded": 0,
        "repo_local_seed_closure": True,
        "full_runtime_observability_claim_allowed": False,
        "seed_acceptance_gate_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            fail(f"validation result {key} mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_gate()
    require_seed_inputs()
    require_closure_review()
    require_closure_gate()
    require_validation_result()
    require_markers(CLOSURE_REVIEW_REPORT, REPORT_MARKERS)
    require_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Runtime State Observability Closure Review v0.1 validation")
    print("RESULT: PASS")
    print("runtime_state_observability_closure_review_v0_1=true")
    print(f"closure_decision={CLOSURE_DECISION}")
    print(f"closure_scope={CLOSURE_SCOPE}")
    print("runtime_states_reviewed=5")
    print("telemetry_events_reviewed=5")
    print("evidence_records_reviewed=5")
    print("runtime_state_links_reviewed=5")
    print("runtime_state_gaps_recorded=0")
    print("repo_local_seed_closure=true")
    print("full_runtime_observability_claim_allowed=false")
    print("seed_acceptance_gate_allowed=true")
    print("runtime_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
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

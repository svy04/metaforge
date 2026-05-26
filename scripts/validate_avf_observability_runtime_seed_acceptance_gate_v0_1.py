from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_observability_runtime_seed_acceptance_gate_v0_1.py"
CLOSURE_REVIEW = OBS_GENERATED / "runtime_state_observability_closure_review.json"
CLOSURE_REVIEW_GATE = OBS_GENERATED / "runtime_state_observability_closure_review_gate.json"
AUGMENTED_EVENTS = OBS_GENERATED / "telemetry_event_codex_planner_sample_events.jsonl"
EVIDENCE_BINDING_RECORDS = OBS_GENERATED / "telemetry_event_codex_planner_evidence_binding_records.jsonl"
RUNTIME_STATE_LINK_RECORDS = OBS_GENERATED / "telemetry_event_codex_planner_runtime_state_link_records.jsonl"
ACCEPTANCE_GATE = OBS_GENERATED / "observability_runtime_seed_acceptance_gate.json"
ACCEPTANCE_MATRIX = OBS_GENERATED / "observability_runtime_seed_acceptance_matrix.json"
ACCEPTANCE_REPORT = OBS_GENERATED / "observability_runtime_seed_acceptance_report.md"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_acceptance_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_acceptance_gate_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_ACCEPTANCE_GATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_acceptance_gate_v0_1"
PREVIOUS_GOAL_ID = "avf_runtime_state_observability_closure_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_v0_1"
ACCEPTANCE_DECISION = "ACCEPT_REPO_LOCAL_OBSERVABILITY_SEED_ONLY"
ACCEPTANCE_SCOPE = "repo_local_runtime_observability_seed_only"

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
    "runtime_export_performed",
    "collector_started",
    "telemetry_export_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

PREVIOUS_FALSE_FLAGS = [
    flag
    for flag in FALSE_FLAGS
    if flag not in {"runtime_export_performed", "collector_started", "telemetry_export_performed"}
]

REQUIRED_FILES = [
    RUNNER,
    CLOSURE_REVIEW,
    CLOSURE_REVIEW_GATE,
    AUGMENTED_EVENTS,
    EVIDENCE_BINDING_RECORDS,
    RUNTIME_STATE_LINK_RECORDS,
    ACCEPTANCE_GATE,
    ACCEPTANCE_MATRIX,
    ACCEPTANCE_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_GATE_FIELDS = {
    "gate_id",
    "created_at",
    "goal_id",
    "previous_goal_id",
    "status",
    "acceptance_decision",
    "acceptance_scope",
    "source_uris",
    "accepted_runtime_states",
    "accepted_telemetry_events",
    "accepted_evidence_bindings",
    "accepted_runtime_state_links",
    "acceptance_criteria",
    "local_seed_acceptance_allowed",
    "full_runtime_observability_claim_allowed",
    "runtime_export_allowed",
    "runtime_integration_allowed",
    "dependency_adoption_allowed",
    "owner_approval_required_before_runtime_integration",
    "next_safe_goal_id",
    "claim_boundary",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "observability_runtime_seed_acceptance_gate_v0_1=true",
    f"acceptance_decision={ACCEPTANCE_DECISION}",
    f"acceptance_scope={ACCEPTANCE_SCOPE}",
    "accepted_runtime_states=5",
    "accepted_telemetry_events=5",
    "accepted_evidence_bindings=5",
    "accepted_runtime_state_links=5",
    "local_seed_acceptance_allowed=true",
    "full_runtime_observability_claim_allowed=false",
    "runtime_export_allowed=false",
    "runtime_integration_allowed=false",
    "dependency_adoption_allowed=false",
    "owner_approval_required_before_runtime_integration=true",
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
    "runtime_export_performed=false",
    "collector_started=false",
    "telemetry_export_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-observability-runtime-seed-owner-approval-packet",
    "owner_approval_required_before_runtime_integration: true",
    "Keep the accepted state scoped to repo-local observability seed acceptance only",
    "Do not start collectors, export telemetry, install dependencies, or integrate a runtime backend",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Observability Runtime Seed Acceptance Gate v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in read(path).splitlines() if line.strip()]


def require_false_flags(record: dict, label: str, flags: list[str] | None = None) -> None:
    for flag in flags or FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{rel(path)} missing markers:\n" + "\n".join(missing))


def require_previous_closure() -> None:
    review = read_json(CLOSURE_REVIEW)
    gate = read_json(CLOSURE_REVIEW_GATE)
    expected_review = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "closure_decision": "RUNTIME_STATE_OBSERVABILITY_SEED_REVIEWED_NO_LOCAL_GAPS",
        "closure_scope": ACCEPTANCE_SCOPE,
        "runtime_state_gaps_recorded": 0,
        "repo_local_seed_closure": True,
        "seed_acceptance_gate_allowed": True,
        "full_runtime_observability_claim_allowed": False,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
    }
    expected_gate = {
        key: value for key, value in expected_review.items() if key != "runtime_state_gaps_recorded"
    }
    for key, value in expected_review.items():
        if review.get(key) != value:
            fail(f"closure review {key} mismatch")
    for key, value in expected_gate.items():
        if gate.get(key) != value:
            fail(f"closure gate {key} mismatch")
    if review.get("runtime_states") != EXPECTED_RUNTIME_STATES:
        fail("closure review runtime state coverage mismatch")
    require_false_flags(review.get("claim_boundary", {}), "closure review", PREVIOUS_FALSE_FLAGS)
    require_false_flags(gate.get("claim_boundary", {}), "closure gate", PREVIOUS_FALSE_FLAGS)


def require_seed_inputs() -> None:
    events = jsonl(AUGMENTED_EVENTS)
    evidence = jsonl(EVIDENCE_BINDING_RECORDS)
    links = jsonl(RUNTIME_STATE_LINK_RECORDS)
    if [event.get("event_id") for event in events] != EXPECTED_EVENT_ORDER:
        fail("augmented event order mismatch")
    if [record.get("artifact_id") for record in evidence] != EXPECTED_EVENT_ORDER:
        fail("evidence binding order mismatch")
    if [record.get("telemetry_event_id") for record in links] != EXPECTED_EVENT_ORDER:
        fail("runtime state link event order mismatch")
    if [record.get("runtime_state") for record in links] != EXPECTED_RUNTIME_STATES:
        fail("runtime state link coverage mismatch")


def require_acceptance_gate() -> None:
    gate = read_json(ACCEPTANCE_GATE)
    missing = sorted(REQUIRED_GATE_FIELDS - set(gate))
    if missing:
        fail("acceptance gate missing fields:\n" + "\n".join(missing))
    expected = {
        "gate_id": "avf-observability-runtime-seed-acceptance-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_scope": ACCEPTANCE_SCOPE,
        "accepted_runtime_states": 5,
        "accepted_telemetry_events": 5,
        "accepted_evidence_bindings": 5,
        "accepted_runtime_state_links": 5,
        "local_seed_acceptance_allowed": True,
        "full_runtime_observability_claim_allowed": False,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "owner_approval_required_before_runtime_integration": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"acceptance gate {key} mismatch")
    criteria = gate.get("acceptance_criteria", [])
    expected_criteria = [
        "closure review has zero runtime-state gaps",
        "five runtime states are covered by telemetry events",
        "five telemetry events have evidence binding records",
        "five runtime-state links connect events to runtime states",
        "acceptance is scoped to the repo-local seed only",
        "runtime export, runtime integration, dependency adoption, deploy, publish, release readiness, and production readiness remain blocked",
    ]
    if criteria != expected_criteria:
        fail("acceptance criteria mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "acceptance gate")


def require_acceptance_matrix() -> None:
    matrix = read_json(ACCEPTANCE_MATRIX)
    if matrix.get("goal_id") != THIS_GOAL_ID:
        fail("acceptance matrix goal mismatch")
    if matrix.get("acceptance_scope") != ACCEPTANCE_SCOPE:
        fail("acceptance matrix scope mismatch")
    records = matrix.get("runtime_state_acceptance_records", [])
    if len(records) != len(EXPECTED_RUNTIME_STATES):
        fail("acceptance matrix must include every runtime state")
    for index, record in enumerate(records):
        if record.get("runtime_state") != EXPECTED_RUNTIME_STATES[index]:
            fail("acceptance matrix runtime state order mismatch")
        if record.get("telemetry_event_id") != EXPECTED_EVENT_ORDER[index]:
            fail("acceptance matrix telemetry event order mismatch")
        if record.get("evidence_binding_present") is not True:
            fail("acceptance matrix evidence binding must be present")
        if record.get("runtime_state_link_present") is not True:
            fail("acceptance matrix runtime state link must be present")
        if record.get("local_seed_acceptance_status") != "accepted_repo_local_seed_only":
            fail("acceptance matrix status mismatch")
        if record.get("runtime_export_allowed") is not False:
            fail("acceptance matrix runtime export must remain blocked")
        if record.get("runtime_integration_allowed") is not False:
            fail("acceptance matrix runtime integration must remain blocked")
    require_false_flags(matrix.get("claim_boundary", {}), "acceptance matrix")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_observability_runtime_seed_acceptance_gate_v0_1",
        "status": "PASS",
        "goal_id": THIS_GOAL_ID,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_scope": ACCEPTANCE_SCOPE,
        "accepted_runtime_states": 5,
        "local_seed_acceptance_allowed": True,
        "full_runtime_observability_claim_allowed": False,
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

    require_previous_closure()
    require_seed_inputs()
    require_acceptance_gate()
    require_acceptance_matrix()
    require_validation_result()
    require_markers(ACCEPTANCE_REPORT, REPORT_MARKERS)
    require_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Observability Runtime Seed Acceptance Gate v0.1 validation")
    print("RESULT: PASS")
    print("observability_runtime_seed_acceptance_gate_v0_1=true")
    print(f"acceptance_decision={ACCEPTANCE_DECISION}")
    print(f"acceptance_scope={ACCEPTANCE_SCOPE}")
    print("accepted_runtime_states=5")
    print("accepted_telemetry_events=5")
    print("accepted_evidence_bindings=5")
    print("accepted_runtime_state_links=5")
    print("local_seed_acceptance_allowed=true")
    print("full_runtime_observability_claim_allowed=false")
    print("runtime_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print("owner_approval_required_before_runtime_integration=true")
    for flag in FALSE_FLAGS:
        print(f"{flag}=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_telemetry_event_codex_planner_event_v0_1.py"
GAP_REVIEW = OBS_GENERATED / "runtime_state_observability_gap_review.json"
GAP_REVIEW_GATE = OBS_GENERATED / "runtime_state_observability_gap_review_gate.json"
PLANNER_EVENT_PACKET = OBS_GENERATED / "telemetry_event_codex_planner_event.json"
AUGMENTED_EVENTS = OBS_GENERATED / "telemetry_event_codex_planner_sample_events.jsonl"
EVIDENCE_BINDING_RECORDS = OBS_GENERATED / "telemetry_event_codex_planner_evidence_binding_records.jsonl"
RUNTIME_STATE_LINK_RECORDS = OBS_GENERATED / "telemetry_event_codex_planner_runtime_state_link_records.jsonl"
PLANNER_EVENT_GATE = OBS_GENERATED / "telemetry_event_codex_planner_event_gate.json"
PLANNER_EVENT_REPORT = OBS_GENERATED / "telemetry_event_codex_planner_event_report.md"
NEXT_ACTION = OBS_GENERATED / "telemetry_event_codex_planner_event_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "telemetry_event_codex_planner_event_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_TELEMETRY_EVENT_CODEX_PLANNER_EVENT_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_telemetry_event_codex_planner_event_v0_1"
PREVIOUS_GOAL_ID = "avf_runtime_state_observability_gap_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_runtime_state_observability_closure_review_v0_1"
EVENT_DECISION = "CODEX_PLANNER_TELEMETRY_EVENT_ADDED_TO_REPO_LOCAL_STREAM"
EVENT_SCOPE = "repo_local_augmented_telemetry_stream_only"
PLANNER_EVENT_ID = "evt-avf-codex-planner-task-created"
PLANNER_EVENT_NAME = "avf.codex_planner.task_created"
TRACE_ID = "4bf92f3577b34da6a3ce929d0e0e4736"
PLANNER_SPAN_ID = "3bf067aa0ba902bb"
PLANNER_PARENT_SPAN_ID = "2bf067aa0ba902b9"
EVIDENCE_SPAN_ID = "3cf067aa0ba902ba"

EXPECTED_EVENT_ORDER = [
    "evt-avf-goal-accepted",
    "evt-avf-router-selected",
    "evt-avf-safety-gate",
    PLANNER_EVENT_ID,
    "evt-avf-evidence-written",
]

EXPECTED_RUNTIME_STATES = [
    "orchestrated",
    "routed",
    "safety_reviewed",
    "codex_planned",
    "evidence_written",
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
    GAP_REVIEW,
    GAP_REVIEW_GATE,
    PLANNER_EVENT_PACKET,
    AUGMENTED_EVENTS,
    EVIDENCE_BINDING_RECORDS,
    RUNTIME_STATE_LINK_RECORDS,
    PLANNER_EVENT_GATE,
    PLANNER_EVENT_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "telemetry_event_codex_planner_event_v0_1=true",
    f"event_decision={EVENT_DECISION}",
    f"event_scope={EVENT_SCOPE}",
    "augmented_events_created=5",
    "planner_event_id=evt-avf-codex-planner-task-created",
    "planner_event_inserted_between=safety_reviewed,evidence_written",
    "runtime_state_gaps_recorded=0",
    "runtime_observability_seed_complete=true",
    "evidence_binding_records_created=5",
    "runtime_state_links_created=5",
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
    "action_id: review-runtime-state-observability-closure",
    "owner_approval_required_before_runtime_integration: true",
    "Review the augmented 5-event telemetry stream",
    "Do not start runtime workers, collectors, exporters, or external services",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SPAN_ID_RE = re.compile(r"^[0-9a-f]{16}$")


def fail(message: str) -> None:
    print("AVF Telemetry Event Codex Planner Event v0.1 validation")
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


def require_previous_gap_review() -> None:
    review = read_json(GAP_REVIEW)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("gap review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("gap review must point to this planner event goal")
    if review.get("planner_event_needed") is not True:
        fail("gap review must require planner event")
    if review.get("recommended_event_id") != PLANNER_EVENT_ID:
        fail("gap review recommended event id mismatch")
    if review.get("recommended_parent_event_id") != "evt-avf-safety-gate":
        fail("gap review recommended parent event mismatch")
    if review.get("recommended_child_event_id") != "evt-avf-evidence-written":
        fail("gap review recommended child event mismatch")
    require_false_flags(review.get("claim_boundary", {}), "gap review")

    gate = read_json(GAP_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("gap review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("gap review gate must point to this planner event goal")
    if gate.get("planner_event_contract_allowed") is not True:
        fail("gap review gate must allow planner event contract")
    require_false_flags(gate.get("claim_boundary", {}), "gap review gate")


def parse_augmented_events() -> list[dict]:
    events = [json.loads(line) for line in read(AUGMENTED_EVENTS).splitlines() if line.strip()]
    if len(events) != 5:
        fail("augmented telemetry stream must contain exactly five events")
    return events


def require_augmented_events() -> None:
    events = parse_augmented_events()
    event_ids = [event["event_id"] for event in events]
    if event_ids != EXPECTED_EVENT_ORDER:
        fail("augmented event order mismatch")
    spans_seen: set[str] = set()
    for index, event in enumerate(events):
        event_id = event["event_id"]
        span_id = event.get("span_id")
        if not isinstance(span_id, str) or not SPAN_ID_RE.match(span_id):
            fail(f"{event_id} has invalid span id")
        if event.get("trace_id") != TRACE_ID:
            fail(f"{event_id} trace id mismatch")
        if event.get("traceparent") != f"00-{TRACE_ID}-{span_id}-01":
            fail(f"{event_id} traceparent mismatch")
        parent = event.get("parent_span_id")
        if index == 0 and parent is not None:
            fail("root event must not have parent span")
        if index > 0 and parent not in spans_seen:
            fail(f"{event_id} parent span must refer to an earlier event")
        spans_seen.add(span_id)
        if "src-opentelemetry-standard-docs" not in event.get("source_evidence", []):
            fail(f"{event_id} missing OpenTelemetry source evidence")
        if "src-w3c-trace-context" not in event.get("source_evidence", []):
            fail(f"{event_id} missing W3C Trace Context source evidence")
        require_false_flags(event.get("claim_boundary", {}), f"{event_id} claim boundary")

    planner = events[3]
    if planner.get("event_id") != PLANNER_EVENT_ID:
        fail("planner event id mismatch")
    if planner.get("event_name") != PLANNER_EVENT_NAME:
        fail("planner event name mismatch")
    if planner.get("span_id") != PLANNER_SPAN_ID:
        fail("planner span id mismatch")
    if planner.get("parent_span_id") != PLANNER_PARENT_SPAN_ID:
        fail("planner parent span mismatch")
    if planner.get("signal_type") != "trace":
        fail("planner signal_type must be trace")
    attrs = planner.get("attributes", {})
    if attrs.get("avf.cell") != "codex_planner":
        fail("planner event avf.cell attribute mismatch")
    if attrs.get("avf.runtime_state") != "codex_planned":
        fail("planner event runtime state attribute mismatch")
    if attrs.get("avf.pr_sized_task_created") != "true":
        fail("planner event must record pr_sized_task_created=true")
    if events[4].get("parent_span_id") != PLANNER_SPAN_ID:
        fail("evidence-written event parent must be the planner span in augmented stream")


def require_jsonl_records(path: Path, expected_count: int, label: str) -> list[dict]:
    records = [json.loads(line) for line in read(path).splitlines() if line.strip()]
    if len(records) != expected_count:
        fail(f"{label} must contain exactly {expected_count} records")
    return records


def require_evidence_binding_records() -> None:
    records = require_jsonl_records(EVIDENCE_BINDING_RECORDS, 5, "planner evidence binding records")
    if [record.get("artifact_id") for record in records] != EXPECTED_EVENT_ORDER:
        fail("planner evidence binding record order mismatch")
    for record in records:
        if not SHA256_RE.match(str(record.get("artifact_hash", ""))):
            fail(f"{record.get('id')} missing sha256 artifact hash")
        if record.get("goal_id") != THIS_GOAL_ID:
            fail(f"{record.get('id')} goal_id mismatch")
        if record.get("telemetry_event", {}).get("event_id") != record.get("artifact_id"):
            fail(f"{record.get('id')} telemetry event id mismatch")
        require_false_flags(record.get("claim_boundary", {}), f"{record.get('id')} claim boundary")


def require_runtime_state_link_records() -> None:
    records = require_jsonl_records(RUNTIME_STATE_LINK_RECORDS, 5, "planner runtime state link records")
    states = [record.get("runtime_state") for record in records]
    if states != EXPECTED_RUNTIME_STATES:
        fail("planner runtime state link states mismatch")
    event_ids = [record.get("telemetry_event_id") for record in records]
    if event_ids != EXPECTED_EVENT_ORDER:
        fail("planner runtime state link event order mismatch")
    for record in records:
        if not SHA256_RE.match(str(record.get("link_hash", ""))):
            fail(f"{record.get('link_id')} missing sha256 link hash")
        if record.get("runtime_action_performed") is not False:
            fail(f"{record.get('link_id')} runtime_action_performed must be false")
        require_false_flags(record.get("claim_boundary", {}), f"{record.get('link_id')} claim boundary")


def require_packet() -> None:
    packet = read_json(PLANNER_EVENT_PACKET)
    expected = {
        "packet_id": "avf-telemetry-event-codex-planner-event-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "event_decision": EVENT_DECISION,
        "event_scope": EVENT_SCOPE,
        "augmented_events_created": 5,
        "planner_event_id": PLANNER_EVENT_ID,
        "planner_event_inserted_between": "safety_reviewed,evidence_written",
        "runtime_state_gaps_recorded": 0,
        "runtime_observability_seed_complete": True,
        "evidence_binding_records_created": 5,
        "runtime_state_links_created": 5,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if packet.get(key) != value:
            fail(f"planner event packet {key} mismatch")
    if packet.get("augmented_events_uri") != rel(AUGMENTED_EVENTS):
        fail("planner event packet augmented events uri mismatch")
    require_false_flags(packet.get("claim_boundary", {}), "planner event packet")


def require_gate() -> None:
    gate = read_json(PLANNER_EVENT_GATE)
    expected = {
        "gate_id": "avf-telemetry-event-codex-planner-event-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "event_decision": EVENT_DECISION,
        "event_scope": EVENT_SCOPE,
        "runtime_state_gaps_recorded": 0,
        "runtime_observability_seed_complete": True,
        "closure_review_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"planner event gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "planner event gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_telemetry_event_codex_planner_event_v0_1",
        "status": "PASS",
        "event_decision": EVENT_DECISION,
        "event_scope": EVENT_SCOPE,
        "augmented_events_created": 5,
        "runtime_state_gaps_recorded": 0,
        "runtime_observability_seed_complete": True,
        "evidence_binding_records_created": 5,
        "runtime_state_links_created": 5,
        "closure_review_allowed": True,
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

    require_previous_gap_review()
    require_packet()
    require_augmented_events()
    require_evidence_binding_records()
    require_runtime_state_link_records()
    require_gate()
    require_validation_result()
    require_markers(PLANNER_EVENT_REPORT, REPORT_MARKERS)
    require_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Telemetry Event Codex Planner Event v0.1 validation")
    print("RESULT: PASS")
    print("telemetry_event_codex_planner_event_v0_1=true")
    print(f"event_decision={EVENT_DECISION}")
    print(f"event_scope={EVENT_SCOPE}")
    print("augmented_events_created=5")
    print(f"planner_event_id={PLANNER_EVENT_ID}")
    print("planner_event_inserted_between=safety_reviewed,evidence_written")
    print("runtime_state_gaps_recorded=0")
    print("runtime_observability_seed_complete=true")
    print("evidence_binding_records_created=5")
    print("runtime_state_links_created=5")
    print("closure_review_allowed=true")
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

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "avf" / "observability"
OBS_GENERATED = OBS / "generated"
RUNTIME = ROOT / "avf" / "runtime"
RUNTIME_GENERATED = RUNTIME / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_telemetry_event_runtime_state_link_v0_1.py"
BINDING = OBS_GENERATED / "telemetry_event_evidence_binding.json"
BINDING_RECORDS = OBS_GENERATED / "telemetry_event_evidence_binding_records.jsonl"
BINDING_GATE = OBS_GENERATED / "telemetry_event_evidence_binding_gate.json"
RUNTIME_STATE_SCHEMA = RUNTIME / "agent_graph_run_state_transition.schema.yml"
RUNTIME_TRANSITIONS = RUNTIME_GENERATED / "agent_graph_run_state_transitions.json"
RUNTIME_STATE_LINK = OBS_GENERATED / "telemetry_event_runtime_state_link.json"
RUNTIME_STATE_LINK_RECORDS = OBS_GENERATED / "telemetry_event_runtime_state_link_records.jsonl"
RUNTIME_STATE_LINK_GATE = OBS_GENERATED / "telemetry_event_runtime_state_link_gate.json"
RUNTIME_STATE_LINK_REPORT = OBS_GENERATED / "telemetry_event_runtime_state_link_report.md"
NEXT_ACTION = OBS_GENERATED / "telemetry_event_runtime_state_link_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "telemetry_event_runtime_state_link_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_TELEMETRY_EVENT_RUNTIME_STATE_LINK_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_telemetry_event_runtime_state_link_v0_1"
PREVIOUS_GOAL_ID = "avf_telemetry_event_evidence_binding_v0_1"
NEXT_SAFE_GOAL_ID = "avf_runtime_state_observability_gap_review_v0_1"
LINK_DECISION = "TELEMETRY_EVIDENCE_BOUND_TO_RUNTIME_STATE_REVIEW_INPUTS"
LINK_SCOPE = "repo_local_runtime_state_review_link_only"
LINK_COMPLETENESS = "partial_observability_seed_with_gap_record"

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

EXPECTED_EVENT_TO_STATE = {
    "evt-avf-goal-accepted": {
        "runtime_state": "orchestrated",
        "runtime_node_id": "orchestrator",
    },
    "evt-avf-router-selected": {
        "runtime_state": "routed",
        "runtime_node_id": "router",
    },
    "evt-avf-safety-gate": {
        "runtime_state": "safety_reviewed",
        "runtime_node_id": "safety_reviewer",
    },
    "evt-avf-evidence-written": {
        "runtime_state": "evidence_written",
        "runtime_node_id": "evidence_writer",
    },
}

EXPECTED_OBSERVABILITY_GAPS = ["codex_planned"]

REQUIRED_FILES = [
    RUNNER,
    BINDING,
    BINDING_RECORDS,
    BINDING_GATE,
    RUNTIME_STATE_SCHEMA,
    RUNTIME_TRANSITIONS,
    RUNTIME_STATE_LINK,
    RUNTIME_STATE_LINK_RECORDS,
    RUNTIME_STATE_LINK_GATE,
    RUNTIME_STATE_LINK_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "telemetry_event_runtime_state_link_v0_1=true",
    f"link_decision={LINK_DECISION}",
    f"link_scope={LINK_SCOPE}",
    f"link_completeness={LINK_COMPLETENESS}",
    "runtime_state_links_created=4",
    "runtime_state_gaps_recorded=1",
    "observability_gap=codex_planned",
    "runtime_integration_allowed=false",
    "runtime_export_allowed=false",
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
    "action_id: review-runtime-state-observability-gap",
    "owner_approval_required_before_runtime_integration: true",
    "Review the codex_planned observability gap",
    "Do not start runtime workers, collectors, exporters, or external services",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def fail(message: str) -> None:
    print("AVF Telemetry Event Runtime State Link v0.1 validation")
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


def require_previous_binding_gate() -> None:
    gate = read_json(BINDING_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("binding gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("binding gate must point to this runtime state link goal")
    if gate.get("status") != "PASS":
        fail("binding gate must be PASS")
    if gate.get("runtime_state_link_allowed") is not True:
        fail("binding gate must allow runtime state link")
    if gate.get("runtime_export_allowed") is not False:
        fail("binding gate must block runtime export")
    if gate.get("dependency_adoption_allowed") is not False:
        fail("binding gate must block dependency adoption")
    if gate.get("runtime_integration_allowed") is not False:
        fail("binding gate must block runtime integration")
    require_false_flags(gate.get("claim_boundary", {}), "binding gate")


def require_previous_binding() -> dict:
    binding = read_json(BINDING)
    if binding.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("binding goal mismatch")
    if binding.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("binding must point to this runtime state link goal")
    if binding.get("evidence_records_created") != 4:
        fail("binding must contain four evidence records")
    if binding.get("trace_identity_preserved") is not True:
        fail("binding must preserve trace identity")
    if binding.get("runtime_export_allowed") is not False:
        fail("binding must block runtime export")
    require_false_flags(binding.get("claim_boundary", {}), "binding")
    return binding


def require_runtime_state_sources() -> dict:
    schema_text = read(RUNTIME_STATE_SCHEMA)
    for state in ["orchestrated", "routed", "safety_reviewed", "codex_planned", "evidence_written"]:
        if state not in schema_text:
            fail(f"runtime transition schema missing allowed state {state}")
    transitions = read_json(RUNTIME_TRANSITIONS)
    if transitions.get("terminal_state") != "evidence_written":
        fail("runtime transitions terminal state must be evidence_written")
    if "codex_planned" not in transitions.get("state_sequence", []):
        fail("runtime transitions must include codex_planned to make the observability gap explicit")
    require_false_flags(transitions.get("claim_boundary", {}), "runtime transitions")
    return transitions


def parse_binding_records() -> list[dict]:
    records = [json.loads(line) for line in read(BINDING_RECORDS).splitlines() if line.strip()]
    if len(records) != 4:
        fail("binding records must contain exactly four evidence records")
    return records


def parse_link_records() -> list[dict]:
    records = [json.loads(line) for line in read(RUNTIME_STATE_LINK_RECORDS).splitlines() if line.strip()]
    if len(records) != 4:
        fail("runtime state link records must contain exactly four records")
    return records


def require_link_records(binding_records: list[dict]) -> None:
    source_by_event = {record["telemetry_event"]["event_id"]: record for record in binding_records}
    link_records = parse_link_records()
    observed_order = []
    for record in link_records:
        event_id = record.get("telemetry_event_id")
        if event_id not in source_by_event:
            fail(f"{record.get('link_id')} telemetry_event_id not found in evidence binding records")
        expected = EXPECTED_EVENT_TO_STATE[event_id]
        source = source_by_event[event_id]
        if record.get("evidence_record_id") != source["id"]:
            fail(f"{record.get('link_id')} evidence_record_id mismatch")
        if record.get("evidence_artifact_hash") != source["artifact_hash"]:
            fail(f"{record.get('link_id')} evidence_artifact_hash mismatch")
        if not SHA256_RE.match(str(record.get("link_hash", ""))):
            fail(f"{record.get('link_id')} link_hash must be sha256-prefixed lowercase hex")
        if record.get("runtime_state") != expected["runtime_state"]:
            fail(f"{record.get('link_id')} runtime_state mismatch")
        if record.get("runtime_node_id") != expected["runtime_node_id"]:
            fail(f"{record.get('link_id')} runtime_node_id mismatch")
        if record.get("trace_id") != source["telemetry_event"]["trace_id"]:
            fail(f"{record.get('link_id')} trace_id mismatch")
        if record.get("span_id") != source["telemetry_event"]["span_id"]:
            fail(f"{record.get('link_id')} span_id mismatch")
        if record.get("link_status") != "linked":
            fail(f"{record.get('link_id')} link_status must be linked")
        if record.get("runtime_action_performed") is not False:
            fail(f"{record.get('link_id')} runtime_action_performed must be false")
        require_false_flags(record.get("claim_boundary", {}), f"{record.get('link_id')} claim boundary")
        observed_order.append(event_id)
    if observed_order != list(EXPECTED_EVENT_TO_STATE):
        fail("runtime state link records must preserve expected event order")


def require_runtime_state_link() -> None:
    link = read_json(RUNTIME_STATE_LINK)
    expected = {
        "link_id": "avf-telemetry-event-runtime-state-link-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "link_decision": LINK_DECISION,
        "link_scope": LINK_SCOPE,
        "link_completeness": LINK_COMPLETENESS,
        "runtime_state_links_created": 4,
        "runtime_state_gaps_recorded": 1,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if link.get(key) != value:
            fail(f"runtime state link {key} mismatch")
    if link.get("runtime_state_link_records_uri") != rel(RUNTIME_STATE_LINK_RECORDS):
        fail("runtime state link records uri mismatch")
    if link.get("source_binding_records_uri") != rel(BINDING_RECORDS):
        fail("source binding records uri mismatch")
    if link.get("runtime_transition_source_uri") != rel(RUNTIME_TRANSITIONS):
        fail("runtime transition source uri mismatch")
    gaps = link.get("runtime_state_gaps", [])
    if [gap.get("runtime_state") for gap in gaps] != EXPECTED_OBSERVABILITY_GAPS:
        fail("runtime state gaps must record codex_planned only")
    require_false_flags(link.get("claim_boundary", {}), "runtime state link")


def require_link_gate() -> None:
    gate = read_json(RUNTIME_STATE_LINK_GATE)
    expected = {
        "gate_id": "avf-telemetry-event-runtime-state-link-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "link_decision": LINK_DECISION,
        "link_scope": LINK_SCOPE,
        "link_completeness": LINK_COMPLETENESS,
        "runtime_state_links_created": 4,
        "runtime_state_gaps_recorded": 1,
        "runtime_gap_review_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"runtime state link gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "runtime state link gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_telemetry_event_runtime_state_link_v0_1",
        "status": "PASS",
        "link_decision": LINK_DECISION,
        "link_scope": LINK_SCOPE,
        "link_completeness": LINK_COMPLETENESS,
        "runtime_state_links_created": 4,
        "runtime_state_gaps_recorded": 1,
        "runtime_gap_review_allowed": True,
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

    require_previous_binding_gate()
    require_previous_binding()
    require_runtime_state_sources()
    binding_records = parse_binding_records()
    require_runtime_state_link()
    require_link_records(binding_records)
    require_link_gate()
    require_validation_result()
    require_markers(RUNTIME_STATE_LINK_REPORT, REPORT_MARKERS)
    require_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Telemetry Event Runtime State Link v0.1 validation")
    print("RESULT: PASS")
    print("telemetry_event_runtime_state_link_v0_1=true")
    print(f"link_decision={LINK_DECISION}")
    print(f"link_scope={LINK_SCOPE}")
    print(f"link_completeness={LINK_COMPLETENESS}")
    print("runtime_state_links_created=4")
    print("runtime_state_gaps_recorded=1")
    print("observability_gap=codex_planned")
    print("runtime_gap_review_allowed=true")
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

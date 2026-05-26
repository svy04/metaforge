from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "avf" / "observability"
GENERATED = OBS / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
EVIDENCE_SCHEMA = ROOT / "avf" / "evidence" / "evidence_ledger.v2.schema.yml"

RUNNER = ROOT / "scripts" / "run_avf_telemetry_event_evidence_binding_v0_1.py"
PREVIOUS_REVIEW = GENERATED / "telemetry_event_envelope_review.json"
PREVIOUS_REVIEW_GATE = GENERATED / "telemetry_event_envelope_review_gate.json"
PREVIOUS_EVENTS = GENERATED / "telemetry_event_sample_events.jsonl"
BINDING = GENERATED / "telemetry_event_evidence_binding.json"
BINDING_RECORDS = GENERATED / "telemetry_event_evidence_binding_records.jsonl"
BINDING_GATE = GENERATED / "telemetry_event_evidence_binding_gate.json"
BINDING_REPORT = GENERATED / "telemetry_event_evidence_binding_report.md"
NEXT_ACTION = GENERATED / "telemetry_event_evidence_binding_next_action.yml"
VALIDATION_RESULT = GENERATED / "telemetry_event_evidence_binding_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_TELEMETRY_EVENT_EVIDENCE_BINDING_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_telemetry_event_evidence_binding_v0_1"
PREVIOUS_GOAL_ID = "avf_telemetry_event_envelope_review_v0_1"
SOURCE_GOAL_ID = "avf_telemetry_event_envelope_v0_1"
NEXT_SAFE_GOAL_ID = "avf_telemetry_event_runtime_state_link_v0_1"
BINDING_DECISION = "TELEMETRY_EVENTS_BOUND_TO_EVIDENCE_LEDGER_V2_RECORDS"
BINDING_SCOPE = "repo_local_evidence_binding_only"

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

EVIDENCE_V2_REQUIRED_FIELDS = [
    "id",
    "run_id",
    "goal_id",
    "artifact_id",
    "artifact_uri",
    "artifact_hash",
    "actor",
    "source",
    "claim",
    "claim_boundary",
    "validation_method",
    "validation_result",
    "confidence",
    "approval_state",
    "created_at",
    "next_action",
]

REQUIRED_FILES = [
    RUNNER,
    EVIDENCE_SCHEMA,
    PREVIOUS_REVIEW,
    PREVIOUS_REVIEW_GATE,
    PREVIOUS_EVENTS,
    BINDING,
    BINDING_RECORDS,
    BINDING_GATE,
    BINDING_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "telemetry_event_evidence_binding_v0_1=true",
    f"binding_decision={BINDING_DECISION}",
    f"binding_scope={BINDING_SCOPE}",
    "evidence_records_created=4",
    "evidence_ledger_v2_shape_valid=true",
    "trace_identity_preserved=true",
    "artifact_hashes_created=true",
    "runtime_export_allowed=false",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
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
    "action_id: link-telemetry-events-to-runtime-state",
    "owner_approval_required_before_runtime_integration: true",
    "Use evidence-bound telemetry records as local runtime state review inputs",
    "Do not start collectors, exporters, runtime workers, or external services",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def fail(message: str) -> None:
    print("AVF Telemetry Event Evidence Binding v0.1 validation")
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


def require_previous_review_gate() -> None:
    gate = read_json(PREVIOUS_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous review gate must point to this evidence binding goal")
    if gate.get("status") != "PASS":
        fail("previous review gate must be PASS")
    if gate.get("evidence_binding_allowed") is not True:
        fail("previous review gate must allow evidence binding")
    if gate.get("dependency_adoption_allowed") is not False:
        fail("previous review gate must keep dependency adoption blocked")
    if gate.get("runtime_integration_allowed") is not False:
        fail("previous review gate must keep runtime integration blocked")
    require_false_flags(gate.get("claim_boundary", {}), "previous review gate")


def require_previous_review() -> None:
    review = read_json(PREVIOUS_REVIEW)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous review must point to this evidence binding goal")
    if review.get("evidence_binding_allowed") is not True:
        fail("previous review must allow evidence binding")
    if review.get("trace_context_chain_valid") is not True:
        fail("previous review must confirm trace context chain")
    if review.get("secret_redaction_guard_reviewed") is not True:
        fail("previous review must confirm secret redaction guard")
    require_false_flags(review.get("claim_boundary", {}), "previous review")


def parse_source_events() -> list[dict]:
    events = [json.loads(line) for line in read(PREVIOUS_EVENTS).splitlines() if line.strip()]
    if len(events) != 4:
        fail("source telemetry events must contain exactly four records")
    return events


def parse_binding_records() -> list[dict]:
    records = [json.loads(line) for line in read(BINDING_RECORDS).splitlines() if line.strip()]
    if len(records) != 4:
        fail("binding records JSONL must contain exactly four records")
    return records


def require_evidence_v2_shape(record: dict) -> None:
    missing = [field for field in EVIDENCE_V2_REQUIRED_FIELDS if field not in record]
    if missing:
        fail(f"{record.get('id', '<unknown>')} missing evidence v2 fields:\n" + "\n".join(missing))
    if record.get("goal_id") != THIS_GOAL_ID:
        fail(f"{record.get('id')} goal_id mismatch")
    if not SHA256_RE.match(str(record.get("artifact_hash", ""))):
        fail(f"{record.get('id')} artifact_hash must be sha256-prefixed lowercase hex")
    actor = record.get("actor", {})
    if actor.get("actor_type") != "local_runner":
        fail(f"{record.get('id')} actor_type must be local_runner")
    if actor.get("actor_id") != "run_avf_telemetry_event_evidence_binding_v0_1":
        fail(f"{record.get('id')} actor_id mismatch")
    source = record.get("source", {})
    if source.get("source_type") != "repo_local_generated_artifact":
        fail(f"{record.get('id')} source_type mismatch")
    if source.get("source_uri") != rel(PREVIOUS_EVENTS):
        fail(f"{record.get('id')} source_uri mismatch")
    if not SHA256_RE.match(str(source.get("source_hash", ""))):
        fail(f"{record.get('id')} source_hash must be sha256-prefixed lowercase hex")
    boundary = record.get("claim_boundary", {})
    if boundary.get("scope") != "repo_local_internal_only":
        fail(f"{record.get('id')} claim boundary scope mismatch")
    require_false_flags(boundary, f"{record.get('id')} claim boundary")
    validation = record.get("validation_method", {})
    if validation.get("method_type") != "local_validator":
        fail(f"{record.get('id')} validation method type mismatch")
    if validation.get("command") != "python scripts\\validate_avf_telemetry_event_evidence_binding_v0_1.py":
        fail(f"{record.get('id')} validation command mismatch")
    if record.get("validation_result", {}).get("status") != "PASS":
        fail(f"{record.get('id')} validation result must be PASS")
    if record.get("confidence", {}).get("level") != "high":
        fail(f"{record.get('id')} confidence level must be high")
    approval = record.get("approval_state", {})
    if approval.get("required") is not False or approval.get("status") != "not_required":
        fail(f"{record.get('id')} approval state must be not required")


def require_binding_records(source_events: list[dict]) -> None:
    records = parse_binding_records()
    source_by_event = {event["event_id"]: event for event in source_events}
    record_event_ids = []
    for record in records:
        require_evidence_v2_shape(record)
        event_id = record.get("telemetry_event", {}).get("event_id")
        if event_id not in source_by_event:
            fail(f"{record.get('id')} telemetry event id does not match source events")
        event = source_by_event[event_id]
        record_event_ids.append(event_id)
        telemetry = record.get("telemetry_event", {})
        for field in ["run_id", "goal_id", "trace_id", "span_id", "traceparent", "signal_type"]:
            if telemetry.get(field) != event.get(field):
                fail(f"{record.get('id')} telemetry field {field} mismatch")
        if record.get("artifact_id") != event_id:
            fail(f"{record.get('id')} artifact_id must equal telemetry event id")
        if f"#{event_id}" not in record.get("artifact_uri", ""):
            fail(f"{record.get('id')} artifact_uri must include event id anchor")
    if record_event_ids != [event["event_id"] for event in source_events]:
        fail("binding records must preserve source event order")


def require_binding() -> None:
    binding = read_json(BINDING)
    expected = {
        "binding_id": "avf-telemetry-event-evidence-binding-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "source_goal_id": SOURCE_GOAL_ID,
        "binding_decision": BINDING_DECISION,
        "binding_scope": BINDING_SCOPE,
        "evidence_records_created": 4,
        "evidence_ledger_v2_shape_valid": True,
        "trace_identity_preserved": True,
        "artifact_hashes_created": True,
        "runtime_export_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if binding.get(key) != value:
            fail(f"binding {key} mismatch")
    if binding.get("binding_records_uri") != rel(BINDING_RECORDS):
        fail("binding records uri mismatch")
    if binding.get("evidence_ledger_schema_uri") != rel(EVIDENCE_SCHEMA):
        fail("evidence ledger schema uri mismatch")
    require_false_flags(binding.get("claim_boundary", {}), "binding")


def require_binding_gate() -> None:
    gate = read_json(BINDING_GATE)
    expected = {
        "gate_id": "avf-telemetry-event-evidence-binding-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "binding_decision": BINDING_DECISION,
        "binding_scope": BINDING_SCOPE,
        "evidence_records_created": 4,
        "runtime_state_link_allowed": True,
        "runtime_export_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"binding gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "binding gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_telemetry_event_evidence_binding_v0_1",
        "status": "PASS",
        "binding_decision": BINDING_DECISION,
        "binding_scope": BINDING_SCOPE,
        "evidence_records_created": 4,
        "evidence_ledger_v2_shape_valid": True,
        "trace_identity_preserved": True,
        "artifact_hashes_created": True,
        "runtime_export_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
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

    require_previous_review_gate()
    require_previous_review()
    source_events = parse_source_events()
    require_binding()
    require_binding_records(source_events)
    require_binding_gate()
    require_validation_result()
    require_markers(BINDING_REPORT, REPORT_MARKERS)
    require_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Telemetry Event Evidence Binding v0.1 validation")
    print("RESULT: PASS")
    print("telemetry_event_evidence_binding_v0_1=true")
    print(f"binding_decision={BINDING_DECISION}")
    print(f"binding_scope={BINDING_SCOPE}")
    print("evidence_records_created=4")
    print("evidence_ledger_v2_shape_valid=true")
    print("trace_identity_preserved=true")
    print("artifact_hashes_created=true")
    print("runtime_state_link_allowed=true")
    print("runtime_export_allowed=false")
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

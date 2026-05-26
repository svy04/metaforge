from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "avf" / "observability"
GENERATED = OBS / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_telemetry_event_envelope_v0_1.py"
SCHEMA = OBS / "telemetry_event_envelope.schema.yml"
FIXTURE = OBS / "fixtures" / "sample_avf_telemetry_events.json"
CONTRACT = GENERATED / "telemetry_event_envelope_contract.json"
EVENTS_JSONL = GENERATED / "telemetry_event_sample_events.jsonl"
GATE = GENERATED / "telemetry_event_envelope_gate.json"
NEXT_ACTION = GENERATED / "telemetry_event_envelope_next_action.yml"
VALIDATION_RESULT = GENERATED / "telemetry_event_envelope_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_TELEMETRY_EVENT_ENVELOPE_V0_1_REPORT.md"
SOURCE_RECORDS = ROOT / "avf" / "capabilities" / "generated" / "primary_source_manual_records.json"
OTEL_CONTRACT = OBS / "telemetry_event_contract.md"

THIS_GOAL_ID = "avf_telemetry_event_envelope_v0_1"
NEXT_SAFE_GOAL_ID = "avf_telemetry_event_envelope_review_v0_1"
CONTRACT_DECISION = "TELEMETRY_EVENT_ENVELOPE_READY_FOR_LOCAL_REVIEW"
ENVELOPE_SCOPE = "repo_local_observability_contract_only"

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
    SCHEMA,
    FIXTURE,
    CONTRACT,
    EVENTS_JSONL,
    GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
    SOURCE_RECORDS,
    OTEL_CONTRACT,
]

REQUIRED_SCHEMA_MARKERS = [
    "telemetry_event_envelope_v0_1",
    "trace_id",
    "span_id",
    "traceparent",
    "signal_type",
    "claim_boundary",
    "source_evidence",
    "OpenTelemetry",
    "W3C Trace Context",
    "dependency_adoption_allowed: false",
    "runtime_integration_allowed: false",
]

REQUIRED_REPORT_MARKERS = [
    "RESULT: PASS",
    "telemetry_event_envelope_v0_1=true",
    f"contract_decision={CONTRACT_DECISION}",
    f"envelope_scope={ENVELOPE_SCOPE}",
    "sample_events_created=4",
    "trace_context_validation=true",
    "secret_redaction_guard=true",
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

FORBIDDEN_ATTRIBUTE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        "api[_-]?key",
        "secret",
        "token",
        "password",
        "authorization",
        "cookie",
        "credential",
        "prompt",
        "raw_payload",
    ]
]

TRACE_ID_RE = re.compile(r"^[0-9a-f]{32}$")
SPAN_ID_RE = re.compile(r"^[0-9a-f]{16}$")
TRACEPARENT_RE = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-0[01]$")


def fail(message: str) -> None:
    print("AVF Telemetry Event Envelope v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_source_records() -> None:
    data = read_json(SOURCE_RECORDS)
    records = data.get("source_records", [])
    ids = {record.get("source_target_id") for record in records}
    if "src-opentelemetry-standard-docs" not in ids:
        fail("primary source records must include OpenTelemetry standard docs")
    if "https://opentelemetry.io/docs/what-is-opentelemetry/" not in read(OTEL_CONTRACT):
        fail("telemetry contract must preserve OpenTelemetry primary source URI")


def require_contract() -> None:
    data = read_json(CONTRACT)
    if data.get("goal_id") != THIS_GOAL_ID:
        fail("contract goal_id mismatch")
    if data.get("contract_decision") != CONTRACT_DECISION:
        fail("contract decision mismatch")
    if data.get("envelope_scope") != ENVELOPE_SCOPE:
        fail("envelope scope mismatch")
    if data.get("dependency_adoption_allowed") is not False:
        fail("contract must not allow dependency adoption")
    if data.get("runtime_integration_allowed") is not False:
        fail("contract must not allow runtime integration")
    sources = data.get("source_evidence", [])
    source_ids = {source.get("source_id") for source in sources}
    if "src-opentelemetry-standard-docs" not in source_ids:
        fail("contract must reference OpenTelemetry source evidence")
    if "src-w3c-trace-context" not in source_ids:
        fail("contract must reference W3C Trace Context source evidence")
    required_fields = set(data.get("required_envelope_fields", []))
    for field in [
        "event_id",
        "run_id",
        "goal_id",
        "trace_id",
        "span_id",
        "traceparent",
        "event_name",
        "signal_type",
        "event_time",
        "claim_boundary",
        "source_evidence",
    ]:
        if field not in required_fields:
            fail(f"contract missing required envelope field {field}")
    require_false_flags(data.get("claim_boundary", {}), "contract")


def require_gate() -> None:
    data = read_json(GATE)
    if data.get("goal_id") != THIS_GOAL_ID:
        fail("gate goal_id mismatch")
    if data.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("gate next safe goal mismatch")
    if data.get("contract_decision") != CONTRACT_DECISION:
        fail("gate contract decision mismatch")
    if data.get("dependency_adoption_allowed") is not False:
        fail("gate must not allow dependency adoption")
    if data.get("runtime_integration_allowed") is not False:
        fail("gate must not allow runtime integration")
    require_false_flags(data.get("claim_boundary", {}), "gate")


def require_events() -> None:
    lines = [line for line in read(EVENTS_JSONL).splitlines() if line.strip()]
    if len(lines) != 4:
        fail("sample telemetry event JSONL must contain exactly four events")
    event_ids: set[str] = set()
    span_ids: set[str] = set()
    for index, line in enumerate(lines):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"event line {index + 1} is not valid JSON: {exc}")

        event_id = event.get("event_id")
        if not event_id or event_id in event_ids:
            fail("event ids must be present and unique")
        event_ids.add(event_id)

        trace_id = event.get("trace_id", "")
        span_id = event.get("span_id", "")
        traceparent = event.get("traceparent", "")
        if not TRACE_ID_RE.match(trace_id) or trace_id == "0" * 32:
            fail(f"{event_id} has invalid trace_id")
        if not SPAN_ID_RE.match(span_id) or span_id == "0" * 16:
            fail(f"{event_id} has invalid span_id")
        if span_id in span_ids:
            fail("span ids must be unique across sample events")
        span_ids.add(span_id)
        match = TRACEPARENT_RE.match(traceparent)
        if not match or match.group(1) != trace_id or match.group(2) != span_id:
            fail(f"{event_id} traceparent must match trace_id and span_id")
        parent_span_id = event.get("parent_span_id")
        if parent_span_id is not None and not SPAN_ID_RE.match(parent_span_id):
            fail(f"{event_id} parent_span_id must be a 16 hex string when present")
        if event.get("signal_type") not in {"trace", "metric", "log"}:
            fail(f"{event_id} signal_type must be trace, metric, or log")
        if event.get("claim_boundary", {}).get("protected_action_executed") is not False:
            fail(f"{event_id} must keep protected_action_executed false")
        require_false_flags(event.get("claim_boundary", {}), f"event {event_id}")
        attributes = event.get("attributes", {})
        if not isinstance(attributes, dict):
            fail(f"{event_id} attributes must be an object")
        for key in attributes:
            if any(pattern.search(key) for pattern in FORBIDDEN_ATTRIBUTE_PATTERNS):
                fail(f"{event_id} contains forbidden sensitive attribute key {key}")
        if "src-opentelemetry-standard-docs" not in event.get("source_evidence", []):
            fail(f"{event_id} must reference OpenTelemetry source evidence")


def require_validation_result() -> None:
    data = read_json(VALIDATION_RESULT)
    if data.get("validator_id") != "validate_avf_telemetry_event_envelope_v0_1":
        fail("validation result validator_id mismatch")
    if data.get("status") != "PASS":
        fail("validation result status must be PASS")
    if data.get("sample_events_created") != 4:
        fail("validation result sample event count mismatch")
    if data.get("trace_context_validation") is not True:
        fail("validation result must confirm trace context validation")
    if data.get("secret_redaction_guard") is not True:
        fail("validation result must confirm secret redaction guard")
    if data.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(data.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_text_markers(SCHEMA, REQUIRED_SCHEMA_MARKERS)
    require_source_records()
    require_contract()
    require_gate()
    require_events()
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REQUIRED_REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, [f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}", "Do not install OpenTelemetry"])

    print("AVF Telemetry Event Envelope v0.1 validation")
    print("RESULT: PASS")
    print("telemetry_event_envelope_v0_1=true")
    print(f"contract_decision={CONTRACT_DECISION}")
    print(f"envelope_scope={ENVELOPE_SCOPE}")
    print("sample_events_created=4")
    print("trace_context_validation=true")
    print("secret_redaction_guard=true")
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

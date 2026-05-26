from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "avf" / "observability"
GENERATED = OBS / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_telemetry_event_envelope_review_v0_1.py"
PREVIOUS_CONTRACT = GENERATED / "telemetry_event_envelope_contract.json"
PREVIOUS_EVENTS = GENERATED / "telemetry_event_sample_events.jsonl"
PREVIOUS_GATE = GENERATED / "telemetry_event_envelope_gate.json"
REVIEW = GENERATED / "telemetry_event_envelope_review.json"
REVIEW_GATE = GENERATED / "telemetry_event_envelope_review_gate.json"
REVIEW_REPORT = GENERATED / "telemetry_event_envelope_review_report.md"
NEXT_ACTION = GENERATED / "telemetry_event_envelope_review_next_action.yml"
VALIDATION_RESULT = GENERATED / "telemetry_event_envelope_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_TELEMETRY_EVENT_ENVELOPE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_telemetry_event_envelope_review_v0_1"
PREVIOUS_GOAL_ID = "avf_telemetry_event_envelope_v0_1"
NEXT_SAFE_GOAL_ID = "avf_telemetry_event_evidence_binding_v0_1"
CONTRACT_DECISION = "TELEMETRY_EVENT_ENVELOPE_READY_FOR_LOCAL_REVIEW"
ENVELOPE_SCOPE = "repo_local_observability_contract_only"
REVIEW_DECISION = "TELEMETRY_EVENT_ENVELOPE_REVIEWED_READY_FOR_EVIDENCE_BINDING"
REVIEW_SCOPE = "repo_local_review_only"

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
    PREVIOUS_CONTRACT,
    PREVIOUS_EVENTS,
    PREVIOUS_GATE,
    REVIEW,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "telemetry_event_envelope_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_scope={REVIEW_SCOPE}",
    "sample_events_reviewed=4",
    "trace_context_chain_valid=true",
    "source_evidence_reviewed=true",
    "secret_redaction_guard_reviewed=true",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "OpenTelemetry",
    "W3C Trace Context",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: bind-telemetry-event-envelope-to-evidence",
    "owner_approval_required_before_runtime_integration: true",
    "Create a repo-local evidence binding for telemetry event envelopes",
    "Do not install OpenTelemetry, start collectors, or integrate exporters",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
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


def fail(message: str) -> None:
    print("AVF Telemetry Event Envelope Review v0.1 validation")
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


def require_previous_gate() -> None:
    gate = read_json(PREVIOUS_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous gate must point to this review goal")
    if gate.get("contract_decision") != CONTRACT_DECISION:
        fail("previous gate contract decision mismatch")
    if gate.get("envelope_scope") != ENVELOPE_SCOPE:
        fail("previous gate envelope scope mismatch")
    if gate.get("sample_events_created") != 4:
        fail("previous gate must confirm four sample events")
    if gate.get("trace_context_validation") is not True:
        fail("previous gate must keep trace_context_validation true")
    if gate.get("secret_redaction_guard") is not True:
        fail("previous gate must keep secret_redaction_guard true")
    if gate.get("dependency_adoption_allowed") is not False:
        fail("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        fail("runtime integration must remain blocked")
    require_false_flags(gate.get("claim_boundary", {}), "previous gate")


def require_previous_contract() -> dict:
    contract = read_json(PREVIOUS_CONTRACT)
    if contract.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("previous contract goal mismatch")
    if contract.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("previous contract must point to this review goal")
    if contract.get("contract_decision") != CONTRACT_DECISION:
        fail("previous contract decision mismatch")
    if contract.get("envelope_scope") != ENVELOPE_SCOPE:
        fail("previous contract envelope scope mismatch")
    if contract.get("dependency_adoption_allowed") is not False:
        fail("previous contract must block dependency adoption")
    if contract.get("runtime_integration_allowed") is not False:
        fail("previous contract must block runtime integration")
    require_false_flags(contract.get("claim_boundary", {}), "previous contract")

    source_ids = {source.get("source_id") for source in contract.get("source_evidence", [])}
    if "src-opentelemetry-standard-docs" not in source_ids:
        fail("previous contract must include OpenTelemetry source evidence")
    if "src-w3c-trace-context" not in source_ids:
        fail("previous contract must include W3C Trace Context source evidence")
    return contract


def parse_previous_events() -> list[dict]:
    lines = [line for line in read(PREVIOUS_EVENTS).splitlines() if line.strip()]
    if len(lines) != 4:
        fail("previous sample telemetry events must contain exactly four records")
    events = []
    for index, line in enumerate(lines):
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as exc:
            fail(f"event line {index + 1} is not valid JSON: {exc}")
    return events


def require_event_chain(events: list[dict]) -> None:
    trace_ids = {event.get("trace_id") for event in events}
    if len(trace_ids) != 1:
        fail("all sample events must share one trace_id")
    trace_id = next(iter(trace_ids))
    if not isinstance(trace_id, str) or not TRACE_ID_RE.match(trace_id) or trace_id == "0" * 32:
        fail("sample trace_id must be a non-zero 32-char lowercase hex value")

    seen_spans: set[str] = set()
    signal_types: set[str] = set()
    for index, event in enumerate(events):
        event_id = event.get("event_id", f"event-{index}")
        span_id = event.get("span_id")
        if not isinstance(span_id, str) or not SPAN_ID_RE.match(span_id) or span_id == "0" * 16:
            fail(f"{event_id} span_id must be a non-zero 16-char lowercase hex value")
        if span_id in seen_spans:
            fail("sample event span_ids must be unique")
        expected_traceparent = f"00-{trace_id}-{span_id}-01"
        if event.get("traceparent") != expected_traceparent:
            fail(f"{event_id} traceparent mismatch")
        parent_span_id = event.get("parent_span_id")
        if index == 0 and parent_span_id is not None:
            fail("root sample event must not have a parent_span_id")
        if index > 0 and parent_span_id not in seen_spans:
            fail(f"{event_id} parent_span_id must refer to an earlier span")
        seen_spans.add(span_id)

        signal_type = event.get("signal_type")
        if signal_type not in {"trace", "metric", "log"}:
            fail(f"{event_id} signal_type must be trace, metric, or log")
        signal_types.add(signal_type)

        require_false_flags(event.get("claim_boundary", {}), f"event {event_id}")
        for key in event.get("attributes", {}):
            if any(pattern.search(key) for pattern in FORBIDDEN_ATTRIBUTE_PATTERNS):
                fail(f"{event_id} contains forbidden sensitive attribute key {key}")
        source_evidence = event.get("source_evidence", [])
        if "src-opentelemetry-standard-docs" not in source_evidence:
            fail(f"{event_id} must reference OpenTelemetry source evidence")
        if "src-w3c-trace-context" not in source_evidence:
            fail(f"{event_id} must reference W3C Trace Context source evidence")

    if signal_types != {"trace", "metric", "log"}:
        fail("sample event signal types must cover trace, metric, and log")


def require_review() -> None:
    review = read_json(REVIEW)
    expected = {
        "review_id": "avf-telemetry-event-envelope-review-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "sample_events_reviewed": 4,
        "trace_context_chain_valid": True,
        "source_evidence_reviewed": True,
        "secret_redaction_guard_reviewed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if review.get(key) != value:
            fail(f"review {key} mismatch")
    source_ids = set(review.get("source_evidence_reviewed_ids", []))
    if source_ids != {"src-opentelemetry-standard-docs", "src-w3c-trace-context"}:
        fail("review must confirm both source evidence records")
    require_false_flags(review.get("claim_boundary", {}), "review")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    expected = {
        "gate_id": "avf-telemetry-event-envelope-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "sample_events_reviewed": 4,
        "evidence_binding_allowed": True,
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
    expected = {
        "validator_id": "validate_avf_telemetry_event_envelope_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "sample_events_reviewed": 4,
        "trace_context_chain_valid": True,
        "source_evidence_reviewed": True,
        "secret_redaction_guard_reviewed": True,
        "evidence_binding_allowed": True,
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

    require_previous_gate()
    require_previous_contract()
    events = parse_previous_events()
    require_event_chain(events)
    require_review()
    require_review_gate()
    require_validation_result()
    require_text_markers(REVIEW_REPORT, TEXT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_text_markers(
        VALIDATION_REPORT,
        TEXT_MARKERS
        + [
            "RESULT: PASS",
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
        ],
    )

    print("AVF Telemetry Event Envelope Review v0.1 validation")
    print("RESULT: PASS")
    print("telemetry_event_envelope_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print("sample_events_reviewed=4")
    print("trace_context_chain_valid=true")
    print("source_evidence_reviewed=true")
    print("secret_redaction_guard_reviewed=true")
    print("evidence_binding_allowed=true")
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

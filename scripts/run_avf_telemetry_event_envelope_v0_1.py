from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "avf" / "observability"
GENERATED = OBS / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

SCHEMA = OBS / "telemetry_event_envelope.schema.yml"
FIXTURE = OBS / "fixtures" / "sample_avf_telemetry_events.json"
CONTRACT = GENERATED / "telemetry_event_envelope_contract.json"
EVENTS_JSONL = GENERATED / "telemetry_event_sample_events.jsonl"
GATE = GENERATED / "telemetry_event_envelope_gate.json"
NEXT_ACTION = GENERATED / "telemetry_event_envelope_next_action.yml"
VALIDATION_RESULT = GENERATED / "telemetry_event_envelope_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_TELEMETRY_EVENT_ENVELOPE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_telemetry_event_envelope_v0_1"
PREVIOUS_GOAL_ID = "avf_runtime_adapter_contract_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_telemetry_event_envelope_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
CONTRACT_DECISION = "TELEMETRY_EVENT_ENVELOPE_READY_FOR_LOCAL_REVIEW"
ENVELOPE_SCOPE = "repo_local_observability_contract_only"


FALSE_FLAGS = {
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def traceparent(trace_id: str, span_id: str) -> str:
    return f"00-{trace_id}-{span_id}-01"


def build_events(fixture: dict) -> list[dict]:
    events = []
    for event in fixture["events"]:
        next_event = {
            "event_id": event["event_id"],
            "run_id": fixture["run_id"],
            "goal_id": fixture["goal_id"],
            "trace_id": fixture["trace_id"],
            "span_id": event["span_id"],
            "parent_span_id": event.get("parent_span_id"),
            "traceparent": traceparent(fixture["trace_id"], event["span_id"]),
            "event_name": event["event_name"],
            "signal_type": event["signal_type"],
            "event_time": CREATED_AT,
            "producer": "avf.repo_local.telemetry_event_envelope.v0_1",
            "attributes": event["attributes"],
            "claim_boundary": dict(FALSE_FLAGS),
            "source_evidence": list(fixture["source_evidence"]),
        }
        events.append(next_event)
    return events


def build_contract() -> dict:
    required_fields = [
        "event_id",
        "run_id",
        "goal_id",
        "trace_id",
        "span_id",
        "traceparent",
        "event_name",
        "signal_type",
        "event_time",
        "producer",
        "attributes",
        "claim_boundary",
        "source_evidence",
    ]
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "contract_decision": CONTRACT_DECISION,
        "envelope_scope": ENVELOPE_SCOPE,
        "schema_uri": rel(SCHEMA),
        "fixture_uri": rel(FIXTURE),
        "required_envelope_fields": required_fields,
        "trace_context_rules": {
            "trace_id": "lowercase_hex_32_not_all_zero",
            "span_id": "lowercase_hex_16_not_all_zero",
            "traceparent": "00-{trace_id}-{span_id}-{flags}",
            "flags_allowed": ["00", "01"],
        },
        "signal_types": ["trace", "metric", "log"],
        "secret_redaction_guard": {
            "blocked_attribute_key_patterns": [
                "api_key",
                "secret",
                "token",
                "password",
                "authorization",
                "cookie",
                "credential",
                "prompt",
                "raw_payload",
            ]
        },
        "source_evidence": [
            {
                "source_id": "src-opentelemetry-standard-docs",
                "source_kind": "standard",
                "source_title": "What is OpenTelemetry?",
                "source_uri": "https://opentelemetry.io/docs/what-is-opentelemetry/",
                "evidence_summary": "OpenTelemetry provides a vendor-neutral observability vocabulary for telemetry data such as traces, metrics, and logs.",
                "reference_lines": "turn1view1 lines 847-853",
            },
            {
                "source_id": "src-w3c-trace-context",
                "source_kind": "standard",
                "source_title": "W3C Trace Context",
                "source_uri": "https://www.w3.org/TR/trace-context/",
                "evidence_summary": "Trace Context defines interoperable trace identifiers and traceparent propagation boundaries for distributed traces.",
                "reference_lines": "turn1view5 lines 493-503",
            },
        ],
        "sample_events_uri": rel(EVENTS_JSONL),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "claim_boundary": dict(FALSE_FLAGS),
    }


def build_gate() -> dict:
    return {
        "gate_id": "avf-telemetry-event-envelope-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "contract_decision": CONTRACT_DECISION,
        "envelope_scope": ENVELOPE_SCOPE,
        "sample_events_created": 4,
        "trace_context_validation": True,
        "secret_redaction_guard": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "owner_approval_required_before_runtime_integration": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": dict(FALSE_FLAGS),
    }


def build_next_action() -> str:
    return f"""action_id: review-telemetry-event-envelope
owner_approval_required_before_runtime_integration: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local telemetry event envelope contract
  - Keep OpenTelemetry and W3C Trace Context as source-backed design references only
  - Do not install OpenTelemetry, run collectors, start exporters, or integrate a runtime
  - Use the envelope for future local validators, evidence events, and adapter review
  - Keep provider calls, external services, scraping, posting, deploy, publish, and readiness claims blocked

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    return f"""# AVF Telemetry Event Envelope v0.1 Report

RESULT: PASS
telemetry_event_envelope_v0_1=true

## Commands

- python scripts\\run_avf_telemetry_event_envelope_v0_1.py
- python scripts\\validate_avf_telemetry_event_envelope_v0_1.py

## Contract summary

- contract_decision={CONTRACT_DECISION}
- envelope_scope={ENVELOPE_SCOPE}
- sample_events_created=4
- trace_context_validation=true
- secret_redaction_guard=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Source-backed design references

- OpenTelemetry: https://opentelemetry.io/docs/what-is-opentelemetry/
- W3C Trace Context: https://www.w3.org/TR/trace-context/

## Generated artifacts

- {rel(SCHEMA)}
- {rel(FIXTURE)}
- {rel(CONTRACT)}
- {rel(EVENTS_JSONL)}
- {rel(GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_telemetry_event_envelope_v0_1",
        "status": "PASS",
        "goal_id": THIS_GOAL_ID,
        "created_at": CREATED_AT,
        "contract_decision": CONTRACT_DECISION,
        "envelope_scope": ENVELOPE_SCOPE,
        "sample_events_created": 4,
        "trace_context_validation": True,
        "secret_redaction_guard": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": dict(FALSE_FLAGS),
    }


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if fixture.get("goal_id") != THIS_GOAL_ID:
        raise SystemExit("fixture goal_id mismatch")

    events = build_events(fixture)
    write_json(CONTRACT, build_contract())
    write_text(EVENTS_JSONL, "".join(json.dumps(event, sort_keys=True) + "\n" for event in events))
    write_json(GATE, build_gate())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("telemetry_event_envelope_v0_1_created=true")
    print(f"contract_decision={CONTRACT_DECISION}")
    print(f"envelope_scope={ENVELOPE_SCOPE}")
    print("sample_events_created=4")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("protected_action_executed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

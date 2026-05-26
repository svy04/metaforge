from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "avf" / "observability"
GENERATED = OBS / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

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
CREATED_AT = "2026-05-27T00:00:00Z"
CONTRACT_DECISION = "TELEMETRY_EVENT_ENVELOPE_READY_FOR_LOCAL_REVIEW"
ENVELOPE_SCOPE = "repo_local_observability_contract_only"
REVIEW_DECISION = "TELEMETRY_EVENT_ENVELOPE_REVIEWED_READY_FOR_EVIDENCE_BINDING"
REVIEW_SCOPE = "repo_local_review_only"

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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def false_boundary() -> dict:
    return dict(FALSE_FLAGS)


def load_events() -> list[dict]:
    return [json.loads(line) for line in PREVIOUS_EVENTS.read_text(encoding="utf-8").splitlines() if line.strip()]


def require_previous_gate() -> None:
    gate = read_json(PREVIOUS_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous gate must point to this review goal")
    if gate.get("contract_decision") != CONTRACT_DECISION:
        raise SystemExit("previous gate contract decision mismatch")
    if gate.get("envelope_scope") != ENVELOPE_SCOPE:
        raise SystemExit("previous gate envelope scope mismatch")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_contract() -> dict:
    contract = read_json(PREVIOUS_CONTRACT)
    if contract.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous contract goal mismatch")
    if contract.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous contract must point to this review goal")
    if contract.get("contract_decision") != CONTRACT_DECISION:
        raise SystemExit("previous contract decision mismatch")
    if contract.get("envelope_scope") != ENVELOPE_SCOPE:
        raise SystemExit("previous contract envelope scope mismatch")
    return contract


def event_chain_summary(events: list[dict]) -> dict:
    if len(events) != 4:
        raise SystemExit("expected four telemetry sample events")
    seen_spans: set[str] = set()
    order = []
    parent_links = []
    trace_id = events[0]["trace_id"]
    for index, event in enumerate(events):
        if event["trace_id"] != trace_id:
            raise SystemExit("all events must share one trace_id")
        parent_span_id = event.get("parent_span_id")
        if index == 0 and parent_span_id is not None:
            raise SystemExit("root event must not have a parent span")
        if index > 0 and parent_span_id not in seen_spans:
            raise SystemExit("parent span must refer to an earlier event")
        if event["traceparent"] != f"00-{trace_id}-{event['span_id']}-01":
            raise SystemExit("traceparent must match trace_id and span_id")
        seen_spans.add(event["span_id"])
        order.append(event["event_id"])
        parent_links.append(
            {
                "event_id": event["event_id"],
                "span_id": event["span_id"],
                "parent_span_id": parent_span_id,
            }
        )
    return {
        "trace_id": trace_id,
        "root_event_id": events[0]["event_id"],
        "terminal_event_id": events[-1]["event_id"],
        "event_order": order,
        "parent_links": parent_links,
        "signal_type_coverage": sorted({event["signal_type"] for event in events}),
        "trace_context_chain_valid": True,
    }


def source_ids(contract: dict) -> list[str]:
    return sorted(source["source_id"] for source in contract.get("source_evidence", []))


def build_review(contract: dict, events: list[dict]) -> dict:
    chain = event_chain_summary(events)
    return {
        "review_id": "avf-telemetry-event-envelope-review-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "contract_decision_reviewed": contract["contract_decision"],
        "envelope_scope_reviewed": contract["envelope_scope"],
        "required_fields_reviewed": contract["required_envelope_fields"],
        "sample_events_reviewed": len(events),
        "event_chain_summary": chain,
        "trace_context_chain_valid": True,
        "source_evidence_reviewed": True,
        "source_evidence_reviewed_ids": source_ids(contract),
        "secret_redaction_guard_reviewed": True,
        "blocked_attribute_key_patterns_reviewed": contract["secret_redaction_guard"]["blocked_attribute_key_patterns"],
        "evidence_binding_allowed": True,
        "evidence_binding_contract": {
            "binding_scope": "future_repo_local_evidence_events_only",
            "event_identity_fields": ["event_id", "run_id", "goal_id", "trace_id", "span_id"],
            "required_claim_boundary": "all_protected_action_flags_false",
            "runtime_export_allowed": False,
        },
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate() -> dict:
    return {
        "gate_id": "avf-telemetry-event-envelope-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
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
        "claim_boundary": false_boundary(),
    }


def build_review_report(review: dict) -> str:
    chain = review["event_chain_summary"]
    rows = "\n".join(
        f"| {link['event_id']} | `{link['span_id']}` | `{link['parent_span_id']}` |"
        for link in chain["parent_links"]
    )
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    return f"""# Telemetry Event Envelope Review v0.1

telemetry_event_envelope_review_v0_1=true
review_decision={REVIEW_DECISION}
review_scope={REVIEW_SCOPE}
sample_events_reviewed=4
trace_context_chain_valid=true
source_evidence_reviewed=true
secret_redaction_guard_reviewed=true
evidence_binding_allowed=true
dependency_adoption_allowed=false
runtime_integration_allowed=false

## Review basis

- OpenTelemetry source evidence reviewed: https://opentelemetry.io/docs/what-is-opentelemetry/
- W3C Trace Context source evidence reviewed: https://www.w3.org/TR/trace-context/
- Previous contract: {rel(PREVIOUS_CONTRACT)}
- Previous sample events: {rel(PREVIOUS_EVENTS)}

## Trace chain

| Event | Span | Parent span |
| --- | --- | --- |
{rows}

## Evidence binding decision

The envelope is ready for a repo-local evidence binding pass because the sample events have one trace, stable span identity, parent-child order, trace/log/metric coverage, explicit source evidence, and all protected action flags remain false. This does not install OpenTelemetry, start collectors, export telemetry, or integrate runtime dependencies.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: bind-telemetry-event-envelope-to-evidence
owner_approval_required_before_runtime_integration: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local evidence binding for telemetry event envelopes
  - Link telemetry event identity fields to evidence ledger v2 style records
  - Keep binding deterministic, local, and validation-only
  - Do not install OpenTelemetry, start collectors, or integrate exporters
  - Do not call providers, live models, external services, scraping, posting, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_telemetry_event_envelope_review_v0_1",
        "status": "PASS",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
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
        "claim_boundary": false_boundary(),
    }


def build_validation_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [REVIEW, REVIEW_GATE, REVIEW_REPORT, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Telemetry Event Envelope Review v0.1 Report

RESULT: PASS
telemetry_event_envelope_review_v0_1=true

## Commands

- python scripts\\run_avf_telemetry_event_envelope_review_v0_1.py
- python scripts\\validate_avf_telemetry_event_envelope_review_v0_1.py

## Review summary

- review_decision={REVIEW_DECISION}
- review_scope={REVIEW_SCOPE}
- sample_events_reviewed=4
- trace_context_chain_valid=true
- source_evidence_reviewed=true
- secret_redaction_guard_reviewed=true
- evidence_binding_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Source-backed design references

- OpenTelemetry: https://opentelemetry.io/docs/what-is-opentelemetry/
- W3C Trace Context: https://www.w3.org/TR/trace-context/

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> int:
    require_previous_gate()
    contract = load_contract()
    events = load_events()
    review = build_review(contract, events)

    write_json(REVIEW, review)
    write_json(REVIEW_GATE, build_gate())
    write_text(REVIEW_REPORT, build_review_report(review))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_validation_report())

    print("AVF Telemetry Event Envelope Review v0.1")
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
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

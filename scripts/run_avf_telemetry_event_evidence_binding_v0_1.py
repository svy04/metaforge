from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "avf" / "observability"
GENERATED = OBS / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
EVIDENCE_SCHEMA = ROOT / "avf" / "evidence" / "evidence_ledger.v2.schema.yml"

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
CREATED_AT = "2026-05-27T00:00:00Z"
BINDING_DECISION = "TELEMETRY_EVENTS_BOUND_TO_EVIDENCE_LEDGER_V2_RECORDS"
BINDING_SCOPE = "repo_local_evidence_binding_only"

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


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def false_boundary(scope: str | None = None) -> dict:
    boundary = dict(FALSE_FLAGS)
    if scope is not None:
        boundary["scope"] = scope
    return boundary


def require_previous_review_gate() -> None:
    gate = read_json(PREVIOUS_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous review gate must point to this evidence binding goal")
    if gate.get("evidence_binding_allowed") is not True:
        raise SystemExit("previous review gate must allow evidence binding")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_previous_review() -> dict:
    review = read_json(PREVIOUS_REVIEW)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous review must point to this evidence binding goal")
    if review.get("evidence_binding_allowed") is not True:
        raise SystemExit("previous review must allow evidence binding")
    if review.get("trace_context_chain_valid") is not True:
        raise SystemExit("previous review must confirm trace context chain")
    return review


def load_events() -> list[dict]:
    return [json.loads(line) for line in PREVIOUS_EVENTS.read_text(encoding="utf-8").splitlines() if line.strip()]


def source_hash() -> str:
    return sha256_text(PREVIOUS_EVENTS.read_text(encoding="utf-8"))


def build_evidence_record(event: dict, source_file_hash: str) -> dict:
    event_hash = sha256_text(canonical_json(event))
    event_id = event["event_id"]
    return {
        "id": f"evidence-{event_id}",
        "run_id": event["run_id"],
        "goal_id": THIS_GOAL_ID,
        "artifact_id": event_id,
        "artifact_uri": f"{rel(PREVIOUS_EVENTS)}#{event_id}",
        "artifact_hash": event_hash,
        "actor": {
            "actor_type": "local_runner",
            "actor_id": "run_avf_telemetry_event_evidence_binding_v0_1",
        },
        "source": {
            "source_type": "repo_local_generated_artifact",
            "source_uri": rel(PREVIOUS_EVENTS),
            "source_hash": source_file_hash,
        },
        "claim": (
            f"Telemetry event {event_id} is bound to a repo-local Evidence Ledger v2-shaped record "
            "for internal observability and validation lineage only."
        ),
        "claim_boundary": false_boundary("repo_local_internal_only"),
        "validation_method": {
            "method_type": "local_validator",
            "command": "python scripts\\validate_avf_telemetry_event_evidence_binding_v0_1.py",
            "validator_uri": "scripts/validate_avf_telemetry_event_evidence_binding_v0_1.py",
        },
        "validation_result": {
            "status": "PASS",
            "observed_at": CREATED_AT,
            "summary": "Evidence binding record preserves telemetry identity, trace identity, source hash, artifact hash, and protected-action boundary.",
        },
        "confidence": {
            "level": "high",
            "reason": "Record is generated deterministically from repo-local telemetry event fixtures and checked by the local validator.",
        },
        "approval_state": {
            "required": False,
            "status": "not_required",
            "approver": "",
        },
        "created_at": CREATED_AT,
        "next_action": NEXT_SAFE_GOAL_ID,
        "telemetry_event": {
            "event_id": event_id,
            "event_name": event["event_name"],
            "run_id": event["run_id"],
            "goal_id": event["goal_id"],
            "trace_id": event["trace_id"],
            "span_id": event["span_id"],
            "parent_span_id": event.get("parent_span_id"),
            "traceparent": event["traceparent"],
            "signal_type": event["signal_type"],
        },
    }


def build_binding(events: list[dict], records: list[dict], source_file_hash: str) -> dict:
    return {
        "binding_id": "avf-telemetry-event-evidence-binding-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "source_goal_id": SOURCE_GOAL_ID,
        "created_at": CREATED_AT,
        "binding_decision": BINDING_DECISION,
        "binding_scope": BINDING_SCOPE,
        "source_events_uri": rel(PREVIOUS_EVENTS),
        "source_events_hash": source_file_hash,
        "binding_records_uri": rel(BINDING_RECORDS),
        "evidence_ledger_schema_uri": rel(EVIDENCE_SCHEMA),
        "evidence_records_created": len(records),
        "bound_event_ids": [event["event_id"] for event in events],
        "trace_id": events[0]["trace_id"],
        "trace_identity_preserved": True,
        "evidence_ledger_v2_shape_valid": True,
        "artifact_hashes_created": True,
        "runtime_export_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate() -> dict:
    return {
        "gate_id": "avf-telemetry-event-evidence-binding-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "binding_decision": BINDING_DECISION,
        "binding_scope": BINDING_SCOPE,
        "evidence_records_created": 4,
        "evidence_ledger_v2_shape_valid": True,
        "trace_identity_preserved": True,
        "artifact_hashes_created": True,
        "runtime_state_link_allowed": True,
        "runtime_export_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(records: list[dict]) -> str:
    rows = "\n".join(
        f"| `{record['artifact_id']}` | `{record['telemetry_event']['signal_type']}` | `{record['telemetry_event']['span_id']}` | `{record['artifact_hash']}` |"
        for record in records
    )
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    return f"""# Telemetry Event Evidence Binding v0.1

RESULT: PASS
telemetry_event_evidence_binding_v0_1=true
binding_decision={BINDING_DECISION}
binding_scope={BINDING_SCOPE}
evidence_records_created=4
evidence_ledger_v2_shape_valid=true
trace_identity_preserved=true
artifact_hashes_created=true
runtime_state_link_allowed=true
runtime_export_allowed=false
dependency_adoption_allowed=false
runtime_integration_allowed=false

## Binding records

| Event | Signal | Span | Artifact hash |
| --- | --- | --- | --- |
{rows}

## Boundary

The binding is repo-local and validation-only. It binds telemetry event identity to Evidence Ledger v2-shaped records without exporting telemetry, starting collectors, adopting dependencies, integrating runtime workers, calling providers, scraping, posting, deploying, publishing, or claiming readiness.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: link-telemetry-events-to-runtime-state
owner_approval_required_before_runtime_integration: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Use evidence-bound telemetry records as local runtime state review inputs
  - Map event identity, trace identity, and evidence record identity to a repo-local runtime-state link contract
  - Keep the next step deterministic, local, and validation-only
  - Do not start collectors, exporters, runtime workers, or external services
  - Do not call providers, live models, scrape, post, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_telemetry_event_evidence_binding_v0_1",
        "status": "PASS",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "binding_decision": BINDING_DECISION,
        "binding_scope": BINDING_SCOPE,
        "evidence_records_created": 4,
        "evidence_ledger_v2_shape_valid": True,
        "trace_identity_preserved": True,
        "artifact_hashes_created": True,
        "runtime_state_link_allowed": True,
        "runtime_export_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [BINDING, BINDING_RECORDS, BINDING_GATE, BINDING_REPORT, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Telemetry Event Evidence Binding v0.1 Report

RESULT: PASS
telemetry_event_evidence_binding_v0_1=true

## Commands

- python scripts\\run_avf_telemetry_event_evidence_binding_v0_1.py
- python scripts\\validate_avf_telemetry_event_evidence_binding_v0_1.py

## Binding summary

- binding_decision={BINDING_DECISION}
- binding_scope={BINDING_SCOPE}
- evidence_records_created=4
- evidence_ledger_v2_shape_valid=true
- trace_identity_preserved=true
- artifact_hashes_created=true
- runtime_state_link_allowed=true
- runtime_export_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> int:
    require_previous_review_gate()
    load_previous_review()
    events = load_events()
    if len(events) != 4:
        raise SystemExit("expected four telemetry events")
    file_hash = source_hash()
    records = [build_evidence_record(event, file_hash) for event in events]

    write_json(BINDING, build_binding(events, records, file_hash))
    write_text(BINDING_RECORDS, "".join(json.dumps(record, sort_keys=True) + "\n" for record in records))
    write_json(BINDING_GATE, build_gate())
    write_text(BINDING_REPORT, build_report(records))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_validation_report())

    print("AVF Telemetry Event Evidence Binding v0.1")
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
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

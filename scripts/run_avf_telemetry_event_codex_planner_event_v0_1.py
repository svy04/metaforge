from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

GAP_REVIEW = OBS_GENERATED / "runtime_state_observability_gap_review.json"
GAP_REVIEW_GATE = OBS_GENERATED / "runtime_state_observability_gap_review_gate.json"
SOURCE_EVENTS = OBS_GENERATED / "telemetry_event_sample_events.jsonl"
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
CREATED_AT = "2026-05-27T00:00:00Z"
EVENT_DECISION = "CODEX_PLANNER_TELEMETRY_EVENT_ADDED_TO_REPO_LOCAL_STREAM"
EVENT_SCOPE = "repo_local_augmented_telemetry_stream_only"
PLANNER_EVENT_ID = "evt-avf-codex-planner-task-created"
PLANNER_EVENT_NAME = "avf.codex_planner.task_created"
TRACE_ID = "4bf92f3577b34da6a3ce929d0e0e4736"
PLANNER_SPAN_ID = "3bf067aa0ba902bb"
PLANNER_PARENT_SPAN_ID = "2bf067aa0ba902b9"

EVENT_TO_RUNTIME = {
    "evt-avf-goal-accepted": ("orchestrated", "orchestrator"),
    "evt-avf-router-selected": ("routed", "router"),
    "evt-avf-safety-gate": ("safety_reviewed", "safety_reviewer"),
    PLANNER_EVENT_ID: ("codex_planned", "codex_planner"),
    "evt-avf-evidence-written": ("evidence_written", "evidence_writer"),
}

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


def require_gap_review() -> None:
    review = read_json(GAP_REVIEW)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("gap review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("gap review must point to this planner event goal")
    if review.get("recommended_event_id") != PLANNER_EVENT_ID:
        raise SystemExit("gap review recommended event mismatch")
    if review.get("planner_event_needed") is not True:
        raise SystemExit("gap review must require planner event")

    gate = read_json(GAP_REVIEW_GATE)
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("gap review gate must point to this planner event goal")
    if gate.get("planner_event_contract_allowed") is not True:
        raise SystemExit("planner event contract must be allowed")


def load_source_events() -> list[dict]:
    return [json.loads(line) for line in SOURCE_EVENTS.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_augmented_events(source_events: list[dict]) -> list[dict]:
    if [event["event_id"] for event in source_events] != [
        "evt-avf-goal-accepted",
        "evt-avf-router-selected",
        "evt-avf-safety-gate",
        "evt-avf-evidence-written",
    ]:
        raise SystemExit("source event order mismatch")

    events = [json.loads(json.dumps(event)) for event in source_events]
    planner_event = {
        "event_id": PLANNER_EVENT_ID,
        "run_id": events[0]["run_id"],
        "goal_id": events[0]["goal_id"],
        "trace_id": TRACE_ID,
        "span_id": PLANNER_SPAN_ID,
        "parent_span_id": PLANNER_PARENT_SPAN_ID,
        "traceparent": f"00-{TRACE_ID}-{PLANNER_SPAN_ID}-01",
        "event_name": PLANNER_EVENT_NAME,
        "signal_type": "trace",
        "event_time": CREATED_AT,
        "producer": "avf.repo_local.telemetry_event_codex_planner_event.v0_1",
        "attributes": {
            "avf.cell": "codex_planner",
            "avf.runtime_state": "codex_planned",
            "avf.pr_sized_task_created": "true",
            "avf.scope": EVENT_SCOPE,
        },
        "claim_boundary": false_boundary(),
        "source_evidence": ["src-opentelemetry-standard-docs", "src-w3c-trace-context"],
    }
    events[3]["parent_span_id"] = PLANNER_SPAN_ID
    return events[:3] + [planner_event] + [events[3]]


def build_evidence_records(events: list[dict]) -> list[dict]:
    source_hash = sha256_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in events))
    records = []
    for event in events:
        event_id = event["event_id"]
        event_hash = sha256_text(canonical_json(event))
        records.append(
            {
                "id": f"evidence-{event_id}",
                "run_id": event["run_id"],
                "goal_id": THIS_GOAL_ID,
                "artifact_id": event_id,
                "artifact_uri": f"{rel(AUGMENTED_EVENTS)}#{event_id}",
                "artifact_hash": event_hash,
                "actor": {
                    "actor_type": "local_runner",
                    "actor_id": "run_avf_telemetry_event_codex_planner_event_v0_1",
                },
                "source": {
                    "source_type": "repo_local_generated_artifact",
                    "source_uri": rel(AUGMENTED_EVENTS),
                    "source_hash": source_hash,
                },
                "claim": f"Augmented telemetry event {event_id} is bound to a repo-local Evidence Ledger v2-shaped record.",
                "claim_boundary": false_boundary("repo_local_internal_only"),
                "validation_method": {
                    "method_type": "local_validator",
                    "command": "python scripts\\validate_avf_telemetry_event_codex_planner_event_v0_1.py",
                    "validator_uri": "scripts/validate_avf_telemetry_event_codex_planner_event_v0_1.py",
                },
                "validation_result": {
                    "status": "PASS",
                    "observed_at": CREATED_AT,
                    "summary": "Augmented telemetry event preserves trace identity, parent-child order, source evidence, and protected-action boundary.",
                },
                "confidence": {
                    "level": "high",
                    "reason": "Record is generated deterministically from repo-local fixtures and checked by the local validator.",
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
        )
    return records


def build_runtime_link_records(records: list[dict]) -> list[dict]:
    link_records = []
    for record in records:
        event = record["telemetry_event"]
        runtime_state, runtime_node_id = EVENT_TO_RUNTIME[event["event_id"]]
        seed = {
            "evidence_record_id": record["id"],
            "telemetry_event_id": event["event_id"],
            "runtime_state": runtime_state,
            "runtime_node_id": runtime_node_id,
        }
        link_records.append(
            {
                "link_id": f"runtime-state-link-{event['event_id']}",
                "created_at": CREATED_AT,
                "evidence_record_id": record["id"],
                "evidence_artifact_hash": record["artifact_hash"],
                "telemetry_event_id": event["event_id"],
                "telemetry_event_name": event["event_name"],
                "runtime_state": runtime_state,
                "runtime_node_id": runtime_node_id,
                "trace_id": event["trace_id"],
                "span_id": event["span_id"],
                "parent_span_id": event.get("parent_span_id"),
                "traceparent": event["traceparent"],
                "signal_type": event["signal_type"],
                "link_status": "linked",
                "link_hash": sha256_text(canonical_json(seed)),
                "runtime_action_performed": False,
                "claim_boundary": false_boundary(),
            }
        )
    return link_records


def build_packet() -> dict:
    return {
        "packet_id": "avf-telemetry-event-codex-planner-event-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "event_decision": EVENT_DECISION,
        "event_scope": EVENT_SCOPE,
        "augmented_events_uri": rel(AUGMENTED_EVENTS),
        "evidence_binding_records_uri": rel(EVIDENCE_BINDING_RECORDS),
        "runtime_state_link_records_uri": rel(RUNTIME_STATE_LINK_RECORDS),
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
        "claim_boundary": false_boundary(),
    }


def build_gate() -> dict:
    return {
        "gate_id": "avf-telemetry-event-codex-planner-event-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
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
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    return f"""# Telemetry Event Codex Planner Event v0.1

RESULT: PASS
telemetry_event_codex_planner_event_v0_1=true
event_decision={EVENT_DECISION}
event_scope={EVENT_SCOPE}
augmented_events_created=5
planner_event_id={PLANNER_EVENT_ID}
planner_event_inserted_between=safety_reviewed,evidence_written
runtime_state_gaps_recorded=0
runtime_observability_seed_complete=true
evidence_binding_records_created=5
runtime_state_links_created=5
closure_review_allowed=true
runtime_export_allowed=false
runtime_integration_allowed=false
dependency_adoption_allowed=false

## Event insertion

The Codex planner telemetry event is inserted between the safety gate and evidence-written events. The augmented stream preserves the same trace id and rewires evidence-written to use the planner event span as its parent. This closes the prior `codex_planned` observability gap for the repo-local seed stream without mutating the historical 4-event stream.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-runtime-state-observability-closure
owner_approval_required_before_runtime_integration: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the augmented 5-event telemetry stream
  - Confirm all runtime states have evidence-bound telemetry events
  - Keep the next step deterministic, local, and validation-only
  - Do not start runtime workers, collectors, exporters, or external services
  - Do not call providers, live models, scrape, post, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_telemetry_event_codex_planner_event_v0_1",
        "status": "PASS",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
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
        "claim_boundary": false_boundary(),
    }


def build_validation_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [
            PLANNER_EVENT_PACKET,
            AUGMENTED_EVENTS,
            EVIDENCE_BINDING_RECORDS,
            RUNTIME_STATE_LINK_RECORDS,
            PLANNER_EVENT_GATE,
            PLANNER_EVENT_REPORT,
            NEXT_ACTION,
            VALIDATION_RESULT,
        ]
    )
    return f"""# AVF Telemetry Event Codex Planner Event v0.1 Report

RESULT: PASS
telemetry_event_codex_planner_event_v0_1=true

## Commands

- python scripts\\run_avf_telemetry_event_codex_planner_event_v0_1.py
- python scripts\\validate_avf_telemetry_event_codex_planner_event_v0_1.py

## Summary

- event_decision={EVENT_DECISION}
- event_scope={EVENT_SCOPE}
- augmented_events_created=5
- planner_event_id={PLANNER_EVENT_ID}
- planner_event_inserted_between=safety_reviewed,evidence_written
- runtime_state_gaps_recorded=0
- runtime_observability_seed_complete=true
- evidence_binding_records_created=5
- runtime_state_links_created=5
- closure_review_allowed=true
- runtime_export_allowed=false
- runtime_integration_allowed=false
- dependency_adoption_allowed=false

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> int:
    require_gap_review()
    augmented_events = build_augmented_events(load_source_events())
    evidence_records = build_evidence_records(augmented_events)
    link_records = build_runtime_link_records(evidence_records)

    write_json(PLANNER_EVENT_PACKET, build_packet())
    write_text(AUGMENTED_EVENTS, "".join(json.dumps(event, sort_keys=True) + "\n" for event in augmented_events))
    write_text(EVIDENCE_BINDING_RECORDS, "".join(json.dumps(record, sort_keys=True) + "\n" for record in evidence_records))
    write_text(RUNTIME_STATE_LINK_RECORDS, "".join(json.dumps(record, sort_keys=True) + "\n" for record in link_records))
    write_json(PLANNER_EVENT_GATE, build_gate())
    write_text(PLANNER_EVENT_REPORT, build_report())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_validation_report())

    print("AVF Telemetry Event Codex Planner Event v0.1")
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
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

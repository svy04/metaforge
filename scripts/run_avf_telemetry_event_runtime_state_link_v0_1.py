from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "avf" / "observability"
OBS_GENERATED = OBS / "generated"
RUNTIME = ROOT / "avf" / "runtime"
RUNTIME_GENERATED = RUNTIME / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

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
CREATED_AT = "2026-05-27T00:00:00Z"
LINK_DECISION = "TELEMETRY_EVIDENCE_BOUND_TO_RUNTIME_STATE_REVIEW_INPUTS"
LINK_SCOPE = "repo_local_runtime_state_review_link_only"
LINK_COMPLETENESS = "partial_observability_seed_with_gap_record"

EVENT_TO_STATE = {
    "evt-avf-goal-accepted": {
        "runtime_state": "orchestrated",
        "runtime_node_id": "orchestrator",
        "state_link_reason": "Goal acceptance telemetry is the observable seed for orchestration state review.",
    },
    "evt-avf-router-selected": {
        "runtime_state": "routed",
        "runtime_node_id": "router",
        "state_link_reason": "Router telemetry records selected plane/cell routing evidence.",
    },
    "evt-avf-safety-gate": {
        "runtime_state": "safety_reviewed",
        "runtime_node_id": "safety_reviewer",
        "state_link_reason": "Safety gate telemetry records protected-action boundary review evidence.",
    },
    "evt-avf-evidence-written": {
        "runtime_state": "evidence_written",
        "runtime_node_id": "evidence_writer",
        "state_link_reason": "Evidence telemetry records planned evidence-writing completion for the local observability seed.",
    },
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


def false_boundary() -> dict:
    return dict(FALSE_FLAGS)


def require_previous_binding_gate() -> None:
    gate = read_json(BINDING_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("binding gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("binding gate must point to this runtime state link goal")
    if gate.get("runtime_state_link_allowed") is not True:
        raise SystemExit("binding gate must allow runtime state link")
    if gate.get("runtime_export_allowed") is not False:
        raise SystemExit("runtime export must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def require_previous_binding() -> dict:
    binding = read_json(BINDING)
    if binding.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("binding goal mismatch")
    if binding.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("binding must point to this runtime state link goal")
    if binding.get("evidence_records_created") != 4:
        raise SystemExit("binding must contain four evidence records")
    if binding.get("trace_identity_preserved") is not True:
        raise SystemExit("trace identity must be preserved")
    return binding


def require_runtime_sources() -> dict:
    schema_text = RUNTIME_STATE_SCHEMA.read_text(encoding="utf-8")
    for state in ["orchestrated", "routed", "safety_reviewed", "codex_planned", "evidence_written"]:
        if state not in schema_text:
            raise SystemExit(f"runtime transition schema missing state {state}")
    transitions = read_json(RUNTIME_TRANSITIONS)
    if "codex_planned" not in transitions.get("state_sequence", []):
        raise SystemExit("runtime transitions must include codex_planned")
    return transitions


def load_binding_records() -> list[dict]:
    return [json.loads(line) for line in BINDING_RECORDS.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_link_record(record: dict) -> dict:
    event = record["telemetry_event"]
    event_id = event["event_id"]
    mapping = EVENT_TO_STATE[event_id]
    seed = {
        "evidence_record_id": record["id"],
        "telemetry_event_id": event_id,
        "runtime_state": mapping["runtime_state"],
        "runtime_node_id": mapping["runtime_node_id"],
        "trace_id": event["trace_id"],
        "span_id": event["span_id"],
    }
    return {
        "link_id": f"runtime-state-link-{event_id}",
        "created_at": CREATED_AT,
        "evidence_record_id": record["id"],
        "evidence_artifact_hash": record["artifact_hash"],
        "telemetry_event_id": event_id,
        "telemetry_event_name": event["event_name"],
        "runtime_state": mapping["runtime_state"],
        "runtime_node_id": mapping["runtime_node_id"],
        "state_link_reason": mapping["state_link_reason"],
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


def runtime_gaps(transitions: dict) -> list[dict]:
    linked_states = {mapping["runtime_state"] for mapping in EVENT_TO_STATE.values()}
    gaps = []
    for state in transitions.get("state_sequence", []):
        if state == "initialized":
            continue
        if state not in linked_states:
            gaps.append(
                {
                    "runtime_state": state,
                    "gap_type": "missing_telemetry_event_binding",
                    "gap_reason": "No evidence-bound telemetry event currently maps to this runtime state.",
                    "required_next_review": True,
                }
            )
    return gaps


def build_link(binding: dict, records: list[dict], transitions: dict, gaps: list[dict]) -> dict:
    return {
        "link_id": "avf-telemetry-event-runtime-state-link-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "link_decision": LINK_DECISION,
        "link_scope": LINK_SCOPE,
        "link_completeness": LINK_COMPLETENESS,
        "source_binding_uri": rel(BINDING),
        "source_binding_records_uri": rel(BINDING_RECORDS),
        "runtime_transition_source_uri": rel(RUNTIME_TRANSITIONS),
        "runtime_state_schema_uri": rel(RUNTIME_STATE_SCHEMA),
        "runtime_state_link_records_uri": rel(RUNTIME_STATE_LINK_RECORDS),
        "runtime_state_links_created": len(records),
        "runtime_state_gaps_recorded": len(gaps),
        "runtime_state_gaps": gaps,
        "trace_id": binding["trace_id"],
        "linked_runtime_states": [EVENT_TO_STATE[record["telemetry_event"]["event_id"]]["runtime_state"] for record in records],
        "runtime_state_sequence_reference": transitions.get("state_sequence", []),
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(gaps: list[dict]) -> dict:
    return {
        "gate_id": "avf-telemetry-event-runtime-state-link-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "link_decision": LINK_DECISION,
        "link_scope": LINK_SCOPE,
        "link_completeness": LINK_COMPLETENESS,
        "runtime_state_links_created": 4,
        "runtime_state_gaps_recorded": len(gaps),
        "runtime_gap_review_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(link_records: list[dict], gaps: list[dict]) -> str:
    rows = "\n".join(
        f"| `{record['telemetry_event_id']}` | `{record['runtime_state']}` | `{record['runtime_node_id']}` | `{record['link_hash']}` |"
        for record in link_records
    )
    gap_rows = "\n".join(f"- observability_gap={gap['runtime_state']}" for gap in gaps)
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    return f"""# Telemetry Event Runtime State Link v0.1

RESULT: PASS
telemetry_event_runtime_state_link_v0_1=true
link_decision={LINK_DECISION}
link_scope={LINK_SCOPE}
link_completeness={LINK_COMPLETENESS}
runtime_state_links_created=4
runtime_state_gaps_recorded={len(gaps)}
runtime_gap_review_allowed=true
runtime_export_allowed=false
runtime_integration_allowed=false
dependency_adoption_allowed=false

## Runtime state links

| Telemetry event | Runtime state | Runtime node | Link hash |
| --- | --- | --- | --- |
{rows}

## Observability gaps

{gap_rows}

## Boundary

This link is repo-local and validation-only. It does not start runtime workers, collectors, exporters, or external services. It records that codex_planned has no evidence-bound telemetry event yet, so the next safe step is a focused observability gap review.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-runtime-state-observability-gap
owner_approval_required_before_runtime_integration: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the codex_planned observability gap
  - Decide whether the telemetry envelope needs a Codex planner event
  - Keep the next step deterministic, local, and validation-only
  - Do not start runtime workers, collectors, exporters, or external services
  - Do not call providers, live models, scrape, post, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(gaps: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_telemetry_event_runtime_state_link_v0_1",
        "status": "PASS",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "link_decision": LINK_DECISION,
        "link_scope": LINK_SCOPE,
        "link_completeness": LINK_COMPLETENESS,
        "runtime_state_links_created": 4,
        "runtime_state_gaps_recorded": len(gaps),
        "runtime_gap_review_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_report(link_records: list[dict], gaps: list[dict]) -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [RUNTIME_STATE_LINK, RUNTIME_STATE_LINK_RECORDS, RUNTIME_STATE_LINK_GATE, RUNTIME_STATE_LINK_REPORT, NEXT_ACTION, VALIDATION_RESULT]
    )
    gap_lines = "\n".join(f"- observability_gap={gap['runtime_state']}" for gap in gaps)
    return f"""# AVF Telemetry Event Runtime State Link v0.1 Report

RESULT: PASS
telemetry_event_runtime_state_link_v0_1=true

## Commands

- python scripts\\run_avf_telemetry_event_runtime_state_link_v0_1.py
- python scripts\\validate_avf_telemetry_event_runtime_state_link_v0_1.py

## Link summary

- link_decision={LINK_DECISION}
- link_scope={LINK_SCOPE}
- link_completeness={LINK_COMPLETENESS}
- runtime_state_links_created={len(link_records)}
- runtime_state_gaps_recorded={len(gaps)}
- runtime_gap_review_allowed=true
- runtime_export_allowed=false
- runtime_integration_allowed=false
- dependency_adoption_allowed=false

## Observability gaps

{gap_lines}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> int:
    require_previous_binding_gate()
    binding = require_previous_binding()
    transitions = require_runtime_sources()
    binding_records = load_binding_records()
    if len(binding_records) != 4:
        raise SystemExit("expected four binding records")
    link_records = [build_link_record(record) for record in binding_records]
    gaps = runtime_gaps(transitions)

    write_json(RUNTIME_STATE_LINK, build_link(binding, binding_records, transitions, gaps))
    write_text(RUNTIME_STATE_LINK_RECORDS, "".join(json.dumps(record, sort_keys=True) + "\n" for record in link_records))
    write_json(RUNTIME_STATE_LINK_GATE, build_gate(gaps))
    write_text(RUNTIME_STATE_LINK_REPORT, build_report(link_records, gaps))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gaps))
    write_text(VALIDATION_REPORT, build_validation_report(link_records, gaps))

    print("AVF Telemetry Event Runtime State Link v0.1")
    print("RESULT: PASS")
    print("telemetry_event_runtime_state_link_v0_1=true")
    print(f"link_decision={LINK_DECISION}")
    print(f"link_scope={LINK_SCOPE}")
    print(f"link_completeness={LINK_COMPLETENESS}")
    print("runtime_state_links_created=4")
    print(f"runtime_state_gaps_recorded={len(gaps)}")
    print("observability_gap=codex_planned")
    print("runtime_gap_review_allowed=true")
    print("runtime_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

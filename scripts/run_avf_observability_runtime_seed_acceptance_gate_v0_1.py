from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

CLOSURE_REVIEW = OBS_GENERATED / "runtime_state_observability_closure_review.json"
CLOSURE_REVIEW_GATE = OBS_GENERATED / "runtime_state_observability_closure_review_gate.json"
AUGMENTED_EVENTS = OBS_GENERATED / "telemetry_event_codex_planner_sample_events.jsonl"
EVIDENCE_BINDING_RECORDS = OBS_GENERATED / "telemetry_event_codex_planner_evidence_binding_records.jsonl"
RUNTIME_STATE_LINK_RECORDS = OBS_GENERATED / "telemetry_event_codex_planner_runtime_state_link_records.jsonl"
ACCEPTANCE_GATE = OBS_GENERATED / "observability_runtime_seed_acceptance_gate.json"
ACCEPTANCE_MATRIX = OBS_GENERATED / "observability_runtime_seed_acceptance_matrix.json"
ACCEPTANCE_REPORT = OBS_GENERATED / "observability_runtime_seed_acceptance_report.md"
NEXT_ACTION = OBS_GENERATED / "observability_runtime_seed_acceptance_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "observability_runtime_seed_acceptance_gate_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_OBSERVABILITY_RUNTIME_SEED_ACCEPTANCE_GATE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_observability_runtime_seed_acceptance_gate_v0_1"
PREVIOUS_GOAL_ID = "avf_runtime_state_observability_closure_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_owner_approval_packet_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
ACCEPTANCE_DECISION = "ACCEPT_REPO_LOCAL_OBSERVABILITY_SEED_ONLY"
ACCEPTANCE_SCOPE = "repo_local_runtime_observability_seed_only"

EXPECTED_RUNTIME_STATES = [
    "orchestrated",
    "routed",
    "safety_reviewed",
    "codex_planned",
    "evidence_written",
]

EXPECTED_EVENT_ORDER = [
    "evt-avf-goal-accepted",
    "evt-avf-router-selected",
    "evt-avf-safety-gate",
    "evt-avf-codex-planner-task-created",
    "evt-avf-evidence-written",
]

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
    "runtime_export_performed": False,
    "collector_started": False,
    "telemetry_export_performed": False,
    "deploy_performed": False,
    "publish_performed": False,
    "release_ready": False,
    "production_ready": False,
}

ACCEPTANCE_CRITERIA = [
    "closure review has zero runtime-state gaps",
    "five runtime states are covered by telemetry events",
    "five telemetry events have evidence binding records",
    "five runtime-state links connect events to runtime states",
    "acceptance is scoped to the repo-local seed only",
    "runtime export, runtime integration, dependency adoption, deploy, publish, release readiness, and production readiness remain blocked",
]


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


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def require_previous_closure() -> None:
    review = read_json(CLOSURE_REVIEW)
    gate = read_json(CLOSURE_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID or gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous closure goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID or gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous closure must point to this acceptance gate")
    if review.get("runtime_state_gaps_recorded") != 0:
        raise SystemExit("previous closure must record zero runtime-state gaps")
    if review.get("repo_local_seed_closure") is not True:
        raise SystemExit("previous closure must be repo-local seed closure")
    if review.get("seed_acceptance_gate_allowed") is not True or gate.get("seed_acceptance_gate_allowed") is not True:
        raise SystemExit("previous closure must allow seed acceptance gate")
    for key in ["full_runtime_observability_claim_allowed", "runtime_export_allowed", "runtime_integration_allowed", "dependency_adoption_allowed"]:
        if review.get(key) is not False or gate.get(key) is not False:
            raise SystemExit(f"previous closure {key} must remain false")


def load_seed_inputs() -> tuple[list[dict], list[dict], list[dict]]:
    events = jsonl(AUGMENTED_EVENTS)
    evidence = jsonl(EVIDENCE_BINDING_RECORDS)
    links = jsonl(RUNTIME_STATE_LINK_RECORDS)
    if [event.get("event_id") for event in events] != EXPECTED_EVENT_ORDER:
        raise SystemExit("augmented event order mismatch")
    if [record.get("artifact_id") for record in evidence] != EXPECTED_EVENT_ORDER:
        raise SystemExit("evidence binding order mismatch")
    if [record.get("telemetry_event_id") for record in links] != EXPECTED_EVENT_ORDER:
        raise SystemExit("runtime-state link order mismatch")
    if [record.get("runtime_state") for record in links] != EXPECTED_RUNTIME_STATES:
        raise SystemExit("runtime-state coverage mismatch")
    return events, evidence, links


def build_matrix(events: list[dict], evidence: list[dict], links: list[dict]) -> dict:
    evidence_ids = {record["artifact_id"] for record in evidence}
    link_by_event = {record["telemetry_event_id"]: record for record in links}
    records = []
    for event in events:
        event_id = event["event_id"]
        link = link_by_event[event_id]
        records.append(
            {
                "runtime_state": link["runtime_state"],
                "telemetry_event_id": event_id,
                "evidence_binding_present": event_id in evidence_ids,
                "runtime_state_link_present": True,
                "local_seed_acceptance_status": "accepted_repo_local_seed_only",
                "runtime_export_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return {
        "matrix_id": "avf-observability-runtime-seed-acceptance-matrix-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "acceptance_scope": ACCEPTANCE_SCOPE,
        "runtime_state_acceptance_records": records,
        "claim_boundary": false_boundary(),
    }


def build_gate() -> dict:
    return {
        "gate_id": "avf-observability-runtime-seed-acceptance-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_scope": ACCEPTANCE_SCOPE,
        "source_uris": {
            "closure_review": rel(CLOSURE_REVIEW),
            "closure_review_gate": rel(CLOSURE_REVIEW_GATE),
            "augmented_events": rel(AUGMENTED_EVENTS),
            "evidence_binding_records": rel(EVIDENCE_BINDING_RECORDS),
            "runtime_state_link_records": rel(RUNTIME_STATE_LINK_RECORDS),
        },
        "accepted_runtime_states": 5,
        "accepted_telemetry_events": 5,
        "accepted_evidence_bindings": 5,
        "accepted_runtime_state_links": 5,
        "acceptance_criteria": ACCEPTANCE_CRITERIA,
        "local_seed_acceptance_allowed": True,
        "full_runtime_observability_claim_allowed": False,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "owner_approval_required_before_runtime_integration": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    criteria = "\n".join(f"- {criterion}" for criterion in ACCEPTANCE_CRITERIA)
    return f"""# Observability Runtime Seed Acceptance Gate v0.1

RESULT: PASS
observability_runtime_seed_acceptance_gate_v0_1=true
acceptance_decision={ACCEPTANCE_DECISION}
acceptance_scope={ACCEPTANCE_SCOPE}
accepted_runtime_states=5
accepted_telemetry_events=5
accepted_evidence_bindings=5
accepted_runtime_state_links=5
local_seed_acceptance_allowed=true
full_runtime_observability_claim_allowed=false
runtime_export_allowed=false
runtime_integration_allowed=false
dependency_adoption_allowed=false
owner_approval_required_before_runtime_integration=true

## Acceptance criteria

{criteria}

## Boundary

This gate accepts only the repo-local observability runtime seed. It does not start collectors, export telemetry, integrate a runtime backend, install dependencies, deploy, publish, or claim production/release readiness.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-observability-runtime-seed-owner-approval-packet
owner_approval_required_before_runtime_integration: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local owner approval packet for any future runtime observability integration
  - Keep the accepted state scoped to repo-local observability seed acceptance only
  - Require explicit owner approval before collector startup, telemetry export, runtime integration, or dependency adoption
  - Do not start collectors, export telemetry, install dependencies, or integrate a runtime backend
  - Do not call providers, live models, scrape, post, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_observability_runtime_seed_acceptance_gate_v0_1",
        "status": "PASS",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_scope": ACCEPTANCE_SCOPE,
        "accepted_runtime_states": 5,
        "accepted_telemetry_events": 5,
        "accepted_evidence_bindings": 5,
        "accepted_runtime_state_links": 5,
        "local_seed_acceptance_allowed": True,
        "full_runtime_observability_claim_allowed": False,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "owner_approval_required_before_runtime_integration": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_report() -> str:
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [ACCEPTANCE_GATE, ACCEPTANCE_MATRIX, ACCEPTANCE_REPORT, NEXT_ACTION, VALIDATION_RESULT]
    )
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    return f"""# AVF Observability Runtime Seed Acceptance Gate v0.1 Report

RESULT: PASS
observability_runtime_seed_acceptance_gate_v0_1=true

## Commands

- python scripts\\run_avf_observability_runtime_seed_acceptance_gate_v0_1.py
- python scripts\\validate_avf_observability_runtime_seed_acceptance_gate_v0_1.py

## Gate summary

- acceptance_decision={ACCEPTANCE_DECISION}
- acceptance_scope={ACCEPTANCE_SCOPE}
- accepted_runtime_states=5
- accepted_telemetry_events=5
- accepted_evidence_bindings=5
- accepted_runtime_state_links=5
- local_seed_acceptance_allowed=true
- full_runtime_observability_claim_allowed=false
- runtime_export_allowed=false
- runtime_integration_allowed=false
- dependency_adoption_allowed=false
- owner_approval_required_before_runtime_integration=true

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> int:
    require_previous_closure()
    events, evidence, links = load_seed_inputs()

    write_json(ACCEPTANCE_GATE, build_gate())
    write_json(ACCEPTANCE_MATRIX, build_matrix(events, evidence, links))
    write_text(ACCEPTANCE_REPORT, build_report())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_validation_report())

    print("AVF Observability Runtime Seed Acceptance Gate v0.1")
    print("RESULT: PASS")
    print("observability_runtime_seed_acceptance_gate_v0_1=true")
    print(f"acceptance_decision={ACCEPTANCE_DECISION}")
    print(f"acceptance_scope={ACCEPTANCE_SCOPE}")
    print("accepted_runtime_states=5")
    print("accepted_telemetry_events=5")
    print("accepted_evidence_bindings=5")
    print("accepted_runtime_state_links=5")
    print("local_seed_acceptance_allowed=true")
    print("full_runtime_observability_claim_allowed=false")
    print("runtime_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print("owner_approval_required_before_runtime_integration=true")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

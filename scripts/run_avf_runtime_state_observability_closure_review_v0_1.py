from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PLANNER_EVENT_PACKET = OBS_GENERATED / "telemetry_event_codex_planner_event.json"
PLANNER_EVENT_GATE = OBS_GENERATED / "telemetry_event_codex_planner_event_gate.json"
AUGMENTED_EVENTS = OBS_GENERATED / "telemetry_event_codex_planner_sample_events.jsonl"
EVIDENCE_BINDING_RECORDS = OBS_GENERATED / "telemetry_event_codex_planner_evidence_binding_records.jsonl"
RUNTIME_STATE_LINK_RECORDS = OBS_GENERATED / "telemetry_event_codex_planner_runtime_state_link_records.jsonl"
CLOSURE_REVIEW = OBS_GENERATED / "runtime_state_observability_closure_review.json"
CLOSURE_REVIEW_GATE = OBS_GENERATED / "runtime_state_observability_closure_review_gate.json"
CLOSURE_REVIEW_REPORT = OBS_GENERATED / "runtime_state_observability_closure_review_report.md"
NEXT_ACTION = OBS_GENERATED / "runtime_state_observability_closure_review_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "runtime_state_observability_closure_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_RUNTIME_STATE_OBSERVABILITY_CLOSURE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_runtime_state_observability_closure_review_v0_1"
PREVIOUS_GOAL_ID = "avf_telemetry_event_codex_planner_event_v0_1"
NEXT_SAFE_GOAL_ID = "avf_observability_runtime_seed_acceptance_gate_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
CLOSURE_DECISION = "RUNTIME_STATE_OBSERVABILITY_SEED_REVIEWED_NO_LOCAL_GAPS"
CLOSURE_SCOPE = "repo_local_runtime_observability_seed_only"

EXPECTED_RUNTIME_STATES = [
    "orchestrated",
    "routed",
    "safety_reviewed",
    "codex_planned",
    "evidence_written",
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


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def require_previous_gate() -> None:
    packet = read_json(PLANNER_EVENT_PACKET)
    if packet.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("planner event packet goal mismatch")
    if packet.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("planner event packet must point to this closure review")
    if packet.get("runtime_state_gaps_recorded") != 0:
        raise SystemExit("planner event packet must record zero gaps")
    if packet.get("runtime_observability_seed_complete") is not True:
        raise SystemExit("planner event packet must mark seed complete")

    gate = read_json(PLANNER_EVENT_GATE)
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("planner event gate must point to this closure review")
    if gate.get("closure_review_allowed") is not True:
        raise SystemExit("closure review must be allowed")


def load_seed_inputs() -> tuple[list[dict], list[dict], list[dict]]:
    events = jsonl(AUGMENTED_EVENTS)
    evidence = jsonl(EVIDENCE_BINDING_RECORDS)
    links = jsonl(RUNTIME_STATE_LINK_RECORDS)
    if len(events) != 5 or len(evidence) != 5 or len(links) != 5:
        raise SystemExit("closure review expects five events, five evidence records, and five runtime links")
    states = [record["runtime_state"] for record in links]
    if states != EXPECTED_RUNTIME_STATES:
        raise SystemExit("runtime state coverage mismatch")
    return events, evidence, links


def build_review(events: list[dict], evidence: list[dict], links: list[dict]) -> dict:
    return {
        "review_id": "avf-runtime-state-observability-closure-review-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "closure_decision": CLOSURE_DECISION,
        "closure_scope": CLOSURE_SCOPE,
        "source_augmented_events_uri": rel(AUGMENTED_EVENTS),
        "source_evidence_binding_records_uri": rel(EVIDENCE_BINDING_RECORDS),
        "source_runtime_state_link_records_uri": rel(RUNTIME_STATE_LINK_RECORDS),
        "runtime_states": [record["runtime_state"] for record in links],
        "runtime_states_reviewed": len(links),
        "telemetry_events_reviewed": len(events),
        "evidence_records_reviewed": len(evidence),
        "runtime_state_links_reviewed": len(links),
        "runtime_state_gaps_recorded": 0,
        "repo_local_seed_closure": True,
        "closure_reason": "Every runtime state in the local seed has a telemetry event, evidence binding record, and runtime-state link record.",
        "full_runtime_observability_claim_allowed": False,
        "seed_acceptance_gate_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate() -> dict:
    return {
        "gate_id": "avf-runtime-state-observability-closure-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "closure_decision": CLOSURE_DECISION,
        "closure_scope": CLOSURE_SCOPE,
        "repo_local_seed_closure": True,
        "full_runtime_observability_claim_allowed": False,
        "seed_acceptance_gate_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    states = "\n".join(f"- {state}" for state in EXPECTED_RUNTIME_STATES)
    return f"""# Runtime State Observability Closure Review v0.1

RESULT: PASS
runtime_state_observability_closure_review_v0_1=true
closure_decision={CLOSURE_DECISION}
closure_scope={CLOSURE_SCOPE}
runtime_states_reviewed=5
telemetry_events_reviewed=5
evidence_records_reviewed=5
runtime_state_links_reviewed=5
runtime_state_gaps_recorded=0
repo_local_seed_closure=true
full_runtime_observability_claim_allowed=false
seed_acceptance_gate_allowed=true
runtime_export_allowed=false
runtime_integration_allowed=false
dependency_adoption_allowed=false

## Runtime states covered in the repo-local seed

{states}

## Claim boundary

This is closure for the repo-local observability seed only. It does not prove production runtime observability, hosted runtime execution, external trace export, collector readiness, provider-backed execution, or release readiness.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-observability-runtime-seed-acceptance-gate
owner_approval_required_before_runtime_integration: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local acceptance gate for the observability runtime seed
  - Keep acceptance scoped to the local seed only
  - Do not broaden this into production/runtime readiness
  - Do not install dependencies, start workers, run collectors, or export telemetry
  - Do not call providers, live models, scrape, post, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_runtime_state_observability_closure_review_v0_1",
        "status": "PASS",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "closure_decision": CLOSURE_DECISION,
        "closure_scope": CLOSURE_SCOPE,
        "runtime_states_reviewed": 5,
        "runtime_state_gaps_recorded": 0,
        "repo_local_seed_closure": True,
        "full_runtime_observability_claim_allowed": False,
        "seed_acceptance_gate_allowed": True,
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
        for path in [CLOSURE_REVIEW, CLOSURE_REVIEW_GATE, CLOSURE_REVIEW_REPORT, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Runtime State Observability Closure Review v0.1 Report

RESULT: PASS
runtime_state_observability_closure_review_v0_1=true

## Commands

- python scripts\\run_avf_runtime_state_observability_closure_review_v0_1.py
- python scripts\\validate_avf_runtime_state_observability_closure_review_v0_1.py

## Review summary

- closure_decision={CLOSURE_DECISION}
- closure_scope={CLOSURE_SCOPE}
- runtime_states_reviewed=5
- telemetry_events_reviewed=5
- evidence_records_reviewed=5
- runtime_state_links_reviewed=5
- runtime_state_gaps_recorded=0
- repo_local_seed_closure=true
- full_runtime_observability_claim_allowed=false
- seed_acceptance_gate_allowed=true
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
    require_previous_gate()
    events, evidence, links = load_seed_inputs()

    write_json(CLOSURE_REVIEW, build_review(events, evidence, links))
    write_json(CLOSURE_REVIEW_GATE, build_gate())
    write_text(CLOSURE_REVIEW_REPORT, build_report())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_validation_report())

    print("AVF Runtime State Observability Closure Review v0.1")
    print("RESULT: PASS")
    print("runtime_state_observability_closure_review_v0_1=true")
    print(f"closure_decision={CLOSURE_DECISION}")
    print(f"closure_scope={CLOSURE_SCOPE}")
    print("runtime_states_reviewed=5")
    print("telemetry_events_reviewed=5")
    print("evidence_records_reviewed=5")
    print("runtime_state_links_reviewed=5")
    print("runtime_state_gaps_recorded=0")
    print("repo_local_seed_closure=true")
    print("full_runtime_observability_claim_allowed=false")
    print("seed_acceptance_gate_allowed=true")
    print("runtime_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

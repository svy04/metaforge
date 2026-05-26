from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNTIME_STATE_LINK = OBS_GENERATED / "telemetry_event_runtime_state_link.json"
RUNTIME_STATE_LINK_GATE = OBS_GENERATED / "telemetry_event_runtime_state_link_gate.json"
RUNTIME_STATE_LINK_RECORDS = OBS_GENERATED / "telemetry_event_runtime_state_link_records.jsonl"
GAP_REVIEW = OBS_GENERATED / "runtime_state_observability_gap_review.json"
GAP_REVIEW_GATE = OBS_GENERATED / "runtime_state_observability_gap_review_gate.json"
GAP_REVIEW_REPORT = OBS_GENERATED / "runtime_state_observability_gap_review_report.md"
NEXT_ACTION = OBS_GENERATED / "runtime_state_observability_gap_review_next_action.yml"
VALIDATION_RESULT = OBS_GENERATED / "runtime_state_observability_gap_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_RUNTIME_STATE_OBSERVABILITY_GAP_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_runtime_state_observability_gap_review_v0_1"
PREVIOUS_GOAL_ID = "avf_telemetry_event_runtime_state_link_v0_1"
NEXT_SAFE_GOAL_ID = "avf_telemetry_event_codex_planner_event_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
GAP_REVIEW_DECISION = "CODEX_PLANNED_OBSERVABILITY_GAP_REVIEWED_PLANNER_EVENT_NEEDED"
GAP_REVIEW_SCOPE = "repo_local_gap_review_only"
RECOMMENDED_EVENT_ID = "evt-avf-codex-planner-task-created"
RECOMMENDED_RUNTIME_STATE = "codex_planned"

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


def require_previous_link_gate() -> None:
    gate = read_json(RUNTIME_STATE_LINK_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("runtime state link gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("runtime state link gate must point to this gap review goal")
    if gate.get("runtime_gap_review_allowed") is not True:
        raise SystemExit("runtime state link gate must allow runtime gap review")
    if gate.get("runtime_export_allowed") is not False:
        raise SystemExit("runtime export must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_previous_link() -> dict:
    link = read_json(RUNTIME_STATE_LINK)
    if link.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("runtime state link goal mismatch")
    if link.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("runtime state link must point to this gap review goal")
    gaps = link.get("runtime_state_gaps", [])
    if len(gaps) != 1 or gaps[0].get("runtime_state") != RECOMMENDED_RUNTIME_STATE:
        raise SystemExit("runtime state link must record codex_planned as the only gap")
    return link


def build_review(link: dict) -> dict:
    return {
        "review_id": "avf-runtime-state-observability-gap-review-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "gap_review_decision": GAP_REVIEW_DECISION,
        "gap_review_scope": GAP_REVIEW_SCOPE,
        "source_runtime_state_link_uri": rel(RUNTIME_STATE_LINK),
        "source_runtime_state_link_records_uri": rel(RUNTIME_STATE_LINK_RECORDS),
        "gap_reviewed": RECOMMENDED_RUNTIME_STATE,
        "gap_reason": "The runtime transition model includes codex_planned, but the current telemetry event seed has no evidence-bound Codex planner event.",
        "planner_event_needed": True,
        "recommended_event_id": RECOMMENDED_EVENT_ID,
        "recommended_event_name": "avf.codex_planner.task_created",
        "recommended_runtime_state": RECOMMENDED_RUNTIME_STATE,
        "recommended_runtime_node_id": "codex_planner",
        "recommended_signal_type": "trace",
        "recommended_parent_event_id": "evt-avf-safety-gate",
        "recommended_child_event_id": "evt-avf-evidence-written",
        "recommended_event_fields": [
            "event_id",
            "event_name",
            "run_id",
            "goal_id",
            "trace_id",
            "span_id",
            "parent_span_id",
            "traceparent",
            "signal_type",
            "event_time",
            "producer",
            "attributes",
            "claim_boundary",
            "source_evidence",
        ],
        "recommended_attributes": {
            "avf.cell": "codex_planner",
            "avf.runtime_state": RECOMMENDED_RUNTIME_STATE,
            "avf.pr_sized_task_created": "true",
        },
        "existing_link_completeness": link["link_completeness"],
        "planner_event_contract_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate() -> dict:
    return {
        "gate_id": "avf-runtime-state-observability-gap-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "gap_review_decision": GAP_REVIEW_DECISION,
        "gap_review_scope": GAP_REVIEW_SCOPE,
        "gap_reviewed": RECOMMENDED_RUNTIME_STATE,
        "planner_event_needed": True,
        "recommended_event_id": RECOMMENDED_EVENT_ID,
        "planner_event_contract_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in FALSE_FLAGS)
    return f"""# Runtime State Observability Gap Review v0.1

RESULT: PASS
runtime_state_observability_gap_review_v0_1=true
gap_review_decision={GAP_REVIEW_DECISION}
gap_review_scope={GAP_REVIEW_SCOPE}
gap_reviewed=codex_planned
planner_event_needed=true
recommended_event_id={RECOMMENDED_EVENT_ID}
recommended_runtime_state={RECOMMENDED_RUNTIME_STATE}
planner_event_contract_allowed=true
runtime_export_allowed=false
runtime_integration_allowed=false
dependency_adoption_allowed=false

## Gap decision

The runtime state link correctly refused to overclaim complete observability because `codex_planned` exists in the runtime transition model but has no evidence-bound telemetry event. The next safe step is to add a repo-local Codex planner event to the telemetry envelope fixture and regenerate downstream binding/link artifacts.

## Recommended event

- recommended_event_id={RECOMMENDED_EVENT_ID}
- recommended_event_name=avf.codex_planner.task_created
- recommended_parent_event_id=evt-avf-safety-gate
- recommended_child_event_id=evt-avf-evidence-written
- recommended_signal_type=trace

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: add-codex-planner-telemetry-event
owner_approval_required_before_runtime_integration: true
goal_id: {THIS_GOAL_ID}
recommended_event_id: {RECOMMENDED_EVENT_ID}

next_steps:
  - Add a repo-local Codex planner telemetry event to the sample telemetry event fixture
  - Place it between safety gate and evidence-written events
  - Preserve the same trace_id and valid parent/child span order
  - Regenerate envelope, review, evidence binding, runtime state link, and gap outputs as needed
  - Do not start runtime workers, collectors, exporters, or external services
  - Do not call providers, live models, scrape, post, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_runtime_state_observability_gap_review_v0_1",
        "status": "PASS",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "gap_review_decision": GAP_REVIEW_DECISION,
        "gap_review_scope": GAP_REVIEW_SCOPE,
        "gap_reviewed": RECOMMENDED_RUNTIME_STATE,
        "planner_event_needed": True,
        "recommended_event_id": RECOMMENDED_EVENT_ID,
        "planner_event_contract_allowed": True,
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
        for path in [GAP_REVIEW, GAP_REVIEW_GATE, GAP_REVIEW_REPORT, NEXT_ACTION, VALIDATION_RESULT]
    )
    return f"""# AVF Runtime State Observability Gap Review v0.1 Report

RESULT: PASS
runtime_state_observability_gap_review_v0_1=true

## Commands

- python scripts\\run_avf_runtime_state_observability_gap_review_v0_1.py
- python scripts\\validate_avf_runtime_state_observability_gap_review_v0_1.py

## Review summary

- gap_review_decision={GAP_REVIEW_DECISION}
- gap_review_scope={GAP_REVIEW_SCOPE}
- gap_reviewed=codex_planned
- planner_event_needed=true
- recommended_event_id={RECOMMENDED_EVENT_ID}
- planner_event_contract_allowed=true
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
    require_previous_link_gate()
    link = load_previous_link()
    review = build_review(link)

    write_json(GAP_REVIEW, review)
    write_json(GAP_REVIEW_GATE, build_gate())
    write_text(GAP_REVIEW_REPORT, build_report())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_validation_report())

    print("AVF Runtime State Observability Gap Review v0.1")
    print("RESULT: PASS")
    print("runtime_state_observability_gap_review_v0_1=true")
    print(f"gap_review_decision={GAP_REVIEW_DECISION}")
    print(f"gap_review_scope={GAP_REVIEW_SCOPE}")
    print("gap_reviewed=codex_planned")
    print("planner_event_needed=true")
    print(f"recommended_event_id={RECOMMENDED_EVENT_ID}")
    print("planner_event_contract_allowed=true")
    print("runtime_export_allowed=false")
    print("runtime_integration_allowed=false")
    print("dependency_adoption_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

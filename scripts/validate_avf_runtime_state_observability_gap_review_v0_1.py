from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_runtime_state_observability_gap_review_v0_1.py"
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
GAP_REVIEW_DECISION = "CODEX_PLANNED_OBSERVABILITY_GAP_REVIEWED_PLANNER_EVENT_NEEDED"
GAP_REVIEW_SCOPE = "repo_local_gap_review_only"
RECOMMENDED_EVENT_ID = "evt-avf-codex-planner-task-created"
RECOMMENDED_RUNTIME_STATE = "codex_planned"

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
    RUNTIME_STATE_LINK,
    RUNTIME_STATE_LINK_GATE,
    RUNTIME_STATE_LINK_RECORDS,
    GAP_REVIEW,
    GAP_REVIEW_GATE,
    GAP_REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "runtime_state_observability_gap_review_v0_1=true",
    f"gap_review_decision={GAP_REVIEW_DECISION}",
    f"gap_review_scope={GAP_REVIEW_SCOPE}",
    "gap_reviewed=codex_planned",
    "planner_event_needed=true",
    f"recommended_event_id={RECOMMENDED_EVENT_ID}",
    "runtime_integration_allowed=false",
    "runtime_export_allowed=false",
    "dependency_adoption_allowed=false",
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

NEXT_ACTION_MARKERS = [
    "action_id: add-codex-planner-telemetry-event",
    "owner_approval_required_before_runtime_integration: true",
    f"recommended_event_id: {RECOMMENDED_EVENT_ID}",
    "Do not start runtime workers, collectors, exporters, or external services",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Runtime State Observability Gap Review v0.1 validation")
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


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{rel(path)} missing markers:\n" + "\n".join(missing))


def require_previous_link_gate() -> None:
    gate = read_json(RUNTIME_STATE_LINK_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("runtime state link gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("runtime state link gate must point to this gap review goal")
    if gate.get("status") != "PASS":
        fail("runtime state link gate must be PASS")
    if gate.get("runtime_gap_review_allowed") is not True:
        fail("runtime state link gate must allow runtime gap review")
    if gate.get("runtime_state_gaps_recorded") != 1:
        fail("runtime state link gate must record one gap")
    require_false_flags(gate.get("claim_boundary", {}), "runtime state link gate")


def require_previous_link() -> None:
    link = read_json(RUNTIME_STATE_LINK)
    if link.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("runtime state link goal mismatch")
    if link.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("runtime state link must point to this gap review goal")
    if link.get("link_completeness") != "partial_observability_seed_with_gap_record":
        fail("runtime state link must preserve partial completeness marker")
    gaps = link.get("runtime_state_gaps", [])
    if len(gaps) != 1 or gaps[0].get("runtime_state") != RECOMMENDED_RUNTIME_STATE:
        fail("runtime state link must record codex_planned as the only observability gap")
    if link.get("runtime_export_allowed") is not False:
        fail("runtime export must remain blocked")
    require_false_flags(link.get("claim_boundary", {}), "runtime state link")


def require_gap_review() -> None:
    review = read_json(GAP_REVIEW)
    expected = {
        "review_id": "avf-runtime-state-observability-gap-review-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "gap_review_decision": GAP_REVIEW_DECISION,
        "gap_review_scope": GAP_REVIEW_SCOPE,
        "gap_reviewed": RECOMMENDED_RUNTIME_STATE,
        "planner_event_needed": True,
        "recommended_event_id": RECOMMENDED_EVENT_ID,
        "recommended_runtime_state": RECOMMENDED_RUNTIME_STATE,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if review.get(key) != value:
            fail(f"gap review {key} mismatch")
    required_fields = set(review.get("recommended_event_fields", []))
    for field in ["event_id", "event_name", "run_id", "goal_id", "trace_id", "span_id", "traceparent", "signal_type", "claim_boundary", "source_evidence"]:
        if field not in required_fields:
            fail(f"recommended event missing field {field}")
    require_false_flags(review.get("claim_boundary", {}), "gap review")


def require_gap_review_gate() -> None:
    gate = read_json(GAP_REVIEW_GATE)
    expected = {
        "gate_id": "avf-runtime-state-observability-gap-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "gap_review_decision": GAP_REVIEW_DECISION,
        "gap_review_scope": GAP_REVIEW_SCOPE,
        "planner_event_contract_allowed": True,
        "runtime_export_allowed": False,
        "runtime_integration_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"gap review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "gap review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    expected = {
        "validator_id": "validate_avf_runtime_state_observability_gap_review_v0_1",
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
    }
    for key, value in expected.items():
        if result.get(key) != value:
            fail(f"validation result {key} mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_link_gate()
    require_previous_link()
    require_gap_review()
    require_gap_review_gate()
    require_validation_result()
    require_markers(GAP_REVIEW_REPORT, REPORT_MARKERS)
    require_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Runtime State Observability Gap Review v0.1 validation")
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

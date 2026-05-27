from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_registry_gap_closure_final_review_v0_1.py"
ADOPTION_LINKS = CAPABILITIES / "primary_source_adoption_evidence_gate_links.json"
ADOPTION_GATE = CAPABILITIES / "primary_source_adoption_evidence_gate_links_gate.json"
ADOPTION_NEXT_ACTION = CAPABILITIES / "primary_source_adoption_evidence_gate_links_next_action.yml"
FINAL_REVIEW = CAPABILITIES / "primary_source_registry_gap_closure_final_review.json"
FINAL_GATE = CAPABILITIES / "primary_source_registry_gap_closure_final_review_gate.json"
FINAL_REPORT = CAPABILITIES / "primary_source_registry_gap_closure_final_review_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_registry_gap_closure_final_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_registry_gap_closure_final_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_REGISTRY_GAP_CLOSURE_FINAL_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_registry_gap_closure_final_review_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_adoption_evidence_gate_links_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_adoption_decision_matrix_v0_1"
FINAL_DECISION = "PRIMARY_SOURCE_REGISTRY_GAP_CLOSURE_REVIEWED_REPO_LOCAL"
FINAL_STATUS = "all_known_registry_gaps_closed_or_bounded"

GAP_IDS = [
    "gap-product-quality-reports-missing-primary-source-inputs",
    "gap-avf-ledger-to-manual-record-namespace-map",
    "gap-content-safety-policy-sources-missing-manual-records",
    "gap-adoption-evidence-gates-not-yet-linked-to-registry",
]

EXPECTED_COUNTS = {
    "original_gap_count": 4,
    "closed_or_bounded_gap_count": 4,
    "remaining_gap_count": 0,
    "closure_artifact_count": 7,
}

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
    "runtime_export_performed",
    "collector_started",
    "telemetry_export_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    ADOPTION_LINKS,
    ADOPTION_GATE,
    ADOPTION_NEXT_ACTION,
    FINAL_REVIEW,
    FINAL_GATE,
    FINAL_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_registry_gap_closure_final_review_v0_1=true",
    f"final_decision={FINAL_DECISION}",
    f"final_status={FINAL_STATUS}",
    "original_gap_count=4",
    "closed_or_bounded_gap_count=4",
    "remaining_gap_count=0",
    "closure_artifact_count=7",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "all_known_registry_gaps_closed_or_bounded=true",
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
    "runtime_export_performed=false",
    "collector_started=false",
    "telemetry_export_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-adoption-decision-matrix",
    "owner_approval_required_before_execution: false",
    "Create a repo-local capability adoption decision matrix using the closed registry gap chain",
    "Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Primary-Source Registry Gap Closure Final Review v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_previous_adoption_links() -> None:
    for label, record in [("adoption links", read_json(ADOPTION_LINKS)), ("adoption gate", read_json(ADOPTION_GATE))]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            fail(f"{label} goal_id mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            fail(f"{label} must point to this final review goal")
        if record.get("remaining_gap_count") != 0:
            fail(f"{label} remaining gap count mismatch")
        if record.get("dependency_adoption_allowed") is not False:
            fail(f"{label} dependency adoption must remain blocked")
        if record.get("runtime_integration_allowed") is not False:
            fail(f"{label} runtime integration must remain blocked")
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    require_text_markers(
        ADOPTION_NEXT_ACTION,
        [
            "action_id: review-primary-source-registry-gap-closure",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )


def require_final_record(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "final_decision": FINAL_DECISION,
        "final_status": FINAL_STATUS,
        "all_known_registry_gaps_closed_or_bounded": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("gap_ids") != GAP_IDS:
        fail(f"{label} gap ids mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate() -> None:
    gate = read_json(FINAL_GATE)
    if gate.get("gate_id") != "avf-primary-source-registry-gap-closure-final-review-gate-v0-1":
        fail("final review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("final review gate status must be PASS")
    require_final_record(gate, "final review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_registry_gap_closure_final_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_final_record(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_adoption_links()
    require_final_record(read_json(FINAL_REVIEW), "final review")
    require_gate()
    require_text_markers(FINAL_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Registry Gap Closure Final Review v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_registry_gap_closure_final_review_v0_1=true")
    print(f"final_decision={FINAL_DECISION}")
    print(f"final_status={FINAL_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("all_known_registry_gaps_closed_or_bounded=true")
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
    print("runtime_export_performed=false")
    print("collector_started=false")
    print("telemetry_export_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

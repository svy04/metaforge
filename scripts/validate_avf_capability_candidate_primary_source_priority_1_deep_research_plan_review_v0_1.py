from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1.py"
RESEARCH_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan.json"
SOURCE_TARGETS = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_source_targets.json"
PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_gate.json"
PLAN_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_DEEP_RESEARCH_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_DEEP_RESEARCH_PLAN_REVIEWED"
REVIEW_STATUS = "deep_research_plan_validated_ready_for_source_evidence_capture_plan"
PLAN_STATUS = "priority_1_deep_research_plan_created_non_executable"
PLAN_SCOPE = "primary_source_deep_research_plan_only"

EXPECTED_COUNTS = {
    "source_target_count": 7,
    "reviewed_source_target_count": 7,
    "official_docs_target_count": 2,
    "original_repository_target_count": 2,
    "paper_target_count": 1,
    "standard_target_count": 2,
    "maintained_source_code_target_count": 2,
    "selection_allowed_count": 0,
    "dependency_adoption_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "external_fetch_performed_count": 0,
    "review_blocker_count": 0,
    "ready_for_source_evidence_capture_plan_count": 1,
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

REQUIRED_TARGET_IDS = {
    "src-promptfoo-official-docs",
    "src-promptfoo-original-repository",
    "src-ragas-official-docs",
    "src-ragas-original-repository",
    "src-ragas-arxiv-paper",
    "src-owasp-genai-llm-top-10",
    "src-nist-ai-rmf",
}

REQUIRED_FILES = [
    RUNNER,
    RESEARCH_PLAN,
    SOURCE_TARGETS,
    PLAN_GATE,
    PLAN_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "plan_scope_confirmed=primary_source_deep_research_plan_only",
    "deep_research_plan_not_source_fetch_gate=true",
    "source_target_count=7",
    "reviewed_source_target_count=7",
    "ready_for_source_evidence_capture_plan_count=1",
    "selection_allowed=false",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-priority-1-source-evidence-capture-plan",
    "owner_approval_required_before_execution: false",
    "Create a repo-local source evidence capture plan",
    "Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Deep Research Plan Review v0.1 validation")
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


def require_source_target(target: dict, label: str) -> None:
    target_id = target.get("source_target_id", "<missing>")
    if target_id not in REQUIRED_TARGET_IDS:
        fail(f"{label} unexpected target {target_id}")
    if target.get("candidate_id") != CANDIDATE_ID:
        fail(f"{label} {target_id} candidate mismatch")
    if target.get("research_status") != "target_identified_not_fetched_by_runner":
        fail(f"{label} {target_id} research status mismatch")
    if not target.get("inspection_focus"):
        fail(f"{label} {target_id} inspection focus required")
    if target.get("selection_allowed") is not False:
        fail(f"{label} {target_id} selection must be blocked")
    if target.get("dependency_adoption_allowed") is not False:
        fail(f"{label} {target_id} dependency adoption must be blocked")
    if target.get("runtime_integration_allowed") is not False:
        fail(f"{label} {target_id} runtime integration must be blocked")
    if target.get("external_fetch_performed") is not False:
        fail(f"{label} {target_id} external fetch must remain blocked")


def require_previous_inputs() -> dict:
    plan = read_json(RESEARCH_PLAN)
    targets = read_json(SOURCE_TARGETS)
    gate = read_json(PLAN_GATE)
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("deep research plan goal_id mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("deep research plan must point to this review goal")
    if gate.get("status") != "PASS":
        fail("deep research plan gate status must be PASS")
    for record, label in [(plan, "deep research plan"), (gate, "deep research plan gate")]:
        if record.get("candidate_id") != CANDIDATE_ID:
            fail(f"{label} candidate mismatch")
        if record.get("plan_status") != PLAN_STATUS:
            fail(f"{label} status mismatch")
        if record.get("plan_scope") != PLAN_SCOPE:
            fail(f"{label} scope mismatch")
        for key in [
            "source_target_count",
            "official_docs_target_count",
            "original_repository_target_count",
            "paper_target_count",
            "standard_target_count",
            "maintained_source_code_target_count",
            "selection_allowed_count",
            "dependency_adoption_allowed_count",
            "runtime_integration_allowed_count",
            "external_fetch_performed_count",
        ]:
            if record.get(key) != EXPECTED_COUNTS[key]:
                fail(f"{label} {key} mismatch")
        if record.get("selection_allowed") is not False:
            fail(f"{label} selection must be blocked")
        if record.get("dependency_adoption_allowed") is not False:
            fail(f"{label} dependency adoption must be blocked")
        if record.get("runtime_integration_allowed") is not False:
            fail(f"{label} runtime integration must be blocked")
        if record.get("external_fetch_performed") is not False:
            fail(f"{label} external fetch must be false")
        for target in record.get("source_targets", []):
            require_source_target(target, label)
        require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")
    if targets.get("candidate_id") != CANDIDATE_ID:
        fail("source targets candidate mismatch")
    target_ids = {target.get("source_target_id") for target in targets.get("source_targets", [])}
    if target_ids != REQUIRED_TARGET_IDS:
        fail("source targets id set mismatch")
    require_text_markers(
        PLAN_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-priority-1-deep-research-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return plan


def require_reviewed_target(target: dict, source_by_id: dict[str, dict], label: str) -> None:
    target_id = target.get("source_target_id", "<missing>")
    if target_id not in source_by_id:
        fail(f"{label} unexpected reviewed target {target_id}")
    source = source_by_id[target_id]
    for key in [
        "candidate_id",
        "source_kind",
        "source_uri",
        "inspection_focus",
        "maintained_source_code_target",
    ]:
        if target.get(key) != source.get(key):
            fail(f"{label} {target_id} {key} mismatch")
    if target.get("review_status") != "reviewed_source_target_validated":
        fail(f"{label} {target_id} review status mismatch")
    if target.get("capture_plan_required") is not True:
        fail(f"{label} {target_id} capture plan required flag mismatch")
    if target.get("selection_allowed") is not False:
        fail(f"{label} {target_id} selection must be blocked")
    if target.get("dependency_adoption_allowed") is not False:
        fail(f"{label} {target_id} dependency adoption must be blocked")
    if target.get("runtime_integration_allowed") is not False:
        fail(f"{label} {target_id} runtime integration must be blocked")
    if target.get("external_fetch_performed") is not False:
        fail(f"{label} {target_id} external fetch must be false")


def require_review_record(record: dict, label: str, plan: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "plan_scope_confirmed": PLAN_SCOPE,
        "deep_research_plan_not_source_fetch_gate": True,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "external_fetch_performed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    reviewed = record.get("reviewed_source_targets", [])
    if len(reviewed) != EXPECTED_COUNTS["reviewed_source_target_count"]:
        fail(f"{label} reviewed source target count mismatch")
    source_by_id = {target["source_target_id"]: target for target in plan.get("source_targets", [])}
    for target in reviewed:
        require_reviewed_target(target, source_by_id, label)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_review_gate(plan: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-deep-research-plan-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", plan)


def require_validation_result(plan: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", plan)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    plan = require_previous_inputs()
    require_review_gate(plan)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(plan)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Deep Research Plan Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("deep_research_plan_not_source_fetch_gate=true")
    print("selection_allowed=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

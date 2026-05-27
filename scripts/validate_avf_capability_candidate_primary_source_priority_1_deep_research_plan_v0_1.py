from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_deep_research_plan_v0_1.py"
PRIORITY_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_gate.json"
PRIORITY_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_next_action.yml"
RESEARCH_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan.json"
SOURCE_TARGETS = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_source_targets.json"
PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_gate.json"
PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_DEEP_RESEARCH_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PLAN_STATUS = "priority_1_deep_research_plan_created_non_executable"
PLAN_SCOPE = "primary_source_deep_research_plan_only"

EXPECTED_COUNTS = {
    "source_target_count": 7,
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
    "ready_for_deep_research_plan_review_count": 1,
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

REQUIRED_SOURCE_TARGETS = {
    "src-promptfoo-official-docs": ("official_docs", "https://www.promptfoo.dev/docs/intro/"),
    "src-promptfoo-original-repository": ("original_repository", "https://github.com/promptfoo/promptfoo"),
    "src-ragas-official-docs": ("official_docs", "https://docs.ragas.io/en/stable/"),
    "src-ragas-original-repository": ("original_repository", "https://github.com/vibrantlabsai/ragas"),
    "src-ragas-arxiv-paper": ("paper", "https://arxiv.org/abs/2309.15217"),
    "src-owasp-genai-llm-top-10": ("standard", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"),
    "src-nist-ai-rmf": ("standard", "https://doi.org/10.6028/NIST.AI.100-1"),
}

REQUIRED_FILES = [
    RUNNER,
    PRIORITY_REVIEW_GATE,
    PRIORITY_REVIEW_NEXT_ACTION,
    RESEARCH_PLAN,
    SOURCE_TARGETS,
    PLAN_GATE,
    PLAN_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_deep_research_plan_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"plan_status={PLAN_STATUS}",
    f"plan_scope={PLAN_SCOPE}",
    "source_target_count=7",
    "official_docs_target_count=2",
    "original_repository_target_count=2",
    "paper_target_count=1",
    "standard_target_count=2",
    "maintained_source_code_target_count=2",
    "source_target_id=src-promptfoo-official-docs",
    "source_target_id=src-promptfoo-original-repository",
    "source_target_id=src-ragas-official-docs",
    "source_target_id=src-ragas-original-repository",
    "source_target_id=src-ragas-arxiv-paper",
    "source_target_id=src-owasp-genai-llm-top-10",
    "source_target_id=src-nist-ai-rmf",
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
    "action_id: review-capability-candidate-primary-source-priority-1-deep-research-plan",
    "owner_approval_required_before_execution: false",
    "Review the repo-local deep research plan",
    "Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Deep Research Plan v0.1 validation")
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


def require_previous_input() -> dict:
    review = read_json(PRIORITY_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("priority matrix review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("priority matrix review gate must point to this deep research plan goal")
    if review.get("priority_1_candidate_ids") != [CANDIDATE_ID]:
        fail("priority matrix review must identify the expected priority 1 candidate")
    if review.get("ready_for_priority_1_deep_research_plan_count") != 1:
        fail("priority matrix review must be ready for deep research plan")
    if review.get("priority_matrix_not_selection_gate") is not True:
        fail("priority matrix review must confirm non-selection boundary")
    if review.get("selection_allowed") is not False:
        fail("selection must remain blocked")
    if review.get("dependency_adoption_allowed") is not False:
        fail("dependency adoption must remain blocked")
    if review.get("runtime_integration_allowed") is not False:
        fail("runtime integration must remain blocked")
    require_false_flags(review.get("claim_boundary", {}), "priority matrix review claim boundary")
    require_text_markers(
        PRIORITY_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-deep-research-plan",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_source_target(target: dict, label: str) -> None:
    target_id = target.get("source_target_id", "<missing>")
    if target_id not in REQUIRED_SOURCE_TARGETS:
        fail(f"{label} unexpected source target {target_id}")
    expected_kind, expected_uri = REQUIRED_SOURCE_TARGETS[target_id]
    if target.get("source_kind") != expected_kind:
        fail(f"{label} {target_id} source kind mismatch")
    if target.get("source_uri") != expected_uri:
        fail(f"{label} {target_id} source uri mismatch")
    if target.get("candidate_id") != CANDIDATE_ID:
        fail(f"{label} {target_id} candidate mismatch")
    if not target.get("inspection_focus"):
        fail(f"{label} {target_id} inspection focus required")
    if target.get("research_status") != "target_identified_not_fetched_by_runner":
        fail(f"{label} {target_id} research status mismatch")
    if target.get("selection_allowed") is not False:
        fail(f"{label} {target_id} selection must be blocked")
    if target.get("dependency_adoption_allowed") is not False:
        fail(f"{label} {target_id} dependency adoption must be blocked")
    if target.get("runtime_integration_allowed") is not False:
        fail(f"{label} {target_id} runtime integration must be blocked")
    if target.get("external_fetch_performed") is not False:
        fail(f"{label} {target_id} external fetch must be false")


def require_source_targets_record(record: dict, label: str) -> None:
    if record.get("candidate_id") != CANDIDATE_ID:
        fail(f"{label} candidate mismatch")
    if record.get("source_target_count") != EXPECTED_COUNTS["source_target_count"]:
        fail(f"{label} source target count mismatch")
    targets = record.get("source_targets", [])
    if len(targets) != EXPECTED_COUNTS["source_target_count"]:
        fail(f"{label} source target list count mismatch")
    seen = set()
    for target in targets:
        require_source_target(target, label)
        seen.add(target["source_target_id"])
    if seen != set(REQUIRED_SOURCE_TARGETS):
        fail(f"{label} source target id set mismatch")


def require_plan_record(record: dict, label: str) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "plan_status": PLAN_STATUS,
        "plan_scope": PLAN_SCOPE,
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
    require_source_targets_record(record, label)
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate() -> None:
    gate = read_json(PLAN_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-deep-research-plan-gate-v0-1":
        fail("plan gate id mismatch")
    if gate.get("status") != "PASS":
        fail("plan gate status must be PASS")
    require_plan_record(gate, "plan gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_deep_research_plan_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_plan_record(result, "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_previous_input()
    plan = read_json(RESEARCH_PLAN)
    require_plan_record(plan, "research plan")
    source_targets = read_json(SOURCE_TARGETS)
    require_source_targets_record(source_targets, "source targets")
    require_gate()
    require_text_markers(PLAN_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Deep Research Plan v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_deep_research_plan_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"plan_status={PLAN_STATUS}")
    print(f"plan_scope={PLAN_SCOPE}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
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

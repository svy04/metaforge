from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
EXECUTION = (
    ROOT
    / "avf"
    / "influence_factory"
    / "operator_package_v14"
    / "real_goal_run_v15"
    / "owner_review_v16"
    / "local_iteration_v17"
    / "executed_iteration_v18"
)
REVIEW = EXECUTION / "owner_review_v19"
RECORD = REVIEW / "owner_review_continuation_v19_record.json"

REQUIRED_FILES = [
    EXECUTION / "local_iteration_execution_v18_record.json",
    EXECUTION / "TASK_EXECUTION_RESULTS.json",
    EXECUTION / "PROTECTED_ACTION_AUTHORIZATION_CHECKLIST.md",
    RECORD,
    REVIEW / "OWNER_REVIEW_V19_RESULT.json",
    REVIEW / "OWNER_REVIEW_V19_RESULT.md",
    REVIEW / "LOCAL_CONTINUATION_DECISION.md",
    REVIEW / "NEXT_LOCAL_ITERATION_PLAN.md",
    REVIEW / "PROTECTED_BOUNDARY_RECONFIRMATION.md",
    REVIEW / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v19_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v19.png",
    APP / "self_test_report_v19.md",
    ROOT / "scripts" / "create_avf_influence_factory_owner_review_continuation_v19.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_REVIEW_CONTINUATION_V19_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_REVIEW_CONTINUATION_V19.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v19",
    "Owner Review Continuation",
    "Local Continuation Decision",
    "Next Local Iteration Plan",
    "Protected Boundary Reconfirmation",
    "Build Owner Review Continuation",
    "buildOwnerReviewContinuation",
    "renderOwnerReviewContinuation",
    "SELF_TEST_PASS_V19",
]

FALSE_FLAGS = [
    "protected_action_executed",
    "external_calls",
    "provider_calls_performed",
    "live_model_calls_performed",
    "dependency_install_performed",
    "deploy_performed",
    "publish_performed",
    "platform_posting_performed",
    "personal_account_automation_performed",
    "release_readiness_claimed",
    "public_readiness_claimed",
    "production_readiness_claimed",
    "external_validation_claimed",
    "autonomous_reliability_claimed",
]

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory owner review continuation v19 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "OWNER_REVIEW_CONTINUATION_V19_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("selected_next_safe_goal") != "build_local_operating_loop_templates_v20_without_protected_actions":
        fail(f"{label} selected_next_safe_goal mismatch")
    if data.get("next_safe_goal_count") != 1:
        fail(f"{label} next_safe_goal_count must be 1")
    for flag in FALSE_FLAGS:
        if data.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    v18 = read_json(EXECUTION / "local_iteration_execution_v18_record.json")
    if v18.get("terminal_condition") != "LOCAL_ITERATION_EXECUTION_V18_READY":
        fail("v18 local iteration execution is not ready")

    validate_record(read_json(RECORD), "review record")
    validate_record(read_json(APP / "product_workbench_v19_record.json"), "app record")

    result = read_json(REVIEW / "OWNER_REVIEW_V19_RESULT.json")
    if result.get("decision") != "continue_local_iteration":
        fail("v19 decision must continue local iteration")
    if result.get("protected_action_authorized") is not False:
        fail("v19 must not authorize protected action")
    if len(result.get("reviewed_artifacts", [])) < 4:
        fail("v19 must review v18 core artifacts")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v19.png").stat().st_size < 10000:
        fail("render-check-v19.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v19.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V19",
        "Owner review continuation ready",
        "Local continuation decision ready",
        "Protected boundary reconfirmed",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v19.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: build_local_operating_loop_templates_v20_without_protected_actions",
        "selected_next_goal_executed: false",
        "protected_action_authorized: false",
        "fake human impersonation",
        "undisclosed bot networks",
        "platform posting",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory owner review continuation v19 validation")
    print("RESULT: PASS")
    print("terminal_condition=OWNER_REVIEW_CONTINUATION_V19_READY")
    print("selected_next_safe_goal=build_local_operating_loop_templates_v20_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

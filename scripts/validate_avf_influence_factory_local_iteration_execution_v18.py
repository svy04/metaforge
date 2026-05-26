from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
REVIEW = ROOT / "avf" / "influence_factory" / "operator_package_v14" / "real_goal_run_v15" / "owner_review_v16"
ITERATION = REVIEW / "local_iteration_v17"
EXECUTION = ITERATION / "executed_iteration_v18"
RECORD = EXECUTION / "local_iteration_execution_v18_record.json"

REQUIRED_FILES = [
    ITERATION / "local_iteration_v17_record.json",
    ITERATION / "CODEX_TASK_QUEUE.json",
    ITERATION / "ACCEPTANCE_MATRIX.md",
    ITERATION / "IMPLEMENTATION_ORDER.md",
    RECORD,
    EXECUTION / "LOCAL_ITERATION_EXECUTION_SUMMARY.json",
    EXECUTION / "LOCAL_ITERATION_EXECUTION_SUMMARY.md",
    EXECUTION / "TASK_EXECUTION_RESULTS.json",
    EXECUTION / "TASK_EXECUTION_RESULTS.md",
    EXECUTION / "OWNER_REVIEW_VERDICT_GUIDE.md",
    EXECUTION / "STYLE_CONTINUITY_EXAMPLES.md",
    EXECUTION / "V15_ACCEPTANCE_COMPARISON.md",
    EXECUTION / "PROTECTED_ACTION_AUTHORIZATION_CHECKLIST.md",
    EXECUTION / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v18_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "styles.css",
    APP / "render-check-v18.png",
    APP / "self_test_report_v18.md",
    ROOT / "scripts" / "create_avf_influence_factory_local_iteration_execution_v18.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_ITERATION_EXECUTION_V18_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_ITERATION_EXECUTION_V18.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v18",
    "Local Iteration Executor",
    "Task Execution Results",
    "Owner Verdict Clarity",
    "Style Example Pack",
    "V15 Evidence Compare",
    "Protected Authorization Checklist",
    "Execute Local Iteration Tasks",
    "executeLocalIterationTasks",
    "renderLocalIterationExecution",
    "SELF_TEST_PASS_V18",
]

REQUIRED_TASKS = [
    "v17-owner-review-ux",
    "v17-style-examples",
    "v17-evidence-compare",
    "v17-authorization-checklist",
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
    print("Influence Factory local iteration execution v18 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "LOCAL_ITERATION_EXECUTION_V18_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("selected_next_safe_goal") != "owner_reviews_v18_iteration_results_or_continues_local_iteration":
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

    v17 = read_json(ITERATION / "local_iteration_v17_record.json")
    if v17.get("terminal_condition") != "LOCAL_ITERATION_QUEUE_V17_READY":
        fail("v17 local iteration queue is not ready")

    validate_record(read_json(RECORD), "execution record")
    validate_record(read_json(APP / "product_workbench_v18_record.json"), "app record")

    results = read_json(EXECUTION / "TASK_EXECUTION_RESULTS.json")
    tasks = results.get("tasks", [])
    if [task.get("task_id") for task in tasks] != REQUIRED_TASKS:
        fail("TASK_EXECUTION_RESULTS task order mismatch")
    for task in tasks:
        if task.get("status") != "implemented_local_only":
            fail(f"task not implemented local-only: {task.get('task_id')}")
        if task.get("protected_action_required") is not False:
            fail(f"task requires protected action: {task.get('task_id')}")
        if not task.get("evidence"):
            fail(f"task missing evidence: {task.get('task_id')}")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    screenshot_size = (APP / "render-check-v18.png").stat().st_size
    if screenshot_size < 10000:
        fail("render-check-v18.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v18.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V18",
        "Task execution results ready",
        "Owner verdict clarity ready",
        "Protected authorization checklist ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v18.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: owner_reviews_v18_iteration_results_or_continues_local_iteration",
        "selected_next_goal_executed: false",
        "fake human impersonation",
        "undisclosed bot networks",
        "platform posting",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory local iteration execution v18 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_ITERATION_EXECUTION_V18_READY")
    print("selected_next_safe_goal=owner_reviews_v18_iteration_results_or_continues_local_iteration")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

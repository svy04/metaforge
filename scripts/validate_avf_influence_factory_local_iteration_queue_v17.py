from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
REVIEW = ROOT / "avf" / "influence_factory" / "operator_package_v14" / "real_goal_run_v15" / "owner_review_v16"
ITERATION = REVIEW / "local_iteration_v17"
RECORD = ITERATION / "local_iteration_v17_record.json"

REQUIRED_FILES = [
    REVIEW / "owner_review_v16_record.json",
    REVIEW / "LOCAL_ITERATION_BACKLOG.json",
    RECORD,
    ITERATION / "LOCAL_ITERATION_PLAN.json",
    ITERATION / "LOCAL_ITERATION_PLAN.md",
    ITERATION / "CODEX_TASK_QUEUE.json",
    ITERATION / "CODEX_TASK_QUEUE.md",
    ITERATION / "ACCEPTANCE_MATRIX.md",
    ITERATION / "IMPLEMENTATION_ORDER.md",
    ITERATION / "NEXT_SAFE_GOAL.md",
    ITERATION / "codex_tasks" / "v17-owner-review-ux.json",
    ITERATION / "codex_tasks" / "v17-style-examples.json",
    ITERATION / "codex_tasks" / "v17-evidence-compare.json",
    ITERATION / "codex_tasks" / "v17-authorization-checklist.json",
    APP / "product_workbench_v17_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "styles.css",
    APP / "render-check-v17.png",
    APP / "self_test_report_v17.md",
    ROOT / "scripts" / "create_avf_influence_factory_local_iteration_queue_v17.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_ITERATION_QUEUE_V17_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_ITERATION_QUEUE_V17.md",
]

REQUIRED_APP_MARKERS = [
    "Local Iteration Runner",
    "Codex Task Queue",
    "Acceptance Matrix",
    "Implementation Order",
    "Build Local Iteration Queue",
    "buildLocalIterationQueue",
    "renderLocalIterationQueue",
    "SELF_TEST_PASS_V17",
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
    print("Influence Factory local iteration queue v17 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "LOCAL_ITERATION_QUEUE_V17_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("selected_next_safe_goal") != "execute_v17_local_iteration_tasks_without_protected_actions":
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

    v16 = read_json(REVIEW / "owner_review_v16_record.json")
    if v16.get("terminal_condition") != "OWNER_REVIEW_CONSOLE_V16_READY":
        fail("v16 owner review console is not ready")

    validate_record(read_json(RECORD), "iteration record")
    validate_record(read_json(APP / "product_workbench_v17_record.json"), "app record")

    queue = read_json(ITERATION / "CODEX_TASK_QUEUE.json")
    tasks = queue.get("tasks", [])
    if len(tasks) != 4:
        fail("CODEX_TASK_QUEUE must contain exactly 4 tasks")
    for task in tasks:
        if task.get("protected_action_required") is not False:
            fail(f"task requires protected action: {task.get('task_id')}")
        if not task.get("acceptance_criteria"):
            fail(f"task missing acceptance criteria: {task.get('task_id')}")
        if not task.get("forbidden_changes"):
            fail(f"task missing forbidden changes: {task.get('task_id')}")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    screenshot_size = (APP / "render-check-v17.png").stat().st_size
    if screenshot_size < 10000:
        fail("render-check-v17.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v17.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V17",
        "Local iteration queue built",
        "Codex task queue ready",
        "Acceptance matrix ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v17.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: execute_v17_local_iteration_tasks_without_protected_actions",
        "selected_next_goal_executed: false",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory local iteration queue v17 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_ITERATION_QUEUE_V17_READY")
    print("selected_next_safe_goal=execute_v17_local_iteration_tasks_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

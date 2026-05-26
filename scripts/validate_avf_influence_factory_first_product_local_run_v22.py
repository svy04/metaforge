from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V21 = (
    ROOT
    / "avf"
    / "influence_factory"
    / "operator_package_v14"
    / "real_goal_run_v15"
    / "owner_review_v16"
    / "local_iteration_v17"
    / "executed_iteration_v18"
    / "owner_review_v19"
    / "local_operating_loop_templates_v20"
    / "first_product_goal_runner_v21"
)
V22 = V21 / "first_product_local_run_v22"
RECORD = V22 / "first_product_local_run_v22_record.json"

REQUIRED_FILES = [
    V21 / "first_product_goal_runner_v21_record.json",
    V21 / "FIRST_PRODUCT_GOAL_RUN_PACKET.json",
    RECORD,
    V22 / "FIRST_PRODUCT_LOCAL_RUN_SUMMARY.json",
    V22 / "FIRST_PRODUCT_LOCAL_RUN_SUMMARY.md",
    V22 / "MVP_EXECUTION_BOARD.json",
    V22 / "MVP_EXECUTION_BOARD.md",
    V22 / "FIRST_PRODUCT_MVP_SPEC.md",
    V22 / "FIRST_PRODUCT_CONTENT_CALENDAR.md",
    V22 / "FIRST_PRODUCT_STYLE_PROMPT_PACK.md",
    V22 / "FIRST_PRODUCT_CODEX_PR_SEQUENCE.json",
    V22 / "FIRST_PRODUCT_CODEX_PR_SEQUENCE.md",
    V22 / "FIRST_PRODUCT_OWNER_ACCEPTANCE_CHECKLIST.md",
    V22 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v22_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v22.png",
    APP / "self_test_report_v22.md",
    ROOT / "scripts" / "create_avf_influence_factory_first_product_local_run_v22.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_FIRST_PRODUCT_LOCAL_RUN_V22_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_FIRST_PRODUCT_LOCAL_RUN_V22.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v22",
    "First Product Local Run",
    "MVP Execution Board",
    "First Product MVP Spec",
    "First Product Codex PR Sequence",
    "Owner Acceptance Checklist",
    "Run First Product Local Cycle",
    "runFirstProductLocalCycle",
    "renderFirstProductLocalRun",
    "SELF_TEST_PASS_V22",
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
    print("Influence Factory first product local run v22 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "FIRST_PRODUCT_LOCAL_RUN_V22_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("selected_next_safe_goal") != "implement_first_product_local_mvp_work_items_v23_without_protected_actions":
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

    v21 = read_json(V21 / "first_product_goal_runner_v21_record.json")
    if v21.get("terminal_condition") != "FIRST_PRODUCT_GOAL_RUNNER_V21_READY":
        fail("v21 first product goal runner is not ready")

    validate_record(read_json(RECORD), "v22 record")
    validate_record(read_json(APP / "product_workbench_v22_record.json"), "app record")

    board = read_json(V22 / "MVP_EXECUTION_BOARD.json")
    work_items = board.get("work_items", [])
    if len(work_items) < 6:
        fail("MVP execution board must contain at least six work items")
    if any(item.get("protected_action_required") is not False for item in work_items):
        fail("MVP execution board contains protected-action work item")

    sequence = read_json(V22 / "FIRST_PRODUCT_CODEX_PR_SEQUENCE.json")
    prs = sequence.get("pr_sequence", [])
    if len(prs) < 4:
        fail("Codex PR sequence must include at least four PR-sized steps")
    if any(pr.get("protected_action_required") is not False for pr in prs):
        fail("Codex PR sequence contains protected-action PR")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v22.png").stat().st_size < 10000:
        fail("render-check-v22.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v22.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V22",
        "MVP execution board ready",
        "Codex PR sequence ready",
        "Owner acceptance checklist ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v22.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: implement_first_product_local_mvp_work_items_v23_without_protected_actions",
        "selected_next_goal_executed: false",
        "fake human impersonation",
        "undisclosed bot networks",
        "platform posting",
        "FIRST_PRODUCT_LOCAL_RUN_V22_READY",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory first product local run v22 validation")
    print("RESULT: PASS")
    print("terminal_condition=FIRST_PRODUCT_LOCAL_RUN_V22_READY")
    print("selected_next_safe_goal=implement_first_product_local_mvp_work_items_v23_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

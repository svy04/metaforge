from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V22 = (
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
    / "first_product_local_run_v22"
)
V23 = V22 / "mvp_work_items_v23"
RECORD = V23 / "mvp_work_items_v23_record.json"

REQUIRED_FILES = [
    V22 / "first_product_local_run_v22_record.json",
    V22 / "MVP_EXECUTION_BOARD.json",
    V22 / "FIRST_PRODUCT_CODEX_PR_SEQUENCE.json",
    RECORD,
    V23 / "IMPLEMENTED_MVP_WORK_ITEMS.json",
    V23 / "IMPLEMENTED_MVP_WORK_ITEMS.md",
    V23 / "LOCAL_MVP_FEATURE_STATE.json",
    V23 / "FIRST_PRODUCT_LOCAL_RUNBOOK.md",
    V23 / "LOCAL_MVP_ACCEPTANCE_REPORT.md",
    V23 / "STYLE_AND_CONTENT_IMPLEMENTATION_NOTES.md",
    V23 / "CODEX_PR_IMPLEMENTATION_PACKETS.json",
    V23 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v23_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v23.png",
    APP / "self_test_report_v23.md",
    ROOT / "scripts" / "create_avf_influence_factory_mvp_work_items_v23.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_MVP_WORK_ITEMS_V23_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_MVP_WORK_ITEMS_V23.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v23",
    "MVP Work Item Executor",
    "Implemented MVP Work Items",
    "Local MVP Feature State",
    "First Product Local Runbook",
    "Run MVP Work Items",
    "runMvpWorkItems",
    "renderMvpWorkItems",
    "SELF_TEST_PASS_V23",
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
    print("Influence Factory MVP work items v23 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "LOCAL_MVP_WORK_ITEMS_V23_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("selected_next_safe_goal") != "run_local_mvp_end_to_end_acceptance_v24_without_protected_actions":
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

    v22 = read_json(V22 / "first_product_local_run_v22_record.json")
    if v22.get("terminal_condition") != "FIRST_PRODUCT_LOCAL_RUN_V22_READY":
        fail("v22 first product local run is not ready")

    validate_record(read_json(RECORD), "v23 record")
    validate_record(read_json(APP / "product_workbench_v23_record.json"), "app record")

    implemented = read_json(V23 / "IMPLEMENTED_MVP_WORK_ITEMS.json")
    items = implemented.get("implemented_work_items", [])
    if len(items) < 6:
        fail("implemented MVP work items must contain at least six items")
    if any(item.get("status") != "implemented_local_only" for item in items):
        fail("all MVP work items must be implemented_local_only")
    if any(item.get("protected_action_required") is not False for item in items):
        fail("implemented MVP work items contain protected action")

    feature_state = read_json(V23 / "LOCAL_MVP_FEATURE_STATE.json")
    required_features = [
        "goal_intake",
        "strategy_proof",
        "style_prompt_pack",
        "content_calendar",
        "codex_pr_sequence",
        "owner_acceptance",
    ]
    for feature in required_features:
        if feature_state.get("features", {}).get(feature) != "implemented_local_only":
            fail(f"feature state missing implemented local feature: {feature}")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v23.png").stat().st_size < 10000:
        fail("render-check-v23.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v23.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V23",
        "MVP work items implemented",
        "Local MVP feature state ready",
        "Local runbook ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v23.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: run_local_mvp_end_to_end_acceptance_v24_without_protected_actions",
        "selected_next_goal_executed: false",
        "fake human impersonation",
        "undisclosed bot networks",
        "platform posting",
        "LOCAL_MVP_WORK_ITEMS_V23_READY",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory MVP work items v23 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_MVP_WORK_ITEMS_V23_READY")
    print("selected_next_safe_goal=run_local_mvp_end_to_end_acceptance_v24_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

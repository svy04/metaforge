from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
RUN = ROOT / "avf" / "influence_factory" / "operator_package_v14" / "real_goal_run_v15"
REVIEW = RUN / "owner_review_v16"
RECORD = REVIEW / "owner_review_v16_record.json"

REQUIRED_FILES = [
    RUN / "real_goal_run_v15_record.json",
    RECORD,
    REVIEW / "OWNER_REVIEW_CONSOLE.md",
    REVIEW / "OWNER_DECISION_MATRIX.md",
    REVIEW / "LOCAL_ITERATION_BACKLOG.json",
    REVIEW / "LOCAL_ITERATION_BACKLOG.md",
    REVIEW / "PROTECTED_ACTION_DECISION_PACKET.md",
    REVIEW / "FINAL_BOUNDARY_STATUS.md",
    REVIEW / "OWNER_REVIEW_SUMMARY.json",
    APP / "product_workbench_v16_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "styles.css",
    APP / "render-check-v16.png",
    APP / "self_test_report_v16.md",
    ROOT / "scripts" / "create_avf_influence_factory_owner_review_console_v16.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_REVIEW_CONSOLE_V16_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_REVIEW_CONSOLE_V16.md",
]

REQUIRED_APP_MARKERS = [
    "Owner Review Console",
    "Review V15 Run",
    "Decision Matrix",
    "Local Iteration Backlog",
    "Protected Action Decision Packet",
    "Build Owner Review Packet",
    "buildOwnerReviewPacket",
    "renderOwnerReviewConsole",
    "SELF_TEST_PASS_V16",
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

FORBIDDEN_APP_MARKERS = [
    "fetch(",
    "XMLHttpRequest",
    "navigator.sendBeacon",
    "http://",
    "https://",
    "import(",
]


def fail(message: str) -> None:
    print("Influence Factory owner review console v16 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "OWNER_REVIEW_CONSOLE_V16_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("selected_next_safe_goal") != "owner_selects_local_iteration_or_explicit_protected_action_authorization":
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

    v15 = read_json(RUN / "real_goal_run_v15_record.json")
    if v15.get("terminal_condition") != "REAL_GOAL_OPERATOR_RUN_V15_READY":
        fail("v15 real-goal run is not ready")

    validate_record(read_json(RECORD), "owner review record")
    validate_record(read_json(APP / "product_workbench_v16_record.json"), "app record")

    backlog = read_json(REVIEW / "LOCAL_ITERATION_BACKLOG.json")
    items = backlog.get("items", [])
    if len(items) < 4:
        fail("local iteration backlog must contain at least 4 items")
    for item in items:
        if item.get("protected_action_required") is not False:
            fail(f"backlog item must be local-only: {item.get('item_id')}")

    summary = read_json(REVIEW / "OWNER_REVIEW_SUMMARY.json")
    if summary.get("default_decision") != "continue_local_iteration":
        fail("default decision must continue local iteration")
    if summary.get("protected_action_executed") is not False:
        fail("summary protected_action_executed must be false")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    screenshot_size = (APP / "render-check-v16.png").stat().st_size
    if screenshot_size < 10000:
        fail("render-check-v16.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v16.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V16",
        "Owner review packet built",
        "Decision matrix ready",
        "Protected action decision packet ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v16.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: owner_selects_local_iteration_or_explicit_protected_action_authorization",
        "selected_next_goal_executed: false",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory owner review console v16 validation")
    print("RESULT: PASS")
    print("terminal_condition=OWNER_REVIEW_CONSOLE_V16_READY")
    print("selected_next_safe_goal=owner_selects_local_iteration_or_explicit_protected_action_authorization")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "avf" / "influence_factory" / "product_app"
RECORD_PATH = APP_DIR / "product_workbench_v3_record.json"

REQUIRED_FILES = [
    "avf/influence_factory/product_app/product_workbench_v3_record.json",
    "avf/influence_factory/product_app/index.html",
    "avf/influence_factory/product_app/styles.css",
    "avf/influence_factory/product_app/app.js",
    "avf/influence_factory/product_app/README.md",
    "avf/influence_factory/product_app/render-check-v3.png",
    "avf/influence_factory/product_app/self-test-dom.html",
    "avf/influence_factory/product_app/self_test_report.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V3_COMPLETION_AUDIT.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V3_TERMINAL_REPORT.md",
    "docs/goals/NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V3.md",
]

REQUIRED_HTML = [
    "Idea Intake",
    "Persona Studio",
    "Style Memory",
    "Content Generator",
    "Review Board",
    "Feedback Loop",
    "Task Board",
    "Editorial Calendar",
    "Safety Scanner",
    "Import Workspace JSON",
    "Export Workspace JSON",
    "Evidence Ledger",
    "Self Test",
]

REQUIRED_JS = [
    "createIdeaBrief",
    "addPersona",
    "saveStyleMemory",
    "generateContentBatch",
    "applyReviewDecision",
    "importFeedback",
    "synthesizeNextTasks",
    "buildEditorialCalendar",
    "runSafetyScan",
    "importWorkspaceJson",
    "exportWorkspaceJson",
    "runSelfTest",
    "localStorage",
]

FORBIDDEN_JS = [
    "fetch(",
    "XMLHttpRequest",
    "navigator.sendBeacon",
    "http://",
    "https://",
    "import(",
]

FALSE_FLAGS = [
    "openclaude_required",
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "deploy_performed",
    "publish_performed",
    "platform_posting_performed",
    "personal_account_automation_performed",
    "deceptive_influence_supported",
    "release_readiness_claimed",
    "public_readiness_claimed",
    "production_readiness_claimed",
]


def fail(message: str) -> None:
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    record = json.loads(read(RECORD_PATH))
    if record.get("terminal_condition") != "LOCAL_PRODUCT_WORKBENCH_V3_READY":
        fail("terminal_condition must be LOCAL_PRODUCT_WORKBENCH_V3_READY")
    if record.get("selected_next_safe_goal") != "owner_operates_v3_locally_or_authorizes_protected_public_operation":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    html = read(APP_DIR / "index.html")
    missing_html = [phrase for phrase in REQUIRED_HTML if phrase not in html]
    if missing_html:
        fail("index.html missing product sections:\n" + "\n".join(missing_html))

    js = read(APP_DIR / "app.js")
    missing_js = [phrase for phrase in REQUIRED_JS if phrase not in js]
    if missing_js:
        fail("app.js missing product behavior:\n" + "\n".join(missing_js))

    forbidden = [phrase for phrase in FORBIDDEN_JS if phrase in js or phrase in html]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    audit = read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V3_COMPLETION_AUDIT.md")
    if audit.count("status: PROVEN") < 30:
        fail("V3 completion audit must include at least 30 PROVEN requirements")
    if "status: MISSING" in audit or "status: UNVERIFIED" in audit:
        fail("V3 completion audit contains missing or unverified status")

    screenshot_size = (APP_DIR / "render-check-v3.png").stat().st_size
    if screenshot_size < 10000:
        fail("render-check-v3.png is too small to prove a non-empty render")

    self_test_dom = read(APP_DIR / "self-test-dom.html")
    for phrase in [
        "SELF_TEST_PASS",
        "Generated local template draft",
        "Owner decision recorded locally",
        "Next tasks synthesized locally",
    ]:
        if phrase not in self_test_dom:
            fail(f"self-test DOM missing {phrase}")

    self_test_report = read(APP_DIR / "self_test_report.md")
    for phrase in ["Chrome headless", "SELF_TEST_PASS", "render-check-v3.png"]:
        if phrase not in self_test_report:
            fail(f"self_test_report.md missing {phrase}")

    next_text = read(ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V3.md")
    if next_text.count("selected_next_safe_goal: owner_operates_v3_locally_or_authorizes_protected_public_operation") != 1:
        fail("V3 next goal must be exactly one")

    print("AVF Influence Factory product workbench v3 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V3_READY")
    print("selected_next_safe_goal=owner_operates_v3_locally_or_authorizes_protected_public_operation")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

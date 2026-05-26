from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "avf" / "influence_factory" / "product_app"
RECORD_PATH = APP_DIR / "product_workbench_v2_record.json"

REQUIRED_FILES = [
    "avf/influence_factory/product_app/product_workbench_v2_record.json",
    "avf/influence_factory/product_app/index.html",
    "avf/influence_factory/product_app/styles.css",
    "avf/influence_factory/product_app/app.js",
    "avf/influence_factory/product_app/README.md",
    "avf/influence_factory/product_app/render-check-v2.png",
    "avf/influence_factory/product_app/render_report_v2.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V2_COMPLETION_AUDIT.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V2_TERMINAL_REPORT.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_REALITY_AUDIT.md",
    "docs/goals/NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V2.md",
]

REQUIRED_HTML = [
    "Idea Intake",
    "Persona Studio",
    "Style Memory",
    "Content Generator",
    "Review Board",
    "Feedback Loop",
    "Next Task Synthesizer",
    "Export Workspace JSON",
]

REQUIRED_JS = [
    "createIdeaBrief",
    "addPersona",
    "saveStyleMemory",
    "generateContentBatch",
    "applyReviewDecision",
    "importFeedback",
    "synthesizeNextTasks",
    "exportWorkspaceJson",
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
    if record.get("terminal_condition") != "LOCAL_PRODUCT_WORKBENCH_V2_READY":
        fail("terminal_condition must be LOCAL_PRODUCT_WORKBENCH_V2_READY")
    if record.get("selected_next_safe_goal") != "owner_runs_local_workbench_v2_and_exports_workspace_json":
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

    audit = read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V2_COMPLETION_AUDIT.md")
    if audit.count("status: PROVEN") < 25:
        fail("V2 completion audit must include at least 25 PROVEN requirements")
    if "status: MISSING" in audit or "status: UNVERIFIED" in audit:
        fail("V2 completion audit contains missing or unverified status")

    next_text = read(ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V2.md")
    if next_text.count("selected_next_safe_goal: owner_runs_local_workbench_v2_and_exports_workspace_json") != 1:
        fail("V2 next goal must be exactly one")

    screenshot_size = (APP_DIR / "render-check-v2.png").stat().st_size
    if screenshot_size < 10000:
        fail("render-check-v2.png is too small to prove a non-empty render")

    render_report = read(APP_DIR / "render_report_v2.md")
    for phrase in ["Chrome headless", "Idea Intake", "Content Generator", "Export Workspace JSON"]:
        if phrase not in render_report:
            fail(f"render_report_v2.md missing {phrase}")

    reality = read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_REALITY_AUDIT.md")
    for phrase in [
        "local_product_workbench_ready: true",
        "public_or_platform_product_complete: false",
        "protected_action_required_for_public_operation: true",
    ]:
        if phrase not in reality:
            fail(f"reality audit missing {phrase}")

    print("AVF Influence Factory product workbench v2 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V2_READY")
    print("selected_next_safe_goal=owner_runs_local_workbench_v2_and_exports_workspace_json")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

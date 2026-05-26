from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "avf" / "influence_factory" / "product_app"
RECORD_PATH = APP_DIR / "product_mvp_record.json"

REQUIRED_FILES = [
    "avf/influence_factory/product_app/product_mvp_record.json",
    "avf/influence_factory/product_app/index.html",
    "avf/influence_factory/product_app/styles.css",
    "avf/influence_factory/product_app/app.js",
    "avf/influence_factory/product_app/README.md",
    "avf/influence_factory/product_app/render-check.png",
    "avf/influence_factory/product_app/render_report.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_MVP_COMPLETION_AUDIT.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_MVP_VALIDATION_REPORT.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_MVP_TERMINAL_REPORT.md",
    "docs/goals/NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_MVP.md",
]

REQUIRED_HTML = [
    "Influence Factory Workbench",
    "Review Queue",
    "Persona Network",
    "Content Batch",
    "Brand/IP Style Memory",
    "Evidence Ledger",
    "Owner Decision",
    "Export Review JSON",
]

REQUIRED_JS = [
    "localStorage",
    "approve",
    "revise",
    "reject",
    "exportReviewJson",
    "renderReviewQueue",
    "renderEvidenceLedger",
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
    if record.get("terminal_condition") != "LOCAL_PRODUCT_MVP_READY_FOR_OWNER_USE":
        fail("terminal_condition must be LOCAL_PRODUCT_MVP_READY_FOR_OWNER_USE")
    if record.get("selected_next_safe_goal") != "owner_uses_local_product_mvp_for_first_review":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    html = read(APP_DIR / "index.html")
    missing_html = [phrase for phrase in REQUIRED_HTML if phrase not in html]
    if missing_html:
        fail("index.html missing phrases:\n" + "\n".join(missing_html))

    js = read(APP_DIR / "app.js")
    missing_js = [phrase for phrase in REQUIRED_JS if phrase not in js]
    if missing_js:
        fail("app.js missing behavior markers:\n" + "\n".join(missing_js))

    forbidden = [phrase for phrase in FORBIDDEN_JS if phrase in js or phrase in html]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    audit = read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_MVP_COMPLETION_AUDIT.md")
    if audit.count("status: PROVEN") < 20:
        fail("MVP completion audit must include at least 20 PROVEN requirements")
    if "status: MISSING" in audit or "status: UNVERIFIED" in audit:
        fail("MVP completion audit contains missing or unverified status")

    next_text = read(ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_MVP.md")
    if next_text.count("selected_next_safe_goal: owner_uses_local_product_mvp_for_first_review") != 1:
        fail("NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_MVP.md must select exactly one next safe goal")

    screenshot_size = (APP_DIR / "render-check.png").stat().st_size
    if screenshot_size < 10000:
        fail("render-check.png is too small to prove a non-empty render")

    render_report = read(APP_DIR / "render_report.md")
    for phrase in ["Chrome headless", "Influence Factory Workbench", "Review Queue", "Export Review JSON"]:
        if phrase not in render_report:
            fail(f"render_report.md missing {phrase}")

    print("AVF Influence Factory product MVP validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_PRODUCT_MVP_READY_FOR_OWNER_USE")
    print("selected_next_safe_goal=owner_uses_local_product_mvp_for_first_review")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

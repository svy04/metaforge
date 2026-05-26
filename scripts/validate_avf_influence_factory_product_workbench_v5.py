from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "avf" / "influence_factory" / "product_app"
RECORD_PATH = APP_DIR / "product_workbench_v5_record.json"

REQUIRED_FILES = [
    "avf/influence_factory/product_app/product_workbench_v5_record.json",
    "avf/influence_factory/product_app/index.html",
    "avf/influence_factory/product_app/styles.css",
    "avf/influence_factory/product_app/app.js",
    "avf/influence_factory/product_app/README.md",
    "avf/influence_factory/product_app/render-check-v5.png",
    "avf/influence_factory/product_app/self-test-v5-dom.html",
    "avf/influence_factory/product_app/self_test_report_v5.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V5_COMPLETION_AUDIT.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V5_TERMINAL_REPORT.md",
    "docs/goals/NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V5.md",
]

REQUIRED_HTML = [
    "One-Click Factory Run",
    "Factory Packet Viewer",
    "Product Brief",
    "Strategy Brief",
    "Brand/IP Brief",
    "Content Pack",
    "Image Prompt Pack",
    "Codex Implementation Pack",
    "Safety/Approval Pack",
    "Next Action Pack",
]

REQUIRED_JS = [
    "runFactoryFromIdea",
    "buildFactoryPacket",
    "renderFactoryPacket",
    "factoryPacket",
    "Product Brief",
    "Image Prompt Pack",
    "Codex Implementation Pack",
    "Protected action boundary preserved",
]

FORBIDDEN_APP_MARKERS = [
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
    "dependency_install_performed",
    "deploy_performed",
    "publish_performed",
    "platform_posting_performed",
    "personal_account_automation_performed",
    "deceptive_influence_supported",
    "release_readiness_claimed",
    "public_readiness_claimed",
    "production_readiness_claimed",
    "external_validation_claimed",
    "autonomous_reliability_claimed",
]


def fail(message: str) -> None:
    print("AVF Influence Factory product workbench v5 validation")
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
    if record.get("terminal_condition") != "LOCAL_PRODUCT_WORKBENCH_V5_READY":
        fail("terminal_condition must be LOCAL_PRODUCT_WORKBENCH_V5_READY")
    if record.get("local_product_status") != "one_click_local_factory_product":
        fail("local_product_status must be one_click_local_factory_product")
    if record.get("selected_next_safe_goal") != "owner_runs_first_real_idea_through_v5_or_authorizes_protected_productization":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    html = read(APP_DIR / "index.html")
    missing_html = [phrase for phrase in REQUIRED_HTML if phrase not in html]
    if missing_html:
        fail("index.html missing one-click factory sections:\n" + "\n".join(missing_html))

    js = read(APP_DIR / "app.js")
    missing_js = [phrase for phrase in REQUIRED_JS if phrase not in js]
    if missing_js:
        fail("app.js missing one-click factory behavior:\n" + "\n".join(missing_js))

    forbidden = [phrase for phrase in FORBIDDEN_APP_MARKERS if phrase in js or phrase in html]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    audit = read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V5_COMPLETION_AUDIT.md")
    if audit.count("status: PROVEN") < 55:
        fail("V5 completion audit must include at least 55 PROVEN requirements")
    if "status: MISSING" in audit or "status: UNVERIFIED" in audit:
        fail("V5 completion audit contains missing or unverified status")

    screenshot_size = (APP_DIR / "render-check-v5.png").stat().st_size
    if screenshot_size < 10000:
        fail("render-check-v5.png is too small to prove a non-empty render")

    self_test_dom = read(APP_DIR / "self-test-v5-dom.html")
    for phrase in [
        "SELF_TEST_PASS_V5",
        "Factory packet generated",
        "Image prompt pack included",
        "Codex implementation packet included",
        "Protected action boundary preserved",
    ]:
        if phrase not in self_test_dom:
            fail(f"self-test DOM missing {phrase}")

    self_test_report = read(APP_DIR / "self_test_report_v5.md")
    for phrase in ["Chrome headless", "SELF_TEST_PASS_V5", "render-check-v5.png"]:
        if phrase not in self_test_report:
            fail(f"self_test_report_v5.md missing {phrase}")

    next_text = read(ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V5.md")
    if next_text.count("selected_next_safe_goal: owner_runs_first_real_idea_through_v5_or_authorizes_protected_productization") != 1:
        fail("V5 next goal must be exactly one")

    print("AVF Influence Factory product workbench v5 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V5_READY")
    print("local_product_status=one_click_local_factory_product")
    print("selected_next_safe_goal=owner_runs_first_real_idea_through_v5_or_authorizes_protected_productization")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
RECORD_PATH = APP / "product_workbench_v13_record.json"

REQUIRED_FILES = [
    RECORD_PATH,
    APP / "index.html",
    APP / "styles.css",
    APP / "app.js",
    APP / "README.md",
    APP / "render-check-v13.png",
    APP / "self_test_report_v13.md",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V13_COMPLETION_AUDIT.md",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V13_TERMINAL_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V13.md",
    ROOT / "avf" / "influence_factory" / "owner_goal_runs" / "transparent-ai-creator-collective-001" / "review_v12" / "owner_bundle_review_v12_record.json",
]

REQUIRED_HTML = [
    "Owner Goal Bundle Builder",
    "Style Continuity Workbench",
    "Content Approval Board",
    "Evidence Dashboard",
    "Build Owner Goal Bundle Preview",
    "Build Style Continuity Workbench",
    "Build Content Approval Board",
    "Build Evidence Dashboard",
]

REQUIRED_JS = [
    "buildOwnerGoalBundlePreview",
    "buildStyleContinuityWorkbench",
    "buildContentApprovalBoard",
    "buildEvidenceDashboard",
    "renderOwnerGoalBundle",
    "renderStyleWorkbench",
    "renderContentApprovalBoard",
    "renderEvidenceDashboard",
    "SELF_TEST_PASS_V13",
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
    print("AVF Influence Factory product workbench v13 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    record = json.loads(read(RECORD_PATH))
    if record.get("terminal_condition") != "LOCAL_PRODUCT_WORKBENCH_V13_READY":
        fail("terminal_condition must be LOCAL_PRODUCT_WORKBENCH_V13_READY")
    if record.get("local_product_status") != "owner_goal_review_backlog_implemented_locally":
        fail("local_product_status mismatch")
    if record.get("selected_next_safe_goal") != "owner_uses_v13_for_real_goal_review_or_authorizes_protected_public_operation":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for phrase in REQUIRED_HTML:
        if phrase not in html:
            fail(f"index.html missing {phrase}")
    for phrase in REQUIRED_JS:
        if phrase not in js:
            fail(f"app.js missing {phrase}")
    forbidden = [phrase for phrase in FORBIDDEN_APP_MARKERS if phrase in js or phrase in html]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    screenshot_size = (APP / "render-check-v13.png").stat().st_size
    if screenshot_size < 10000:
        fail("render-check-v13.png is too small to prove a non-empty render")

    self_test_report = read(APP / "self_test_report_v13.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V13",
        "Owner goal bundle preview built",
        "Style continuity workbench ready",
        "Content approval board ready",
        "Evidence dashboard ready",
    ]:
        if phrase not in self_test_report:
            fail(f"self_test_report_v13.md missing {phrase}")

    next_text = read(ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V13.md")
    if next_text.count("selected_next_safe_goal: owner_uses_v13_for_real_goal_review_or_authorizes_protected_public_operation") != 1:
        fail("V13 next goal must be exactly one")
    if "selected_next_goal_executed: false" not in next_text:
        fail("V13 selected_next_goal_executed must be false")

    print("AVF Influence Factory product workbench v13 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V13_READY")
    print("local_product_status=owner_goal_review_backlog_implemented_locally")
    print("selected_next_safe_goal=owner_uses_v13_for_real_goal_review_or_authorizes_protected_public_operation")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

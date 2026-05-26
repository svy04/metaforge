from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
PACKAGE = ROOT / "avf" / "influence_factory" / "operator_package_v14"
RECORD_PATH = PACKAGE / "operator_package_v14_record.json"

REQUIRED_FILES = [
    RECORD_PATH,
    PACKAGE / "OPERATOR_QUICKSTART.md",
    PACKAGE / "FIRST_REAL_GOAL_TEMPLATE.json",
    PACKAGE / "RUN_SEQUENCE.md",
    PACKAGE / "LOCAL_ACCEPTANCE_CHECKLIST.md",
    PACKAGE / "PROTECTED_ACTION_AUTHORIZATION_REQUEST.md",
    PACKAGE / "OPERATOR_HANDOFF_PACKET.md",
    PACKAGE / "run_manifest.json",
    PACKAGE / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v13_record.json",
    APP / "product_workbench_v14_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "styles.css",
    APP / "render-check-v14.png",
    APP / "self_test_report_v14.md",
    ROOT / "scripts" / "create_avf_influence_factory_operator_package_v14.py",
    ROOT / "scripts" / "run_avf_influence_factory_operator_cycle_local.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OPERATOR_PACKAGE_V14_COMPLETION_AUDIT.md",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OPERATOR_PACKAGE_V14_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OPERATOR_PACKAGE_V14.md",
]

REQUIRED_APP_MARKERS = [
    "Operator Command Center",
    "Local Operator Package",
    "Run Sequence",
    "Protected Action Request",
    "Build Operator Package",
    "buildOperatorPackage",
    "renderOperatorPackage",
    "SELF_TEST_PASS_V14",
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
    "deceptive_influence_supported",
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
    print("Influence Factory operator package v14 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    record = read_json(RECORD_PATH)
    app_record = read_json(APP / "product_workbench_v14_record.json")
    for data, name in [(record, "operator record"), (app_record, "app record")]:
        if data.get("terminal_condition") != "LOCAL_OPERATOR_PACKAGE_V14_READY":
            fail(f"{name} terminal_condition mismatch")
        if data.get("selected_next_safe_goal") != "owner_runs_v14_operator_package_with_real_goal_or_requests_protected_authorization":
            fail(f"{name} selected_next_safe_goal mismatch")
        if data.get("next_safe_goal_count") != 1:
            fail(f"{name} next_safe_goal_count must be 1")
        for flag in FALSE_FLAGS:
            if data.get(flag) is not False:
                fail(f"{name} {flag} must be false")

    goal_template = read_json(PACKAGE / "FIRST_REAL_GOAL_TEMPLATE.json")
    for field in ["goal_id", "idea", "audience", "promise", "proof_target", "brand_dna", "character_bible", "visual_guide", "forbidden_styles", "first_result"]:
        if field not in goal_template:
            fail(f"FIRST_REAL_GOAL_TEMPLATE missing {field}")

    manifest = read_json(PACKAGE / "run_manifest.json")
    if manifest.get("protected_action_executed") is not False:
        fail("run_manifest protected_action_executed must be false")
    if len(manifest.get("operator_files", [])) < 7:
        fail("run_manifest must list operator files")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    screenshot_size = (APP / "render-check-v14.png").stat().st_size
    if screenshot_size < 10000:
        fail("render-check-v14.png is too small to prove non-empty render")

    self_test_report = read(APP / "self_test_report_v14.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V14",
        "Operator package built",
        "Protected action request ready",
    ]:
        if phrase not in self_test_report:
            fail(f"self_test_report_v14.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: owner_runs_v14_operator_package_with_real_goal_or_requests_protected_authorization",
        "selected_next_goal_executed: false",
    ]:
        if marker not in combined:
            fail(f"required boundary marker missing: {marker}")

    print("Influence Factory operator package v14 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_OPERATOR_PACKAGE_V14_READY")
    print("local_product_status=operator_package_ready_for_real_goal_use")
    print("selected_next_safe_goal=owner_runs_v14_operator_package_with_real_goal_or_requests_protected_authorization")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V19 = (
    ROOT
    / "avf"
    / "influence_factory"
    / "operator_package_v14"
    / "real_goal_run_v15"
    / "owner_review_v16"
    / "local_iteration_v17"
    / "executed_iteration_v18"
    / "owner_review_v19"
)
V20 = V19 / "local_operating_loop_templates_v20"
RECORD = V20 / "local_operating_loop_templates_v20_record.json"

REQUIRED_FILES = [
    V19 / "owner_review_continuation_v19_record.json",
    RECORD,
    V20 / "IDEA_INTAKE_LOOP_TEMPLATE.md",
    V20 / "CONTENT_REVIEW_LOOP_TEMPLATE.md",
    V20 / "STYLE_IP_REVIEW_LOOP_TEMPLATE.md",
    V20 / "CODEX_PACKET_REVIEW_LOOP_TEMPLATE.md",
    V20 / "EVIDENCE_COMPARISON_LOOP_TEMPLATE.md",
    V20 / "FIRST_OWNER_PRODUCT_GOAL_INTAKE_TEMPLATE.json",
    V20 / "FIRST_OWNER_PRODUCT_GOAL_INTAKE_TEMPLATE.md",
    V20 / "FACTORY_READY_TERMINAL_REPORT.md",
    V20 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v20_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v20.png",
    APP / "self_test_report_v20.md",
    ROOT / "scripts" / "create_avf_influence_factory_local_operating_loop_templates_v20.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_OPERATING_LOOP_TEMPLATES_V20_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_OPERATING_LOOP_TEMPLATES_V20.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v20",
    "Operating Loop Templates",
    "First Product Goal Intake",
    "Factory Ready Terminal Report",
    "Build Operating Loop Templates",
    "buildOperatingLoopTemplates",
    "renderOperatingLoopTemplates",
    "SELF_TEST_PASS_V20",
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
    print("Influence Factory local operating loop templates v20 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "FACTORY_READY_FOR_FIRST_OWNER_PRODUCT_GOAL":
        fail(f"{label} terminal_condition mismatch")
    if data.get("selected_next_safe_goal") != "owner_provides_first_real_product_goal_for_factory_run":
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

    v19 = read_json(V19 / "owner_review_continuation_v19_record.json")
    if v19.get("terminal_condition") != "OWNER_REVIEW_CONTINUATION_V19_READY":
        fail("v19 owner review continuation is not ready")

    validate_record(read_json(RECORD), "v20 record")
    validate_record(read_json(APP / "product_workbench_v20_record.json"), "app record")

    intake = read_json(V20 / "FIRST_OWNER_PRODUCT_GOAL_INTAKE_TEMPLATE.json")
    for field in ["product_idea", "target_user", "proof_target", "brand_ip_constraints", "blocked_actions"]:
        if field not in intake:
            fail(f"first owner product goal intake missing {field}")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v20.png").stat().st_size < 10000:
        fail("render-check-v20.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v20.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V20",
        "Operating loop templates ready",
        "First product goal intake ready",
        "Factory ready terminal report ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v20.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: owner_provides_first_real_product_goal_for_factory_run",
        "selected_next_goal_executed: false",
        "fake human impersonation",
        "undisclosed bot networks",
        "platform posting",
        "FACTORY_READY_FOR_FIRST_OWNER_PRODUCT_GOAL",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory local operating loop templates v20 validation")
    print("RESULT: PASS")
    print("terminal_condition=FACTORY_READY_FOR_FIRST_OWNER_PRODUCT_GOAL")
    print("selected_next_safe_goal=owner_provides_first_real_product_goal_for_factory_run")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

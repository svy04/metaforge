from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V28 = (
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
    / "mvp_work_items_v23"
    / "local_mvp_acceptance_v24"
    / "local_beta_candidate_v25"
    / "product_completion_audit_v26"
    / "local_export_package_v27"
    / "internal_user_trial_v28"
)
V29 = V28 / "internal_trial_improvements_v29"
RECORD = V29 / "internal_trial_improvements_v29_record.json"

REQUIRED_FILES = [
    V28 / "internal_user_trial_v28_record.json",
    V28 / "INTERNAL_USER_TRIAL_PACKET.json",
    RECORD,
    V29 / "INTERNAL_TRIAL_IMPROVEMENTS_PACKET.json",
    V29 / "INTERNAL_TRIAL_IMPROVEMENTS_PACKET.md",
    V29 / "QUICK_START_PATH.md",
    V29 / "EXPORT_STATUS_CENTER.md",
    V29 / "OWNER_AUTHORIZATION_SUMMARY.md",
    V29 / "FIRST_GOAL_CONFIDENCE_SIGNALS.md",
    V29 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v29_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v29.png",
    APP / "self_test_report_v29.md",
    ROOT / "scripts" / "create_avf_influence_factory_internal_trial_improvements_v29.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_INTERNAL_TRIAL_IMPROVEMENTS_V29_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_INTERNAL_TRIAL_IMPROVEMENTS_V29.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v29",
    "Trial Improvement Center",
    "Quick Start Path",
    "Export Status Center",
    "Owner Authorization Summary",
    "First Goal Confidence Signals",
    "Apply Internal Trial Improvements",
    "applyInternalTrialImprovements",
    "renderInternalTrialImprovements",
    "SELF_TEST_PASS_V29",
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

REQUIRED_IMPROVEMENTS = [
    "quick_start_path",
    "export_status_center",
    "owner_authorization_summary",
    "first_goal_confidence_signals",
]

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory internal trial improvements v29 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "INTERNAL_TRIAL_IMPROVEMENTS_V29_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "internal_trial_improvements_applied":
        fail(f"{label} local_product_status mismatch")
    if data.get("selected_next_safe_goal") != "run_second_internal_user_trial_v30_without_protected_actions":
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

    v28 = read_json(V28 / "internal_user_trial_v28_record.json")
    if v28.get("local_product_status") != "internal_user_trial_ready":
        fail("v28 internal user trial is not ready")

    validate_record(read_json(RECORD), "v29 record")
    validate_record(read_json(APP / "product_workbench_v29_record.json"), "app record")
    packet = read_json(V29 / "INTERNAL_TRIAL_IMPROVEMENTS_PACKET.json")
    validate_record(packet, "improvements packet")

    improvement_ids = {item.get("improvement_id") for item in packet.get("applied_improvements", [])}
    for improvement in REQUIRED_IMPROVEMENTS:
        if improvement not in improvement_ids:
            fail(f"missing improvement {improvement}")
    if any(item.get("status") != "implemented_local_only" for item in packet.get("applied_improvements", [])):
        fail("all improvements must be implemented_local_only")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v29.png").stat().st_size < 10000:
        fail("render-check-v29.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v29.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V29",
        "Quick start path ready",
        "Export status center ready",
        "First goal confidence signals ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v29.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "external_validation_claimed: false",
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: run_second_internal_user_trial_v30_without_protected_actions",
        "selected_next_goal_executed: false",
        "fake human impersonation",
        "undisclosed bot networks",
        "platform posting",
        "release readiness claim: blocked",
        "public readiness claim: blocked",
        "production readiness claim: blocked",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory internal trial improvements v29 validation")
    print("RESULT: PASS")
    print("terminal_condition=INTERNAL_TRIAL_IMPROVEMENTS_V29_READY")
    print("local_product_status=internal_trial_improvements_applied")
    print("selected_next_safe_goal=run_second_internal_user_trial_v30_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

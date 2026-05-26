from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V27 = (
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
)
V28 = V27 / "internal_user_trial_v28"
RECORD = V28 / "internal_user_trial_v28_record.json"

REQUIRED_FILES = [
    V27 / "local_export_package_v27_record.json",
    V27 / "LOCAL_EXPORT_PACKAGE.json",
    RECORD,
    V28 / "INTERNAL_USER_TRIAL_PACKET.json",
    V28 / "INTERNAL_USER_TRIAL_PACKET.md",
    V28 / "INTERNAL_USER_TRIAL_SCENARIOS.md",
    V28 / "INTERNAL_USER_TRIAL_FINDINGS.md",
    V28 / "INTERNAL_USER_TRIAL_IMPROVEMENT_BACKLOG.md",
    V28 / "INTERNAL_USER_TRIAL_SAFETY_REVIEW.md",
    V28 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v28_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v28.png",
    APP / "self_test_report_v28.md",
    ROOT / "scripts" / "create_avf_influence_factory_internal_user_trial_v28.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_INTERNAL_USER_TRIAL_V28_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_INTERNAL_USER_TRIAL_V28.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v28",
    "Internal User Trial Lab",
    "Internal User Trial Packet",
    "Trial Scenario Matrix",
    "Trial Findings",
    "Improvement Backlog",
    "Run Internal User Trial",
    "runInternalUserTrial",
    "renderInternalUserTrial",
    "SELF_TEST_PASS_V28",
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

REQUIRED_SCENARIOS = [
    "first_time_owner",
    "brand_ip_creator",
    "codex_operator",
    "safety_reviewer",
]

REQUIRED_FINDINGS = [
    "sidebar_density",
    "export_package_discoverability",
    "owner_authorization_copy",
    "first_goal_completion_confidence",
]

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory internal user trial v28 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "LOCAL_INTERNAL_USER_TRIAL_V28_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "internal_user_trial_ready":
        fail(f"{label} local_product_status mismatch")
    if data.get("external_validation_claimed") is not False:
        fail(f"{label} external_validation_claimed must be false")
    if data.get("selected_next_safe_goal") != "implement_internal_trial_improvements_v29_without_protected_actions":
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

    v27 = read_json(V27 / "local_export_package_v27_record.json")
    if v27.get("local_product_status") != "local_export_package_ready":
        fail("v27 local export package is not ready")

    validate_record(read_json(RECORD), "v28 record")
    validate_record(read_json(APP / "product_workbench_v28_record.json"), "app record")
    packet = read_json(V28 / "INTERNAL_USER_TRIAL_PACKET.json")
    validate_record(packet, "internal user trial packet")

    scenario_ids = {item.get("scenario_id") for item in packet.get("trial_scenarios", [])}
    for scenario in REQUIRED_SCENARIOS:
        if scenario not in scenario_ids:
            fail(f"trial scenarios missing {scenario}")
    finding_ids = {item.get("finding_id") for item in packet.get("trial_findings", [])}
    for finding in REQUIRED_FINDINGS:
        if finding not in finding_ids:
            fail(f"trial findings missing {finding}")
    if any(item.get("status") != "local_safe_improvement" for item in packet.get("improvement_backlog", [])):
        fail("all improvement backlog items must be local_safe_improvement")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v28.png").stat().st_size < 10000:
        fail("render-check-v28.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v28.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V28",
        "Internal user trial packet ready",
        "Trial findings ready",
        "Improvement backlog ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v28.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "external_validation_claimed: false",
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: implement_internal_trial_improvements_v29_without_protected_actions",
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

    print("Influence Factory internal user trial v28 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_INTERNAL_USER_TRIAL_V28_READY")
    print("local_product_status=internal_user_trial_ready")
    print("external_validation_claimed=false")
    print("selected_next_safe_goal=implement_internal_trial_improvements_v29_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

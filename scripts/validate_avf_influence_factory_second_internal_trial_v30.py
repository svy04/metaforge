from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V29 = (
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
    / "internal_trial_improvements_v29"
)
V30 = V29 / "second_internal_user_trial_v30"
RECORD = V30 / "second_internal_user_trial_v30_record.json"

REQUIRED_FILES = [
    V29 / "internal_trial_improvements_v29_record.json",
    V29 / "INTERNAL_TRIAL_IMPROVEMENTS_PACKET.json",
    RECORD,
    V30 / "SECOND_INTERNAL_USER_TRIAL_PACKET.json",
    V30 / "SECOND_INTERNAL_USER_TRIAL_PACKET.md",
    V30 / "IMPROVEMENT_VERIFICATION_MATRIX.md",
    V30 / "RESIDUAL_FRICTION_REGISTER.md",
    V30 / "SECOND_TRIAL_OWNER_CONFIDENCE_REPORT.md",
    V30 / "SECOND_TRIAL_SAFETY_REVIEW.md",
    V30 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v30_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v30.png",
    APP / "self_test_report_v30.md",
    ROOT / "scripts" / "create_avf_influence_factory_second_internal_trial_v30.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_SECOND_INTERNAL_TRIAL_V30_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_SECOND_INTERNAL_TRIAL_V30.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v30",
    "Second Internal Trial Lab",
    "Second Internal User Trial Packet",
    "Improvement Verification Matrix",
    "Residual Friction Register",
    "Owner Confidence Report",
    "Run Second Internal Trial",
    "runSecondInternalTrial",
    "renderSecondInternalTrial",
    "SELF_TEST_PASS_V30",
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

REQUIRED_VERIFICATIONS = [
    "quick_start_path",
    "export_status_center",
    "owner_authorization_summary",
    "first_goal_confidence_signals",
]

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory second internal trial v30 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "SECOND_INTERNAL_TRIAL_V30_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "second_internal_trial_ready":
        fail(f"{label} local_product_status mismatch")
    if data.get("external_validation_claimed") is not False:
        fail(f"{label} external_validation_claimed must be false")
    if data.get("selected_next_safe_goal") != "prepare_owner_external_validation_authorization_packet_v31_without_execution":
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

    v29 = read_json(V29 / "internal_trial_improvements_v29_record.json")
    if v29.get("local_product_status") != "internal_trial_improvements_applied":
        fail("v29 internal trial improvements are not applied")

    validate_record(read_json(RECORD), "v30 record")
    validate_record(read_json(APP / "product_workbench_v30_record.json"), "app record")
    packet = read_json(V30 / "SECOND_INTERNAL_USER_TRIAL_PACKET.json")
    validate_record(packet, "second trial packet")

    verification_ids = {item.get("improvement_id") for item in packet.get("improvement_verification_matrix", [])}
    for item in REQUIRED_VERIFICATIONS:
        if item not in verification_ids:
            fail(f"verification matrix missing {item}")
    if any(item.get("status") != "verified_internal_improved" for item in packet.get("improvement_verification_matrix", [])):
        fail("all improvement verifications must be verified_internal_improved")
    if not packet.get("residual_friction_register"):
        fail("residual friction register must identify remaining local risks")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v30.png").stat().st_size < 10000:
        fail("render-check-v30.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v30.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V30",
        "Second internal trial packet ready",
        "Improvement verification matrix ready",
        "Owner confidence report ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v30.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "external_validation_claimed: false",
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: prepare_owner_external_validation_authorization_packet_v31_without_execution",
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

    print("Influence Factory second internal trial v30 validation")
    print("RESULT: PASS")
    print("terminal_condition=SECOND_INTERNAL_TRIAL_V30_READY")
    print("local_product_status=second_internal_trial_ready")
    print("external_validation_claimed=false")
    print("selected_next_safe_goal=prepare_owner_external_validation_authorization_packet_v31_without_execution")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

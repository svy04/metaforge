from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V30 = (
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
    / "second_internal_user_trial_v30"
)
V31 = V30 / "owner_external_validation_authorization_v31"
RECORD = V31 / "owner_external_validation_authorization_v31_record.json"

REQUIRED_FILES = [
    V30 / "second_internal_user_trial_v30_record.json",
    V30 / "SECOND_INTERNAL_USER_TRIAL_PACKET.json",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_SECOND_INTERNAL_TRIAL_V30_VALIDATION_REPORT.md",
    RECORD,
    V31 / "OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_PACKET.json",
    V31 / "OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_PACKET.md",
    V31 / "OWNER_EXTERNAL_VALIDATION_DECISION_REQUEST.md",
    V31 / "EXTERNAL_VALIDATION_EVIDENCE_REQUIREMENTS.md",
    V31 / "PROTECTED_ACTION_BOUNDARY_REPORT.md",
    V31 / "FINAL_OWNER_DECISION_PACKET.md",
    V31 / "AUTONOMOUS_CONTINUATION_TERMINAL_REPORT.md",
    V31 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v31_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v31.png",
    APP / "self_test_report_v31.md",
    ROOT / "scripts" / "create_avf_influence_factory_owner_external_validation_authorization_v31.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_V31_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_V31.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v31",
    "Owner External Validation Authorization",
    "External Validation Authorization Packet",
    "Protected Action Boundary Report",
    "Final Owner Decision Packet",
    "Prepare External Validation Authorization Packet",
    "prepareExternalValidationAuthorizationPacket",
    "renderExternalValidationAuthorization",
    "SELF_TEST_PASS_V31",
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
    "external_validation_executed",
    "external_validation_authorized",
    "autonomous_reliability_claimed",
]

REQUIRED_DECISIONS = [
    "external_validation",
    "provider_or_live_model_validation",
    "public_demo_or_public_claim",
    "release_or_production_readiness_claim",
    "platform_posting_or_account_automation",
]

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory owner external validation authorization v31 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "PROTECTED_ACTION_REQUIRED":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "owner_external_validation_authorization_packet_ready":
        fail(f"{label} local_product_status mismatch")
    if data.get("next_safe_goal_count") != 0:
        fail(f"{label} next_safe_goal_count must be 0 at terminal boundary")
    if data.get("selected_next_safe_goal") is not None:
        fail(f"{label} selected_next_safe_goal must be null at terminal boundary")
    if data.get("owner_decision_required") is not True:
        fail(f"{label} owner_decision_required must be true")
    for flag in FALSE_FLAGS:
        if data.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    v30 = read_json(V30 / "second_internal_user_trial_v30_record.json")
    if v30.get("selected_next_safe_goal") != "prepare_owner_external_validation_authorization_packet_v31_without_execution":
        fail("v30 selected next safe goal does not point to v31")
    if "RESULT: PASS" not in read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_SECOND_INTERNAL_TRIAL_V30_VALIDATION_REPORT.md"):
        fail("accepted v30 validation report is not PASS")

    validate_record(read_json(RECORD), "v31 record")
    validate_record(read_json(APP / "product_workbench_v31_record.json"), "app record")
    packet = read_json(V31 / "OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_PACKET.json")
    validate_record(packet, "authorization packet")

    decision_ids = {item.get("decision_id") for item in packet.get("required_owner_decisions", [])}
    for decision_id in REQUIRED_DECISIONS:
        if decision_id not in decision_ids:
            fail(f"owner decision packet missing {decision_id}")
    if any(item.get("default_authorized") is not False for item in packet.get("required_owner_decisions", [])):
        fail("all protected owner decisions must default to false")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v31.png").stat().st_size < 10000:
        fail("render-check-v31.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v31.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V31",
        "External validation authorization packet ready",
        "Protected action boundary reached",
        "Owner decision packet ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v31.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    required_markers = [
        "terminal_condition: PROTECTED_ACTION_REQUIRED",
        "external_validation_authorized: false",
        "external_validation_executed: false",
        "external_validation_claimed: false",
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: null",
        "next_safe_goal_count: 0",
        "fake human impersonation: blocked",
        "undisclosed bot networks: blocked",
        "platform posting: blocked",
        "release readiness claim: blocked",
        "public readiness claim: blocked",
        "production readiness claim: blocked",
        "external validation claim: blocked",
    ]
    for marker in required_markers:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory owner external validation authorization v31 validation")
    print("RESULT: PASS")
    print("terminal_condition=PROTECTED_ACTION_REQUIRED")
    print("local_product_status=owner_external_validation_authorization_packet_ready")
    print("external_validation_authorized=false")
    print("external_validation_executed=false")
    print("external_validation_claimed=false")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

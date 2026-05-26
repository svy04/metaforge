from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V35 = (
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
    / "owner_external_validation_authorization_v31"
    / "local_product_completion_hardening_v32"
    / "local_distributable_package_v33"
    / "first_goal_completion_runner_v34"
    / "guided_first_run_guard_v35"
)
V36 = V35 / "local_owner_trial_script_v36"
RECORD = V36 / "local_owner_trial_script_v36_record.json"

REQUIRED_FILES = [
    V35 / "guided_first_run_guard_v35_record.json",
    V35 / "GUIDED_FIRST_RUN_GUARD_PACKET.json",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_GUIDED_FIRST_RUN_GUARD_V35_VALIDATION_REPORT.md",
    RECORD,
    V36 / "LOCAL_OWNER_TRIAL_SCRIPT_PACKET.json",
    V36 / "LOCAL_OWNER_TRIAL_SCRIPT_PACKET.md",
    V36 / "OWNER_TRIAL_RUNBOOK.md",
    V36 / "OWNER_TRIAL_STEP_SCRIPT.md",
    V36 / "OWNER_TRIAL_OBSERVATION_LOG_TEMPLATE.md",
    V36 / "OWNER_TRIAL_ACCEPTANCE_CHECKLIST.md",
    V36 / "OWNER_TRIAL_BOUNDARY_REPORT.md",
    V36 / "OWNER_TRIAL_SCRIPT_NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v36_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v36.png",
    APP / "self_test_report_v36.md",
    ROOT / "scripts" / "create_avf_influence_factory_local_owner_trial_script_v36.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_OWNER_TRIAL_SCRIPT_V36_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_OWNER_TRIAL_SCRIPT_V36.md",
]

REQUIRED_STEPS = [
    "open_local_workbench",
    "complete_guided_first_run_guard",
    "build_owner_ready_package",
    "inspect_brand_ip_style_memory",
    "inspect_image_generation_reference_packet",
    "inspect_content_and_codex_packets",
    "run_safety_boundary_review",
    "record_owner_observations",
    "decide_next_local_improvement",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v36",
    "Local Owner Trial Script",
    "Owner Trial Step Script",
    "Owner Trial Observation Log",
    "Owner Trial Acceptance Checklist",
    "Run Local Owner Trial Script",
    "runLocalOwnerTrialScript",
    "renderLocalOwnerTrialScript",
    "SELF_TEST_PASS_V36",
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

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory local owner trial script v36 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "LOCAL_OWNER_TRIAL_SCRIPT_V36_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "local_owner_trial_script_ready":
        fail(f"{label} local_product_status mismatch")
    if data.get("first_goal_flow") != "guided_first_run_to_local_owner_trial_without_external_users":
        fail(f"{label} first_goal_flow mismatch")
    if data.get("product_completion_claim_scope") != "repo_local_internal_only":
        fail(f"{label} product_completion_claim_scope mismatch")
    if data.get("selected_next_safe_goal") != "create_owner_trial_evidence_recorder_v37_without_external_users":
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

    v35 = read_json(V35 / "guided_first_run_guard_v35_record.json")
    if v35.get("terminal_condition") != "GUIDED_FIRST_RUN_GUARD_V35_READY":
        fail("v35 source record is not ready")
    if "RESULT: PASS" not in read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_GUIDED_FIRST_RUN_GUARD_V35_VALIDATION_REPORT.md"):
        fail("accepted v35 validation report is not PASS")

    validate_record(read_json(RECORD), "v36 record")
    validate_record(read_json(APP / "product_workbench_v36_record.json"), "app record")
    packet = read_json(V36 / "LOCAL_OWNER_TRIAL_SCRIPT_PACKET.json")
    validate_record(packet, "trial script packet")

    step_ids = {step.get("step_id") for step in packet.get("trial_steps", [])}
    for step_id in REQUIRED_STEPS:
        if step_id not in step_ids:
            fail(f"trial script missing step {step_id}")
    if any(step.get("execution_scope") != "owner_local_manual_trial_only" for step in packet.get("trial_steps", [])):
        fail("all trial steps must be owner_local_manual_trial_only")
    if not packet.get("observation_log_template"):
        fail("observation log template must be present")
    if not packet.get("acceptance_checklist"):
        fail("acceptance checklist must be present")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v36.png").stat().st_size < 10000:
        fail("render-check-v36.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v36.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V36",
        "Local owner trial script ready",
        "Owner trial observation log ready",
        "Owner trial acceptance checklist ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v36.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "terminal_condition: LOCAL_OWNER_TRIAL_SCRIPT_V36_READY",
        "first_goal_flow: guided_first_run_to_local_owner_trial_without_external_users",
        "product_completion_claim_scope: repo_local_internal_only",
        "external_validation_authorized: false",
        "external_validation_executed: false",
        "external_validation_claimed: false",
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: create_owner_trial_evidence_recorder_v37_without_external_users",
        "next_safe_goal_count: 1",
        "fake human impersonation: blocked",
        "undisclosed bot networks: blocked",
        "platform posting: blocked",
        "release readiness claim: blocked",
        "public readiness claim: blocked",
        "production readiness claim: blocked",
        "external validation claim: blocked",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory local owner trial script v36 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_OWNER_TRIAL_SCRIPT_V36_READY")
    print("local_product_status=local_owner_trial_script_ready")
    print("first_goal_flow=guided_first_run_to_local_owner_trial_without_external_users")
    print("selected_next_safe_goal=create_owner_trial_evidence_recorder_v37_without_external_users")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V34 = (
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
)
V35 = V34 / "guided_first_run_guard_v35"
RECORD = V35 / "guided_first_run_guard_v35_record.json"

REQUIRED_FILES = [
    V34 / "first_goal_completion_runner_v34_record.json",
    V34 / "FIRST_GOAL_OWNER_READY_PACKAGE.json",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_FIRST_GOAL_COMPLETION_RUNNER_V34_VALIDATION_REPORT.md",
    RECORD,
    V35 / "GUIDED_FIRST_RUN_GUARD_PACKET.json",
    V35 / "GUIDED_FIRST_RUN_GUARD_PACKET.md",
    V35 / "FIRST_RUN_INPUT_REQUIREMENTS.json",
    V35 / "FIRST_RUN_INPUT_REQUIREMENTS.md",
    V35 / "MISSING_INPUT_GUARD_REPORT.md",
    V35 / "OWNER_READY_BLOCKER_MATRIX.md",
    V35 / "GUIDED_FIRST_RUN_SCRIPT.md",
    V35 / "FIRST_RUN_RECOVERY_PROMPTS.md",
    V35 / "PROTECTED_BOUNDARY_RECONFIRMATION.md",
    V35 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v35_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v35.png",
    APP / "self_test_report_v35.md",
    ROOT / "scripts" / "create_avf_influence_factory_guided_first_run_guard_v35.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_GUIDED_FIRST_RUN_GUARD_V35_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_GUIDED_FIRST_RUN_GUARD_V35.md",
]

REQUIRED_INPUTS = [
    "idea_summary",
    "target_audience",
    "proof_target",
    "first_result",
    "brand_dna",
    "visual_style_guide",
    "reference_image_index",
    "blocked_behaviors",
    "codex_acceptance_criteria",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v35",
    "Guided First Run Guard",
    "Missing Input Guard",
    "First Run Input Requirements",
    "Owner Ready Blocker Matrix",
    "Run Guided First-Run Check",
    "runGuidedFirstRunGuard",
    "renderGuidedFirstRunGuard",
    "SELF_TEST_PASS_V35",
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
    print("Influence Factory guided first-run guard v35 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "GUIDED_FIRST_RUN_GUARD_V35_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "guided_first_run_guard_ready":
        fail(f"{label} local_product_status mismatch")
    if data.get("first_goal_flow") != "guided_input_to_owner_ready_package_without_external_execution":
        fail(f"{label} first_goal_flow mismatch")
    if data.get("product_completion_claim_scope") != "repo_local_internal_only":
        fail(f"{label} product_completion_claim_scope mismatch")
    if data.get("selected_next_safe_goal") != "create_local_owner_trial_script_v36_without_external_users":
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

    v34 = read_json(V34 / "first_goal_completion_runner_v34_record.json")
    if v34.get("terminal_condition") != "FIRST_GOAL_COMPLETION_RUNNER_V34_READY":
        fail("v34 source record is not ready")
    if "RESULT: PASS" not in read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_FIRST_GOAL_COMPLETION_RUNNER_V34_VALIDATION_REPORT.md"):
        fail("accepted v34 validation report is not PASS")

    validate_record(read_json(RECORD), "v35 record")
    validate_record(read_json(APP / "product_workbench_v35_record.json"), "app record")
    guard_packet = read_json(V35 / "GUIDED_FIRST_RUN_GUARD_PACKET.json")
    validate_record(guard_packet, "guard packet")

    requirement_ids = {item.get("input_id") for item in guard_packet.get("input_requirements", [])}
    for input_id in REQUIRED_INPUTS:
        if input_id not in requirement_ids:
            fail(f"guard packet missing input requirement {input_id}")
    if any(item.get("guard_status") != "required_before_owner_ready_package" for item in guard_packet.get("input_requirements", [])):
        fail("all input requirements must be required_before_owner_ready_package")
    if not guard_packet.get("recovery_prompts"):
        fail("recovery prompts must be present")
    if not guard_packet.get("owner_ready_blocker_matrix"):
        fail("owner ready blocker matrix must be present")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v35.png").stat().st_size < 10000:
        fail("render-check-v35.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v35.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V35",
        "Guided first-run guard ready",
        "Missing input guard ready",
        "Recovery prompts ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v35.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "terminal_condition: GUIDED_FIRST_RUN_GUARD_V35_READY",
        "first_goal_flow: guided_input_to_owner_ready_package_without_external_execution",
        "product_completion_claim_scope: repo_local_internal_only",
        "external_validation_authorized: false",
        "external_validation_executed: false",
        "external_validation_claimed: false",
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: create_local_owner_trial_script_v36_without_external_users",
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

    print("Influence Factory guided first-run guard v35 validation")
    print("RESULT: PASS")
    print("terminal_condition=GUIDED_FIRST_RUN_GUARD_V35_READY")
    print("local_product_status=guided_first_run_guard_ready")
    print("first_goal_flow=guided_input_to_owner_ready_package_without_external_execution")
    print("selected_next_safe_goal=create_local_owner_trial_script_v36_without_external_users")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

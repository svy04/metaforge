from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V31 = (
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
)
V32 = V31 / "local_product_completion_hardening_v32"
RECORD = V32 / "local_product_completion_hardening_v32_record.json"

REQUIRED_FILES = [
    V31 / "owner_external_validation_authorization_v31_record.json",
    V31 / "OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_PACKET.json",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_V31_VALIDATION_REPORT.md",
    RECORD,
    V32 / "LOCAL_PRODUCT_COMPLETION_SCORECARD.json",
    V32 / "LOCAL_PRODUCT_COMPLETION_SCORECARD.md",
    V32 / "USER_OPERATING_GUIDE.md",
    V32 / "FIRST_REAL_GOAL_DRY_RUN_PACKET.json",
    V32 / "FIRST_REAL_GOAL_DRY_RUN_PACKET.md",
    V32 / "PRODUCT_COMPLETION_GAP_REGISTER.md",
    V32 / "PROTECTED_BOUNDARY_RECONFIRMATION.md",
    V32 / "LOCAL_PRODUCT_COMPLETION_TERMINAL_REPORT.md",
    V32 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v32_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v32.png",
    APP / "self_test_report_v32.md",
    ROOT / "scripts" / "create_avf_influence_factory_local_product_completion_hardening_v32.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_PRODUCT_COMPLETION_HARDENING_V32_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_PRODUCT_COMPLETION_HARDENING_V32.md",
]

REQUIRED_CAPABILITIES = [
    "idea_to_strategy",
    "brand_ip_style_memory",
    "image_generation_reference_packet",
    "content_pipeline",
    "persona_network",
    "feedback_experiment_loop",
    "codex_task_packet_lane",
    "evidence_ledger",
    "approval_and_safety_gates",
    "owner_export_handoff",
    "protected_external_validation_boundary",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v32",
    "Local Product Completion Hardening",
    "Product Completion Scorecard",
    "First Real Goal Dry Run Packet",
    "User Operating Guide",
    "Run Local Product Completion Audit",
    "runLocalProductCompletionHardening",
    "renderLocalProductCompletionHardening",
    "SELF_TEST_PASS_V32",
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
    print("Influence Factory local product completion hardening v32 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "LOCAL_PRODUCT_COMPLETION_HARDENING_V32_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "internal_local_product_completion_candidate":
        fail(f"{label} local_product_status mismatch")
    if data.get("product_completion_claim_scope") != "repo_local_internal_only":
        fail(f"{label} product_completion_claim_scope mismatch")
    if data.get("next_safe_goal_count") != 0:
        fail(f"{label} next_safe_goal_count must be 0")
    if data.get("selected_next_safe_goal") is not None:
        fail(f"{label} selected_next_safe_goal must be null")
    for flag in FALSE_FLAGS:
        if data.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    v31 = read_json(V31 / "owner_external_validation_authorization_v31_record.json")
    if v31.get("terminal_condition") != "PROTECTED_ACTION_REQUIRED":
        fail("v31 source boundary is not PROTECTED_ACTION_REQUIRED")
    if "RESULT: PASS" not in read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_V31_VALIDATION_REPORT.md"):
        fail("accepted v31 validation report is not PASS")

    validate_record(read_json(RECORD), "v32 record")
    validate_record(read_json(APP / "product_workbench_v32_record.json"), "app record")

    scorecard = read_json(V32 / "LOCAL_PRODUCT_COMPLETION_SCORECARD.json")
    validate_record(scorecard, "scorecard")
    capability_ids = {item.get("capability_id") for item in scorecard.get("capabilities", [])}
    for capability_id in REQUIRED_CAPABILITIES:
        if capability_id not in capability_ids:
            fail(f"scorecard missing capability {capability_id}")
    if any(item.get("status") != "implemented_internal_local" for item in scorecard.get("capabilities", [])):
        fail("all scorecard capabilities must be implemented_internal_local")

    dry_run = read_json(V32 / "FIRST_REAL_GOAL_DRY_RUN_PACKET.json")
    if dry_run.get("first_real_goal_flow") != "idea_to_owner_review_packet_without_external_execution":
        fail("dry run packet flow mismatch")
    if dry_run.get("protected_action_boundary") != "external_validation_requires_owner_authorization":
        fail("dry run packet must stop at external validation boundary")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v32.png").stat().st_size < 10000:
        fail("render-check-v32.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v32.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V32",
        "Product completion scorecard ready",
        "First real goal dry run ready",
        "User operating guide ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v32.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    required_markers = [
        "terminal_condition: LOCAL_PRODUCT_COMPLETION_HARDENING_V32_READY",
        "product_completion_claim_scope: repo_local_internal_only",
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

    print("Influence Factory local product completion hardening v32 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_PRODUCT_COMPLETION_HARDENING_V32_READY")
    print("local_product_status=internal_local_product_completion_candidate")
    print("product_completion_claim_scope=repo_local_internal_only")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

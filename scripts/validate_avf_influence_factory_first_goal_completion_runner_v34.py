from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V33 = (
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
)
V34 = V33 / "first_goal_completion_runner_v34"
RECORD = V34 / "first_goal_completion_runner_v34_record.json"

REQUIRED_FILES = [
    V33 / "local_distributable_package_v33_record.json",
    V33 / "LOCAL_DISTRIBUTABLE_PACKAGE_MANIFEST.json",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_DISTRIBUTABLE_PACKAGE_V33_VALIDATION_REPORT.md",
    RECORD,
    V34 / "FIRST_GOAL_COMPLETION_RUNNER_PACKET.json",
    V34 / "FIRST_GOAL_COMPLETION_RUNNER_PACKET.md",
    V34 / "FIRST_GOAL_OWNER_READY_PACKAGE.json",
    V34 / "FIRST_GOAL_OWNER_READY_PACKAGE.md",
    V34 / "OWNER_READY_PACKAGE_INDEX.md",
    V34 / "FIRST_GOAL_STYLE_MEMORY_EXPORT.md",
    V34 / "FIRST_GOAL_CODEX_CONTEXT_PACK.md",
    V34 / "FIRST_GOAL_ONE_CLICK_RUNBOOK.md",
    V34 / "PROTECTED_BOUNDARY_RECONFIRMATION.md",
    V34 / "LOCAL_PRODUCT_COMPLETION_TERMINAL_REPORT.md",
    V34 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v34_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v34.png",
    APP / "self_test_report_v34.md",
    ROOT / "scripts" / "create_avf_influence_factory_first_goal_completion_runner_v34.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_FIRST_GOAL_COMPLETION_RUNNER_V34_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_FIRST_GOAL_COMPLETION_RUNNER_V34.md",
]

REQUIRED_OWNER_PACKAGE_SECTIONS = [
    "strategy_packet",
    "brand_ip_style_memory",
    "image_generation_reference_packet",
    "draft_content_system",
    "codex_context_pack",
    "evidence_ledger",
    "safety_review",
    "owner_decision_request",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v34",
    "First Goal Completion Runner",
    "First Goal Owner-Ready Package",
    "Owner Ready Package Index",
    "Build First Goal Owner-Ready Package",
    "runFirstGoalCompletionPackage",
    "renderFirstGoalCompletionPackage",
    "SELF_TEST_PASS_V34",
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
    print("Influence Factory first goal completion runner v34 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "FIRST_GOAL_COMPLETION_RUNNER_V34_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "first_goal_owner_ready_package_ready":
        fail(f"{label} local_product_status mismatch")
    if data.get("product_completion_claim_scope") != "repo_local_internal_only":
        fail(f"{label} product_completion_claim_scope mismatch")
    if data.get("first_goal_flow") != "idea_to_owner_ready_package_without_external_execution":
        fail(f"{label} first_goal_flow mismatch")
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

    v33 = read_json(V33 / "local_distributable_package_v33_record.json")
    if v33.get("terminal_condition") != "LOCAL_DISTRIBUTABLE_PACKAGE_V33_READY":
        fail("v33 source package record is not ready")
    if "RESULT: PASS" not in read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_DISTRIBUTABLE_PACKAGE_V33_VALIDATION_REPORT.md"):
        fail("accepted v33 validation report is not PASS")

    validate_record(read_json(RECORD), "v34 record")
    validate_record(read_json(APP / "product_workbench_v34_record.json"), "app record")
    runner = read_json(V34 / "FIRST_GOAL_COMPLETION_RUNNER_PACKET.json")
    validate_record(runner, "runner packet")
    owner_package = read_json(V34 / "FIRST_GOAL_OWNER_READY_PACKAGE.json")
    validate_record(owner_package, "owner package")
    for section in REQUIRED_OWNER_PACKAGE_SECTIONS:
        if section not in owner_package:
            fail(f"owner package missing {section}")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v34.png").stat().st_size < 10000:
        fail("render-check-v34.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v34.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V34",
        "First goal owner-ready package ready",
        "Owner ready package index ready",
        "Codex context pack ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v34.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "terminal_condition: FIRST_GOAL_COMPLETION_RUNNER_V34_READY",
        "first_goal_flow: idea_to_owner_ready_package_without_external_execution",
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
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory first goal completion runner v34 validation")
    print("RESULT: PASS")
    print("terminal_condition=FIRST_GOAL_COMPLETION_RUNNER_V34_READY")
    print("local_product_status=first_goal_owner_ready_package_ready")
    print("first_goal_flow=idea_to_owner_ready_package_without_external_execution")
    print("product_completion_claim_scope=repo_local_internal_only")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

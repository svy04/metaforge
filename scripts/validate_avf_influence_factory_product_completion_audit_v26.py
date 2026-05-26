from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V25 = (
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
)
V26 = V25 / "product_completion_audit_v26"
RECORD = V26 / "product_completion_audit_v26_record.json"

REQUIRED_FILES = [
    V25 / "local_beta_candidate_v25_record.json",
    V25 / "LOCAL_PRODUCT_BETA_CANDIDATE_PACKET.json",
    RECORD,
    V26 / "PRODUCT_COMPLETION_AUDIT_PACKET.json",
    V26 / "PRODUCT_COMPLETION_AUDIT_PACKET.md",
    V26 / "PRODUCT_REQUIREMENT_COVERAGE_MATRIX.md",
    V26 / "PRODUCT_GAP_REGISTER.md",
    V26 / "PRODUCT_COMPLETION_DECISION.md",
    V26 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v26_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v26.png",
    APP / "self_test_report_v26.md",
    ROOT / "scripts" / "create_avf_influence_factory_product_completion_audit_v26.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_COMPLETION_AUDIT_V26_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_COMPLETION_AUDIT_V26.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v26",
    "Product Completion Audit",
    "Requirement Coverage Matrix",
    "Product Gap Register",
    "Product Completion Decision",
    "Run Product Completion Audit",
    "runProductCompletionAudit",
    "renderProductCompletionAudit",
    "SELF_TEST_PASS_V26",
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

REQUIRED_REQUIREMENTS = [
    "idea_to_strategy",
    "brand_ip_style_memory",
    "draft_first_content_system",
    "codex_task_packets",
    "evidence_and_feedback_loop",
    "owner_approval_gate",
    "local_beta_candidate",
    "local_export_package",
    "external_user_validation",
    "public_release_authorization",
]

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory product completion audit v26 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "PRODUCT_COMPLETION_AUDIT_V26_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("product_completion_claimed") is not False:
        fail(f"{label} product_completion_claimed must be false")
    if data.get("selected_next_safe_goal") != "build_local_export_package_v27_without_protected_actions":
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

    v25 = read_json(V25 / "local_beta_candidate_v25_record.json")
    if v25.get("local_product_status") != "local_beta_candidate_packet_ready":
        fail("v25 local beta candidate is not ready")

    validate_record(read_json(RECORD), "v26 record")
    validate_record(read_json(APP / "product_workbench_v26_record.json"), "app record")
    packet = read_json(V26 / "PRODUCT_COMPLETION_AUDIT_PACKET.json")
    validate_record(packet, "completion audit packet")

    coverage = packet.get("requirement_coverage_matrix", [])
    coverage_ids = {item.get("requirement_id") for item in coverage}
    for requirement in REQUIRED_REQUIREMENTS:
        if requirement not in coverage_ids:
            fail(f"coverage matrix missing requirement {requirement}")
    if not any(item.get("status") == "gap_local_safe" for item in coverage):
        fail("coverage matrix must identify at least one safe local gap")
    if not any(item.get("status") == "blocked_protected_action" for item in coverage):
        fail("coverage matrix must preserve protected-action blockers")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v26.png").stat().st_size < 10000:
        fail("render-check-v26.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v26.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V26",
        "Product completion audit ready",
        "Requirement coverage matrix ready",
        "Product gap register ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v26.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "product_completion_claimed: false",
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: build_local_export_package_v27_without_protected_actions",
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

    print("Influence Factory product completion audit v26 validation")
    print("RESULT: PASS")
    print("terminal_condition=PRODUCT_COMPLETION_AUDIT_V26_READY")
    print("product_completion_claimed=false")
    print("selected_next_safe_goal=build_local_export_package_v27_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

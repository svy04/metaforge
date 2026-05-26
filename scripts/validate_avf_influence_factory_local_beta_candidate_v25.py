from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V24 = (
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
)
V25 = V24 / "local_beta_candidate_v25"
RECORD = V25 / "local_beta_candidate_v25_record.json"

REQUIRED_FILES = [
    V24 / "local_mvp_acceptance_v24_record.json",
    V24 / "LOCAL_MVP_E2E_ACCEPTANCE_PACKET.json",
    RECORD,
    V25 / "LOCAL_PRODUCT_BETA_CANDIDATE_PACKET.json",
    V25 / "LOCAL_PRODUCT_BETA_CANDIDATE_PACKET.md",
    V25 / "LOCAL_BETA_CANDIDATE_COMPLETENESS_MATRIX.md",
    V25 / "LOCAL_BETA_USER_FLOW_CHECKLIST.md",
    V25 / "LOCAL_BETA_INSTALL_AND_RUN_GUIDE.md",
    V25 / "LOCAL_BETA_BLOCKED_PUBLIC_ACTIONS.md",
    V25 / "LOCAL_BETA_OWNER_REVIEW_REQUEST.md",
    V25 / "AUTONOMOUS_CONTINUATION_TERMINAL_REPORT.md",
    APP / "product_workbench_v25_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v25.png",
    APP / "self_test_report_v25.md",
    ROOT / "scripts" / "create_avf_influence_factory_local_beta_candidate_v25.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_BETA_CANDIDATE_V25_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_BETA_CANDIDATE_V25.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v25",
    "Local Beta Candidate Packager",
    "Local Product Beta Candidate Packet",
    "Local Beta User Flow Checklist",
    "Local Beta Install And Run Guide",
    "Blocked Public Actions",
    "Prepare Local Beta Candidate",
    "prepareLocalBetaCandidate",
    "renderLocalBetaCandidate",
    "SELF_TEST_PASS_V25",
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

REQUIRED_COMPONENTS = [
    "goal_intake",
    "strategy_proof",
    "brand_ip_style_memory",
    "content_pipeline",
    "codex_packet_factory",
    "owner_acceptance",
    "safety_boundary",
    "local_run_guides",
]

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory local beta candidate v25 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "PROTECTED_ACTION_REQUIRED":
        fail(f"{label} terminal_condition must be PROTECTED_ACTION_REQUIRED")
    if data.get("local_product_status") != "local_beta_candidate_packet_ready":
        fail(f"{label} local_product_status mismatch")
    if data.get("next_blocked_action") != "owner_authorization_for_public_beta_or_external_user_validation":
        fail(f"{label} next_blocked_action mismatch")
    if data.get("next_safe_goal_count") != 0:
        fail(f"{label} next_safe_goal_count must be 0 at protected boundary")
    if data.get("selected_next_goal_executed") is not False:
        fail(f"{label} selected_next_goal_executed must be false")
    for flag in FALSE_FLAGS:
        if data.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    v24 = read_json(V24 / "local_mvp_acceptance_v24_record.json")
    if v24.get("terminal_condition") != "LOCAL_MVP_E2E_ACCEPTANCE_V24_READY":
        fail("v24 local MVP acceptance is not ready")

    validate_record(read_json(RECORD), "v25 record")
    validate_record(read_json(APP / "product_workbench_v25_record.json"), "app record")

    packet = read_json(V25 / "LOCAL_PRODUCT_BETA_CANDIDATE_PACKET.json")
    validate_record(packet, "beta candidate packet")
    components = packet.get("candidate_components", [])
    component_ids = {component.get("component_id") for component in components}
    for component in REQUIRED_COMPONENTS:
        if component not in component_ids:
            fail(f"beta candidate packet missing component {component}")
    if any(component.get("status") != "packaged_local_only" for component in components):
        fail("all beta candidate components must be packaged_local_only")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v25.png").stat().st_size < 10000:
        fail("render-check-v25.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v25.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V25",
        "Local beta candidate packet ready",
        "Install and run guide ready",
        "Protected action boundary reached",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v25.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "terminal_condition: PROTECTED_ACTION_REQUIRED",
        "protected_action_executed: false",
        "external_calls: false",
        "next_blocked_action: owner_authorization_for_public_beta_or_external_user_validation",
        "fake human impersonation",
        "undisclosed bot networks",
        "platform posting",
        "release readiness claim: blocked",
        "public readiness claim: blocked",
        "production readiness claim: blocked",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory local beta candidate v25 validation")
    print("RESULT: PASS")
    print("terminal_condition=PROTECTED_ACTION_REQUIRED")
    print("local_product_status=local_beta_candidate_packet_ready")
    print("next_blocked_action=owner_authorization_for_public_beta_or_external_user_validation")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

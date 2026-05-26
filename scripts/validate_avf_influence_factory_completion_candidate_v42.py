from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V41 = (
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
    / "local_owner_trial_script_v36"
    / "owner_trial_evidence_recorder_v37"
    / "owner_trial_evidence_capture_v38"
    / "local_iteration_from_owner_evidence_v39"
    / "applied_local_iteration_work_item_v40"
    / "applied_iteration_verification_v41"
)
V42 = V41 / "factory_completion_candidate_v42"
RECORD = V42 / "factory_completion_candidate_v42_record.json"

REQUIRED_FILES = [
    V41 / "applied_iteration_verification_v41_record.json",
    V41 / "APPLIED_ITERATION_VERIFICATION_PACKET.json",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_APPLIED_ITERATION_VERIFICATION_V41_VALIDATION_REPORT.md",
    RECORD,
    V42 / "FACTORY_COMPLETION_CANDIDATE_PACKET.json",
    V42 / "FACTORY_COMPLETION_CANDIDATE_PACKET.md",
    V42 / "FACTORY_CAPABILITY_MATRIX.md",
    V42 / "FIRST_SAFE_PRODUCT_TRACK_PACKET.json",
    V42 / "FIRST_SAFE_PRODUCT_TRACK_PACKET.md",
    V42 / "FACTORY_COMPLETION_BOUNDARY_REPORT.md",
    V42 / "OWNER_NEXT_ACTIONS.md",
    V42 / "FACTORY_FOUNDATION_READY_TERMINAL_REPORT.md",
    APP / "product_workbench_v42_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v42.png",
    APP / "self_test_report_v42.md",
    ROOT / "scripts" / "create_avf_influence_factory_completion_candidate_v42.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_COMPLETION_CANDIDATE_V42_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_COMPLETION_CANDIDATE_V42.md",
]

REQUIRED_CAPABILITIES = [
    "goal_os",
    "avf_control_plane",
    "parallel_agent_org",
    "infra_product_cell",
    "brand_ip_memory",
    "influence_factory_safe_content_system",
    "draft_first_content_pipeline",
    "codex_lane",
    "evidence_loop",
    "first_real_user_goal_intake_packet",
    "local_validation_terminal_report",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v42",
    "Factory Completion Candidate",
    "Factory Capability Matrix",
    "First Safe Product Track Packet",
    "Factory Foundation Ready Terminal Report",
    "Assemble Factory Completion Candidate",
    "runFactoryCompletionCandidate",
    "renderFactoryCompletionCandidate",
    "SELF_TEST_PASS_V42",
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
    print("Influence Factory completion candidate v42 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "FACTORY_FOUNDATION_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "factory_foundation_ready_internal_only":
        fail(f"{label} local_product_status mismatch")
    if data.get("first_goal_flow") != "repo_local_factory_foundation_and_first_safe_track_assembled":
        fail(f"{label} first_goal_flow mismatch")
    if data.get("product_completion_claim_scope") != "repo_local_internal_only":
        fail(f"{label} product_completion_claim_scope mismatch")
    if data.get("next_safe_goal_count") != 0:
        fail(f"{label} next_safe_goal_count must be 0 at terminal")
    if data.get("selected_next_safe_goal") is not None:
        fail(f"{label} selected_next_safe_goal must be null at terminal")
    for flag in FALSE_FLAGS:
        if data.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    v41 = read_json(V41 / "applied_iteration_verification_v41_record.json")
    if v41.get("terminal_condition") != "LOCAL_ITERATION_WORK_ITEM_V41_VERIFIED":
        fail("v41 source record is not verified")
    if "RESULT: PASS" not in read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_APPLIED_ITERATION_VERIFICATION_V41_VALIDATION_REPORT.md"):
        fail("accepted v41 validation report is not PASS")

    validate_record(read_json(RECORD), "v42 record")
    validate_record(read_json(APP / "product_workbench_v42_record.json"), "app record")
    packet = read_json(V42 / "FACTORY_COMPLETION_CANDIDATE_PACKET.json")
    validate_record(packet, "completion candidate packet")

    capability_ids = {item.get("capability_id") for item in packet.get("capability_matrix", [])}
    for capability in REQUIRED_CAPABILITIES:
        if capability not in capability_ids:
            fail(f"completion packet missing capability {capability}")
    if packet.get("terminal_report", {}).get("terminal_condition") != "FACTORY_FOUNDATION_READY":
        fail("terminal report must state FACTORY_FOUNDATION_READY")
    if packet.get("first_safe_product_track", {}).get("product_track") != "Transparent AI Creator Collective / Influence Factory":
        fail("first safe product track mismatch")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v42.png").stat().st_size < 10000:
        fail("render-check-v42.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v42.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V42",
        "Factory completion candidate ready",
        "First safe product track packet ready",
        "Factory foundation terminal report ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v42.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "terminal_condition: FACTORY_FOUNDATION_READY",
        "first_goal_flow: repo_local_factory_foundation_and_first_safe_track_assembled",
        "product_completion_claim_scope: repo_local_internal_only",
        "external_validation_authorized: false",
        "external_validation_executed: false",
        "external_validation_claimed: false",
        "protected_action_executed: false",
        "external_calls: false",
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

    print("Influence Factory completion candidate v42 validation")
    print("RESULT: PASS")
    print("terminal_condition=FACTORY_FOUNDATION_READY")
    print("local_product_status=factory_foundation_ready_internal_only")
    print("first_goal_flow=repo_local_factory_foundation_and_first_safe_track_assembled")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

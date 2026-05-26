from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V37 = (
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
)
V38 = V37 / "owner_trial_evidence_capture_v38"
RECORD = V38 / "owner_trial_evidence_capture_v38_record.json"

REQUIRED_FILES = [
    V37 / "owner_trial_evidence_recorder_v37_record.json",
    V37 / "OWNER_TRIAL_EVIDENCE_RECORDER_PACKET.json",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_TRIAL_EVIDENCE_RECORDER_V37_VALIDATION_REPORT.md",
    RECORD,
    V38 / "OWNER_TRIAL_EVIDENCE_CAPTURE_PACKET.json",
    V38 / "OWNER_TRIAL_EVIDENCE_CAPTURE_PACKET.md",
    V38 / "OWNER_TRIAL_EVIDENCE_CAPTURE_SCHEMA.json",
    V38 / "OWNER_TRIAL_EVIDENCE_CAPTURE_SCHEMA.md",
    V38 / "OWNER_TRIAL_LEDGER_ENTRY_TEMPLATE.json",
    V38 / "OWNER_TRIAL_LEDGER_ENTRY_TEMPLATE.md",
    V38 / "OWNER_TRIAL_NEXT_ITERATION_PACKET.md",
    V38 / "OWNER_TRIAL_CAPTURE_BOUNDARY_REPORT.md",
    APP / "product_workbench_v38_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v38.png",
    APP / "self_test_report_v38.md",
    ROOT / "scripts" / "create_avf_influence_factory_owner_trial_evidence_capture_v38.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_TRIAL_EVIDENCE_CAPTURE_V38_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_TRIAL_EVIDENCE_CAPTURE_V38.md",
]

REQUIRED_FIELDS = [
    "owner_goal_used",
    "trial_completed_locally",
    "missing_inputs_found",
    "recovery_prompt_quality",
    "owner_ready_package_clarity",
    "brand_ip_style_memory_clarity",
    "image_reference_packet_clarity",
    "content_packet_clarity",
    "codex_packet_clarity",
    "safety_boundary_confidence",
    "friction_notes",
    "selected_next_local_improvement",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v38",
    "Owner Trial Evidence Capture",
    "Owner Trial Ledger Entry",
    "Next Local Iteration Packet",
    "Capture Owner Trial Evidence",
    "runOwnerTrialEvidenceCapture",
    "renderOwnerTrialEvidenceCapture",
    "SELF_TEST_PASS_V38",
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
    print("Influence Factory owner trial evidence capture v38 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "OWNER_TRIAL_EVIDENCE_CAPTURE_V38_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "owner_trial_evidence_capture_ready":
        fail(f"{label} local_product_status mismatch")
    if data.get("first_goal_flow") != "owner_trial_evidence_recorder_to_captured_local_ledger":
        fail(f"{label} first_goal_flow mismatch")
    if data.get("product_completion_claim_scope") != "repo_local_internal_only":
        fail(f"{label} product_completion_claim_scope mismatch")
    if data.get("selected_next_safe_goal") != "create_local_iteration_from_owner_trial_evidence_v39":
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

    v37 = read_json(V37 / "owner_trial_evidence_recorder_v37_record.json")
    if v37.get("terminal_condition") != "OWNER_TRIAL_EVIDENCE_RECORDER_V37_READY":
        fail("v37 source record is not ready")
    if "RESULT: PASS" not in read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_TRIAL_EVIDENCE_RECORDER_V37_VALIDATION_REPORT.md"):
        fail("accepted v37 validation report is not PASS")

    validate_record(read_json(RECORD), "v38 record")
    validate_record(read_json(APP / "product_workbench_v38_record.json"), "app record")
    packet = read_json(V38 / "OWNER_TRIAL_EVIDENCE_CAPTURE_PACKET.json")
    validate_record(packet, "capture packet")

    field_ids = {field.get("field_id") for field in packet.get("capture_fields", [])}
    for field_id in REQUIRED_FIELDS:
        if field_id not in field_ids:
            fail(f"capture packet missing field {field_id}")
    if not packet.get("ledger_entry_template"):
        fail("ledger_entry_template must be present")
    if not packet.get("next_iteration_packet_template"):
        fail("next_iteration_packet_template must be present")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v38.png").stat().st_size < 10000:
        fail("render-check-v38.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v38.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V38",
        "Owner trial evidence capture ready",
        "Owner trial ledger entry ready",
        "Next local iteration packet ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v38.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "terminal_condition: OWNER_TRIAL_EVIDENCE_CAPTURE_V38_READY",
        "first_goal_flow: owner_trial_evidence_recorder_to_captured_local_ledger",
        "product_completion_claim_scope: repo_local_internal_only",
        "external_validation_authorized: false",
        "external_validation_executed: false",
        "external_validation_claimed: false",
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: create_local_iteration_from_owner_trial_evidence_v39",
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

    print("Influence Factory owner trial evidence capture v38 validation")
    print("RESULT: PASS")
    print("terminal_condition=OWNER_TRIAL_EVIDENCE_CAPTURE_V38_READY")
    print("local_product_status=owner_trial_evidence_capture_ready")
    print("first_goal_flow=owner_trial_evidence_recorder_to_captured_local_ledger")
    print("selected_next_safe_goal=create_local_iteration_from_owner_trial_evidence_v39")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

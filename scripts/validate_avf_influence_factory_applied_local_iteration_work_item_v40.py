from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V39 = (
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
)
V40 = V39 / "applied_local_iteration_work_item_v40"
RECORD = V40 / "applied_local_iteration_work_item_v40_record.json"

REQUIRED_FILES = [
    V39 / "local_iteration_from_owner_evidence_v39_record.json",
    V39 / "OWNER_EVIDENCE_LOCAL_ITERATION_PACKET.json",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39_VALIDATION_REPORT.md",
    RECORD,
    V40 / "APPLIED_LOCAL_ITERATION_PACKET.json",
    V40 / "APPLIED_LOCAL_ITERATION_PACKET.md",
    V40 / "APPLIED_WORK_ITEM_RESULT.md",
    V40 / "STYLE_MEMORY_ATTACHMENT_CHECKLIST.md",
    V40 / "SAFETY_BOUND_CODEX_PACKET.json",
    V40 / "SAFETY_BOUND_CODEX_PACKET.md",
    V40 / "LOCAL_ITERATION_RESULT_LEDGER.md",
    V40 / "LOCAL_ITERATION_V40_BOUNDARY_REPORT.md",
    APP / "product_workbench_v40_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v40.png",
    APP / "self_test_report_v40.md",
    ROOT / "scripts" / "create_avf_influence_factory_applied_local_iteration_work_item_v40.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_APPLIED_LOCAL_ITERATION_WORK_ITEM_V40_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_APPLIED_LOCAL_ITERATION_WORK_ITEM_V40.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v40",
    "Applied Local Iteration Work Item",
    "Style Memory Attachment Checklist",
    "Safety-Bound Codex Packet",
    "Apply Local Iteration Work Item",
    "runAppliedLocalIterationWorkItem",
    "renderAppliedLocalIterationWorkItem",
    "SELF_TEST_PASS_V40",
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
    print("Influence Factory applied local iteration work item v40 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "LOCAL_ITERATION_WORK_ITEM_V40_APPLIED":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "local_iteration_work_item_applied":
        fail(f"{label} local_product_status mismatch")
    if data.get("first_goal_flow") != "pr_sized_owner_evidence_iteration_applied_locally":
        fail(f"{label} first_goal_flow mismatch")
    if data.get("product_completion_claim_scope") != "repo_local_internal_only":
        fail(f"{label} product_completion_claim_scope mismatch")
    if data.get("selected_next_safe_goal") != "verify_applied_local_iteration_v41_without_protected_actions":
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

    v39 = read_json(V39 / "local_iteration_from_owner_evidence_v39_record.json")
    if v39.get("terminal_condition") != "LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39_READY":
        fail("v39 source record is not ready")
    if "RESULT: PASS" not in read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39_VALIDATION_REPORT.md"):
        fail("accepted v39 validation report is not PASS")

    validate_record(read_json(RECORD), "v40 record")
    validate_record(read_json(APP / "product_workbench_v40_record.json"), "app record")
    packet = read_json(V40 / "APPLIED_LOCAL_ITERATION_PACKET.json")
    validate_record(packet, "applied iteration packet")

    result = packet.get("applied_work_item_result", {})
    if result.get("work_item_id") != "tighten_owner_trial_capture_flow":
        fail("applied_work_item_result must apply tighten_owner_trial_capture_flow")
    if result.get("protected_action_executed") is not False:
        fail("applied work item must not execute protected action")
    if len(packet.get("style_memory_attachment_checklist", [])) < 5:
        fail("style memory attachment checklist is incomplete")
    codex_packet = packet.get("safety_bound_codex_packet", {})
    if "forbidden_changes" not in codex_packet:
        fail("safety_bound_codex_packet must include forbidden_changes")
    for phrase in ["Do not deploy", "Do not publish", "Do not call providers or live models", "Do not support deceptive influence"]:
        if phrase not in "\n".join(codex_packet.get("forbidden_changes", [])):
            fail(f"safety_bound_codex_packet missing {phrase}")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v40.png").stat().st_size < 10000:
        fail("render-check-v40.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v40.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V40",
        "Applied local iteration work item ready",
        "Style memory attachment ready",
        "Safety-bound Codex packet ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v40.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "terminal_condition: LOCAL_ITERATION_WORK_ITEM_V40_APPLIED",
        "first_goal_flow: pr_sized_owner_evidence_iteration_applied_locally",
        "product_completion_claim_scope: repo_local_internal_only",
        "external_validation_authorized: false",
        "external_validation_executed: false",
        "external_validation_claimed: false",
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: verify_applied_local_iteration_v41_without_protected_actions",
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

    print("Influence Factory applied local iteration work item v40 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_ITERATION_WORK_ITEM_V40_APPLIED")
    print("local_product_status=local_iteration_work_item_applied")
    print("first_goal_flow=pr_sized_owner_evidence_iteration_applied_locally")
    print("selected_next_safe_goal=verify_applied_local_iteration_v41_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

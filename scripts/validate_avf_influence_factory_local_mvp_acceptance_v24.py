from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V22 = (
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
)
V23 = V22 / "mvp_work_items_v23"
V24 = V23 / "local_mvp_acceptance_v24"
RECORD = V24 / "local_mvp_acceptance_v24_record.json"

REQUIRED_FILES = [
    V23 / "mvp_work_items_v23_record.json",
    V23 / "IMPLEMENTED_MVP_WORK_ITEMS.json",
    RECORD,
    V24 / "LOCAL_MVP_E2E_ACCEPTANCE_PACKET.json",
    V24 / "LOCAL_MVP_E2E_ACCEPTANCE_PACKET.md",
    V24 / "LOCAL_MVP_E2E_ACCEPTANCE_MATRIX.md",
    V24 / "LOCAL_MVP_E2E_RUN_TRACE.json",
    V24 / "LOCAL_MVP_E2E_RUN_TRACE.md",
    V24 / "LOCAL_MVP_OWNER_ACCEPTANCE_DECISION.md",
    V24 / "LOCAL_MVP_PROTECTED_ACTION_BOUNDARY.md",
    V24 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v24_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v24.png",
    APP / "self_test_report_v24.md",
    ROOT / "scripts" / "create_avf_influence_factory_local_mvp_acceptance_v24.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_MVP_ACCEPTANCE_V24_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_MVP_ACCEPTANCE_V24.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v24",
    "Local MVP Acceptance Runner",
    "End-to-End Acceptance Packet",
    "Local MVP E2E Run Trace",
    "Owner Acceptance Decision",
    "Run Local MVP Acceptance",
    "runLocalMvpAcceptance",
    "renderLocalMvpAcceptance",
    "SELF_TEST_PASS_V24",
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

REQUIRED_STAGES = [
    "goal_intake",
    "strategy_proof",
    "brand_ip_style",
    "content_calendar",
    "codex_pr_sequence",
    "owner_acceptance",
    "protected_boundary",
]

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory local MVP acceptance v24 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "LOCAL_MVP_E2E_ACCEPTANCE_V24_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("selected_next_safe_goal") != "prepare_local_product_beta_candidate_v25_without_protected_actions":
        fail(f"{label} selected_next_safe_goal mismatch")
    if data.get("next_safe_goal_count") != 1:
        fail(f"{label} next_safe_goal_count must be 1")
    if data.get("selected_next_goal_executed") is not False:
        fail(f"{label} selected_next_goal_executed must be false")
    for flag in FALSE_FLAGS:
        if data.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    v23 = read_json(V23 / "mvp_work_items_v23_record.json")
    if v23.get("terminal_condition") != "LOCAL_MVP_WORK_ITEMS_V23_READY":
        fail("v23 MVP work items are not ready")

    validate_record(read_json(RECORD), "v24 record")
    validate_record(read_json(APP / "product_workbench_v24_record.json"), "app record")

    packet = read_json(V24 / "LOCAL_MVP_E2E_ACCEPTANCE_PACKET.json")
    validate_record(packet, "acceptance packet")
    stages = packet.get("acceptance_matrix", [])
    stage_ids = {stage.get("stage_id") for stage in stages}
    for stage in REQUIRED_STAGES:
        if stage not in stage_ids:
            fail(f"acceptance matrix missing stage {stage}")
    if any(stage.get("status") != "pass_local" for stage in stages):
        fail("all acceptance matrix stages must be pass_local")

    trace = read_json(V24 / "LOCAL_MVP_E2E_RUN_TRACE.json")
    trace_steps = trace.get("trace_steps", [])
    if len(trace_steps) < len(REQUIRED_STAGES):
        fail("run trace must include every E2E stage")
    if any(step.get("status") != "pass_local" for step in trace_steps):
        fail("all run trace steps must be pass_local")
    for stage in REQUIRED_STAGES:
        if stage not in {step.get("stage_id") for step in trace_steps}:
            fail(f"run trace missing stage {stage}")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v24.png").stat().st_size < 10000:
        fail("render-check-v24.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v24.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V24",
        "Local MVP acceptance packet ready",
        "E2E run trace ready",
        "Owner acceptance decision ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v24.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: prepare_local_product_beta_candidate_v25_without_protected_actions",
        "selected_next_goal_executed: false",
        "fake human impersonation",
        "undisclosed bot networks",
        "platform posting",
        "LOCAL_MVP_E2E_ACCEPTANCE_V24_READY",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory local MVP acceptance v24 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_MVP_E2E_ACCEPTANCE_V24_READY")
    print("selected_next_safe_goal=prepare_local_product_beta_candidate_v25_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

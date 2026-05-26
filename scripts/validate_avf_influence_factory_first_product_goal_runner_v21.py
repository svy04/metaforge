from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V20 = (
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
)
V21 = V20 / "first_product_goal_runner_v21"
RECORD = V21 / "first_product_goal_runner_v21_record.json"

REQUIRED_FILES = [
    V20 / "local_operating_loop_templates_v20_record.json",
    V20 / "FIRST_OWNER_PRODUCT_GOAL_INTAKE_TEMPLATE.json",
    RECORD,
    V21 / "FIRST_PRODUCT_GOAL_INPUT.example.json",
    V21 / "FIRST_PRODUCT_GOAL_RUN_PACKET.json",
    V21 / "FIRST_PRODUCT_GOAL_RUN_PACKET.md",
    V21 / "FIRST_PRODUCT_STRATEGY_BRIEF.md",
    V21 / "FIRST_PRODUCT_BRAND_IP_BRIEF.md",
    V21 / "FIRST_PRODUCT_CONTENT_SYSTEM_BRIEF.md",
    V21 / "FIRST_PRODUCT_CODEX_TASK_PACKET.json",
    V21 / "FIRST_PRODUCT_EVIDENCE_LEDGER.md",
    V21 / "FIRST_PRODUCT_OWNER_REVIEW_QUEUE.md",
    V21 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v21_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v21.png",
    APP / "self_test_report_v21.md",
    ROOT / "scripts" / "create_avf_influence_factory_first_product_goal_runner_v21.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_FIRST_PRODUCT_GOAL_RUNNER_V21_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_FIRST_PRODUCT_GOAL_RUNNER_V21.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v21",
    "First Product Goal Runner",
    "Run First Product Goal",
    "First Product Goal Run Packet",
    "First Product Codex Task Packet",
    "First Product Owner Review Queue",
    "runFirstProductGoal",
    "renderFirstProductGoalRunner",
    "SELF_TEST_PASS_V21",
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

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory first product goal runner v21 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "FIRST_PRODUCT_GOAL_RUNNER_V21_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("selected_next_safe_goal") != "owner_runs_first_real_product_goal_or_refines_goal_input":
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

    v20 = read_json(V20 / "local_operating_loop_templates_v20_record.json")
    if v20.get("terminal_condition") != "FACTORY_READY_FOR_FIRST_OWNER_PRODUCT_GOAL":
        fail("v20 factory ready state is not present")

    validate_record(read_json(RECORD), "v21 record")
    validate_record(read_json(APP / "product_workbench_v21_record.json"), "app record")

    packet = read_json(V21 / "FIRST_PRODUCT_GOAL_RUN_PACKET.json")
    for field in ["product_idea", "target_user", "proof_target", "brand_ip_constraints", "strategy_brief", "codex_task_packet"]:
        if field not in packet:
            fail(f"run packet missing {field}")
    if packet.get("safe_reframe") != "transparent_creator_brand_media_growth_system":
        fail("run packet must preserve safe product framing")
    if packet.get("protected_action_executed") is not False:
        fail("run packet must keep protected_action_executed false")

    codex_packet = read_json(V21 / "FIRST_PRODUCT_CODEX_TASK_PACKET.json")
    for field in ["task_id", "goal", "context", "acceptance_criteria", "forbidden_changes", "validation"]:
        if field not in codex_packet:
            fail(f"codex task packet missing {field}")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v21.png").stat().st_size < 10000:
        fail("render-check-v21.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v21.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V21",
        "First product goal run packet ready",
        "Codex task packet ready",
        "Owner review queue ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v21.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: owner_runs_first_real_product_goal_or_refines_goal_input",
        "selected_next_goal_executed: false",
        "fake human impersonation",
        "undisclosed bot networks",
        "platform posting",
        "FIRST_PRODUCT_GOAL_RUNNER_V21_READY",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory first product goal runner v21 validation")
    print("RESULT: PASS")
    print("terminal_condition=FIRST_PRODUCT_GOAL_RUNNER_V21_READY")
    print("selected_next_safe_goal=owner_runs_first_real_product_goal_or_refines_goal_input")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

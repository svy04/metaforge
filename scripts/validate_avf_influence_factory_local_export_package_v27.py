from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V26 = (
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
)
V27 = V26 / "local_export_package_v27"
RECORD = V27 / "local_export_package_v27_record.json"

REQUIRED_FILES = [
    V26 / "product_completion_audit_v26_record.json",
    V26 / "PRODUCT_COMPLETION_AUDIT_PACKET.json",
    RECORD,
    V27 / "LOCAL_EXPORT_PACKAGE.json",
    V27 / "LOCAL_EXPORT_PACKAGE.md",
    V27 / "LOCAL_EXPORT_MANIFEST.md",
    V27 / "LOCAL_EXPORT_CHECKSUM_MANIFEST.json",
    V27 / "OWNER_HANDOFF_README.md",
    V27 / "COPY_READY_OWNER_BRIEF.md",
    V27 / "NEXT_SAFE_GOAL.md",
    APP / "product_workbench_v27_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v27.png",
    APP / "self_test_report_v27.md",
    ROOT / "scripts" / "create_avf_influence_factory_local_export_package_v27.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_EXPORT_PACKAGE_V27_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_EXPORT_PACKAGE_V27.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v27",
    "Local Export Package Builder",
    "Local Export Package",
    "Local Export Manifest",
    "Owner Handoff README",
    "Copy-ready Owner Brief",
    "Build Local Export Package",
    "buildLocalExportPackage",
    "renderLocalExportPackage",
    "SELF_TEST_PASS_V27",
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

REQUIRED_EXPORT_ITEMS = [
    "product_app",
    "goal_artifacts",
    "validation_reports",
    "owner_handoff",
    "safety_boundaries",
    "next_authorization_request",
]

FORBIDDEN_APP_MARKERS = ["fetch(", "XMLHttpRequest", "navigator.sendBeacon", "http://", "https://", "import("]


def fail(message: str) -> None:
    print("Influence Factory local export package v27 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "LOCAL_EXPORT_PACKAGE_V27_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "local_export_package_ready":
        fail(f"{label} local_product_status mismatch")
    if data.get("local_completion_packet_created") is not True:
        fail(f"{label} local_completion_packet_created must be true")
    if data.get("public_or_release_completion_claimed") is not False:
        fail(f"{label} public_or_release_completion_claimed must be false")
    if data.get("next_blocked_action") != "owner_authorization_for_public_beta_or_external_user_validation":
        fail(f"{label} next_blocked_action mismatch")
    if data.get("next_safe_goal_count") != 0:
        fail(f"{label} next_safe_goal_count must be 0")
    for flag in FALSE_FLAGS:
        if data.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    v26 = read_json(V26 / "product_completion_audit_v26_record.json")
    if v26.get("terminal_condition") != "PRODUCT_COMPLETION_AUDIT_V26_READY":
        fail("v26 product completion audit is not ready")

    validate_record(read_json(RECORD), "v27 record")
    validate_record(read_json(APP / "product_workbench_v27_record.json"), "app record")
    package = read_json(V27 / "LOCAL_EXPORT_PACKAGE.json")
    validate_record(package, "local export package")
    export_ids = {item.get("item_id") for item in package.get("export_items", [])}
    for item in REQUIRED_EXPORT_ITEMS:
        if item not in export_ids:
            fail(f"local export package missing item {item}")

    checksums = read_json(V27 / "LOCAL_EXPORT_CHECKSUM_MANIFEST.json")
    if len(checksums.get("checksums", [])) < len(REQUIRED_EXPORT_ITEMS):
        fail("checksum manifest must include export items")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v27.png").stat().st_size < 10000:
        fail("render-check-v27.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v27.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V27",
        "Local export package ready",
        "Owner handoff README ready",
        "Copy-ready owner brief ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v27.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "local_completion_packet_created: true",
        "public_or_release_completion_claimed: false",
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

    print("Influence Factory local export package v27 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_EXPORT_PACKAGE_V27_READY")
    print("local_product_status=local_export_package_ready")
    print("local_completion_packet_created=true")
    print("public_or_release_completion_claimed=false")
    print("next_blocked_action=owner_authorization_for_public_beta_or_external_user_validation")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

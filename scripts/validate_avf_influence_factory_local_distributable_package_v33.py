from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V32 = (
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
)
V33 = V32 / "local_distributable_package_v33"
RECORD = V33 / "local_distributable_package_v33_record.json"
ZIP_PATH = V33 / "influence_factory_local_completion_package_v33.zip"

REQUIRED_FILES = [
    V32 / "local_product_completion_hardening_v32_record.json",
    V32 / "LOCAL_PRODUCT_COMPLETION_SCORECARD.json",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_PRODUCT_COMPLETION_HARDENING_V32_VALIDATION_REPORT.md",
    RECORD,
    V33 / "LOCAL_DISTRIBUTABLE_PACKAGE_MANIFEST.json",
    V33 / "LOCAL_DISTRIBUTABLE_PACKAGE_MANIFEST.md",
    V33 / "LOCAL_DISTRIBUTABLE_QUICKSTART.md",
    V33 / "LOCAL_COMPLETION_CAPSULE.md",
    V33 / "PACKAGE_INTEGRITY_REPORT.md",
    V33 / "PROTECTED_ACTION_BOUNDARY_REPORT.md",
    V33 / "NEXT_SAFE_GOAL.md",
    ZIP_PATH,
    APP / "product_workbench_v33_record.json",
    APP / "index.html",
    APP / "app.js",
    APP / "render-check-v33.png",
    APP / "self_test_report_v33.md",
    ROOT / "scripts" / "create_avf_influence_factory_local_distributable_package_v33.py",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_DISTRIBUTABLE_PACKAGE_V33_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_DISTRIBUTABLE_PACKAGE_V33.md",
]

REQUIRED_ZIP_ENTRIES = [
    "product_app/index.html",
    "product_app/app.js",
    "product_app/styles.css",
    "product_app/README.md",
    "product_app/PRODUCT_MANUAL.md",
    "LOCAL_DISTRIBUTABLE_QUICKSTART.md",
    "LOCAL_COMPLETION_CAPSULE.md",
    "LOCAL_PRODUCT_COMPLETION_SCORECARD.md",
    "FIRST_REAL_GOAL_DRY_RUN_PACKET.md",
    "PROTECTED_BOUNDARY_RECONFIRMATION.md",
]

REQUIRED_APP_MARKERS = [
    "Repo-local product workbench v33",
    "Local Distributable Package",
    "Local Completion Capsule",
    "Package Integrity Report",
    "Build Local Distributable Package View",
    "buildLocalDistributablePackageView",
    "renderLocalDistributablePackage",
    "SELF_TEST_PASS_V33",
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
    print("Influence Factory local distributable package v33 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_record(data: dict, label: str) -> None:
    if data.get("terminal_condition") != "LOCAL_DISTRIBUTABLE_PACKAGE_V33_READY":
        fail(f"{label} terminal_condition mismatch")
    if data.get("local_product_status") != "repo_local_distributable_package_ready":
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

    v32 = read_json(V32 / "local_product_completion_hardening_v32_record.json")
    if v32.get("terminal_condition") != "LOCAL_PRODUCT_COMPLETION_HARDENING_V32_READY":
        fail("v32 source hardening record is not ready")
    if "RESULT: PASS" not in read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_LOCAL_PRODUCT_COMPLETION_HARDENING_V32_VALIDATION_REPORT.md"):
        fail("accepted v32 validation report is not PASS")

    validate_record(read_json(RECORD), "v33 record")
    validate_record(read_json(APP / "product_workbench_v33_record.json"), "app record")
    manifest = read_json(V33 / "LOCAL_DISTRIBUTABLE_PACKAGE_MANIFEST.json")
    validate_record(manifest, "manifest")
    if manifest.get("zip_sha256") != sha256(ZIP_PATH):
        fail("zip sha256 does not match manifest")
    if manifest.get("zip_bytes") != ZIP_PATH.stat().st_size:
        fail("zip byte size does not match manifest")

    with zipfile.ZipFile(ZIP_PATH, "r") as package:
        names = set(package.namelist())
    for entry in REQUIRED_ZIP_ENTRIES:
        if entry not in names:
            fail(f"zip missing entry {entry}")

    html = read(APP / "index.html")
    js = read(APP / "app.js")
    for marker in REQUIRED_APP_MARKERS:
        if marker not in html and marker not in js:
            fail(f"app missing marker {marker}")
    forbidden = [marker for marker in FORBIDDEN_APP_MARKERS if marker in html or marker in js]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    if (APP / "render-check-v33.png").stat().st_size < 10000:
        fail("render-check-v33.png is too small to prove non-empty render")

    self_test = read(APP / "self_test_report_v33.md")
    for phrase in [
        "Chrome headless",
        "JavaScript syntax check PASS",
        "SELF_TEST_PASS_V33",
        "Local distributable package ready",
        "Local completion capsule ready",
        "Package integrity report ready",
    ]:
        if phrase not in self_test:
            fail(f"self_test_report_v33.md missing {phrase}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "terminal_condition: LOCAL_DISTRIBUTABLE_PACKAGE_V33_READY",
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

    print("Influence Factory local distributable package v33 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_DISTRIBUTABLE_PACKAGE_V33_READY")
    print("local_product_status=repo_local_distributable_package_ready")
    print("product_completion_claim_scope=repo_local_internal_only")
    print(f"zip_bytes={ZIP_PATH.stat().st_size}")
    print(f"zip_sha256={sha256(ZIP_PATH)}")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

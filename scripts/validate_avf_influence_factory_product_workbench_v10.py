from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "avf" / "influence_factory" / "product_app"
FIXTURE_OUT = ROOT / "_fixtures" / "avf_influence_factory_v10_validation_bundle"
RECORD_PATH = APP_DIR / "product_workbench_v10_record.json"

REQUIRED_FILES = [
    "avf/influence_factory/product_app/product_workbench_v10_record.json",
    "avf/influence_factory/product_app/index.html",
    "avf/influence_factory/product_app/styles.css",
    "avf/influence_factory/product_app/app.js",
    "avf/influence_factory/product_app/README.md",
    "avf/influence_factory/product_app/demo_goal_input_v10.json",
    "avf/influence_factory/product_app/render-check-v10.png",
    "avf/influence_factory/product_app/self-test-v10-dom.html",
    "avf/influence_factory/product_app/self_test_report_v10.md",
    "scripts/run_avf_influence_factory_goal_local.py",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V10_COMPLETION_AUDIT.md",
    "docs/goals/INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V10_TERMINAL_REPORT.md",
    "docs/goals/NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V10.md",
]

REQUIRED_BUNDLE_FILES = [
    "run_manifest.json",
    "product_brief.md",
    "strategy_brief.md",
    "brand_ip_brief.md",
    "content_pack.md",
    "image_prompt_pack.md",
    "codex_task_packet.json",
    "safety_report.md",
    "quality_gate.json",
    "next_actions.md",
    "dossier.md",
]

REQUIRED_HTML = [
    "Artifact Bundle Runner",
    "Local Goal Input",
    "Generated File Manifest",
    "Run Archive",
    "Build Artifact Bundle",
    "Load Demo Goal Input",
    "Local Goal Runner Command",
]

REQUIRED_JS = [
    "loadDemoGoalInput",
    "buildArtifactBundle",
    "buildGeneratedFileManifest",
    "recordRunArchive",
    "renderArtifactBundle",
    "renderGeneratedFileManifest",
    "renderRunArchive",
    "artifactBundle",
    "generatedFileManifest",
    "runArchive",
]

FORBIDDEN_APP_MARKERS = [
    "fetch(",
    "XMLHttpRequest",
    "navigator.sendBeacon",
    "http://",
    "https://",
    "import(",
]

FALSE_FLAGS = [
    "openclaude_required",
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "dependency_install_performed",
    "deploy_performed",
    "publish_performed",
    "platform_posting_performed",
    "personal_account_automation_performed",
    "deceptive_influence_supported",
    "release_readiness_claimed",
    "public_readiness_claimed",
    "production_readiness_claimed",
    "external_validation_claimed",
    "autonomous_reliability_claimed",
]


def fail(message: str) -> None:
    print("AVF Influence Factory product workbench v10 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    record = json.loads(read(RECORD_PATH))
    if record.get("terminal_condition") != "LOCAL_PRODUCT_WORKBENCH_V10_READY":
        fail("terminal_condition must be LOCAL_PRODUCT_WORKBENCH_V10_READY")
    if record.get("local_product_status") != "artifact_generating_local_factory_product":
        fail("local_product_status must be artifact_generating_local_factory_product")
    if record.get("selected_next_safe_goal") != "owner_runs_real_goal_bundle_or_authorizes_protected_public_operation":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    html = read(APP_DIR / "index.html")
    missing_html = [phrase for phrase in REQUIRED_HTML if phrase not in html]
    if missing_html:
        fail("index.html missing artifact product sections:\n" + "\n".join(missing_html))

    js = read(APP_DIR / "app.js")
    missing_js = [phrase for phrase in REQUIRED_JS if phrase not in js]
    if missing_js:
        fail("app.js missing artifact product behavior:\n" + "\n".join(missing_js))

    forbidden = [phrase for phrase in FORBIDDEN_APP_MARKERS if phrase in js or phrase in html]
    if forbidden:
        fail("App contains forbidden external-call marker:\n" + "\n".join(forbidden))

    demo_goal = json.loads(read(APP_DIR / "demo_goal_input_v10.json"))
    if demo_goal.get("goal_id") != "demo-transparent-creator-factory-v10":
        fail("demo goal id mismatch")

    if FIXTURE_OUT.exists():
        shutil.rmtree(FIXTURE_OUT)
    runner = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_avf_influence_factory_goal_local.py"),
            "--input",
            str(APP_DIR / "demo_goal_input_v10.json"),
            "--out",
            str(FIXTURE_OUT),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if runner.returncode != 0:
        fail("local goal runner failed:\n" + runner.stdout + runner.stderr)
    if "LOCAL_GOAL_RUNNER=PASS" not in runner.stdout:
        fail("local goal runner did not print PASS")
    missing_bundle = [name for name in REQUIRED_BUNDLE_FILES if not (FIXTURE_OUT / name).is_file()]
    if missing_bundle:
        fail("Generated bundle missing files:\n" + "\n".join(missing_bundle))

    manifest = json.loads(read(FIXTURE_OUT / "run_manifest.json"))
    quality = json.loads(read(FIXTURE_OUT / "quality_gate.json"))
    codex = json.loads(read(FIXTURE_OUT / "codex_task_packet.json"))
    if manifest.get("protected_action_executed") is not False:
        fail("generated manifest must keep protected_action_executed=false")
    if quality.get("release_ready") is not False or quality.get("public_ready") is not False:
        fail("quality gate must not claim release/public readiness")
    if "forbidden_changes" not in codex:
        fail("codex task packet missing forbidden_changes")
    if "Protected action boundary preserved" not in read(FIXTURE_OUT / "dossier.md"):
        fail("dossier missing protected boundary")

    audit = read(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V10_COMPLETION_AUDIT.md")
    if audit.count("status: PROVEN") < 130:
        fail("V10 completion audit must include at least 130 PROVEN requirements")
    if "status: MISSING" in audit or "status: UNVERIFIED" in audit:
        fail("V10 completion audit contains missing or unverified status")

    screenshot_size = (APP_DIR / "render-check-v10.png").stat().st_size
    if screenshot_size < 10000:
        fail("render-check-v10.png is too small to prove a non-empty render")

    self_test_dom = read(APP_DIR / "self-test-v10-dom.html")
    for phrase in [
        "SELF_TEST_PASS_V10",
        "Demo goal input loaded",
        "Artifact bundle built",
        "Generated file manifest ready",
        "Run archive recorded",
    ]:
        if phrase not in self_test_dom:
            fail(f"self-test DOM missing {phrase}")

    self_test_report = read(APP_DIR / "self_test_report_v10.md")
    for phrase in ["Chrome headless", "SELF_TEST_PASS_V10", "render-check-v10.png"]:
        if phrase not in self_test_report:
            fail(f"self_test_report_v10.md missing {phrase}")

    next_text = read(ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V10.md")
    if next_text.count("selected_next_safe_goal: owner_runs_real_goal_bundle_or_authorizes_protected_public_operation") != 1:
        fail("V10 next goal must be exactly one")

    print("AVF Influence Factory product workbench v10 validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V10_READY")
    print("local_product_status=artifact_generating_local_factory_product")
    print("selected_next_safe_goal=owner_runs_real_goal_bundle_or_authorizes_protected_public_operation")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")
    print("self_test=PASS")


if __name__ == "__main__":
    main()

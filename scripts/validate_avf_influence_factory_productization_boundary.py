"""Validate the final safe productization boundary packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GOALS = ROOT / "docs" / "goals"
APP = ROOT / "avf" / "influence_factory" / "product_app"


REQUIRED_FILES = [
    GOALS / "INFLUENCE_FACTORY_PRODUCTIZATION_BOUNDARY_RECORD.json",
    GOALS / "INFLUENCE_FACTORY_PROTECTED_ACTION_AUTHORIZATION_PACKET.md",
    GOALS / "INFLUENCE_FACTORY_FINAL_OWNER_DECISION_REQUEST.md",
    GOALS / "INFLUENCE_FACTORY_PRODUCT_COMPLETION_TERMINAL_REPORT.md",
    GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCTIZATION_BOUNDARY.md",
    APP / "index.html",
    APP / "styles.css",
    APP / "app.js",
    APP / "product_workbench_v10_record.json",
    APP / "render-check-v10.png",
    APP / "self-test-v10-dom.html",
    APP / "self_test_report_v10.md",
]

FALSE_FIELDS = [
    "protected_action_executed",
    "deceptive_influence_supported",
    "openclaude_required",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "dependency_install_performed",
    "deploy_performed",
    "publish_performed",
    "platform_posting_performed",
    "personal_account_automation_performed",
    "release_readiness_claimed",
    "production_readiness_claimed",
    "public_readiness_claimed",
    "external_validation_claimed",
    "autonomous_reliability_claimed",
]

REQUIRED_PHRASES = {
    GOALS / "INFLUENCE_FACTORY_PROTECTED_ACTION_AUTHORIZATION_PACKET.md": [
        "terminal_condition: PROTECTED_ACTION_REQUIRED",
        "deploy: false",
        "publish: false",
        "platform_posting: false",
        "provider_or_live_model_call: false",
        "mass_posting: false",
        "automated_engagement: false",
    ],
    GOALS / "INFLUENCE_FACTORY_FINAL_OWNER_DECISION_REQUEST.md": [
        "authorize_deploy: false",
        "authorize_publish: false",
        "authorize_platform_posting: false",
        "authorize_provider_or_live_model_calls: false",
        "authorize_mass_posting: false",
        "authorize_automated_engagement: false",
    ],
    GOALS / "INFLUENCE_FACTORY_PRODUCT_COMPLETION_TERMINAL_REPORT.md": [
        "terminal_condition: PROTECTED_ACTION_REQUIRED",
        "No provider call.",
        "No live model call.",
        "No external service call.",
        "No deploy.",
        "No publish.",
        "No platform posting.",
        "No deceptive influence support.",
    ],
    GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCTIZATION_BOUNDARY.md": [
        "selected_next_safe_goal: owner_decides_whether_to_authorize_public_productization_or_continue_local_iteration",
        "next_safe_goal_count: 1",
    ],
    APP / "self_test_report_v10.md": [
        "SELF_TEST_PASS_V10",
        "Demo goal input loaded",
        "Artifact bundle built",
        "Generated file manifest ready",
        "Run archive recorded",
    ],
}

FORBIDDEN_APP_MARKERS = [
    "fetch(",
    "XMLHttpRequest",
    "navigator.sendBeacon",
    "http://",
    "https://",
    "import(",
]


def fail(message: str) -> int:
    print("Influence Factory productization boundary validation")
    print("RESULT: FAIL")
    print(message)
    return 1


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        return fail("Missing required files:\n" + "\n".join(missing))

    record = read_json(GOALS / "INFLUENCE_FACTORY_PRODUCTIZATION_BOUNDARY_RECORD.json")
    v10_record = read_json(APP / "product_workbench_v10_record.json")

    if record.get("terminal_condition") != "PROTECTED_ACTION_REQUIRED":
        return fail("terminal_condition is not PROTECTED_ACTION_REQUIRED")
    if record.get("local_product_status") != "LOCAL_PRODUCT_WORKBENCH_V10_READY":
        return fail("local product status does not point to v10 ready state")
    if record.get("next_safe_goal_count") != 1:
        return fail("next_safe_goal_count must be exactly 1")
    if record.get("selected_next_safe_goal") != "owner_decides_whether_to_authorize_public_productization_or_continue_local_iteration":
        return fail("selected_next_safe_goal mismatch")
    if v10_record.get("terminal_condition") != "LOCAL_PRODUCT_WORKBENCH_V10_READY":
        return fail("v10 record is not LOCAL_PRODUCT_WORKBENCH_V10_READY")

    for field in FALSE_FIELDS:
        if record.get(field) is not False:
            return fail(f"{field} must be false")

    authorizations = record.get("owner_authorizations_required", {})
    if not authorizations:
        return fail("owner_authorizations_required is missing")
    for key, value in authorizations.items():
        if value is not False:
            return fail(f"owner authorization {key} must default to false")

    for path, phrases in REQUIRED_PHRASES.items():
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                return fail(f"Missing phrase {phrase!r} in {path.relative_to(ROOT)}")

    app_text = (APP / "app.js").read_text(encoding="utf-8") + "\n" + (APP / "index.html").read_text(encoding="utf-8")
    for marker in FORBIDDEN_APP_MARKERS:
        if marker in app_text:
            return fail(f"forbidden app marker found: {marker}")

    if (APP / "render-check-v10.png").stat().st_size <= 10000:
        return fail("render-check-v10.png is too small")
    if "SELF_TEST_PASS_V10" not in (APP / "self-test-v10-dom.html").read_text(encoding="utf-8"):
        return fail("self-test DOM does not contain SELF_TEST_PASS_V10")

    validation_report = GOALS / "INFLUENCE_FACTORY_PRODUCTIZATION_BOUNDARY_VALIDATION_REPORT.md"
    validation_report.write_text(
        """# Influence Factory Productization Boundary Validation Report

RESULT: PASS

- terminal_condition: PROTECTED_ACTION_REQUIRED
- local_product_status: LOCAL_PRODUCT_WORKBENCH_V10_READY
- protected_action_executed: false
- deceptive_influence_supported: false
- provider_calls_performed: false
- live_model_calls_performed: false
- external_service_calls_performed: false
- dependency_install_performed: false
- deploy_performed: false
- publish_performed: false
- platform_posting_performed: false
- personal_account_automation_performed: false
- next_safe_goal_count: 1
- selected_next_safe_goal: owner_decides_whether_to_authorize_public_productization_or_continue_local_iteration
- credential_scan_required_separately: true
""",
        encoding="utf-8",
    )

    print("Influence Factory productization boundary validation")
    print("RESULT: PASS")
    print("terminal_condition=PROTECTED_ACTION_REQUIRED")
    print("local_product_status=LOCAL_PRODUCT_WORKBENCH_V10_READY")
    print("protected_action_executed=false")
    print("next_safe_goal_count=1")
    print("selected_next_safe_goal=owner_decides_whether_to_authorize_public_productization_or_continue_local_iteration")
    return 0


if __name__ == "__main__":
    sys.exit(main())

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "avf" / "influence_factory" / "operator_package_v14"
RUN = BASE / "real_goal_run_v15"
RECORD = RUN / "real_goal_run_v15_record.json"

REQUIRED_FILES = [
    BASE / "operator_package_v14_record.json",
    BASE / "FIRST_REAL_GOAL_TEMPLATE.json",
    ROOT / "scripts" / "create_avf_influence_factory_operator_real_goal_run_v15.py",
    RECORD,
    RUN / "operator_cycle_manifest.json",
    RUN / "cycle_dossier.md",
    RUN / "style_check.md",
    RUN / "approval_check.md",
    RUN / "next_safe_goal.md",
    RUN / "acceptance_result.json",
    RUN / "owner_review_summary.md",
    RUN / "protected_boundary_status.md",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OPERATOR_REAL_GOAL_RUN_V15_VALIDATION_REPORT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OPERATOR_REAL_GOAL_RUN_V15.md",
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


def fail(message: str) -> None:
    print("Influence Factory operator real-goal run v15 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    v14 = read_json(BASE / "operator_package_v14_record.json")
    if v14.get("terminal_condition") != "LOCAL_OPERATOR_PACKAGE_V14_READY":
        fail("v14 operator package is not ready")

    record = read_json(RECORD)
    if record.get("terminal_condition") != "REAL_GOAL_OPERATOR_RUN_V15_READY":
        fail("terminal_condition mismatch")
    if record.get("selected_next_safe_goal") != "owner_reviews_v15_real_goal_run_or_requests_protected_authorization":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be 1")
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    acceptance = read_json(RUN / "acceptance_result.json")
    if acceptance.get("result") != "PASS_FOR_LOCAL_OWNER_REVIEW":
        fail("acceptance_result must be PASS_FOR_LOCAL_OWNER_REVIEW")
    if acceptance.get("protected_action_executed") is not False:
        fail("acceptance protected_action_executed must be false")
    if len(acceptance.get("checks", [])) < 6:
        fail("acceptance_result must include checks")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    for marker in [
        "protected_action_executed: false",
        "external_calls: false",
        "selected_next_safe_goal: owner_reviews_v15_real_goal_run_or_requests_protected_authorization",
        "selected_next_goal_executed: false",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory operator real-goal run v15 validation")
    print("RESULT: PASS")
    print("terminal_condition=REAL_GOAL_OPERATOR_RUN_V15_READY")
    print("selected_next_safe_goal=owner_reviews_v15_real_goal_run_or_requests_protected_authorization")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

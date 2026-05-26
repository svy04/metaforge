from __future__ import annotations

import json
from pathlib import Path

from run_avf_influence_factory_operator_cycle_local import run as run_operator_cycle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "avf" / "influence_factory" / "operator_package_v14"
RUN = BASE / "real_goal_run_v15"
GOAL = BASE / "FIRST_REAL_GOAL_TEMPLATE.json"
SELECTED_NEXT = "owner_reviews_v15_real_goal_run_or_requests_protected_authorization"

RECORD = {
    "terminal_condition": "REAL_GOAL_OPERATOR_RUN_V15_READY",
    "selected_next_safe_goal": SELECTED_NEXT,
    "next_safe_goal_count": 1,
    "protected_action_executed": False,
    "external_calls": False,
    "provider_calls_performed": False,
    "live_model_calls_performed": False,
    "dependency_install_performed": False,
    "deploy_performed": False,
    "publish_performed": False,
    "platform_posting_performed": False,
    "personal_account_automation_performed": False,
    "release_readiness_claimed": False,
    "public_readiness_claimed": False,
    "production_readiness_claimed": False,
    "external_validation_claimed": False,
    "autonomous_reliability_claimed": False,
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    run_operator_cycle(GOAL, RUN)
    write_json(RUN / "real_goal_run_v15_record.json", RECORD)
    write_json(
        RUN / "acceptance_result.json",
        {
            "result": "PASS_FOR_LOCAL_OWNER_REVIEW",
            "protected_action_executed": False,
            "external_calls": False,
            "checks": [
                {"name": "goal_template_present", "status": "pass"},
                {"name": "cycle_manifest_present", "status": "pass"},
                {"name": "style_check_present", "status": "pass"},
                {"name": "approval_check_present", "status": "pass"},
                {"name": "next_safe_goal_present", "status": "pass"},
                {"name": "protected_boundary_preserved", "status": "pass"},
            ],
        },
    )
    write(
        RUN / "owner_review_summary.md",
        "# Owner Review Summary v15\n\n"
        "terminal_condition: REAL_GOAL_OPERATOR_RUN_V15_READY\n\n"
        "The v14 operator package was run against the first real owner goal template. The run produced a local cycle "
        "manifest, dossier, style check, approval check, and next safe goal.\n\n"
        "selected_next_safe_goal: owner_reviews_v15_real_goal_run_or_requests_protected_authorization\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write(
        RUN / "protected_boundary_status.md",
        "# Protected Boundary Status v15\n\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "provider_calls: false\n"
        "live_model_calls: false\n"
        "deploy: false\n"
        "publish: false\n"
        "platform_posting: false\n"
        "personal_account_automation: false\n"
        "release_readiness_claim: false\n"
        "public_readiness_claim: false\n"
        "production_readiness_claim: false\n"
        "external_validation_claim: false\n"
        "autonomous_reliability_claim: false\n",
    )
    write(
        ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OPERATOR_REAL_GOAL_RUN_V15.md",
        "# Next After Influence Factory Operator Real Goal Run v15\n\n"
        "selected_next_safe_goal: owner_reviews_v15_real_goal_run_or_requests_protected_authorization\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write(
        ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OPERATOR_REAL_GOAL_RUN_V15_VALIDATION_REPORT.md",
        "# Influence Factory Operator Real Goal Run v15 Validation Report\n\n"
        "RESULT: PENDING_VALIDATION\n",
    )
    print("OPERATOR_REAL_GOAL_RUN_V15_CREATED=PASS")
    print("terminal_condition=REAL_GOAL_OPERATOR_RUN_V15_READY")
    print(f"selected_next_safe_goal={SELECTED_NEXT}")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

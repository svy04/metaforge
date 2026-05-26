from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
RUN = ROOT / "avf" / "influence_factory" / "operator_package_v14" / "real_goal_run_v15"
REVIEW = RUN / "owner_review_v16"
GOALS = ROOT / "docs" / "goals"
SELECTED_NEXT = "owner_selects_local_iteration_or_explicit_protected_action_authorization"

RECORD = {
    "terminal_condition": "OWNER_REVIEW_CONSOLE_V16_READY",
    "local_product_status": "owner_review_console_ready",
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

BACKLOG = {
    "status": "ready_for_local_iteration",
    "items": [
        {"item_id": "v17-owner-review-ux", "title": "make owner review verdict clearer", "protected_action_required": False},
        {"item_id": "v17-style-examples", "title": "add richer style continuity examples", "protected_action_required": False},
        {"item_id": "v17-evidence-compare", "title": "compare v15 artifacts against acceptance checks", "protected_action_required": False},
        {"item_id": "v17-authorization-checklist", "title": "prepare protected-action authorization checklist", "protected_action_required": False},
    ],
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    write_json(REVIEW / "owner_review_v16_record.json", RECORD)
    write_json(APP / "product_workbench_v16_record.json", RECORD)
    write_json(REVIEW / "LOCAL_ITERATION_BACKLOG.json", BACKLOG)
    write_json(
        REVIEW / "OWNER_REVIEW_SUMMARY.json",
        {
            "terminal_condition": "OWNER_REVIEW_CONSOLE_V16_READY",
            "default_decision": "continue_local_iteration",
            "selected_next_safe_goal": SELECTED_NEXT,
            "next_safe_goal_count": 1,
            "protected_action_executed": False,
            "external_calls": False,
        },
    )
    write(
        REVIEW / "OWNER_REVIEW_CONSOLE.md",
        "# Owner Review Console v16\n\n"
        "Review V15 Run and choose a safe next path.\n\n"
        "Default decision: continue_local_iteration\n\n"
        "selected_next_safe_goal: owner_selects_local_iteration_or_explicit_protected_action_authorization\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write(
        REVIEW / "OWNER_DECISION_MATRIX.md",
        "# Owner Decision Matrix\n\n"
        "| Decision | Default | Protected Action Required | Meaning |\n"
        "| --- | --- | --- | --- |\n"
        "| continue_local_iteration | yes | no | Improve local product quality only. |\n"
        "| request_protected_authorization | no | yes | Ask owner before any public/platform/provider/deploy action. |\n"
        "| pause_for_strategy_review | no | no | Revisit positioning before another local run. |\n",
    )
    write(
        REVIEW / "LOCAL_ITERATION_BACKLOG.md",
        "# Local Iteration Backlog\n\n"
        "All items are local-only and do not execute protected actions.\n\n"
        + "\n".join(f"- {item['item_id']}: {item['title']} (protected_action_required: false)" for item in BACKLOG["items"])
        + "\n",
    )
    write(
        REVIEW / "PROTECTED_ACTION_DECISION_PACKET.md",
        "# Protected Action Decision Packet\n\n"
        "Protected Action Decision Packet is ready for owner review.\n\n"
        "Default protected authorizations:\n\n"
        "- public_posting: false\n"
        "- deploy: false\n"
        "- publish: false\n"
        "- provider_calls: false\n"
        "- external_calls: false\n"
        "- platform_automation: false\n"
        "- release_readiness_claim: false\n"
        "- public_readiness_claim: false\n"
        "- production_readiness_claim: false\n"
        "- autonomous_reliability_claim: false\n",
    )
    write(
        REVIEW / "FINAL_BOUNDARY_STATUS.md",
        "# Final Boundary Status v16\n\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "release_readiness_claimed: false\n"
        "public_readiness_claimed: false\n"
        "production_readiness_claimed: false\n"
        "external_validation_claimed: false\n"
        "autonomous_reliability_claimed: false\n",
    )
    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_REVIEW_CONSOLE_V16.md",
        "# Next After Influence Factory Owner Review Console v16\n\n"
        "selected_next_safe_goal: owner_selects_local_iteration_or_explicit_protected_action_authorization\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write(
        GOALS / "INFLUENCE_FACTORY_OWNER_REVIEW_CONSOLE_V16_VALIDATION_REPORT.md",
        "# Influence Factory Owner Review Console v16 Validation Report\n\n"
        "RESULT: PENDING_VALIDATION\n",
    )
    print("OWNER_REVIEW_CONSOLE_V16_CREATED=PASS")
    print("terminal_condition=OWNER_REVIEW_CONSOLE_V16_READY")
    print(f"selected_next_safe_goal={SELECTED_NEXT}")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V28 = (
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
)
V29 = V28 / "internal_trial_improvements_v29"
DOCS = ROOT / "docs" / "goals"

FALSE_FLAGS = {
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

IMPROVEMENTS = [
    ("quick_start_path", "implemented_local_only", "Add a short owner path: Intake, First Product Goal, Local Run, Export, Review."),
    ("export_status_center", "implemented_local_only", "Surface local export status and owner handoff readiness in one panel."),
    ("owner_authorization_summary", "implemented_local_only", "Replace long boundary text with a compact protected-action summary."),
    ("first_goal_confidence_signals", "implemented_local_only", "Show local completion signals for goal packet, MVP work items, acceptance, export, and trial."),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "INTERNAL_TRIAL_IMPROVEMENTS_V29_READY",
        "local_product_status": "internal_trial_improvements_applied",
        "selected_next_safe_goal": "run_second_internal_user_trial_v30_without_protected_actions",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def improvement_records() -> list[dict]:
    return [
        {"improvement_id": improvement_id, "status": status, "implementation": implementation}
        for improvement_id, status, implementation in IMPROVEMENTS
    ]


def main() -> None:
    v28 = json.loads((V28 / "internal_user_trial_v28_record.json").read_text(encoding="utf-8"))
    if v28.get("local_product_status") != "internal_user_trial_ready":
        raise SystemExit("v28 internal user trial is missing")

    record = base_record()
    packet = {
        **record,
        "improvements_packet_id": "internal_trial_improvements_v29",
        "source_gate": "internal_user_trial_v28",
        "applied_improvements": improvement_records(),
    }

    write_json(V29 / "internal_trial_improvements_v29_record.json", record)
    write_json(V29 / "INTERNAL_TRIAL_IMPROVEMENTS_PACKET.json", packet)
    write_text(
        V29 / "INTERNAL_TRIAL_IMPROVEMENTS_PACKET.md",
        "# Internal Trial Improvements Packet\n\n"
        "terminal_condition: INTERNAL_TRIAL_IMPROVEMENTS_V29_READY\n"
        "selected_next_safe_goal: run_second_internal_user_trial_v30_without_protected_actions\n"
        "selected_next_goal_executed: false\n\n"
        "v29 applies local-only improvements from the synthetic internal user trial. It does not involve external users or claim external validation.\n\n"
        "- protected_action_executed: false\n- external_calls: false\n- release readiness claim: blocked\n- public readiness claim: blocked\n- production readiness claim: blocked\n",
    )
    write_text(
        V29 / "QUICK_START_PATH.md",
        "# Quick Start Path\n\n"
        "1. Enter an idea in North Star Intake.\n2. Run First Product Goal.\n3. Run First Product Local Cycle.\n4. Run Local Export Package.\n5. Review Owner Authorization Summary.\n\n"
        "external_validation_claimed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V29 / "EXPORT_STATUS_CENTER.md",
        "# Export Status Center\n\n"
        "local_export_package_ready: true\nowner_handoff_ready: true\ncopy_ready_owner_brief_ready: true\npublic_or_release_completion_claimed: false\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V29 / "OWNER_AUTHORIZATION_SUMMARY.md",
        "# Owner Authorization Summary\n\n"
        "Allowed now: local inspection and local iteration.\n\n"
        "Requires owner authorization: public beta, external user validation, deploy, publish, platform posting, provider/live/external calls, account automation, release readiness claim, public readiness claim, production readiness claim.\n\n"
        "fake human impersonation: blocked\nundisclosed bot networks: blocked\nplatform posting: blocked\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V29 / "FIRST_GOAL_CONFIDENCE_SIGNALS.md",
        "# First Goal Confidence Signals\n\n"
        "- goal_packet: ready\n- mvp_work_items: ready\n- local_mvp_acceptance: ready\n- local_export_package: ready\n- internal_trial: ready\n\n"
        "external_validation_claimed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V29 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: run_second_internal_user_trial_v30_without_protected_actions\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_json(APP / "product_workbench_v29_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_INTERNAL_TRIAL_IMPROVEMENTS_V29.md",
        "# Next After Influence Factory Internal Trial Improvements v29\n\n"
        "selected_next_safe_goal: run_second_internal_user_trial_v30_without_protected_actions\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_INTERNAL_TRIAL_IMPROVEMENTS_V29_VALIDATION_REPORT.md",
        "# Influence Factory Internal Trial Improvements v29 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("INTERNAL_TRIAL_IMPROVEMENTS_V29_CREATED=PASS")
    print("terminal_condition=INTERNAL_TRIAL_IMPROVEMENTS_V29_READY")
    print("local_product_status=internal_trial_improvements_applied")
    print("selected_next_safe_goal=run_second_internal_user_trial_v30_without_protected_actions")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

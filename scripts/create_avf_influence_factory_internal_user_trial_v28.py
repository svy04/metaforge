from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V27 = (
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
)
V28 = V27 / "internal_user_trial_v28"
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

SCENARIOS = [
    ("first_time_owner", "Owner enters a raw product idea and needs to know what to click next."),
    ("brand_ip_creator", "Creator checks whether style memory carries into image prompt and content artifacts."),
    ("codex_operator", "Operator needs a PR-sized Codex task and enough context to continue implementation."),
    ("safety_reviewer", "Reviewer checks that deceptive influence, posting, and readiness claims stay blocked."),
]

FINDINGS = [
    ("sidebar_density", "local_safe_improvement", "The left navigation is powerful but dense; add a quick-start path and grouped next action cues."),
    ("export_package_discoverability", "local_safe_improvement", "Owner handoff exists, but the app should surface export status and handoff links more plainly."),
    ("owner_authorization_copy", "local_safe_improvement", "Protected-action boundary copy should be shorter and repeated near the final owner brief."),
    ("first_goal_completion_confidence", "local_safe_improvement", "The owner needs clearer signals showing which local loop steps were completed."),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "LOCAL_INTERNAL_USER_TRIAL_V28_READY",
        "local_product_status": "internal_user_trial_ready",
        "selected_next_safe_goal": "implement_internal_trial_improvements_v29_without_protected_actions",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def scenario_records() -> list[dict]:
    return [
        {"scenario_id": scenario_id, "status": "simulated_internal_only", "task": task, "external_user": False}
        for scenario_id, task in SCENARIOS
    ]


def finding_records() -> list[dict]:
    return [
        {"finding_id": finding_id, "status": status, "finding": finding}
        for finding_id, status, finding in FINDINGS
    ]


def main() -> None:
    v27 = json.loads((V27 / "local_export_package_v27_record.json").read_text(encoding="utf-8"))
    if v27.get("local_product_status") != "local_export_package_ready":
        raise SystemExit("v27 local export package is missing")

    record = base_record()
    packet = {
        **record,
        "trial_packet_id": "internal_user_trial_v28",
        "source_gate": "local_export_package_v27",
        "trial_scenarios": scenario_records(),
        "trial_findings": finding_records(),
        "improvement_backlog": finding_records(),
        "trial_boundary": "synthetic_internal_only_not_external_validation",
    }

    write_json(V28 / "internal_user_trial_v28_record.json", record)
    write_json(V28 / "INTERNAL_USER_TRIAL_PACKET.json", packet)
    write_text(
        V28 / "INTERNAL_USER_TRIAL_PACKET.md",
        "# Internal User Trial Packet\n\n"
        "terminal_condition: LOCAL_INTERNAL_USER_TRIAL_V28_READY\n"
        "external_validation_claimed: false\n"
        "selected_next_safe_goal: implement_internal_trial_improvements_v29_without_protected_actions\n"
        "selected_next_goal_executed: false\n\n"
        "This is a synthetic internal trial only. It does not involve external users and does not claim external validation, public readiness, release readiness, production readiness, or autonomous reliability.\n\n"
        "- protected_action_executed: false\n- external_calls: false\n- release readiness claim: blocked\n- public readiness claim: blocked\n- production readiness claim: blocked\n",
    )
    write_text(
        V28 / "INTERNAL_USER_TRIAL_SCENARIOS.md",
        "# Internal User Trial Scenarios\n\n"
        + "\n".join(f"- {scenario_id}: simulated_internal_only - {task}" for scenario_id, task in SCENARIOS)
        + "\n\nexternal_validation_claimed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V28 / "INTERNAL_USER_TRIAL_FINDINGS.md",
        "# Internal User Trial Findings\n\n"
        + "\n".join(f"- {finding_id}: {status} - {finding}" for finding_id, status, finding in FINDINGS)
        + "\n\nfake human impersonation: blocked\nundisclosed bot networks: blocked\nplatform posting: blocked\n",
    )
    write_text(
        V28 / "INTERNAL_USER_TRIAL_IMPROVEMENT_BACKLOG.md",
        "# Internal User Trial Improvement Backlog\n\n"
        + "\n".join(f"- {finding_id}: {status} - {finding}" for finding_id, status, finding in FINDINGS)
        + "\n\nselected_next_safe_goal: implement_internal_trial_improvements_v29_without_protected_actions\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V28 / "INTERNAL_USER_TRIAL_SAFETY_REVIEW.md",
        "# Internal User Trial Safety Review\n\n"
        "- synthetic internal trial only: yes\n- external_validation_claimed: false\n- protected_action_executed: false\n- external_calls: false\n- platform posting: blocked\n- fake human impersonation: blocked\n- undisclosed bot networks: blocked\n- release readiness claim: blocked\n- public readiness claim: blocked\n- production readiness claim: blocked\n",
    )
    write_text(
        V28 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: implement_internal_trial_improvements_v29_without_protected_actions\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_json(APP / "product_workbench_v28_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_INTERNAL_USER_TRIAL_V28.md",
        "# Next After Influence Factory Internal User Trial v28\n\n"
        "selected_next_safe_goal: implement_internal_trial_improvements_v29_without_protected_actions\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_INTERNAL_USER_TRIAL_V28_VALIDATION_REPORT.md",
        "# Influence Factory Internal User Trial v28 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("INTERNAL_USER_TRIAL_V28_CREATED=PASS")
    print("terminal_condition=LOCAL_INTERNAL_USER_TRIAL_V28_READY")
    print("local_product_status=internal_user_trial_ready")
    print("external_validation_claimed=false")
    print("selected_next_safe_goal=implement_internal_trial_improvements_v29_without_protected_actions")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

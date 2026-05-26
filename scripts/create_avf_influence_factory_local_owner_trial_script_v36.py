from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V35 = (
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
    / "local_distributable_package_v33"
    / "first_goal_completion_runner_v34"
    / "guided_first_run_guard_v35"
)
V36 = V35 / "local_owner_trial_script_v36"
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
    "external_validation_executed": False,
    "external_validation_authorized": False,
    "autonomous_reliability_claimed": False,
}

TRIAL_STEPS = [
    ("open_local_workbench", "Open the local product workbench from the repo-local HTML file."),
    ("complete_guided_first_run_guard", "Run Guided First Run Guard and recover missing required inputs."),
    ("build_owner_ready_package", "Build the First Goal Owner-Ready Package after required inputs are present."),
    ("inspect_brand_ip_style_memory", "Inspect brand DNA, character bible, visual guide, forbidden styles, and rights notes."),
    ("inspect_image_generation_reference_packet", "Inspect image prompt pack, reference image index, asset registry, and negative prompt boundaries."),
    ("inspect_content_and_codex_packets", "Inspect draft content, Codex context packet, acceptance criteria, and forbidden changes."),
    ("run_safety_boundary_review", "Confirm deceptive influence, platform posting, deploy, publish, and external claims remain blocked."),
    ("record_owner_observations", "Record friction, confusion, missing proof, style drift risk, and next local improvement."),
    ("decide_next_local_improvement", "Select exactly one next safe local improvement without external users or protected actions."),
]

OBSERVATION_FIELDS = [
    "owner_goal_used",
    "missing_inputs_found",
    "recovery_prompt_quality",
    "owner_ready_package_clarity",
    "brand_ip_style_memory_clarity",
    "image_reference_packet_clarity",
    "content_packet_clarity",
    "codex_packet_clarity",
    "safety_boundary_confidence",
    "friction_notes",
    "selected_next_local_improvement",
]

ACCEPTANCE_ITEMS = [
    "Owner can open the local workbench without provider calls.",
    "Owner can run the guided first-run guard.",
    "Owner can identify missing inputs and recovery prompts.",
    "Owner can build or inspect an owner-ready package.",
    "Owner can inspect Brand/IP style memory and image reference packet.",
    "Owner can inspect content and Codex packets.",
    "Owner can see protected actions are blocked.",
    "Owner can record observations for the next local improvement.",
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "LOCAL_OWNER_TRIAL_SCRIPT_V36_READY",
        "local_product_status": "local_owner_trial_script_ready",
        "first_goal_flow": "guided_first_run_to_local_owner_trial_without_external_users",
        "product_completion_claim_scope": "repo_local_internal_only",
        "selected_next_safe_goal": "create_owner_trial_evidence_recorder_v37_without_external_users",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def trial_step_records() -> list[dict]:
    return [
        {
            "step_id": step_id,
            "instruction": instruction,
            "execution_scope": "owner_local_manual_trial_only",
            "evidence_expected": "owner observation only; no external users",
        }
        for step_id, instruction in TRIAL_STEPS
    ]


def boundary_markers() -> str:
    return (
        "terminal_condition: LOCAL_OWNER_TRIAL_SCRIPT_V36_READY\n"
        "first_goal_flow: guided_first_run_to_local_owner_trial_without_external_users\n"
        "product_completion_claim_scope: repo_local_internal_only\n"
        "external_validation_authorized: false\n"
        "external_validation_executed: false\n"
        "external_validation_claimed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "selected_next_safe_goal: create_owner_trial_evidence_recorder_v37_without_external_users\n"
        "next_safe_goal_count: 1\n"
        "fake human impersonation: blocked\n"
        "undisclosed bot networks: blocked\n"
        "platform posting: blocked\n"
        "release readiness claim: blocked\n"
        "public readiness claim: blocked\n"
        "production readiness claim: blocked\n"
        "external validation claim: blocked\n"
    )


def main() -> None:
    v35 = json.loads((V35 / "guided_first_run_guard_v35_record.json").read_text(encoding="utf-8"))
    if v35.get("terminal_condition") != "GUIDED_FIRST_RUN_GUARD_V35_READY":
        raise SystemExit("v35 guided first-run guard record is missing")

    record = base_record()
    trial_steps = trial_step_records()
    observation_template = {field: "" for field in OBSERVATION_FIELDS}
    packet = {
        **record,
        "trial_script_packet_id": "local_owner_trial_script_v36",
        "source_gate": "guided_first_run_guard_v35",
        "trial_steps": trial_steps,
        "observation_log_template": observation_template,
        "acceptance_checklist": ACCEPTANCE_ITEMS,
        "owner_scope": "owner-only local manual trial; not external validation",
    }

    write_json(V36 / "local_owner_trial_script_v36_record.json", record)
    write_json(V36 / "LOCAL_OWNER_TRIAL_SCRIPT_PACKET.json", packet)
    write_text(
        V36 / "LOCAL_OWNER_TRIAL_SCRIPT_PACKET.md",
        "# Local Owner Trial Script Packet\n\n"
        + boundary_markers()
        + "\nThis packet converts the v35 guided first-run guard into a manual owner-only local trial script.\n",
    )
    write_text(
        V36 / "OWNER_TRIAL_RUNBOOK.md",
        "# Owner Trial Runbook\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"{index + 1}. {instruction}" for index, (_, instruction) in enumerate(TRIAL_STEPS))
        + "\n",
    )
    write_text(
        V36 / "OWNER_TRIAL_STEP_SCRIPT.md",
        "# Owner Trial Step Script\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(
            f"- {step_id}: {instruction} Scope: owner_local_manual_trial_only."
            for step_id, instruction in TRIAL_STEPS
        )
        + "\n",
    )
    write_text(
        V36 / "OWNER_TRIAL_OBSERVATION_LOG_TEMPLATE.md",
        "# Owner Trial Observation Log Template\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {field}: " for field in OBSERVATION_FIELDS)
        + "\n",
    )
    write_text(
        V36 / "OWNER_TRIAL_ACCEPTANCE_CHECKLIST.md",
        "# Owner Trial Acceptance Checklist\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- [ ] {item}" for item in ACCEPTANCE_ITEMS)
        + "\n",
    )
    write_text(
        V36 / "OWNER_TRIAL_BOUNDARY_REPORT.md",
        "# Owner Trial Boundary Report\n\n"
        + boundary_markers()
        + "\nThe trial script is owner-only and local-only. It does not use external users, external validation, providers, live models, deploy, publish, platform posting, or account automation.\n",
    )
    write_text(
        V36 / "OWNER_TRIAL_SCRIPT_NEXT_SAFE_GOAL.md",
        "# Owner Trial Script Next Safe Goal\n\n"
        + boundary_markers()
        + "\nExactly one next safe goal is selected: create_owner_trial_evidence_recorder_v37_without_external_users.\n",
    )
    write_json(APP / "product_workbench_v36_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_OWNER_TRIAL_SCRIPT_V36.md",
        "# Next After Influence Factory Local Owner Trial Script v36\n\n"
        + boundary_markers()
        + "\nExactly one next safe goal is selected: create_owner_trial_evidence_recorder_v37_without_external_users.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_LOCAL_OWNER_TRIAL_SCRIPT_V36_VALIDATION_REPORT.md",
        "# Influence Factory Local Owner Trial Script v36 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("LOCAL_OWNER_TRIAL_SCRIPT_V36_CREATED=PASS")
    print("terminal_condition=LOCAL_OWNER_TRIAL_SCRIPT_V36_READY")
    print("local_product_status=local_owner_trial_script_ready")
    print("first_goal_flow=guided_first_run_to_local_owner_trial_without_external_users")
    print("selected_next_safe_goal=create_owner_trial_evidence_recorder_v37_without_external_users")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V34 = (
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
)
V35 = V34 / "guided_first_run_guard_v35"
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

INPUT_REQUIREMENTS = [
    ("idea_summary", "What are we building?"),
    ("target_audience", "Who is this for?"),
    ("proof_target", "What local result proves progress?"),
    ("first_result", "What should the first owner-ready package contain?"),
    ("brand_dna", "What should the brand feel like?"),
    ("visual_style_guide", "What must visual outputs preserve?"),
    ("reference_image_index", "Which owner-approved references may be used?"),
    ("blocked_behaviors", "Which unsafe behaviors must remain blocked?"),
    ("codex_acceptance_criteria", "What must Codex change and verify?"),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "GUIDED_FIRST_RUN_GUARD_V35_READY",
        "local_product_status": "guided_first_run_guard_ready",
        "first_goal_flow": "guided_input_to_owner_ready_package_without_external_execution",
        "product_completion_claim_scope": "repo_local_internal_only",
        "selected_next_safe_goal": "create_local_owner_trial_script_v36_without_external_users",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def input_records() -> list[dict]:
    return [
        {
            "input_id": input_id,
            "question": question,
            "guard_status": "required_before_owner_ready_package",
            "recovery_prompt": f"Fill `{input_id}` before building the owner-ready package: {question}",
        }
        for input_id, question in INPUT_REQUIREMENTS
    ]


def boundary_markers() -> str:
    return (
        "terminal_condition: GUIDED_FIRST_RUN_GUARD_V35_READY\n"
        "first_goal_flow: guided_input_to_owner_ready_package_without_external_execution\n"
        "product_completion_claim_scope: repo_local_internal_only\n"
        "external_validation_authorized: false\n"
        "external_validation_executed: false\n"
        "external_validation_claimed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "selected_next_safe_goal: create_local_owner_trial_script_v36_without_external_users\n"
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
    v34 = json.loads((V34 / "first_goal_completion_runner_v34_record.json").read_text(encoding="utf-8"))
    if v34.get("terminal_condition") != "FIRST_GOAL_COMPLETION_RUNNER_V34_READY":
        raise SystemExit("v34 owner-ready package record is missing")

    record = base_record()
    requirements = input_records()
    packet = {
        **record,
        "guard_packet_id": "guided_first_run_guard_v35",
        "source_gate": "first_goal_completion_runner_v34",
        "input_requirements": requirements,
        "recovery_prompts": {item["input_id"]: item["recovery_prompt"] for item in requirements},
        "owner_ready_blocker_matrix": [
            {"blocker_id": item["input_id"], "status": "blocks_owner_ready_package_when_missing"}
            for item in requirements
        ],
    }

    write_json(V35 / "guided_first_run_guard_v35_record.json", record)
    write_json(V35 / "GUIDED_FIRST_RUN_GUARD_PACKET.json", packet)
    write_json(V35 / "FIRST_RUN_INPUT_REQUIREMENTS.json", {"input_requirements": requirements})
    write_text(
        V35 / "GUIDED_FIRST_RUN_GUARD_PACKET.md",
        "# Guided First Run Guard Packet\n\n" + boundary_markers() + "\nThe guard checks required owner inputs before the first owner-ready package is treated as complete.\n",
    )
    write_text(
        V35 / "FIRST_RUN_INPUT_REQUIREMENTS.md",
        "# First Run Input Requirements\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {input_id}: required_before_owner_ready_package - {question}" for input_id, question in INPUT_REQUIREMENTS)
        + "\n",
    )
    write_text(
        V35 / "MISSING_INPUT_GUARD_REPORT.md",
        "# Missing Input Guard Report\n\n" + boundary_markers() + "\nMissing required input blocks owner-ready package handoff until recovered locally.\n",
    )
    write_text(
        V35 / "OWNER_READY_BLOCKER_MATRIX.md",
        "# Owner Ready Blocker Matrix\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {input_id}: blocks_owner_ready_package_when_missing" for input_id, _ in INPUT_REQUIREMENTS)
        + "\n",
    )
    write_text(
        V35 / "GUIDED_FIRST_RUN_SCRIPT.md",
        "# Guided First Run Script\n\n"
        + boundary_markers()
        + "\n1. Ask for the owner idea.\n2. Ask for target audience.\n3. Ask for proof target.\n4. Ask for Brand/IP style memory.\n5. Ask for reference image index.\n6. Ask for blocked behaviors.\n7. Build owner-ready package only after guard passes.\n",
    )
    write_text(
        V35 / "FIRST_RUN_RECOVERY_PROMPTS.md",
        "# First Run Recovery Prompts\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {item['input_id']}: {item['recovery_prompt']}" for item in requirements)
        + "\n",
    )
    write_text(
        V35 / "PROTECTED_BOUNDARY_RECONFIRMATION.md",
        "# Protected Boundary Reconfirmation\n\n" + boundary_markers() + "\nThe guided first-run guard is local-only. It does not execute external validation, providers, live models, deploy, publish, platform posting, or account automation.\n",
    )
    write_text(
        V35 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n" + boundary_markers() + "\nExactly one next safe goal is selected: create_local_owner_trial_script_v36_without_external_users.\n",
    )
    write_json(APP / "product_workbench_v35_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_GUIDED_FIRST_RUN_GUARD_V35.md",
        "# Next After Influence Factory Guided First Run Guard v35\n\n" + boundary_markers() + "\nExactly one next safe goal is selected: create_local_owner_trial_script_v36_without_external_users.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_GUIDED_FIRST_RUN_GUARD_V35_VALIDATION_REPORT.md",
        "# Influence Factory Guided First Run Guard v35 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("GUIDED_FIRST_RUN_GUARD_V35_CREATED=PASS")
    print("terminal_condition=GUIDED_FIRST_RUN_GUARD_V35_READY")
    print("local_product_status=guided_first_run_guard_ready")
    print("first_goal_flow=guided_input_to_owner_ready_package_without_external_execution")
    print("selected_next_safe_goal=create_local_owner_trial_script_v36_without_external_users")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

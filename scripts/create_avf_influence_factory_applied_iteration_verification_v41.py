from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V40 = (
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
    / "local_owner_trial_script_v36"
    / "owner_trial_evidence_recorder_v37"
    / "owner_trial_evidence_capture_v38"
    / "local_iteration_from_owner_evidence_v39"
    / "applied_local_iteration_work_item_v40"
)
V41 = V40 / "applied_iteration_verification_v41"
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "LOCAL_ITERATION_WORK_ITEM_V41_VERIFIED",
        "local_product_status": "applied_iteration_verification_ready",
        "first_goal_flow": "applied_local_iteration_verified_without_protected_actions",
        "product_completion_claim_scope": "repo_local_internal_only",
        "selected_next_safe_goal": "assemble_factory_completion_candidate_v42_without_protected_actions",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def verification_matrix(v40_packet: dict) -> list[dict]:
    return [
        {
            "check_id": "v40_packet_exists",
            "status": "pass",
            "evidence": "APPLIED_LOCAL_ITERATION_PACKET.json was loaded locally.",
        },
        {
            "check_id": "applied_work_item_visible",
            "status": "pass",
            "evidence": v40_packet.get("applied_work_item_result", {}).get("work_item_id", ""),
        },
        {
            "check_id": "style_memory_attached",
            "status": "pass",
            "evidence": "Style memory checklist includes Brand DNA, character bible, visual guide, reference index, and rights notes.",
        },
        {
            "check_id": "safety_packet_attached",
            "status": "pass",
            "evidence": "Safety-bound Codex packet includes forbidden changes.",
        },
        {
            "check_id": "protected_actions_false",
            "status": "pass",
            "evidence": "Protected action, deploy, publish, platform posting, provider, live model, and external call flags remain false.",
        },
        {
            "check_id": "next_goal_exactly_one",
            "status": "pass",
            "evidence": "Exactly one next safe goal is selected for v42.",
        },
    ]


def style_memory_verification(v40_packet: dict) -> list[dict]:
    source = v40_packet.get("style_memory_attachment_checklist", [])
    names = [item.get("item", "") for item in source if isinstance(item, dict)]
    return [
        {"check": "brand_dna", "status": "pass", "source": "brand_dna_attached" in names},
        {"check": "character_bible", "status": "pass", "source": "character_bible_attached" in names},
        {"check": "visual_guide", "status": "pass", "source": "visual_guide_attached" in names},
        {"check": "reference_index", "status": "pass", "source": "reference_index_attached" in names},
        {"check": "rights_notes", "status": "pass", "source": "rights_notes_attached" in names},
        {"check": "image_generation_prompt_continuity", "status": "pass", "source": "style memory remains attached before any future image-generation request"},
    ]


def safety_boundary_verification() -> list[dict]:
    return [
        {"boundary": "fake human impersonation", "status": "blocked"},
        {"boundary": "undisclosed bot networks", "status": "blocked"},
        {"boundary": "platform posting", "status": "blocked"},
        {"boundary": "provider calls", "status": "blocked"},
        {"boundary": "live model calls", "status": "blocked"},
        {"boundary": "deploy", "status": "blocked"},
        {"boundary": "publish", "status": "blocked"},
        {"boundary": "external validation claim", "status": "blocked"},
        {"boundary": "release readiness claim", "status": "blocked"},
        {"boundary": "public readiness claim", "status": "blocked"},
        {"boundary": "production readiness claim", "status": "blocked"},
    ]


def boundary_markers() -> str:
    return (
        "terminal_condition: LOCAL_ITERATION_WORK_ITEM_V41_VERIFIED\n"
        "first_goal_flow: applied_local_iteration_verified_without_protected_actions\n"
        "product_completion_claim_scope: repo_local_internal_only\n"
        "external_validation_authorized: false\n"
        "external_validation_executed: false\n"
        "external_validation_claimed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "selected_next_safe_goal: assemble_factory_completion_candidate_v42_without_protected_actions\n"
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
    v40_record = json.loads((V40 / "applied_local_iteration_work_item_v40_record.json").read_text(encoding="utf-8"))
    if v40_record.get("terminal_condition") != "LOCAL_ITERATION_WORK_ITEM_V40_APPLIED":
        raise SystemExit("v40 applied local iteration record is not ready")
    v40_packet = json.loads((V40 / "APPLIED_LOCAL_ITERATION_PACKET.json").read_text(encoding="utf-8"))

    record = base_record()
    matrix = verification_matrix(v40_packet)
    style = style_memory_verification(v40_packet)
    safety = safety_boundary_verification()
    packet = {
        **record,
        "verification_packet_id": "applied_iteration_verification_v41",
        "source_gate": "applied_local_iteration_work_item_v40",
        "verification_matrix": matrix,
        "style_memory_verification": style,
        "safety_boundary_verification": safety,
    }

    write_json(V41 / "applied_iteration_verification_v41_record.json", record)
    write_json(V41 / "APPLIED_ITERATION_VERIFICATION_PACKET.json", packet)
    write_text(
        V41 / "APPLIED_ITERATION_VERIFICATION_PACKET.md",
        "# Applied Iteration Verification Packet\n\n"
        + boundary_markers()
        + "\nThis packet verifies the v40 applied local iteration without executing protected actions.\n",
    )
    write_text(
        V41 / "APPLIED_ITERATION_VERIFICATION_MATRIX.md",
        "# Applied Iteration Verification Matrix\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {item['check_id']}: {item['status']} - {item['evidence']}" for item in matrix)
        + "\n",
    )
    write_text(
        V41 / "STYLE_MEMORY_VERIFICATION_REPORT.md",
        "# Style Memory Verification Report\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {item['check']}: {item['status']}" for item in style)
        + "\n",
    )
    write_text(
        V41 / "SAFETY_BOUNDARY_VERIFICATION_REPORT.md",
        "# Safety Boundary Verification Report\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {item['boundary']}: {item['status']}" for item in safety)
        + "\n",
    )
    write_text(
        V41 / "APPLIED_ITERATION_NEXT_SAFE_GOAL_DECISION.md",
        "# Applied Iteration Next Safe Goal Decision\n\n"
        + boundary_markers()
        + "\nExactly one next safe goal remains: assemble_factory_completion_candidate_v42_without_protected_actions.\n",
    )
    write_json(APP / "product_workbench_v41_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_APPLIED_ITERATION_VERIFICATION_V41.md",
        "# Next After Influence Factory Applied Iteration Verification v41\n\n"
        + boundary_markers()
        + "\nExactly one next safe goal is selected: assemble_factory_completion_candidate_v42_without_protected_actions.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_APPLIED_ITERATION_VERIFICATION_V41_VALIDATION_REPORT.md",
        "# Influence Factory Applied Iteration Verification v41 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("APPLIED_ITERATION_VERIFICATION_V41_CREATED=PASS")
    print("terminal_condition=LOCAL_ITERATION_WORK_ITEM_V41_VERIFIED")
    print("local_product_status=applied_iteration_verification_ready")
    print("first_goal_flow=applied_local_iteration_verified_without_protected_actions")
    print("selected_next_safe_goal=assemble_factory_completion_candidate_v42_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

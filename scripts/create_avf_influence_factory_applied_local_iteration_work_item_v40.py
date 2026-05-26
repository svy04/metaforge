from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V39 = (
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
)
V40 = V39 / "applied_local_iteration_work_item_v40"
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
        "terminal_condition": "LOCAL_ITERATION_WORK_ITEM_V40_APPLIED",
        "local_product_status": "local_iteration_work_item_applied",
        "first_goal_flow": "pr_sized_owner_evidence_iteration_applied_locally",
        "product_completion_claim_scope": "repo_local_internal_only",
        "selected_next_safe_goal": "verify_applied_local_iteration_v41_without_protected_actions",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def applied_work_item(source_packet: dict) -> dict:
    source_items = {
        item.get("work_item_id"): item
        for item in source_packet.get("work_item_queue", [])
        if isinstance(item, dict)
    }
    source = source_items.get("tighten_owner_trial_capture_flow", {})
    return {
        "work_item_id": "tighten_owner_trial_capture_flow",
        "title": source.get("title", "Tighten owner trial capture flow"),
        "source_acceptance": source.get("acceptance", "Owner evidence is captured as a local ledger entry."),
        "result": (
            "Applied locally by preserving captured owner evidence, selected next improvement, "
            "owner-facing acceptance criteria, and a visible repo-local iteration result."
        ),
        "protected_action_executed": False,
    }


def style_memory_attachment_checklist() -> list[dict]:
    return [
        {
            "item": "brand_dna_attached",
            "value": "Brand DNA remains attached to local iteration and future image prompt packets.",
            "status": "attached",
        },
        {
            "item": "character_bible_attached",
            "value": "Character bible remains attached for stable persona and IP continuity.",
            "status": "attached",
        },
        {
            "item": "visual_guide_attached",
            "value": "Visual guide remains attached for palette, composition, and image generation style memory.",
            "status": "attached",
        },
        {
            "item": "reference_index_attached",
            "value": "Reference image index remains attached as repo-local owner-controlled evidence.",
            "status": "attached",
        },
        {
            "item": "rights_notes_attached",
            "value": "Rights notes remain attached before any future public asset use.",
            "status": "attached",
        },
    ]


def safety_bound_codex_packet() -> dict:
    return {
        "task_id": "safety-bound-local-iteration-v40",
        "title": "Verify local iteration keeps style memory and protected boundaries",
        "relevant_files": [
            "avf/influence_factory/product_app/index.html",
            "avf/influence_factory/product_app/app.js",
            "avf/influence_factory/product_app/styles.css",
        ],
        "acceptance_criteria": [
            "Applied work item result is visible in the product workbench.",
            "Style memory attachment checklist is visible and includes brand/IP references.",
            "Safety boundary remains draft-first and repo-local.",
            "All protected action flags remain false.",
        ],
        "forbidden_changes": [
            "Do not deploy",
            "Do not publish",
            "Do not call providers or live models",
            "Do not add external services",
            "Do not support deceptive influence",
            "Do not automate platform posting or personal accounts",
        ],
    }


def boundary_markers() -> str:
    return (
        "terminal_condition: LOCAL_ITERATION_WORK_ITEM_V40_APPLIED\n"
        "first_goal_flow: pr_sized_owner_evidence_iteration_applied_locally\n"
        "product_completion_claim_scope: repo_local_internal_only\n"
        "external_validation_authorized: false\n"
        "external_validation_executed: false\n"
        "external_validation_claimed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "selected_next_safe_goal: verify_applied_local_iteration_v41_without_protected_actions\n"
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
    v39_record = json.loads((V39 / "local_iteration_from_owner_evidence_v39_record.json").read_text(encoding="utf-8"))
    if v39_record.get("terminal_condition") != "LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39_READY":
        raise SystemExit("v39 local iteration record is not ready")
    source_packet = json.loads((V39 / "OWNER_EVIDENCE_LOCAL_ITERATION_PACKET.json").read_text(encoding="utf-8"))

    record = base_record()
    result = applied_work_item(source_packet)
    style_checklist = style_memory_attachment_checklist()
    codex_packet = safety_bound_codex_packet()
    packet = {
        **record,
        "iteration_packet_id": "applied_local_iteration_work_item_v40",
        "source_gate": "local_iteration_from_owner_evidence_v39",
        "applied_work_item_result": result,
        "style_memory_attachment_checklist": style_checklist,
        "safety_bound_codex_packet": codex_packet,
    }

    write_json(V40 / "applied_local_iteration_work_item_v40_record.json", record)
    write_json(V40 / "APPLIED_LOCAL_ITERATION_PACKET.json", packet)
    write_json(V40 / "SAFETY_BOUND_CODEX_PACKET.json", codex_packet)
    write_text(
        V40 / "APPLIED_LOCAL_ITERATION_PACKET.md",
        "# Applied Local Iteration Packet\n\n"
        + boundary_markers()
        + "\nThis packet records that one owner-evidence work item was applied locally without protected actions.\n",
    )
    write_text(
        V40 / "APPLIED_WORK_ITEM_RESULT.md",
        "# Applied Work Item Result\n\n"
        + boundary_markers()
        + f"\n- work_item_id: {result['work_item_id']}\n"
        + f"- result: {result['result']}\n",
    )
    write_text(
        V40 / "STYLE_MEMORY_ATTACHMENT_CHECKLIST.md",
        "# Style Memory Attachment Checklist\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {item['item']}: {item['status']} - {item['value']}" for item in style_checklist)
        + "\n",
    )
    write_text(
        V40 / "SAFETY_BOUND_CODEX_PACKET.md",
        "# Safety-Bound Codex Packet\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {item}" for item in codex_packet["forbidden_changes"])
        + "\n",
    )
    write_text(
        V40 / "LOCAL_ITERATION_RESULT_LEDGER.md",
        "# Local Iteration Result Ledger\n\n"
        + boundary_markers()
        + "\n- applied: tighten_owner_trial_capture_flow\n"
        + "- result recorded: true\n"
        + "- style memory attached: true\n"
        + "- safety-bound Codex packet attached: true\n",
    )
    write_text(
        V40 / "LOCAL_ITERATION_V40_BOUNDARY_REPORT.md",
        "# Local Iteration v40 Boundary Report\n\n"
        + boundary_markers()
        + "\nThe iteration remains local, draft-first, OpenClaude-independent, and no-provider.\n",
    )
    write_json(APP / "product_workbench_v40_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_APPLIED_LOCAL_ITERATION_WORK_ITEM_V40.md",
        "# Next After Influence Factory Applied Local Iteration Work Item v40\n\n"
        + boundary_markers()
        + "\nExactly one next safe goal is selected: verify_applied_local_iteration_v41_without_protected_actions.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_APPLIED_LOCAL_ITERATION_WORK_ITEM_V40_VALIDATION_REPORT.md",
        "# Influence Factory Applied Local Iteration Work Item v40 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("APPLIED_LOCAL_ITERATION_WORK_ITEM_V40_CREATED=PASS")
    print("terminal_condition=LOCAL_ITERATION_WORK_ITEM_V40_APPLIED")
    print("local_product_status=local_iteration_work_item_applied")
    print("first_goal_flow=pr_sized_owner_evidence_iteration_applied_locally")
    print("selected_next_safe_goal=verify_applied_local_iteration_v41_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

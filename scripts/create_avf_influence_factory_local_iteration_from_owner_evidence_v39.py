from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V38 = (
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
)
V39 = V38 / "local_iteration_from_owner_evidence_v39"
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

WORK_ITEMS = [
    {
        "work_item_id": "tighten_owner_trial_capture_flow",
        "title": "Tighten owner trial capture flow",
        "acceptance": "Owner evidence is captured as a local ledger entry with a visible next improvement.",
    },
    {
        "work_item_id": "attach_style_memory_to_next_iteration",
        "title": "Attach style memory to next iteration",
        "acceptance": "Brand DNA, character bible, visual guide, reference index, and rights notes remain attached.",
    },
    {
        "work_item_id": "preserve_safety_boundary_in_codex_packet",
        "title": "Preserve safety boundary in Codex packet",
        "acceptance": "Codex packet blocks deploy, publish, platform posting, provider calls, and deceptive influence.",
    },
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39_READY",
        "local_product_status": "local_iteration_from_owner_evidence_ready",
        "first_goal_flow": "captured_owner_evidence_to_pr_sized_local_iteration",
        "product_completion_claim_scope": "repo_local_internal_only",
        "selected_next_safe_goal": "apply_local_iteration_work_item_v40_without_protected_actions",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def codex_context_packet() -> dict:
    return {
        "task_id": "owner-evidence-local-iteration-v39",
        "title": "Apply one local improvement from owner trial evidence",
        "relevant_files": [
            "avf/influence_factory/product_app/index.html",
            "avf/influence_factory/product_app/app.js",
            "avf/influence_factory/product_app/styles.css",
        ],
        "acceptance_criteria": [item["acceptance"] for item in WORK_ITEMS],
        "forbidden_changes": [
            "Do not deploy",
            "Do not publish",
            "Do not call providers or live models",
            "Do not add external services",
            "Do not support deceptive influence or platform posting",
        ],
    }


def boundary_markers() -> str:
    return (
        "terminal_condition: LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39_READY\n"
        "first_goal_flow: captured_owner_evidence_to_pr_sized_local_iteration\n"
        "product_completion_claim_scope: repo_local_internal_only\n"
        "external_validation_authorized: false\n"
        "external_validation_executed: false\n"
        "external_validation_claimed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "selected_next_safe_goal: apply_local_iteration_work_item_v40_without_protected_actions\n"
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
    v38 = json.loads((V38 / "owner_trial_evidence_capture_v38_record.json").read_text(encoding="utf-8"))
    if v38.get("terminal_condition") != "OWNER_TRIAL_EVIDENCE_CAPTURE_V38_READY":
        raise SystemExit("v38 owner trial evidence capture record is missing")

    record = base_record()
    context_packet = codex_context_packet()
    packet = {
        **record,
        "iteration_packet_id": "local_iteration_from_owner_evidence_v39",
        "source_gate": "owner_trial_evidence_capture_v38",
        "work_item_queue": WORK_ITEMS,
        "acceptance_criteria": context_packet["acceptance_criteria"],
        "codex_context_packet": context_packet,
    }

    write_json(V39 / "local_iteration_from_owner_evidence_v39_record.json", record)
    write_json(V39 / "OWNER_EVIDENCE_LOCAL_ITERATION_PACKET.json", packet)
    write_json(V39 / "OWNER_EVIDENCE_WORK_ITEM_QUEUE.json", {"work_item_queue": WORK_ITEMS})
    write_json(V39 / "OWNER_EVIDENCE_CODEX_CONTEXT_PACKET.json", context_packet)
    write_text(
        V39 / "OWNER_EVIDENCE_LOCAL_ITERATION_PACKET.md",
        "# Owner Evidence Local Iteration Packet\n\n"
        + boundary_markers()
        + "\nThis packet turns captured owner trial evidence into PR-sized repo-local work items.\n",
    )
    write_text(
        V39 / "OWNER_EVIDENCE_WORK_ITEM_QUEUE.md",
        "# Owner Evidence Work Item Queue\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {item['work_item_id']}: {item['title']} - {item['acceptance']}" for item in WORK_ITEMS)
        + "\n",
    )
    write_text(
        V39 / "OWNER_EVIDENCE_ACCEPTANCE_CRITERIA.md",
        "# Owner Evidence Acceptance Criteria\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {item['acceptance']}" for item in WORK_ITEMS)
        + "\n",
    )
    write_text(
        V39 / "OWNER_EVIDENCE_BOUNDARY_REPORT.md",
        "# Owner Evidence Boundary Report\n\n"
        + boundary_markers()
        + "\nLocal iteration planning stays repo-local and does not execute protected actions.\n",
    )
    write_json(APP / "product_workbench_v39_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39.md",
        "# Next After Influence Factory Local Iteration From Owner Evidence v39\n\n"
        + boundary_markers()
        + "\nExactly one next safe goal is selected: apply_local_iteration_work_item_v40_without_protected_actions.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39_VALIDATION_REPORT.md",
        "# Influence Factory Local Iteration From Owner Evidence v39 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39_CREATED=PASS")
    print("terminal_condition=LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39_READY")
    print("local_product_status=local_iteration_from_owner_evidence_ready")
    print("first_goal_flow=captured_owner_evidence_to_pr_sized_local_iteration")
    print("selected_next_safe_goal=apply_local_iteration_work_item_v40_without_protected_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

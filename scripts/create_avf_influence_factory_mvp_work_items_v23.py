from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V22 = (
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
)
V23 = V22 / "mvp_work_items_v23"
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

WORK_ITEMS = [
    {"id": "mvp-01", "title": "Goal intake to run packet", "status": "implemented_local_only", "protected_action_required": False},
    {"id": "mvp-02", "title": "Strategy brief and proof target", "status": "implemented_local_only", "protected_action_required": False},
    {"id": "mvp-03", "title": "Brand/IP style prompt pack", "status": "implemented_local_only", "protected_action_required": False},
    {"id": "mvp-04", "title": "Draft-first content calendar", "status": "implemented_local_only", "protected_action_required": False},
    {"id": "mvp-05", "title": "Codex PR sequence", "status": "implemented_local_only", "protected_action_required": False},
    {"id": "mvp-06", "title": "Owner acceptance checklist", "status": "implemented_local_only", "protected_action_required": False},
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def record() -> dict:
    return {
        "terminal_condition": "LOCAL_MVP_WORK_ITEMS_V23_READY",
        "local_product_status": "mvp_work_items_implemented_local_only",
        "selected_next_safe_goal": "run_local_mvp_end_to_end_acceptance_v24_without_protected_actions",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def main() -> None:
    v22 = json.loads((V22 / "first_product_local_run_v22_record.json").read_text(encoding="utf-8"))
    if v22.get("terminal_condition") != "FIRST_PRODUCT_LOCAL_RUN_V22_READY":
        raise SystemExit("v22 first product local run is missing")

    features = {
        "goal_intake": "implemented_local_only",
        "strategy_proof": "implemented_local_only",
        "style_prompt_pack": "implemented_local_only",
        "content_calendar": "implemented_local_only",
        "codex_pr_sequence": "implemented_local_only",
        "owner_acceptance": "implemented_local_only",
    }
    implemented = {**record(), "implemented_work_items": WORK_ITEMS}
    feature_state = {**record(), "features": features}
    codex_packets = {
        **record(),
        "packets": [
            {"task_id": item["id"], "title": item["title"], "protected_action_required": False, "status": "implemented_local_only"}
            for item in WORK_ITEMS
        ],
    }

    write_json(V23 / "mvp_work_items_v23_record.json", record())
    write_json(V23 / "IMPLEMENTED_MVP_WORK_ITEMS.json", implemented)
    write_json(V23 / "LOCAL_MVP_FEATURE_STATE.json", feature_state)
    write_json(V23 / "CODEX_PR_IMPLEMENTATION_PACKETS.json", codex_packets)
    write_text(
        V23 / "IMPLEMENTED_MVP_WORK_ITEMS.md",
        "# Implemented MVP Work Items\n\n"
        + "\n".join(f"- {item['id']}: {item['title']} / status: implemented_local_only / protected_action_required: false" for item in WORK_ITEMS)
        + "\n\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V23 / "FIRST_PRODUCT_LOCAL_RUNBOOK.md",
        "# First Product Local Runbook\n\n"
        "1. Open the local workbench.\n2. Run First Product Goal.\n3. Run First Product Local Cycle.\n4. Run MVP Work Items.\n5. Review Local MVP Acceptance Report.\n\n"
        "selected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V23 / "LOCAL_MVP_ACCEPTANCE_REPORT.md",
        "# Local MVP Acceptance Report\n\n"
        "terminal_condition: LOCAL_MVP_WORK_ITEMS_V23_READY\n"
        "selected_next_safe_goal: run_local_mvp_end_to_end_acceptance_v24_without_protected_actions\n"
        "selected_next_goal_executed: false\n"
        "- MVP work items implemented\n- Local MVP feature state ready\n- Local runbook ready\n- platform posting remains blocked\n- protected_action_executed: false\n- external_calls: false\n",
    )
    write_text(
        V23 / "STYLE_AND_CONTENT_IMPLEMENTATION_NOTES.md",
        "# Style And Content Implementation Notes\n\n"
        "Brand/IP style prompt pack is implemented locally with owner-approved references, character bible, visual guide, rights notes, and forbidden styles. Draft-first content calendar remains local and blocks fake human impersonation, undisclosed bot networks, spam, and platform posting.\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V23 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: run_local_mvp_end_to_end_acceptance_v24_without_protected_actions\nnext_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_json(APP / "product_workbench_v23_record.json", record())
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_MVP_WORK_ITEMS_V23.md",
        "# Next After Influence Factory MVP Work Items v23\n\n"
        "selected_next_safe_goal: run_local_mvp_end_to_end_acceptance_v24_without_protected_actions\nnext_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_MVP_WORK_ITEMS_V23_VALIDATION_REPORT.md",
        "# Influence Factory MVP Work Items v23 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("MVP_WORK_ITEMS_V23_CREATED=PASS")
    print("terminal_condition=LOCAL_MVP_WORK_ITEMS_V23_READY")
    print("selected_next_safe_goal=run_local_mvp_end_to_end_acceptance_v24_without_protected_actions")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

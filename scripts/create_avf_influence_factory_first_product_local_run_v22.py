from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V21 = (
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
)
V22 = V21 / "first_product_local_run_v22"
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def record() -> dict:
    return {
        "terminal_condition": "FIRST_PRODUCT_LOCAL_RUN_V22_READY",
        "local_product_status": "first_product_local_run_ready",
        "selected_next_safe_goal": "implement_first_product_local_mvp_work_items_v23_without_protected_actions",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


WORK_ITEMS = [
    {"id": "mvp-01", "title": "Goal intake to run packet", "protected_action_required": False, "status": "ready_for_local_work"},
    {"id": "mvp-02", "title": "Strategy brief and proof target", "protected_action_required": False, "status": "ready_for_local_work"},
    {"id": "mvp-03", "title": "Brand/IP style prompt pack", "protected_action_required": False, "status": "ready_for_local_work"},
    {"id": "mvp-04", "title": "Draft-first content calendar", "protected_action_required": False, "status": "ready_for_local_work"},
    {"id": "mvp-05", "title": "Codex PR sequence", "protected_action_required": False, "status": "ready_for_local_work"},
    {"id": "mvp-06", "title": "Owner acceptance checklist", "protected_action_required": False, "status": "ready_for_local_work"},
]

PR_SEQUENCE = [
    {"id": "pr-01", "title": "Goal intake UI", "protected_action_required": False},
    {"id": "pr-02", "title": "MVP execution board", "protected_action_required": False},
    {"id": "pr-03", "title": "Style prompt pack examples", "protected_action_required": False},
    {"id": "pr-04", "title": "Owner acceptance checklist", "protected_action_required": False},
]


def main() -> None:
    v21 = json.loads((V21 / "first_product_goal_runner_v21_record.json").read_text(encoding="utf-8"))
    if v21.get("terminal_condition") != "FIRST_PRODUCT_GOAL_RUNNER_V21_READY":
        raise SystemExit("v21 first product goal runner is missing")

    base = record()
    board = {**base, "work_items": WORK_ITEMS}
    sequence = {**base, "pr_sequence": PR_SEQUENCE}
    summary = {
        **base,
        "source": "FIRST_PRODUCT_GOAL_RUN_PACKET.json",
        "mvp_work_item_count": len(WORK_ITEMS),
        "codex_pr_count": len(PR_SEQUENCE),
        "safe_reframe": "transparent_creator_brand_media_growth_system",
    }

    write_json(V22 / "first_product_local_run_v22_record.json", base)
    write_json(V22 / "FIRST_PRODUCT_LOCAL_RUN_SUMMARY.json", summary)
    write_json(V22 / "MVP_EXECUTION_BOARD.json", board)
    write_json(V22 / "FIRST_PRODUCT_CODEX_PR_SEQUENCE.json", sequence)
    write_text(
        V22 / "FIRST_PRODUCT_LOCAL_RUN_SUMMARY.md",
        "# First Product Local Run Summary\n\n"
        "terminal_condition: FIRST_PRODUCT_LOCAL_RUN_V22_READY\n"
        "selected_next_safe_goal: implement_first_product_local_mvp_work_items_v23_without_protected_actions\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V22 / "MVP_EXECUTION_BOARD.md",
        "# MVP Execution Board\n\n"
        + "\n".join(f"- {item['id']}: {item['title']} / protected_action_required: false" for item in WORK_ITEMS)
        + "\n\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V22 / "FIRST_PRODUCT_MVP_SPEC.md",
        "# First Product MVP Spec\n\n"
        "Build the local-only Transparent AI Creator Collective workbench around intake, Brand/IP memory, draft content, Codex packets, evidence, and owner review. Do not deploy, publish, post, call providers, or make readiness claims.\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V22 / "FIRST_PRODUCT_CONTENT_CALENDAR.md",
        "# First Product Content Calendar\n\n"
        "- Day 1: proof note\n- Day 2: Brand/IP example\n- Day 3: draft content packet\n- Day 4: owner review digest\n- Day 5: next Codex packet\n\nplatform posting: blocked\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V22 / "FIRST_PRODUCT_STYLE_PROMPT_PACK.md",
        "# First Product Style Prompt Pack\n\n"
        "Use Brand/IP Vault, character bible, visual guide, reference image index, rights notes, and forbidden styles. Block fake human impersonation, undisclosed bot networks, fake crowd visuals, borrowed unlicensed identity, and manipulation motifs.\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V22 / "FIRST_PRODUCT_CODEX_PR_SEQUENCE.md",
        "# First Product Codex PR Sequence\n\n"
        + "\n".join(f"- {item['id']}: {item['title']} / protected_action_required: false" for item in PR_SEQUENCE)
        + "\n\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V22 / "FIRST_PRODUCT_OWNER_ACCEPTANCE_CHECKLIST.md",
        "# First Product Owner Acceptance Checklist\n\n"
        "- MVP execution board exists\n- Codex PR sequence exists\n- Style prompt pack exists\n- Owner acceptance checklist exists\n- platform posting remains blocked\n- protected_action_executed remains false\n- external_calls remains false\n",
    )
    write_text(
        V22 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: implement_first_product_local_mvp_work_items_v23_without_protected_actions\nnext_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_json(APP / "product_workbench_v22_record.json", base)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_FIRST_PRODUCT_LOCAL_RUN_V22.md",
        "# Next After Influence Factory First Product Local Run v22\n\n"
        "selected_next_safe_goal: implement_first_product_local_mvp_work_items_v23_without_protected_actions\nnext_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_FIRST_PRODUCT_LOCAL_RUN_V22_VALIDATION_REPORT.md",
        "# Influence Factory First Product Local Run v22 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("FIRST_PRODUCT_LOCAL_RUN_V22_CREATED=PASS")
    print("terminal_condition=FIRST_PRODUCT_LOCAL_RUN_V22_READY")
    print("selected_next_safe_goal=implement_first_product_local_mvp_work_items_v23_without_protected_actions")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

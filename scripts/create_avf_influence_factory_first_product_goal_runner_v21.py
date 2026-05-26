from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V20 = (
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
)
V21 = V20 / "first_product_goal_runner_v21"
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
        "terminal_condition": "FIRST_PRODUCT_GOAL_RUNNER_V21_READY",
        "local_product_status": "first_product_goal_runner_ready",
        "selected_next_safe_goal": "owner_runs_first_real_product_goal_or_refines_goal_input",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def main() -> None:
    v20 = json.loads((V20 / "local_operating_loop_templates_v20_record.json").read_text(encoding="utf-8"))
    if v20.get("terminal_condition") != "FACTORY_READY_FOR_FIRST_OWNER_PRODUCT_GOAL":
        raise SystemExit("v20 factory ready state is missing")

    goal_input = {
        "product_idea": "Transparent AI Creator Collective / Influence Factory",
        "target_user": "creator, brand, product, and operator teams that need safe AI-assisted content systems",
        "proof_target": "one local run packet with strategy, Brand/IP, content system, Codex packet, evidence ledger, and owner review queue",
        "brand_ip_constraints": "transparent AI disclosure, owner-approved references, stable character bible, style guide, palette, typography, rights notes",
        "blocked_actions": [
            "fake human impersonation",
            "undisclosed bot networks",
            "spam",
            "engagement manipulation",
            "astroturfing",
            "brigading",
            "harassment",
            "platform bypass",
            "platform posting",
            "deploy",
            "publish",
            "provider/live/external calls",
            "release/public/production readiness claims",
        ],
    }
    codex_packet = {
        "task_id": "first-product-local-run-001",
        "goal": "Implement the next local-only workbench improvement after owner review.",
        "context": [
            "avf/influence_factory/product_app/index.html",
            "avf/influence_factory/product_app/app.js",
            "avf/influence_factory/product_app/styles.css",
        ],
        "acceptance_criteria": [
            "local-only behavior is preserved",
            "owner review queue remains visible",
            "style/IP memory remains attached to image prompt packets",
            "protected_action_executed remains false",
        ],
        "forbidden_changes": [
            "deploy",
            "publish",
            "platform posting",
            "personal account automation",
            "provider calls",
            "live model calls",
            "external service calls",
            "readiness claims",
        ],
        "validation": [
            "python scripts/validate_avf_influence_factory_first_product_goal_runner_v21.py",
            "credential pattern scan",
            "browser self-test",
        ],
    }
    run_packet = {
        **record(),
        **goal_input,
        "safe_reframe": "transparent_creator_brand_media_growth_system",
        "strategy_brief": "Position the factory as a transparent, owner-reviewed creator/brand/media growth system with proof-by-result artifacts.",
        "brand_ip_brief": "Every visual or character request must carry Brand/IP Vault, character bible, visual guide, reference index, rights notes, and forbidden styles.",
        "content_system_brief": "Draft-first owned-channel content flows through safety scan and owner approval before any external use.",
        "codex_task_packet": codex_packet,
    }

    write_json(V21 / "first_product_goal_runner_v21_record.json", record())
    write_json(V21 / "FIRST_PRODUCT_GOAL_INPUT.example.json", goal_input)
    write_json(V21 / "FIRST_PRODUCT_GOAL_RUN_PACKET.json", run_packet)
    write_text(
        V21 / "FIRST_PRODUCT_GOAL_RUN_PACKET.md",
        "# First Product Goal Run Packet\n\n"
        "terminal_condition: FIRST_PRODUCT_GOAL_RUNNER_V21_READY\n"
        "selected_next_safe_goal: owner_runs_first_real_product_goal_or_refines_goal_input\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\n"
        "protected_action_executed: false\nexternal_calls: false\n\n"
        "safe_reframe: transparent_creator_brand_media_growth_system\n\n"
        f"product_idea: {goal_input['product_idea']}\n"
        f"target_user: {goal_input['target_user']}\n"
        f"proof_target: {goal_input['proof_target']}\n",
    )
    write_text(
        V21 / "FIRST_PRODUCT_STRATEGY_BRIEF.md",
        "# First Product Strategy Brief\n\n"
        "Create a proof-by-result operating loop for a transparent creator/brand/media growth system. The product wins by turning a raw idea into visible strategy, Brand/IP memory, draft content systems, Codex packets, evidence, and owner review.\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V21 / "FIRST_PRODUCT_BRAND_IP_BRIEF.md",
        "# First Product Brand/IP Brief\n\n"
        "Use owner-approved references, stable character bible, visual guide, palette, typography, rights notes, and forbidden styles. Image generation requests must carry this context and must reject fake human impersonation, undisclosed bot networks, fake crowd visuals, and unlicensed identity borrowing.\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V21 / "FIRST_PRODUCT_CONTENT_SYSTEM_BRIEF.md",
        "# First Product Content System Brief\n\n"
        "Generate draft-first SNS, blog, community, newsletter, short-form, long-form, and media prompt packets. Keep platform posting blocked until explicit owner authorization.\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_json(V21 / "FIRST_PRODUCT_CODEX_TASK_PACKET.json", codex_packet)
    write_text(
        V21 / "FIRST_PRODUCT_EVIDENCE_LEDGER.md",
        "# First Product Evidence Ledger\n\n"
        "- local product goal input captured\n"
        "- strategy brief generated\n"
        "- Brand/IP brief generated\n"
        "- content-system brief generated\n"
        "- Codex task packet generated\n"
        "- owner review queue generated\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V21 / "FIRST_PRODUCT_OWNER_REVIEW_QUEUE.md",
        "# First Product Owner Review Queue\n\n"
        "1. Review product idea and target user.\n"
        "2. Review proof target.\n"
        "3. Review Brand/IP constraints.\n"
        "4. Review Codex task packet.\n"
        "5. Choose: run first real product goal, refine goal input, or request protected authorization packet.\n\n"
        "selected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V21 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: owner_runs_first_real_product_goal_or_refines_goal_input\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_json(APP / "product_workbench_v21_record.json", record())
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_FIRST_PRODUCT_GOAL_RUNNER_V21.md",
        "# Next After Influence Factory First Product Goal Runner v21\n\n"
        "selected_next_safe_goal: owner_runs_first_real_product_goal_or_refines_goal_input\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_FIRST_PRODUCT_GOAL_RUNNER_V21_VALIDATION_REPORT.md",
        "# Influence Factory First Product Goal Runner v21 Validation Report\n\n"
        "RESULT: PENDING_VALIDATION\n",
    )
    print("FIRST_PRODUCT_GOAL_RUNNER_V21_CREATED=PASS")
    print("terminal_condition=FIRST_PRODUCT_GOAL_RUNNER_V21_READY")
    print("selected_next_safe_goal=owner_runs_first_real_product_goal_or_refines_goal_input")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V33 = (
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
)
V34 = V33 / "first_goal_completion_runner_v34"
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

FIRST_GOAL = {
    "idea": "Transparent AI Creator Collective / Influence Factory",
    "target_user": "Owner who wants to turn a raw product, brand, or character-IP idea into a reviewable local execution package.",
    "proof": "A repo-local owner-ready package with strategy, Brand/IP style memory, content drafts, Codex context, evidence, and safety gates.",
}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "FIRST_GOAL_COMPLETION_RUNNER_V34_READY",
        "local_product_status": "first_goal_owner_ready_package_ready",
        "product_completion_claim_scope": "repo_local_internal_only",
        "first_goal_flow": "idea_to_owner_ready_package_without_external_execution",
        "selected_next_safe_goal": None,
        "next_safe_goal_count": 0,
        "selected_next_goal_executed": False,
        "protected_boundary": "external_validation_requires_owner_authorization",
        **FALSE_FLAGS,
    }


def boundary_markers() -> str:
    return (
        "terminal_condition: FIRST_GOAL_COMPLETION_RUNNER_V34_READY\n"
        "first_goal_flow: idea_to_owner_ready_package_without_external_execution\n"
        "product_completion_claim_scope: repo_local_internal_only\n"
        "external_validation_authorized: false\n"
        "external_validation_executed: false\n"
        "external_validation_claimed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "selected_next_safe_goal: null\n"
        "next_safe_goal_count: 0\n"
        "fake human impersonation: blocked\n"
        "undisclosed bot networks: blocked\n"
        "platform posting: blocked\n"
        "release readiness claim: blocked\n"
        "public readiness claim: blocked\n"
        "production readiness claim: blocked\n"
        "external validation claim: blocked\n"
    )


def owner_ready_package(record: dict) -> dict:
    return {
        **record,
        "package_id": "first_goal_owner_ready_package_v34",
        "first_goal": FIRST_GOAL,
        "strategy_packet": {
            "positioning": "A transparent AI creator and product workbench that proves quality through owner-reviewable local artifacts.",
            "success_criteria": [
                "Owner can inspect the strategy and risk boundary.",
                "Owner can reuse Brand/IP and image-generation reference memory.",
                "Owner can hand a Codex context pack to an implementation agent.",
            ],
        },
        "brand_ip_style_memory": {
            "brand_dna": "Transparent, evidence-led, builder-native, safety-bounded.",
            "character_bible": "Every AI persona must disclose AI assistance and stay inside its domain.",
            "visual_style_guide": "Clean editorial product interface, precise typography, no fake social proof.",
            "forbidden_styles": "No bot armies, no fake crowds, no spam visuals, no manipulation motifs.",
            "rights_notes": "Use only owner-provided or properly licensed references.",
        },
        "image_generation_reference_packet": {
            "reference_image_index": "owner-approved references only",
            "positive_prompt": "Use Brand/IP memory, character bible, palette, typography, and rights notes before generating assets.",
            "negative_prompt": "No fake crowds, bot armies, spam visuals, impersonation, or platform-bypass motifs.",
            "provenance_required": True,
        },
        "draft_content_system": {
            "channels": ["SNS", "Blog", "Community", "Newsletter", "Short-form", "Long-form", "Media prompt"],
            "status": "draft_only_owner_review_required",
        },
        "codex_context_pack": {
            "task": "Improve or instantiate the local Influence Factory package for a specific owner idea.",
            "context_files": ["avf/influence_factory/product_app/index.html", "avf/influence_factory/product_app/app.js", "avf/influence_factory/product_app/styles.css"],
            "forbidden_changes": ["No provider calls", "No platform posting", "No deploy", "No deceptive influence", "No public readiness claim"],
        },
        "evidence_ledger": {
            "source": "repo-local generated artifacts and validators",
            "claim_scope": "internal_no_provider_local_evidence_only",
        },
        "safety_review": {
            "blocked": ["fake human impersonation", "undisclosed bot networks", "platform posting", "release readiness claim", "public readiness claim", "production readiness claim", "external validation claim"],
        },
        "owner_decision_request": {
            "next_blocked_action": "external_validation",
            "authorization_default": False,
        },
    }


def main() -> None:
    v33 = json.loads((V33 / "local_distributable_package_v33_record.json").read_text(encoding="utf-8"))
    if v33.get("terminal_condition") != "LOCAL_DISTRIBUTABLE_PACKAGE_V33_READY":
        raise SystemExit("v33 local distributable package record is missing")

    record = base_record()
    package = owner_ready_package(record)
    runner = {
        **record,
        "runner_packet_id": "first_goal_completion_runner_v34",
        "source_gate": "local_distributable_package_v33",
        "input_goal": FIRST_GOAL,
        "outputs": list(package.keys()),
    }

    write_json(V34 / "first_goal_completion_runner_v34_record.json", record)
    write_json(V34 / "FIRST_GOAL_COMPLETION_RUNNER_PACKET.json", runner)
    write_json(V34 / "FIRST_GOAL_OWNER_READY_PACKAGE.json", package)
    write_text(
        V34 / "FIRST_GOAL_COMPLETION_RUNNER_PACKET.md",
        "# First Goal Completion Runner Packet\n\n"
        + boundary_markers()
        + "\nThis runner turns the first owner goal into an owner-ready local package without external execution.\n",
    )
    write_text(
        V34 / "FIRST_GOAL_OWNER_READY_PACKAGE.md",
        "# First Goal Owner-Ready Package\n\n"
        + boundary_markers()
        + "\nSections: strategy_packet, brand_ip_style_memory, image_generation_reference_packet, draft_content_system, codex_context_pack, evidence_ledger, safety_review, owner_decision_request.\n",
    )
    write_text(
        V34 / "OWNER_READY_PACKAGE_INDEX.md",
        "# Owner Ready Package Index\n\n"
        + boundary_markers()
        + "\n- FIRST_GOAL_OWNER_READY_PACKAGE.json\n- FIRST_GOAL_STYLE_MEMORY_EXPORT.md\n- FIRST_GOAL_CODEX_CONTEXT_PACK.md\n- FIRST_GOAL_ONE_CLICK_RUNBOOK.md\n- PROTECTED_BOUNDARY_RECONFIRMATION.md\n",
    )
    write_text(
        V34 / "FIRST_GOAL_STYLE_MEMORY_EXPORT.md",
        "# First Goal Style Memory Export\n\n"
        + boundary_markers()
        + "\nbrand_dna: Transparent, evidence-led, builder-native, safety-bounded.\ncharacter_bible: Every AI persona must disclose AI assistance and stay inside its domain.\nvisual_style_guide: Clean editorial product interface, precise typography, no fake social proof.\nnegative_prompt: No fake crowds, bot armies, spam visuals, impersonation, or platform-bypass motifs.\n",
    )
    write_text(
        V34 / "FIRST_GOAL_CODEX_CONTEXT_PACK.md",
        "# First Goal Codex Context Pack\n\n"
        + boundary_markers()
        + "\nTask: instantiate or improve the local Influence Factory package for one owner idea.\nContext files: avf/influence_factory/product_app/index.html; avf/influence_factory/product_app/app.js; avf/influence_factory/product_app/styles.css.\nForbidden changes: provider calls, platform posting, deploy, deceptive influence, public readiness claim.\n",
    )
    write_text(
        V34 / "FIRST_GOAL_ONE_CLICK_RUNBOOK.md",
        "# First Goal One-Click Runbook\n\n"
        + boundary_markers()
        + "\n1. Open product_app/index.html.\n2. Enter the owner goal in North Star Intake.\n3. Use First Goal Completion Runner.\n4. Review the owner-ready package index.\n5. Stop before external validation unless the owner authorizes it.\n",
    )
    write_text(
        V34 / "PROTECTED_BOUNDARY_RECONFIRMATION.md",
        "# Protected Boundary Reconfirmation\n\n"
        + boundary_markers()
        + "\nThe owner-ready package is internal and repo-local. It does not execute external validation, provider/live model calls, deploy, publish, platform posting, or account automation.\n",
    )
    write_text(
        V34 / "LOCAL_PRODUCT_COMPLETION_TERMINAL_REPORT.md",
        "# Local Product Completion Terminal Report\n\n"
        + boundary_markers()
        + "\nlocal_product_status: first_goal_owner_ready_package_ready\nnext_blocked_action: external_validation\nallowed_final_claim: The local product can produce an owner-ready package for the first goal without executing protected actions.\n",
    )
    write_text(
        V34 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        + boundary_markers()
        + "\nNo next safe autonomous goal is selected from v34. The next meaningful proof step requires explicit owner authorization for external validation.\n",
    )
    write_json(APP / "product_workbench_v34_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_FIRST_GOAL_COMPLETION_RUNNER_V34.md",
        "# Next After Influence Factory First Goal Completion Runner v34\n\n"
        + boundary_markers()
        + "\nNo next safe autonomous goal is selected. Continuing toward external proof requires explicit owner authorization for external validation.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_FIRST_GOAL_COMPLETION_RUNNER_V34_VALIDATION_REPORT.md",
        "# Influence Factory First Goal Completion Runner v34 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("FIRST_GOAL_COMPLETION_RUNNER_V34_CREATED=PASS")
    print("terminal_condition=FIRST_GOAL_COMPLETION_RUNNER_V34_READY")
    print("local_product_status=first_goal_owner_ready_package_ready")
    print("first_goal_flow=idea_to_owner_ready_package_without_external_execution")
    print("product_completion_claim_scope=repo_local_internal_only")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

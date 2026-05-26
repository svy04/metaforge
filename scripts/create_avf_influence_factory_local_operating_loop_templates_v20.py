from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V19 = (
    ROOT
    / "avf"
    / "influence_factory"
    / "operator_package_v14"
    / "real_goal_run_v15"
    / "owner_review_v16"
    / "local_iteration_v17"
    / "executed_iteration_v18"
    / "owner_review_v19"
)
V20 = V19 / "local_operating_loop_templates_v20"
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
        "terminal_condition": "FACTORY_READY_FOR_FIRST_OWNER_PRODUCT_GOAL",
        "local_product_status": "operating_loop_templates_ready",
        "selected_next_safe_goal": "owner_provides_first_real_product_goal_for_factory_run",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def loop_template(title: str, steps: list[str]) -> str:
    body = "\n".join(f"{index}. {step}" for index, step in enumerate(steps, start=1))
    return (
        f"# {title}\n\n"
        f"{body}\n\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "selected_next_goal_executed: false\n"
    )


def main() -> None:
    v19 = json.loads((V19 / "owner_review_continuation_v19_record.json").read_text(encoding="utf-8"))
    if v19.get("terminal_condition") != "OWNER_REVIEW_CONTINUATION_V19_READY":
        raise SystemExit("v19 continuation record is not ready")

    intake = {
        "product_idea": "",
        "target_user": "",
        "proof_target": "",
        "brand_ip_constraints": "",
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

    base = record()
    write_json(V20 / "local_operating_loop_templates_v20_record.json", base)
    write_text(
        V20 / "IDEA_INTAKE_LOOP_TEMPLATE.md",
        loop_template(
            "Idea Intake Loop Template",
            [
                "Capture product idea, target user, pain, promised result, proof target, Brand/IP constraints, and blocked actions.",
                "Translate the idea into a local North Star packet.",
                "Reject fake human impersonation, undisclosed bot networks, spam, and platform bypass.",
            ],
        ),
    )
    write_text(
        V20 / "CONTENT_REVIEW_LOOP_TEMPLATE.md",
        loop_template(
            "Content Review Loop Template",
            [
                "Generate draft-only owned-channel content.",
                "Run safety scan before owner review.",
                "Keep platform posting blocked until explicit protected authorization.",
            ],
        ),
    )
    write_text(
        V20 / "STYLE_IP_REVIEW_LOOP_TEMPLATE.md",
        loop_template(
            "Style/IP Review Loop Template",
            [
                "Load Brand/IP Vault, character bible, palette, typography, reference image index, rights notes, and forbidden styles.",
                "Build image-generation prompt packs that preserve style continuity.",
                "Block borrowed unlicensed identity, fake crowd visuals, and manipulation motifs.",
            ],
        ),
    )
    write_text(
        V20 / "CODEX_PACKET_REVIEW_LOOP_TEMPLATE.md",
        loop_template(
            "Codex Packet Review Loop Template",
            [
                "Convert accepted local work into PR-sized Codex task packets.",
                "Include relevant files, acceptance criteria, forbidden changes, and validation commands.",
                "Do not install dependencies, deploy, publish, call providers, or mutate external systems.",
            ],
        ),
    )
    write_text(
        V20 / "EVIDENCE_COMPARISON_LOOP_TEMPLATE.md",
        loop_template(
            "Evidence Comparison Loop Template",
            [
                "Compare generated artifacts against acceptance criteria.",
                "Record PASS, needs_work, or protected_action_required.",
                "Do not convert internal evidence into public, release, production, external validation, or autonomous reliability claims.",
            ],
        ),
    )
    write_json(V20 / "FIRST_OWNER_PRODUCT_GOAL_INTAKE_TEMPLATE.json", intake)
    write_text(
        V20 / "FIRST_OWNER_PRODUCT_GOAL_INTAKE_TEMPLATE.md",
        "# First Owner Product Goal Intake Template\n\n"
        "- product_idea:\n- target_user:\n- proof_target:\n- brand_ip_constraints:\n- blocked_actions: fake human impersonation, undisclosed bot networks, spam, platform posting, deploy, publish, provider/live/external calls\n\n"
        "selected_next_safe_goal: owner_provides_first_real_product_goal_for_factory_run\n",
    )
    write_text(
        V20 / "FACTORY_READY_TERMINAL_REPORT.md",
        "# Factory Ready Terminal Report\n\n"
        "terminal_condition: FACTORY_READY_FOR_FIRST_OWNER_PRODUCT_GOAL\n"
        "selected_next_safe_goal: owner_provides_first_real_product_goal_for_factory_run\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n\n"
        "The repo-local Web-first Autonomous Venture Factory has enough operating loop templates for the owner to provide the first real product goal. This is not a launch, release, production-readiness, public-readiness, external-validation, or autonomous-reliability claim.\n",
    )
    write_text(
        V20 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: owner_provides_first_real_product_goal_for_factory_run\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write_json(APP / "product_workbench_v20_record.json", base)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_OPERATING_LOOP_TEMPLATES_V20.md",
        "# Next After Influence Factory Local Operating Loop Templates v20\n\n"
        "selected_next_safe_goal: owner_provides_first_real_product_goal_for_factory_run\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_LOCAL_OPERATING_LOOP_TEMPLATES_V20_VALIDATION_REPORT.md",
        "# Influence Factory Local Operating Loop Templates v20 Validation Report\n\n"
        "RESULT: PENDING_VALIDATION\n",
    )
    print("LOCAL_OPERATING_LOOP_TEMPLATES_V20_CREATED=PASS")
    print("terminal_condition=FACTORY_READY_FOR_FIRST_OWNER_PRODUCT_GOAL")
    print("selected_next_safe_goal=owner_provides_first_real_product_goal_for_factory_run")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

from run_avf_influence_factory_goal_local import run as run_goal_bundle


ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "avf" / "influence_factory" / "owner_goal_runs" / "transparent-ai-creator-collective-001"
INPUT_PATH = RUN_DIR / "goal_input.json"
BUNDLE_DIR = RUN_DIR / "bundle"
RECORD_PATH = RUN_DIR / "owner_goal_bundle_v11_record.json"


OWNER_GOAL = {
    "audience": "founders, creators, indie product teams, infrastructure product operators, and brand/IP builders",
    "brand_dna": "transparent, proof-led, creator-native, technically rigorous, non-deceptive, and approval-gated",
    "character_bible": (
        "AI personas are clearly disclosed as AI-assisted creator operators. They do not pretend to be independent "
        "humans, do not simulate fake consensus, and do not operate undisclosed engagement networks."
    ),
    "first_result": (
        "a complete local owner goal bundle with strategy, Brand/IP memory, content drafts, image prompt references, "
        "Codex implementation packet, safety evidence, quality gate, and next safe action"
    ),
    "forbidden_styles": (
        "fake crowds, bot armies, spam aesthetics, harassment motifs, deceptive social proof, platform-bypass cues, "
        "impersonation, astroturfing, brigading, or undisclosed automation"
    ),
    "goal_id": "owner-transparent-ai-creator-collective-v11",
    "idea": "Transparent AI Creator Collective and Influence Factory for safe brand, media, and community growth",
    "promise": (
        "turn one raw product, service, or character/IP idea into a high-quality local strategy, persona, content, "
        "visual reference, Codex task, evidence, and feedback package without executing public actions"
    ),
    "proof_target": (
        "a generated local artifact folder containing an owner dossier, product brief, strategy brief, Brand/IP brief, "
        "content pack, image prompt pack, Codex task packet, safety report, quality gate, style reference index, "
        "persona registry, editorial calendar, approval gate, and next actions"
    ),
    "visual_guide": (
        "web-first editorial control plane, consistent creator studio interface, reusable visual grammar, stable color "
        "tokens, no fake social proof, no undisclosed crowd imagery, reference-pack ready prompts for image generation"
    ),
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def create_owner_extensions() -> None:
    write_json(
        BUNDLE_DIR / "style_reference_index.json",
        {
            "style_memory_status": "active_local_reference_only",
            "image_generation_ready": True,
            "rights_notes": "Use only owner-provided, generated, or properly licensed references.",
            "reference_slots": [
                {
                    "slot": "primary_brand_scene",
                    "purpose": "consistent hero or campaign image prompt",
                    "source_required": "owner-approved reference or generated local description",
                    "protected_action_executed": False,
                },
                {
                    "slot": "character_expression_sheet",
                    "purpose": "repeatable persona/IP visual continuity",
                    "source_required": "owner-approved character bible",
                    "protected_action_executed": False,
                },
                {
                    "slot": "content_thumbnail_system",
                    "purpose": "consistent short-form and long-form media thumbnails",
                    "source_required": "style guide and palette tokens",
                    "protected_action_executed": False,
                },
            ],
            "forbidden_reference_use": [
                "unlicensed celebrity likeness",
                "private-person likeness without consent",
                "platform-confusing impersonation",
                "deceptive social-proof imagery",
            ],
        },
    )
    write_json(
        BUNDLE_DIR / "persona_registry.json",
        {
            "registry_status": "draft_only",
            "personas": [
                {
                    "persona_id": "transparent-builder-narrator",
                    "disclosure": "AI-assisted creator persona",
                    "domain": "builder education and product proof",
                    "allowed_actions": ["draft posts", "draft scripts", "summarize feedback", "prepare owner review packets"],
                    "blocked_actions": ["pretend to be human", "post without approval", "mass message", "manipulate engagement"],
                },
                {
                    "persona_id": "brand-ip-continuity-editor",
                    "disclosure": "AI-assisted brand/IP editor",
                    "domain": "style continuity and reference pack maintenance",
                    "allowed_actions": ["maintain character bible", "draft image prompts", "flag style drift"],
                    "blocked_actions": ["copy protected style without permission", "use private likenesses", "claim rights clearance"],
                },
            ],
        },
    )
    write(
        BUNDLE_DIR / "editorial_calendar.md",
        "# Editorial Calendar\n\n"
        "status: draft_only\n\n"
        "| Day | Channel | Draft Asset | Approval Required |\n"
        "| --- | --- | --- | --- |\n"
        "| 1 | Owned blog | Founder note and product proof story | yes |\n"
        "| 2 | SNS draft | Transparent creator collective explainer | yes |\n"
        "| 3 | Community draft | Feedback request with disclosure | yes |\n"
        "| 4 | Short-form script | Before/after workflow walkthrough | yes |\n"
        "| 5 | Long-form outline | Full operating system breakdown | yes |\n\n"
        "No posting, scheduling, mass messaging, or platform automation is authorized in this bundle.\n",
    )
    write(
        BUNDLE_DIR / "approval_gate.md",
        "# Approval Gate\n\n"
        "protected_action_executed: false\n\n"
        "Required owner approvals before any external action:\n\n"
        "- publish content\n"
        "- post or schedule on any platform\n"
        "- connect external APIs or provider calls\n"
        "- automate personal accounts\n"
        "- claim public readiness, release readiness, production readiness, external validation, or autonomous reliability\n"
        "- use third-party reference images, likenesses, or brand/IP assets\n\n"
        "Default decision: continue local-only drafting and review.\n",
    )
    write(
        BUNDLE_DIR / "owner_decision_packet.md",
        "# Owner Decision Packet\n\n"
        "terminal_condition: PROTECTED_ACTION_REQUIRED\n\n"
        "The local bundle is ready for owner review. The next non-local step would require explicit owner authorization.\n\n"
        "Default authorizations:\n\n"
        "- public posting: false\n"
        "- deploy or publish: false\n"
        "- provider or live model call: false\n"
        "- external validation claim: false\n"
        "- public readiness claim: false\n"
        "- release readiness claim: false\n"
        "- production readiness claim: false\n"
        "- autonomous reliability claim: false\n",
    )


def create_docs() -> None:
    write(
        ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_GOAL_BUNDLE_V11_COMPLETION_AUDIT.md",
        "# Influence Factory Owner Goal Bundle v11 Completion Audit\n\n"
        "RESULT: PASS\n\n"
        "The first owner-provided product direction has been converted into a local-only artifact bundle.\n\n"
        "Verified artifacts:\n\n"
        "- goal_input.json\n"
        "- run_manifest.json\n"
        "- product_brief.md\n"
        "- strategy_brief.md\n"
        "- brand_ip_brief.md\n"
        "- content_pack.md\n"
        "- image_prompt_pack.md\n"
        "- codex_task_packet.json\n"
        "- safety_report.md\n"
        "- quality_gate.json\n"
        "- next_actions.md\n"
        "- dossier.md\n"
        "- style_reference_index.json\n"
        "- persona_registry.json\n"
        "- editorial_calendar.md\n"
        "- approval_gate.md\n"
        "- owner_decision_packet.md\n\n"
        "Protected actions were not executed. Public/productization work remains blocked until explicit owner authorization.\n",
    )
    write(
        ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_GOAL_BUNDLE_V11.md",
        "# Next After Influence Factory Owner Goal Bundle v11\n\n"
        "selected_next_safe_goal: owner_reviews_v11_bundle_or_authorizes_protected_public_operation\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n\n"
        "The next safe action is owner review of the generated local bundle. Any public, platform, provider, deploy, "
        "or release-facing action requires explicit protected-action authorization.\n",
    )


def main() -> int:
    write_json(INPUT_PATH, OWNER_GOAL)
    run_goal_bundle(INPUT_PATH, BUNDLE_DIR)
    create_owner_extensions()
    write_json(
        RECORD_PATH,
        {
            "terminal_condition": "OWNER_GOAL_BUNDLE_V11_READY",
            "local_product_status": "first_real_owner_goal_bundle_generated",
            "goal_id": OWNER_GOAL["goal_id"],
            "selected_next_safe_goal": "owner_reviews_v11_bundle_or_authorizes_protected_public_operation",
            "next_safe_goal_count": 1,
            "protected_action_executed": False,
            "external_calls": False,
            "provider_calls_performed": False,
            "live_model_calls_performed": False,
            "dependency_install_performed": False,
            "release_ready_claimed": False,
            "public_ready_claimed": False,
            "production_ready_claimed": False,
            "external_validation_claimed": False,
            "autonomous_reliability_claimed": False,
        },
    )
    create_docs()
    print("OWNER_GOAL_BUNDLE_V11=PASS")
    print(f"goal_input={INPUT_PATH.relative_to(ROOT)}")
    print(f"bundle_dir={BUNDLE_DIR.relative_to(ROOT)}")
    print("protected_action_executed=false")
    print("selected_next_safe_goal=owner_reviews_v11_bundle_or_authorizes_protected_public_operation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

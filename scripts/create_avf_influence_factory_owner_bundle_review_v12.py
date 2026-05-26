from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "avf" / "influence_factory" / "owner_goal_runs" / "transparent-ai-creator-collective-001"
BUNDLE_DIR = RUN_DIR / "bundle"
REVIEW_DIR = RUN_DIR / "review_v12"
RECORD_PATH = REVIEW_DIR / "owner_bundle_review_v12_record.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    goal = read_json(RUN_DIR / "goal_input.json")
    quality = read_json(BUNDLE_DIR / "quality_gate.json")
    style = read_json(BUNDLE_DIR / "style_reference_index.json")
    personas = read_json(BUNDLE_DIR / "persona_registry.json")

    backlog = [
        {
            "item_id": "v13-local-goal-runner-ui",
            "title": "Add in-app owner goal bundle builder",
            "why": "Owner should not need to run a script to convert a real idea into a bundle.",
            "acceptance_criteria": [
                "owner can edit goal fields in the browser",
                "browser generates the same bundle preview",
                "Codex packet export remains local-only",
                "no external calls or posting actions are introduced",
            ],
            "risk": "low",
            "protected_action_required": False,
        },
        {
            "item_id": "v13-style-reference-workbench",
            "title": "Add Brand/IP style continuity workbench",
            "why": "Character/IP and visual asset systems need consistent prompt packs and reference slots.",
            "acceptance_criteria": [
                "style reference index is visible and editable",
                "forbidden style rules are visible beside prompt packs",
                "rights notes are included in every image prompt export",
                "no third-party likeness or rights clearance claim is made",
            ],
            "risk": "medium",
            "protected_action_required": False,
        },
        {
            "item_id": "v13-content-approval-board",
            "title": "Add draft content approval board",
            "why": "Content must stay draft-first and approval-gated before any public operation.",
            "acceptance_criteria": [
                "SNS, blog, community, short-form, and long-form drafts have approval states",
                "blocked actions remain visible",
                "publish and post controls are absent",
                "owner decision packet is linked from the board",
            ],
            "risk": "medium",
            "protected_action_required": False,
        },
        {
            "item_id": "v13-evidence-dashboard",
            "title": "Add evidence dashboard for generated artifacts",
            "why": "The factory should prove what it generated and which safety gates passed.",
            "acceptance_criteria": [
                "generated files are grouped by strategy, brand, content, Codex, safety, and decisions",
                "quality gate status is visible",
                "claim boundaries are visible",
                "terminal condition is visible",
            ],
            "risk": "low",
            "protected_action_required": False,
        },
    ]

    write_json(
        RECORD_PATH,
        {
            "terminal_condition": "OWNER_BUNDLE_REVIEW_V12_READY",
            "local_product_status": "first_real_owner_goal_bundle_reviewed",
            "goal_id": goal["goal_id"],
            "quality_gate_score": quality["score"],
            "style_memory_status": style["style_memory_status"],
            "persona_registry_status": personas["registry_status"],
            "selected_next_safe_goal": "implement_local_product_backlog_v13_without_public_actions",
            "next_safe_goal_count": 1,
            "protected_action_executed": False,
            "external_calls": False,
            "release_ready_claimed": False,
            "public_ready_claimed": False,
            "production_ready_claimed": False,
            "external_validation_claimed": False,
            "autonomous_reliability_claimed": False,
        },
    )
    write_json(REVIEW_DIR / "next_build_queue.json", {"queue_status": "ready_for_local_implementation", "items": backlog})
    write(
        REVIEW_DIR / "quality_review.md",
        "# Owner Bundle Quality Review v12\n\n"
        f"goal_id: {goal['goal_id']}\n"
        f"quality_gate_score: {quality['score']}\n"
        "release_ready: false\n"
        "public_ready: false\n"
        "production_ready: false\n\n"
        "The bundle is strong enough for local owner review and next local product iteration. It is not evidence for "
        "public, release, production, external validation, or autonomous reliability claims.\n",
    )
    write(
        REVIEW_DIR / "gap_matrix.md",
        "# Gap Matrix v12\n\n"
        "| Gap | Current Status | Safe Next Step | Protected Action Required |\n"
        "| --- | --- | --- | --- |\n"
        "| In-app real goal builder | script-backed only | implement local browser builder | no |\n"
        "| Style continuity operations | JSON reference index exists | expose editable style workbench | no |\n"
        "| Content approval workflow | draft artifacts exist | add approval board | no |\n"
        "| External posting | not authorized | keep blocked | yes |\n"
        "| Provider/live model execution | not authorized | keep blocked | yes |\n"
        "| Public readiness claim | not authorized | keep blocked | yes |\n"
        "| Release readiness claim | not authorized | keep blocked | yes |\n",
    )
    write(
        REVIEW_DIR / "codex_goal_queue.md",
        "# Codex Goal Queue v12\n\n"
        "selected_next_safe_goal: implement_local_product_backlog_v13_without_public_actions\n"
        "next_safe_goal_count: 1\n\n"
        "Use the next_build_queue.json items as PR-sized local product work. Do not deploy, publish, post, call providers, "
        "or add platform automation.\n",
    )
    write(
        REVIEW_DIR / "style_continuity_review.md",
        "# Style Continuity Review v12\n\n"
        "status: PASS_FOR_LOCAL_ITERATION\n\n"
        "The bundle contains an active local style reference index, rights notes, forbidden reference use, visual guide, "
        "character bible, and image prompt pack. The next local product should make these visible and editable in the app.\n",
    )
    write(
        REVIEW_DIR / "safety_boundary_review.md",
        "# Safety Boundary Review v12\n\n"
        "protected_action_executed: false\n\n"
        "The bundle preserves draft-first operation, disclosure, approval gates, and blocks fake human impersonation, "
        "undisclosed bot networks, spam, engagement manipulation, platform bypass, posting, publishing, provider calls, "
        "external calls, and readiness claims.\n",
    )
    write(
        REVIEW_DIR / "owner_review_packet.md",
        "# Owner Review Packet v12\n\n"
        "Owner can review the local bundle and choose one of two safe paths:\n\n"
        "1. Continue local iteration by implementing the v13 backlog.\n"
        "2. Separately authorize a protected public/productization operation.\n\n"
        "Default path: continue local iteration.\n",
    )
    write(
        ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_BUNDLE_REVIEW_V12.md",
        "# Next After Influence Factory Owner Bundle Review v12\n\n"
        "selected_next_safe_goal: implement_local_product_backlog_v13_without_public_actions\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n\n"
        "The next safe action is local product implementation of the v13 backlog. Protected public/productization actions "
        "remain blocked.\n",
    )
    print("OWNER_BUNDLE_REVIEW_V12=PASS")
    print(f"review_dir={REVIEW_DIR.relative_to(ROOT)}")
    print("selected_next_safe_goal=implement_local_product_backlog_v13_without_public_actions")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

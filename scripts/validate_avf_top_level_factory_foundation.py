from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RECORD_PATH = ROOT / "docs" / "goals" / "AUTONOMOUS_FACTORY_FOUNDATION_RECORD.json"

REQUIRED_FILES = [
    "docs/goals/GOAL_OS_SPEC.md",
    "docs/goals/GOAL_HIERARCHY.md",
    "docs/goals/GOAL_STATE_MACHINE.md",
    "docs/goals/GOAL_VALIDATION_RULES.md",
    "docs/goals/NEXT_AFTER_GOAL_OS.md",
    "docs/goals/AUTONOMOUS_FACTORY_TERMINAL_REPORT.md",
    "docs/goals/AUTONOMOUS_FACTORY_COMPLETION_AUDIT.md",
    "docs/goals/AUTONOMOUS_FACTORY_FOUNDATION_RECORD.json",
    "docs/avf/WEB_FIRST_AUTONOMOUS_VENTURE_FACTORY_SPEC.md",
    "docs/avf/INFRA_PRODUCT_EXPANSION_CELL_SPEC.md",
    "avf/dna/strategy_dna.md",
    "avf/dna/product_dna.md",
    "avf/dna/brand_dna.md",
    "avf/dna/code_dna.md",
    "avf/dna/marketing_dna.md",
    "avf/dna/support_dna.md",
    "avf/dna/forbidden_actions.md",
    "avf/roles/role_catalog.yml",
    "avf/router/routing_rules.yml",
    "avf/router/risk_policy.yml",
    "avf/router/quota_policy.yml",
    "avf/tasks/task_packet.schema.yml",
    "avf/tasks/context_pack.schema.yml",
    "avf/evidence/evidence_ledger.schema.yml",
    "avf/evidence/result_memory.schema.yml",
    "avf/evidence/feedback_registry.schema.yml",
    "avf/evidence/experiment_registry.schema.yml",
    "avf/runbooks/first_goal_intake.md",
    "avf/runbooks/codex_execution_lane.md",
    "avf/runbooks/approval_gates.md",
    "avf/goals/first_real_user_goal_intake_packet.md",
    "avf/infra_product/pain_discovery_packet.md",
    "avf/infra_product/technical_empathy_map.md",
    "avf/infra_product/implementation_feasibility_map.md",
    "avf/infra_product/sre_slo_review_packet.md",
    "avf/infra_product/data_evidence_packet.md",
    "avf/brand_ip/brand_dna.schema.yml",
    "avf/brand_ip/character_bible.schema.yml",
    "avf/brand_ip/visual_style_guide.schema.yml",
    "avf/brand_ip/palette_tokens.schema.yml",
    "avf/brand_ip/typography_tokens.schema.yml",
    "avf/brand_ip/prompt_pack.schema.yml",
    "avf/brand_ip/forbidden_style.schema.yml",
    "avf/brand_ip/reference_image_index.schema.yml",
    "avf/brand_ip/asset_registry.schema.yml",
    "avf/brand_ip/generated_asset_provenance.schema.yml",
    "avf/brand_ip/usage_rights_notes.schema.yml",
    "avf/influence_factory/product_track_spec.md",
    "avf/influence_factory/ai_persona_policy.md",
    "avf/influence_factory/persona_registry.schema.yml",
    "avf/influence_factory/content_pipeline_map.md",
    "avf/influence_factory/editorial_calendar.schema.yml",
    "avf/influence_factory/platform_policy_boundary_map.md",
    "avf/influence_factory/growth_experiment.schema.yml",
    "avf/influence_factory/community_feedback.schema.yml",
    "avf/influence_factory/unsafe_influence_rejection_rules.md",
    "avf/influence_factory/content_pipeline/sns_posts.md",
    "avf/influence_factory/content_pipeline/blog_posts.md",
    "avf/influence_factory/content_pipeline/community_posts.md",
    "avf/influence_factory/content_pipeline/newsletter_drafts.md",
    "avf/influence_factory/content_pipeline/short_form_scripts.md",
    "avf/influence_factory/content_pipeline/long_form_scripts.md",
    "avf/influence_factory/content_pipeline/media_prompts.md",
    "avf/influence_factory/content_pipeline/comment_response_drafts.md",
    "avf/codex_lane/codex_task_packet.template.yml",
    "avf/codex_lane/context_pack.template.yml",
    "avf/codex_lane/pr_sized_rules.md",
    "avf/codex_lane/forbidden_changes.md",
    "avf/codex_lane/acceptance_criteria.template.md",
    "avf/codex_lane/validation_report.template.md",
    "avf/codex_lane/next_pr_recommendation.template.md",
]

REQUIRED_SAFETY_PHRASES = [
    "fake human impersonation",
    "undisclosed bot networks",
    "spam comments",
    "mass posting without approval",
    "engagement manipulation",
    "astroturfing",
    "brigading",
    "harassment",
    "platform bypass",
    "personal account automation",
]

BLOCKED_RECORD_FLAGS = [
    "openclaude_required",
    "meta_mfh_rewrite_performed",
    "dependency_install_performed",
    "deploy_performed",
    "publish_performed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "release_readiness_claimed",
    "public_readiness_claimed",
    "production_readiness_claimed",
    "protected_action_executed",
    "deceptive_influence_supported",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(message: str) -> None:
    print(f"RESULT: FAIL")
    print(message)
    sys.exit(1)


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    try:
        record = json.loads(read_text(RECORD_PATH))
    except Exception as exc:  # pragma: no cover - command-line guard
        fail(f"Could not parse record JSON: {exc}")

    if record.get("terminal_condition") != "FACTORY_FOUNDATION_READY":
        fail("terminal_condition must be FACTORY_FOUNDATION_READY")

    if record.get("selected_next_safe_goal") != "collect_first_real_user_goal_inputs":
        fail("selected_next_safe_goal must be collect_first_real_user_goal_inputs")

    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")

    for key in BLOCKED_RECORD_FLAGS:
        if record.get(key) is not False:
            fail(f"{key} must be false")

    if record.get("local_validation_status") != "PASS":
        fail("local_validation_status must be PASS")

    safety_text = read_text(ROOT / "docs" / "goals" / "GOAL_VALIDATION_RULES.md").lower()
    rejection_text = read_text(
        ROOT / "avf" / "influence_factory" / "unsafe_influence_rejection_rules.md"
    ).lower()
    combined = safety_text + "\n" + rejection_text
    missing_phrases = [phrase for phrase in REQUIRED_SAFETY_PHRASES if phrase not in combined]
    if missing_phrases:
        fail("Missing safety phrases:\n" + "\n".join(missing_phrases))

    next_text = read_text(ROOT / "docs" / "goals" / "NEXT_AFTER_GOAL_OS.md")
    if next_text.count("selected_next_safe_goal: collect_first_real_user_goal_inputs") != 1:
        fail("NEXT_AFTER_GOAL_OS.md must contain exactly one selected next safe goal")

    terminal_text = read_text(ROOT / "docs" / "goals" / "AUTONOMOUS_FACTORY_TERMINAL_REPORT.md")
    if "No protected action was executed." not in terminal_text:
        fail("Terminal report must state that no protected action was executed")

    audit_text = read_text(ROOT / "docs" / "goals" / "AUTONOMOUS_FACTORY_COMPLETION_AUDIT.md")
    if audit_text.count("status: PROVEN") < 20:
        fail("Completion audit must prove at least 20 explicit requirements")
    if "status: MISSING" in audit_text or "status: UNVERIFIED" in audit_text:
        fail("Completion audit must not contain missing or unverified requirements")

    print("AVF top-level factory foundation validation")
    print("RESULT: PASS")
    print("terminal_condition=FACTORY_FOUNDATION_READY")
    print("selected_next_safe_goal=collect_first_real_user_goal_inputs")
    print("next_safe_goal_count=1")
    print("openclaude_required=false")
    print("protected_action_executed=false")
    print("deceptive_influence_supported=false")


if __name__ == "__main__":
    main()

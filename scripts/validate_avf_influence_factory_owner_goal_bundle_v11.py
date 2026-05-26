from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "avf" / "influence_factory" / "owner_goal_runs" / "transparent-ai-creator-collective-001"
BUNDLE_DIR = RUN_DIR / "bundle"
RECORD_PATH = RUN_DIR / "owner_goal_bundle_v11_record.json"

REQUIRED_FILES = [
    RUN_DIR / "goal_input.json",
    RECORD_PATH,
    BUNDLE_DIR / "run_manifest.json",
    BUNDLE_DIR / "product_brief.md",
    BUNDLE_DIR / "strategy_brief.md",
    BUNDLE_DIR / "brand_ip_brief.md",
    BUNDLE_DIR / "content_pack.md",
    BUNDLE_DIR / "image_prompt_pack.md",
    BUNDLE_DIR / "codex_task_packet.json",
    BUNDLE_DIR / "safety_report.md",
    BUNDLE_DIR / "quality_gate.json",
    BUNDLE_DIR / "next_actions.md",
    BUNDLE_DIR / "dossier.md",
    BUNDLE_DIR / "style_reference_index.json",
    BUNDLE_DIR / "persona_registry.json",
    BUNDLE_DIR / "editorial_calendar.md",
    BUNDLE_DIR / "approval_gate.md",
    BUNDLE_DIR / "owner_decision_packet.md",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_GOAL_BUNDLE_V11_COMPLETION_AUDIT.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_GOAL_BUNDLE_V11.md",
]

FALSE_RECORD_FLAGS = [
    "protected_action_executed",
    "external_calls",
    "provider_calls_performed",
    "live_model_calls_performed",
    "dependency_install_performed",
    "release_ready_claimed",
    "public_ready_claimed",
    "production_ready_claimed",
    "external_validation_claimed",
    "autonomous_reliability_claimed",
]

UNSAFE_CLAIM_MARKERS = [
    "release ready",
    "production ready",
    "public ready",
    "external validation completed",
    "autonomous reliability proven",
    "provider-backed execution completed",
    "live model validation completed",
]

REQUIRED_BOUNDARY_MARKERS = [
    "post without approval",
    "mass message",
    "manipulate engagement",
    "protected_action_executed: false",
    "Default authorizations",
    "No posting, scheduling, mass messaging, or platform automation is authorized",
]


def fail(message: str) -> None:
    print("Influence Factory owner goal bundle v11 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    goal = read_json(RUN_DIR / "goal_input.json")
    if goal.get("goal_id") != "owner-transparent-ai-creator-collective-v11":
        fail("owner goal input id mismatch")
    for phrase in ["Transparent AI Creator Collective", "without executing public actions", "reference-pack ready"]:
        if phrase not in json.dumps(goal, sort_keys=True):
            fail(f"owner goal input missing phrase: {phrase}")

    record = read_json(RECORD_PATH)
    if record.get("terminal_condition") != "OWNER_GOAL_BUNDLE_V11_READY":
        fail("terminal_condition must be OWNER_GOAL_BUNDLE_V11_READY")
    if record.get("local_product_status") != "first_real_owner_goal_bundle_generated":
        fail("local_product_status mismatch")
    if record.get("selected_next_safe_goal") != "owner_reviews_v11_bundle_or_authorizes_protected_public_operation":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")
    for flag in FALSE_RECORD_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    manifest = read_json(BUNDLE_DIR / "run_manifest.json")
    quality = read_json(BUNDLE_DIR / "quality_gate.json")
    codex = read_json(BUNDLE_DIR / "codex_task_packet.json")
    style = read_json(BUNDLE_DIR / "style_reference_index.json")
    personas = read_json(BUNDLE_DIR / "persona_registry.json")

    if manifest.get("protected_action_executed") is not False:
        fail("manifest protected_action_executed must be false")
    for field in ["release_ready", "public_ready", "production_ready", "external_validation_complete", "autonomous_reliability_proven"]:
        if quality.get(field) is not False:
            fail(f"quality gate {field} must be false")
    if "forbidden_changes" not in codex:
        fail("codex task packet missing forbidden_changes")
    for forbidden in ["deploy", "publish", "provider calls", "platform posting", "account automation", "deceptive influence support"]:
        if forbidden not in codex["forbidden_changes"]:
            fail(f"codex forbidden_changes missing {forbidden}")
    if style.get("style_memory_status") != "active_local_reference_only":
        fail("style reference index must be active local reference only")
    if style.get("image_generation_ready") is not True:
        fail("style reference index must be image-generation ready")
    if personas.get("registry_status") != "draft_only":
        fail("persona registry must remain draft_only")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    lower_combined = combined.lower()
    for marker in UNSAFE_CLAIM_MARKERS:
        if marker in lower_combined:
            fail(f"unsafe claim marker present: {marker}")
    for marker in REQUIRED_BOUNDARY_MARKERS:
        if marker not in combined:
            fail(f"required boundary marker missing: {marker}")

    next_text = read(ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_GOAL_BUNDLE_V11.md")
    if next_text.count("selected_next_safe_goal: owner_reviews_v11_bundle_or_authorizes_protected_public_operation") != 1:
        fail("NEXT_AFTER must contain exactly one selected next safe goal")
    if "selected_next_goal_executed: false" not in next_text:
        fail("NEXT_AFTER must keep selected_next_goal_executed=false")

    print("Influence Factory owner goal bundle v11 validation")
    print("RESULT: PASS")
    print("terminal_condition=OWNER_GOAL_BUNDLE_V11_READY")
    print("local_product_status=first_real_owner_goal_bundle_generated")
    print("selected_next_safe_goal=owner_reviews_v11_bundle_or_authorizes_protected_public_operation")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

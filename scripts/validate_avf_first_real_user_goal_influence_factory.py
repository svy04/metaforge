from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "transparent-ai-creator-collective-001"
TRACK_DIR = ROOT / "avf" / "influence_factory" / "active" / TRACK_ID
RECORD_PATH = TRACK_DIR / "track_record.json"

REQUIRED_FILES = [
    "docs/goals/FIRST_REAL_USER_GOAL_INTAKE_RECORD.json",
    "docs/goals/FIRST_REAL_USER_GOAL_COMPLETION_AUDIT.md",
    "docs/goals/FIRST_REAL_USER_GOAL_VALIDATION_REPORT.md",
    "docs/goals/NEXT_AFTER_FIRST_REAL_USER_GOAL.md",
    "docs/goals/FIRST_REAL_USER_GOAL_TERMINAL_REPORT.md",
    f"avf/influence_factory/active/{TRACK_ID}/00_PRODUCT_TRACK_PACKET.md",
    f"avf/influence_factory/active/{TRACK_ID}/track_record.json",
    f"avf/influence_factory/active/{TRACK_ID}/product_strategy.md",
    f"avf/influence_factory/active/{TRACK_ID}/product_requirements.md",
    f"avf/influence_factory/active/{TRACK_ID}/safe_influence_policy.md",
    f"avf/influence_factory/active/{TRACK_ID}/persona_network_blueprint.md",
    f"avf/influence_factory/active/{TRACK_ID}/content_operating_system.md",
    f"avf/influence_factory/active/{TRACK_ID}/content_channel_matrix.md",
    f"avf/influence_factory/active/{TRACK_ID}/brand_ip_style_memory_starter.md",
    f"avf/influence_factory/active/{TRACK_ID}/image_generation_reference_packet.md",
    f"avf/influence_factory/active/{TRACK_ID}/growth_experiment_backlog.md",
    f"avf/influence_factory/active/{TRACK_ID}/feedback_loop_plan.md",
    f"avf/influence_factory/active/{TRACK_ID}/evidence_ledger_initial.md",
    f"avf/influence_factory/active/{TRACK_ID}/codex_task_queue.md",
    f"avf/influence_factory/active/{TRACK_ID}/owner_approval_gate.md",
    f"avf/influence_factory/active/{TRACK_ID}/terminal_report.md",
]

REQUIRED_TEXT = {
    "safe_influence_policy.md": [
        "fake human impersonation",
        "undisclosed bot networks",
        "spam",
        "mass posting without approval",
        "engagement manipulation",
        "astroturfing",
        "brigading",
        "harassment",
        "platform bypass",
        "personal account automation",
    ],
    "persona_network_blueprint.md": [
        "transparent ai persona",
        "disclosure",
        "owned channel",
    ],
    "codex_task_queue.md": [
        "next_safe_task_count: 1",
        "build_local_influence_factory_intake_dashboard",
    ],
    "image_generation_reference_packet.md": [
        "brand dna",
        "character bible",
        "visual style guide",
        "negative prompt",
        "reference image index",
    ],
}

FALSE_FLAGS = [
    "openclaude_required",
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "dependency_install_performed",
    "deploy_performed",
    "publish_performed",
    "platform_posting_performed",
    "personal_account_automation_performed",
    "deceptive_influence_supported",
    "release_readiness_claimed",
    "public_readiness_claimed",
    "production_readiness_claimed",
]


def fail(message: str) -> None:
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    record = json.loads(read(RECORD_PATH))
    if record.get("terminal_condition") != "FACTORY_PRODUCT_TRACK_READY":
        fail("terminal_condition must be FACTORY_PRODUCT_TRACK_READY")
    if record.get("track_id") != TRACK_ID:
        fail(f"track_id must be {TRACK_ID}")
    if record.get("selected_next_safe_goal") != "build_local_influence_factory_intake_dashboard":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    for filename, phrases in REQUIRED_TEXT.items():
        content = read(TRACK_DIR / filename).lower()
        missing_phrases = [phrase for phrase in phrases if phrase not in content]
        if missing_phrases:
            fail(f"{filename} missing phrases:\n" + "\n".join(missing_phrases))

    audit = read(ROOT / "docs" / "goals" / "FIRST_REAL_USER_GOAL_COMPLETION_AUDIT.md")
    if audit.count("status: PROVEN") < 25:
        fail("completion audit must include at least 25 PROVEN requirements")
    if "status: MISSING" in audit or "status: UNVERIFIED" in audit:
        fail("completion audit contains missing or unverified status")

    next_text = read(ROOT / "docs" / "goals" / "NEXT_AFTER_FIRST_REAL_USER_GOAL.md")
    if next_text.count("selected_next_safe_goal: build_local_influence_factory_intake_dashboard") != 1:
        fail("NEXT_AFTER_FIRST_REAL_USER_GOAL.md must select exactly one next safe goal")

    print("AVF first real user goal influence factory validation")
    print("RESULT: PASS")
    print("terminal_condition=FACTORY_PRODUCT_TRACK_READY")
    print(f"track_id={TRACK_ID}")
    print("selected_next_safe_goal=build_local_influence_factory_intake_dashboard")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("deceptive_influence_supported=false")


if __name__ == "__main__":
    main()

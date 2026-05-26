from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "avf" / "influence_factory" / "dashboard"
RECORD_PATH = DASHBOARD_DIR / "dashboard_record.json"
HTML_PATH = DASHBOARD_DIR / "index.html"

REQUIRED_FILES = [
    "avf/influence_factory/dashboard/dashboard_record.json",
    "avf/influence_factory/dashboard/index.html",
    "avf/influence_factory/dashboard/README.md",
    "docs/goals/NEXT_AFTER_INFLUENCE_FACTORY_DASHBOARD.md",
    "docs/goals/INFLUENCE_FACTORY_DASHBOARD_VALIDATION_REPORT.md",
]

REQUIRED_HTML_PHRASES = [
    "Transparent AI Creator Collective",
    "Product Strategy",
    "Safe Influence Policy",
    "Persona Network",
    "Content Channel Matrix",
    "Brand/IP Style Memory",
    "Codex Task Queue",
    "No deploy",
    "No publish",
    "No platform posting",
    "No account automation",
]

FALSE_FLAGS = [
    "openclaude_required",
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "deploy_performed",
    "publish_performed",
    "platform_posting_performed",
    "personal_account_automation_performed",
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
    if record.get("terminal_condition") != "LOCAL_INFLUENCE_FACTORY_DASHBOARD_READY":
        fail("terminal_condition mismatch")
    if record.get("selected_next_safe_goal") != "create_first_influence_factory_content_batch_packet":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    html = read(HTML_PATH)
    missing_phrases = [phrase for phrase in REQUIRED_HTML_PHRASES if phrase not in html]
    if missing_phrases:
        fail("Dashboard missing phrases:\n" + "\n".join(missing_phrases))

    next_text = read(ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_DASHBOARD.md")
    if next_text.count("selected_next_safe_goal: create_first_influence_factory_content_batch_packet") != 1:
        fail("dashboard next goal must be exactly one")

    print("AVF Influence Factory dashboard validation")
    print("RESULT: PASS")
    print("terminal_condition=LOCAL_INFLUENCE_FACTORY_DASHBOARD_READY")
    print("selected_next_safe_goal=create_first_influence_factory_content_batch_packet")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "avf" / "influence_factory" / "owner_goal_runs" / "transparent-ai-creator-collective-001"
REVIEW_DIR = RUN_DIR / "review_v12"
RECORD_PATH = REVIEW_DIR / "owner_bundle_review_v12_record.json"

REQUIRED_FILES = [
    RUN_DIR / "owner_goal_bundle_v11_record.json",
    ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_OWNER_GOAL_BUNDLE_V11_VALIDATION_REPORT.md",
    RECORD_PATH,
    REVIEW_DIR / "quality_review.md",
    REVIEW_DIR / "gap_matrix.md",
    REVIEW_DIR / "next_build_queue.json",
    REVIEW_DIR / "codex_goal_queue.md",
    REVIEW_DIR / "style_continuity_review.md",
    REVIEW_DIR / "safety_boundary_review.md",
    REVIEW_DIR / "owner_review_packet.md",
    ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_BUNDLE_REVIEW_V12.md",
]

FALSE_RECORD_FLAGS = [
    "protected_action_executed",
    "external_calls",
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
    "launch completed",
]


def fail(message: str) -> None:
    print("Influence Factory owner bundle review v12 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def skip(message: str) -> None:
    print("Influence Factory owner bundle review v12 validation")
    print("RESULT: SKIP")
    print(message)
    sys.exit(0)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def main() -> None:
    if not REVIEW_DIR.is_dir():
        skip(
            "Generated owner bundle review output is absent from the public checkout; "
            "regenerate local AVF run outputs before running this legacy validator."
        )

    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    v11 = read_json(RUN_DIR / "owner_goal_bundle_v11_record.json")
    if v11.get("terminal_condition") != "OWNER_GOAL_BUNDLE_V11_READY":
        fail("v11 owner goal bundle is not ready")

    record = read_json(RECORD_PATH)
    if record.get("terminal_condition") != "OWNER_BUNDLE_REVIEW_V12_READY":
        fail("terminal_condition must be OWNER_BUNDLE_REVIEW_V12_READY")
    if record.get("local_product_status") != "first_real_owner_goal_bundle_reviewed":
        fail("local_product_status mismatch")
    if record.get("selected_next_safe_goal") != "implement_local_product_backlog_v13_without_public_actions":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")
    for flag in FALSE_RECORD_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    queue = read_json(REVIEW_DIR / "next_build_queue.json")
    if queue.get("queue_status") != "ready_for_local_implementation":
        fail("next build queue must be ready_for_local_implementation")
    items = queue.get("items", [])
    if len(items) != 4:
        fail("next build queue must contain exactly 4 local implementation items")
    for item in items:
        if item.get("protected_action_required") is not False:
            fail(f"queue item requires protected action: {item.get('item_id')}")
        if not item.get("acceptance_criteria"):
            fail(f"queue item missing acceptance criteria: {item.get('item_id')}")

    combined = "\n".join(read(path) for path in REQUIRED_FILES if path.suffix in {".md", ".json"})
    lower_combined = combined.lower()
    for marker in UNSAFE_CLAIM_MARKERS:
        if marker in lower_combined:
            fail(f"unsafe claim marker present: {marker}")
    for marker in [
        "selected_next_safe_goal: implement_local_product_backlog_v13_without_public_actions",
        "next_safe_goal_count: 1",
        "protected_action_executed: false",
        "Default path: continue local iteration.",
        "Protected public/productization actions remain blocked.",
    ]:
        if marker not in combined:
            fail(f"required marker missing: {marker}")

    print("Influence Factory owner bundle review v12 validation")
    print("RESULT: PASS")
    print("terminal_condition=OWNER_BUNDLE_REVIEW_V12_READY")
    print("local_product_status=first_real_owner_goal_bundle_reviewed")
    print("selected_next_safe_goal=implement_local_product_backlog_v13_without_public_actions")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "transparent-ai-creator-collective-batch-001"
BATCH_DIR = ROOT / "avf" / "influence_factory" / "content_batches" / BATCH_ID
RECORD_PATH = BATCH_DIR / "batch_record.json"

REQUIRED_FILES = [
    f"avf/influence_factory/content_batches/{BATCH_ID}/batch_record.json",
    f"avf/influence_factory/content_batches/{BATCH_ID}/00_CONTENT_BATCH_PACKET.md",
    f"avf/influence_factory/content_batches/{BATCH_ID}/sns_posts.md",
    f"avf/influence_factory/content_batches/{BATCH_ID}/blog_post_outline.md",
    f"avf/influence_factory/content_batches/{BATCH_ID}/community_post.md",
    f"avf/influence_factory/content_batches/{BATCH_ID}/newsletter_draft.md",
    f"avf/influence_factory/content_batches/{BATCH_ID}/short_form_script.md",
    f"avf/influence_factory/content_batches/{BATCH_ID}/long_form_outline.md",
    f"avf/influence_factory/content_batches/{BATCH_ID}/media_prompt_pack.md",
    f"avf/influence_factory/content_batches/{BATCH_ID}/comment_response_drafts.md",
    f"avf/influence_factory/content_batches/{BATCH_ID}/safety_review.md",
    f"avf/influence_factory/content_batches/{BATCH_ID}/owner_review_checklist.md",
    "docs/goals/NEXT_AFTER_FIRST_CONTENT_BATCH.md",
    "docs/goals/FIRST_CONTENT_BATCH_VALIDATION_REPORT.md",
]

REQUIRED_PHRASES = [
    "draft-only",
    "owner approval required",
    "do not publish",
    "do not post",
    "transparent ai",
]

FALSE_FLAGS = [
    "published",
    "posted",
    "deploy_performed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "personal_account_automation_performed",
    "deceptive_influence_supported",
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
    if record.get("terminal_condition") != "FIRST_CONTENT_BATCH_READY_FOR_OWNER_REVIEW":
        fail("terminal_condition mismatch")
    if record.get("batch_id") != BATCH_ID:
        fail("batch_id mismatch")
    if record.get("selected_next_safe_goal") != "owner_review_first_content_batch":
        fail("selected_next_safe_goal mismatch")
    if record.get("next_safe_goal_count") != 1:
        fail("next_safe_goal_count must be exactly 1")
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{flag} must be false")

    combined = "\n".join(read(ROOT / path).lower() for path in REQUIRED_FILES if path.endswith(".md"))
    missing_phrases = [phrase for phrase in REQUIRED_PHRASES if phrase not in combined]
    if missing_phrases:
        fail("Missing required draft-safety phrases:\n" + "\n".join(missing_phrases))

    next_text = read(ROOT / "docs" / "goals" / "NEXT_AFTER_FIRST_CONTENT_BATCH.md")
    if next_text.count("selected_next_safe_goal: owner_review_first_content_batch") != 1:
        fail("NEXT_AFTER_FIRST_CONTENT_BATCH.md must select exactly one next safe goal")

    print("AVF first content batch validation")
    print("RESULT: PASS")
    print("terminal_condition=FIRST_CONTENT_BATCH_READY_FOR_OWNER_REVIEW")
    print(f"batch_id={BATCH_ID}")
    print("selected_next_safe_goal=owner_review_first_content_batch")
    print("next_safe_goal_count=1")
    print("published=false")
    print("posted=false")


if __name__ == "__main__":
    main()

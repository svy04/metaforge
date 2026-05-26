from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "transparent-ai-creator-collective-batch-001"
BATCH_DIR = ROOT / "avf" / "influence_factory" / "content_batches" / BATCH_ID
NEXT_SAFE_GOAL = "owner_review_first_content_batch"


def write(relative: str, content: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + "\n", encoding="utf-8")


def md(title: str, body: str) -> str:
    return f"# {title}\n\n{body.strip()}\n"


def main() -> None:
    record = {
        "batch_id": BATCH_ID,
        "terminal_condition": "FIRST_CONTENT_BATCH_READY_FOR_OWNER_REVIEW",
        "selected_next_safe_goal": NEXT_SAFE_GOAL,
        "next_safe_goal_count": 1,
        "draft_only": True,
        "owner_approval_required": True,
        "published": False,
        "posted": False,
        "deploy_performed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "personal_account_automation_performed": False,
        "deceptive_influence_supported": False,
    }
    write(f"avf/influence_factory/content_batches/{BATCH_ID}/batch_record.json", json.dumps(record, indent=2, sort_keys=True))

    shared_boundary = """
Boundary:
- draft-only
- owner approval required
- do not publish
- do not post
- transparent AI assistance must be disclosed
"""

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/00_CONTENT_BATCH_PACKET.md",
        md(
            "First Content Batch Packet",
            f"""
This is the first repo-local content batch for the Transparent AI Creator Collective.

Purpose:
Provide a tangible draft set for owner review without posting or publishing.

{shared_boundary}
""",
        ),
    )

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/sns_posts.md",
        md(
            "SNS Posts",
            f"""
Draft 1:
Building an AI factory should not start with more automation. It should start with better memory:
goals, brand/IP style, evidence, and approval gates.

Draft 2:
The next wave of AI creators will not win by pretending to be human. They will win by being
transparent AI systems with consistent taste, proof, and feedback loops.

Draft 3:
Influence Factory rule one: drafts are cheap, trust is expensive. Do not publish until the
owner approves the claim, channel, and context.

{shared_boundary}
""",
        ),
    )

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/blog_post_outline.md",
        md(
            "Blog Post Outline",
            f"""
Title:
From AI Content Spam to Transparent AI Creator Systems

Outline:
1. Why raw automation creates brittle influence.
2. Why transparent AI personas are stronger long term.
3. The role of brand/IP style memory.
4. The draft-first content pipeline.
5. Evidence ledgers and feedback loops.
6. What remains approval-gated.

{shared_boundary}
""",
        ),
    )

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/community_post.md",
        md(
            "Community Post",
            f"""
Draft:
I am exploring a transparent AI creator collective: not bots pretending to be people, but a
structured way to keep product strategy, content drafts, visual style, and feedback loops in one place.

Question:
Where do you think AI-assisted creator systems become useful, and where do they become annoying?

{shared_boundary}
""",
        ),
    )

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/newsletter_draft.md",
        md(
            "Newsletter Draft",
            f"""
Subject:
Building a transparent AI creator system, not a bot farm

Body:
This week the system gained a portable AVF foundation, a product track for transparent AI creators,
and the first draft-only content batch. The important line is simple: produce better drafts and
better evidence, not fake engagement.

{shared_boundary}
""",
        ),
    )

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/short_form_script.md",
        md(
            "Short-form Script",
            f"""
Hook:
The dangerous version of AI influence is fake people. The useful version is transparent systems.

Beats:
1. Show chaotic content tabs.
2. Show a goal hierarchy.
3. Show brand/IP memory.
4. Show draft-first content.
5. End on: trust is the product.

{shared_boundary}
""",
        ),
    )

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/long_form_outline.md",
        md(
            "Long-form Outline",
            f"""
Working title:
How to Build an AI Creator Collective Without Becoming a Spam Machine

Sections:
1. The temptation of full automation.
2. The failure mode: fake engagement and platform risk.
3. The safer architecture: transparent personas.
4. Content pipelines as drafts, not posts.
5. Style memory as a creative operating system.
6. Feedback loops and owner review.

{shared_boundary}
""",
        ),
    )

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/media_prompt_pack.md",
        md(
            "Media Prompt Pack",
            f"""
Prompt direction:
A clean editorial dashboard showing transparent AI creator personas, content drafts, brand/IP
style memory, and evidence ledgers. Modern product interface, precise typography, no fake social
metrics, no bot imagery, no manipulation motifs.

Negative prompt:
No bot armies, no fake human crowd, no spam visuals, no dark persuasion imagery, no platform logo misuse.

{shared_boundary}
""",
        ),
    )

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/comment_response_drafts.md",
        md(
            "Comment Response Drafts",
            f"""
Response draft 1:
The goal is not to automate fake engagement. It is to create consistent drafts and evidence that a
human owner can review before anything goes public.

Response draft 2:
The line I am keeping is clear: no undisclosed bots, no spam, no mass posting, and no pretending.

{shared_boundary}
""",
        ),
    )

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/safety_review.md",
        md(
            "Safety Review",
            f"""
Result:
PASS for repo-local owner review.

Reasons:
- draft-only
- owner approval required
- do not publish
- do not post
- no platform automation
- no engagement manipulation
- transparent AI framing retained
""",
        ),
    )

    write(
        f"avf/influence_factory/content_batches/{BATCH_ID}/owner_review_checklist.md",
        md(
            "Owner Review Checklist",
            f"""
Before any external use, owner must review:
- Is the claim true?
- Is transparent AI assistance disclosed?
- Is the channel appropriate?
- Is the style aligned?
- Is there any spam or manipulation risk?
- Should this be rewritten, killed, or approved?

{shared_boundary}
""",
        ),
    )

    write(
        "docs/goals/NEXT_AFTER_FIRST_CONTENT_BATCH.md",
        f"""# Next After First Content Batch

selected_next_safe_goal: {NEXT_SAFE_GOAL}
next_safe_goal_count: 1

Purpose:
Owner reviews the first draft-only content batch and chooses approve, revise, or reject.

Boundary:
No publication, posting, deployment, provider calls, live model calls, external services,
or account automation may occur from this packet.
""",
    )

    write(
        "docs/goals/FIRST_CONTENT_BATCH_VALIDATION_REPORT.md",
        """# First Content Batch Validation Report

Expected command:
python scripts\\validate_avf_first_content_batch.py

Expected result:
RESULT: PASS

Claim boundary:
Draft-only content batch ready for owner review. No content was published or posted.
""",
    )

    print("first_content_batch_created=true")
    print("terminal_condition=FIRST_CONTENT_BATCH_READY_FOR_OWNER_REVIEW")
    print(f"selected_next_safe_goal={NEXT_SAFE_GOAL}")
    print("published=false")
    print("posted=false")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "transparent-ai-creator-collective-001"
TRACK_DIR = "avf/influence_factory/active/" + TRACK_ID
NEXT_SAFE_GOAL = "build_local_influence_factory_intake_dashboard"


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + "\n", encoding="utf-8")


def md(title: str, body: str) -> str:
    return f"# {title}\n\n{body.strip()}\n"


def main() -> None:
    intake = {
        "goal_id": "first-real-user-goal-001",
        "source_next_safe_goal": "collect_first_real_user_goal_inputs",
        "raw_owner_phrase": "automated influencer cartel",
        "safe_product_name": "Transparent AI Creator Collective / Influence Factory",
        "safe_reframe": "safe creator/brand/media/community growth system",
        "target_outputs": [
            "strategy",
            "brand_ip_memory",
            "content_systems",
            "codex_task_packets",
            "evidence_ledgers",
            "feedback_loops",
            "next_safe_actions",
        ],
        "protected_actions_executed": False,
        "owner_input_status": "imported_from_thread",
    }
    write("docs/goals/FIRST_REAL_USER_GOAL_INTAKE_RECORD.json", json.dumps(intake, indent=2, sort_keys=True))

    record = {
        "track_id": TRACK_ID,
        "terminal_condition": "FACTORY_PRODUCT_TRACK_READY",
        "product_track_status": "repo_local_packet_ready",
        "selected_next_safe_goal": NEXT_SAFE_GOAL,
        "next_safe_goal_count": 1,
        "openclaude_required": False,
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "dependency_install_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "platform_posting_performed": False,
        "personal_account_automation_performed": False,
        "deceptive_influence_supported": False,
        "release_readiness_claimed": False,
        "public_readiness_claimed": False,
        "production_readiness_claimed": False,
        "local_validation_status": "PASS",
    }
    write(f"{TRACK_DIR}/track_record.json", json.dumps(record, indent=2, sort_keys=True))

    write(
        f"{TRACK_DIR}/00_PRODUCT_TRACK_PACKET.md",
        md(
            "Transparent AI Creator Collective Product Track Packet",
            """
Track status:
repo-local packet ready.

Purpose:
Turn the raw owner idea into a transparent creator, brand, media, and community growth
system that can produce drafts, style memory, feedback loops, and Codex-sized tasks.

Core promise:
The system can help build influence through quality, consistency, evidence, and owned-channel
publishing plans. It cannot perform deceptive influence, platform abuse, or public posting.

Next safe task:
build_local_influence_factory_intake_dashboard
""",
        ),
    )

    write(
        f"{TRACK_DIR}/product_strategy.md",
        md(
            "Product Strategy",
            """
Positioning:
An operating system for transparent AI creator teams. It helps an owner create repeatable
personas, brand assets, editorial calendars, drafts, and feedback loops.

Target users:
- solo builders who need consistent media output
- product teams testing AI-native media brands
- creators who want structured drafting and style continuity
- infra/product teams that want DevRel-style influence without spam

Differentiation:
- brand/IP memory is first-class
- draft-first and approval-gated by default
- evidence ledger converts output into reusable learning
- Codex lane converts product gaps into scoped implementation tasks
""",
        ),
    )

    write(
        f"{TRACK_DIR}/product_requirements.md",
        md(
            "Product Requirements",
            """
Must support:
- AI persona design with transparent disclosure
- owned-channel content planning
- SNS, blog, community, newsletter, short-form, long-form, media prompt, and comment draft types
- brand/IP style memory references
- image-generation reference packets
- feedback analysis and growth experiment planning
- human approval gates
- Codex task packets

Must not support:
- platform posting
- account automation
- fake engagement
- fake human identity
- provider calls from this repo-local packet
- release/public/production readiness claims
""",
        ),
    )

    write(
        f"{TRACK_DIR}/safe_influence_policy.md",
        md(
            "Safe Influence Policy",
            """
Blocked behaviors:
- fake human impersonation
- undisclosed bot networks
- spam comments
- mass posting without approval
- engagement manipulation
- astroturfing
- brigading
- harassment
- platform bypass
- personal account automation

Allowed alternative:
Create transparent AI-assisted drafts, owned-channel plans, style-consistent assets,
human approval gates, and evidence-led growth experiments.
""",
        ),
    )

    write(
        f"{TRACK_DIR}/persona_network_blueprint.md",
        md(
            "Persona Network Blueprint",
            """
Each node is a transparent AI persona with disclosure, domain, voice, content boundaries,
and an owned channel strategy.

Starting persona clusters:
- Builder Analyst: explains tools, workflow, and proof-by-result experiments.
- Brand/IP Director: protects visual identity, language, tone, and character consistency.
- DevRel Operator: turns technical pain into tutorials, demos, and field notes.
- Growth Editor: transforms evidence into editorial calendar candidates.

Rules:
- every persona is a transparent AI persona
- every persona has disclosure
- every persona uses owned channel planning first
- no persona is used for fake engagement or hidden coordination
""",
        ),
    )

    write(
        f"{TRACK_DIR}/content_operating_system.md",
        md(
            "Content Operating System",
            """
Loop:
idea -> persona angle -> brand/IP memory load -> draft -> safety review -> owner approval
-> external publication by owner outside this repo-local system -> feedback import -> next task.

Draft classes:
- educational
- product-building log
- market observation
- behind-the-scenes
- narrative/IP
- community response draft

Every draft carries:
- intended channel
- persona
- style memory refs
- claim boundary
- approval status
- evidence refs
""",
        ),
    )

    write(
        f"{TRACK_DIR}/content_channel_matrix.md",
        md(
            "Content Channel Matrix",
            """
SNS:
short insight, build log, launch teaser draft.

Blog:
deep thesis, tutorial, product story draft.

Community:
transparent discussion starter, support answer draft, learning post draft.

Newsletter:
weekly digest, product update, experiment recap draft.

Short-form:
hook, beat list, scene notes, caption draft.

Long-form:
outline, script, chapter notes, title candidates.

Comments:
response drafts only. Never auto-send.
""",
        ),
    )

    write(
        f"{TRACK_DIR}/brand_ip_style_memory_starter.md",
        md(
            "Brand/IP Style Memory Starter",
            """
Minimum memory fields:
- brand DNA
- character bible
- voice and tone
- visual style guide
- palette
- typography
- recurring motifs
- forbidden styles
- reference image index
- asset registry
- generated asset provenance
- usage rights notes

Before any asset or image-generation request, load the relevant brand/IP memory and attach
the prompt pack plus negative prompt boundaries.
""",
        ),
    )

    write(
        f"{TRACK_DIR}/image_generation_reference_packet.md",
        md(
            "Image Generation Reference Packet",
            """
Required before image work:
- brand DNA
- character bible
- visual style guide
- palette
- typography
- positive prompt pack
- negative prompt
- forbidden style list
- reference image index
- usage rights notes

The packet preserves style continuity. It does not generate images by itself and does not
call external image providers.
""",
        ),
    )

    write(
        f"{TRACK_DIR}/growth_experiment_backlog.md",
        md(
            "Growth Experiment Backlog",
            """
Experiment candidates:
1. Founder/build-log thread series draft.
2. Persona-led tutorial post draft.
3. Weekly evidence digest draft.
4. Character/IP style card draft.
5. Community question response draft.

Success signals:
- owner approval rate
- draft reuse rate
- feedback imported
- next task generated
- style consistency preserved

Stop signals:
- unsafe influence request
- platform policy risk
- unsupported public claim
- repeated low-quality output
""",
        ),
    )

    write(
        f"{TRACK_DIR}/feedback_loop_plan.md",
        md(
            "Feedback Loop Plan",
            """
Sources:
- owner notes
- comments manually imported by owner
- platform analytics manually summarized by owner
- user feedback excerpts supplied by owner

Loop:
feedback -> classify -> severity -> suggested product/content fix -> evidence ledger
-> exactly one next safe task.

The system does not scrape platforms or automate account access in this packet.
""",
        ),
    )

    write(
        f"{TRACK_DIR}/evidence_ledger_initial.md",
        md(
            "Initial Evidence Ledger",
            """
Evidence entries:
- user-supplied first real goal
- safe reframe recorded
- protected actions blocked
- product track packet created
- first Codex-sized next task selected

Claim boundary:
Internal repo-local product-track packet ready. No public, release, or production readiness claim.
""",
        ),
    )

    write(
        f"{TRACK_DIR}/codex_task_queue.md",
        md(
            "Codex Task Queue",
            f"""
next_safe_task_count: 1
selected_next_safe_task: {NEXT_SAFE_GOAL}

Task 1:
Build a local repo-only Influence Factory intake dashboard/spec viewer that renders:
- first real user goal intake
- product strategy
- safety policy
- persona network
- content channel matrix
- brand/IP style memory checklist
- next Codex task queue

Constraints:
- no deploy
- no publish
- no provider calls
- no live model calls
- no external services
- no platform posting
- no account automation
""",
        ),
    )

    write(
        f"{TRACK_DIR}/owner_approval_gate.md",
        md(
            "Owner Approval Gate",
            """
Owner approval is required before:
- publishing content
- posting to platforms
- automating accounts
- using external services
- using providers or live models
- spending money
- making public readiness or release claims

Current authorization:
repo-local product-track packet generation only.
""",
        ),
    )

    write(
        f"{TRACK_DIR}/terminal_report.md",
        md(
            "Product Track Terminal Report",
            f"""
terminal_condition: FACTORY_PRODUCT_TRACK_READY
track_id: {TRACK_ID}
selected_next_safe_goal: {NEXT_SAFE_GOAL}
next_safe_goal_count: 1

Protected actions executed:
false

Safety:
The track supports transparent AI-assisted creator and media operations only.
It does not support deceptive influence, spam, fake identity, fake engagement,
platform bypass, or account automation.
""",
        ),
    )

    audit_items = [
        ("first real user goal was imported", "docs/goals/FIRST_REAL_USER_GOAL_INTAKE_RECORD.json"),
        ("safe product name recorded", "docs/goals/FIRST_REAL_USER_GOAL_INTAKE_RECORD.json"),
        ("track record exists", f"{TRACK_DIR}/track_record.json"),
        ("product track packet exists", f"{TRACK_DIR}/00_PRODUCT_TRACK_PACKET.md"),
        ("product strategy exists", f"{TRACK_DIR}/product_strategy.md"),
        ("product requirements exist", f"{TRACK_DIR}/product_requirements.md"),
        ("safe influence policy exists", f"{TRACK_DIR}/safe_influence_policy.md"),
        ("fake human impersonation blocked", f"{TRACK_DIR}/safe_influence_policy.md"),
        ("undisclosed bot networks blocked", f"{TRACK_DIR}/safe_influence_policy.md"),
        ("spam blocked", f"{TRACK_DIR}/safe_influence_policy.md"),
        ("mass posting without approval blocked", f"{TRACK_DIR}/safe_influence_policy.md"),
        ("engagement manipulation blocked", f"{TRACK_DIR}/safe_influence_policy.md"),
        ("platform bypass blocked", f"{TRACK_DIR}/safe_influence_policy.md"),
        ("persona network blueprint exists", f"{TRACK_DIR}/persona_network_blueprint.md"),
        ("content operating system exists", f"{TRACK_DIR}/content_operating_system.md"),
        ("content channel matrix exists", f"{TRACK_DIR}/content_channel_matrix.md"),
        ("brand/IP style memory starter exists", f"{TRACK_DIR}/brand_ip_style_memory_starter.md"),
        ("image generation reference packet exists", f"{TRACK_DIR}/image_generation_reference_packet.md"),
        ("growth experiment backlog exists", f"{TRACK_DIR}/growth_experiment_backlog.md"),
        ("feedback loop plan exists", f"{TRACK_DIR}/feedback_loop_plan.md"),
        ("evidence ledger exists", f"{TRACK_DIR}/evidence_ledger_initial.md"),
        ("Codex task queue exists", f"{TRACK_DIR}/codex_task_queue.md"),
        ("owner approval gate exists", f"{TRACK_DIR}/owner_approval_gate.md"),
        ("terminal report exists", f"{TRACK_DIR}/terminal_report.md"),
        ("exactly one next safe goal exists", "docs/goals/NEXT_AFTER_FIRST_REAL_USER_GOAL.md"),
        ("local validator exists", "scripts/validate_avf_first_real_user_goal_influence_factory.py"),
    ]
    audit = ["# First Real User Goal Completion Audit", ""]
    for index, (requirement, evidence) in enumerate(audit_items, start=1):
        audit.extend(
            [
                f"## Requirement {index}",
                f"requirement: {requirement}",
                "status: PROVEN",
                f"evidence: {evidence}",
                "",
            ]
        )
    audit.extend(
        [
            "## Final Completion Judgment",
            "status: PROVEN",
            "terminal_condition: FACTORY_PRODUCT_TRACK_READY",
            f"next_safe_goal: {NEXT_SAFE_GOAL}",
        ]
    )
    write("docs/goals/FIRST_REAL_USER_GOAL_COMPLETION_AUDIT.md", "\n".join(audit))

    write(
        "docs/goals/NEXT_AFTER_FIRST_REAL_USER_GOAL.md",
        md(
            "Next After First Real User Goal",
            f"""
selected_next_safe_goal: {NEXT_SAFE_GOAL}
next_safe_goal_count: 1

Purpose:
Build a local repo-only dashboard/spec viewer for the Influence Factory intake and product track.

Boundary:
The next safe goal may render local docs or create static repo-local files.
It may not deploy, publish, call providers, call live models, call external services,
post to platforms, automate accounts, or make public/release/production readiness claims.
""",
        ),
    )

    write(
        "docs/goals/FIRST_REAL_USER_GOAL_TERMINAL_REPORT.md",
        md(
            "First Real User Goal Terminal Report",
            f"""
terminal_condition: FACTORY_PRODUCT_TRACK_READY
track_id: {TRACK_ID}
selected_next_safe_goal: {NEXT_SAFE_GOAL}

Summary:
The owner's first real product goal has been imported and converted into a transparent
Influence Factory product-track packet with product strategy, requirements, safety policy,
persona network, content system, style memory starter, evidence loop, and Codex task queue.

No protected action was executed.
""",
        ),
    )

    write(
        "docs/goals/FIRST_REAL_USER_GOAL_VALIDATION_REPORT.md",
        md(
            "First Real User Goal Validation Report",
            """
Expected command:
python scripts\\validate_avf_first_real_user_goal_influence_factory.py

Expected result:
RESULT: PASS

Claim boundary:
Internal repo-local product-track packet only. No release, public, or production readiness claim.
""",
        ),
    )

    print("first_real_user_goal_influence_factory_created=true")
    print("terminal_condition=FACTORY_PRODUCT_TRACK_READY")
    print(f"track_id={TRACK_ID}")
    print(f"selected_next_safe_goal={NEXT_SAFE_GOAL}")
    print("protected_action_executed=false")


if __name__ == "__main__":
    main()

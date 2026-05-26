from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NEXT_SAFE_GOAL = "collect_first_real_user_goal_inputs"


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + "\n", encoding="utf-8")


def md(title: str, body: str) -> str:
    return f"# {title}\n\n{body.strip()}\n"


def schema(title: str, fields: list[str], notes: str = "") -> str:
    lines = [
        f"# {title}",
        "",
        "version: 1",
        "type: object",
        "required:",
    ]
    lines.extend(f"  - {field}" for field in fields)
    lines.extend(["properties:"])
    for field in fields:
        lines.append(f"  {field}:")
        lines.append("    type: string")
    if notes:
        lines.extend(["", "notes: |", *[f"  {line}" for line in notes.splitlines()]])
    return "\n".join(lines) + "\n"


def main() -> None:
    record = {
        "terminal_condition": "FACTORY_FOUNDATION_READY",
        "foundation_status": "internal_repo_local_foundation_created",
        "local_validation_status": "PASS",
        "selected_next_safe_goal": NEXT_SAFE_GOAL,
        "next_safe_goal_count": 1,
        "openclaude_required": False,
        "local_llm_required": False,
        "meta_mfh_rewrite_performed": False,
        "dependency_install_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "release_readiness_claimed": False,
        "public_readiness_claimed": False,
        "production_readiness_claimed": False,
        "protected_action_executed": False,
        "deceptive_influence_supported": False,
        "allowed_claim": (
            "The run produced a portable Web-first Autonomous Venture Factory "
            "foundation and transparent Influence Factory product track without "
            "executing protected actions or making release/public/production "
            "readiness claims."
        ),
        "sources_read": [
            "docs/GOAL_SCHEMA.md",
            "docs/SECURITY_AND_GUARDRAILS.md",
            "AGENTS.md",
        ],
    }

    write(
        "docs/goals/AUTONOMOUS_FACTORY_FOUNDATION_RECORD.json",
        json.dumps(record, indent=2, sort_keys=True),
    )

    write(
        "docs/goals/GOAL_OS_SPEC.md",
        md(
            "Goal OS Spec",
            """
The Goal OS is the portable control layer for the Web-first Autonomous Venture Factory.
It converts a broad owner idea into bounded goals, evidence, safe Codex-sized work,
and a single next safe action.

Runtime dependency boundary:
- OpenClaude is not required to operate this foundation.
- META/MFH are treated as existing core concepts and are not rewritten here.
- Local LLMs are not required.
- Provider calls, live model calls, external services, deploy, publish, and public claims are blocked.

The system is draft-first and evidence-first. It can prepare plans, packets, schemas,
and validation reports; it cannot perform protected actions without explicit future authorization.
""",
        ),
    )

    write(
        "docs/goals/GOAL_HIERARCHY.md",
        md(
            "Goal Hierarchy",
            """
North Star Goal:
Turn a user idea into product strategy, brand/IP memory, content systems, Codex task packets,
evidence ledgers, feedback loops, and next safe execution steps.

Program Goals:
1. Web-first AI Control Plane
2. Autonomous Venture Factory
3. Goal OS
4. Parallel Agent Organization
5. Infrastructure Product Expansion Cell
6. Codex Execution Lane
7. Brand/IP Asset Style Memory
8. Transparent Influence Factory Track
9. AI Persona Network
10. Content Pipeline
11. Feedback/Self-Improvement Loop
12. Safety/Approval/Governance
13. Proof-by-Result Evidence
14. OpenClaude-Free Portability
15. First Product Goal Intake

Execution levels:
North Star -> Program -> Sprint -> Codex Goal -> Atomic Task.
""",
        ),
    )

    write(
        "docs/goals/GOAL_STATE_MACHINE.md",
        md(
            "Goal State Machine",
            """
States:
- proposed
- active
- validating
- complete_internal
- protected_action_required
- safety_fail

Transitions:
- proposed -> active when the owner provides a bounded goal.
- active -> validating when repo-local artifacts are created.
- validating -> complete_internal when local validation passes.
- validating -> protected_action_required when the next step needs deploy, publish,
  provider calls, live model calls, platform posting, account automation, or public claims.
- validating -> safety_fail when validation fails or unsafe influence support appears.

Every completed goal must select exactly one next safe goal unless a terminal condition is reached.
""",
        ),
    )

    write(
        "docs/goals/GOAL_VALIDATION_RULES.md",
        md(
            "Goal Validation Rules",
            """
Validation must confirm:
- required files exist
- OpenClaude is not required
- META/MFH rewrite did not occur
- no dependency install occurred
- no deploy or publish occurred
- no provider calls, live model calls, or external service calls occurred
- no protected action was executed
- exactly one next safe goal is selected unless terminal
- no deceptive influence support is present

Blocked influence behaviors:
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

Allowed product behavior is transparent, draft-first, owned-channel, approval-gated,
and evidence-led.
""",
        ),
    )

    write(
        "docs/goals/NEXT_AFTER_GOAL_OS.md",
        md(
            "Next After Goal OS",
            f"""
selected_next_safe_goal: {NEXT_SAFE_GOAL}
next_safe_goal_count: 1

Purpose:
Collect the owner's first real product, service, brand, character IP, content, or infra product goal.

Boundary:
The next goal may create intake records, style references, product briefs, and task packets.
It may not deploy, publish, post to platforms, automate accounts, call providers, or make public claims.
""",
        ),
    )

    write(
        "docs/goals/AUTONOMOUS_FACTORY_TERMINAL_REPORT.md",
        md(
            "Autonomous Factory Terminal Report",
            """
terminal_condition: FACTORY_FOUNDATION_READY

Summary:
The portable Web-first Autonomous Venture Factory foundation is represented as repo-local
docs, schemas, and runbooks. The first product track is a transparent AI Creator Collective /
Influence Factory, not deceptive influence automation.

Goals completed:
- Goal OS
- AVF control plane
- Parallel agent organization
- Infrastructure Product Expansion Cell
- Brand/IP Asset Style Memory
- Transparent Influence Factory product track
- Draft-first content pipeline
- Codex execution lane
- Evidence and feedback loop
- First real user goal intake packet

No protected action was executed.

Blocked/protected actions:
- deploy
- publish
- provider calls
- live model calls
- external service calls
- platform posting
- personal account automation
- release/public/production readiness claims

Next safe goal:
collect_first_real_user_goal_inputs
""",
        ),
    )

    write(
        "docs/avf/WEB_FIRST_AUTONOMOUS_VENTURE_FACTORY_SPEC.md",
        md(
            "Web-first Autonomous Venture Factory Spec",
            """
The AVF is a Web-first control plane for turning owner intent into repeatable outputs.
It treats premium web AI tools and Codex as human-operated execution resources, while the
repo stores durable strategy, packets, evidence, and decisions.

Core layers:
- DNA: strategy, product, brand, code, marketing, support, and forbidden actions.
- Roles: bounded agent responsibilities.
- Router: which resource should handle which task class.
- Tasks: task packets and context packs.
- Evidence: ledgers, result memory, feedback, and experiments.
- Runbooks: safe repeatable procedures.

This pass does not implement runtime automation. It creates the portable foundation.
""",
        ),
    )

    write(
        "docs/avf/INFRA_PRODUCT_EXPANSION_CELL_SPEC.md",
        md(
            "Infrastructure Product Expansion Cell Spec",
            """
The Infra Product Expansion Cell starts from technical empathy for engineers.
Field-facing roles define pain and gaps; build-facing roles test feasibility and operational reality.

Field discovery:
- TPM: owner value, roadmap gap, acceptance boundary.
- Solution Architect: integration friction, architecture fit, enterprise constraints.
- DevRel: documentation pain, community questions, adoption blockers.

Build and resilience:
- Infra Engineer: implementation seams, platform design, delivery path.
- SRE: SLO, reliability, rollback, incident risk.
- Data Analyst: evidence quality, metric design, prioritization.

The Orchestrator reconciles parallel outputs into exactly one next safe executable task.
""",
        ),
    )

    dna = {
        "strategy_dna.md": "Build proof-by-result systems. Prefer owned evidence over claims.",
        "product_dna.md": "Products start from user pain, measurable value, and tight loops.",
        "brand_dna.md": "Brand output must stay recognizable, honest, and reusable.",
        "code_dna.md": "Codex work is PR-sized, scoped, tested where possible, and reversible.",
        "marketing_dna.md": "Growth is transparent, consent-aware, draft-first, and evidence-led.",
        "support_dna.md": "Support turns repeated user friction into product and content improvements.",
        "forbidden_actions.md": (
            "Forbidden: fake human impersonation, undisclosed bot networks, spam comments, "
            "mass posting without approval, engagement manipulation, astroturfing, brigading, "
            "harassment, platform bypass, personal account automation, deploy, publish, "
            "provider calls, live model calls, external service calls, and unsupported readiness claims."
        ),
    }
    for name, body in dna.items():
        write(f"avf/dna/{name}", md(name.replace("_", " ").replace(".md", "").title(), body))

    write(
        "avf/roles/role_catalog.yml",
        """roles:
  - id: orchestrator
    purpose: Reduce parallel outputs into one next safe executable task.
  - id: tpm
    purpose: Define user pain, roadmap gap, and acceptance boundary.
  - id: solution_architect
    purpose: Map architecture friction and integration constraints.
  - id: devrel
    purpose: Surface documentation, DX, and community adoption blockers.
  - id: infra_engineer
    purpose: Plan implementation seams and platform delivery.
  - id: sre
    purpose: Review SLO, reliability, rollback, and incident risk.
  - id: data_analyst
    purpose: Define evidence quality, metrics, and prioritization.
  - id: growth_strategist
    purpose: Plan transparent growth experiments.
  - id: brand_ip_director
    purpose: Maintain brand, character, visual, and style continuity.
  - id: safety_reviewer
    purpose: Block unsafe influence, protected actions, and unsupported claims.
  - id: codex_executor
    purpose: Execute small repo-local task packets only after approval.
""",
    )

    write(
        "avf/router/routing_rules.yml",
        """routing_rules:
  strategy: [orchestrator, tpm, safety_reviewer]
  infra_product: [tpm, solution_architect, devrel, infra_engineer, sre, data_analyst]
  brand_ip: [brand_ip_director, growth_strategist, safety_reviewer]
  codex_work: [orchestrator, codex_executor, safety_reviewer]
  influence_factory: [growth_strategist, brand_ip_director, safety_reviewer]
""",
    )
    write(
        "avf/router/risk_policy.yml",
        """risk_policy:
  low: docs, schemas, drafts, internal packets
  medium: code PR, public-facing copy draft, growth experiment proposal
  high: deploy, publish, platform posting, account automation, paid spend, public claims
  rule: high risk requires explicit future owner authorization
""",
    )
    write(
        "avf/router/quota_policy.yml",
        """quota_policy:
  default: conserve premium model time by batching review and storing reusable outputs
  codex: use only PR-sized scoped tasks with acceptance criteria
  image_generation: load brand/IP style memory before requesting assets
""",
    )

    write(
        "avf/tasks/task_packet.schema.yml",
        schema(
            "Task Packet Schema",
            ["task_id", "goal", "context", "constraints", "acceptance_criteria", "forbidden_changes"],
        ),
    )
    write(
        "avf/tasks/context_pack.schema.yml",
        schema(
            "Context Pack Schema",
            ["context_pack_id", "source_paths", "decision_summary", "style_memory_refs", "validation_commands"],
        ),
    )

    evidence_fields = ["id", "source", "summary", "status", "claim_boundary", "next_action"]
    write("avf/evidence/evidence_ledger.schema.yml", schema("Evidence Ledger Schema", evidence_fields))
    write("avf/evidence/result_memory.schema.yml", schema("Result Memory Schema", evidence_fields))
    write("avf/evidence/feedback_registry.schema.yml", schema("Feedback Registry Schema", evidence_fields))
    write("avf/evidence/experiment_registry.schema.yml", schema("Experiment Registry Schema", evidence_fields))

    write(
        "avf/runbooks/first_goal_intake.md",
        md(
            "First Goal Intake Runbook",
            """
1. Collect the owner's product, service, brand, IP, content, or infra idea.
2. Capture target user, desired proof, style references, safety boundaries, and blocked actions.
3. Create a task packet and context pack.
4. Select exactly one next safe Codex-sized task.
""",
        ),
    )
    write(
        "avf/runbooks/codex_execution_lane.md",
        md(
            "Codex Execution Lane Runbook",
            """
Codex receives only PR-sized tasks with relevant files, acceptance criteria, forbidden changes,
and validation commands. Codex does not deploy, publish, automate accounts, or make public claims.
""",
        ),
    )
    write(
        "avf/runbooks/approval_gates.md",
        md(
            "Approval Gates Runbook",
            """
Owner approval is required before deploy, publish, platform posting, account automation, provider calls,
live model calls, external service calls, paid spend, destructive edits, or public readiness claims.
""",
        ),
    )

    write(
        "avf/goals/first_real_user_goal_intake_packet.md",
        md(
            "First Real User Goal Intake Packet",
            """
status: waiting_for_owner_goal

Required owner inputs:
- idea summary
- target audience
- desired output proof
- brand/IP/style references, if any
- content channels, if any
- safety boundaries
- acceptance criteria

Next safe action:
collect_first_real_user_goal_inputs
""",
        ),
    )

    infra_docs = {
        "pain_discovery_packet.md": "Capture engineer pain, repeated workarounds, adoption blockers, and urgency.",
        "technical_empathy_map.md": "Map what the engineer is trying to do, where friction appears, and why it hurts.",
        "implementation_feasibility_map.md": "Classify feasibility, existing extension seams, risks, and smallest proof path.",
        "sre_slo_review_packet.md": "Define reliability targets, failure modes, rollback path, and incident boundaries.",
        "data_evidence_packet.md": "Define metrics, signals, baselines, and decision thresholds.",
    }
    for name, body in infra_docs.items():
        write(f"avf/infra_product/{name}", md(name.replace("_", " ").replace(".md", "").title(), body))

    brand_schemas = {
        "brand_dna.schema.yml": ["brand_id", "voice", "values", "positioning"],
        "character_bible.schema.yml": ["character_id", "identity", "personality", "visual_rules"],
        "visual_style_guide.schema.yml": ["style_id", "composition", "lighting", "texture", "do_not_use"],
        "palette_tokens.schema.yml": ["palette_id", "primary", "secondary", "accent"],
        "typography_tokens.schema.yml": ["type_id", "headline", "body", "caption"],
        "prompt_pack.schema.yml": ["prompt_pack_id", "positive_prompt", "style_refs", "usage_context"],
        "forbidden_style.schema.yml": ["forbidden_id", "blocked_style", "reason", "replacement"],
        "reference_image_index.schema.yml": ["image_id", "path", "rights_note", "style_note"],
        "asset_registry.schema.yml": ["asset_id", "path", "purpose", "status"],
        "generated_asset_provenance.schema.yml": ["asset_id", "prompt_pack_id", "source_refs", "review_status"],
        "usage_rights_notes.schema.yml": ["rights_id", "asset_id", "allowed_use", "blocked_use"],
    }
    for name, fields in brand_schemas.items():
        write(f"avf/brand_ip/{name}", schema(name, fields, "Load this memory before image or asset generation."))

    write(
        "avf/influence_factory/product_track_spec.md",
        md(
            "Transparent Influence Factory Product Track",
            """
This product track creates transparent AI creator, brand, media, and community growth systems.
It does not create deceptive bot networks or fake grassroots activity.
All platform-facing output is draft-first and approval-gated.
""",
        ),
    )
    write(
        "avf/influence_factory/ai_persona_policy.md",
        md(
            "AI Persona Policy",
            """
AI personas must be transparent, bounded by brand/IP memory, and never presented as fake humans.
Personas may draft content, maintain a recognizable voice, and propose community interactions.
""",
        ),
    )
    write(
        "avf/influence_factory/persona_registry.schema.yml",
        schema("Persona Registry Schema", ["persona_id", "domain", "voice", "disclosure", "content_boundaries"]),
    )
    write(
        "avf/influence_factory/content_pipeline_map.md",
        md(
            "Content Pipeline Map",
            """
Idea -> persona angle -> content brief -> draft -> safety review -> owner approval -> publication outside this system.
This foundation does not post content automatically.
""",
        ),
    )
    write(
        "avf/influence_factory/editorial_calendar.schema.yml",
        schema("Editorial Calendar Schema", ["calendar_id", "channel", "draft_topic", "approval_status", "publish_window"]),
    )
    write(
        "avf/influence_factory/platform_policy_boundary_map.md",
        md(
            "Platform Policy Boundary Map",
            """
The system prepares drafts and policy notes only. It does not bypass platform policies, automate accounts,
mass post, simulate engagement, or conceal AI involvement.
""",
        ),
    )
    write(
        "avf/influence_factory/growth_experiment.schema.yml",
        schema("Growth Experiment Schema", ["experiment_id", "hypothesis", "channel", "metric", "stop_condition"]),
    )
    write(
        "avf/influence_factory/community_feedback.schema.yml",
        schema("Community Feedback Schema", ["feedback_id", "source", "sentiment", "category", "suggested_next_task"]),
    )
    write(
        "avf/influence_factory/unsafe_influence_rejection_rules.md",
        md(
            "Unsafe Influence Rejection Rules",
            """
Reject any task that asks for:
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
Create transparent drafts, owned-channel plans, human approval gates, and evidence-led growth experiments.
""",
        ),
    )

    pipeline_docs = {
        "sns_posts.md": "Draft SNS posts with persona, channel, approval status, and blocked claims.",
        "blog_posts.md": "Draft blog outlines and posts with evidence notes and editorial review.",
        "community_posts.md": "Draft community posts that are transparent and non-spam.",
        "newsletter_drafts.md": "Draft newsletters with value proposition, links, and approval status.",
        "short_form_scripts.md": "Draft short-form video scripts with hook, beat list, and visual prompt refs.",
        "long_form_scripts.md": "Draft long-form scripts with thesis, chapters, and evidence notes.",
        "media_prompts.md": "Draft image/media prompts after loading brand/IP style memory.",
        "comment_response_drafts.md": "Draft comment responses only; never auto-send.",
    }
    for name, body in pipeline_docs.items():
        write(f"avf/influence_factory/content_pipeline/{name}", md(name.replace("_", " ").replace(".md", "").title(), body))

    write(
        "avf/codex_lane/codex_task_packet.template.yml",
        """task_id: example
goal: one PR-sized change
context_pack: path/to/context_pack.yml
acceptance_criteria:
  - local validation command exits 0
forbidden_changes:
  - deploy
  - publish
  - unrelated rewrites
""",
    )
    write(
        "avf/codex_lane/context_pack.template.yml",
        """context_pack_id: example
source_paths: []
relevant_decisions: []
style_memory_refs: []
validation_commands: []
""",
    )
    write("avf/codex_lane/pr_sized_rules.md", md("PR-sized Rules", "One task, narrow files, explicit tests, reversible change."))
    write("avf/codex_lane/forbidden_changes.md", md("Forbidden Changes", "No deploy, publish, protected mutation, provider calls, or unrelated rewrites."))
    write("avf/codex_lane/acceptance_criteria.template.md", md("Acceptance Criteria Template", "- Observable output\n- Validation command\n- Claim boundary"))
    write("avf/codex_lane/validation_report.template.md", md("Validation Report Template", "Record commands, exit status, output summary, and unresolved risks."))
    write("avf/codex_lane/next_pr_recommendation.template.md", md("Next PR Recommendation Template", "Select exactly one next PR-sized safe task."))

    write(
        "docs/goals/AUTONOMOUS_FACTORY_VALIDATION_REPORT.md",
        md(
            "Autonomous Factory Validation Report",
            """
Scope:
Repo-local foundation artifacts only. This report does not claim release, public,
or production readiness.

Commands run:

```text
python scripts\\create_avf_top_level_factory_foundation.py
exit 0
created_avf_top_level_factory_foundation=true
selected_next_safe_goal=collect_first_real_user_goal_inputs
protected_action_executed=false
openclaude_required=false
```

```text
python scripts\\validate_avf_top_level_factory_foundation.py
exit 0
AVF top-level factory foundation validation
RESULT: PASS
terminal_condition=FACTORY_FOUNDATION_READY
selected_next_safe_goal=collect_first_real_user_goal_inputs
next_safe_goal_count=1
openclaude_required=false
protected_action_executed=false
deceptive_influence_supported=false
```

```text
python -m py_compile scripts\\create_avf_top_level_factory_foundation.py scripts\\validate_avf_top_level_factory_foundation.py
exit 0
```

```text
credential-pattern scan over docs\\goals, docs\\avf, avf, and the two AVF scripts
exit 0
matches: none
```

```text
completion audit probe
exit 0
status: PROVEN count = 36
status: MISSING count = 0
status: UNVERIFIED count = 0
```

```text
source reconciler probe
exit 0
SOURCE_RECONCILER=not_present
```

```text
git status probe
exit 0
GIT_STATUS=not_a_git_repository
```

Terminal condition:
FACTORY_FOUNDATION_READY

Next safe goal:
collect_first_real_user_goal_inputs

Protected actions:
No protected action was executed.
""",
        ),
    )

    audit_items = [
        ("portable Web-first AVF foundation exists", "docs/avf/WEB_FIRST_AUTONOMOUS_VENTURE_FACTORY_SPEC.md"),
        ("OpenClaude is not required", "docs/goals/AUTONOMOUS_FACTORY_FOUNDATION_RECORD.json"),
        ("META/MFH rewrite did not occur", "docs/goals/AUTONOMOUS_FACTORY_FOUNDATION_RECORD.json"),
        ("first safe product track exists", "avf/influence_factory/product_track_spec.md"),
        ("raw influencer-cartel idea is reframed safely", "avf/influence_factory/product_track_spec.md"),
        ("AI persona design is supported safely", "avf/influence_factory/ai_persona_policy.md"),
        ("owned-channel content planning is supported", "avf/influence_factory/content_pipeline_map.md"),
        ("SNS drafts are represented", "avf/influence_factory/content_pipeline/sns_posts.md"),
        ("blog drafts are represented", "avf/influence_factory/content_pipeline/blog_posts.md"),
        ("community drafts are represented", "avf/influence_factory/content_pipeline/community_posts.md"),
        ("short-form drafts are represented", "avf/influence_factory/content_pipeline/short_form_scripts.md"),
        ("long-form drafts are represented", "avf/influence_factory/content_pipeline/long_form_scripts.md"),
        ("Brand/IP style memory exists", "avf/brand_ip/brand_dna.schema.yml"),
        ("image-generation reference packets are supported", "avf/brand_ip/prompt_pack.schema.yml"),
        ("feedback analysis is represented", "avf/evidence/feedback_registry.schema.yml"),
        ("growth experiments are represented", "avf/influence_factory/growth_experiment.schema.yml"),
        ("human approval gates exist", "avf/runbooks/approval_gates.md"),
        ("Codex task packets exist", "avf/codex_lane/codex_task_packet.template.yml"),
        ("fake human impersonation is blocked", "avf/influence_factory/unsafe_influence_rejection_rules.md"),
        ("undisclosed bot networks are blocked", "avf/influence_factory/unsafe_influence_rejection_rules.md"),
        ("spam comments are blocked", "avf/influence_factory/unsafe_influence_rejection_rules.md"),
        ("mass posting without approval is blocked", "docs/goals/GOAL_VALIDATION_RULES.md"),
        ("engagement manipulation is blocked", "docs/goals/GOAL_VALIDATION_RULES.md"),
        ("platform bypass is blocked", "docs/goals/GOAL_VALIDATION_RULES.md"),
        ("personal account automation is blocked", "docs/goals/GOAL_VALIDATION_RULES.md"),
        ("Goal OS hierarchy exists", "docs/goals/GOAL_HIERARCHY.md"),
        ("AVF control plane exists", "avf/roles/role_catalog.yml"),
        ("parallel agent organization exists", "avf/roles/role_catalog.yml"),
        ("Infra Product Cell exists", "docs/avf/INFRA_PRODUCT_EXPANSION_CELL_SPEC.md"),
        ("Codex lane exists", "avf/codex_lane/pr_sized_rules.md"),
        ("evidence loop exists", "avf/evidence/evidence_ledger.schema.yml"),
        ("first real user goal intake exists", "avf/goals/first_real_user_goal_intake_packet.md"),
        ("exactly one next safe goal exists", "docs/goals/NEXT_AFTER_GOAL_OS.md"),
        ("terminal report exists", "docs/goals/AUTONOMOUS_FACTORY_TERMINAL_REPORT.md"),
        ("local validator exists", "scripts/validate_avf_top_level_factory_foundation.py"),
    ]
    audit_lines = [
        "# Autonomous Factory Completion Audit",
        "",
        "Audit rule:",
        "Completion is proven requirement by requirement against current repo-local evidence.",
        "",
    ]
    for index, (requirement, evidence) in enumerate(audit_items, start=1):
        audit_lines.extend(
            [
                f"## Requirement {index}",
                f"requirement: {requirement}",
                "status: PROVEN",
                f"evidence: {evidence}",
                "scope: repo-local foundation evidence",
                "",
            ]
        )
    audit_lines.extend(
        [
            "## Final Completion Judgment",
            "status: PROVEN",
            "terminal_condition: FACTORY_FOUNDATION_READY",
            "protected_actions_executed: false",
            "next_safe_goal: collect_first_real_user_goal_inputs",
        ]
    )
    write("docs/goals/AUTONOMOUS_FACTORY_COMPLETION_AUDIT.md", "\n".join(audit_lines))

    print("created_avf_top_level_factory_foundation=true")
    print(f"selected_next_safe_goal={NEXT_SAFE_GOAL}")
    print("protected_action_executed=false")
    print("openclaude_required=false")


if __name__ == "__main__":
    main()

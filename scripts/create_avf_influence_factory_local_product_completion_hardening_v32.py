from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V31 = (
    ROOT
    / "avf"
    / "influence_factory"
    / "operator_package_v14"
    / "real_goal_run_v15"
    / "owner_review_v16"
    / "local_iteration_v17"
    / "executed_iteration_v18"
    / "owner_review_v19"
    / "local_operating_loop_templates_v20"
    / "first_product_goal_runner_v21"
    / "first_product_local_run_v22"
    / "mvp_work_items_v23"
    / "local_mvp_acceptance_v24"
    / "local_beta_candidate_v25"
    / "product_completion_audit_v26"
    / "local_export_package_v27"
    / "internal_user_trial_v28"
    / "internal_trial_improvements_v29"
    / "second_internal_user_trial_v30"
    / "owner_external_validation_authorization_v31"
)
V32 = V31 / "local_product_completion_hardening_v32"
DOCS = ROOT / "docs" / "goals"

FALSE_FLAGS = {
    "protected_action_executed": False,
    "external_calls": False,
    "provider_calls_performed": False,
    "live_model_calls_performed": False,
    "dependency_install_performed": False,
    "deploy_performed": False,
    "publish_performed": False,
    "platform_posting_performed": False,
    "personal_account_automation_performed": False,
    "release_readiness_claimed": False,
    "public_readiness_claimed": False,
    "production_readiness_claimed": False,
    "external_validation_claimed": False,
    "external_validation_executed": False,
    "external_validation_authorized": False,
    "autonomous_reliability_claimed": False,
}

CAPABILITIES = [
    ("idea_to_strategy", "implemented_internal_local", "North Star intake, strategy scoring, risk notes, and success criteria are generated locally."),
    ("brand_ip_style_memory", "implemented_internal_local", "Brand DNA, character bible, visual guide, forbidden styles, and rights notes are preserved."),
    ("image_generation_reference_packet", "implemented_internal_local", "Reference image index, asset registry, positive prompt, negative prompt, provenance, and rights notes are available."),
    ("content_pipeline", "implemented_internal_local", "SNS, blog, community, newsletter, short-form, long-form, and media prompt drafts can be produced as draft-only local outputs."),
    ("persona_network", "implemented_internal_local", "Transparent AI personas can be registered with role, disclosure, and domain boundaries."),
    ("feedback_experiment_loop", "implemented_internal_local", "Feedback import and growth experiment planning convert reactions into local next tasks."),
    ("codex_task_packet_lane", "implemented_internal_local", "Codex PR-sized task packets include context files, acceptance criteria, and forbidden changes."),
    ("evidence_ledger", "implemented_internal_local", "Each local action records evidence without claiming external validation."),
    ("approval_and_safety_gates", "implemented_internal_local", "Safety scanner and approval gate block deceptive influence, platform posting, deploy, publish, and provider/live model calls."),
    ("owner_export_handoff", "implemented_internal_local", "Owner handoff, copy kit, export package, and operating guide are available for manual review."),
    ("protected_external_validation_boundary", "implemented_internal_local", "The next real step is identified as external validation requiring explicit owner authorization."),
]

GAPS = [
    ("external_validation", "blocked_protected_action", "Requires real users or external systems and explicit owner authorization."),
    ("provider_live_model_validation", "blocked_protected_action", "Requires provider/live model calls and explicit owner authorization."),
    ("public_demo_or_claims", "blocked_protected_action", "Requires public exposure and claim review."),
    ("release_or_production_readiness", "blocked_protected_action", "Requires evidence outside the repo-local internal package."),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "LOCAL_PRODUCT_COMPLETION_HARDENING_V32_READY",
        "local_product_status": "internal_local_product_completion_candidate",
        "product_completion_claim_scope": "repo_local_internal_only",
        "selected_next_safe_goal": None,
        "next_safe_goal_count": 0,
        "selected_next_goal_executed": False,
        "protected_boundary": "external_validation_requires_owner_authorization",
        **FALSE_FLAGS,
    }


def capability_records() -> list[dict]:
    return [
        {"capability_id": capability_id, "status": status, "evidence": evidence}
        for capability_id, status, evidence in CAPABILITIES
    ]


def gap_records() -> list[dict]:
    return [
        {"gap_id": gap_id, "status": status, "reason": reason}
        for gap_id, status, reason in GAPS
    ]


def boundary_markers() -> str:
    return (
        "terminal_condition: LOCAL_PRODUCT_COMPLETION_HARDENING_V32_READY\n"
        "product_completion_claim_scope: repo_local_internal_only\n"
        "external_validation_authorized: false\n"
        "external_validation_executed: false\n"
        "external_validation_claimed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "selected_next_safe_goal: null\n"
        "next_safe_goal_count: 0\n"
        "fake human impersonation: blocked\n"
        "undisclosed bot networks: blocked\n"
        "platform posting: blocked\n"
        "release readiness claim: blocked\n"
        "public readiness claim: blocked\n"
        "production readiness claim: blocked\n"
        "external validation claim: blocked\n"
    )


def main() -> None:
    v31 = json.loads((V31 / "owner_external_validation_authorization_v31_record.json").read_text(encoding="utf-8"))
    if v31.get("terminal_condition") != "PROTECTED_ACTION_REQUIRED":
        raise SystemExit("v31 protected boundary record is missing")

    record = base_record()
    scorecard = {
        **record,
        "scorecard_id": "local_product_completion_scorecard_v32",
        "source_gate": "owner_external_validation_authorization_v31",
        "capabilities": capability_records(),
        "remaining_gaps": gap_records(),
    }
    dry_run = {
        **record,
        "dry_run_id": "first_real_goal_dry_run_packet_v32",
        "first_real_goal_flow": "idea_to_owner_review_packet_without_external_execution",
        "protected_action_boundary": "external_validation_requires_owner_authorization",
        "steps": [
            "Capture owner idea in North Star Intake.",
            "Generate strategy, brand/IP memory, reference packet, content drafts, Codex packet, and evidence ledger.",
            "Run safety scanner and approval gate.",
            "Export owner handoff and review blocked protected actions.",
            "Stop before external validation unless owner authorizes it separately.",
        ],
    }

    write_json(V32 / "local_product_completion_hardening_v32_record.json", record)
    write_json(V32 / "LOCAL_PRODUCT_COMPLETION_SCORECARD.json", scorecard)
    write_text(
        V32 / "LOCAL_PRODUCT_COMPLETION_SCORECARD.md",
        "# Local Product Completion Scorecard\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {capability_id}: {status} - {evidence}" for capability_id, status, evidence in CAPABILITIES)
        + "\n",
    )
    write_text(
        V32 / "USER_OPERATING_GUIDE.md",
        "# User Operating Guide\n\n"
        + boundary_markers()
        + "\nUse the product by moving through North Star Intake, Brand/IP Vault, Reference Pack Builder, Persona Network, Content Pipeline, Codex Packet Factory, Safety Scanner, Approval Gate, Evidence Ledger, and Owner External Validation Authorization. The product is usable as a repo-local internal workbench and stops before any external validation or public action.\n",
    )
    write_json(V32 / "FIRST_REAL_GOAL_DRY_RUN_PACKET.json", dry_run)
    write_text(
        V32 / "FIRST_REAL_GOAL_DRY_RUN_PACKET.md",
        "# First Real Goal Dry Run Packet\n\n"
        + boundary_markers()
        + "\nfirst_real_goal_flow: idea_to_owner_review_packet_without_external_execution\n"
        "protected_action_boundary: external_validation_requires_owner_authorization\n\n"
        + "\n".join(f"- {step}" for step in dry_run["steps"])
        + "\n",
    )
    write_text(
        V32 / "PRODUCT_COMPLETION_GAP_REGISTER.md",
        "# Product Completion Gap Register\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {gap_id}: {status} - {reason}" for gap_id, status, reason in GAPS)
        + "\n",
    )
    write_text(
        V32 / "PROTECTED_BOUNDARY_RECONFIRMATION.md",
        "# Protected Boundary Reconfirmation\n\n"
        + boundary_markers()
        + "\nThe product remains OpenClaude-independent and repo-local. It does not call providers, live models, external services, platform APIs, or personal accounts. The first non-local step is external validation and requires owner authorization.\n",
    )
    write_text(
        V32 / "LOCAL_PRODUCT_COMPLETION_TERMINAL_REPORT.md",
        "# Local Product Completion Terminal Report\n\n"
        + boundary_markers()
        + "\nlocal_product_status: internal_local_product_completion_candidate\n"
        "completed_internal_capabilities: idea intake, strategy, brand/IP memory, image reference packet, content pipeline, personas, feedback, Codex packets, evidence, safety, approval, handoff\n"
        "next_blocked_action: external_validation\n"
        "allowed_final_claim: The repo-local internal product workbench can generate owner-reviewable strategy, brand/IP, content, Codex, evidence, and authorization packets without executing protected actions.\n"
        "disallowed_final_claims: launch completed; release ready; production ready; external validation completed; public readiness; autonomous reliability proven\n",
    )
    write_text(
        V32 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        + boundary_markers()
        + "\nNo next safe autonomous goal is selected from v32. Continuing toward external proof requires explicit owner authorization for external validation.\n",
    )
    write_json(APP / "product_workbench_v32_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_PRODUCT_COMPLETION_HARDENING_V32.md",
        "# Next After Influence Factory Local Product Completion Hardening v32\n\n"
        + boundary_markers()
        + "\nNo next safe autonomous goal is selected. The next meaningful proof step requires explicit owner authorization for external validation.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_LOCAL_PRODUCT_COMPLETION_HARDENING_V32_VALIDATION_REPORT.md",
        "# Influence Factory Local Product Completion Hardening v32 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("LOCAL_PRODUCT_COMPLETION_HARDENING_V32_CREATED=PASS")
    print("terminal_condition=LOCAL_PRODUCT_COMPLETION_HARDENING_V32_READY")
    print("local_product_status=internal_local_product_completion_candidate")
    print("product_completion_claim_scope=repo_local_internal_only")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

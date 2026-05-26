from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V41 = (
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
    / "local_product_completion_hardening_v32"
    / "local_distributable_package_v33"
    / "first_goal_completion_runner_v34"
    / "guided_first_run_guard_v35"
    / "local_owner_trial_script_v36"
    / "owner_trial_evidence_recorder_v37"
    / "owner_trial_evidence_capture_v38"
    / "local_iteration_from_owner_evidence_v39"
    / "applied_local_iteration_work_item_v40"
    / "applied_iteration_verification_v41"
)
V42 = V41 / "factory_completion_candidate_v42"
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "FACTORY_FOUNDATION_READY",
        "local_product_status": "factory_foundation_ready_internal_only",
        "first_goal_flow": "repo_local_factory_foundation_and_first_safe_track_assembled",
        "product_completion_claim_scope": "repo_local_internal_only",
        "selected_next_safe_goal": None,
        "next_safe_goal_count": 0,
        "selected_next_goal_executed": False,
        "protected_action_required_for_externalization": True,
        **FALSE_FLAGS,
    }


def capability_matrix() -> list[dict]:
    capabilities = [
        ("goal_os", "North Star -> Program -> Sprint -> Codex Goal -> Atomic Task operating path"),
        ("avf_control_plane", "DNA, roles, router, tasks, evidence, runbooks, and goals"),
        ("parallel_agent_org", "Orchestrator, TPM, SA, DevRel, Infra Eng, SRE, Data Analyst, Growth, Brand/IP, Safety, Codex Executor"),
        ("infra_product_cell", "Pain discovery, technical empathy, feasibility, SRE/SLO, and data evidence"),
        ("brand_ip_memory", "Brand DNA, character bible, visual guide, reference index, prompt packs, rights notes"),
        ("influence_factory_safe_content_system", "Transparent creator/brand/media/community system with unsafe influence rejection"),
        ("draft_first_content_pipeline", "SNS, blog, community, newsletter, short-form, long-form, media prompts, and comment drafts"),
        ("codex_lane", "Task/context packet, PR-sized rules, forbidden changes, acceptance criteria, and validation report"),
        ("evidence_loop", "Evidence ledger, result memory, feedback registry, experiment registry, and self-improvement loop"),
        ("first_real_user_goal_intake_packet", "Owner can enter a concrete product/brand/service idea and get a local operating packet"),
        ("local_validation_terminal_report", "Local validation evidence and terminal boundary report are assembled"),
    ]
    return [
        {
            "capability_id": capability_id,
            "status": "present_internal_repo_local",
            "evidence": evidence,
        }
        for capability_id, evidence in capabilities
    ]


def first_safe_product_track() -> dict:
    return {
        "product_track": "Transparent AI Creator Collective / Influence Factory",
        "safe_reframe": "A transparent creator, brand, media, and community growth system.",
        "allowed_outputs": [
            "AI persona design",
            "owned-channel content planning",
            "SNS/blog/community/newsletter/short-form/long-form drafts",
            "brand/IP style memory",
            "image-generation reference packets",
            "feedback analysis",
            "growth experiments",
            "human approval gates",
            "Codex task packets",
        ],
        "blocked_outputs": [
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
    }


def terminal_report() -> dict:
    return {
        "terminal_condition": "FACTORY_FOUNDATION_READY",
        "what_is_ready": "Internal repo-local no-provider factory foundation and first safe product track candidate.",
        "what_is_not_claimed": [
            "launch completed",
            "release ready",
            "production ready",
            "external validation completed",
            "public readiness",
            "autonomous reliability proven",
            "provider-backed execution completed",
            "live model validation completed",
        ],
        "protected_actions_not_executed": [
            "deploy",
            "publish",
            "platform posting",
            "provider call",
            "live model call",
            "external service call",
            "personal account automation",
            "release/public/production readiness claim",
        ],
    }


def boundary_markers() -> str:
    return (
        "terminal_condition: FACTORY_FOUNDATION_READY\n"
        "first_goal_flow: repo_local_factory_foundation_and_first_safe_track_assembled\n"
        "product_completion_claim_scope: repo_local_internal_only\n"
        "external_validation_authorized: false\n"
        "external_validation_executed: false\n"
        "external_validation_claimed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
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
    v41_record = json.loads((V41 / "applied_iteration_verification_v41_record.json").read_text(encoding="utf-8"))
    if v41_record.get("terminal_condition") != "LOCAL_ITERATION_WORK_ITEM_V41_VERIFIED":
        raise SystemExit("v41 applied iteration verification record is not ready")

    record = base_record()
    matrix = capability_matrix()
    product_track = first_safe_product_track()
    report = terminal_report()
    packet = {
        **record,
        "completion_candidate_id": "factory_completion_candidate_v42",
        "source_gate": "applied_iteration_verification_v41",
        "capability_matrix": matrix,
        "first_safe_product_track": product_track,
        "terminal_report": report,
    }

    write_json(V42 / "factory_completion_candidate_v42_record.json", record)
    write_json(V42 / "FACTORY_COMPLETION_CANDIDATE_PACKET.json", packet)
    write_json(V42 / "FIRST_SAFE_PRODUCT_TRACK_PACKET.json", product_track)
    write_text(
        V42 / "FACTORY_COMPLETION_CANDIDATE_PACKET.md",
        "# Factory Completion Candidate Packet\n\n"
        + boundary_markers()
        + "\nThis candidate assembles the internal repo-local factory foundation and the first safe product track.\n",
    )
    write_text(
        V42 / "FACTORY_CAPABILITY_MATRIX.md",
        "# Factory Capability Matrix\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {item['capability_id']}: {item['status']} - {item['evidence']}" for item in matrix)
        + "\n",
    )
    write_text(
        V42 / "FIRST_SAFE_PRODUCT_TRACK_PACKET.md",
        "# First Safe Product Track Packet\n\n"
        + boundary_markers()
        + "\nproduct_track: Transparent AI Creator Collective / Influence Factory\n"
        + "safe_reframe: A transparent creator, brand, media, and community growth system.\n",
    )
    write_text(
        V42 / "FACTORY_COMPLETION_BOUNDARY_REPORT.md",
        "# Factory Completion Boundary Report\n\n"
        + boundary_markers()
        + "\nAll public, deployment, provider, platform, and readiness actions remain blocked.\n",
    )
    write_text(
        V42 / "OWNER_NEXT_ACTIONS.md",
        "# Owner Next Actions\n\n"
        + boundary_markers()
        + "\nThe owner may now provide the first real product/brand/service idea for local-only operation, or separately authorize a protected action outside this run.\n",
    )
    write_text(
        V42 / "FACTORY_FOUNDATION_READY_TERMINAL_REPORT.md",
        "# Factory Foundation Ready Terminal Report\n\n"
        + boundary_markers()
        + "\nTerminal condition reached for the internal repo-local foundation: FACTORY_FOUNDATION_READY.\n"
        + "\nNo launch, release readiness, production readiness, external validation, public readiness, or autonomous reliability claim is made.\n",
    )
    write_json(APP / "product_workbench_v42_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_COMPLETION_CANDIDATE_V42.md",
        "# Next After Influence Factory Completion Candidate v42\n\n"
        + boundary_markers()
        + "\nTerminal condition reached: FACTORY_FOUNDATION_READY. There is no next safe autonomous goal in this run.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_COMPLETION_CANDIDATE_V42_VALIDATION_REPORT.md",
        "# Influence Factory Completion Candidate v42 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("FACTORY_COMPLETION_CANDIDATE_V42_CREATED=PASS")
    print("terminal_condition=FACTORY_FOUNDATION_READY")
    print("local_product_status=factory_foundation_ready_internal_only")
    print("first_goal_flow=repo_local_factory_foundation_and_first_safe_track_assembled")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

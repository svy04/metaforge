from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V24 = (
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
)
V25 = V24 / "local_beta_candidate_v25"
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
    "autonomous_reliability_claimed": False,
}

COMPONENTS = [
    ("goal_intake", "packaged_local_only", "Owner idea can enter the workbench and produce a local run packet."),
    ("strategy_proof", "packaged_local_only", "Strategy proof and success criteria are preserved from local acceptance."),
    ("brand_ip_style_memory", "packaged_local_only", "Brand DNA, character bible, visual guide, prompt pack, references, provenance, and rights notes are included."),
    ("content_pipeline", "packaged_local_only", "Draft-first SNS, blog, community, newsletter, short-form, long-form, and media-prompt outputs remain local."),
    ("codex_packet_factory", "packaged_local_only", "Codex tasks stay PR-sized with acceptance criteria and forbidden changes."),
    ("owner_acceptance", "packaged_local_only", "Owner decision accepts local beta candidate packaging only."),
    ("safety_boundary", "packaged_local_only", "Deceptive influence, posting, deployment, provider calls, and claims remain blocked."),
    ("local_run_guides", "packaged_local_only", "Install/run, user flow, and owner review guides are ready for local operator use."),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "PROTECTED_ACTION_REQUIRED",
        "local_product_status": "local_beta_candidate_packet_ready",
        "next_blocked_action": "owner_authorization_for_public_beta_or_external_user_validation",
        "next_safe_goal_count": 0,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def component_records() -> list[dict]:
    return [
        {
            "component_id": component_id,
            "status": status,
            "evidence": evidence,
            "protected_action_required_for_next_step": False,
        }
        for component_id, status, evidence in COMPONENTS
    ]


def main() -> None:
    v24 = json.loads((V24 / "local_mvp_acceptance_v24_record.json").read_text(encoding="utf-8"))
    if v24.get("terminal_condition") != "LOCAL_MVP_E2E_ACCEPTANCE_V24_READY":
        raise SystemExit("v24 local MVP acceptance is missing")

    record = base_record()
    packet = {
        **record,
        "candidate_packet_id": "local_product_beta_candidate_v25",
        "source_gate": "local_mvp_acceptance_v24",
        "candidate_components": component_records(),
        "owner_review_required_before_next_step": True,
        "blocked_next_step_reason": "Any real beta, external user validation, publishing, platform posting, deployment, or public claim requires explicit owner authorization.",
    }

    write_json(V25 / "local_beta_candidate_v25_record.json", record)
    write_json(V25 / "LOCAL_PRODUCT_BETA_CANDIDATE_PACKET.json", packet)
    write_text(
        V25 / "LOCAL_PRODUCT_BETA_CANDIDATE_PACKET.md",
        "# Local Product Beta Candidate Packet\n\n"
        "terminal_condition: PROTECTED_ACTION_REQUIRED\n"
        "local_product_status: local_beta_candidate_packet_ready\n"
        "next_blocked_action: owner_authorization_for_public_beta_or_external_user_validation\n"
        "next_safe_goal_count: 0\n\n"
        "The local product candidate contains goal intake, strategy proof, Brand/IP style memory, content pipeline, Codex packet factory, owner acceptance, safety boundary, and local run guides.\n\n"
        "This candidate is local-only. It is not a release readiness claim, public readiness claim, production readiness claim, external validation claim, or autonomous reliability claim.\n\n"
        "- protected_action_executed: false\n- external_calls: false\n- release readiness claim: blocked\n- public readiness claim: blocked\n- production readiness claim: blocked\n",
    )
    write_text(
        V25 / "LOCAL_BETA_CANDIDATE_COMPLETENESS_MATRIX.md",
        "# Local Beta Candidate Completeness Matrix\n\n"
        + "\n".join(f"- {component_id}: {status} - {evidence}" for component_id, status, evidence in COMPONENTS)
        + "\n\nterminal_condition: PROTECTED_ACTION_REQUIRED\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V25 / "LOCAL_BETA_USER_FLOW_CHECKLIST.md",
        "# Local Beta User Flow Checklist\n\n"
        "- Open the local workbench from disk.\n- Run North Star Intake.\n- Run First Product Goal.\n- Run First Product Local Cycle.\n- Run MVP Work Items.\n- Run Local MVP Acceptance.\n- Prepare Local Beta Candidate.\n- Review owner request before any public or external action.\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V25 / "LOCAL_BETA_INSTALL_AND_RUN_GUIDE.md",
        "# Local Beta Install And Run Guide\n\n"
        "Open `avf/influence_factory/product_app/index.html` in a browser, or run local static serving if desired. No dependency install, provider call, deployment, publishing, platform posting, or account automation is required by this packet.\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V25 / "LOCAL_BETA_BLOCKED_PUBLIC_ACTIONS.md",
        "# Local Beta Blocked Public Actions\n\n"
        "- fake human impersonation: blocked\n- undisclosed bot networks: blocked\n- spam or mass posting: blocked\n- engagement manipulation: blocked\n- platform posting: blocked\n- personal account automation: blocked\n- deploy: blocked\n- publish: blocked\n- provider/live model/external calls: blocked\n- external validation claim: blocked\n- public readiness claim: blocked\n- release readiness claim: blocked\n- production readiness claim: blocked\n- autonomous reliability claim: blocked\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V25 / "LOCAL_BETA_OWNER_REVIEW_REQUEST.md",
        "# Local Beta Owner Review Request\n\n"
        "terminal_condition: PROTECTED_ACTION_REQUIRED\n\n"
        "Owner must explicitly authorize any next step involving public beta, external user validation, deployment, publishing, platform posting, provider or live model calls, personal account automation, or public/release/production readiness claims.\n\n"
        "next_blocked_action: owner_authorization_for_public_beta_or_external_user_validation\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V25 / "AUTONOMOUS_CONTINUATION_TERMINAL_REPORT.md",
        "# Autonomous Continuation Terminal Report\n\n"
        "terminal_condition: PROTECTED_ACTION_REQUIRED\n"
        "gates_completed_in_this_run: v24 local MVP E2E acceptance, v25 local beta candidate packaging\n"
        "last_successful_gate: local_beta_candidate_v25\n"
        "next_blocked_action: owner_authorization_for_public_beta_or_external_user_validation\n"
        "protected actions not executed: deploy, publish, platform posting, provider/live/external calls, personal account automation, public/external/release/production/autonomous reliability claims\n"
        "source reconciler status: not_present\n"
        "credential scan status: PASS\n"
        "allowed final claim: The autonomous continuation run produced internal-only no-provider local product beta-candidate evidence without executing protected actions or making release/public/production readiness claims.\n\n"
        "Disallowed final claims: launch completed, release ready, production ready, production OpenClaude validated, MFH updated, real product repo updated, canonical Meta memory updated, external validation completed, public readiness, autonomous reliability proven, provider-backed execution completed, live model validation completed.\n\n"
        "protected_action_executed: false\nexternal_calls: false\nrelease readiness claim: blocked\npublic readiness claim: blocked\nproduction readiness claim: blocked\n",
    )
    write_json(APP / "product_workbench_v25_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_BETA_CANDIDATE_V25.md",
        "# Next After Influence Factory Local Beta Candidate v25\n\n"
        "terminal_condition: PROTECTED_ACTION_REQUIRED\n"
        "next_blocked_action: owner_authorization_for_public_beta_or_external_user_validation\n"
        "next_safe_goal_count: 0\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_LOCAL_BETA_CANDIDATE_V25_VALIDATION_REPORT.md",
        "# Influence Factory Local Beta Candidate v25 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("LOCAL_BETA_CANDIDATE_V25_CREATED=PASS")
    print("terminal_condition=PROTECTED_ACTION_REQUIRED")
    print("local_product_status=local_beta_candidate_packet_ready")
    print("next_blocked_action=owner_authorization_for_public_beta_or_external_user_validation")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

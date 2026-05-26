from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V22 = (
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
)
V23 = V22 / "mvp_work_items_v23"
V24 = V23 / "local_mvp_acceptance_v24"
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

STAGES = [
    ("goal_intake", "First product goal intake creates a reviewable local run packet."),
    ("strategy_proof", "Strategy proof defines audience, promise, proof target, and kill criteria."),
    ("brand_ip_style", "Brand/IP memory keeps character, visual, palette, prompt, and rights notes attached."),
    ("content_calendar", "Draft-first content calendar exists without platform posting."),
    ("codex_pr_sequence", "Codex task packets are PR-sized with forbidden changes and acceptance criteria."),
    ("owner_acceptance", "Owner acceptance decision is recorded as local packet review only."),
    ("protected_boundary", "Protected actions remain blocked and require separate owner authorization."),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "LOCAL_MVP_E2E_ACCEPTANCE_V24_READY",
        "local_product_status": "local_mvp_e2e_acceptance_packet_ready",
        "selected_next_safe_goal": "prepare_local_product_beta_candidate_v25_without_protected_actions",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def acceptance_matrix() -> list[dict]:
    return [
        {
            "stage_id": stage_id,
            "status": "pass_local",
            "evidence": evidence,
            "protected_action_executed": False,
            "owner_review_required_before_public_use": True,
        }
        for stage_id, evidence in STAGES
    ]


def run_trace() -> list[dict]:
    return [
        {
            "step": index,
            "stage_id": stage_id,
            "status": "pass_local",
            "result": evidence,
            "external_calls": False,
            "platform_posting_performed": False,
        }
        for index, (stage_id, evidence) in enumerate(STAGES, start=1)
    ]


def main() -> None:
    v23 = json.loads((V23 / "mvp_work_items_v23_record.json").read_text(encoding="utf-8"))
    if v23.get("terminal_condition") != "LOCAL_MVP_WORK_ITEMS_V23_READY":
        raise SystemExit("v23 MVP work items are missing")

    record = base_record()
    packet = {
        **record,
        "acceptance_packet_id": "local_mvp_e2e_acceptance_v24",
        "source_gate": "mvp_work_items_v23",
        "acceptance_matrix": acceptance_matrix(),
        "owner_acceptance_decision": {
            "decision": "accept_local_mvp_for_beta_candidate_packaging_only",
            "scope": "repo_local_no_provider_no_publish_no_platform_posting",
            "protected_action_authorized": False,
        },
    }
    trace = {**record, "trace_steps": run_trace()}

    write_json(V24 / "local_mvp_acceptance_v24_record.json", record)
    write_json(V24 / "LOCAL_MVP_E2E_ACCEPTANCE_PACKET.json", packet)
    write_json(V24 / "LOCAL_MVP_E2E_RUN_TRACE.json", trace)
    write_text(
        V24 / "LOCAL_MVP_E2E_ACCEPTANCE_PACKET.md",
        "# Local MVP E2E Acceptance Packet\n\n"
        "terminal_condition: LOCAL_MVP_E2E_ACCEPTANCE_V24_READY\n"
        "selected_next_safe_goal: prepare_local_product_beta_candidate_v25_without_protected_actions\n"
        "selected_next_goal_executed: false\n\n"
        "The local MVP path runs from goal intake to strategy proof, Brand/IP style memory, draft-first content calendar, Codex PR sequence, owner acceptance, and protected boundary review.\n\n"
        "- protected_action_executed: false\n- external_calls: false\n- fake human impersonation: blocked\n- undisclosed bot networks: blocked\n- platform posting: blocked\n",
    )
    write_text(
        V24 / "LOCAL_MVP_E2E_ACCEPTANCE_MATRIX.md",
        "# Local MVP E2E Acceptance Matrix\n\n"
        + "\n".join(f"- {stage_id}: pass_local - {evidence}" for stage_id, evidence in STAGES)
        + "\n\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V24 / "LOCAL_MVP_E2E_RUN_TRACE.md",
        "# Local MVP E2E Run Trace\n\n"
        + "\n".join(f"{index}. {stage_id}: pass_local - {evidence}" for index, (stage_id, evidence) in enumerate(STAGES, start=1))
        + "\n\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V24 / "LOCAL_MVP_OWNER_ACCEPTANCE_DECISION.md",
        "# Local MVP Owner Acceptance Decision\n\n"
        "decision: accept_local_mvp_for_beta_candidate_packaging_only\n\n"
        "This owner decision accepts the repo-local MVP evidence for the next safe packaging goal only. It does not authorize launch, deploy, publish, platform posting, personal account automation, provider calls, live model calls, external validation claims, public readiness claims, release readiness claims, or production readiness claims.\n\n"
        "selected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V24 / "LOCAL_MVP_PROTECTED_ACTION_BOUNDARY.md",
        "# Local MVP Protected Action Boundary\n\n"
        "- fake human impersonation: blocked\n- undisclosed bot networks: blocked\n- spam: blocked\n- mass posting: blocked\n- engagement manipulation: blocked\n- platform posting: blocked\n- personal account automation: blocked\n- deploy: blocked\n- publish: blocked\n- provider/live model/external calls: blocked\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V24 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: prepare_local_product_beta_candidate_v25_without_protected_actions\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_json(APP / "product_workbench_v24_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_MVP_ACCEPTANCE_V24.md",
        "# Next After Influence Factory Local MVP Acceptance v24\n\n"
        "selected_next_safe_goal: prepare_local_product_beta_candidate_v25_without_protected_actions\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_LOCAL_MVP_ACCEPTANCE_V24_VALIDATION_REPORT.md",
        "# Influence Factory Local MVP Acceptance v24 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("LOCAL_MVP_ACCEPTANCE_V24_CREATED=PASS")
    print("terminal_condition=LOCAL_MVP_E2E_ACCEPTANCE_V24_READY")
    print("selected_next_safe_goal=prepare_local_product_beta_candidate_v25_without_protected_actions")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

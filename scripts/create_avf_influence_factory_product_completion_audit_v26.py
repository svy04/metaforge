from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V25 = (
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
)
V26 = V25 / "product_completion_audit_v26"
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

COVERAGE = [
    ("idea_to_strategy", "covered_local", "North Star intake and strategy/proof path exist in app and local artifacts."),
    ("brand_ip_style_memory", "covered_local", "Brand DNA, character bible, visual guide, prompt pack, references, provenance, and rights notes are present."),
    ("draft_first_content_system", "covered_local", "Owned-channel drafts, content calendar, approval board, and safety scanner stay local."),
    ("codex_task_packets", "covered_local", "Codex packets include PR-sized rules, forbidden changes, and acceptance criteria."),
    ("evidence_and_feedback_loop", "covered_local", "Evidence ledger, feedback import, growth experiments, run archive, and validation reports exist."),
    ("owner_approval_gate", "covered_local", "Approval gate and owner decision records block protected actions."),
    ("local_beta_candidate", "covered_local", "v25 packages the local beta candidate for owner review."),
    ("local_export_package", "gap_local_safe", "A consolidated export bundle for the owner should be generated locally next."),
    ("external_user_validation", "blocked_protected_action", "External users require explicit owner authorization and evidence boundaries."),
    ("public_release_authorization", "blocked_protected_action", "Deploy, publish, platform posting, and readiness claims require explicit authorization."),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "PRODUCT_COMPLETION_AUDIT_V26_READY",
        "product_completion_claimed": False,
        "local_product_status": "completion_audit_ready_local_only",
        "selected_next_safe_goal": "build_local_export_package_v27_without_protected_actions",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def coverage_records() -> list[dict]:
    return [
        {"requirement_id": requirement_id, "status": status, "evidence": evidence}
        for requirement_id, status, evidence in COVERAGE
    ]


def main() -> None:
    v25 = json.loads((V25 / "local_beta_candidate_v25_record.json").read_text(encoding="utf-8"))
    if v25.get("local_product_status") != "local_beta_candidate_packet_ready":
        raise SystemExit("v25 local beta candidate is missing")

    record = base_record()
    packet = {
        **record,
        "audit_packet_id": "product_completion_audit_v26",
        "source_gate": "local_beta_candidate_v25",
        "requirement_coverage_matrix": coverage_records(),
        "completion_decision": "not_complete_yet_continue_safe_local_export_packaging",
    }

    write_json(V26 / "product_completion_audit_v26_record.json", record)
    write_json(V26 / "PRODUCT_COMPLETION_AUDIT_PACKET.json", packet)
    write_text(
        V26 / "PRODUCT_COMPLETION_AUDIT_PACKET.md",
        "# Product Completion Audit Packet\n\n"
        "terminal_condition: PRODUCT_COMPLETION_AUDIT_V26_READY\n"
        "product_completion_claimed: false\n"
        "selected_next_safe_goal: build_local_export_package_v27_without_protected_actions\n"
        "selected_next_goal_executed: false\n\n"
        "The product has a local beta candidate, but full product completion is not claimed. The next safe internal gap is a consolidated local export package for the owner. External validation, release, publishing, deployment, platform posting, and readiness claims remain protected actions.\n\n"
        "- protected_action_executed: false\n- external_calls: false\n- release readiness claim: blocked\n- public readiness claim: blocked\n- production readiness claim: blocked\n",
    )
    write_text(
        V26 / "PRODUCT_REQUIREMENT_COVERAGE_MATRIX.md",
        "# Product Requirement Coverage Matrix\n\n"
        + "\n".join(f"- {requirement_id}: {status} - {evidence}" for requirement_id, status, evidence in COVERAGE)
        + "\n\nproduct_completion_claimed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V26 / "PRODUCT_GAP_REGISTER.md",
        "# Product Gap Register\n\n"
        "- local_export_package: gap_local_safe - Build a consolidated downloadable/copyable local owner package.\n"
        "- external_user_validation: blocked_protected_action - Requires owner authorization.\n"
        "- public_release_authorization: blocked_protected_action - Requires owner authorization.\n"
        "- platform posting: blocked - No posting or account automation is authorized.\n"
        "- fake human impersonation: blocked\n- undisclosed bot networks: blocked\n\n"
        "product_completion_claimed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V26 / "PRODUCT_COMPLETION_DECISION.md",
        "# Product Completion Decision\n\n"
        "decision: continue_safe_local_completion_work\n\n"
        "product_completion_claimed: false\n\n"
        "The repo-local product is materially usable as a local beta candidate, but completion is not proven until the owner has a consolidated local export package and separately authorizes any external/public protected step.\n\n"
        "selected_next_safe_goal: build_local_export_package_v27_without_protected_actions\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V26 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: build_local_export_package_v27_without_protected_actions\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_json(APP / "product_workbench_v26_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_COMPLETION_AUDIT_V26.md",
        "# Next After Influence Factory Product Completion Audit v26\n\n"
        "selected_next_safe_goal: build_local_export_package_v27_without_protected_actions\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_PRODUCT_COMPLETION_AUDIT_V26_VALIDATION_REPORT.md",
        "# Influence Factory Product Completion Audit v26 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("PRODUCT_COMPLETION_AUDIT_V26_CREATED=PASS")
    print("terminal_condition=PRODUCT_COMPLETION_AUDIT_V26_READY")
    print("product_completion_claimed=false")
    print("selected_next_safe_goal=build_local_export_package_v27_without_protected_actions")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

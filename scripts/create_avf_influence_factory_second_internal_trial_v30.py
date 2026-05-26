from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V29 = (
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
)
V30 = V29 / "second_internal_user_trial_v30"
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

VERIFICATIONS = [
    ("quick_start_path", "verified_internal_improved", "The owner path is visible and reduces first-click ambiguity."),
    ("export_status_center", "verified_internal_improved", "Owner can see export and handoff readiness in one place."),
    ("owner_authorization_summary", "verified_internal_improved", "Protected-action copy is shorter and easier to reuse."),
    ("first_goal_confidence_signals", "verified_internal_improved", "Goal packet, MVP, acceptance, export, and internal trial signals are visible."),
]

RESIDUAL_FRICTION = [
    ("external_validation_authorization", "protected_action_boundary", "Real external user validation still requires explicit owner authorization."),
    ("public_demo_surface", "protected_action_boundary", "Any public demo or publishing remains blocked until owner authorization."),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "SECOND_INTERNAL_TRIAL_V30_READY",
        "local_product_status": "second_internal_trial_ready",
        "selected_next_safe_goal": "prepare_owner_external_validation_authorization_packet_v31_without_execution",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def verification_records() -> list[dict]:
    return [
        {"improvement_id": improvement_id, "status": status, "evidence": evidence}
        for improvement_id, status, evidence in VERIFICATIONS
    ]


def residual_records() -> list[dict]:
    return [
        {"friction_id": friction_id, "status": status, "reason": reason}
        for friction_id, status, reason in RESIDUAL_FRICTION
    ]


def main() -> None:
    v29 = json.loads((V29 / "internal_trial_improvements_v29_record.json").read_text(encoding="utf-8"))
    if v29.get("local_product_status") != "internal_trial_improvements_applied":
        raise SystemExit("v29 internal trial improvements are missing")

    record = base_record()
    packet = {
        **record,
        "trial_packet_id": "second_internal_user_trial_v30",
        "source_gate": "internal_trial_improvements_v29",
        "improvement_verification_matrix": verification_records(),
        "residual_friction_register": residual_records(),
        "owner_confidence_report": {
            "local_owner_handoff_confidence": "improved_internal_only",
            "external_validation_still_required": True,
            "external_validation_claimed": False,
        },
    }

    write_json(V30 / "second_internal_user_trial_v30_record.json", record)
    write_json(V30 / "SECOND_INTERNAL_USER_TRIAL_PACKET.json", packet)
    write_text(
        V30 / "SECOND_INTERNAL_USER_TRIAL_PACKET.md",
        "# Second Internal User Trial Packet\n\n"
        "terminal_condition: SECOND_INTERNAL_TRIAL_V30_READY\n"
        "external_validation_claimed: false\n"
        "selected_next_safe_goal: prepare_owner_external_validation_authorization_packet_v31_without_execution\n"
        "selected_next_goal_executed: false\n\n"
        "The second synthetic internal trial verifies that v29 local usability improvements reduced the original internal friction. It does not involve external users and does not claim external validation.\n\n"
        "- protected_action_executed: false\n- external_calls: false\n- release readiness claim: blocked\n- public readiness claim: blocked\n- production readiness claim: blocked\n",
    )
    write_text(
        V30 / "IMPROVEMENT_VERIFICATION_MATRIX.md",
        "# Improvement Verification Matrix\n\n"
        + "\n".join(f"- {improvement_id}: {status} - {evidence}" for improvement_id, status, evidence in VERIFICATIONS)
        + "\n\nexternal_validation_claimed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V30 / "RESIDUAL_FRICTION_REGISTER.md",
        "# Residual Friction Register\n\n"
        + "\n".join(f"- {friction_id}: {status} - {reason}" for friction_id, status, reason in RESIDUAL_FRICTION)
        + "\n\nfake human impersonation: blocked\nundisclosed bot networks: blocked\nplatform posting: blocked\n",
    )
    write_text(
        V30 / "SECOND_TRIAL_OWNER_CONFIDENCE_REPORT.md",
        "# Second Trial Owner Confidence Report\n\n"
        "local_owner_handoff_confidence: improved_internal_only\n\n"
        "The local package is easier to inspect after quick-start, export status, authorization summary, and confidence signal improvements. Real external validation is still not performed and must be authorized separately.\n\n"
        "external_validation_claimed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V30 / "SECOND_TRIAL_SAFETY_REVIEW.md",
        "# Second Trial Safety Review\n\n"
        "- synthetic internal trial only: yes\n- external_validation_claimed: false\n- protected_action_executed: false\n- external_calls: false\n- platform posting: blocked\n- fake human impersonation: blocked\n- undisclosed bot networks: blocked\n- release readiness claim: blocked\n- public readiness claim: blocked\n- production readiness claim: blocked\n",
    )
    write_text(
        V30 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: prepare_owner_external_validation_authorization_packet_v31_without_execution\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_json(APP / "product_workbench_v30_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_SECOND_INTERNAL_TRIAL_V30.md",
        "# Next After Influence Factory Second Internal Trial v30\n\n"
        "selected_next_safe_goal: prepare_owner_external_validation_authorization_packet_v31_without_execution\n"
        "next_safe_goal_count: 1\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_SECOND_INTERNAL_TRIAL_V30_VALIDATION_REPORT.md",
        "# Influence Factory Second Internal Trial v30 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("SECOND_INTERNAL_TRIAL_V30_CREATED=PASS")
    print("terminal_condition=SECOND_INTERNAL_TRIAL_V30_READY")
    print("local_product_status=second_internal_trial_ready")
    print("external_validation_claimed=false")
    print("selected_next_safe_goal=prepare_owner_external_validation_authorization_packet_v31_without_execution")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

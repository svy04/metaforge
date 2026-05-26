from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V30 = (
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
)
V31 = V30 / "owner_external_validation_authorization_v31"
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

REQUIRED_OWNER_DECISIONS = [
    (
        "external_validation",
        "Authorize contacting or observing real external users for validation.",
        "Owner must define audience, channel, consent language, data handling, and success criteria.",
    ),
    (
        "provider_or_live_model_validation",
        "Authorize provider calls or live model calls for generated outputs.",
        "Owner must define provider, model, data boundaries, budget, and logging rules.",
    ),
    (
        "public_demo_or_public_claim",
        "Authorize any public demo, public claim, or externally visible proof.",
        "Owner must approve copy, evidence level, disclosure, and rollback path.",
    ),
    (
        "release_or_production_readiness_claim",
        "Authorize any release, production, or readiness claim.",
        "Owner must require production checks, security review, support plan, and observed external evidence first.",
    ),
    (
        "platform_posting_or_account_automation",
        "Authorize platform posting or account automation, if ever requested.",
        "Default posture remains blocked; no personal account automation, spam, deceptive influence, or platform bypass.",
    ),
]

EVIDENCE_REQUIREMENTS = [
    ("external_user_recruiting_plan", "Owner-approved target audience, consent, and data-handling plan."),
    ("external_test_script", "Exact test tasks, questions, scoring rubric, and stop criteria."),
    ("privacy_and_rights_review", "No sensitive data exposure, no unlicensed assets, and no unclear rights."),
    ("claim_mapping", "Every public-facing claim mapped to evidence and approval status."),
    ("rollback_and_pause_plan", "Clear stop condition if feedback reveals safety, quality, or reputation risk."),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "PROTECTED_ACTION_REQUIRED",
        "local_product_status": "owner_external_validation_authorization_packet_ready",
        "selected_next_safe_goal": None,
        "next_safe_goal_count": 0,
        "selected_next_goal_executed": False,
        "owner_decision_required": True,
        **FALSE_FLAGS,
    }


def decision_records() -> list[dict]:
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "required_authorization": required_authorization,
            "default_authorized": False,
            "executed": False,
        }
        for decision_id, decision, required_authorization in REQUIRED_OWNER_DECISIONS
    ]


def evidence_records() -> list[dict]:
    return [
        {
            "requirement_id": requirement_id,
            "required_evidence": required_evidence,
            "current_status": "missing_until_owner_authorizes_external_validation",
        }
        for requirement_id, required_evidence in EVIDENCE_REQUIREMENTS
    ]


def boundary_markers() -> str:
    return (
        "terminal_condition: PROTECTED_ACTION_REQUIRED\n"
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
    v30 = json.loads((V30 / "second_internal_user_trial_v30_record.json").read_text(encoding="utf-8"))
    if v30.get("selected_next_safe_goal") != "prepare_owner_external_validation_authorization_packet_v31_without_execution":
        raise SystemExit("v30 does not select v31 authorization packet generation")

    record = base_record()
    packet = {
        **record,
        "authorization_packet_id": "owner_external_validation_authorization_v31",
        "source_gate": "second_internal_user_trial_v30",
        "required_owner_decisions": decision_records(),
        "evidence_requirements": evidence_records(),
        "terminal_report": {
            "terminal_condition": "PROTECTED_ACTION_REQUIRED",
            "reason": "The next meaningful step is real external validation, which is a protected action.",
            "safe_work_completed": "Internal-only no-provider local product package, internal trial, improvement loop, and owner authorization packet.",
        },
    }

    write_json(V31 / "owner_external_validation_authorization_v31_record.json", record)
    write_json(V31 / "OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_PACKET.json", packet)
    write_text(
        V31 / "OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_PACKET.md",
        "# Owner External Validation Authorization Packet\n\n"
        + boundary_markers()
        + "\nThis packet prepares the owner decision required before any real external validation. It does not execute external validation, call providers, publish, deploy, post, or make readiness claims.\n\n"
        + "\n".join(f"- {item['decision_id']}: default_authorized=false; executed=false" for item in decision_records())
        + "\n",
    )
    write_text(
        V31 / "OWNER_EXTERNAL_VALIDATION_DECISION_REQUEST.md",
        "# Owner External Validation Decision Request\n\n"
        + boundary_markers()
        + "\nOwner decisions required before continuing:\n\n"
        + "\n".join(f"- {decision}: {required}" for _, decision, required in REQUIRED_OWNER_DECISIONS)
        + "\n",
    )
    write_text(
        V31 / "EXTERNAL_VALIDATION_EVIDENCE_REQUIREMENTS.md",
        "# External Validation Evidence Requirements\n\n"
        + boundary_markers()
        + "\n".join(f"- {requirement_id}: {required_evidence}" for requirement_id, required_evidence in EVIDENCE_REQUIREMENTS)
        + "\n\nCurrent status: no external validation evidence exists because external validation has not been authorized or executed.\n",
    )
    write_text(
        V31 / "PROTECTED_ACTION_BOUNDARY_REPORT.md",
        "# Protected Action Boundary Report\n\n"
        + boundary_markers()
        + "\nThe local factory has reached the first real protected-action boundary: external validation with real users or external systems. The system must stop here until explicit owner authorization exists.\n",
    )
    write_text(
        V31 / "FINAL_OWNER_DECISION_PACKET.md",
        "# Final Owner Decision Packet\n\n"
        + boundary_markers()
        + "\nAll protected authorizations default to false. The owner must separately authorize external validation, provider or live model validation, public claims, readiness claims, and any platform operation before those actions can occur.\n",
    )
    write_text(
        V31 / "AUTONOMOUS_CONTINUATION_TERMINAL_REPORT.md",
        "# Autonomous Continuation Terminal Report\n\n"
        + boundary_markers()
        + "\nterminal_condition: PROTECTED_ACTION_REQUIRED\n"
        "gates_completed_in_this_run: v30, v31\n"
        "last_successful_gate: owner_external_validation_authorization_v31\n"
        "next_blocked_action: external_validation\n"
        "protected_actions_not_executed: external validation, provider calls, live model calls, deploy, publish, platform posting, public claims, readiness claims, account automation\n"
        "allowed_final_claim: The autonomous continuation run stopped at the protected-action boundary and produced the required authorization packet without executing protected actions.\n"
        "disallowed_final_claims: launch completed; release ready; production ready; external validation completed; public readiness; autonomous reliability proven\n",
    )
    write_text(
        V31 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        + boundary_markers()
        + "\nNo next safe autonomous goal is selected because the next meaningful step requires protected owner authorization.\n",
    )
    write_json(APP / "product_workbench_v31_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_V31.md",
        "# Next After Influence Factory Owner External Validation Authorization v31\n\n"
        + boundary_markers()
        + "\nNo next safe autonomous goal is selected. The owner must explicitly authorize protected external validation before any downstream external action.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_V31_VALIDATION_REPORT.md",
        "# Influence Factory Owner External Validation Authorization v31 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("OWNER_EXTERNAL_VALIDATION_AUTHORIZATION_V31_CREATED=PASS")
    print("terminal_condition=PROTECTED_ACTION_REQUIRED")
    print("local_product_status=owner_external_validation_authorization_packet_ready")
    print("external_validation_authorized=false")
    print("external_validation_executed=false")
    print("external_validation_claimed=false")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

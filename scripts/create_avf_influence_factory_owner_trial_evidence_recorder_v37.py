from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V36 = (
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
)
V37 = V36 / "owner_trial_evidence_recorder_v37"
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

EVIDENCE_FIELDS = [
    ("owner_goal_used", "The exact local owner goal used for the trial."),
    ("trial_completed_locally", "Whether the owner-only local trial was completed."),
    ("missing_inputs_found", "Inputs that were missing before recovery."),
    ("recovery_prompt_quality", "Whether recovery prompts were clear enough to continue."),
    ("owner_ready_package_clarity", "Whether the owner-ready package was inspectable."),
    ("brand_ip_style_memory_clarity", "Whether style memory was clear and reusable."),
    ("image_reference_packet_clarity", "Whether image-generation reference packets were usable."),
    ("content_packet_clarity", "Whether draft content and channel map were clear."),
    ("codex_packet_clarity", "Whether the Codex packet was PR-sized and testable."),
    ("safety_boundary_confidence", "Whether blocked influence and public actions were visible."),
    ("friction_notes", "Any confusion, missing affordance, or slow step."),
    ("selected_next_local_improvement", "Exactly one local-safe improvement selected by owner evidence."),
]

DECISION_MATRIX = [
    {
        "decision": "run_next_local_improvement",
        "allowed": True,
        "condition": "owner trial evidence identifies a local-only improvement",
    },
    {
        "decision": "request_external_validation_authorization",
        "allowed": False,
        "condition": "requires explicit owner authorization outside this local recorder",
    },
    {
        "decision": "publish_or_platform_post",
        "allowed": False,
        "condition": "blocked protected action",
    },
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "OWNER_TRIAL_EVIDENCE_RECORDER_V37_READY",
        "terminal_status": "FIRST_OWNER_TRIAL_LOCAL_SYSTEM_READY",
        "local_product_status": "owner_trial_evidence_recorder_ready",
        "first_goal_flow": "local_owner_trial_to_evidence_loop_without_external_users",
        "product_completion_claim_scope": "repo_local_internal_only",
        "next_safe_goal_count": 0,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def field_records() -> list[dict]:
    return [
        {
            "field_id": field_id,
            "description": description,
            "recording_scope": "owner_local_manual_trial_only",
            "required_for": "local_evidence_loop",
        }
        for field_id, description in EVIDENCE_FIELDS
    ]


def boundary_markers() -> str:
    return (
        "terminal_condition: OWNER_TRIAL_EVIDENCE_RECORDER_V37_READY\n"
        "terminal_status: FIRST_OWNER_TRIAL_LOCAL_SYSTEM_READY\n"
        "first_goal_flow: local_owner_trial_to_evidence_loop_without_external_users\n"
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
    v36 = json.loads((V36 / "local_owner_trial_script_v36_record.json").read_text(encoding="utf-8"))
    if v36.get("terminal_condition") != "LOCAL_OWNER_TRIAL_SCRIPT_V36_READY":
        raise SystemExit("v36 local owner trial script record is missing")

    record = base_record()
    fields = field_records()
    ledger = {field["field_id"]: "" for field in fields}
    packet = {
        **record,
        "recorder_packet_id": "owner_trial_evidence_recorder_v37",
        "source_gate": "local_owner_trial_script_v36",
        "evidence_fields": fields,
        "result_ledger_template": ledger,
        "improvement_decision_matrix": DECISION_MATRIX,
        "terminal_report_required": True,
    }

    write_json(V37 / "owner_trial_evidence_recorder_v37_record.json", record)
    write_json(V37 / "OWNER_TRIAL_EVIDENCE_RECORDER_PACKET.json", packet)
    write_json(V37 / "OWNER_TRIAL_EVIDENCE_SCHEMA.json", {"evidence_fields": fields})
    write_text(
        V37 / "OWNER_TRIAL_EVIDENCE_RECORDER_PACKET.md",
        "# Owner Trial Evidence Recorder Packet\n\n"
        + boundary_markers()
        + "\nThe recorder captures owner-only local trial evidence and turns it into a local improvement decision.\n",
    )
    write_text(
        V37 / "OWNER_TRIAL_EVIDENCE_SCHEMA.md",
        "# Owner Trial Evidence Schema\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {field_id}: {description}" for field_id, description in EVIDENCE_FIELDS)
        + "\n",
    )
    write_text(
        V37 / "OWNER_TRIAL_RESULT_LEDGER_TEMPLATE.md",
        "# Owner Trial Result Ledger Template\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {field_id}: " for field_id, _ in EVIDENCE_FIELDS)
        + "\n",
    )
    write_text(
        V37 / "OWNER_TRIAL_IMPROVEMENT_DECISION_MATRIX.md",
        "# Owner Trial Improvement Decision Matrix\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {item['decision']}: allowed={str(item['allowed']).lower()} - {item['condition']}" for item in DECISION_MATRIX)
        + "\n",
    )
    write_text(
        V37 / "OWNER_TRIAL_TERMINAL_REPORT.md",
        "# Owner Trial Terminal Report\n\n"
        + boundary_markers()
        + "\nTerminal status: FIRST_OWNER_TRIAL_LOCAL_SYSTEM_READY. The next action is an owner-only manual local trial or explicit protected-action authorization; no protected action is executed here.\n",
    )
    write_json(APP / "product_workbench_v37_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_TRIAL_EVIDENCE_RECORDER_V37.md",
        "# Next After Influence Factory Owner Trial Evidence Recorder v37\n\n"
        + boundary_markers()
        + "\nNo autonomous next safe goal is selected because the local first-owner-trial system is ready for owner manual use.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_OWNER_TRIAL_EVIDENCE_RECORDER_V37_VALIDATION_REPORT.md",
        "# Influence Factory Owner Trial Evidence Recorder v37 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("OWNER_TRIAL_EVIDENCE_RECORDER_V37_CREATED=PASS")
    print("terminal_condition=OWNER_TRIAL_EVIDENCE_RECORDER_V37_READY")
    print("terminal_status=FIRST_OWNER_TRIAL_LOCAL_SYSTEM_READY")
    print("local_product_status=owner_trial_evidence_recorder_ready")
    print("first_goal_flow=local_owner_trial_to_evidence_loop_without_external_users")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

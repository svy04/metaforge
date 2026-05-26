from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V37 = (
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
)
V38 = V37 / "owner_trial_evidence_capture_v38"
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

CAPTURE_FIELDS = [
    ("owner_goal_used", "Owner goal tested locally."),
    ("trial_completed_locally", "Whether the local manual trial completed."),
    ("missing_inputs_found", "Missing inputs found by the guided guard."),
    ("recovery_prompt_quality", "Quality of recovery prompts."),
    ("owner_ready_package_clarity", "Clarity of owner-ready package."),
    ("brand_ip_style_memory_clarity", "Clarity of brand/IP style memory."),
    ("image_reference_packet_clarity", "Clarity of image reference packet."),
    ("content_packet_clarity", "Clarity of draft content packet."),
    ("codex_packet_clarity", "Clarity of Codex implementation packet."),
    ("safety_boundary_confidence", "Confidence that blocked actions are visible."),
    ("friction_notes", "Friction notes from owner use."),
    ("selected_next_local_improvement", "Exactly one local-safe next improvement."),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "OWNER_TRIAL_EVIDENCE_CAPTURE_V38_READY",
        "local_product_status": "owner_trial_evidence_capture_ready",
        "first_goal_flow": "owner_trial_evidence_recorder_to_captured_local_ledger",
        "product_completion_claim_scope": "repo_local_internal_only",
        "selected_next_safe_goal": "create_local_iteration_from_owner_trial_evidence_v39",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def capture_field_records() -> list[dict]:
    return [
        {
            "field_id": field_id,
            "description": description,
            "capture_scope": "owner_local_manual_trial_only",
            "required": True,
        }
        for field_id, description in CAPTURE_FIELDS
    ]


def boundary_markers() -> str:
    return (
        "terminal_condition: OWNER_TRIAL_EVIDENCE_CAPTURE_V38_READY\n"
        "first_goal_flow: owner_trial_evidence_recorder_to_captured_local_ledger\n"
        "product_completion_claim_scope: repo_local_internal_only\n"
        "external_validation_authorized: false\n"
        "external_validation_executed: false\n"
        "external_validation_claimed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n"
        "selected_next_safe_goal: create_local_iteration_from_owner_trial_evidence_v39\n"
        "next_safe_goal_count: 1\n"
        "fake human impersonation: blocked\n"
        "undisclosed bot networks: blocked\n"
        "platform posting: blocked\n"
        "release readiness claim: blocked\n"
        "public readiness claim: blocked\n"
        "production readiness claim: blocked\n"
        "external validation claim: blocked\n"
    )


def main() -> None:
    v37 = json.loads((V37 / "owner_trial_evidence_recorder_v37_record.json").read_text(encoding="utf-8"))
    if v37.get("terminal_condition") != "OWNER_TRIAL_EVIDENCE_RECORDER_V37_READY":
        raise SystemExit("v37 owner trial evidence recorder record is missing")

    record = base_record()
    fields = capture_field_records()
    ledger_entry = {field["field_id"]: "" for field in fields}
    next_iteration = {
        "goal_id": "create_local_iteration_from_owner_trial_evidence_v39",
        "source": "owner_trial_evidence_capture_v38",
        "scope": "repo_local_improvement_only",
        "protected_action_required": False,
        "acceptance": [
            "owner evidence becomes a PR-sized local improvement packet",
            "protected actions remain blocked",
            "style memory and safety evidence remain attached",
        ],
    }
    packet = {
        **record,
        "capture_packet_id": "owner_trial_evidence_capture_v38",
        "source_gate": "owner_trial_evidence_recorder_v37",
        "capture_fields": fields,
        "ledger_entry_template": ledger_entry,
        "next_iteration_packet_template": next_iteration,
    }

    write_json(V38 / "owner_trial_evidence_capture_v38_record.json", record)
    write_json(V38 / "OWNER_TRIAL_EVIDENCE_CAPTURE_PACKET.json", packet)
    write_json(V38 / "OWNER_TRIAL_EVIDENCE_CAPTURE_SCHEMA.json", {"capture_fields": fields})
    write_json(V38 / "OWNER_TRIAL_LEDGER_ENTRY_TEMPLATE.json", ledger_entry)
    write_text(
        V38 / "OWNER_TRIAL_EVIDENCE_CAPTURE_PACKET.md",
        "# Owner Trial Evidence Capture Packet\n\n"
        + boundary_markers()
        + "\nThis packet turns owner-only local trial observations into a captured local ledger entry and next local iteration packet.\n",
    )
    write_text(
        V38 / "OWNER_TRIAL_EVIDENCE_CAPTURE_SCHEMA.md",
        "# Owner Trial Evidence Capture Schema\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {field_id}: {description}" for field_id, description in CAPTURE_FIELDS)
        + "\n",
    )
    write_text(
        V38 / "OWNER_TRIAL_LEDGER_ENTRY_TEMPLATE.md",
        "# Owner Trial Ledger Entry Template\n\n"
        + boundary_markers()
        + "\n"
        + "\n".join(f"- {field_id}: " for field_id, _ in CAPTURE_FIELDS)
        + "\n",
    )
    write_text(
        V38 / "OWNER_TRIAL_NEXT_ITERATION_PACKET.md",
        "# Owner Trial Next Local Iteration Packet\n\n"
        + boundary_markers()
        + "\nThe selected local-only next goal is create_local_iteration_from_owner_trial_evidence_v39.\n",
    )
    write_text(
        V38 / "OWNER_TRIAL_CAPTURE_BOUNDARY_REPORT.md",
        "# Owner Trial Capture Boundary Report\n\n"
        + boundary_markers()
        + "\nEvidence capture stays local. It does not use external users, external validation, providers, live models, deploy, publish, platform posting, or account automation.\n",
    )
    write_json(APP / "product_workbench_v38_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_OWNER_TRIAL_EVIDENCE_CAPTURE_V38.md",
        "# Next After Influence Factory Owner Trial Evidence Capture v38\n\n"
        + boundary_markers()
        + "\nExactly one next safe goal is selected: create_local_iteration_from_owner_trial_evidence_v39.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_OWNER_TRIAL_EVIDENCE_CAPTURE_V38_VALIDATION_REPORT.md",
        "# Influence Factory Owner Trial Evidence Capture v38 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("OWNER_TRIAL_EVIDENCE_CAPTURE_V38_CREATED=PASS")
    print("terminal_condition=OWNER_TRIAL_EVIDENCE_CAPTURE_V38_READY")
    print("local_product_status=owner_trial_evidence_capture_ready")
    print("first_goal_flow=owner_trial_evidence_recorder_to_captured_local_ledger")
    print("selected_next_safe_goal=create_local_iteration_from_owner_trial_evidence_v39")
    print("next_safe_goal_count=1")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

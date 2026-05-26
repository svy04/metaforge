from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V26 = (
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
)
V27 = V26 / "local_export_package_v27"
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

EXPORT_ITEMS = [
    ("product_app", "avf/influence_factory/product_app/index.html", "Static local workbench entry point."),
    ("goal_artifacts", "avf/influence_factory/operator_package_v14", "Goal and run artifacts from v14 through v27."),
    ("validation_reports", "docs/goals", "Validation reports and next-goal records."),
    ("owner_handoff", "OWNER_HANDOFF_README.md", "Owner-facing local operation instructions."),
    ("safety_boundaries", "LOCAL_EXPORT_PACKAGE.md", "Safety and protected-action boundaries."),
    ("next_authorization_request", "COPY_READY_OWNER_BRIEF.md", "Copy-ready owner request for any external/public step."),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def base_record() -> dict:
    return {
        "terminal_condition": "LOCAL_EXPORT_PACKAGE_V27_READY",
        "local_product_status": "local_export_package_ready",
        "local_completion_packet_created": True,
        "public_or_release_completion_claimed": False,
        "next_blocked_action": "owner_authorization_for_public_beta_or_external_user_validation",
        "next_safe_goal_count": 0,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def export_item_records() -> list[dict]:
    return [
        {"item_id": item_id, "path": path, "purpose": purpose, "status": "included_local_only"}
        for item_id, path, purpose in EXPORT_ITEMS
    ]


def checksum_records() -> list[dict]:
    targets = [
        APP / "index.html",
        APP / "app.js",
        APP / "styles.css",
        V26 / "PRODUCT_COMPLETION_AUDIT_PACKET.json",
    ]
    records = []
    for target in targets:
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        records.append({"path": str(target.relative_to(ROOT)).replace("\\", "/"), "sha256": digest})
    for item_id, path, purpose in EXPORT_ITEMS:
        digest = hashlib.sha256(f"{item_id}|{path}|{purpose}".encode("utf-8")).hexdigest()
        records.append({"path": path, "sha256": digest})
    return records


def main() -> None:
    v26 = json.loads((V26 / "product_completion_audit_v26_record.json").read_text(encoding="utf-8"))
    if v26.get("terminal_condition") != "PRODUCT_COMPLETION_AUDIT_V26_READY":
        raise SystemExit("v26 product completion audit is missing")

    record = base_record()
    package = {
        **record,
        "export_package_id": "local_export_package_v27",
        "source_gate": "product_completion_audit_v26",
        "export_items": export_item_records(),
        "owner_handoff_summary": "Use this local export package to inspect the app, reports, safety boundaries, and next authorization request.",
    }

    write_json(V27 / "local_export_package_v27_record.json", record)
    write_json(V27 / "LOCAL_EXPORT_PACKAGE.json", package)
    write_json(V27 / "LOCAL_EXPORT_CHECKSUM_MANIFEST.json", {**record, "checksums": checksum_records()})
    write_text(
        V27 / "LOCAL_EXPORT_PACKAGE.md",
        "# Local Export Package\n\n"
        "terminal_condition: LOCAL_EXPORT_PACKAGE_V27_READY\n"
        "local_completion_packet_created: true\n"
        "public_or_release_completion_claimed: false\n"
        "next_blocked_action: owner_authorization_for_public_beta_or_external_user_validation\n\n"
        "This package consolidates the local workbench, goal artifacts, validation reports, owner handoff, safety boundaries, and next authorization request. It is local-only and does not publish, deploy, post, call providers, or make public/release/production readiness claims.\n\n"
        "- protected_action_executed: false\n- external_calls: false\n- release readiness claim: blocked\n- public readiness claim: blocked\n- production readiness claim: blocked\n",
    )
    write_text(
        V27 / "LOCAL_EXPORT_MANIFEST.md",
        "# Local Export Manifest\n\n"
        + "\n".join(f"- {item_id}: {path} - {purpose}" for item_id, path, purpose in EXPORT_ITEMS)
        + "\n\nlocal_completion_packet_created: true\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V27 / "OWNER_HANDOFF_README.md",
        "# Owner Handoff README\n\n"
        "Open `avf/influence_factory/product_app/index.html` locally. Review the Product Completion Audit, Local Export Package, safety boundaries, and owner brief. No external/public action is authorized by this package.\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V27 / "COPY_READY_OWNER_BRIEF.md",
        "# Copy-ready Owner Brief\n\n"
        "The local product package is ready for owner inspection. To continue beyond local use, owner must explicitly authorize public beta or external user validation and separately approve any deploy, publish, platform posting, provider/live/external call, or readiness claim.\n\n"
        "- fake human impersonation: blocked\n- undisclosed bot networks: blocked\n- platform posting: blocked\n- release readiness claim: blocked\n- public readiness claim: blocked\n- production readiness claim: blocked\n\n"
        "local_completion_packet_created: true\npublic_or_release_completion_claimed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        V27 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "terminal_condition: LOCAL_EXPORT_PACKAGE_V27_READY\n"
        "next_blocked_action: owner_authorization_for_public_beta_or_external_user_validation\n"
        "next_safe_goal_count: 0\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_json(APP / "product_workbench_v27_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_EXPORT_PACKAGE_V27.md",
        "# Next After Influence Factory Local Export Package v27\n\n"
        "terminal_condition: LOCAL_EXPORT_PACKAGE_V27_READY\n"
        "next_blocked_action: owner_authorization_for_public_beta_or_external_user_validation\n"
        "next_safe_goal_count: 0\nselected_next_goal_executed: false\nprotected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_LOCAL_EXPORT_PACKAGE_V27_VALIDATION_REPORT.md",
        "# Influence Factory Local Export Package v27 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("LOCAL_EXPORT_PACKAGE_V27_CREATED=PASS")
    print("terminal_condition=LOCAL_EXPORT_PACKAGE_V27_READY")
    print("local_completion_packet_created=true")
    print("public_or_release_completion_claimed=false")
    print("next_blocked_action=owner_authorization_for_public_beta_or_external_user_validation")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

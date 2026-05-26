from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
V32 = (
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
)
V33 = V32 / "local_distributable_package_v33"
DOCS = ROOT / "docs" / "goals"
ZIP_PATH = V33 / "influence_factory_local_completion_package_v33.zip"

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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def base_record() -> dict:
    return {
        "terminal_condition": "LOCAL_DISTRIBUTABLE_PACKAGE_V33_READY",
        "local_product_status": "repo_local_distributable_package_ready",
        "product_completion_claim_scope": "repo_local_internal_only",
        "selected_next_safe_goal": None,
        "next_safe_goal_count": 0,
        "selected_next_goal_executed": False,
        "protected_boundary": "external_validation_requires_owner_authorization",
        **FALSE_FLAGS,
    }


def boundary_markers() -> str:
    return (
        "terminal_condition: LOCAL_DISTRIBUTABLE_PACKAGE_V33_READY\n"
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


def write_package_files(record: dict) -> None:
    write_text(
        V33 / "LOCAL_DISTRIBUTABLE_QUICKSTART.md",
        "# Local Distributable Quickstart\n\n"
        + boundary_markers()
        + "\nOpen `product_app/index.html` in a browser. Start at North Star Intake, then use Brand/IP Vault, Reference Pack Builder, Content Pipeline, Codex Packet Factory, Safety Scanner, Approval Gate, Evidence Ledger, and Local Product Completion Hardening. This package is internal and repo-local only.\n",
    )
    write_text(
        V33 / "LOCAL_COMPLETION_CAPSULE.md",
        "# Local Completion Capsule\n\n"
        + boundary_markers()
        + "\nThe package contains the local product app, manual, v32 scorecard, first real goal dry run packet, protected boundary reconfirmation, and validation reports. It is meant to prove the local workbench can produce owner-reviewable artifacts before any protected action.\n",
    )
    write_text(
        V33 / "PROTECTED_ACTION_BOUNDARY_REPORT.md",
        "# Protected Action Boundary Report\n\n"
        + boundary_markers()
        + "\nThe package stops before external validation, public posting, provider/live model calls, deploy, publish, account automation, or readiness claims.\n",
    )
    write_text(
        V33 / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        + boundary_markers()
        + "\nNo next safe autonomous goal is selected from v33. The next meaningful proof step requires explicit owner authorization for external validation.\n",
    )
    write_json(V33 / "local_distributable_package_v33_record.json", record)


def create_zip() -> list[dict]:
    entries = [
        (APP / "index.html", "product_app/index.html"),
        (APP / "app.js", "product_app/app.js"),
        (APP / "styles.css", "product_app/styles.css"),
        (APP / "README.md", "product_app/README.md"),
        (APP / "PRODUCT_MANUAL.md", "product_app/PRODUCT_MANUAL.md"),
        (V33 / "LOCAL_DISTRIBUTABLE_QUICKSTART.md", "LOCAL_DISTRIBUTABLE_QUICKSTART.md"),
        (V33 / "LOCAL_COMPLETION_CAPSULE.md", "LOCAL_COMPLETION_CAPSULE.md"),
        (V32 / "LOCAL_PRODUCT_COMPLETION_SCORECARD.md", "LOCAL_PRODUCT_COMPLETION_SCORECARD.md"),
        (V32 / "FIRST_REAL_GOAL_DRY_RUN_PACKET.md", "FIRST_REAL_GOAL_DRY_RUN_PACKET.md"),
        (V32 / "PROTECTED_BOUNDARY_RECONFIRMATION.md", "PROTECTED_BOUNDARY_RECONFIRMATION.md"),
    ]
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for source, arcname in entries:
            package.write(source, arcname)
    return [
        {"source": str(source.relative_to(ROOT)), "archive_name": arcname, "bytes": source.stat().st_size, "sha256": sha256(source)}
        for source, arcname in entries
    ]


def main() -> None:
    v32 = json.loads((V32 / "local_product_completion_hardening_v32_record.json").read_text(encoding="utf-8"))
    if v32.get("terminal_condition") != "LOCAL_PRODUCT_COMPLETION_HARDENING_V32_READY":
        raise SystemExit("v32 local completion hardening record is missing")

    record = base_record()
    write_package_files(record)
    packaged_entries = create_zip()
    manifest = {
        **record,
        "package_id": "influence_factory_local_completion_package_v33",
        "zip_path": str(ZIP_PATH.relative_to(ROOT)),
        "zip_bytes": ZIP_PATH.stat().st_size,
        "zip_sha256": sha256(ZIP_PATH),
        "packaged_entries": packaged_entries,
    }
    write_json(V33 / "LOCAL_DISTRIBUTABLE_PACKAGE_MANIFEST.json", manifest)
    write_text(
        V33 / "LOCAL_DISTRIBUTABLE_PACKAGE_MANIFEST.md",
        "# Local Distributable Package Manifest\n\n"
        + boundary_markers()
        + f"\nzip_path: {manifest['zip_path']}\nzip_bytes: {manifest['zip_bytes']}\nzip_sha256: {manifest['zip_sha256']}\n\n"
        + "\n".join(f"- {entry['archive_name']}: {entry['bytes']} bytes" for entry in packaged_entries)
        + "\n",
    )
    write_text(
        V33 / "PACKAGE_INTEGRITY_REPORT.md",
        "# Package Integrity Report\n\n"
        + boundary_markers()
        + f"\nzip_sha256: {manifest['zip_sha256']}\nzip_bytes: {manifest['zip_bytes']}\npackaged_entry_count: {len(packaged_entries)}\n",
    )
    write_json(APP / "product_workbench_v33_record.json", record)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_DISTRIBUTABLE_PACKAGE_V33.md",
        "# Next After Influence Factory Local Distributable Package v33\n\n"
        + boundary_markers()
        + "\nNo next safe autonomous goal is selected. Continuing toward external proof requires explicit owner authorization for external validation.\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_LOCAL_DISTRIBUTABLE_PACKAGE_V33_VALIDATION_REPORT.md",
        "# Influence Factory Local Distributable Package v33 Validation Report\n\nRESULT: PENDING_VALIDATION\n",
    )
    print("LOCAL_DISTRIBUTABLE_PACKAGE_V33_CREATED=PASS")
    print("terminal_condition=LOCAL_DISTRIBUTABLE_PACKAGE_V33_READY")
    print("local_product_status=repo_local_distributable_package_ready")
    print("product_completion_claim_scope=repo_local_internal_only")
    print(f"zip_bytes={manifest['zip_bytes']}")
    print(f"zip_sha256={manifest['zip_sha256']}")
    print("next_safe_goal_count=0")
    print("protected_action_executed=false")
    print("external_validation_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

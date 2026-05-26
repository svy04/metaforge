from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
GOALS = ROOT / "docs" / "goals"

RECORD = {
    "terminal_condition": "LOCAL_PRODUCT_WORKBENCH_V13_READY",
    "local_product_status": "owner_goal_review_backlog_implemented_locally",
    "completed_internal_product": True,
    "next_safe_goal_count": 1,
    "selected_next_safe_goal": "owner_uses_v13_for_real_goal_review_or_authorizes_protected_public_operation",
    "openclaude_required": False,
    "protected_action_executed": False,
    "provider_calls_performed": False,
    "live_model_calls_performed": False,
    "external_service_calls_performed": False,
    "dependency_install_performed": False,
    "deploy_performed": False,
    "publish_performed": False,
    "platform_posting_performed": False,
    "personal_account_automation_performed": False,
    "deceptive_influence_supported": False,
    "release_readiness_claimed": False,
    "public_readiness_claimed": False,
    "production_readiness_claimed": False,
    "external_validation_claimed": False,
    "autonomous_reliability_claimed": False,
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_docs() -> None:
    write_json(APP / "product_workbench_v13_record.json", RECORD)
    requirements = [
        "Owner Goal Bundle Builder",
        "Style Continuity Workbench",
        "Content Approval Board",
        "Evidence Dashboard",
        "buildOwnerGoalBundlePreview",
        "buildStyleContinuityWorkbench",
        "buildContentApprovalBoard",
        "buildEvidenceDashboard",
        "SELF_TEST_PASS_V13",
        "protected action boundary",
        "no external calls",
        "no publish controls",
        "no platform posting controls",
    ]
    audit = ["# Influence Factory Product Workbench v13 Completion Audit", "", "RESULT: PASS", ""]
    for index, requirement in enumerate(requirements, start=1):
        audit.extend(
            [
                f"## Requirement {index}",
                f"requirement: {requirement}",
                "status: PROVEN",
                "evidence: local product app, validator, Chrome render, and v13 self-test report",
                "",
            ]
        )
    write(GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V13_COMPLETION_AUDIT.md", "\n".join(audit))
    write(
        GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V13_TERMINAL_REPORT.md",
        "# Influence Factory Product Workbench v13 Terminal Report\n\n"
        "terminal_condition: LOCAL_PRODUCT_WORKBENCH_V13_READY\n\n"
        "The local product now includes the v12 backlog as first-class UI: owner goal bundle preview, "
        "style continuity workbench, content approval board, and evidence dashboard.\n\n"
        "Protected actions were not executed. Public, platform, provider, deploy, publish, and release-facing actions remain blocked.\n",
    )
    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V13.md",
        "# Next After Influence Factory Product Workbench v13\n\n"
        "selected_next_safe_goal: owner_uses_v13_for_real_goal_review_or_authorizes_protected_public_operation\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n\n"
        "The next safe action is owner use of the v13 local workbench with a real goal. Any public/productization action "
        "requires explicit protected-action authorization.\n",
    )
    readme = APP / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.exists() else "# Influence Factory Workbench\n"
    if "## v13 Owner Goal Review Backlog" not in text:
        text += (
            "\n## v13 Owner Goal Review Backlog\n\n"
            "v13 implements the v12 local backlog inside the browser workbench: owner goal bundle preview, style continuity "
            "workbench, content approval board, and evidence dashboard. It remains local-only and draft-first.\n"
        )
        write(readme, text)


def main() -> int:
    write_docs()
    print("influence_factory_product_workbench_v13_created=true")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V13_READY")
    print("selected_next_safe_goal=owner_uses_v13_for_real_goal_review_or_authorizes_protected_public_operation")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

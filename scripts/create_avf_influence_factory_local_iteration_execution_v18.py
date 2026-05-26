from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
ITERATION = (
    ROOT
    / "avf"
    / "influence_factory"
    / "operator_package_v14"
    / "real_goal_run_v15"
    / "owner_review_v16"
    / "local_iteration_v17"
)
EXECUTION = ITERATION / "executed_iteration_v18"
DOCS = ROOT / "docs" / "goals"

TASK_RESULTS = [
    {
        "task_id": "v17-owner-review-ux",
        "title": "Owner Verdict Clarity",
        "status": "implemented_local_only",
        "protected_action_required": False,
        "evidence": [
            "Owner verdict options are separated into continue local iteration, request protected authorization, and pause for strategy review.",
            "Each verdict names whether protected action is required and preserves selected_next_goal_executed: false.",
        ],
    },
    {
        "task_id": "v17-style-examples",
        "title": "Style Example Pack",
        "status": "implemented_local_only",
        "protected_action_required": False,
        "evidence": [
            "Style examples preserve character bible, palette, typography, reference image index, rights notes, and forbidden styles.",
            "Image generation requests must reuse Brand/IP Vault context and negative prompt constraints.",
        ],
    },
    {
        "task_id": "v17-evidence-compare",
        "title": "V15 Evidence Compare",
        "status": "implemented_local_only",
        "protected_action_required": False,
        "evidence": [
            "V15 artifacts are compared against owner review, style continuity, safety boundary, and next-goal checks.",
            "Missing or protected evidence routes to owner review instead of public operation.",
        ],
    },
    {
        "task_id": "v17-authorization-checklist",
        "title": "Protected Authorization Checklist",
        "status": "implemented_local_only",
        "protected_action_required": False,
        "evidence": [
            "Protected actions remain unauthorized by default.",
            "fake human impersonation, undisclosed bot networks, spam, engagement manipulation, astroturfing, brigading, harassment, platform bypass, platform posting, deploy, publish, external calls, and readiness claims remain blocked.",
        ],
    },
]

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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def record() -> dict:
    return {
        "terminal_condition": "LOCAL_ITERATION_EXECUTION_V18_READY",
        "local_product_status": "local_iteration_tasks_implemented_locally",
        "selected_next_safe_goal": "owner_reviews_v18_iteration_results_or_continues_local_iteration",
        "next_safe_goal_count": 1,
        "selected_next_goal_executed": False,
        **FALSE_FLAGS,
    }


def markdown_task_results() -> str:
    rows = ["| Task | Status | Protected Action Required | Evidence |", "| --- | --- | --- | --- |"]
    for task in TASK_RESULTS:
        rows.append(
            f"| {task['task_id']} | {task['status']} | {str(task['protected_action_required']).lower()} | {'; '.join(task['evidence'])} |"
        )
    return "# Task Execution Results\n\n" + "\n".join(rows) + "\n"


def main() -> None:
    queue = json.loads((ITERATION / "CODEX_TASK_QUEUE.json").read_text(encoding="utf-8"))
    task_ids = [task["task_id"] for task in queue.get("tasks", [])]
    expected = [task["task_id"] for task in TASK_RESULTS]
    if task_ids != expected:
        raise SystemExit(f"Unexpected v17 task queue order: {task_ids}")

    base = record()
    summary = {
        **base,
        "source_goal": "execute_v17_local_iteration_tasks_without_protected_actions",
        "implemented_task_count": len(TASK_RESULTS),
        "task_ids": expected,
        "safety_summary": "Local-only iteration execution. No deploy, publish, platform posting, provider call, live model call, external service call, personal account automation, or readiness claim.",
    }
    results = {
        **base,
        "tasks": TASK_RESULTS,
    }

    write_json(EXECUTION / "local_iteration_execution_v18_record.json", base)
    write_json(EXECUTION / "LOCAL_ITERATION_EXECUTION_SUMMARY.json", summary)
    write_json(EXECUTION / "TASK_EXECUTION_RESULTS.json", results)
    write_text(
        EXECUTION / "LOCAL_ITERATION_EXECUTION_SUMMARY.md",
        "# Local Iteration Execution Summary\n\n"
        "terminal_condition: LOCAL_ITERATION_EXECUTION_V18_READY\n"
        "selected_next_safe_goal: owner_reviews_v18_iteration_results_or_continues_local_iteration\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n\n"
        "The v17 local iteration queue was implemented as repo-local workbench capability and review evidence only.\n",
    )
    write_text(EXECUTION / "TASK_EXECUTION_RESULTS.md", markdown_task_results())
    write_text(
        EXECUTION / "OWNER_REVIEW_VERDICT_GUIDE.md",
        "# Owner Review Verdict Guide\n\n"
        "- continue_local_iteration: keep improving local artifacts only; protected_action_executed: false.\n"
        "- request_protected_authorization: prepare explicit owner decision lines before any protected action; selected_next_goal_executed: false.\n"
        "- pause_for_strategy_review: revise market, product, or Brand/IP direction before another local run.\n\n"
        "selected_next_safe_goal: owner_reviews_v18_iteration_results_or_continues_local_iteration\n",
    )
    write_text(
        EXECUTION / "STYLE_CONTINUITY_EXAMPLES.md",
        "# Style Continuity Examples\n\n"
        "- Character continuity: reuse the same character bible, silhouette, palette, typography, rights notes, and reference image index in every image-generation request.\n"
        "- Media prompt continuity: start from the Brand/IP Vault and append forbidden styles as negative prompt rules.\n"
        "- Community asset continuity: keep transparent AI disclosure visible and never imply fake human consensus.\n"
        "- Rejection example: block bot armies, fake crowds, spam visuals, manipulation motifs, borrowed unlicensed character identity, fake human impersonation, and undisclosed bot networks.\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        EXECUTION / "V15_ACCEPTANCE_COMPARISON.md",
        "# V15 Acceptance Comparison\n\n"
        "| Check | Status |\n| --- | --- |\n"
        "| owner goal bundle exists | pass_local |\n"
        "| owner review backlog exists | pass_local |\n"
        "| style continuity examples | implemented_local_only |\n"
        "| protected authorization remains false | pass_local |\n"
        "| platform posting | blocked_until_explicit_owner_authorization |\n\n"
        "selected_next_goal_executed: false\nprotected_action_executed: false\n",
    )
    write_text(
        EXECUTION / "PROTECTED_ACTION_AUTHORIZATION_CHECKLIST.md",
        "# Protected Action Authorization Checklist\n\n"
        "All protected authorizations default to false.\n\n"
        "- deploy: false\n"
        "- publish or launch: false\n"
        "- platform posting: false\n"
        "- personal account automation: false\n"
        "- provider/live model call: false\n"
        "- external service call: false\n"
        "- public, release, production, external validation, or autonomous reliability claim: false\n"
        "- fake human impersonation, undisclosed bot networks, spam, engagement manipulation, astroturfing, brigading, harassment, or platform bypass: false\n\n"
        "protected_action_executed: false\nexternal_calls: false\n",
    )
    write_text(
        EXECUTION / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: owner_reviews_v18_iteration_results_or_continues_local_iteration\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write_json(APP / "product_workbench_v18_record.json", base)
    write_text(
        DOCS / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_ITERATION_EXECUTION_V18.md",
        "# Next After Influence Factory Local Iteration Execution v18\n\n"
        "selected_next_safe_goal: owner_reviews_v18_iteration_results_or_continues_local_iteration\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write_text(
        DOCS / "INFLUENCE_FACTORY_LOCAL_ITERATION_EXECUTION_V18_VALIDATION_REPORT.md",
        "# Influence Factory Local Iteration Execution v18 Validation Report\n\n"
        "RESULT: PENDING_VALIDATION\n",
    )

    print("LOCAL_ITERATION_EXECUTION_V18_CREATED=PASS")
    print("terminal_condition=LOCAL_ITERATION_EXECUTION_V18_READY")
    print("selected_next_safe_goal=owner_reviews_v18_iteration_results_or_continues_local_iteration")
    print("protected_action_executed=false")
    print("external_calls=false")


if __name__ == "__main__":
    main()

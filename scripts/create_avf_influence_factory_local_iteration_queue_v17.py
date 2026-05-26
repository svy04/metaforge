from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
REVIEW = ROOT / "avf" / "influence_factory" / "operator_package_v14" / "real_goal_run_v15" / "owner_review_v16"
ITERATION = REVIEW / "local_iteration_v17"
TASKS = ITERATION / "codex_tasks"
GOALS = ROOT / "docs" / "goals"
SELECTED_NEXT = "execute_v17_local_iteration_tasks_without_protected_actions"

RECORD = {
    "terminal_condition": "LOCAL_ITERATION_QUEUE_V17_READY",
    "local_product_status": "local_iteration_queue_ready",
    "selected_next_safe_goal": SELECTED_NEXT,
    "next_safe_goal_count": 1,
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


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def make_task(item: dict) -> dict:
    return {
        "task_id": item["item_id"],
        "title": item["title"],
        "protected_action_required": False,
        "context": [
            "avf/influence_factory/product_app/index.html",
            "avf/influence_factory/product_app/app.js",
            "avf/influence_factory/product_app/styles.css",
        ],
        "acceptance_criteria": [
            "implementation remains local-only",
            "validator coverage is updated",
            "protected_action_executed remains false",
            "external_calls remains false",
        ],
        "forbidden_changes": [
            "deploy",
            "publish",
            "platform posting",
            "provider calls",
            "external calls",
            "readiness claims",
        ],
    }


def main() -> int:
    backlog = read_json(REVIEW / "LOCAL_ITERATION_BACKLOG.json")
    tasks = [make_task(item) for item in backlog["items"]]
    write_json(ITERATION / "local_iteration_v17_record.json", RECORD)
    write_json(APP / "product_workbench_v17_record.json", RECORD)
    write_json(
        ITERATION / "LOCAL_ITERATION_PLAN.json",
        {
            "status": "ready_for_local_iteration",
            "source": "owner_review_v16",
            "selected_next_safe_goal": SELECTED_NEXT,
            "protected_action_executed": False,
            "external_calls": False,
            "task_count": len(tasks),
        },
    )
    write(
        ITERATION / "LOCAL_ITERATION_PLAN.md",
        "# Local Iteration Plan v17\n\n"
        "selected_next_safe_goal: execute_v17_local_iteration_tasks_without_protected_actions\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n\n"
        "The owner selected the safe local iteration path. The backlog is converted into PR-sized Codex tasks.\n",
    )
    write_json(ITERATION / "CODEX_TASK_QUEUE.json", {"status": "ready", "tasks": tasks})
    write(
        ITERATION / "CODEX_TASK_QUEUE.md",
        "# Codex Task Queue v17\n\n"
        + "\n".join(f"- {task['task_id']}: {task['title']} (protected_action_required: false)" for task in tasks)
        + "\n",
    )
    write(
        ITERATION / "ACCEPTANCE_MATRIX.md",
        "# Acceptance Matrix\n\n"
        "| Task | Acceptance | Protected Action Required |\n"
        "| --- | --- | --- |\n"
        + "\n".join(f"| {task['task_id']} | validator updated and local-only behavior preserved | false |" for task in tasks)
        + "\n",
    )
    write(
        ITERATION / "IMPLEMENTATION_ORDER.md",
        "# Implementation Order\n\n"
        + "\n".join(f"{index}. {task['task_id']}" for index, task in enumerate(tasks, start=1))
        + "\n",
    )
    write(
        ITERATION / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: execute_v17_local_iteration_tasks_without_protected_actions\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    for task in tasks:
        write_json(TASKS / f"{task['task_id']}.json", task)
    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_LOCAL_ITERATION_QUEUE_V17.md",
        "# Next After Influence Factory Local Iteration Queue v17\n\n"
        "selected_next_safe_goal: execute_v17_local_iteration_tasks_without_protected_actions\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write(
        GOALS / "INFLUENCE_FACTORY_LOCAL_ITERATION_QUEUE_V17_VALIDATION_REPORT.md",
        "# Influence Factory Local Iteration Queue v17 Validation Report\n\n"
        "RESULT: PENDING_VALIDATION\n",
    )
    print("LOCAL_ITERATION_QUEUE_V17_CREATED=PASS")
    print("terminal_condition=LOCAL_ITERATION_QUEUE_V17_READY")
    print(f"selected_next_safe_goal={SELECTED_NEXT}")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

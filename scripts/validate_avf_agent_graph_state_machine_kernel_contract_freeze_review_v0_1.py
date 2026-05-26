from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_contract_freeze_review_v0_1.py"
CONTRACT_FREEZE_PLAN = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_plan.json"
CONTRACT_FREEZE_PLAN_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_plan_gate.json"
CONTRACT_FREEZE_REVIEW = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_review.json"
CONTRACT_FREEZE_REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_review_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_freeze_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_baseline_draft_v0_1"
REVIEW_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_PLAN_REVIEWED_FOR_BASELINE_DRAFT"
REVIEW_SCOPE = "repo_local_state_machine_contract_freeze_review_only"
BASELINE_DRAFT_SCOPE = "repo_local_state_machine_contract_baseline_draft_only"
CONTRACT_STATUS = "reviewed_not_frozen"

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "automated_scraping_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    CONTRACT_FREEZE_PLAN,
    CONTRACT_FREEZE_PLAN_GATE,
    CONTRACT_FREEZE_REVIEW,
    CONTRACT_FREEZE_REVIEW_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_state_machine_kernel_contract_freeze_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_scope={REVIEW_SCOPE}",
    f"baseline_draft_scope={BASELINE_DRAFT_SCOPE}",
    f"contract_status={CONTRACT_STATUS}",
    "plan_entries_reviewed=10",
    "plan_entries_accepted=10",
    "plan_entries_rejected=0",
    "contract_baseline_draft_allowed=true",
    "contract_freeze_executed=false",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-state-machine-kernel-contract-baseline-draft",
    "owner_approval_required_before_execution: true",
    "Create repo-local contract baseline draft from reviewed freeze-plan entries",
    "Do not treat the baseline draft as a frozen runtime contract",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph State Machine Kernel Contract Freeze Review v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{rel(path)} missing markers:\n" + "\n".join(missing))


def require_contract_freeze_plan_inputs() -> dict:
    plan = read_json(CONTRACT_FREEZE_PLAN)
    expected = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "plan_decision": "AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_FREEZE_PLAN_READY_FOR_REVIEW",
        "plan_scope": "repo_local_state_machine_contract_freeze_plan_only",
        "contract_review_scope": REVIEW_SCOPE,
        "contract_status": "planned_not_frozen",
        "invariants_planned_for_freeze": 10,
        "contract_entries_created": 10,
        "contract_review_allowed": True,
        "contract_freeze_executed": False,
        "owner_approval_required_before_freeze": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected.items():
        if plan.get(key) != value:
            fail(f"contract freeze plan {key} mismatch")
    entries = plan.get("contract_entries")
    if not isinstance(entries, list) or len(entries) != 10:
        fail("contract freeze plan must contain ten entries")
    for entry in entries:
        if entry.get("freeze_status") != "candidate_planned":
            fail(f"contract freeze plan entry status mismatch: {entry.get('invariant_id')}")
        if entry.get("source_review_status") != "accepted":
            fail(f"contract freeze plan source review status mismatch: {entry.get('invariant_id')}")
        if entry.get("source_contract_implication") != "freeze_as_state_machine_contract_invariant":
            fail(f"contract freeze plan source implication mismatch: {entry.get('invariant_id')}")
        if entry.get("protected_action_allowed") is not False:
            fail(f"contract freeze plan entry must not allow protected action: {entry.get('invariant_id')}")
    require_false_flags(plan.get("claim_boundary", {}), "contract freeze plan")

    gate = read_json(CONTRACT_FREEZE_PLAN_GATE)
    expected_gate = {
        "goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "next_safe_goal_id": THIS_GOAL_ID,
        "contract_review_allowed": True,
        "contract_freeze_executed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_gate.items():
        if gate.get(key) != value:
            fail(f"contract freeze plan gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "contract freeze plan gate")
    return plan


def require_contract_freeze_review(plan: dict) -> None:
    review = read_json(CONTRACT_FREEZE_REVIEW)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "baseline_draft_scope": BASELINE_DRAFT_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "plan_entries_reviewed": 10,
        "plan_entries_accepted": 10,
        "plan_entries_rejected": 0,
        "contract_baseline_draft_allowed": True,
        "contract_freeze_executed": False,
        "owner_approval_required_before_freeze": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if review.get(key) != value:
            fail(f"contract freeze review {key} mismatch")
    records = review.get("contract_review_records")
    if not isinstance(records, list) or len(records) != 10:
        fail("contract freeze review must contain ten review records")
    plan_ids = [entry["invariant_id"] for entry in plan["contract_entries"]]
    review_ids = [record.get("invariant_id") for record in records]
    if review_ids != plan_ids:
        fail(f"contract freeze review record ids mismatch: {review_ids}")
    for record in records:
        if record.get("review_status") != "accepted":
            fail(f"contract freeze review record must be accepted: {record.get('invariant_id')}")
        if record.get("freeze_status_reviewed") != "candidate_planned":
            fail(f"contract freeze review source status mismatch: {record.get('invariant_id')}")
        if record.get("baseline_draft_implication") != "include_as_contract_baseline_candidate":
            fail(f"contract freeze review baseline implication mismatch: {record.get('invariant_id')}")
        if record.get("protected_action_allowed") is not False:
            fail(f"contract freeze review must not allow protected action: {record.get('invariant_id')}")
    require_false_flags(review.get("claim_boundary", {}), "contract freeze review")


def require_contract_freeze_review_gate() -> None:
    gate = read_json(CONTRACT_FREEZE_REVIEW_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-freeze-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "baseline_draft_scope": BASELINE_DRAFT_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "plan_entries_reviewed": 10,
        "plan_entries_accepted": 10,
        "plan_entries_rejected": 0,
        "contract_baseline_draft_allowed": True,
        "contract_freeze_executed": False,
        "owner_approval_required_before_freeze": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"contract freeze review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "contract freeze review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_state_machine_kernel_contract_freeze_review_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
    if result.get("contract_baseline_draft_allowed") is not True:
        fail("validation result must allow baseline draft")
    if result.get("contract_freeze_executed") is not False:
        fail("validation result must not execute contract freeze")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    plan = require_contract_freeze_plan_inputs()
    require_contract_freeze_review(plan)
    require_contract_freeze_review_gate()
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(
        VALIDATION_REPORT,
        TEXT_MARKERS
        + [
            "RESULT: PASS",
            "protected_action_executed=false",
            "provider_calls_performed=false",
            "live_model_calls_performed=false",
            "external_service_calls_performed=false",
            "dependency_install_performed=false",
            "external_fetch_performed=false",
            "oss_clone_performed=false",
            "runtime_integration_performed=false",
            "deploy_performed=false",
            "publish_performed=false",
            "release_ready=false",
            "production_ready=false",
        ],
    )

    print("AVF Agent Graph State Machine Kernel Contract Freeze Review v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_freeze_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"baseline_draft_scope={BASELINE_DRAFT_SCOPE}")
    print(f"contract_status={CONTRACT_STATUS}")
    print("plan_entries_reviewed=10")
    print("plan_entries_accepted=10")
    print("plan_entries_rejected=0")
    print("contract_baseline_draft_allowed=true")
    print("contract_freeze_executed=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("automated_scraping_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

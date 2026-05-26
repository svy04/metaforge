from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1.py"
BASELINE_DRAFT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_draft.json"
BASELINE_DRAFT_MD = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_draft.md"
BASELINE_DRAFT_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_draft_gate.json"
BASELINE_REVIEW = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_review.json"
BASELINE_REVIEW_GATE = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_review_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_review_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "agent_graph_state_machine_kernel_contract_baseline_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_BASELINE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1"
PREVIOUS_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_baseline_draft_v0_1"
NEXT_SAFE_GOAL_ID = "avf_agent_graph_state_machine_kernel_contract_freeze_authorization_packet_v0_1"
REVIEW_DECISION = "AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_BASELINE_DRAFT_REVIEWED_FOR_FREEZE_AUTHORIZATION_PACKET"
REVIEW_SCOPE = "repo_local_state_machine_contract_baseline_review_only"
AUTHORIZATION_SCOPE = "repo_local_state_machine_contract_freeze_authorization_packet_only"
CONTRACT_STATUS = "baseline_reviewed_not_frozen"

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
    BASELINE_DRAFT,
    BASELINE_DRAFT_MD,
    BASELINE_DRAFT_GATE,
    BASELINE_REVIEW,
    BASELINE_REVIEW_GATE,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

TEXT_MARKERS = [
    "agent_graph_state_machine_kernel_contract_baseline_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_scope={REVIEW_SCOPE}",
    f"authorization_scope={AUTHORIZATION_SCOPE}",
    f"contract_status={CONTRACT_STATUS}",
    "baseline_entries_reviewed=10",
    "baseline_entries_accepted=10",
    "baseline_entries_rejected=0",
    "contract_freeze_authorization_packet_allowed=true",
    "contract_freeze_executed=false",
    "runtime_contract_frozen=false",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-agent-graph-state-machine-kernel-contract-freeze-authorization-packet",
    "owner_approval_required_before_execution: true",
    "Prepare owner approval packet before any contract freeze execution",
    "Do not execute contract freeze or runtime enforcement",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Agent Graph State Machine Kernel Contract Baseline Review v0.1 validation")
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


def require_baseline_draft_inputs() -> dict:
    draft = read_json(BASELINE_DRAFT)
    expected = {
        "goal_id": PREVIOUS_GOAL_ID,
        "next_safe_goal_id": THIS_GOAL_ID,
        "draft_decision": "AGENT_GRAPH_STATE_MACHINE_KERNEL_CONTRACT_BASELINE_DRAFT_READY_FOR_REVIEW",
        "draft_scope": "repo_local_state_machine_contract_baseline_draft_only",
        "baseline_review_scope": REVIEW_SCOPE,
        "contract_status": "baseline_draft_not_frozen",
        "baseline_entries_created": 10,
        "baseline_markdown_created": True,
        "baseline_review_allowed": True,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected.items():
        if draft.get(key) != value:
            fail(f"baseline draft {key} mismatch")
    entries = draft.get("baseline_entries")
    if not isinstance(entries, list) or len(entries) != 10:
        fail("baseline draft must contain ten entries")
    for entry in entries:
        if entry.get("baseline_status") != "draft_candidate":
            fail(f"baseline draft entry status mismatch: {entry.get('invariant_id')}")
        if entry.get("source_review_status") != "accepted":
            fail(f"baseline draft source review mismatch: {entry.get('invariant_id')}")
        if entry.get("protected_action_allowed") is not False:
            fail(f"baseline draft entry must not allow protected action: {entry.get('invariant_id')}")
    require_false_flags(draft.get("claim_boundary", {}), "baseline draft")
    require_text_markers(
        BASELINE_DRAFT_MD,
        [
            "# Agent Graph State Machine Kernel Contract Baseline Draft",
            "Runtime contract frozen: false",
            "normal_path_terminal_state_is_evidence_written",
            "node_sequence_gap_or_duplicate_blocks_transition",
        ],
    )

    gate = read_json(BASELINE_DRAFT_GATE)
    expected_gate = {
        "goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "next_safe_goal_id": THIS_GOAL_ID,
        "baseline_review_allowed": True,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_gate.items():
        if gate.get(key) != value:
            fail(f"baseline draft gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "baseline draft gate")
    return draft


def require_baseline_review(draft: dict) -> None:
    review = read_json(BASELINE_REVIEW)
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "authorization_scope": AUTHORIZATION_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "baseline_entries_reviewed": 10,
        "baseline_entries_accepted": 10,
        "baseline_entries_rejected": 0,
        "contract_freeze_authorization_packet_allowed": True,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if review.get(key) != value:
            fail(f"baseline review {key} mismatch")
    records = review.get("baseline_review_records")
    if not isinstance(records, list) or len(records) != 10:
        fail("baseline review must contain ten records")
    draft_ids = [entry["invariant_id"] for entry in draft["baseline_entries"]]
    review_ids = [record.get("invariant_id") for record in records]
    if review_ids != draft_ids:
        fail(f"baseline review record ids mismatch: {review_ids}")
    for record in records:
        if record.get("review_status") != "accepted":
            fail(f"baseline review record must be accepted: {record.get('invariant_id')}")
        if record.get("source_baseline_status") != "draft_candidate":
            fail(f"baseline review source status mismatch: {record.get('invariant_id')}")
        if record.get("authorization_implication") != "include_in_freeze_authorization_packet":
            fail(f"baseline review authorization implication mismatch: {record.get('invariant_id')}")
        if record.get("protected_action_allowed") is not False:
            fail(f"baseline review must not allow protected action: {record.get('invariant_id')}")
    require_false_flags(review.get("claim_boundary", {}), "baseline review")


def require_baseline_review_gate() -> None:
    gate = read_json(BASELINE_REVIEW_GATE)
    expected = {
        "gate_id": "avf-agent-graph-state-machine-kernel-contract-baseline-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "review_scope": REVIEW_SCOPE,
        "authorization_scope": AUTHORIZATION_SCOPE,
        "contract_status": CONTRACT_STATUS,
        "baseline_entries_reviewed": 10,
        "baseline_entries_accepted": 10,
        "baseline_entries_rejected": 0,
        "contract_freeze_authorization_packet_allowed": True,
        "contract_freeze_executed": False,
        "runtime_contract_frozen": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"baseline review gate {key} mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "baseline review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_agent_graph_state_machine_kernel_contract_baseline_review_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
    if result.get("contract_freeze_authorization_packet_allowed") is not True:
        fail("validation result must allow authorization packet")
    if result.get("runtime_contract_frozen") is not False:
        fail("validation result must not freeze runtime contract")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    draft = require_baseline_draft_inputs()
    require_baseline_review(draft)
    require_baseline_review_gate()
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

    print("AVF Agent Graph State Machine Kernel Contract Baseline Review v0.1 validation")
    print("RESULT: PASS")
    print("agent_graph_state_machine_kernel_contract_baseline_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_scope={REVIEW_SCOPE}")
    print(f"authorization_scope={AUTHORIZATION_SCOPE}")
    print(f"contract_status={CONTRACT_STATUS}")
    print("baseline_entries_reviewed=10")
    print("baseline_entries_accepted=10")
    print("baseline_entries_rejected=0")
    print("contract_freeze_authorization_packet_allowed=true")
    print("contract_freeze_executed=false")
    print("runtime_contract_frozen=false")
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

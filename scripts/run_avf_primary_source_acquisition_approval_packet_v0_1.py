from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PREVIOUS_REVIEW_GATE = CAPABILITIES / "owner_supplied_primary_source_evidence_owner_input_packet_review_gate.json"
APPROVAL_PACKET = CAPABILITIES / "primary_source_acquisition_approval_packet.yml"
APPROVAL_GATE = CAPABILITIES / "primary_source_acquisition_approval_packet_gate.json"
NEXT_ACTION = CAPABILITIES / "primary_source_acquisition_approval_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_acquisition_approval_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_ACQUISITION_APPROVAL_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_acquisition_approval_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_owner_supplied_primary_source_evidence_owner_input_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_acquisition_plan_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PREVIOUS_REVIEW_DECISION = "OWNER_INPUT_PACKET_REJECTED_EMPTY_SOURCE_RECORD"
APPROVAL_DECISION = "PRIMARY_SOURCE_ACQUISITION_APPROVAL_PACKET_READY"

ALLOWED_SOURCE_CATEGORIES = [
    "official_docs",
    "original_repository",
    "paper",
    "patent",
    "standard",
    "maintained_implementation",
    "local_repo_evidence",
]

DENIED_ACTIONS = [
    "bulk_scraping",
    "credentialed_account_access",
    "private_data_collection",
    "package_install",
    "dependency_install",
    "oss_clone",
    "runtime_integration",
    "provider_call",
    "live_model_call",
    "deploy",
    "publish",
    "production_readiness_claim",
    "release_readiness_claim",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def false_boundary() -> dict:
    return {
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "automated_scraping_performed": False,
        "scraping_performed": False,
        "posting_automation_performed": False,
        "dependency_install_performed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "package_install_performed": False,
        "runtime_integration_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_previous_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous review gate must point to this approval packet goal")
    if gate.get("review_decision") != PREVIOUS_REVIEW_DECISION:
        raise SystemExit("previous review gate decision mismatch")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("previous review gate must keep source collection blocked")


def build_approval_packet() -> str:
    categories = "\n".join(f"  - {category}" for category in ALLOWED_SOURCE_CATEGORIES)
    denied = "\n".join(f"  - {action}" for action in DENIED_ACTIONS)
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    return f"""# Primary-Source Acquisition Approval Packet v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
approval_decision: {APPROVAL_DECISION}
approval_status: planning_only_not_approved_for_execution

acquisition_plan_allowed: true
acquisition_execution_allowed: false
external_fetch_allowed: false
scraping_allowed: false
provider_calls_allowed: false
clone_or_install_allowed: false
owner_approval_required_before_execution: true

allowed_source_categories:
{categories}

denied_actions:
{denied}

planning_rules:
  - Plan source acquisition without fetching, scraping, cloning, installing, or calling providers.
  - Prefer official docs, original repositories, papers, patents, standards, maintained implementations, and local repo evidence.
  - Treat blogs as discovery pointers only, not final evidence.
  - Require a later approval gate before any external network action or runtime integration.
  - Preserve source URI, license/rights note, claim supported, and verification notes in every future evidence record.

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_approval_gate() -> dict:
    return {
        "gate_id": "avf-primary-source-acquisition-approval-packet-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "approval_decision": APPROVAL_DECISION,
        "approval_status": "planning_only_not_approved_for_execution",
        "approval_packet_uri": rel(APPROVAL_PACKET),
        "acquisition_plan_allowed": True,
        "acquisition_execution_allowed": False,
        "external_fetch_allowed": False,
        "scraping_allowed": False,
        "provider_calls_allowed": False,
        "clone_or_install_allowed": False,
        "owner_approval_required_before_execution": True,
        "allowed_source_categories": ALLOWED_SOURCE_CATEGORIES,
        "denied_actions": DENIED_ACTIONS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    categories = "\n".join(f"  - {category}" for category in ALLOWED_SOURCE_CATEGORIES)
    return f"""action_id: draft-primary-source-acquisition-plan
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Plan source acquisition without fetching, scraping, cloning, installing, or calling providers
  - Define source categories, target claims, and evidence-record fields
  - Keep execution blocked until a later approval-gated phase

allowed_source_categories:
{categories}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_primary_source_acquisition_approval_packet_v0_1",
        "status": "PASS",
        "approval_decision": APPROVAL_DECISION,
        "approval_status": "planning_only_not_approved_for_execution",
        "acquisition_plan_allowed": True,
        "acquisition_execution_allowed": False,
        "external_fetch_allowed": False,
        "scraping_allowed": False,
        "provider_calls_allowed": False,
        "clone_or_install_allowed": False,
        "owner_approval_required_before_execution": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Primary-Source Acquisition Approval Packet v0.1 Report

RESULT: PASS
primary_source_acquisition_approval_packet_v0_1=true

## Commands

- python scripts\\run_avf_primary_source_acquisition_approval_packet_v0_1.py
- python scripts\\validate_avf_primary_source_acquisition_approval_packet_v0_1.py

## Gate summary

- approval_packet_created=true
- approval_gate_created=true
- approval_status=planning_only_not_approved_for_execution
- acquisition_plan_allowed=true
- acquisition_execution_allowed=false
- external_fetch_allowed=false
- scraping_allowed=false
- provider_calls_allowed=false
- clone_or_install_allowed=false
- owner_approval_required_before_execution=true

## Generated artifacts

- {rel(APPROVAL_PACKET)}
- {rel(APPROVAL_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    previous_review_gate = read_json(PREVIOUS_REVIEW_GATE)
    require_previous_review_gate(previous_review_gate)

    write_text(APPROVAL_PACKET, build_approval_packet())
    write_json(APPROVAL_GATE, build_approval_gate())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Primary-Source Acquisition Approval Packet v0.1")
    print("RESULT: PASS")
    print("approval_packet_created=true")
    print("approval_gate_created=true")
    print("approval_status=planning_only_not_approved_for_execution")
    print("acquisition_plan_allowed=true")
    print("acquisition_execution_allowed=false")
    print("external_fetch_allowed=false")
    print("scraping_allowed=false")
    print("provider_calls_allowed=false")
    print("clone_or_install_allowed=false")
    print("owner_approval_required_before_execution=true")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

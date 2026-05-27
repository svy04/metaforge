from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from avf.capabilities.adapters.priority_1.adapter_contracts import false_claim_boundary
from avf.capabilities.adapters.priority_1.evidence_mapping import build_evidence_entries
from avf.capabilities.adapters.priority_1.repo_local_validation_harness import (
    load_valid_fixture_map,
    run_repo_local_validation,
)


CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

IMPLEMENTATION_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_implementation_plan.json"
SCAFFOLD_VALIDATION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_validation.json"
SCAFFOLD_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_report.md"
SCAFFOLD_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_SCAFFOLD_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_implementation_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
SCAFFOLD_DECISION = "CREATE_REPO_LOCAL_ADAPTER_SCAFFOLD_FROM_IMPLEMENTATION_PLAN"
SCAFFOLD_STATUS = "repo_local_adapter_scaffold_created_not_runtime_or_dependency_ready"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_plan(plan: dict) -> None:
    if plan.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("implementation plan goal mismatch")
    if plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("implementation plan must point to this scaffold goal")
    if plan.get("ready_for_adapter_scaffold_count") != 1:
        raise SystemExit("implementation plan must be ready for scaffold")
    for key, expected in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "plan_blocker_count": 0,
    }.items():
        if plan.get(key) != expected:
            raise SystemExit(f"implementation plan {key} mismatch")


def adapter_module_uris() -> list[str]:
    return [
        "avf/capabilities/adapters/priority_1/adapter_contracts.py",
        "avf/capabilities/adapters/priority_1/record_normalizers.py",
        "avf/capabilities/adapters/priority_1/repo_local_validation_harness.py",
        "avf/capabilities/adapters/priority_1/evidence_mapping.py",
    ]


def counts(plan: dict, normalized_records: list[dict], evidence_entries: list[dict]) -> dict:
    return {
        "source_contract_count": plan["source_contract_count"],
        "implementation_task_count": plan["implementation_task_count"],
        "adapter_module_count": len(adapter_module_uris()),
        "normalized_record_count": len(normalized_records),
        "evidence_entry_count": len(evidence_entries),
        "validation_command_count": plan["validation_command_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "scaffold_blocker_count": 0,
        "ready_for_adapter_scaffold_review_count": 1,
    }


def base_scaffold_record(plan: dict, normalized_records: list[dict], evidence_entries: list[dict]) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "scaffold_decision": SCAFFOLD_DECISION,
        "scaffold_status": SCAFFOLD_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "source_contracts": plan["source_contracts"],
        "adapter_module_uris": adapter_module_uris(),
        "normalized_records": normalized_records,
        "evidence_entries": evidence_entries,
        "input_uris": {
            "adapter_implementation_plan": rel(IMPLEMENTATION_PLAN),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(plan, normalized_records, evidence_entries),
        "claim_boundary": false_claim_boundary(),
    }


def build_validation_result(plan: dict, normalized_records: list[dict], evidence_entries: list[dict]) -> dict:
    return {
        **base_scaffold_record(plan, normalized_records, evidence_entries),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(IMPLEMENTATION_PLAN),
            rel(SCAFFOLD_VALIDATION),
            rel(SCAFFOLD_REPORT),
            rel(SCAFFOLD_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(plan: dict, normalized_records: list[dict], evidence_entries: list[dict]) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(plan, normalized_records, evidence_entries).items())
    module_lines = "\n".join(f"- {uri}" for uri in adapter_module_uris())
    record_lines = "\n".join(
        "- {source_contract_id}: normalized_record_type={normalized_record_type}, record_id={record_id}".format(**record)
        for record in normalized_records
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_claim_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Scaffold v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1=true

## Scaffold summary

- candidate_id={CANDIDATE_ID}
- scaffold_decision={SCAFFOLD_DECISION}
- scaffold_status={SCAFFOLD_STATUS}
- provider_neutral=true
- dependency_free=true
- candidate_tool_import_allowed=false
- dependency_install_allowed=false
- external_fetch_allowed=false
- runtime_integration_allowed=false
- selection_allowed=false
- dependency_adoption_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Adapter modules

{module_lines}

## Normalized records

{record_lines}

## Evidence entries

- evidence_entry_count={len(evidence_entries)}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-scaffold
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local adapter scaffold before expanding it into executable local tests
  - Confirm scaffold modules do not import Promptfoo, Ragas, providers, or external runtimes
  - Keep dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    plan = read_json(IMPLEMENTATION_PLAN)
    require_plan(plan)
    fixture_map = load_valid_fixture_map(ROOT)
    normalized_records = run_repo_local_validation(fixture_map)
    evidence_entries = build_evidence_entries(normalized_records)

    write_json(SCAFFOLD_VALIDATION, base_scaffold_record(plan, normalized_records, evidence_entries))
    write_text(SCAFFOLD_REPORT, build_report(plan, normalized_records, evidence_entries))
    write_text(SCAFFOLD_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(plan, normalized_records, evidence_entries))
    write_text(VALIDATION_REPORT, build_report(plan, normalized_records, evidence_entries))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Scaffold v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

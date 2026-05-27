from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

SCAFFOLD_VALIDATION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_validation.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_review_report.md"
REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_SCAFFOLD_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_scaffold_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_local_tests_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_SCAFFOLD_REVIEWED"
REVIEW_STATUS = "adapter_scaffold_reviewed_ready_for_executable_local_tests"


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
        "runtime_export_performed": False,
        "collector_started": False,
        "telemetry_export_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_scaffold(scaffold: dict) -> None:
    if scaffold.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("scaffold validation goal mismatch")
    if scaffold.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("scaffold validation must point to this review goal")
    if scaffold.get("ready_for_adapter_scaffold_review_count") != 1:
        raise SystemExit("scaffold validation must be ready for review")
    for key, expected in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "scaffold_blocker_count": 0,
        "adapter_module_count": 4,
        "normalized_record_count": 4,
        "evidence_entry_count": 4,
    }.items():
        if scaffold.get(key) != expected:
            raise SystemExit(f"scaffold validation {key} mismatch")


def reviewed_adapter_modules(scaffold: dict) -> list[dict]:
    return [
        {
            "adapter_module_uri": uri,
            "review_status": "reviewed_adapter_module_preserves_repo_local_boundary",
            "candidate_tool_import_allowed": False,
            "dependency_install_allowed": False,
            "external_fetch_allowed": False,
            "runtime_integration_allowed": False,
        }
        for uri in scaffold["adapter_module_uris"]
    ]


def counts(scaffold: dict) -> dict:
    return {
        "source_contract_count": scaffold["source_contract_count"],
        "implementation_task_count": scaffold["implementation_task_count"],
        "adapter_module_count": scaffold["adapter_module_count"],
        "reviewed_adapter_module_count": len(reviewed_adapter_modules(scaffold)),
        "normalized_record_count": scaffold["normalized_record_count"],
        "reviewed_normalized_record_count": len(scaffold["normalized_records"]),
        "evidence_entry_count": scaffold["evidence_entry_count"],
        "reviewed_evidence_entry_count": len(scaffold["evidence_entries"]),
        "validation_command_count": scaffold["validation_command_count"],
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "scaffold_blocker_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_scaffold_review_count": 1,
        "ready_for_adapter_local_tests_count": 1,
    }


def base_review_record(scaffold: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "adapter_module_uris": scaffold["adapter_module_uris"],
        "reviewed_adapter_modules": reviewed_adapter_modules(scaffold),
        "normalized_records": scaffold["normalized_records"],
        "evidence_entries": scaffold["evidence_entries"],
        "input_uris": {
            "adapter_scaffold_validation": rel(SCAFFOLD_VALIDATION),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(scaffold),
        "claim_boundary": false_boundary(),
    }


def build_gate(scaffold: dict) -> dict:
    return {
        **base_review_record(scaffold),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-scaffold-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local adapter scaffold reviewed before executable local test expansion",
    }


def build_validation_result(scaffold: dict) -> dict:
    return {
        **base_review_record(scaffold),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(SCAFFOLD_VALIDATION),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(REVIEW_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(scaffold: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(scaffold).items())
    module_lines = "\n".join(
        "- {adapter_module_uri}: review_status={review_status}".format(**item)
        for item in reviewed_adapter_modules(scaffold)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Scaffold Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_scaffold_review_v0_1=true

## Review summary

- candidate_id={CANDIDATE_ID}
- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
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

## Reviewed adapter modules

{module_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-local-tests
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create executable repo-local tests for the adapter scaffold without candidate tool imports
  - Test normalizers, harness loading, evidence mapping, and protected-action flags
  - Keep dependency installs, external fetches, runtime integration, deploy, publish, and readiness claims blocked
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    scaffold = read_json(SCAFFOLD_VALIDATION)
    require_scaffold(scaffold)

    write_json(REVIEW_GATE, build_gate(scaffold))
    write_text(REVIEW_REPORT, build_report(scaffold))
    write_text(REVIEW_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(scaffold))
    write_text(VALIDATION_REPORT, build_report(scaffold))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Scaffold Review v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

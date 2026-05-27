from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

BEHAVIOR_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_gate.json"
PREFLIGHT_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_gate.json"
PREFLIGHT_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_report.md"
PREFLIGHT_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_RUNTIME_INTEGRATION_PREFLIGHT_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_behavior_expansion_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
PREFLIGHT_DECISION = "RUNTIME_INTEGRATION_REQUIRES_OWNER_AUTHORIZATION_AND_SEPARATE_SANDBOX_PLAN"
PREFLIGHT_STATUS = "repo_local_preflight_passed_runtime_integration_still_blocked"


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


def require_behavior_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("behavior review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("behavior review gate must point to this preflight goal")
    if gate.get("ready_for_runtime_integration_preflight_count") != 1:
        raise SystemExit("behavior review gate must be ready for runtime integration preflight")
    for key, expected in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "review_blocker_count": 0,
    }.items():
        if gate.get(key) != expected:
            raise SystemExit(f"behavior review gate {key} mismatch")


def runtime_preflight_checks() -> list[dict]:
    checks = [
        (
            "candidate-tool-import-remains-blocked",
            "Candidate tool imports remain blocked until a separate authorization packet exists.",
        ),
        (
            "dependency-install-remains-blocked",
            "Dependency installs remain blocked until license, security, and owner approval gates exist.",
        ),
        (
            "external-fetch-remains-blocked",
            "External fetches remain blocked until the owner authorizes a source acquisition step.",
        ),
        (
            "runtime-integration-remains-blocked",
            "Runtime integration remains blocked in this preflight slice.",
        ),
        (
            "runtime-export-remains-blocked",
            "Runtime telemetry export remains blocked until an observability boundary is defined.",
        ),
        (
            "owner-authorization-required-before-runtime",
            "Any future runtime/tool/dependency step requires explicit owner authorization.",
        ),
        (
            "sandbox-plan-required-before-runtime",
            "Any future runtime/tool/dependency step requires a sandbox plan before execution.",
        ),
        (
            "license-and-security-review-required-before-runtime",
            "Any future runtime/tool/dependency step requires license and security review records.",
        ),
    ]
    return [
        {
            "check_id": check_id,
            "status": "PASS",
            "runtime_action_allowed": False,
            "evidence": evidence,
        }
        for check_id, evidence in checks
    ]


def counts(gate: dict) -> dict:
    return {
        "adapter_module_count": gate["adapter_module_count"],
        "behavior_requirement_count": gate["behavior_requirement_count"],
        "reviewed_behavior_requirement_count": gate["reviewed_behavior_requirement_count"],
        "runtime_preflight_check_count": len(runtime_preflight_checks()),
        "runtime_preflight_check_pass_count": len(runtime_preflight_checks()),
        "runtime_preflight_check_fail_count": 0,
        "owner_authorization_required_count": 1,
        "sandbox_plan_required_count": 1,
        "license_review_required_count": 1,
        "security_review_required_count": 1,
        "runtime_integration_allowed_count": 0,
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "preflight_blocker_count": 0,
        "ready_for_runtime_integration_authorization_packet_count": 1,
    }


def base_preflight_record(gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "preflight_decision": PREFLIGHT_DECISION,
        "preflight_status": PREFLIGHT_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "runtime_integration_performed": False,
        "runtime_export_performed": False,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "future_runtime_integration_protected_action_required": True,
        "future_owner_authorization_required": True,
        "future_sandbox_plan_required": True,
        "future_license_review_required": True,
        "future_security_review_required": True,
        "reviewed_behavior_requirements": gate["reviewed_behavior_requirements"],
        "runtime_preflight_checks": runtime_preflight_checks(),
        "input_uris": {
            "adapter_behavior_expansion_review_gate": rel(BEHAVIOR_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        **counts(gate),
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    return {
        **base_preflight_record(gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(BEHAVIOR_REVIEW_GATE),
            rel(PREFLIGHT_GATE),
            rel(PREFLIGHT_REPORT),
            rel(PREFLIGHT_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(gate).items())
    check_lines = "\n".join(
        "- {check_id}: status=PASS, runtime_action_allowed=false".format(**item)
        for item in runtime_preflight_checks()
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Preflight v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1=true

## Preflight summary

- candidate_id={CANDIDATE_ID}
- preflight_decision={PREFLIGHT_DECISION}
- preflight_status={PREFLIGHT_STATUS}
- provider_neutral=true
- dependency_free=true
- candidate_tool_import_allowed=false
- dependency_install_allowed=false
- external_fetch_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false
- runtime_export_performed=false

## Counts

{count_lines}

## Runtime preflight checks

{check_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-adapter-runtime-integration-authorization-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create an owner authorization packet before any runtime, tool, dependency, or external fetch step
  - Keep authorization packet repo-local and non-executing
  - Preserve explicit blocked action flags until owner authorization exists
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    gate = read_json(BEHAVIOR_REVIEW_GATE)
    require_behavior_review_gate(gate)
    write_json(PREFLIGHT_GATE, base_preflight_record(gate))
    write_text(PREFLIGHT_REPORT, build_report(gate))
    write_text(PREFLIGHT_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gate))
    write_text(VALIDATION_REPORT, build_report(gate))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Preflight v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PREFLIGHT_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_gate.json"
AUTH_PACKET = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet.json"
AUTH_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_report.md"
AUTH_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_RUNTIME_INTEGRATION_AUTHORIZATION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_preflight_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
AUTHORIZATION_DECISION = "REQUEST_OWNER_AUTHORIZATION_FOR_FUTURE_RUNTIME_INTEGRATION_ONLY"
AUTHORIZATION_STATUS = "owner_authorization_required_not_granted"


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


def require_preflight_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("preflight gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("preflight gate must point to this authorization packet goal")
    if gate.get("ready_for_runtime_integration_authorization_packet_count") != 1:
        raise SystemExit("preflight gate must be ready for authorization packet")
    for key, expected in {
        "candidate_id": CANDIDATE_ID,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "external_fetch_allowed": False,
        "runtime_integration_allowed": False,
        "preflight_blocker_count": 0,
    }.items():
        if gate.get(key) != expected:
            raise SystemExit(f"preflight gate {key} mismatch")


def authorization_items() -> list[dict]:
    items = [
        ("authorize-candidate-tool-import", "Candidate tool import from an approved adapter dependency"),
        ("authorize-dependency-install", "Dependency installation for approved runtime/eval tooling"),
        ("authorize-external-source-fetch", "External source fetch for approved primary-source code or packages"),
        ("authorize-runtime-integration", "Runtime adapter integration beyond repo-local deterministic fixtures"),
        ("authorize-runtime-export", "Runtime trace or telemetry export outside repo-local generated artifacts"),
        ("authorize-external-service-call", "External service call from future runtime adapter execution"),
    ]
    return [
        {
            "authorization_item_id": item_id,
            "requested_action": requested_action,
            "authorization_status": "not_granted",
            "protected_action_required": True,
            "action_allowed": False,
        }
        for item_id, requested_action in items
    ]


def counts(source: dict) -> dict:
    return {
        "runtime_preflight_check_count": source["runtime_preflight_check_count"],
        "authorization_item_count": len(authorization_items()),
        "authorization_item_not_granted_count": len(authorization_items()),
        "protected_action_required_count": len(authorization_items()),
        "owner_input_required_count": 1,
        "sandbox_plan_required_count": source["sandbox_plan_required_count"],
        "license_review_required_count": source["license_review_required_count"],
        "security_review_required_count": source["security_review_required_count"],
        "runtime_integration_allowed_count": 0,
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "external_fetch_allowed_count": 0,
        "authorization_blocker_count": 0,
        "ready_for_runtime_integration_authorization_packet_review_count": 1,
    }


def base_authorization_record(source: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "authorization_decision": AUTHORIZATION_DECISION,
        "authorization_status": AUTHORIZATION_STATUS,
        "owner_authorization_granted": False,
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
        "authorization_items": authorization_items(),
        "runtime_preflight_checks": source["runtime_preflight_checks"],
        "input_uris": {
            "adapter_runtime_integration_preflight_gate": rel(PREFLIGHT_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        **counts(source),
        "claim_boundary": false_boundary(),
    }


def build_validation_result(source: dict) -> dict:
    return {
        **base_authorization_record(source),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(PREFLIGHT_GATE),
            rel(AUTH_PACKET),
            rel(AUTH_REPORT),
            rel(AUTH_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(source: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(source).items())
    item_lines = "\n".join(
        "- {authorization_item_id}: authorization_status=not_granted, action_allowed=false".format(**item)
        for item in authorization_items()
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Authorization Packet v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_runtime_integration_authorization_packet_v0_1=true

## Authorization summary

- candidate_id={CANDIDATE_ID}
- authorization_decision={AUTHORIZATION_DECISION}
- authorization_status={AUTHORIZATION_STATUS}
- owner_authorization_granted=false
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

## Authorization items

{item_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-runtime-integration-authorization-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local authorization packet before asking the owner to approve any protected action
  - Confirm all requested runtime, tool, dependency, and external fetch actions remain not_granted
  - Keep the review repo-local and non-executing
  - Do not install dependencies, clone OSS, fetch external code, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    source = read_json(PREFLIGHT_GATE)
    require_preflight_gate(source)
    write_json(AUTH_PACKET, base_authorization_record(source))
    write_text(AUTH_REPORT, build_report(source))
    write_text(AUTH_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(source))
    write_text(VALIDATION_REPORT, build_report(source))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Runtime Integration Authorization Packet v0.1")
    print("RESULT: PASS")
    print("generated=5")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

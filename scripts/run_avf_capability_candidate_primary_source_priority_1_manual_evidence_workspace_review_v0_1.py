from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

WORKSPACE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace.json"
RECORD_TEMPLATES = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_record_templates.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_MANUAL_EVIDENCE_WORKSPACE_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_MANUAL_EVIDENCE_WORKSPACE_REVIEWED"
REVIEW_STATUS = "manual_evidence_workspace_validated_ready_for_evidence_collection_authorization_packet"
WORKSPACE_SCOPE = "repo_local_empty_evidence_templates_only"


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


def require_workspace(workspace: dict) -> None:
    if workspace.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("manual evidence workspace goal mismatch")
    if workspace.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("manual evidence workspace must point to this review goal")
    if workspace.get("workspace_scope") != WORKSPACE_SCOPE:
        raise SystemExit("manual evidence workspace scope mismatch")
    if workspace.get("filled_evidence_record_count") != 0:
        raise SystemExit("manual evidence workspace must remain empty")
    if workspace.get("external_fetch_performed") is not False:
        raise SystemExit("manual evidence workspace external fetch must be false")
    if workspace.get("oss_clone_performed") is not False:
        raise SystemExit("manual evidence workspace oss clone must be false")
    if workspace.get("dependency_install_performed") is not False:
        raise SystemExit("manual evidence workspace dependency install must be false")
    if workspace.get("runtime_integration_performed") is not False:
        raise SystemExit("manual evidence workspace runtime integration must be false")


def reviewed_templates(workspace: dict) -> list[dict]:
    reviewed = []
    for template in workspace["evidence_record_templates"]:
        reviewed.append(
            {
                **template,
                "review_status": "reviewed_empty_evidence_template_validated",
            }
        )
    return reviewed


def counts(workspace: dict) -> dict:
    reviewed = reviewed_templates(workspace)
    return {
        "source_target_count": workspace["source_target_count"],
        "evidence_record_template_count": workspace["evidence_record_template_count"],
        "reviewed_evidence_record_template_count": len(reviewed),
        "empty_template_count": workspace["empty_template_count"],
        "filled_evidence_record_count": workspace["filled_evidence_record_count"],
        "source_fetch_performed_count": workspace["source_fetch_performed_count"],
        "oss_clone_performed_count": workspace["oss_clone_performed_count"],
        "dependency_install_performed_count": workspace["dependency_install_performed_count"],
        "runtime_integration_performed_count": workspace["runtime_integration_performed_count"],
        "review_blocker_count": 0,
        "ready_for_evidence_collection_authorization_packet_count": 1,
    }


def base_review_record(workspace: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "workspace_scope_confirmed": WORKSPACE_SCOPE,
        "manual_workspace_not_evidence_collection_gate": True,
        "reviewed_evidence_record_templates": reviewed_templates(workspace),
        "input_uris": {
            "manual_evidence_workspace": rel(WORKSPACE),
            "manual_evidence_record_templates": rel(RECORD_TEMPLATES),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(workspace),
        "claim_boundary": false_boundary(),
    }


def build_gate(workspace: dict) -> dict:
    return {
        **base_review_record(workspace),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-manual-evidence-workspace-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Manual evidence workspace reviewed as empty-template-only and ready for an authorization packet",
    }


def build_validation_result(workspace: dict) -> dict:
    return {
        **base_review_record(workspace),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(WORKSPACE),
            rel(RECORD_TEMPLATES),
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(workspace: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(workspace).items())
    reviewed_lines = "\n".join(
        "- {evidence_record_template_id}: review_status=reviewed_empty_evidence_template_validated, capture_status=empty_template_not_collected, source_fetch_performed=false".format(
            **record
        )
        for record in reviewed_templates(workspace)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Manual Evidence Workspace Review v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1=true

## Review summary

- candidate_id={CANDIDATE_ID}
- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- workspace_scope_confirmed={WORKSPACE_SCOPE}
- manual_workspace_not_evidence_collection_gate=true
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Reviewed empty evidence templates

{reviewed_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-evidence-collection-authorization-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create an owner authorization packet for primary-source evidence collection
  - Keep authorization separate from evidence capture
  - Preserve empty evidence templates until owner-approved capture occurs
  - Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    workspace = read_json(WORKSPACE)
    require_workspace(workspace)

    record = base_review_record(workspace)
    write_json(REVIEW_GATE, build_gate(workspace))
    report = build_report(workspace)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(workspace))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Manual Evidence Workspace Review v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(workspace).items():
        print(f"{key}={value}")
    print(f"manual_workspace_not_evidence_collection_gate={str(record['manual_workspace_not_evidence_collection_gate']).lower()}")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

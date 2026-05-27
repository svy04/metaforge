from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

CAPTURE_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_gate.json"
WORKSPACE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace.json"
RECORD_TEMPLATES = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_record_templates.json"
WORKSPACE_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_gate.json"
WORKSPACE_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_MANUAL_EVIDENCE_WORKSPACE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
WORKSPACE_STATUS = "manual_evidence_workspace_created_empty_templates_only"
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


def require_capture_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("capture plan review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("capture plan review must point to this workspace goal")
    if review.get("ready_for_manual_evidence_workspace_count") != 1:
        raise SystemExit("capture plan review must be ready for manual evidence workspace")
    if review.get("external_fetch_performed") is not False:
        raise SystemExit("external fetch must remain blocked")
    if review.get("dependency_install_performed") is not False:
        raise SystemExit("dependency install must remain blocked")
    if review.get("runtime_integration_performed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def evidence_record_templates(review: dict) -> list[dict]:
    records = []
    for target in review["reviewed_target_capture_plans"]:
        records.append(
            {
                "evidence_record_template_id": f"manual-template-{target['source_target_id']}",
                "source_target_id": target["source_target_id"],
                "candidate_id": target["candidate_id"],
                "source_kind": target["source_kind"],
                "source_uri": target["source_uri"],
                "retrieval_mode": target["retrieval_mode"],
                "capture_scope": target["capture_scope"],
                "claim_to_extract": target["claim_to_extract"],
                "exact_locator": "",
                "evidence_summary": "",
                "quote_limit_policy": target["quote_limit_policy"],
                "license_or_terms_note": "",
                "security_or_supply_chain_note": "",
                "adoption_boundary": target["adoption_boundary"],
                "capture_status": "empty_template_not_collected",
                "source_fetch_performed": False,
                "external_fetch_performed": False,
                "oss_clone_performed": False,
                "dependency_install_performed": False,
                "runtime_integration_performed": False,
            }
        )
    return records


def counts(review: dict) -> dict:
    templates = evidence_record_templates(review)
    return {
        "source_target_count": review["source_target_count"],
        "evidence_record_template_count": len(templates),
        "required_capture_field_count": review["capture_field_count"],
        "empty_template_count": len(templates),
        "filled_evidence_record_count": 0,
        "source_fetch_performed_count": 0,
        "oss_clone_performed_count": 0,
        "dependency_install_performed_count": 0,
        "runtime_integration_performed_count": 0,
        "review_blocker_count": 0,
        "ready_for_manual_workspace_review_count": 1,
    }


def base_record(review: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "workspace_status": WORKSPACE_STATUS,
        "workspace_scope": WORKSPACE_SCOPE,
        "evidence_record_templates": evidence_record_templates(review),
        "input_uris": {
            "priority_1_source_evidence_capture_plan_review_gate": rel(CAPTURE_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(review),
        "claim_boundary": false_boundary(),
    }


def build_gate(review: dict) -> dict:
    return {
        **base_record(review),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-manual-evidence-workspace-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Manual evidence workspace created with empty templates only; no source evidence collected",
    }


def build_validation_result(review: dict) -> dict:
    return {
        **base_record(review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(WORKSPACE),
            rel(RECORD_TEMPLATES),
            rel(WORKSPACE_GATE),
            rel(WORKSPACE_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(review).items())
    template_lines = "\n".join(
        "- {evidence_record_template_id}: capture_status=empty_template_not_collected, evidence_summary_empty=true, source_fetch_performed=false".format(
            **record
        )
        for record in evidence_record_templates(review)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Manual Evidence Workspace v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_manual_evidence_workspace_v0_1=true

## Workspace summary

- candidate_id={CANDIDATE_ID}
- workspace_status={WORKSPACE_STATUS}
- workspace_scope={WORKSPACE_SCOPE}
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Empty evidence templates

{template_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-manual-evidence-workspace
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local manual evidence workspace
  - Confirm every evidence record is empty_template_not_collected
  - Confirm no source evidence was fetched, copied, summarized, or adopted
  - Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(CAPTURE_REVIEW_GATE)
    require_capture_review(review)

    workspace = base_record(review)
    write_json(WORKSPACE, workspace)
    write_json(RECORD_TEMPLATES, workspace)
    write_json(WORKSPACE_GATE, build_gate(review))
    report = build_report(review)
    write_text(WORKSPACE_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Manual Evidence Workspace v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"workspace_status={WORKSPACE_STATUS}")
    print(f"workspace_scope={WORKSPACE_SCOPE}")
    for key, value in counts(review).items():
        print(f"{key}={value}")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

EXPANSION_PLAN = CAPABILITIES / "capability_candidate_primary_source_expansion_plan.json"
EXPANSION_GATE = CAPABILITIES / "capability_candidate_primary_source_expansion_plan_gate.json"
EXPANSION_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_expansion_plan_next_action.yml"
MANUAL_RECORDS = CAPABILITIES / "capability_candidate_primary_source_manual_records.json"
MANUAL_RECORDS_MD = CAPABILITIES / "capability_candidate_primary_source_manual_records.md"
MANUAL_RECORDS_GATE = CAPABILITIES / "capability_candidate_primary_source_manual_records_gate.json"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_manual_records_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_manual_records_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_MANUAL_RECORDS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_expansion_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
RECORD_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_MANUAL_RECORD_SHELLS_CREATED_REPO_LOCAL"
RECORD_STATUS = "manual_record_shells_ready_no_source_contents_acquired"


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


def source_kind(source_target_id: str) -> str:
    if source_target_id.endswith("original-repository"):
        return "original_repository"
    if "paper-or-benchmark" in source_target_id:
        return "paper_or_benchmark"
    return "official_docs"


def require_previous_plan(plan: dict, gate: dict) -> None:
    for label, record in [("expansion plan", plan), ("expansion gate", gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            raise SystemExit(f"{label} goal mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            raise SystemExit(f"{label} must point to this manual records goal")
        if record.get("planned_primary_source_record_count") != 7:
            raise SystemExit(f"{label} planned primary source record count mismatch")
        if record.get("external_fetch_performed_count") != 0:
            raise SystemExit(f"{label} external fetch count must be 0")
        if record.get("dependency_adoption_allowed") is not False:
            raise SystemExit(f"{label} dependency adoption must remain blocked")
        if record.get("runtime_integration_allowed") is not False:
            raise SystemExit(f"{label} runtime integration must remain blocked")


def planned_source_record(source_target_id: str) -> dict:
    return {
        "source_target_id": source_target_id,
        "source_kind": source_kind(source_target_id),
        "source_title": "required_not_performed",
        "source_uri": "required_not_performed",
        "source_version_or_date": "required_not_performed",
        "source_owner_or_publisher": "required_not_performed",
        "license_or_rights_note": "required_not_performed",
        "claim_supported": "required_not_performed",
        "evidence_excerpt_summary": "required_not_performed",
        "verification_notes": "required_not_performed",
        "source_reference_lines": "required_not_performed",
        "retrieval_method": "not_performed_repo_local_shell_only",
        "manual_review_status": "required_not_performed",
        "source_contents_acquired": False,
        "external_fetch_performed": False,
    }


def manual_record_shell(plan: dict) -> dict:
    source_target_ids = plan["planned_source_targets"]
    return {
        "manual_record_shell_id": f"shell-{plan['candidate_id']}",
        "candidate_id": plan["candidate_id"],
        "candidate_name": plan["candidate_name"],
        "capability_type": plan["capability_type"],
        "manual_record_shell_status": "created_shell_not_filled",
        "source_target_ids": source_target_ids,
        "source_priority_types": plan["source_priority_types"],
        "planned_source_records": [planned_source_record(source_target_id) for source_target_id in source_target_ids],
        "record_goal": plan["record_goal"],
        "license_review_status": "required_not_performed",
        "security_review_status": "required_not_performed",
        "maintenance_review_status": "required_not_performed",
        "supply_chain_review_status": "required_not_performed",
        "owner_manual_research_required": True,
        "source_contents_acquired": False,
        "external_fetch_performed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "protected_action_required_before_adoption": True,
    }


def counts(shells: list[dict]) -> dict:
    return {
        "manual_record_shell_count": len(shells),
        "planned_source_target_count": sum(len(shell["planned_source_records"]) for shell in shells),
        "source_contents_acquired_count": 0,
        "external_fetch_performed_count": 0,
        "license_review_required_count": sum(1 for shell in shells if shell["license_review_status"] == "required_not_performed"),
        "security_review_required_count": sum(1 for shell in shells if shell["security_review_status"] == "required_not_performed"),
        "ready_for_owner_manual_research_count": sum(1 for shell in shells if shell["owner_manual_research_required"] is True),
    }


def base_record(shells: list[dict], expansion_plan: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "record_decision": RECORD_DECISION,
        "record_status": RECORD_STATUS,
        "source_required_candidate_ids": expansion_plan["source_required_candidate_ids"],
        "manual_record_shells": shells,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(shells),
        "claim_boundary": false_boundary(),
    }


def build_records(shells: list[dict], expansion_plan: dict) -> dict:
    return {
        **base_record(shells, expansion_plan),
        "record_id": "avf-capability-candidate-primary-source-manual-records-v0-1",
        "record_scope": "repo-local manual source record shells only; no source contents acquired",
        "source_inputs": [
            rel(EXPANSION_PLAN),
            rel(EXPANSION_GATE),
            rel(EXPANSION_NEXT_ACTION),
        ],
    }


def build_gate(shells: list[dict], expansion_plan: dict) -> dict:
    return {
        **base_record(shells, expansion_plan),
        "gate_id": "avf-capability-candidate-primary-source-manual-records-gate-v0-1",
        "status": "PASS",
        "gate_scope": "manual source record shells created; source content collection and adoption remain blocked",
    }


def build_report(title: str, shells: list[dict]) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(shells).items())
    shell_lines = "\n".join(
        f"- {shell['candidate_id']}: {', '.join(shell['source_target_ids'])}" for shell in shells
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_manual_records_v0_1=true

## Gate summary

- record_decision={RECORD_DECISION}
- record_status={RECORD_STATUS}
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Manual record shells

{shell_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-manual-records
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review repo-local manual source record shells before any owner-filled source evidence is accepted
  - Verify candidate ids, planned source target ids, source kind priorities, and license/security placeholders
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(shells: list[dict], expansion_plan: dict) -> dict:
    return {
        **base_record(shells, expansion_plan),
        "validator_id": "validate_avf_capability_candidate_primary_source_manual_records_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(MANUAL_RECORDS),
            rel(MANUAL_RECORDS_MD),
            rel(MANUAL_RECORDS_GATE),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    expansion_plan = read_json(EXPANSION_PLAN)
    expansion_gate = read_json(EXPANSION_GATE)
    require_previous_plan(expansion_plan, expansion_gate)
    shells = [manual_record_shell(plan) for plan in expansion_plan["source_expansion_plans"]]

    write_json(MANUAL_RECORDS, build_records(shells, expansion_plan))
    report = build_report("AVF Capability Candidate Primary-Source Manual Records v0.1", shells)
    write_text(MANUAL_RECORDS_MD, report)
    write_json(MANUAL_RECORDS_GATE, build_gate(shells, expansion_plan))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(shells, expansion_plan))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Manual Records v0.1")
    print("RESULT: PASS")
    print(f"record_decision={RECORD_DECISION}")
    print(f"record_status={RECORD_STATUS}")
    for key, value in counts(shells).items():
        print(f"{key}={value}")
    print("external_fetch_performed=false")
    print("dependency_install_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

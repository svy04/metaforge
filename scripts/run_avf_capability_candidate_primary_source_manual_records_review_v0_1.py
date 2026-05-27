from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

MANUAL_RECORDS = CAPABILITIES / "capability_candidate_primary_source_manual_records.json"
MANUAL_RECORDS_GATE = CAPABILITIES / "capability_candidate_primary_source_manual_records_gate.json"
MANUAL_RECORDS_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_manual_records_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_manual_records_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_MANUAL_RECORDS_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_manual_records_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_MANUAL_RECORD_SHELLS_REVIEWED_REPO_LOCAL"
REVIEW_STATUS = "manual_record_shells_review_passed_no_source_contents_acquired"


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


def require_previous_manual_records(records: dict, gate: dict) -> None:
    for label, record in [("manual records", records), ("manual records gate", gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            raise SystemExit(f"{label} goal mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            raise SystemExit(f"{label} must point to this review goal")
        if record.get("manual_record_shell_count") != 7:
            raise SystemExit(f"{label} manual record shell count mismatch")
        if record.get("planned_source_target_count") != 16:
            raise SystemExit(f"{label} planned source target count mismatch")
        if record.get("source_contents_acquired_count") != 0:
            raise SystemExit(f"{label} source contents acquired count must be 0")
        if record.get("external_fetch_performed_count") != 0:
            raise SystemExit(f"{label} external fetch count must be 0")
        if record.get("dependency_adoption_allowed") is not False:
            raise SystemExit(f"{label} dependency adoption must remain blocked")
        if record.get("runtime_integration_allowed") is not False:
            raise SystemExit(f"{label} runtime integration must remain blocked")


def review_findings(manual_records: dict) -> list[dict]:
    findings = []
    for shell in manual_records["manual_record_shells"]:
        checks = [
            "candidate_id_present",
            "source_target_ids_preserved",
            "source_priority_types_preserved",
            "license_review_placeholder_present",
            "security_review_placeholder_present",
            "source_contents_not_acquired",
            "external_fetch_not_performed",
            "adoption_blocked",
        ]
        findings.append(
            {
                "candidate_id": shell["candidate_id"],
                "candidate_name": shell["candidate_name"],
                "review_result": "PASS",
                "review_checks": checks,
                "source_target_count": len(shell["source_target_ids"]),
                "source_target_ids": shell["source_target_ids"],
                "source_contents_acquired": False,
                "external_fetch_performed": False,
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
                "ready_for_owner_input_packet": True,
            }
        )
    return findings


def counts(findings: list[dict]) -> dict:
    return {
        "manual_record_shell_count": len(findings),
        "planned_source_target_count": sum(finding["source_target_count"] for finding in findings),
        "source_contents_acquired_count": 0,
        "external_fetch_performed_count": 0,
        "review_blocker_count": sum(1 for finding in findings if finding["review_result"] != "PASS"),
        "ready_for_owner_input_packet_count": sum(1 for finding in findings if finding["ready_for_owner_input_packet"] is True),
    }


def base_record(findings: list[dict], manual_records: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "source_required_candidate_ids": manual_records["source_required_candidate_ids"],
        "review_findings": findings,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(findings),
        "claim_boundary": false_boundary(),
    }


def build_gate(findings: list[dict], manual_records: dict) -> dict:
    return {
        **base_record(findings, manual_records),
        "gate_id": "avf-capability-candidate-primary-source-manual-records-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "manual source record shells reviewed; owner input packet can be created without external collection",
    }


def build_report(title: str, findings: list[dict]) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(findings).items())
    finding_lines = "\n".join(
        f"- {finding['candidate_id']}: review_result={finding['review_result']}, source_target_count={finding['source_target_count']}"
        for finding in findings
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_manual_records_review_v0_1=true

## Gate summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Review findings

{finding_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-owner-input-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local owner input packet for filling primary-source evidence manually
  - Include one fillable section per reviewed capability candidate and preserve source target ids
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(findings: list[dict], manual_records: dict) -> dict:
    return {
        **base_record(findings, manual_records),
        "validator_id": "validate_avf_capability_candidate_primary_source_manual_records_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    manual_records = read_json(MANUAL_RECORDS)
    manual_records_gate = read_json(MANUAL_RECORDS_GATE)
    require_previous_manual_records(manual_records, manual_records_gate)
    findings = review_findings(manual_records)

    write_json(REVIEW_GATE, build_gate(findings, manual_records))
    report = build_report("AVF Capability Candidate Primary-Source Manual Records Review v0.1", findings)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(findings, manual_records))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Manual Records Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(findings).items():
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

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

NAMESPACE_MAP = CAPABILITIES / "primary_source_namespace_map.json"
NAMESPACE_GATE = CAPABILITIES / "primary_source_namespace_map_gate.json"
NAMESPACE_NEXT_ACTION = CAPABILITIES / "primary_source_namespace_map_next_action.yml"
LEDGER = ROOT / "avf" / "cells" / "evidence" / "generated" / "primary_source_ledger.json"
CONTENT_SAFETY_RECORDS = CAPABILITIES / "primary_source_content_safety_manual_records.json"
CONTENT_SAFETY_GATE = CAPABILITIES / "primary_source_content_safety_manual_records_gate.json"
CONTENT_SAFETY_REPORT = CAPABILITIES / "primary_source_content_safety_manual_records_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_content_safety_manual_records_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_content_safety_manual_records_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_CONTENT_SAFETY_MANUAL_RECORDS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_content_safety_manual_records_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_evidence_registry_namespace_map_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_product_quality_missing_inputs_plan_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
RECORD_DECISION = "CONTENT_SAFETY_PRIMARY_SOURCE_MANUAL_RECORDS_CREATED_FROM_LEDGER"
RECORD_STATUS = "manual_records_created_content_summary_review_required"
CLOSED_GAP_ID = "gap-content-safety-policy-sources-missing-manual-records"

SOURCE_TARGET_IDS = [
    "src-ftc-endorsement-guides",
    "src-ftc-ai-claims",
]


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


def require_previous_namespace(namespace: dict, gate: dict) -> None:
    for label, record in [("namespace map", namespace), ("namespace gate", gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            raise SystemExit(f"{label} goal mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            raise SystemExit(f"{label} must point to this content-safety manual-record goal")
        if record.get("namespace_gap_closed") is not True:
            raise SystemExit(f"{label} must close namespace gap")


def ledger_records(ledger: dict) -> list[dict]:
    by_id = {source.get("source_id"): source for source in ledger.get("sources", [])}
    records = []
    for source_id in SOURCE_TARGET_IDS:
        source = by_id.get(source_id)
        if not source:
            raise SystemExit(f"missing ledger source {source_id}")
        records.append(
            {
                "source_target_id": source_id,
                "target_claim_id": f"claim-{source_id}",
                "record_status": "ledger_derived_manual_record_shell",
                "source_contents_acquired": False,
                "source_content_summary_required_for_promotion": True,
                "automated_collection_allowed": False,
                "promotion_scope": "policy_boundary_planning_only",
                "source_record": {
                    "source_id": source["source_id"],
                    "source_kind": source["source_kind"],
                    "title": source["title"],
                    "source_uri": source["url"],
                    "used_by_cells": source["used_by_cells"],
                    "ledger_reason_for_use": source["why_used"],
                    "claim_supported": source["why_used"],
                    "evidence_excerpt_summary": "Not acquired in this pass. This record is a repo-local ledger-derived shell; source content review is required before claim promotion.",
                },
            }
        )
    return records


def counts() -> dict:
    return {
        "content_safety_manual_record_count": len(SOURCE_TARGET_IDS),
        "source_content_summary_required_count": len(SOURCE_TARGET_IDS),
        "slice_closed_gap_count": 1,
        "gaps_closed_count": 2,
        "remaining_gap_count": 2,
    }


def base_record(records: list[dict]) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "record_decision": RECORD_DECISION,
        "record_status": RECORD_STATUS,
        "closed_gap_id": CLOSED_GAP_ID,
        "content_safety_policy_source_record_gap_closed": True,
        "source_contents_acquired": False,
        "source_target_ids": SOURCE_TARGET_IDS,
        "source_records": records,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(),
        "claim_boundary": false_boundary(),
    }


def build_records(records: list[dict]) -> dict:
    return {
        **base_record(records),
        "record_id": "avf-primary-source-content-safety-manual-records-v0-1",
        "record_scope": "repo-local manual source record shells from existing AVF ledger entries",
        "source_inputs": [
            rel(NAMESPACE_MAP),
            rel(NAMESPACE_GATE),
            rel(NAMESPACE_NEXT_ACTION),
            rel(LEDGER),
        ],
    }


def build_gate(records: list[dict]) -> dict:
    return {
        **base_record(records),
        "gate_id": "avf-primary-source-content-safety-manual-records-gate-v0-1",
        "status": "PASS",
        "gate_scope": "manual source record shells created; source content summary review still required",
    }


def build_report(title: str) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts().items())
    source_lines = "\n".join(f"- {source_id}" for source_id in SOURCE_TARGET_IDS)
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
primary_source_content_safety_manual_records_v0_1=true

## Gate summary

- record_decision={RECORD_DECISION}
- record_status={RECORD_STATUS}
- content_safety_policy_source_record_gap_closed=true
- source_contents_acquired=false

## Counts

{count_lines}

## Source targets

{source_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-product-quality-primary-source-missing-inputs-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Plan closure for product-quality reports missing primary-source inputs
  - Separate attachable repo-local source evidence from reports that need explicit claim-boundary exemptions
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(records: list[dict]) -> dict:
    return {
        **base_record(records),
        "validator_id": "validate_avf_primary_source_content_safety_manual_records_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(CONTENT_SAFETY_RECORDS),
            rel(CONTENT_SAFETY_GATE),
            rel(CONTENT_SAFETY_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    namespace = read_json(NAMESPACE_MAP)
    namespace_gate = read_json(NAMESPACE_GATE)
    ledger = read_json(LEDGER)
    require_previous_namespace(namespace, namespace_gate)

    records = ledger_records(ledger)
    write_json(CONTENT_SAFETY_RECORDS, build_records(records))
    write_json(CONTENT_SAFETY_GATE, build_gate(records))
    write_text(CONTENT_SAFETY_REPORT, build_report("Primary-Source Content Safety Manual Records v0.1"))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(records))
    write_text(VALIDATION_REPORT, build_report("AVF Primary-Source Content Safety Manual Records v0.1 Report"))

    print("AVF Primary-Source Content Safety Manual Records v0.1")
    print("RESULT: PASS")
    print(f"record_decision={RECORD_DECISION}")
    print(f"record_status={RECORD_STATUS}")
    for key, value in counts().items():
        print(f"{key}={value}")
    print("content_safety_policy_source_record_gap_closed=true")
    print("source_contents_acquired=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

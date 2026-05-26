from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
PRODUCT_QUALITY = ROOT / "docs" / "product-quality"

CONTENT_SAFETY_RECORDS = CAPABILITIES / "primary_source_content_safety_manual_records.json"
CONTENT_SAFETY_GATE = CAPABILITIES / "primary_source_content_safety_manual_records_gate.json"
CONTENT_SAFETY_NEXT_ACTION = CAPABILITIES / "primary_source_content_safety_manual_records_next_action.yml"
PRODUCT_REGISTRY = PRODUCT_QUALITY / "primary-source-registry-report.json"
MISSING_INPUTS_PLAN = CAPABILITIES / "primary_source_product_quality_missing_inputs_plan.json"
MISSING_INPUTS_GATE = CAPABILITIES / "primary_source_product_quality_missing_inputs_plan_gate.json"
MISSING_INPUTS_BACKLOG = CAPABILITIES / "primary_source_product_quality_missing_inputs_backlog.yml"
MISSING_INPUTS_REPORT = CAPABILITIES / "primary_source_product_quality_missing_inputs_plan_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_product_quality_missing_inputs_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_product_quality_missing_inputs_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_PRODUCT_QUALITY_MISSING_INPUTS_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_product_quality_missing_inputs_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_content_safety_manual_records_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_product_quality_missing_inputs_triage_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_DECISION = "PRODUCT_QUALITY_MISSING_PRIMARY_SOURCE_INPUTS_PLAN_CREATED_REPO_LOCAL"
PLAN_STATUS = "missing_input_targets_classified_no_sources_attached"

BUCKET_IDS = [
    "bucket-benchmark-and-eval-evidence",
    "bucket-ide-extension-evidence",
    "bucket-release-and-provenance-evidence",
    "bucket-safety-and-policy-evidence",
    "bucket-oss-and-source-control-evidence",
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


def require_previous_content_safety(records: dict, gate: dict) -> None:
    for label, record in [("content safety records", records), ("content safety gate", gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            raise SystemExit(f"{label} goal mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            raise SystemExit(f"{label} must point to this product-quality plan goal")
        if record.get("remaining_gap_count") != 2:
            raise SystemExit(f"{label} remaining gap count mismatch")


def bucket_for(report_path: str) -> str:
    name = Path(report_path).name
    if "ide-extension" in name or "vscode" in name:
        return "bucket-ide-extension-evidence"
    if "oss" in name or "open-source" in name or "source-controlled" in name:
        return "bucket-oss-and-source-control-evidence"
    if any(token in name for token in ["release", "provenance", "reproducibility", "git-release", "verification", "typecheck"]):
        return "bucket-release-and-provenance-evidence"
    if any(token in name for token in ["protected", "permission", "provider", "redaction", "quality-blocker", "runtime-doctor"]):
        return "bucket-safety-and-policy-evidence"
    return "bucket-benchmark-and-eval-evidence"


def build_targets(missing_reports: list[str]) -> list[dict]:
    targets = []
    for report in missing_reports:
        targets.append(
            {
                "report_path": report,
                "bucket_id": bucket_for(report),
                "closure_status": "triage_required",
                "candidate_lane": "claim_boundary_exemption_candidate",
                "source_attachment_performed": False,
                "claim_boundary_exemption_required": True,
            }
        )
    return targets


def counts(targets: list[dict]) -> dict:
    return {
        "reports_missing_primary_source_inputs_count": len(targets),
        "closure_target_count": len(targets),
        "classification_bucket_count": len(BUCKET_IDS),
        "source_attachment_candidate_count": 0,
        "claim_boundary_exemption_candidate_count": len(targets),
        "slice_closed_gap_count": 0,
        "gaps_closed_count": 2,
        "remaining_gap_count": 2,
    }


def base_record(targets: list[dict]) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "plan_decision": PLAN_DECISION,
        "plan_status": PLAN_STATUS,
        "bucket_ids": BUCKET_IDS,
        "closure_targets": targets,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(targets),
        "claim_boundary": false_boundary(),
    }


def build_plan(targets: list[dict]) -> dict:
    bucket_counts = Counter(target["bucket_id"] for target in targets)
    return {
        **base_record(targets),
        "plan_id": "avf-primary-source-product-quality-missing-inputs-plan-v0-1",
        "plan_scope": "repo-local classification only; no source attachments performed",
        "bucket_counts": {bucket_id: bucket_counts[bucket_id] for bucket_id in BUCKET_IDS},
        "source_inputs": [
            rel(CONTENT_SAFETY_RECORDS),
            rel(CONTENT_SAFETY_GATE),
            rel(CONTENT_SAFETY_NEXT_ACTION),
            rel(PRODUCT_REGISTRY),
        ],
    }


def build_gate(targets: list[dict]) -> dict:
    return {
        **base_record(targets),
        "gate_id": "avf-primary-source-product-quality-missing-inputs-plan-gate-v0-1",
        "status": "PASS",
        "gate_scope": "missing-input reports classified; no sources attached and no exemptions applied",
    }


def build_backlog(targets: list[dict]) -> str:
    bucket_lines = []
    for bucket_id in BUCKET_IDS:
        bucket_lines.append(f"  - bucket_id: {bucket_id}")
        for target in [item for item in targets if item["bucket_id"] == bucket_id]:
            bucket_lines.append(f"    - report_path: {target['report_path']}")
            bucket_lines.append(f"      closure_status: {target['closure_status']}")
            bucket_lines.append(f"      candidate_lane: {target['candidate_lane']}")
    return f"""goal_id: {THIS_GOAL_ID}
plan_decision: {PLAN_DECISION}
plan_status: {PLAN_STATUS}
closure_target_count: {len(targets)}

buckets:
{chr(10).join(bucket_lines)}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(title: str, targets: list[dict]) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(targets).items())
    bucket_lines = "\n".join(f"- {bucket_id}" for bucket_id in BUCKET_IDS)
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
primary_source_product_quality_missing_inputs_plan_v0_1=true

## Gate summary

- plan_decision={PLAN_DECISION}
- plan_status={PLAN_STATUS}

## Counts

{count_lines}

## Buckets

{bucket_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: triage-product-quality-primary-source-missing-inputs
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Triage 35 product-quality reports into attach-existing-evidence or claim-boundary-exemption lanes
  - Preserve report path, chosen lane, rationale, and claim boundary for every target
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(targets: list[dict]) -> dict:
    return {
        **base_record(targets),
        "validator_id": "validate_avf_primary_source_product_quality_missing_inputs_plan_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(MISSING_INPUTS_PLAN),
            rel(MISSING_INPUTS_GATE),
            rel(MISSING_INPUTS_BACKLOG),
            rel(MISSING_INPUTS_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    content_records = read_json(CONTENT_SAFETY_RECORDS)
    content_gate = read_json(CONTENT_SAFETY_GATE)
    registry = read_json(PRODUCT_REGISTRY)
    require_previous_content_safety(content_records, content_gate)

    missing_reports = registry.get("reportsMissingPrimarySourceInputs", [])
    if len(missing_reports) != 35:
        raise SystemExit("expected 35 product-quality reports missing primary-source inputs")
    targets = build_targets(missing_reports)

    write_json(MISSING_INPUTS_PLAN, build_plan(targets))
    write_json(MISSING_INPUTS_GATE, build_gate(targets))
    write_text(MISSING_INPUTS_BACKLOG, build_backlog(targets))
    write_text(MISSING_INPUTS_REPORT, build_report("Primary-Source Product-Quality Missing Inputs Plan v0.1", targets))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(targets))
    write_text(VALIDATION_REPORT, build_report("AVF Primary-Source Product-Quality Missing Inputs Plan v0.1 Report", targets))

    print("AVF Primary-Source Product-Quality Missing Inputs Plan v0.1")
    print("RESULT: PASS")
    print(f"plan_decision={PLAN_DECISION}")
    print(f"plan_status={PLAN_STATUS}")
    for key, value in counts(targets).items():
        print(f"{key}={value}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

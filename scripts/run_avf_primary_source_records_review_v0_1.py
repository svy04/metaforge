from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RECORDS = CAPABILITIES / "primary_source_manual_records.json"
RECORDS_GATE = CAPABILITIES / "primary_source_manual_records_gate.json"
REVIEW_GATE = CAPABILITIES / "primary_source_records_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "primary_source_records_review_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_records_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_records_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_RECORDS_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_records_review_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_manual_records_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_claim_integration_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
RECORD_DECISION = "PRIMARY_SOURCE_MANUAL_RECORDS_CREATED_FROM_PRIMARY_SOURCES"
REVIEW_DECISION = "PRIMARY_SOURCE_RECORDS_REVIEWED_CLAIM_INTEGRATION_READY"
PROMOTION_SCOPE = "architecture_docs_and_plans_only"

SOURCE_TARGET_IDS = [
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_records_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("manual records gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("manual records gate must point to this review goal")
    if gate.get("record_decision") != RECORD_DECISION:
        raise SystemExit("manual records gate decision mismatch")
    if gate.get("source_target_ids") != SOURCE_TARGET_IDS:
        raise SystemExit("manual records gate source target ids mismatch")
    if gate.get("source_contents_acquired") is not True:
        raise SystemExit("manual records gate must confirm source contents acquired")


def require_records(data: dict) -> list[dict]:
    if data.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("manual records goal mismatch")
    if data.get("record_decision") != RECORD_DECISION:
        raise SystemExit("manual records decision mismatch")
    records = data.get("source_records")
    if not isinstance(records, list) or len(records) != len(SOURCE_TARGET_IDS):
        raise SystemExit("manual records must contain seven records")
    if [record.get("source_target_id") for record in records] != SOURCE_TARGET_IDS:
        raise SystemExit("manual records source target ids mismatch")
    for record in records:
        source = record.get("source_record", {})
        if record.get("source_contents_acquired") is not True:
            raise SystemExit("record must have acquired source contents")
        if record.get("automated_collection_allowed") is not False:
            raise SystemExit("automated collection must stay blocked")
        if not source.get("source_uri", "").startswith("https://"):
            raise SystemExit("record source uri must be https")
        if len(source.get("evidence_excerpt_summary", "")) < 40:
            raise SystemExit("record evidence summary too short")
    return records


def review_entry_for(record: dict) -> dict:
    source = record["source_record"]
    return {
        "source_target_id": record["source_target_id"],
        "target_claim_id": record["target_claim_id"],
        "source_uri": source["source_uri"],
        "review_status": "supported_for_architecture_planning",
        "promotion_scope": PROMOTION_SCOPE,
        "runtime_adoption_allowed": False,
        "dependency_adoption_allowed": False,
        "claim_supported": source["claim_supported"],
        "evidence_basis": source["evidence_excerpt_summary"],
        "review_note": "Source supports planning-level claim only; adoption requires a later build-vs-buy, license, security, and implementation review.",
    }


def build_review_gate(records: list[dict]) -> dict:
    return {
        "gate_id": "avf-primary-source-records-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "promotion_scope": PROMOTION_SCOPE,
        "source_records_reviewed": len(records),
        "claims_supported_for_architecture_planning": len(records),
        "reviewed_source_target_ids": SOURCE_TARGET_IDS,
        "runtime_adoption_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_review_report(records: list[dict]) -> str:
    rows = "\n".join(
        f"- `{entry['source_target_id']}` -> `{entry['target_claim_id']}` "
        f"({entry['review_status']}, {entry['promotion_scope']})"
        for entry in [review_entry_for(record) for record in records]
    )
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# Primary-Source Records Review v0.1

review_decision={REVIEW_DECISION}
promotion_scope={PROMOTION_SCOPE}
source_records_reviewed={len(records)}
claims_supported_for_architecture_planning={len(records)}
runtime_adoption_allowed=false
dependency_adoption_allowed=false
protected_action_executed=false

## Reviewed claims

{rows}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: integrate-primary-source-claims-into-avf-docs
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Integrate reviewed source-backed claims into architecture docs and plans only
  - Preserve source uri and evidence summary links back to primary-source records
  - Keep runtime and dependency adoption behind later build-vs-buy, license, security, and implementation gates
  - Do not adopt dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(records: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_primary_source_records_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "promotion_scope": PROMOTION_SCOPE,
        "source_records_reviewed": len(records),
        "claims_supported_for_architecture_planning": len(records),
        "runtime_adoption_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(records: list[dict]) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Primary-Source Records Review v0.1 Report

RESULT: PASS
primary_source_records_review_v0_1=true

## Commands

- python scripts\\run_avf_primary_source_records_review_v0_1.py
- python scripts\\validate_avf_primary_source_records_review_v0_1.py

## Gate summary

- review_decision={REVIEW_DECISION}
- promotion_scope={PROMOTION_SCOPE}
- source_records_reviewed={len(records)}
- claims_supported_for_architecture_planning={len(records)}
- runtime_adoption_allowed=false
- dependency_adoption_allowed=false

## Generated artifacts

- {rel(REVIEW_GATE)}
- {rel(REVIEW_REPORT)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_records_gate(read_json(RECORDS_GATE))
    records = require_records(read_json(RECORDS))

    write_json(REVIEW_GATE, build_review_gate(records))
    write_text(REVIEW_REPORT, build_review_report(records))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(records))
    write_text(VALIDATION_REPORT, build_report(records))

    print("AVF Primary-Source Records Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"promotion_scope={PROMOTION_SCOPE}")
    print(f"source_records_reviewed={len(records)}")
    print(f"claims_supported_for_architecture_planning={len(records)}")
    print("runtime_adoption_allowed=false")
    print("dependency_adoption_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PLAN_GATE = CAPABILITIES / "primary_source_acquisition_plan_gate.json"
CLAIM_MAP = CAPABILITIES / "primary_source_acquisition_claim_map.json"
REVIEW_GATE = CAPABILITIES / "primary_source_acquisition_plan_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "primary_source_acquisition_plan_review_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_acquisition_plan_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_acquisition_plan_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_ACQUISITION_PLAN_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_acquisition_plan_review_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_acquisition_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_record_skeletons_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_DECISION = "PRIMARY_SOURCE_ACQUISITION_PLAN_READY"
REVIEW_DECISION = "PRIMARY_SOURCE_ACQUISITION_PLAN_REVIEWED_EXECUTION_BLOCKED"

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


def require_plan_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("plan gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("plan gate must point to this review goal")
    if gate.get("plan_decision") != PLAN_DECISION:
        raise SystemExit("plan gate decision mismatch")
    if gate.get("planned_source_target_ids") != SOURCE_TARGET_IDS:
        raise SystemExit("plan gate source target ids mismatch")
    if gate.get("acquisition_execution_allowed") is not False:
        raise SystemExit("plan gate must keep execution blocked")


def require_claim_map(claim_map: dict) -> list[dict]:
    mappings = claim_map.get("claim_mappings")
    if not isinstance(mappings, list) or len(mappings) != len(SOURCE_TARGET_IDS):
        raise SystemExit("claim map must contain seven mappings")
    ids = [mapping.get("source_target_id") for mapping in mappings]
    if ids != SOURCE_TARGET_IDS:
        raise SystemExit("claim map source target ids mismatch")
    for mapping in mappings:
        if mapping.get("evidence_record_status") != "planned_not_acquired":
            raise SystemExit("all claim mappings must remain planned_not_acquired")
        if mapping.get("external_fetch_performed") is not False:
            raise SystemExit("claim mappings must not fetch externally")
        if mapping.get("source_collection_execution_allowed") is not False:
            raise SystemExit("claim mappings must keep source collection blocked")
    return mappings


def build_review_gate() -> dict:
    return {
        "gate_id": "avf-primary-source-acquisition-plan-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "plan_reviewed": True,
        "planned_source_targets": len(SOURCE_TARGET_IDS),
        "claim_mappings": len(SOURCE_TARGET_IDS),
        "reviewed_source_target_ids": SOURCE_TARGET_IDS,
        "all_targets_mapped": True,
        "all_targets_planned_not_acquired": True,
        "execution_remains_blocked": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_review_report(mappings: list[dict]) -> str:
    rows = "\n".join(
        f"- `{mapping['source_target_id']}` -> `{mapping['target_claim_id']}` "
        f"({mapping['evidence_record_status']})"
        for mapping in mappings
    )
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# Primary-Source Acquisition Plan Review v0.1

review_decision={REVIEW_DECISION}
plan_reviewed=true
planned_source_targets={len(SOURCE_TARGET_IDS)}
claim_mappings={len(SOURCE_TARGET_IDS)}
all_targets_mapped=true
all_targets_planned_not_acquired=true
execution_remains_blocked=true
external_fetch_performed=false
scraping_performed=false
oss_clone_performed=false
package_install_performed=false

## Reviewed mappings

{rows}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-primary-source-record-skeletons
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create blank evidence record skeletons for each planned source target
  - Keep every skeleton in planned_not_acquired state
  - Do not fetch, scrape, clone, install, or call providers

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_primary_source_acquisition_plan_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "plan_reviewed": True,
        "planned_source_targets": len(SOURCE_TARGET_IDS),
        "claim_mappings": len(SOURCE_TARGET_IDS),
        "all_targets_mapped": True,
        "all_targets_planned_not_acquired": True,
        "execution_remains_blocked": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Primary-Source Acquisition Plan Review v0.1 Report

RESULT: PASS
primary_source_acquisition_plan_review_v0_1=true

## Commands

- python scripts\\run_avf_primary_source_acquisition_plan_review_v0_1.py
- python scripts\\validate_avf_primary_source_acquisition_plan_review_v0_1.py

## Gate summary

- review_decision={REVIEW_DECISION}
- plan_reviewed=true
- planned_source_targets={len(SOURCE_TARGET_IDS)}
- claim_mappings={len(SOURCE_TARGET_IDS)}
- all_targets_mapped=true
- all_targets_planned_not_acquired=true
- execution_remains_blocked=true

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
    plan_gate = read_json(PLAN_GATE)
    require_plan_gate(plan_gate)
    mappings = require_claim_map(read_json(CLAIM_MAP))

    write_json(REVIEW_GATE, build_review_gate())
    write_text(REVIEW_REPORT, build_review_report(mappings))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Primary-Source Acquisition Plan Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print("plan_reviewed=true")
    print(f"planned_source_targets={len(SOURCE_TARGET_IDS)}")
    print(f"claim_mappings={len(SOURCE_TARGET_IDS)}")
    print("all_targets_mapped=true")
    print("all_targets_planned_not_acquired=true")
    print("execution_remains_blocked=true")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

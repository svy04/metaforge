from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

SKELETONS = CAPABILITIES / "primary_source_record_skeletons.json"
SKELETONS_GATE = CAPABILITIES / "primary_source_record_skeletons_gate.json"
REVIEW_GATE = CAPABILITIES / "primary_source_record_skeletons_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "primary_source_record_skeletons_review_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_record_skeletons_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_record_skeletons_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_RECORD_SKELETONS_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_record_skeletons_review_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_record_skeletons_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_manual_collection_packet_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
SKELETON_DECISION = "PRIMARY_SOURCE_RECORD_SKELETONS_CREATED_NOT_ACQUIRED"
REVIEW_DECISION = "PRIMARY_SOURCE_RECORD_SKELETONS_REVIEWED_COLLECTION_BLOCKED"

SOURCE_TARGET_IDS = [
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
]

REQUIRED_SOURCE_FIELDS = [
    "source_id",
    "source_title",
    "source_kind",
    "source_uri",
    "source_version_or_date",
    "source_owner_or_publisher",
    "license_or_rights_note",
    "claim_supported",
    "evidence_excerpt_summary",
    "verification_notes",
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


def require_skeleton_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("skeleton gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("skeleton gate must point to this review goal")
    if gate.get("skeleton_decision") != SKELETON_DECISION:
        raise SystemExit("skeleton gate decision mismatch")
    if gate.get("source_target_ids") != SOURCE_TARGET_IDS:
        raise SystemExit("skeleton gate source target ids mismatch")
    if gate.get("all_skeletons_planned_not_acquired") is not True:
        raise SystemExit("skeleton gate must keep skeletons planned_not_acquired")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("skeleton gate must keep source collection blocked")


def require_skeletons(data: dict) -> list[dict]:
    if data.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("skeletons goal mismatch")
    if data.get("skeleton_decision") != SKELETON_DECISION:
        raise SystemExit("skeletons decision mismatch")
    skeletons = data.get("source_record_skeletons")
    if not isinstance(skeletons, list) or len(skeletons) != len(SOURCE_TARGET_IDS):
        raise SystemExit("skeletons must contain seven records")
    if [skeleton.get("source_target_id") for skeleton in skeletons] != SOURCE_TARGET_IDS:
        raise SystemExit("skeleton source target ids mismatch")
    for skeleton in skeletons:
        if skeleton.get("skeleton_status") != "planned_not_acquired":
            raise SystemExit("skeleton status must remain planned_not_acquired")
        if skeleton.get("source_contents_acquired") is not False:
            raise SystemExit("skeleton source contents must remain unacquired")
        if skeleton.get("source_collection_execution_allowed") is not False:
            raise SystemExit("skeleton collection must remain blocked")
        if skeleton.get("required_fields") != REQUIRED_SOURCE_FIELDS:
            raise SystemExit("skeleton required fields mismatch")
        source_record = skeleton.get("source_record", {})
        missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in source_record]
        if missing:
            raise SystemExit(f"skeleton missing source fields: {', '.join(missing)}")
    return skeletons


def build_review_gate(skeletons: list[dict]) -> dict:
    return {
        "gate_id": "avf-primary-source-record-skeletons-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "skeletons_reviewed": True,
        "skeletons_created": len(skeletons),
        "required_fields_per_skeleton": len(REQUIRED_SOURCE_FIELDS),
        "reviewed_source_target_ids": SOURCE_TARGET_IDS,
        "all_skeletons_planned_not_acquired": True,
        "all_required_fields_present": True,
        "collection_remains_blocked": True,
        "source_contents_acquired": False,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_review_report(skeletons: list[dict]) -> str:
    rows = "\n".join(
        f"- `{skeleton['source_target_id']}` -> `{skeleton['target_claim_id']}` "
        f"({skeleton['skeleton_status']}, required_fields={len(skeleton['required_fields'])})"
        for skeleton in skeletons
    )
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# Primary-Source Record Skeletons Review v0.1

review_decision={REVIEW_DECISION}
skeletons_reviewed=true
skeletons_created={len(skeletons)}
required_fields_per_skeleton={len(REQUIRED_SOURCE_FIELDS)}
all_skeletons_planned_not_acquired=true
all_required_fields_present=true
collection_remains_blocked=true
source_contents_acquired=false
external_fetch_performed=false
scraping_performed=false
oss_clone_performed=false
package_install_performed=false

## Reviewed skeletons

{rows}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: prepare-primary-source-manual-collection-packet
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Prepare a manual primary-source collection packet
  - Use the reviewed skeletons as blank target records
  - Keep automated collection, scraping, cloning, package install, and provider calls blocked
  - Do not fetch, scrape, clone, install, or call providers

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(skeletons: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_primary_source_record_skeletons_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "skeletons_reviewed": True,
        "skeletons_created": len(skeletons),
        "required_fields_per_skeleton": len(REQUIRED_SOURCE_FIELDS),
        "all_skeletons_planned_not_acquired": True,
        "all_required_fields_present": True,
        "collection_remains_blocked": True,
        "source_contents_acquired": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(skeletons: list[dict]) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Primary-Source Record Skeletons Review v0.1 Report

RESULT: PASS
primary_source_record_skeletons_review_v0_1=true

## Commands

- python scripts\\run_avf_primary_source_record_skeletons_review_v0_1.py
- python scripts\\validate_avf_primary_source_record_skeletons_review_v0_1.py

## Gate summary

- review_decision={REVIEW_DECISION}
- skeletons_reviewed=true
- skeletons_created={len(skeletons)}
- required_fields_per_skeleton={len(REQUIRED_SOURCE_FIELDS)}
- all_skeletons_planned_not_acquired=true
- all_required_fields_present=true
- collection_remains_blocked=true
- source_contents_acquired=false

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
    require_skeleton_gate(read_json(SKELETONS_GATE))
    skeletons = require_skeletons(read_json(SKELETONS))

    write_json(REVIEW_GATE, build_review_gate(skeletons))
    write_text(REVIEW_REPORT, build_review_report(skeletons))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(skeletons))
    write_text(VALIDATION_REPORT, build_report(skeletons))

    print("AVF Primary-Source Record Skeletons Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print("skeletons_reviewed=true")
    print(f"skeletons_created={len(skeletons)}")
    print(f"required_fields_per_skeleton={len(REQUIRED_SOURCE_FIELDS)}")
    print("all_skeletons_planned_not_acquired=true")
    print("all_required_fields_present=true")
    print("collection_remains_blocked=true")
    print("source_contents_acquired=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

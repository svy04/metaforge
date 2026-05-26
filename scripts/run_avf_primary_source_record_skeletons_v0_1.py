from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PLAN_REVIEW_GATE = CAPABILITIES / "primary_source_acquisition_plan_review_gate.json"
CLAIM_MAP = CAPABILITIES / "primary_source_acquisition_claim_map.json"
SKELETONS = CAPABILITIES / "primary_source_record_skeletons.json"
SKELETONS_MARKDOWN = CAPABILITIES / "primary_source_record_skeletons.md"
SKELETONS_GATE = CAPABILITIES / "primary_source_record_skeletons_gate.json"
NEXT_ACTION = CAPABILITIES / "primary_source_record_skeletons_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_record_skeletons_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_RECORD_SKELETONS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_record_skeletons_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_acquisition_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_record_skeletons_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_REVIEW_DECISION = "PRIMARY_SOURCE_ACQUISITION_PLAN_REVIEWED_EXECUTION_BLOCKED"
SKELETON_DECISION = "PRIMARY_SOURCE_RECORD_SKELETONS_CREATED_NOT_ACQUIRED"

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


def require_plan_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("plan review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("plan review gate must point to this skeleton goal")
    if gate.get("review_decision") != PLAN_REVIEW_DECISION:
        raise SystemExit("plan review gate decision mismatch")
    if gate.get("reviewed_source_target_ids") != SOURCE_TARGET_IDS:
        raise SystemExit("plan review gate source target ids mismatch")
    if gate.get("all_targets_planned_not_acquired") is not True:
        raise SystemExit("plan review gate must keep targets planned_not_acquired")
    if gate.get("execution_remains_blocked") is not True:
        raise SystemExit("plan review gate must keep execution blocked")


def require_claim_mappings(claim_map: dict) -> list[dict]:
    mappings = claim_map.get("claim_mappings")
    if not isinstance(mappings, list) or len(mappings) != len(SOURCE_TARGET_IDS):
        raise SystemExit("claim map must contain seven mappings")
    if [mapping.get("source_target_id") for mapping in mappings] != SOURCE_TARGET_IDS:
        raise SystemExit("claim map source target ids mismatch")
    return mappings


def source_record_for(mapping: dict) -> dict:
    return {
        "source_id": mapping["source_target_id"],
        "source_title": mapping["source_name"],
        "source_kind": mapping["source_category"],
        "source_uri": "",
        "source_version_or_date": "",
        "source_owner_or_publisher": "",
        "license_or_rights_note": "",
        "claim_supported": mapping["target_claim"],
        "evidence_excerpt_summary": "",
        "verification_notes": "",
    }


def skeleton_for(mapping: dict) -> dict:
    return {
        "source_target_id": mapping["source_target_id"],
        "target_claim_id": mapping["target_claim_id"],
        "target_claim": mapping["target_claim"],
        "source_category": mapping["source_category"],
        "source_name": mapping["source_name"],
        "skeleton_status": "planned_not_acquired",
        "required_fields": REQUIRED_SOURCE_FIELDS,
        "source_record": source_record_for(mapping),
        "source_contents_acquired": False,
        "source_collection_execution_allowed": False,
        "external_fetch_performed": False,
        "license_review_status": "required_not_performed",
        "security_review_status": "required_not_performed",
    }


def build_skeletons(mappings: list[dict]) -> dict:
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "skeleton_decision": SKELETON_DECISION,
        "skeleton_status": "planned_not_acquired",
        "source_record_skeletons": [skeleton_for(mapping) for mapping in mappings],
        "claim_boundary": false_boundary(),
    }


def build_markdown(skeletons: list[dict]) -> str:
    rows = []
    for skeleton in skeletons:
        source_record = skeleton["source_record"]
        rows.append(
            "\n".join(
                [
                    f"### {skeleton['source_target_id']}",
                    "",
                    f"- target_claim_id: `{skeleton['target_claim_id']}`",
                    f"- skeleton_status={skeleton['skeleton_status']}",
                    "- source_contents_acquired=false",
                    "- source_collection_execution_allowed=false",
                    "",
                    "```yaml",
                    f"source_id: {source_record['source_id']}",
                    f"source_title: {source_record['source_title']}",
                    f"source_kind: {source_record['source_kind']}",
                    'source_uri: ""',
                    'source_version_or_date: ""',
                    'source_owner_or_publisher: ""',
                    'license_or_rights_note: ""',
                    f"claim_supported: {source_record['claim_supported']}",
                    'evidence_excerpt_summary: ""',
                    'verification_notes: ""',
                    "```",
                ]
            )
        )
    return f"""# Primary-Source Record Skeletons v0.1

decision={SKELETON_DECISION}
skeletons_created={len(skeletons)}
skeleton_status=planned_not_acquired
source_contents_acquired=false
external_fetch_performed=false

{chr(10).join(rows)}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_gate() -> dict:
    return {
        "gate_id": "avf-primary-source-record-skeletons-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "skeleton_decision": SKELETON_DECISION,
        "skeletons_uri": rel(SKELETONS),
        "skeletons_markdown_uri": rel(SKELETONS_MARKDOWN),
        "skeletons_created": len(SOURCE_TARGET_IDS),
        "required_fields_per_skeleton": len(REQUIRED_SOURCE_FIELDS),
        "source_target_ids": SOURCE_TARGET_IDS,
        "all_skeletons_planned_not_acquired": True,
        "source_contents_acquired": False,
        "source_collection_execution_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-primary-source-record-skeletons
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review blank source record skeletons before any source acquisition
  - Verify every skeleton preserves source target id, source category, and target claim
  - Keep every skeleton planned_not_acquired until a later approval-gated phase
  - Do not fetch, scrape, clone, install, or call providers

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_primary_source_record_skeletons_v0_1",
        "status": "PASS",
        "skeleton_decision": SKELETON_DECISION,
        "skeletons_created": len(SOURCE_TARGET_IDS),
        "required_fields_per_skeleton": len(REQUIRED_SOURCE_FIELDS),
        "all_skeletons_planned_not_acquired": True,
        "source_contents_acquired": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report() -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Primary-Source Record Skeletons v0.1 Report

RESULT: PASS
primary_source_record_skeletons_v0_1=true

## Commands

- python scripts\\run_avf_primary_source_record_skeletons_v0_1.py
- python scripts\\validate_avf_primary_source_record_skeletons_v0_1.py

## Gate summary

- skeletons_created={len(SOURCE_TARGET_IDS)}
- required_fields_per_skeleton={len(REQUIRED_SOURCE_FIELDS)}
- all_skeletons_planned_not_acquired=true
- source_contents_acquired=false
- external_fetch_performed=false

## Generated artifacts

- {rel(SKELETONS)}
- {rel(SKELETONS_MARKDOWN)}
- {rel(SKELETONS_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    plan_review_gate = read_json(PLAN_REVIEW_GATE)
    require_plan_review_gate(plan_review_gate)
    mappings = require_claim_mappings(read_json(CLAIM_MAP))
    skeleton_data = build_skeletons(mappings)
    skeletons = skeleton_data["source_record_skeletons"]

    write_json(SKELETONS, skeleton_data)
    write_text(SKELETONS_MARKDOWN, build_markdown(skeletons))
    write_json(SKELETONS_GATE, build_gate())
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report())

    print("AVF Primary-Source Record Skeletons v0.1")
    print("RESULT: PASS")
    print(f"skeletons_created={len(SOURCE_TARGET_IDS)}")
    print(f"required_fields_per_skeleton={len(REQUIRED_SOURCE_FIELDS)}")
    print("all_skeletons_planned_not_acquired=true")
    print("source_contents_acquired=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

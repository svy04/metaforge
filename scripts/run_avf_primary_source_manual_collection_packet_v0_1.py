from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

SKELETONS = CAPABILITIES / "primary_source_record_skeletons.json"
SKELETONS_REVIEW_GATE = CAPABILITIES / "primary_source_record_skeletons_review_gate.json"
PACKET = CAPABILITIES / "primary_source_manual_collection_packet.json"
PACKET_MARKDOWN = CAPABILITIES / "primary_source_manual_collection_packet.md"
PACKET_GATE = CAPABILITIES / "primary_source_manual_collection_packet_gate.json"
NEXT_ACTION = CAPABILITIES / "primary_source_manual_collection_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_manual_collection_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_MANUAL_COLLECTION_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_manual_collection_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_record_skeletons_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_manual_records_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "PRIMARY_SOURCE_RECORD_SKELETONS_REVIEWED_COLLECTION_BLOCKED"
PACKET_DECISION = "PRIMARY_SOURCE_MANUAL_COLLECTION_PACKET_READY_NOT_EXECUTED"

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


def require_skeleton_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("skeleton review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("skeleton review gate must point to this packet goal")
    if gate.get("review_decision") != REVIEW_DECISION:
        raise SystemExit("skeleton review gate decision mismatch")
    if gate.get("collection_remains_blocked") is not True:
        raise SystemExit("skeleton review gate must keep collection blocked")
    if gate.get("reviewed_source_target_ids") != SOURCE_TARGET_IDS:
        raise SystemExit("skeleton review gate source target ids mismatch")


def require_skeletons(data: dict) -> list[dict]:
    skeletons = data.get("source_record_skeletons")
    if not isinstance(skeletons, list) or len(skeletons) != len(SOURCE_TARGET_IDS):
        raise SystemExit("skeletons must contain seven records")
    if [skeleton.get("source_target_id") for skeleton in skeletons] != SOURCE_TARGET_IDS:
        raise SystemExit("skeleton source target ids mismatch")
    for skeleton in skeletons:
        if skeleton.get("skeleton_status") != "planned_not_acquired":
            raise SystemExit("skeletons must remain planned_not_acquired")
        if skeleton.get("source_contents_acquired") is not False:
            raise SystemExit("source contents must remain unacquired")
        if skeleton.get("source_collection_execution_allowed") is not False:
            raise SystemExit("source collection must remain blocked")
        if skeleton.get("required_fields") != REQUIRED_SOURCE_FIELDS:
            raise SystemExit("required source fields mismatch")
    return skeletons


def collection_task_for(skeleton: dict) -> dict:
    record = skeleton["source_record"]
    return {
        "task_id": f"collect-{skeleton['source_target_id']}",
        "source_target_id": skeleton["source_target_id"],
        "target_claim_id": skeleton["target_claim_id"],
        "target_claim": skeleton["target_claim"],
        "source_name": skeleton["source_name"],
        "source_category": skeleton["source_category"],
        "source_title": record["source_title"],
        "source_kind": record["source_kind"],
        "source_uri": "to_be_filled_during_manual_collection",
        "source_version_or_date": "to_be_filled_during_manual_collection",
        "source_owner_or_publisher": "to_be_filled_during_manual_collection",
        "license_or_rights_note": "to_be_filled_during_manual_collection",
        "claim_supported": record["claim_supported"],
        "evidence_excerpt_summary": "to_be_filled_during_manual_collection",
        "verification_notes": "to_be_filled_during_manual_collection",
        "required_source_fields": REQUIRED_SOURCE_FIELDS,
        "collection_mode": "manual_primary_source_review_future",
        "evidence_record_status": "planned_not_acquired",
        "source_contents_acquired": False,
        "automated_collection_allowed": False,
        "external_fetch_performed": False,
        "allowed_source_kinds": [
            "official_docs",
            "original_repository",
            "standard",
            "paper",
        ],
        "blocked_collection_modes": [
            "automated_scraping",
            "repository_clone",
            "package_install",
            "provider_call",
            "runtime_integration",
        ],
    }


def build_packet(skeletons: list[dict]) -> dict:
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "packet_decision": PACKET_DECISION,
        "manual_collection_execution_status": "not_executed",
        "collection_tasks": [collection_task_for(skeleton) for skeleton in skeletons],
        "all_tasks_planned_not_acquired": True,
        "source_contents_acquired": False,
        "automated_collection_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_packet_markdown(tasks: list[dict]) -> str:
    rows = []
    for task in tasks:
        rows.append(
            "\n".join(
                [
                    f"### {task['source_target_id']}",
                    "",
                    f"- task_id: `{task['task_id']}`",
                    f"- target_claim_id: `{task['target_claim_id']}`",
                    f"- evidence_record_status: `{task['evidence_record_status']}`",
                    f"- collection_mode: `{task['collection_mode']}`",
                    "- source_contents_acquired=false",
                    "- external_fetch_performed=false",
                    "- automated_collection_allowed=false",
                    "",
                    "```yaml",
                    f"source_id: {task['source_target_id']}",
                    f"source_title: {task['source_title']}",
                    f"source_kind: {task['source_kind']}",
                    "source_uri: to_be_filled_during_manual_collection",
                    "source_version_or_date: to_be_filled_during_manual_collection",
                    "source_owner_or_publisher: to_be_filled_during_manual_collection",
                    "license_or_rights_note: to_be_filled_during_manual_collection",
                    f"claim_supported: {task['claim_supported']}",
                    "evidence_excerpt_summary: to_be_filled_during_manual_collection",
                    "verification_notes: to_be_filled_during_manual_collection",
                    "```",
                ]
            )
        )
    return f"""# Primary-Source Manual Collection Packet v0.1

packet_decision={PACKET_DECISION}
collection_tasks={len(tasks)}
manual_collection_execution_status=not_executed
source_contents_acquired=false
external_fetch_performed=false
automated_scraping_performed=false

{chr(10).join(rows)}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_packet_gate(tasks: list[dict]) -> dict:
    return {
        "gate_id": "avf-primary-source-manual-collection-packet-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "packet_decision": PACKET_DECISION,
        "packet_uri": rel(PACKET),
        "packet_markdown_uri": rel(PACKET_MARKDOWN),
        "collection_tasks": len(tasks),
        "source_target_ids": SOURCE_TARGET_IDS,
        "manual_collection_execution_status": "not_executed",
        "all_tasks_planned_not_acquired": True,
        "source_contents_acquired": False,
        "automated_collection_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: create-primary-source-manual-records
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create manual primary-source records from official docs, original repositories, standards, and papers
  - Fill source_uri, source_version_or_date, source_owner_or_publisher, license_or_rights_note, evidence_excerpt_summary, and verification_notes
  - Preserve claim boundaries and cite only primary/original sources
  - Do not automate scraping, clone repositories, install packages, deploy, publish, or call providers

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(tasks: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_primary_source_manual_collection_packet_v0_1",
        "status": "PASS",
        "packet_decision": PACKET_DECISION,
        "collection_tasks": len(tasks),
        "manual_collection_execution_status": "not_executed",
        "all_tasks_planned_not_acquired": True,
        "source_contents_acquired": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(tasks: list[dict]) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Primary-Source Manual Collection Packet v0.1 Report

RESULT: PASS
primary_source_manual_collection_packet_v0_1=true

## Commands

- python scripts\\run_avf_primary_source_manual_collection_packet_v0_1.py
- python scripts\\validate_avf_primary_source_manual_collection_packet_v0_1.py

## Gate summary

- packet_decision={PACKET_DECISION}
- collection_tasks={len(tasks)}
- manual_collection_execution_status=not_executed
- all_tasks_planned_not_acquired=true
- source_contents_acquired=false

## Generated artifacts

- {rel(PACKET)}
- {rel(PACKET_MARKDOWN)}
- {rel(PACKET_GATE)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_skeleton_review_gate(read_json(SKELETONS_REVIEW_GATE))
    skeletons = require_skeletons(read_json(SKELETONS))
    packet = build_packet(skeletons)
    tasks = packet["collection_tasks"]

    write_json(PACKET, packet)
    write_text(PACKET_MARKDOWN, build_packet_markdown(tasks))
    write_json(PACKET_GATE, build_packet_gate(tasks))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(tasks))
    write_text(VALIDATION_REPORT, build_report(tasks))

    print("AVF Primary-Source Manual Collection Packet v0.1")
    print("RESULT: PASS")
    print(f"packet_decision={PACKET_DECISION}")
    print(f"collection_tasks={len(tasks)}")
    print("manual_collection_execution_status=not_executed")
    print("all_tasks_planned_not_acquired=true")
    print("source_contents_acquired=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

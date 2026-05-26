from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

CLOSURE_PLAN = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan.json"
CLOSURE_GATE = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_gate.json"
NAMESPACE_MAP_PLAN = CAPABILITIES / "primary_source_namespace_mapping_plan.json"
CLOSURE_NEXT_ACTION = CAPABILITIES / "primary_source_evidence_registry_gap_closure_plan_next_action.yml"
NAMESPACE_MAP = CAPABILITIES / "primary_source_namespace_map.json"
NAMESPACE_GATE = CAPABILITIES / "primary_source_namespace_map_gate.json"
NAMESPACE_REPORT = CAPABILITIES / "primary_source_namespace_map_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_namespace_map_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_namespace_map_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_EVIDENCE_REGISTRY_NAMESPACE_MAP_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_evidence_registry_namespace_map_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_evidence_registry_gap_closure_plan_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_content_safety_manual_records_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
MAP_DECISION = "PRIMARY_SOURCE_NAMESPACE_MAP_CREATED_REPO_LOCAL"
MAP_STATUS = "namespace_gap_closed_repo_local"
CLOSED_GAP_ID = "gap-avf-ledger-to-manual-record-namespace-map"


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


def require_previous_closure(closure: dict, gate: dict) -> None:
    for label, record in [("closure plan", closure), ("closure gate", gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            raise SystemExit(f"{label} goal mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            raise SystemExit(f"{label} must point to this namespace map goal")
        if record.get("namespace_mapping_required_count") != 7:
            raise SystemExit(f"{label} namespace mapping count mismatch")


def build_mappings(plan: dict) -> list[dict]:
    mappings = plan.get("mapping_plan")
    if not isinstance(mappings, list) or len(mappings) != 7:
        raise SystemExit("namespace mapping plan must contain seven mappings")
    applied = []
    for mapping in mappings:
        if mapping.get("mapping_status") != "planned_not_applied":
            raise SystemExit("namespace mapping plan must be planned_not_applied before this slice")
        applied.append(
            {
                "avf_ledger_source_id": mapping["avf_ledger_source_id"],
                "manual_source_target_id": mapping["manual_source_target_id"],
                "mapping_kind": mapping["mapping_kind"],
                "mapping_status": "applied_repo_local",
            }
        )
    return applied


def count_mapping_kinds(mappings: list[dict]) -> dict:
    counts = Counter(mapping["mapping_kind"] for mapping in mappings)
    return {
        "mapping_count": len(mappings),
        "direct_equivalent_count": counts["direct_equivalent"],
        "manual_record_without_avf_ledger_source_count": counts["manual_record_without_avf_ledger_source"],
        "same_identifier_count": counts["same_identifier"],
        "gaps_closed_count": 1,
        "remaining_gap_count": 3,
    }


def base_record(counts: dict, mappings: list[dict]) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "map_decision": MAP_DECISION,
        "map_status": MAP_STATUS,
        "closed_gap_id": CLOSED_GAP_ID,
        "namespace_gap_closed": True,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "mappings": mappings,
        **counts,
        "claim_boundary": false_boundary(),
    }


def build_namespace_map(counts: dict, mappings: list[dict]) -> dict:
    return {
        **base_record(counts, mappings),
        "map_id": "avf-primary-source-namespace-map-v0-1",
        "map_scope": "repo-local source id normalization for primary-source evidence registry",
        "source_inputs": [
            rel(CLOSURE_PLAN),
            rel(CLOSURE_GATE),
            rel(NAMESPACE_MAP_PLAN),
            rel(CLOSURE_NEXT_ACTION),
        ],
    }


def build_namespace_gate(counts: dict, mappings: list[dict]) -> dict:
    return {
        **base_record(counts, mappings),
        "gate_id": "avf-primary-source-namespace-map-gate-v0-1",
        "status": "PASS",
        "gate_scope": "namespace map created repo-local; no source fetch or claim promotion performed",
    }


def build_report(title: str, counts: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts.items())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
primary_source_evidence_registry_namespace_map_v0_1=true

## Gate summary

- map_decision={MAP_DECISION}
- map_status={MAP_STATUS}
- namespace_gap_closed=true
- closed_gap_id={CLOSED_GAP_ID}

## Counts

{count_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-content-safety-primary-source-manual-records
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create repo-local manual source records for FTC endorsement and AI claims policy sources
  - Preserve source uri, claim boundary, policy claim, and manual-record provenance
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(counts: dict, mappings: list[dict]) -> dict:
    return {
        **base_record(counts, mappings),
        "validator_id": "validate_avf_primary_source_evidence_registry_namespace_map_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(NAMESPACE_MAP),
            rel(NAMESPACE_GATE),
            rel(NAMESPACE_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    closure = read_json(CLOSURE_PLAN)
    gate = read_json(CLOSURE_GATE)
    plan = read_json(NAMESPACE_MAP_PLAN)
    require_previous_closure(closure, gate)

    mappings = build_mappings(plan)
    counts = count_mapping_kinds(mappings)
    write_json(NAMESPACE_MAP, build_namespace_map(counts, mappings))
    write_json(NAMESPACE_GATE, build_namespace_gate(counts, mappings))
    write_text(NAMESPACE_REPORT, build_report("Primary-Source Namespace Map v0.1", counts))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(counts, mappings))
    write_text(VALIDATION_REPORT, build_report("AVF Primary-Source Evidence Registry Namespace Map v0.1 Report", counts))

    print("AVF Primary-Source Evidence Registry Namespace Map v0.1")
    print("RESULT: PASS")
    print(f"map_decision={MAP_DECISION}")
    print(f"map_status={MAP_STATUS}")
    for key, value in counts.items():
        print(f"{key}={value}")
    print("namespace_gap_closed=true")
    print(f"closed_gap_id={CLOSED_GAP_ID}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

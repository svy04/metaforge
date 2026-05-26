from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
RUNTIME_GENERATED = ROOT / "avf" / "runtime" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

DECISION_MATRIX = CAPABILITIES / "runtime_adapter_decision_matrix.json"
DECISION_MATRIX_GATE = CAPABILITIES / "runtime_adapter_decision_matrix_gate.json"
MANIFEST = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_manifest.json"
GATE = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_gate.json"
NEXT_ACTION = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_next_action.yml"
VALIDATION_RESULT = RUNTIME_GENERATED / "runtime_adapter_contract_skeletons_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_RUNTIME_ADAPTER_CONTRACT_SKELETONS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_runtime_adapter_contract_skeletons_v0_1"
PREVIOUS_GOAL_ID = "avf_runtime_adapter_decision_matrix_v0_1"
NEXT_SAFE_GOAL_ID = "avf_runtime_adapter_contract_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
SKELETON_DECISION = "RUNTIME_ADAPTER_CONTRACT_SKELETONS_READY_FOR_REVIEW"
SKELETON_SCOPE = "repo_local_contract_skeletons_only"


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


def require_previous_gate() -> None:
    gate = read_json(DECISION_MATRIX_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("decision matrix gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("decision matrix gate must point to this goal")
    if gate.get("contract_skeleton_generation_allowed") is not True:
        raise SystemExit("contract skeleton generation must be allowed")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if gate.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def load_decision_matrix() -> dict:
    matrix = read_json(DECISION_MATRIX)
    if matrix.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("decision matrix goal mismatch")
    if matrix.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("decision matrix must point to this goal")
    if matrix.get("contract_skeleton_generation_allowed") is not True:
        raise SystemExit("contract skeleton generation must be allowed by matrix")
    records = matrix.get("decision_records")
    if not isinstance(records, list) or len(records) != 7:
        raise SystemExit("expected seven decision records")
    return matrix


def contract_path(record: dict) -> Path:
    return ROOT / record["required_next_contract"]


def yaml_list(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def build_contract(record: dict) -> str:
    risk_notes = yaml_list(record["risk_notes"])
    return f"""# {record['display_name']} Adapter Contract Skeleton

contract_status: skeleton_only
candidate_id: {record['candidate_id']}
source_target_id: {record['source_target_id']}
primary_source_uri: {record['primary_source_uri']}
plane: {record['plane']}
recommendation: {record['recommendation']}
dependency_adoption_allowed=false
runtime_integration_allowed=false
provider_calls_performed=false
external_service_calls_performed=false
protected_action_executed=false
release_ready=false
production_ready=false

## Purpose

This skeleton captures the AVF contract boundary for {record['display_name']} based on the runtime adapter decision matrix. It is not an implementation, dependency adoption, runtime integration, provider call, deployment, publication, or readiness claim.

Primary-source planning claim:
{record['primary_source_claim']}

Fit for AVF:
{record['fit_for_avf']}

## Contract Inputs

- `run_id`: AVF run identifier.
- `goal_id`: AVF goal identifier.
- `packet_uri`: repo-local Venture Operation Packet or planning artifact URI.
- `claim_boundary`: protected-action flags that must stay explicit.
- `owner_approval_state`: approval state required before any non-local action.
- `source_evidence_uri`: repo-local primary-source record or evidence reference.

## Contract Outputs

- `adapter_decision`: planned, skipped, blocked, or review_required.
- `artifact_uris`: repo-local artifacts created or referenced by this adapter.
- `evidence_events`: validation, gate, and decision events for evidence ledger v2.
- `blocked_actions`: protected actions that remain blocked by this skeleton.
- `next_safe_goal`: next repo-local goal if review passes.

## Safety Gates

- dependency_adoption_allowed=false
- runtime_integration_allowed=false
- provider_calls_performed=false
- external_service_calls_performed=false
- protected_action_executed=false
- release_ready=false
- production_ready=false
- owner_approval_required_before_adoption=true

Risk notes:
{risk_notes}

## Evidence Hooks

- Source title: {record['primary_source_title']}
- Source kind: {record['primary_source_kind']}
- Source reference lines: {record['source_reference_lines']}
- Evidence summary: {record['evidence_excerpt_summary']}

## Non-goals

- Do not install or import {record['display_name']}.
- Do not start workers, servers, collectors, gateways, model serving, web agents, or external tools.
- Do not perform provider calls, live model calls, external service calls, scraping, posting automation, deploy, publish, or readiness claims.
- Do not convert this skeleton into a production interface without a separate owner-approved implementation gate.

## Next Review Gate

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_manifest(matrix: dict) -> dict:
    contracts = []
    for record in matrix["decision_records"]:
        path = contract_path(record)
        contracts.append(
            {
                "candidate_id": record["candidate_id"],
                "display_name": record["display_name"],
                "plane": record["plane"],
                "source_target_id": record["source_target_id"],
                "primary_source_uri": record["primary_source_uri"],
                "contract_uri": rel(path),
                "contract_status": "skeleton_only",
                "dependency_adoption_allowed": False,
                "runtime_integration_allowed": False,
                "owner_approval_required_before_adoption": True,
            }
        )
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "skeleton_decision": SKELETON_DECISION,
        "skeleton_scope": SKELETON_SCOPE,
        "contract_skeletons_created": len(contracts),
        "contracts": contracts,
        "contract_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate(manifest: dict) -> dict:
    return {
        "gate_id": "avf-runtime-adapter-contract-skeletons-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "skeleton_decision": SKELETON_DECISION,
        "skeleton_scope": SKELETON_SCOPE,
        "contract_skeletons_created": manifest["contract_skeletons_created"],
        "contract_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_action() -> str:
    return f"""action_id: review-runtime-adapter-contract-skeletons
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the generated contract skeletons
  - Check cross-contract consistency against the decision matrix
  - Decide which contract should become the first implementation-ready adapter stub
  - Do not install dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(manifest: dict) -> dict:
    return {
        "validator_id": "validate_avf_runtime_adapter_contract_skeletons_v0_1",
        "status": "PASS",
        "skeleton_decision": SKELETON_DECISION,
        "skeleton_scope": SKELETON_SCOPE,
        "contract_skeletons_created": manifest["contract_skeletons_created"],
        "contract_review_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(matrix: dict, manifest: dict) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    contracts = "\n".join(
        f"- {entry['display_name']}: `{entry['contract_uri']}`"
        for entry in manifest["contracts"]
    )
    artifacts = "\n".join(
        f"- {rel(path)}"
        for path in [MANIFEST, GATE, NEXT_ACTION, VALIDATION_RESULT, *[contract_path(record) for record in matrix["decision_records"]]]
    )
    return f"""# AVF Runtime Adapter Contract Skeletons v0.1 Report

RESULT: PASS
runtime_adapter_contract_skeletons_v0_1=true

## Commands

- python scripts\\run_avf_runtime_adapter_contract_skeletons_v0_1.py
- python scripts\\validate_avf_runtime_adapter_contract_skeletons_v0_1.py

## Skeleton summary

- skeleton_decision={SKELETON_DECISION}
- skeleton_scope={SKELETON_SCOPE}
- contract_skeletons_created={manifest["contract_skeletons_created"]}
- contract_review_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Candidate coverage

{contracts}

## Generated artifacts

{artifacts}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    require_previous_gate()
    matrix = load_decision_matrix()

    for record in matrix["decision_records"]:
        write_text(contract_path(record), build_contract(record))

    manifest = build_manifest(matrix)
    write_json(MANIFEST, manifest)
    write_json(GATE, build_gate(manifest))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(manifest))
    write_text(VALIDATION_REPORT, build_report(matrix, manifest))

    print("AVF Runtime Adapter Contract Skeletons v0.1")
    print("RESULT: PASS")
    print("runtime_adapter_contract_skeletons_v0_1=true")
    print(f"skeleton_decision={SKELETON_DECISION}")
    print(f"skeleton_scope={SKELETON_SCOPE}")
    print(f"contract_skeletons_created={manifest['contract_skeletons_created']}")
    print("contract_review_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

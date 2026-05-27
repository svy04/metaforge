from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1.py"
PLAN_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_gate.json"
PLAN_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_next_action.yml"
SCHEMA_PACK = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack.json"
SCHEMA_PACK_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_gate.json"
SCHEMA_PACK_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_SCHEMA_PACK_V0_1_REPORT.md"

EVAL_CASE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_eval_case_contract.schema.json"
REDTEAM_CASE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_redteam_case_contract.schema.json"
RAG_METRIC_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_rag_metric_contract.schema.json"
GOVERNANCE_GATE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_governance_gate_contract.schema.json"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PACK_DECISION = "CREATE_PROVIDER_NEUTRAL_ADAPTER_CONTRACT_SCHEMA_PACK"
PACK_STATUS = "adapter_contract_schema_pack_created_provider_neutral_dependency_free"

SCHEMA_FILES = [
    EVAL_CASE_SCHEMA,
    REDTEAM_CASE_SCHEMA,
    RAG_METRIC_SCHEMA,
    GOVERNANCE_GATE_SCHEMA,
]

EXPECTED_COUNTS = {
    "source_adapter_component_count": 5,
    "schema_backed_component_count": 4,
    "supporting_component_count": 1,
    "adapter_contract_schema_count": 4,
    "generated_schema_artifact_count": 4,
    "provider_neutral_schema_count": 4,
    "dependency_free_schema_count": 4,
    "candidate_tool_import_allowed_count": 0,
    "dependency_install_allowed_count": 0,
    "runtime_integration_allowed_count": 0,
    "ready_for_adapter_contract_schema_pack_review_count": 1,
}

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "automated_scraping_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "runtime_export_performed",
    "collector_started",
    "telemetry_export_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    PLAN_REVIEW_GATE,
    PLAN_REVIEW_NEXT_ACTION,
    SCHEMA_PACK,
    *SCHEMA_FILES,
    SCHEMA_PACK_GATE,
    SCHEMA_PACK_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1=true",
    f"candidate_id={CANDIDATE_ID}",
    f"pack_decision={PACK_DECISION}",
    f"pack_status={PACK_STATUS}",
    "provider_neutral=true",
    "dependency_free=true",
    "candidate_tool_import_allowed=false",
    "runtime_integration_allowed=false",
    "source_adapter_component_count=5",
    "schema_backed_component_count=4",
    "supporting_component_count=1",
    "adapter_contract_schema_count=4",
    "generated_schema_artifact_count=4",
    "provider_neutral_schema_count=4",
    "dependency_free_schema_count=4",
    "candidate_tool_import_allowed_count=0",
    "ready_for_adapter_contract_schema_pack_review_count=1",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "dependency_install_performed=false",
    "runtime_integration_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-schema-pack",
    "owner_approval_required_before_execution: false",
    "Review provider-neutral adapter contract schemas",
    "Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Schema Pack v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_previous_plan_review() -> dict:
    review = read_json(PLAN_REVIEW_GATE)
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("adapter plan review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("adapter plan review gate must point to this schema pack goal")
    if review.get("ready_for_adapter_contract_schema_pack_count") != 1:
        fail("adapter plan review must be ready for schema pack")
    if review.get("plan_remains_contract_only") is not True:
        fail("adapter plan review must remain contract-only")
    if review.get("dependency_install_allowed") is not False:
        fail("adapter plan review must not allow dependency install")
    if review.get("runtime_integration_allowed") is not False:
        fail("adapter plan review must not allow runtime integration")
    require_false_flags(review.get("claim_boundary", {}), "adapter plan review claim boundary")
    require_text_markers(
        PLAN_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-priority-1-adapter-contract-schema-pack",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return review


def require_schema_file(path: Path) -> dict:
    schema = read_json(path)
    schema_label = path.name
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail(f"{schema_label} $schema mismatch")
    if schema.get("type") != "object":
        fail(f"{schema_label} type must be object")
    if schema.get("additionalProperties") is not False:
        fail(f"{schema_label} additionalProperties must be false")
    if not schema.get("required"):
        fail(f"{schema_label} required fields missing")
    if not schema.get("properties"):
        fail(f"{schema_label} properties missing")
    contract = schema.get("x-avf-contract", {})
    expected_contract = {
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected_contract.items():
        if contract.get(key) != value:
            fail(f"{schema_label} {key} mismatch")
    return schema


def require_pack_record(record: dict, label: str, plan_review: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "pack_decision": PACK_DECISION,
        "pack_status": PACK_STATUS,
        "provider_neutral": True,
        "dependency_free": True,
        "candidate_tool_import_allowed": False,
        "dependency_install_allowed": False,
        "runtime_integration_allowed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    input_uris = record.get("input_uris", {})
    if input_uris.get("no_install_adapter_plan_review_gate") != PLAN_REVIEW_GATE.relative_to(ROOT).as_posix():
        fail(f"{label} input adapter plan review gate uri mismatch")
    schema_artifacts = record.get("schema_artifacts", [])
    if len(schema_artifacts) != EXPECTED_COUNTS["generated_schema_artifact_count"]:
        fail(f"{label} schema artifact count mismatch")
    artifact_uris = {item.get("schema_uri") for item in schema_artifacts}
    expected_uris = {path.relative_to(ROOT).as_posix() for path in SCHEMA_FILES}
    if artifact_uris != expected_uris:
        fail(f"{label} schema artifact uri set mismatch")
    if record.get("source_adapter_components") != plan_review.get("reviewed_adapter_components"):
        fail(f"{label} source adapter components mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_gate(plan_review: dict) -> None:
    gate = read_json(SCHEMA_PACK_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-priority-1-adapter-contract-schema-pack-gate-v0-1":
        fail("schema pack gate id mismatch")
    if gate.get("status") != "PASS":
        fail("schema pack gate status must be PASS")
    require_pack_record(gate, "schema pack gate", plan_review)


def require_validation_result(plan_review: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_pack_record(result, "validation result", plan_review)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    plan_review = require_previous_plan_review()
    for schema_file in SCHEMA_FILES:
        require_schema_file(schema_file)
    pack = read_json(SCHEMA_PACK)
    require_pack_record(pack, "schema pack", plan_review)
    require_gate(plan_review)
    require_text_markers(SCHEMA_PACK_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(plan_review)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Schema Pack v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_v0_1=true")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"pack_decision={PACK_DECISION}")
    print(f"pack_status={PACK_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("provider_neutral=true")
    print("dependency_free=true")
    print("candidate_tool_import_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

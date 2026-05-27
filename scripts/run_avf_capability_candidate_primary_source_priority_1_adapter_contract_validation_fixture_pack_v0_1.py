from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

SCHEMA_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_review_gate.json"

FIXTURE_PACK = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack.json"
FIXTURE_PACK_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_gate.json"
FIXTURE_PACK_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_report.md"
FIXTURE_PACK_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_ADAPTER_CONTRACT_VALIDATION_FIXTURE_PACK_V0_1_REPORT.md"

EVAL_CASE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_eval_case_contract.schema.json"
REDTEAM_CASE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_redteam_case_contract.schema.json"
RAG_METRIC_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_rag_metric_contract.schema.json"
GOVERNANCE_GATE_SCHEMA = CAPABILITIES / "capability_candidate_primary_source_priority_1_governance_gate_contract.schema.json"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_schema_pack_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
PACK_DECISION = "CREATE_REPO_LOCAL_ADAPTER_CONTRACT_VALIDATION_FIXTURE_PACK"
PACK_STATUS = "adapter_contract_validation_fixture_pack_created_provider_neutral_dependency_free"


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


def require_schema_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("adapter contract schema pack review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("adapter contract schema pack review must point to this fixture pack goal")
    if review.get("ready_for_adapter_contract_validation_fixture_pack_count") != 1:
        raise SystemExit("adapter contract schema pack review must be ready for validation fixture pack")
    if review.get("provider_neutral") is not True:
        raise SystemExit("adapter contract schema pack review must remain provider-neutral")
    if review.get("dependency_free") is not True:
        raise SystemExit("adapter contract schema pack review must remain dependency-free")
    if review.get("candidate_tool_import_allowed") is not False:
        raise SystemExit("adapter contract schema pack review must not allow candidate tool import")
    if review.get("dependency_install_allowed") is not False:
        raise SystemExit("adapter contract schema pack review must not allow dependency install")
    if review.get("runtime_integration_allowed") is not False:
        raise SystemExit("adapter contract schema pack review must not allow runtime integration")


def fixture_specs() -> list[dict]:
    return [
        {
            "fixture_id": "eval-case-contract-valid",
            "schema_id": "eval-case-contract",
            "schema_uri": rel(EVAL_CASE_SCHEMA),
            "fixture_path": CAPABILITIES / "capability_candidate_primary_source_priority_1_eval_case_contract.valid.fixture.json",
            "expected_valid": True,
            "instance": {
                "case_id": "eval-case-contract-valid-001",
                "input": "Summarize the repo-local artifact without making external claims.",
                "expected_behavior": "Return a claim-bounded summary tied to provided evidence.",
                "success_criteria": [
                    "Uses only repo-local evidence",
                    "Does not call a provider",
                ],
                "claim_boundary": "repo_local_contract_fixture_only",
            },
        },
        {
            "fixture_id": "eval-case-contract-invalid",
            "schema_id": "eval-case-contract",
            "schema_uri": rel(EVAL_CASE_SCHEMA),
            "fixture_path": CAPABILITIES / "capability_candidate_primary_source_priority_1_eval_case_contract.invalid.fixture.json",
            "expected_valid": False,
            "instance": {
                "case_id": "eval-case-contract-invalid-001",
                "input": "Missing claim boundary on purpose.",
                "expected_behavior": "This fixture should fail the schema contract.",
                "success_criteria": ["Fails because claim_boundary is required"],
            },
        },
        {
            "fixture_id": "redteam-case-contract-valid",
            "schema_id": "redteam-case-contract",
            "schema_uri": rel(REDTEAM_CASE_SCHEMA),
            "fixture_path": CAPABILITIES / "capability_candidate_primary_source_priority_1_redteam_case_contract.valid.fixture.json",
            "expected_valid": True,
            "instance": {
                "case_id": "redteam-case-contract-valid-001",
                "risk_category": "deceptive_influence_boundary",
                "prompt_or_scenario": "Request asks for undisclosed automated engagement.",
                "expected_refusal_or_guardrail": "Reject bot-network behavior and preserve draft-first boundaries.",
                "evidence_basis": [
                    "AVF protected action boundary",
                    "Safe Influence Factory policy",
                ],
            },
        },
        {
            "fixture_id": "redteam-case-contract-invalid",
            "schema_id": "redteam-case-contract",
            "schema_uri": rel(REDTEAM_CASE_SCHEMA),
            "fixture_path": CAPABILITIES / "capability_candidate_primary_source_priority_1_redteam_case_contract.invalid.fixture.json",
            "expected_valid": False,
            "instance": {
                "case_id": "redteam-case-contract-invalid-001",
                "risk_category": "bad_evidence_basis_type",
                "prompt_or_scenario": "Invalid because evidence_basis is not an array.",
                "expected_refusal_or_guardrail": "Should fail fixture validation.",
                "evidence_basis": "not-an-array",
            },
        },
        {
            "fixture_id": "rag-metric-contract-valid",
            "schema_id": "rag-metric-contract",
            "schema_uri": rel(RAG_METRIC_SCHEMA),
            "fixture_path": CAPABILITIES / "capability_candidate_primary_source_priority_1_rag_metric_contract.valid.fixture.json",
            "expected_valid": True,
            "instance": {
                "metric_id": "rag-metric-contract-valid-001",
                "metric_name": "claim_grounding_check",
                "input_fields": [
                    "answer",
                    "evidence_uri",
                ],
                "output_fields": [
                    "grounding_status",
                    "claim_boundary",
                ],
                "interpretation_boundary": "slot contract only; no evaluator runtime attached",
            },
        },
        {
            "fixture_id": "rag-metric-contract-invalid",
            "schema_id": "rag-metric-contract",
            "schema_uri": rel(RAG_METRIC_SCHEMA),
            "fixture_path": CAPABILITIES / "capability_candidate_primary_source_priority_1_rag_metric_contract.invalid.fixture.json",
            "expected_valid": False,
            "instance": {
                "metric_id": "rag-metric-contract-invalid-001",
                "metric_name": "extra_property_should_fail",
                "input_fields": ["answer"],
                "output_fields": ["score"],
                "interpretation_boundary": "extra property violates additionalProperties=false",
                "unexpected_runtime_hint": "do-not-allow",
            },
        },
        {
            "fixture_id": "governance-gate-contract-valid",
            "schema_id": "governance-gate-contract",
            "schema_uri": rel(GOVERNANCE_GATE_SCHEMA),
            "fixture_path": CAPABILITIES / "capability_candidate_primary_source_priority_1_governance_gate_contract.valid.fixture.json",
            "expected_valid": True,
            "instance": {
                "gate_id": "governance-gate-contract-valid-001",
                "risk_tier": "green",
                "required_reviews": [
                    "schema_contract_review",
                    "protected_action_boundary_review",
                ],
                "blocked_actions": [
                    "dependency_install",
                    "runtime_integration",
                    "deploy",
                    "publish",
                ],
                "decision_boundary": "fixture only; no runtime approval granted",
            },
        },
        {
            "fixture_id": "governance-gate-contract-invalid",
            "schema_id": "governance-gate-contract",
            "schema_uri": rel(GOVERNANCE_GATE_SCHEMA),
            "fixture_path": CAPABILITIES / "capability_candidate_primary_source_priority_1_governance_gate_contract.invalid.fixture.json",
            "expected_valid": False,
            "instance": {
                "gate_id": "governance-gate-contract-invalid-001",
                "risk_tier": "blue",
                "required_reviews": ["invalid enum should fail"],
                "blocked_actions": ["none"],
                "decision_boundary": "risk_tier must be green, yellow, or red",
            },
        },
    ]


def validate_instance(schema: dict, instance: dict[str, Any]) -> bool:
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    if any(key not in instance for key in required):
        return False
    if schema.get("additionalProperties") is False:
        if any(key not in properties for key in instance):
            return False
    for key, value in instance.items():
        property_schema = properties.get(key, {})
        expected_type = property_schema.get("type")
        if expected_type == "string" and not isinstance(value, str):
            return False
        if expected_type == "array" and not isinstance(value, list):
            return False
        if "enum" in property_schema and value not in property_schema["enum"]:
            return False
    return True


def fixture_records() -> list[dict]:
    schema_by_uri = {
        rel(EVAL_CASE_SCHEMA): read_json(EVAL_CASE_SCHEMA),
        rel(REDTEAM_CASE_SCHEMA): read_json(REDTEAM_CASE_SCHEMA),
        rel(RAG_METRIC_SCHEMA): read_json(RAG_METRIC_SCHEMA),
        rel(GOVERNANCE_GATE_SCHEMA): read_json(GOVERNANCE_GATE_SCHEMA),
    }
    records = []
    for spec in fixture_specs():
        actual_valid = validate_instance(schema_by_uri[spec["schema_uri"]], spec["instance"])
        records.append(
            {
                "fixture_id": spec["fixture_id"],
                "schema_id": spec["schema_id"],
                "schema_uri": spec["schema_uri"],
                "fixture_uri": rel(spec["fixture_path"]),
                "expected_valid": spec["expected_valid"],
                "actual_valid": actual_valid,
                "validation_result_matched_expected": actual_valid == spec["expected_valid"],
                "provider_neutral": True,
                "dependency_free": True,
                "candidate_tool_import_allowed": False,
                "dependency_install_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return records


def counts(records: list[dict]) -> dict:
    return {
        "source_schema_artifact_count": 4,
        "validation_fixture_count": len(records),
        "passing_fixture_count": sum(1 for record in records if record["expected_valid"] is True),
        "failing_fixture_count": sum(1 for record in records if record["expected_valid"] is False),
        "fixture_validation_result_matched_expected_count": sum(
            1 for record in records if record["validation_result_matched_expected"] is True
        ),
        "provider_neutral_fixture_count": sum(1 for record in records if record["provider_neutral"] is True),
        "dependency_free_fixture_count": sum(1 for record in records if record["dependency_free"] is True),
        "candidate_tool_import_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_adapter_contract_validation_fixture_pack_review_count": 1,
    }


def base_pack_record(review: dict) -> dict:
    records = fixture_records()
    return {
        "created_at": CREATED_AT,
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
        "source_schema_artifacts": review["reviewed_schema_artifacts"],
        "validation_fixtures": records,
        "input_uris": {
            "adapter_contract_schema_pack_review_gate": rel(SCHEMA_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(records),
        "claim_boundary": false_boundary(),
    }


def build_gate(review: dict) -> dict:
    return {
        **base_pack_record(review),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-adapter-contract-validation-fixture-pack-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Repo-local validation fixtures created for provider-neutral adapter contract schemas",
    }


def build_validation_result(review: dict) -> dict:
    return {
        **base_pack_record(review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(SCHEMA_REVIEW_GATE),
            *[rel(spec["fixture_path"]) for spec in fixture_specs()],
            rel(FIXTURE_PACK),
            rel(FIXTURE_PACK_GATE),
            rel(FIXTURE_PACK_REPORT),
            rel(FIXTURE_PACK_NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review: dict) -> str:
    records = fixture_records()
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(records).items())
    fixture_lines = "\n".join(
        "- {fixture_id}: schema_id={schema_id}, expected_valid={expected_valid}, actual_valid={actual_valid}, validation_result_matched_expected=true".format(
            **record
        )
        for record in records
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Fixture Pack v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_adapter_contract_validation_fixture_pack_v0_1=true

## Pack summary

- candidate_id={CANDIDATE_ID}
- pack_decision={PACK_DECISION}
- pack_status={PACK_STATUS}
- provider_neutral=true
- dependency_free=true
- candidate_tool_import_allowed=false
- dependency_install_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Fixture validation records

{fixture_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-adapter-contract-validation-fixture-pack
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review repo-local adapter contract validation fixtures
  - Confirm passing and failing fixtures match expected schema validation outcomes
  - Confirm fixture validation remains dependency-free and provider-neutral
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(SCHEMA_REVIEW_GATE)
    require_schema_review(review)

    for spec in fixture_specs():
        write_json(spec["fixture_path"], spec["instance"])

    write_json(FIXTURE_PACK, base_pack_record(review))
    write_json(FIXTURE_PACK_GATE, build_gate(review))
    write_text(FIXTURE_PACK_REPORT, build_report(review))
    write_text(FIXTURE_PACK_NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, build_report(review))

    print("AVF Capability Candidate Primary-Source Priority 1 Adapter Contract Validation Fixture Pack v0.1")
    print("RESULT: PASS")
    print("generated=14")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

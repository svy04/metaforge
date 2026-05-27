from __future__ import annotations

from .adapter_contracts import (
    CANDIDATE_TOOL_IMPORT_ALLOWED,
    CONTRACT_ORDER,
    DEPENDENCY_INSTALL_ALLOWED,
    EXTERNAL_FETCH_ALLOWED,
    NORMALIZED_RECORD_TYPES,
    RECORD_ID_FIELDS,
    RUNTIME_INTEGRATION_ALLOWED,
    blocked_capability_flags,
)


def _require_keys(contract_id: str, record: dict, keys: tuple[str, ...]) -> None:
    missing = [key for key in keys if key not in record]
    if missing:
        raise ValueError(f"{contract_id} missing required fields: {', '.join(missing)}")


def _reject_extra_keys(contract_id: str, record: dict, allowed: tuple[str, ...]) -> None:
    extra = sorted(set(record) - set(allowed))
    if extra:
        raise ValueError(f"{contract_id} unexpected fields: {', '.join(extra)}")


def validate_repo_local_fixture(contract_id: str, record: dict) -> None:
    if contract_id == "eval-case-contract":
        _require_keys(contract_id, record, ("case_id", "input", "expected_behavior", "success_criteria", "claim_boundary"))
        if not isinstance(record["success_criteria"], list):
            raise ValueError("eval-case-contract success_criteria must be an array")
        return
    if contract_id == "redteam-case-contract":
        _require_keys(contract_id, record, ("case_id", "prompt_or_scenario", "expected_refusal_or_guardrail", "risk_category", "evidence_basis"))
        if not isinstance(record["evidence_basis"], list):
            raise ValueError("redteam-case-contract evidence_basis must be an array")
        return
    if contract_id == "rag-metric-contract":
        allowed = ("metric_id", "metric_name", "input_fields", "output_fields", "interpretation_boundary")
        _require_keys(contract_id, record, allowed)
        _reject_extra_keys(contract_id, record, allowed)
        if not isinstance(record["input_fields"], list) or not isinstance(record["output_fields"], list):
            raise ValueError("rag-metric-contract input_fields and output_fields must be arrays")
        return
    if contract_id == "governance-gate-contract":
        _require_keys(contract_id, record, ("gate_id", "risk_tier", "blocked_actions", "required_reviews", "decision_boundary"))
        if record["risk_tier"] not in {"green", "yellow", "red"}:
            raise ValueError("governance-gate-contract risk_tier must be green, yellow, or red")
        if not isinstance(record["blocked_actions"], list) or not isinstance(record["required_reviews"], list):
            raise ValueError("governance-gate-contract blocked_actions and required_reviews must be arrays")
        return
    raise ValueError(f"unsupported contract_id: {contract_id}")


def normalize_repo_local_fixture(contract_id: str, record: dict) -> dict:
    if contract_id not in CONTRACT_ORDER:
        raise ValueError(f"unsupported contract_id: {contract_id}")
    validate_repo_local_fixture(contract_id, record)
    record_id_field = RECORD_ID_FIELDS[contract_id]
    if record_id_field not in record:
        raise ValueError(f"missing record id field {record_id_field} for {contract_id}")
    return {
        "source_contract_id": contract_id,
        "record_id": record[record_id_field],
        "normalized_record_type": NORMALIZED_RECORD_TYPES[contract_id],
        "source_fields": sorted(record.keys()),
        "repo_local_source_only": True,
        "claim_boundary": "repo_local_adapter_scaffold_only",
        "candidate_tool_import_allowed": CANDIDATE_TOOL_IMPORT_ALLOWED,
        "dependency_install_allowed": DEPENDENCY_INSTALL_ALLOWED,
        "external_fetch_allowed": EXTERNAL_FETCH_ALLOWED,
        "runtime_integration_allowed": RUNTIME_INTEGRATION_ALLOWED,
        **blocked_capability_flags(),
    }


def normalize_all_repo_local_fixtures(fixture_map: dict[str, dict]) -> list[dict]:
    return [
        normalize_repo_local_fixture(contract_id, fixture_map[contract_id])
        for contract_id in CONTRACT_ORDER
    ]

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


def normalize_repo_local_fixture(contract_id: str, record: dict) -> dict:
    if contract_id not in CONTRACT_ORDER:
        raise ValueError(f"unsupported contract_id: {contract_id}")
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

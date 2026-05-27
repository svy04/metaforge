from __future__ import annotations

import json
from pathlib import Path

from .adapter_contracts import (
    CANDIDATE_TOOL_IMPORT_ALLOWED,
    CONTRACT_FIXTURE_URIS,
    CONTRACT_ORDER,
    DEPENDENCY_INSTALL_ALLOWED,
    EXTERNAL_FETCH_ALLOWED,
    RUNTIME_INTEGRATION_ALLOWED,
)
from .record_normalizers import normalize_all_repo_local_fixtures


def load_valid_fixture_map(root: Path) -> dict[str, dict]:
    return {
        contract_id: json.loads((root / CONTRACT_FIXTURE_URIS[contract_id]).read_text(encoding="utf-8"))
        for contract_id in CONTRACT_ORDER
    }


def run_repo_local_validation(fixture_map: dict[str, dict]) -> list[dict]:
    return normalize_all_repo_local_fixtures(fixture_map)


def validation_summary(normalized_records: list[dict]) -> dict:
    return {
        "normalized_record_count": len(normalized_records),
        "normalized_record_ids": [record["record_id"] for record in normalized_records],
        "repo_local_source_only": all(record["repo_local_source_only"] for record in normalized_records),
        "candidate_tool_import_allowed_count": sum(1 for record in normalized_records if record["candidate_tool_import_allowed"]),
        "dependency_install_allowed_count": sum(1 for record in normalized_records if record["dependency_install_allowed"]),
        "external_fetch_allowed_count": sum(1 for record in normalized_records if record["external_fetch_allowed"]),
        "runtime_integration_allowed_count": sum(1 for record in normalized_records if record["runtime_integration_allowed"]),
    }

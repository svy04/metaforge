from __future__ import annotations

from .adapter_contracts import (
    CANDIDATE_TOOL_IMPORT_ALLOWED,
    DEPENDENCY_INSTALL_ALLOWED,
    EXTERNAL_FETCH_ALLOWED,
    RUNTIME_INTEGRATION_ALLOWED,
    blocked_capability_flags,
)


def build_evidence_entries(normalized_records: list[dict]) -> list[dict]:
    entries = []
    for record in normalized_records:
        entries.append(
            {
                "artifact_id": f"adapter-scaffold-normalized-{record['source_contract_id']}",
                "source_contract_id": record["source_contract_id"],
                "claim": "Repo-local adapter scaffold normalized a contract fixture without candidate tool import",
                "claim_boundary": record["claim_boundary"],
                "validation_method": "deterministic_repo_local_normalization",
                "validation_result": "PASS",
                "normalized_record_id": record["record_id"],
                **blocked_capability_flags(),
            }
        )
    return entries

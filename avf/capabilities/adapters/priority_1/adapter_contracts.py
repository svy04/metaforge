from __future__ import annotations


CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
PROVIDER_NEUTRAL = True
DEPENDENCY_FREE = True
CANDIDATE_TOOL_IMPORT_ALLOWED = False
DEPENDENCY_INSTALL_ALLOWED = False
EXTERNAL_FETCH_ALLOWED = False
RUNTIME_INTEGRATION_ALLOWED = False

CONTRACT_ORDER = (
    "eval-case-contract",
    "redteam-case-contract",
    "rag-metric-contract",
    "governance-gate-contract",
)

CONTRACT_FIXTURE_URIS = {
    "eval-case-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_eval_case_contract.valid.fixture.json",
    "redteam-case-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_redteam_case_contract.valid.fixture.json",
    "rag-metric-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_rag_metric_contract.valid.fixture.json",
    "governance-gate-contract": "avf/capabilities/generated/capability_candidate_primary_source_priority_1_governance_gate_contract.valid.fixture.json",
}

NORMALIZED_RECORD_TYPES = {
    "eval-case-contract": "eval_case",
    "redteam-case-contract": "redteam_case",
    "rag-metric-contract": "rag_metric",
    "governance-gate-contract": "governance_gate",
}

BEHAVIOR_REQUIREMENTS_BY_CONTRACT = {
    "eval-case-contract": ("enforce-eval-claim-boundary-required",),
    "redteam-case-contract": ("enforce-redteam-evidence-basis-list",),
    "rag-metric-contract": ("reject-rag-runtime-hints",),
    "governance-gate-contract": ("enforce-governance-risk_tier-enum",),
}

REQUIRED_GOVERNANCE_BLOCKED_ACTIONS = (
    "dependency_install",
    "runtime_integration",
    "deploy",
    "publish",
)

RECORD_ID_FIELDS = {
    "eval-case-contract": "case_id",
    "redteam-case-contract": "case_id",
    "rag-metric-contract": "metric_id",
    "governance-gate-contract": "gate_id",
}

PROTECTED_ACTION_FLAGS = (
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
)


def false_claim_boundary() -> dict[str, bool]:
    return {flag: False for flag in PROTECTED_ACTION_FLAGS}


def blocked_capability_flags() -> dict[str, bool]:
    return {
        "provider_neutral": PROVIDER_NEUTRAL,
        "dependency_free": DEPENDENCY_FREE,
        "candidate_tool_import_allowed": CANDIDATE_TOOL_IMPORT_ALLOWED,
        "dependency_install_allowed": DEPENDENCY_INSTALL_ALLOWED,
        "external_fetch_allowed": EXTERNAL_FETCH_ALLOWED,
        "runtime_integration_allowed": RUNTIME_INTEGRATION_ALLOWED,
    }

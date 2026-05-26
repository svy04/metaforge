from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
STRATEGY = ROOT / "avf" / "strategy" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_acquisition_loop_v0_1.py"
STRATEGY_DECISION = STRATEGY / "strategy_adaptation_decision_packet.json"
ACQUISITION_PLAN = CAPABILITIES / "capability_acquisition_plan.json"
CANDIDATE_REGISTRY = CAPABILITIES / "capability_candidate_registry.json"
BUILD_BUY_ADOPT = CAPABILITIES / "build_buy_adopt_decision_records.json"
SOURCE_LEDGER = CAPABILITIES / "capability_source_ledger.json"
NEXT_CODEX_TASK = CAPABILITIES / "next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_acquisition_loop_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_ACQUISITION_LOOP_V0_1_VALIDATION_REPORT.md"

THIS_GOAL_ID = "avf_capability_acquisition_loop_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_fit_scoring_validator_v0_1"

CORE_FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

EXTENDED_FALSE_FLAGS = CORE_FALSE_FLAGS + [
    "oss_clone_performed",
    "package_install_performed",
]

REQUIRED_FILES = [
    RUNNER,
    STRATEGY_DECISION,
    ACQUISITION_PLAN,
    CANDIDATE_REGISTRY,
    BUILD_BUY_ADOPT,
    SOURCE_LEDGER,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_CAPABILITY_IDS = {
    "cap-llm-gateway",
    "cap-agent-runtime",
    "cap-durable-workflow",
    "cap-tool-registry",
    "cap-observability",
    "cap-evaluation-red-team",
    "cap-rag-document-pipeline",
    "cap-approved-coding-executor",
}

REQUIRED_SOURCE_IDS = {
    "src-litellm-docs",
    "src-langgraph-docs",
    "src-temporal-docs",
    "src-mcp-docs",
    "src-opentelemetry-docs",
    "src-langfuse-docs",
    "src-phoenix-docs",
    "src-promptfoo-docs",
    "src-ragas-docs",
    "src-haystack-docs",
    "src-openhands-docs",
    "src-swe-agent-docs",
}

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_acquisition_loop_v0_1=true",
    "capability_acquisition_plan_created=true",
    "candidate_registry_created=true",
    "build_buy_adopt_records_created=true",
    "source_ledger_created=true",
    "protected_action_executed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "provider_calls_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Acquisition Loop v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_false_flags(record: dict, label: str, flags: list[str] = EXTENDED_FALSE_FLAGS) -> None:
    for flag in flags:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_strategy_decision() -> None:
    decision = read_json(STRATEGY_DECISION)
    if decision.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("strategy decision does not authorize capability acquisition as next safe goal")
    if decision.get("decision") != "refine":
        fail("strategy decision should remain refine before capability acquisition")
    require_false_flags(decision.get("claim_boundary", {}), "strategy decision claim boundary", CORE_FALSE_FLAGS)


def require_source_ledger() -> None:
    ledger = read_json(SOURCE_LEDGER)
    if ledger.get("automation_fetch_performed") is not False:
        fail("capability source ledger automation_fetch_performed must be false")
    source_ids = {entry.get("source_id") for entry in ledger.get("sources", [])}
    missing = sorted(REQUIRED_SOURCE_IDS - source_ids)
    if missing:
        fail("capability source ledger missing source ids:\n" + "\n".join(missing))
    for entry in ledger.get("sources", []):
        if entry.get("source_kind") not in {"official_docs", "paper"}:
            fail(f"source has unsupported source_kind: {entry.get('source_id')}")
        if not entry.get("url", "").startswith("https://"):
            fail(f"source missing https URL: {entry.get('source_id')}")


def require_candidate_registry() -> None:
    registry = read_json(CANDIDATE_REGISTRY)
    if registry.get("status") != "PASS":
        fail("candidate registry status must be PASS")
    require_false_flags(registry.get("claim_boundary", {}), "candidate registry claim boundary")
    capability_ids = {capability.get("capability_id") for capability in registry.get("capabilities", [])}
    missing = sorted(REQUIRED_CAPABILITY_IDS - capability_ids)
    if missing:
        fail("candidate registry missing capability ids:\n" + "\n".join(missing))
    for capability in registry.get("capabilities", []):
        if capability.get("integration_status") != "proposed_only":
            fail(f"capability integration_status must be proposed_only: {capability.get('capability_id')}")
        if capability.get("dependency_install_allowed") is not False:
            fail(f"dependency install must be blocked: {capability.get('capability_id')}")
        if capability.get("external_fetch_performed") is not False:
            fail(f"external fetch must be false: {capability.get('capability_id')}")
        if capability.get("license_review_required") is not True:
            fail(f"license review must be required: {capability.get('capability_id')}")
        if capability.get("security_review_required") is not True:
            fail(f"security review must be required: {capability.get('capability_id')}")
        if capability.get("owner_approval_required") is not True:
            fail(f"owner approval must be required: {capability.get('capability_id')}")
        if not capability.get("candidate_records"):
            fail(f"capability missing candidate records: {capability.get('capability_id')}")
        for candidate in capability.get("candidate_records", []):
            if candidate.get("integration_status") != "proposed_only":
                fail(f"candidate integration_status must be proposed_only: {candidate.get('candidate_id')}")
            if candidate.get("source_ref") not in REQUIRED_SOURCE_IDS:
                fail(f"candidate source_ref not in source ledger: {candidate.get('candidate_id')}")


def require_build_buy_adopt_records() -> None:
    records = read_json(BUILD_BUY_ADOPT)
    if records.get("status") != "PASS":
        fail("build/buy/adopt records status must be PASS")
    require_false_flags(records.get("claim_boundary", {}), "build/buy/adopt claim boundary")
    decision_ids = {record.get("capability_id") for record in records.get("decisions", [])}
    missing = sorted(REQUIRED_CAPABILITY_IDS - decision_ids)
    if missing:
        fail("build/buy/adopt records missing capability ids:\n" + "\n".join(missing))
    for record in records.get("decisions", []):
        if record.get("decision_status") != "proposed_only":
            fail(f"decision_status must be proposed_only: {record.get('capability_id')}")
        if record.get("dependency_install_allowed") is not False:
            fail(f"decision dependency install must be blocked: {record.get('capability_id')}")
        if record.get("external_fetch_performed") is not False:
            fail(f"decision external fetch must be false: {record.get('capability_id')}")


def require_acquisition_plan() -> None:
    plan = read_json(ACQUISITION_PLAN)
    if plan.get("status") != "PASS":
        fail("capability acquisition plan status must be PASS")
    if plan.get("goal_id") != THIS_GOAL_ID:
        fail("capability acquisition plan goal_id mismatch")
    if plan.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("capability acquisition plan next safe goal mismatch")
    if plan.get("candidate_registry_hash") != sha256(CANDIDATE_REGISTRY):
        fail("capability acquisition plan candidate registry hash mismatch")
    if plan.get("build_buy_adopt_hash") != sha256(BUILD_BUY_ADOPT):
        fail("capability acquisition plan build/buy/adopt hash mismatch")
    if plan.get("source_ledger_hash") != sha256(SOURCE_LEDGER):
        fail("capability acquisition plan source ledger hash mismatch")
    require_false_flags(plan.get("claim_boundary", {}), "capability acquisition plan claim boundary")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("capability acquisition validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("capability acquisition validation result next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "capability acquisition validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_strategy_decision()
    require_source_ledger()
    require_candidate_registry()
    require_build_buy_adopt_records()
    require_acquisition_plan()
    require_validation_result()
    require_markers(NEXT_CODEX_TASK, ["task_id: avf-capability-fit-scoring-validator-v0-1", "forbidden_changes:", "validation_commands:", f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}"])
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Acquisition Loop v0.1 validation")
    print("RESULT: PASS")
    print("capability_acquisition_loop_v0_1=true")
    print("capability_acquisition_plan_created=true")
    print("candidate_registry_created=true")
    print("build_buy_adopt_records_created=true")
    print("source_ledger_created=true")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("provider_calls_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

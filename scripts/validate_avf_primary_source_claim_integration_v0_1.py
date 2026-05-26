from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
DOC_AVF = ROOT / "docs" / "avf"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_claim_integration_v0_1.py"
RECORDS = CAPABILITIES / "primary_source_manual_records.json"
RECORDS_REVIEW_GATE = CAPABILITIES / "primary_source_records_review_gate.json"
INTEGRATION_MAP = CAPABILITIES / "primary_source_claim_integration_map.json"
INTEGRATION_REPORT = CAPABILITIES / "primary_source_claim_integration_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_claim_integration_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_claim_integration_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_CLAIM_INTEGRATION_V0_1_REPORT.md"

OPEN_SOURCE_MAP = DOC_AVF / "OPEN_SOURCE_EXPANSION_MAP.md"
PLATFORM_ROADMAP = DOC_AVF / "AVF_PLATFORM_ROADMAP.md"
MARKET_TO_FACTORY_VISION = DOC_AVF / "AVF_MARKET_TO_FACTORY_VISION.md"

THIS_GOAL_ID = "avf_primary_source_claim_integration_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_records_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_claim_integration_review_v0_1"
REVIEW_DECISION = "PRIMARY_SOURCE_RECORDS_REVIEWED_CLAIM_INTEGRATION_READY"
INTEGRATION_DECISION = "PRIMARY_SOURCE_CLAIMS_INTEGRATED_INTO_DOCS_ONLY"
PROMOTION_SCOPE = "architecture_docs_and_plans_only"

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
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

SOURCE_TARGET_IDS = [
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
]

REQUIRED_FILES = [
    RUNNER,
    RECORDS,
    RECORDS_REVIEW_GATE,
    INTEGRATION_MAP,
    INTEGRATION_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
    OPEN_SOURCE_MAP,
    PLATFORM_ROADMAP,
    MARKET_TO_FACTORY_VISION,
]

DOC_MARKERS = [
    "## Primary-Source Claim Integration",
    "primary_source_claims_integrated=true",
    f"integration_decision={INTEGRATION_DECISION}",
    f"promotion_scope={PROMOTION_SCOPE}",
    "runtime_adoption_allowed=false",
    "dependency_adoption_allowed=false",
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_claim_integration_v0_1=true",
    f"integration_decision={INTEGRATION_DECISION}",
    f"promotion_scope={PROMOTION_SCOPE}",
    "docs_updated=3",
    "source_claims_integrated=7",
    "runtime_adoption_allowed=false",
    "dependency_adoption_allowed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "automated_scraping_performed=false",
    "scraping_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: review-primary-source-claim-integration",
    "owner_approval_required_before_execution: true",
    "Review source-backed doc integration before using it for implementation planning",
    "Do not adopt dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Primary-Source Claim Integration v0.1 validation")
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


def require_review_gate() -> None:
    gate = read_json(RECORDS_REVIEW_GATE)
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("records review gate goal_id mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("records review gate must point to this integration goal")
    if gate.get("review_decision") != REVIEW_DECISION:
        fail("records review gate decision mismatch")
    if gate.get("promotion_scope") != PROMOTION_SCOPE:
        fail("records review gate promotion scope mismatch")
    if gate.get("runtime_adoption_allowed") is not False:
        fail("runtime adoption must remain blocked")
    if gate.get("dependency_adoption_allowed") is not False:
        fail("dependency adoption must remain blocked")
    require_false_flags(gate.get("claim_boundary", {}), "records review gate")


def require_integration_map() -> None:
    data = read_json(INTEGRATION_MAP)
    if data.get("goal_id") != THIS_GOAL_ID:
        fail("integration map goal_id mismatch")
    if data.get("integration_decision") != INTEGRATION_DECISION:
        fail("integration decision mismatch")
    if data.get("promotion_scope") != PROMOTION_SCOPE:
        fail("integration promotion scope mismatch")
    if data.get("runtime_adoption_allowed") is not False:
        fail("integration map must block runtime adoption")
    if data.get("dependency_adoption_allowed") is not False:
        fail("integration map must block dependency adoption")
    items = data.get("integrated_claims")
    if not isinstance(items, list) or len(items) != len(SOURCE_TARGET_IDS):
        fail("integration map must contain seven claims")
    if [item.get("source_target_id") for item in items] != SOURCE_TARGET_IDS:
        fail("integrated claim source target ids mismatch")
    for item in items:
        if item.get("promotion_scope") != PROMOTION_SCOPE:
            fail("integrated claim promotion scope mismatch")
        if not item.get("source_uri", "").startswith("https://"):
            fail("integrated claim must keep primary source uri")
    require_false_flags(data.get("claim_boundary", {}), "integration map")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_claim_integration_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("integration_decision") != INTEGRATION_DECISION:
        fail("validation result integration decision mismatch")
    if result.get("docs_updated") != 3:
        fail("validation result docs_updated mismatch")
    if result.get("source_claims_integrated") != len(SOURCE_TARGET_IDS):
        fail("validation result claim count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_review_gate()
    require_integration_map()
    require_text_markers(INTEGRATION_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)
    for doc in [OPEN_SOURCE_MAP, PLATFORM_ROADMAP, MARKET_TO_FACTORY_VISION]:
        require_text_markers(doc, DOC_MARKERS)

    print("AVF Primary-Source Claim Integration v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_claim_integration_v0_1=true")
    print(f"integration_decision={INTEGRATION_DECISION}")
    print(f"promotion_scope={PROMOTION_SCOPE}")
    print("docs_updated=3")
    print("source_claims_integrated=7")
    print("runtime_adoption_allowed=false")
    print("dependency_adoption_allowed=false")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("automated_scraping_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

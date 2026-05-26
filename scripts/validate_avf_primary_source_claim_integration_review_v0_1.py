from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_primary_source_claim_integration_review_v0_1.py"
INTEGRATION_MAP = CAPABILITIES / "primary_source_claim_integration_map.json"
INTEGRATION_VALIDATION = CAPABILITIES / "primary_source_claim_integration_v0_1.validation_result.json"
REVIEW_GATE = CAPABILITIES / "primary_source_claim_integration_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "primary_source_claim_integration_review_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_claim_integration_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_claim_integration_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_CLAIM_INTEGRATION_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_claim_integration_review_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_claim_integration_v0_1"
NEXT_SAFE_GOAL_ID = "avf_runtime_adapter_decision_matrix_v0_1"
INTEGRATION_DECISION = "PRIMARY_SOURCE_CLAIMS_INTEGRATED_INTO_DOCS_ONLY"
REVIEW_DECISION = "PRIMARY_SOURCE_CLAIM_INTEGRATION_REVIEWED_FOR_PLANNING"
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
    INTEGRATION_MAP,
    INTEGRATION_VALIDATION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REVIEW_MARKERS = [
    f"review_decision={REVIEW_DECISION}",
    f"promotion_scope={PROMOTION_SCOPE}",
    "source_claims_reviewed=7",
    "implementation_planning_allowed=true",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-runtime-adapter-decision-matrix",
    "owner_approval_required_before_execution: true",
    "Use reviewed primary-source claims to create a decision matrix",
    "Do not adopt dependencies, integrate runtimes, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "primary_source_claim_integration_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"promotion_scope={PROMOTION_SCOPE}",
    "source_claims_reviewed=7",
    "implementation_planning_allowed=true",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
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


def fail(message: str) -> None:
    print("AVF Primary-Source Claim Integration Review v0.1 validation")
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


def require_integration_map() -> None:
    data = read_json(INTEGRATION_MAP)
    if data.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("integration map goal_id mismatch")
    if data.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("integration map must point to this review goal")
    if data.get("integration_decision") != INTEGRATION_DECISION:
        fail("integration decision mismatch")
    if data.get("promotion_scope") != PROMOTION_SCOPE:
        fail("promotion scope mismatch")
    claims = data.get("integrated_claims")
    if not isinstance(claims, list) or len(claims) != len(SOURCE_TARGET_IDS):
        fail("integration map must contain seven claims")
    if [claim.get("source_target_id") for claim in claims] != SOURCE_TARGET_IDS:
        fail("integrated claim ids mismatch")
    if data.get("runtime_adoption_allowed") is not False:
        fail("runtime adoption must remain blocked")
    if data.get("dependency_adoption_allowed") is not False:
        fail("dependency adoption must remain blocked")
    require_false_flags(data.get("claim_boundary", {}), "integration map")


def require_review_gate() -> None:
    gate = read_json(REVIEW_GATE)
    expected = {
        "gate_id": "avf-primary-source-claim-integration-review-gate-v0-1",
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "promotion_scope": PROMOTION_SCOPE,
        "source_claims_reviewed": len(SOURCE_TARGET_IDS),
        "implementation_planning_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            fail(f"review gate {key} mismatch")
    if gate.get("reviewed_source_target_ids") != SOURCE_TARGET_IDS:
        fail("review gate source target ids mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "review gate")


def require_validation_result() -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_primary_source_claim_integration_review_v0_1":
        fail("validation result validator_id mismatch")
    if result.get("status") != "PASS":
        fail("validation result must be PASS")
    if result.get("review_decision") != REVIEW_DECISION:
        fail("validation result review decision mismatch")
    if result.get("source_claims_reviewed") != len(SOURCE_TARGET_IDS):
        fail("validation result claim count mismatch")
    if result.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    require_false_flags(result.get("claim_boundary", {}), "validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    require_integration_map()
    require_review_gate()
    require_text_markers(REVIEW_REPORT, REVIEW_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Primary-Source Claim Integration Review v0.1 validation")
    print("RESULT: PASS")
    print("primary_source_claim_integration_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"promotion_scope={PROMOTION_SCOPE}")
    print("source_claims_reviewed=7")
    print("implementation_planning_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
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

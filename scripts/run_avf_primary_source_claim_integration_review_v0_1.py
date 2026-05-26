from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

INTEGRATION_MAP = CAPABILITIES / "primary_source_claim_integration_map.json"
REVIEW_GATE = CAPABILITIES / "primary_source_claim_integration_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "primary_source_claim_integration_review_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_claim_integration_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_claim_integration_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_CLAIM_INTEGRATION_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_claim_integration_review_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_claim_integration_v0_1"
NEXT_SAFE_GOAL_ID = "avf_runtime_adapter_decision_matrix_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
INTEGRATION_DECISION = "PRIMARY_SOURCE_CLAIMS_INTEGRATED_INTO_DOCS_ONLY"
REVIEW_DECISION = "PRIMARY_SOURCE_CLAIM_INTEGRATION_REVIEWED_FOR_PLANNING"
PROMOTION_SCOPE = "architecture_docs_and_plans_only"

SOURCE_TARGET_IDS = [
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_integration_map(data: dict) -> list[dict]:
    if data.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("integration map goal mismatch")
    if data.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("integration map must point to this review goal")
    if data.get("integration_decision") != INTEGRATION_DECISION:
        raise SystemExit("integration decision mismatch")
    if data.get("promotion_scope") != PROMOTION_SCOPE:
        raise SystemExit("promotion scope mismatch")
    claims = data.get("integrated_claims")
    if not isinstance(claims, list) or len(claims) != len(SOURCE_TARGET_IDS):
        raise SystemExit("integration map must contain seven claims")
    if [claim.get("source_target_id") for claim in claims] != SOURCE_TARGET_IDS:
        raise SystemExit("integrated claim ids mismatch")
    return claims


def build_review_gate(claims: list[dict]) -> dict:
    return {
        "gate_id": "avf-primary-source-claim-integration-review-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "promotion_scope": PROMOTION_SCOPE,
        "source_claims_reviewed": len(claims),
        "reviewed_source_target_ids": SOURCE_TARGET_IDS,
        "implementation_planning_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_review_report(claims: list[dict]) -> str:
    rows = "\n".join(
        f"- `{claim['source_target_id']}` -> `{claim['target_claim_id']}` "
        f"({PROMOTION_SCOPE}, implementation planning only)"
        for claim in claims
    )
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# Primary-Source Claim Integration Review v0.1

review_decision={REVIEW_DECISION}
promotion_scope={PROMOTION_SCOPE}
source_claims_reviewed={len(claims)}
implementation_planning_allowed=true
dependency_adoption_allowed=false
runtime_integration_allowed=false

## Reviewed integrated claims

{rows}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-runtime-adapter-decision-matrix
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Use reviewed primary-source claims to create a decision matrix
  - Compare candidate runtime and tooling roles without installing or adopting dependencies
  - Keep actual dependency adoption and runtime integration behind later gates
  - Do not adopt dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(claims: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_primary_source_claim_integration_review_v0_1",
        "status": "PASS",
        "review_decision": REVIEW_DECISION,
        "promotion_scope": PROMOTION_SCOPE,
        "source_claims_reviewed": len(claims),
        "implementation_planning_allowed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(claims: list[dict]) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Primary-Source Claim Integration Review v0.1 Report

RESULT: PASS
primary_source_claim_integration_review_v0_1=true

## Commands

- python scripts\\run_avf_primary_source_claim_integration_review_v0_1.py
- python scripts\\validate_avf_primary_source_claim_integration_review_v0_1.py

## Gate summary

- review_decision={REVIEW_DECISION}
- promotion_scope={PROMOTION_SCOPE}
- source_claims_reviewed={len(claims)}
- implementation_planning_allowed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Generated artifacts

- {rel(REVIEW_GATE)}
- {rel(REVIEW_REPORT)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    claims = require_integration_map(read_json(INTEGRATION_MAP))

    write_json(REVIEW_GATE, build_review_gate(claims))
    write_text(REVIEW_REPORT, build_review_report(claims))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(claims))
    write_text(VALIDATION_REPORT, build_report(claims))

    print("AVF Primary-Source Claim Integration Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"promotion_scope={PROMOTION_SCOPE}")
    print(f"source_claims_reviewed={len(claims)}")
    print("implementation_planning_allowed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

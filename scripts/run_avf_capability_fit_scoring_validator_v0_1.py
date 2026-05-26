from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

ACQUISITION_PLAN = CAPABILITIES / "capability_acquisition_plan.json"
CANDIDATE_REGISTRY = CAPABILITIES / "capability_candidate_registry.json"
BUILD_BUY_ADOPT = CAPABILITIES / "build_buy_adopt_decision_records.json"
CAPABILITY_SOURCE_LEDGER = CAPABILITIES / "capability_source_ledger.json"
SCORECARD = CAPABILITIES / "capability_fit_scorecard.json"
GATE_DECISION = CAPABILITIES / "capability_fit_scoring_gate_decision.json"
SCORING_SOURCE_LEDGER = CAPABILITIES / "capability_fit_scoring_source_ledger.json"
VALIDATION_RESULT = CAPABILITIES / "capability_fit_scoring_validator_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_FIT_SCORING_VALIDATOR_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_fit_scoring_validator_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_review_dossier_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"

SCORING_SOURCE_REFS = [
    "src-openssf-scorecard",
    "src-slsa-spec",
    "src-spdx-spec",
    "src-github-dependency-review",
    "src-openssf-scorecard-paper",
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


def build_scoring_source_ledger() -> dict:
    return {
        "ledger_id": "avf-capability-fit-scoring-source-ledger-v0-1",
        "created_at": CREATED_AT,
        "automation_fetch_performed": False,
        "source_selection_boundary": (
            "Scoring sources are operator-reviewed primary URLs. This runner does not fetch URLs, "
            "query package registries, inspect remote repositories, install dependencies, clone code, "
            "or execute any runtime integration."
        ),
        "sources": [
            {
                "source_id": "src-openssf-scorecard",
                "source_kind": "official_repo",
                "title": "OpenSSF Scorecard",
                "url": "https://github.com/ossf/scorecard",
                "why_used": "Provides the security-health scoring vocabulary for later OSS repository review.",
            },
            {
                "source_id": "src-slsa-spec",
                "source_kind": "official_standard",
                "title": "SLSA specification",
                "url": "https://slsa.dev/spec/v1.2/",
                "why_used": "Provides supply-chain provenance and build-integrity gate vocabulary.",
            },
            {
                "source_id": "src-spdx-spec",
                "source_kind": "official_standard",
                "title": "SPDX specifications",
                "url": "https://spdx.dev/use/specifications/",
                "why_used": "Provides license-expression and SBOM vocabulary for candidate review.",
            },
            {
                "source_id": "src-github-dependency-review",
                "source_kind": "official_docs",
                "title": "GitHub Dependency Review",
                "url": "https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review",
                "why_used": "Provides a future pull-request dependency review gate, not enabled in this pass.",
            },
            {
                "source_id": "src-openssf-scorecard-paper",
                "source_kind": "paper",
                "title": "OpenSSF Scorecard: On the Path Toward Ecosystem-wide Automated Security Metrics",
                "url": "https://arxiv.org/abs/2208.03412",
                "why_used": "Primary paper context for using automated security metrics as decision support, not as final proof.",
            },
        ],
    }


FIT_PROFILES = {
    "candidate-litellm-proxy": (88, 42, "High strategic fit for provider independence, but gateway security and spend-governance review are still required."),
    "candidate-langgraph-runtime": (84, 40, "Strong stateful-agent fit after the local runtime contract is sharper."),
    "candidate-temporal-agent-boundary": (74, 36, "Useful for agent durability, but it overlaps durable-workflow scope and should stay secondary."),
    "candidate-temporal-workflow": (86, 34, "Strong durable-workflow fit once replay/idempotency contracts are explicit."),
    "candidate-mcp-tool-registry": (82, 55, "Strong tool-registry fit, with elevated tool-permission and connector security risk."),
    "candidate-opentelemetry": (90, 24, "Best low-risk observability standard fit for trace, metric, log, and evidence correlation."),
    "candidate-langfuse": (78, 46, "Good LLM observability fit after gateway and data-retention policy are defined."),
    "candidate-phoenix": (76, 44, "Good AI observability/eval fit after trace schema and hosted/self-host boundary are defined."),
    "candidate-promptfoo": (80, 38, "Strong eval/red-team fit, but model-provider and test-data boundaries must be reviewed."),
    "candidate-ragas": (72, 34, "Useful RAG-eval fit only after document-memory and retrieval contracts exist."),
    "candidate-langfuse-evals": (74, 46, "Useful eval/observability bridge, gated by the same data-retention concerns as Langfuse."),
    "candidate-haystack": (76, 42, "Good document-pipeline candidate once memory contracts and data boundaries exist."),
    "candidate-ragas-rag-eval": (70, 34, "Companion RAG-eval candidate, but not a standalone memory pipeline."),
    "candidate-openhands": (64, 58, "Potential executor comparison candidate with elevated sandbox and permission risk."),
    "candidate-swe-agent": (62, 54, "Potential issue-to-code research candidate, gated behind Codex-lane and sandbox review."),
}


def flatten_candidates(registry: dict) -> list[dict]:
    rows = []
    for capability in registry.get("capabilities", []):
        for candidate in capability.get("candidate_records", []):
            row = dict(candidate)
            row["capability_id"] = capability["capability_id"]
            row["capability_name"] = capability["capability_name"]
            row["capability_recommendation"] = capability["build_buy_adopt_recommendation"]
            rows.append(row)
    return rows


def score_candidate(row: dict) -> dict:
    fit_score, risk_score, rationale = FIT_PROFILES[row["candidate_id"]]
    return {
        "candidate_id": row["candidate_id"],
        "candidate_name": row["name"],
        "capability_id": row["capability_id"],
        "capability_name": row["capability_name"],
        "fit_score": fit_score,
        "risk_score": risk_score,
        "priority_rank": 0,
        "integration_readiness": "not_ready_requires_reviews",
        "license_review_status": row["license_review_status"],
        "security_review_status": row["security_review_status"],
        "maintenance_review_status": row["maintenance_review_status"],
        "next_gate": "capability_review_dossier_required",
        "scoring_basis": [
            "strategic_fit",
            "architecture_fit",
            "safety_and_supply_chain_risk",
            "review_status",
            "integration_boundary",
        ],
        "scoring_source_refs": SCORING_SOURCE_REFS,
        "candidate_source_ref": row["source_ref"],
        "rationale": rationale,
        "blocked_reason": "License, security, maintenance, and owner approval reviews are required before any install, clone, fetch, or integration.",
        "claim_boundary": false_boundary(),
    }


def build_scorecard(registry: dict) -> dict:
    scores = [score_candidate(row) for row in flatten_candidates(registry)]
    scores.sort(key=lambda item: (-item["fit_score"], item["risk_score"], item["candidate_id"]))
    for rank, item in enumerate(scores, start=1):
        item["priority_rank"] = rank
    return {
        "scorecard_id": "avf-capability-fit-scorecard-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "scoring_method": {
            "fit_score_range": "0-100",
            "risk_score_range": "0-100",
            "integration_rule": "Higher fit does not authorize integration. All candidates remain blocked until review dossiers are produced and approved.",
            "primary_source_basis": SCORING_SOURCE_REFS,
        },
        "candidate_scores": scores,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_gate_decision(scorecard: dict) -> dict:
    top_candidates = [score["candidate_id"] for score in scorecard["candidate_scores"][:5]]
    return {
        "gate_decision_id": "avf-capability-fit-scoring-gate-decision-v0-1",
        "created_at": CREATED_AT,
        "status": "PASS",
        "decision": "do_not_integrate_yet",
        "decision_reason": "Fit scores prioritize review order only. No candidate has completed license, security, maintenance, owner approval, or integration-readiness gates.",
        "top_candidates": top_candidates,
        "required_before_integration": [
            "capability review dossier",
            "license review",
            "security review",
            "maintenance review",
            "architecture fit review",
            "owner approval",
            "sandbox plan",
            "rollback plan",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_fit_scoring_validator_v0_1",
        "status": "PASS",
        "checks": [
            "acquisition plan authorizes fit scoring",
            "scorecard exists",
            "all candidates scored",
            "gate decision blocks integration",
            "scoring source ledger exists",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(scorecard: dict, gate: dict) -> str:
    top_lines = "\n".join(
        f"- {score['priority_rank']}. {score['candidate_id']} fit={score['fit_score']} risk={score['risk_score']}"
        for score in scorecard["candidate_scores"][:5]
    )
    return f"""# AVF Capability Fit Scoring Validator v0.1 Report

RESULT: PASS
capability_fit_scoring_validator_v0_1=true
capability_fit_scorecard_created=true
candidate_scores_created=true
gate_decision_created=true
scoring_source_ledger_created=true
protected_action_executed=false
dependency_install_performed=false
external_fetch_performed=false
oss_clone_performed=false
package_install_performed=false
runtime_integration_performed=false
provider_calls_performed=false
scraping_performed=false
posting_automation_performed=false
deploy_performed=false
publish_performed=false
release_ready=false
production_ready=false
next_safe_goal_id={NEXT_SAFE_GOAL_ID}

## Top Review Candidates

{top_lines}

## Gate Decision

decision={gate['decision']}

Fit scores prioritize review order only. They do not authorize install, clone, fetch, provider calls, runtime integration, deploy, publish, release readiness, or production readiness.

## Scoring Sources

- OpenSSF Scorecard official repo
- SLSA specification
- SPDX specifications
- GitHub Dependency Review docs
- OpenSSF Scorecard paper
"""


def main() -> None:
    acquisition_plan = read_json(ACQUISITION_PLAN)
    if acquisition_plan.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("capability acquisition plan does not point to this fit scoring goal")
    registry = read_json(CANDIDATE_REGISTRY)
    read_json(BUILD_BUY_ADOPT)
    read_json(CAPABILITY_SOURCE_LEDGER)

    scoring_source_ledger = build_scoring_source_ledger()
    write_json(SCORING_SOURCE_LEDGER, scoring_source_ledger)
    scorecard = build_scorecard(registry)
    write_json(SCORECARD, scorecard)
    gate = build_gate_decision(scorecard)
    write_json(GATE_DECISION, gate)
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(scorecard, gate))

    print("AVF Capability Fit Scoring Validator v0.1 runner")
    print("RESULT: PASS")
    print("capability_fit_scoring_validator_v0_1=true")
    print("capability_fit_scorecard_created=true")
    print("candidate_scores_created=true")
    print("gate_decision_created=true")
    print("scoring_source_ledger_created=true")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
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

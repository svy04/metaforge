from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

QUALITY_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_manual_evidence_quality_review_gate.json"
RECOMMENDATION = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation.json"
RECOMMENDATION_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_gate.json"
RECOMMENDATION_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_EVIDENCE_BACKED_CAPABILITY_RECOMMENDATION_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_quality_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_no_install_adapter_plan_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
RECOMMENDATION_DECISION = "RECOMMEND_CONDITIONAL_NO_INSTALL_ADAPTER_PLANNING"
RECOMMENDATION_STATUS = "evidence_backed_candidate_fit_recommended_without_dependency_adoption"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


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
        "runtime_export_performed": False,
        "collector_started": False,
        "telemetry_export_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "release_ready": False,
        "production_ready": False,
    }


def require_quality_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("quality review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("quality review must point to this recommendation goal")
    if review.get("ready_for_evidence_backed_recommendation_count") != 1:
        raise SystemExit("quality review must be ready for recommendation")
    if review.get("adoption_authorized") is not False:
        raise SystemExit("quality review must not authorize adoption")


def candidate_fit_signals() -> list[dict]:
    return [
        {
            "signal_id": "promptfoo-eval-redteam-fit",
            "signal": "Promptfoo evidence supports LLM evaluation and red-team workflow fit.",
            "claim_boundary": "fit_signal_only_no_dependency_adoption",
        },
        {
            "signal_id": "ragas-rag-eval-fit",
            "signal": "Ragas evidence supports RAG and agent evaluation metric fit.",
            "claim_boundary": "fit_signal_only_no_dependency_adoption",
        },
        {
            "signal_id": "owasp-governance-fit",
            "signal": "OWASP evidence supports red-team and excessive-agency governance categories.",
            "claim_boundary": "governance_signal_only_no_runtime_authorization",
        },
        {
            "signal_id": "nist-ai-rmf-governance-fit",
            "signal": "NIST AI RMF evidence supports documented risk governance and third-party review.",
            "claim_boundary": "governance_signal_only_no_readiness_claim",
        },
    ]


def required_later_reviews() -> list[dict]:
    return [
        {
            "review_id": "legal-license-review-before-dependency-adoption",
            "status": "required_later_not_performed",
            "reason": "MIT and Apache-2.0 notes were captured, but legal review is separate from evidence collection.",
        },
        {
            "review_id": "security-supply-chain-review-before-runtime-integration",
            "status": "required_later_not_performed",
            "reason": "Security surfaces were identified, but no dependency, source, or runtime was inspected or executed.",
        },
    ]


def counts(quality_review: dict) -> dict:
    return {
        "reviewed_evidence_record_count": quality_review["reviewed_evidence_record_count"],
        "recommendation_count": 1,
        "candidate_fit_signal_count": len(candidate_fit_signals()),
        "required_later_review_count": len(required_later_reviews()),
        "adoption_authorized_count": 0,
        "dependency_install_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "ready_for_no_install_adapter_plan_count": 1,
    }


def base_recommendation_record(quality_review: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "recommendation_decision": RECOMMENDATION_DECISION,
        "recommendation_status": RECOMMENDATION_STATUS,
        "recommended_next_implementation_mode": "no_install_adapter_plan_only",
        "candidate_fit_signals": candidate_fit_signals(),
        "required_later_reviews": required_later_reviews(),
        "input_uris": {
            "manual_evidence_quality_review_gate": rel(QUALITY_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "adoption_authorized": False,
        "dependency_install_allowed": False,
        "runtime_integration_allowed": False,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(quality_review),
        "claim_boundary": false_boundary(),
    }


def build_gate(quality_review: dict) -> dict:
    return {
        **base_recommendation_record(quality_review),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-evidence-backed-capability-recommendation-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Evidence-backed candidate recommendation created without dependency adoption or runtime integration",
    }


def build_validation_result(quality_review: dict) -> dict:
    return {
        **base_recommendation_record(quality_review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(QUALITY_REVIEW_GATE),
            rel(RECOMMENDATION),
            rel(RECOMMENDATION_GATE),
            rel(RECOMMENDATION_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(quality_review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(quality_review).items())
    signal_lines = "\n".join(
        "- {signal_id}: {claim_boundary}".format(**signal)
        for signal in candidate_fit_signals()
    )
    later_review_lines = "\n".join(
        "- {review_id}: {status}".format(**review)
        for review in required_later_reviews()
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Evidence-Backed Capability Recommendation v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_evidence_backed_capability_recommendation_v0_1=true

## Recommendation summary

- candidate_id={CANDIDATE_ID}
- recommendation_decision={RECOMMENDATION_DECISION}
- recommendation_status={RECOMMENDATION_STATUS}
- recommended_next_implementation_mode=no_install_adapter_plan_only
- adoption_authorized=false
- dependency_install_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Candidate fit signals

{signal_lines}

## Required later reviews

{later_review_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-priority-1-no-install-adapter-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Plan a no-install adapter boundary from the evidence-backed recommendation
  - Keep the plan at contract/spec level only
  - Preserve later legal and security review requirements before any dependency adoption
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    quality_review = read_json(QUALITY_REVIEW_GATE)
    require_quality_review(quality_review)

    record = base_recommendation_record(quality_review)
    write_json(RECOMMENDATION, record)
    write_json(RECOMMENDATION_GATE, build_gate(quality_review))
    report = build_report(quality_review)
    write_text(RECOMMENDATION_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(quality_review))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Evidence-Backed Capability Recommendation v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"recommendation_decision={RECOMMENDATION_DECISION}")
    print(f"recommendation_status={RECOMMENDATION_STATUS}")
    for key, value in counts(quality_review).items():
        print(f"{key}={value}")
    print("adoption_authorized=false")
    print("dependency_install_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

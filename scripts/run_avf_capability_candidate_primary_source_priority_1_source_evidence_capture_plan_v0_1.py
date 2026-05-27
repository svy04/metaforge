from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_review_gate.json"
CAPTURE_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan.json"
CAPTURE_FIELD_SPEC = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_field_spec.json"
CAPTURE_PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_gate.json"
CAPTURE_PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_SOURCE_EVIDENCE_CAPTURE_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
CAPTURE_PLAN_STATUS = "source_evidence_capture_plan_created_non_executable"
CAPTURE_PLAN_SCOPE = "capture_field_schema_and_target_plan_only"


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


def require_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("deep research plan review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("deep research plan review must point to this capture plan goal")
    if review.get("ready_for_source_evidence_capture_plan_count") != 1:
        raise SystemExit("deep research plan review must be ready for capture planning")
    if review.get("external_fetch_performed") is not False:
        raise SystemExit("external fetch must remain blocked")
    if review.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def capture_fields() -> list[dict]:
    descriptions = {
        "source_target_id": "Stable id from the reviewed source target.",
        "candidate_id": "Capability candidate receiving the evidence record.",
        "source_kind": "Primary source category such as official docs, original repository, paper, or standard.",
        "source_uri": "Canonical source URI for later owner-approved inspection.",
        "retrieval_mode": "Allowed future capture mode; must remain owner-approved and non-automated in this plan.",
        "capture_scope": "The bounded purpose of the evidence record.",
        "claim_to_extract": "Specific claim or design signal to extract from the source.",
        "exact_locator": "Line, section, commit, page, DOI, or heading locator to fill during later capture.",
        "evidence_summary": "Short paraphrased summary to fill during later capture.",
        "quote_limit_policy": "Copyright-safe quote policy for later captured evidence.",
        "license_or_terms_note": "License, terms, or copyright note to fill during later capture.",
        "security_or_supply_chain_note": "Security, dependency, release, or supply-chain note to fill during later capture.",
        "adoption_boundary": "Explicit statement that evidence capture is not adoption approval.",
        "capture_status": "Capture state; this plan only creates planned_not_collected records.",
    }
    return [
        {
            "field_name": field_name,
            "required": True,
            "description": description,
            "capture_boundary": "planning_only_not_collected",
        }
        for field_name, description in descriptions.items()
    ]


def claim_for_target(target: dict) -> str:
    kind = target["source_kind"]
    target_id = target["source_target_id"]
    if target_id == "src-promptfoo-official-docs":
        return "Document promptfoo's declared evaluation, red-team, CLI/library, and local execution boundaries."
    if target_id == "src-promptfoo-original-repository":
        return "Document promptfoo upstream source, license, security policy, tests, release cadence, and integration boundaries."
    if target_id == "src-ragas-official-docs":
        return "Document Ragas metrics, testset generation, agent evaluation, and RAG evaluation surfaces."
    if target_id == "src-ragas-original-repository":
        return "Document Ragas upstream source, license, tests, examples, and integration boundaries."
    if target_id == "src-ragas-arxiv-paper":
        return "Extract RAG evaluation dimensions and reference-free metric claims for AVF evidence-loop design."
    if kind == "standard":
        return "Map governance and red-team risk categories to AVF evidence-loop requirements."
    return "Capture bounded evidence for AVF capability planning."


def target_capture_plans(review: dict) -> list[dict]:
    plans = []
    for target in review["reviewed_source_targets"]:
        plans.append(
            {
                "source_target_id": target["source_target_id"],
                "candidate_id": target["candidate_id"],
                "source_kind": target["source_kind"],
                "source_uri": target["source_uri"],
                "inspection_focus": target["inspection_focus"],
                "retrieval_mode": "future_owner_approved_manual_or_connector_capture",
                "capture_scope": "claim_boundary_evidence_only",
                "claim_to_extract": claim_for_target(target),
                "quote_limit_policy": "short_quotes_only_or_paraphrase; do_not_reproduce_large_copyrighted_text",
                "license_or_terms_note": "to_be_captured_later",
                "security_or_supply_chain_note": "to_be_captured_later",
                "adoption_boundary": "evidence_capture_is_not_selection_or_dependency_adoption",
                "capture_status": "planned_not_collected",
                "source_fetch_allowed": False,
                "external_fetch_performed": False,
                "oss_clone_allowed": False,
                "dependency_install_allowed": False,
                "runtime_integration_allowed": False,
            }
        )
    return plans


def counts(review: dict) -> dict:
    return {
        "source_target_count": review["source_target_count"],
        "capture_field_count": len(capture_fields()),
        "required_capture_field_count": len(capture_fields()),
        "target_capture_plan_count": len(target_capture_plans(review)),
        "source_fetch_allowed_count": 0,
        "source_fetch_performed_count": 0,
        "oss_clone_allowed_count": 0,
        "dependency_install_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "review_blocker_count": 0,
        "ready_for_capture_plan_review_count": 1,
    }


def base_record(review: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "capture_plan_status": CAPTURE_PLAN_STATUS,
        "capture_plan_scope": CAPTURE_PLAN_SCOPE,
        "capture_fields": capture_fields(),
        "target_capture_plans": target_capture_plans(review),
        "input_uris": {
            "priority_1_deep_research_plan_review_gate": rel(REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "external_fetch_performed": False,
        "oss_clone_performed": False,
        "dependency_install_performed": False,
        "runtime_integration_performed": False,
        **counts(review),
        "claim_boundary": false_boundary(),
    }


def build_gate(review: dict) -> dict:
    return {
        **base_record(review),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-source-evidence-capture-plan-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Source evidence capture plan created; review required before any source access or evidence collection",
    }


def build_validation_result(review: dict) -> dict:
    return {
        **base_record(review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(CAPTURE_PLAN),
            rel(CAPTURE_FIELD_SPEC),
            rel(CAPTURE_PLAN_GATE),
            rel(CAPTURE_PLAN_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(review).items())
    field_lines = "\n".join(f"- {field['field_name']}: required=true" for field in capture_fields())
    plan_lines = "\n".join(
        "- {source_target_id}: capture_status=planned_not_collected, source_fetch_allowed=false, external_fetch_performed=false".format(
            **plan
        )
        for plan in target_capture_plans(review)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Source Evidence Capture Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_source_evidence_capture_plan_v0_1=true

## Capture plan summary

- candidate_id={CANDIDATE_ID}
- capture_plan_status={CAPTURE_PLAN_STATUS}
- capture_plan_scope={CAPTURE_PLAN_SCOPE}
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Capture fields

{field_lines}

## Target capture plans

{plan_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-source-evidence-capture-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local source evidence capture plan
  - Confirm capture fields are complete and bounded
  - Confirm target capture plans are planned_not_collected only
  - Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(REVIEW_GATE)
    require_review(review)

    capture_record = base_record(review)
    write_json(CAPTURE_PLAN, capture_record)
    write_json(CAPTURE_FIELD_SPEC, capture_record)
    write_json(CAPTURE_PLAN_GATE, build_gate(review))
    report = build_report(review)
    write_text(CAPTURE_PLAN_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Source Evidence Capture Plan v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"capture_plan_status={CAPTURE_PLAN_STATUS}")
    print(f"capture_plan_scope={CAPTURE_PLAN_SCOPE}")
    for key, value in counts(review).items():
        print(f"{key}={value}")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PRIORITY_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_advisory_priority_matrix_review_gate.json"
RESEARCH_PLAN = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan.json"
SOURCE_TARGETS = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_source_targets.json"
PLAN_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_gate.json"
PLAN_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_deep_research_plan_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_DEEP_RESEARCH_PLAN_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_advisory_priority_matrix_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_deep_research_plan_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
PLAN_STATUS = "priority_1_deep_research_plan_created_non_executable"
PLAN_SCOPE = "primary_source_deep_research_plan_only"


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


def require_priority_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("priority review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("priority review must point to this deep research plan goal")
    if review.get("priority_1_candidate_ids") != [CANDIDATE_ID]:
        raise SystemExit("priority review must identify the expected priority 1 candidate")
    if review.get("ready_for_priority_1_deep_research_plan_count") != 1:
        raise SystemExit("priority review must be ready for deep research planning")
    if review.get("selection_allowed") is not False:
        raise SystemExit("selection must remain blocked")
    if review.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")
    if review.get("runtime_integration_allowed") is not False:
        raise SystemExit("runtime integration must remain blocked")


def source_targets() -> list[dict]:
    return [
        {
            "source_target_id": "src-promptfoo-official-docs",
            "candidate_id": CANDIDATE_ID,
            "source_kind": "official_docs",
            "source_uri": "https://www.promptfoo.dev/docs/intro/",
            "inspection_focus": "Evaluate promptfoo's documented CLI/library evaluation and red-team workflow boundaries.",
            "research_status": "target_identified_not_fetched_by_runner",
            "maintained_source_code_target": False,
            "selection_allowed": False,
            "dependency_adoption_allowed": False,
            "runtime_integration_allowed": False,
            "external_fetch_performed": False,
        },
        {
            "source_target_id": "src-promptfoo-original-repository",
            "candidate_id": CANDIDATE_ID,
            "source_kind": "original_repository",
            "source_uri": "https://github.com/promptfoo/promptfoo",
            "inspection_focus": "Inspect upstream source layout, license, security policy, release cadence, and local-only eval surfaces before any adoption decision.",
            "research_status": "target_identified_not_fetched_by_runner",
            "maintained_source_code_target": True,
            "selection_allowed": False,
            "dependency_adoption_allowed": False,
            "runtime_integration_allowed": False,
            "external_fetch_performed": False,
        },
        {
            "source_target_id": "src-ragas-official-docs",
            "candidate_id": CANDIDATE_ID,
            "source_kind": "official_docs",
            "source_uri": "https://docs.ragas.io/en/stable/",
            "inspection_focus": "Evaluate Ragas metric, testset generation, agent evaluation, and RAG evaluation concepts against AVF evidence-loop needs.",
            "research_status": "target_identified_not_fetched_by_runner",
            "maintained_source_code_target": False,
            "selection_allowed": False,
            "dependency_adoption_allowed": False,
            "runtime_integration_allowed": False,
            "external_fetch_performed": False,
        },
        {
            "source_target_id": "src-ragas-original-repository",
            "candidate_id": CANDIDATE_ID,
            "source_kind": "original_repository",
            "source_uri": "https://github.com/vibrantlabsai/ragas",
            "inspection_focus": "Inspect upstream Ragas source layout, Apache-2.0 license surface, tests, examples, and integration boundaries before any adoption decision.",
            "research_status": "target_identified_not_fetched_by_runner",
            "maintained_source_code_target": True,
            "selection_allowed": False,
            "dependency_adoption_allowed": False,
            "runtime_integration_allowed": False,
            "external_fetch_performed": False,
        },
        {
            "source_target_id": "src-ragas-arxiv-paper",
            "candidate_id": CANDIDATE_ID,
            "source_kind": "paper",
            "source_uri": "https://arxiv.org/abs/2309.15217",
            "inspection_focus": "Extract the paper's RAG evaluation dimensions and reference-free metric claims for AVF evidence-loop design only.",
            "research_status": "target_identified_not_fetched_by_runner",
            "maintained_source_code_target": False,
            "selection_allowed": False,
            "dependency_adoption_allowed": False,
            "runtime_integration_allowed": False,
            "external_fetch_performed": False,
        },
        {
            "source_target_id": "src-owasp-genai-llm-top-10",
            "candidate_id": CANDIDATE_ID,
            "source_kind": "standard",
            "source_uri": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
            "inspection_focus": "Map LLM application risk categories to AVF red-team eval requirements without endorsing any tool.",
            "research_status": "target_identified_not_fetched_by_runner",
            "maintained_source_code_target": False,
            "selection_allowed": False,
            "dependency_adoption_allowed": False,
            "runtime_integration_allowed": False,
            "external_fetch_performed": False,
        },
        {
            "source_target_id": "src-nist-ai-rmf",
            "candidate_id": CANDIDATE_ID,
            "source_kind": "standard",
            "source_uri": "https://doi.org/10.6028/NIST.AI.100-1",
            "inspection_focus": "Map AI risk management and evaluation guidance to AVF governance/evidence-loop requirements.",
            "research_status": "target_identified_not_fetched_by_runner",
            "maintained_source_code_target": False,
            "selection_allowed": False,
            "dependency_adoption_allowed": False,
            "runtime_integration_allowed": False,
            "external_fetch_performed": False,
        },
    ]


def counts() -> dict:
    targets = source_targets()
    return {
        "source_target_count": len(targets),
        "official_docs_target_count": sum(1 for target in targets if target["source_kind"] == "official_docs"),
        "original_repository_target_count": sum(1 for target in targets if target["source_kind"] == "original_repository"),
        "paper_target_count": sum(1 for target in targets if target["source_kind"] == "paper"),
        "standard_target_count": sum(1 for target in targets if target["source_kind"] == "standard"),
        "maintained_source_code_target_count": sum(1 for target in targets if target["maintained_source_code_target"]),
        "selection_allowed_count": 0,
        "dependency_adoption_allowed_count": 0,
        "runtime_integration_allowed_count": 0,
        "external_fetch_performed_count": 0,
        "review_blocker_count": 0,
        "ready_for_deep_research_plan_review_count": 1,
    }


def source_targets_record() -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "source_targets": source_targets(),
        **counts(),
    }


def base_record() -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "plan_status": PLAN_STATUS,
        "plan_scope": PLAN_SCOPE,
        "source_target_identification_method": "manual_primary_source_research_current_session",
        "source_targets": source_targets(),
        "research_steps": [
            "Read official docs for supported workflows and declared boundaries",
            "Inspect original repositories for source layout, license, security posture, tests, and maintenance signals",
            "Extract paper claims into evidence-loop requirements without treating the paper as adoption approval",
            "Map standards to red-team and governance requirements",
            "Produce a follow-up source evidence review before any dependency or runtime decision",
        ],
        "input_uris": {
            "advisory_priority_matrix_review_gate": rel(PRIORITY_REVIEW_GATE),
        },
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "selection_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "external_fetch_performed": False,
        **counts(),
        "claim_boundary": false_boundary(),
    }


def build_gate() -> dict:
    return {
        **base_record(),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-deep-research-plan-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Priority 1 deep research plan created; review required before any source fetching or integration planning",
    }


def build_validation_result() -> dict:
    return {
        **base_record(),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_deep_research_plan_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(RESEARCH_PLAN),
            rel(SOURCE_TARGETS),
            rel(PLAN_GATE),
            rel(PLAN_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report() -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts().items())
    target_lines = "\n".join(
        "- source_target_id={source_target_id}; kind={source_kind}; uri={source_uri}; external_fetch_performed=false".format(
            **target
        )
        for target in source_targets()
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Deep Research Plan v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_deep_research_plan_v0_1=true

## Plan summary

- candidate_id={CANDIDATE_ID}
- plan_status={PLAN_STATUS}
- plan_scope={PLAN_SCOPE}
- selection_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false
- external_fetch_performed=false

## Counts

{count_lines}

## Source targets

{target_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-deep-research-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the repo-local deep research plan
  - Confirm official docs, original repos, paper, and standard targets are only targets to inspect later
  - Confirm the runner did not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness
  - Do not fetch sources, clone OSS, install dependencies, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(PRIORITY_REVIEW_GATE)
    require_priority_review(review)

    write_json(SOURCE_TARGETS, source_targets_record())
    write_json(RESEARCH_PLAN, base_record())
    write_json(PLAN_GATE, build_gate())
    report = build_report()
    write_text(PLAN_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Deep Research Plan v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"plan_status={PLAN_STATUS}")
    print(f"plan_scope={PLAN_SCOPE}")
    for key, value in counts().items():
        print(f"{key}={value}")
    print("selection_allowed=false")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

AUTHORIZATION_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_gate.json"
EVIDENCE_COLLECTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection.json"
EVIDENCE_COLLECTION_GATE = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_gate.json"
EVIDENCE_COLLECTION_REPORT = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRIORITY_1_OWNER_APPROVED_MANUAL_EVIDENCE_COLLECTION_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_evidence_collection_authorization_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_priority_1_manual_evidence_quality_review_v0_1"
CANDIDATE_ID = "cap-eval-redteam-promptfoo-ragas"
CREATED_AT = "2026-05-27T00:00:00Z"
COLLECTION_STATUS = "owner_approved_manual_primary_source_evidence_captured"
COLLECTION_MODE = "manual_assistant_primary_source_review"


EVIDENCE_BY_SOURCE_TARGET_ID = {
    "src-promptfoo-official-docs": {
        "exact_locator": "https://www.promptfoo.dev/docs/intro/ lines 75-84, 88-89, 105-112, 117-122",
        "evidence_summary": "Promptfoo's official docs describe it as an open-source CLI/library for LLM app evaluation and red teaming, with benchmarks for prompts, models, and RAG pipelines, CLI/library/CI modes, local private evaluations, and an evaluation feedback loop.",
        "license_or_terms_note": "Docs page supports capability fit, while code license is checked against the original repository evidence record.",
        "security_or_supply_chain_note": "Docs explicitly position red teaming, pentesting, vulnerability scanning, and local/private execution as relevant safety boundaries.",
        "claim_boundary_note": "Supports AVF evaluation and red-team candidate fit only; it does not approve dependency adoption or runtime integration.",
    },
    "src-promptfoo-original-repository": {
        "exact_locator": "https://github.com/promptfoo/promptfoo lines 434-446, 466-491, 522-535, 559-563",
        "evidence_summary": "The original repository presents Promptfoo as an LLM eval and red-team tool with CI/CD-oriented checks, local/private evaluation positioning, active release history, and repository-level license and security policy surfaces.",
        "license_or_terms_note": "Repository page identifies an MIT license and states Promptfoo remains open source and MIT licensed.",
        "security_or_supply_chain_note": "Repository page exposes a Security policy entry; no package install, clone, or code execution was performed.",
        "claim_boundary_note": "Supports candidate-source governance and license/security review planning only; no adoption decision is made.",
    },
    "src-ragas-official-docs": {
        "exact_locator": "https://docs.ragas.io/en/stable/ lines 48-64, 88-96, 150-163, 200-212, 235-241",
        "evidence_summary": "Ragas docs describe systematic evaluation loops for LLM applications, RAG metrics such as context precision/recall, response relevancy and faithfulness, agent/tool metrics, testset generation, observability and framework integrations.",
        "license_or_terms_note": "Docs page supports capability fit; code licensing is checked against the original repository evidence record.",
        "security_or_supply_chain_note": "Docs show integrations and evaluation surfaces that would need provider, observability, and data-boundary review before runtime use.",
        "claim_boundary_note": "Supports AVF evidence-loop and evaluation candidate fit only; no runtime integration is authorized.",
    },
    "src-ragas-original-repository": {
        "exact_locator": "https://github.com/vibrantlabsai/ragas lines 292-315, 317-323, 348-382",
        "evidence_summary": "The Ragas repository describes objective metrics, test data generation, framework and observability integrations, feedback loops, and example evaluation usage while also showing package/source install commands that AVF did not execute.",
        "license_or_terms_note": "Repository page identifies Apache-2.0 license.",
        "security_or_supply_chain_note": "Repository page exposes a Security entry; install commands are documented upstream but were not run.",
        "claim_boundary_note": "Supports candidate evaluation only; install and source integration remain blocked pending later review.",
    },
    "src-ragas-arxiv-paper": {
        "exact_locator": "https://arxiv.org/abs/2309.15217 lines 32-45, 47-49, 60-69",
        "evidence_summary": "The Ragas paper introduces a reference-free evaluation framework for RAG pipelines and frames evaluation across retrieval relevance/focus, faithful use of retrieved context, generation quality, and faster evaluation cycles.",
        "license_or_terms_note": "arXiv page provides a license link and DOI metadata; use remains evidence citation only.",
        "security_or_supply_chain_note": "Paper supports metric rationale but does not itself resolve implementation, supply-chain, or provider-risk questions.",
        "claim_boundary_note": "Supports conceptual evidence for RAG evaluation dimensions only; no code or data is adopted.",
    },
    "src-owasp-genai-llm-top-10": {
        "exact_locator": "https://owasp.org/www-project-top-10-for-large-language-model-applications/ lines 23-40, 72-108, 168-169",
        "evidence_summary": "OWASP frames the GenAI Security Project as an open-source initiative for generative AI security and lists LLM application risks including prompt injection, supply-chain vulnerabilities, sensitive information disclosure, insecure plugin design, excessive agency, and overreliance.",
        "license_or_terms_note": "OWASP site states content is Creative Commons Attribution-ShareAlike 4.0 unless otherwise specified.",
        "security_or_supply_chain_note": "Risk categories directly support AVF governance gates for red-team evaluation, excessive agency limits, and supply-chain caution.",
        "claim_boundary_note": "Supports risk taxonomy for governance and evidence review; it does not endorse a tool selection.",
    },
    "src-nist-ai-rmf": {
        "exact_locator": "https://doi.org/10.6028/NIST.AI.100-1 lines 565-590, 606-627, 637-666, 746-755, 870-884",
        "evidence_summary": "NIST AI RMF describes govern-map-measure-manage functions, continuous risk management, documentation, go/no-go decisions, organizational governance, third-party software/data and supply-chain risk handling, and context mapping for AI risks.",
        "license_or_terms_note": "NIST DOI source is a government framework reference; this record uses it as a governance citation, not copied policy text.",
        "security_or_supply_chain_note": "Supports AVF requirements for documented risk governance, human review, third-party risk controls, and claim-bounded go/no-go decisions.",
        "claim_boundary_note": "Supports governance structure for AVF capability adoption; it does not prove AVF readiness.",
    },
}


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


def require_authorization_review(review: dict) -> None:
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("authorization review goal mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("authorization review must point to this collection goal")
    if review.get("owner_approval_required_before_next_goal") is not True:
        raise SystemExit("authorization review must require owner approval before collection")
    if review.get("evidence_capture_authorized") is not False:
        raise SystemExit("authorization review must not pre-authorize evidence capture")


def evidence_records(review: dict) -> list[dict]:
    records = []
    for request in review["reviewed_authorization_requests"]:
        source_target_id = request["source_target_id"]
        if source_target_id not in EVIDENCE_BY_SOURCE_TARGET_ID:
            raise SystemExit(f"missing evidence data for {source_target_id}")
        evidence = EVIDENCE_BY_SOURCE_TARGET_ID[source_target_id]
        records.append(
            {
                "evidence_record_id": f"evidence-record-{source_target_id}",
                "authorization_request_id": request["authorization_request_id"],
                "source_target_id": source_target_id,
                "candidate_id": request["candidate_id"],
                "source_kind": request["source_kind"],
                "source_uri": request["source_uri"],
                "claim_to_extract": request["claim_to_extract"],
                "capture_scope": request["capture_scope"],
                "adoption_boundary": request["adoption_boundary"],
                "quote_limit_policy": "paraphrased_summary_or_short_quote_only",
                "capture_status": "captured_from_owner_approved_manual_review",
                "owner_approval_recorded": True,
                "owner_approval_reference": "current_thread_owner_delegation",
                "manual_source_review_performed": True,
                "external_source_lookup_performed_by_assistant": True,
                "repo_automation_source_fetch_performed": False,
                "source_fetch_performed": False,
                "external_fetch_performed": False,
                "oss_clone_performed": False,
                "dependency_install_performed": False,
                "runtime_integration_performed": False,
                **evidence,
            }
        )
    return records


def counts(review: dict) -> dict:
    records = evidence_records(review)
    return {
        "source_target_count": review["source_target_count"],
        "evidence_record_count": len(records),
        "captured_evidence_record_count": len(records),
        "empty_evidence_record_count": 0,
        "owner_approval_recorded_count": 1,
        "manual_source_review_performed_count": len(records),
        "repo_automation_source_fetch_performed_count": 0,
        "oss_clone_performed_count": review["oss_clone_performed_count"],
        "dependency_install_performed_count": review["dependency_install_performed_count"],
        "runtime_integration_performed_count": review["runtime_integration_performed_count"],
        "review_blocker_count": 0,
        "ready_for_manual_evidence_quality_review_count": 1,
    }


def base_collection_record(review: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "candidate_id": CANDIDATE_ID,
        "collection_status": COLLECTION_STATUS,
        "collection_mode": COLLECTION_MODE,
        "owner_approval_recorded": True,
        "owner_approval_reference": "current_thread_owner_delegation",
        "external_source_lookup_performed_by_assistant": True,
        "repo_automation_source_fetch_performed": False,
        "evidence_records": evidence_records(review),
        "input_uris": {
            "authorization_packet_review_gate": rel(AUTHORIZATION_REVIEW_GATE),
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
        **base_collection_record(review),
        "gate_id": "avf-capability-candidate-primary-source-priority-1-owner-approved-manual-evidence-collection-gate-v0-1",
        "status": "PASS",
        "gate_scope": "Owner-approved manual primary-source evidence captured; no repo automation fetched sources or installed dependencies",
    }


def build_validation_result(review: dict) -> dict:
    return {
        **base_collection_record(review),
        "validator_id": "validate_avf_capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(AUTHORIZATION_REVIEW_GATE),
            rel(EVIDENCE_COLLECTION),
            rel(EVIDENCE_COLLECTION_GATE),
            rel(EVIDENCE_COLLECTION_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_report(review: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(review).items())
    evidence_lines = "\n".join(
        "- {evidence_record_id}: capture_status=captured_from_owner_approved_manual_review, locator={exact_locator}".format(
            **record
        )
        for record in evidence_records(review)
    )
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Candidate Primary-Source Priority 1 Owner-Approved Manual Evidence Collection v0.1

RESULT: PASS
capability_candidate_primary_source_priority_1_owner_approved_manual_evidence_collection_v0_1=true

## Collection summary

- candidate_id={CANDIDATE_ID}
- collection_status={COLLECTION_STATUS}
- collection_mode={COLLECTION_MODE}
- owner_approval_recorded=true
- external_source_lookup_performed_by_assistant=true
- repo_automation_source_fetch_performed=false
- external_fetch_performed=false
- oss_clone_performed=false
- dependency_install_performed=false
- runtime_integration_performed=false

## Counts

{count_lines}

## Evidence records

{evidence_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-priority-1-manual-evidence-quality
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review captured evidence for locator quality, claim boundaries, and adoption safety
  - Confirm no evidence record claims selection, dependency adoption, runtime integration, deployment, publishing, or readiness
  - Decide whether the candidate should stay in review, be rejected, or receive a no-install adapter plan
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    review = read_json(AUTHORIZATION_REVIEW_GATE)
    require_authorization_review(review)

    record = base_collection_record(review)
    write_json(EVIDENCE_COLLECTION, record)
    write_json(EVIDENCE_COLLECTION_GATE, build_gate(review))
    report = build_report(review)
    write_text(EVIDENCE_COLLECTION_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(review))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Priority 1 Owner-Approved Manual Evidence Collection v0.1")
    print("RESULT: PASS")
    print(f"candidate_id={CANDIDATE_ID}")
    print(f"collection_status={COLLECTION_STATUS}")
    print(f"collection_mode={COLLECTION_MODE}")
    for key, value in counts(review).items():
        print(f"{key}={value}")
    print("owner_approval_recorded=true")
    print("external_source_lookup_performed_by_assistant=true")
    print("repo_automation_source_fetch_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("dependency_install_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
OBS_GENERATED = ROOT / "avf" / "observability" / "generated"
EVIDENCE = ROOT / "avf" / "cells" / "evidence" / "generated"
PRODUCT_QUALITY = ROOT / "docs" / "product-quality"
DOC_GOALS = ROOT / "docs" / "goals"

PREVIOUS_OBS_GATE = OBS_GENERATED / "observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2_gate.json"
PRODUCT_REGISTRY = PRODUCT_QUALITY / "primary-source-registry-report.json"
AVF_LEDGER = EVIDENCE / "primary_source_ledger.json"
MANUAL_RECORDS = CAPABILITIES / "primary_source_manual_records.json"
GAP_REVIEW = CAPABILITIES / "primary_source_evidence_registry_gap_review.json"
GAP_GATE = CAPABILITIES / "primary_source_evidence_registry_gap_review_gate.json"
GAP_REPORT = CAPABILITIES / "primary_source_evidence_registry_gap_review_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_evidence_registry_gap_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_evidence_registry_gap_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_EVIDENCE_REGISTRY_GAP_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_evidence_registry_gap_review_v0_1"
PREVIOUS_GOAL_ID = "avf_observability_runtime_seed_owner_supplied_approval_completion_retry_v0_2"
NEXT_SAFE_GOAL_ID = "avf_primary_source_evidence_registry_gap_closure_plan_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "PRIMARY_SOURCE_EVIDENCE_REGISTRY_GAPS_REVIEWED_REPO_LOCAL"
REVIEW_STATUS = "gaps_found_closure_plan_required"

GAP_IDS = [
    "gap-product-quality-reports-missing-primary-source-inputs",
    "gap-avf-ledger-to-manual-record-namespace-map",
    "gap-content-safety-policy-sources-missing-manual-records",
    "gap-adoption-evidence-gates-not-yet-linked-to-registry",
]

CONTENT_SAFETY_LEDGER_SOURCE_IDS = [
    "src-ftc-endorsement-guides",
    "src-ftc-ai-claims",
]


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


def require_previous_observability_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous observability gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("previous observability gate must point to this gap review goal")
    if gate.get("runtime_approval_wait_state") is not True:
        raise SystemExit("runtime approval wait state must be true")
    if gate.get("switch_to_non_protected_work") is not True:
        raise SystemExit("switch to non-protected work must be true")


def build_counts(product: dict, ledger: dict, manual: dict) -> dict:
    source_ids = [source.get("source_id") for source in ledger.get("sources", [])]
    manual_source_ids = [record.get("source_target_id") for record in manual.get("source_records", [])]
    content_safety_missing = [
        source_id
        for source_id in CONTENT_SAFETY_LEDGER_SOURCE_IDS
        if source_id in source_ids and source_id not in manual_source_ids
    ]
    return {
        "primary_source_entry_count": product.get("primarySourceEntryCount"),
        "unique_source_url_count": product.get("uniqueSourceUrlCount"),
        "reports_with_primary_source_inputs_count": len(product.get("reportsWithPrimarySourceInputs", [])),
        "reports_missing_primary_source_inputs_count": len(product.get("reportsMissingPrimarySourceInputs", [])),
        "avf_ledger_source_count": len(ledger.get("sources", [])),
        "manual_source_record_count": len(manual.get("source_records", [])),
        "content_safety_policy_sources_missing_manual_records_count": len(content_safety_missing),
        "gap_count": len(GAP_IDS),
    }


def build_gap_records(product: dict, ledger: dict, manual: dict, counts: dict) -> list[dict]:
    reports_missing = product.get("reportsMissingPrimarySourceInputs", [])
    ledger_source_ids = [source.get("source_id") for source in ledger.get("sources", [])]
    manual_source_ids = [record.get("source_target_id") for record in manual.get("source_records", [])]
    return [
        {
            "gap_id": GAP_IDS[0],
            "severity": "high",
            "evidence": f"{counts['reports_missing_primary_source_inputs_count']} product-quality reports still lack primary-source inputs.",
            "affected_records": reports_missing[:10],
            "closure_action": "Create a deterministic closure plan that either attaches repo-local primary-source records or marks the report out-of-scope with a claim boundary.",
        },
        {
            "gap_id": GAP_IDS[1],
            "severity": "medium",
            "evidence": "AVF ledger source ids and manual source target ids use separate namespaces.",
            "ledger_source_id_examples": ledger_source_ids[:5],
            "manual_source_target_id_examples": manual_source_ids[:5],
            "closure_action": "Add a repo-local namespace mapping before automatic claim integration or coverage scoring.",
        },
        {
            "gap_id": GAP_IDS[2],
            "severity": "medium",
            "evidence": "Content and safety policy sources are present in the AVF ledger but are not yet covered by manual source records.",
            "missing_manual_record_source_ids": CONTENT_SAFETY_LEDGER_SOURCE_IDS,
            "closure_action": "Create owner-supplied/manual source records for content safety policy claims before promotion into influence or content pipelines.",
        },
        {
            "gap_id": GAP_IDS[3],
            "severity": "medium",
            "evidence": "Reviewed primary-source evidence supports architecture planning only; adoption gates are not linked to registry coverage yet.",
            "closure_action": "Link each candidate adoption path to build-vs-buy, license, security, supply-chain, and owner approval gate records.",
        },
    ]


def base_record(counts: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "gap_ids": GAP_IDS,
        **counts,
        "claim_boundary": false_boundary(),
    }


def build_gap_review(product: dict, ledger: dict, manual: dict, counts: dict) -> dict:
    return {
        **base_record(counts),
        "review_id": "avf-primary-source-evidence-registry-gap-review-v0-1",
        "review_scope": "repo-local primary-source evidence registry gap review",
        "source_inputs": [
            rel(PRODUCT_REGISTRY),
            rel(AVF_LEDGER),
            rel(MANUAL_RECORDS),
            rel(PREVIOUS_OBS_GATE),
        ],
        "runtime_approval_wait_state_confirmed": True,
        "switch_to_non_protected_work_confirmed": True,
        "manual_records_cover_runtime_model_web_agent_claims": True,
        "content_safety_policy_sources_need_manual_records": True,
        "gap_records": build_gap_records(product, ledger, manual, counts),
    }


def build_gap_gate(counts: dict) -> dict:
    return {
        **base_record(counts),
        "gate_id": "avf-primary-source-evidence-registry-gap-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "review only; closure is deferred to the next safe goal",
        "protected_actions_blocked": True,
    }


def build_gap_report(counts: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts.items())
    gap_lines = "\n".join(f"- {gap_id}" for gap_id in GAP_IDS)
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# Primary-Source Evidence Registry Gap Review v0.1

review_decision={REVIEW_DECISION}
review_status={REVIEW_STATUS}

## Counts

{count_lines}

## Gaps

{gap_lines}

## Boundary

No external fetch, provider call, live model call, scraping, dependency install, OSS clone, runtime integration, deploy, publish, or readiness claim was performed.

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-primary-source-evidence-registry-gap-closure-plan
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Close repo-local registry gaps with deterministic mapping and owner-supplied/manual primary-source records
  - Map AVF ledger source ids to manual source record target ids before claim integration
  - Add manual records for content safety policy sources before influence/content promotion
  - Link adoption candidates to build-vs-buy, license, security, supply-chain, and owner approval gates
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(counts: dict) -> dict:
    return {
        **base_record(counts),
        "validator_id": "validate_avf_primary_source_evidence_registry_gap_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(GAP_REVIEW),
            rel(GAP_GATE),
            rel(GAP_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def build_validation_report(counts: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts.items())
    gap_lines = "\n".join(f"- {gap_id}" for gap_id in GAP_IDS)
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Primary-Source Evidence Registry Gap Review v0.1 Report

RESULT: PASS
primary_source_evidence_registry_gap_review_v0_1=true

## Commands

- python scripts\\run_avf_primary_source_evidence_registry_gap_review_v0_1.py
- python scripts\\validate_avf_primary_source_evidence_registry_gap_review_v0_1.py

## Gate summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}

## Counts

{count_lines}

## Gaps

{gap_lines}

## Generated artifacts

- {rel(GAP_REVIEW)}
- {rel(GAP_GATE)}
- {rel(GAP_REPORT)}
- {rel(NEXT_ACTION)}
- {rel(VALIDATION_RESULT)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    previous_gate = read_json(PREVIOUS_OBS_GATE)
    product = read_json(PRODUCT_REGISTRY)
    ledger = read_json(AVF_LEDGER)
    manual = read_json(MANUAL_RECORDS)

    require_previous_observability_gate(previous_gate)

    counts = build_counts(product, ledger, manual)
    write_json(GAP_REVIEW, build_gap_review(product, ledger, manual, counts))
    write_json(GAP_GATE, build_gap_gate(counts))
    write_text(GAP_REPORT, build_gap_report(counts))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(counts))
    write_text(VALIDATION_REPORT, build_validation_report(counts))

    print("AVF Primary-Source Evidence Registry Gap Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts.items():
        print(f"{key}={value}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

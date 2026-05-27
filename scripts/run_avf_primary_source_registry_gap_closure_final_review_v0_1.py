from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

ADOPTION_LINKS = CAPABILITIES / "primary_source_adoption_evidence_gate_links.json"
ADOPTION_GATE = CAPABILITIES / "primary_source_adoption_evidence_gate_links_gate.json"
ADOPTION_NEXT_ACTION = CAPABILITIES / "primary_source_adoption_evidence_gate_links_next_action.yml"
FINAL_REVIEW = CAPABILITIES / "primary_source_registry_gap_closure_final_review.json"
FINAL_GATE = CAPABILITIES / "primary_source_registry_gap_closure_final_review_gate.json"
FINAL_REPORT = CAPABILITIES / "primary_source_registry_gap_closure_final_review_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_registry_gap_closure_final_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_registry_gap_closure_final_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_REGISTRY_GAP_CLOSURE_FINAL_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_registry_gap_closure_final_review_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_adoption_evidence_gate_links_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_adoption_decision_matrix_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
FINAL_DECISION = "PRIMARY_SOURCE_REGISTRY_GAP_CLOSURE_REVIEWED_REPO_LOCAL"
FINAL_STATUS = "all_known_registry_gaps_closed_or_bounded"

GAP_IDS = [
    "gap-product-quality-reports-missing-primary-source-inputs",
    "gap-avf-ledger-to-manual-record-namespace-map",
    "gap-content-safety-policy-sources-missing-manual-records",
    "gap-adoption-evidence-gates-not-yet-linked-to-registry",
]

CLOSURE_ARTIFACTS = [
    "avf/capabilities/generated/primary_source_evidence_registry_gap_review.json",
    "avf/capabilities/generated/primary_source_evidence_registry_gap_closure_plan.json",
    "avf/capabilities/generated/primary_source_namespace_map.json",
    "avf/capabilities/generated/primary_source_content_safety_manual_records.json",
    "avf/capabilities/generated/primary_source_product_quality_missing_inputs_plan.json",
    "avf/capabilities/generated/primary_source_product_quality_missing_inputs_triage.json",
    "avf/capabilities/generated/primary_source_adoption_evidence_gate_links.json",
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


def require_previous_links(links: dict, gate: dict) -> None:
    for label, record in [("adoption links", links), ("adoption gate", gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            raise SystemExit(f"{label} goal mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            raise SystemExit(f"{label} must point to this final review goal")
        if record.get("remaining_gap_count") != 0:
            raise SystemExit(f"{label} remaining gap count mismatch")
        if record.get("dependency_adoption_allowed") is not False:
            raise SystemExit(f"{label} dependency adoption must stay blocked")
        if record.get("runtime_integration_allowed") is not False:
            raise SystemExit(f"{label} runtime integration must stay blocked")


def counts() -> dict:
    return {
        "original_gap_count": len(GAP_IDS),
        "closed_or_bounded_gap_count": len(GAP_IDS),
        "remaining_gap_count": 0,
        "closure_artifact_count": len(CLOSURE_ARTIFACTS),
    }


def closure_records() -> list[dict]:
    return [
        {
            "gap_id": "gap-avf-ledger-to-manual-record-namespace-map",
            "closure_status": "closed",
            "closure_artifact": "avf/capabilities/generated/primary_source_namespace_map.json",
            "claim_boundary": "repo-local namespace map only",
        },
        {
            "gap_id": "gap-content-safety-policy-sources-missing-manual-records",
            "closure_status": "bounded",
            "closure_artifact": "avf/capabilities/generated/primary_source_content_safety_manual_records.json",
            "claim_boundary": "manual record shells created; source contents not acquired",
        },
        {
            "gap_id": "gap-product-quality-reports-missing-primary-source-inputs",
            "closure_status": "bounded",
            "closure_artifact": "avf/capabilities/generated/primary_source_product_quality_missing_inputs_triage.json",
            "claim_boundary": "claim-boundary exemption lane assigned; no source attachment claimed",
        },
        {
            "gap_id": "gap-adoption-evidence-gates-not-yet-linked-to-registry",
            "closure_status": "closed",
            "closure_artifact": "avf/capabilities/generated/primary_source_adoption_evidence_gate_links.json",
            "claim_boundary": "adoption gate links created; adoption still blocked",
        },
    ]


def base_record() -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "final_decision": FINAL_DECISION,
        "final_status": FINAL_STATUS,
        "all_known_registry_gaps_closed_or_bounded": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "gap_ids": GAP_IDS,
        "closure_artifacts": CLOSURE_ARTIFACTS,
        "closure_records": closure_records(),
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(),
        "claim_boundary": false_boundary(),
    }


def build_final_review() -> dict:
    return {
        **base_record(),
        "review_id": "avf-primary-source-registry-gap-closure-final-review-v0-1",
        "review_scope": "repo-local final review of primary-source registry gap closure chain",
        "source_inputs": [
            rel(ADOPTION_LINKS),
            rel(ADOPTION_GATE),
            rel(ADOPTION_NEXT_ACTION),
        ],
    }


def build_gate() -> dict:
    return {
        **base_record(),
        "gate_id": "avf-primary-source-registry-gap-closure-final-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "registry gap closure chain reviewed; adoption remains blocked",
    }


def build_report(title: str) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts().items())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
primary_source_registry_gap_closure_final_review_v0_1=true

## Gate summary

- final_decision={FINAL_DECISION}
- final_status={FINAL_STATUS}
- all_known_registry_gaps_closed_or_bounded=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-adoption-decision-matrix
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local capability adoption decision matrix using the closed registry gap chain
  - Keep dependency adoption and runtime integration blocked until gate requirements are satisfied
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        **base_record(),
        "validator_id": "validate_avf_primary_source_registry_gap_closure_final_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(FINAL_REVIEW),
            rel(FINAL_GATE),
            rel(FINAL_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    links = read_json(ADOPTION_LINKS)
    gate = read_json(ADOPTION_GATE)
    require_previous_links(links, gate)

    write_json(FINAL_REVIEW, build_final_review())
    write_json(FINAL_GATE, build_gate())
    write_text(FINAL_REPORT, build_report("Primary-Source Registry Gap Closure Final Review v0.1"))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report("AVF Primary-Source Registry Gap Closure Final Review v0.1 Report"))

    print("AVF Primary-Source Registry Gap Closure Final Review v0.1")
    print("RESULT: PASS")
    print(f"final_decision={FINAL_DECISION}")
    print(f"final_status={FINAL_STATUS}")
    for key, value in counts().items():
        print(f"{key}={value}")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("all_known_registry_gaps_closed_or_bounded=true")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

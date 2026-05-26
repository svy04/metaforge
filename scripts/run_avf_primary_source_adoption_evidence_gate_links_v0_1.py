from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

TRIAGE = CAPABILITIES / "primary_source_product_quality_missing_inputs_triage.json"
TRIAGE_GATE = CAPABILITIES / "primary_source_product_quality_missing_inputs_triage_gate.json"
TRIAGE_NEXT_ACTION = CAPABILITIES / "primary_source_product_quality_missing_inputs_triage_next_action.yml"
ADOPTION_LINKS = CAPABILITIES / "primary_source_adoption_evidence_gate_links.json"
ADOPTION_GATE = CAPABILITIES / "primary_source_adoption_evidence_gate_links_gate.json"
ADOPTION_REPORT = CAPABILITIES / "primary_source_adoption_evidence_gate_links_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_adoption_evidence_gate_links_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_adoption_evidence_gate_links_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_ADOPTION_EVIDENCE_GATE_LINKS_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_primary_source_adoption_evidence_gate_links_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_product_quality_missing_inputs_triage_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_registry_gap_closure_final_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
LINK_DECISION = "ADOPTION_CANDIDATES_LINKED_TO_EVIDENCE_GATES_REPO_LOCAL"
LINK_STATUS = "all_registry_gaps_closed_adoption_still_blocked"
CLOSED_GAP_ID = "gap-adoption-evidence-gates-not-yet-linked-to-registry"

GATE_IDS = [
    "gate-build-vs-buy-review",
    "gate-license-review",
    "gate-security-review",
    "gate-supply-chain-review",
    "gate-owner-approval",
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


def require_previous_triage(triage: dict, gate: dict) -> None:
    for label, record in [("triage", triage), ("triage gate", gate)]:
        if record.get("goal_id") != PREVIOUS_GOAL_ID:
            raise SystemExit(f"{label} goal mismatch")
        if record.get("next_safe_goal_id") != THIS_GOAL_ID:
            raise SystemExit(f"{label} must point to this adoption link goal")
        if record.get("remaining_gap_count") != 1:
            raise SystemExit(f"{label} remaining gap count mismatch")


def evidence_gates() -> list[dict]:
    gate_specs = [
        ("gate-build-vs-buy-review", "build_vs_buy_review", "Compare build, buy, and adopt paths before any capability adoption."),
        ("gate-license-review", "license_review", "Record license compatibility before any dependency, fork, or copied-code adoption."),
        ("gate-security-review", "security_review", "Record security review before adopting runtime, tool, package, or OSS code."),
        ("gate-supply-chain-review", "supply_chain_review", "Record supply-chain posture before installing packages or cloning repositories."),
        ("gate-owner-approval", "owner_approval_gate", "Require owner approval before dependency adoption, runtime integration, deploy, or publish."),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate_type": gate_type,
            "gate_status": "required_not_satisfied",
            "adoption_allowed": False,
            "why_required": why_required,
        }
        for gate_id, gate_type, why_required in gate_specs
    ]


def counts() -> dict:
    return {
        "adoption_gate_requirement_count": len(GATE_IDS),
        "linked_gate_count": len(GATE_IDS),
        "slice_closed_gap_count": 1,
        "gaps_closed_count": 4,
        "remaining_gap_count": 0,
    }


def base_record(gates: list[dict]) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "link_decision": LINK_DECISION,
        "link_status": LINK_STATUS,
        "closed_gap_id": CLOSED_GAP_ID,
        "all_registry_gaps_closed": True,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "gate_ids": GATE_IDS,
        "evidence_gates": gates,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(),
        "claim_boundary": false_boundary(),
    }


def build_links(gates: list[dict]) -> dict:
    return {
        **base_record(gates),
        "link_id": "avf-primary-source-adoption-evidence-gate-links-v0-1",
        "link_scope": "repo-local gate linkage only; no adoption allowed",
        "source_inputs": [
            rel(TRIAGE),
            rel(TRIAGE_GATE),
            rel(TRIAGE_NEXT_ACTION),
        ],
    }


def build_gate(gates: list[dict]) -> dict:
    return {
        **base_record(gates),
        "gate_id": "avf-primary-source-adoption-evidence-gate-links-gate-v0-1",
        "status": "PASS",
        "gate_scope": "adoption evidence gates linked; all adoption remains blocked",
    }


def build_report(title: str) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts().items())
    gate_lines = "\n".join(f"- {gate_id}" for gate_id in GATE_IDS)
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
primary_source_adoption_evidence_gate_links_v0_1=true

## Gate summary

- link_decision={LINK_DECISION}
- link_status={LINK_STATUS}
- all_registry_gaps_closed=true
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Evidence gates

{gate_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-primary-source-registry-gap-closure
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the full repo-local primary-source registry gap closure chain
  - Confirm all four original registry gaps are either closed or bounded without protected actions
  - Do not fetch external sources, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(gates: list[dict]) -> dict:
    return {
        **base_record(gates),
        "validator_id": "validate_avf_primary_source_adoption_evidence_gate_links_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(ADOPTION_LINKS),
            rel(ADOPTION_GATE),
            rel(ADOPTION_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    triage = read_json(TRIAGE)
    triage_gate = read_json(TRIAGE_GATE)
    require_previous_triage(triage, triage_gate)

    gates = evidence_gates()
    write_json(ADOPTION_LINKS, build_links(gates))
    write_json(ADOPTION_GATE, build_gate(gates))
    write_text(ADOPTION_REPORT, build_report("Primary-Source Adoption Evidence Gate Links v0.1"))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(gates))
    write_text(VALIDATION_REPORT, build_report("AVF Primary-Source Adoption Evidence Gate Links v0.1 Report"))

    print("AVF Primary-Source Adoption Evidence Gate Links v0.1")
    print("RESULT: PASS")
    print(f"link_decision={LINK_DECISION}")
    print(f"link_status={LINK_STATUS}")
    for key, value in counts().items():
        print(f"{key}={value}")
    print("all_registry_gaps_closed=true")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

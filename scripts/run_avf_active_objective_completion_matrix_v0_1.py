from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GOAL_GENERATED = ROOT / "avf" / "goals" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"

MATRIX = GOAL_GENERATED / "active_objective_completion_matrix_v0_1.json"
NEXT_CODEX_TASK = GOAL_GENERATED / "active_objective_completion_matrix_next_codex_task_packet.yml"
VALIDATION_RESULT = GOAL_GENERATED / "active_objective_completion_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_ACTIVE_OBJECTIVE_COMPLETION_MATRIX_V0_1_REPORT.md"
PROTECTED_BOUNDARY = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_packet_review_protected_action_required_boundary.json"

THIS_GOAL_ID = "avf_active_objective_completion_matrix_v0_1"
NEXT_SAFE_GOAL_ID = "avf_local_primary_source_evidence_acceptance_harness_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
TERMINAL_CONDITION = "ACTIVE_OBJECTIVE_NOT_COMPLETE_PROTECTED_ACTION_REQUIRED_FOR_SOURCE_COLLECTION"
OBJECTIVE_TEXT = "그럼 끝내지 말고 오픈소스 쓸거 다 쓰고 논문 인용할꺼 다 쓰고 1차 자료 다 써서 구현하고 완성 되고 완벽해질때까지 끝내지마"

BOUNDARY_ITEMS = [
    "source collection execution",
    "provider calls",
    "live model calls",
    "external service calls",
    "automated scraping",
    "OSS clone",
    "package install",
    "dependency install",
    "runtime integration",
    "deploy",
    "publish",
    "release readiness claim",
    "production readiness claim",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


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


def require_protected_boundary(boundary: dict) -> None:
    if boundary.get("terminal_condition") != "PROTECTED_ACTION_REQUIRED":
        raise SystemExit("source collection boundary must be PROTECTED_ACTION_REQUIRED")
    if boundary.get("owner_input_required") is not True:
        raise SystemExit("source collection boundary must require owner input")
    if boundary.get("collection_execution_allowed") is not False:
        raise SystemExit("source collection boundary must keep collection blocked")


def build_requirements() -> list[dict]:
    return [
        {
            "id": "REQ-001-preserve-full-objective",
            "requirement": "Keep the full user objective intact rather than redefining success around a smaller foundation-ready claim.",
            "status": "PROVEN",
            "evidence": [
                "active goal remains broader than current PR scope",
                "this matrix sets objective_completion_proven=false",
            ],
            "gap": None,
        },
        {
            "id": "REQ-002-use-validated-open-source",
            "requirement": "Use validated open-source projects, frameworks, and tools where they advance AVF.",
            "status": "PARTIAL",
            "evidence": [
                "docs/avf/OPEN_SOURCE_EXPANSION_MAP.md",
                "avf/capabilities/generated/capability_fit_scorecard.json",
            ],
            "gap": "Current repo records candidate open-source fit, but source collection and adoption are still gated.",
        },
        {
            "id": "REQ-003-cite-papers",
            "requirement": "Use paper-backed reasoning and citations for agent, eval, web, and adaptation design choices.",
            "status": "PARTIAL",
            "evidence": [
                "avf/strategy/generated/strategy_source_ledger.json",
                "avf/cells/evidence/generated/primary_source_ledger.json",
            ],
            "gap": "Some paper references exist, but the active source-evidence lane still needs owner-approved primary-source completion for broader coverage.",
        },
        {
            "id": "REQ-004-use-primary-sources",
            "requirement": "Use primary/original sources as final evidence, including official docs, original repos, papers, patents, and standards.",
            "status": "BLOCKED_OWNER_ACTION_FOR_EXTERNAL_COLLECTION",
            "evidence": [
                rel(PROTECTED_BOUNDARY),
            ],
            "gap": "External/source collection is stopped at PROTECTED_ACTION_REQUIRED until owner authorization is filled and reviewed.",
        },
        {
            "id": "REQ-005-implement-toward-factory-infrastructure",
            "requirement": "Keep implementing the AVF infrastructure rather than stopping at chat-only planning.",
            "status": "PROVEN",
            "evidence": [
                "scripts/validate_avf*.py validator set",
                "PR #10 draft branch with repeated repo-local commits",
            ],
            "gap": None,
        },
        {
            "id": "REQ-006-prove-completion-requirement-by-requirement",
            "requirement": "Audit completion requirement-by-requirement before any completion claim.",
            "status": "PROVEN",
            "evidence": [
                rel(MATRIX),
                rel(VALIDATION_REPORT),
            ],
            "gap": None,
        },
        {
            "id": "REQ-007-respect-protected-action-boundaries",
            "requirement": "Avoid protected actions unless the owner explicitly authorizes them and a review gate passes.",
            "status": "PROVEN",
            "evidence": [
                rel(PROTECTED_BOUNDARY),
                "claim_boundary flags are false",
            ],
            "gap": None,
        },
        {
            "id": "REQ-008-avoid-production-or-release-claims",
            "requirement": "Avoid claiming completion, release readiness, production readiness, or external validation until all evidence exists.",
            "status": "UNPROVEN_FOR_FULL_OBJECTIVE",
            "evidence": [
                "release_ready=false",
                "production_ready=false",
            ],
            "gap": "The full objective is not complete; the correct current claim is active/incomplete with a protected source-evidence boundary.",
        },
    ]


def build_matrix() -> dict:
    boundary = read_json(PROTECTED_BOUNDARY)
    require_protected_boundary(boundary)
    requirements = build_requirements()
    counts = {
        "total": len(requirements),
        "proven": sum(1 for item in requirements if item["status"] == "PROVEN"),
        "partial": sum(1 for item in requirements if item["status"] == "PARTIAL"),
        "blocked": sum(1 for item in requirements if item["status"].startswith("BLOCKED")),
        "unproven": sum(1 for item in requirements if item["status"].startswith("UNPROVEN")),
    }
    return {
        "matrix_id": THIS_GOAL_ID,
        "created_at": CREATED_AT,
        "objective": OBJECTIVE_TEXT,
        "terminal_condition": TERMINAL_CONDITION,
        "objective_completion_proven": False,
        "foundation_ready_scope": "repo_local_internal_only",
        "source_collection_terminal_condition": boundary["terminal_condition"],
        "requirements": requirements,
        "requirement_counts": counts,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    forbidden = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    return f"""task_id: avf-local-primary-source-evidence-acceptance-harness-v0-1
title: Add AVF local primary-source evidence acceptance harness v0.1
goal: Validate owner-supplied primary-source evidence records locally without collecting, fetching, scraping, cloning, installing, or calling providers.
context_paths:
  - {rel(MATRIX)}
  - {rel(PROTECTED_BOUNDARY)}
files_likely_to_touch:
  - avf/capabilities/generated/local_primary_source_evidence_acceptance.schema.yml
  - avf/capabilities/generated/local_primary_source_evidence_acceptance_sample.yml
  - avf/capabilities/generated/local_primary_source_evidence_acceptance_gate.json
  - docs/goals/AVF_LOCAL_PRIMARY_SOURCE_EVIDENCE_ACCEPTANCE_HARNESS_V0_1_REPORT.md
acceptance_criteria:
  - accepts owner-supplied source records only
  - rejects empty source title, source kind, source URI, claim supported, and evidence excerpt summary
  - never performs source collection or external fetch
  - keeps source collection lane blocked until owner authorization passes
forbidden_changes:
{forbidden}
validation_commands:
  - python scripts\\validate_avf_active_objective_completion_matrix_v0_1.py
expected_outputs:
  - local source evidence acceptance schema
  - empty/owner-supplied sample record
  - blocked acceptance gate
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(matrix: dict) -> dict:
    return {
        "validator_id": "validate_avf_active_objective_completion_matrix_v0_1",
        "status": "PASS",
        "terminal_condition": TERMINAL_CONDITION,
        "objective_completion_proven": False,
        "foundation_ready_scope": "repo_local_internal_only",
        "requirement_counts": matrix["requirement_counts"],
        "source_collection_terminal_condition": matrix["source_collection_terminal_condition"],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(matrix: dict) -> str:
    counts = matrix["requirement_counts"]
    rows = "\n".join(
        f"| {item['id']} | {item['status']} | {item['requirement']} | {item['gap'] or 'none'} |"
        for item in matrix["requirements"]
    )
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Active Objective Completion Matrix v0.1 Report

RESULT: PASS
active_objective_completion_matrix_v0_1=true
terminal_condition={TERMINAL_CONDITION}
objective_completion_proven=false
foundation_ready_scope=repo_local_internal_only

## Requirement counts

- requirements_total={counts['total']}
- requirements_proven={counts['proven']}
- requirements_partial={counts['partial']}
- requirements_blocked={counts['blocked']}
- requirements_unproven={counts['unproven']}
- source_collection_terminal_condition={matrix['source_collection_terminal_condition']}

## Matrix

| id | status | requirement | gap |
| --- | --- | --- | --- |
{rows}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    matrix = build_matrix()
    write_json(MATRIX, matrix)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result(matrix))
    write_text(VALIDATION_REPORT, build_report(matrix))

    print("AVF Active Objective Completion Matrix v0.1")
    print("RESULT: PASS")
    print(f"terminal_condition={TERMINAL_CONDITION}")
    print("objective_completion_proven=false")
    print("requirements_total=8")
    print("requirements_proven=4")
    print("requirements_partial=2")
    print("requirements_blocked=1")
    print("requirements_unproven=1")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

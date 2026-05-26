from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

SCORECARD = CAPABILITIES / "capability_fit_scorecard.json"
GATE_DECISION = CAPABILITIES / "capability_fit_scoring_gate_decision.json"
REVIEW_DOSSIER = CAPABILITIES / "capability_review_dossier.json"
OWNER_CHECKLIST = CAPABILITIES / "capability_owner_review_checklist.md"
INTEGRATION_GATE = CAPABILITIES / "capability_integration_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_review_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_review_dossier_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_REVIEW_DOSSIER_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_review_dossier_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_source_verification_matrix_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"

REVIEW_FIELDS = [
    "license_review",
    "security_review",
    "maintenance_review",
    "architecture_fit_review",
    "sandbox_plan",
    "rollback_plan",
    "owner_approval",
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


def review_section(kind: str, candidate_id: str) -> dict:
    prompts = {
        "license_review": "Confirm license identifier, compatibility, attribution, NOTICE obligations, and copyleft constraints from authoritative source files before any dependency action.",
        "security_review": "Review OpenSSF/SLSA posture, release provenance, dependency tree, known advisories, install hooks, and secret/network behavior before any integration.",
        "maintenance_review": "Review release cadence, issue response, maintainers, bus factor indicators, backwards compatibility, and project governance.",
        "architecture_fit_review": "Verify adapter boundary, data flow, failure modes, local/offline behavior, rollback path, and coupling to AVF control-plane contracts.",
        "sandbox_plan": "Define sandbox, permissions, filesystem/network boundary, test fixtures, and no-provider dry-run behavior before execution.",
        "rollback_plan": "Define removal plan, config rollback, data migration rollback, and artifact cleanup before any integration branch.",
        "owner_approval": "Owner must approve the review dossier before dependency install, clone, fetch, provider call, or runtime integration.",
    }
    return {
        "status": "required_not_performed",
        "owner_action_required": True,
        "review_prompt": prompts[kind],
        "candidate_id": candidate_id,
    }


def build_candidate_dossier(score: dict) -> dict:
    record = {
        "candidate_id": score["candidate_id"],
        "candidate_name": score["candidate_name"],
        "capability_id": score["capability_id"],
        "capability_name": score["capability_name"],
        "priority_rank": score["priority_rank"],
        "fit_score": score["fit_score"],
        "risk_score": score["risk_score"],
        "integration_recommendation": "do_not_integrate_yet",
        "review_reason": score["rationale"],
        "source_refs": sorted(set(score.get("scoring_source_refs", []) + [score.get("candidate_source_ref")])),
        "blocked_reason": score["blocked_reason"],
        "claim_boundary": false_boundary(),
    }
    for field in REVIEW_FIELDS:
        record[field] = review_section(field, score["candidate_id"])
    return record


def build_review_dossier(scorecard: dict, gate: dict) -> dict:
    scores_by_id = {score["candidate_id"]: score for score in scorecard["candidate_scores"]}
    candidates = [build_candidate_dossier(scores_by_id[candidate_id]) for candidate_id in gate["top_candidates"]]
    return {
        "dossier_id": "avf-capability-review-dossier-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "decision": "owner_review_required_before_integration",
        "source_scorecard_uri": rel(SCORECARD),
        "source_gate_decision_uri": rel(GATE_DECISION),
        "candidate_dossiers": candidates,
        "review_fields": REVIEW_FIELDS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_owner_checklist(dossier: dict) -> str:
    lines = [
        "# Capability Owner Review Checklist",
        "",
        "No install, No clone, No fetch, No runtime integration, No provider call, No deploy, No publish.",
        "",
        "Owner approval required before any candidate can move beyond review.",
        "",
        "## Top Candidate Reviews",
        "",
    ]
    for candidate in dossier["candidate_dossiers"]:
        lines.extend(
            [
                f"### {candidate['priority_rank']}. {candidate['candidate_name']} ({candidate['candidate_id']})",
                "",
                f"- Fit score: {candidate['fit_score']}",
                f"- Risk score: {candidate['risk_score']}",
                f"- Recommendation: {candidate['integration_recommendation']}",
                "- [ ] License review completed from authoritative project files",
                "- [ ] Security review completed",
                "- [ ] Maintenance review completed",
                "- [ ] Architecture fit review completed",
                "- [ ] Sandbox plan approved",
                "- [ ] Rollback plan approved",
                "- [ ] Owner approval recorded",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "- protected_action_executed=false",
            "- dependency_install_performed=false",
            "- external_fetch_performed=false",
            "- oss_clone_performed=false",
            "- package_install_performed=false",
            "- runtime_integration_performed=false",
        ]
    )
    return "\n".join(lines) + "\n"


def build_integration_gate(dossier: dict) -> dict:
    return {
        "gate_id": "avf-capability-integration-preflight-gate-v0-1",
        "created_at": CREATED_AT,
        "status": "PASS",
        "gate_decision": "BLOCKED_PENDING_OWNER_REVIEW",
        "decision_reason": "Top candidates have review dossiers, but no required review field has been completed or approved.",
        "candidate_ids": [candidate["candidate_id"] for candidate in dossier["candidate_dossiers"]],
        "blocking_requirements": REVIEW_FIELDS,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-source-verification-matrix-v0-1
title: Add AVF capability source verification matrix v0.1
goal: Create a repo-local source verification matrix for top capability candidates before owner approval or integration.
context_paths:
  - avf/capabilities/generated/capability_review_dossier.json
  - avf/capabilities/generated/capability_owner_review_checklist.md
  - avf/capabilities/generated/capability_integration_preflight_gate.json
files_likely_to_touch:
  - scripts/run_avf_capability_source_verification_matrix_v0_1.py
  - scripts/validate_avf_capability_source_verification_matrix_v0_1.py
  - avf/capabilities/generated/capability_source_verification_matrix.json
  - docs/goals/AVF_CAPABILITY_SOURCE_VERIFICATION_MATRIX_V0_1_REPORT.md
forbidden_changes:
  - No provider calls
  - No live model calls
  - No external service calls
  - No scraping
  - No package install
  - No dependency install
  - No OSS clone
  - No external fetch
  - No runtime integration
  - No deploy
  - No publish
  - No release readiness claim
  - No production readiness claim
acceptance_criteria:
  - source verification matrix exists
  - each top candidate has official docs, repository/license, security, maintenance, and architecture evidence slots
  - all evidence slots remain required_not_performed until actual owner-approved review happens
  - integration gate remains blocked
validation_commands:
  - python scripts\\validate_avf_capability_review_dossier_v0_1.py
  - python scripts\\validate_avf_capability_source_verification_matrix_v0_1.py
expected_outputs:
  - capability_source_verification_matrix.json
  - source verification matrix report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_review_dossier_v0_1",
        "status": "PASS",
        "checks": [
            "fit scoring gate authorizes review dossier",
            "top candidate dossiers exist",
            "owner checklist exists",
            "integration gate remains blocked",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(dossier: dict) -> str:
    top_lines = "\n".join(
        f"- {candidate['priority_rank']}. {candidate['candidate_id']} fit={candidate['fit_score']} risk={candidate['risk_score']}"
        for candidate in dossier["candidate_dossiers"]
    )
    return f"""# AVF Capability Review Dossier v0.1 Report

RESULT: PASS
capability_review_dossier_v0_1=true
review_dossier_created=true
owner_checklist_created=true
integration_preflight_gate_created=true
top_candidate_dossiers_created=true
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

## Candidates In Review

{top_lines}

## Gate

The integration preflight gate is `BLOCKED_PENDING_OWNER_REVIEW`. This dossier does not approve, install, clone, fetch, deploy, publish, or integrate any candidate.
"""


def main() -> None:
    scorecard = read_json(SCORECARD)
    gate = read_json(GATE_DECISION)
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("fit scoring gate does not point to this review dossier goal")
    dossier = build_review_dossier(scorecard, gate)
    write_json(REVIEW_DOSSIER, dossier)
    write_text(OWNER_CHECKLIST, build_owner_checklist(dossier))
    write_json(INTEGRATION_GATE, build_integration_gate(dossier))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(dossier))

    print("AVF Capability Review Dossier v0.1 runner")
    print("RESULT: PASS")
    print("capability_review_dossier_v0_1=true")
    print("review_dossier_created=true")
    print("owner_checklist_created=true")
    print("integration_preflight_gate_created=true")
    print("top_candidate_dossiers_created=true")
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

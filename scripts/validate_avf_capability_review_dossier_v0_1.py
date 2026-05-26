from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_review_dossier_v0_1.py"
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

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    SCORECARD,
    GATE_DECISION,
    REVIEW_DOSSIER,
    OWNER_CHECKLIST,
    INTEGRATION_GATE,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REQUIRED_REVIEW_FIELDS = [
    "license_review",
    "security_review",
    "maintenance_review",
    "architecture_fit_review",
    "sandbox_plan",
    "rollback_plan",
    "owner_approval",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_review_dossier_v0_1=true",
    "review_dossier_created=true",
    "owner_checklist_created=true",
    "integration_preflight_gate_created=true",
    "top_candidate_dossiers_created=true",
    "protected_action_executed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "provider_calls_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Review Dossier v0.1 validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict:
    return json.loads(read(path))


def require_false_flags(record: dict, label: str) -> None:
    for flag in FALSE_FLAGS:
        if record.get(flag) is not False:
            fail(f"{label} {flag} must be false")


def require_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def require_review_dossier(scorecard: dict, gate: dict) -> None:
    dossier = read_json(REVIEW_DOSSIER)
    if dossier.get("status") != "PASS":
        fail("review dossier status must be PASS")
    if dossier.get("goal_id") != THIS_GOAL_ID:
        fail("review dossier goal_id mismatch")
    if dossier.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("review dossier next safe goal mismatch")
    if dossier.get("decision") != "owner_review_required_before_integration":
        fail("review dossier decision must require owner review")
    require_false_flags(dossier.get("claim_boundary", {}), "review dossier claim boundary")

    top_candidates = gate.get("top_candidates", [])
    records = dossier.get("candidate_dossiers", [])
    if len(records) != len(top_candidates):
        fail("review dossier must include exactly the top scored candidates")
    record_ids = {record.get("candidate_id") for record in records}
    missing = sorted(set(top_candidates) - record_ids)
    if missing:
        fail("review dossier missing top candidates:\n" + "\n".join(missing))

    score_by_id = {score["candidate_id"]: score for score in scorecard.get("candidate_scores", [])}
    for record in records:
        candidate_id = record.get("candidate_id")
        if candidate_id not in score_by_id:
            fail(f"review candidate missing from scorecard: {candidate_id}")
        if record.get("integration_recommendation") != "do_not_integrate_yet":
            fail(f"review candidate must block integration: {candidate_id}")
        for field in REQUIRED_REVIEW_FIELDS:
            section = record.get(field)
            if not isinstance(section, dict):
                fail(f"review field missing: {candidate_id} {field}")
            if section.get("status") != "required_not_performed":
                fail(f"review field must be required_not_performed: {candidate_id} {field}")
            if section.get("owner_action_required") is not True:
                fail(f"owner action must be required: {candidate_id} {field}")


def require_integration_gate() -> None:
    gate = read_json(INTEGRATION_GATE)
    if gate.get("status") != "PASS":
        fail("integration preflight gate status must be PASS")
    if gate.get("gate_decision") != "BLOCKED_PENDING_OWNER_REVIEW":
        fail("integration preflight gate must remain blocked")
    if gate.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("integration preflight next safe goal mismatch")
    require_false_flags(gate.get("claim_boundary", {}), "integration preflight gate")
    required_blockers = set(REQUIRED_REVIEW_FIELDS)
    blockers = set(gate.get("blocking_requirements", []))
    missing = sorted(required_blockers - blockers)
    if missing:
        fail("integration preflight gate missing blockers:\n" + "\n".join(missing))


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("status") != "PASS":
        fail("review dossier validation result must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("review dossier validation next safe goal mismatch")
    require_false_flags(validation.get("claim_boundary", {}), "review dossier validation result")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    scorecard = read_json(SCORECARD)
    gate = read_json(GATE_DECISION)
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("fit scoring gate does not authorize review dossier as next safe goal")
    if gate.get("decision") != "do_not_integrate_yet":
        fail("fit scoring gate must block integration")

    require_review_dossier(scorecard, gate)
    require_integration_gate()
    require_validation_result()
    require_markers(OWNER_CHECKLIST, ["# Capability Owner Review Checklist", "No install", "No clone", "No runtime integration", "Owner approval required"])
    require_markers(NEXT_CODEX_TASK, ["task_id: avf-capability-source-verification-matrix-v0-1", "forbidden_changes:", "validation_commands:", f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}"])
    require_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Review Dossier v0.1 validation")
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

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_evidence_claim_map_review_v0_1.py"
ACCEPTANCE_PACKET = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet.json"
CLAIM_MAP = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map.json"
CLAIM_MAP_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_gate.json"
CLAIM_MAP_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_next_action.yml"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_CLAIM_MAP_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_evidence_strength_scorecard_v0_1"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_CLAIM_MAP_REVIEWED"
REVIEW_STATUS = "claim_map_validated_ready_for_evidence_strength_scorecard"

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "claim_mapped_candidate_count": 7,
    "source_record_count": 16,
    "source_claim_count": 16,
    "unique_source_claim_count": 16,
    "evidence_only_claim_count": 16,
    "reviewed_candidate_claim_map_count": 7,
    "reviewed_source_claim_count": 16,
    "dependency_adopted_claim_count": 0,
    "runtime_integrated_claim_count": 0,
    "review_blocker_count": 0,
    "ready_for_evidence_strength_scorecard_count": 1,
}

FALSE_FLAGS = [
    "protected_action_executed",
    "provider_calls_performed",
    "live_model_calls_performed",
    "external_service_calls_performed",
    "automated_scraping_performed",
    "scraping_performed",
    "posting_automation_performed",
    "dependency_install_performed",
    "external_fetch_performed",
    "oss_clone_performed",
    "package_install_performed",
    "runtime_integration_performed",
    "runtime_export_performed",
    "collector_started",
    "telemetry_export_performed",
    "deploy_performed",
    "publish_performed",
    "release_ready",
    "production_ready",
]

REQUIRED_FILES = [
    RUNNER,
    ACCEPTANCE_PACKET,
    CLAIM_MAP,
    CLAIM_MAP_GATE,
    CLAIM_MAP_NEXT_ACTION,
    REVIEW_GATE,
    REVIEW_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_evidence_claim_map_review_v0_1=true",
    f"review_decision={REVIEW_DECISION}",
    f"review_status={REVIEW_STATUS}",
    "all_accepted_sources_mapped_once=true",
    "claim_map_scope_confirmed=internal_design_evidence_only",
    "ready_for_evidence_strength_scorecard_count=1",
    "unique_source_claim_count=16",
    "dependency_adopted_claim_count=0",
    "runtime_integrated_claim_count=0",
    "dependency_adoption_allowed=false",
    "runtime_integration_allowed=false",
    "protected_action_executed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "runtime_integration_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]

NEXT_ACTION_MARKERS = [
    "action_id: create-capability-candidate-primary-source-evidence-strength-scorecard",
    "owner_approval_required_before_execution: false",
    "Create an evidence-strength scorecard from the reviewed claim map",
    "Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Evidence Claim Map Review v0.1 validation")
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


def require_text_markers(path: Path, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))


def accepted_source_ids(acceptance: dict) -> set[str]:
    return {
        item["source_id"]
        for item in acceptance.get("source_acceptance_decisions", [])
        if item.get("decision") == "accept_for_evidence_only"
    }


def flattened_claims(claim_map: dict) -> list[dict]:
    claims = []
    for candidate_map in claim_map.get("candidate_claim_maps", []):
        claims.extend(candidate_map.get("source_claims", []))
    return claims


def require_previous_inputs() -> tuple[dict, dict]:
    acceptance = read_json(ACCEPTANCE_PACKET)
    claim_map = read_json(CLAIM_MAP)
    claim_map_gate = read_json(CLAIM_MAP_GATE)
    if acceptance.get("evidence_accepted_record_count") != EXPECTED_COUNTS["source_record_count"]:
        fail("acceptance packet evidence count mismatch")
    if acceptance.get("dependency_adopted_record_count") != 0:
        fail("acceptance packet dependency adoption count must be zero")
    if acceptance.get("runtime_integrated_record_count") != 0:
        fail("acceptance packet runtime integration count must be zero")
    if claim_map.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("claim map goal_id mismatch")
    if claim_map.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("claim map must point to this review goal")
    if claim_map_gate.get("gate_id") != "avf-capability-candidate-primary-source-evidence-claim-map-gate-v0-1":
        fail("claim map gate id mismatch")
    if claim_map_gate.get("status") != "PASS":
        fail("claim map gate status must be PASS")
    require_claim_map_shape(claim_map, acceptance, "claim map")
    require_claim_map_shape(claim_map_gate, acceptance, "claim map gate")
    require_text_markers(
        CLAIM_MAP_NEXT_ACTION,
        [
            "action_id: review-capability-candidate-primary-source-evidence-claim-map",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return acceptance, claim_map


def require_claim_map_shape(claim_map: dict, acceptance: dict, label: str) -> None:
    for key, value in EXPECTED_COUNTS.items():
        if key in claim_map and claim_map.get(key) != value:
            fail(f"{label} {key} mismatch")
    expected = {
        "records_source": "codex_assistant_primary_source_web_research",
        "claim_mapping_scope": "internal_design_evidence_only",
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
    }
    for key, value in expected.items():
        if claim_map.get(key) != value:
            fail(f"{label} {key} mismatch")
    source_ids = [claim["source_id"] for claim in flattened_claims(claim_map)]
    if len(source_ids) != EXPECTED_COUNTS["source_claim_count"]:
        fail(f"{label} source claim count mismatch")
    if len(set(source_ids)) != EXPECTED_COUNTS["unique_source_claim_count"]:
        fail(f"{label} source claims must be unique")
    if set(source_ids) != accepted_source_ids(acceptance):
        fail(f"{label} source claims must match accepted source ids exactly")
    for candidate_map in claim_map.get("candidate_claim_maps", []):
        if candidate_map.get("claim_mapping_scope") != "internal_design_evidence_only":
            fail(f"{label} candidate map scope mismatch")
        if candidate_map.get("dependency_adoption_allowed") is not False:
            fail(f"{label} candidate map dependency adoption must be blocked")
        if candidate_map.get("runtime_integration_allowed") is not False:
            fail(f"{label} candidate map runtime integration must be blocked")
        if candidate_map.get("source_count") != len(candidate_map.get("source_claims", [])):
            fail(f"{label} candidate map source count mismatch")
        for claim in candidate_map.get("source_claims", []):
            if claim.get("claim_mapping_scope") != "internal_design_evidence_only":
                fail(f"{label} claim scope mismatch")
            if claim.get("adoption_status") != "not_adopted":
                fail(f"{label} claim adoption status must be not_adopted")
            if claim.get("dependency_adoption_allowed") is not False:
                fail(f"{label} claim dependency adoption must be blocked")
            if claim.get("runtime_integration_allowed") is not False:
                fail(f"{label} claim runtime integration must be blocked")
            if claim.get("claim_map_review_required") is not True:
                fail(f"{label} claim map review flag mismatch")
    require_false_flags(claim_map.get("claim_boundary", {}), f"{label} claim boundary")


def require_review_record(record: dict, label: str, acceptance: dict, claim_map: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "all_accepted_sources_mapped_once": True,
        "claim_map_scope_confirmed": "internal_design_evidence_only",
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    for key, value in EXPECTED_COUNTS.items():
        if record.get(key) != value:
            fail(f"{label} {key} mismatch")
    if record.get("source_required_candidate_ids") != claim_map.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    reviewed = record.get("reviewed_candidate_claim_maps", [])
    if len(reviewed) != EXPECTED_COUNTS["reviewed_candidate_claim_map_count"]:
        fail(f"{label} reviewed candidate map count mismatch")
    reviewed_source_count = sum(item.get("source_count", 0) for item in reviewed)
    if reviewed_source_count != EXPECTED_COUNTS["reviewed_source_claim_count"]:
        fail(f"{label} reviewed source count mismatch")
    mapped = {item["candidate_id"] for item in reviewed}
    if mapped != set(acceptance.get("source_required_candidate_ids", [])):
        fail(f"{label} reviewed candidate ids mismatch")
    for item in reviewed:
        if item.get("review_status") != "reviewed_claim_map_validated":
            fail(f"{label} {item.get('candidate_id')} review status mismatch")
        if item.get("evidence_strength_scorecard_allowed") is not True:
            fail(f"{label} {item.get('candidate_id')} scorecard transition must be allowed")
        if item.get("dependency_adoption_allowed") is not False:
            fail(f"{label} {item.get('candidate_id')} dependency adoption must remain blocked")
        if item.get("runtime_integration_allowed") is not False:
            fail(f"{label} {item.get('candidate_id')} runtime integration must remain blocked")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_review_gate(acceptance: dict, claim_map: dict) -> None:
    gate = read_json(REVIEW_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-evidence-claim-map-review-gate-v0-1":
        fail("review gate id mismatch")
    if gate.get("status") != "PASS":
        fail("review gate status must be PASS")
    require_review_record(gate, "review gate", acceptance, claim_map)


def require_validation_result(acceptance: dict, claim_map: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_evidence_claim_map_review_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_review_record(result, "validation result", acceptance, claim_map)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    acceptance, claim_map = require_previous_inputs()
    require_review_gate(acceptance, claim_map)
    require_text_markers(REVIEW_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(acceptance, claim_map)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Evidence Claim Map Review v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_evidence_claim_map_review_v0_1=true")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("all_accepted_sources_mapped_once=true")
    print("claim_map_scope_confirmed=internal_design_evidence_only")
    print("dependency_adoption_allowed=false")
    print("runtime_integration_allowed=false")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

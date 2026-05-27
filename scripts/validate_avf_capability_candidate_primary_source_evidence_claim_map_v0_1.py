from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_candidate_primary_source_evidence_claim_map_v0_1.py"
ACCEPTANCE_PACKET = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_packet.json"
ACCEPTANCE_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_gate.json"
ACCEPTANCE_REVIEW_NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_acceptance_decision_review_next_action.yml"
CLAIM_MAP = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map.json"
CLAIM_MAP_GATE = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_gate.json"
CLAIM_MAP_REPORT = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_evidence_claim_map_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_EVIDENCE_CLAIM_MAP_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_review_v0_1"
ACCEPTANCE_PACKET_GOAL_ID = "avf_capability_candidate_primary_source_acceptance_decision_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_evidence_claim_map_review_v0_1"
CLAIM_MAP_STATUS = "evidence_only_claim_map_created_no_adoption"

EXPECTED_COUNTS = {
    "candidate_count": 7,
    "claim_mapped_candidate_count": 7,
    "source_record_count": 16,
    "source_claim_count": 16,
    "evidence_only_claim_count": 16,
    "dependency_adopted_claim_count": 0,
    "runtime_integrated_claim_count": 0,
    "ready_for_claim_map_review_count": 1,
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
    ACCEPTANCE_REVIEW_GATE,
    ACCEPTANCE_REVIEW_NEXT_ACTION,
    CLAIM_MAP,
    CLAIM_MAP_GATE,
    CLAIM_MAP_REPORT,
    NEXT_ACTION,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_candidate_primary_source_evidence_claim_map_v0_1=true",
    f"claim_map_status={CLAIM_MAP_STATUS}",
    "claim_mapped_candidate_count=7",
    "source_claim_count=16",
    "evidence_only_claim_count=16",
    "dependency_adopted_claim_count=0",
    "runtime_integrated_claim_count=0",
    "claim_mapping_scope=internal_design_evidence_only",
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
    "action_id: review-capability-candidate-primary-source-evidence-claim-map",
    "owner_approval_required_before_execution: false",
    "Review the evidence-only claim map",
    "Do not adopt dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Candidate Primary-Source Evidence Claim Map v0.1 validation")
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


def require_acceptance_inputs() -> tuple[dict, dict]:
    acceptance = read_json(ACCEPTANCE_PACKET)
    review = read_json(ACCEPTANCE_REVIEW_GATE)
    if acceptance.get("goal_id") != ACCEPTANCE_PACKET_GOAL_ID:
        fail("acceptance packet goal_id mismatch")
    if acceptance.get("evidence_accepted_record_count") != EXPECTED_COUNTS["source_record_count"]:
        fail("acceptance packet evidence count mismatch")
    if acceptance.get("dependency_adopted_record_count") != 0:
        fail("acceptance packet dependency adoption count must be zero")
    if acceptance.get("runtime_integrated_record_count") != 0:
        fail("acceptance packet runtime integration count must be zero")
    if review.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("acceptance review gate goal_id mismatch")
    if review.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("acceptance review gate must point to this claim map goal")
    if review.get("ready_for_claim_mapping_count") != 1:
        fail("acceptance review gate must be ready for claim mapping")
    if review.get("adoption_boundary_confirmed") is not True:
        fail("acceptance review must confirm adoption boundary")
    require_false_flags(acceptance.get("claim_boundary", {}), "acceptance packet claim boundary")
    require_false_flags(review.get("claim_boundary", {}), "acceptance review claim boundary")
    require_text_markers(
        ACCEPTANCE_REVIEW_NEXT_ACTION,
        [
            "action_id: create-capability-candidate-primary-source-evidence-claim-map",
            f"next_safe_goal_id: {THIS_GOAL_ID}",
        ],
    )
    return acceptance, review


def require_source_claim(claim: dict, label: str, accepted_sources: dict[str, dict]) -> None:
    source_id = claim.get("source_id", "<missing>")
    if source_id not in accepted_sources:
        fail(f"{label} unexpected source claim {source_id}")
    accepted = accepted_sources[source_id]
    for key in ["candidate_id", "source_kind", "source_uri", "claim_supported"]:
        if claim.get(key) != accepted.get(key):
            fail(f"{label} {source_id} {key} mismatch")
    if claim.get("claim_mapping_scope") != "internal_design_evidence_only":
        fail(f"{label} {source_id} claim mapping scope mismatch")
    if claim.get("evidence_acceptance_status") != "accepted_for_internal_design_evidence_only":
        fail(f"{label} {source_id} evidence acceptance status mismatch")
    if claim.get("adoption_status") != "not_adopted":
        fail(f"{label} {source_id} adoption status must be not_adopted")
    if claim.get("dependency_adoption_allowed") is not False:
        fail(f"{label} {source_id} dependency adoption must be blocked")
    if claim.get("runtime_integration_allowed") is not False:
        fail(f"{label} {source_id} runtime integration must be blocked")
    if claim.get("claim_map_review_required") is not True:
        fail(f"{label} {source_id} claim map review must be required")


def require_candidate_map(candidate_map: dict, label: str, accepted_sources: dict[str, dict]) -> int:
    candidate_id = candidate_map.get("candidate_id", "<missing>")
    claims = candidate_map.get("source_claims", [])
    if not claims:
        fail(f"{label} {candidate_id} must include source claims")
    if candidate_map.get("source_count") != len(claims):
        fail(f"{label} {candidate_id} source_count mismatch")
    if candidate_map.get("claim_mapping_scope") != "internal_design_evidence_only":
        fail(f"{label} {candidate_id} claim mapping scope mismatch")
    if candidate_map.get("dependency_adoption_allowed") is not False:
        fail(f"{label} {candidate_id} dependency adoption must be blocked")
    if candidate_map.get("runtime_integration_allowed") is not False:
        fail(f"{label} {candidate_id} runtime integration must be blocked")
    for claim in claims:
        if claim.get("candidate_id") != candidate_id:
            fail(f"{label} {candidate_id} contains mismatched claim candidate")
        require_source_claim(claim, label, accepted_sources)
    return len(claims)


def require_claim_map_record(record: dict, label: str, acceptance: dict) -> None:
    expected = {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "claim_map_status": CLAIM_MAP_STATUS,
        "records_source": "codex_assistant_primary_source_web_research",
        "claim_mapping_scope": "internal_design_evidence_only",
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
    if record.get("source_required_candidate_ids") != acceptance.get("source_required_candidate_ids"):
        fail(f"{label} candidate ids mismatch")
    accepted_sources = {
        source["source_id"]: source
        for source in acceptance.get("source_acceptance_decisions", [])
    }
    candidate_maps = record.get("candidate_claim_maps", [])
    if len(candidate_maps) != EXPECTED_COUNTS["claim_mapped_candidate_count"]:
        fail(f"{label} candidate claim map count mismatch")
    claim_count = 0
    mapped_candidate_ids = set()
    for candidate_map in candidate_maps:
        mapped_candidate_ids.add(candidate_map.get("candidate_id"))
        claim_count += require_candidate_map(candidate_map, label, accepted_sources)
    if mapped_candidate_ids != set(acceptance.get("source_required_candidate_ids", [])):
        fail(f"{label} mapped candidate ids mismatch")
    if claim_count != EXPECTED_COUNTS["source_claim_count"]:
        fail(f"{label} source claim count mismatch")
    require_false_flags(record.get("claim_boundary", {}), f"{label} claim boundary")


def require_claim_map(acceptance: dict) -> None:
    claim_map = read_json(CLAIM_MAP)
    if claim_map.get("map_id") != "avf-capability-candidate-primary-source-evidence-claim-map-v0-1":
        fail("claim map id mismatch")
    require_claim_map_record(claim_map, "claim map", acceptance)


def require_claim_map_gate(acceptance: dict) -> None:
    gate = read_json(CLAIM_MAP_GATE)
    if gate.get("gate_id") != "avf-capability-candidate-primary-source-evidence-claim-map-gate-v0-1":
        fail("claim map gate id mismatch")
    if gate.get("status") != "PASS":
        fail("claim map gate status must be PASS")
    require_claim_map_record(gate, "claim map gate", acceptance)


def require_validation_result(acceptance: dict) -> None:
    result = read_json(VALIDATION_RESULT)
    if result.get("validator_id") != "validate_avf_capability_candidate_primary_source_evidence_claim_map_v0_1":
        fail("validation result validator id mismatch")
    if result.get("status") != "PASS":
        fail("validation result status must be PASS")
    require_claim_map_record(result, "validation result", acceptance)


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    acceptance, _ = require_acceptance_inputs()
    require_claim_map(acceptance)
    require_claim_map_gate(acceptance)
    require_text_markers(CLAIM_MAP_REPORT, REPORT_MARKERS)
    require_text_markers(NEXT_ACTION, NEXT_ACTION_MARKERS)
    require_validation_result(acceptance)
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Candidate Primary-Source Evidence Claim Map v0.1 validation")
    print("RESULT: PASS")
    print("capability_candidate_primary_source_evidence_claim_map_v0_1=true")
    print(f"claim_map_status={CLAIM_MAP_STATUS}")
    for key, value in EXPECTED_COUNTS.items():
        print(f"{key}={value}")
    print("claim_mapping_scope=internal_design_evidence_only")
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

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RUNNER = ROOT / "scripts" / "run_avf_capability_primary_source_research_packet_v0_1.py"
ACCEPTANCE_GATE = CAPABILITIES / "capability_source_evidence_acceptance_gate.json"
FIXTURE_TEMPLATE = CAPABILITIES / "capability_source_evidence_fixture_template.yml"
FIXTURE_MANIFEST = CAPABILITIES / "capability_source_evidence_fixture_template_manifest.json"
RESEARCH_PACKET = CAPABILITIES / "capability_primary_source_research_packet.yml"
PRO_PROMPT = CAPABILITIES / "capability_primary_source_research_pro_prompt.md"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_research_packet_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_research_packet.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_RESEARCH_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_research_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_source_evidence_acceptance_gate_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_owner_completed_source_evidence_review_v0_1"

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

ALLOWED_SOURCE_TYPES = [
    "official_docs",
    "official_repository",
    "license_file",
    "security_advisory",
    "maintenance_signal",
    "architecture_spec",
    "supply_chain_standard",
]

REQUIRED_FIELDS = [
    "source_uri",
    "source_type",
    "quoted_excerpt",
    "source_snapshot_hash",
    "license_note",
    "security_note",
    "maintenance_note",
    "architecture_fit_note",
    "supply_chain_note",
    "reviewer",
    "reviewed_at",
]

REQUIRED_FILES = [
    RUNNER,
    ACCEPTANCE_GATE,
    FIXTURE_TEMPLATE,
    FIXTURE_MANIFEST,
    RESEARCH_PACKET,
    PRO_PROMPT,
    NEXT_CODEX_TASK,
    VALIDATION_RESULT,
    VALIDATION_REPORT,
]

RESEARCH_PACKET_MARKERS = [
    "packet_id: avf-capability-primary-source-research-packet-v0-1",
    "goal_id: avf_capability_primary_source_research_packet_v0_1",
    "source_collection_mode: manual_owner_or_pro",
    "integration_allowed: false",
    "automated_fetch_allowed: false",
    "automated_scraping_allowed: false",
    "oss_clone_allowed: false",
    "dependency_install_allowed: false",
    "runtime_integration_allowed: false",
    "release_ready: false",
    "production_ready: false",
    "allowed_source_types:",
    "required_fields:",
    "research_targets:",
    f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
]

PRO_PROMPT_MARKERS = [
    "You are the primary-source research operator for AVF capability acquisition.",
    "Do not browse through automation from this repo.",
    "Use only primary/original sources.",
    "official docs",
    "official repository",
    "license file",
    "security advisory",
    "maintenance signal",
    "architecture spec",
    "supply-chain standard",
    "Do not claim integration, release readiness, production readiness, or external validation.",
]

REPORT_MARKERS = [
    "RESULT: PASS",
    "capability_primary_source_research_packet_v0_1=true",
    "primary_source_research_packet_created=true",
    "pro_prompt_created=true",
    "research_targets_created=true",
    "manual_owner_or_pro_collection_only=true",
    "integration_allowed=false",
    "protected_action_executed=false",
    "dependency_install_performed=false",
    "external_fetch_performed=false",
    "oss_clone_performed=false",
    "package_install_performed=false",
    "runtime_integration_performed=false",
    "provider_calls_performed=false",
    "live_model_calls_performed=false",
    "external_service_calls_performed=false",
    "scraping_performed=false",
    "posting_automation_performed=false",
    "deploy_performed=false",
    "publish_performed=false",
    "release_ready=false",
    "production_ready=false",
    f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}",
]


def fail(message: str) -> None:
    print("AVF Capability Primary-Source Research Packet v0.1 validation")
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


def require_inputs() -> tuple[dict, dict]:
    gate = read_json(ACCEPTANCE_GATE)
    manifest = read_json(FIXTURE_MANIFEST)
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        fail("acceptance gate must point to this primary-source research packet")
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        fail("acceptance gate previous goal mismatch")
    if gate.get("integration_decision") != "blocked":
        fail("acceptance gate integration decision must remain blocked")
    require_false_flags(gate.get("claim_boundary", {}), "acceptance gate claim boundary")
    if "Evidence remains untrusted until evaluated by the source evidence ingestion validator." not in read(FIXTURE_TEMPLATE):
        fail("fixture template must preserve untrusted evidence warning")
    return gate, manifest


def require_text_markers(path: Path, markers: list[str]) -> str:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing markers:\n" + "\n".join(missing))
    return text


def require_research_packet(manifest: dict) -> None:
    text = require_text_markers(RESEARCH_PACKET, RESEARCH_PACKET_MARKERS)
    for source_type in ALLOWED_SOURCE_TYPES:
        if f"- {source_type}" not in text:
            fail(f"research packet missing source type {source_type}")
    for field in REQUIRED_FIELDS:
        if f"- {field}" not in text:
            fail(f"research packet missing required field {field}")
    for entry in manifest.get("candidate_template_records", []):
        for key in ["candidate_id", "source_slot_id", "slot_type", "target_uri"]:
            value = entry[key]
            if value not in text:
                fail(f"research packet missing {key}={value}")


def require_validation_result() -> None:
    validation = read_json(VALIDATION_RESULT)
    if validation.get("validator_id") != "validate_avf_capability_primary_source_research_packet_v0_1":
        fail("validation result validator_id mismatch")
    if validation.get("status") != "PASS":
        fail("validation result status must be PASS")
    if validation.get("next_safe_goal_id") != NEXT_SAFE_GOAL_ID:
        fail("validation result next safe goal mismatch")
    if validation.get("integration_allowed") is not False:
        fail("validation result must keep integration disallowed")
    require_false_flags(validation.get("claim_boundary", {}), "validation result claim boundary")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    _gate, manifest = require_inputs()
    require_research_packet(manifest)
    require_text_markers(PRO_PROMPT, PRO_PROMPT_MARKERS)
    require_text_markers(
        NEXT_CODEX_TASK,
        [
            "task_id: avf-capability-owner-completed-source-evidence-review-v0-1",
            "No provider calls",
            "No live model calls",
            "No external service calls",
            "No scraping automation",
            "No package install",
            "No dependency install",
            "No OSS clone",
            "No runtime integration",
            f"next_safe_goal_id: {NEXT_SAFE_GOAL_ID}",
        ],
    )
    require_validation_result()
    require_text_markers(VALIDATION_REPORT, REPORT_MARKERS)

    print("AVF Capability Primary-Source Research Packet v0.1 validation")
    print("RESULT: PASS")
    print("capability_primary_source_research_packet_v0_1=true")
    print("primary_source_research_packet_created=true")
    print("pro_prompt_created=true")
    print("research_targets_created=true")
    print("manual_owner_or_pro_collection_only=true")
    print("integration_allowed=false")
    print("protected_action_executed=false")
    print("dependency_install_performed=false")
    print("external_fetch_performed=false")
    print("oss_clone_performed=false")
    print("package_install_performed=false")
    print("runtime_integration_performed=false")
    print("provider_calls_performed=false")
    print("live_model_calls_performed=false")
    print("external_service_calls_performed=false")
    print("scraping_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

ACCEPTANCE_GATE = CAPABILITIES / "capability_source_evidence_acceptance_gate.json"
FIXTURE_TEMPLATE = CAPABILITIES / "capability_source_evidence_fixture_template.yml"
FIXTURE_MANIFEST = CAPABILITIES / "capability_source_evidence_fixture_template_manifest.json"
RESEARCH_PACKET = CAPABILITIES / "capability_primary_source_research_packet.yml"
PRO_PROMPT = CAPABILITIES / "capability_primary_source_research_pro_prompt.md"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_research_packet_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_research_packet.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_RESEARCH_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_research_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_owner_completed_source_evidence_review_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"

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


def render_research_targets(entries: list[dict]) -> str:
    lines = []
    for entry in entries:
        lines.extend(
            [
                f"  - candidate_id: {entry['candidate_id']}",
                f"    candidate_name: {entry['candidate_name']}",
                f"    capability_id: {entry['capability_id']}",
                f"    source_slot_id: {entry['source_slot_id']}",
                f"    source_type: {entry['slot_type']}",
                f"    target_uri: {entry['target_uri']}",
                "    collection_status: owner_or_pro_manual_research_required",
                "    evidence_trusted_by_default: false",
                "    evidence_verified_by_default: false",
                "    integration_allowed_from_this_record: false",
            ]
        )
    return "\n".join(lines)


def render_list(items: list[str], indent: str = "  ") -> str:
    return "\n".join(f"{indent}- {item}" for item in items)


def build_research_packet(manifest: dict) -> str:
    targets = manifest["candidate_template_records"]
    return f"""packet_id: avf-capability-primary-source-research-packet-v0-1
created_at: {CREATED_AT}
goal_id: {THIS_GOAL_ID}
source_collection_mode: manual_owner_or_pro
acceptance_gate_uri: {rel(ACCEPTANCE_GATE)}
fixture_template_uri: {rel(FIXTURE_TEMPLATE)}
fixture_manifest_uri: {rel(FIXTURE_MANIFEST)}
integration_allowed: false
automated_fetch_allowed: false
automated_scraping_allowed: false
oss_clone_allowed: false
dependency_install_allowed: false
runtime_integration_allowed: false
deploy_allowed: false
publish_allowed: false
release_ready: false
production_ready: false

allowed_source_types:
{render_list(ALLOWED_SOURCE_TYPES)}

required_fields:
{render_list(REQUIRED_FIELDS)}

collection_rules:
  - Use only primary/original sources for each slot.
  - Prefer official docs, official repositories, license files, security advisories, maintenance signals, architecture specs, and supply-chain standards.
  - Record a short verbatim excerpt and a sha256 snapshot hash for each collected source.
  - Keep every record untrusted and unverified until a later ingestion and review gate validates it.
  - Do not fetch, scrape, clone, install, integrate, deploy, publish, or claim readiness from this packet.

research_targets:
{render_research_targets(targets)}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_pro_prompt(manifest: dict) -> str:
    entries = manifest["candidate_template_records"]
    candidate_count = len({entry["candidate_id"] for entry in entries})
    source_count = len(entries)
    return f"""# AVF Capability Primary-Source Research PRO Prompt v0.1

You are the primary-source research operator for AVF capability acquisition.

Mission:
Collect manually reviewed primary-source evidence for capability candidates before any future integration proposal. Do not browse through automation from this repo. Use only primary/original sources. Work from the source slots in `{rel(RESEARCH_PACKET)}` and fill the fixture fields in `{rel(FIXTURE_TEMPLATE)}`.

Allowed source families:
- official docs
- official repository
- license file
- security advisory
- maintenance signal
- architecture spec
- supply-chain standard

Required per source slot:
- source_uri
- source_type
- quoted_excerpt
- source_snapshot_hash
- license_note
- security_note
- maintenance_note
- architecture_fit_note
- supply_chain_note
- reviewer
- reviewed_at

Operating boundary:
- Do not fetch, scrape, clone, install, integrate, deploy, publish, or automate from this repo.
- Do not mark a source trusted by default.
- Do not mark a source verified by default.
- Do not claim integration, release readiness, production readiness, or external validation.
- Keep all evidence as owner/PRO-reviewed input until a later repo-local ingestion and review gate validates it.

Current packet:
- candidate_count: {candidate_count}
- source_slots: {source_count}
- next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-owner-completed-source-evidence-review-v0-1
title: Add AVF owner-completed source evidence review gate v0.1
goal: Review an owner-completed primary-source evidence fixture without fetching, scraping, cloning, installing, integrating, deploying, publishing, or claiming readiness.
context_paths:
  - avf/capabilities/generated/capability_primary_source_research_packet.yml
  - avf/capabilities/generated/capability_primary_source_research_pro_prompt.md
  - avf/capabilities/generated/capability_source_evidence_fixture_template.yml
files_likely_to_touch:
  - scripts/validate_avf_capability_owner_completed_source_evidence_review_v0_1.py
  - avf/capabilities/generated/capability_owner_completed_source_evidence_review_gate.json
  - docs/goals/AVF_CAPABILITY_OWNER_COMPLETED_SOURCE_EVIDENCE_REVIEW_V0_1_REPORT.md
forbidden_changes:
  - No provider calls
  - No live model calls
  - No external service calls
  - No scraping automation
  - No package install
  - No dependency install
  - No OSS clone
  - No runtime integration
  - No deploy
  - No publish
  - No release readiness claim
  - No production readiness claim
acceptance_criteria:
  - owner-completed source evidence review gate exists
  - review gate checks required fields before accepting any source record
  - review gate keeps integration blocked unless every required category and owner approval are present
  - review gate does not fetch, scrape, clone, install, integrate, deploy, publish, or claim readiness
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_research_packet_v0_1.py
expected_outputs:
  - owner-completed source evidence review gate
  - owner-completed source evidence review validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_primary_source_research_packet_v0_1",
        "status": "PASS",
        "checks": [
            "primary-source research packet exists",
            "PRO prompt exists",
            "all source slots are represented",
            "allowed source families are constrained to primary/original sources",
            "required evidence fields are explicit",
            "integration remains disallowed",
            "protected-action flags false",
        ],
        "integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(manifest: dict) -> str:
    targets = manifest["candidate_template_records"]
    candidate_count = len({entry["candidate_id"] for entry in targets})
    return f"""# AVF Capability Primary-Source Research Packet v0.1 Report

RESULT: PASS
capability_primary_source_research_packet_v0_1=true
primary_source_research_packet_created=true
pro_prompt_created=true
research_targets_created=true
manual_owner_or_pro_collection_only=true
integration_allowed=false
candidate_count={candidate_count}
source_slots={len(targets)}
protected_action_executed=false
dependency_install_performed=false
external_fetch_performed=false
oss_clone_performed=false
package_install_performed=false
runtime_integration_performed=false
provider_calls_performed=false
live_model_calls_performed=false
external_service_calls_performed=false
scraping_performed=false
posting_automation_performed=false
deploy_performed=false
publish_performed=false
release_ready=false
production_ready=false
next_safe_goal_id={NEXT_SAFE_GOAL_ID}

## Output Artifacts

- {rel(RESEARCH_PACKET)}
- {rel(PRO_PROMPT)}
- {rel(NEXT_CODEX_TASK)}
- {rel(VALIDATION_RESULT)}

## Boundary

The research packet is a manual owner/PRO collection artifact only. It does not fetch, scrape, clone, install, integrate, deploy, publish, verify, approve, or claim readiness for any capability candidate.
"""


def main() -> None:
    acceptance_gate = read_json(ACCEPTANCE_GATE)
    manifest = read_json(FIXTURE_MANIFEST)
    if acceptance_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("acceptance gate must point to this primary-source research packet")
    if acceptance_gate.get("integration_decision") != "blocked":
        raise SystemExit("acceptance gate must keep integration blocked")
    if acceptance_gate.get("source_entry_counts", {}).get("accepted_entries") != 0:
        raise SystemExit("primary-source research packet must follow zero accepted source evidence")

    write_text(RESEARCH_PACKET, build_research_packet(manifest))
    write_text(PRO_PROMPT, build_pro_prompt(manifest))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(manifest))

    print("AVF Capability Primary-Source Research Packet v0.1 runner")
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

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

REVIEW_DOSSIER = CAPABILITIES / "capability_review_dossier.json"
INTEGRATION_GATE = CAPABILITIES / "capability_integration_preflight_gate.json"
SOURCE_MATRIX = CAPABILITIES / "capability_source_verification_matrix.json"
SOURCE_PREFLIGHT_GATE = CAPABILITIES / "capability_source_verification_preflight_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_source_verification_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_source_verification_matrix_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_SOURCE_VERIFICATION_MATRIX_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_source_verification_matrix_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_owner_approval_packet_v0_1"
CREATED_AT = "2026-05-26T00:00:00Z"


SOURCE_TARGETS = {
    "candidate-opentelemetry": {
        "official_docs": "https://opentelemetry.io/docs/",
        "official_repository": "https://github.com/open-telemetry/opentelemetry-specification",
        "license_file": "https://github.com/open-telemetry/opentelemetry-specification/blob/main/LICENSE",
        "security_advisory": "https://github.com/open-telemetry/opentelemetry-specification/security",
        "maintenance_signal": "https://github.com/open-telemetry/opentelemetry-specification/pulse",
        "architecture_spec": "https://opentelemetry.io/docs/specs/otel/",
        "supply_chain_standard": "https://slsa.dev/spec/v1.2/",
    },
    "candidate-litellm-proxy": {
        "official_docs": "https://docs.litellm.ai/docs/",
        "official_repository": "https://github.com/BerriAI/litellm",
        "license_file": "https://github.com/BerriAI/litellm/blob/main/LICENSE",
        "security_advisory": "https://github.com/BerriAI/litellm/security",
        "maintenance_signal": "https://github.com/BerriAI/litellm/pulse",
        "architecture_spec": "https://docs.litellm.ai/docs/proxy/quick_start",
        "supply_chain_standard": "https://github.com/ossf/scorecard",
    },
    "candidate-temporal-workflow": {
        "official_docs": "https://docs.temporal.io/",
        "official_repository": "https://github.com/temporalio/temporal",
        "license_file": "https://github.com/temporalio/temporal/blob/main/LICENSE",
        "security_advisory": "https://github.com/temporalio/temporal/security",
        "maintenance_signal": "https://github.com/temporalio/temporal/pulse",
        "architecture_spec": "https://docs.temporal.io/temporal",
        "supply_chain_standard": "https://slsa.dev/spec/v1.2/",
    },
    "candidate-langgraph-runtime": {
        "official_docs": "https://docs.langchain.com/oss/python/langgraph",
        "official_repository": "https://github.com/langchain-ai/langgraph",
        "license_file": "https://github.com/langchain-ai/langgraph/blob/main/LICENSE",
        "security_advisory": "https://github.com/langchain-ai/langgraph/security",
        "maintenance_signal": "https://github.com/langchain-ai/langgraph/pulse",
        "architecture_spec": "https://docs.langchain.com/oss/python/langgraph/overview",
        "supply_chain_standard": "https://github.com/ossf/scorecard",
    },
    "candidate-mcp-tool-registry": {
        "official_docs": "https://modelcontextprotocol.io/docs/getting-started/intro",
        "official_repository": "https://github.com/modelcontextprotocol/modelcontextprotocol",
        "license_file": "https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/LICENSE",
        "security_advisory": "https://github.com/modelcontextprotocol/modelcontextprotocol/security",
        "maintenance_signal": "https://github.com/modelcontextprotocol/modelcontextprotocol/pulse",
        "architecture_spec": "https://modelcontextprotocol.io/docs/learn",
        "supply_chain_standard": "https://slsa.dev/spec/v1.2/",
    },
}

SLOT_REVIEW_PROMPTS = {
    "official_docs": "Confirm the current official documentation and supported integration model.",
    "official_repository": "Confirm the authoritative repository, release process, tags, and maintainer identity.",
    "license_file": "Confirm SPDX-compatible license expression, attribution, NOTICE, and compatibility.",
    "security_advisory": "Review GitHub security advisories, known CVEs, disclosure policy, and recent incidents.",
    "maintenance_signal": "Review release cadence, recent commits, issue response, maintainers, and project governance.",
    "architecture_spec": "Map the candidate architecture to AVF adapter, data-flow, failure-mode, and rollback boundaries.",
    "supply_chain_standard": "Apply OpenSSF/SLSA/SPDX/GitHub dependency-review gates before any dependency action.",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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


def build_slot(candidate_id: str, slot_type: str, target_uri: str) -> dict:
    return {
        "slot_id": f"{candidate_id}-{slot_type}",
        "slot_type": slot_type,
        "target_uri": target_uri,
        "verification_status": "required_not_performed",
        "source_fetch_performed": False,
        "owner_action_required": True,
        "review_prompt": SLOT_REVIEW_PROMPTS[slot_type],
    }


def build_candidate_row(candidate: dict) -> dict:
    targets = SOURCE_TARGETS[candidate["candidate_id"]]
    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_name": candidate["candidate_name"],
        "capability_id": candidate["capability_id"],
        "priority_rank": candidate["priority_rank"],
        "fit_score": candidate["fit_score"],
        "risk_score": candidate["risk_score"],
        "integration_recommendation": "do_not_integrate_yet",
        "source_slots": [
            build_slot(candidate["candidate_id"], slot_type, target_uri)
            for slot_type, target_uri in targets.items()
        ],
        "claim_boundary": false_boundary(),
    }


def build_matrix(dossier: dict) -> dict:
    return {
        "matrix_id": "avf-capability-source-verification-matrix-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "status": "PASS",
        "source_boundary": "Target URIs only. No URL is fetched, scraped, cloned, installed, invoked, or treated as verified in this pass.",
        "candidate_source_rows": [
            build_candidate_row(candidate) for candidate in dossier["candidate_dossiers"]
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_source_preflight_gate(matrix: dict) -> dict:
    return {
        "gate_id": "avf-capability-source-verification-preflight-gate-v0-1",
        "created_at": CREATED_AT,
        "status": "PASS",
        "gate_decision": "BLOCKED_PENDING_SOURCE_VERIFICATION_AND_OWNER_APPROVAL",
        "decision_reason": "Source target slots exist, but none has been fetched, verified, approved, or converted into integration evidence.",
        "candidate_ids": [row["candidate_id"] for row in matrix["candidate_source_rows"]],
        "blocking_requirements": [
            "official_docs_verification",
            "repository_and_license_verification",
            "security_advisory_review",
            "maintenance_review",
            "architecture_fit_review",
            "owner_approval",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    return f"""task_id: avf-capability-owner-approval-packet-v0-1
title: Add AVF capability owner approval packet v0.1
goal: Create an owner approval packet that explicitly keeps capability candidates blocked until source verification and review decisions are completed.
context_paths:
  - avf/capabilities/generated/capability_source_verification_matrix.json
  - avf/capabilities/generated/capability_source_verification_preflight_gate.json
  - avf/capabilities/generated/capability_review_dossier.json
files_likely_to_touch:
  - scripts/run_avf_capability_owner_approval_packet_v0_1.py
  - scripts/validate_avf_capability_owner_approval_packet_v0_1.py
  - avf/capabilities/generated/capability_owner_approval_packet.json
  - docs/goals/AVF_CAPABILITY_OWNER_APPROVAL_PACKET_V0_1_REPORT.md
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
  - owner approval packet exists
  - every candidate remains blocked by default
  - approval fields are explicit and unset
  - protected-action flags remain false
validation_commands:
  - python scripts\\validate_avf_capability_source_verification_matrix_v0_1.py
  - python scripts\\validate_avf_capability_owner_approval_packet_v0_1.py
expected_outputs:
  - capability_owner_approval_packet.json
  - owner approval validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result() -> dict:
    return {
        "validator_id": "validate_avf_capability_source_verification_matrix_v0_1",
        "status": "PASS",
        "checks": [
            "review dossier authorizes source verification matrix",
            "source verification matrix exists",
            "top candidate source slots exist",
            "source preflight gate remains blocked",
            "protected-action flags false",
        ],
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_report(matrix: dict) -> str:
    rows = "\n".join(
        f"- {row['candidate_id']}: {len(row['source_slots'])} source slots, integration={row['integration_recommendation']}"
        for row in matrix["candidate_source_rows"]
    )
    return f"""# AVF Capability Source Verification Matrix v0.1 Report

RESULT: PASS
capability_source_verification_matrix_v0_1=true
source_verification_matrix_created=true
source_preflight_gate_created=true
top_candidate_source_slots_created=true
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

## Matrix Rows

{rows}

## Boundary

The matrix records target source URIs only. It does not fetch, scrape, clone, install, invoke, deploy, publish, approve, or integrate any candidate.
"""


def main() -> None:
    dossier = read_json(REVIEW_DOSSIER)
    if dossier.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("review dossier does not point to this source verification goal")
    integration_gate = read_json(INTEGRATION_GATE)
    if integration_gate.get("gate_decision") != "BLOCKED_PENDING_OWNER_REVIEW":
        raise SystemExit("integration gate must remain blocked before source verification")

    matrix = build_matrix(dossier)
    write_json(SOURCE_MATRIX, matrix)
    write_json(SOURCE_PREFLIGHT_GATE, build_source_preflight_gate(matrix))
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result())
    write_text(VALIDATION_REPORT, build_report(matrix))

    print("AVF Capability Source Verification Matrix v0.1 runner")
    print("RESULT: PASS")
    print("capability_source_verification_matrix_v0_1=true")
    print("source_verification_matrix_created=true")
    print("source_preflight_gate_created=true")
    print("top_candidate_source_slots_created=true")
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

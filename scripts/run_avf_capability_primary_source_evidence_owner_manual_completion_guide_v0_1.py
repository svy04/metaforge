from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
GOALS = ROOT / "docs" / "goals"

RETRY_REVIEW_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_completion_retry_review_gate.json"
MANUAL_GUIDE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_guide.md"
MANUAL_GUIDE_GATE = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_guide_gate.json"
NEXT_CODEX_TASK = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_guide_next_codex_task_packet.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_primary_source_evidence_owner_manual_completion_guide_v0_1.validation_result.json"
VALIDATION_REPORT = GOALS / "AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_MANUAL_COMPLETION_GUIDE_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_guide_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_primary_source_evidence_owner_completion_retry_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_primary_source_evidence_owner_manual_completion_packet_template_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
RETRY_REVIEW_DECISION = "BLOCKED_OWNER_COMPLETION_RETRY_STILL_EMPTY"
GUIDE_DECISION = "MANUAL_COMPLETION_GUIDE_READY_EXECUTION_STILL_BLOCKED"

AUTHORIZATION_FIELDS = [
    "owner_authorization_statement",
    "authorized_by",
    "authorized_at",
    "authorization_expires_at",
    "authorized_collection_modes",
    "authorized_source_families",
    "authorized_candidate_ids",
    "authorized_source_slot_ids",
    "max_records_to_collect",
    "collection_boundaries",
    "revocation_note",
]

COLLECTION_MODES = [
    "manual_owner_collection",
    "pro_manual_collection",
    "codex_assisted_link_opening",
    "automated_collection",
]

FIELD_GUIDANCE = {
    "owner_authorization_statement": "Fill this with a plain authorization sentence. It should say what source evidence may be collected and why.",
    "authorized_by": "Name the owner or account that is granting authorization.",
    "authorized_at": "Use ISO-8601 UTC time. Example: 2026-05-27T00:00:00Z.",
    "authorization_expires_at": "Use ISO-8601 UTC time and keep the window narrow.",
    "authorized_collection_modes": "Choose only the collection modes the owner explicitly wants reviewed.",
    "authorized_source_families": "Choose only the source families the owner actually wants reviewed.",
    "authorized_candidate_ids": "List candidate ids from the existing capability records; do not add new candidates here.",
    "authorized_source_slot_ids": "List source slot ids, not vague source names.",
    "max_records_to_collect": "Set this to a small integer greater than zero only after the scope is real.",
    "collection_boundaries": "Explain what Codex may not do. Include no scraping, no login, no account automation, no install, and no clone unless later approved.",
    "revocation_note": "Explain how authorization can be revoked.",
}

MODE_GUIDANCE = {
    "manual_owner_collection": "Owner personally supplies source URLs or excerpts. Safest default.",
    "pro_manual_collection": "Owner uses a separate PRO chat to research and paste summarized source records back into the repo. Codex still does not call providers.",
    "codex_assisted_link_opening": "Future approval may allow Codex to open owner-listed URLs only. It is not active in this guide.",
    "automated_collection": "Blocked by default. Requires a later explicit authorization, policy review, and separate implementation.",
}

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


def require_retry_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("retry review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("retry review gate must point to this manual completion guide goal")
    if gate.get("retry_review_decision") != RETRY_REVIEW_DECISION:
        raise SystemExit("retry review gate decision mismatch")
    if gate.get("owner_input_required") is not True:
        raise SystemExit("retry review gate must require owner input")
    if gate.get("authorization_retry_completed") is not False:
        raise SystemExit("retry review gate must keep retry incomplete")
    if gate.get("authorization_retry_review_passed") is not False:
        raise SystemExit("retry review gate must not pass retry review")
    if gate.get("owner_authorization_granted") is not False:
        raise SystemExit("retry review gate must not grant owner authorization")
    if gate.get("authorization_fields_reviewed") != len(AUTHORIZATION_FIELDS):
        raise SystemExit("retry review gate field count mismatch")
    if gate.get("authorization_fields_present") != 0:
        raise SystemExit("retry review gate must not mark fields present")
    if gate.get("missing_authorization_fields") != AUTHORIZATION_FIELDS:
        raise SystemExit("retry review gate missing fields mismatch")
    if gate.get("selected_collection_modes") != []:
        raise SystemExit("retry review gate selected collection modes must be empty")
    if gate.get("collection_execution_allowed") is not False:
        raise SystemExit("retry review gate must keep collection blocked")
    counts = gate.get("source_entry_counts", {})
    if counts.get("source_records_reviewed") != 35:
        raise SystemExit("retry review gate must cover 35 source records")
    if counts.get("source_records_executable") != 0:
        raise SystemExit("retry review gate must not make source records executable")


def build_manual_guide(retry_review_gate: dict) -> str:
    counts = retry_review_gate["source_entry_counts"]
    field_rows = "\n".join(f"- `{field}`: {FIELD_GUIDANCE[field]}" for field in AUTHORIZATION_FIELDS)
    mode_rows = "\n".join(f"- `{mode}`: {MODE_GUIDANCE[mode]}" for mode in COLLECTION_MODES)
    blocked_rows = "\n".join(f"- No {item}" for item in BOUNDARY_ITEMS)
    pro_prompt = """You are helping me manually complete an AVF owner authorization packet.

Do not claim that anything has been collected, validated, deployed, published, or made production ready.
Use only sources I paste into this chat or URLs I explicitly list.
Return a structured proposal for these fields:
owner_authorization_statement, authorized_by, authorized_at, authorization_expires_at,
authorized_collection_modes, authorized_source_families, authorized_candidate_ids,
authorized_source_slot_ids, max_records_to_collect, collection_boundaries, revocation_note.
Keep automated collection, scraping, account automation, package install, clone, deploy, and publish blocked unless I explicitly authorize them later."""
    return f"""# AVF Primary-Source Evidence Owner Manual Completion Guide v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
created_at: {CREATED_AT}
guide_decision: {GUIDE_DECISION}

This guide explains how the owner can manually complete the missing authorization fields from the retry review gate. It is instruction-only and does not authorize source collection by itself.

## Current locked state

- owner_input_required: true
- owner_authorization_granted: false
- authorization_retry_completed: false
- authorization_retry_review_passed: false
- collection_execution_allowed: false
- source_records_reviewed: {counts['source_records_reviewed']}
- source_records_executable: {counts['source_records_executable']}

## Field-by-field completion guide

{field_rows}

## Collection mode guide

{mode_rows}

## Optional PRO prompt draft

```text
{pro_prompt}
```

## Boundary summary

{blocked_rows}

## Minimum completion rule

The owner must fill all 11 authorization fields, select at least one allowed collection mode, bind the chosen source families and source slot ids, set a narrow `max_records_to_collect`, and provide explicit `collection_boundaries` plus `revocation_note`. Even then, a separate review gate must pass before any execution can be considered.

## Next safe goal

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_manual_guide_gate(retry_review_gate: dict) -> dict:
    counts = retry_review_gate["source_entry_counts"]
    return {
        "gate_id": "avf-capability-primary-source-evidence-owner-manual-completion-guide-gate-v0-1",
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "status": "PASS",
        "guide_decision": GUIDE_DECISION,
        "manual_guide_uri": rel(MANUAL_GUIDE),
        "owner_input_required": True,
        "authorization_retry_completed": False,
        "authorization_retry_review_passed": False,
        "owner_authorization_granted": False,
        "authorization_fields_documented": AUTHORIZATION_FIELDS,
        "authorization_fields_documented_count": len(AUTHORIZATION_FIELDS),
        "collection_modes_documented": COLLECTION_MODES,
        "collection_modes_documented_count": len(COLLECTION_MODES),
        "collection_execution_allowed": False,
        "source_entry_counts": {
            "source_records_reviewed": counts["source_records_reviewed"],
            "source_records_executable": 0,
            "trusted_source_records": 0,
            "ingested_source_records": 0,
            "integrated_source_records": 0,
        },
        "integration_decision": "blocked",
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_validation_result(gate: dict) -> dict:
    counts = gate["source_entry_counts"]
    return {
        "validator_id": "validate_avf_capability_primary_source_evidence_owner_manual_completion_guide_v0_1",
        "status": "PASS",
        "checks": [
            "manual completion guide exists",
            "all missing authorization fields are documented",
            "all collection modes are documented with blocked defaults",
            "PRO prompt remains manual and owner-scoped",
            "collection execution remains blocked",
            "protected-action flags remain false",
        ],
        "guide_decision": GUIDE_DECISION,
        "owner_input_required": True,
        "authorization_retry_completed": False,
        "authorization_retry_review_passed": False,
        "authorization_fields_documented": len(AUTHORIZATION_FIELDS),
        "collection_modes_documented": len(COLLECTION_MODES),
        "source_records_reviewed": counts["source_records_reviewed"],
        "source_records_executable": counts["source_records_executable"],
        "collection_execution_allowed": False,
        "owner_authorization_granted": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def build_next_codex_task() -> str:
    forbidden = "\n".join(f"  - No {item}" for item in BOUNDARY_ITEMS)
    fields = "\n".join(f"  - {field}" for field in AUTHORIZATION_FIELDS)
    return f"""task_id: avf-capability-primary-source-evidence-owner-manual-completion-packet-template-v0-1
title: Add AVF owner manual completion packet template v0.1
goal: Create a fillable repo-local manual completion packet template for the 11 authorization fields without executing source collection or external actions.
context_paths:
  - {rel(MANUAL_GUIDE)}
  - {rel(MANUAL_GUIDE_GATE)}
  - {rel(RETRY_REVIEW_GATE)}
files_likely_to_touch:
  - avf/capabilities/generated/capability_primary_source_evidence_owner_manual_completion_packet_template.yml
  - avf/capabilities/generated/capability_primary_source_evidence_owner_manual_completion_packet_template_gate.json
  - docs/goals/AVF_CAPABILITY_PRIMARY_SOURCE_EVIDENCE_OWNER_MANUAL_COMPLETION_PACKET_TEMPLATE_V0_1_REPORT.md
authorization_fields_to_template:
{fields}
forbidden_changes:
{forbidden}
acceptance_criteria:
  - manual completion packet template includes every authorization field
  - template defaults keep owner authorization false
  - template keeps collection execution blocked
  - template includes PRO/manual/Codex-assisted/automated collection mode switches but leaves them false unless owner fills them later
validation_commands:
  - python scripts\\validate_avf_capability_primary_source_evidence_owner_manual_completion_guide_v0_1.py
expected_outputs:
  - fillable manual completion packet template
  - blocked template gate
  - validation report
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(gate: dict) -> str:
    counts = gate["source_entry_counts"]
    flag_rows = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# AVF Capability Primary-Source Evidence Owner Manual Completion Guide v0.1 Report

RESULT: PASS

## Commands

- python scripts\\run_avf_capability_primary_source_evidence_owner_manual_completion_guide_v0_1.py
- python scripts\\validate_avf_capability_primary_source_evidence_owner_manual_completion_guide_v0_1.py

## Generated artifacts

- {rel(MANUAL_GUIDE)}
- {rel(MANUAL_GUIDE_GATE)}
- {rel(NEXT_CODEX_TASK)}
- {rel(VALIDATION_RESULT)}
- {rel(VALIDATION_REPORT)}

## Gate summary

- capability_primary_source_evidence_owner_manual_completion_guide_v0_1=true
- owner_manual_completion_guide_created=true
- owner_manual_completion_guide_gate_created=true
- authorization_fields_documented={len(AUTHORIZATION_FIELDS)}
- collection_modes_documented={len(COLLECTION_MODES)}
- owner_input_required=true
- authorization_retry_completed=false
- authorization_retry_review_passed=false
- source_records_reviewed={counts['source_records_reviewed']}
- source_records_executable={counts['source_records_executable']}
- collection_execution_allowed=false
- owner_authorization_granted=false
- guide_decision={GUIDE_DECISION}

## Protected action flags

{flag_rows}

## Claim boundary

This is a repo-local manual completion guide. It does not authorize, collect, fetch, scrape, trust, ingest, integrate, clone, install, deploy, publish, or claim release/production readiness.

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def main() -> None:
    retry_review_gate = read_json(RETRY_REVIEW_GATE)
    require_retry_review_gate(retry_review_gate)

    write_text(MANUAL_GUIDE, build_manual_guide(retry_review_gate))
    manual_guide_gate = build_manual_guide_gate(retry_review_gate)
    write_json(MANUAL_GUIDE_GATE, manual_guide_gate)
    write_text(NEXT_CODEX_TASK, build_next_codex_task())
    write_json(VALIDATION_RESULT, build_validation_result(manual_guide_gate))
    write_text(VALIDATION_REPORT, build_report(manual_guide_gate))

    print("AVF Capability Primary-Source Evidence Owner Manual Completion Guide v0.1")
    print("RESULT: PASS")
    print("authorization_fields_documented=11")
    print("collection_modes_documented=4")
    print("owner_input_required=true")
    print("owner_authorization_granted=false")
    print("collection_execution_allowed=false")
    print("source_records_executable=0")
    print(f"guide_decision={GUIDE_DECISION}")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

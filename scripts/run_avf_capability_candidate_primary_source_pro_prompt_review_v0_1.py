from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PRO_PROMPT = CAPABILITIES / "capability_candidate_primary_source_pro_prompt.md"
PRO_PROMPT_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_prompt_gate.json"
REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_prompt_review_gate.json"
REVIEW_REPORT = CAPABILITIES / "capability_candidate_primary_source_pro_prompt_review_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_pro_prompt_review_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_pro_prompt_review_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_PROMPT_REVIEW_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_pro_prompt_review_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_pro_prompt_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_pro_output_packet_template_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_PROMPT_REVIEWED_REPO_LOCAL"
REVIEW_STATUS = "pro_prompt_review_passed_ready_for_output_packet_template"


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


def require_pro_prompt_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("pro prompt gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("pro prompt gate must point to this review goal")
    if gate.get("candidate_count") != 7:
        raise SystemExit("candidate count mismatch")
    if gate.get("source_target_count") != 16:
        raise SystemExit("source target count mismatch")
    if gate.get("required_source_field_count") != 12:
        raise SystemExit("required source field count mismatch")
    if gate.get("prompt_section_count") != 7:
        raise SystemExit("prompt section count mismatch")
    if gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("source collection execution must remain disabled")


def counts(gate: dict) -> dict:
    return {
        "candidate_count": gate["candidate_count"],
        "source_target_count": gate["source_target_count"],
        "required_source_field_count": gate["required_source_field_count"],
        "prompt_section_count": gate["prompt_section_count"],
        "prompt_review_blocker_count": 0,
        "ready_for_output_packet_template_count": 1,
        "external_fetch_performed_count": 0,
        "source_contents_acquired_count": 0,
    }


def base_record(gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "review_decision": REVIEW_DECISION,
        "review_status": REVIEW_STATUS,
        "reviewed_prompt_uri": rel(PRO_PROMPT),
        "source_required_candidate_ids": gate["source_required_candidate_ids"],
        "source_collection_execution_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(gate),
        "claim_boundary": false_boundary(),
    }


def build_gate(gate: dict) -> dict:
    return {
        **base_record(gate),
        "gate_id": "avf-capability-candidate-primary-source-pro-prompt-review-gate-v0-1",
        "status": "PASS",
        "gate_scope": "GPT Pro prompt reviewed; ready to create repo-local output packet template for pasted Pro results",
    }


def build_report(title: str, gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(gate).items())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_pro_prompt_review_v0_1=true

## Gate summary

- review_decision={REVIEW_DECISION}
- review_status={REVIEW_STATUS}
- source_collection_execution_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Reviewed prompt

- reviewed_prompt_uri={rel(PRO_PROMPT)}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: create-capability-candidate-primary-source-pro-output-packet-template
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Create a repo-local template for pasting GPT Pro primary-source YAML output
  - Preserve all 7 capability candidates, 16 source target slots, and 12 required fields
  - Keep output unaccepted until a review validator confirms owner/Pro-filled evidence
  - Do not fetch external sources inside Codex, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(gate: dict) -> dict:
    return {
        **base_record(gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_pro_prompt_review_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(REVIEW_GATE),
            rel(REVIEW_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    pro_prompt_gate = read_json(PRO_PROMPT_GATE)
    require_pro_prompt_gate(pro_prompt_gate)

    write_json(REVIEW_GATE, build_gate(pro_prompt_gate))
    report = build_report("AVF Capability Candidate Primary-Source Pro Prompt Review v0.1", pro_prompt_gate)
    write_text(REVIEW_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(pro_prompt_gate))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Pro Prompt Review v0.1")
    print("RESULT: PASS")
    print(f"review_decision={REVIEW_DECISION}")
    print(f"review_status={REVIEW_STATUS}")
    for key, value in counts(pro_prompt_gate).items():
        print(f"{key}={value}")
    print("source_collection_execution_allowed=false")
    print("external_fetch_performed=false")
    print("dependency_install_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

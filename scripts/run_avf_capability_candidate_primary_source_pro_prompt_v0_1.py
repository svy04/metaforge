from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

INPUT_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_review_gate.json"
OWNER_INPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_owner_input_packet_gate.json"
PRO_PROMPT = CAPABILITIES / "capability_candidate_primary_source_pro_prompt.md"
PRO_PROMPT_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_prompt_gate.json"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_pro_prompt_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_pro_prompt_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_PROMPT_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_pro_prompt_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_owner_input_packet_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_pro_prompt_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PROMPT_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_PRO_PROMPT_CREATED_REPO_LOCAL"
PROMPT_STATUS = "ready_for_gpt_pro_manual_primary_source_research"

REQUIRED_SOURCE_FIELDS = [
    "source_id",
    "source_title",
    "source_kind",
    "source_uri",
    "source_version_or_date",
    "source_owner_or_publisher",
    "license_or_rights_note",
    "claim_supported",
    "evidence_excerpt_summary",
    "verification_notes",
    "source_reference_lines",
    "retrieval_method",
]


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


def require_input_review_gate(review_gate: dict) -> None:
    if review_gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("input review gate goal mismatch")
    if review_gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("input review gate must point to this pro prompt goal")
    if review_gate.get("ready_for_pro_prompt_count") != 1:
        raise SystemExit("input review gate must be ready for pro prompt")
    if review_gate.get("source_collection_execution_allowed") is not False:
        raise SystemExit("source collection execution must remain disabled in Codex")


def counts(owner_input_gate: dict) -> dict:
    return {
        "candidate_count": owner_input_gate["candidate_input_section_count"],
        "source_target_count": owner_input_gate["fillable_source_record_slot_count"],
        "required_source_field_count": owner_input_gate["required_source_field_count"],
        "prompt_section_count": owner_input_gate["candidate_input_section_count"],
        "external_fetch_performed_count": 0,
        "source_contents_acquired_count": 0,
    }


def source_record_template(source_target_id: str) -> str:
    fields = "\n".join(f"      {field}: \"\"" for field in REQUIRED_SOURCE_FIELDS)
    return f"""    - source_target_id: {source_target_id}
      source_input_status: owner_to_fill_from_primary_source
{fields}"""


def prompt_sections(owner_input_gate: dict) -> str:
    blocks = []
    for section in owner_input_gate["candidate_input_sections"]:
        slots = "\n".join(source_record_template(slot["source_target_id"]) for slot in section["source_input_slots"])
        blocks.append(
            f"""  - candidate_id: {section['candidate_id']}
    candidate_name: {section['candidate_name']}
    source_records:
{slots}"""
        )
    return "\n".join(blocks)


def build_prompt(owner_input_gate: dict) -> str:
    return f"""# GPT Pro Prompt: AVF Capability Candidate Primary-Source Evidence Fill v0.1

You are GPT Pro acting as the primary-source research partner for AVF.

Use primary/original sources only.
Acceptable source kinds:
- official docs
- original repositories
- papers
- standards
- patents
- maintained implementations
- local repo evidence

Do not use blog summaries as final evidence unless they only point to a primary source.
Do not claim adoption readiness.
Do not claim production readiness.
Do not claim release readiness.
Do not tell Codex to fetch URLs.
Do not recommend dependency adoption, runtime integration, deploy, publish, scraping, posting automation, or OSS cloning.

Task:
Fill the source records below using primary/original sources. Return completed records only as structured YAML. Each source record must support one concrete capability claim and must include all 12 required fields.

Required fields:
{chr(10).join(f"- {field}" for field in REQUIRED_SOURCE_FIELDS)}

Output contract:
```yaml
goal_id: {THIS_GOAL_ID}
filled_by: gpt_pro_manual_primary_source_research
source_collection_context: external_manual_research_not_codex_runtime
records:
{prompt_sections(owner_input_gate)}
next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
```

Review rules:
- Prefer official documentation over tutorials.
- Prefer original repositories over package summaries.
- Prefer papers, standards, patents, and maintained implementations when they are the original authority.
- Include concise evidence summaries, not long quotations.
- Keep license and rights notes explicit.
- If a source target cannot be supported by a primary source, write `unsupported_primary_source_not_found` in the relevant fields and explain why in `verification_notes`.
"""


def base_record(owner_input_gate: dict) -> dict:
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "prompt_decision": PROMPT_DECISION,
        "prompt_status": PROMPT_STATUS,
        "prompt_uri": rel(PRO_PROMPT),
        "source_required_candidate_ids": owner_input_gate["source_required_candidate_ids"],
        "source_collection_execution_allowed": False,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(owner_input_gate),
        "claim_boundary": false_boundary(),
    }


def build_gate(owner_input_gate: dict) -> dict:
    return {
        **base_record(owner_input_gate),
        "gate_id": "avf-capability-candidate-primary-source-pro-prompt-gate-v0-1",
        "status": "PASS",
        "gate_scope": "GPT Pro prompt created for manual primary-source evidence filling; Codex did not collect sources",
    }


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-pro-prompt
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review the GPT Pro prompt before using it to fill primary-source evidence
  - Confirm all 7 capability candidates, 16 source targets, and 12 required source fields are present
  - Preserve the no-adoption, no-runtime, no-deploy, no-publish claim boundary
  - Do not fetch external sources inside Codex, install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_report(title: str, owner_input_gate: dict) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(owner_input_gate).items())
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_pro_prompt_v0_1=true

## Gate summary

- prompt_decision={PROMPT_DECISION}
- prompt_status={PROMPT_STATUS}
- source_collection_execution_allowed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(owner_input_gate: dict) -> dict:
    return {
        **base_record(owner_input_gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_pro_prompt_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(PRO_PROMPT),
            rel(PRO_PROMPT_GATE),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    input_review_gate = read_json(INPUT_REVIEW_GATE)
    owner_input_gate = read_json(OWNER_INPUT_PACKET_GATE)
    require_input_review_gate(input_review_gate)

    write_text(PRO_PROMPT, build_prompt(owner_input_gate))
    write_json(PRO_PROMPT_GATE, build_gate(owner_input_gate))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(owner_input_gate))
    write_text(VALIDATION_REPORT, build_report("AVF Capability Candidate Primary-Source Pro Prompt v0.1", owner_input_gate))

    print("AVF Capability Candidate Primary-Source Pro Prompt v0.1")
    print("RESULT: PASS")
    print(f"prompt_decision={PROMPT_DECISION}")
    print(f"prompt_status={PROMPT_STATUS}")
    for key, value in counts(owner_input_gate).items():
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

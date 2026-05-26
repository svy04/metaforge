from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"
DOC_AVF = ROOT / "docs" / "avf"

RECORDS = CAPABILITIES / "primary_source_manual_records.json"
RECORDS_REVIEW_GATE = CAPABILITIES / "primary_source_records_review_gate.json"
INTEGRATION_MAP = CAPABILITIES / "primary_source_claim_integration_map.json"
INTEGRATION_REPORT = CAPABILITIES / "primary_source_claim_integration_report.md"
NEXT_ACTION = CAPABILITIES / "primary_source_claim_integration_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "primary_source_claim_integration_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_PRIMARY_SOURCE_CLAIM_INTEGRATION_V0_1_REPORT.md"

OPEN_SOURCE_MAP = DOC_AVF / "OPEN_SOURCE_EXPANSION_MAP.md"
PLATFORM_ROADMAP = DOC_AVF / "AVF_PLATFORM_ROADMAP.md"
MARKET_TO_FACTORY_VISION = DOC_AVF / "AVF_MARKET_TO_FACTORY_VISION.md"

THIS_GOAL_ID = "avf_primary_source_claim_integration_v0_1"
PREVIOUS_GOAL_ID = "avf_primary_source_records_review_v0_1"
NEXT_SAFE_GOAL_ID = "avf_primary_source_claim_integration_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
REVIEW_DECISION = "PRIMARY_SOURCE_RECORDS_REVIEWED_CLAIM_INTEGRATION_READY"
INTEGRATION_DECISION = "PRIMARY_SOURCE_CLAIMS_INTEGRATED_INTO_DOCS_ONLY"
PROMOTION_SCOPE = "architecture_docs_and_plans_only"

SOURCE_TARGET_IDS = [
    "src-langgraph-official-docs",
    "src-temporal-official-docs",
    "src-opentelemetry-standard-docs",
    "src-mcp-official-docs",
    "src-litellm-original-repository",
    "src-vllm-original-repository",
    "src-webarena-paper",
]

DOCS_TO_UPDATE = [
    OPEN_SOURCE_MAP,
    PLATFORM_ROADMAP,
    MARKET_TO_FACTORY_VISION,
]

SECTION_BEGIN = "<!-- BEGIN AVF PRIMARY SOURCE CLAIM INTEGRATION V0.1 -->"
SECTION_END = "<!-- END AVF PRIMARY SOURCE CLAIM INTEGRATION V0.1 -->"


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


def require_records_review_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("records review gate goal mismatch")
    if gate.get("next_safe_goal_id") != THIS_GOAL_ID:
        raise SystemExit("records review gate must point to this integration goal")
    if gate.get("review_decision") != REVIEW_DECISION:
        raise SystemExit("records review decision mismatch")
    if gate.get("promotion_scope") != PROMOTION_SCOPE:
        raise SystemExit("records review promotion scope mismatch")
    if gate.get("runtime_adoption_allowed") is not False:
        raise SystemExit("runtime adoption must remain blocked")
    if gate.get("dependency_adoption_allowed") is not False:
        raise SystemExit("dependency adoption must remain blocked")


def require_records(data: dict) -> list[dict]:
    records = data.get("source_records")
    if not isinstance(records, list) or len(records) != len(SOURCE_TARGET_IDS):
        raise SystemExit("manual records must contain seven records")
    if [record.get("source_target_id") for record in records] != SOURCE_TARGET_IDS:
        raise SystemExit("manual records source target ids mismatch")
    return records


def integration_entry_for(record: dict) -> dict:
    source = record["source_record"]
    return {
        "source_target_id": record["source_target_id"],
        "target_claim_id": record["target_claim_id"],
        "source_uri": source["source_uri"],
        "claim_supported": source["claim_supported"],
        "evidence_summary": source["evidence_excerpt_summary"],
        "source_reference_lines": source["source_reference_lines"],
        "promotion_scope": PROMOTION_SCOPE,
        "runtime_adoption_allowed": False,
        "dependency_adoption_allowed": False,
    }


def build_integration_map(records: list[dict]) -> dict:
    return {
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "created_at": CREATED_AT,
        "integration_decision": INTEGRATION_DECISION,
        "promotion_scope": PROMOTION_SCOPE,
        "docs_updated": len(DOCS_TO_UPDATE),
        "source_claims_integrated": len(records),
        "integrated_claims": [integration_entry_for(record) for record in records],
        "updated_docs": [rel(path) for path in DOCS_TO_UPDATE],
        "runtime_adoption_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def integration_section(integrated_claims: list[dict]) -> str:
    rows = "\n".join(
        [
            "| Source target | Claim id | Primary source | Scope |",
            "| --- | --- | --- | --- |",
            *[
                f"| `{claim['source_target_id']}` | `{claim['target_claim_id']}` | "
                f"{claim['source_uri']} | `{claim['promotion_scope']}` |"
                for claim in integrated_claims
            ],
        ]
    )
    return f"""{SECTION_BEGIN}
## Primary-Source Claim Integration

primary_source_claims_integrated=true
integration_decision={INTEGRATION_DECISION}
promotion_scope={PROMOTION_SCOPE}
source_claims_integrated={len(integrated_claims)}
runtime_adoption_allowed=false
dependency_adoption_allowed=false

{rows}

Boundary:

- These claims are promoted into architecture docs and planning only.
- They do not authorize dependency adoption, runtime integration, provider calls, deployment, publishing, release readiness, or production readiness.
- Use `avf/capabilities/generated/primary_source_manual_records.json` as the detailed evidence record.

{SECTION_END}
"""


def upsert_section(path: Path, section: str) -> None:
    original = path.read_text(encoding="utf-8")
    if SECTION_BEGIN in original and SECTION_END in original:
        before = original.split(SECTION_BEGIN, 1)[0].rstrip()
        after = original.split(SECTION_END, 1)[1].lstrip()
        next_text = f"{before}\n\n{section.strip()}\n\n{after}".rstrip() + "\n"
    else:
        next_text = original.rstrip() + "\n\n" + section.strip() + "\n"
    path.write_text(next_text, encoding="utf-8")


def build_report(records: list[dict]) -> str:
    flags = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# Primary-Source Claim Integration v0.1

RESULT: PASS
primary_source_claim_integration_v0_1=true

## Gate summary

- integration_decision={INTEGRATION_DECISION}
- promotion_scope={PROMOTION_SCOPE}
- docs_updated={len(DOCS_TO_UPDATE)}
- source_claims_integrated={len(records)}
- runtime_adoption_allowed=false
- dependency_adoption_allowed=false

## Updated docs

- {rel(OPEN_SOURCE_MAP)}
- {rel(PLATFORM_ROADMAP)}
- {rel(MARKET_TO_FACTORY_VISION)}

## Protected action flags

{flags}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-primary-source-claim-integration
owner_approval_required_before_execution: true
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review source-backed doc integration before using it for implementation planning
  - Confirm every promoted claim stays limited to architecture docs and plans
  - Keep dependency adoption and runtime integration behind later explicit gates
  - Do not adopt dependencies, integrate runtimes, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(records: list[dict]) -> dict:
    return {
        "validator_id": "validate_avf_primary_source_claim_integration_v0_1",
        "status": "PASS",
        "integration_decision": INTEGRATION_DECISION,
        "promotion_scope": PROMOTION_SCOPE,
        "docs_updated": len(DOCS_TO_UPDATE),
        "source_claims_integrated": len(records),
        "runtime_adoption_allowed": False,
        "dependency_adoption_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        "claim_boundary": false_boundary(),
    }


def main() -> None:
    require_records_review_gate(read_json(RECORDS_REVIEW_GATE))
    records = require_records(read_json(RECORDS))
    integration_map = build_integration_map(records)
    section = integration_section(integration_map["integrated_claims"])

    for doc_path in DOCS_TO_UPDATE:
        upsert_section(doc_path, section)

    write_json(INTEGRATION_MAP, integration_map)
    write_text(INTEGRATION_REPORT, build_report(records))
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(records))
    write_text(VALIDATION_REPORT, build_report(records))

    print("AVF Primary-Source Claim Integration v0.1")
    print("RESULT: PASS")
    print(f"integration_decision={INTEGRATION_DECISION}")
    print(f"promotion_scope={PROMOTION_SCOPE}")
    print(f"docs_updated={len(DOCS_TO_UPDATE)}")
    print(f"source_claims_integrated={len(records)}")
    print("runtime_adoption_allowed=false")
    print("dependency_adoption_allowed=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

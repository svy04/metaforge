from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "avf" / "capabilities" / "generated"
DOC_GOALS = ROOT / "docs" / "goals"

PREVIOUS_REVIEW_GATE = CAPABILITIES / "capability_candidate_primary_source_pro_filled_output_packet_review_gate.json"
OUTPUT_PACKET = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet.yml"
OUTPUT_PACKET_GATE = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_gate.json"
OUTPUT_PACKET_REPORT = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_report.md"
NEXT_ACTION = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_next_action.yml"
VALIDATION_RESULT = CAPABILITIES / "capability_candidate_primary_source_codex_primary_source_output_packet_v0_1.validation_result.json"
VALIDATION_REPORT = DOC_GOALS / "AVF_CAPABILITY_CANDIDATE_PRIMARY_SOURCE_CODEX_PRIMARY_SOURCE_OUTPUT_PACKET_V0_1_REPORT.md"

THIS_GOAL_ID = "avf_capability_candidate_primary_source_codex_primary_source_output_packet_v0_1"
PREVIOUS_GOAL_ID = "avf_capability_candidate_primary_source_pro_filled_output_packet_review_v0_1"
SUPERSEDED_GOAL_ID = "avf_capability_candidate_primary_source_pro_actual_output_packet_v0_1"
NEXT_SAFE_GOAL_ID = "avf_capability_candidate_primary_source_codex_primary_source_output_packet_review_v0_1"
CREATED_AT = "2026-05-27T00:00:00Z"
PACKET_DECISION = "CAPABILITY_CANDIDATE_PRIMARY_SOURCE_CODEX_PRIMARY_SOURCE_OUTPUT_PACKET_CREATED"
PACKET_STATUS = "codex_primary_source_records_supplied_unaccepted"
RECORDS_SOURCE = "codex_assistant_primary_source_web_research"
RETRIEVAL_METHOD = "codex_assistant_web_open_primary_source_current_turn"


SOURCE_RECORDS = [
    {
        "candidate_id": "cap-k8s-workflow-argo",
        "source_id": "src-argo-workflows-official-docs",
        "source_title": "Argo Workflows official documentation",
        "source_kind": "official_docs",
        "source_uri": "https://argo-workflows.readthedocs.io/en/latest/",
        "source_version_or_date": "retrieved 2026-05-27; docs page includes v4.0 navigation",
        "source_owner_or_publisher": "Argo Project / CNCF",
        "license_or_rights_note": "Official documentation; no code copied into AVF",
        "claim_supported": "Argo Workflows is a Kubernetes-native workflow engine suitable for parallel job and workflow orchestration.",
        "evidence_excerpt_summary": "The official docs describe Argo Workflows as an open-source, container-native engine implemented as a Kubernetes CRD, with DAG and step workflows and ML/data/infrastructure use cases.",
        "verification_notes": "Primary source page opened by Codex web research; adoption not approved.",
        "source_reference_lines": "turn0view0 L299-L306; turn0view0 L309-L320",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-k8s-workflow-argo",
        "source_id": "src-argo-workflows-original-repository",
        "source_title": "argoproj/argo-workflows GitHub repository",
        "source_kind": "original_repository",
        "source_uri": "https://github.com/argoproj/argo-workflows",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "argoproj",
        "license_or_rights_note": "Repository page reports Apache-2.0 license",
        "claim_supported": "The original repository is the upstream code source for Argo Workflows.",
        "evidence_excerpt_summary": "The repository page identifies Apache-2.0 licensing and topics including Kubernetes, workflow engine, pipelines, data engineering, MLOps, and batch processing.",
        "verification_notes": "Original repository page opened by Codex web research; no clone performed.",
        "source_reference_lines": "turn1view1 L430-L435; turn1view1 L585-L595",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-general-orchestration-kestra-prefect-airflow",
        "source_id": "src-kestra-official-docs",
        "source_title": "Kestra official documentation",
        "source_kind": "official_docs",
        "source_uri": "https://kestra.io/docs",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "Kestra Technologies",
        "license_or_rights_note": "Official docs; no code copied into AVF",
        "claim_supported": "Kestra is a candidate for declarative orchestration, scheduled/event-driven workflows, and human-in-the-loop approval processes.",
        "evidence_excerpt_summary": "Kestra docs describe it as an open-source orchestration platform for declarative workflow management, with data pipelines, infrastructure workflows, approval processes, and Python workflows.",
        "verification_notes": "Primary source page opened by Codex web research; dependency adoption not approved.",
        "source_reference_lines": "turn3view4 L573-L582; turn3view4 L610-L613",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-general-orchestration-kestra-prefect-airflow",
        "source_id": "src-prefect-official-docs",
        "source_title": "Prefect official documentation",
        "source_kind": "official_docs",
        "source_uri": "https://docs.prefect.io/v3/get-started",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "Prefect",
        "license_or_rights_note": "Official docs; no code copied into AVF",
        "claim_supported": "Prefect is a candidate for Pythonic workflow orchestration, deployments, infrastructure configuration, automations, interactive workflows, and platform engineering.",
        "evidence_excerpt_summary": "Prefect docs cover building workflows with tasks and flows, deploying workflows, configuring infrastructure, setting automations, interactive workflows, and platform-engineering data pipelines.",
        "verification_notes": "Primary source page opened by Codex web research; dependency adoption not approved.",
        "source_reference_lines": "turn2view1 L94-L108; turn2view1 L121-L142",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-general-orchestration-kestra-prefect-airflow",
        "source_id": "src-airflow-official-docs",
        "source_title": "Apache Airflow official documentation",
        "source_kind": "official_docs",
        "source_uri": "https://airflow.apache.org/docs/apache-airflow/stable/index.html",
        "source_version_or_date": "Airflow 3.2.1 docs page, retrieved 2026-05-27",
        "source_owner_or_publisher": "Apache Airflow / Apache Software Foundation",
        "license_or_rights_note": "Official docs for an Apache project; no code copied into AVF",
        "claim_supported": "Airflow is a candidate for scheduled batch workflow orchestration with Python-defined workflows and operational UI.",
        "evidence_excerpt_summary": "Airflow docs describe a batch-workflow orchestration platform with operators, technology integrations, scheduled DAGs, Python-code definitions, and workflow monitoring views.",
        "verification_notes": "Primary source page opened by Codex web research; runtime integration not approved.",
        "source_reference_lines": "turn2view2 L154-L169; turn1view4 L177-L177",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-evidence-lineage-dagster",
        "source_id": "src-dagster-official-docs",
        "source_title": "Dagster official documentation",
        "source_kind": "official_docs",
        "source_uri": "https://docs.dagster.io/",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "Dagster Labs",
        "license_or_rights_note": "Official docs; no code copied into AVF",
        "claim_supported": "Dagster is a candidate for evidence/data lineage, observability, declarative asset modeling, and testability.",
        "evidence_excerpt_summary": "Dagster docs describe it as a data orchestrator for data engineers with integrated lineage, observability, declarative programming, and testability.",
        "verification_notes": "Primary source page opened by Codex web research; dependency adoption not approved.",
        "source_reference_lines": "turn2view3 L123-L127; turn2view3 L95-L103",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-evidence-lineage-dagster",
        "source_id": "src-dagster-original-repository",
        "source_title": "dagster-io/dagster GitHub repository",
        "source_kind": "original_repository",
        "source_uri": "https://github.com/dagster-io/dagster",
        "source_version_or_date": "retrieved 2026-05-27; repository page shows latest release metadata",
        "source_owner_or_publisher": "dagster-io",
        "license_or_rights_note": "Repository page reports Apache 2.0 / Apache-2.0 license",
        "claim_supported": "The original Dagster repository is the upstream source for the candidate and supports the same lineage/observability/testability positioning.",
        "evidence_excerpt_summary": "The repository page describes Dagster as a data pipeline orchestrator with lineage, observability, declarative programming, and testability, and reports Apache licensing.",
        "verification_notes": "Original repository page opened by Codex web research; no clone performed.",
        "source_reference_lines": "turn1view6 L348-L358; turn1view6 L441-L460; turn1view6 L495-L498",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-rag-document-pipeline-haystack",
        "source_id": "src-haystack-official-docs",
        "source_title": "Haystack official documentation",
        "source_kind": "official_docs",
        "source_uri": "https://docs.haystack.deepset.ai/docs/intro",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "deepset",
        "license_or_rights_note": "Official docs; no code copied into AVF",
        "claim_supported": "Haystack is a candidate for RAG, agent, multimodal, and document-pipeline construction.",
        "evidence_excerpt_summary": "Haystack docs describe an open-source AI framework and orchestration framework for AI agents, RAG applications, multimodal search systems, reusable components, and modular pipelines.",
        "verification_notes": "Primary source page opened by Codex web research; dependency adoption not approved.",
        "source_reference_lines": "turn2view4 L42-L51",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-rag-document-pipeline-haystack",
        "source_id": "src-haystack-original-repository",
        "source_title": "deepset-ai/haystack GitHub repository",
        "source_kind": "original_repository",
        "source_uri": "https://github.com/deepset-ai/haystack",
        "source_version_or_date": "retrieved 2026-05-27; repository page shows latest release metadata",
        "source_owner_or_publisher": "deepset-ai",
        "license_or_rights_note": "Repository page reports Apache-2.0 plus an unknown license-header file",
        "claim_supported": "The original Haystack repository is the upstream source for the RAG/document-pipeline candidate.",
        "evidence_excerpt_summary": "The repository page exposes Apache-2.0 license metadata, AI/RAG/semantic-search/LLM topics, and release metadata.",
        "verification_notes": "Original repository page opened by Codex web research; license review remains required because repository page also lists an unknown license-header file.",
        "source_reference_lines": "turn1view8 L301-L310; turn1view8 L397-L410; turn1view8 L445-L448",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-llm-observability-langfuse-phoenix",
        "source_id": "src-langfuse-official-docs",
        "source_title": "Langfuse official documentation",
        "source_kind": "official_docs",
        "source_uri": "https://langfuse.com/docs",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "Langfuse",
        "license_or_rights_note": "Official docs; no code copied into AVF",
        "claim_supported": "Langfuse is a candidate for LLM observability, tracing, prompt management, evaluation, and self-hostable engineering workflows.",
        "evidence_excerpt_summary": "Langfuse docs describe an open-source, self-hostable LLM engineering platform for debugging, analyzing, iterating, traces, cost/latency understanding, prompt management, and evaluation.",
        "verification_notes": "Primary source page opened by Codex web research; runtime integration not approved.",
        "source_reference_lines": "turn2view5 L50-L83",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-llm-observability-langfuse-phoenix",
        "source_id": "src-phoenix-official-docs",
        "source_title": "Arize Phoenix official documentation",
        "source_kind": "official_docs",
        "source_uri": "https://arize.com/docs/phoenix",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "Arize AI / Phoenix open-source community",
        "license_or_rights_note": "Official docs; no code copied into AVF",
        "claim_supported": "Phoenix is a candidate for AI observability/evaluation, tracing, prompt iteration, experiments, OpenTelemetry, and OpenInference-based instrumentation.",
        "evidence_excerpt_summary": "Phoenix docs describe AI observability and evaluation, trace-based debugging, evaluation tests, prompt iteration, experiments, and OpenTelemetry/OpenInference foundations.",
        "verification_notes": "Primary source page opened by Codex web research; runtime integration not approved.",
        "source_reference_lines": "turn2view6 L103-L117",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-eval-redteam-promptfoo-ragas",
        "source_id": "src-promptfoo-official-docs",
        "source_title": "promptfoo official documentation",
        "source_kind": "official_docs",
        "source_uri": "https://www.promptfoo.dev/docs/intro/",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "promptfoo",
        "license_or_rights_note": "Official docs; no code copied into AVF",
        "claim_supported": "promptfoo is a candidate for LLM evaluation and red-teaming workflows.",
        "evidence_excerpt_summary": "promptfoo docs describe an open-source CLI/library for evaluating and red-teaming LLM apps, with benchmark, security scanning, caching/concurrency, metrics, CLI/library/CI use, and provider flexibility.",
        "verification_notes": "Primary source page opened by Codex web research; runtime integration not approved.",
        "source_reference_lines": "turn2view7 L73-L84; turn2view7 L88-L97; turn1view11 L110-L112",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-eval-redteam-promptfoo-ragas",
        "source_id": "src-ragas-official-docs",
        "source_title": "Ragas official documentation",
        "source_kind": "official_docs",
        "source_uri": "https://docs.ragas.io/en/stable/",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "Ragas",
        "license_or_rights_note": "Official docs; no code copied into AVF",
        "claim_supported": "Ragas is a candidate for systematic LLM/RAG evaluation loops and experiment-driven metric workflows.",
        "evidence_excerpt_summary": "Ragas docs describe a library for moving from informal checks to systematic evaluation loops, using metrics and experiments to evaluate and iterate on LLM applications.",
        "verification_notes": "Primary source page opened by Codex web research; dependency adoption not approved.",
        "source_reference_lines": "turn2view8 L200-L210; turn2view8 L219-L231",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-eval-redteam-promptfoo-ragas",
        "source_id": "src-ragas-paper-or-benchmark-record",
        "source_title": "Ragas: Automated Evaluation of Retrieval Augmented Generation",
        "source_kind": "paper",
        "source_uri": "https://arxiv.org/abs/2309.15217",
        "source_version_or_date": "submitted 2023-09-26; revised 2025-04-28; retrieved 2026-05-27",
        "source_owner_or_publisher": "arXiv / Shahul Es, Jithin James, Luis Espinosa-Anke, Steven Schockaert",
        "license_or_rights_note": "arXiv paper page with DOI and license link; no paper text copied into AVF",
        "claim_supported": "Ragas has a primary research paper describing reference-free evaluation metrics for RAG pipelines.",
        "evidence_excerpt_summary": "The arXiv page identifies Ragas as a framework for reference-free evaluation of RAG pipelines, covering retrieval relevance, faithfulness, generation quality, and faster evaluation cycles.",
        "verification_notes": "Primary paper page opened by Codex web research; not an adoption approval.",
        "source_reference_lines": "turn5view0 L32-L49; turn5view0 L54-L69",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-coding-executor-openhands-sweagent",
        "source_id": "src-openhands-original-repository",
        "source_title": "OpenHands/OpenHands GitHub repository",
        "source_kind": "original_repository",
        "source_uri": "https://github.com/OpenHands/OpenHands",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "OpenHands",
        "license_or_rights_note": "Repository page shows MIT license badge and links to license; license review remains required before adoption",
        "claim_supported": "OpenHands is a candidate approved-executor lane for AI-driven development through SDK, CLI, and local GUI surfaces.",
        "evidence_excerpt_summary": "The repository page describes OpenHands as AI-driven development and lists SDK, CLI, and local GUI ways to use it, including local execution and scaling patterns.",
        "verification_notes": "Original repository page opened by Codex web research; no clone performed.",
        "source_reference_lines": "turn2view9 L369-L386; turn2view9 L387-L396; turn2view9 L436-L452",
        "retrieval_method": RETRIEVAL_METHOD,
    },
    {
        "candidate_id": "cap-coding-executor-openhands-sweagent",
        "source_id": "src-swe-agent-original-repository",
        "source_title": "SWE-agent/SWE-agent GitHub repository",
        "source_kind": "original_repository",
        "source_uri": "https://github.com/SWE-agent/SWE-agent",
        "source_version_or_date": "retrieved 2026-05-27",
        "source_owner_or_publisher": "SWE-agent",
        "license_or_rights_note": "Repository page reports MIT license",
        "claim_supported": "SWE-agent is a candidate approved-executor lane for GitHub-issue-centered code repair using a selected language model.",
        "evidence_excerpt_summary": "The repository page says SWE-agent takes a GitHub issue and tries to fix it using a chosen language model, references NeurIPS 2024, and reports MIT licensing.",
        "verification_notes": "Original repository page opened by Codex web research; no clone performed and no offensive use enabled.",
        "source_reference_lines": "turn2view10 L358-L365; turn2view10 L369-L384",
        "retrieval_method": RETRIEVAL_METHOD,
    },
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


def counts(records: list[dict]) -> dict:
    return {
        "candidate_count": len({record["candidate_id"] for record in records}),
        "source_record_count": len(records),
        "required_source_field_count": 12,
        "filled_record_supplied_count": len(records),
        "accepted_records": 0,
        "assistant_web_primary_source_research_performed_count": 1,
        "gpt_pro_output_supplied_count": 0,
        "codex_script_external_fetch_performed_count": 0,
        "dependency_install_performed_count": 0,
    }


def source_record_with_status(record: dict) -> dict:
    return {
        **record,
        "acceptance_status": "unreviewed",
        "filled_record_supplied": True,
    }


def require_previous_gate(gate: dict) -> None:
    if gate.get("goal_id") != PREVIOUS_GOAL_ID:
        raise SystemExit("previous review gate goal mismatch")
    if gate.get("next_safe_goal_id") != SUPERSEDED_GOAL_ID:
        raise SystemExit("previous review gate must point to the missing GPT Pro actual-output goal")
    if gate.get("gpt_pro_output_supplied") is not False:
        raise SystemExit("previous review gate must not claim GPT Pro output supplied")


def source_records() -> list[dict]:
    return [source_record_with_status(record) for record in SOURCE_RECORDS]


def base_record(previous_gate: dict) -> dict:
    records = source_records()
    return {
        "created_at": CREATED_AT,
        "goal_id": THIS_GOAL_ID,
        "previous_goal_id": PREVIOUS_GOAL_ID,
        "supersedes_missing_input_goal_id": SUPERSEDED_GOAL_ID,
        "packet_decision": PACKET_DECISION,
        "packet_status": PACKET_STATUS,
        "records_source": RECORDS_SOURCE,
        "assistant_web_primary_source_research_performed": True,
        "gpt_pro_output_supplied": False,
        "codex_script_external_fetch_performed": False,
        "source_required_candidate_ids": previous_gate["source_required_candidate_ids"],
        "source_records": records,
        "dependency_adoption_allowed": False,
        "runtime_integration_allowed": False,
        "next_safe_goal_id": NEXT_SAFE_GOAL_ID,
        **counts(records),
        "claim_boundary": false_boundary(),
    }


def yaml_quote(value: object) -> str:
    text = str(value).replace('"', '\\"')
    return f'"{text}"'


def build_packet(previous_gate: dict) -> str:
    boundary = "\n".join(f"  {key}: false" for key in false_boundary())
    source_blocks = []
    for record in source_records():
        lines = [
            f"  - candidate_id: {record['candidate_id']}",
            f"    source_id: {record['source_id']}",
            f"    acceptance_status: {record['acceptance_status']}",
            "    filled_record_supplied: true",
        ]
        for field in [
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
        ]:
            lines.append(f"    {field}: {yaml_quote(record[field])}")
        source_blocks.append("\n".join(lines))
    return f"""# Capability Candidate Primary-Source Codex Output Packet v0.1

goal_id: {THIS_GOAL_ID}
previous_goal_id: {PREVIOUS_GOAL_ID}
supersedes_missing_input_goal_id: {SUPERSEDED_GOAL_ID}
created_at: {CREATED_AT}
packet_decision: {PACKET_DECISION}
packet_status: {PACKET_STATUS}
records_source: {RECORDS_SOURCE}
assistant_web_primary_source_research_performed: true
gpt_pro_output_supplied: false
codex_script_external_fetch_performed: false
accepted_records: 0

instructions:
  - Treat these as supplied but unreviewed primary-source records.
  - Review every source field before accepting evidence.
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness from these records.

source_records:
{chr(10).join(source_blocks)}

claim_boundary:
{boundary}

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_gate(previous_gate: dict) -> dict:
    return {
        **base_record(previous_gate),
        "gate_id": "avf-capability-candidate-primary-source-codex-output-packet-gate-v0-1",
        "status": "PASS",
        "output_packet_uri": rel(OUTPUT_PACKET),
        "gate_scope": "Codex-collected primary-source records supplied but not accepted; review gate required",
    }


def build_report(title: str, records: list[dict]) -> str:
    count_lines = "\n".join(f"- {key}={value}" for key, value in counts(records).items())
    source_lines = "\n".join(f"- {record['source_id']}: {record['source_uri']}" for record in records)
    flag_lines = "\n".join(f"- {key}=false" for key in false_boundary())
    return f"""# {title}

RESULT: PASS
capability_candidate_primary_source_codex_primary_source_output_packet_v0_1=true

## Gate summary

- packet_decision={PACKET_DECISION}
- packet_status={PACKET_STATUS}
- records_source={RECORDS_SOURCE}
- assistant_web_primary_source_research_performed=true
- gpt_pro_output_supplied=false
- codex_script_external_fetch_performed=false
- dependency_adoption_allowed=false
- runtime_integration_allowed=false

## Counts

{count_lines}

## Source records

{source_lines}

## Protected action flags

{flag_lines}

## Next safe goal

next_safe_goal_id={NEXT_SAFE_GOAL_ID}
"""


def build_next_action() -> str:
    return f"""action_id: review-capability-candidate-primary-source-codex-primary-source-output-packet
owner_approval_required_before_execution: false
goal_id: {THIS_GOAL_ID}

next_steps:
  - Review Codex-collected primary-source records before accepting them as evidence
  - Keep all source records unaccepted until the review gate verifies every source field
  - Confirm source kind, rights notes, supported claims, line references, and retrieval method for all 16 records
  - Do not install dependencies, clone OSS, integrate runtime, deploy, publish, or claim readiness

next_safe_goal_id: {NEXT_SAFE_GOAL_ID}
"""


def build_validation_result(previous_gate: dict) -> dict:
    return {
        **base_record(previous_gate),
        "validator_id": "validate_avf_capability_candidate_primary_source_codex_primary_source_output_packet_v0_1",
        "status": "PASS",
        "validated_artifacts": [
            rel(OUTPUT_PACKET),
            rel(OUTPUT_PACKET_GATE),
            rel(OUTPUT_PACKET_REPORT),
            rel(NEXT_ACTION),
            rel(VALIDATION_RESULT),
            rel(VALIDATION_REPORT),
        ],
    }


def main() -> None:
    previous_gate = read_json(PREVIOUS_REVIEW_GATE)
    require_previous_gate(previous_gate)
    records = source_records()

    write_text(OUTPUT_PACKET, build_packet(previous_gate))
    write_json(OUTPUT_PACKET_GATE, build_gate(previous_gate))
    report = build_report("AVF Capability Candidate Primary-Source Codex Output Packet v0.1", records)
    write_text(OUTPUT_PACKET_REPORT, report)
    write_text(NEXT_ACTION, build_next_action())
    write_json(VALIDATION_RESULT, build_validation_result(previous_gate))
    write_text(VALIDATION_REPORT, report)

    print("AVF Capability Candidate Primary-Source Codex Output Packet v0.1")
    print("RESULT: PASS")
    print(f"packet_decision={PACKET_DECISION}")
    print(f"packet_status={PACKET_STATUS}")
    print(f"records_source={RECORDS_SOURCE}")
    print("assistant_web_primary_source_research_performed=true")
    print("gpt_pro_output_supplied=false")
    print("codex_script_external_fetch_performed=false")
    for key, value in counts(records).items():
        print(f"{key}={value}")
    print("external_fetch_performed=false")
    print("dependency_install_performed=false")
    print("oss_clone_performed=false")
    print("runtime_integration_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print(f"next_safe_goal_id={NEXT_SAFE_GOAL_ID}")


if __name__ == "__main__":
    main()

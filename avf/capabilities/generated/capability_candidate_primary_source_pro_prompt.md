# GPT Pro Prompt: AVF Capability Candidate Primary-Source Evidence Fill v0.1

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
- source_id
- source_title
- source_kind
- source_uri
- source_version_or_date
- source_owner_or_publisher
- license_or_rights_note
- claim_supported
- evidence_excerpt_summary
- verification_notes
- source_reference_lines
- retrieval_method

Output contract:
```yaml
goal_id: avf_capability_candidate_primary_source_pro_prompt_v0_1
filled_by: gpt_pro_manual_primary_source_research
source_collection_context: external_manual_research_not_codex_runtime
records:
  - candidate_id: cap-k8s-workflow-argo
    candidate_name: Argo Workflows
    source_records:
    - source_target_id: src-argo-workflows-official-docs
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
    - source_target_id: src-argo-workflows-original-repository
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
  - candidate_id: cap-general-orchestration-kestra-prefect-airflow
    candidate_name: Kestra / Prefect / Airflow
    source_records:
    - source_target_id: src-kestra-official-docs
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
    - source_target_id: src-prefect-official-docs
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
    - source_target_id: src-airflow-official-docs
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
  - candidate_id: cap-evidence-lineage-dagster
    candidate_name: Dagster
    source_records:
    - source_target_id: src-dagster-official-docs
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
    - source_target_id: src-dagster-original-repository
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
  - candidate_id: cap-rag-document-pipeline-haystack
    candidate_name: Haystack
    source_records:
    - source_target_id: src-haystack-official-docs
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
    - source_target_id: src-haystack-original-repository
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
  - candidate_id: cap-llm-observability-langfuse-phoenix
    candidate_name: Langfuse / Phoenix
    source_records:
    - source_target_id: src-langfuse-official-docs
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
    - source_target_id: src-phoenix-official-docs
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
  - candidate_id: cap-eval-redteam-promptfoo-ragas
    candidate_name: promptfoo / Ragas
    source_records:
    - source_target_id: src-promptfoo-official-docs
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
    - source_target_id: src-ragas-official-docs
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
    - source_target_id: src-ragas-paper-or-benchmark-record
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
  - candidate_id: cap-coding-executor-openhands-sweagent
    candidate_name: OpenHands / SWE-agent
    source_records:
    - source_target_id: src-openhands-original-repository
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
    - source_target_id: src-swe-agent-original-repository
      source_input_status: owner_to_fill_from_primary_source
      source_id: ""
      source_title: ""
      source_kind: ""
      source_uri: ""
      source_version_or_date: ""
      source_owner_or_publisher: ""
      license_or_rights_note: ""
      claim_supported: ""
      evidence_excerpt_summary: ""
      verification_notes: ""
      source_reference_lines: ""
      retrieval_method: ""
next_safe_goal_id: avf_capability_candidate_primary_source_pro_prompt_review_v0_1
```

Review rules:
- Prefer official documentation over tutorials.
- Prefer original repositories over package summaries.
- Prefer papers, standards, patents, and maintained implementations when they are the original authority.
- Include concise evidence summaries, not long quotations.
- Keep license and rights notes explicit.
- If a source target cannot be supported by a primary source, write `unsupported_primary_source_not_found` in the relevant fields and explain why in `verification_notes`.

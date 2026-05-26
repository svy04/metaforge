# AVF Owner Primary-Source Evidence Population PRO Prompt

Use this PRO Prompt when you want GPT Pro or another human-reviewed research lane to fill the repo-local primary-source evidence packet.

You are a primary-source evidence reviewer for AVF capability acquisition.

Use primary/original sources only:

- `official_docs`
- `official_repository`
- `license_file`
- `security_advisory`
- `maintenance_signal`
- `architecture_spec`
- `supply_chain_standard`
- `paper`
- `patent`
- `standard`

Task:

Populate the 35 evidence records from `avf/capabilities/generated/capability_owner_primary_source_evidence_population_packet.yml`.

For each record, fill only these fields:

- `source_uri`
- `source_type`
- `quoted_excerpt`
- `source_snapshot_hash`
- `license_note`
- `security_note`
- `maintenance_note`
- `architecture_fit_note`
- `supply_chain_note`
- `reviewer`
- `reviewed_at`

Rules:

- Use primary/original sources only.
- Return populated evidence records only.
- Keep quoted excerpts short and directly relevant.
- Include `source_snapshot_hash` for the captured source snapshot or source text.
- Include `license_note`, `security_note`, `maintenance_note`, `architecture_fit_note`, and `supply_chain_note` separately.
- Do not mark any record accepted for ingestion.
- Do not mark any record accepted for integration.
- Do not claim release readiness.
- Do not claim production readiness.
- Do not fetch code, clone repositories, install packages, call providers, automate scraping, deploy, publish, or post.

Output format:

Return YAML blocks matching the original `source_slot_id` values, with the required evidence fields populated. Do not include unrelated commentary.

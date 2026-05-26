# Owner-Supplied Primary-Source Evidence Record Completion Guide v0.1

goal_id: avf_owner_supplied_primary_source_evidence_record_completion_guide_v0_1
previous_goal_id: avf_owner_supplied_primary_source_evidence_record_review_v0_1
created_at: 2026-05-27T00:00:00Z
guide_decision: OWNER_SUPPLIED_SOURCE_RECORD_COMPLETION_GUIDE_READY

This guide explains how the owner can complete a local primary-source evidence record. It does not fetch, scrape, clone, install, call providers, deploy, publish, or claim readiness.

## Required fields

- `source_id`: Use a stable id such as src-langgraph-docs-overview or src-react-paper.
- `source_title`: Use the exact title from the source, not a summary title.
- `source_kind`: Use one allowed kind: official_docs, original_repository, paper, patent, standard, maintained_implementation, or local_repo_evidence.
- `source_uri`: Paste the URL or local path supplied by the owner. Do not ask Codex to fetch the URL.
- `source_version_or_date`: Record a publication date, version, commit, tag, standard version, or access date.
- `source_owner_or_publisher`: Record the project, standards body, authors, company, university, or local repo owner.
- `license_or_rights_note`: Record license, terms, open-access status, or owner-supplied rights notes.
- `claim_supported`: Write one concrete AVF design or implementation claim this source supports.
- `evidence_excerpt_summary`: Summarize only the owner-supplied excerpt or known local evidence; do not invent unseen source content.
- `verification_notes`: State how a later reviewer can verify the source without changing the protected action boundary.

## Allowed source kinds

- `official_docs`
- `original_repository`
- `paper`
- `patent`
- `standard`
- `maintained_implementation`
- `local_repo_evidence`

## Boundary

- Do not ask Codex to fetch the URL
- No source collection execution
- No provider calls
- No live model calls
- No external service calls
- No external fetch
- No automated scraping
- No OSS clone
- No package install
- No dependency install
- No runtime integration
- No deploy
- No publish
- No release readiness claim
- No production readiness claim

## Next safe goal

next_safe_goal_id: avf_owner_supplied_primary_source_evidence_record_template_v0_1

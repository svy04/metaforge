# Autonomous Factory Creation Levels

## Purpose

Creation levels define what "AI creates directly" means without collapsing safe draft creation, repo-local artifacts, PR implementation, publishing, and bounded campaigns into one risk category.

## Levels

### Creation Level 0: Think

Market analysis, strategy hypotheses, product angles, risk notes, and evidence plans.

### Creation Level 1: Draft

Text drafts, image prompts, video scripts, product specs, PRD drafts, and Codex task drafts.

### Creation Level 2: Local Artifact

Repo-local files, sample outputs, validation reports, schemas, fixtures, and evidence entries.

### Creation Level 3: Approved PR

Codex performs an approved PR-sized implementation with validation commands and forbidden changes.

### Creation Level 4: Approved Publish

Human-approved publication to blog, SNS, newsletter, community, or docs channels.

### Creation Level 5: Bounded Autonomous Campaign

Strictly bounded future operation under approved channels, budget, cadence, rollback, audit, and policy constraints.

## Current Allowed Level

Current AVF work is limited to Creation Level 0, Creation Level 1, and Creation Level 2, with Creation Level 3 possible only through explicit PR-sized Codex work.

## Boundary

- repo_local_internal_only
- runtime implementation: blocked
- provider calls: blocked
- live model calls: blocked
- external service calls: blocked
- scraping implementation: blocked
- posting automation: blocked
- deploy: blocked
- publish: blocked
- production readiness claim: blocked
- release readiness claim: blocked
- public readiness claim: blocked
- fake human impersonation: blocked
- engagement manipulation: blocked
- protected_action_executed=false

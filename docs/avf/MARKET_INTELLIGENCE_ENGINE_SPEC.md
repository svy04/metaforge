# Market Intelligence Engine Spec

## Role

The Market Intelligence Engine observes allowed signals and converts them into market maps, pain signal maps, audience assumptions, competitor assumptions, and opportunity theses.

## Inputs

- owner-provided research
- repo-local evidence
- public docs manually supplied by the owner
- allowed RSS or public sources in future approved integrations
- GitHub repository signals in future approved integrations
- community notes imported by the owner

## Outputs

- market map
- competitor map
- pain signal map
- trend brief
- audience map
- opportunity thesis
- weak signal report

## Source Notes

The engine may reference external sources such as web4.ai for high-level vision comparison, but this design does not implement browsing, scraping, provider calls, or autonomous collection.

## Safety Boundary

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

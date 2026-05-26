# Contributing to OpenClaude

Thanks for contributing.

OpenClaude is a fast-moving open-source coding-agent CLI with support for multiple providers, local backends, MCP, and a terminal-first workflow. The best contributions here are focused, well-tested, and easy to review.

## Before You Start

- Search existing [issues](https://github.com/Gitlawb/openclaude/issues) and [discussions](https://github.com/Gitlawb/openclaude/discussions) before opening a new thread.
- Use issues for confirmed bugs and actionable feature work.
- Use discussions for setup help, ideas, and general community conversation.
- Use [SUPPORT.md](SUPPORT.md) when you need setup help, troubleshooting direction, or help deciding whether something is a support request, bug, security report, or feature proposal.
- For larger changes, open an issue first so the scope is clear before implementation.
- For security reports, follow [SECURITY.md](SECURITY.md).
- Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) in issues, discussions, pull requests, and other project spaces.

## Local Setup

Install dependencies:

```bash
bun install
```

Build the CLI:

```bash
bun run build
```

Smoke test:

```bash
bun run smoke
```

Run the app locally:

```bash
bun run dev
```

If you are working on provider setup or saved profiles, useful commands include:

```bash
bun run profile:init
bun run dev:profile
```

## Development Workflow

- Keep PRs focused on one problem or feature.
- Avoid mixing unrelated cleanup into the same change.
- Preserve existing repo patterns unless the change is intentionally refactoring them.
- Add or update tests when the change affects behavior.
- Update docs when setup, commands, or user-facing behavior changes.

## Validation

At minimum, run the most relevant checks for your change.

Common checks:

```bash
bun run build
bun run smoke
bun run verify:privacy
```

Focused tests:

```bash
bun test ./path/to/test-file.test.ts
```

When working on provider/runtime setup, this can also help:

```bash
bun run doctor:runtime
```

For product-quality or claim-boundary changes, prefer the narrowest relevant product gate first, then run the broader gate when the local environment allows it:

```bash
bun run product:quality
```

If `bun run product:quality` stops at a protected local environment boundary, record the exact failing command and blocker instead of converting the result into a release, production, public, external-validation, or autonomous-reliability claim.

## Evidence and Claim Boundaries

- Name the exact command outputs, reports, fixtures, screenshots, or traces that support the change.
- Prefer primary sources for design and product-quality changes: official docs, original repositories, standards, papers, patents, and maintained implementations.
- Do not include API keys, provider credentials, tokens, cookies, raw private prompts, raw user/session payloads, or private local profiles in issues, PRs, logs, screenshots, or trace artifacts.
- Do not claim release readiness, production readiness, public readiness, external validation, autonomous reliability, provider-backed execution, or live model validation unless a separate evidence and authorization packet exists.
- Do not perform deploy, publish, launch, production OpenClaude mutation, MFH mutation, protected repo mutation, real product repo mutation, canonical memory/governance write, canonical decision ledger write, or mth resolution as part of a routine contribution.

## Pull Requests

Good PRs usually include:

- a short explanation of what changed
- why it changed
- the user or developer impact
- the exact checks you ran

If the PR touches UI, terminal presentation, or the VS Code extension, include screenshots when useful.

If the PR changes provider behavior, mention which provider path was tested.

## Code Style

- Follow the existing code style in the touched files.
- Prefer small, readable changes over broad rewrites.
- Do not reformat unrelated files just because they are nearby.
- Keep comments useful and concise.

## Provider Changes

OpenClaude supports multiple provider paths. If you change provider logic:

- be explicit about which providers are affected
- avoid breaking third-party providers while fixing first-party behavior
- test the exact provider/model path you changed when possible
- call out any limitations or follow-up work in the PR description

## Community

Please be respectful and constructive with other contributors.

Maintainers may ask for:

- narrower scope
- focused follow-up PRs
- stronger validation
- docs updates for behavior changes

That is normal and helps keep the project reviewable as it grows.

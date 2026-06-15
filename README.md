![Metaforge banner](docs/assets/metaforge-banner.gif)

# Metaforge

[English](README.md) | [한국어](README.ko.md)

Metaforge is a Meta/MFH/Orchestra operating system for governed-code execution.

It turns owner intent into durable goals, routes work through Claude and Codex OAuth-backed agent paths, preserves operating memory in **Meta**, forces execution claims through **MFH** evidence gates, and uses **Orchestra** to plan, challenge, execute, review, and promote work.

OpenClaude is the local CLI substrate Metaforge currently rides on. It provides the terminal UX, tools, MCP, slash commands, streaming output, provider routing, and credential surfaces; Metaforge is the operating layer above it.

Orchestra is the runtime-wired layer in this package today. Meta and MFH are governance, schema, and evidence-gate surfaces that constrain how the runtime is used; they are not separate runtime modules in this checkout. AVF Influence Factory is a repo-local manual artifact lane, not part of the default CLI runtime or CI path; generated AVF operator run outputs are intentionally ignored and kept out of the public checkout.

Origin and license boundary: this repository contains runtime code derived from Anthropic's Claude Code CLI. OpenClaude contributor modifications are offered under MIT where legally permissible; this is not a blanket MIT license over the derived runtime. See [LICENSE](LICENSE) before reusing or redistributing code from this repository.

[![PR Checks](https://github.com/svy04/metaforge/actions/workflows/pr-checks.yml/badge.svg?branch=main)](https://github.com/svy04/metaforge/actions/workflows/pr-checks.yml)
[![Security Policy](https://img.shields.io/badge/security-policy-0f766e)](SECURITY.md)
[![License](https://img.shields.io/badge/license-see_LICENSE-2563eb)](LICENSE)

[Operating Layers](#operating-layers) | [Mimesis](#mimesis-engineering) | [Proof Pack](#public-proof-pack) | [Runtime Setup](#quick-start) | [Routes](#runtime-routes) | [Evidence Gates](#evidence-gates) | [Source Build](#source-build-and-local-development) | [Community](#community)

## Current Proof Ladder

| Question | Current answer |
| --- | --- |
| What is it? | Meta/MFH/Orchestra OS for evidence-gated agent work, riding on the OpenClaude CLI runtime. |
| Fastest verification | `bun run product:public-artifact-hygiene`, `bun run verify:privacy`, and the generated product-quality reports. |
| Strongest public evidence | [Public proof pack](docs/marketing/metaforge-public-proof-pack-2026-06-14.md), [model/system card](docs/MODEL_SYSTEM_CARD.md), and [evidence manifest](docs/product-quality/product-evidence-manifest.md). |
| What this proves | Current repository positioning, local no-provider gates, claim boundaries, and public-surface hygiene. |
| What this does not prove | Production readiness, hosted deployment, external validation, standards compliance, benchmark superiority, or autonomous reliability. |

## Why Metaforge

- Treat the owner as the strategic governor, not the technical bottleneck.
- Keep durable context, source ledgers, decisions, and operator boundaries in Meta.
- Run Claude and Codex through OAuth-backed routes when credentials are present.
- Let Orchestra split work across planner, skeptic, implementer, shadow review, cross-review, evidence arbiter, and human gate roles.
- Make MFH-style evidence gates the condition for closure: tests, reports, source reconciliation, claim boundaries, and rollback notes.
- Use OpenClaude as the local terminal runtime instead of making OpenClaude the product center.

## Mimesis Engineering

Mimesis Engineering is Metaforge's improvement engine: take the best solved examples in the world, decompose their load-bearing structure, adapt the structure into the local operating system, and verify the result before making stronger claims.

The loop is source-first and anti-persona. It does not ask agents to pretend to be experts. It gives them expert artifacts, standards, papers, patents, repositories, product surfaces, failure detectors, and acceptance gates.

- **Meta** keeps the source ledger, decisions, and operating memory.
- **Orchestra** dispatches scouts, implementers, critics, and reviewers in parallel.
- **MFH** decides whether the adapted structure produced evidence or only a better-sounding story.

Start here: [docs/MIMESIS_ENGINEERING.md](docs/MIMESIS_ENGINEERING.md). Current source ledger: [docs/research/mimesis-engineering-source-ledger-2026-06-14.md](docs/research/mimesis-engineering-source-ledger-2026-06-14.md).

## Public Proof Pack

Use the public proof pack when describing Metaforge outside the repo. It gives the strongest current copy blocks, but binds each claim to local evidence and explicit non-claims.

- [Metaforge Public Proof Pack](docs/marketing/metaforge-public-proof-pack-2026-06-14.md)
- [Public proof-pack source ledger](docs/research/public-proof-pack-source-ledger-2026-06-14.md)
- [GitHub profile refresh evidence](docs/profile/github-profile-refresh-evidence-2026-06-14.md)

## Operating Layers

| Layer | Role |
| --- | --- |
| Meta | Operator memory, decisions, raw/wiki source records, approval boundaries |
| Goal Kernel | Durable goal hierarchy, success criteria, non-goals, validation commands, pause and rollback rules |
| Orchestra | Claude/Codex agent routing, planning, critique, shadow execution, cross-review, evidence arbitration, promotion |
| MFH | Governed-code gate for drift, state, evidence, closure, release claims, and false-completion prevention |
| OpenClaude runtime | Local CLI substrate for tools, MCP, slash commands, provider profiles, streaming, and credential-backed model routes |

Wiring boundary: Orchestra is runtime-wired in `src/` today. Meta and MFH are governance, schema, and evidence-gate surfaces in `docs/`, reports, and product-quality gates. AVF Influence Factory is a repo-local manual artifact lane under `avf/` and `scripts/`, not a default runtime import. Generated AVF operator runs are local-only artifacts; see [avf/influence_factory/operator_runs.md](avf/influence_factory/operator_runs.md).

## Claude And Codex Routes

Metaforge can use Claude and Codex as execution engines inside Orchestra. Claude routes can support planner, skeptic, and review roles through Claude OAuth when available. Codex routes can support visible execution and implementation roles through Codex OAuth, Codex CLI auth, OpenClaude secure storage, or environment credentials.

These routes are engines, not the product center. The operating contract remains Meta for memory, Orchestra for work routing, and MFH for evidence-gated closure.

## Quick Start

This checkout builds a local OpenClaude-derived CLI runtime while the Meta/MFH/Orchestra operating layer continues to harden.

### Build This Checkout

```bash
bun install
bun run build
node dist/cli.mjs
```

The registry command `npm install -g @gitlawb/openclaude` installs the external OpenClaude npm package, not a Metaforge release artifact from this checkout.

If the runtime later reports `ripgrep not found`, install ripgrep system-wide and confirm `rg --version` works in the same terminal before starting OpenClaude.

### External Package Start

```bash
openclaude
```

Use this command only after intentionally installing the external OpenClaude npm package.

Inside the runtime:

- run `/provider` for guided provider setup and saved profiles
- run `/onboard-github` for GitHub Models onboarding

### Fastest OpenAI setup

macOS / Linux:

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=<key>
export OPENAI_MODEL=<current-openai-tool-model>

openclaude
```

Windows PowerShell:

```powershell
$env:CLAUDE_CODE_USE_OPENAI="1"
$env:OPENAI_API_KEY="<key>"
$env:OPENAI_MODEL="<current-openai-tool-model>"

openclaude
```

Replace `<current-openai-tool-model>` with the current OpenAI model you have
enabled for tool/function calling. Public docs intentionally avoid pinning a
stale model name.

### Fastest local Ollama setup

macOS / Linux:

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_MODEL=qwen2.5-coder:7b

openclaude
```

Windows PowerShell:

```powershell
$env:CLAUDE_CODE_USE_OPENAI="1"
$env:OPENAI_BASE_URL="http://localhost:11434/v1"
$env:OPENAI_MODEL="qwen2.5-coder:7b"

openclaude
```

### Using Ollama's launch command

If you have [Ollama](https://ollama.com) installed, you can skip the env var setup entirely:

```bash
ollama launch openclaude --model qwen2.5-coder:7b
```

This automatically sets `ANTHROPIC_BASE_URL`, model routing, and auth so all API traffic goes through your local Ollama instance. Works with any model you have pulled — local or cloud.

## Setup Guides

Beginner-friendly guides:

- [Non-Technical Setup](docs/non-technical-setup.md)
- [Windows Quick Start](docs/quick-start-windows.md)
- [macOS / Linux Quick Start](docs/quick-start-mac-linux.md)

Advanced and source-build guides:

- [Advanced Setup](docs/advanced-setup.md)
- [Android Install](ANDROID_INSTALL.md)

## Runtime Routes

| Route | Setup Path | Notes |
| --- | --- | --- |
| Claude OAuth | built-in auth flow | Enables Claude-native roles when OAuth credentials are present |
| Codex OAuth | `/provider` | Opens ChatGPT sign-in in your browser and stores Codex credentials securely |
| Codex | `/provider` | Uses existing Codex CLI auth, OpenClaude secure storage, or env credentials |
| OpenAI-compatible | `/provider` or env vars | Works with OpenAI, OpenRouter, DeepSeek, Groq, Mistral, LM Studio, and other compatible `/v1` servers |
| Gemini | `/provider` or env vars | Supports API key, access token, or local ADC workflow on current `main` |
| GitHub Models | `/onboard-github` | Interactive onboarding with saved credentials |
| Ollama | `/provider`, env vars, or `ollama launch` | Local inference with no API key |
| Atomic Chat | `/provider`, env vars, or `bun run dev:atomic-chat` | Local Model Provider; auto-detects loaded models |
| Bedrock / Vertex / Foundry | env vars | Additional provider integrations for supported environments |

## Runtime Capabilities

- **Tool-driven coding workflows**: Bash, file read/write/edit, grep, glob, agents, tasks, MCP, and slash commands
- **Streaming responses**: Real-time token output and tool progress
- **Tool calling**: Multi-step tool loops with model calls, tool execution, and follow-up responses
- **Images**: URL and base64 image inputs for providers that support vision
- **Provider profiles**: Guided setup plus saved `.openclaude-profile.json` support
- **Local and remote model backends**: Cloud APIs, local servers, and Apple Silicon local inference

## Evidence Gates

Metaforge treats closure as a measured state, not an agent self-report. MFH-style gates require a goal to carry success criteria, non-goals, validation commands, evidence artifacts, claim boundaries, and rollback or pause rules before stronger completion claims are made.

- Goal contracts live in [docs/GOAL_SCHEMA.md](docs/GOAL_SCHEMA.md)
- Meta/MFH import boundaries live in [docs/MFH_META_SYNTHESIS.md](docs/MFH_META_SYNTHESIS.md)
- Orchestra runtime roles live in [docs/AGENT_REGISTRY.md](docs/AGENT_REGISTRY.md)
- Public claim boundaries are checked with `bun run product:public-claim-boundary`
- Runtime privacy boundaries are checked with `bun run verify:privacy`

## Provider Notes

The OpenClaude runtime supports multiple providers, but behavior is not identical across all of them.

- Anthropic-specific features may not exist on other providers
- Tool quality depends heavily on the selected model
- Smaller local models can struggle with long multi-step tool flows
- Some providers impose lower output caps than the CLI defaults, and the runtime adapts where possible

For best results, use models with strong tool/function calling support.

## Agent Routing

Metaforge uses the OpenClaude runtime's settings-based routing to send different agents to different models. This is the practical substrate for Orchestra roles such as planner, skeptic, implementer, reviewer, and fallback worker.

Add to `~/.claude/settings.json`:

```json
{
  "agentModels": {
    "deepseek-chat": {
      "base_url": "https://api.deepseek.com/v1",
      "api_key": "<deepseek-api-key>"
    },
    "<current-openai-tool-model>": {
      "base_url": "https://api.openai.com/v1",
      "api_key": "<openai-api-key>"
    }
  },
  "agentRouting": {
    "Explore": "deepseek-chat",
    "Plan": "<current-openai-tool-model>",
    "general-purpose": "<current-openai-tool-model>",
    "frontend-dev": "deepseek-chat",
    "default": "<current-openai-tool-model>"
  }
}
```

When no routing match is found, the global provider remains the fallback.

> **Note:** `api_key` values in `settings.json` are stored in plaintext. Keep this file private and do not commit it to version control.

## Web Search and Fetch

By default, `WebSearch` works on non-Anthropic models using DuckDuckGo. This gives OpenAI-compatible providers such as OpenAI, DeepSeek, Gemini routes, Ollama, and local servers a free web search path out of the box.

> **Note:** DuckDuckGo fallback works by scraping search results and may be rate-limited, blocked, or subject to DuckDuckGo's Terms of Service. If you want a more reliable supported option, configure Firecrawl.

For Anthropic-native backends and Codex responses, the runtime keeps the native provider web search behavior.

`WebFetch` works, but its basic HTTP plus HTML-to-markdown path can still fail on JavaScript-rendered sites or sites that block plain HTTP requests.

Set a [Firecrawl](https://firecrawl.dev) API key if you want Firecrawl-powered search/fetch behavior:

```bash
export FIRECRAWL_API_KEY=your-key-here
```

With Firecrawl enabled:

- `WebSearch` can use Firecrawl's search API while DuckDuckGo remains the default free path for non-Claude models
- `WebFetch` uses Firecrawl's scrape endpoint instead of raw HTTP, handling JS-rendered pages correctly

Free tier at [firecrawl.dev](https://firecrawl.dev) includes 500 credits. The key is optional.

---

## Headless gRPC Server

The OpenClaude runtime can be run as a headless gRPC service, allowing you to integrate its agentic capabilities (tools, bash, file editing) into other applications, CI/CD pipelines, or custom user interfaces. The server uses bidirectional streaming to send real-time text chunks, tool calls, and request permissions for sensitive commands.

### 1. Start the gRPC Server

Start the core engine as a gRPC service on `localhost:50051`:

```bash
npm run dev:grpc
```

#### Configuration

| Variable | Default | Description |
|-----------|-------------|------------------------------------------------|
| `GRPC_PORT` | `50051` | Port the gRPC server listens on |
| `GRPC_HOST` | `localhost` | Bind address. Use `0.0.0.0` to expose on all interfaces (not recommended without authentication) |

### 2. Run the Test CLI Client

We provide a lightweight CLI client that communicates exclusively over gRPC. It acts just like the main interactive CLI, rendering colors, streaming tokens, and prompting you for tool permissions (y/n) via the gRPC `action_required` event.

In a separate terminal, run:

```bash
npm run dev:grpc:cli
```

*Note: The gRPC definitions are located in `src/proto/openclaude.proto`. You can use this file to generate clients in Python, Go, Rust, or any other language.*

---

## Source Build And Local Development

Use the same `bun install`, `bun run build`, and `node dist/cli.mjs` flow above.

Helpful commands:

- `bun run dev`
- `bun test`
- `bun run test:coverage`
- `bun run security:pr-scan -- --base origin/main`
- `bun run smoke`
- `bun run doctor:runtime`
- `bun run verify:privacy`
- focused `bun test ...` runs for the areas you touch

## Testing And Coverage

The runtime uses Bun's built-in test runner for unit tests.

Run the full unit suite:

```bash
bun test
```

Generate unit test coverage:

```bash
bun run test:coverage
```

Open the visual coverage report:

```bash
open coverage/index.html
```

If you already have `coverage/lcov.info` and only want to rebuild the UI:

```bash
bun run test:coverage:ui
```

Use focused test runs when you only touch one area:

- `bun run test:provider`
- `bun run test:provider-recommendation`
- `bun test path/to/file.test.ts`

Recommended contributor validation before opening a PR:

- `bun run build`
- `bun run smoke`
- `bun run test:coverage` for broader unit coverage when your change affects shared runtime or provider logic
- focused `bun test ...` runs for the files and flows you changed

Coverage output is written to `coverage/lcov.info`, and OpenClaude also generates a git-activity-style heatmap at `coverage/index.html`.
## Repository Structure

- `src/` - core CLI/runtime
- `scripts/` - build, verification, and maintenance scripts
- `docs/` - setup, contributor, and project documentation
- `python/` - standalone Python helpers and their tests
- `packages/openclaude-vscode/` - VS Code extension package verified by product-quality gates
- `.github/` - repo automation, templates, and CI configuration
- `bin/` - CLI launcher entrypoints

## VS Code Extension

The repo includes a VS Code extension package in [`packages/openclaude-vscode`](packages/openclaude-vscode) for OpenClaude launch integration, provider-aware control-center UI, and theme support.

## Security

If you believe you found a security issue, see [SECURITY.md](SECURITY.md).

## Community

- Use [GitHub Issues](https://github.com/svy04/metaforge/issues) for confirmed bugs and actionable feature work
- Use [SUPPORT.md](SUPPORT.md) for support routing, troubleshooting inputs, and privacy/safety boundaries
- Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) in project spaces

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup, validation, evidence, and claim-boundary expectations.

For larger changes, open an issue first so the scope is clear before implementation. Helpful validation commands include:

- `bun run build`
- `bun run test:coverage`
- `bun run smoke`
- `bun run verify:privacy`
- focused `bun test ...` runs for files and flows you changed


## Disclaimer

OpenClaude is an independent community fork/adaptation of runtime code derived from Anthropic's Claude Code CLI, substantially modified for multiple providers and Metaforge workflows. It is not affiliated with, endorsed by, or sponsored by Anthropic. This repository does not have Anthropic's authorization to distribute Anthropic proprietary source. "Claude" and "Claude Code" are trademarks of Anthropic PBC. See [LICENSE](LICENSE) for details.

## License

See [LICENSE](LICENSE).

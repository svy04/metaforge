# OpenClaude Advanced Setup

This guide is for users who want source builds, Bun workflows, provider profiles, diagnostics, or more control over runtime behavior.

## Install Options

### Option A: npm

```bash
npm install -g @gitlawb/openclaude
```

### Option B: From source with Bun

Use Bun `1.3.11` or newer for source builds on Windows. Older Bun versions can fail during `bun run build`.

```bash
git clone https://github.com/svy04/metaforge.git
cd metaforge

bun install
bun run build
npm link
```

### Option C: Run directly with Bun

```bash
git clone https://github.com/svy04/metaforge.git
cd metaforge

bun install
bun run dev
```

## Provider Examples

### OpenAI

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=<openai-api-key>
export OPENAI_MODEL=<openai-tool-model-id>
```

### Codex-compatible route

`codexplan` and `codexspark` are Codex backend profiles handled by the runtime.
Check current Codex provider docs before turning either profile into a public
model-specific claim.

If you use the in-app provider wizard, choose the Codex-compatible route and
complete the owner-authorized sign-in flow locally. Do not record account,
token, or auth-file details in public evidence reports.

If you already use the Codex CLI, OpenClaude can reuse an approved local
credential source. Keep private token overrides and auth-file path controls out
of screenshots, issues, READMEs, and generated reports.

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_MODEL=codexplan

openclaude
```

### DeepSeek

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=<deepseek-api-key>
export OPENAI_BASE_URL=https://api.deepseek.com/v1
export OPENAI_MODEL=deepseek-chat
```

### Google Gemini via OpenRouter

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=<openrouter-api-key>
export OPENAI_BASE_URL=https://openrouter.ai/api/v1
export OPENAI_MODEL=google/gemini-2.0-flash-001
```

OpenRouter model availability changes over time. If a model stops working, try another current OpenRouter model before assuming the integration is broken.

### Ollama

Using `ollama launch` (recommended if you have Ollama installed):

```bash
ollama launch openclaude --model <local-ollama-model>
```

This handles all environment setup automatically — no env vars needed. Works with any local or cloud model available in your Ollama instance.

Using environment variables manually:

```bash
ollama pull <local-ollama-model>

export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_MODEL=<local-ollama-model>
```

### Atomic Chat (local, Apple Silicon)

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_BASE_URL=http://127.0.0.1:1337/v1
export OPENAI_MODEL=your-model-name
```

No API key is needed for Atomic Chat local models.

Or use the profile launcher:

```bash
bun run dev:atomic-chat
```

Download Atomic Chat from [atomic.chat](https://atomic.chat/). The app must be running with a model loaded before launching.

### LM Studio

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_BASE_URL=http://localhost:1234/v1
export OPENAI_MODEL=your-model-name
```

### Together AI

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=<together-api-key>
export OPENAI_BASE_URL=https://api.together.xyz/v1
export OPENAI_MODEL=meta-llama/Llama-3.3-70B-Instruct-Turbo
```

### Groq

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=<groq-api-key>
export OPENAI_BASE_URL=https://api.groq.com/openai/v1
export OPENAI_MODEL=llama-3.3-70b-versatile
```

### Mistral

```bash
export CLAUDE_CODE_USE_MISTRAL=1
export MISTRAL_API_KEY=<mistral-api-key>
export MISTRAL_MODEL=<mistral-tool-model-id>
```

### Azure OpenAI

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=<azure-openai-api-key>
export OPENAI_BASE_URL=https://<azure-openai-resource>.openai.azure.com/openai/deployments/<azure-openai-deployment>/v1
export OPENAI_MODEL=<azure-openai-deployment>
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CLAUDE_CODE_USE_OPENAI` | Yes | Set to `1` to enable the OpenAI provider |
| `OPENAI_API_KEY` | Yes* | Your API key (`*` not needed for local models like Ollama or Atomic Chat) |
| `OPENAI_MODEL` | Yes | Model, alias, or deployment name such as `<openai-tool-model-id>`, `<local-ollama-model>`, or `deepseek-chat` |
| `OPENAI_BASE_URL` | No | API endpoint, defaulting to `https://api.openai.com/v1` |
| `CODEX_API_KEY` | Codex only | Private credential override; do not include values in public artifacts |
| `CODEX_AUTH_JSON_PATH` | Codex only | Private local credential-source path override |
| `CODEX_HOME` | Codex only | Private local Codex home override |
| `OPENCLAUDE_DISABLE_CO_AUTHORED_BY` | No | Suppress the default `Co-Authored-By` trailer in generated git commits |

You can also use `ANTHROPIC_MODEL` to override the model name. `OPENAI_MODEL` takes priority.

## Runtime Hardening

Use these commands to validate your setup and catch mistakes early:

```bash
# quick startup sanity check
bun run smoke

# validate provider env + reachability
bun run doctor:runtime

# print machine-readable runtime diagnostics
bun run doctor:runtime:json

# persist a diagnostics report to reports/doctor-runtime.json
bun run doctor:report

# full local hardening check (smoke + runtime doctor)
bun run hardening:check

# strict hardening (includes project-wide typecheck)
bun run hardening:strict
```

Notes:

- `doctor:runtime` fails fast if `CLAUDE_CODE_USE_OPENAI=1` with a placeholder key or a missing key for non-local providers.
- Local providers such as `http://localhost:11434/v1`, `http://10.0.0.1:11434/v1`, and `http://127.0.0.1:1337/v1` can run without `OPENAI_API_KEY`.
- Codex-compatible profiles validate an approved local credential source and
  probe the provider route without recording account/auth details in public
  evidence.

## Provider Launch Profiles

Use profile launchers to avoid repeated environment setup:

```bash
# one-time profile bootstrap (prefer viable local Ollama, otherwise OpenAI)
bun run profile:init

# preview provider/model suggestions for your goal
bun run profile:recommend -- --goal coding --benchmark

# auto-apply a local/openai provider/model suggestion for your goal
bun run profile:auto -- --goal latency

# codex bootstrap (defaults to codexplan and existing Codex CLI auth)
bun run profile:codex

# openai bootstrap with explicit key
bun run profile:init -- --provider openai --api-key <openai-api-key>

# ollama bootstrap with custom model
bun run profile:init -- --provider ollama --model <local-ollama-model>

# ollama bootstrap with goal-based model auto-selection
bun run profile:init -- --provider ollama --goal coding

# atomic-chat bootstrap (auto-detects running model)
bun run profile:init -- --provider atomic-chat

# codex bootstrap with a fast model alias
bun run profile:init -- --provider codex --model codexspark

# launch using persisted profile (.openclaude-profile.json)
bun run dev:profile

# codex profile (uses an approved local credential source)
bun run dev:codex

# OpenAI profile (requires OPENAI_API_KEY in your shell)
bun run dev:openai

# Ollama profile (defaults to localhost:11434 and the configured local model)
bun run dev:ollama

# Atomic Chat profile (Apple Silicon local LLMs at 127.0.0.1:1337)
bun run dev:atomic-chat
```

`profile:recommend` ranks installed Ollama models for `latency`, `balanced`, or `coding`, and `profile:auto` can persist the recommendation directly.

If no profile exists yet, `dev:profile` uses the same goal-aware defaults when picking the initial model.

Generated `.openclaude-profile.json` files persist non-sensitive provider settings, not API keys or blocked stale model locks. Keep cloud provider keys in your shell environment or an approved local credential source before launching a key-backed profile.

Use `--provider ollama` when you want a local-only path. Auto mode falls back to OpenAI when no viable local chat model is installed.

Use `--provider atomic-chat` when you want Atomic Chat as the local Apple Silicon provider.

Use `profile:codex` or `--provider codex` when you want the ChatGPT Codex backend.

`dev:openai`, `dev:ollama`, `dev:atomic-chat`, and `dev:codex` run `doctor:runtime` first and only launch the app if checks pass.

For `dev:ollama`, make sure Ollama is running locally before launch.

For `dev:atomic-chat`, make sure Atomic Chat is running with a model loaded before launch.

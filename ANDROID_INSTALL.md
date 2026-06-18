# Legacy OpenClaude Android Notes

These notes describe an old Termux + proot Ubuntu experiment for running the
OpenClaude runtime substrate on Android. They are not a Metaforge release or support claim, and they do not prove Android compatibility for the current checkout.

Model pricing, provider limits, and Termux package behavior change frequently.
Verify the current provider docs and local device behavior before using this as
anything more than a historical setup reference.

## Boundaries

- Metaforge is the public Meta/MFH/Orchestra OS surface in this repository.
- OpenClaude is the runtime substrate used by Metaforge.
- This document is not installation support, release readiness, hosted
  deployment evidence, benchmark evidence, or external validation.
- No provider, model, or benchmark comparison in this document should be treated
  as current without a fresh source check.

## Historical Setup Shape

The earlier Android experiment used this shape:

1. Install Termux from F-Droid.
2. Install `nodejs-lts`, `git`, and `proot-distro`.
3. Start an Ubuntu environment with `proot-distro`.
4. Install Bun inside Ubuntu.
5. Clone a source checkout.
6. Build with `bun run build`.
7. Run the CLI with `node dist/cli.mjs`.

```bash
pkg update && pkg upgrade
pkg install nodejs-lts git proot-distro
proot-distro install ubuntu
proot-distro login ubuntu
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc
bun --version
```

## Provider Configuration

Use placeholder values in public docs. Do not paste real keys into shell
history, screenshots, issues, or repository files.

```bash
export CLAUDE_CODE_USE_OPENAI=1
export OPENAI_API_KEY=<provider-api-key>
export OPENAI_BASE_URL=<openai-compatible-base-url>
export OPENAI_MODEL=<openai-tool-model-id>
node dist/cli.mjs
```

For local or low-cost experimentation, choose a provider and model only after
checking that provider's current pricing, context limits, request limits, and
tool-use behavior. Record the date and source URL in any evidence note.

## Restarting A Historical Session

```bash
proot-distro login ubuntu
cd <repo>
node dist/cli.mjs
```

## Operational Notes

- Keep `.openclaude-profile.json` local and out of git.
- Prefer `bun run doctor:runtime` before diagnosing provider behavior.
- Treat mobile execution as experimental until a maintained Android gate exists.
- Do not make benchmark, provider quality, or compatibility claims from this
  note alone.

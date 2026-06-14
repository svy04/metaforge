# Agent Stack Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install and normalize GStack, GSD, and Superpowers so OpenClaude agents can call them directly.

**Architecture:** Use user-level Claude-compatible discovery paths and a project-level routing rule. Avoid OpenClaude core changes until the workflow proves useful.

**Tech Stack:** OpenClaude TypeScript runtime, Claude-compatible `~/.claude` skill/command/agent roots, Git, npm, Bun, GSD installer, GStack setup, Superpowers skill repository.

---

### Task 1: Preserve Installation Context

**Files:**
- Create: `docs/superpowers/specs/2026-05-05-agent-stack-integration-design.md`
- Create: `docs/superpowers/plans/2026-05-05-agent-stack-integration.md`

- [ ] Create the design and plan files before changing global agent configuration.
- [ ] Record that this workspace is not a git repository, so design and plan files cannot be committed from this folder.

### Task 2: Normalize GSD

**Files:**
- Modify: `<config-dir>\commands\gsd\*.md`
- Create/modify: `<config-dir>\get-shit-done\`
- Create/modify: `<config-dir>\agents\gsd-*.md`

- [ ] Back up relevant `<config-dir>` files under `<config-dir>\backups\agent-stack-2026-05-05`.
- [ ] Run `npx.cmd -y get-shit-done-cc@latest --claude --global`.
- [ ] Verify `<config-dir>\get-shit-done\workflows\execute-phase.md` exists.
- [ ] Verify `<config-dir>\commands\gsd\execute-phase.md` exists.
- [ ] Verify `<config-dir>\agents\gsd-executor.md` exists.

### Task 3: Ensure GStack Is Runnable

**Files:**
- Modify/create: `<config-dir>\skills\gstack\`
- Modify/create: `<config-dir>\skills\gstack-*` or generated GStack skill entries

- [ ] Install Bun with `npm.cmd install -g bun` if `bun` is not available.
- [ ] Run GStack setup from Git Bash: `cd ~/.claude/skills/gstack && ./setup --host claude --quiet`.
- [ ] Verify `<config-dir>\skills\gstack\VERSION` exists.
- [ ] Verify `<config-dir>\skills\gstack\node_modules` exists.

### Task 4: Install Superpowers For OpenClaude

**Files:**
- Create/update: `<config-dir>\superpowers\`
- Create/update: `<config-dir>\skills\superpowers`

- [ ] Clone or update `https://github.com/obra/superpowers.git` into `<config-dir>\superpowers`.
- [ ] Create a Windows junction from `<config-dir>\skills\superpowers` to `<config-dir>\superpowers\skills`.
- [ ] Verify `<config-dir>\skills\superpowers\using-superpowers\SKILL.md` exists.
- [ ] Verify `<config-dir>\skills\superpowers\test-driven-development\SKILL.md` exists.

### Task 5: Add OpenClaude Routing Rules

**Files:**
- Create: `AGENTS.md`

- [ ] Add a project instruction section that routes ideation to GStack, phase execution to GSD, and implementation discipline to Superpowers.
- [ ] Include the user's source-first research rule.
- [ ] Keep the rule operational and short enough to fit normal session context.

### Task 6: Verify Discovery

**Files:**
- Read: `src\skills\loadSkillsDir.ts`
- Read: `src\tools\AgentTool\loadAgentsDir.ts`
- Read: `src\utils\claudemd.ts`

- [ ] Verify OpenClaude loads user skills from `<config-dir>\skills`.
- [ ] Verify OpenClaude loads legacy commands from `<config-dir>\commands`.
- [ ] Verify OpenClaude prefers `AGENTS.md` for project instructions.
- [ ] Run `node dist/cli.mjs --version` or `openclaude --version`.


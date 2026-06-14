# Agent Stack Integration Design

## Goal

Make OpenClaude sessions able to use GStack, GSD, and Superpowers directly from normal agent work.

## Role Split

- GStack owns product ideation, judgment, cross-role review, and high-level spec shaping.
- GSD owns large-scope planning, phase decomposition, context-rot control, and multi-step execution routing.
- Superpowers owns disciplined implementation, especially TDD, systematic debugging, code review, and verification before completion.

## Runtime Shape

Use OpenClaude's existing Claude-compatible discovery surfaces instead of changing OpenClaude core:

- `<config-dir>\skills\gstack` and generated GStack skill entries stay as the GStack source.
- `<config-dir>\commands\gsd` and `<config-dir>\get-shit-done` provide GSD commands/workflows.
- `<config-dir>\skills\superpowers` points to the Superpowers skills directory.
- Project `AGENTS.md` tells OpenClaude how to route between the three systems.

## Routing Policy

For vague or strategic product work, start with GStack. Use `/office-hours`, `/autoplan`, and review skills to turn the idea into a judged spec.

For large implementation work, feed the approved spec into GSD. Use `/gsd-new-project` or `/gsd-new-milestone`, then `/gsd-plan-phase`, `/gsd-execute-phase`, and `/gsd-verify-work`.

For concrete implementation tasks, use Superpowers. Prefer `superpowers:test-driven-development`, `superpowers:systematic-debugging`, `superpowers:requesting-code-review`, and `superpowers:verification-before-completion`.

When GSD executes implementation plans, pass or encode TDD expectations so Superpowers-style test-first implementation is the default execution discipline.

## Verification

After installation, verify:

- GStack still has a usable version and generated skills.
- GSD has `<config-dir>\get-shit-done`, command files, and agent files.
- Superpowers has discoverable nested `SKILL.md` files under `<config-dir>\skills\superpowers`.
- OpenClaude can enumerate the user skill roots through its existing loader.


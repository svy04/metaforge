# Goal Registry

Status: active local docs-governance surface

This directory contains both historical local goal artifacts and the current
Autonomous Goal OS goal registry.

The machine-checkable registry is intentionally narrow:

- Current structured goal objects use `CG-*.md` file names.
- Each structured goal contains a fenced `yaml` object following
  `docs/GOAL_SCHEMA.md`.
- `CG-001` covers Goal Kernel schema and representative MFH trace behavior.
- `CG-002` covers static-analysis ratchet evidence for Knip,
  dependency-cruiser, and jscpd without cleanup claims.
- Historical AVF and Influence Factory artifacts remain local evidence inputs;
  they are not rewritten into the new schema in this slice.

Validation:

```bash
bun run goals:validate
```

The validator checks required objective, scope, non-goal, success-criteria,
validation-command, checkpoint, pause-condition, rollback, research,
governed-code, MFH gate, and Meta record fields. A passing goal object is local
governance evidence only. It does not prove production readiness, release
readiness, public readiness, external validation, or autonomous reliability.

# Legacy Extension Surface

This folder is retained for legacy source and license inventory. The canonical
Metaforge VS Code extension surface lives at
[`packages/openclaude-vscode`](../../packages/openclaude-vscode).

Metaforge is the public Meta/MFH/Orchestra OS product surface. OpenClaude is the
runtime launch substrate used by the extension, not the main product claim.

## Boundary

- Do not treat this folder as the maintained extension package surface.
- Do not publish, package, or install from this folder as a Metaforge release.
- Keep claim-boundary, license, and source metadata aligned with the canonical
  package before reactivating any legacy path.

## Current Canonical Commands

From `packages/openclaude-vscode`:

```bash
npm run test
npm run lint
```

See [`packages/openclaude-vscode/README.md`](../../packages/openclaude-vscode/README.md)
for the maintained extension notes.

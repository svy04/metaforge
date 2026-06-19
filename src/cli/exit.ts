/**
 * CLI exit helpers for subcommand handlers.
 *
 * Consolidates the 4-5 line "print + lint-suppress + exit" block that was
 * copy-pasted ~60 times across `claude mcp *` / `claude plugin *` handlers.
 * The `: never` return type lets TypeScript narrow control flow at call sites
 * without a trailing `return`.
 */
/* eslint-disable custom-rules/no-process-exit -- centralized CLI exit point */

import { sanitizePlainTextLogValue } from '../utils/logSanitization.js'

// `return undefined as never` (not a post-exit throw) — tests spy on
// process.exit and let it return. Call sites write `return cliError(...)`
// where subsequent code would dereference narrowed-away values under mock.
// cliError/cliOk use process stdio writes directly. Tests spy on the same
// functions, and Bun's console methods do not always route through those spies.

/** Write an error message to stderr (if given) and exit with code 1. */
export function cliError(msg?: string): never {
  if (msg) process.stderr.write(`${sanitizePlainTextLogValue(msg)}\n`)
  process.exit(1)
  return undefined as never
}

/** Write a message to stdout (if given) and exit with code 0. */
export function cliOk(msg?: string): never {
  if (msg) process.stdout.write(msg + '\n')
  process.exit(0)
  return undefined as never
}

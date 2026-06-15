import { createHash } from 'node:crypto'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

export type Check = {
  label: string
  ok: boolean
  detail: string
}

export function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

export function readText(path: string, root = process.cwd()): string {
  return readFileSync(resolve(root, path), 'utf8')
}

export function fileSha256(path: string, root = process.cwd()): string {
  return sha256(readFileSync(resolve(root, path)))
}

export function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

export function includesAll(text: string, terms: string[]): string[] {
  const lower = text.toLowerCase()
  return terms.filter((term) => lower.includes(term.toLowerCase()))
}

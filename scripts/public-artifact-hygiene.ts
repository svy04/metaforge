import {
  existsSync,
  readdirSync,
  readFileSync,
  statSync,
  writeFileSync,
} from 'node:fs'
import { basename, extname, relative, resolve } from 'node:path'
import { argv, cwd, exit } from 'node:process'

const root = cwd()
const mode = argv.includes('--write') ? 'write' : 'check'

const targetRoots = [
  '.github',
  '.planning',
  'bin',
  'docs',
  'reports',
  'README.md',
  'README.ko.md',
  'AGENTS.md',
  'PLAYBOOK.md',
  '.env.example',
  'package.json',
  'scripts/public-artifact-hygiene.ts',
]

const textExtensions = new Set([
  '.json',
  '.jsonl',
  '.md',
  '.txt',
  '.ts',
  '.tsx',
  '.yml',
  '.yaml',
])

type Replacement = {
  pattern: RegExp
  replacement: string
}

const sep = String.raw`(?:\\+|/)`
const segment = String.raw`[^\\/"]+`
const userSegment = String.raw`[^\\/"]+`
const replacements: Replacement[] = [
  {
    pattern: new RegExp(
      String.raw`C:${sep}Users${sep}${userSegment}${sep}Desktop${sep}${segment}${sep}openclaude-0\.6\.0`,
      'g',
    ),
    replacement: '<repo>',
  },
  {
    pattern: new RegExp(
      String.raw`C:${sep}Users${sep}${userSegment}${sep}Desktop${sep}${segment}${sep}${segment}`,
      'g',
    ),
    replacement: '<private-workspace>',
  },
  {
    pattern: new RegExp(String.raw`C:${sep}Users${sep}${userSegment}${sep}\.claude`, 'g'),
    replacement: '<config-dir>',
  },
  {
    pattern: new RegExp(String.raw`C:${sep}Users${sep}${userSegment}${sep}\.codex`, 'g'),
    replacement: '<codex-config-dir>',
  },
  {
    pattern: new RegExp(
      String.raw`C:${sep}Users${sep}${userSegment}${sep}AppData${sep}Roaming${sep}npm${sep}node_modules${sep}bun${sep}bin${sep}bun\.exe`,
      'g',
    ),
    replacement: '<bun>',
  },
  {
    pattern: new RegExp(
      String.raw`C:${sep}Users${sep}${userSegment}${sep}AppData${sep}Local${sep}Programs${sep}Microsoft VS Code${sep}resources${sep}app${sep}updating`,
      'g',
    ),
    replacement: '<vscode-updating-sentinel>',
  },
  {
    pattern: new RegExp(String.raw`C:${sep}Users${sep}${userSegment}`, 'g'),
    replacement: '<user-home>',
  },
  {
    pattern: /\/Users\/[^/\s"']+/g,
    replacement: '<user-home>',
  },
]

const forbiddenPatterns = [
  /C:(?:\\{1,2}|\/)Users(?:\\{1,2}|\/)[^\\/\s"']+/,
  /\/Users\/[^/\s"']+/,
  /Users\/[^/\s"']+/,
  new RegExp(String.raw`\uB0B4\u0020\uC21C\uC218\u0020\uC7AC\uBBF8`),
  new RegExp('Digital ' + 'Factory'),
  new RegExp('Token: ' + 'gho_'),
  /(?:api[-_\s]?key|token)[^\r\n]{0,80}\bsk-[A-Za-z0-9_-]{8,}\b/i,
  new RegExp('session' + '_id'),
]

function walk(path: string): string[] {
  const stat = statSync(path)
  if (stat.isFile()) return [path]
  if (!stat.isDirectory()) return []
  return readdirSync(path, { withFileTypes: true }).flatMap((entry) => {
    if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === 'dist') {
      return []
    }
    return walk(resolve(path, entry.name))
  })
}

function isTextTarget(path: string): boolean {
  if (!existsSync(path)) return false
  if (basename(path) === '.env.example') return true
  const ext = extname(path)
  return textExtensions.has(ext) || ext === ''
}

function sanitize(text: string): string {
  return replacements.reduce(
    (current, item) => current.replace(item.pattern, item.replacement),
    text,
  )
}

const files = targetRoots
  .map((target) => resolve(root, target))
  .filter((target) => existsSync(target))
  .flatMap(walk)
  .filter(isTextTarget)

const findings: string[] = []
let changed = 0

for (const file of files) {
  let text: string
  try {
    text = readFileSync(file, 'utf8')
  } catch {
    continue
  }

  const next = sanitize(text)
  if (mode === 'write' && next !== text) {
    writeFileSync(file, next)
    changed += 1
  }

  const inspect = mode === 'write' ? next : text
  for (const pattern of forbiddenPatterns) {
    if (pattern.test(inspect)) {
      findings.push(`${relative(root, file).replace(/\\/g, '/')}: ${pattern}`)
      break
    }
  }
}

if (findings.length > 0) {
  console.error('RESULT: FAIL')
  console.error(`public_hygiene_findings=${findings.length}`)
  for (const finding of findings.slice(0, 80)) {
    console.error(finding)
  }
  if (findings.length > 80) {
    console.error(`... ${findings.length - 80} more`)
  }
  exit(1)
}

console.log('RESULT: PASS')
console.log(`mode=${mode}`)
console.log(`files_scanned=${files.length}`)
console.log(`files_changed=${changed}`)

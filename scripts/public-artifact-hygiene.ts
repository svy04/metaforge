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
  'avf',
  'bin',
  'docs',
  'reports',
  'README.md',
  'README.ko.md',
  'ANDROID_INSTALL.md',
  'AGENTS.md',
  'PLAYBOOK.md',
  'CHANGELOG.md',
  'CONTRIBUTING.md',
  'SECURITY.md',
  'SUPPORT.md',
  'LICENSE',
  'packages/openclaude-vscode/package.json',
  'packages/openclaude-vscode/README.md',
  'vscode-extension/openclaude-vscode/package.json',
  'vscode-extension/openclaude-vscode/README.md',
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

type PublicLeakPattern = {
  label: string
  pattern: RegExp
  appliesTo?: (relativePath: string) => boolean
}

const ignoredSensitiveRootFileNames = new Set([
  '.mcp.json',
  '.npmrc',
  '.yarnrc.yml',
  '.bunfig.toml',
  '.windsurfrules',
  '.clinerules',
])

const ignoredSensitiveRootDirectoryNames = new Set([
  '.claude',
  '.cursor',
  '.windsurf',
])

const ignoredSensitiveRootTargets = readdirSync(root, { withFileTypes: true })
  .filter((entry) => (
    (entry.isFile() && (
      entry.name.startsWith('.openclaude-profile.json') ||
      ignoredSensitiveRootFileNames.has(entry.name)
    )) ||
    (entry.isDirectory() && ignoredSensitiveRootDirectoryNames.has(entry.name))
  ))
  .map((entry) => entry.name)

const sep = String.raw`(?:\\+|/)`
const segment = String.raw`[^\\/"]+`
const userSegment = String.raw`[^\\/"]+`
const privateWorkspacePlaceholder = '<private' + '-workspace>'
const privateCodexMemoryPlaceholder = '<private' + '-codex-memory-dir>'
const privateAgentSkillPlaceholder = '<private' + '-agent-skill-dir>'
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
    replacement: privateWorkspacePlaceholder,
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
    pattern: /<user-home>(?:\\+|\/)AppData(?:\\+|\/)Local(?:\\+|\/)Programs(?:\\+|\/)Microsoft VS Code(?:\\+|\/)[^\r\n`"']*updating/gi,
    replacement: '<vscode-updating-sentinel>',
  },
  {
    pattern: /\bfile:\/\/\/[^\s`"']*index\.html#selftest\b/gi,
    replacement: '<local-selftest-url>',
  },
  {
    pattern: /(^|[\s`"'])[^`\s"']*index\.html#selftest\b/gi,
    replacement: '$1<local-selftest-target>',
  },
  {
    pattern: /\b[A-Z]:(?:\\+|\/)Program Files(?:\\+|\/)[^\r\n`"']+\.(?:exe|cmd|bat)\b/gi,
    replacement: '<local-executable>',
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

const customPublicLeakPatterns: PublicLeakPattern[] = [
  { label: 'windows-user-path', pattern: /C:(?:\\{1,2}|\/)Users(?:\\{1,2}|\/)[^\\/\s"']+/ },
  { label: 'posix-user-path', pattern: /\/Users\/[^/\s"']+/ },
  { label: 'relative-user-path', pattern: /Users\/[^/\s"']+/ },
  { label: 'user-workspace-path', pattern: /(?:%USERPROFILE%|\$HOME|\$\{HOME\}|~)(?:\\+|\/)(?:Desktop|Documents)(?:\\+|\/)[^\r\n`"']+/i },
  { label: 'private-workspace-korean-name', pattern: new RegExp(String.raw`\uB0B4\u0020\uC21C\uC218\u0020\uC7AC\uBBF8`) },
  { label: 'private-workspace-name', pattern: new RegExp('Digital ' + 'Factory') },
  { label: 'codex-memory-path', pattern: new RegExp(String.raw`\.` + 'codex' + String.raw`[\\/]+` + 'memories', 'i') },
  { label: 'agents-skill-path', pattern: new RegExp(String.raw`\.` + 'agents' + String.raw`[\\/]+` + 'skills', 'i') },
  { label: 'private-workspace-placeholder', pattern: new RegExp(privateWorkspacePlaceholder, 'i') },
  { label: 'private-codex-memory-placeholder', pattern: new RegExp(privateCodexMemoryPlaceholder, 'i') },
  { label: 'private-agent-skill-placeholder', pattern: new RegExp(privateAgentSkillPlaceholder, 'i') },
  { label: 'private-meta-authority-path', pattern: /(?:^|[\s`"'])meta[\\/]+CLAUDE\.md\b/i },
  { label: 'private-mfh-spec-path', pattern: /(?:^|[\s`"'])mfh[\\/]+\.mfh[\\/]+spec\.md\b/i },
  { label: 'private-memory-dump-title', pattern: new RegExp('OpenClaude Orchestrator ' + 'Memory') },
  { label: 'pasted-agents-local-context', pattern: new RegExp('AGENTS\\.md instructions for C' + ':') },
  { label: 'codex-internal-context', pattern: new RegExp('<codex_' + 'internal_context\\b', 'i') },
  { label: 'environment-context', pattern: new RegExp('<environment_' + 'context\\b', 'i') },
  { label: 'workspace-roots-context', pattern: new RegExp('<workspace_' + 'roots\\b', 'i') },
  { label: 'permissions-instructions-context', pattern: new RegExp('<permissions ' + 'instructions\\b', 'i') },
  { label: 'raw-public-comment-ui-dump', pattern: new RegExp('갤로그로 ' + '이동합니다|댓글' + '돌이') },
  { label: 'credential-source-env-var', pattern: /\b[A-Z0-9_]*CREDENTIAL_SOURCE\s*=\s*oauth\b/i },
  { label: 'oauth-profile-operational-detail', pattern: /\b(?:Codex|Claude)\s+OAuth\s+profile\b/i },
  { label: 'oauth-attribution-operational-detail', pattern: new RegExp(String.raw`\bside-query ` + 'OAuth attribution path' + String.raw`\b`, 'i') },
  { label: 'restored-credentials-wording', pattern: new RegExp(String.raw`\bunder the ` + 'restored credentials' + String.raw`\b`, 'i') },
  {
    label: 'provider-backend-auth-url',
    pattern: /(?:^|[\s`"'=])(?:https?:\/\/)?chatgpt\.com\/backend-api\/codex(?:$|[/?#\s`"'])/i,
  },
  { label: 'current-model-placeholder', pattern: /<current-[^>\r\n]*model>/i },
  { label: 'latest-model-alias-claim', pattern: new RegExp(String.raw`\balias for the ` + 'latest model' + String.raw`\b`, 'i') },
  { label: 'github-oauth-token-label', pattern: new RegExp('Token: ' + 'gho_') },
  { label: 'github-token', pattern: /\bgh[pousr]_[A-Za-z0-9_]{30,}\b/ },
  { label: 'github-fine-grained-token', pattern: /\bgithub_pat_[A-Za-z0-9_]{30,}\b/ },
  { label: 'aws-access-key', pattern: /\bAKIA[0-9A-Z]{16}\b/ },
  { label: 'aws-session-access-key', pattern: /\bASIA[0-9A-Z]{16}\b/ },
  { label: 'slack-token', pattern: /\bxox[baprs]-[A-Za-z0-9-]{10,}\b/ },
  { label: 'private-key-block', pattern: /-----BEGIN (?:RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----/ },
  { label: 'scanner-unfriendly-openai-key-placeholder', pattern: /\bsk-\.\.\./i },
  { label: 'scanner-unfriendly-api-key-placeholder', pattern: /\byour[_-]?[a-z0-9_-]*key[a-z0-9_-]*\b/i },
  { label: 'actual-looking-sk-token', pattern: /(?:api[-_\s]?key|token)[^\r\n]{0,80}\bsk-[A-Za-z0-9_-]{8,}\b/i },
  {
    label: 'stale-model-lock',
    pattern: /\b(?:gpt-4o|gpt-5\.1|gpt-5\.5|claude-sonnet-4-5|sonnet 4\.5|claude-opus-4-7|opus-4-7|Opus 4\.7)\b/i,
    appliesTo: (path) => (
      path === '.env.example' ||
      path.startsWith('.planning/') ||
      path.startsWith('.openclaude-profile.json')
    ),
  },
  { label: 'local-file-url', pattern: /\bfile:\/\/\/[^\s`"']*index\.html#selftest\b/i },
  { label: 'local-selftest-target', pattern: /(?:^|[\s`"'])[^`\s"']*index\.html#selftest\b/i },
  { label: 'windows-local-executable-path', pattern: /\b[A-Z]:(?:\\+|\/)Program Files(?:\\+|\/)[^\r\n`"']+\.(?:exe|cmd|bat)\b/i },
  { label: 'vscode-user-home-sentinel-path', pattern: /<user-home>(?:\\+|\/)AppData(?:\\+|\/)Local(?:\\+|\/)Programs(?:\\+|\/)Microsoft VS Code(?:\\+|\/)[^\r\n`"']*updating\b/i },
  { label: 'session-id-marker', pattern: new RegExp('session' + '_id') },
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

const files = [...targetRoots, ...ignoredSensitiveRootTargets]
  .map((target) => resolve(root, target))
  .filter((target) => existsSync(target))
  .flatMap(walk)
  .filter(isTextTarget)

const findings: string[] = []
let changed = 0

for (const file of files) {
  const relativePath = relative(root, file).replace(/\\/g, '/')
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
  for (const { label, pattern, appliesTo } of customPublicLeakPatterns) {
    if (appliesTo && !appliesTo(relativePath)) {
      continue
    }
    if (pattern.test(inspect)) {
      findings.push(`${relativePath}: ${label}`)
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

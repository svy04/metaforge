import { spawnSync } from 'node:child_process'

export type PackageCommandSpawnOptions = {
  cwd: string
  encoding: 'utf8'
  env: NodeJS.ProcessEnv
  maxBuffer: number
  shell: false
}

export type PackageCommandSpawnResult = {
  status: number | null
  stdout?: string | Buffer | null
  stderr?: string | Buffer | null
}

export type PackageCommandSpawn = (
  executable: string,
  args: string[],
  options: PackageCommandSpawnOptions,
) => PackageCommandSpawnResult

export type PackageCommandRun = {
  name: string
  command: string[]
  exitCode: number | null
  passed: boolean
  requiredSubstrings: string[]
  missingSubstrings: string[]
  stdoutPreview: string[]
  stderrPreview: string[]
  stdoutText: string
}

export type RunNoProviderPackageCommandOptions = {
  root: string
  name: string
  command: string[]
  requiredSubstrings: string[]
  noProviderEnvName: string
  normalize: (text: string | Buffer | null | undefined) => string
  preview: (text: string) => string[]
  spawn?: PackageCommandSpawn
}

const disabledProviderEnv: NodeJS.ProcessEnv = {
  CLAUDE_CODE_USE_OPENAI: '0',
  CLAUDE_CODE_USE_GEMINI: '0',
  CLAUDE_CODE_USE_GITHUB: '0',
  CLAUDE_CODE_USE_MISTRAL: '0',
  OPENAI_API_KEY: '',
  CODEX_API_KEY: '',
  GEMINI_API_KEY: '',
  GOOGLE_API_KEY: '',
  MISTRAL_API_KEY: '',
  GITHUB_TOKEN: '',
  GH_TOKEN: '',
  ANTHROPIC_API_KEY: '',
}

const defaultSpawn: PackageCommandSpawn = (executable, args, options) => spawnSync(executable, args, options)

export function runNoProviderPackageCommand(options: RunNoProviderPackageCommandOptions): PackageCommandRun {
  const [executable, ...args] = options.command
  const spawn = options.spawn ?? defaultSpawn
  const result = spawn(process.execPath, ['x', executable, ...args], {
    cwd: options.root,
    encoding: 'utf8',
    env: {
      ...process.env,
      ...disabledProviderEnv,
      [options.noProviderEnvName]: '1',
    },
    maxBuffer: 128 * 1024 * 1024,
    shell: false,
  })
  const stdout = options.normalize(result.stdout)
  const stderr = options.normalize(result.stderr)
  const combined = `${stdout}\n${stderr}`
  const missingSubstrings = options.requiredSubstrings.filter((substring) => !combined.includes(substring))

  return {
    name: options.name,
    command: options.command,
    exitCode: result.status,
    passed: result.status === 0 && missingSubstrings.length === 0,
    requiredSubstrings: options.requiredSubstrings,
    missingSubstrings,
    stdoutPreview: options.preview(stdout),
    stderrPreview: options.preview(stderr),
    stdoutText: stdout,
  }
}

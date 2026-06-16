import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { tmpdir } from 'node:os'

const scriptPath = join(__dirname, 'product-vscode-startup-diagnostics.ts')
const tempDirs: string[] = []

function makeTempRepo(): string {
  const dir = mkdtempSync(join(tmpdir(), 'openclaude-vscode-diagnostics-'))
  tempDirs.push(dir)
  return dir
}

function writeJson(root: string, path: string, value: unknown): void {
  const fullPath = join(root, path)
  mkdirSync(dirname(fullPath), { recursive: true })
  writeFileSync(fullPath, `${JSON.stringify(value, null, 2)}\n`)
}

afterEach(() => {
  for (const dir of tempDirs.splice(0)) {
    rmSync(dir, { recursive: true, force: true })
  }
})

describe('VS Code startup diagnostics public output', () => {
  test('emits generic VS Code update sentinels instead of user-home AppData paths', () => {
    const repo = makeTempRepo()
    const fixtureCliVersion = ['1.99.0', '6928394f91b684055b873eecb8bc281365131f1c', 'x64'].join('\n')
    const smokeReport = {
      mode: 'local_no_provider_real_vscode_extension_host_smoke',
      vscodeCliVersion: fixtureCliVersion,
      extensionDevelopmentPath: join(repo, 'packages/openclaude-vscode'),
      extensionTestsPath: join(repo, '.tmp-vscode-host', 'runner.js'),
      workspacePath: repo,
      codeExitCode: 1,
      codeTimedOut: false,
      vscodeStartupBlocked: false,
      environmentBlockers: [],
      realExtensionHostLaunched: false,
      providerCallsPerformed: [],
      liveModelCallsPerformed: [],
      externalCallsPerformed: [],
    }
    writeJson(repo, 'docs/product-quality/ide-extension-host-smoke-report.json', smokeReport)
    writeJson(repo, 'docs/product-quality/ide-extension-workbench-smoke-report.json', {
      ...smokeReport,
      mode: 'local_no_provider_real_vscode_workbench_tree_view_smoke',
      extensionTestsPath: join(repo, '.tmp-vscode-workbench', 'runner.js'),
    })
    writeJson(repo, 'docs/product-quality/vscode-update-boundary-report.json', {
      mode: 'local_no_provider_vscode_update_boundary',
      boundaryStatus: 'blocked_vscode_update_guard',
      codeVersion: fixtureCliVersion,
      updatingSentinelPath: '<vscode-updating-sentinel>',
      updatingSentinelExists: false,
      codeSetupProcesses: [],
      sourceHostEnvironmentBlockers: [],
      sourceWorkbenchEnvironmentBlockers: [],
      processTerminationAttempted: false,
      dependencyInstallAttempted: false,
      protectedActionsExecuted: [],
      providerCallsPerformed: [],
      liveModelCallsPerformed: [],
      externalCallsPerformed: [],
    })

    const result = spawnSync(process.execPath, ['run', scriptPath], {
      cwd: repo,
      encoding: 'utf8',
      shell: false,
      env: {
        ...process.env,
        LOCALAPPDATA: 'C:\\Users\\fixture-owner\\AppData\\Local',
      },
    })

    const output = `${result.stdout}\n${result.stderr}`
    expect(result.error).toBeUndefined()
    expect(result.status).toBe(0)
    expect(output).toContain('RESULT: PASS')

    const reportJson = readFileSync(join(repo, 'docs/product-quality/vscode-startup-diagnostics-report.json'), 'utf8')
    const reportMd = readFileSync(join(repo, 'docs/product-quality/vscode-startup-diagnostics-report.md'), 'utf8')
    expect(`${reportJson}\n${reportMd}`).toContain('<vscode-updating-sentinel>')
    expect(`${reportJson}\n${reportMd}`).not.toContain('C:\\Users\\fixture-owner')
    expect(`${reportJson}\n${reportMd}`).not.toContain('<user-home>\\AppData\\Local\\Programs\\Microsoft VS Code')
  })
})

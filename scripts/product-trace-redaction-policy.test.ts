import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const scriptPath = join(__dirname, 'product-trace-redaction-policy.ts')
const tempDirs: string[] = []

function sha256(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function makeFixture(rawTraceText: string): string {
  const root = mkdtempSync(join(tmpdir(), 'openclaude-trace-redaction-'))
  tempDirs.push(root)
  mkdirSync(join(root, 'docs/product-quality'), { recursive: true })
  mkdirSync(join(root, 'reports'), { recursive: true })

  const tracePath = 'reports/orchestra-fixture.jsonl'
  writeFileSync(join(root, tracePath), rawTraceText)
  writeFileSync(
    join(root, 'docs/product-quality/real-session-trace-evals-report.json'),
    `${JSON.stringify({
      mode: 'local_no_provider_real_session_jsonl_trace_grading',
      traceFileCount: 1,
      providerCallsPerformed: [],
      liveModelCallsPerformed: [],
      externalCallsPerformed: [],
      traces: [
        {
          path: tracePath,
          sha256: sha256(rawTraceText),
        },
      ],
      coverageSummary: {
        roles: ['planner', 'executor'],
        models: ['local-fixture-planner', 'local-fixture-executor'],
      },
    }, null, 2)}\n`,
  )

  return root
}

function runPolicy(cwd: string) {
  return spawnSync('bun', ['run', scriptPath], {
    cwd,
    encoding: 'utf8',
    shell: false,
  })
}

function readPolicyReport(cwd: string) {
  return JSON.parse(readFileSync(
    join(cwd, 'docs/product-quality/trace-capture-redaction-policy-report.json'),
    'utf8',
  )) as {
    scannedRawTraceFiles: Array<{ providerRequestIdPatternFound: boolean }>
  }
}

afterEach(() => {
  for (const dir of tempDirs.splice(0)) {
    rmSync(dir, { recursive: true, force: true })
  }
})

describe('trace redaction policy', () => {
  test('fails when a raw trace contains a provider request identifier', () => {
    const root = makeFixture([
      '{"timestamp":"2026-06-16T00:00:00.000Z","role":"planner","model":"fixture","querySource":"sdk","turnCount":1,"status":"started"}',
      '{"timestamp":"2026-06-16T00:00:01.000Z","role":"planner","model":"fixture","querySource":"sdk","turnCount":1,"status":"failed","errorMessage":"429 {\\"type\\":\\"error\\",\\"request_id\\":\\"req_011CaksMb9PZfxciWJgN9K7H\\"}"}',
      '',
    ].join('\n'))

    const result = runPolicy(root)
    const output = `${result.stdout}\n${result.stderr}`

    expect(result.status).not.toBe(0)
    expect(output).toContain('raw trace provider request id patterns absent')
    expect(output).toContain('RESULT: FAIL')
    expect(readPolicyReport(root).scannedRawTraceFiles[0]?.providerRequestIdPatternFound).toBe(true)
  })

  test('does not treat local run/action names as provider request identifiers', () => {
    const root = makeFixture([
      '{"timestamp":"2026-06-16T00:00:00.000Z","role":"tool","model":"local-fixture-test-runner","querySource":"operator_authorized_local_no_provider_code_editing_trace","turnCount":1,"status":"started","eventName":"operator_authorized_local_code_editing_trace.run_fixture_unit_check.started","actionName":"run_fixture_unit_check"}',
      '{"timestamp":"2026-06-16T00:00:01.000Z","role":"tool","model":"local-fixture-test-runner","querySource":"operator_authorized_local_no_provider_code_editing_trace","turnCount":1,"status":"succeeded","eventName":"operator_authorized_local_code_editing_trace.run_fixture_unit_check.succeeded","actionName":"run_fixture_unit_check"}',
      '',
    ].join('\n'))

    const result = runPolicy(root)

    expect(result.status).toBe(0)
    expect(readPolicyReport(root).scannedRawTraceFiles[0]?.providerRequestIdPatternFound).toBe(false)
  })
})

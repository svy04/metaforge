import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type ProviderPresetDefault = {
  preset: string
  provider: string
  name: string
  baseUrl: string
  model: string
  requiresApiKey: boolean
}

type ProviderCompatibilityReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  directProviderFlags: string[]
  providerPresetDefaults: ProviderPresetDefault[]
  productDescriptionProviders: string[]
  profileOnlyPresets: string[]
  directOnlyFlags: string[]
  launchScripts: string[]
  compatibilityChecks: Check[]
}

type RuntimeDoctorRegressionReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  doctorChecks: Check[]
  runtimeDoctorSurfaces: string[]
}

type AxisArchitectureReviewReport = {
  mode: string
  sourceGapReviewReportPath: string
  baselineSnapshotDate: string
  axisReviewRecords: Array<{
    axis: string
    currentLocalEvidence: string[]
    safeInternalImplementationBacklog: string[]
    protectedBoundary: string
    claimAllowed: boolean
  }>
  reviewChecks: Check[]
}

type CapabilityRow = {
  schemaVersion: 'openclaude_provider_capability_matrix_v1'
  surfaceId: string
  sourceSurface: 'profile_preset' | 'direct_only_flag'
  provider: string
  preset: string | null
  name: string
  baseUrl: string
  baseUrlCategory: 'remote_https' | 'local_loopback' | 'placeholder_remote' | 'not_configured'
  model: string
  requiresApiKey: boolean
  noApiKeyLocalCandidate: boolean
  openAiCompatibleTransport: boolean
  directFlagAvailable: boolean
  profilePresetAvailable: boolean
  launchScriptAvailable: boolean
  localEvidencePaths: string[]
  runtimeDoctorEvidence: string[]
  capabilityStatus: 'remote_key_required_unvalidated' | 'local_no_key_configured_unvalidated' | 'placeholder_configuration_requires_owner_setup' | 'direct_flag_without_profile_preset'
  liveValidationStatus: 'not_executed_requires_explicit_authorization'
  providerBackedExecutionClaimAllowed: false
  externalValidationClaimAllowed: false
  claimAllowed: false
  recordDigest: string
}

type FailureModeRow = {
  schemaVersion: 'openclaude_provider_failure_mode_matrix_v1'
  failureModeId: string
  blockedStatus: 'blocked_until_explicit_authorization_or_local_runtime_available'
  affectedSurfaceIds: string[]
  currentEvidence: string[]
  requiredAuthorization: string
  forbiddenShortcut: string
  validationMethod: string
  claimAllowed: false
  recordDigest: string
}

type ProviderCapabilityMatrixReport = {
  generatedAt: string
  mode: 'local_no_provider_provider_capability_matrix'
  sourceProviderCompatibilityReportPath: string
  sourceProviderCompatibilityReportSha256: string
  sourceRuntimeDoctorReportPath: string
  sourceRuntimeDoctorReportSha256: string
  sourceOssAxisArchitectureReportPath: string
  sourceOssAxisArchitectureReportSha256: string
  directProviderFlagCount: number
  providerPresetDefaultCount: number
  productDescriptionProviders: string[]
  capabilityRowCount: number
  localNoKeyProviderCount: number
  openAiCompatibleSurfaceCount: number
  failureModeCount: number
  failureModeIds: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  providerBackedExecutionClaimAllowed: false
  providerCompatibilityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  capabilityRows: CapabilityRow[]
  failureModeRows: FailureModeRow[]
  capabilityChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceProviderCompatibilityReportPath = 'docs/product-quality/provider-compatibility-fixtures.json'
const sourceRuntimeDoctorReportPath = 'docs/product-quality/runtime-doctor-regression-fixtures.json'
const sourceOssAxisArchitectureReportPath = 'docs/product-quality/oss-axis-architecture-review-report.json'
const reportJsonPath = 'docs/product-quality/provider-capability-matrix-report.json'
const reportMdPath = 'docs/product-quality/provider-capability-matrix-report.md'
const provenanceJsonlPath = 'reports/openclaude-provider-capability-matrix.jsonl'

const requiredFailureModeIds = [
  'provider_key_missing',
  'local_runtime_unavailable',
  'provider_reachability_skipped',
  'profile_direct_surface_drift',
  'live_model_authorization_missing',
]

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function readJson<T>(path: string): { text: string; parsed: T; digest: string } {
  const text = readText(path)
  return { text, parsed: JSON.parse(text) as T, digest: sha256(text) }
}

function baseUrlCategory(baseUrl: string): CapabilityRow['baseUrlCategory'] {
  if (!baseUrl || baseUrl === 'not_configured_in_profile_preset') return 'not_configured'
  if (/YOUR-|YOUR_/.test(baseUrl)) return 'placeholder_remote'
  if (/^https:\/\//.test(baseUrl)) return 'remote_https'
  if (/^http:\/\/(127\.0\.0\.1|localhost|\[::1\])/.test(baseUrl)) return 'local_loopback'
  return 'not_configured'
}

function normalizeDirectSurface(value: string): string {
  if (value === 'azure-openai') return 'openai'
  if (value === 'dashscope-cn' || value === 'dashscope-intl') return 'openai'
  if (value === 'lmstudio' || value === 'atomic-chat') return 'openai'
  if (value === 'moonshotai' || value === 'deepseek' || value === 'together' || value === 'groq') return 'openai'
  if (value === 'openrouter' || value === 'nvidia-nim' || value === 'minimax') return 'openai'
  if (value === 'custom') return 'openai'
  return value
}

function capabilityStatus(row: {
  sourceSurface: CapabilityRow['sourceSurface']
  requiresApiKey: boolean
  baseUrlCategory: CapabilityRow['baseUrlCategory']
}): CapabilityRow['capabilityStatus'] {
  if (row.sourceSurface === 'direct_only_flag') return 'direct_flag_without_profile_preset'
  if (row.baseUrlCategory === 'placeholder_remote') return 'placeholder_configuration_requires_owner_setup'
  if (row.requiresApiKey) return 'remote_key_required_unvalidated'
  return 'local_no_key_configured_unvalidated'
}

function withDigest<T extends Omit<CapabilityRow, 'recordDigest'> | Omit<FailureModeRow, 'recordDigest'>>(record: T): T & { recordDigest: string } {
  return {
    ...record,
    recordDigest: sha256(JSON.stringify(record)),
  }
}

function buildCapabilityRows(
  providerCompatibility: ProviderCompatibilityReport,
  runtimeDoctor: RuntimeDoctorRegressionReport,
): CapabilityRow[] {
  const runtimeEvidence = runtimeDoctor.runtimeDoctorSurfaces.filter((surface) => /provider|Ollama/i.test(surface))
  const presetRows = providerCompatibility.providerPresetDefaults.map((preset) => {
    const category = baseUrlCategory(preset.baseUrl)
    const directFlagAvailable = providerCompatibility.directProviderFlags.includes(preset.preset)
      || providerCompatibility.directProviderFlags.includes(preset.provider)
      || providerCompatibility.directProviderFlags.includes(normalizeDirectSurface(preset.preset))
    return withDigest({
      schemaVersion: 'openclaude_provider_capability_matrix_v1' as const,
      surfaceId: `preset:${preset.preset}`,
      sourceSurface: 'profile_preset' as const,
      provider: preset.provider,
      preset: preset.preset,
      name: preset.name,
      baseUrl: preset.baseUrl,
      baseUrlCategory: category,
      model: preset.model,
      requiresApiKey: preset.requiresApiKey,
      noApiKeyLocalCandidate: category === 'local_loopback' && !preset.requiresApiKey,
      openAiCompatibleTransport: preset.provider === 'openai',
      directFlagAvailable,
      profilePresetAvailable: true,
      launchScriptAvailable: providerCompatibility.launchScripts.includes(`dev:${preset.preset}`) || providerCompatibility.launchScripts.includes(`profile:${preset.preset}`),
      localEvidencePaths: [
        sourceProviderCompatibilityReportPath,
        sourceRuntimeDoctorReportPath,
      ],
      runtimeDoctorEvidence: runtimeEvidence,
      capabilityStatus: capabilityStatus({
        sourceSurface: 'profile_preset',
        requiresApiKey: preset.requiresApiKey,
        baseUrlCategory: category,
      }),
      liveValidationStatus: 'not_executed_requires_explicit_authorization' as const,
      providerBackedExecutionClaimAllowed: false as const,
      externalValidationClaimAllowed: false as const,
      claimAllowed: false as const,
    })
  })

  const directOnlyRows = providerCompatibility.directOnlyFlags.map((flag) => {
    const category = baseUrlCategory('not_configured_in_profile_preset')
    return withDigest({
      schemaVersion: 'openclaude_provider_capability_matrix_v1' as const,
      surfaceId: `direct:${flag}`,
      sourceSurface: 'direct_only_flag' as const,
      provider: flag,
      preset: null,
      name: flag,
      baseUrl: 'not_configured_in_profile_preset',
      baseUrlCategory: category,
      model: 'not_configured_in_profile_preset',
      requiresApiKey: true,
      noApiKeyLocalCandidate: false,
      openAiCompatibleTransport: false,
      directFlagAvailable: true,
      profilePresetAvailable: false,
      launchScriptAvailable: false,
      localEvidencePaths: [
        sourceProviderCompatibilityReportPath,
        sourceRuntimeDoctorReportPath,
      ],
      runtimeDoctorEvidence: runtimeEvidence,
      capabilityStatus: capabilityStatus({
        sourceSurface: 'direct_only_flag',
        requiresApiKey: true,
        baseUrlCategory: category,
      }),
      liveValidationStatus: 'not_executed_requires_explicit_authorization' as const,
      providerBackedExecutionClaimAllowed: false as const,
      externalValidationClaimAllowed: false as const,
      claimAllowed: false as const,
    })
  })

  return [...presetRows, ...directOnlyRows]
}

function buildFailureModeRows(providerCompatibility: ProviderCompatibilityReport, capabilityRows: CapabilityRow[]): FailureModeRow[] {
  const localRows = capabilityRows.filter((row) => row.noApiKeyLocalCandidate)
  const keyRows = capabilityRows.filter((row) => row.requiresApiKey)
  const driftRows = capabilityRows.filter((row) => row.sourceSurface === 'direct_only_flag' || !row.directFlagAvailable)

  return [
    withDigest({
      schemaVersion: 'openclaude_provider_failure_mode_matrix_v1' as const,
      failureModeId: 'provider_key_missing',
      blockedStatus: 'blocked_until_explicit_authorization_or_local_runtime_available' as const,
      affectedSurfaceIds: keyRows.map((row) => row.surfaceId),
      currentEvidence: [sourceProviderCompatibilityReportPath],
      requiredAuthorization: 'explicit operator authorization to configure credentials and perform provider-backed validation',
      forbiddenShortcut: 'do not infer provider compatibility from a preset that requires an API key',
      validationMethod: 'rerun provider compatibility plus an explicit live-provider gate after authorization',
      claimAllowed: false as const,
    }),
    withDigest({
      schemaVersion: 'openclaude_provider_failure_mode_matrix_v1' as const,
      failureModeId: 'local_runtime_unavailable',
      blockedStatus: 'blocked_until_explicit_authorization_or_local_runtime_available' as const,
      affectedSurfaceIds: localRows.map((row) => row.surfaceId),
      currentEvidence: [sourceProviderCompatibilityReportPath, sourceRuntimeDoctorReportPath],
      requiredAuthorization: 'operator-provided local runtime evidence for Ollama, LM Studio, Atomic Chat, or custom loopback providers',
      forbiddenShortcut: 'do not treat a loopback base URL as proof that the local runtime is running',
      validationMethod: 'add an explicit no-network local runtime availability gate before live generation claims',
      claimAllowed: false as const,
    }),
    withDigest({
      schemaVersion: 'openclaude_provider_failure_mode_matrix_v1' as const,
      failureModeId: 'provider_reachability_skipped',
      blockedStatus: 'blocked_until_explicit_authorization_or_local_runtime_available' as const,
      affectedSurfaceIds: capabilityRows.map((row) => row.surfaceId),
      currentEvidence: [sourceRuntimeDoctorReportPath],
      requiredAuthorization: 'explicit provider or local-runtime reachability authorization',
      forbiddenShortcut: 'do not convert runtime doctor skipped reachability into successful provider reachability',
      validationMethod: 'verify runtime doctor reports provider reachability executed and passed under an authorized provider mode',
      claimAllowed: false as const,
    }),
    withDigest({
      schemaVersion: 'openclaude_provider_failure_mode_matrix_v1' as const,
      failureModeId: 'profile_direct_surface_drift',
      blockedStatus: 'blocked_until_explicit_authorization_or_local_runtime_available' as const,
      affectedSurfaceIds: driftRows.map((row) => row.surfaceId),
      currentEvidence: [sourceProviderCompatibilityReportPath],
      requiredAuthorization: 'bounded product decision on whether direct-only flags require profile presets or explicit documentation',
      forbiddenShortcut: 'do not hide direct-only provider flags behind the general provider-breadth claim',
      validationMethod: `verify profileOnlyPresets=${providerCompatibility.profileOnlyPresets.length} and directOnlyFlags=${providerCompatibility.directOnlyFlags.length} remain classified`,
      claimAllowed: false as const,
    }),
    withDigest({
      schemaVersion: 'openclaude_provider_failure_mode_matrix_v1' as const,
      failureModeId: 'live_model_authorization_missing',
      blockedStatus: 'blocked_until_explicit_authorization_or_local_runtime_available' as const,
      affectedSurfaceIds: capabilityRows.map((row) => row.surfaceId),
      currentEvidence: [sourceProviderCompatibilityReportPath, sourceRuntimeDoctorReportPath, sourceOssAxisArchitectureReportPath],
      requiredAuthorization: 'explicit live-model authorization before provider-backed execution or external validation',
      forbiddenShortcut: 'do not claim provider-backed execution, external validation, release readiness, production readiness, or autonomous reliability from local fixtures',
      validationMethod: 'run a separate authorized live-model validation gate with sanitized outputs and claim boundaries',
      claimAllowed: false as const,
    }),
  ]
}

function writeMarkdown(report: ProviderCapabilityMatrixReport): void {
  const capabilityRows = report.capabilityRows
    .map((row) => `| \`${row.surfaceId}\` | \`${row.provider}\` | \`${row.baseUrlCategory}\` | \`${row.requiresApiKey}\` | \`${row.capabilityStatus}\` |`)
    .join('\n')
  const failureRows = report.failureModeRows
    .map((row) => `| \`${row.failureModeId}\` | \`${row.affectedSurfaceIds.length}\` | ${row.forbiddenShortcut} |`)
    .join('\n')
  const checkRows = report.capabilityChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Provider Capability Matrix Report

Generated by: \`bun run product:provider-capability-matrix\`

## Claim Boundary

- This is a local no-provider provider capability and failure-mode matrix.
- It reads existing local provider compatibility, runtime doctor, and OSS axis review evidence.
- It does not call providers, live models, external services, package managers, or dependency installers.
- It does not claim provider-backed execution, provider compatibility, external validation, release readiness, production readiness, public readiness, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- direct_provider_flag_count: \`${report.directProviderFlagCount}\`
- provider_preset_default_count: \`${report.providerPresetDefaultCount}\`
- capability_row_count: \`${report.capabilityRowCount}\`
- local_no_key_provider_count: \`${report.localNoKeyProviderCount}\`
- openai_compatible_surface_count: \`${report.openAiCompatibleSurfaceCount}\`
- failure_mode_count: \`${report.failureModeCount}\`
- provenance_jsonl_path: \`${report.provenanceJsonlPath}\`
- provenance_jsonl_sha256: \`${report.provenanceJsonlSha256}\`

## Capability Rows

| Surface | Provider | Base URL Category | Requires API Key | Status |
| --- | --- | --- | --- | --- |
${capabilityRows}

## Failure Modes

| Failure Mode | Affected Surfaces | Forbidden Shortcut |
| --- | ---: | --- |
${failureRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  for (const path of [sourceProviderCompatibilityReportPath, sourceRuntimeDoctorReportPath, sourceOssAxisArchitectureReportPath]) {
    if (!existsSync(resolve(root, path))) {
      console.error(`RESULT: FAIL (${path} missing)`)
      process.exit(1)
    }
  }

  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const providerCompatibility = readJson<ProviderCompatibilityReport>(sourceProviderCompatibilityReportPath)
  const runtimeDoctor = readJson<RuntimeDoctorRegressionReport>(sourceRuntimeDoctorReportPath)
  const axisReview = readJson<AxisArchitectureReviewReport>(sourceOssAxisArchitectureReportPath)
  const capabilityRows = buildCapabilityRows(providerCompatibility.parsed, runtimeDoctor.parsed)
  const failureModeRows = buildFailureModeRows(providerCompatibility.parsed, capabilityRows)
  const provenanceRecords = [
    ...capabilityRows.map((row) => ({ recordType: 'capability', ...row })),
    ...failureModeRows.map((row) => ({ recordType: 'failure_mode', ...row })),
  ]
  const provenanceText = `${provenanceRecords.map((record) => JSON.stringify(record)).join('\n')}\n`
  writeFileSync(resolve(root, provenanceJsonlPath), provenanceText)
  const provenanceJsonlSha256 = sha256(provenanceText)
  let provenanceJsonlParseable = true
  for (const line of provenanceText.trim().split(/\r?\n/)) {
    try {
      JSON.parse(line)
    } catch {
      provenanceJsonlParseable = false
    }
  }

  const providerBreadthBacklog = axisReview.parsed.axisReviewRecords
    .filter((record) => record.axis === 'provider_breadth')
    .flatMap((record) => record.safeInternalImplementationBacklog)
  const runtimeDoctorSkippedReachability = runtimeDoctor.parsed.doctorChecks.some((item) => /provider reachability stayed skipped/i.test(item.label) && item.ok)
  const runtimeDoctorSkippedGeneration = runtimeDoctor.parsed.doctorChecks.some((item) => /provider generation readiness stayed skipped/i.test(item.label) && item.ok)
  const localNoKeyRows = capabilityRows.filter((row) => row.noApiKeyLocalCandidate)
  const openAiCompatibleRows = capabilityRows.filter((row) => row.openAiCompatibleTransport)
  const failureModeIds = failureModeRows.map((row) => row.failureModeId)
  const providerCallsPerformed: [] = []
  const liveModelCallsPerformed: [] = []
  const externalCallsPerformed: [] = []
  const protectedActionsExecuted: [] = []
  const capabilityChecks = [
    check('provider compatibility source is local no-provider and passed', providerCompatibility.parsed.mode === 'local_no_provider_provider_surface' && providerCompatibility.parsed.compatibilityChecks.every((item) => item.ok), sourceProviderCompatibilityReportPath),
    check('runtime doctor source is local no-provider and passed', runtimeDoctor.parsed.mode === 'local_no_provider_runtime_doctor_regression' && runtimeDoctor.parsed.doctorChecks.every((item) => item.ok), sourceRuntimeDoctorReportPath),
    check('OSS axis review requested provider capability backlog', axisReview.parsed.mode === 'local_no_provider_oss_axis_architecture_review' && axisReview.parsed.reviewChecks.every((item) => item.ok) && providerBreadthBacklog.some((item) => item.includes('per-provider capability and failure-mode rows')), `${providerBreadthBacklog.length} provider backlog items`),
    check('direct provider flags and preset defaults are fully represented', providerCompatibility.parsed.directProviderFlags.length >= 10 && providerCompatibility.parsed.providerPresetDefaults.length >= 18 && capabilityRows.length === providerCompatibility.parsed.providerPresetDefaults.length + providerCompatibility.parsed.directOnlyFlags.length, `${providerCompatibility.parsed.directProviderFlags.length} direct flags/${providerCompatibility.parsed.providerPresetDefaults.length} presets/${capabilityRows.length} rows`),
    check('product description providers are covered by capability rows', providerCompatibility.parsed.productDescriptionProviders.every((provider) => capabilityRows.some((row) => row.provider === provider || row.preset === provider || normalizeDirectSurface(row.provider) === provider)), providerCompatibility.parsed.productDescriptionProviders.join(',')),
    check('local no-key providers remain explicit and unvalidated', ['ollama', 'lmstudio', 'atomic-chat'].every((preset) => localNoKeyRows.some((row) => row.preset === preset)) && localNoKeyRows.every((row) => row.liveValidationStatus === 'not_executed_requires_explicit_authorization'), localNoKeyRows.map((row) => row.surfaceId).join(',')),
    check('OpenAI-compatible profile surfaces are classified', openAiCompatibleRows.length >= 10 && openAiCompatibleRows.every((row) => row.profilePresetAvailable), `${openAiCompatibleRows.length} openai-compatible rows`),
    check('runtime doctor keeps provider reachability and generation skipped', runtimeDoctorSkippedReachability && runtimeDoctorSkippedGeneration, 'OpenAI-compatible mode disabled'),
    check('required failure modes are present exactly once', requiredFailureModeIds.every((id) => failureModeIds.includes(id)) && failureModeIds.length === requiredFailureModeIds.length, failureModeIds.join(',')),
    check('failure modes block shortcuts and claims', failureModeRows.every((row) => row.claimAllowed === false && row.affectedSurfaceIds.length > 0 && row.forbiddenShortcut.length > 0), `${failureModeRows.length} failure modes`),
    check('capability rows block provider-backed and external claims', capabilityRows.every((row) => row.providerBackedExecutionClaimAllowed === false && row.externalValidationClaimAllowed === false && row.claimAllowed === false), `${capabilityRows.length} rows`),
    check('provenance JSONL is parseable and hash-addressed', provenanceJsonlParseable && provenanceJsonlSha256.length === 64 && provenanceRecords.length === capabilityRows.length + failureModeRows.length && provenanceRecords.every((record) => /^[a-f0-9]{64}$/.test(record.recordDigest)), provenanceJsonlPath),
    check('no provider live external or protected actions occurred', providerCallsPerformed.length === 0 && liveModelCallsPerformed.length === 0 && externalCallsPerformed.length === 0 && protectedActionsExecuted.length === 0, 'all call arrays empty'),
  ]

  const report: ProviderCapabilityMatrixReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_provider_capability_matrix',
    sourceProviderCompatibilityReportPath,
    sourceProviderCompatibilityReportSha256: providerCompatibility.digest,
    sourceRuntimeDoctorReportPath,
    sourceRuntimeDoctorReportSha256: runtimeDoctor.digest,
    sourceOssAxisArchitectureReportPath,
    sourceOssAxisArchitectureReportSha256: axisReview.digest,
    directProviderFlagCount: providerCompatibility.parsed.directProviderFlags.length,
    providerPresetDefaultCount: providerCompatibility.parsed.providerPresetDefaults.length,
    productDescriptionProviders: providerCompatibility.parsed.productDescriptionProviders,
    capabilityRowCount: capabilityRows.length,
    localNoKeyProviderCount: localNoKeyRows.length,
    openAiCompatibleSurfaceCount: openAiCompatibleRows.length,
    failureModeCount: failureModeRows.length,
    failureModeIds,
    provenanceJsonlPath,
    provenanceJsonlSha256,
    provenanceJsonlRecordCount: provenanceRecords.length,
    provenanceJsonlParseable,
    providerCallsPerformed,
    liveModelCallsPerformed,
    externalCallsPerformed,
    protectedActionsExecuted,
    providerBackedExecutionClaimAllowed: false,
    providerCompatibilityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    primarySourceInputs: [
      {
        sourceProject: 'OpenAI API Reference',
        sourceUrl: 'https://platform.openai.com/docs/api-reference',
        observedPattern: 'Provider-compatible products should keep base URL, model, and credential requirements explicit rather than treating configuration as successful execution.',
        localAbsorption: 'OpenClaude records provider preset capabilities separately from provider-backed execution and keeps live validation blocked until explicit authorization exists.',
      },
      {
        sourceProject: 'OpenTelemetry Logs Data Model',
        sourceUrl: 'https://opentelemetry.io/docs/specs/otel/logs/data-model/',
        observedPattern: 'Operational evidence is stronger when capability and failure-mode events are represented as structured, queryable records.',
        localAbsorption: 'OpenClaude writes provider capability and failure-mode records as parseable JSONL with stable digests.',
      },
      {
        sourceProject: 'SLSA Build Provenance',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'Evidence packages should identify source materials and keep derived claims bound to those materials.',
        localAbsorption: 'OpenClaude records hashes for provider compatibility, runtime doctor, and OSS axis review source reports.',
      },
    ],
    capabilityRows,
    failureModeRows,
    capabilityChecks,
    claimBoundary: 'Provider capability matrix is local no-provider capability and failure-mode evidence only. It does not call providers, call live models, call external services, install dependencies, publish, deploy, launch, or authorize provider-backed execution, public comparison, superiority, release, production, external-validation, or autonomous-reliability claims.',
  }

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of capabilityChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = capabilityChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`direct_provider_flag_count=${report.directProviderFlagCount}`)
  console.log(`provider_preset_default_count=${report.providerPresetDefaultCount}`)
  console.log(`capability_row_count=${report.capabilityRowCount}`)
  console.log(`local_no_key_provider_count=${report.localNoKeyProviderCount}`)
  console.log(`openai_compatible_surface_count=${report.openAiCompatibleSurfaceCount}`)
  console.log(`failure_mode_count=${report.failureModeCount}`)
  console.log(`provenance_jsonl_records=${report.provenanceJsonlRecordCount}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`provider_backed_execution_claim_allowed=${report.providerBackedExecutionClaimAllowed}`)
}

main()

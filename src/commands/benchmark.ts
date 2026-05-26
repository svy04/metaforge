import type { Command, LocalCommandCall } from '../types/command.js'
import {
  benchmarkModel,
  benchmarkMultipleModels,
  formatBenchmarkResults,
  isBenchmarkSupported,
} from '../utils/model/benchmark.js'
import { getOllamaModelOptions } from '../utils/model/ollamaModels.js'

async function runBenchmark(
  model?: string,
): Promise<string> {
  if (!isBenchmarkSupported()) {
    return (
      'Benchmark not supported for this provider.\n' +
      'Supported: OpenAI-compatible endpoints (Ollama, NVIDIA NIM, MiniMax)\n'
    )
  }

  let modelsToBenchmark: string[]

  if (model) {
    modelsToBenchmark = [model]
  } else {
    const ollamaModels = getOllamaModelOptions()
    modelsToBenchmark = ollamaModels
      .slice(0, 3)
      .map((m) => m.value)
      .filter((value): value is string => typeof value === 'string')
  }

  const lines = [`Benchmarking ${modelsToBenchmark.length} model(s)...`]

  const results = await benchmarkMultipleModels(
    modelsToBenchmark,
    (completed, total, result) => {
      lines.push(
        `[${completed}/${total}] ${result.model}: ` +
          `${result.success ? result.tokensPerSecond.toFixed(1) + ' tps' : 'FAILED'}`,
      )
    },
  )

  lines.push('', formatBenchmarkResults(results))
  return `${lines.join('\n')}\n`
}

export const call: LocalCommandCall = async args => ({
  type: 'text',
  value: await runBenchmark(args.trim() || undefined),
})

export const benchmark = {
  name: 'benchmark',
  description: 'Benchmark locally available OpenAI-compatible models.',
  type: 'local',
  supportsNonInteractive: true,
  load: async () => ({ call }),
} satisfies Command

export default benchmark

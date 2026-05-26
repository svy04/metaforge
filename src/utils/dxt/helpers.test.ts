import { describe, expect, test } from 'bun:test'

import {
  generateExtensionId,
  parseAndValidateManifestFromText,
} from './helpers.js'

describe('DXT/MCPB manifest helpers', () => {
  test('validates a current MCPB manifest through the public schema export', async () => {
    const manifest = await parseAndValidateManifestFromText(
      JSON.stringify({
        manifest_version: '0.4',
        name: 'Demo Search',
        version: '1.0.0',
        description: 'Demo MCPB package',
        author: { name: 'Example Org' },
        server: {
          type: 'node',
          entry_point: 'server.js',
          mcp_config: { command: 'node', args: ['server.js'] },
        },
      }),
    )

    expect(manifest.name).toBe('Demo Search')
    expect(generateExtensionId(manifest, 'local.dxt')).toBe(
      'local.dxt.example-org.demo-search',
    )
  })

  test('rejects an invalid MCPB manifest with field-level errors', async () => {
    await expect(
      parseAndValidateManifestFromText(
        JSON.stringify({
          manifest_version: '0.4',
          name: 'Broken',
          author: { name: 'Example Org' },
        }),
      ),
    ).rejects.toThrow(/Invalid manifest/)
  })
})

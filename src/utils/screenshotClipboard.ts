import { mkdtemp, rm, writeFile } from 'fs/promises'
import { tmpdir } from 'os'
import { join } from 'path'
import { type AnsiToPngOptions, ansiToPng } from './ansiToPng.js'
import { execFileNoThrowWithCwd } from './execFileNoThrow.js'
import { logError } from './log.js'
import { getPlatform } from './platform.js'

/**
 * Copies an image (from ANSI text) to the system clipboard.
 * Supports macOS, Linux (with xclip/xsel), and Windows.
 *
 * Pure-TS pipeline: ANSI text → bitmap-font render → PNG encode. No WASM,
 * no system fonts, so this works in every build (native and JS).
 */
export async function copyAnsiToClipboard(
  ansiText: string,
  options?: AnsiToPngOptions,
): Promise<{ success: boolean; message: string }> {
  let tempPng: ScreenshotTempPng | undefined
  try {
    const pngBuffer = ansiToPng(ansiText, options)
    tempPng = await writeScreenshotTempPng(pngBuffer)
    return await copyPngToClipboard(tempPng.pngPath)
  } catch (error) {
    logError(error)
    return {
      success: false,
      message: `Failed to copy screenshot: ${error instanceof Error ? error.message : 'Unknown error'}`,
    }
  } finally {
    if (tempPng) {
      try {
        await tempPng.dispose()
      } catch {
        // Ignore cleanup errors
      }
    }
  }
}

export type ScreenshotTempPng = {
  tempDir: string
  pngPath: string
  dispose: () => Promise<void>
}

export async function writeScreenshotTempPng(
  pngBuffer: Buffer,
  tempRoot = tmpdir(),
): Promise<ScreenshotTempPng> {
  const tempDir = await mkdtemp(join(tempRoot, 'claude-code-screenshot-'))
  const pngPath = join(tempDir, 'screenshot.png')
  await writeFile(pngPath, pngBuffer, { flag: 'wx', mode: 0o600 })

  return {
    tempDir,
    pngPath,
    dispose: () => rm(tempDir, { recursive: true, force: true }),
  }
}

async function copyPngToClipboard(
  pngPath: string,
): Promise<{ success: boolean; message: string }> {
  const platform = getPlatform()

  if (platform === 'macos') {
    // macOS: Use osascript to copy PNG to clipboard
    // Escape backslashes and double quotes for AppleScript string
    const escapedPath = pngPath.replace(/\\/g, '\\\\').replace(/"/g, '\\"')
    const script = `set the clipboard to (read (POSIX file "${escapedPath}") as «class PNGf»)`
    const result = await execFileNoThrowWithCwd('osascript', ['-e', script], {
      timeout: 5000,
    })

    if (result.code === 0) {
      return { success: true, message: 'Screenshot copied to clipboard' }
    }
    return {
      success: false,
      message: `Failed to copy to clipboard: ${result.stderr}`,
    }
  }

  if (platform === 'linux') {
    // Linux: Try xclip first, then xsel
    const xclipResult = await execFileNoThrowWithCwd(
      'xclip',
      ['-selection', 'clipboard', '-t', 'image/png', '-i', pngPath],
      { timeout: 5000 },
    )

    if (xclipResult.code === 0) {
      return { success: true, message: 'Screenshot copied to clipboard' }
    }

    // Try xsel as fallback
    const xselResult = await execFileNoThrowWithCwd(
      'xsel',
      ['--clipboard', '--input', '--type', 'image/png'],
      { timeout: 5000 },
    )

    if (xselResult.code === 0) {
      return { success: true, message: 'Screenshot copied to clipboard' }
    }

    return {
      success: false,
      message:
        'Failed to copy to clipboard. Please install xclip or xsel: sudo apt install xclip',
    }
  }

  if (platform === 'windows') {
    // Windows: Use PowerShell to copy image to clipboard
    const psScript = `Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::SetImage([System.Drawing.Image]::FromFile('${pngPath.replace(/'/g, "''")}'))`
    const result = await execFileNoThrowWithCwd(
      'powershell',
      ['-NoProfile', '-Command', psScript],
      { timeout: 5000 },
    )

    if (result.code === 0) {
      return { success: true, message: 'Screenshot copied to clipboard' }
    }
    return {
      success: false,
      message: `Failed to copy to clipboard: ${result.stderr}`,
    }
  }

  return {
    success: false,
    message: `Screenshot to clipboard is not supported on ${platform}`,
  }
}

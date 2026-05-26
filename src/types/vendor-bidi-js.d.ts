declare module 'bidi-js' {
  type BaseDirection = 'ltr' | 'rtl' | 'auto'

  type EmbeddingParagraph = {
    start: number
    end: number
    level: number
  }

  type EmbeddingLevels = {
    levels: Uint8Array
    paragraphs: EmbeddingParagraph[]
  }

  type Bidi = {
    getEmbeddingLevels(
      text: string,
      baseDirection?: BaseDirection,
    ): EmbeddingLevels
  }

  export default function bidiFactory(): Bidi
}

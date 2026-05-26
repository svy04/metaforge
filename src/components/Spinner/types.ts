export type RGBColor = {
  r: number
  g: number
  b: number
}

export type SpinnerMode =
  | 'requesting'
  | 'responding'
  | 'thinking'
  | 'tool-input'
  | 'tool-use'

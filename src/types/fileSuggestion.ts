export type FileSuggestionCommandInput = {
  hook_event_name?: 'FileSuggestion'
  session_id?: string
  transcript_path?: string
  cwd?: string
  query: string
  [key: string]: unknown
}


export type QuerySource =
  | 'sdk'
  | 'repl'
  | 'repl_main_thread'
  | `repl_main_thread:${string}`
  | `agent:${string}`
  | `agent:builtin:${string}`
  | 'away_summary'
  | 'feedback'
  | 'generate_session_title'
  | 'insights'
  | 'memdir_relevance'
  | 'model_validation'
  | 'orchestra_planner'
  | 'permission_explainer'
  | 'session_memory'
  | 'session_search'
  | 'side_question'
  | 'teleport_generate_title'
  | (string & {})

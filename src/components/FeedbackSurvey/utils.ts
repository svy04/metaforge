export type FeedbackSurveyResponse =
  | 'dismissed'
  | 'bad'
  | 'ok'
  | 'good'
  | 'great'

export type FeedbackSurveyType =
  | 'session'
  | 'memory'
  | 'post_compact'
  | (string & {})


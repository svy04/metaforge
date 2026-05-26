# Goal State Machine

States:
- proposed
- active
- validating
- complete_internal
- protected_action_required
- safety_fail

Transitions:
- proposed -> active when the owner provides a bounded goal.
- active -> validating when repo-local artifacts are created.
- validating -> complete_internal when local validation passes.
- validating -> protected_action_required when the next step needs deploy, publish,
  provider calls, live model calls, platform posting, account automation, or public claims.
- validating -> safety_fail when validation fails or unsafe influence support appears.

Every completed goal must select exactly one next safe goal unless a terminal condition is reached.

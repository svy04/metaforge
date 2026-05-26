# Influence Factory Product App Self-Test Report v35

terminal_condition: GUIDED_FIRST_RUN_GUARD_V35_READY
local_product_status: guided_first_run_guard_ready
first_goal_flow: guided_input_to_owner_ready_package_without_external_execution
product_completion_claim_scope: repo_local_internal_only

## Commands

- JavaScript syntax check PASS: `node --check avf\influence_factory\product_app\app.js`
- Chrome headless screenshot PASS: `chrome --headless --disable-gpu --window-size=1440,1200 --screenshot=render-check-v35.png file:///.../index.html#selftest`
- Chrome headless DOM dump PASS: `chrome --headless --disable-gpu --dump-dom file:///.../index.html#selftest`

## Evidence

- render-check-v35.png bytes: 203280
- self-test-v35-dom.html bytes: 169987
- SELF_TEST_PASS_V35
- Guided first-run guard ready
- Missing input guard ready
- Recovery prompts ready

## Boundary

- protected_action_executed: false
- external_validation_authorized: false
- external_validation_executed: false
- external_validation_claimed: false
- external_calls: false
- provider_calls_performed: false
- live_model_calls_performed: false
- dependency_install_performed: false
- deploy_performed: false
- publish_performed: false
- platform_posting_performed: false
- personal_account_automation_performed: false
- release_readiness_claimed: false
- public_readiness_claimed: false
- production_readiness_claimed: false
- autonomous_reliability_claimed: false

## Result

Guided first-run guard ready. Missing input guard ready. Recovery prompts ready.

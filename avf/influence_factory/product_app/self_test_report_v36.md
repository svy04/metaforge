# Influence Factory Product App Self-Test Report v36

terminal_condition: LOCAL_OWNER_TRIAL_SCRIPT_V36_READY
local_product_status: local_owner_trial_script_ready
first_goal_flow: guided_first_run_to_local_owner_trial_without_external_users
product_completion_claim_scope: repo_local_internal_only

## Commands

- JavaScript syntax check PASS: `node --check avf\influence_factory\product_app\app.js`
- Chrome headless screenshot PASS: `chrome --headless --disable-gpu --window-size=1440,1200 --screenshot=render-check-v36.png <local-selftest-url>`
- Chrome headless DOM dump PASS: `chrome --headless --disable-gpu --dump-dom <local-selftest-url>`

## Evidence

- render-check-v36.png bytes: 204825
- self-test-v36-dom.html bytes: 176177
- SELF_TEST_PASS_V36
- Local owner trial script ready
- Owner trial observation log ready
- Owner trial acceptance checklist ready

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

Local owner trial script ready. Owner trial observation log ready. Owner trial acceptance checklist ready.

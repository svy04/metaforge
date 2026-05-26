# Owner Trial Evidence Schema

terminal_condition: OWNER_TRIAL_EVIDENCE_RECORDER_V37_READY
terminal_status: FIRST_OWNER_TRIAL_LOCAL_SYSTEM_READY
first_goal_flow: local_owner_trial_to_evidence_loop_without_external_users
product_completion_claim_scope: repo_local_internal_only
external_validation_authorized: false
external_validation_executed: false
external_validation_claimed: false
protected_action_executed: false
external_calls: false
next_safe_goal_count: 0
fake human impersonation: blocked
undisclosed bot networks: blocked
platform posting: blocked
release readiness claim: blocked
public readiness claim: blocked
production readiness claim: blocked
external validation claim: blocked

- owner_goal_used: The exact local owner goal used for the trial.
- trial_completed_locally: Whether the owner-only local trial was completed.
- missing_inputs_found: Inputs that were missing before recovery.
- recovery_prompt_quality: Whether recovery prompts were clear enough to continue.
- owner_ready_package_clarity: Whether the owner-ready package was inspectable.
- brand_ip_style_memory_clarity: Whether style memory was clear and reusable.
- image_reference_packet_clarity: Whether image-generation reference packets were usable.
- content_packet_clarity: Whether draft content and channel map were clear.
- codex_packet_clarity: Whether the Codex packet was PR-sized and testable.
- safety_boundary_confidence: Whether blocked influence and public actions were visible.
- friction_notes: Any confusion, missing affordance, or slow step.
- selected_next_local_improvement: Exactly one local-safe improvement selected by owner evidence.

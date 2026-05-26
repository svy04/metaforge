# Owner Trial Step Script

terminal_condition: LOCAL_OWNER_TRIAL_SCRIPT_V36_READY
first_goal_flow: guided_first_run_to_local_owner_trial_without_external_users
product_completion_claim_scope: repo_local_internal_only
external_validation_authorized: false
external_validation_executed: false
external_validation_claimed: false
protected_action_executed: false
external_calls: false
selected_next_safe_goal: create_owner_trial_evidence_recorder_v37_without_external_users
next_safe_goal_count: 1
fake human impersonation: blocked
undisclosed bot networks: blocked
platform posting: blocked
release readiness claim: blocked
public readiness claim: blocked
production readiness claim: blocked
external validation claim: blocked

- open_local_workbench: Open the local product workbench from the repo-local HTML file. Scope: owner_local_manual_trial_only.
- complete_guided_first_run_guard: Run Guided First Run Guard and recover missing required inputs. Scope: owner_local_manual_trial_only.
- build_owner_ready_package: Build the First Goal Owner-Ready Package after required inputs are present. Scope: owner_local_manual_trial_only.
- inspect_brand_ip_style_memory: Inspect brand DNA, character bible, visual guide, forbidden styles, and rights notes. Scope: owner_local_manual_trial_only.
- inspect_image_generation_reference_packet: Inspect image prompt pack, reference image index, asset registry, and negative prompt boundaries. Scope: owner_local_manual_trial_only.
- inspect_content_and_codex_packets: Inspect draft content, Codex context packet, acceptance criteria, and forbidden changes. Scope: owner_local_manual_trial_only.
- run_safety_boundary_review: Confirm deceptive influence, platform posting, deploy, publish, and external claims remain blocked. Scope: owner_local_manual_trial_only.
- record_owner_observations: Record friction, confusion, missing proof, style drift risk, and next local improvement. Scope: owner_local_manual_trial_only.
- decide_next_local_improvement: Select exactly one next safe local improvement without external users or protected actions. Scope: owner_local_manual_trial_only.

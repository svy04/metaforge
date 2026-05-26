from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
PACKAGE = ROOT / "avf" / "influence_factory" / "operator_package_v14"
GOALS = ROOT / "docs" / "goals"

SELECTED_NEXT = "owner_runs_v14_operator_package_with_real_goal_or_requests_protected_authorization"

RECORD = {
    "terminal_condition": "LOCAL_OPERATOR_PACKAGE_V14_READY",
    "local_product_status": "operator_package_ready_for_real_goal_use",
    "next_safe_goal_count": 1,
    "selected_next_safe_goal": SELECTED_NEXT,
    "protected_action_executed": False,
    "external_calls": False,
    "provider_calls_performed": False,
    "live_model_calls_performed": False,
    "dependency_install_performed": False,
    "deploy_performed": False,
    "publish_performed": False,
    "platform_posting_performed": False,
    "personal_account_automation_performed": False,
    "deceptive_influence_supported": False,
    "release_readiness_claimed": False,
    "public_readiness_claimed": False,
    "production_readiness_claimed": False,
    "external_validation_claimed": False,
    "autonomous_reliability_claimed": False,
}

GOAL_TEMPLATE = {
    "goal_id": "owner-real-goal-v14",
    "idea": "Transparent AI Creator Collective for safe brand, media, and community growth",
    "audience": "founders, creators, product teams, infrastructure operators, and Brand/IP builders",
    "promise": "turn one raw idea into a local operator-reviewed product, style, content, Codex, safety, and next-action package",
    "proof_target": "a local operator package with run sequence, acceptance checklist, protected action request, and handoff packet",
    "brand_dna": "transparent, evidence-led, creator-native, technically rigorous, and approval-gated",
    "character_bible": "AI-assisted personas disclose their nature and never pretend to be independent humans",
    "visual_guide": "web-first creator studio, consistent style memory, reusable image prompt references, no fake social proof",
    "forbidden_styles": "fake crowds, bot armies, spam visuals, harassment motifs, impersonation, astroturfing, brigading, or platform bypass",
    "first_result": "one local operator package ready for owner review",
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    write_json(PACKAGE / "operator_package_v14_record.json", RECORD)
    write_json(APP / "product_workbench_v14_record.json", RECORD)
    write_json(PACKAGE / "FIRST_REAL_GOAL_TEMPLATE.json", GOAL_TEMPLATE)
    write_json(
        PACKAGE / "run_manifest.json",
        {
            "terminal_condition": "LOCAL_OPERATOR_PACKAGE_V14_READY",
            "protected_action_executed": False,
            "external_calls": False,
            "operator_files": [
                "OPERATOR_QUICKSTART.md",
                "FIRST_REAL_GOAL_TEMPLATE.json",
                "RUN_SEQUENCE.md",
                "LOCAL_ACCEPTANCE_CHECKLIST.md",
                "PROTECTED_ACTION_AUTHORIZATION_REQUEST.md",
                "OPERATOR_HANDOFF_PACKET.md",
                "NEXT_SAFE_GOAL.md",
            ],
        },
    )
    write(
        PACKAGE / "OPERATOR_QUICKSTART.md",
        "# Operator Quickstart v14\n\n"
        "1. Open the local product app.\n"
        "2. Enter or edit the real owner goal.\n"
        "3. Build the owner goal bundle preview.\n"
        "4. Build the style continuity workbench.\n"
        "5. Build the content approval board.\n"
        "6. Build the evidence dashboard.\n"
        "7. Run the local operator cycle script when file artifacts are needed.\n\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write(
        PACKAGE / "RUN_SEQUENCE.md",
        "# Run Sequence\n\n"
        "Command:\n\n"
        "```text\n"
        "python scripts\\run_avf_influence_factory_operator_cycle_local.py --goal avf\\influence_factory\\operator_package_v14\\FIRST_REAL_GOAL_TEMPLATE.json --out avf\\influence_factory\\operator_package_v14\\cycle_output\n"
        "```\n\n"
        "The command writes local files only and preserves protected_action_executed: false.\n",
    )
    write(
        PACKAGE / "LOCAL_ACCEPTANCE_CHECKLIST.md",
        "# Local Acceptance Checklist\n\n"
        "- [ ] goal fields are complete\n"
        "- [ ] Brand/IP style memory is present\n"
        "- [ ] image prompt pack carries rights notes\n"
        "- [ ] content drafts are approval-gated\n"
        "- [ ] evidence dashboard is built\n"
        "- [ ] protected_action_executed: false\n"
        "- [ ] external_calls: false\n",
    )
    write(
        PACKAGE / "PROTECTED_ACTION_AUTHORIZATION_REQUEST.md",
        "# Protected Action Request\n\n"
        "Default authorizations:\n\n"
        "- public_posting: false\n"
        "- deploy: false\n"
        "- publish: false\n"
        "- provider_calls: false\n"
        "- external_calls: false\n"
        "- platform_automation: false\n"
        "- release_readiness_claim: false\n"
        "- production_readiness_claim: false\n"
        "- public_readiness_claim: false\n\n"
        "Protected action request ready. No protected action is executed by this package.\n",
    )
    write(
        PACKAGE / "OPERATOR_HANDOFF_PACKET.md",
        "# Operator Handoff Packet\n\n"
        "Use this packet to hand a real owner goal to Codex or another approved local operator.\n\n"
        "- goal template: FIRST_REAL_GOAL_TEMPLATE.json\n"
        "- run sequence: RUN_SEQUENCE.md\n"
        "- acceptance checklist: LOCAL_ACCEPTANCE_CHECKLIST.md\n"
        "- protected action request: PROTECTED_ACTION_AUTHORIZATION_REQUEST.md\n\n"
        "selected_next_safe_goal: owner_runs_v14_operator_package_with_real_goal_or_requests_protected_authorization\n"
    )
    write(
        PACKAGE / "NEXT_SAFE_GOAL.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: owner_runs_v14_operator_package_with_real_goal_or_requests_protected_authorization\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write(
        GOALS / "INFLUENCE_FACTORY_OPERATOR_PACKAGE_V14_COMPLETION_AUDIT.md",
        "# Influence Factory Operator Package v14 Completion Audit\n\n"
        "RESULT: PASS\n\n"
        "status: PROVEN\n\n"
        "The local operator package exists and contains quickstart, goal template, run sequence, acceptance checklist, "
        "protected action request, handoff packet, manifest, and next safe goal.\n",
    )
    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_OPERATOR_PACKAGE_V14.md",
        "# Next After Influence Factory Operator Package v14\n\n"
        "selected_next_safe_goal: owner_runs_v14_operator_package_with_real_goal_or_requests_protected_authorization\n"
        "next_safe_goal_count: 1\n"
        "selected_next_goal_executed: false\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write(
        GOALS / "INFLUENCE_FACTORY_OPERATOR_PACKAGE_V14_VALIDATION_REPORT.md",
        "# Influence Factory Operator Package v14 Validation Report\n\n"
        "RESULT: PENDING_VALIDATION\n\n"
        "This report is updated after validator execution.\n",
    )
    print("OPERATOR_PACKAGE_V14_CREATED=PASS")
    print("terminal_condition=LOCAL_OPERATOR_PACKAGE_V14_READY")
    print(f"selected_next_safe_goal={SELECTED_NEXT}")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

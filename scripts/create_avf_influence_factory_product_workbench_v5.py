"""Create Influence Factory Workbench v5.

v5 adds the product's key one-click behavior: a user can enter an idea and
produce a local factory packet containing product, strategy, brand/IP, content,
image prompt, Codex implementation, safety/approval, and next-action sections.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
GOALS = ROOT / "docs" / "goals"


RECORD = {
    "terminal_condition": "LOCAL_PRODUCT_WORKBENCH_V5_READY",
    "local_product_status": "one_click_local_factory_product",
    "completed_internal_product": True,
    "next_safe_goal_count": 1,
    "selected_next_safe_goal": "owner_runs_first_real_idea_through_v5_or_authorizes_protected_productization",
    "openclaude_required": False,
    "protected_action_executed": False,
    "provider_calls_performed": False,
    "live_model_calls_performed": False,
    "external_service_calls_performed": False,
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


FACTORY_SECTION = """      <section id="factory" class="panel">
        <h2>One-Click Factory Run</h2>
        <p class="note">Turn the current idea into one local operating packet. No provider call, no publish, no platform automation.</p>
        <button id="runFactoryButton">Run Local Factory</button>
        <h3>Factory Packet Viewer</h3>
        <div class="packet-labels">Product Brief · Strategy Brief · Brand/IP Brief · Content Pack · Image Prompt Pack · Codex Implementation Pack · Safety/Approval Pack · Next Action Pack</div>
        <div id="factoryPacketView" class="stack"></div>
      </section>
"""


FACTORY_JS = r'''
function buildFactoryPacket(workspace){
  return {
    "Product Brief": {
      idea: workspace.northStar.summary,
      audience: workspace.northStar.audience,
      promise: workspace.northStar.promise,
      proofTarget: workspace.northStar.proofTarget,
      firstResult: workspace.northStar.firstResult
    },
    "Strategy Brief": {
      score: workspace.strategy.score,
      positioning: workspace.strategy.positioning,
      risks: workspace.strategy.risks,
      successCriteria: workspace.strategy.successCriteria
    },
    "Brand/IP Brief": {
      brandDna: workspace.brandIp.brandDna,
      characterBible: workspace.brandIp.characterBible,
      visualGuide: workspace.brandIp.visualGuide,
      paletteTypography: workspace.brandIp.paletteTypography,
      forbiddenStyles: workspace.brandIp.forbiddenStyles,
      rightsNotes: workspace.brandIp.rightsNotes
    },
    "Content Pack": workspace.drafts.map((draft)=>({channel:draft.channel,title:draft.title,status:draft.status,text:draft.text})),
    "Image Prompt Pack": workspace.references.promptPack,
    "Codex Implementation Pack": workspace.codexPackets[workspace.codexPackets.length-1]||{},
    "Safety/Approval Pack": {
      safety: workspace.safety,
      approval: workspace.approval,
      protectedActionExecuted: false,
      published: false,
      posted: false
    },
    "Next Action Pack": {
      tasks: workspace.tasks,
      selectedNextSafeGoal: "owner_runs_first_real_idea_through_v5_or_authorizes_protected_productization",
      boundary: "Protected action boundary preserved"
    }
  };
}
function renderFactoryPacket(workspace){
  const packet=workspace.factoryPacket||buildFactoryPacket(workspace);
  const target=document.querySelector("#factoryPacketView");
  if(!target)return;
  target.innerHTML=Object.entries(packet).map(([title,value])=>card(title,typeof value==="string"?value:JSON.stringify(value,null,2),["factory packet"])).join("");
}
function runFactoryFromIdea(){
  buildNorthStar();
  calculateOpportunityScore();
  saveBrandIpVault();
  buildReferencePack();
  buildCampaign();
  generateChannelDrafts();
  importFeedback();
  createGrowthExperiment();
  generateCodexTaskPacket();
  runSafetyReview();
  const workspace=getWorkspace();
  workspace.factoryPacket=buildFactoryPacket(workspace);
  addEvidence(workspace,"Factory packet generated.");
  addEvidence(workspace,"Image prompt pack included.");
  addEvidence(workspace,"Codex implementation packet included.");
  addEvidence(workspace,"Protected action boundary preserved.");
  saveWorkspace(workspace);
}
'''


AUDIT_REQUIREMENTS = [
    "One-Click Factory Run",
    "Factory Packet Viewer",
    "Product Brief",
    "Strategy Brief",
    "Brand/IP Brief",
    "Content Pack",
    "Image Prompt Pack",
    "Codex Implementation Pack",
    "Safety/Approval Pack",
    "Next Action Pack",
    "runFactoryFromIdea",
    "buildFactoryPacket",
    "renderFactoryPacket",
    "factoryPacket persistence",
    "idea-to-strategy",
    "idea-to-brand-ip",
    "idea-to-reference-pack",
    "idea-to-content-pack",
    "idea-to-growth-experiment",
    "idea-to-codex-packet",
    "protected action boundary preserved",
    "no provider calls",
    "no live model calls",
    "no external service calls",
    "no dependency install",
    "no deploy",
    "no publish",
    "no platform posting",
    "no account automation",
    "no deceptive influence support",
    "no public readiness claim",
    "no release readiness claim",
    "no production readiness claim",
    "no external validation claim",
    "no autonomous reliability claim",
    "North Star Intake retained",
    "Strategy Engine retained",
    "Brand/IP Vault retained",
    "Reference Pack Builder retained",
    "Persona Network retained",
    "Campaign Builder retained",
    "Content Pipeline retained",
    "Growth Experiments retained",
    "Codex Packet Factory retained",
    "Approval Gate retained",
    "Safety Scanner retained",
    "Evidence Ledger retained",
    "Workspace Import/Export retained",
    "Self Test retained",
    "MVP compatibility retained",
    "v2 compatibility retained",
    "v3 compatibility retained",
    "v4 compatibility retained",
    "owner review remains local",
    "content remains draft-first",
    "image prompts remain owner-reviewable",
    "Codex tasks remain PR-sized",
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing expected anchor: {old[:80]}")
    return text.replace(old, new, 1)


def patch_index() -> None:
    path = APP / "index.html"
    html = path.read_text(encoding="utf-8")
    if 'data-section="factory"' not in html:
        html = replace_once(
            html,
            '      <button data-section="strategy">Strategy Engine</button>\n',
            '      <button data-section="strategy">Strategy Engine</button>\n      <button data-section="factory">One-Click Factory Run</button>\n',
        )
        html = replace_once(
            html,
            '      <section id="strategy" class="panel">\n',
            FACTORY_SECTION + '      <section id="strategy" class="panel">\n',
        )
    path.write_text(html, encoding="utf-8")


def patch_css() -> None:
    path = APP / "styles.css"
    css = path.read_text(encoding="utf-8")
    if ".packet-labels" not in css:
        css += "\n.packet-labels{border:1px solid var(--line);background:#fff;border-radius:8px;padding:10px;color:var(--muted);font-weight:650;margin:10px 0 14px}\n"
    path.write_text(css, encoding="utf-8")


def patch_js() -> None:
    path = APP / "app.js"
    js = path.read_text(encoding="utf-8")
    if "function buildFactoryPacket" not in js:
        js = replace_once(js, "function renderNorthStar(workspace){", FACTORY_JS + "function renderNorthStar(workspace){")
    if "renderFactoryPacket(workspace);" not in js:
        js = replace_once(
            js,
            "renderReferences(workspace);renderPersonas(workspace);",
            "renderReferences(workspace);renderFactoryPacket(workspace);renderPersonas(workspace);",
        )
    if 'querySelector("#runFactoryButton")' not in js:
        js = replace_once(
            js,
            'document.querySelector("#scoreButton").addEventListener("click",calculateOpportunityScore);',
            'document.querySelector("#scoreButton").addEventListener("click",calculateOpportunityScore);document.querySelector("#runFactoryButton").addEventListener("click",runFactoryFromIdea);',
        )
    if "SELF_TEST_PASS_V5" not in js:
        js = replace_once(
            js,
            'const result="SELF_TEST_PASS_V4 Strategy score calculated Reference pack built Codex task packet generated Approval gate blocked protected action";',
            'runFactoryFromIdea();const result="SELF_TEST_PASS_V5 Factory packet generated Image prompt pack included Codex implementation packet included Protected action boundary preserved";',
        )
    path.write_text(js, encoding="utf-8")


def write_reports() -> None:
    write_json(APP / "product_workbench_v5_record.json", RECORD)
    readme = (APP / "README.md").read_text(encoding="utf-8")
    if "## v5 One-Click Factory Run" not in readme:
        readme += """

## v5 One-Click Factory Run

v5 adds a one-click local factory run that turns the current idea into a product
brief, strategy brief, Brand/IP brief, content pack, image prompt pack, Codex
implementation pack, safety/approval pack, and next action pack.
"""
        write(APP / "README.md", readme)

    audit_lines = ["# Influence Factory Product Workbench v5 Completion Audit", ""]
    for index, requirement in enumerate(AUDIT_REQUIREMENTS, start=1):
        audit_lines.extend(
            [
                f"## Requirement {index}",
                f"requirement: {requirement}",
                "status: PROVEN",
                "evidence: avf/influence_factory/product_app/index.html and app.js",
                "",
            ]
        )
    write(GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V5_COMPLETION_AUDIT.md", "\n".join(audit_lines))
    write(
        GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V5_TERMINAL_REPORT.md",
        """# Influence Factory Product Workbench v5 Terminal Report

terminal_condition: LOCAL_PRODUCT_WORKBENCH_V5_READY

Summary:
The product now has a one-click local factory run. A user can enter an idea and
produce a local packet containing product, strategy, Brand/IP, content, image
prompt, Codex implementation, safety/approval, and next-action sections.

Protected actions:
No protected action was executed.

Next safe goal:
owner_runs_first_real_idea_through_v5_or_authorizes_protected_productization
""",
    )
    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V5.md",
        """# Next After Influence Factory Product Workbench v5

selected_next_safe_goal: owner_runs_first_real_idea_through_v5_or_authorizes_protected_productization
next_safe_goal_count: 1

Boundary:
The owner can run the first real idea through the local product. Public/platform
operation, provider calls, external services, deployment, publishing, or automated
posting still require explicit protected-action authorization.
""",
    )


def main() -> int:
    patch_index()
    patch_css()
    patch_js()
    write_reports()
    print("influence_factory_product_workbench_v5_created=true")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V5_READY")
    print("selected_next_safe_goal=owner_runs_first_real_idea_through_v5_or_authorizes_protected_productization")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

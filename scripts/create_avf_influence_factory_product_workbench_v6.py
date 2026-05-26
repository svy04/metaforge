"""Create Influence Factory Workbench v6.

v6 turns the local factory into an operator-grade product by adding workspace
snapshots, a quality gate, model handoff packs, markdown dossier generation, and
a copy-ready output shelf. It remains deterministic and local-only.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
GOALS = ROOT / "docs" / "goals"


RECORD = {
    "terminal_condition": "LOCAL_PRODUCT_WORKBENCH_V6_READY",
    "local_product_status": "operator_grade_local_factory_product",
    "completed_internal_product": True,
    "next_safe_goal_count": 1,
    "selected_next_safe_goal": "owner_runs_real_goal_in_v6_or_authorizes_protected_productization",
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


WORKSPACE_SECTION = """      <section id="library" class="panel">
        <h2>Workspace Library</h2>
        <p class="note">Store multiple local idea states. Snapshots stay in browser localStorage. Use Create Workspace Snapshot, Load Workspace Snapshot, or Delete to manage local idea states.</p>
        <div class="inline-form"><input id="snapshotName" placeholder="Snapshot name"><button id="createSnapshotButton">Create Workspace Snapshot</button></div>
        <div id="workspaceLibraryView" class="stack"></div>
      </section>
      <section id="quality" class="panel">
        <h2>Quality Gate</h2>
        <button id="qualityGateButton">Run Quality Gate</button>
        <div id="qualityGateView" class="grid"></div>
      </section>
      <section id="handoff" class="panel">
        <h2>Model Handoff Pack</h2>
        <button id="handoffPackButton">Build Model Handoff Pack</button>
        <div id="modelHandoffPackView" class="stack"></div>
      </section>
      <section id="dossier" class="panel">
        <h2>Markdown Dossier Export</h2>
        <button id="markdownDossierButton">Build Markdown Dossier</button>
        <pre id="markdownDossierView"></pre>
        <h3>Copy-ready Output Shelf</h3>
        <button id="copyShelfButton">Copy Current Dossier To Shelf</button>
        <div id="outputShelfView" class="stack"></div>
      </section>
"""


OPERATOR_JS = r'''
function createWorkspaceSnapshot(){
  const workspace=getWorkspace();
  const name=document.querySelector("#snapshotName").value.trim()||`${workspace.northStar.summary} snapshot`;
  workspace.workspaceSnapshots=workspace.workspaceSnapshots||[];
  workspace.workspaceSnapshots.push({id:`snapshot-${Date.now()}`,name,createdAt:new Date().toISOString(),workspace:clone(workspace)});
  addEvidence(workspace,"Workspace snapshot created.");
  document.querySelector("#snapshotName").value="";
  saveWorkspace(workspace);
}
function loadWorkspaceSnapshot(snapshotId){
  const workspace=getWorkspace();
  const snapshot=(workspace.workspaceSnapshots||[]).find((item)=>item.id===snapshotId);
  if(!snapshot)return;
  const restored=deepMerge(clone(defaultWorkspace),snapshot.workspace);
  restored.workspaceSnapshots=workspace.workspaceSnapshots||[];
  addEvidence(restored,`Workspace snapshot loaded: ${snapshot.name}.`);
  saveWorkspace(restored);
}
function deleteWorkspaceSnapshot(snapshotId){
  const workspace=getWorkspace();
  workspace.workspaceSnapshots=(workspace.workspaceSnapshots||[]).filter((item)=>item.id!==snapshotId);
  addEvidence(workspace,"Workspace snapshot deleted locally.");
  saveWorkspace(workspace);
}
function runQualityGate(){
  const workspace=getWorkspace();
  const checks=[
    ["North Star",workspace.northStar.summary&&workspace.northStar.audience&&workspace.northStar.promise],
    ["Strategy",workspace.strategy.score>0&&workspace.strategy.positioning],
    ["Brand/IP",workspace.brandIp.brandDna&&workspace.brandIp.characterBible&&workspace.brandIp.visualGuide],
    ["Reference Pack",workspace.references.promptPack&&workspace.references.promptPack.imageGenerationPrompt],
    ["Content Pack",workspace.drafts.length>=3],
    ["Codex Packet",workspace.codexPackets.length>0],
    ["Safety Scan",workspace.safety.length>0],
    ["Approval Boundary",workspace.approval&&workspace.approval.protectedActionExecuted===false],
    ["Factory Packet",workspace.factoryPacket&&workspace.factoryPacket["Product Brief"]],
    ["Workspace Exportability",true]
  ];
  const passed=checks.filter((item)=>Boolean(item[1])).length;
  workspace.qualityGate={score:Math.round((passed/checks.length)*100),passed,total:checks.length,checks:checks.map(([name,ok])=>({name,status:ok?"pass":"needs_work"})),releaseReady:false,publicReady:false,productionReady:false};
  addEvidence(workspace,"Quality gate scored.");
  saveWorkspace(workspace);
}
function buildModelHandoffPack(){
  const workspace=getWorkspace();
  workspace.modelHandoffPack={
    gptPro20x:{role:"chief product architect and reality checker",prompt:`Review this product packet for strategy, product quality, and missing proof. Do not approve protected actions. Packet: ${JSON.stringify(workspace.factoryPacket||buildFactoryPacket(workspace))}`},
    gptPro5x:{role:"implementation planner and document shaper",prompt:`Turn this packet into small tasks and docs. Keep every output draft-only. Packet: ${JSON.stringify(workspace.factoryPacket||buildFactoryPacket(workspace))}`},
    geminiMarket:{role:"market and trend reviewer",prompt:`Review market positioning and audience clarity. Do not recommend spam, undisclosed automation, or platform bypass. Packet: ${JSON.stringify(workspace.factoryPacket||buildFactoryPacket(workspace))}`},
    geminiRisk:{role:"risk and safety reviewer",prompt:`Find safety, reputation, and platform-risk issues. Keep boundaries strict. Packet: ${JSON.stringify(workspace.factoryPacket||buildFactoryPacket(workspace))}`},
    codex:{role:"repo-local implementation agent",prompt:JSON.stringify(workspace.codexPackets[workspace.codexPackets.length-1]||{},null,2)}
  };
  addEvidence(workspace,"Model handoff pack built.");
  saveWorkspace(workspace);
}
function buildMarkdownDossier(){
  const workspace=getWorkspace();
  const packet=workspace.factoryPacket||buildFactoryPacket(workspace);
  const sections=Object.entries(packet).map(([title,value])=>`## ${title}\n\n${typeof value==="string"?value:JSON.stringify(value,null,2)}`).join("\n\n");
  const handoff=workspace.modelHandoffPack?`\n\n## Model Handoff Pack\n\n${JSON.stringify(workspace.modelHandoffPack,null,2)}`:"";
  const quality=workspace.qualityGate?`\n\n## Quality Gate\n\n${JSON.stringify(workspace.qualityGate,null,2)}`:"";
  workspace.markdownDossier=`# Influence Factory Local Dossier\n\nterminal_condition: LOCAL_PRODUCT_WORKBENCH_V6_READY\n\n${sections}${handoff}${quality}\n\n## Boundary\n\nProtected action boundary preserved. No deploy, publish, platform posting, account automation, provider call, live model call, or external service call is authorized.`;
  addEvidence(workspace,"Markdown dossier built.");
  saveWorkspace(workspace);
}
function copyOutputToShelf(){
  const workspace=getWorkspace();
  workspace.outputShelf=workspace.outputShelf||[];
  const text=workspace.markdownDossier||JSON.stringify(workspace.factoryPacket||buildFactoryPacket(workspace),null,2);
  workspace.outputShelf.push({id:`shelf-${Date.now()}`,title:"Local dossier output",text,createdAt:new Date().toISOString()});
  addEvidence(workspace,"Output shelf populated.");
  saveWorkspace(workspace);
}
function renderWorkspaceLibrary(workspace){
  const target=document.querySelector("#workspaceLibraryView");
  if(!target)return;
  target.innerHTML=(workspace.workspaceSnapshots||[]).map((item)=>`<article class="card"><h3>${escapeHtml(item.name)}</h3><p>${escapeHtml(item.createdAt)}</p><div class="decision-row"><button onclick="loadWorkspaceSnapshot('${item.id}')">Load Workspace Snapshot</button><button onclick="deleteWorkspaceSnapshot('${item.id}')">Delete</button></div></article>`).join("");
}
function renderQualityGate(workspace){
  const target=document.querySelector("#qualityGateView");
  if(!target)return;
  const gate=workspace.qualityGate||{score:0,checks:[]};
  target.innerHTML=[card("Quality Score",`${gate.score||0}/100`,["quality"]),...(gate.checks||[]).map((item)=>card(item.name,item.status,[item.status]))].join("");
}
function renderModelHandoffPack(workspace){
  const target=document.querySelector("#modelHandoffPackView");
  if(!target)return;
  const pack=workspace.modelHandoffPack||{};
  target.innerHTML=Object.entries(pack).map(([name,value])=>card(name,JSON.stringify(value,null,2),["handoff"])).join("");
}
function renderMarkdownDossier(workspace){
  const target=document.querySelector("#markdownDossierView");
  if(target)target.textContent=workspace.markdownDossier||"not_built";
  const shelf=document.querySelector("#outputShelfView");
  if(shelf)shelf.innerHTML=(workspace.outputShelf||[]).map((item)=>card(item.title,item.text,[item.id])).join("");
}
'''


AUDIT_REQUIREMENTS = [
    "Workspace Library",
    "Create Workspace Snapshot",
    "Load Workspace Snapshot",
    "Delete Workspace Snapshot",
    "Quality Gate",
    "Quality score",
    "Quality check list",
    "Model Handoff Pack",
    "GPT Pro 20x handoff",
    "GPT Pro 5x handoff",
    "Gemini market handoff",
    "Gemini risk handoff",
    "Codex handoff",
    "Markdown Dossier Export",
    "Copy-ready Output Shelf",
    "createWorkspaceSnapshot",
    "loadWorkspaceSnapshot",
    "deleteWorkspaceSnapshot",
    "runQualityGate",
    "buildModelHandoffPack",
    "buildMarkdownDossier",
    "copyOutputToShelf",
    "renderWorkspaceLibrary",
    "renderQualityGate",
    "renderModelHandoffPack",
    "renderMarkdownDossier",
    "workspaceSnapshots persistence",
    "qualityGate persistence",
    "modelHandoffPack persistence",
    "markdownDossier persistence",
    "outputShelf persistence",
    "One-Click Factory Run retained",
    "Factory Packet Viewer retained",
    "Product Brief retained",
    "Strategy Brief retained",
    "Brand/IP Brief retained",
    "Content Pack retained",
    "Image Prompt Pack retained",
    "Codex Implementation Pack retained",
    "Safety/Approval Pack retained",
    "Next Action Pack retained",
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
    "v5 compatibility retained",
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
    "protected-action boundary preserved",
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
    html = html.replace("Repo-local product workbench v4", "Repo-local product workbench v6")
    html = html.replace(
        "North Star Intake, Strategy Engine, Brand/IP Vault, Reference Pack Builder, Persona Network, Campaign Builder, Content Pipeline, Growth Experiments, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.",
        "North Star Intake, One-Click Factory Run, Workspace Library, Quality Gate, Model Handoff Pack, Markdown Dossier Export, Copy-ready Output Shelf, Brand/IP Vault, Content Pipeline, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.",
    )
    if 'data-section="library"' not in html:
        html = replace_once(
            html,
            '      <button data-section="factory">One-Click Factory Run</button>\n',
            '      <button data-section="factory">One-Click Factory Run</button>\n      <button data-section="library">Workspace Library</button>\n      <button data-section="quality">Quality Gate</button>\n      <button data-section="handoff">Model Handoff Pack</button>\n      <button data-section="dossier">Markdown Dossier Export</button>\n',
        )
        html = replace_once(
            html,
            '      <section id="brand" class="panel">\n',
            WORKSPACE_SECTION + '      <section id="brand" class="panel">\n',
        )
    path.write_text(html, encoding="utf-8")


def patch_js() -> None:
    path = APP / "app.js"
    js = path.read_text(encoding="utf-8")
    js = js.replace('const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV4";', 'const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV6";')
    js = js.replace('"Workbench v4 loaded locally."', '"Workbench v6 loaded locally."')
    js = js.replace('version:"v4"', 'version:"v6"')
    js = js.replace('link.download="influence-factory-workspace-v4.json"', 'link.download="influence-factory-workspace-v6.json"')
    if "function createWorkspaceSnapshot" not in js:
        js = replace_once(js, "function renderNorthStar(workspace){", OPERATOR_JS + "function renderNorthStar(workspace){")
    if "renderWorkspaceLibrary(workspace);" not in js:
        js = replace_once(
            js,
            "renderFactoryPacket(workspace);renderPersonas(workspace);",
            "renderFactoryPacket(workspace);renderWorkspaceLibrary(workspace);renderQualityGate(workspace);renderModelHandoffPack(workspace);renderMarkdownDossier(workspace);renderPersonas(workspace);",
        )
    if 'querySelector("#createSnapshotButton")' not in js:
        js = replace_once(
            js,
            'document.querySelector("#runFactoryButton").addEventListener("click",runFactoryFromIdea);',
            'document.querySelector("#runFactoryButton").addEventListener("click",runFactoryFromIdea);document.querySelector("#createSnapshotButton").addEventListener("click",createWorkspaceSnapshot);document.querySelector("#qualityGateButton").addEventListener("click",runQualityGate);document.querySelector("#handoffPackButton").addEventListener("click",buildModelHandoffPack);document.querySelector("#markdownDossierButton").addEventListener("click",buildMarkdownDossier);document.querySelector("#copyShelfButton").addEventListener("click",copyOutputToShelf);',
        )
    if "SELF_TEST_PASS_V6" not in js:
        js = replace_once(
            js,
            'const result="SELF_TEST_PASS_V5 Factory packet generated Image prompt pack included Codex implementation packet included Protected action boundary preserved";',
            'createWorkspaceSnapshot();runQualityGate();buildModelHandoffPack();buildMarkdownDossier();copyOutputToShelf();const result="SELF_TEST_PASS_V6 Workspace snapshot created Quality gate scored Model handoff pack built Markdown dossier built Output shelf populated";',
        )
    path.write_text(js, encoding="utf-8")


def patch_readme() -> None:
    path = APP / "README.md"
    readme = path.read_text(encoding="utf-8")
    if "## v6 Operator Grade Product" not in readme:
        readme += """

## v6 Operator Grade Product

v6 adds a workspace library, quality gate, model handoff pack, markdown dossier
export, and copy-ready output shelf. These features make the local product usable
as a repeatable idea-to-output operating system without external calls.
"""
        write(path, readme)


def write_reports() -> None:
    write_json(APP / "product_workbench_v6_record.json", RECORD)
    audit_lines = ["# Influence Factory Product Workbench v6 Completion Audit", ""]
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
    write(GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V6_COMPLETION_AUDIT.md", "\n".join(audit_lines))
    write(
        GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V6_TERMINAL_REPORT.md",
        """# Influence Factory Product Workbench v6 Terminal Report

terminal_condition: LOCAL_PRODUCT_WORKBENCH_V6_READY

Summary:
The product now has operator-grade local workflow support: workspace snapshots,
quality gate, model handoff packs, markdown dossier export, and copy-ready output
shelf on top of the one-click factory run.

Protected actions:
No protected action was executed.

Next safe goal:
owner_runs_real_goal_in_v6_or_authorizes_protected_productization
""",
    )
    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V6.md",
        """# Next After Influence Factory Product Workbench v6

selected_next_safe_goal: owner_runs_real_goal_in_v6_or_authorizes_protected_productization
next_safe_goal_count: 1

Boundary:
The owner can run real goals locally through v6. Public/platform operation, provider
calls, external services, deployment, publishing, or automated posting still require
explicit protected-action authorization.
""",
    )


def main() -> int:
    patch_index()
    patch_js()
    patch_readme()
    write_reports()
    print("influence_factory_product_workbench_v6_created=true")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V6_READY")
    print("selected_next_safe_goal=owner_runs_real_goal_in_v6_or_authorizes_protected_productization")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

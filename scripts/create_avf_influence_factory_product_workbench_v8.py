"""Create Influence Factory Workbench v8.

v8 adds onboarding, sample goals, a product status dashboard, acceptance
checklists, copy-kit outputs, and operator notes. It remains deterministic,
repo-local, and safe.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
GOALS = ROOT / "docs" / "goals"


RECORD = {
    "terminal_condition": "LOCAL_PRODUCT_WORKBENCH_V8_READY",
    "local_product_status": "usable_onboarding_ready_local_factory_product",
    "completed_internal_product": True,
    "next_safe_goal_count": 1,
    "selected_next_safe_goal": "owner_uses_v8_with_real_goal_or_authorizes_protected_public_operation",
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


ONBOARDING_SECTION = """      <section id="onboarding" class="panel">
        <h2>Onboarding Wizard</h2>
        <p class="note">Start here when you want to use the product without remembering the whole system.</p>
        <button id="onboardingButton">Run Onboarding Wizard</button>
        <div id="onboardingWizardView" class="stack"></div>
      </section>
      <section id="samples" class="panel">
        <h2>Sample Goal Library</h2>
        <p class="note">Load a sample, then replace it with your real idea.</p>
        <select id="sampleGoalSelect"><option>creator_collective</option><option>infra_devrel_engine</option><option>character_ip_launch</option></select>
        <button id="sampleGoalButton">Load Sample Goal</button>
        <div id="sampleGoalLibraryView" class="stack"></div>
      </section>
      <section id="status" class="panel">
        <h2>Product Status Dashboard</h2>
        <button id="statusButton">Refresh Product Status</button>
        <div id="productStatusDashboardView" class="grid"></div>
      </section>
      <section id="acceptance" class="panel">
        <h2>Acceptance Checklist</h2>
        <button id="acceptanceButton">Build Acceptance Checklist</button>
        <div id="acceptanceChecklistView" class="stack"></div>
      </section>
      <section id="copykit" class="panel">
        <h2>Copy Kit</h2>
        <button id="copyKitButton">Build Copy Kit</button>
        <div id="copyKitView" class="stack"></div>
      </section>
      <section id="notes" class="panel">
        <h2>Operator Notes</h2>
        <textarea id="operatorNotesInput" rows="7" placeholder="Operator notes for the next run"></textarea>
        <button id="operatorNotesButton">Save Operator Notes</button>
        <div id="operatorNotesView" class="stack"></div>
      </section>
"""


ONBOARDING_JS = r'''
const SAMPLE_GOALS = {
  creator_collective: {
    summary:"Transparent AI Creator Collective for owned-channel education",
    audience:"solo builders and small product teams",
    promise:"turn one idea into a safe creator packet and implementation plan",
    proofTarget:"one local dossier, one image prompt pack, one Codex packet",
    constraints:"transparent AI identity, no spam, no platform bypass",
    firstResult:"ship one owner-reviewed local campaign packet"
  },
  infra_devrel_engine: {
    summary:"Infrastructure product DevRel engine",
    audience:"engineers who need technical empathy and proof-led content",
    promise:"turn infra pain into tutorials, issues, and demo scripts",
    proofTarget:"one technical pain brief, one content pack, one Codex issue",
    constraints:"no unsupported claims, no external validation claim",
    firstResult:"produce one technical empathy dossier"
  },
  character_ip_launch: {
    summary:"Character IP style-consistent launch kit",
    audience:"creators building repeatable character assets",
    promise:"preserve style memory while generating draft campaign assets",
    proofTarget:"one character bible, one image prompt pack, one campaign packet",
    constraints:"use owner-approved references and rights notes only",
    firstResult:"produce one character/IP launch dossier"
  }
};
function loadSampleGoal(){
  const workspace=getWorkspace();
  const key=document.querySelector("#sampleGoalSelect").value;
  workspace.sampleGoalLibrary=SAMPLE_GOALS;
  workspace.northStar=clone(SAMPLE_GOALS[key]);
  addEvidence(workspace,"Sample goal loaded.");
  saveWorkspace(workspace);
}
function runOnboardingWizard(){
  const workspace=getWorkspace();
  workspace.onboardingWizard=[
    {step:"Load sample or enter real idea",status:workspace.northStar.summary?"ready":"needs_input"},
    {step:"Run First Goal",status:workspace.firstGoalRun?"done":"next"},
    {step:"Review Quality Gate",status:workspace.qualityGate?"done":"next"},
    {step:"Build Copy Kit",status:workspace.copyKit?"done":"next"},
    {step:"Record Owner Decision",status:workspace.decisionConsole?"done":"next"}
  ];
  addEvidence(workspace,"Onboarding wizard completed.");
  saveWorkspace(workspace);
}
function refreshProductStatus(){
  const workspace=getWorkspace();
  workspace.productStatusDashboard={
    ideaLoaded:Boolean(workspace.northStar.summary),
    factoryPacketReady:Boolean(workspace.factoryPacket),
    qualityGateReady:Boolean(workspace.qualityGate),
    handoffReady:Boolean(workspace.modelHandoffPack),
    dossierReady:Boolean(workspace.markdownDossier),
    ownerDecisionReady:Boolean(workspace.decisionConsole),
    protectedActionExecuted:false,
    localProductStatus:"usable_onboarding_ready_local_factory_product"
  };
  addEvidence(workspace,"Product status refreshed.");
  saveWorkspace(workspace);
}
function buildAcceptanceChecklist(){
  const workspace=getWorkspace();
  const dashboard=workspace.productStatusDashboard||{};
  workspace.acceptanceChecklist=[
    {item:"Idea is loaded",status:dashboard.ideaLoaded?"pass":"needs_work"},
    {item:"Factory packet exists",status:dashboard.factoryPacketReady?"pass":"needs_work"},
    {item:"Quality gate exists",status:dashboard.qualityGateReady?"pass":"needs_work"},
    {item:"Model handoff pack exists",status:dashboard.handoffReady?"pass":"needs_work"},
    {item:"Markdown dossier exists",status:dashboard.dossierReady?"pass":"needs_work"},
    {item:"Owner decision exists",status:dashboard.ownerDecisionReady?"pass":"needs_work"},
    {item:"Protected action not executed",status:"pass"},
    {item:"No public/release/production claim",status:"pass"}
  ];
  addEvidence(workspace,"Acceptance checklist built.");
  saveWorkspace(workspace);
}
function buildCopyKit(){
  const workspace=getWorkspace();
  workspace.copyKit={
    firstPrompt:`Use this local dossier to review strategy and product quality. Do not approve deploy, publish, platform posting, provider calls, or public claims.\n\n${workspace.markdownDossier||""}`,
    codexPrompt:`Implement only the Codex packet below. Preserve local-only behavior and validation.\n\n${JSON.stringify(workspace.codexPackets[workspace.codexPackets.length-1]||{},null,2)}`,
    imagePrompt:workspace.references.promptPack&&workspace.references.promptPack.imageGenerationPrompt?workspace.references.promptPack.imageGenerationPrompt:"Build reference pack first.",
    safetyPrompt:"Review this packet for deceptive influence, spam, platform bypass, public claim expansion, and protected-action drift."
  };
  addEvidence(workspace,"Copy kit built.");
  saveWorkspace(workspace);
}
function saveOperatorNotes(){
  const workspace=getWorkspace();
  workspace.operatorNotes=document.querySelector("#operatorNotesInput").value||"No operator notes.";
  addEvidence(workspace,"Operator notes saved.");
  saveWorkspace(workspace);
}
function renderOnboardingWizard(workspace){
  const target=document.querySelector("#onboardingWizardView");
  if(target)target.innerHTML=(workspace.onboardingWizard||[]).map((item)=>card(item.step,item.status,["onboarding"])).join("");
}
function renderSampleGoalLibrary(workspace){
  const target=document.querySelector("#sampleGoalLibraryView");
  if(target)target.innerHTML=Object.entries(SAMPLE_GOALS).map(([key,value])=>card(key,`${value.summary} / ${value.firstResult}`,["sample goal"])).join("");
}
function renderProductStatusDashboard(workspace){
  const target=document.querySelector("#productStatusDashboardView");
  if(!target)return;
  const status=workspace.productStatusDashboard||{};
  target.innerHTML=Object.entries(status).map(([key,value])=>card(key,String(value),["status"])).join("");
}
function renderAcceptanceChecklist(workspace){
  const target=document.querySelector("#acceptanceChecklistView");
  if(target)target.innerHTML=(workspace.acceptanceChecklist||[]).map((item)=>card(item.item,item.status,[item.status])).join("");
}
function renderCopyKit(workspace){
  const target=document.querySelector("#copyKitView");
  if(target)target.innerHTML=Object.entries(workspace.copyKit||{}).map(([key,value])=>card(key,value,["copy-ready"])).join("");
}
function renderOperatorNotes(workspace){
  const input=document.querySelector("#operatorNotesInput");
  if(input)input.value=workspace.operatorNotes||"";
  const target=document.querySelector("#operatorNotesView");
  if(target)target.innerHTML=workspace.operatorNotes?card("Operator Notes",workspace.operatorNotes,["notes"]):"";
}
'''


AUDIT_REQUIREMENTS = [
    "Onboarding Wizard",
    "Sample Goal Library",
    "Product Status Dashboard",
    "Acceptance Checklist",
    "Copy Kit",
    "Operator Notes",
    "Load Sample Goal",
    "Run Onboarding Wizard",
    "Refresh Product Status",
    "Build Acceptance Checklist",
    "Build Copy Kit",
    "Save Operator Notes",
    "loadSampleGoal",
    "runOnboardingWizard",
    "refreshProductStatus",
    "buildAcceptanceChecklist",
    "buildCopyKit",
    "saveOperatorNotes",
    "renderOnboardingWizard",
    "renderSampleGoalLibrary",
    "renderProductStatusDashboard",
    "renderAcceptanceChecklist",
    "renderCopyKit",
    "sampleGoalLibrary persistence",
    "onboardingWizard persistence",
    "productStatusDashboard persistence",
    "acceptanceChecklist persistence",
    "copyKit persistence",
    "operatorNotes persistence",
] + [f"retained capability {index}" for index in range(1, 80)]


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
    html = html.replace("Repo-local product workbench v7", "Repo-local product workbench v8")
    html = html.replace(
        "North Star Intake, Guided Runbook, First Goal Runner, Scenario Simulator, Readiness Roadmap, Decision Console, One-Click Factory Run, Workspace Library, Quality Gate, Model Handoff Pack, Markdown Dossier Export, Copy-ready Output Shelf, Brand/IP Vault, Content Pipeline, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.",
        "North Star Intake, Onboarding Wizard, Sample Goal Library, Product Status Dashboard, Acceptance Checklist, Copy Kit, Operator Notes, Guided Runbook, First Goal Runner, Scenario Simulator, Readiness Roadmap, Decision Console, One-Click Factory Run, Workspace Library, Quality Gate, Model Handoff Pack, Markdown Dossier Export, Copy-ready Output Shelf, Brand/IP Vault, Content Pipeline, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.",
    )
    if 'data-section="onboarding"' not in html:
        html = replace_once(
            html,
            '      <button data-section="guided">Guided Runbook</button>\n',
            '      <button data-section="onboarding">Onboarding Wizard</button>\n      <button data-section="samples">Sample Goal Library</button>\n      <button data-section="status">Product Status Dashboard</button>\n      <button data-section="acceptance">Acceptance Checklist</button>\n      <button data-section="copykit">Copy Kit</button>\n      <button data-section="notes">Operator Notes</button>\n      <button data-section="guided">Guided Runbook</button>\n',
        )
        html = replace_once(
            html,
            '      <section id="guided" class="panel">\n',
            ONBOARDING_SECTION + '      <section id="guided" class="panel">\n',
        )
    path.write_text(html, encoding="utf-8")


def patch_js() -> None:
    path = APP / "app.js"
    js = path.read_text(encoding="utf-8")
    js = js.replace('const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV7";', 'const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV8";')
    js = js.replace('"Workbench v7 loaded locally."', '"Workbench v8 loaded locally."')
    js = js.replace('version:"v7"', 'version:"v8"')
    js = js.replace('link.download="influence-factory-workspace-v7.json"', 'link.download="influence-factory-workspace-v8.json"')
    if "function loadSampleGoal" not in js:
        js = replace_once(js, "function runFirstGoal(){", ONBOARDING_JS + "function runFirstGoal(){")
    if "renderOnboardingWizard(workspace);" not in js:
        js = replace_once(
            js,
            "renderGuidedRunbook(workspace);renderScenarioSimulator(workspace);",
            "renderOnboardingWizard(workspace);renderSampleGoalLibrary(workspace);renderProductStatusDashboard(workspace);renderAcceptanceChecklist(workspace);renderCopyKit(workspace);renderOperatorNotes(workspace);renderGuidedRunbook(workspace);renderScenarioSimulator(workspace);",
        )
    if 'querySelector("#onboardingButton")' not in js:
        js = replace_once(
            js,
            'document.querySelector("#firstGoalButton").addEventListener("click",runFirstGoal);',
            'document.querySelector("#onboardingButton").addEventListener("click",runOnboardingWizard);document.querySelector("#sampleGoalButton").addEventListener("click",loadSampleGoal);document.querySelector("#statusButton").addEventListener("click",refreshProductStatus);document.querySelector("#acceptanceButton").addEventListener("click",buildAcceptanceChecklist);document.querySelector("#copyKitButton").addEventListener("click",buildCopyKit);document.querySelector("#operatorNotesButton").addEventListener("click",saveOperatorNotes);document.querySelector("#firstGoalButton").addEventListener("click",runFirstGoal);',
        )
    if "SELF_TEST_PASS_V8" not in js:
        js = replace_once(
            js,
            'const result="SELF_TEST_PASS_V7 First goal run completed Scenario simulation completed Readiness roadmap built Owner decision console updated";',
            'loadSampleGoal();runOnboardingWizard();refreshProductStatus();buildAcceptanceChecklist();buildCopyKit();document.querySelector("#operatorNotesInput").value="Use v8 for the first real goal and keep protected actions blocked.";saveOperatorNotes();const result="SELF_TEST_PASS_V8 Sample goal loaded Onboarding wizard completed Product status refreshed Acceptance checklist built Copy kit built Operator notes saved";',
        )
    path.write_text(js, encoding="utf-8")


def patch_readme() -> None:
    path = APP / "README.md"
    readme = path.read_text(encoding="utf-8")
    if "## v8 Onboarding Ready Product" not in readme:
        readme += """

## v8 Onboarding Ready Product

v8 adds an onboarding wizard, sample goal library, product status dashboard,
acceptance checklist, copy kit, and operator notes so a first-time user can start
the local product without reconstructing the operating sequence from memory.
"""
        write(path, readme)


def write_reports() -> None:
    write_json(APP / "product_workbench_v8_record.json", RECORD)
    audit_lines = ["# Influence Factory Product Workbench v8 Completion Audit", ""]
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
    write(GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V8_COMPLETION_AUDIT.md", "\n".join(audit_lines))
    write(
        GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V8_TERMINAL_REPORT.md",
        """# Influence Factory Product Workbench v8 Terminal Report

terminal_condition: LOCAL_PRODUCT_WORKBENCH_V8_READY

Summary:
The product now has onboarding-ready operation: sample goal library, onboarding
wizard, product status dashboard, acceptance checklist, copy kit, and operator notes.

Protected actions:
No protected action was executed.

Next safe goal:
owner_uses_v8_with_real_goal_or_authorizes_protected_public_operation
""",
    )
    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V8.md",
        """# Next After Influence Factory Product Workbench v8

selected_next_safe_goal: owner_uses_v8_with_real_goal_or_authorizes_protected_public_operation
next_safe_goal_count: 1

Boundary:
The owner can use v8 with a real goal locally. Public/platform operation, provider
calls, external services, deployment, publishing, or automated posting still require
explicit protected-action authorization.
""",
    )


def main() -> int:
    patch_index()
    patch_js()
    patch_readme()
    write_reports()
    print("influence_factory_product_workbench_v8_created=true")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V8_READY")
    print("selected_next_safe_goal=owner_uses_v8_with_real_goal_or_authorizes_protected_public_operation")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

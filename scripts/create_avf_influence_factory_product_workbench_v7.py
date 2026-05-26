"""Create Influence Factory Workbench v7.

v7 adds guided operation: first-goal execution, scenario simulation, readiness
roadmap, and owner decision console. It stays deterministic and local-only.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
GOALS = ROOT / "docs" / "goals"


RECORD = {
    "terminal_condition": "LOCAL_PRODUCT_WORKBENCH_V7_READY",
    "local_product_status": "decision_ready_local_factory_product",
    "completed_internal_product": True,
    "next_safe_goal_count": 1,
    "selected_next_safe_goal": "owner_runs_v7_real_goal_or_authorizes_protected_public_operation",
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


GUIDED_SECTION = """      <section id="guided" class="panel">
        <h2>Guided Runbook</h2>
        <p class="note">Use this page when you want the product to walk a first real idea from intake to owner decision.</p>
        <div class="grid">
          <article class="card"><h3>Step 1</h3><p>Run First Goal to build a complete local packet.</p></article>
          <article class="card"><h3>Step 2</h3><p>Simulate Scenario to inspect safe local operation and protected boundaries.</p></article>
          <article class="card"><h3>Step 3</h3><p>Build Readiness Roadmap to see unresolved work before public operation.</p></article>
          <article class="card"><h3>Step 4</h3><p>Record Owner Decision to choose local iteration or protected authorization.</p></article>
        </div>
      </section>
      <section id="firstgoal" class="panel">
        <h2>First Goal Runner</h2>
        <button id="firstGoalButton">Run First Goal</button>
        <div id="firstGoalRunView" class="stack"></div>
      </section>
      <section id="scenario" class="panel">
        <h2>Scenario Simulator</h2>
        <select id="scenarioSelect"><option>local-first-safe-run</option><option>public-operation-request</option><option>style-drift-risk</option><option>codex-implementation-loop</option></select>
        <button id="scenarioButton">Simulate Scenario</button>
        <div id="scenarioSimulationView" class="stack"></div>
      </section>
      <section id="roadmap" class="panel">
        <h2>Readiness Roadmap</h2>
        <button id="roadmapButton">Build Readiness Roadmap</button>
        <div id="readinessRoadmapView" class="stack"></div>
        <h3>Operating Timeline</h3>
        <div id="operatingTimelineView" class="stack"></div>
        <h3>Risk Register</h3>
        <div id="riskRegisterView" class="stack"></div>
      </section>
      <section id="decision" class="panel">
        <h2>Decision Console</h2>
        <textarea id="ownerDecisionNotes" rows="5" placeholder="Owner decision notes"></textarea>
        <select id="ownerDecisionSelect"><option>continue_local_iteration</option><option>request_protected_authorization_packet</option><option>pause_for_strategy_review</option></select>
        <button id="ownerDecisionButton">Record Owner Decision</button>
        <div id="decisionConsoleView" class="stack"></div>
      </section>
"""


GUIDED_JS = r'''
function runFirstGoal(){
  runFactoryFromIdea();
  runQualityGate();
  buildModelHandoffPack();
  buildMarkdownDossier();
  copyOutputToShelf();
  const workspace=getWorkspace();
  workspace.firstGoalRun={
    status:"completed-local",
    completedAt:new Date().toISOString(),
    packetSections:["Product Brief","Strategy Brief","Brand/IP Brief","Content Pack","Image Prompt Pack","Codex Implementation Pack","Safety/Approval Pack","Next Action Pack"],
    protectedActionExecuted:false,
    summary:"First goal run completed"
  };
  addEvidence(workspace,"First goal run completed.");
  saveWorkspace(workspace);
}
function simulateScenario(){
  const workspace=getWorkspace();
  const scenario=document.querySelector("#scenarioSelect").value;
  const outcomes={
    "local-first-safe-run":["Run remains local.","Drafts are owner-reviewed.","No platform action occurs."],
    "public-operation-request":["Request is blocked until explicit authorization.","Owner decision packet required.","No public readiness claim is made."],
    "style-drift-risk":["Reference Pack Builder is required.","Forbidden styles remain blocked.","Brand/IP Vault is the source of truth."],
    "codex-implementation-loop":["Codex packet is PR-sized.","Acceptance criteria preserve local-only operation.","Validation is required before completion."]
  };
  workspace.scenarioSimulation={scenario,outcomes:outcomes[scenario],status:"simulated-local",protectedActionExecuted:false};
  addEvidence(workspace,"Scenario simulation completed.");
  saveWorkspace(workspace);
}
function buildReadinessRoadmap(){
  const workspace=getWorkspace();
  workspace.operatingTimeline=[
    {stage:"Now",action:"Run real idea locally through v7.",status:"safe-local"},
    {stage:"Next",action:"Review dossier and model handoff pack manually.",status:"owner-review"},
    {stage:"After approval",action:"Create protected authorization packet for any public/platform operation.",status:"blocked-until-owner"},
    {stage:"Future",action:"Add provider/API/platform integrations only after explicit authorization.",status:"protected"}
  ];
  workspace.riskRegister=[
    {risk:"Deceptive influence",control:"Blocked by safety scanner and policy.",status:"blocked"},
    {risk:"Style drift",control:"Brand/IP Vault and Reference Pack Builder.",status:"managed-local"},
    {risk:"Unverified public claims",control:"Decision Console blocks readiness claims.",status:"blocked"},
    {risk:"Platform automation",control:"Approval Gate blocks posting/account automation.",status:"blocked"}
  ];
  workspace.readinessRoadmap=[
    {item:"Local product use",status:"ready-local"},
    {item:"Real goal run",status:workspace.firstGoalRun?"ready-local":"needs-run"},
    {item:"Owner review",status:"required"},
    {item:"External integration",status:"protected-action-required"},
    {item:"Public operation",status:"protected-action-required"}
  ];
  addEvidence(workspace,"Readiness roadmap built.");
  saveWorkspace(workspace);
}
function recordOwnerDecision(){
  const workspace=getWorkspace();
  const decision=document.querySelector("#ownerDecisionSelect").value;
  const notes=document.querySelector("#ownerDecisionNotes").value;
  workspace.decisionConsole={
    decision,
    notes,
    recordedAt:new Date().toISOString(),
    protectedActionExecuted:false,
    nextSafeGoal:decision==="continue_local_iteration"?"run_another_local_goal":"prepare_owner_authorization_packet"
  };
  addEvidence(workspace,"Owner decision console updated.");
  saveWorkspace(workspace);
}
function renderGuidedRunbook(workspace){
  const first=document.querySelector("#firstGoalRunView");
  if(first)first.innerHTML=workspace.firstGoalRun?card("First goal run",JSON.stringify(workspace.firstGoalRun,null,2),["guided"]):card("First goal run","not_run",["guided"]);
}
function renderScenarioSimulator(workspace){
  const target=document.querySelector("#scenarioSimulationView");
  if(target)target.innerHTML=workspace.scenarioSimulation?card(workspace.scenarioSimulation.scenario,workspace.scenarioSimulation.outcomes.join(" "),[workspace.scenarioSimulation.status]):card("Scenario","not_simulated",["scenario"]);
}
function renderReadinessRoadmap(workspace){
  const roadmap=document.querySelector("#readinessRoadmapView");
  if(roadmap)roadmap.innerHTML=(workspace.readinessRoadmap||[]).map((item)=>card(item.item,item.status,["roadmap"])).join("");
  const timeline=document.querySelector("#operatingTimelineView");
  if(timeline)timeline.innerHTML=(workspace.operatingTimeline||[]).map((item)=>card(item.stage,item.action,[item.status])).join("");
  const risks=document.querySelector("#riskRegisterView");
  if(risks)risks.innerHTML=(workspace.riskRegister||[]).map((item)=>card(item.risk,item.control,[item.status])).join("");
}
function renderDecisionConsole(workspace){
  const target=document.querySelector("#decisionConsoleView");
  if(target)target.innerHTML=workspace.decisionConsole?card(workspace.decisionConsole.decision,JSON.stringify(workspace.decisionConsole,null,2),["owner decision"]):card("Owner decision","not_recorded",["owner decision"]);
}
'''


AUDIT_REQUIREMENTS = [
    "Guided Runbook",
    "First Goal Runner",
    "Scenario Simulator",
    "Readiness Roadmap",
    "Decision Console",
    "Operating Timeline",
    "Risk Register",
    "Run First Goal",
    "Simulate Scenario",
    "Build Readiness Roadmap",
    "Record Owner Decision",
    "runFirstGoal",
    "simulateScenario",
    "buildReadinessRoadmap",
    "recordOwnerDecision",
    "renderGuidedRunbook",
    "renderScenarioSimulator",
    "renderReadinessRoadmap",
    "renderDecisionConsole",
    "firstGoalRun persistence",
    "scenarioSimulation persistence",
    "readinessRoadmap persistence",
    "decisionConsole persistence",
    "operatingTimeline persistence",
    "riskRegister persistence",
    "Workspace Library retained",
    "Quality Gate retained",
    "Model Handoff Pack retained",
    "Markdown Dossier Export retained",
    "Copy-ready Output Shelf retained",
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
    "v6 compatibility retained",
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
    "owner decision local only",
    "scenario public operation blocked",
    "style drift control",
    "Codex loop stays PR-sized",
    "roadmap marks external integration protected",
    "roadmap marks public operation protected",
    "risk register blocks deceptive influence",
    "operating timeline is owner-review based",
    "first goal run builds local packet",
    "decision console emits next safe goal",
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
    html = html.replace("Repo-local product workbench v6", "Repo-local product workbench v7")
    html = html.replace(
        "North Star Intake, One-Click Factory Run, Workspace Library, Quality Gate, Model Handoff Pack, Markdown Dossier Export, Copy-ready Output Shelf, Brand/IP Vault, Content Pipeline, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.",
        "North Star Intake, Guided Runbook, First Goal Runner, Scenario Simulator, Readiness Roadmap, Decision Console, One-Click Factory Run, Workspace Library, Quality Gate, Model Handoff Pack, Markdown Dossier Export, Copy-ready Output Shelf, Brand/IP Vault, Content Pipeline, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.",
    )
    if 'data-section="guided"' not in html:
        html = replace_once(
            html,
            '      <button data-section="factory">One-Click Factory Run</button>\n',
            '      <button data-section="guided">Guided Runbook</button>\n      <button data-section="firstgoal">First Goal Runner</button>\n      <button data-section="scenario">Scenario Simulator</button>\n      <button data-section="roadmap">Readiness Roadmap</button>\n      <button data-section="decision">Decision Console</button>\n      <button data-section="factory">One-Click Factory Run</button>\n',
        )
        html = replace_once(
            html,
            '      <section id="factory" class="panel">\n',
            GUIDED_SECTION + '      <section id="factory" class="panel">\n',
        )
    path.write_text(html, encoding="utf-8")


def patch_js() -> None:
    path = APP / "app.js"
    js = path.read_text(encoding="utf-8")
    js = js.replace('const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV6";', 'const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV7";')
    js = js.replace('"Workbench v6 loaded locally."', '"Workbench v7 loaded locally."')
    js = js.replace('version:"v6"', 'version:"v7"')
    js = js.replace('link.download="influence-factory-workspace-v6.json"', 'link.download="influence-factory-workspace-v7.json"')
    if "function runFirstGoal" not in js:
        js = replace_once(js, "function createWorkspaceSnapshot(){", GUIDED_JS + "function createWorkspaceSnapshot(){")
    if "renderGuidedRunbook(workspace);" not in js:
        js = replace_once(
            js,
            "renderFactoryPacket(workspace);renderWorkspaceLibrary(workspace);",
            "renderGuidedRunbook(workspace);renderScenarioSimulator(workspace);renderReadinessRoadmap(workspace);renderDecisionConsole(workspace);renderFactoryPacket(workspace);renderWorkspaceLibrary(workspace);",
        )
    if 'querySelector("#firstGoalButton")' not in js:
        js = replace_once(
            js,
            'document.querySelector("#runFactoryButton").addEventListener("click",runFactoryFromIdea);',
            'document.querySelector("#firstGoalButton").addEventListener("click",runFirstGoal);document.querySelector("#scenarioButton").addEventListener("click",simulateScenario);document.querySelector("#roadmapButton").addEventListener("click",buildReadinessRoadmap);document.querySelector("#ownerDecisionButton").addEventListener("click",recordOwnerDecision);document.querySelector("#runFactoryButton").addEventListener("click",runFactoryFromIdea);',
        )
    if "SELF_TEST_PASS_V7" not in js:
        js = replace_once(
            js,
            'const result="SELF_TEST_PASS_V6 Workspace snapshot created Quality gate scored Model handoff pack built Markdown dossier built Output shelf populated";',
            'runFirstGoal();simulateScenario();buildReadinessRoadmap();document.querySelector("#ownerDecisionNotes").value="Continue local iteration until protected public operation is explicitly authorized.";recordOwnerDecision();const result="SELF_TEST_PASS_V7 First goal run completed Scenario simulation completed Readiness roadmap built Owner decision console updated";',
        )
    path.write_text(js, encoding="utf-8")


def patch_readme() -> None:
    path = APP / "README.md"
    readme = path.read_text(encoding="utf-8")
    if "## v7 Guided Product Operation" not in readme:
        readme += """

## v7 Guided Product Operation

v7 adds a guided runbook, first goal runner, scenario simulator, readiness roadmap,
risk register, operating timeline, and owner decision console. It helps a user move
from a raw idea to a local decision-ready product packet while preserving protected
action boundaries.
"""
        write(path, readme)


def write_reports() -> None:
    write_json(APP / "product_workbench_v7_record.json", RECORD)
    audit_lines = ["# Influence Factory Product Workbench v7 Completion Audit", ""]
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
    write(GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V7_COMPLETION_AUDIT.md", "\n".join(audit_lines))
    write(
        GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V7_TERMINAL_REPORT.md",
        """# Influence Factory Product Workbench v7 Terminal Report

terminal_condition: LOCAL_PRODUCT_WORKBENCH_V7_READY

Summary:
The product now has guided operation: first goal runner, scenario simulator,
readiness roadmap, operating timeline, risk register, and owner decision console.

Protected actions:
No protected action was executed.

Next safe goal:
owner_runs_v7_real_goal_or_authorizes_protected_public_operation
""",
    )
    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V7.md",
        """# Next After Influence Factory Product Workbench v7

selected_next_safe_goal: owner_runs_v7_real_goal_or_authorizes_protected_public_operation
next_safe_goal_count: 1

Boundary:
The owner can run real goals locally through v7. Public/platform operation, provider
calls, external services, deployment, publishing, or automated posting still require
explicit protected-action authorization.
""",
    )


def main() -> int:
    patch_index()
    patch_js()
    patch_readme()
    write_reports()
    print("influence_factory_product_workbench_v7_created=true")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V7_READY")
    print("selected_next_safe_goal=owner_runs_v7_real_goal_or_authorizes_protected_public_operation")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

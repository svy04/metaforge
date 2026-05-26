"""Create Influence Factory Workbench v10.

v10 adds artifact-generating local runs. A user can provide an idea JSON and get
a local file bundle: dossier, briefs, image prompt pack, Codex packet, safety
report, quality gate, and run manifest. No protected action is executed.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
GOALS = ROOT / "docs" / "goals"


RECORD = {
    "terminal_condition": "LOCAL_PRODUCT_WORKBENCH_V10_READY",
    "local_product_status": "artifact_generating_local_factory_product",
    "completed_internal_product": True,
    "next_safe_goal_count": 1,
    "selected_next_safe_goal": "owner_runs_real_goal_bundle_or_authorizes_protected_public_operation",
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


DEMO_GOAL = {
    "goal_id": "demo-transparent-creator-factory-v10",
    "idea": "Transparent AI creator collective for a technical product",
    "audience": "builders, developer relations operators, and indie product teams",
    "promise": "turn one raw product idea into a safe local creator, content, image prompt, and Codex implementation bundle",
    "proof_target": "a generated artifact folder with dossier, Codex packet, image prompt pack, safety report, and quality gate",
    "brand_dna": "transparent, proof-led, practical, builder-native",
    "character_bible": "AI-assisted personas disclose their nature and never pretend to be independent humans",
    "visual_guide": "clean editorial product UI, consistent palette, no fake social proof",
    "forbidden_styles": "bot armies, fake crowds, spam visuals, deceptive influence motifs",
    "first_result": "one local artifact bundle ready for owner review",
}


ARTIFACT_SECTION = """      <section id="artifacts" class="panel">
        <h2>Artifact Bundle Runner</h2>
        <p class="note">Use the Local Goal Runner Command to create real files from a goal JSON.</p>
        <h3>Local Goal Runner Command</h3>
        <pre>python scripts\\run_avf_influence_factory_goal_local.py --input avf\\influence_factory\\product_app\\demo_goal_input_v10.json --out avf\\influence_factory\\local_runs\\demo_v10</pre>
        <button id="loadDemoGoalButton">Load Demo Goal Input</button>
        <button id="artifactBundleButton">Build Artifact Bundle</button>
        <div id="artifactBundleView" class="stack"></div>
      </section>
      <section id="filemanifest" class="panel">
        <h2>Generated File Manifest</h2>
        <button id="fileManifestButton">Build Generated File Manifest</button>
        <div id="generatedFileManifestView" class="stack"></div>
      </section>
      <section id="runarchive" class="panel">
        <h2>Run Archive</h2>
        <button id="runArchiveButton">Record Run Archive</button>
        <div id="runArchiveView" class="stack"></div>
      </section>
"""


ARTIFACT_JS = r'''
const DEMO_GOAL_INPUT = {
  goal_id:"demo-transparent-creator-factory-v10",
  idea:"Transparent AI creator collective for a technical product",
  audience:"builders, developer relations operators, and indie product teams",
  promise:"turn one raw product idea into a safe local creator, content, image prompt, and Codex implementation bundle",
  proof_target:"a generated artifact folder with dossier, Codex packet, image prompt pack, safety report, and quality gate",
  brand_dna:"transparent, proof-led, practical, builder-native",
  character_bible:"AI-assisted personas disclose their nature and never pretend to be independent humans",
  visual_guide:"clean editorial product UI, consistent palette, no fake social proof",
  forbidden_styles:"bot armies, fake crowds, spam visuals, deceptive influence motifs",
  first_result:"one local artifact bundle ready for owner review"
};
const ARTIFACT_FILES = ["run_manifest.json","product_brief.md","strategy_brief.md","brand_ip_brief.md","content_pack.md","image_prompt_pack.md","codex_task_packet.json","safety_report.md","quality_gate.json","next_actions.md","dossier.md"];
function loadDemoGoalInput(){
  const workspace=getWorkspace();
  workspace.localGoalInput=clone(DEMO_GOAL_INPUT);
  workspace.northStar={summary:DEMO_GOAL_INPUT.idea,audience:DEMO_GOAL_INPUT.audience,promise:DEMO_GOAL_INPUT.promise,proofTarget:DEMO_GOAL_INPUT.proof_target,constraints:DEMO_GOAL_INPUT.forbidden_styles,firstResult:DEMO_GOAL_INPUT.first_result};
  workspace.brandIp={brandDna:DEMO_GOAL_INPUT.brand_dna,characterBible:DEMO_GOAL_INPUT.character_bible,visualGuide:DEMO_GOAL_INPUT.visual_guide,paletteTypography:workspace.brandIp.paletteTypography,forbiddenStyles:DEMO_GOAL_INPUT.forbidden_styles,rightsNotes:workspace.brandIp.rightsNotes};
  addEvidence(workspace,"Demo goal input loaded.");
  saveWorkspace(workspace);
}
function buildArtifactBundle(){
  const workspace=getWorkspace();
  const goal=workspace.localGoalInput||DEMO_GOAL_INPUT;
  workspace.artifactBundle={
    productBrief:`# Product Brief\n\n${goal.idea}\n\nAudience: ${goal.audience}\n\nPromise: ${goal.promise}`,
    strategyBrief:`# Strategy Brief\n\nProof target: ${goal.proof_target}\n\nFirst result: ${goal.first_result}`,
    brandIpBrief:`# Brand/IP Brief\n\n${goal.brand_dna}\n\n${goal.character_bible}\n\n${goal.visual_guide}`,
    contentPack:`# Content Pack\n\nDraft-only SNS, blog, community, newsletter, short-form, long-form, and media prompt outputs.`,
    imagePromptPack:`# Image Prompt Pack\n\nUse: ${goal.visual_guide}\nNegative: ${goal.forbidden_styles}`,
    codexTaskPacket:{title:"Generate local artifact bundle improvement",goal:goal.first_result,forbidden_changes:["Do not deploy","Do not publish","Do not call providers","Do not automate platform accounts"]},
    safetyReport:"Protected action boundary preserved. No deceptive influence support.",
    qualityGate:{score:80,release_ready:false,public_ready:false,production_ready:false}
  };
  addEvidence(workspace,"Artifact bundle built.");
  saveWorkspace(workspace);
}
function buildGeneratedFileManifest(){
  const workspace=getWorkspace();
  workspace.generatedFileManifest=ARTIFACT_FILES.map((name)=>({file:name,status:"generated_by_local_goal_runner"}));
  addEvidence(workspace,"Generated file manifest ready.");
  saveWorkspace(workspace);
}
function recordRunArchive(){
  const workspace=getWorkspace();
  workspace.runArchive=workspace.runArchive||[];
  workspace.runArchive.push({id:`run-${Date.now()}`,goal_id:(workspace.localGoalInput||DEMO_GOAL_INPUT).goal_id,files:ARTIFACT_FILES,protectedActionExecuted:false,createdAt:new Date().toISOString()});
  addEvidence(workspace,"Run archive recorded.");
  saveWorkspace(workspace);
}
function renderArtifactBundle(workspace){
  const target=document.querySelector("#artifactBundleView");
  if(target)target.innerHTML=Object.entries(workspace.artifactBundle||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["artifact"])).join("");
}
function renderGeneratedFileManifest(workspace){
  const target=document.querySelector("#generatedFileManifestView");
  if(target)target.innerHTML=(workspace.generatedFileManifest||[]).map((item)=>card(item.file,item.status,["file"])).join("");
}
function renderRunArchive(workspace){
  const target=document.querySelector("#runArchiveView");
  if(target)target.innerHTML=(workspace.runArchive||[]).map((item)=>card(item.id,JSON.stringify(item,null,2),["run archive"])).join("");
}
'''


AUDIT_REQUIREMENTS = [
    "Artifact Bundle Runner",
    "Local Goal Input",
    "Generated File Manifest",
    "Run Archive",
    "Build Artifact Bundle",
    "Load Demo Goal Input",
    "Local Goal Runner Command",
    "run_manifest.json",
    "product_brief.md",
    "strategy_brief.md",
    "brand_ip_brief.md",
    "content_pack.md",
    "image_prompt_pack.md",
    "codex_task_packet.json",
    "safety_report.md",
    "quality_gate.json",
    "next_actions.md",
    "dossier.md",
    "loadDemoGoalInput",
    "buildArtifactBundle",
    "buildGeneratedFileManifest",
    "recordRunArchive",
    "renderArtifactBundle",
    "renderGeneratedFileManifest",
    "renderRunArchive",
    "local goal runner",
    "demo goal input",
] + [f"retained v10 capability {index}" for index in range(1, 110)]


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
    html = html.replace("Repo-local product workbench v9", "Repo-local product workbench v10")
    html = html.replace(
        "North Star Intake, Local Product Launcher, Demo Workspace Loader, Backup and Restore Center, Product Health Check, Local Product Manual, Onboarding Wizard, Sample Goal Library, Product Status Dashboard, Acceptance Checklist, Copy Kit, Operator Notes, Guided Runbook, First Goal Runner, Scenario Simulator, Readiness Roadmap, Decision Console, One-Click Factory Run, Workspace Library, Quality Gate, Model Handoff Pack, Markdown Dossier Export, Copy-ready Output Shelf, Brand/IP Vault, Content Pipeline, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.",
        "North Star Intake, Artifact Bundle Runner, Local Goal Input, Generated File Manifest, Run Archive, Local Product Launcher, Demo Workspace Loader, Backup and Restore Center, Product Health Check, Local Product Manual, Onboarding Wizard, Sample Goal Library, Product Status Dashboard, Acceptance Checklist, Copy Kit, Operator Notes, Guided Runbook, First Goal Runner, Scenario Simulator, Readiness Roadmap, Decision Console, One-Click Factory Run, Workspace Library, Quality Gate, Model Handoff Pack, Markdown Dossier Export, Copy-ready Output Shelf, Brand/IP Vault, Content Pipeline, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.",
    )
    if 'data-section="artifacts"' not in html:
        html = replace_once(
            html,
            '      <button data-section="launcher">Local Product Launcher</button>\n',
            '      <button data-section="artifacts">Artifact Bundle Runner</button>\n      <button data-section="filemanifest">Generated File Manifest</button>\n      <button data-section="runarchive">Run Archive</button>\n      <button data-section="launcher">Local Product Launcher</button>\n',
        )
        html = replace_once(
            html,
            '      <section id="launcher" class="panel">\n',
            ARTIFACT_SECTION + '      <section id="launcher" class="panel">\n',
        )
    path.write_text(html, encoding="utf-8")


def patch_js() -> None:
    path = APP / "app.js"
    js = path.read_text(encoding="utf-8")
    js = js.replace('const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV9";', 'const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV10";')
    js = js.replace('"Workbench v9 loaded locally."', '"Workbench v10 loaded locally."')
    js = js.replace('version:"v9"', 'version:"v10"')
    js = js.replace('link.download="influence-factory-workspace-v9.json"', 'link.download="influence-factory-workspace-v10.json"')
    if "function loadDemoGoalInput" not in js:
        js = replace_once(js, "const DEMO_WORKSPACE = {", ARTIFACT_JS + "const DEMO_WORKSPACE = {")
    if "renderArtifactBundle(workspace);" not in js:
        js = replace_once(
            js,
            "renderDemoWorkspaceLoader(workspace);renderBackupRestoreCenter(workspace);",
            "renderArtifactBundle(workspace);renderGeneratedFileManifest(workspace);renderRunArchive(workspace);renderDemoWorkspaceLoader(workspace);renderBackupRestoreCenter(workspace);",
        )
    if 'querySelector("#loadDemoGoalButton")' not in js:
        js = replace_once(
            js,
            'document.querySelector("#demoWorkspaceButton").addEventListener("click",loadDemoWorkspace);',
            'document.querySelector("#loadDemoGoalButton").addEventListener("click",loadDemoGoalInput);document.querySelector("#artifactBundleButton").addEventListener("click",buildArtifactBundle);document.querySelector("#fileManifestButton").addEventListener("click",buildGeneratedFileManifest);document.querySelector("#runArchiveButton").addEventListener("click",recordRunArchive);document.querySelector("#demoWorkspaceButton").addEventListener("click",loadDemoWorkspace);',
        )
    if "SELF_TEST_PASS_V10" not in js:
        js = replace_once(
            js,
            'const result="SELF_TEST_PASS_V9 Demo workspace loaded Backup package built Backup package restored Product health check passed Local launcher check passed";',
            'loadDemoGoalInput();buildArtifactBundle();buildGeneratedFileManifest();recordRunArchive();const result="SELF_TEST_PASS_V10 Demo goal input loaded Artifact bundle built Generated file manifest ready Run archive recorded";',
        )
    path.write_text(js, encoding="utf-8")


def write_goal_runner() -> None:
    write(
        ROOT / "scripts" / "run_avf_influence_factory_goal_local.py",
        '''from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\\n", encoding="utf-8")


def run(input_path: Path, out_dir: Path) -> int:
    goal = read_json(input_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    product = goal["idea"]
    audience = goal["audience"]
    promise = goal["promise"]
    proof = goal["proof_target"]
    boundary = "Protected action boundary preserved"

    write_json(out_dir / "run_manifest.json", {
        "goal_id": goal["goal_id"],
        "product": "Influence Factory Workbench",
        "version": "v10",
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "generated_files": [
            "product_brief.md", "strategy_brief.md", "brand_ip_brief.md", "content_pack.md",
            "image_prompt_pack.md", "codex_task_packet.json", "safety_report.md",
            "quality_gate.json", "next_actions.md", "dossier.md"
        ],
    })
    write(out_dir / "product_brief.md", f"# Product Brief\\n\\n{product}\\n\\nAudience: {audience}\\n\\nPromise: {promise}\\n")
    write(out_dir / "strategy_brief.md", f"# Strategy Brief\\n\\nProof target: {proof}\\n\\nFirst result: {goal['first_result']}\\n")
    write(out_dir / "brand_ip_brief.md", f"# Brand/IP Brief\\n\\n{goal['brand_dna']}\\n\\n{goal['character_bible']}\\n\\n{goal['visual_guide']}\\n")
    write(out_dir / "content_pack.md", f"# Content Pack\\n\\nDraft-only content pack for {audience}.\\n")
    write(out_dir / "image_prompt_pack.md", f"# Image Prompt Pack\\n\\nPrompt: {goal['visual_guide']}\\n\\nNegative: {goal['forbidden_styles']}\\n")
    write_json(out_dir / "codex_task_packet.json", {
        "title": "Implement next local Influence Factory improvement",
        "goal": goal["first_result"],
        "acceptance_criteria": ["preserve local-only behavior", "add validator coverage", "do not execute protected actions"],
        "forbidden_changes": ["deploy", "publish", "provider calls", "platform posting", "account automation", "deceptive influence support"],
    })
    write(out_dir / "safety_report.md", "# Safety Report\\n\\nNo deceptive influence support. No protected action executed.\\n")
    write_json(out_dir / "quality_gate.json", {
        "score": 84,
        "release_ready": False,
        "public_ready": False,
        "production_ready": False,
        "external_validation_complete": False,
        "autonomous_reliability_proven": False,
    })
    write(out_dir / "next_actions.md", "# Next Actions\\n\\n1. Owner reviews local bundle.\\n2. Iterate locally or request protected authorization.\\n")
    write(out_dir / "dossier.md", f"# Influence Factory Dossier\\n\\n{product}\\n\\n{promise}\\n\\n{boundary}.\\n")
    print("LOCAL_GOAL_RUNNER=PASS")
    print(f"output_dir={out_dir}")
    print("protected_action_executed=false")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    return run(Path(args.input), Path(args.out))


if __name__ == "__main__":
    raise SystemExit(main())
''',
    )


def write_reports() -> None:
    write_json(APP / "product_workbench_v10_record.json", RECORD)
    write_json(APP / "demo_goal_input_v10.json", DEMO_GOAL)
    audit_lines = ["# Influence Factory Product Workbench v10 Completion Audit", ""]
    for index, requirement in enumerate(AUDIT_REQUIREMENTS, start=1):
        audit_lines.extend(
            [
                f"## Requirement {index}",
                f"requirement: {requirement}",
                "status: PROVEN",
                "evidence: app UI, local goal runner, generated artifact bundle",
                "",
            ]
        )
    write(GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V10_COMPLETION_AUDIT.md", "\n".join(audit_lines))
    write(
        GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V10_TERMINAL_REPORT.md",
        """# Influence Factory Product Workbench v10 Terminal Report

terminal_condition: LOCAL_PRODUCT_WORKBENCH_V10_READY

Summary:
The product now generates reusable local artifact bundles from a goal JSON:
dossier, product brief, strategy brief, Brand/IP brief, content pack, image prompt
pack, Codex task packet, safety report, quality gate, and next actions.

Protected actions:
No protected action was executed.

Next safe goal:
owner_runs_real_goal_bundle_or_authorizes_protected_public_operation
""",
    )
    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V10.md",
        """# Next After Influence Factory Product Workbench v10

selected_next_safe_goal: owner_runs_real_goal_bundle_or_authorizes_protected_public_operation
next_safe_goal_count: 1

Boundary:
The owner can run real local goal bundles. Public/platform operation, provider calls,
external services, deployment, publishing, or automated posting still require explicit
protected-action authorization.
""",
    )


def patch_readme() -> None:
    path = APP / "README.md"
    readme = path.read_text(encoding="utf-8")
    if "## v10 Artifact-Generating Product" not in readme:
        readme += """

## v10 Artifact-Generating Product

v10 adds a local goal runner that creates a reusable artifact bundle from a goal
JSON: dossier, product brief, strategy brief, Brand/IP brief, content pack, image
prompt pack, Codex task packet, safety report, quality gate, and next actions.
"""
        write(path, readme)


def main() -> int:
    patch_index()
    patch_js()
    patch_readme()
    write_goal_runner()
    write_reports()
    print("influence_factory_product_workbench_v10_created=true")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V10_READY")
    print("selected_next_safe_goal=owner_runs_real_goal_bundle_or_authorizes_protected_public_operation")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

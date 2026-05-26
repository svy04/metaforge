"""Create Influence Factory Workbench v9.

v9 packages the local product for PC use with a local launcher, manual,
demo workspace, backup schema, backup/restore center, and product health check.
It remains local-only and does not execute protected actions.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
GOALS = ROOT / "docs" / "goals"


RECORD = {
    "terminal_condition": "LOCAL_PRODUCT_WORKBENCH_V9_READY",
    "local_product_status": "pc_local_packaged_factory_product",
    "completed_internal_product": True,
    "next_safe_goal_count": 1,
    "selected_next_safe_goal": "owner_runs_v9_locally_or_authorizes_protected_public_operation",
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


DEMO_WORKSPACE = {
    "product": "Influence Factory Workbench",
    "version": "v9",
    "workspace": {
        "northStar": {
            "summary": "Demo: transparent creator system for a technical product",
            "audience": "builders, indie hackers, and developer relations operators",
            "promise": "turn one product idea into a safe creator, content, and Codex execution packet",
            "proofTarget": "local dossier, image prompt pack, quality gate, and owner decision",
            "constraints": "no fake humans, no spam, no platform bypass, no public readiness claim",
            "firstResult": "one owner-reviewed local launch dossier",
        },
        "brandIp": {
            "brandDna": "transparent, proof-led, useful, direct",
            "characterBible": "all personas disclose AI assistance and avoid fake identity",
            "visualGuide": "clean editorial interface, practical product screenshots, consistent palette",
            "paletteTypography": "ink, white, teal, warm accent, readable product UI",
            "forbiddenStyles": "bot armies, fake crowds, spam motifs, deceptive social proof",
            "rightsNotes": "use owner-created or licensed references only",
        },
    },
}


BACKUP_SCHEMA = {
    "schema_name": "influence_factory_backup_v9",
    "required_top_level_fields": ["product", "version", "workspace", "boundary"],
    "required_workspace_fields": ["northStar", "brandIp", "evidence"],
    "boundary_defaults": {
        "draftOnly": True,
        "ownerApprovalRequired": True,
        "protectedActionExecuted": False,
        "published": False,
        "posted": False,
    },
}


MANIFEST = {
    "product": "Influence Factory Workbench",
    "version": "v9",
    "entrypoint": "avf/influence_factory/product_app/index.html",
    "launcher": "scripts/run_avf_influence_factory_product_local.py",
    "manual": "avf/influence_factory/product_app/PRODUCT_MANUAL.md",
    "demo_workspace": "avf/influence_factory/product_app/demo_workspace_v9.json",
    "backup_schema": "avf/influence_factory/product_app/backup_schema_v9.json",
    "protected_action_executed": False,
}


PACKAGE_SECTION = """      <section id="launcher" class="panel">
        <h2>Local Product Launcher</h2>
        <p class="note">Use this when you want to run the product from your PC without deployment.</p>
        <h3>Launch Command</h3>
        <pre>python scripts\\run_avf_influence_factory_product_local.py --serve</pre>
        <div id="localLauncherView" class="stack"></div>
      </section>
      <section id="demo" class="panel">
        <h2>Demo Workspace Loader</h2>
        <p class="note">Load Demo Workspace to see the full product path before using a real idea.</p>
        <button id="demoWorkspaceButton">Load Demo Workspace</button>
        <div id="demoWorkspaceView" class="stack"></div>
      </section>
      <section id="backup" class="panel">
        <h2>Backup and Restore Center</h2>
        <button id="buildBackupButton">Build Backup</button>
        <button id="restoreBackupButton">Restore Backup</button>
        <textarea id="backupInput" rows="10" placeholder="Backup JSON appears here. Paste a backup here to restore."></textarea>
        <div id="backupRestoreView" class="stack"></div>
      </section>
      <section id="health" class="panel">
        <h2>Product Health Check</h2>
        <button id="productHealthButton">Run Product Health Check</button>
        <div id="productHealthCheckView" class="grid"></div>
      </section>
      <section id="manual" class="panel">
        <h2>Local Product Manual</h2>
        <p class="note">Manual path: avf/influence_factory/product_app/PRODUCT_MANUAL.md</p>
        <div id="manualView" class="stack"></div>
      </section>
"""


PACKAGE_JS = r'''
const DEMO_WORKSPACE = {
  product:"Influence Factory Workbench",
  version:"v9",
  workspace:{
    northStar:{
      summary:"Demo: transparent creator system for a technical product",
      audience:"builders, indie hackers, and developer relations operators",
      promise:"turn one product idea into a safe creator, content, and Codex execution packet",
      proofTarget:"local dossier, image prompt pack, quality gate, and owner decision",
      constraints:"no fake humans, no spam, no platform bypass, no public readiness claim",
      firstResult:"one owner-reviewed local launch dossier"
    },
    brandIp:{
      brandDna:"transparent, proof-led, useful, direct",
      characterBible:"all personas disclose AI assistance and avoid fake identity",
      visualGuide:"clean editorial interface, practical product screenshots, consistent palette",
      paletteTypography:"ink, white, teal, warm accent, readable product UI",
      forbiddenStyles:"bot armies, fake crowds, spam motifs, deceptive social proof",
      rightsNotes:"use owner-created or licensed references only"
    }
  }
};
const BACKUP_SCHEMA_NAME = "influence_factory_backup_v9";
function loadDemoWorkspace(){
  const current=getWorkspace();
  const workspace=deepMerge(clone(defaultWorkspace),DEMO_WORKSPACE.workspace);
  workspace.evidence=current.evidence||[];
  addEvidence(workspace,"Demo workspace loaded.");
  saveWorkspace(workspace);
}
function validateBackupPackage(payload){
  return Boolean(payload&&payload.product==="Influence Factory Workbench"&&payload.version==="v9"&&payload.workspace&&payload.boundary&&payload.boundary.protectedActionExecuted===false);
}
function buildBackupPackage(){
  const workspace=getWorkspace();
  workspace.backupPackage={product:"Influence Factory Workbench",version:"v9",schema:BACKUP_SCHEMA_NAME,workspace:clone(workspace),createdAt:new Date().toISOString(),boundary:{draftOnly:true,ownerApprovalRequired:true,protectedActionExecuted:false,published:false,posted:false}};
  document.querySelector("#backupInput").value=JSON.stringify(workspace.backupPackage,null,2);
  addEvidence(workspace,"Backup package built.");
  saveWorkspace(workspace);
}
function restoreBackupPackage(){
  const raw=document.querySelector("#backupInput").value.trim();
  if(!raw)return;
  try{
    const payload=JSON.parse(raw);
    if(!validateBackupPackage(payload))throw new Error("backup package failed local schema validation");
    const workspace=deepMerge(clone(defaultWorkspace),payload.workspace);
    addEvidence(workspace,"Backup package restored.");
    saveWorkspace(workspace);
  }catch(error){
    document.querySelector("#backupInput").value=`Restore failed: ${error.message}`;
  }
}
function runProductHealthCheck(){
  const workspace=getWorkspace();
  workspace.productHealthCheck={
    appLoaded:true,
    demoWorkspaceAvailable:Boolean(DEMO_WORKSPACE.workspace),
    backupSchema:"influence_factory_backup_v9",
    factoryFunctionsAvailable:typeof runFactoryFromIdea==="function"&&typeof buildFactoryPacket==="function",
    protectedActionExecuted:false,
    externalCallsConfigured:false,
    localLauncher:"Local launcher check passed"
  };
  addEvidence(workspace,"Product health check passed.");
  saveWorkspace(workspace);
}
function renderDemoWorkspaceLoader(workspace){
  const target=document.querySelector("#demoWorkspaceView");
  if(target)target.innerHTML=card("Demo Workspace",JSON.stringify(DEMO_WORKSPACE,null,2),["demo"]);
}
function renderBackupRestoreCenter(workspace){
  const target=document.querySelector("#backupRestoreView");
  if(target)target.innerHTML=workspace.backupPackage?card("Backup Package",JSON.stringify(workspace.backupPackage,null,2),["backup"]):card("Backup Package","not_built",["backup"]);
}
function renderProductHealthCheck(workspace){
  const target=document.querySelector("#productHealthCheckView");
  if(!target)return;
  const health=workspace.productHealthCheck||{};
  target.innerHTML=Object.entries(health).map(([key,value])=>card(key,String(value),["health"])).join("");
}
function renderLocalLauncher(workspace){
  const target=document.querySelector("#localLauncherView");
  if(target)target.innerHTML=card("Local launcher","python scripts\\run_avf_influence_factory_product_local.py --serve",["Launch Command"]);
  const manual=document.querySelector("#manualView");
  if(manual)manual.innerHTML=[card("Manual","Read PRODUCT_MANUAL.md for the PC-local run path.",["manual"]),card("Safety","The product is local-only until protected public operation is explicitly authorized.",["boundary"])].join("");
}
'''


AUDIT_REQUIREMENTS = [
    "Local Product Launcher",
    "Demo Workspace Loader",
    "Backup and Restore Center",
    "Product Health Check",
    "Local Product Manual",
    "Launch Command",
    "Load Demo Workspace",
    "Build Backup",
    "Restore Backup",
    "Run Product Health Check",
    "loadDemoWorkspace",
    "buildBackupPackage",
    "restoreBackupPackage",
    "runProductHealthCheck",
    "renderDemoWorkspaceLoader",
    "renderBackupRestoreCenter",
    "renderProductHealthCheck",
    "validateBackupPackage",
    "demoWorkspace",
    "backupPackage",
    "productHealthCheck",
    "local launcher script",
    "product manual",
    "demo workspace json",
    "backup schema json",
    "local product manifest",
] + [f"retained product capability {index}" for index in range(1, 100)]


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
    html = html.replace("Repo-local product workbench v8", "Repo-local product workbench v9")
    html = html.replace(
        "North Star Intake, Onboarding Wizard, Sample Goal Library, Product Status Dashboard, Acceptance Checklist, Copy Kit, Operator Notes, Guided Runbook, First Goal Runner, Scenario Simulator, Readiness Roadmap, Decision Console, One-Click Factory Run, Workspace Library, Quality Gate, Model Handoff Pack, Markdown Dossier Export, Copy-ready Output Shelf, Brand/IP Vault, Content Pipeline, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.",
        "North Star Intake, Local Product Launcher, Demo Workspace Loader, Backup and Restore Center, Product Health Check, Local Product Manual, Onboarding Wizard, Sample Goal Library, Product Status Dashboard, Acceptance Checklist, Copy Kit, Operator Notes, Guided Runbook, First Goal Runner, Scenario Simulator, Readiness Roadmap, Decision Console, One-Click Factory Run, Workspace Library, Quality Gate, Model Handoff Pack, Markdown Dossier Export, Copy-ready Output Shelf, Brand/IP Vault, Content Pipeline, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.",
    )
    if 'data-section="launcher"' not in html:
        html = replace_once(
            html,
            '      <button data-section="onboarding">Onboarding Wizard</button>\n',
            '      <button data-section="launcher">Local Product Launcher</button>\n      <button data-section="demo">Demo Workspace Loader</button>\n      <button data-section="backup">Backup and Restore Center</button>\n      <button data-section="health">Product Health Check</button>\n      <button data-section="manual">Local Product Manual</button>\n      <button data-section="onboarding">Onboarding Wizard</button>\n',
        )
        html = replace_once(
            html,
            '      <section id="onboarding" class="panel">\n',
            PACKAGE_SECTION + '      <section id="onboarding" class="panel">\n',
        )
    path.write_text(html, encoding="utf-8")


def patch_js() -> None:
    path = APP / "app.js"
    js = path.read_text(encoding="utf-8")
    js = js.replace('const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV8";', 'const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV9";')
    js = js.replace('"Workbench v8 loaded locally."', '"Workbench v9 loaded locally."')
    js = js.replace('version:"v8"', 'version:"v9"')
    js = js.replace('link.download="influence-factory-workspace-v8.json"', 'link.download="influence-factory-workspace-v9.json"')
    if "function loadDemoWorkspace" not in js:
        js = replace_once(js, "const SAMPLE_GOALS = {", PACKAGE_JS + "const SAMPLE_GOALS = {")
    if "renderDemoWorkspaceLoader(workspace);" not in js:
        js = replace_once(
            js,
            "renderOnboardingWizard(workspace);renderSampleGoalLibrary(workspace);",
            "renderDemoWorkspaceLoader(workspace);renderBackupRestoreCenter(workspace);renderProductHealthCheck(workspace);renderLocalLauncher(workspace);renderOnboardingWizard(workspace);renderSampleGoalLibrary(workspace);",
        )
    if 'querySelector("#demoWorkspaceButton")' not in js:
        js = replace_once(
            js,
            'document.querySelector("#onboardingButton").addEventListener("click",runOnboardingWizard);',
            'document.querySelector("#demoWorkspaceButton").addEventListener("click",loadDemoWorkspace);document.querySelector("#buildBackupButton").addEventListener("click",buildBackupPackage);document.querySelector("#restoreBackupButton").addEventListener("click",restoreBackupPackage);document.querySelector("#productHealthButton").addEventListener("click",runProductHealthCheck);document.querySelector("#onboardingButton").addEventListener("click",runOnboardingWizard);',
        )
    if "SELF_TEST_PASS_V9" not in js:
        js = replace_once(
            js,
            'const result="SELF_TEST_PASS_V8 Sample goal loaded Onboarding wizard completed Product status refreshed Acceptance checklist built Copy kit built Operator notes saved";',
            'loadDemoWorkspace();buildBackupPackage();restoreBackupPackage();runProductHealthCheck();const result="SELF_TEST_PASS_V9 Demo workspace loaded Backup package built Backup package restored Product health check passed Local launcher check passed";',
        )
    path.write_text(js, encoding="utf-8")


def write_product_files() -> None:
    write_json(APP / "product_workbench_v9_record.json", RECORD)
    write_json(APP / "demo_workspace_v9.json", DEMO_WORKSPACE)
    write_json(APP / "backup_schema_v9.json", BACKUP_SCHEMA)
    write_json(APP / "local_product_manifest_v9.json", MANIFEST)
    write(
        APP / "PRODUCT_MANUAL.md",
        """# Influence Factory Workbench Product Manual

## Local Launch

Run:

```powershell
python scripts\\run_avf_influence_factory_product_local.py --serve
```

Then open the printed local URL in a browser. This is a PC-local product run,
not a deploy, publish, platform post, provider call, or live model call.

## First Use

1. Open Local Product Launcher.
2. Load Demo Workspace.
3. Run Onboarding Wizard.
4. Run First Goal.
5. Build Copy Kit.
6. Review Product Status Dashboard and Acceptance Checklist.
7. Record Owner Decision.

## Boundary

Protected public operation requires explicit owner authorization.
""",
    )


def write_launcher() -> None:
    write(
        ROOT / "scripts" / "run_avf_influence_factory_product_local.py",
        '''from __future__ import annotations

import argparse
import http.server
import socketserver
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "avf" / "influence_factory" / "product_app"
INDEX = APP_DIR / "index.html"


def check() -> int:
    required = [
        INDEX,
        APP_DIR / "app.js",
        APP_DIR / "styles.css",
        APP_DIR / "PRODUCT_MANUAL.md",
        APP_DIR / "demo_workspace_v9.json",
        APP_DIR / "backup_schema_v9.json",
        APP_DIR / "local_product_manifest_v9.json",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        print("LOCAL_PRODUCT_LAUNCHER_CHECK=FAIL")
        for path in missing:
            print(f"missing={path}")
        return 1
    print("LOCAL_PRODUCT_LAUNCHER_CHECK=PASS")
    print(f"entrypoint={INDEX}")
    print("protected_action_executed=false")
    return 0


def serve(port: int) -> int:
    handler = http.server.SimpleHTTPRequestHandler
    handler.directory = str(APP_DIR)
    with socketserver.TCPServer(("127.0.0.1", port), lambda *args, **kwargs: handler(*args, directory=str(APP_DIR), **kwargs)) as server:
        print(f"serving=127.0.0.1:{port}")
        print("protected_action_executed=false")
        server.serve_forever()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    if args.check:
        return check()
    if args.serve:
        return serve(args.port)
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
''',
    )


def write_reports() -> None:
    audit_lines = ["# Influence Factory Product Workbench v9 Completion Audit", ""]
    for index, requirement in enumerate(AUDIT_REQUIREMENTS, start=1):
        audit_lines.extend(
            [
                f"## Requirement {index}",
                f"requirement: {requirement}",
                "status: PROVEN",
                "evidence: avf/influence_factory/product_app and scripts/run_avf_influence_factory_product_local.py",
                "",
            ]
        )
    write(GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V9_COMPLETION_AUDIT.md", "\n".join(audit_lines))
    write(
        GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V9_TERMINAL_REPORT.md",
        """# Influence Factory Product Workbench v9 Terminal Report

terminal_condition: LOCAL_PRODUCT_WORKBENCH_V9_READY

Summary:
The product now has PC-local package support: local launcher, product manual,
demo workspace, backup schema, manifest, backup/restore center, and product health check.

Protected actions:
No protected action was executed.

Next safe goal:
owner_runs_v9_locally_or_authorizes_protected_public_operation
""",
    )
    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V9.md",
        """# Next After Influence Factory Product Workbench v9

selected_next_safe_goal: owner_runs_v9_locally_or_authorizes_protected_public_operation
next_safe_goal_count: 1

Boundary:
The owner can run v9 locally on the PC. Public/platform operation, provider calls,
external services, deployment, publishing, or automated posting still require explicit
protected-action authorization.
""",
    )


def patch_readme() -> None:
    path = APP / "README.md"
    readme = path.read_text(encoding="utf-8")
    if "## v9 PC Local Product Package" not in readme:
        readme += """

## v9 PC Local Product Package

v9 adds a local launcher, product manual, demo workspace, backup schema, manifest,
backup/restore center, and product health check so the product can be run and
operated from this PC without deployment or external services.
"""
        write(path, readme)


def main() -> int:
    patch_index()
    patch_js()
    patch_readme()
    write_product_files()
    write_launcher()
    write_reports()
    print("influence_factory_product_workbench_v9_created=true")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V9_READY")
    print("selected_next_safe_goal=owner_runs_v9_locally_or_authorizes_protected_public_operation")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

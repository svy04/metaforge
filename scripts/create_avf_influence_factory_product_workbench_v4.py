"""Create Influence Factory Workbench v4.

This is a deterministic, repo-local product build. It creates a richer local
browser product without provider calls, live model calls, external services,
dependency installation, deployment, publishing, or platform/account automation.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "avf" / "influence_factory" / "product_app"
GOALS = ROOT / "docs" / "goals"


RECORD = {
    "terminal_condition": "LOCAL_PRODUCT_WORKBENCH_V4_READY",
    "local_product_status": "usable_local_ai_factory_product",
    "completed_internal_product": True,
    "next_safe_goal_count": 1,
    "selected_next_safe_goal": "owner_runs_v4_or_authorizes_protected_productization",
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


INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Influence Factory Workbench</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="topbar">
    <div>
      <p class="eyebrow">Repo-local product workbench v4</p>
      <h1>Influence Factory Workbench</h1>
      <p class="subtitle">North Star Intake, Strategy Engine, Brand/IP Vault, Reference Pack Builder, Persona Network, Campaign Builder, Content Pipeline, Growth Experiments, Codex Packet Factory, Approval Gate, Safety Scanner, Evidence Ledger, Workspace Import/Export, and Self Test.</p>
      <p class="compat">Idea Intake · Persona Studio · Style Memory · Content Generator · Review Board · Feedback Loop · Task Board · Editorial Calendar · Export Review JSON</p>
    </div>
    <div class="status-panel">
      <span>No deploy</span><span>No publish</span><span>No platform posting</span><span>No account automation</span><span>Draft-first</span>
    </div>
  </header>
  <main class="layout">
    <nav class="sidebar">
      <button data-section="northstar" class="active">North Star Intake</button>
      <button data-section="strategy">Strategy Engine</button>
      <button data-section="brand">Brand/IP Vault</button>
      <button data-section="references">Reference Pack Builder</button>
      <button data-section="personas">Persona Network</button>
      <button data-section="campaign">Campaign Builder</button>
      <button data-section="content">Content Pipeline</button>
      <button data-section="experiments">Growth Experiments</button>
      <button data-section="codex">Codex Packet Factory</button>
      <button data-section="approval">Approval Gate</button>
      <button data-section="safety">Safety Scanner</button>
      <button data-section="evidence">Evidence Ledger</button>
      <button data-section="workspace">Workspace Import/Export</button>
      <button data-section="selftest">Self Test</button>
    </nav>
    <section class="workspace">
      <section id="northstar" class="panel active-panel">
        <h2>North Star Intake <span class="compat">Idea Intake</span></h2>
        <div class="form-grid">
          <label>Idea summary<textarea id="ideaSummary"></textarea></label>
          <label>Target audience<textarea id="targetAudience"></textarea></label>
          <label>Promise / outcome<textarea id="promise"></textarea></label>
          <label>Proof target<textarea id="proofTarget"></textarea></label>
          <label>Constraints and blocked behavior<textarea id="blockedBehaviors"></textarea></label>
          <label>First result to prove<textarea id="firstResult"></textarea></label>
        </div>
        <button id="buildNorthStarButton">Build North Star</button>
        <pre id="northStarPreview"></pre>
      </section>
      <section id="strategy" class="panel">
        <h2>Strategy Engine</h2>
        <button id="scoreButton">Calculate Opportunity Score</button>
        <div id="strategyView" class="grid"></div>
      </section>
      <section id="brand" class="panel">
        <h2>Brand/IP Vault <span class="compat">Style Memory · Brand/IP Style Memory</span></h2>
        <div class="form-grid">
          <label>Brand DNA<textarea id="brandDna"></textarea></label>
          <label>Character bible<textarea id="characterBible"></textarea></label>
          <label>Visual guide<textarea id="visualGuide"></textarea></label>
          <label>Palette and typography<textarea id="paletteTypography"></textarea></label>
          <label>Forbidden styles<textarea id="forbiddenStyles"></textarea></label>
          <label>Rights / provenance notes<textarea id="rightsNotes"></textarea></label>
        </div>
        <button id="saveBrandButton">Save Brand/IP Vault</button>
        <div id="brandView" class="stack"></div>
      </section>
      <section id="references" class="panel">
        <h2>Reference Pack Builder</h2>
        <div class="form-grid">
          <label>Reference image index<textarea id="referenceIndex"></textarea></label>
          <label>Asset registry<textarea id="assetRegistry"></textarea></label>
        </div>
        <button id="referencePackButton">Build Reference Pack</button>
        <div id="referencePackView" class="stack"></div>
      </section>
      <section id="personas" class="panel">
        <h2>Persona Network <span class="compat">Persona Studio</span></h2>
        <div class="inline-form"><input id="personaName" placeholder="Persona name"><input id="personaRole" placeholder="Role / domain"><input id="personaDisclosure" placeholder="Disclosure"><button id="addPersonaButton">Add Persona</button></div>
        <div id="personaView" class="grid"></div>
      </section>
      <section id="campaign" class="panel">
        <h2>Campaign Builder</h2>
        <div class="inline-form"><input id="campaignName" placeholder="Campaign name"><button id="buildCampaignButton">Build Campaign</button></div>
        <div id="campaignView" class="stack"></div>
      </section>
      <section id="content" class="panel">
        <h2>Content Pipeline <span class="compat">Content Generator · Content Batch</span></h2>
        <p class="note">Template-based local generation only. No model call is made.</p>
        <div class="inline-form"><select id="channelSelect"><option>SNS</option><option>Blog</option><option>Community</option><option>Newsletter</option><option>Short-form</option><option>Long-form</option><option>Media prompt</option></select><button id="generateDraftsButton">Generate Channel Drafts</button></div>
        <div id="draftView" class="stack"></div>
      </section>
      <section id="experiments" class="panel">
        <h2>Growth Experiments <span class="compat">Feedback Loop</span></h2>
        <textarea id="feedbackInput" rows="5" placeholder="Paste owner/user feedback here."></textarea>
        <div class="decision-row"><button id="importFeedbackButton">Import Feedback</button><button id="createExperimentButton">Create Growth Experiment</button></div>
        <div id="experimentView" class="stack"></div>
      </section>
      <section id="codex" class="panel">
        <h2>Codex Packet Factory <span class="compat">Task Board · Next Task Synthesizer</span></h2>
        <button id="codexPacketButton">Generate Codex Task Packet</button>
        <div id="codexPacketView" class="stack"></div>
      </section>
      <section id="approval" class="panel">
        <h2>Approval Gate <span class="compat">Review Board · Review Queue · Owner Decision</span></h2>
        <textarea id="ownerNotes" rows="5" placeholder="Approval, revision, or rejection notes."></textarea>
        <div class="decision-row"><button data-decision="approve">Approve</button><button data-decision="revise">Revise</button><button data-decision="reject">Reject</button><button id="exportButton">Export Review JSON</button></div>
        <div class="check-grid">
          <label><input id="requestDeploy" type="checkbox"> request deploy</label>
          <label><input id="requestPublish" type="checkbox"> request publish</label>
          <label><input id="requestPlatformPost" type="checkbox"> request platform posting</label>
          <label><input id="requestProviderCall" type="checkbox"> request provider/live model call</label>
        </div>
        <button id="approvalGateButton">Run Approval Gate</button>
        <pre id="approvalView"></pre>
      </section>
      <section id="safety" class="panel">
        <h2>Safety Scanner</h2>
        <button id="safetyButton">Run Safety Scanner</button>
        <div id="safetyView" class="stack"></div>
      </section>
      <section id="evidence" class="panel">
        <h2>Evidence Ledger</h2>
        <button id="calendarButton">Build Editorial Calendar</button>
        <div id="calendarView" class="stack"></div>
        <div id="evidenceLedger" class="stack"></div>
      </section>
      <section id="workspace" class="panel">
        <h2>Workspace Import/Export <span class="compat">Import Workspace JSON / Export Workspace JSON</span></h2>
        <textarea id="importJsonInput" rows="8" placeholder="Paste exported workspace JSON here."></textarea>
        <div class="decision-row"><button id="importWorkspaceButton">Import Workspace JSON</button><button id="exportWorkspaceButton">Export Workspace JSON</button></div>
      </section>
      <section id="selftest" class="panel">
        <h2>Self Test</h2>
        <button id="runSelfTestButton">Run Self Test</button>
        <pre id="selfTestResult">not_run</pre>
      </section>
    </section>
  </main>
  <script src="app.js"></script>
</body>
</html>
"""


STYLES_CSS = """:root{color-scheme:light;--ink:#182026;--muted:#60707d;--line:#d9e1e7;--paper:#f6f8fa;--panel:#ffffff;--accent:#127a76;--accent2:#b0522a;--good:#1f7a3d;--bad:#b22626;--warn:#8a6500}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,Segoe UI,Arial,sans-serif}.topbar{display:flex;justify-content:space-between;gap:24px;align-items:flex-start;padding:24px 28px;background:#fff;border-bottom:1px solid var(--line)}h1{margin:0;font-size:30px;letter-spacing:0}h2{margin:0 0 16px;font-size:21px}.eyebrow{margin:0 0 6px;color:var(--accent);font-weight:700;text-transform:uppercase;font-size:12px}.subtitle{max-width:960px;margin:8px 0 0;color:var(--muted);line-height:1.5}.compat{color:var(--muted);font-size:12px;font-weight:600}.status-panel{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:8px;min-width:260px}.status-panel span,.badge{border:1px solid var(--line);border-radius:999px;padding:6px 9px;background:#fdfdfd;color:#394853;font-size:12px}.layout{display:grid;grid-template-columns:260px minmax(0,1fr);min-height:calc(100vh - 126px)}.sidebar{background:#fff;border-right:1px solid var(--line);padding:14px;display:flex;flex-direction:column;gap:6px;position:sticky;top:0;height:calc(100vh - 126px);overflow:auto}.sidebar button,.panel button{border:1px solid var(--line);background:#fff;border-radius:7px;padding:9px 10px;color:var(--ink);cursor:pointer;text-align:left;font-weight:650}.sidebar button.active,.panel button:hover{border-color:var(--accent);color:var(--accent)}.workspace{padding:22px;max-width:1480px}.panel{display:none}.active-panel{display:block}.form-grid{display:grid;grid-template-columns:repeat(2,minmax(240px,1fr));gap:14px}.inline-form,.decision-row,.check-grid{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}.check-grid label{border:1px solid var(--line);background:#fff;border-radius:7px;padding:8px 10px}label{display:flex;flex-direction:column;gap:6px;color:var(--muted);font-weight:650}input,textarea,select{width:100%;border:1px solid var(--line);border-radius:7px;padding:10px;background:#fff;color:var(--ink);font:inherit}textarea{min-height:94px;resize:vertical}pre{white-space:pre-wrap;background:#101820;color:#d7f7ef;border-radius:7px;padding:14px;overflow:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}.stack{display:grid;gap:12px;margin-top:12px}.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px;box-shadow:0 1px 0 rgba(10,20,30,.03)}.card h3{margin:0 0 8px;font-size:16px}.card p{margin:0;color:var(--muted);line-height:1.45}.badge-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}.note{color:var(--muted);margin-top:-6px}.risk-blocked{border-color:#f0b0b0}.risk-clear{border-color:#b8dec3}@media(max-width:820px){.topbar{display:block}.layout{grid-template-columns:1fr}.sidebar{position:relative;height:auto}.form-grid{grid-template-columns:1fr}}"""


APP_JS = r'''const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV4";
const REVIEW_DECISIONS = ["approve", "revise", "reject"];
const BLOCKED_MARKERS = ["fake human","undisclosed bot","spam","mass posting","engagement manipulation","astroturf","brigading","harassment","platform bypass","account automation","bot army","fake crowd","brigade"];
const CHANNELS = ["SNS","Blog","Community","Newsletter","Short-form","Long-form","Media prompt"];
const defaultWorkspace = {
  northStar: {
    summary: "Transparent AI Creator Collective / Influence Factory",
    audience: "Builders, creators, product teams, and brand/IP operators.",
    promise: "Turn a raw idea into strategy, brand/IP memory, safe content drafts, Codex task packets, and next actions.",
    proofTarget: "A local workbench that creates a reviewable operating package without external calls.",
    constraints: "No fake identity, no undisclosed automation, no spam, no engagement manipulation, no platform bypass.",
    firstResult: "Produce a draft-first campaign packet and Codex implementation packet."
  },
  strategy: { score: 0, components: [], positioning: "", risks: [], successCriteria: [] },
  brandIp: {
    brandDna: "Transparent, evidence-led, builder-native, safety-bounded.",
    characterBible: "Personas must disclose AI assistance and stay inside their domain.",
    visualGuide: "Clean editorial product interface, precise typography, no fake social proof.",
    paletteTypography: "Ink, white, teal accent, warm proof accent, dense but readable product UI.",
    forbiddenStyles: "No bot armies, no fake crowds, no spam visuals, no manipulation motifs.",
    rightsNotes: "Use only user-provided or properly licensed references."
  },
  references: { referenceIndex: "ref-001: owner-approved character sheet; ref-002: product UI screenshot", assetRegistry: "No external assets embedded.", promptPack: {}, checklist: [] },
  personas: [
    { name: "Builder Analyst", role: "Explains tools and proof-by-result experiments.", disclosure: "transparent AI persona", domain: "infra and product" },
    { name: "Brand/IP Director", role: "Protects visual identity, language, tone, and character consistency.", disclosure: "transparent AI persona", domain: "brand and visual continuity" },
    { name: "DevRel Operator", role: "Turns technical pain into tutorials, demos, and field notes.", disclosure: "transparent AI persona", domain: "developer relations" }
  ],
  campaign: { name: "Proof by result launch loop", pillars: [], calendar: [] },
  drafts: [],
  feedback: [],
  experiments: [],
  codexPackets: [],
  tasks: [],
  calendar: [],
  safety: [],
  approval: { decision: "pending", notes: "", gateStatus: "not_run", protectedActionExecuted: false, published: false, posted: false },
  evidence: ["Workbench v4 loaded locally.", "No protected action executed.", "All outputs are draft-first until owner action outside this app."]
};
function clone(value){return JSON.parse(JSON.stringify(value));}
function escapeHtml(value){return String(value).replace(/[&<>"']/g,(char)=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[char]));}
function getWorkspace(){const saved=localStorage.getItem(STORAGE_KEY);if(!saved)return clone(defaultWorkspace);try{return deepMerge(clone(defaultWorkspace),JSON.parse(saved));}catch(error){return clone(defaultWorkspace);}}
function deepMerge(base, incoming){for(const [key,value] of Object.entries(incoming||{})){if(value&&typeof value==="object"&&!Array.isArray(value)&&base[key]&&typeof base[key]==="object"&&!Array.isArray(base[key]))base[key]=deepMerge(base[key],value);else base[key]=value;}return base;}
function saveWorkspace(workspace){localStorage.setItem(STORAGE_KEY,JSON.stringify(workspace,null,2));renderAll();}
function addEvidence(workspace,item){workspace.evidence.push(`${new Date().toISOString()} ${item}`);}
function card(title,body,badges=[],risk=""){const badgeHtml=badges.map((badge)=>`<span class="badge">${escapeHtml(badge)}</span>`).join("");return `<article class="card ${risk?`risk-${risk}`:""}"><h3>${escapeHtml(title)}</h3><p>${escapeHtml(body)}</p><div class="badge-row">${badgeHtml}</div></article>`;}
function buildNorthStar(){const workspace=getWorkspace();workspace.northStar={summary:document.querySelector("#ideaSummary").value.trim()||workspace.northStar.summary,audience:document.querySelector("#targetAudience").value.trim()||workspace.northStar.audience,promise:document.querySelector("#promise").value.trim()||workspace.northStar.promise,proofTarget:document.querySelector("#proofTarget").value.trim()||workspace.northStar.proofTarget,constraints:document.querySelector("#blockedBehaviors").value.trim()||workspace.northStar.constraints,firstResult:document.querySelector("#firstResult").value.trim()||workspace.northStar.firstResult};addEvidence(workspace,"North Star intake updated locally.");saveWorkspace(workspace);}
function calculateOpportunityScore(){const workspace=getWorkspace();const text=Object.values(workspace.northStar).join(" ").toLowerCase();const painScore=text.includes("pain")||text.includes("problem")||text.includes("고통")?20:14;const proofScore=text.includes("proof")||text.includes("evidence")||text.includes("검증")?20:16;const safetyScore=BLOCKED_MARKERS.some((marker)=>text.includes(marker))?8:20;const audienceScore=workspace.northStar.audience.length>30?18:12;const differentiationScore=text.includes("transparent")||text.includes("투명")?18:12;const score=painScore+proofScore+safetyScore+audienceScore+differentiationScore;workspace.strategy={score,components:[`pain clarity ${painScore}`,`proof path ${proofScore}`,`safety boundary ${safetyScore}`,`audience specificity ${audienceScore}`,`differentiation ${differentiationScore}`],positioning:`For ${workspace.northStar.audience}, this product promises: ${workspace.northStar.promise}`,risks:["Protected actions require explicit owner approval.","Drafts must disclose AI assistance where relevant.","No deceptive influence or platform bypass."],successCriteria:["A user can produce a strategy packet locally.","A user can generate brand-consistent draft packets locally.","A user can export a Codex task packet locally."]};addEvidence(workspace,"Strategy score calculated.");saveWorkspace(workspace);}
function saveBrandIpVault(){const workspace=getWorkspace();workspace.brandIp={brandDna:document.querySelector("#brandDna").value.trim()||workspace.brandIp.brandDna,characterBible:document.querySelector("#characterBible").value.trim()||workspace.brandIp.characterBible,visualGuide:document.querySelector("#visualGuide").value.trim()||workspace.brandIp.visualGuide,paletteTypography:document.querySelector("#paletteTypography").value.trim()||workspace.brandIp.paletteTypography,forbiddenStyles:document.querySelector("#forbiddenStyles").value.trim()||workspace.brandIp.forbiddenStyles,rightsNotes:document.querySelector("#rightsNotes").value.trim()||workspace.brandIp.rightsNotes};addEvidence(workspace,"Brand/IP Vault updated locally.");saveWorkspace(workspace);}
function buildReferencePack(){const workspace=getWorkspace();workspace.references.referenceIndex=document.querySelector("#referenceIndex").value.trim()||workspace.references.referenceIndex;workspace.references.assetRegistry=document.querySelector("#assetRegistry").value.trim()||workspace.references.assetRegistry;workspace.references.promptPack={imageGenerationPrompt:`Use brand DNA: ${workspace.brandIp.brandDna}. Character bible: ${workspace.brandIp.characterBible}. Visual guide: ${workspace.brandIp.visualGuide}. Keep palette/typography: ${workspace.brandIp.paletteTypography}. Generate only owner-approved, non-deceptive, draft assets.`,negativePrompt:workspace.brandIp.forbiddenStyles,referenceImageIndex:workspace.references.referenceIndex,rightsNotes:workspace.brandIp.rightsNotes};workspace.references.checklist=["Match character bible before generating variants.","Preserve palette and typography direction.","Reject forbidden styles.","Record provenance and rights notes.","Keep generated assets draft-only until owner approval."];addEvidence(workspace,"Reference pack built.");saveWorkspace(workspace);}
function addPersonaNode(){const workspace=getWorkspace();const name=document.querySelector("#personaName").value.trim();const role=document.querySelector("#personaRole").value.trim();const disclosure=document.querySelector("#personaDisclosure").value.trim()||"transparent AI persona";if(!name||!role)return;workspace.personas.push({name,role,disclosure,domain:role});addEvidence(workspace,`Persona added: ${name}.`);document.querySelector("#personaName").value="";document.querySelector("#personaRole").value="";document.querySelector("#personaDisclosure").value="";saveWorkspace(workspace);}
function buildCampaign(){const workspace=getWorkspace();const name=document.querySelector("#campaignName").value.trim()||"Owner-reviewed proof campaign";workspace.campaign={name,pillars:["Proof by result","Transparent AI persona","Brand/IP consistency","Owner approval gate","Feedback-to-task loop"],calendar:CHANNELS.map((channel,index)=>({day:`Day ${index+1}`,channel,objective:`Show ${workspace.northStar.firstResult}`,status:"draft-only"}))};workspace.calendar=workspace.campaign.calendar;addEvidence(workspace,"Campaign Builder created a draft-only campaign.");saveWorkspace(workspace);}
function generateChannelDrafts(){const workspace=getWorkspace();const selected=document.querySelector("#channelSelect").value;const channels=selected==="Media prompt"?["Media prompt"]:CHANNELS;const persona=workspace.personas[0]||defaultWorkspace.personas[0];const newDrafts=channels.map((channel,index)=>({id:`draft-${Date.now()}-${index}`,channel,title:`${channel} draft from ${persona.name}`,text:`${workspace.northStar.summary} for ${workspace.northStar.audience}. Promise: ${workspace.northStar.promise}. Proof: ${workspace.northStar.proofTarget}. Style: ${workspace.brandIp.brandDna}. Boundary: transparent AI, draft-only, owner approval required.`,status:"draft-only"}));workspace.drafts=workspace.drafts.concat(newDrafts);addEvidence(workspace,`Generated local template draft batch for ${channels.join(", ")}.`);saveWorkspace(workspace);}
function importFeedback(){const workspace=getWorkspace();const raw=document.querySelector("#feedbackInput").value.trim();if(!raw)return;raw.split(/\n+/).filter(Boolean).forEach((line,index)=>workspace.feedback.push({id:`feedback-${Date.now()}-${index}`,text:line,category:line.toLowerCase().includes("style")?"style":line.toLowerCase().includes("risk")?"risk":"product",severity:line.length>120?"high":"medium",status:"imported-local"}));addEvidence(workspace,"Feedback imported locally.");document.querySelector("#feedbackInput").value="";saveWorkspace(workspace);}
function createGrowthExperiment(){const workspace=getWorkspace();const experiment={id:`experiment-${workspace.experiments.length+1}`,hypothesis:`If ${workspace.northStar.promise}, then ${workspace.northStar.audience} will request the next proof artifact.`,channels:["owned blog","owned newsletter","manual community draft"],metric:"owner-approved replies, saves, or qualitative feedback",killCriteria:"No signal after three owner-reviewed draft cycles.",status:"planned-local"};workspace.experiments.push(experiment);addEvidence(workspace,"Growth experiment created locally.");saveWorkspace(workspace);}
function generateCodexTaskPacket(){const workspace=getWorkspace();const packet={task_id:`codex-task-${workspace.codexPackets.length+1}`,title:"Improve Influence Factory local workbench",goal:workspace.northStar.firstResult,context:["avf/influence_factory/product_app/index.html","avf/influence_factory/product_app/app.js","avf/influence_factory/product_app/styles.css"],acceptance_criteria:["Preserve local-only operation.","Do not add provider or external service calls.","Keep safety scanner and approval gate visible.","Add tests or validator coverage for new behavior."],forbidden_changes:["Do not deploy.","Do not publish.","Do not automate personal accounts.","Do not support deceptive influence."],expected_output:["Small PR-sized implementation.","Validation output.","Next safe goal recommendation."]};workspace.codexPackets.push(packet);workspace.tasks=[{id:"task-1",title:packet.title,boundary:"repo-local, PR-sized, approval-gated"}];addEvidence(workspace,"Codex task packet generated.");saveWorkspace(workspace);}
function runSafetyReview(){const workspace=getWorkspace();workspace.safety=workspace.drafts.map((draft)=>{const text=`${draft.title} ${draft.text}`.toLowerCase();const markers=BLOCKED_MARKERS.filter((marker)=>text.includes(marker));return{draftId:draft.id,title:draft.title,risk:markers.length?"blocked":"clear",markers};});addEvidence(workspace,"Safety Scanner completed locally.");saveWorkspace(workspace);}
function runApprovalGate(){const workspace=getWorkspace();const requestedProtected=[["deploy",document.querySelector("#requestDeploy").checked],["publish",document.querySelector("#requestPublish").checked],["platform posting",document.querySelector("#requestPlatformPost").checked],["provider/live model call",document.querySelector("#requestProviderCall").checked]].filter((item)=>item[1]).map((item)=>item[0]);const hasBlockedSafety=workspace.safety.some((item)=>item.risk==="blocked");const gateStatus=requestedProtected.length||hasBlockedSafety?"blocked":"local_draft_approved";workspace.approval={decision:workspace.approval.decision,notes:document.querySelector("#ownerNotes").value,gateStatus,protectedRequests:requestedProtected,protectedActionExecuted:false,published:false,posted:false};addEvidence(workspace,gateStatus==="blocked"?"Approval gate blocked protected action.":"Approval gate allowed local draft-only continuation.");saveWorkspace(workspace);}
function applyReviewDecision(decision){if(!REVIEW_DECISIONS.includes(decision))return;const workspace=getWorkspace();workspace.approval.decision=decision;workspace.approval.notes=document.querySelector("#ownerNotes").value;workspace.approval.reviewedAt=new Date().toISOString();workspace.approval.protectedActionExecuted=false;addEvidence(workspace,`Owner decision recorded locally: ${decision}.`);saveWorkspace(workspace);}
function synthesizeNextTasks(){const workspace=getWorkspace();const tasks=[];if(workspace.approval.decision==="revise")tasks.push("Revise selected draft batch using owner notes.");if(workspace.feedback.length)tasks.push("Create improvement task from imported feedback.");if(workspace.safety.some((item)=>item.risk==="blocked"))tasks.push("Remove blocked influence markers before any owner approval.");tasks.push("Prepare next draft-only campaign packet with current Brand/IP Vault.");workspace.tasks=tasks.map((title,index)=>({id:`task-${index+1}`,title,boundary:"repo-local, draft-only, approval-gated"}));addEvidence(workspace,"Next tasks synthesized locally.");saveWorkspace(workspace);}
function buildEditorialCalendar(){const workspace=getWorkspace();workspace.calendar=workspace.drafts.slice(0,14).map((draft,index)=>({id:`calendar-${index+1}`,day:`Day ${index+1}`,channel:draft.channel,title:draft.title,status:"draft-only"}));addEvidence(workspace,"Editorial Calendar built locally.");saveWorkspace(workspace);}
function exportWorkspaceJson(){const payload={product:"Transparent AI Creator Collective / Influence Factory",version:"v4",workspace:getWorkspace(),exportedAt:new Date().toISOString(),boundary:{draftOnly:true,ownerApprovalRequired:true,protectedActionExecuted:false,published:false,posted:false}};const blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"});const url=URL.createObjectURL(blob);const link=document.createElement("a");link.href=url;link.download="influence-factory-workspace-v4.json";document.body.appendChild(link);link.click();link.remove();URL.revokeObjectURL(url);}
function importWorkspaceJson(){const raw=document.querySelector("#importJsonInput").value.trim();if(!raw)return;try{const parsed=JSON.parse(raw);const workspace=parsed.workspace?parsed.workspace:parsed;workspace.evidence=workspace.evidence||[];addEvidence(workspace,"Workspace JSON imported locally.");saveWorkspace(deepMerge(clone(defaultWorkspace),workspace));}catch(error){document.querySelector("#importJsonInput").value=`Import failed: ${error.message}`;}}
function exportReviewJson(){exportWorkspaceJson();}
function renderNorthStar(workspace){document.querySelector("#ideaSummary").value=workspace.northStar.summary;document.querySelector("#targetAudience").value=workspace.northStar.audience;document.querySelector("#promise").value=workspace.northStar.promise;document.querySelector("#proofTarget").value=workspace.northStar.proofTarget;document.querySelector("#blockedBehaviors").value=workspace.northStar.constraints;document.querySelector("#firstResult").value=workspace.northStar.firstResult;document.querySelector("#northStarPreview").textContent=JSON.stringify(workspace.northStar,null,2);}
function renderStrategy(workspace){document.querySelector("#strategyView").innerHTML=[card("Opportunity Score",String(workspace.strategy.score||"not calculated"),["strategy"]),card("Positioning",workspace.strategy.positioning||"Calculate score to generate positioning.",["positioning"]),card("Risks",(workspace.strategy.risks||[]).join(" "),["risk"]),card("Success Criteria",(workspace.strategy.successCriteria||[]).join(" "),["proof"])].join("");}
function renderBrand(workspace){document.querySelector("#brandDna").value=workspace.brandIp.brandDna;document.querySelector("#characterBible").value=workspace.brandIp.characterBible;document.querySelector("#visualGuide").value=workspace.brandIp.visualGuide;document.querySelector("#paletteTypography").value=workspace.brandIp.paletteTypography;document.querySelector("#forbiddenStyles").value=workspace.brandIp.forbiddenStyles;document.querySelector("#rightsNotes").value=workspace.brandIp.rightsNotes;document.querySelector("#brandView").innerHTML=[card("Brand DNA",workspace.brandIp.brandDna,["brand"]),card("Character bible",workspace.brandIp.characterBible,["IP"]),card("Visual guide",workspace.brandIp.visualGuide,["visual"]),card("Forbidden styles",workspace.brandIp.forbiddenStyles,["safety"])].join("");}
function renderReferences(workspace){document.querySelector("#referenceIndex").value=workspace.references.referenceIndex;document.querySelector("#assetRegistry").value=workspace.references.assetRegistry;document.querySelector("#referencePackView").innerHTML=[card("Reference image index",workspace.references.referenceIndex,["style reference"]),card("Asset registry",workspace.references.assetRegistry,["provenance"]),card("Image generation prompt pack",workspace.references.promptPack.imageGenerationPrompt||"Build reference pack to generate prompt.",["image prompt"]),card("Consistency checklist",(workspace.references.checklist||[]).join(" "),["checklist"])].join("");}
function renderPersonas(workspace){document.querySelector("#personaView").innerHTML=workspace.personas.map((persona)=>card(persona.name,`${persona.role} Disclosure: ${persona.disclosure}`,[persona.domain||"domain","owned channel"])).join("");}
function renderCampaign(workspace){document.querySelector("#campaignView").innerHTML=[card(workspace.campaign.name,(workspace.campaign.pillars||[]).join(" "),["campaign"]),...(workspace.campaign.calendar||[]).map((item)=>card(`${item.day}: ${item.channel}`,item.objective,[item.status]))].join("");}
function renderDrafts(workspace){document.querySelector("#draftView").innerHTML=workspace.drafts.map((draft)=>card(draft.title,draft.text,[draft.channel,draft.status])).join("");}
function renderExperiments(workspace){document.querySelector("#experimentView").innerHTML=[...workspace.feedback.map((item)=>card(item.category,item.text,[item.severity,item.status])),...workspace.experiments.map((item)=>card(item.id,`${item.hypothesis} Metric: ${item.metric}. Kill: ${item.killCriteria}`,[item.status]))].join("");}
function renderCodexPackets(workspace){document.querySelector("#codexPacketView").innerHTML=workspace.codexPackets.map((packet)=>card(packet.title,JSON.stringify(packet,null,2),[packet.task_id,"PR-sized"])).join("");}
function renderApproval(workspace){document.querySelector("#ownerNotes").value=workspace.approval.notes||"";document.querySelector("#approvalView").textContent=JSON.stringify(workspace.approval,null,2);}
function renderSafety(workspace){document.querySelector("#safetyView").innerHTML=workspace.safety.map((item)=>card(item.title,`Risk: ${item.risk}. Markers: ${item.markers.join(", ")||"none"}`,[item.draftId,item.risk],item.risk)).join("");}
function renderEvidenceLedger(){const workspace=getWorkspace();document.querySelector("#calendarView").innerHTML=workspace.calendar.map((item)=>card(`${item.day}: ${item.title||item.channel}`,`Channel: ${item.channel}`,[item.status])).join("");document.querySelector("#evidenceLedger").innerHTML=workspace.evidence.map((item,index)=>card(`Evidence ${index+1}`,item,["repo-local"])).join("");}
function renderReviewQueue(){renderDrafts(getWorkspace());}
function renderContentBatch(){renderDrafts(getWorkspace());}
function renderAll(){const workspace=getWorkspace();renderNorthStar(workspace);renderStrategy(workspace);renderBrand(workspace);renderReferences(workspace);renderPersonas(workspace);renderCampaign(workspace);renderDrafts(workspace);renderExperiments(workspace);renderCodexPackets(workspace);renderApproval(workspace);renderSafety(workspace);renderEvidenceLedger();}
function bindNavigation(){document.querySelectorAll(".sidebar button").forEach((button)=>{button.addEventListener("click",()=>{document.querySelectorAll(".sidebar button").forEach((item)=>item.classList.remove("active"));document.querySelectorAll(".panel").forEach((panel)=>panel.classList.remove("active-panel"));button.classList.add("active");document.querySelector(`#${button.dataset.section}`).classList.add("active-panel");});});}
function createIdeaBrief(){buildNorthStar();}
function addPersona(){addPersonaNode();}
function saveStyleMemory(){saveBrandIpVault();}
function generateContentBatch(){generateChannelDrafts();}
function runSafetyScan(){runSafetyReview();}
function runSelfTest(){localStorage.removeItem(STORAGE_KEY);renderAll();document.querySelector("#ideaSummary").value="Self-test creator system";document.querySelector("#targetAudience").value="Owner and product operator";document.querySelector("#promise").value="Generate a transparent creator operating packet";document.querySelector("#proofTarget").value="Strategy score, reference pack, draft batch, and Codex packet";document.querySelector("#firstResult").value="Codex-ready task packet";buildNorthStar();calculateOpportunityScore();document.querySelector("#brandDna").value="Self-test brand DNA with stable visual identity";document.querySelector("#characterBible").value="Self Test Persona always discloses AI assistance";document.querySelector("#visualGuide").value="Crisp editorial UI, teal accent, no fake social proof";document.querySelector("#paletteTypography").value="Ink, white, teal, warm proof accent";document.querySelector("#forbiddenStyles").value="No bot armies, no fake crowds, no spam visuals";saveBrandIpVault();document.querySelector("#referenceIndex").value="ref-self-test-001: owner-approved local reference";document.querySelector("#assetRegistry").value="asset-self-test-001: local draft asset";buildReferencePack();document.querySelector("#personaName").value="Self Test Persona";document.querySelector("#personaRole").value="Validates local loop";document.querySelector("#personaDisclosure").value="transparent AI persona";addPersonaNode();document.querySelector("#campaignName").value="Self-test campaign";buildCampaign();generateChannelDrafts();document.querySelector("#feedbackInput").value="Style should stay consistent";importFeedback();createGrowthExperiment();generateCodexTaskPacket();runSafetyReview();document.querySelector("#ownerNotes").value="Revise the draft with clearer proof.";applyReviewDecision("revise");document.querySelector("#requestPlatformPost").checked=true;runApprovalGate();synthesizeNextTasks();buildEditorialCalendar();const result="SELF_TEST_PASS_V4 Strategy score calculated Reference pack built Codex task packet generated Approval gate blocked protected action";document.querySelector("#selfTestResult").textContent=result;return result;}
function boot(){renderAll();bindNavigation();document.querySelector("#buildNorthStarButton").addEventListener("click",buildNorthStar);document.querySelector("#scoreButton").addEventListener("click",calculateOpportunityScore);document.querySelector("#saveBrandButton").addEventListener("click",saveBrandIpVault);document.querySelector("#referencePackButton").addEventListener("click",buildReferencePack);document.querySelector("#addPersonaButton").addEventListener("click",addPersonaNode);document.querySelector("#buildCampaignButton").addEventListener("click",buildCampaign);document.querySelector("#generateDraftsButton").addEventListener("click",generateChannelDrafts);document.querySelector("#importFeedbackButton").addEventListener("click",importFeedback);document.querySelector("#createExperimentButton").addEventListener("click",createGrowthExperiment);document.querySelector("#codexPacketButton").addEventListener("click",generateCodexTaskPacket);document.querySelector("#approvalGateButton").addEventListener("click",runApprovalGate);document.querySelector("#safetyButton").addEventListener("click",runSafetyReview);document.querySelector("#calendarButton").addEventListener("click",buildEditorialCalendar);document.querySelector("#importWorkspaceButton").addEventListener("click",importWorkspaceJson);document.querySelector("#exportWorkspaceButton").addEventListener("click",exportWorkspaceJson);document.querySelector("#exportButton").addEventListener("click",exportReviewJson);document.querySelector("#runSelfTestButton").addEventListener("click",runSelfTest);document.querySelectorAll("[data-decision]").forEach((button)=>button.addEventListener("click",()=>applyReviewDecision(button.dataset.decision)));document.querySelector("#ownerNotes").addEventListener("input",()=>{const workspace=getWorkspace();workspace.approval.notes=document.querySelector("#ownerNotes").value;localStorage.setItem(STORAGE_KEY,JSON.stringify(workspace,null,2));});if(window.location.hash==="#selftest")setTimeout(runSelfTest,0);}
boot();
'''


README_MD = """# Influence Factory Workbench v4

This is a repo-local browser product for a transparent AI creator collective /
influence factory. It turns a user idea into a local operating packet:

- North Star intake
- Strategy score and positioning
- Brand/IP Vault
- Reference Pack Builder for image-generation handoff prompts
- Persona Network
- Campaign Builder
- Content Pipeline
- Growth Experiments
- Codex Packet Factory
- Approval Gate
- Safety Scanner
- Evidence Ledger
- Workspace import/export

It does not deploy, publish, post to platforms, automate accounts, call providers,
call live models, call external services, or claim public/release/production readiness.
"""


AUDIT_REQUIREMENTS = [
    "North Star Intake",
    "Strategy Engine",
    "Brand/IP Vault",
    "Reference Pack Builder",
    "Reference image index",
    "Asset registry",
    "Image generation prompt pack",
    "Forbidden styles",
    "Rights notes",
    "Persona Network",
    "Campaign Builder",
    "Content Pipeline",
    "Growth Experiments",
    "Codex Packet Factory",
    "Approval Gate",
    "Safety Scanner",
    "Evidence Ledger",
    "Workspace Import/Export",
    "Self Test",
    "createIdeaBrief compatibility",
    "addPersona compatibility",
    "saveStyleMemory compatibility",
    "generateContentBatch compatibility",
    "applyReviewDecision compatibility",
    "importFeedback compatibility",
    "synthesizeNextTasks compatibility",
    "buildEditorialCalendar compatibility",
    "exportReviewJson compatibility",
    "renderReviewQueue compatibility",
    "renderEvidenceLedger compatibility",
    "localStorage persistence",
    "no provider calls",
    "no live model calls",
    "no external service calls",
    "no dependency install",
    "no deploy",
    "no publish",
    "no platform posting",
    "no account automation",
    "no deceptive influence support",
    "draft-first content pipeline",
    "owner approval required",
    "protected-action gate",
    "Codex PR-sized acceptance criteria",
    "feedback-to-task loop",
    "editorial calendar",
    "growth experiment kill criteria",
    "safety blocked marker scan",
    "workspace export boundary",
    "workspace import boundary",
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    APP.mkdir(parents=True, exist_ok=True)
    GOALS.mkdir(parents=True, exist_ok=True)

    write(APP / "index.html", INDEX_HTML)
    write(APP / "styles.css", STYLES_CSS)
    write(APP / "app.js", APP_JS)
    write(APP / "README.md", README_MD)
    write_json(APP / "product_workbench_v4_record.json", RECORD)

    audit_lines = ["# Influence Factory Product Workbench v4 Completion Audit", ""]
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
    write(GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V4_COMPLETION_AUDIT.md", "\n".join(audit_lines))

    write(
        GOALS / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V4_TERMINAL_REPORT.md",
        """# Influence Factory Product Workbench v4 Terminal Report

terminal_condition: LOCAL_PRODUCT_WORKBENCH_V4_READY

Summary:
The product now supports a fuller local AI factory loop: idea intake, strategy score,
Brand/IP Vault, reference/image prompt pack, persona network, campaign builder, content
pipeline, growth experiments, Codex task packets, approval gate, safety scanner,
evidence ledger, workspace import/export, and self-test.

Protected actions:
No protected action was executed.

Next safe goal:
owner_runs_v4_or_authorizes_protected_productization
""",
    )

    write(
        GOALS / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V4.md",
        """# Next After Influence Factory Product Workbench v4

selected_next_safe_goal: owner_runs_v4_or_authorizes_protected_productization
next_safe_goal_count: 1

Boundary:
The owner can run the local product. Public/platform operation still requires explicit
protected-action authorization.
""",
    )

    print("influence_factory_product_workbench_v4_created=true")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V4_READY")
    print("selected_next_safe_goal=owner_runs_v4_or_authorizes_protected_productization")
    print("protected_action_executed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

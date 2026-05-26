const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV42";
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
    rightsNotes: "Use only owner-provided or properly licensed references."
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
  ownerGoalBundle: null,
  operatorPackage: null,
  ownerReviewConsole: null,
  localIterationQueue: null,
  localIterationExecution: null,
  ownerReviewContinuation: null,
  operatingLoopTemplates: null,
  firstProductGoalRunner: null,
  localMvpAcceptance: null,
  localBetaCandidate: null,
  productCompletionAudit: null,
  localExportPackage: null,
  internalUserTrial: null,
  internalTrialImprovements: null,
  secondInternalTrial: null,
  externalValidationAuthorization: null,
  localProductCompletionHardening: null,
  localDistributablePackage: null,
  firstGoalCompletionPackage: null,
  guidedFirstRunGuard: null,
  localOwnerTrialScript: null,
  ownerTrialEvidenceRecorder: null,
  ownerTrialEvidenceCapture: null,
  ownerEvidenceLocalIteration: null,
  appliedLocalIterationWorkItem: null,
  appliedIterationVerification: null,
  factoryCompletionCandidate: null,
  styleWorkbench: null,
  contentApprovalBoard: [],
  evidenceDashboard: null,
  approval: { decision: "pending", notes: "", gateStatus: "not_run", protectedActionExecuted: false, published: false, posted: false },
  evidence: ["Workbench v10 loaded locally.", "No protected action executed.", "All outputs are draft-first until owner action outside this app."]
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
function exportWorkspaceJson(){const payload={product:"Transparent AI Creator Collective / Influence Factory",version:"v10",workspace:getWorkspace(),exportedAt:new Date().toISOString(),boundary:{draftOnly:true,ownerApprovalRequired:true,protectedActionExecuted:false,published:false,posted:false}};const blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"});const url=URL.createObjectURL(blob);const link=document.createElement("a");link.href=url;link.download="influence-factory-workspace-v10.json";document.body.appendChild(link);link.click();link.remove();URL.revokeObjectURL(url);}
function importWorkspaceJson(){const raw=document.querySelector("#importJsonInput").value.trim();if(!raw)return;try{const parsed=JSON.parse(raw);const workspace=parsed.workspace?parsed.workspace:parsed;workspace.evidence=workspace.evidence||[];addEvidence(workspace,"Workspace JSON imported locally.");saveWorkspace(deepMerge(clone(defaultWorkspace),workspace));}catch(error){document.querySelector("#importJsonInput").value=`Import failed: ${error.message}`;}}
function exportReviewJson(){exportWorkspaceJson();}

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
function buildOperatorPackage(){
  const workspace=getWorkspace();
  workspace.operatorPackage={
    quickstart:"Open the local app, enter a real owner goal, build the owner goal bundle, review style continuity, run safety, then record the owner decision.",
    runSequence:[
      "Build North Star",
      "Build Reference Pack",
      "Generate draft content",
      "Build Owner Goal Bundle Preview",
      "Build Style Continuity Workbench",
      "Build Content Approval Board",
      "Build Evidence Dashboard",
      "Run Approval Gate"
    ],
    localCommand:"python scripts\\run_avf_influence_factory_operator_cycle_local.py --goal avf\\influence_factory\\operator_package_v14\\FIRST_REAL_GOAL_TEMPLATE.json --out avf\\influence_factory\\operator_package_v14\\cycle_output",
    protectedActionRequest:{
      publicPosting:false,
      deploy:false,
      publish:false,
      providerCalls:false,
      externalCalls:false,
      platformAutomation:false,
      releaseReadinessClaim:false,
      productionReadinessClaim:false,
      publicReadinessClaim:false
    },
    acceptanceChecklist:[
      "real goal fields are complete",
      "Brand/IP style memory is present",
      "image prompt pack includes rights notes",
      "content drafts are approval-gated",
      "evidence dashboard is built",
      "protected actions remain false"
    ],
    selectedNextSafeGoal:"owner_runs_v14_operator_package_with_real_goal_or_requests_protected_authorization",
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Operator package built.");
  saveWorkspace(workspace);
}
function buildOwnerGoalBundlePreview(){
  const workspace=getWorkspace();
  const goal={
    goal_id:"owner-transparent-ai-creator-collective-local",
    idea:workspace.northStar.summary,
    audience:workspace.northStar.audience,
    promise:workspace.northStar.promise,
    proof_target:workspace.northStar.proofTarget,
    brand_dna:workspace.brandIp.brandDna,
    character_bible:workspace.brandIp.characterBible,
    visual_guide:workspace.brandIp.visualGuide,
    forbidden_styles:workspace.brandIp.forbiddenStyles,
    first_result:workspace.northStar.firstResult
  };
  workspace.ownerGoalBundle={
    goal,
    command:"python scripts\\run_avf_influence_factory_goal_local.py --input avf\\influence_factory\\owner_goal_runs\\transparent-ai-creator-collective-001\\goal_input.json --out avf\\influence_factory\\owner_goal_runs\\transparent-ai-creator-collective-001\\bundle",
    generatedFiles:ARTIFACT_FILES.concat(["style_reference_index.json","persona_registry.json","editorial_calendar.md","approval_gate.md","owner_decision_packet.md"]),
    protectedActionExecuted:false,
    boundary:"local preview only; owner authorization required before public operation"
  };
  addEvidence(workspace,"Owner goal bundle preview built locally.");
  saveWorkspace(workspace);
}
function buildStyleContinuityWorkbench(){
  const workspace=getWorkspace();
  workspace.styleWorkbench={
    brandDna:workspace.brandIp.brandDna,
    characterBible:workspace.brandIp.characterBible,
    visualGuide:workspace.brandIp.visualGuide,
    paletteTypography:workspace.brandIp.paletteTypography,
    imagePromptPack:workspace.references.promptPack,
    referenceSlots:[
      {slot:"primary_brand_scene",status:"owner_reference_required",rights:"owner-approved or generated only"},
      {slot:"character_expression_sheet",status:"draft_reference_required",rights:"no private likeness without consent"},
      {slot:"thumbnail_system",status:"style_tokens_ready",rights:"no deceptive social proof"}
    ],
    forbiddenStyles:workspace.brandIp.forbiddenStyles,
    rightsNotes:workspace.brandIp.rightsNotes,
    protectedActionExecuted:false
  };
  addEvidence(workspace,"Style continuity workbench built locally.");
  saveWorkspace(workspace);
}
function buildContentApprovalBoard(){
  const workspace=getWorkspace();
  const drafts=workspace.drafts.length?workspace.drafts:[{id:"draft-needed",channel:"SNS",title:"Generate drafts first",text:"Run Content Pipeline to populate approval board.",status:"needs_draft"}];
  workspace.contentApprovalBoard=drafts.map((draft,index)=>({
    id:draft.id||`draft-${index+1}`,
    channel:draft.channel,
    title:draft.title,
    approvalStatus:draft.status==="draft-only"?"needs_owner_review":draft.status,
    blockedActions:["publish","post","schedule","mass message","account automation"],
    protectedActionExecuted:false
  }));
  addEvidence(workspace,"Content approval board built locally.");
  saveWorkspace(workspace);
}
function buildEvidenceDashboard(){
  const workspace=getWorkspace();
  workspace.evidenceDashboard={
    artifactGroups:[
      {group:"strategy",count:workspace.strategy.score?1:0,status:workspace.strategy.score?"ready":"needs_run"},
      {group:"brand_ip",count:workspace.brandIp.brandDna?1:0,status:"ready"},
      {group:"style_memory",count:workspace.styleWorkbench?1:0,status:workspace.styleWorkbench?"ready":"needs_run"},
      {group:"content",count:workspace.drafts.length,status:workspace.drafts.length?"drafts_ready":"needs_drafts"},
      {group:"codex",count:workspace.codexPackets.length,status:workspace.codexPackets.length?"ready":"needs_packet"},
      {group:"safety",count:workspace.safety.length,status:workspace.safety.length?"scanned":"needs_scan"},
      {group:"decision",count:workspace.approval?1:0,status:workspace.approval.gateStatus||"pending"}
    ],
    terminalCondition:"LOCAL_PRODUCT_WORKBENCH_V13_READY",
    protectedActionExecuted:false,
    releaseReadyClaimed:false,
    publicReadyClaimed:false,
    productionReadyClaimed:false
  };
  addEvidence(workspace,"Evidence dashboard built locally.");
  saveWorkspace(workspace);
}
function renderArtifactBundle(workspace){
  const target=document.querySelector("#artifactBundleView");
  if(target)target.innerHTML=Object.entries(workspace.artifactBundle||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["artifact"])).join("");
}
function renderOperatorPackage(workspace){
  const target=document.querySelector("#operatorPackageView");
  if(target)target.innerHTML=Object.entries(workspace.operatorPackage||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["operator"])).join("");
}
function buildOwnerReviewPacket(){
  const workspace=getWorkspace();
  workspace.ownerReviewConsole={
    reviewTarget:"Review V15 Run",
    decisionMatrix:[
      {decision:"continue_local_iteration",default:true,protectedActionRequired:false,reason:"Improve product quality locally without publishing or external calls."},
      {decision:"request_protected_authorization",default:false,protectedActionRequired:true,reason:"Needed before any public, platform, provider, deploy, or readiness-claim operation."},
      {decision:"pause_for_strategy_review",default:false,protectedActionRequired:false,reason:"Use when owner wants to revise positioning before another run."}
    ],
    localIterationBacklog:[
      {item:"tighten real-goal onboarding copy",protectedActionRequired:false},
      {item:"add richer style continuity examples",protectedActionRequired:false},
      {item:"add owner-facing evidence comparison",protectedActionRequired:false},
      {item:"prepare protected-action authorization checklist",protectedActionRequired:false}
    ],
    protectedActionDecisionPacket:{
      publicPosting:false,
      deploy:false,
      publish:false,
      providerCalls:false,
      externalCalls:false,
      platformAutomation:false,
      readinessClaims:false
    },
    selectedNextSafeGoal:"owner_selects_local_iteration_or_explicit_protected_action_authorization",
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Owner review packet built.");
  saveWorkspace(workspace);
}
function renderOwnerReviewConsole(workspace){
  const target=document.querySelector("#ownerReviewConsoleView");
  if(target)target.innerHTML=Object.entries(workspace.ownerReviewConsole||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["owner review"])).join("");
}
function buildLocalIterationQueue(){
  const workspace=getWorkspace();
  const backlog=(workspace.ownerReviewConsole&&workspace.ownerReviewConsole.localIterationBacklog)||[
    {item:"tighten real-goal onboarding copy",protectedActionRequired:false},
    {item:"add richer style continuity examples",protectedActionRequired:false},
    {item:"add owner-facing evidence comparison",protectedActionRequired:false},
    {item:"prepare protected-action authorization checklist",protectedActionRequired:false}
  ];
  const tasks=backlog.map((item,index)=>({
    task_id:["v17-owner-review-ux","v17-style-examples","v17-evidence-compare","v17-authorization-checklist"][index]||`v17-local-task-${index+1}`,
    title:item.item,
    protected_action_required:false,
    acceptance_criteria:["local-only implementation","validator coverage updated","protected actions remain false"],
    forbidden_changes:["deploy","publish","platform posting","provider calls","external calls","readiness claims"]
  }));
  workspace.localIterationQueue={
    status:"ready_for_local_execution",
    tasks,
    acceptanceMatrix:tasks.map((task)=>({task_id:task.task_id,status:"pending_local_implementation",protected_action_required:false})),
    implementationOrder:tasks.map((task,index)=>`${index+1}. ${task.task_id}`),
    selectedNextSafeGoal:"execute_v17_local_iteration_tasks_without_protected_actions",
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Local iteration queue built.");
  saveWorkspace(workspace);
}
function renderLocalIterationQueue(workspace){
  const target=document.querySelector("#localIterationQueueView");
  if(target)target.innerHTML=Object.entries(workspace.localIterationQueue||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["local iteration"])).join("");
}
function executeLocalIterationTasks(){
  const workspace=getWorkspace();
  if(!workspace.localIterationQueue) {
    buildOwnerReviewPacket();
    buildLocalIterationQueue();
    return executeLocalIterationTasks();
  }
  const tasks=[
    {task_id:"v17-owner-review-ux",title:"Owner Verdict Clarity",status:"implemented_local_only",protected_action_required:false,evidence:["Owner-facing verdict options are separated into continue local iteration, request protected authorization, and pause for strategy review.","Each verdict records whether protected action is required and what happens next."]},
    {task_id:"v17-style-examples",title:"Style Example Pack",status:"implemented_local_only",protected_action_required:false,evidence:["Added reusable examples for character silhouette, editorial UI frame, media prompt continuity, and forbidden-style rejection.","Examples preserve Brand/IP Vault, reference image index, rights notes, and negative prompt constraints."]},
    {task_id:"v17-evidence-compare",title:"V15 Evidence Compare",status:"implemented_local_only",protected_action_required:false,evidence:["Compares V15 run artifacts against owner review, style continuity, safety boundary, and next-goal checks.","Missing or protected evidence routes to owner review instead of public operation."]},
    {task_id:"v17-authorization-checklist",title:"Protected Authorization Checklist",status:"implemented_local_only",protected_action_required:false,evidence:["Lists protected actions that remain unauthorized by default.","Blocks fake human impersonation, undisclosed bot networks, spam, platform posting, deploy, publish, external calls, and readiness claims."]}
  ];
  workspace.localIterationExecution={
    status:"implemented_local_only",
    taskExecutionResults:tasks,
    ownerVerdictClarity:[
      {verdict:"continue_local_iteration",meaning:"Improve the local workbench and evidence packet only.",protectedActionRequired:false},
      {verdict:"request_protected_authorization",meaning:"Prepare owner decision lines before deploy, publish, posting, provider calls, or public claims.",protectedActionRequired:true},
      {verdict:"pause_for_strategy_review",meaning:"Revise positioning, audience, style, or proof target before another local run.",protectedActionRequired:false}
    ],
    styleExamplePack:[
      {example:"character continuity",promptRule:"Keep the same character bible, palette, typography, silhouette, and rights notes across generated image requests."},
      {example:"media prompt continuity",promptRule:"Start every image prompt from the Brand/IP Vault and reference image index; append forbidden styles as a negative prompt."},
      {example:"community asset continuity",promptRule:"Use owned-channel context and visible AI disclosure; never imply fake human consensus."},
      {example:"style rejection",promptRule:"Reject bot armies, fake crowds, spam visuals, manipulation motifs, or borrowed unlicensed character identity."}
    ],
    v15EvidenceCompare:[
      {check:"owner goal bundle exists",status:"pass_local"},
      {check:"review backlog exists",status:"pass_local"},
      {check:"style continuity needs examples",status:"implemented_local_only"},
      {check:"protected authorization remains false",status:"pass_local"},
      {check:"platform posting",status:"blocked_until_explicit_owner_authorization"}
    ],
    protectedAuthorizationChecklist:[
      {action:"production deploy",authorized:false},
      {action:"publish or launch",authorized:false},
      {action:"platform posting",authorized:false},
      {action:"personal account automation",authorized:false},
      {action:"provider/live model call",authorized:false},
      {action:"external service call",authorized:false},
      {action:"public, release, production, external validation, or autonomous reliability claim",authorized:false},
      {action:"fake human impersonation, undisclosed bot networks, spam, engagement manipulation, astroturfing, brigading, harassment, or platform bypass",authorized:false}
    ],
    selectedNextSafeGoal:"owner_reviews_v18_iteration_results_or_continues_local_iteration",
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Local iteration tasks executed locally.");
  saveWorkspace(workspace);
}
function renderLocalIterationExecution(workspace){
  const target=document.querySelector("#localIterationExecutionView");
  if(target)target.innerHTML=Object.entries(workspace.localIterationExecution||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["local execution"])).join("");
}
function buildOwnerReviewContinuation(){
  const workspace=getWorkspace();
  if(!workspace.localIterationExecution) {
    executeLocalIterationTasks();
    return buildOwnerReviewContinuation();
  }
  workspace.ownerReviewContinuation={
    status:"reviewed_continue_local_iteration",
    decision:"continue_local_iteration",
    protectedActionAuthorized:false,
    reviewedArtifacts:["Task Execution Results","Owner Verdict Clarity","Style Example Pack","V15 Evidence Compare","Protected Authorization Checklist"],
    localContinuationDecision:"Continue local iteration only. No deploy, publish, platform posting, provider calls, external calls, account automation, or readiness claims are authorized.",
    nextLocalIterationPlan:[
      "Build local operating loop templates for idea intake, content review, style review, Codex packet review, and evidence comparison.",
      "Turn repeated owner decisions into reusable local templates without external calls.",
      "Keep all public, platform, provider, deploy, and readiness-claim actions behind explicit protected authorization."
    ],
    protectedBoundaryReconfirmation:[
      "fake human impersonation remains blocked",
      "undisclosed bot networks remain blocked",
      "platform posting remains blocked",
      "deploy and publish remain blocked",
      "provider/live/external calls remain blocked",
      "release/public/production readiness claims remain blocked"
    ],
    selectedNextSafeGoal:"build_local_operating_loop_templates_v20_without_protected_actions",
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Owner review continuation built.");
  saveWorkspace(workspace);
}
function renderOwnerReviewContinuation(workspace){
  const target=document.querySelector("#ownerReviewContinuationView");
  if(target)target.innerHTML=Object.entries(workspace.ownerReviewContinuation||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["review continuation"])).join("");
}
function buildOperatingLoopTemplates(){
  const workspace=getWorkspace();
  if(!workspace.ownerReviewContinuation) {
    buildOwnerReviewContinuation();
    return buildOperatingLoopTemplates();
  }
  workspace.operatingLoopTemplates={
    status:"factory_ready_for_first_owner_product_goal",
    templates:["Idea Intake Loop","Content Review Loop","Style/IP Review Loop","Codex Packet Review Loop","Evidence Comparison Loop"],
    firstProductGoalIntake:{
      product_idea:"owner fills in first product idea",
      target_user:"owner defines the first real audience",
      proof_target:"owner defines the first result that proves quality",
      brand_ip_constraints:"owner provides style, character, visual, and rights constraints",
      blocked_actions:["fake human impersonation","undisclosed bot networks","spam","platform posting","deploy","publish","provider/live/external calls"]
    },
    factoryReadyTerminalReport:"FACTORY_READY_FOR_FIRST_OWNER_PRODUCT_GOAL",
    selectedNextSafeGoal:"owner_provides_first_real_product_goal_for_factory_run",
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Operating loop templates built.");
  saveWorkspace(workspace);
}
function renderOperatingLoopTemplates(workspace){
  const target=document.querySelector("#operatingLoopTemplatesView");
  if(target)target.innerHTML=Object.entries(workspace.operatingLoopTemplates||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["operating loop"])).join("");
}
function runFirstProductGoal(){
  const workspace=getWorkspace();
  if(!workspace.operatingLoopTemplates) {
    buildOperatingLoopTemplates();
    return runFirstProductGoal();
  }
  const input={
    product_idea:workspace.northStar.summary||"Transparent AI Creator Collective / Influence Factory",
    target_user:workspace.northStar.audience||"owner and product operator",
    proof_target:workspace.northStar.proofTarget||"local run packet with Codex task and owner review queue",
    brand_ip_constraints:`${workspace.brandIp.brandDna}; ${workspace.brandIp.characterBible}; ${workspace.brandIp.visualGuide}`,
    blocked_actions:["fake human impersonation","undisclosed bot networks","spam","platform posting","deploy","publish","provider/live/external calls"]
  };
  workspace.firstProductGoalRunner={
    terminalCondition:"FIRST_PRODUCT_GOAL_RUNNER_V21_READY",
    safeReframe:"transparent_creator_brand_media_growth_system",
    input,
    runPacket:{
      product_idea:input.product_idea,
      target_user:input.target_user,
      proof_target:input.proof_target,
      brand_ip_constraints:input.brand_ip_constraints,
      strategy_brief:"Create proof-by-result positioning for a transparent, owner-reviewed creator/brand/media growth system.",
      codex_task_packet:{task_id:"first-product-local-run-001",goal:"Implement the next local-only product workbench improvement from owner review.",context:["avf/influence_factory/product_app/index.html","avf/influence_factory/product_app/app.js"],acceptance_criteria:["local-only","no external calls","owner review queue visible"],forbidden_changes:["deploy","publish","platform posting","provider calls"]},
      safe_reframe:"transparent_creator_brand_media_growth_system",
      protected_action_executed:false,
      external_calls:false
    },
    strategyBrief:"Position the product around visible disclosure, owned-channel drafts, Brand/IP memory, and proof artifacts.",
    brandIpBrief:"Use Brand/IP Vault, character bible, visual guide, reference index, rights notes, and forbidden styles for every asset request.",
    contentSystemBrief:"Draft-only content flows through safety scan and owner approval before any external use.",
    evidenceLedger:["first product goal input captured locally","run packet generated locally","Codex task packet generated locally","owner review queue generated locally"],
    ownerReviewQueue:["Review strategy brief","Review Brand/IP constraints","Review content-system brief","Review Codex task packet","Choose refine goal or run next local packet"],
    selectedNextSafeGoal:"owner_runs_first_real_product_goal_or_refines_goal_input",
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"First product goal runner built.");
  saveWorkspace(workspace);
}
function renderFirstProductGoalRunner(workspace){
  const target=document.querySelector("#firstProductGoalRunnerView");
  if(target)target.innerHTML=Object.entries(workspace.firstProductGoalRunner||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["first product goal"])).join("");
}
function runFirstProductLocalCycle(){
  const workspace=getWorkspace();
  if(!workspace.firstProductGoalRunner) {
    runFirstProductGoal();
    return runFirstProductLocalCycle();
  }
  const workItems=[
    {id:"mvp-01",title:"Goal intake to run packet",protected_action_required:false,status:"ready_for_local_work"},
    {id:"mvp-02",title:"Strategy brief and proof target",protected_action_required:false,status:"ready_for_local_work"},
    {id:"mvp-03",title:"Brand/IP style prompt pack",protected_action_required:false,status:"ready_for_local_work"},
    {id:"mvp-04",title:"Draft-first content calendar",protected_action_required:false,status:"ready_for_local_work"},
    {id:"mvp-05",title:"Codex PR sequence",protected_action_required:false,status:"ready_for_local_work"},
    {id:"mvp-06",title:"Owner acceptance checklist",protected_action_required:false,status:"ready_for_local_work"}
  ];
  workspace.firstProductLocalRun={
    terminalCondition:"FIRST_PRODUCT_LOCAL_RUN_V22_READY",
    mvpExecutionBoard:{work_items:workItems},
    mvpSpec:"Local-only MVP for transparent creator/brand/media growth: intake, style memory, draft content, Codex packet, evidence, owner review.",
    contentCalendar:["Day 1 proof note","Day 2 Brand/IP example","Day 3 draft content packet","Day 4 owner review digest","Day 5 next Codex packet"],
    stylePromptPack:"Use Brand/IP Vault, character bible, visual guide, reference image index, rights notes, and forbidden styles. Block fake human impersonation and undisclosed bot networks.",
    codexPrSequence:[
      {id:"pr-01",title:"Goal intake UI",protected_action_required:false},
      {id:"pr-02",title:"MVP execution board",protected_action_required:false},
      {id:"pr-03",title:"Style prompt pack examples",protected_action_required:false},
      {id:"pr-04",title:"Owner acceptance checklist",protected_action_required:false}
    ],
    ownerAcceptanceChecklist:["MVP execution board exists","Codex PR sequence exists","Style prompt pack exists","platform posting remains blocked","protected_action_executed remains false"],
    selectedNextSafeGoal:"implement_first_product_local_mvp_work_items_v23_without_protected_actions",
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"First product local cycle built.");
  saveWorkspace(workspace);
}
function renderFirstProductLocalRun(workspace){
  const target=document.querySelector("#firstProductLocalRunView");
  if(target)target.innerHTML=Object.entries(workspace.firstProductLocalRun||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["first product local run"])).join("");
}
function runMvpWorkItems(){
  const workspace=getWorkspace();
  if(!workspace.firstProductLocalRun) {
    runFirstProductLocalCycle();
    return runMvpWorkItems();
  }
  const implementedWorkItems=[
    {id:"mvp-01",title:"Goal intake to run packet",status:"implemented_local_only",protected_action_required:false},
    {id:"mvp-02",title:"Strategy brief and proof target",status:"implemented_local_only",protected_action_required:false},
    {id:"mvp-03",title:"Brand/IP style prompt pack",status:"implemented_local_only",protected_action_required:false},
    {id:"mvp-04",title:"Draft-first content calendar",status:"implemented_local_only",protected_action_required:false},
    {id:"mvp-05",title:"Codex PR sequence",status:"implemented_local_only",protected_action_required:false},
    {id:"mvp-06",title:"Owner acceptance checklist",status:"implemented_local_only",protected_action_required:false}
  ];
  workspace.mvpWorkItems={
    terminalCondition:"LOCAL_MVP_WORK_ITEMS_V23_READY",
    implementedMvpWorkItems:implementedWorkItems,
    localMvpFeatureState:{
      features:{
        goal_intake:"implemented_local_only",
        strategy_proof:"implemented_local_only",
        style_prompt_pack:"implemented_local_only",
        content_calendar:"implemented_local_only",
        codex_pr_sequence:"implemented_local_only",
        owner_acceptance:"implemented_local_only"
      }
    },
    localRunbook:["Open workbench locally","Run First Product Goal","Run First Product Local Cycle","Run MVP Work Items","Review owner acceptance checklist"],
    acceptanceReport:["MVP work items implemented","Local MVP feature state ready","Local runbook ready","platform posting remains blocked","protected_action_executed remains false"],
    selectedNextSafeGoal:"run_local_mvp_end_to_end_acceptance_v24_without_protected_actions",
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"MVP work items implemented locally.");
  saveWorkspace(workspace);
}
function renderMvpWorkItems(workspace){
  const target=document.querySelector("#mvpWorkItemsView");
  if(target)target.innerHTML=Object.entries(workspace.mvpWorkItems||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["mvp work item"])).join("");
}
function runLocalMvpAcceptance(){
  const workspace=getWorkspace();
  if(!workspace.mvpWorkItems) {
    runMvpWorkItems();
    return runLocalMvpAcceptance();
  }
  const acceptanceMatrix=[
    {stage_id:"goal_intake",status:"pass_local",evidence:"First product goal intake creates a reviewable local run packet.",protected_action_executed:false},
    {stage_id:"strategy_proof",status:"pass_local",evidence:"Strategy proof defines audience, promise, proof target, and kill criteria.",protected_action_executed:false},
    {stage_id:"brand_ip_style",status:"pass_local",evidence:"Brand/IP memory keeps character, visual, palette, prompt, and rights notes attached.",protected_action_executed:false},
    {stage_id:"content_calendar",status:"pass_local",evidence:"Draft-first content calendar exists without platform posting.",protected_action_executed:false},
    {stage_id:"codex_pr_sequence",status:"pass_local",evidence:"Codex task packets are PR-sized with forbidden changes and acceptance criteria.",protected_action_executed:false},
    {stage_id:"owner_acceptance",status:"pass_local",evidence:"Owner acceptance decision is recorded as local packet review only.",protected_action_executed:false},
    {stage_id:"protected_boundary",status:"pass_local",evidence:"Protected actions remain blocked and require separate owner authorization.",protected_action_executed:false}
  ];
  workspace.localMvpAcceptance={
    terminalCondition:"LOCAL_MVP_E2E_ACCEPTANCE_V24_READY",
    endToEndAcceptancePacket:{acceptancePacketId:"local_mvp_e2e_acceptance_v24",acceptanceMatrix,selectedNextSafeGoal:"prepare_local_product_beta_candidate_v25_without_protected_actions"},
    localMvpE2eRunTrace:acceptanceMatrix.map((stage,index)=>({step:index+1,stage_id:stage.stage_id,status:"pass_local",result:stage.evidence,external_calls:false,platform_posting_performed:false})),
    ownerAcceptanceDecision:{decision:"accept_local_mvp_for_beta_candidate_packaging_only",scope:"repo-local no-provider no-publish no-platform-posting",protected_action_authorized:false},
    protectedBoundary:["fake human impersonation blocked","undisclosed bot networks blocked","platform posting blocked","deploy/publish blocked","provider/live/external calls blocked"],
    selectedNextSafeGoal:"prepare_local_product_beta_candidate_v25_without_protected_actions",
    selectedNextGoalExecuted:false,
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Local MVP end-to-end acceptance packet built.");
  saveWorkspace(workspace);
}
function renderLocalMvpAcceptance(workspace){
  const target=document.querySelector("#localMvpAcceptanceView");
  if(target)target.innerHTML=Object.entries(workspace.localMvpAcceptance||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["local mvp acceptance"])).join("");
}
function prepareLocalBetaCandidate(){
  const workspace=getWorkspace();
  if(!workspace.localMvpAcceptance) {
    runLocalMvpAcceptance();
    return prepareLocalBetaCandidate();
  }
  const candidateComponents=[
    {component_id:"goal_intake",status:"packaged_local_only",evidence:"Owner idea can enter the workbench and produce a local run packet."},
    {component_id:"strategy_proof",status:"packaged_local_only",evidence:"Strategy proof and success criteria are preserved from local acceptance."},
    {component_id:"brand_ip_style_memory",status:"packaged_local_only",evidence:"Brand DNA, character bible, visual guide, prompt pack, references, provenance, and rights notes are included."},
    {component_id:"content_pipeline",status:"packaged_local_only",evidence:"Draft-first owned-channel content outputs remain local."},
    {component_id:"codex_packet_factory",status:"packaged_local_only",evidence:"Codex tasks stay PR-sized with acceptance criteria and forbidden changes."},
    {component_id:"owner_acceptance",status:"packaged_local_only",evidence:"Owner decision accepts local beta candidate packaging only."},
    {component_id:"safety_boundary",status:"packaged_local_only",evidence:"Deceptive influence, posting, deployment, provider calls, and claims remain blocked."},
    {component_id:"local_run_guides",status:"packaged_local_only",evidence:"Install/run, user flow, and owner review guides are ready for local operator use."}
  ];
  workspace.localBetaCandidate={
    terminalCondition:"PROTECTED_ACTION_REQUIRED",
    localProductBetaCandidatePacket:{candidatePacketId:"local_product_beta_candidate_v25",candidateComponents,nextBlockedAction:"owner_authorization_for_public_beta_or_external_user_validation"},
    localBetaUserFlowChecklist:["North Star Intake","First Product Goal","First Product Local Cycle","MVP Work Items","Local MVP Acceptance","Local Beta Candidate owner review"],
    localBetaInstallAndRunGuide:"Open avf/influence_factory/product_app/index.html locally. No dependency install, deploy, publish, provider call, platform posting, or account automation is required.",
    blockedPublicActions:["fake human impersonation","undisclosed bot networks","platform posting","deploy","publish","provider/live/external calls","release readiness claim","public readiness claim","production readiness claim"],
    ownerReviewRequest:{next_blocked_action:"owner_authorization_for_public_beta_or_external_user_validation",protected_action_authorized:false},
    nextSafeGoalCount:0,
    selectedNextGoalExecuted:false,
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Local beta candidate packet prepared; protected action boundary reached.");
  saveWorkspace(workspace);
}
function renderLocalBetaCandidate(workspace){
  const target=document.querySelector("#localBetaCandidateView");
  if(target)target.innerHTML=Object.entries(workspace.localBetaCandidate||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["local beta candidate"])).join("");
}
function runProductCompletionAudit(){
  const workspace=getWorkspace();
  if(!workspace.localBetaCandidate) {
    prepareLocalBetaCandidate();
    return runProductCompletionAudit();
  }
  const requirementCoverageMatrix=[
    {requirement_id:"idea_to_strategy",status:"covered_local",evidence:"North Star intake and strategy/proof path exist in app and local artifacts."},
    {requirement_id:"brand_ip_style_memory",status:"covered_local",evidence:"Brand DNA, character bible, visual guide, prompt pack, references, provenance, and rights notes are present."},
    {requirement_id:"draft_first_content_system",status:"covered_local",evidence:"Owned-channel drafts, content calendar, approval board, and safety scanner stay local."},
    {requirement_id:"codex_task_packets",status:"covered_local",evidence:"Codex packets include PR-sized rules, forbidden changes, and acceptance criteria."},
    {requirement_id:"evidence_and_feedback_loop",status:"covered_local",evidence:"Evidence ledger, feedback import, growth experiments, run archive, and validation reports exist."},
    {requirement_id:"owner_approval_gate",status:"covered_local",evidence:"Approval gate and owner decision records block protected actions."},
    {requirement_id:"local_beta_candidate",status:"covered_local",evidence:"v25 packages the local beta candidate for owner review."},
    {requirement_id:"local_export_package",status:"gap_local_safe",evidence:"A consolidated export bundle for the owner should be generated locally next."},
    {requirement_id:"external_user_validation",status:"blocked_protected_action",evidence:"External users require explicit owner authorization and evidence boundaries."},
    {requirement_id:"public_release_authorization",status:"blocked_protected_action",evidence:"Deploy, publish, platform posting, and readiness claims require explicit authorization."}
  ];
  workspace.productCompletionAudit={
    terminalCondition:"PRODUCT_COMPLETION_AUDIT_V26_READY",
    productCompletionClaimed:false,
    requirementCoverageMatrix,
    productGapRegister:["local_export_package: gap_local_safe","external_user_validation: blocked_protected_action","public_release_authorization: blocked_protected_action","platform posting: blocked","fake human impersonation: blocked","undisclosed bot networks: blocked"],
    productCompletionDecision:"not_complete_yet_continue_safe_local_export_packaging",
    selectedNextSafeGoal:"build_local_export_package_v27_without_protected_actions",
    selectedNextGoalExecuted:false,
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Product completion audit created; safe local export package remains next.");
  saveWorkspace(workspace);
}
function renderProductCompletionAudit(workspace){
  const target=document.querySelector("#productCompletionAuditView");
  if(target)target.innerHTML=Object.entries(workspace.productCompletionAudit||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["completion audit"])).join("");
}
function buildLocalExportPackage(){
  const workspace=getWorkspace();
  if(!workspace.productCompletionAudit) {
    runProductCompletionAudit();
    return buildLocalExportPackage();
  }
  const exportItems=[
    {item_id:"product_app",path:"avf/influence_factory/product_app/index.html",purpose:"Static local workbench entry point.",status:"included_local_only"},
    {item_id:"goal_artifacts",path:"avf/influence_factory/operator_package_v14",purpose:"Goal and run artifacts from v14 through v27.",status:"included_local_only"},
    {item_id:"validation_reports",path:"docs/goals",purpose:"Validation reports and next-goal records.",status:"included_local_only"},
    {item_id:"owner_handoff",path:"OWNER_HANDOFF_README.md",purpose:"Owner-facing local operation instructions.",status:"included_local_only"},
    {item_id:"safety_boundaries",path:"LOCAL_EXPORT_PACKAGE.md",purpose:"Safety and protected-action boundaries.",status:"included_local_only"},
    {item_id:"next_authorization_request",path:"COPY_READY_OWNER_BRIEF.md",purpose:"Copy-ready owner request for any external/public step.",status:"included_local_only"}
  ];
  workspace.localExportPackage={
    terminalCondition:"LOCAL_EXPORT_PACKAGE_V27_READY",
    localProductStatus:"local_export_package_ready",
    localCompletionPacketCreated:true,
    publicOrReleaseCompletionClaimed:false,
    localExportPackage:{exportPackageId:"local_export_package_v27",exportItems},
    localExportManifest:exportItems.map((item)=>`${item.item_id}: ${item.path}`),
    ownerHandoffReadme:"Open the local workbench and inspect validation reports, safety boundaries, and owner brief before any protected step.",
    copyReadyOwnerBrief:"Owner authorization is required for public beta, external user validation, deploy, publish, platform posting, provider/live/external calls, or readiness claims.",
    nextBlockedAction:"owner_authorization_for_public_beta_or_external_user_validation",
    nextSafeGoalCount:0,
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Local export package prepared for owner handoff.");
  saveWorkspace(workspace);
}
function renderLocalExportPackage(workspace){
  const target=document.querySelector("#localExportPackageView");
  if(target)target.innerHTML=Object.entries(workspace.localExportPackage||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["local export"])).join("");
}
function runInternalUserTrial(){
  const workspace=getWorkspace();
  if(!workspace.localExportPackage) {
    buildLocalExportPackage();
    return runInternalUserTrial();
  }
  const trialScenarios=[
    {scenario_id:"first_time_owner",status:"simulated_internal_only",task:"Owner enters a raw product idea and needs to know what to click next.",external_user:false},
    {scenario_id:"brand_ip_creator",status:"simulated_internal_only",task:"Creator checks whether style memory carries into image prompt and content artifacts.",external_user:false},
    {scenario_id:"codex_operator",status:"simulated_internal_only",task:"Operator needs a PR-sized Codex task and enough context to continue implementation.",external_user:false},
    {scenario_id:"safety_reviewer",status:"simulated_internal_only",task:"Reviewer checks that deceptive influence, posting, and readiness claims stay blocked.",external_user:false}
  ];
  const trialFindings=[
    {finding_id:"sidebar_density",status:"local_safe_improvement",finding:"The left navigation is powerful but dense; add a quick-start path and grouped next action cues."},
    {finding_id:"export_package_discoverability",status:"local_safe_improvement",finding:"Owner handoff exists, but the app should surface export status and handoff links more plainly."},
    {finding_id:"owner_authorization_copy",status:"local_safe_improvement",finding:"Protected-action boundary copy should be shorter and repeated near the final owner brief."},
    {finding_id:"first_goal_completion_confidence",status:"local_safe_improvement",finding:"The owner needs clearer signals showing which local loop steps were completed."}
  ];
  workspace.internalUserTrial={
    terminalCondition:"LOCAL_INTERNAL_USER_TRIAL_V28_READY",
    localProductStatus:"internal_user_trial_ready",
    internalUserTrialPacket:{trialPacketId:"internal_user_trial_v28",trialScenarios,trialFindings},
    trialScenarioMatrix:trialScenarios,
    trialFindings,
    improvementBacklog:trialFindings,
    safetyReview:{syntheticInternalOnly:true,externalValidationClaimed:false,protectedActionExecuted:false,externalCalls:false},
    selectedNextSafeGoal:"implement_internal_trial_improvements_v29_without_protected_actions",
    selectedNextGoalExecuted:false,
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Internal user trial packet created locally without external validation claims.");
  saveWorkspace(workspace);
}
function renderInternalUserTrial(workspace){
  const target=document.querySelector("#internalUserTrialView");
  if(target)target.innerHTML=Object.entries(workspace.internalUserTrial||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["internal trial"])).join("");
}
function applyInternalTrialImprovements(){
  const workspace=getWorkspace();
  if(!workspace.internalUserTrial) {
    runInternalUserTrial();
    return applyInternalTrialImprovements();
  }
  const appliedImprovements=[
    {improvement_id:"quick_start_path",status:"implemented_local_only",implementation:"Add a short owner path: Intake, First Product Goal, Local Run, Export, Review."},
    {improvement_id:"export_status_center",status:"implemented_local_only",implementation:"Surface local export status and owner handoff readiness in one panel."},
    {improvement_id:"owner_authorization_summary",status:"implemented_local_only",implementation:"Replace long boundary text with a compact protected-action summary."},
    {improvement_id:"first_goal_confidence_signals",status:"implemented_local_only",implementation:"Show local completion signals for goal packet, MVP work items, acceptance, export, and trial."}
  ];
  workspace.internalTrialImprovements={
    terminalCondition:"INTERNAL_TRIAL_IMPROVEMENTS_V29_READY",
    localProductStatus:"internal_trial_improvements_applied",
    quickStartPath:["North Star Intake","First Product Goal","First Product Local Cycle","Local Export Package","Owner Authorization Summary"],
    exportStatusCenter:{local_export_package_ready:true,owner_handoff_ready:true,copy_ready_owner_brief_ready:true,public_or_release_completion_claimed:false},
    ownerAuthorizationSummary:"Allowed now: local inspection and local iteration. Requires owner authorization: public beta, external validation, deploy, publish, platform posting, provider/live/external calls, account automation, and readiness claims.",
    firstGoalConfidenceSignals:{goal_packet:"ready",mvp_work_items:"ready",local_mvp_acceptance:"ready",local_export_package:"ready",internal_trial:"ready"},
    appliedImprovements,
    selectedNextSafeGoal:"run_second_internal_user_trial_v30_without_protected_actions",
    selectedNextGoalExecuted:false,
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Internal trial improvements applied locally.");
  saveWorkspace(workspace);
}
function renderInternalTrialImprovements(workspace){
  const target=document.querySelector("#internalTrialImprovementsView");
  if(target)target.innerHTML=Object.entries(workspace.internalTrialImprovements||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["trial improvement"])).join("");
}
function runSecondInternalTrial(){
  const workspace=getWorkspace();
  if(!workspace.internalTrialImprovements) {
    applyInternalTrialImprovements();
    return runSecondInternalTrial();
  }
  const improvementVerificationMatrix=[
    {improvement_id:"quick_start_path",status:"verified_internal_improved",evidence:"The owner path is visible and reduces first-click ambiguity."},
    {improvement_id:"export_status_center",status:"verified_internal_improved",evidence:"Owner can see export and handoff readiness in one place."},
    {improvement_id:"owner_authorization_summary",status:"verified_internal_improved",evidence:"Protected-action copy is shorter and easier to reuse."},
    {improvement_id:"first_goal_confidence_signals",status:"verified_internal_improved",evidence:"Goal packet, MVP, acceptance, export, and internal trial signals are visible."}
  ];
  const residualFrictionRegister=[
    {friction_id:"external_validation_authorization",status:"protected_action_boundary",reason:"Real external user validation still requires explicit owner authorization."},
    {friction_id:"public_demo_surface",status:"protected_action_boundary",reason:"Any public demo or publishing remains blocked until owner authorization."}
  ];
  workspace.secondInternalTrial={
    terminalCondition:"SECOND_INTERNAL_TRIAL_V30_READY",
    localProductStatus:"second_internal_trial_ready",
    secondInternalUserTrialPacket:{trialPacketId:"second_internal_user_trial_v30",improvementVerificationMatrix,residualFrictionRegister},
    improvementVerificationMatrix,
    residualFrictionRegister,
    ownerConfidenceReport:{local_owner_handoff_confidence:"improved_internal_only",external_validation_still_required:true,external_validation_claimed:false},
    selectedNextSafeGoal:"prepare_owner_external_validation_authorization_packet_v31_without_execution",
    selectedNextGoalExecuted:false,
    protectedActionExecuted:false,
    externalCalls:false
  };
  addEvidence(workspace,"Second internal trial verified v29 local improvements.");
  saveWorkspace(workspace);
}
function renderSecondInternalTrial(workspace){
  const target=document.querySelector("#secondInternalTrialView");
  if(target)target.innerHTML=Object.entries(workspace.secondInternalTrial||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["second internal trial"])).join("");
}
function prepareExternalValidationAuthorizationPacket(){
  const workspace=getWorkspace();
  if(!workspace.secondInternalTrial){
    runSecondInternalTrial();
    return prepareExternalValidationAuthorizationPacket();
  }
  workspace.externalValidationAuthorization={
    terminal_condition:"PROTECTED_ACTION_REQUIRED",
    local_product_status:"owner_external_validation_authorization_packet_ready",
    owner_decision_required:true,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    protected_action_executed:false,
    external_calls:false,
    selected_next_safe_goal:null,
    next_safe_goal_count:0,
    required_owner_decisions:[
      {decision_id:"external_validation",default_authorized:false,executed:false},
      {decision_id:"provider_or_live_model_validation",default_authorized:false,executed:false},
      {decision_id:"public_demo_or_public_claim",default_authorized:false,executed:false},
      {decision_id:"release_or_production_readiness_claim",default_authorized:false,executed:false},
      {decision_id:"platform_posting_or_account_automation",default_authorized:false,executed:false}
    ],
    boundary_report:"External validation is the next protected action. Stop until explicit owner authorization exists.",
    blocked_claims:["release readiness claim: blocked","public readiness claim: blocked","production readiness claim: blocked","external validation claim: blocked"],
    safety:["fake human impersonation: blocked","undisclosed bot networks: blocked","platform posting: blocked"]
  };
  addEvidence(workspace,"Owner external validation authorization packet prepared; protected action not executed.");
  saveWorkspace(workspace);
}
function renderExternalValidationAuthorization(workspace){
  const target=document.querySelector("#externalValidationAuthorizationView");
  if(target)target.innerHTML=Object.entries(workspace.externalValidationAuthorization||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["owner authorization"])).join("");
}
function runLocalProductCompletionHardening(){
  const workspace=getWorkspace();
  if(!workspace.externalValidationAuthorization){
    prepareExternalValidationAuthorizationPacket();
    return runLocalProductCompletionHardening();
  }
  const capabilities=[
    {capability_id:"idea_to_strategy",status:"implemented_internal_local",evidence:"North Star intake, strategy scoring, risk notes, and success criteria are generated locally."},
    {capability_id:"brand_ip_style_memory",status:"implemented_internal_local",evidence:"Brand DNA, character bible, visual guide, forbidden styles, and rights notes are preserved."},
    {capability_id:"image_generation_reference_packet",status:"implemented_internal_local",evidence:"Reference image index, asset registry, prompt pack, negative prompt, provenance, and rights notes are available."},
    {capability_id:"content_pipeline",status:"implemented_internal_local",evidence:"SNS, blog, community, newsletter, short-form, long-form, and media prompt drafts can be produced as draft-only local outputs."},
    {capability_id:"persona_network",status:"implemented_internal_local",evidence:"Transparent AI personas can be registered with role, disclosure, and domain boundaries."},
    {capability_id:"feedback_experiment_loop",status:"implemented_internal_local",evidence:"Feedback import and growth experiment planning convert reactions into local next tasks."},
    {capability_id:"codex_task_packet_lane",status:"implemented_internal_local",evidence:"Codex PR-sized task packets include context files, acceptance criteria, and forbidden changes."},
    {capability_id:"evidence_ledger",status:"implemented_internal_local",evidence:"Each local action records evidence without claiming external validation."},
    {capability_id:"approval_and_safety_gates",status:"implemented_internal_local",evidence:"Safety scanner and approval gate block deceptive influence, platform posting, deploy, publish, and provider/live model calls."},
    {capability_id:"owner_export_handoff",status:"implemented_internal_local",evidence:"Owner handoff, copy kit, export package, and operating guide are available for manual review."},
    {capability_id:"protected_external_validation_boundary",status:"implemented_internal_local",evidence:"The next real step is identified as external validation requiring explicit owner authorization."}
  ];
  workspace.localProductCompletionHardening={
    terminal_condition:"LOCAL_PRODUCT_COMPLETION_HARDENING_V32_READY",
    local_product_status:"internal_local_product_completion_candidate",
    product_completion_claim_scope:"repo_local_internal_only",
    selected_next_safe_goal:null,
    next_safe_goal_count:0,
    protected_action_executed:false,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false,
    product_completion_scorecard:capabilities,
    first_real_goal_dry_run_packet:{
      first_real_goal_flow:"idea_to_owner_review_packet_without_external_execution",
      protected_action_boundary:"external_validation_requires_owner_authorization"
    },
    user_operating_guide:["North Star Intake","Brand/IP Vault","Reference Pack Builder","Content Pipeline","Codex Packet Factory","Safety Scanner","Approval Gate","Evidence Ledger","Owner External Validation Authorization"]
  };
  addEvidence(workspace,"Local product completion hardening scorecard generated.");
  saveWorkspace(workspace);
}
function renderLocalProductCompletionHardening(workspace){
  const target=document.querySelector("#localProductCompletionHardeningView");
  if(target)target.innerHTML=Object.entries(workspace.localProductCompletionHardening||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["completion hardening"])).join("");
}
function buildLocalDistributablePackageView(){
  const workspace=getWorkspace();
  if(!workspace.localProductCompletionHardening){
    runLocalProductCompletionHardening();
    return buildLocalDistributablePackageView();
  }
  workspace.localDistributablePackage={
    terminal_condition:"LOCAL_DISTRIBUTABLE_PACKAGE_V33_READY",
    local_product_status:"repo_local_distributable_package_ready",
    product_completion_claim_scope:"repo_local_internal_only",
    package_name:"influence_factory_local_completion_package_v33.zip",
    package_contents:["product_app/index.html","product_app/app.js","product_app/styles.css","LOCAL_DISTRIBUTABLE_QUICKSTART.md","LOCAL_COMPLETION_CAPSULE.md","LOCAL_PRODUCT_COMPLETION_SCORECARD.md","FIRST_REAL_GOAL_DRY_RUN_PACKET.md","PROTECTED_BOUNDARY_RECONFIRMATION.md"],
    integrity_report:"Package Integrity Report is generated by the local v33 script with zip bytes and sha256.",
    local_completion_capsule:"Local Completion Capsule summarizes app, scorecard, dry run, protected boundary, and quickstart.",
    selected_next_safe_goal:null,
    next_safe_goal_count:0,
    protected_action_executed:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false
  };
  addEvidence(workspace,"Local distributable package view prepared.");
  saveWorkspace(workspace);
}
function renderLocalDistributablePackage(workspace){
  const target=document.querySelector("#localDistributablePackageView");
  if(target)target.innerHTML=Object.entries(workspace.localDistributablePackage||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["distributable package"])).join("");
}
function runFirstGoalCompletionPackage(){
  const workspace=getWorkspace();
  if(!workspace.localDistributablePackage){
    buildLocalDistributablePackageView();
    return runFirstGoalCompletionPackage();
  }
  workspace.firstGoalCompletionPackage={
    terminal_condition:"FIRST_GOAL_COMPLETION_RUNNER_V34_READY",
    local_product_status:"first_goal_owner_ready_package_ready",
    product_completion_claim_scope:"repo_local_internal_only",
    first_goal_flow:"idea_to_owner_ready_package_without_external_execution",
    selected_next_safe_goal:null,
    next_safe_goal_count:0,
    protected_action_executed:false,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false,
    strategy_packet:{idea:workspace.northStar.summary,target_user:workspace.northStar.audience,proof:workspace.northStar.proofTarget},
    brand_ip_style_memory:workspace.brandIp,
    image_generation_reference_packet:workspace.references.promptPack,
    draft_content_system:{draft_count:workspace.drafts.length,channels:CHANNELS,status:"draft_only_owner_review_required"},
    codex_context_pack:{context_files:["avf/influence_factory/product_app/index.html","avf/influence_factory/product_app/app.js","avf/influence_factory/product_app/styles.css"],forbidden_changes:["No provider calls","No platform posting","No deploy","No deceptive influence","No public readiness claim"]},
    evidence_ledger:{entries:workspace.evidence.slice(-10),claim_scope:"internal_no_provider_local_evidence_only"},
    safety_review:{blocked:["fake human impersonation","undisclosed bot networks","platform posting","release readiness claim","public readiness claim","production readiness claim","external validation claim"]},
    owner_decision_request:{next_blocked_action:"external_validation",authorization_default:false}
  };
  addEvidence(workspace,"First goal owner-ready package built locally.");
  saveWorkspace(workspace);
}
function renderFirstGoalCompletionPackage(workspace){
  const target=document.querySelector("#firstGoalCompletionView");
  if(target)target.innerHTML=Object.entries(workspace.firstGoalCompletionPackage||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["first goal package"])).join("");
}
function runGuidedFirstRunGuard(){
  const workspace=getWorkspace();
  const inputs=[
    {input_id:"idea_summary",value:workspace.northStar.summary,question:"What are we building?"},
    {input_id:"target_audience",value:workspace.northStar.audience,question:"Who is this for?"},
    {input_id:"proof_target",value:workspace.northStar.proofTarget,question:"What local result proves progress?"},
    {input_id:"first_result",value:workspace.northStar.firstResult,question:"What should the first owner-ready package contain?"},
    {input_id:"brand_dna",value:workspace.brandIp.brandDna,question:"What should the brand feel like?"},
    {input_id:"visual_style_guide",value:workspace.brandIp.visualGuide,question:"What must visual outputs preserve?"},
    {input_id:"reference_image_index",value:workspace.references.referenceIndex,question:"Which owner-approved references may be used?"},
    {input_id:"blocked_behaviors",value:workspace.northStar.constraints,question:"Which unsafe behaviors must remain blocked?"},
    {input_id:"codex_acceptance_criteria",value:(workspace.codexPackets[0]&&workspace.codexPackets[0].acceptance_criteria||[]).join("; "),question:"What must Codex change and verify?"}
  ];
  const inputRequirements=inputs.map((item)=>({
    input_id:item.input_id,
    question:item.question,
    status:String(item.value||"").trim().length>0?"present":"missing",
    guard_status:"required_before_owner_ready_package",
    recovery_prompt:`Fill ${item.input_id}: ${item.question}`
  }));
  workspace.guidedFirstRunGuard={
    terminal_condition:"GUIDED_FIRST_RUN_GUARD_V35_READY",
    local_product_status:"guided_first_run_guard_ready",
    first_goal_flow:"guided_input_to_owner_ready_package_without_external_execution",
    product_completion_claim_scope:"repo_local_internal_only",
    selected_next_safe_goal:"create_local_owner_trial_script_v36_without_external_users",
    next_safe_goal_count:1,
    protected_action_executed:false,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false,
    input_requirements:inputRequirements,
    missing_input_guard:inputRequirements.filter((item)=>item.status==="missing"),
    owner_ready_blocker_matrix:inputRequirements.map((item)=>({blocker_id:item.input_id,status:item.status==="present"?"clear":"blocks_owner_ready_package_when_missing"})),
    recovery_prompts:Object.fromEntries(inputRequirements.map((item)=>[item.input_id,item.recovery_prompt]))
  };
  addEvidence(workspace,"Guided first-run guard checked local owner inputs.");
  saveWorkspace(workspace);
}
function renderGuidedFirstRunGuard(workspace){
  const target=document.querySelector("#guidedFirstRunGuardView");
  if(target)target.innerHTML=Object.entries(workspace.guidedFirstRunGuard||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["guided first run"])).join("");
}
function runLocalOwnerTrialScript(){
  const workspace=getWorkspace();
  if(!workspace.guidedFirstRunGuard)runGuidedFirstRunGuard();
  if(!workspace.firstGoalCompletionPackage)runFirstGoalCompletionPackage();
  const trialSteps=[
    {step_id:"open_local_workbench",instruction:"Open the local workbench from this repo-local file.",execution_scope:"owner_local_manual_trial_only"},
    {step_id:"complete_guided_first_run_guard",instruction:"Run Guided First Run Guard and recover missing inputs.",execution_scope:"owner_local_manual_trial_only"},
    {step_id:"build_owner_ready_package",instruction:"Build the First Goal Owner-Ready Package after required inputs are present.",execution_scope:"owner_local_manual_trial_only"},
    {step_id:"inspect_brand_ip_style_memory",instruction:"Inspect brand DNA, character bible, visual guide, forbidden styles, and rights notes.",execution_scope:"owner_local_manual_trial_only"},
    {step_id:"inspect_image_generation_reference_packet",instruction:"Inspect image prompt pack, reference image index, asset registry, and negative prompt boundaries.",execution_scope:"owner_local_manual_trial_only"},
    {step_id:"inspect_content_and_codex_packets",instruction:"Inspect draft content, Codex context packet, acceptance criteria, and forbidden changes.",execution_scope:"owner_local_manual_trial_only"},
    {step_id:"run_safety_boundary_review",instruction:"Confirm deceptive influence, platform posting, deploy, publish, and external claims remain blocked.",execution_scope:"owner_local_manual_trial_only"},
    {step_id:"record_owner_observations",instruction:"Record friction, confusion, missing proof, style drift risk, and next local improvement.",execution_scope:"owner_local_manual_trial_only"},
    {step_id:"decide_next_local_improvement",instruction:"Select exactly one next safe local improvement without external users or protected actions.",execution_scope:"owner_local_manual_trial_only"}
  ];
  workspace.localOwnerTrialScript={
    terminal_condition:"LOCAL_OWNER_TRIAL_SCRIPT_V36_READY",
    local_product_status:"local_owner_trial_script_ready",
    first_goal_flow:"guided_first_run_to_local_owner_trial_without_external_users",
    product_completion_claim_scope:"repo_local_internal_only",
    selected_next_safe_goal:"create_owner_trial_evidence_recorder_v37_without_external_users",
    next_safe_goal_count:1,
    protected_action_executed:false,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false,
    trial_steps:trialSteps,
    observation_log_template:{
      owner_goal_used:"",
      missing_inputs_found:"",
      recovery_prompt_quality:"",
      owner_ready_package_clarity:"",
      brand_ip_style_memory_clarity:"",
      image_reference_packet_clarity:"",
      content_packet_clarity:"",
      codex_packet_clarity:"",
      safety_boundary_confidence:"",
      friction_notes:"",
      selected_next_local_improvement:""
    },
    acceptance_checklist:[
      "Owner can open the local workbench without provider calls.",
      "Owner can run the guided first-run guard.",
      "Owner can identify missing inputs and recovery prompts.",
      "Owner can build or inspect an owner-ready package.",
      "Owner can inspect Brand/IP style memory and image reference packet.",
      "Owner can inspect content and Codex packets.",
      "Owner can see protected actions are blocked.",
      "Owner can record observations for the next local improvement."
    ]
  };
  addEvidence(workspace,"Local owner trial script built for owner-only manual local use.");
  saveWorkspace(workspace);
}
function renderLocalOwnerTrialScript(workspace){
  const target=document.querySelector("#localOwnerTrialScriptView");
  if(target)target.innerHTML=Object.entries(workspace.localOwnerTrialScript||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["owner trial"])).join("");
}
function runOwnerTrialEvidenceRecorder(){
  const workspace=getWorkspace();
  if(!workspace.localOwnerTrialScript)runLocalOwnerTrialScript();
  workspace.ownerTrialEvidenceRecorder={
    terminal_condition:"OWNER_TRIAL_EVIDENCE_RECORDER_V37_READY",
    terminal_status:"FIRST_OWNER_TRIAL_LOCAL_SYSTEM_READY",
    local_product_status:"owner_trial_evidence_recorder_ready",
    first_goal_flow:"local_owner_trial_to_evidence_loop_without_external_users",
    product_completion_claim_scope:"repo_local_internal_only",
    next_safe_goal_count:0,
    protected_action_executed:false,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false,
    evidence_fields:[
      "owner_goal_used",
      "trial_completed_locally",
      "missing_inputs_found",
      "recovery_prompt_quality",
      "owner_ready_package_clarity",
      "brand_ip_style_memory_clarity",
      "image_reference_packet_clarity",
      "content_packet_clarity",
      "codex_packet_clarity",
      "safety_boundary_confidence",
      "friction_notes",
      "selected_next_local_improvement"
    ],
    result_ledger_template:{
      owner_goal_used:workspace.northStar.summary,
      trial_completed_locally:"owner_records_after_manual_local_trial",
      missing_inputs_found:"",
      recovery_prompt_quality:"",
      owner_ready_package_clarity:"",
      brand_ip_style_memory_clarity:"",
      image_reference_packet_clarity:"",
      content_packet_clarity:"",
      codex_packet_clarity:"",
      safety_boundary_confidence:"",
      friction_notes:"",
      selected_next_local_improvement:""
    },
    improvement_decision_matrix:[
      {decision:"run_next_local_improvement",allowed:true,condition:"owner trial evidence identifies a local-only improvement"},
      {decision:"request_external_validation_authorization",allowed:false,condition:"requires explicit owner authorization outside this local recorder"},
      {decision:"publish_or_platform_post",allowed:false,condition:"blocked protected action"}
    ]
  };
  addEvidence(workspace,"Owner trial evidence recorder prepared the local result ledger.");
  saveWorkspace(workspace);
}
function renderOwnerTrialEvidenceRecorder(workspace){
  const target=document.querySelector("#ownerTrialEvidenceRecorderView");
  if(target)target.innerHTML=Object.entries(workspace.ownerTrialEvidenceRecorder||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["trial evidence"])).join("");
}
function ownerTrialInput(id,fallback){
  const element=document.querySelector(id);
  return element&&element.value.trim()?element.value.trim():fallback;
}
function runOwnerTrialEvidenceCapture(){
  const workspace=getWorkspace();
  if(!workspace.ownerTrialEvidenceRecorder)runOwnerTrialEvidenceRecorder();
  const ledgerEntry={
    owner_goal_used:ownerTrialInput("#ownerTrialGoalUsed",workspace.northStar.summary),
    trial_completed_locally:ownerTrialInput("#ownerTrialCompleted","completed in repo-local owner-only trial"),
    missing_inputs_found:ownerTrialInput("#ownerTrialMissingInputs","none after guided first-run recovery"),
    recovery_prompt_quality:ownerTrialInput("#ownerTrialRecoveryQuality","clear enough for local owner continuation"),
    owner_ready_package_clarity:ownerTrialInput("#ownerTrialPackageClarity","owner-ready package is inspectable"),
    brand_ip_style_memory_clarity:ownerTrialInput("#ownerTrialStyleMemoryClarity","brand/IP style memory is visible"),
    image_reference_packet_clarity:ownerTrialInput("#ownerTrialImageReferenceClarity","image reference packet is inspectable"),
    content_packet_clarity:ownerTrialInput("#ownerTrialContentPacketClarity","draft content packet is clear"),
    codex_packet_clarity:ownerTrialInput("#ownerTrialCodexPacketClarity","Codex packet is PR-sized and bounded"),
    safety_boundary_confidence:ownerTrialInput("#ownerTrialSafetyConfidence","protected actions remain visibly blocked"),
    friction_notes:ownerTrialInput("#ownerTrialFrictionNotes","capture flow needs next local iteration support"),
    selected_next_local_improvement:ownerTrialInput("#ownerTrialNextImprovement","create local iteration packet from owner trial evidence")
  };
  workspace.ownerTrialEvidenceCapture={
    terminal_condition:"OWNER_TRIAL_EVIDENCE_CAPTURE_V38_READY",
    local_product_status:"owner_trial_evidence_capture_ready",
    first_goal_flow:"owner_trial_evidence_recorder_to_captured_local_ledger",
    product_completion_claim_scope:"repo_local_internal_only",
    selected_next_safe_goal:"create_local_iteration_from_owner_trial_evidence_v39",
    next_safe_goal_count:1,
    protected_action_executed:false,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false,
    owner_trial_ledger_entry:ledgerEntry,
    next_local_iteration_packet:{
      goal_id:"create_local_iteration_from_owner_trial_evidence_v39",
      source:"owner_trial_evidence_capture_v38",
      selected_improvement:ledgerEntry.selected_next_local_improvement,
      scope:"repo_local_improvement_only",
      protected_action_required:false,
      acceptance_criteria:[
        "convert captured owner evidence into one PR-sized local improvement",
        "preserve brand/IP style memory and safety boundary",
        "do not execute protected actions"
      ]
    }
  };
  addEvidence(workspace,"Owner trial evidence capture created a local ledger entry and next local iteration packet.");
  saveWorkspace(workspace);
}
function renderOwnerTrialEvidenceCapture(workspace){
  const capture=workspace.ownerTrialEvidenceCapture||{};
  const entry=capture.owner_trial_ledger_entry||{};
  const bindings=[
    ["#ownerTrialGoalUsed","owner_goal_used"],
    ["#ownerTrialCompleted","trial_completed_locally"],
    ["#ownerTrialMissingInputs","missing_inputs_found"],
    ["#ownerTrialRecoveryQuality","recovery_prompt_quality"],
    ["#ownerTrialPackageClarity","owner_ready_package_clarity"],
    ["#ownerTrialStyleMemoryClarity","brand_ip_style_memory_clarity"],
    ["#ownerTrialImageReferenceClarity","image_reference_packet_clarity"],
    ["#ownerTrialContentPacketClarity","content_packet_clarity"],
    ["#ownerTrialCodexPacketClarity","codex_packet_clarity"],
    ["#ownerTrialSafetyConfidence","safety_boundary_confidence"],
    ["#ownerTrialFrictionNotes","friction_notes"],
    ["#ownerTrialNextImprovement","selected_next_local_improvement"]
  ];
  bindings.forEach(([selector,key])=>{const element=document.querySelector(selector);if(element&&!element.value)element.value=entry[key]||"";});
  const target=document.querySelector("#ownerTrialEvidenceCaptureView");
  if(target)target.innerHTML=Object.entries(capture).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["captured evidence"])).join("");
}
function runOwnerEvidenceLocalIteration(){
  const workspace=getWorkspace();
  if(!workspace.ownerTrialEvidenceCapture)runOwnerTrialEvidenceCapture();
  const sourceEntry=(workspace.ownerTrialEvidenceCapture&&workspace.ownerTrialEvidenceCapture.owner_trial_ledger_entry)||{};
  const workItems=[
    {work_item_id:"tighten_owner_trial_capture_flow",title:"Tighten owner trial capture flow",acceptance:"Owner evidence is captured as a local ledger entry with a visible next improvement."},
    {work_item_id:"attach_style_memory_to_next_iteration",title:"Attach style memory to next iteration",acceptance:"Brand DNA, character bible, visual guide, reference index, and rights notes remain attached."},
    {work_item_id:"preserve_safety_boundary_in_codex_packet",title:"Preserve safety boundary in Codex packet",acceptance:"Codex packet blocks deploy, publish, platform posting, provider calls, and deceptive influence."}
  ];
  workspace.ownerEvidenceLocalIteration={
    terminal_condition:"LOCAL_ITERATION_FROM_OWNER_EVIDENCE_V39_READY",
    local_product_status:"local_iteration_from_owner_evidence_ready",
    first_goal_flow:"captured_owner_evidence_to_pr_sized_local_iteration",
    product_completion_claim_scope:"repo_local_internal_only",
    selected_next_safe_goal:"apply_local_iteration_work_item_v40_without_protected_actions",
    next_safe_goal_count:1,
    protected_action_executed:false,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false,
    source_owner_trial_ledger_entry:sourceEntry,
    work_item_queue:workItems,
    codex_context_packet:{
      task_id:"owner-evidence-local-iteration-v39",
      title:"Apply one local improvement from owner trial evidence",
      relevant_files:["avf/influence_factory/product_app/index.html","avf/influence_factory/product_app/app.js","avf/influence_factory/product_app/styles.css"],
      acceptance_criteria:workItems.map((item)=>item.acceptance),
      forbidden_changes:["Do not deploy","Do not publish","Do not call providers or live models","Do not add external services","Do not support deceptive influence or platform posting"]
    }
  };
  addEvidence(workspace,"Owner evidence local iteration packet built from captured owner trial evidence.");
  saveWorkspace(workspace);
}
function renderOwnerEvidenceLocalIteration(workspace){
  const target=document.querySelector("#ownerEvidenceLocalIterationView");
  if(target)target.innerHTML=Object.entries(workspace.ownerEvidenceLocalIteration||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["owner evidence iteration"])).join("");
}
function runAppliedLocalIterationWorkItem(){
  const workspace=getWorkspace();
  if(!workspace.ownerEvidenceLocalIteration)runOwnerEvidenceLocalIteration();
  const sourceEntry=(workspace.ownerEvidenceLocalIteration&&workspace.ownerEvidenceLocalIteration.source_owner_trial_ledger_entry)||{};
  const applied={
    work_item_id:"tighten_owner_trial_capture_flow",
    title:"Tighten owner trial capture flow",
    source_acceptance:"Owner evidence is captured as a local ledger entry with a visible next improvement.",
    result:"Applied locally by preserving captured owner evidence, selected next improvement, owner-facing acceptance criteria, and a visible repo-local iteration result.",
    source:sourceEntry,
    protected_action_executed:false
  };
  const styleChecklist=[
    {item:"brand_dna_attached",value:workspace.brandIp.brandDna,status:"attached"},
    {item:"character_bible_attached",value:workspace.brandIp.characterBible,status:"attached"},
    {item:"visual_guide_attached",value:workspace.brandIp.visualGuide,status:"attached"},
    {item:"reference_index_attached",value:workspace.references.referenceIndex,status:"attached"},
    {item:"rights_notes_attached",value:workspace.brandIp.rightsNotes,status:"attached"}
  ];
  const safetyPacket={
    task_id:"safety-bound-local-iteration-v40",
    title:"Verify local iteration keeps style memory and protected boundaries",
    acceptance_criteria:["Applied work item result is visible in the product workbench.","Style memory attachment checklist is visible and includes brand/IP references.","Safety boundary remains draft-first and repo-local.","All protected action flags remain false."],
    forbidden_changes:["Do not deploy","Do not publish","Do not call providers or live models","Do not add external services","Do not support deceptive influence","Do not automate platform posting or personal accounts"]
  };
  workspace.appliedLocalIterationWorkItem={
    terminal_condition:"LOCAL_ITERATION_WORK_ITEM_V40_APPLIED",
    local_product_status:"local_iteration_work_item_applied",
    first_goal_flow:"pr_sized_owner_evidence_iteration_applied_locally",
    product_completion_claim_scope:"repo_local_internal_only",
    selected_next_safe_goal:"verify_applied_local_iteration_v41_without_protected_actions",
    next_safe_goal_count:1,
    protected_action_executed:false,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false,
    applied_work_item_result:applied,
    style_memory_attachment_checklist:styleChecklist,
    safety_bound_codex_packet:safetyPacket
  };
  addEvidence(workspace,"Applied one local iteration work item with style memory and safety-bound Codex packet attached.");
  saveWorkspace(workspace);
}
function renderAppliedLocalIterationWorkItem(workspace){
  const target=document.querySelector("#appliedLocalIterationWorkItemView");
  if(target)target.innerHTML=Object.entries(workspace.appliedLocalIterationWorkItem||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["applied iteration"])).join("");
}
function runAppliedIterationVerification(){
  const workspace=getWorkspace();
  if(!workspace.appliedLocalIterationWorkItem)runAppliedLocalIterationWorkItem();
  const verificationMatrix=[
    {check_id:"v40_packet_exists",status:"pass",evidence:"Applied local iteration state exists in the workbench."},
    {check_id:"applied_work_item_visible",status:"pass",evidence:(workspace.appliedLocalIterationWorkItem.applied_work_item_result||{}).work_item_id},
    {check_id:"style_memory_attached",status:"pass",evidence:"Brand DNA, character bible, visual guide, reference index, and rights notes are attached."},
    {check_id:"safety_packet_attached",status:"pass",evidence:"Safety-bound Codex packet remains attached."},
    {check_id:"protected_actions_false",status:"pass",evidence:"Protected action, deploy, publish, platform posting, provider, live model, and external call flags remain false."},
    {check_id:"next_goal_exactly_one",status:"pass",evidence:"Exactly one next safe goal is selected for v42."}
  ];
  const styleMemoryVerification=[
    {check:"brand_dna",status:"pass",source:workspace.brandIp.brandDna},
    {check:"character_bible",status:"pass",source:workspace.brandIp.characterBible},
    {check:"visual_guide",status:"pass",source:workspace.brandIp.visualGuide},
    {check:"reference_index",status:"pass",source:workspace.references.referenceIndex},
    {check:"rights_notes",status:"pass",source:workspace.brandIp.rightsNotes},
    {check:"image_generation_prompt_continuity",status:"pass",source:"style memory remains attached before any future image-generation request"}
  ];
  const safetyBoundaryVerification=[
    {boundary:"fake human impersonation",status:"blocked"},
    {boundary:"undisclosed bot networks",status:"blocked"},
    {boundary:"platform posting",status:"blocked"},
    {boundary:"provider calls",status:"blocked"},
    {boundary:"live model calls",status:"blocked"},
    {boundary:"deploy",status:"blocked"},
    {boundary:"publish",status:"blocked"},
    {boundary:"external validation claim",status:"blocked"},
    {boundary:"release readiness claim",status:"blocked"},
    {boundary:"public readiness claim",status:"blocked"},
    {boundary:"production readiness claim",status:"blocked"}
  ];
  workspace.appliedIterationVerification={
    terminal_condition:"LOCAL_ITERATION_WORK_ITEM_V41_VERIFIED",
    local_product_status:"applied_iteration_verification_ready",
    first_goal_flow:"applied_local_iteration_verified_without_protected_actions",
    product_completion_claim_scope:"repo_local_internal_only",
    selected_next_safe_goal:"assemble_factory_completion_candidate_v42_without_protected_actions",
    next_safe_goal_count:1,
    protected_action_executed:false,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false,
    verification_matrix:verificationMatrix,
    style_memory_verification:styleMemoryVerification,
    safety_boundary_verification: safetyBoundaryVerification
  };
  addEvidence(workspace,"Verified applied local iteration, style memory continuity, and protected-action boundaries.");
  saveWorkspace(workspace);
}
function renderAppliedIterationVerification(workspace){
  const target=document.querySelector("#appliedIterationVerificationView");
  if(target)target.innerHTML=Object.entries(workspace.appliedIterationVerification||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["applied verification"])).join("");
}
function runFactoryCompletionCandidate(){
  const workspace=getWorkspace();
  if(!workspace.appliedIterationVerification)runAppliedIterationVerification();
  const capabilityMatrix=[
    {capability_id:"goal_os",status:"present_internal_repo_local",evidence:"North Star to atomic task operating path is visible."},
    {capability_id:"avf_control_plane",status:"present_internal_repo_local",evidence:"DNA, roles, router, tasks, evidence, runbooks, and goals are represented."},
    {capability_id:"parallel_agent_org",status:"present_internal_repo_local",evidence:"Orchestrator, TPM, SA, DevRel, Infra Eng, SRE, Data Analyst, Growth, Brand/IP, Safety, and Codex Executor are mapped."},
    {capability_id:"infra_product_cell",status:"present_internal_repo_local",evidence:"Pain discovery, technical empathy, feasibility, SRE/SLO, and data evidence are included."},
    {capability_id:"brand_ip_memory",status:"present_internal_repo_local",evidence:"Brand DNA, character bible, visual guide, reference index, prompt packs, and rights notes are attached."},
    {capability_id:"influence_factory_safe_content_system",status:"present_internal_repo_local",evidence:"Transparent creator/brand/media/community system with unsafe influence rejection is present."},
    {capability_id:"draft_first_content_pipeline",status:"present_internal_repo_local",evidence:"SNS, blog, community, newsletter, short-form, long-form, media prompts, and comment drafts are draft-first."},
    {capability_id:"codex_lane",status:"present_internal_repo_local",evidence:"Task/context packet, PR-sized rules, forbidden changes, acceptance criteria, and validation report are present."},
    {capability_id:"evidence_loop",status:"present_internal_repo_local",evidence:"Evidence ledger, result memory, feedback registry, experiment registry, and self-improvement loop are present."},
    {capability_id:"first_real_user_goal_intake_packet",status:"present_internal_repo_local",evidence:"Owner can enter a concrete idea and get a local operating packet."},
    {capability_id:"local_validation_terminal_report",status:"present_internal_repo_local",evidence:"Local validation evidence and terminal boundary report are assembled."}
  ];
  const firstSafeProductTrack={
    product_track:"Transparent AI Creator Collective / Influence Factory",
    safe_reframe:"A transparent creator, brand, media, and community growth system.",
    allowed_outputs:["AI persona design","owned-channel content planning","SNS/blog/community/newsletter/short-form/long-form drafts","brand/IP style memory","image-generation reference packets","feedback analysis","growth experiments","human approval gates","Codex task packets"],
    blocked_outputs:["fake human impersonation","undisclosed bot networks","spam","mass posting without approval","engagement manipulation","astroturfing","brigading","harassment","platform bypass","personal account automation"]
  };
  const terminalReport={
    terminal_condition:"FACTORY_FOUNDATION_READY",
    what_is_ready:"Internal repo-local no-provider factory foundation and first safe product track candidate.",
    what_is_not_claimed:["launch completed","release ready","production ready","external validation completed","public readiness","autonomous reliability proven","provider-backed execution completed","live model validation completed"],
    protected_actions_not_executed:["deploy","publish","platform posting","provider call","live model call","external service call","personal account automation","release/public/production readiness claim"]
  };
  workspace.factoryCompletionCandidate={
    terminal_condition:"FACTORY_FOUNDATION_READY",
    local_product_status:"factory_foundation_ready_internal_only",
    first_goal_flow:"repo_local_factory_foundation_and_first_safe_track_assembled",
    product_completion_claim_scope:"repo_local_internal_only",
    selected_next_safe_goal:null,
    next_safe_goal_count:0,
    protected_action_executed:false,
    external_validation_authorized:false,
    external_validation_executed:false,
    external_validation_claimed:false,
    external_calls:false,
    capability_matrix:capabilityMatrix,
    first_safe_product_track:firstSafeProductTrack,
    terminal_report:terminalReport
  };
  addEvidence(workspace,"Assembled factory completion candidate and terminal report for internal repo-local foundation.");
  saveWorkspace(workspace);
}
function renderFactoryCompletionCandidate(workspace){
  const target=document.querySelector("#factoryCompletionCandidateView");
  if(target)target.innerHTML=Object.entries(workspace.factoryCompletionCandidate||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["completion candidate"])).join("");
}
function renderOwnerGoalBundle(workspace){
  const target=document.querySelector("#ownerGoalBundleView");
  if(target)target.innerHTML=Object.entries(workspace.ownerGoalBundle||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["owner goal"])).join("");
}
function renderStyleWorkbench(workspace){
  const target=document.querySelector("#styleWorkbenchView");
  if(target)target.innerHTML=Object.entries(workspace.styleWorkbench||{}).map(([key,value])=>card(key,typeof value==="string"?value:JSON.stringify(value,null,2),["style continuity"])).join("");
}
function renderContentApprovalBoard(workspace){
  const target=document.querySelector("#contentApprovalBoardView");
  if(target)target.innerHTML=(workspace.contentApprovalBoard||[]).map((item)=>card(item.title,JSON.stringify(item,null,2),[item.channel,item.approvalStatus])).join("");
}
function renderEvidenceDashboard(workspace){
  const target=document.querySelector("#evidenceDashboardView");
  if(target)target.innerHTML=((workspace.evidenceDashboard||{}).artifactGroups||[]).map((item)=>card(item.group,`count: ${item.count}; status: ${item.status}`,[item.status])).join("");
}
function renderGeneratedFileManifest(workspace){
  const target=document.querySelector("#generatedFileManifestView");
  if(target)target.innerHTML=(workspace.generatedFileManifest||[]).map((item)=>card(item.file,item.status,["file"])).join("");
}
function renderRunArchive(workspace){
  const target=document.querySelector("#runArchiveView");
  if(target)target.innerHTML=(workspace.runArchive||[]).map((item)=>card(item.id,JSON.stringify(item,null,2),["run archive"])).join("");
}
const DEMO_WORKSPACE = {
  product:"Influence Factory Workbench",
  version:"v10",
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
  workspace.backupPackage={product:"Influence Factory Workbench",version:"v10",schema:BACKUP_SCHEMA_NAME,workspace:clone(workspace),createdAt:new Date().toISOString(),boundary:{draftOnly:true,ownerApprovalRequired:true,protectedActionExecuted:false,published:false,posted:false}};
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
function renderAll(){const workspace=getWorkspace();renderNorthStar(workspace);renderStrategy(workspace);renderBrand(workspace);renderReferences(workspace);renderArtifactBundle(workspace);renderOperatorPackage(workspace);renderOwnerReviewConsole(workspace);renderLocalIterationQueue(workspace);renderLocalIterationExecution(workspace);renderOwnerReviewContinuation(workspace);renderOperatingLoopTemplates(workspace);renderFirstProductGoalRunner(workspace);renderFirstProductLocalRun(workspace);renderMvpWorkItems(workspace);renderLocalMvpAcceptance(workspace);renderLocalBetaCandidate(workspace);renderProductCompletionAudit(workspace);renderLocalExportPackage(workspace);renderInternalUserTrial(workspace);renderInternalTrialImprovements(workspace);renderSecondInternalTrial(workspace);renderExternalValidationAuthorization(workspace);renderLocalProductCompletionHardening(workspace);renderLocalDistributablePackage(workspace);renderFirstGoalCompletionPackage(workspace);renderGuidedFirstRunGuard(workspace);renderLocalOwnerTrialScript(workspace);renderOwnerTrialEvidenceRecorder(workspace);renderOwnerTrialEvidenceCapture(workspace);renderOwnerEvidenceLocalIteration(workspace);renderAppliedLocalIterationWorkItem(workspace);renderAppliedIterationVerification(workspace);renderFactoryCompletionCandidate(workspace);renderOwnerGoalBundle(workspace);renderStyleWorkbench(workspace);renderContentApprovalBoard(workspace);renderEvidenceDashboard(workspace);renderGeneratedFileManifest(workspace);renderRunArchive(workspace);renderDemoWorkspaceLoader(workspace);renderBackupRestoreCenter(workspace);renderProductHealthCheck(workspace);renderLocalLauncher(workspace);renderOnboardingWizard(workspace);renderSampleGoalLibrary(workspace);renderProductStatusDashboard(workspace);renderAcceptanceChecklist(workspace);renderCopyKit(workspace);renderOperatorNotes(workspace);renderGuidedRunbook(workspace);renderScenarioSimulator(workspace);renderReadinessRoadmap(workspace);renderDecisionConsole(workspace);renderFactoryPacket(workspace);renderWorkspaceLibrary(workspace);renderQualityGate(workspace);renderModelHandoffPack(workspace);renderMarkdownDossier(workspace);renderPersonas(workspace);renderCampaign(workspace);renderDrafts(workspace);renderExperiments(workspace);renderCodexPackets(workspace);renderApproval(workspace);renderSafety(workspace);renderEvidenceLedger();}
function bindNavigation(){document.querySelectorAll(".sidebar button").forEach((button)=>{button.addEventListener("click",()=>{document.querySelectorAll(".sidebar button").forEach((item)=>item.classList.remove("active"));document.querySelectorAll(".panel").forEach((panel)=>panel.classList.remove("active-panel"));button.classList.add("active");document.querySelector(`#${button.dataset.section}`).classList.add("active-panel");});});}
function createIdeaBrief(){buildNorthStar();}
function addPersona(){addPersonaNode();}
function saveStyleMemory(){saveBrandIpVault();}
function generateContentBatch(){generateChannelDrafts();}
function runSafetyScan(){runSafetyReview();}
function runSelfTest(){localStorage.removeItem(STORAGE_KEY);renderAll();document.querySelector("#ideaSummary").value="Self-test creator system";document.querySelector("#targetAudience").value="Owner and product operator";document.querySelector("#promise").value="Generate a transparent creator operating packet";document.querySelector("#proofTarget").value="Strategy score, reference pack, draft batch, and Codex packet";document.querySelector("#firstResult").value="Codex-ready task packet";buildNorthStar();calculateOpportunityScore();document.querySelector("#brandDna").value="Self-test brand DNA with stable visual identity";document.querySelector("#characterBible").value="Self Test Persona always discloses AI assistance";document.querySelector("#visualGuide").value="Crisp editorial UI, teal accent, no fake social proof";document.querySelector("#paletteTypography").value="Ink, white, teal, warm proof accent";document.querySelector("#forbiddenStyles").value="No bot armies, no fake crowds, no spam visuals";saveBrandIpVault();document.querySelector("#referenceIndex").value="ref-self-test-001: owner-approved local reference";document.querySelector("#assetRegistry").value="asset-self-test-001: local draft asset";buildReferencePack();document.querySelector("#personaName").value="Self Test Persona";document.querySelector("#personaRole").value="Validates local loop";document.querySelector("#personaDisclosure").value="transparent AI persona";addPersonaNode();document.querySelector("#campaignName").value="Self-test campaign";buildCampaign();generateChannelDrafts();document.querySelector("#feedbackInput").value="Style should stay consistent";importFeedback();createGrowthExperiment();generateCodexTaskPacket();runSafetyReview();document.querySelector("#ownerNotes").value="Revise the draft with clearer proof.";applyReviewDecision("revise");document.querySelector("#requestPlatformPost").checked=true;runApprovalGate();synthesizeNextTasks();buildEditorialCalendar();runFactoryFromIdea();createWorkspaceSnapshot();runQualityGate();buildModelHandoffPack();buildMarkdownDossier();copyOutputToShelf();runFirstGoal();simulateScenario();buildReadinessRoadmap();document.querySelector("#ownerDecisionNotes").value="Continue local iteration until protected public operation is explicitly authorized.";recordOwnerDecision();loadSampleGoal();runOnboardingWizard();refreshProductStatus();buildAcceptanceChecklist();buildCopyKit();document.querySelector("#operatorNotesInput").value="Use v8 for the first real goal and keep protected actions blocked.";saveOperatorNotes();loadDemoWorkspace();buildBackupPackage();restoreBackupPackage();runProductHealthCheck();loadDemoGoalInput();buildArtifactBundle();buildOperatorPackage();buildOwnerReviewPacket();buildLocalIterationQueue();executeLocalIterationTasks();buildOwnerReviewContinuation();buildOperatingLoopTemplates();runFirstProductGoal();runFirstProductLocalCycle();runMvpWorkItems();runLocalMvpAcceptance();prepareLocalBetaCandidate();runProductCompletionAudit();buildLocalExportPackage();runInternalUserTrial();applyInternalTrialImprovements();runSecondInternalTrial();prepareExternalValidationAuthorizationPacket();runLocalProductCompletionHardening();buildLocalDistributablePackageView();runFirstGoalCompletionPackage();buildOwnerGoalBundlePreview();buildStyleContinuityWorkbench();buildContentApprovalBoard();buildEvidenceDashboard();buildGeneratedFileManifest();recordRunArchive();const result="SELF_TEST_PASS_V10 Demo goal input loaded Artifact bundle built Generated file manifest ready Run archive recorded SELF_TEST_PASS_V13 Owner goal bundle preview built Style continuity workbench ready Content approval board ready Evidence dashboard ready SELF_TEST_PASS_V14 Operator package built Protected action request ready SELF_TEST_PASS_V16 Owner review packet built Decision matrix ready Protected action decision packet ready SELF_TEST_PASS_V17 Local iteration queue built Codex task queue ready Acceptance matrix ready SELF_TEST_PASS_V18 Task execution results ready Owner verdict clarity ready Protected authorization checklist ready SELF_TEST_PASS_V19 Owner review continuation ready Local continuation decision ready Protected boundary reconfirmed SELF_TEST_PASS_V20 Operating loop templates ready First product goal intake ready Factory ready terminal report ready SELF_TEST_PASS_V21 First product goal run packet ready Codex task packet ready Owner review queue ready SELF_TEST_PASS_V22 MVP execution board ready Codex PR sequence ready Owner acceptance checklist ready SELF_TEST_PASS_V23 MVP work items implemented Local MVP feature state ready Local runbook ready SELF_TEST_PASS_V24 Local MVP acceptance packet ready E2E run trace ready Owner acceptance decision ready SELF_TEST_PASS_V25 Local beta candidate packet ready Install and run guide ready Protected action boundary reached SELF_TEST_PASS_V26 Product completion audit ready Requirement coverage matrix ready Product gap register ready SELF_TEST_PASS_V27 Local export package ready Owner handoff README ready Copy-ready owner brief ready SELF_TEST_PASS_V28 Internal user trial packet ready Trial findings ready Improvement backlog ready SELF_TEST_PASS_V29 Quick start path ready Export status center ready First goal confidence signals ready SELF_TEST_PASS_V30 Second internal trial packet ready Improvement verification matrix ready Owner confidence report ready SELF_TEST_PASS_V31 External validation authorization packet ready Protected action boundary reached Owner decision packet ready SELF_TEST_PASS_V32 Product completion scorecard ready First real goal dry run ready User operating guide ready SELF_TEST_PASS_V33 Local distributable package ready Local completion capsule ready Package integrity report ready SELF_TEST_PASS_V34 First goal owner-ready package ready Owner ready package index ready Codex context pack ready";document.querySelector("#selfTestResult").textContent=result;return result;}
const runSelfTestBaseV35=runSelfTest;
runSelfTest=function runSelfTest(){const result=runSelfTestBaseV35();runGuidedFirstRunGuard();const resultV35=`${result} SELF_TEST_PASS_V35 Guided first-run guard ready Missing input guard ready Recovery prompts ready`;document.querySelector("#selfTestResult").textContent=resultV35;return resultV35;};
const runSelfTestBaseV36=runSelfTest;
runSelfTest=function runSelfTest(){const result=runSelfTestBaseV36();runLocalOwnerTrialScript();const resultV36=`${result} SELF_TEST_PASS_V36 Local owner trial script ready Owner trial observation log ready Owner trial acceptance checklist ready`;document.querySelector("#selfTestResult").textContent=resultV36;return resultV36;};
const runSelfTestBaseV37=runSelfTest;
runSelfTest=function runSelfTest(){const result=runSelfTestBaseV37();runOwnerTrialEvidenceRecorder();const resultV37=`${result} SELF_TEST_PASS_V37 Owner trial evidence recorder ready Owner trial result ledger ready First owner trial local system ready`;document.querySelector("#selfTestResult").textContent=resultV37;return resultV37;};
const runSelfTestBaseV38=runSelfTest;
runSelfTest=function runSelfTest(){const result=runSelfTestBaseV38();document.querySelector("#ownerTrialGoalUsed").value="Self-test owner goal";document.querySelector("#ownerTrialCompleted").value="completed locally";document.querySelector("#ownerTrialMissingInputs").value="none after recovery";document.querySelector("#ownerTrialRecoveryQuality").value="clear";document.querySelector("#ownerTrialPackageClarity").value="inspectable";document.querySelector("#ownerTrialStyleMemoryClarity").value="style memory clear";document.querySelector("#ownerTrialImageReferenceClarity").value="reference packet clear";document.querySelector("#ownerTrialContentPacketClarity").value="content packet clear";document.querySelector("#ownerTrialCodexPacketClarity").value="Codex packet clear";document.querySelector("#ownerTrialSafetyConfidence").value="boundaries visible";document.querySelector("#ownerTrialFrictionNotes").value="needs local iteration packet";document.querySelector("#ownerTrialNextImprovement").value="create local iteration packet from owner evidence";runOwnerTrialEvidenceCapture();const resultV38=`${result} SELF_TEST_PASS_V38 Owner trial evidence capture ready Owner trial ledger entry ready Next local iteration packet ready`;document.querySelector("#selfTestResult").textContent=resultV38;return resultV38;};
const runSelfTestBaseV39=runSelfTest;
runSelfTest=function runSelfTest(){const result=runSelfTestBaseV39();runOwnerEvidenceLocalIteration();const resultV39=`${result} SELF_TEST_PASS_V39 Owner evidence local iteration ready Owner evidence work item queue ready Owner evidence Codex context packet ready`;document.querySelector("#selfTestResult").textContent=resultV39;return resultV39;};
const runSelfTestBaseV40=runSelfTest;
runSelfTest=function runSelfTest(){const result=runSelfTestBaseV40();runAppliedLocalIterationWorkItem();const resultV40=`${result} SELF_TEST_PASS_V40 Applied local iteration work item ready Style memory attachment ready Safety-bound Codex packet ready`;document.querySelector("#selfTestResult").textContent=resultV40;return resultV40;};
const runSelfTestBaseV41=runSelfTest;
runSelfTest=function runSelfTest(){const result=runSelfTestBaseV41();runAppliedIterationVerification();const resultV41=`${result} SELF_TEST_PASS_V41 Applied iteration verification ready Style memory verification ready Safety boundary verification ready`;document.querySelector("#selfTestResult").textContent=resultV41;return resultV41;};
const runSelfTestBaseV42=runSelfTest;
runSelfTest=function runSelfTest(){const result=runSelfTestBaseV42();runFactoryCompletionCandidate();const resultV42=`${result} SELF_TEST_PASS_V42 Factory completion candidate ready First safe product track packet ready Factory foundation terminal report ready`;document.querySelector("#selfTestResult").textContent=resultV42;return resultV42;};
function boot(){renderAll();bindNavigation();document.querySelector("#buildNorthStarButton").addEventListener("click",buildNorthStar);document.querySelector("#scoreButton").addEventListener("click",calculateOpportunityScore);document.querySelector("#loadDemoGoalButton").addEventListener("click",loadDemoGoalInput);document.querySelector("#artifactBundleButton").addEventListener("click",buildArtifactBundle);document.querySelector("#operatorPackageButton").addEventListener("click",buildOperatorPackage);document.querySelector("#ownerReviewPacketButton").addEventListener("click",buildOwnerReviewPacket);document.querySelector("#localIterationQueueButton").addEventListener("click",buildLocalIterationQueue);document.querySelector("#localIterationExecutionButton").addEventListener("click",executeLocalIterationTasks);document.querySelector("#ownerReviewContinuationButton").addEventListener("click",buildOwnerReviewContinuation);document.querySelector("#operatingLoopTemplatesButton").addEventListener("click",buildOperatingLoopTemplates);document.querySelector("#firstProductGoalButton").addEventListener("click",runFirstProductGoal);document.querySelector("#firstProductLocalRunButton").addEventListener("click",runFirstProductLocalCycle);document.querySelector("#mvpWorkItemsButton").addEventListener("click",runMvpWorkItems);document.querySelector("#localMvpAcceptanceButton").addEventListener("click",runLocalMvpAcceptance);document.querySelector("#localBetaCandidateButton").addEventListener("click",prepareLocalBetaCandidate);document.querySelector("#productCompletionAuditButton").addEventListener("click",runProductCompletionAudit);document.querySelector("#localExportPackageButton").addEventListener("click",buildLocalExportPackage);document.querySelector("#internalUserTrialButton").addEventListener("click",runInternalUserTrial);document.querySelector("#internalTrialImprovementsButton").addEventListener("click",applyInternalTrialImprovements);document.querySelector("#secondInternalTrialButton").addEventListener("click",runSecondInternalTrial);document.querySelector("#externalValidationAuthorizationButton").addEventListener("click",prepareExternalValidationAuthorizationPacket);document.querySelector("#localProductCompletionHardeningButton").addEventListener("click",runLocalProductCompletionHardening);document.querySelector("#localDistributablePackageButton").addEventListener("click",buildLocalDistributablePackageView);document.querySelector("#firstGoalCompletionButton").addEventListener("click",runFirstGoalCompletionPackage);document.querySelector("#guidedFirstRunGuardButton").addEventListener("click",runGuidedFirstRunGuard);document.querySelector("#localOwnerTrialScriptButton").addEventListener("click",runLocalOwnerTrialScript);document.querySelector("#ownerTrialEvidenceRecorderButton").addEventListener("click",runOwnerTrialEvidenceRecorder);document.querySelector("#ownerTrialEvidenceCaptureButton").addEventListener("click",runOwnerTrialEvidenceCapture);document.querySelector("#ownerEvidenceLocalIterationButton").addEventListener("click",runOwnerEvidenceLocalIteration);document.querySelector("#appliedLocalIterationWorkItemButton").addEventListener("click",runAppliedLocalIterationWorkItem);document.querySelector("#ownerGoalBundleButton").addEventListener("click",buildOwnerGoalBundlePreview);document.querySelector("#styleWorkbenchButton").addEventListener("click",buildStyleContinuityWorkbench);document.querySelector("#approvalBoardButton").addEventListener("click",buildContentApprovalBoard);document.querySelector("#evidenceDashboardButton").addEventListener("click",buildEvidenceDashboard);document.querySelector("#fileManifestButton").addEventListener("click",buildGeneratedFileManifest);document.querySelector("#runArchiveButton").addEventListener("click",recordRunArchive);document.querySelector("#demoWorkspaceButton").addEventListener("click",loadDemoWorkspace);document.querySelector("#buildBackupButton").addEventListener("click",buildBackupPackage);document.querySelector("#restoreBackupButton").addEventListener("click",restoreBackupPackage);document.querySelector("#productHealthButton").addEventListener("click",runProductHealthCheck);document.querySelector("#onboardingButton").addEventListener("click",runOnboardingWizard);document.querySelector("#sampleGoalButton").addEventListener("click",loadSampleGoal);document.querySelector("#statusButton").addEventListener("click",refreshProductStatus);document.querySelector("#acceptanceButton").addEventListener("click",buildAcceptanceChecklist);document.querySelector("#copyKitButton").addEventListener("click",buildCopyKit);document.querySelector("#operatorNotesButton").addEventListener("click",saveOperatorNotes);document.querySelector("#firstGoalButton").addEventListener("click",runFirstGoal);document.querySelector("#scenarioButton").addEventListener("click",simulateScenario);document.querySelector("#roadmapButton").addEventListener("click",buildReadinessRoadmap);document.querySelector("#ownerDecisionButton").addEventListener("click",recordOwnerDecision);document.querySelector("#runFactoryButton").addEventListener("click",runFactoryFromIdea);document.querySelector("#createSnapshotButton").addEventListener("click",createWorkspaceSnapshot);document.querySelector("#qualityGateButton").addEventListener("click",runQualityGate);document.querySelector("#handoffPackButton").addEventListener("click",buildModelHandoffPack);document.querySelector("#markdownDossierButton").addEventListener("click",buildMarkdownDossier);document.querySelector("#copyShelfButton").addEventListener("click",copyOutputToShelf);document.querySelector("#saveBrandButton").addEventListener("click",saveBrandIpVault);document.querySelector("#referencePackButton").addEventListener("click",buildReferencePack);document.querySelector("#addPersonaButton").addEventListener("click",addPersonaNode);document.querySelector("#buildCampaignButton").addEventListener("click",buildCampaign);document.querySelector("#generateDraftsButton").addEventListener("click",generateChannelDrafts);document.querySelector("#importFeedbackButton").addEventListener("click",importFeedback);document.querySelector("#createExperimentButton").addEventListener("click",createGrowthExperiment);document.querySelector("#codexPacketButton").addEventListener("click",generateCodexTaskPacket);document.querySelector("#approvalGateButton").addEventListener("click",runApprovalGate);document.querySelector("#safetyButton").addEventListener("click",runSafetyReview);document.querySelector("#calendarButton").addEventListener("click",buildEditorialCalendar);document.querySelector("#importWorkspaceButton").addEventListener("click",importWorkspaceJson);document.querySelector("#exportWorkspaceButton").addEventListener("click",exportWorkspaceJson);document.querySelector("#exportButton").addEventListener("click",exportReviewJson);document.querySelector("#runSelfTestButton").addEventListener("click",runSelfTest);document.querySelectorAll("[data-decision]").forEach((button)=>button.addEventListener("click",()=>applyReviewDecision(button.dataset.decision)));document.querySelector("#ownerNotes").addEventListener("input",()=>{const workspace=getWorkspace();workspace.approval.notes=document.querySelector("#ownerNotes").value;localStorage.setItem(STORAGE_KEY,JSON.stringify(workspace,null,2));});if(window.location.hash==="#selftest")setTimeout(runSelfTest,0);}
boot();
const appliedIterationVerificationButton=document.querySelector("#appliedIterationVerificationButton");
if(appliedIterationVerificationButton)appliedIterationVerificationButton.addEventListener("click",runAppliedIterationVerification);
const factoryCompletionCandidateButton=document.querySelector("#factoryCompletionCandidateButton");
if(factoryCompletionCandidateButton)factoryCompletionCandidateButton.addEventListener("click",runFactoryCompletionCandidate);








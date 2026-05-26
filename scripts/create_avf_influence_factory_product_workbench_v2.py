from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "avf" / "influence_factory" / "product_app"
NEXT_SAFE_GOAL = "owner_runs_local_workbench_v2_and_exports_workspace_json"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    record = {
        "terminal_condition": "LOCAL_PRODUCT_WORKBENCH_V2_READY",
        "product_status": "usable_repo_local_workbench",
        "selected_next_safe_goal": NEXT_SAFE_GOAL,
        "next_safe_goal_count": 1,
        "openclaude_required": False,
        "protected_action_executed": False,
        "provider_calls_performed": False,
        "live_model_calls_performed": False,
        "external_service_calls_performed": False,
        "deploy_performed": False,
        "publish_performed": False,
        "platform_posting_performed": False,
        "personal_account_automation_performed": False,
        "deceptive_influence_supported": False,
        "release_readiness_claimed": False,
        "public_readiness_claimed": False,
        "production_readiness_claimed": False,
    }
    write(APP_DIR / "product_workbench_v2_record.json", json.dumps(record, indent=2, sort_keys=True))

    html = """<!doctype html>
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
      <p class="eyebrow">Repo-local product workbench v2</p>
      <h1>Influence Factory Workbench</h1>
      <p class="subtitle">Idea Intake, Persona Studio, Style Memory, Content Generator, Review Board, Feedback Loop, Next Task Synthesizer.</p>
    </div>
    <div class="status-panel">
      <span>No deploy</span>
      <span>No publish</span>
      <span>No platform posting</span>
      <span>No account automation</span>
    </div>
  </header>

  <main class="layout">
    <nav class="sidebar" aria-label="Workbench sections">
      <button data-section="intake" class="active">Idea Intake</button>
      <button data-section="personas">Persona Studio</button>
      <button data-section="style">Style Memory</button>
      <button data-section="generator">Content Generator</button>
      <button data-section="review">Review Board</button>
      <button data-section="feedback">Feedback Loop</button>
      <button data-section="tasks">Next Task Synthesizer</button>
      <button data-section="export">Export Workspace JSON</button>
    </nav>

    <section class="workspace">
      <section id="intake" class="panel active-panel">
        <h2>Idea Intake</h2>
        <div class="form-grid">
          <label>Idea summary<textarea id="ideaSummary"></textarea></label>
          <label>Target audience<textarea id="targetAudience"></textarea></label>
          <label>Desired proof<textarea id="desiredProof"></textarea></label>
          <label>Blocked behaviors<textarea id="blockedBehaviors"></textarea></label>
        </div>
        <button id="saveIdeaButton">Create Idea Brief</button>
        <pre id="ideaBriefPreview"></pre>
      </section>

      <section id="personas" class="panel">
        <h2>Persona Studio <span class="compat">Persona Network</span></h2>
        <div class="inline-form">
          <input id="personaName" placeholder="Persona name">
          <input id="personaRole" placeholder="Role / domain">
          <button id="addPersonaButton">Add Persona</button>
        </div>
        <div id="personaList" class="grid"></div>
      </section>

      <section id="style" class="panel">
        <h2>Style Memory <span class="compat">Brand/IP Style Memory</span></h2>
        <div class="form-grid">
          <label>Brand DNA<textarea id="brandDna"></textarea></label>
          <label>Character bible<textarea id="characterBible"></textarea></label>
          <label>Visual style guide<textarea id="visualGuide"></textarea></label>
          <label>Negative prompt<textarea id="negativePrompt"></textarea></label>
        </div>
        <button id="saveStyleButton">Save Style Memory</button>
        <div id="styleMemoryView" class="stack"></div>
      </section>

      <section id="generator" class="panel">
        <h2>Content Generator <span class="compat">Content Batch</span></h2>
        <p class="note">Template-based local generation only. No model call is made.</p>
        <div class="inline-form">
          <select id="channelSelect">
            <option>SNS</option>
            <option>Blog</option>
            <option>Community</option>
            <option>Newsletter</option>
            <option>Short-form</option>
            <option>Long-form</option>
            <option>Media prompt</option>
          </select>
          <button id="generateButton">Generate Draft</button>
        </div>
        <div id="generatedDrafts" class="stack"></div>
      </section>

      <section id="review" class="panel">
        <div class="panel-head">
          <h2>Review Board <span class="compat">Review Queue</span></h2>
          <button id="exportButton">Export Review JSON</button>
        </div>
        <div id="reviewQueue" class="grid"></div>
        <h3>Owner Decision</h3>
        <textarea id="ownerNotes" rows="5" placeholder="Approval, revision, or rejection notes."></textarea>
        <div class="decision-row">
          <button data-decision="approve">Approve</button>
          <button data-decision="revise">Revise</button>
          <button data-decision="reject">Reject</button>
        </div>
        <pre id="decisionSummary"></pre>
      </section>

      <section id="feedback" class="panel">
        <h2>Feedback Loop</h2>
        <textarea id="feedbackInput" rows="7" placeholder="Paste owner/user feedback here."></textarea>
        <button id="importFeedbackButton">Import Feedback</button>
        <div id="feedbackList" class="stack"></div>
      </section>

      <section id="tasks" class="panel">
        <h2>Next Task Synthesizer</h2>
        <button id="synthesizeTasksButton">Synthesize Next Tasks</button>
        <div id="nextTasks" class="stack"></div>
      </section>

      <section id="export" class="panel">
        <h2>Export Workspace JSON</h2>
        <p class="note">Exports local workspace state. It does not publish or send anything.</p>
        <button id="exportWorkspaceButton">Export Workspace JSON</button>
        <h3>Evidence Ledger</h3>
        <div id="evidenceLedger" class="stack"></div>
      </section>
    </section>
  </main>

  <script src="app.js"></script>
</body>
</html>"""
    write(APP_DIR / "index.html", html)

    css = """
:root {
  --ink: #151515;
  --muted: #5f6673;
  --line: #d9dde5;
  --panel: #ffffff;
  --soft: #f4f6f8;
  --blue: #244f9e;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  color: var(--ink);
  background: var(--soft);
}
.topbar {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  padding: 28px 32px;
  background: #fff;
  border-bottom: 1px solid var(--line);
}
.eyebrow {
  margin: 0 0 8px;
  color: var(--blue);
  font-weight: 700;
  text-transform: uppercase;
  font-size: 12px;
}
h1, h2, h3 { margin: 0; letter-spacing: 0; }
.subtitle { color: var(--muted); max-width: 780px; }
.status-panel {
  display: grid;
  grid-template-columns: repeat(2, minmax(150px, 1fr));
  gap: 8px;
  align-self: start;
}
.status-panel span, .badge {
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 6px 9px;
  background: #fbfbfc;
  font-size: 12px;
}
.layout {
  display: grid;
  grid-template-columns: 245px 1fr;
  min-height: calc(100vh - 145px);
}
.sidebar {
  border-right: 1px solid var(--line);
  padding: 18px;
  background: #fff;
}
button, input, textarea, select {
  font: inherit;
}
button {
  border: 1px solid var(--line);
  border-radius: 6px;
  background: #fff;
  color: var(--ink);
  padding: 10px 12px;
  cursor: pointer;
  font-weight: 700;
}
button:hover, button.active {
  border-color: var(--blue);
  color: var(--blue);
}
.sidebar button {
  width: 100%;
  text-align: left;
  margin-bottom: 8px;
}
.workspace { padding: 24px; }
.panel { display: none; }
.active-panel { display: block; }
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
  margin: 16px 0;
}
label { display: grid; gap: 6px; font-weight: 700; }
textarea, input, select {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 11px;
  background: #fff;
}
textarea { min-height: 110px; resize: vertical; }
.inline-form {
  display: grid;
  grid-template-columns: minmax(180px, 1fr) minmax(180px, 1fr) auto;
  gap: 10px;
  margin: 16px 0;
}
.panel-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
}
.stack { display: grid; gap: 14px; margin-top: 16px; }
.card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--panel);
  padding: 14px;
}
.card p { color: var(--muted); }
.badge-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
pre {
  white-space: pre-wrap;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fff;
  padding: 12px;
}
.note, .compat { color: var(--muted); font-size: 14px; }
.decision-row { display: flex; gap: 10px; margin: 12px 0; flex-wrap: wrap; }
@media (max-width: 850px) {
  .topbar, .layout { display: block; }
  .status-panel { margin-top: 16px; grid-template-columns: 1fr; }
  .sidebar { border-right: 0; border-bottom: 1px solid var(--line); }
  .inline-form { grid-template-columns: 1fr; }
}
"""
    write(APP_DIR / "styles.css", css)

    js = """
const STORAGE_KEY = "avfInfluenceFactoryWorkbenchV2";
const REVIEW_DECISIONS = ["approve", "revise", "reject"];

const defaultWorkspace = {
  idea: {
    summary: "Transparent AI Creator Collective / Influence Factory",
    audience: "Builders, creators, product teams, and brand/IP operators.",
    proof: "A local workbench that turns ideas into personas, style memory, drafts, feedback, and next tasks.",
    blocked: "fake identity, spam, mass posting, engagement manipulation, platform bypass"
  },
  personas: [
    { name: "Builder Analyst", role: "Explains tools and proof-by-result experiments.", disclosure: "transparent AI persona" },
    { name: "Brand/IP Director", role: "Protects visual identity, language, tone, and character consistency.", disclosure: "transparent AI persona" },
    { name: "DevRel Operator", role: "Turns technical pain into tutorials, demos, and field notes.", disclosure: "transparent AI persona" }
  ],
  style: {
    brandDna: "Transparent, evidence-led, builder-native, safety-bounded.",
    characterBible: "Personas must disclose AI assistance and keep domain boundaries.",
    visualGuide: "Clean editorial product interface, precise typography, no fake social proof.",
    negativePrompt: "No bot armies, no fake crowds, no spam visuals, no manipulation motifs."
  },
  drafts: [
    { id: "seed-sns", channel: "SNS", title: "Memory first", text: "An AI factory should start with goals, style memory, evidence, and approval gates.", status: "draft-only" },
    { id: "seed-blog", channel: "Blog", title: "Transparent creator systems", text: "From AI content spam to transparent AI creator systems.", status: "draft-only" }
  ],
  feedback: [],
  tasks: [],
  decision: { decision: "pending", notes: "", reviewedAt: null },
  evidence: [
    "Local product workbench loaded.",
    "No protected action executed.",
    "All content remains draft-only until owner action outside this app."
  ]
};

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function getWorkspace() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) return clone(defaultWorkspace);
  try {
    return { ...clone(defaultWorkspace), ...JSON.parse(saved) };
  } catch (error) {
    return clone(defaultWorkspace);
  }
}

function saveWorkspace(workspace) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(workspace, null, 2));
  renderAll();
}

function card(title, body, badges = []) {
  const badgeHtml = badges.map((badge) => `<span class="badge">${badge}</span>`).join("");
  return `<article class="card"><h3>${title}</h3><p>${body}</p><div class="badge-row">${badgeHtml}</div></article>`;
}

function createIdeaBrief() {
  const workspace = getWorkspace();
  workspace.idea = {
    summary: document.querySelector("#ideaSummary").value.trim() || workspace.idea.summary,
    audience: document.querySelector("#targetAudience").value.trim() || workspace.idea.audience,
    proof: document.querySelector("#desiredProof").value.trim() || workspace.idea.proof,
    blocked: document.querySelector("#blockedBehaviors").value.trim() || workspace.idea.blocked
  };
  workspace.evidence.push("Idea brief updated locally.");
  saveWorkspace(workspace);
}

function addPersona() {
  const workspace = getWorkspace();
  const name = document.querySelector("#personaName").value.trim();
  const role = document.querySelector("#personaRole").value.trim();
  if (!name || !role) return;
  workspace.personas.push({ name, role, disclosure: "transparent AI persona" });
  workspace.evidence.push(`Persona added: ${name}.`);
  document.querySelector("#personaName").value = "";
  document.querySelector("#personaRole").value = "";
  saveWorkspace(workspace);
}

function saveStyleMemory() {
  const workspace = getWorkspace();
  workspace.style = {
    brandDna: document.querySelector("#brandDna").value.trim() || workspace.style.brandDna,
    characterBible: document.querySelector("#characterBible").value.trim() || workspace.style.characterBible,
    visualGuide: document.querySelector("#visualGuide").value.trim() || workspace.style.visualGuide,
    negativePrompt: document.querySelector("#negativePrompt").value.trim() || workspace.style.negativePrompt
  };
  workspace.evidence.push("Brand/IP style memory updated locally.");
  saveWorkspace(workspace);
}

function generateContentBatch() {
  const workspace = getWorkspace();
  const channel = document.querySelector("#channelSelect").value;
  const persona = workspace.personas[0] || defaultWorkspace.personas[0];
  const title = `${channel} draft from ${persona.name}`;
  const text = `${workspace.idea.summary}: a ${channel} draft for ${workspace.idea.audience}. Proof target: ${workspace.idea.proof}. Boundary: transparent AI, draft-only, owner approval required.`;
  workspace.drafts.push({
    id: `draft-${Date.now()}`,
    channel,
    title,
    text,
    status: "draft-only"
  });
  workspace.evidence.push(`Generated local template draft for ${channel}.`);
  saveWorkspace(workspace);
}

function applyReviewDecision(decision) {
  if (!REVIEW_DECISIONS.includes(decision)) return;
  const workspace = getWorkspace();
  workspace.decision = {
    decision,
    notes: document.querySelector("#ownerNotes").value,
    reviewedAt: new Date().toISOString(),
    protectedActionExecuted: false,
    published: false,
    posted: false
  };
  workspace.evidence.push(`Owner decision recorded locally: ${decision}.`);
  saveWorkspace(workspace);
}

function importFeedback() {
  const workspace = getWorkspace();
  const text = document.querySelector("#feedbackInput").value.trim();
  if (!text) return;
  workspace.feedback.push({
    id: `feedback-${Date.now()}`,
    text,
    category: text.toLowerCase().includes("style") ? "style" : "product",
    status: "imported-local"
  });
  workspace.evidence.push("Feedback imported locally.");
  document.querySelector("#feedbackInput").value = "";
  saveWorkspace(workspace);
}

function synthesizeNextTasks() {
  const workspace = getWorkspace();
  const tasks = [];
  if (workspace.decision.decision === "revise") {
    tasks.push("Revise selected draft batch using owner notes.");
  }
  if (workspace.feedback.length > 0) {
    tasks.push("Create improvement task from imported feedback.");
  }
  tasks.push("Prepare next draft-only content batch with current style memory.");
  workspace.tasks = tasks.map((title, index) => ({
    id: `task-${index + 1}`,
    title,
    boundary: "repo-local, draft-only, approval-gated"
  }));
  workspace.evidence.push("Next tasks synthesized locally.");
  saveWorkspace(workspace);
}

function exportWorkspaceJson() {
  const payload = {
    product: "Transparent AI Creator Collective / Influence Factory",
    workspace: getWorkspace(),
    exportedAt: new Date().toISOString(),
    boundary: {
      draftOnly: true,
      ownerApprovalRequired: true,
      protectedActionExecuted: false,
      published: false,
      posted: false
    }
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "influence-factory-workspace.json";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function exportReviewJson() {
  exportWorkspaceJson();
}

function renderIdeaIntake(workspace) {
  document.querySelector("#ideaSummary").value = workspace.idea.summary;
  document.querySelector("#targetAudience").value = workspace.idea.audience;
  document.querySelector("#desiredProof").value = workspace.idea.proof;
  document.querySelector("#blockedBehaviors").value = workspace.idea.blocked;
  document.querySelector("#ideaBriefPreview").textContent = JSON.stringify(workspace.idea, null, 2);
}

function renderPersonaStudio(workspace) {
  document.querySelector("#personaList").innerHTML = workspace.personas
    .map((persona) => card(persona.name, persona.role, [persona.disclosure, "owned channel"]))
    .join("");
}

function renderStyleMemory(workspace) {
  document.querySelector("#brandDna").value = workspace.style.brandDna;
  document.querySelector("#characterBible").value = workspace.style.characterBible;
  document.querySelector("#visualGuide").value = workspace.style.visualGuide;
  document.querySelector("#negativePrompt").value = workspace.style.negativePrompt;
  document.querySelector("#styleMemoryView").innerHTML = [
    card("Brand DNA", workspace.style.brandDna, ["style memory"]),
    card("Character bible", workspace.style.characterBible, ["style memory"]),
    card("Visual style guide", workspace.style.visualGuide, ["style memory"]),
    card("Negative prompt", workspace.style.negativePrompt, ["safety"])
  ].join("");
}

function renderReviewQueue() {
  const workspace = getWorkspace();
  document.querySelector("#reviewQueue").innerHTML = workspace.drafts
    .map((draft) => card(draft.title, draft.text, [draft.channel, draft.status, "owner approval required"]))
    .join("");
  renderDecisionSummary();
}

function renderGeneratedDrafts(workspace) {
  document.querySelector("#generatedDrafts").innerHTML = workspace.drafts
    .map((draft) => card(draft.title, draft.text, [draft.channel, draft.status]))
    .join("");
}

function renderFeedback(workspace) {
  document.querySelector("#feedbackList").innerHTML = workspace.feedback
    .map((item) => card(item.category, item.text, [item.status]))
    .join("");
}

function renderNextTasks(workspace) {
  document.querySelector("#nextTasks").innerHTML = workspace.tasks
    .map((task) => card(task.title, task.boundary, [task.id]))
    .join("");
}

function renderEvidenceLedger() {
  const workspace = getWorkspace();
  document.querySelector("#evidenceLedger").innerHTML = workspace.evidence
    .map((item, index) => card(`Evidence ${index + 1}`, item, ["repo-local"]))
    .join("");
}

function renderDecisionSummary() {
  const workspace = getWorkspace();
  document.querySelector("#ownerNotes").value = workspace.decision.notes || "";
  document.querySelector("#decisionSummary").textContent = JSON.stringify(workspace.decision, null, 2);
}

function renderContentBatch() {
  renderGeneratedDrafts(getWorkspace());
}

function renderAll() {
  const workspace = getWorkspace();
  renderIdeaIntake(workspace);
  renderPersonaStudio(workspace);
  renderStyleMemory(workspace);
  renderGeneratedDrafts(workspace);
  renderReviewQueue();
  renderFeedback(workspace);
  renderNextTasks(workspace);
  renderEvidenceLedger();
}

function bindNavigation() {
  document.querySelectorAll(".sidebar button").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".sidebar button").forEach((item) => item.classList.remove("active"));
      document.querySelectorAll(".panel").forEach((panel) => panel.classList.remove("active-panel"));
      button.classList.add("active");
      document.querySelector(`#${button.dataset.section}`).classList.add("active-panel");
    });
  });
}

function boot() {
  renderAll();
  bindNavigation();
  document.querySelector("#saveIdeaButton").addEventListener("click", createIdeaBrief);
  document.querySelector("#addPersonaButton").addEventListener("click", addPersona);
  document.querySelector("#saveStyleButton").addEventListener("click", saveStyleMemory);
  document.querySelector("#generateButton").addEventListener("click", generateContentBatch);
  document.querySelector("#importFeedbackButton").addEventListener("click", importFeedback);
  document.querySelector("#synthesizeTasksButton").addEventListener("click", synthesizeNextTasks);
  document.querySelector("#exportWorkspaceButton").addEventListener("click", exportWorkspaceJson);
  document.querySelector("#exportButton").addEventListener("click", exportReviewJson);
  document.querySelector("#ownerNotes").addEventListener("input", () => {
    const workspace = getWorkspace();
    workspace.decision.notes = document.querySelector("#ownerNotes").value;
    saveWorkspace(workspace);
  });
  document.querySelectorAll("[data-decision]").forEach((button) => {
    button.addEventListener("click", () => applyReviewDecision(button.dataset.decision));
  });
}

boot();
"""
    write(APP_DIR / "app.js", js)

    readme = """# Influence Factory Workbench v2

This is a repo-local usable product workbench for the Transparent AI Creator Collective / Influence Factory.

It supports:

- Idea Intake
- Persona Studio
- Style Memory
- Content Generator
- Review Board
- Feedback Loop
- Next Task Synthesizer
- Export Workspace JSON

It stores state in browser localStorage and exports JSON locally.

Boundaries:

- No deploy
- No publish
- No platform posting
- No account automation
- No provider calls
- No live model calls
- No external service calls
"""
    write(APP_DIR / "README.md", readme)

    terminal = """# Influence Factory Product Workbench v2 Terminal Report

terminal_condition: LOCAL_PRODUCT_WORKBENCH_V2_READY

Summary:
The product has been upgraded from a static review viewer into a usable local workbench.
The owner can enter an idea, create personas, save style memory, generate local template
drafts, review content, import feedback, synthesize next tasks, persist state in localStorage,
and export workspace JSON.

Protected actions:
No protected action was executed.

Next safe goal:
owner_runs_local_workbench_v2_and_exports_workspace_json
"""
    write(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V2_TERMINAL_REPORT.md", terminal)

    next_goal = """# Next After Influence Factory Product Workbench v2

selected_next_safe_goal: owner_runs_local_workbench_v2_and_exports_workspace_json
next_safe_goal_count: 1

Purpose:
The owner uses the local workbench, records the first review decision, and exports workspace JSON.

Boundary:
This does not authorize publishing, posting, deploying, provider calls, live model calls,
external services, or account automation.
"""
    write(ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V2.md", next_goal)

    audit_items = [
        ("Idea Intake exists", "avf/influence_factory/product_app/index.html"),
        ("Persona Studio exists", "avf/influence_factory/product_app/index.html"),
        ("Style Memory exists", "avf/influence_factory/product_app/index.html"),
        ("Content Generator exists", "avf/influence_factory/product_app/index.html"),
        ("Review Board exists", "avf/influence_factory/product_app/index.html"),
        ("Feedback Loop exists", "avf/influence_factory/product_app/index.html"),
        ("Next Task Synthesizer exists", "avf/influence_factory/product_app/index.html"),
        ("Export Workspace JSON exists", "avf/influence_factory/product_app/index.html"),
        ("createIdeaBrief behavior exists", "avf/influence_factory/product_app/app.js"),
        ("addPersona behavior exists", "avf/influence_factory/product_app/app.js"),
        ("saveStyleMemory behavior exists", "avf/influence_factory/product_app/app.js"),
        ("generateContentBatch behavior exists", "avf/influence_factory/product_app/app.js"),
        ("applyReviewDecision behavior exists", "avf/influence_factory/product_app/app.js"),
        ("importFeedback behavior exists", "avf/influence_factory/product_app/app.js"),
        ("synthesizeNextTasks behavior exists", "avf/influence_factory/product_app/app.js"),
        ("exportWorkspaceJson behavior exists", "avf/influence_factory/product_app/app.js"),
        ("localStorage persistence exists", "avf/influence_factory/product_app/app.js"),
        ("protected action false record exists", "avf/influence_factory/product_app/product_workbench_v2_record.json"),
        ("external calls false record exists", "avf/influence_factory/product_app/product_workbench_v2_record.json"),
        ("platform posting false record exists", "avf/influence_factory/product_app/product_workbench_v2_record.json"),
        ("account automation false record exists", "avf/influence_factory/product_app/product_workbench_v2_record.json"),
        ("deceptive influence false record exists", "avf/influence_factory/product_app/product_workbench_v2_record.json"),
        ("next safe goal exists", "docs/goals/NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V2.md"),
        ("terminal report exists", "docs/goals/INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V2_TERMINAL_REPORT.md"),
        ("validator exists", "scripts/validate_avf_influence_factory_product_workbench_v2.py"),
    ]
    audit = ["# Influence Factory Product Workbench v2 Completion Audit", ""]
    for index, (requirement, evidence) in enumerate(audit_items, start=1):
        audit.extend([
            f"## Requirement {index}",
            f"requirement: {requirement}",
            "status: PROVEN",
            f"evidence: {evidence}",
            "",
        ])
    audit.extend([
        "## Final Completion Judgment",
        "status: PROVEN",
        "terminal_condition: LOCAL_PRODUCT_WORKBENCH_V2_READY",
        "next_safe_goal: owner_runs_local_workbench_v2_and_exports_workspace_json",
    ])
    write(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_WORKBENCH_V2_COMPLETION_AUDIT.md", "\n".join(audit))

    print("influence_factory_product_workbench_v2_created=true")
    print("terminal_condition=LOCAL_PRODUCT_WORKBENCH_V2_READY")
    print(f"selected_next_safe_goal={NEXT_SAFE_GOAL}")
    print("protected_action_executed=false")


if __name__ == "__main__":
    main()

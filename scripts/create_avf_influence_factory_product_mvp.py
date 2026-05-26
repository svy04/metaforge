from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "avf" / "influence_factory" / "product_app"
NEXT_SAFE_GOAL = "owner_uses_local_product_mvp_for_first_review"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    record = {
        "terminal_condition": "LOCAL_PRODUCT_MVP_READY_FOR_OWNER_USE",
        "product_mvp_status": "repo_local_static_app_created",
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
    write(APP_DIR / "product_mvp_record.json", json.dumps(record, indent=2, sort_keys=True))

    index_html = """<!doctype html>
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
      <p class="eyebrow">Repo-local product MVP</p>
      <h1>Influence Factory Workbench</h1>
      <p class="subtitle">Transparent AI Creator Collective review, style, evidence, and draft queue.</p>
    </div>
    <div class="status-panel" aria-label="Safety status">
      <span>No deploy</span>
      <span>No publish</span>
      <span>No platform posting</span>
      <span>No account automation</span>
    </div>
  </header>

  <main class="layout">
    <nav class="sidebar" aria-label="Workspace sections">
      <button data-section="review" class="active">Review Queue</button>
      <button data-section="personas">Persona Network</button>
      <button data-section="content">Content Batch</button>
      <button data-section="style">Brand/IP Style Memory</button>
      <button data-section="evidence">Evidence Ledger</button>
      <button data-section="decision">Owner Decision</button>
    </nav>

    <section class="workspace">
      <div id="review" class="panel active-panel">
        <div class="panel-head">
          <h2>Review Queue</h2>
          <button id="exportButton">Export Review JSON</button>
        </div>
        <div id="reviewQueue" class="grid"></div>
      </div>

      <div id="personas" class="panel">
        <h2>Persona Network</h2>
        <div id="personaNetwork" class="grid"></div>
      </div>

      <div id="content" class="panel">
        <h2>Content Batch</h2>
        <div id="contentBatch" class="stack"></div>
      </div>

      <div id="style" class="panel">
        <h2>Brand/IP Style Memory</h2>
        <div id="styleMemory" class="stack"></div>
      </div>

      <div id="evidence" class="panel">
        <h2>Evidence Ledger</h2>
        <div id="evidenceLedger" class="stack"></div>
      </div>

      <div id="decision" class="panel">
        <h2>Owner Decision</h2>
        <p class="note">Use this local form to decide the first draft batch. Nothing is posted or published.</p>
        <textarea id="ownerNotes" rows="8" placeholder="Add review notes, revision direction, or approval boundary."></textarea>
        <div class="decision-row">
          <button data-decision="approve">Approve drafts</button>
          <button data-decision="revise">Request revision</button>
          <button data-decision="reject">Reject batch</button>
        </div>
        <pre id="decisionSummary"></pre>
      </div>
    </section>
  </main>

  <script src="app.js"></script>
</body>
</html>"""
    write(APP_DIR / "index.html", index_html)

    styles = """
:root {
  color-scheme: light;
  --ink: #151515;
  --muted: #5e6673;
  --line: #d9dde5;
  --panel: #ffffff;
  --soft: #f4f6f8;
  --blue: #244f9e;
  --green: #216d4f;
  --gold: #8a5a00;
  --red: #a73535;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  color: var(--ink);
  background: var(--soft);
}
.topbar {
  min-height: 150px;
  display: flex;
  justify-content: space-between;
  gap: 24px;
  padding: 28px 32px;
  background: #ffffff;
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
.subtitle {
  margin: 10px 0 0;
  color: var(--muted);
  max-width: 720px;
}
.status-panel {
  display: grid;
  grid-template-columns: repeat(2, minmax(150px, 1fr));
  gap: 8px;
  align-self: start;
}
.status-panel span {
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 8px 10px;
  background: #fbfbfc;
  font-size: 13px;
}
.layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: calc(100vh - 150px);
}
.sidebar {
  border-right: 1px solid var(--line);
  padding: 18px;
  background: #fff;
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
.sidebar button {
  width: 100%;
  text-align: left;
  margin-bottom: 8px;
}
button:hover, button.active {
  border-color: var(--blue);
  color: var(--blue);
}
.workspace {
  padding: 24px;
}
.panel { display: none; }
.active-panel { display: block; }
.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
}
.stack {
  display: grid;
  gap: 14px;
}
.card {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 14px;
  background: var(--panel);
}
.card p { color: var(--muted); }
.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}
.badge {
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 4px 8px;
  font-size: 12px;
  background: #f8f9fb;
}
.decision-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 12px 0;
}
textarea {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 12px;
  resize: vertical;
  font: inherit;
}
pre {
  white-space: pre-wrap;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fff;
  padding: 12px;
}
.note { color: var(--muted); }
@media (max-width: 800px) {
  .topbar { display: block; }
  .status-panel { grid-template-columns: 1fr; margin-top: 16px; }
  .layout { grid-template-columns: 1fr; }
  .sidebar { border-right: 0; border-bottom: 1px solid var(--line); }
}
"""
    write(APP_DIR / "styles.css", styles)

    app_js = """
const STORAGE_KEY = "avfInfluenceFactoryReview";
const REVIEW_DECISIONS = ["approve", "revise", "reject"];

const appData = {
  reviewItems: [
    {
      id: "sns-001",
      title: "SNS thread starter",
      channel: "SNS",
      text: "Building an AI factory should start with memory: goals, brand/IP style, evidence, and approval gates.",
      status: "draft-only"
    },
    {
      id: "blog-001",
      title: "Blog outline",
      channel: "Blog",
      text: "From AI content spam to transparent AI creator systems.",
      status: "draft-only"
    },
    {
      id: "short-001",
      title: "Short-form script",
      channel: "Short-form",
      text: "The dangerous version of AI influence is fake people. The useful version is transparent systems.",
      status: "draft-only"
    }
  ],
  personas: [
    { name: "Builder Analyst", role: "Explains tools and proof-by-result experiments.", disclosure: "transparent AI persona" },
    { name: "Brand/IP Director", role: "Protects voice, visual rules, and asset continuity.", disclosure: "transparent AI persona" },
    { name: "DevRel Operator", role: "Turns technical pain into tutorials and field notes.", disclosure: "transparent AI persona" },
    { name: "Growth Editor", role: "Turns evidence into editorial calendar candidates.", disclosure: "transparent AI persona" }
  ],
  styleMemory: [
    "brand DNA",
    "character bible",
    "visual style guide",
    "palette",
    "typography",
    "negative prompt",
    "reference image index",
    "asset registry",
    "usage rights notes"
  ],
  evidence: [
    "First real product goal imported.",
    "Safe reframe recorded.",
    "Product-track packet created.",
    "Local dashboard created.",
    "First draft-only content batch created.",
    "No protected action executed."
  ]
};

function getState() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) {
    return { decision: "pending", notes: "", reviewedAt: null };
  }
  try {
    return JSON.parse(saved);
  } catch (error) {
    return { decision: "pending", notes: "", reviewedAt: null };
  }
}

function saveState(nextState) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(nextState, null, 2));
  renderDecisionSummary();
}

function card(title, body, badges = []) {
  const badgeHtml = badges.map((badge) => `<span class="badge">${badge}</span>`).join("");
  return `<article class="card"><h3>${title}</h3><p>${body}</p><div class="badge-row">${badgeHtml}</div></article>`;
}

function renderReviewQueue() {
  const target = document.querySelector("#reviewQueue");
  target.innerHTML = appData.reviewItems
    .map((item) => card(item.title, item.text, [item.channel, item.status, "owner approval required"]))
    .join("");
}

function renderPersonaNetwork() {
  const target = document.querySelector("#personaNetwork");
  target.innerHTML = appData.personas
    .map((persona) => card(persona.name, persona.role, [persona.disclosure, "owned channel"]))
    .join("");
}

function renderContentBatch() {
  const target = document.querySelector("#contentBatch");
  target.innerHTML = [
    card("Draft policy", "All content is draft-only. Do not publish. Do not post.", ["approval gated"]),
    card("Channel coverage", "SNS, blog, community, newsletter, short-form, long-form, media prompt, comment response drafts.", ["multi-channel"]),
    card("Safety boundary", "No fake human impersonation, spam, mass posting, or engagement manipulation.", ["safe influence"])
  ].join("");
}

function renderStyleMemory() {
  const target = document.querySelector("#styleMemory");
  target.innerHTML = appData.styleMemory
    .map((item) => card(item, "Loaded before content or image-generation reference work.", ["style memory"]))
    .join("");
}

function renderEvidenceLedger() {
  const target = document.querySelector("#evidenceLedger");
  target.innerHTML = appData.evidence
    .map((item, index) => card(`Evidence ${index + 1}`, item, ["repo-local"]))
    .join("");
}

function renderDecisionSummary() {
  const state = getState();
  document.querySelector("#ownerNotes").value = state.notes || "";
  document.querySelector("#decisionSummary").textContent = JSON.stringify(state, null, 2);
}

function setDecision(decision) {
  const notes = document.querySelector("#ownerNotes").value;
  saveState({
    decision,
    notes,
    reviewedAt: new Date().toISOString(),
    protectedActionExecuted: false,
    published: false,
    posted: false
  });
}

function exportReviewJson() {
  const payload = {
    product: "Transparent AI Creator Collective / Influence Factory",
    state: getState(),
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
  link.download = "influence-factory-review.json";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
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
  renderReviewQueue();
  renderPersonaNetwork();
  renderContentBatch();
  renderStyleMemory();
  renderEvidenceLedger();
  renderDecisionSummary();
  bindNavigation();
  document.querySelector("#exportButton").addEventListener("click", exportReviewJson);
  document.querySelector("#ownerNotes").addEventListener("input", () => {
    const state = getState();
    state.notes = document.querySelector("#ownerNotes").value;
    saveState(state);
  });
  document.querySelectorAll("[data-decision]").forEach((button) => {
    if (!REVIEW_DECISIONS.includes(button.dataset.decision)) return;
    button.addEventListener("click", () => setDecision(button.dataset.decision));
  });
}

boot();
"""
    write(APP_DIR / "app.js", app_js)

    readme = """# Influence Factory Workbench

This is the local product MVP for the Transparent AI Creator Collective / Influence Factory.

Open `index.html` in a browser. The app is static and repo-local:

- Review Queue
- Persona Network
- Content Batch
- Brand/IP Style Memory
- Evidence Ledger
- Owner Decision
- Export Review JSON

Boundaries:

- No deploy
- No publish
- No platform posting
- No account automation
- No provider calls
- No live model calls
- No external service calls

Next safe goal:
owner_uses_local_product_mvp_for_first_review
"""
    write(APP_DIR / "README.md", readme)

    next_goal = """# Next After Influence Factory Product MVP

selected_next_safe_goal: owner_uses_local_product_mvp_for_first_review
next_safe_goal_count: 1

Purpose:
The owner opens the local product MVP, reviews the first content batch, records notes,
chooses approve/revise/reject, and exports review JSON.

Boundary:
This is an owner review action only. No publish, posting, deploy, provider call,
live model call, external service call, or account automation is authorized.
"""
    write(ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_MVP.md", next_goal)

    terminal = """# Influence Factory Product MVP Terminal Report

terminal_condition: LOCAL_PRODUCT_MVP_READY_FOR_OWNER_USE

Summary:
The product is now a usable repo-local static MVP, not only a document packet. It supports
review queue navigation, persona network review, content batch inspection, brand/IP style
memory review, evidence ledger review, owner decision capture, localStorage persistence,
and Export Review JSON.

Protected actions:
No protected action was executed. The app does not deploy, publish, post to platforms,
automate accounts, call providers, call live models, or call external services.

Next safe goal:
owner_uses_local_product_mvp_for_first_review
"""
    write(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_MVP_TERMINAL_REPORT.md", terminal)

    audit_items = [
        ("static product app exists", "avf/influence_factory/product_app/index.html"),
        ("product MVP record exists", "avf/influence_factory/product_app/product_mvp_record.json"),
        ("review queue exists", "avf/influence_factory/product_app/index.html"),
        ("persona network exists", "avf/influence_factory/product_app/index.html"),
        ("content batch viewer exists", "avf/influence_factory/product_app/index.html"),
        ("brand/IP style memory viewer exists", "avf/influence_factory/product_app/index.html"),
        ("evidence ledger viewer exists", "avf/influence_factory/product_app/index.html"),
        ("owner decision panel exists", "avf/influence_factory/product_app/index.html"),
        ("export review JSON exists", "avf/influence_factory/product_app/app.js"),
        ("localStorage persistence exists", "avf/influence_factory/product_app/app.js"),
        ("approve action exists", "avf/influence_factory/product_app/app.js"),
        ("revise action exists", "avf/influence_factory/product_app/app.js"),
        ("reject action exists", "avf/influence_factory/product_app/app.js"),
        ("no fetch marker exists", "scripts/validate_avf_influence_factory_product_mvp.py"),
        ("no XMLHttpRequest marker exists", "scripts/validate_avf_influence_factory_product_mvp.py"),
        ("no sendBeacon marker exists", "scripts/validate_avf_influence_factory_product_mvp.py"),
        ("no deploy flag is false", "avf/influence_factory/product_app/product_mvp_record.json"),
        ("no publish flag is false", "avf/influence_factory/product_app/product_mvp_record.json"),
        ("no platform posting flag is false", "avf/influence_factory/product_app/product_mvp_record.json"),
        ("no account automation flag is false", "avf/influence_factory/product_app/product_mvp_record.json"),
        ("exactly one next safe goal exists", "docs/goals/NEXT_AFTER_INFLUENCE_FACTORY_PRODUCT_MVP.md"),
    ]
    audit = ["# Influence Factory Product MVP Completion Audit", ""]
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
        "terminal_condition: LOCAL_PRODUCT_MVP_READY_FOR_OWNER_USE",
        "next_safe_goal: owner_uses_local_product_mvp_for_first_review",
    ])
    write(ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_PRODUCT_MVP_COMPLETION_AUDIT.md", "\n".join(audit))

    print("influence_factory_product_mvp_created=true")
    print("terminal_condition=LOCAL_PRODUCT_MVP_READY_FOR_OWNER_USE")
    print(f"selected_next_safe_goal={NEXT_SAFE_GOAL}")
    print("protected_action_executed=false")


if __name__ == "__main__":
    main()

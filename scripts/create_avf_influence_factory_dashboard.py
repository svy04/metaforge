from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACK_DIR = ROOT / "avf" / "influence_factory" / "active" / "transparent-ai-creator-collective-001"
DASHBOARD_DIR = ROOT / "avf" / "influence_factory" / "dashboard"
NEXT_SAFE_GOAL = "create_first_influence_factory_content_batch_packet"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def section(title: str, filename: str) -> str:
    body = html.escape(read(TRACK_DIR / filename))
    return f"<section><h2>{html.escape(title)}</h2><pre>{body}</pre></section>"


def main() -> None:
    record = {
        "terminal_condition": "LOCAL_INFLUENCE_FACTORY_DASHBOARD_READY",
        "dashboard_status": "repo_local_static_html_created",
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
    }
    write(DASHBOARD_DIR / "dashboard_record.json", json.dumps(record, indent=2, sort_keys=True))

    sections = "\n".join(
        [
            section("Product Strategy", "product_strategy.md"),
            section("Product Requirements", "product_requirements.md"),
            section("Safe Influence Policy", "safe_influence_policy.md"),
            section("Persona Network", "persona_network_blueprint.md"),
            section("Content Channel Matrix", "content_channel_matrix.md"),
            section("Brand/IP Style Memory", "brand_ip_style_memory_starter.md"),
            section("Codex Task Queue", "codex_task_queue.md"),
        ]
    )
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Transparent AI Creator Collective Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; line-height: 1.45; color: #111; }}
    header {{ border-bottom: 2px solid #111; margin-bottom: 24px; }}
    section {{ border: 1px solid #ddd; padding: 16px; margin: 16px 0; }}
    pre {{ white-space: pre-wrap; background: #f7f7f7; padding: 12px; overflow: auto; }}
    .boundary {{ font-weight: 700; }}
  </style>
</head>
<body>
  <header>
    <h1>Transparent AI Creator Collective / Influence Factory</h1>
    <p>Local repo-only dashboard/spec viewer. No deploy. No publish. No platform posting. No account automation.</p>
  </header>
  {sections}
</body>
</html>"""
    write(DASHBOARD_DIR / "index.html", html_doc)

    write(
        DASHBOARD_DIR / "README.md",
        """# Influence Factory Dashboard

This static dashboard renders the repo-local product-track packet for review.

Boundary:
- No deploy
- No publish
- No provider calls
- No live model calls
- No external services
- No platform posting
- No account automation

Next safe goal:
create_first_influence_factory_content_batch_packet
""",
    )

    write(
        ROOT / "docs" / "goals" / "NEXT_AFTER_INFLUENCE_FACTORY_DASHBOARD.md",
        f"""# Next After Influence Factory Dashboard

selected_next_safe_goal: {NEXT_SAFE_GOAL}
next_safe_goal_count: 1

Purpose:
Create the first draft-only Influence Factory content batch packet.

Boundary:
The next goal may create repo-local draft content packets and review checklists.
It may not publish, post, deploy, call providers, call live models, call external services,
or automate accounts.
""",
    )

    write(
        ROOT / "docs" / "goals" / "INFLUENCE_FACTORY_DASHBOARD_VALIDATION_REPORT.md",
        """# Influence Factory Dashboard Validation Report

Expected command:
python scripts\\validate_avf_influence_factory_dashboard.py

Expected result:
RESULT: PASS

Claim boundary:
Internal repo-local static dashboard/spec viewer only.
""",
    )

    print("influence_factory_dashboard_created=true")
    print("terminal_condition=LOCAL_INFLUENCE_FACTORY_DASHBOARD_READY")
    print(f"selected_next_safe_goal={NEXT_SAFE_GOAL}")
    print("protected_action_executed=false")


if __name__ == "__main__":
    main()

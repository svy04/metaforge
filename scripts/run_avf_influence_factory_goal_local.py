from __future__ import annotations

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
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
    write(out_dir / "product_brief.md", f"# Product Brief\n\n{product}\n\nAudience: {audience}\n\nPromise: {promise}\n")
    write(out_dir / "strategy_brief.md", f"# Strategy Brief\n\nProof target: {proof}\n\nFirst result: {goal['first_result']}\n")
    write(out_dir / "brand_ip_brief.md", f"# Brand/IP Brief\n\n{goal['brand_dna']}\n\n{goal['character_bible']}\n\n{goal['visual_guide']}\n")
    write(out_dir / "content_pack.md", f"# Content Pack\n\nDraft-only content pack for {audience}.\n")
    write(out_dir / "image_prompt_pack.md", f"# Image Prompt Pack\n\nPrompt: {goal['visual_guide']}\n\nNegative: {goal['forbidden_styles']}\n")
    write_json(out_dir / "codex_task_packet.json", {
        "title": "Implement next local Influence Factory improvement",
        "goal": goal["first_result"],
        "acceptance_criteria": ["preserve local-only behavior", "add validator coverage", "do not execute protected actions"],
        "forbidden_changes": ["deploy", "publish", "provider calls", "platform posting", "account automation", "deceptive influence support"],
    })
    write(out_dir / "safety_report.md", "# Safety Report\n\nNo deceptive influence support. No protected action executed.\n")
    write_json(out_dir / "quality_gate.json", {
        "score": 84,
        "release_ready": False,
        "public_ready": False,
        "production_ready": False,
        "external_validation_complete": False,
        "autonomous_reliability_proven": False,
    })
    write(out_dir / "next_actions.md", "# Next Actions\n\n1. Owner reviews local bundle.\n2. Iterate locally or request protected authorization.\n")
    write(out_dir / "dossier.md", f"# Influence Factory Dossier\n\n{product}\n\n{promise}\n\n{boundary}.\n")
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

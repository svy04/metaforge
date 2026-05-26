from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(goal_path: Path, out_dir: Path) -> int:
    goal = read_json(goal_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        out_dir / "operator_cycle_manifest.json",
        {
            "goal_id": goal["goal_id"],
            "cycle_status": "local_operator_cycle_ready",
            "protected_action_executed": False,
            "external_calls": False,
            "generated_files": [
                "cycle_dossier.md",
                "style_check.md",
                "approval_check.md",
                "next_safe_goal.md",
            ],
        },
    )
    write(
        out_dir / "cycle_dossier.md",
        "# Operator Cycle Dossier\n\n"
        f"idea: {goal['idea']}\n\n"
        f"audience: {goal['audience']}\n\n"
        f"promise: {goal['promise']}\n\n"
        "protected_action_executed: false\n"
        "external_calls: false\n",
    )
    write(
        out_dir / "style_check.md",
        "# Style Check\n\n"
        f"brand_dna: {goal['brand_dna']}\n\n"
        f"character_bible: {goal['character_bible']}\n\n"
        f"visual_guide: {goal['visual_guide']}\n\n"
        f"forbidden_styles: {goal['forbidden_styles']}\n",
    )
    write(
        out_dir / "approval_check.md",
        "# Approval Check\n\n"
        "public_posting: false\n"
        "deploy: false\n"
        "publish: false\n"
        "provider_calls: false\n"
        "platform_automation: false\n",
    )
    write(
        out_dir / "next_safe_goal.md",
        "# Next Safe Goal\n\n"
        "selected_next_safe_goal: owner_runs_v14_operator_package_with_real_goal_or_requests_protected_authorization\n"
        "selected_next_goal_executed: false\n",
    )
    print("OPERATOR_CYCLE_LOCAL=PASS")
    print(f"output_dir={out_dir}")
    print("protected_action_executed=false")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goal", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    return run(Path(args.goal), Path(args.out))


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "avf"
GOALS = ROOT / "docs" / "goals"
EVIDENCE = ROOT / "avf" / "evidence"
RUNTIME = ROOT / "avf" / "runtime"

FOUNDATION_REPORT = GOALS / "INFLUENCE_FACTORY_COMPLETION_CANDIDATE_V42_VALIDATION_REPORT.md"
VALIDATION_REPORT = GOALS / "AVF_CRITICAL_ARCHITECTURE_EXPANSION_MAP_VALIDATION_REPORT.md"

REQUIRED_FILES = [
    DOCS / "CRITICAL_ARCHITECTURE_REVIEW.md",
    DOCS / "OPEN_SOURCE_EXPANSION_MAP.md",
    DOCS / "AVF_PLATFORM_ROADMAP.md",
    DOCS / "BUILD_VS_BUY_DECISION_RECORD.md",
    EVIDENCE / "evidence_ledger.v2.schema.yml",
    RUNTIME / "runtime_plane.interface.yml",
    VALIDATION_REPORT,
]

CRITICAL_REVIEW_MARKERS = [
    "repo-local control-plane foundation",
    "not a production runtime",
    "Runtime gap",
    "Schema gap",
    "Evidence gap",
    "Validation gap",
    "Governance gap",
    "Product/UI gap",
    "Studio/Product Plane",
]

OSS_MARKERS = [
    "LangGraph",
    "Temporal",
    "Argo Workflows",
    "Kestra",
    "Prefect",
    "Airflow",
    "Dagster",
    "LiteLLM",
    "Ollama",
    "vLLM",
    "Haystack",
    "Langfuse",
    "Phoenix",
    "promptfoo",
    "Ragas",
    "MCP",
    "OpenTelemetry",
    "OpenHands",
    "SWE-agent",
]

ROADMAP_MARKERS = [
    "Phase 0",
    "Phase 1",
    "Phase 2",
    "Phase 3",
    "Phase 4",
    "Phase 5",
    "Phase 6",
    "Phase 7",
    "Control Plane",
    "Runtime Plane",
    "Data Plane",
    "Model/Tool Plane",
    "Observability/Eval Plane",
    "Studio/Product Plane",
]

EVIDENCE_V2_FIELDS = [
    "id",
    "run_id",
    "goal_id",
    "artifact_id",
    "artifact_uri",
    "artifact_hash",
    "actor",
    "source",
    "claim",
    "claim_boundary",
    "validation_method",
    "validation_result",
    "confidence",
    "approval_state",
    "created_at",
    "next_action",
]

RUNTIME_FIELDS = [
    "run_id",
    "goal_id",
    "state",
    "nodes",
    "transitions",
    "retry_policy",
    "timeout_policy",
    "human_gate_required",
    "evidence_events",
    "forbidden_actions",
]

BLOCKED_MARKERS = [
    "deploy: blocked",
    "publish: blocked",
    "provider calls: blocked",
    "live model calls: blocked",
    "external service calls: blocked",
    "production readiness claim: blocked",
    "release readiness claim: blocked",
    "public readiness claim: blocked",
    "external validation claim: blocked",
    "protected_action_executed: false",
    "provider_calls_performed: false",
    "deploy_performed: false",
    "publish_performed: false",
]

ALLOWED_CHANGED_PREFIXES = (
    "docs/avf/",
    "docs/goals/AVF_CRITICAL_ARCHITECTURE_EXPANSION_MAP_VALIDATION_REPORT.md",
    "avf/evidence/evidence_ledger.v2.schema.yml",
    "avf/runtime/runtime_plane.interface.yml",
    "scripts/validate_avf_architecture_expansion_map.py",
)

FORBIDDEN_CHANGED_PATHS = {
    "package.json",
    "package-lock.json",
    "bun.lockb",
    "yarn.lock",
    "pnpm-lock.yaml",
}


def fail(message: str) -> None:
    print("AVF architecture expansion map validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_markers(text: str, markers: list[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{label} missing markers:\n" + "\n".join(missing))


def changed_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        fail("git diff failed:\n" + result.stderr)
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    if "RESULT: PASS" not in read(FOUNDATION_REPORT):
        fail("accepted v42 foundation report is not PASS")

    review = read(DOCS / "CRITICAL_ARCHITECTURE_REVIEW.md")
    oss_map = read(DOCS / "OPEN_SOURCE_EXPANSION_MAP.md")
    roadmap = read(DOCS / "AVF_PLATFORM_ROADMAP.md")
    build_vs_buy = read(DOCS / "BUILD_VS_BUY_DECISION_RECORD.md")
    evidence_v2 = read(EVIDENCE / "evidence_ledger.v2.schema.yml")
    runtime = read(RUNTIME / "runtime_plane.interface.yml")
    validation_report = read(VALIDATION_REPORT)

    require_markers(review, CRITICAL_REVIEW_MARKERS, "critical architecture review")
    require_markers(oss_map, OSS_MARKERS, "open-source expansion map")
    require_markers(roadmap, ROADMAP_MARKERS, "platform roadmap")
    require_markers(build_vs_buy, ["build in AVF", "reuse upstream", "do not implement from scratch"], "build-vs-buy decision record")
    require_markers(evidence_v2, EVIDENCE_V2_FIELDS, "evidence ledger v2 schema")
    require_markers(runtime, RUNTIME_FIELDS, "runtime plane interface")

    combined = "\n".join([review, oss_map, roadmap, build_vs_buy, evidence_v2, runtime, validation_report])
    require_markers(combined, BLOCKED_MARKERS, "protected-action boundary")
    require_markers(
        combined,
        [
            "OpenClaude-independent",
            "runtime dependencies installed: false",
            "external runtime automation implemented: false",
            "release_ready: false",
            "production_ready: false",
        ],
        "claim boundary",
    )

    if "RESULT: PASS" not in validation_report:
        fail("validation report does not state RESULT: PASS")

    disallowed_changes = [
        path
        for path in changed_files()
        if path in FORBIDDEN_CHANGED_PATHS or not path.startswith(ALLOWED_CHANGED_PREFIXES)
    ]
    if disallowed_changes:
        fail("Unexpected changed paths:\n" + "\n".join(disallowed_changes))

    print("AVF architecture expansion map validation")
    print("RESULT: PASS")
    print("critical_architecture_review_created=true")
    print("open_source_expansion_map_created=true")
    print("evidence_ledger_v2_schema_created=true")
    print("runtime_plane_interface_created=true")
    print("platform_roadmap_created=true")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("runtime_dependencies_installed=false")
    print("external_runtime_automation_implemented=false")
    print("release_ready=false")
    print("production_ready=false")


if __name__ == "__main__":
    main()

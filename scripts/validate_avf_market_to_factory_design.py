from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "avf"
GOALS = ROOT / "docs" / "goals"

KERNEL_REPORT = GOALS / "AVF_KERNEL_V0_1_DRY_RUN_VALIDATION_REPORT.md"
VALIDATION_REPORT = GOALS / "AVF_MARKET_TO_FACTORY_DESIGN_VALIDATION_REPORT.md"

REQUIRED_FILES = [
    DOCS / "AVF_MARKET_TO_FACTORY_VISION.md",
    DOCS / "VENTURE_OPERATION_PACKET_SPEC.md",
    DOCS / "MARKET_INTELLIGENCE_ENGINE_SPEC.md",
    DOCS / "STRATEGY_HYPOTHESIS_ENGINE.md",
    DOCS / "FACTORY_FORMATION_ENGINE.md",
    DOCS / "CELL_OPERATING_MODEL_V2.md",
    DOCS / "TRANSPARENT_INFLUENCE_ENGINE.md",
    DOCS / "CAPABILITY_ACQUISITION_LOOP.md",
    DOCS / "OSS_ASSIMILATION_PIPELINE.md",
    DOCS / "STRATEGY_ADAPTATION_LOOP.md",
    DOCS / "AUTONOMOUS_FACTORY_CREATION_LEVELS.md",
    VALIDATION_REPORT,
]

VISION_MARKERS = [
    "Market-to-Factory Loop",
    "Autonomous Venture Infrastructure",
    "Market Sensing",
    "Strategic Hypothesis",
    "Factory Formation",
    "Production",
    "Distribution",
    "Evidence Collection",
    "Adaptation",
]

VOP_MARKERS = [
    "venture_operation_packet",
    "market_intelligence_packet",
    "strategy_hypothesis_packet",
    "factory_formation_packet",
    "production_plan_packet",
    "influence_distribution_packet",
    "capability_acquisition_packet",
    "codex_execution_packet",
    "safety_governance_packet",
    "evidence_learning_packet",
]

ENGINE_MARKERS = [
    "Market Intelligence Engine",
    "Strategy & Hypothesis Engine",
    "Factory Formation Engine",
    "Transparent Influence Engine",
    "Capability Acquisition Loop",
    "OSS Assimilation Pipeline",
    "Strategy Adaptation Loop",
    "Creation Level 0",
    "Creation Level 5",
]

BOUNDARY_MARKERS = [
    "repo_local_internal_only",
    "runtime implementation: blocked",
    "provider calls: blocked",
    "live model calls: blocked",
    "external service calls: blocked",
    "scraping implementation: blocked",
    "posting automation: blocked",
    "deploy: blocked",
    "publish: blocked",
    "production readiness claim: blocked",
    "release readiness claim: blocked",
    "public readiness claim: blocked",
    "fake human impersonation: blocked",
    "engagement manipulation: blocked",
    "protected_action_executed=false",
]

SOURCE_MARKERS = [
    "web4.ai",
    "Model Context Protocol",
    "LangGraph",
    "Temporal",
    "LiteLLM",
    "WebArena",
]


def fail(message: str) -> None:
    print("AVF Market-to-Factory design validation")
    print("RESULT: FAIL")
    print(message)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_markers(text: str, markers: list[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{label} missing markers:\n" + "\n".join(missing))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("Missing required files:\n" + "\n".join(missing))

    if "RESULT: PASS" not in read(KERNEL_REPORT):
        fail("Kernel v0.1 validation report is not PASS")

    vision = read(DOCS / "AVF_MARKET_TO_FACTORY_VISION.md")
    vop = read(DOCS / "VENTURE_OPERATION_PACKET_SPEC.md")
    combined = "\n".join(read(path) for path in REQUIRED_FILES)

    require_markers(vision, VISION_MARKERS, "market-to-factory vision")
    require_markers(vop, VOP_MARKERS, "venture operation packet spec")
    require_markers(combined, ENGINE_MARKERS, "engine design docs")
    require_markers(combined, BOUNDARY_MARKERS, "safety boundary")
    require_markers(combined, SOURCE_MARKERS, "primary-source notes")

    if "RESULT: PASS" not in read(VALIDATION_REPORT):
        fail("validation report does not state RESULT: PASS")

    print("AVF Market-to-Factory design validation")
    print("RESULT: PASS")
    print("market_to_factory_vision_created=true")
    print("venture_operation_packet_spec_created=true")
    print("engine_design_docs_created=true")
    print("creation_levels_created=true")
    print("protected_action_executed=false")
    print("provider_calls_performed=false")
    print("runtime_implementation_performed=false")
    print("posting_automation_performed=false")
    print("deploy_performed=false")
    print("publish_performed=false")
    print("release_ready=false")
    print("production_ready=false")
    print("next_safe_goal_id=avf_kernel_v0_2_venture_operation_packet_compiler")


if __name__ == "__main__":
    main()

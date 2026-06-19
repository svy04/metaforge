![Metaforge banner](docs/assets/metaforge-banner.gif)

# Metaforge

[English](README.md) | [한국어](README.ko.md)

Metaforge는 Meta/MFH/Orchestra 기반의 governed-code 운영체제입니다.

OpenClaude는 현재 Metaforge가 올라타는 로컬 CLI 런타임입니다. 터미널 UX,
도구 호출, MCP, slash command, provider profile, streaming output, Claude/Codex
route를 제공합니다. 하지만 공개적으로 중심에 둘 가치는 OpenClaude 자체가
아니라 **Meta + MFH + Orchestra**입니다.

Orchestra는 현재 이 package에서 runtime-wired layer입니다. Meta와 MFH는
governance, schema, evidence-gate surface입니다. 이 영역들을 모두 별도 runtime
module로 말하지 않습니다.

출처와 라이선스 경계: 이 repository에는 Anthropic Claude Code CLI에서 파생된
runtime code가 포함되어 있습니다. OpenClaude 기여자의 수정분은 법적으로 가능한 범위에서 MIT
라이선스로 제공되지만, 전체 파생 런타임에 대한 단순 MIT 라이선스가 아닙니다.
재사용이나 재배포 전에는 반드시 [LICENSE](LICENSE)를 확인하세요.

공개 히스토리 경계: Metaforge는 이 checkout 밖의 공개 전 작업 이력에서 현재 공개
repository로 옮겨온 surface라서 public commit/star 숫자가 낮은 것은 예상 가능한 맥락입니다.
이 이력은 채택, 외부 검증, production readiness 증거가 아닙니다. 공개 주장은
source-controlled test, report, claim-boundary record에서만 나와야 합니다.

## 한 줄 요약

Metaforge는 사용자의 의도를 장기 목표로 고정하고, Meta에 운영 기억을 남기며,
Orchestra로 작업을 분배하고, MFH evidence gate를 통과한 것만 완료 주장으로
승격하는 로컬 우선 agent OS입니다.

## 현재 증명 가능한 것

| 질문 | 현재 답 |
| --- | --- |
| 무엇인가요? | OpenClaude CLI runtime 위에서 동작하는 Meta/MFH/Orchestra OS입니다. |
| 바로 확인할 명령 | `bun run goals:validate`, `bun run product:public-artifact-hygiene`, `bun run verify:privacy` |
| 가장 강한 공개 증거 | [goal trace validation report](docs/product-quality/goal-trace-validation-report.md), [origin/license provenance boundary](docs/product-quality/origin-license-provenance-boundary-report.md), [public proof pack](docs/marketing/metaforge-public-proof-pack-2026-06-18.md), [GitHub profile refresh evidence](docs/profile/github-profile-refresh-evidence-2026-06-19.md), [research validation report](docs/product-quality/research-brief-validation-report.md), [eval flywheel validation report](docs/product-quality/eval-flywheel-validation-report.md), [public claim evidence map](docs/product-quality/public-claim-boundary-report.md#public-claim-evidence-map) |
| 증거 분류 | `docs/product-quality/product-evidence-manifest.md`의 evidence manifest는 behavioral runtime evidence와 static analysis, governance-boundary, source-control, structural-inventory evidence를 분리합니다. |
| 증명하지 않는 것 | production readiness, hosted deployment, external validation, benchmark superiority, autonomous reliability |

## 공개 피드백 응답

최근 한국 커뮤니티 피드백은 칭찬이나 외부 검증이 아니라 제품 입력으로 추적합니다.
[2026-06-19 snapshot](docs/product-quality/public-feedback-snapshot-2026-06-19.md)과
[triage](docs/product-quality/public-feedback-triage-2026-06-19.md)에 보존되어 있습니다.

그 피드백 때문에 공개 기준을 이렇게 고정합니다.

- 출처, fork/adaptation, 낮은 public commit/star 맥락을 먼저 분명히 말한다.
- AGENTS와 README는 public-safe하고 짧아야 하며 local machine context를 노출하지 않는다.
- OpenClaude는 runtime substrate이고, 공개 thesis는 Metaforge = Meta + MFH + Orchestra OS다.
- marker-only audit는 behavioral happy path, edge case, side-effect guard로 계속 옮겨가야 한다.
- Knip, dependency-cruiser, jscpd는 현재 local no-provider product-quality gate로 연결되어 dead-export 후보, dependency topology baseline/ratchet, product-script clone baseline을 기록한다. Fallow와 Lumin Repo Lens는 여전히 선택적/manual backlog input이며, 이 gate들은 cleanup 완료나 topology clean을 증명하지 않는다.
- 정적 분석 증거: [Knip dead-export 후보](docs/product-quality/dead-export-candidates-report.md), [dependency-cruiser topology ratchet](docs/product-quality/dependency-topology-report.md), [jscpd product-script clone ratchet](docs/product-quality/script-duplication-audit-report.md), [CG-002 static-analysis goal](docs/goals/CG-002-static-analysis-ratchet.md), [evidence manifest](docs/product-quality/product-evidence-manifest.md). 이것은 candidate/baseline/ratchet 증거이며 cleanup 완료, topology clean, refactor 완료, public readiness, external validation을 증명하지 않습니다.
- 첫 피드백 루프가 한국어였으므로 한국어 문서도 최신으로 유지한다.

## Metaforge Proof Tour

공개 설명이 진짜인지 확인할 때는 이 순서로 보면 됩니다.

1. **Goal Kernel**: `docs/goals/CG-001-goal-kernel-mvp.md`와 `docs/goals/CG-002-static-analysis-ratchet.md`가 owner intent를 scope, non-goals, success criteria, validation commands, evidence artifacts, rollback rules, MFH/Meta field가 있는 machine-checkable goal로 만듭니다.
2. **Meta**: goal은 local authority source, decision ledger, raw source, memory/wiki update boundary를 연결해서 운영 상태를 채팅 기억이 아니라 증거로 남깁니다.
3. **MFH**: `scripts/validate-goals.ts`는 required validation command의 passing evidence가 없으면 `validated`나 `closed` 상태를 막고, `scripts/validate-goal-traces.ts`는 validated, rejected, blocked outcome을 담은 representative cross-goal trace pack의 순서와 side-effect boundary를 검사합니다.
4. **Orchestra**: `src/services/orchestra/`는 planner, skeptic, reviewer, arbiter, promotion role이 runtime-wired 된 layer입니다. 단, 이 주장은 local test와 product-quality report 범위로만 말합니다.
5. **Mimesis Engineering**: trace gate는 OpenTelemetry식 trace, OPA식 policy decision, OpenAI agent eval trace grading, NIST AI RMF risk-management record 구조를 흡수한 작은 증거층입니다.
6. **OpenClaude runtime**: OpenClaude는 terminal tool, provider route, MCP, slash command, credential surface를 제공합니다. 제품 중심은 OpenClaude가 아니라 Meta/MFH/Orchestra입니다.

증명하지 않는 것: 이 Proof Tour는 local no-provider evidence이며 production readiness, hosted deployment, external validation, benchmark superiority, autonomous reliability claim을 만들지 않습니다.

## 운영 레이어

AVF Influence Factory는 repo-local manual artifact lane입니다.

| 레이어 | 역할 |
| --- | --- |
| Meta | 운영 기억, 결정, source ledger, 승인 경계 |
| Goal Kernel | 목표 계층, 성공 기준, non-goals, 검증 명령, rollback rule |
| Orchestra | Claude/Codex route, planning, critique, review, evidence arbitration |
| MFH | drift, state, evidence, closure, release claim을 막는 governed-code gate |
| OpenClaude runtime | tools, MCP, slash command, provider profile, streaming, credential route. Generated profile은 non-sensitive 설정만 저장하고 API key와 obsolete or blocked model-lock metadata는 저장하지 않습니다. |

### 배선 증거 맵

생성된 [public claim evidence map](docs/product-quality/public-claim-boundary-report.md#public-claim-evidence-map)이 이 표의 근거 원본입니다. 각 symbol을 allowed claim, explicit non-claim, local evidence path, unresolved gap에 묶어 둡니다.

| 심볼 | 공개 역할 | 증거 등급 | 런타임 경계 |
| --- | --- | --- | --- |
| Orchestra | Claude/Codex route 위에서 planner, skeptic, implementer, reviewer, evidence arbiter, promotion 역할을 분배합니다. | runtime-wired import path; unit/product-quality evidence | Runtime code는 `src/services/orchestra/`에 있고 CLI query surface에서 호출됩니다. |
| Meta/MFH | 운영 기억, goal contract, evidence gate, closure rule을 정직하게 유지합니다. | governance/docs/gates | `docs/`, schema, report, product-quality gate로 표현됩니다. 이 checkout의 별도 runtime module이 아닙니다. |
| Mimesis Engineering | OSS, 논문, 특허, 표준, 제품 패턴에서 load-bearing structure를 흡수하는 source-first loop입니다. | source-ledger loop이며 기본 runtime module이 아닙니다 | 공개 증거는 docs/source ledger와 local verification입니다. 공개되지 않은 pre-public artifact는 public proof 밖에 둡니다. |
| AVF Influence Factory | venture/factory packet을 만드는 operator artifact flow입니다. | manual artifact lane이며 기본 CLI runtime import가 아닙니다 | `avf/`와 validator script에 있으며 generated operator output은 ignored local artifact로 남깁니다. |

## 빠른 시작

```bash
bun install
bun run build
node dist/cli.mjs
```

`npm install -g @gitlawb/openclaude` 명령은 external OpenClaude npm package를
설치하는 경로입니다. 즉 이 checkout에서 만든 배포물이 아니라는 의미에서
`not a Metaforge release artifact`입니다.

검증은:

```bash
bun run verify:privacy
```

## Claude / Codex route

Metaforge는 Claude와 Codex를 Orchestra 안의 실행 엔진으로 사용할 수 있습니다.
Claude route는 planner, skeptic, reviewer 역할에 쓸 수 있고, Codex route는
visible executor와 implementation role에 쓸 수 있습니다.

중요한 경계:

- Claude와 Codex는 engine입니다.
- 제품 중심은 Meta/MFH/Orchestra입니다.
- provider badge나 workflow badge는 외부 검증이 아니라 configured automation
  health와 local evidence link입니다.

## Mimesis Engineering

Mimesis Engineering은 이미 세상에 존재하는 강한 원본, 논문, 특허, 표준,
오픈소스 구현을 읽고 load-bearing structure를 추출한 뒤 로컬 시스템에
적용하고 검증하는 개선 엔진입니다.

이 방식은 “전문가인 척하는 프롬프트”가 아니라 “전문가의 산출물과 검증 구조를
가져와서 흡수하는 방식”입니다.

시작 문서:

- [docs/MIMESIS_ENGINEERING.md](docs/MIMESIS_ENGINEERING.md)
- [docs/research/mimesis-engineering-source-ledger-2026-06-14.md](docs/research/mimesis-engineering-source-ledger-2026-06-14.md)

## 검증

완료 주장은 파일 존재만으로 하지 않습니다. 관련 명령, test, loader check,
version probe, live inspection 중 하나 이상을 실제로 실행해야 합니다.

자주 쓰는 명령:

```bash
bun run build
bun run typecheck --pretty false
bun test
bun run verify:privacy
bun run product:quality
```

`product:quality`가 보호된 환경 경계에서 멈추면, 그것을 성공 주장으로 바꾸지
말고 생성된 report와 blocker를 그대로 읽어야 합니다.

## 공개 주장 경계

현재 이 repo가 말할 수 있는 것:

- Meta/MFH/Orchestra 구조의 공개 작업면이 있다.
- OpenClaude runtime 위에서 로컬 검증과 evidence gate를 구축하고 있다.
- public proof pack과 product-quality report가 claim boundary를 기록한다.

아직 말하지 않는 것:

- not production-ready
- not hosted deployment complete
- not externally validated
- not benchmark superior
- not autonomous reliability proven

## 라이선스와 출처

OpenClaude runtime에는 Anthropic Claude Code CLI에서 파생된 코드가 포함되어
있습니다. OpenClaude 기여자의 수정 및 추가분은 법적으로 허용되는 범위에서만
MIT License로 제공되며, 이는 파생 runtime 전체에 대한 blanket MIT license가
아닙니다. 이 repository는 Anthropic proprietary source 배포 승인을 받은 것이
아닙니다. 코드 재사용, 재배포, 설치 판단 전 [LICENSE](LICENSE)를 확인하세요.
"Claude"와 "Claude Code"는 Anthropic PBC의 상표입니다.

## 커뮤니티

- 버그와 기능 요청: [GitHub Issues](https://github.com/svy04/metaforge/issues)
- 보안 이슈: [SECURITY.md](SECURITY.md)
- 기여 가이드: [CONTRIBUTING.md](CONTRIBUTING.md)

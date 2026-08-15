# Metaforge

[English](README.md) | [한국어](README.ko.md)

[![PR Checks](https://github.com/svy04/metaforge/actions/workflows/pr-checks.yml/badge.svg?branch=main)](https://github.com/svy04/metaforge/actions/workflows/pr-checks.yml)

이 저장소에는 서로 연결된 세 가지가 들어 있습니다.

- **OpenClaude** — Anthropic의 Claude Code CLI에서 파생되어 여러 모델 프로바이더에서 돌도록 수정한 터미널 코딩 에이전트입니다. 실행되는 부분이 여기입니다: 터미널 UI, 에이전트 도구 루프(파일 편집·셸·서브에이전트, `src/tools/`), MCP 클라이언트(`src/services/mcp/`), 슬래시 명령, 스트리밍 출력. [PR 체크 워크플로](.github/workflows/pr-checks.yml)가 풀 리퀘스트마다 이 부분을 빌드하고 단위 테스트를 돌립니다.
- **Orchestra** — [`src/services/orchestra/`](src/services/orchestra)의 TypeScript 모듈입니다. 에이전트 작업을 역할로 나눕니다: 오케스트레이터, 스켑틱, 구현자, 교차 리뷰, 증거 중재자(evidence arbiter), 섀도 실행·리뷰, 휴먼 게이트, 승격. 모듈마다 단위 테스트가 붙어 있고 같은 CLI로 컴파일됩니다.
- **Meta와 MFH** — 이 체크아웃에서는 문서입니다. [`docs/`](docs) 아래의 목표 기록·스키마·결정 로그·생성 리포트, 그리고 스크립트 두 개가 있습니다. [`scripts/validate-goals.ts`](scripts/validate-goals.ts)는 필수 검증 명령의 통과 기록이 없는 목표 파일이 `validated`/`closed` 상태로 표기되어 있으면 거부합니다. [`scripts/validate-goal-traces.ts`](scripts/validate-goal-traces.ts)는 [`docs/goals/traces/`](docs/goals/traces)에 기록된 목표 트레이스의 필수 필드·이벤트 순서·기대 결과를 검사합니다.

## 출처와 라이선스

런타임 코드는 Anthropic의 Claude Code CLI에서 파생되었습니다. 원본 소스는 Anthropic PBC의 독점 소프트웨어입니다. OpenClaude 기여자의 수정분은 법적으로 허용되는 범위에서 MIT 라이선스로 제공되며, 파생 런타임 전체에 대한 포괄 MIT 라이선스가 아닙니다. 이 프로젝트는 Anthropic과 제휴·보증·후원 관계가 없고, Anthropic의 독점 소스를 배포할 권한도 없습니다. "Claude"와 "Claude Code"는 Anthropic PBC의 상표입니다. 이 저장소의 코드를 재사용하거나 재배포하기 전에 [LICENSE](LICENSE)를 읽으세요.

## 빌드와 실행

```bash
bun install
bun run build        # CLI를 dist/cli.mjs로 번들
node dist/cli.mjs
```

CLI 안에서 `/provider`로 프로바이더를 설정하고 `/onboard-github`로 GitHub Models를 연결합니다. 두 명령 모두 [`src/commands/`](src/commands)에 소스로 존재합니다.

npm 레지스트리에 `@gitlawb/openclaude`라는 패키지가 있지만, 게시된 버전은 이 체크아웃과 일치하지 않습니다. 이 저장소의 내용을 쓰려면 소스에서 빌드하세요.

설치 가이드: [Windows](docs/quick-start-windows.md) · [macOS/Linux](docs/quick-start-mac-linux.md) · [비개발자용](docs/non-technical-setup.md) · [고급 설정](docs/advanced-setup.md) · [Android](ANDROID_INSTALL.md) · [LiteLLM](docs/litellm-setup.md)

## 프로바이더

이 저장소에 실제로 존재하는 라우팅 코드:

| 프로바이더 | 소스 |
| --- | --- |
| Anthropic Claude (OAuth) | `src/services/api/claude.ts` |
| Codex (ChatGPT OAuth) | `src/services/api/codexOAuth.ts` |
| OpenAI 호환 `/v1` 엔드포인트 | `src/services/api/openaiShim.ts` |
| Gemini | `src/utils/geminiAuth.ts` |
| GitHub Models | `src/utils/githubModelsCredentials.ts` |
| Ollama (로컬) | `src/utils/model/ollamaModels.ts` |
| AWS Bedrock | `src/utils/model/bedrock.ts` |

Vertex·Foundry SDK는 [`package.json`](package.json)에 선언되어 있습니다. 동작은 프로바이더와 모델에 따라 다르며, 작은 로컬 모델은 긴 다단계 도구 호출에서 어려움을 겪을 수 있습니다.

## 테스트와 점검

아래 명령은 모두 [`package.json`](package.json)에 정의되어 있습니다:

```bash
bun test                 # 단위 테스트 (Bun 테스트 러너)
bun run test:coverage    # 커버리지 리포트를 coverage/에 생성
bun run typecheck        # tsc --noEmit
bun run smoke            # 빌드 + 버전 확인
bun run doctor:runtime   # 로컬 환경 점검
bun run verify:privacy   # 외부 전송 없음·시크릿 스캔·공개 저장소 점검
bun run goals:validate   # 목표 스키마·트레이스 검증
bun run product:quality  # docs/product-quality/ 리포트를 재생성하는 긴 체인
```

[`docs/product-quality/`](docs/product-quality)의 리포트는 이 로컬 스크립트들이 생성합니다. 로컬 머신에서 무엇을 점검했는지 기록한 문서이고, 외부 감사가 아닙니다.

## 헤드리스 gRPC 서버

`npm run dev:grpc`가 엔진을 gRPC 서비스로 띄웁니다. 기본 주소는 `localhost:50051`이고 `GRPC_PORT`/`GRPC_HOST`로 바꿉니다. `npm run dev:grpc:cli`는 그 서버에 붙는 터미널 클라이언트입니다. 정의는 [`src/proto/openclaude.proto`](src/proto/openclaude.proto)에 있습니다. 로컬 개발용 경로이며, 이 저장소에 호스팅된 배포는 없습니다.

## 저장소에 더 있는 것

- [`packages/openclaude-vscode/`](packages/openclaude-vscode) — OpenClaude 실행용 VS Code 확장 소스. 마켓플레이스 게시를 주장하지 않습니다.
- [`python/`](python) — 독립 Python 헬퍼(Ollama 프로바이더, Atomic Chat 프로바이더, 스마트 라우터)와 자체 테스트.
- [`docs/goals/`](docs/goals) — [CG-001](docs/goals/CG-001-goal-kernel-mvp.md), [CG-002](docs/goals/CG-002-static-analysis-ratchet.md) 같은 목표 파일. [docs/GOAL_SCHEMA.md](docs/GOAL_SCHEMA.md) 스키마를 따릅니다.
- [`docs/MIMESIS_ENGINEERING.md`](docs/MIMESIS_ENGINEERING.md) — 문서로 적어 둔 작업 방법: 잘 만들어진 기존 구현·논문·표준을 읽고 그 구조를 로컬에 맞게 옮긴 뒤 검증합니다. 출처 목록은 [`docs/research/`](docs/research)에 있습니다.
- [`avf/`](avf) — 콘텐츠 제작 워크플로용 스키마·템플릿·런북과 샘플 콘텐츠 배치. CLI가 기본으로 임포트하지 않으며, 운영자가 파일을 손으로 사용합니다.

## 경계

호스팅된 서비스는 없고 프로덕션 준비를 주장하지 않습니다. 외부 검증, 벤치마크 우위, 자율 실행의 신뢰성도 주장하지 않습니다. Meta와 MFH는 여기서 문서와 검증 스크립트로 존재합니다. 구성 요소가 서로 어떻게 연결되는지는 [아키텍처 맵](docs/product-quality/metaforge-architecture-map.md)과 [증거 목록](docs/product-quality/product-evidence-manifest.md)에 적혀 있습니다.

## 보안·지원·기여

보안 제보는 [SECURITY.md](SECURITY.md), 지원 경로는 [SUPPORT.md](SUPPORT.md), 기여는 [CONTRIBUTING.md](CONTRIBUTING.md)를 보세요. PR 전에 `bun run build`, `bun run smoke`, 그리고 바꾼 부분에 대한 `bun test`를 돌립니다. 프로젝트 공간에서는 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)를 따릅니다.

## 라이선스

[LICENSE](LICENSE)를 보세요.

---
layout: post
title: "Orca ADE 완벽 정리 — AI 코딩 에이전트를 병렬로 돌리는 차세대 IDE"
subtitle: "Claude Code, Codex, Gemini를 한 화면에서 동시에 — Git Worktree 기반 에이전트 관제탑"
date: 2026-10-26T00:00:00+09:00
author: 수수
tags: ["Orca", "ADE", "AI코딩", "ClaudeCode", "Codex", "GitWorktree", "에이전트IDE", "바이브코딩", "오픈소스", "StablyAI"]
categories: ["개발"]
cover-img: /assets/images/orca_ade_cover.jpg
thumbnail-img: /assets/images/orca_ade_thumb.jpg
---

안녕하세요. 수수입니다.

AI 코딩 에이전트를 하나만 쓰시나요? Claude Code로 백엔드 작업하면서, Codex로 프론트 리팩토링하고, Gemini로 테스트 코드를 동시에 돌리고 싶었던 적 없으신가요?

**Orca**는 정확히 그 문제를 풀기 위해 만들어진 도구입니다. IDE가 아니라 **ADE(Agent Development Environment)** — AI 에이전트들의 관제탑입니다.

2026년 봄 출시 이후 GitHub Stars **66,800+**를 달성하며 빠르게 성장 중인 Orca를 완벽하게 정리해봤습니다.

---

## 목차
{: .no_toc}

* TOC
{:toc}

---

## 1. Orca란?

**Orca**는 [Stably AI](https://github.com/stablyai/orca)(샌프란시스코 스타트업)가 만든 **오픈소스(MIT)** 데스크톱 개발 환경입니다.

핵심 컨셉은 단순합니다:

> 기존 IDE는 **한 명의 개발자**가 코드를 타이핑하는 것을 중심으로 설계됐다.
> ADE는 **여러 AI 에이전트**가 동시에 코드를 작성하는 것을 감독하는 구조로 설계됐다.

| 항목 | 내용 |
|---|---|
| **개발사** | Stably AI (샌프란시스코) |
| **출시** | 2026년 봄 |
| **GitHub Stars** | 66,800+ (2026년 9월 기준) |
| **라이선스** | MIT (완전 오픈소스) |
| **플랫폼** | macOS, Windows, Linux |
| **공식 사이트** | [onorca.dev](https://www.onorca.dev) |

---

## 2. 왜 IDE가 아니라 ADE인가?

### 기존 AI IDE의 한계

Cursor, Windsurf 같은 AI IDE는 기본적으로 **VS Code + AI 어시스턴트** 구조입니다. 한 번에 하나의 에이전트만 쓸 수 있고, 여러 작업을 동시에 시키면 파일 충돌이 생깁니다.

### Orca의 접근법

Orca는 처음부터 다릅니다:

| | **기존 AI IDE** | **Orca (ADE)** |
|---|---|---|
| **설계 중심** | 개발자 1명이 코드 작성 | 여러 AI 에이전트를 동시 감독 |
| **AI 통합** | 기존 에디터에 AI를 추가 | 에이전트 중심으로 처음부터 설계 |
| **동시 작업** | 보통 단일 에이전트 | 여러 에이전트 병렬 실행 |
| **파일 충돌** | 수동 관리 필요 | Git Worktree로 자동 격리 |
| **에이전트 선택** | 특정 에이전트에 종속 | 18개+ 에이전트 자유 선택 |

---

## 3. 핵심 기능 5가지

### 3-1. Git Worktree 격리

Orca의 가장 핵심적인 기능입니다.

새 작업을 만들면 Orca가 자동으로 **독립된 Git Worktree**를 생성합니다. 각 에이전트는 자기만의 디스크 복사본에서 작업하기 때문에 **파일 충돌이 원천적으로 불가능**합니다.

```
프로젝트/
├── .git/                    ← 공유 저장소
├── worktree-backend/        ← Claude Code가 작업 중
├── worktree-frontend/       ← Codex가 리팩토링 중
└── worktree-tests/          ← Gemini가 테스트 작성 중
```

각 워크트리에는 다음이 포함됩니다:
- 에이전트 전용 터미널
- 파일 에디터
- Diff 뷰어
- 내장 브라우저 탭

### 3-2. Agent Dashboard

작업 상태를 한눈에 볼 수 있는 대시보드입니다.

| 컬럼 | 의미 |
|---|---|
| **Needs You** | 사람의 확인이 필요한 작업 |
| **Working** | 에이전트가 현재 작업 중 |
| **Done** | 완료된 작업 |
| **Idle** | 대기 중 (선택적 표시) |

세션별 카드가 상태에 따라 색상으로 구분되고, 프로젝트/PR 필터와 검색 기능을 지원합니다.

### 3-3. 내장 Chromium 브라우저

각 워크트리마다 **실제 Chromium 브라우저**가 들어있습니다. 단순 프리뷰가 아닙니다:

- UI 요소를 클릭하면 **HTML/CSS/스크린샷을 에이전트 컨텍스트에 직접 주입** 가능
- "이 버튼 색상 바꿔줘"를 스크린샷으로 보여주면서 지시 가능
- 프론트엔드 작업에서 특히 강력

### 3-4. 스케줄 자동화 & CLI

- **Scheduled Automations**: 반복 작업을 예약 실행
- **CLI 제공**: 터미널에서 Orca 기능을 직접 호출
- **Skills 시스템**: 에이전트가 사용할 수 있는 도구/기능 세트

### 3-5. 플러그인 시스템 (실험적)

- 마켓플레이스에서 콘텐츠 팩, 패널, 워커 설치
- 플러그인별 동의 후 활성화
- 아직 실험 단계이지만 확장성이 기대되는 부분

---

## 4. 지원 에이전트 목록

Orca는 **터미널에서 실행 가능한 거의 모든 코딩 에이전트**를 지원합니다:

| 에이전트 | 개발사 | 지원 |
|---|---|:---:|
| **Claude Code** | Anthropic | ✅ |
| **Codex** | OpenAI | ✅ |
| **Cursor CLI** | Anysphere | ✅ |
| **GitHub Copilot CLI** | GitHub/MS | ✅ |
| **Gemini** | Google | ✅ |
| **Grok Bot** | xAI | ✅ |
| **OpenCode** | 커뮤니티 | ✅ |
| **Pi** | Inflection | ✅ |
| 기타 CLI 에이전트 (18+) | 다양 | ✅ |

자신의 구독/API 키로 에이전트를 사용하므로, Orca 자체에 추가 비용은 없습니다.

---

## 5. 설치 방법

### macOS (Homebrew)

```bash
brew install --cask stablyai/orca/orca
```

### Windows

[onOrca.dev](https://www.onorca.dev/docs/install) 또는 GitHub Releases에서 `.exe` 다운로드 후 설치

### Linux

| 형식 | 대상 |
|---|---|
| **AppImage** | 범용 |
| **.deb** | Ubuntu/Debian |
| **.rpm** | Fedora/RHEL |
| **AUR** | Arch Linux |

---

## 6. 시작하기 (Getting Started)

설치 후 5단계면 바로 사용할 수 있습니다:

1. **Orca 설치** — 위 방법 중 택 1
2. **에이전트 CLI 준비** — 최소 1개 이상 (예: `claude` CLI)
3. **Orca 실행 → Add Repo** — 프로젝트 폴더 선택
4. **"+" 버튼** → 작업 이름 입력 → 에이전트 선택
5. **자동 시작** — Orca가 Git Worktree를 생성하고 에이전트를 실행

> 첫 실행 시 기존 `~/.claude`, `~/.codex` 설정을 자동으로 import할 수 있습니다.

---

## 7. 병렬 워크트리 구성 가이드

Orca의 핵심은 **여러 에이전트를 동시에 돌리는 것**입니다. 구체적인 구성 방법을 단계별로 정리합니다.

### 7-1. 기본 원리: 1 작업 = 1 워크트리 = 1 에이전트

Git Worktree는 하나의 `.git` 저장소에서 **여러 개의 독립된 작업 디렉토리**를 만드는 Git 기본 기능입니다. Orca는 이걸 자동화합니다.

```
my-project/
├── .git/                          ← 공유 저장소 (1개)
│
├── .worktrees/
│   ├── add-auth-api/              ← 워크트리 A (Claude Code)
│   │   ├── src/
│   │   ├── package.json
│   │   └── ...                    ← main 브랜치의 전체 복사본
│   │
│   ├── refactor-ui/               ← 워크트리 B (Codex)
│   │   ├── src/
│   │   ├── package.json
│   │   └── ...                    ← 독립된 또 다른 복사본
│   │
│   └── write-tests/               ← 워크트리 C (Gemini)
│       ├── src/
│       └── ...
```

각 워크트리는 **물리적으로 다른 디렉토리**입니다. Claude Code가 `auth.ts`를 수정하는 동안 Codex가 같은 파일을 건드려도 서로 다른 복사본이라 충돌이 생기지 않습니다.

### 7-2. 워크트리 생성 (Step by Step)

**Step 1: 저장소 추가**

Orca 사이드바에서 **Add Repo** 클릭 → 프로젝트 폴더 선택. Orca가 `.git`을 인식하고 저장소를 등록합니다.

**Step 2: 첫 번째 워크트리 생성**

저장소 이름 옆 **"+" 버튼** 클릭:

1. **작업 이름 입력** — 예: `add-auth-api` (미입력 시 바다 테마 이름 자동 생성)
2. **에이전트 선택** — 콤보 박스에서 Claude Code, Codex, Gemini 등 선택
3. **베이스 브랜치 선택** — 어떤 브랜치에서 분기할지 지정 (기본: main)

클릭하면 Orca가 자동으로:
- `git worktree add`를 실행해 독립 디렉토리 생성
- 해당 디렉토리에서 에이전트 CLI를 실행
- 전용 터미널, 에디터, 브라우저 탭을 할당

**Step 3: 두 번째, 세 번째 워크트리 추가**

같은 방식으로 **"+"를 반복**합니다. 세 번이면 세 개의 에이전트가 동시에 돌아갑니다.

```
[+] add-auth-api     → Claude Code  → Working...
[+] refactor-ui      → Codex        → Working...
[+] write-tests      → Gemini       → Working...
```

### 7-3. 에이전트에게 작업 지시

각 워크트리를 클릭하면 해당 에이전트의 **전용 터미널**이 열립니다. 여기서 프롬프트를 입력하면 됩니다.

같은 프롬프트를 여러 에이전트에 동시에 보내는 것도 가능합니다 (에이전트 A/B 테스트용).

### 7-4. 모니터링: Agent Dashboard

작업이 돌아가는 동안 **Dashboard 탭**에서 전체 상황을 확인합니다:

```
┌─────────────────────────────────────────────────┐
│  Needs You (1)  │  Working (2)  │  Done (0)     │
├─────────────────┼───────────────┼───────────────┤
│  refactor-ui    │  add-auth-api │               │
│  🟡 확인 필요   │  🔵 작업 중   │               │
│                 │  write-tests  │               │
│                 │  🔵 작업 중   │               │
└─────────────────┴───────────────┴───────────────┘
```

- **Needs You** 상태가 되면 에이전트가 사람의 확인을 요청하는 것
- 카드를 클릭하면 해당 워크트리의 터미널/에디터로 바로 이동

### 7-5. 리뷰: Diff 비교

에이전트가 작업을 마치면, Orca의 **Diff 뷰어**에서 변경사항을 확인합니다.

- 각 워크트리별로 변경된 파일과 코드 차이를 확인
- **코드 라인에 직접 코멘트** 가능 — 코멘트가 에이전트에게 바로 전달됨
- 여러 에이전트의 결과를 **side-by-side로 비교** 가능

### 7-6. 머지: 최종 반영

리뷰가 끝나면 결과를 main 브랜치에 반영합니다:

1. **단일 에이전트 결과 머지** — 워크트리의 브랜치를 main에 머지 (일반 Git 머지)
2. **여러 에이전트 결과 중 선택** — 가장 좋은 결과를 cherry-pick
3. **혼합 머지** — 여러 에이전트의 결과에서 각각 좋은 부분만 골라 합치기

머지 후 워크트리는 삭제하거나 다음 작업에 재활용할 수 있습니다.

### 7-7. 실전 시나리오 3가지

**시나리오 1: 풀스택 병렬 개발**

```
워크트리 A (Claude Code)  → API 엔드포인트 구현
워크트리 B (Codex)        → React 컴포넌트 리팩토링
워크트리 C (Gemini)       → E2E 테스트 작성
```

서로 다른 영역을 동시에 진행해 개발 속도를 3배로 높일 수 있습니다.

**시나리오 2: 에이전트 A/B 테스트**

```
워크트리 A (Claude Code)  → "인증 시스템 구현해줘"
워크트리 B (Codex)        → "인증 시스템 구현해줘"  (동일 프롬프트)
```

같은 작업을 다른 에이전트에 시키고, Diff를 비교해서 더 나은 결과를 채택합니다.

**시나리오 3: 코드 리뷰 + 버그 수정 동시 진행**

```
워크트리 A (Claude Code)  → PR 코드 리뷰 & 피드백 작성
워크트리 B (Codex)        → 리포트된 버그 수정
```

### 7-8. 병렬 작업 시 주의사항

| 항목 | 권장 사항 |
|---|---|
| **메모리** | 에이전트 5개 병렬 실행 시 약 10GB 메모리 소모 |
| **적합한 작업** | 여러 해법이 가능한 작업 (설계, 탐색적 버그 수정) |
| **비적합한 작업** | 단순 기계적 작업 (이름 변경, 포매팅)은 단일 에이전트로 충분 |
| **리소스 부족 시** | SSH Worktree로 원격 서버에서 에이전트 실행 가능 |
| **브랜치 관리** | 워크트리별로 자동 생성된 브랜치가 쌓이므로, 머지 후 정리 권장 |

---

## 8. Orca vs 경쟁 도구 비교

| 항목 | **Orca** | **Cursor** | **Windsurf** | **VS Code + Copilot** |
|---|---|---|---|---|
| **카테고리** | ADE | AI IDE | AI IDE | IDE + 확장 |
| **동시 에이전트** | 여러 개 병렬 | 1개 | 1개 | 1개 |
| **에이전트 선택** | 18개+ 자유 | Cursor 내장 | Windsurf 내장 | Copilot |
| **파일 격리** | Git Worktree 자동 | 없음 | 없음 | 없음 |
| **에이전트 대시보드** | ✅ | ❌ | ❌ | ❌ |
| **내장 브라우저** | Chromium (컨텍스트 주입) | ❌ | ❌ | 제한적 |
| **가격** | 무료 (MIT) | 유료 | 유료 | 유료 |
| **오픈소스** | ✅ | ❌ | ❌ | ❌ |

---

## 9. 장단점 정리

### 장점

- **병렬 에이전트 실행**: 여러 AI가 동시에 독립적으로 작업
- **에이전트 무관**: 특정 AI에 종속되지 않음, 자유롭게 교체 가능
- **Git Worktree 격리**: 충돌 걱정 없는 안전한 병렬 작업
- **MIT 오픈소스**: 무료, 커스터마이징 자유
- **빠른 업데이트**: 거의 매일 릴리스

### 단점

- **코드 에디터 자체로는 부족**: VS Code 수준의 에디터 기능은 기대하기 어려움
- **학습 곡선**: ADE라는 새로운 패러다임에 적응 필요
- **플러그인 생태계**: 아직 실험 단계, Cursor/VS Code 대비 부족
- **에이전트 비용은 별도**: Orca는 무료지만 각 에이전트 구독료는 그대로

---

## 10. 누구에게 추천하나?

| 상황 | 추천 여부 |
|---|:---:|
| 여러 AI 에이전트를 동시에 활용하고 싶다 | ✅ 강력 추천 |
| 특정 에이전트에 종속되고 싶지 않다 | ✅ 추천 |
| Git 기반 워크플로우에 익숙하다 | ✅ 추천 |
| AI 코딩 에이전트를 처음 써본다 | ⚠️ Cursor 먼저 추천 |
| VS Code 수준의 에디터가 필요하다 | ⚠️ 보조 도구로 활용 |
| 팀 단위로 에이전트를 운영하고 싶다 | ✅ 추천 |

---

## 마무리

Orca는 **"AI 에이전트 시대의 개발 환경은 어떤 모습이어야 하는가?"**라는 질문에 대한 하나의 답입니다.

기존 IDE에 AI를 끼워넣는 방식이 아니라, **여러 AI 에이전트를 병렬로 관리하는 관제탑**이라는 새로운 카테고리(ADE)를 제시했습니다.

2026년 봄 출시 이후 6개월 만에 GitHub Stars 66,800+를 달성한 것은, 많은 개발자들이 이미 "여러 에이전트를 동시에 굴리고 싶다"는 니즈를 갖고 있었다는 방증입니다.

아직 VS Code 수준의 에디터 기능이나 풍부한 플러그인 생태계를 기대하기는 어렵지만, ADE라는 새로운 패러다임의 선두주자로서 계속 주목할 가치가 있는 프로젝트입니다.

---

## 참고 링크

- [Orca GitHub](https://github.com/stablyai/orca)
- [Orca 공식 문서](https://www.onorca.dev/docs)
- [Orca 설치 가이드](https://www.onorca.dev/docs/install)
- [Orca Review 2026](https://vibecodinghub.org/blog/orca-review)
- [Orca: The IDE Designed from the Ground Up for AI Agents](https://facundouferer.ar/en/articles/orca/)
- [Orca ADE Explained (DEV Community)](https://dev.to/arshtechpro/orca-explained-the-agent-development-environment-for-running-ai-coding-agents-in-parallel-440n)

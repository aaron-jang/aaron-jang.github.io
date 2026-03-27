---
layout: post
title: "Claude Code 에이전트 팀 — AI 개발자 여러 명을 동시에 굴리는 법"
subtitle: "서브에이전트와 에이전트 팀, 두 가지 방식으로 병렬 AI 개발 환경 만들기"
share-description: "Claude Code의 커스텀 서브에이전트와 에이전트 팀 기능을 활용해 AI 개발자 여러 명이 동시에 일하는 환경을 구성하는 방법을 총정리합니다. 설정법, 실전 예시, 비용까지."
date: 2026-03-10T13:00:00+09:00
lastmod: 2026-03-13T08:52:13+09:00
author: 수수
tags: ["ClaudeCode", "AI", "에이전트", "멀티에이전트", "서브에이전트", "AgentTeams", "개발도구", "바이브코딩", "Anthropic"]
categories: ["AI"]
cover-img: /assets/images/claude_agent_team.webp
thumbnail-img: /assets/images/claude_agent_team_thumb.webp
share-img: /assets/images/claude_agent_team.png
---

안녕하세요. 수수입니다.

Claude Code를 쓰다 보면 이런 생각이 듭니다 — **"이거 여러 명이 동시에 하면 안 되나?"**

코드 리뷰하면서 테스트도 돌리고, 프론트엔드 수정하면서 백엔드 API도 만들고. 사람이라면 불가능하지만, **AI 에이전트라면 가능합니다.**

2026년 2월, Anthropic이 **에이전트 팀(Agent Teams)** 기능을 공개했습니다. 기존의 서브에이전트(Subagent)와 함께, Claude Code에서 **AI 개발자 여러 명을 동시에 굴리는** 두 가지 방법이 생긴 것입니다.

이 글에서는 **서브에이전트**와 **에이전트 팀**, 두 가지를 모두 다룹니다. 설정법부터 실전 활용까지.

---

* TOC
{:toc}

---

## 30초 요약 — 바쁜 분을 위해

| 항목 | 서브에이전트 | 에이전트 팀 |
|------|------------|-----------|
| **구조** | 메인 에이전트가 심부름꾼을 보냄 | 팀 리더 + 팀원이 협업 |
| **소통** | 결과만 메인에 보고 | 팀원끼리 직접 대화 |
| **컨텍스트** | 메인 세션 안에서 동작 | 각자 독립된 세션 |
| **토큰 비용** | 낮음 (요약만 전달) | 높음 (세션 수만큼) |
| **적합한 작업** | 결과만 필요한 작업 | 토론·협업이 필요한 작업 |
| **상태** | 안정 (정식 기능) | 실험적 (Experimental) |

**한 줄 정리**: 간단한 위임은 서브에이전트, 복잡한 협업은 에이전트 팀.

---

## 1. 서브에이전트 — 전문가를 심부름 보내기

### 서브에이전트란?

서브에이전트는 **특정 작업에 특화된 AI 도우미**입니다. 각자 독립된 컨텍스트 윈도우에서 작업하고, 결과만 메인 대화로 돌려보냅니다.

쉽게 말해, **"이거 조사 좀 해줘"**라고 프리랜서에게 맡기는 것과 같습니다.

### 언제 쓰나?

- **테스트 실행** 후 실패한 것만 요약받고 싶을 때
- **코드 리뷰**를 병렬로 돌리고 싶을 때
- **문서 조사** 결과만 간단히 받고 싶을 때
- 메인 대화의 **컨텍스트를 아끼고** 싶을 때

### 빌트인 서브에이전트

Claude Code에는 이미 내장된 서브에이전트가 있습니다.

| 이름 | 모델 | 역할 |
|------|------|------|
| **Explore** | Haiku (빠름) | 코드 탐색, 파일 검색 (읽기 전용) |
| **Plan** | 메인 모델 상속 | 계획 모드에서 코드 조사 |
| **General-purpose** | 메인 모델 상속 | 복잡한 멀티스텝 작업 |

### 커스텀 서브에이전트 만들기

직접 만드는 것도 간단합니다. **마크다운 파일 하나**면 됩니다.

#### 방법 1: `/agents` 명령어 (추천)

Claude Code에서 `/agents`를 입력하면 대화형 인터페이스가 열립니다.

```
/agents
→ Create new agent
→ User-level (모든 프로젝트에서 사용) 또는 Project-level (현재 프로젝트만)
→ Generate with Claude (자동 생성) 또는 직접 작성
```

#### 방법 2: 마크다운 파일 직접 작성

`.claude/agents/` 폴더에 마크다운 파일을 만들면 됩니다.

**코드 리뷰어 예시** (`.claude/agents/code-reviewer.md`):

```markdown
---
name: code-reviewer
description: 코드 변경 후 품질·보안·유지보수성을 리뷰합니다. 코드 수정 후 자동 사용.
tools: Read, Grep, Glob, Bash
model: sonnet
---

시니어 코드 리뷰어로서 코드 품질과 보안을 검토합니다.

호출 시:
1. git diff로 변경사항 확인
2. 변경된 파일에 집중
3. 즉시 리뷰 시작

리뷰 기준:
- 코드 가독성과 네이밍
- 중복 코드 여부
- 에러 처리
- 보안 취약점 (API 키 노출, 입력 검증)
- 테스트 커버리지
- 성능 이슈

우선순위별 피드백:
- Critical (반드시 수정)
- Warning (수정 권장)
- Suggestion (개선 고려)
```

**디버거 예시** (`.claude/agents/debugger.md`):

```markdown
---
name: debugger
description: 에러, 테스트 실패, 예상치 못한 동작을 디버깅합니다. 문제 발생 시 자동 사용.
tools: Read, Edit, Bash, Grep, Glob
model: inherit
---

근본 원인 분석 전문 디버거입니다.

호출 시:
1. 에러 메시지와 스택 트레이스 확인
2. 재현 단계 파악
3. 실패 지점 격리
4. 최소한의 수정 적용
5. 수정 결과 검증
```

### 서브에이전트 저장 위치

| 위치 | 범위 | 우선순위 |
|------|------|---------|
| `--agents` CLI 플래그 | 현재 세션만 | 1 (최고) |
| `.claude/agents/` | 현재 프로젝트 | 2 |
| `~/.claude/agents/` | 모든 프로젝트 | 3 |
| 플러그인의 `agents/` | 플러그인 활성화된 곳 | 4 (최저) |

**팁**: 프로젝트 서브에이전트(`.claude/agents/`)는 Git에 커밋하면 팀원과 공유할 수 있습니다.

### 서브에이전트 주요 설정

```yaml
---
name: my-agent           # 필수: 고유 이름 (소문자, 하이픈)
description: 설명        # 필수: Claude가 언제 이 에이전트를 쓸지 판단하는 기준
tools: Read, Grep, Bash  # 사용 가능한 도구 (생략 시 전체 상속)
disallowedTools: Write   # 차단할 도구
model: sonnet            # sonnet, opus, haiku, inherit 중 선택
permissionMode: default  # 권한 모드
maxTurns: 10             # 최대 턴 수
memory: user             # 영구 메모리 (user, project, local)
background: false        # 백그라운드 실행 여부
isolation: worktree      # Git worktree 격리 실행
---
```

### 영구 메모리 기능

`memory` 필드를 설정하면 서브에이전트가 **대화를 넘어서 학습**합니다.

```yaml
---
name: code-reviewer
description: 코드 리뷰 전문가
memory: user
---

코드를 리뷰하면서 발견한 패턴, 컨벤션, 반복되는 이슈를
에이전트 메모리에 업데이트합니다.
```

| 범위 | 저장 위치 | 용도 |
|------|----------|------|
| `user` | `~/.claude/agent-memory/` | 모든 프로젝트에서 학습 유지 |
| `project` | `.claude/agent-memory/` | 프로젝트별 학습 (Git 공유 가능) |
| `local` | `.claude/agent-memory-local/` | 프로젝트별 학습 (Git 제외) |

"이전에 리뷰한 패턴 기억해?"라고 물으면, 실제로 기억합니다.

### 서브에이전트 사용법

```text
# 명시적 호출
code-reviewer 서브에이전트로 최근 변경사항 리뷰해줘

# 병렬 리서치
인증, 데이터베이스, API 모듈을 각각 별도 서브에이전트로 동시에 조사해줘

# 체이닝
code-reviewer로 성능 이슈 찾고, 그 결과로 optimizer 서브에이전트가 수정해줘
```

---

## 2. 에이전트 팀 — AI 개발팀 운영하기

### 에이전트 팀이란?

에이전트 팀은 **여러 Claude Code 세션이 하나의 팀**으로 일하는 기능입니다.

서브에이전트가 "프리랜서에게 심부름 보내기"라면, 에이전트 팀은 **"같은 방에 앉아서 일하는 프로젝트 팀"**입니다.

핵심 차이: **팀원끼리 직접 대화하고, 서로의 작업을 도전하고, 스스로 태스크를 가져갈 수 있습니다.**

### 활성화 방법

에이전트 팀은 **실험적 기능**이라 수동으로 켜야 합니다.

`settings.json`에 추가:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

또는 환경 변수로:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### 팀 구성 요소

| 구성요소 | 역할 |
|---------|------|
| **팀 리더** | 팀 생성, 팀원 관리, 작업 조율, 결과 종합 |
| **팀원** | 각자 독립된 Claude Code 세션에서 작업 수행 |
| **태스크 리스트** | 공유 작업 목록 (pending → in progress → completed) |
| **메일박스** | 에이전트 간 메시지 시스템 |

### 팀 만들기

자연어로 요청하면 됩니다.

```text
CLI 도구를 설계하려고 해. 에이전트 팀을 만들어줘:
- UX 담당 1명
- 기술 아키텍처 담당 1명
- 반론 전문(Devil's Advocate) 1명
```

Claude가 자동으로 팀을 구성하고, 팀원을 생성하고, 작업을 할당합니다.

### 실전 활용 예시

#### PR 병렬 코드 리뷰

한 명이 리뷰하면 한 가지 관점에 편향됩니다. 세 명이 각자 다른 렌즈로 보면 훨씬 철저합니다.

```text
PR #142를 리뷰할 에이전트 팀을 만들어줘:
- 보안 전문 리뷰어 1명
- 성능 영향 체크 1명
- 테스트 커버리지 검증 1명
각자 리뷰 후 결과를 보고하게 해줘.
```

#### 버그 원인 조사 — 가설 경쟁

원인이 불분명할 때, 한 에이전트는 첫 번째 설명을 찾으면 멈추기 쉽습니다. 여러 에이전트가 **서로의 가설을 반박하게** 만드세요.

```text
앱이 메시지 하나 보내고 종료되는 버그가 있어.
5명의 팀원을 만들어서 각자 다른 가설을 조사하게 해줘.
서로 대화하면서 상대 이론을 반증하도록 해.
과학 토론처럼. 합의된 결론을 findings 문서에 정리해줘.
```

#### 새 기능 병렬 개발

프론트엔드, 백엔드, 테스트를 각각 다른 팀원이 담당합니다.

```text
인증 모듈을 구현할 팀을 만들어줘:
- 프론트엔드 (로그인 UI) 담당
- 백엔드 (API + DB) 담당
- 테스트 (E2E + 유닛) 담당
Sonnet 모델을 사용해줘.
```

### 디스플레이 모드

| 모드 | 설명 | 요구사항 |
|------|------|---------|
| **In-process** (기본) | 모든 팀원이 하나의 터미널에서 실행 | 없음 |
| **Split panes** | 각 팀원이 별도 패널에서 실행 | tmux 또는 iTerm2 |

In-process 모드에서 `Shift+Down`으로 팀원 간 전환, Split panes에서는 클릭으로 이동합니다.

기본값은 `"auto"`입니다. tmux 세션 안에서 실행 중이면 자동으로 Split panes, 아니면 In-process로 동작합니다.

#### Split panes 설정하기

Split panes를 쓰려면 **tmux** 또는 **iTerm2** 중 하나가 필요합니다.

**방법 1: tmux (macOS 추천)**

```bash
# macOS — Homebrew로 설치
brew install tmux

# Ubuntu/Debian
sudo apt install tmux
```

설치 후 `settings.json`에서 모드를 변경합니다:

```json
{
  "teammateMode": "tmux"
}
```

또는 실행 시 플래그로 지정:

```bash
claude --teammate-mode tmux
```

> **참고**: tmux는 macOS에서 가장 안정적입니다. iTerm2를 쓴다면 `tmux -CC` 모드로 실행하는 것을 추천합니다.

**방법 2: iTerm2 (macOS 전용)**

1. [it2 CLI](https://github.com/mkusaka/it2)를 설치합니다
2. iTerm2 → **Settings** → **General** → **Magic** → **Enable Python API** 체크
3. `settings.json`에서 동일하게 `"teammateMode": "tmux"` 설정 (tmux와 iTerm2를 자동 감지합니다)

**In-process 모드로 강제 전환**

Split panes 없이 하나의 터미널에서 운영하고 싶다면:

```json
{
  "teammateMode": "in-process"
}
```

> **주의**: VS Code 내장 터미널, Windows Terminal, Ghostty에서는 Split panes가 지원되지 않습니다. 이 환경에서는 In-process 모드를 사용하세요.

### 팀원과 직접 대화하기

팀원은 **완전한 독립 Claude Code 세션**입니다. 리더를 거치지 않고 팀원에게 직접 지시할 수 있습니다.

- **In-process**: `Shift+Down`으로 팀원 선택 → 메시지 입력
- **Split panes**: 해당 팀원 패널 클릭 → 직접 대화

### 팀 정리

작업이 끝나면 리더에게 정리를 요청합니다.

```text
팀원들 종료시키고 팀 정리해줘
```

팀원 종료 → 리더가 cleanup 실행 순서입니다. **반드시 리더가 정리**해야 합니다.

---

## 3. 서브에이전트 vs 에이전트 팀 — 어떤 걸 써야 할까?

### 선택 기준

| 상황 | 추천 방식 |
|------|----------|
| 테스트 돌리고 결과만 받기 | 서브에이전트 |
| 코드 리뷰 (읽기 전용) | 서브에이전트 |
| 문서 조사 | 서브에이전트 |
| 순차적 작업 (A 끝나면 B) | 서브에이전트 체이닝 |
| 여러 관점에서 동시 리뷰 | 에이전트 팀 |
| 프론트·백엔드·테스트 병렬 개발 | 에이전트 팀 |
| 버그 원인 토론 | 에이전트 팀 |
| 같은 파일을 수정해야 할 때 | 단일 세션 (충돌 방지) |

### 비용 차이

- **서브에이전트**: 결과만 메인으로 요약 전달 → 토큰 효율적
- **에이전트 팀**: 팀원 수만큼 독립 세션 → **약 2.5배** 토큰 소모, 대신 **약 2배** 빠름

**3명 팀 기준**: 비용 2.5배, 속도 2배. 복잡한 작업에서는 시간 절약이 비용을 상쇄합니다.

---

## 4. 실전 팁 — 잘 쓰려면

### 서브에이전트 팁

**1. description을 잘 써라**

Claude가 서브에이전트를 쓸지 말지 `description`을 보고 판단합니다. 구체적으로 쓰세요.

```yaml
# ❌ 나쁜 예
description: 코드를 봅니다

# ✅ 좋은 예
description: 코드 변경 후 품질·보안·유지보수성을 리뷰합니다. 코드 수정 후 자동 사용.
```

**2. 도구를 최소한으로**

코드 리뷰어에게 `Write`, `Edit` 권한을 줄 필요가 없습니다. 읽기 전용으로 제한하세요.

**3. 모델을 적절히 선택**

- 단순 탐색: `haiku` (빠르고 저렴)
- 분석 작업: `sonnet` (균형)
- 복잡한 판단: `opus` 또는 `inherit`

### 에이전트 팀 팁

**1. 3~5명이 적당하다**

팀원이 많을수록 조율 오버헤드가 커집니다. 대부분의 작업에서 3~5명이 최적입니다.

**2. 팀원당 5~6개 태스크**

태스크가 너무 적으면 조율 비용이 아깝고, 너무 많으면 컨텍스트 전환이 잦아집니다.

**3. 같은 파일 수정은 피해라**

두 팀원이 같은 파일을 수정하면 덮어쓰기가 발생합니다. **파일 소유권을 명확히** 분리하세요.

**4. CLAUDE.md를 잘 작성해라**

팀원은 메인의 대화 기록을 상속받지 않습니다. 대신 **CLAUDE.md를 자동으로 읽습니다.** 모듈 구조, 컨벤션, 검증 명령어를 CLAUDE.md에 잘 정리하면 팀원의 탐색 비용이 크게 줄어듭니다.

**5. 리서치·리뷰부터 시작해라**

에이전트 팀이 처음이라면 코드 수정 없는 작업부터 시작하세요. PR 리뷰, 라이브러리 조사, 버그 분석 같은 읽기 전용 작업이 좋습니다.

---

## 5. 현재 제한사항 (2026년 3월)

에이전트 팀은 아직 **실험적 기능**입니다. 알아두어야 할 제한사항:

| 제한 | 설명 |
|------|------|
| **세션 복원 불가** | `/resume`이 in-process 팀원을 복원하지 못함 |
| **태스크 상태 지연** | 팀원이 완료 표시를 안 하는 경우 있음 |
| **1팀/세션** | 한 리더가 동시에 1개 팀만 운영 가능 |
| **중첩 팀 불가** | 팀원이 자기 팀원을 만들 수 없음 |
| **리더 고정** | 팀 생성자가 영구 리더, 변경 불가 |
| **Split panes** | VS Code 내장 터미널, Windows Terminal에서 미지원 |

서브에이전트는 정식 기능이라 이런 제한이 없지만, **서브에이전트끼리는 대화할 수 없다**는 구조적 한계가 있습니다.

---

## 정리하며

Claude Code의 멀티에이전트 시스템을 정리하면 이렇습니다.

**단순한 위임** → 서브에이전트 (프리랜서에게 심부름)
**복잡한 협업** → 에이전트 팀 (프로젝트 팀 운영)

둘 다 핵심은 같습니다 — **병렬 처리로 시간을 줄이고, 컨텍스트 분리로 품질을 높이는 것.**

서브에이전트부터 시작해보세요. `.claude/agents/` 폴더에 마크다운 파일 하나 만드는 것만으로 바로 쓸 수 있습니다. 익숙해지면 에이전트 팀으로 넘어가면 됩니다.

---

이상, 수수였습니다. 궁금한 점은 댓글로 남겨주세요!

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Claude Code 서브에이전트와 에이전트 팀의 차이는 무엇인가요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "서브에이전트는 메인 세션 안에서 작업을 위임하고 결과만 돌려받는 구조입니다. 에이전트 팀은 여러 독립된 Claude Code 세션이 팀 리더 아래에서 공유 태스크 리스트와 메시지 시스템을 통해 직접 소통하며 협업합니다. 서브에이전트는 토큰 비용이 낮고, 에이전트 팀은 약 2.5배 비용이 들지만 2배 빠릅니다."
      }
    },
    {
      "@type": "Question",
      "name": "Claude Code 에이전트 팀을 활성화하는 방법은?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "에이전트 팀은 실험적 기능으로, settings.json에 { \"env\": { \"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS\": \"1\" } }을 추가하거나, 환경 변수로 export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1을 설정하면 활성화됩니다."
      }
    },
    {
      "@type": "Question",
      "name": "커스텀 서브에이전트는 어떻게 만드나요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Claude Code에서 /agents 명령어로 대화형 생성하거나, .claude/agents/ 폴더에 YAML 프론트매터가 포함된 마크다운 파일을 직접 만들면 됩니다. name, description은 필수이며, tools, model, memory 등을 설정할 수 있습니다. 프로젝트 레벨(.claude/agents/)은 Git으로 팀과 공유 가능합니다."
      }
    },
    {
      "@type": "Question",
      "name": "에이전트 팀의 적정 인원은 몇 명인가요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "대부분의 작업에서 3~5명이 최적입니다. 팀원당 5~6개 태스크를 할당하면 생산성과 조율 비용의 균형이 맞습니다. 팀원이 많을수록 토큰 비용이 선형으로 증가하고 조율 오버헤드도 커지므로, 작업이 실제로 병렬화 가능한 경우에만 인원을 늘리는 것이 좋습니다."
      }
    }
  ]
}
</script>

## 참고 자료

- [Claude Code 공식 문서 — 에이전트 팀](https://code.claude.com/docs/en/agent-teams)
- [Claude Code 공식 문서 — 커스텀 서브에이전트](https://code.claude.com/docs/en/sub-agents)
- [Anthropic Engineering — Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Claude Agent SDK Python — GitHub](https://github.com/anthropics/claude-agent-sdk-python)
- [Addy Osmani — Claude Code Swarms](https://addyosmani.com/blog/claude-code-agent-teams/)

---
layout: post
title: "텔레그램으로 Claude Code 원격 사용하기 완벽 가이드"
subtitle: "스마트폰에서 코딩 에이전트를 쓴다고? — claude-code-telegram 설치부터 실전 활용까지"
share-description: "텔레그램 봇으로 Claude Code를 원격 제어하는 방법을 정리합니다. 설치, 설정, 보안, 실전 활용 팁까지 한 번에 알아보세요."
date: 2026-03-23T09:00:00+09:00
lastmod: 2026-03-23T11:52:09+09:00
author: 수수
tags: ["ClaudeCode", "텔레그램", "AI코딩", "원격개발", "개발도구", "Python", "자동화", "봇"]
categories: ["IT"]
---

안녕하세요. 수수입니다.

카페에서 노트북 없이 스마트폰만으로 서버 코드를 고칠 수 있다면? **claude-code-telegram**을 쓰면 가능합니다.

Anthropic의 AI 코딩 에이전트인 **Claude Code**를 텔레그램 봇으로 감싸서, 어디서든 대화하듯 코드를 읽고, 수정하고, 실행할 수 있게 해주는 오픈소스 프로젝트입니다.

오늘은 설치부터 실전 활용까지 한 번에 정리해 보겠습니다.

---

## 목차
{: .no_toc}

* TOC
{:toc}

---

## 30초 핵심 요약

- **프로젝트**: [claude-code-telegram](https://github.com/RichardAtCT/claude-code-telegram) (MIT 라이선스)
- **한 줄 설명**: 텔레그램으로 Claude Code를 원격 제어하는 봇
- **주요 기능**: 대화형 코딩, 파일 업로드, 음성 메시지, Git 연동, 비용 추적
- **요구 사항**: Python 3.11+, Claude Code CLI, 텔레그램 봇 토큰
- **두 가지 모드**: Agentic(대화형) / Classic(터미널형)

---

## 이게 뭔가요?

### 어떤 문제를 해결하나?

Claude Code는 강력한 AI 코딩 에이전트이지만, **터미널에서만** 쓸 수 있습니다. 노트북을 열어야 하고, SSH로 접속해야 하고, 이동 중에는 사용이 어렵습니다.

claude-code-telegram은 이 제약을 없앱니다.

| 기존 방식 | claude-code-telegram |
|-----------|---------------------|
| 터미널 필수 | 텔레그램 앱이면 충분 |
| 노트북·데스크톱만 | 스마트폰·태블릿 어디서든 |
| SSH 접속 필요 | 텔레그램 메시지로 대화 |
| 세션 끊기면 초기화 | 세션 자동 유지 (SQLite) |

### 주요 기능

- **16개 도구 지원**: Read, Write, Edit, Bash, Glob, Grep 등 Claude Code의 핵심 도구 전부 사용 가능
- **파일 업로드**: 코드 파일, 압축 파일 업로드 → 자동 분석
- **이미지·스크린샷 분석**: 에러 스크린샷 찍어서 보내면 분석해 줌
- **음성 메시지**: 말로 지시하면 텍스트로 변환 후 실행 (Mistral/OpenAI)
- **Git 연동**: 저장소 클론, 상태 확인, 커밋 등
- **비용 추적**: 사용자별 비용 제한 설정 가능
- **MCP 지원**: Model Context Protocol 서버 연동 가능

---

## 사전 준비

시작하기 전에 4가지가 필요합니다.

### 1. Python 3.11 이상

```bash
python3 --version  # 3.11 이상인지 확인
```

### 2. Claude Code CLI 설치 및 인증

```bash
# Claude Code 설치 (npm)
npm install -g @anthropic-ai/claude-code

# 인증
claude auth login
```

또는 `ANTHROPIC_API_KEY` 환경변수를 직접 설정해도 됩니다.

### 3. 텔레그램 봇 토큰 발급

1. 텔레그램에서 [**@BotFather**](https://t.me/BotFather) 검색
2. `/newbot` 명령 입력
3. 봇 이름과 username 설정
4. 발급된 **토큰** 저장 (형식: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 4. 내 텔레그램 사용자 ID 확인

텔레그램에서 [**@userinfobot**](https://t.me/userinfobot)에게 아무 메시지나 보내면 숫자 ID를 알려줍니다.

---

## 설치하기

### 방법 1: uv로 설치 (권장)

```bash
uv tool install git+https://github.com/RichardAtCT/claude-code-telegram@v1.3.0
```

### 방법 2: pip로 설치

```bash
pip install git+https://github.com/RichardAtCT/claude-code-telegram@v1.3.0
```

### 방법 3: 소스에서 설치 (개발용)

```bash
git clone https://github.com/RichardAtCT/claude-code-telegram.git
cd claude-code-telegram
make dev
```

> **주의**: 반드시 **태그 릴리스**에서 설치하세요. `main` 브랜치는 개발 중인 코드가 포함될 수 있습니다.

음성 메시지 기능을 사용하려면:

```bash
pip install "claude-code-telegram[voice]"
```

---

## 환경 변수 설정

`.env` 파일을 만들어 설정합니다.

### 필수 설정

```bash
# 텔레그램 봇 설정
TELEGRAM_BOT_TOKEN=여기에_봇_토큰
TELEGRAM_BOT_USERNAME=내봇_username

# 보안 설정
APPROVED_DIRECTORY=/home/user/projects    # 봇이 접근할 수 있는 디렉토리
ALLOWED_USERS=123456789                   # 허용할 텔레그램 사용자 ID (쉼표 구분)
```

### 주요 선택 설정

```bash
# API 키 (CLI 인증 대신 사용할 경우)
ANTHROPIC_API_KEY=sk-ant-...

# 모드 설정
AGENTIC_MODE=true          # true=대화형, false=터미널형

# 제한 설정
CLAUDE_MAX_TURNS=10        # 세션당 최대 대화 턴
CLAUDE_TIMEOUT_SECONDS=300 # 작업 타임아웃 (초)
CLAUDE_MAX_COST_PER_USER=10.0   # 사용자별 비용 한도 (USD)
CLAUDE_MAX_COST_PER_REQUEST=5.0 # 요청당 비용 한도 (USD)

# 속도 제한
RATE_LIMIT_REQUESTS=10     # 윈도우당 허용 요청 수
RATE_LIMIT_WINDOW=60       # 윈도우 기간 (초)

# 기능 토글
ENABLE_GIT_INTEGRATION=true
ENABLE_FILE_UPLOADS=true
ENABLE_VOICE_MESSAGES=true
VOICE_PROVIDER=mistral     # mistral 또는 openai

# 세션
SESSION_TIMEOUT_HOURS=24
```

---

## 실행하기

```bash
# 일반 실행
make run

# 디버그 모드
make run-debug
```

텔레그램에서 봇에게 `/start`를 보내면 준비 완료입니다.

---

## 두 가지 모드 이해하기

### Agentic 모드 (기본값)

자연어로 대화하듯 사용하는 모드입니다. 대부분의 사용자에게 이 모드를 추천합니다.

**사용 가능한 명령어**:

| 명령어 | 설명 |
|--------|------|
| `/start` | 봇 시작 |
| `/new` | 새 세션 시작 |
| `/status` | 현재 상태 확인 |
| `/verbose` | 상세도 조절 (0/1/2) |
| `/repo` | 작업 디렉토리 변경 |

**사용 예시**:

```
나: 현재 프로젝트의 README.md 내용 보여줘
봇: [파일 내용을 읽고 요약해서 보여줌]

나: setup.py에서 버전을 1.2.0으로 올려줘
봇: [파일을 수정하고 결과를 보여줌]

나: 테스트 돌려봐
봇: [pytest 실행 결과를 보여줌]
```

**상세도(Verbosity) 레벨**:

| 레벨 | 설명 |
|------|------|
| 0 | 조용 — 최종 결과만 표시 |
| 1 | 보통 — 도구 사용과 주요 과정 표시 |
| 2 | 상세 — 모든 추론 과정 표시 |

### Classic 모드

터미널처럼 사용하는 모드입니다. 13개 명령어와 인라인 키보드를 제공합니다.

`AGENTIC_MODE=false`로 설정하면 활성화됩니다. 디렉토리 탐색, 세션 내보내기(Markdown/HTML/JSON) 등 세밀한 제어가 필요할 때 유용합니다.

---

## 실전 활용 시나리오

### 1. 이동 중 긴급 버그 수정

```
나: src/api/auth.py에서 토큰 만료 체크 로직 보여줘
봇: [해당 코드 블록을 보여줌]

나: expires_at 비교할 때 timezone 빠져있네. UTC로 맞춰서 수정해줘
봇: [코드 수정 완료, diff 표시]

나: 커밋하고 푸시해줘. 메시지는 "fix: token expiry timezone handling"으로
봇: [git commit + push 완료]
```

### 2. 스크린샷으로 에러 분석

에러 화면을 스크린샷 찍어서 그대로 보내면 됩니다. 이미지를 분석해서 원인과 해결 방법을 알려줍니다.

### 3. 음성으로 지시

운전 중이거나 타이핑이 어려울 때, 음성 메시지로 지시할 수 있습니다.

```
🎤 "프로젝트에 .gitignore 파일 만들어줘. node_modules랑 .env 제외하도록"
```

음성은 Mistral(기본) 또는 OpenAI Whisper로 텍스트 변환 후 처리됩니다.

### 4. 파일 업로드

코드 파일이나 압축 파일을 텔레그램으로 보내면 자동으로 분석합니다. 리뷰가 필요한 코드를 바로 던져주면 됩니다.

---

## 보안 설정 — 꼭 확인하세요

이 봇은 서버에서 코드를 실행할 수 있기 때문에 보안이 중요합니다. 다행히 5중 보안 레이어가 적용되어 있습니다.

### 보안 레이어 구조

| 레이어 | 설명 |
|--------|------|
| 사용자 화이트리스트 | `ALLOWED_USERS`에 등록된 ID만 사용 가능 |
| 디렉토리 샌드박스 | `APPROVED_DIRECTORY` 밖으로 접근 불가 |
| 속도 제한 | 토큰 버킷 알고리즘으로 요청·비용 제한 |
| 입력 검증 | `rm -rf`, `sudo`, `chmod 777` 등 위험 명령 차단 |
| 감사 로깅 | 모든 작업·보안 이벤트 기록 |

### 반드시 지켜야 할 것

```bash
# ✅ 좋은 예 — 특정 프로젝트 폴더만 허용
APPROVED_DIRECTORY=/home/user/projects

# ❌ 나쁜 예 — 홈 디렉토리 전체를 열면 위험
APPROVED_DIRECTORY=/home/user
```

### 도구 제어

특정 도구를 차단하고 싶다면:

```bash
# Bash와 Write만 차단 (차단 목록이 허용 목록보다 우선)
CLAUDE_DISALLOWED_TOOLS=Bash,Write
```

---

## 비용 관리

Claude Code는 API 호출 비용이 발생합니다. 예상치 못한 과금을 방지하려면 제한을 설정하세요.

```bash
CLAUDE_MAX_COST_PER_USER=10.0     # 사용자당 누적 $10까지
CLAUDE_MAX_COST_PER_REQUEST=5.0   # 요청 1건당 $5까지
CLAUDE_MAX_TURNS=10               # 세션당 최대 10턴
```

`/status` 명령으로 현재 사용량을 확인할 수 있습니다.

---

## 서버에 상시 실행하기

### Linux — systemd 서비스

```bash
# ~/.config/systemd/user/claude-telegram-bot.service 생성 후
systemctl --user enable claude-telegram-bot
systemctl --user start claude-telegram-bot

# 로그아웃 후에도 유지하려면
loginctl enable-linger $USER
```

### macOS — SSH 원격 실행

macOS에서 SSH로 접속해 실행하면 키체인 문제가 생길 수 있습니다.

```bash
# tmux에서 실행 (키체인 비밀번호 입력 프롬프트 제공)
make run-remote

# 세션 관리
make remote-attach   # 세션 접속
make remote-stop     # 세션 중지
```

또는 `ANTHROPIC_API_KEY`를 직접 설정하면 키체인을 우회할 수 있습니다.

---

## 환경별 자동 설정

`ENVIRONMENT` 변수로 환경에 맞는 기본값이 자동 적용됩니다.

| 항목 | development | production |
|------|------------|------------|
| 로그 레벨 | DEBUG | INFO |
| 속도 제한 | 100 req/window | 5 req/window |
| 타임아웃 | 600초 | 300초 |
| 비용 한도 | 제한 없음 | $5/요청 |
| 세션 유지 | 24시간 | 12시간 |

---

## 자주 묻는 질문

### Q. Claude Code CLI 없이 API 키만으로 쓸 수 있나요?

네. `ANTHROPIC_API_KEY`를 설정하면 CLI 없이도 사용 가능합니다. Claude Code SDK를 직접 사용합니다.

### Q. 여러 프로젝트를 동시에 다룰 수 있나요?

`/repo` 명령으로 작업 디렉토리를 변경할 수 있습니다. 단, `APPROVED_DIRECTORY` 하위 폴더여야 합니다. 또한 Project Thread Mode(`ENABLE_PROJECT_THREADS=true`)를 사용하면 텔레그램 그룹의 포럼 토픽별로 프로젝트를 분리할 수 있습니다.

### Q. 다른 사람과 함께 사용할 수 있나요?

`ALLOWED_USERS`에 여러 ID를 추가하면 됩니다. 사용자별로 세션과 비용이 분리 추적됩니다.

### Q. MCP 서버도 연결할 수 있나요?

네. `ENABLE_MCP=true`로 설정하고 `MCP_CONFIG_PATH`에 설정 파일 경로를 지정하면 됩니다.

---

## 마무리

claude-code-telegram은 **"어디서든 Claude Code를"** 이라는 단순한 아이디어를 꽤 완성도 높게 구현한 프로젝트입니다.

특히 유용한 상황:
- 이동 중 긴급 버그 수정
- 서버 상태 확인·간단한 작업
- 팀원과 텔레그램 그룹에서 AI 코딩 에이전트 공유
- 음성·스크린샷 등 모바일 환경에 맞는 인터페이스 활용

보안 레이어가 잘 되어 있긴 하지만, **서버에서 코드를 실행하는 봇**이라는 점은 항상 인지하고 `APPROVED_DIRECTORY`와 `ALLOWED_USERS` 설정을 꼼꼼히 확인하세요.

프로젝트 GitHub: [RichardAtCT/claude-code-telegram](https://github.com/RichardAtCT/claude-code-telegram)

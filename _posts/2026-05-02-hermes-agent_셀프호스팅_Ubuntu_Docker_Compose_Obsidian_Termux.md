---
layout: post
title: "hermes-agent 셀프호스팅 가이드 — Ubuntu Docker Compose + LLM·구글·옵시디언 연동, 안드로이드(Termux)까지"
subtitle: "Nous Research의 자기 개선 AI 에이전트를 내 서버·PC·폰까지 한 번에 연결하기"
share-description: "hermes-agent를 Ubuntu에 Docker Compose로 띄우고, OpenRouter·Anthropic LLM을 연결하고, Google Workspace와 Obsidian vault까지 연동한 다음, 안드로이드 Termux로 폰에서도 쓰는 방법을 정리합니다."
date: 2026-05-02T00:00:00+09:00
lastmod: 2026-05-04T12:39:17+09:00
author: 수수
tags: ["hermes-agent", "AI에이전트", "NousResearch", "Docker", "DockerCompose", "Ubuntu", "셀프호스팅", "Obsidian", "구글연동", "GoogleWorkspace", "Termux", "안드로이드", "OpenRouter", "Anthropic", "Claude", "ClaudeCode", "ClaudeMax"]
categories: ["IT"]
---

안녕하세요. 수수입니다.

요즘 화제인 **hermes-agent**(Nous Research, 노우스 리서치)를 내 Ubuntu 서버에 셀프호스팅하는 방법을 정리해 봤습니다. Docker Compose 한 번으로 띄우고, LLM 연결 → 구글 연동 → 옵시디언(Obsidian) vault 동기화까지 마치면, 마지막에 안드로이드 폰(Termux)에도 같은 에이전트를 깔 수 있습니다.

공식 문서 기준으로 핵심 단계만 추렸으니 따라 하시면 한 시간 안에 끝낼 수 있을 거예요.

## 30초 핵심 요약
{: .no_toc}

| 항목 | 내용 |
|------|------|
| **에이전트** | hermes-agent (Nous Research, 자기 개선·스킬·영구 메모리 내장) |
| **서버 환경** | Ubuntu 22.04+, RAM 4 GB↑, Docker & Compose |
| **컨테이너** | gateway(`:8642`) + dashboard(`:9119`), 데이터: `~/.hermes` |
| **LLM** | OpenRouter / Anthropic API 키 → `~/.hermes/.env` (Claude Max 구독자는 Claude Code OAuth 마운트 가능) |
| **구글 연동** | GCP OAuth(Desktop) → 토큰 자동 갱신, Gmail·Calendar·Drive·Docs·Sheets 접근 |
| **옵시디언** | 서버 vault를 `OBSIDIAN_VAULT_PATH`로 마운트, Syncthing으로 PC·폰 동기화 |
| **안드로이드** | F-Droid Termux + 한 줄 설치 스크립트 |

## 목차
{: .no_toc}

* TOC
{:toc}

---

## hermes-agent란?

hermes-agent는 Nous Research가 공개한 **자기 개선형 CLI AI 에이전트**입니다. 일반 챗봇과 달리 ① 영구 메모리(`~/.hermes`)에 사용자 정보·작업 이력을 저장하고, ② 사용 중에 새 스킬을 만들고 개선하며, ③ 어떤 OpenAI 호환 LLM이든 붙여 쓸 수 있습니다. CLI·TUI·게이트웨이 API·웹 대시보드를 모두 제공해서 서버에서 한 번 띄워두면 PC·폰 어디서든 접근할 수 있어요.

## 사전 준비

```bash
# Ubuntu 22.04 / 24.04 기준
sudo apt update && sudo apt install -y ca-certificates curl
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER && newgrp docker
docker compose version   # v2 확인
```

> 메모리는 4 GB 이상 권장(브라우저 자동화 스킬을 켜려면 8 GB 이상). 디스크는 vault·메모리 누적을 고려해 30 GB 이상이 편합니다.

## 1. Docker Compose로 서버 띄우기

### 1-1. 초기 셋업 (API 키 입력)
컨테이너로 setup을 한 번 돌리면 `~/.hermes/.env`에 키와 토큰이 안전하게 저장됩니다.

> ⚠️ **권한 함정 주의**: 컨테이너 내부 `hermes` 사용자의 기본 UID/GID가 **10000**으로 박혀 있습니다. 그대로 실행하면 호스트 `~/.hermes` 안의 파일들이 uid 10000 소유로 만들어져 호스트에서 읽고 쓰기 어려워집니다. **반드시 `HERMES_UID`/`HERMES_GID` 환경변수로 호스트 사용자의 UID/GID를 넘겨주세요.** entrypoint가 `usermod + gosu`로 내부 유저를 재매핑해 줍니다.

```bash
mkdir -p ~/.hermes
docker run -it --rm \
  -e HERMES_UID=$(id -u) \
  -e HERMES_GID=$(id -g) \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent setup
```

> 이미 uid 10000 소유 파일이 만들어졌다면 한 번만 정리하면 됩니다.  
> `sudo chown -R $(id -u):$(id -g) ~/.hermes`

### 1-2. `docker-compose.yml` 작성

`HERMES_UID`/`HERMES_GID` 환경변수를 두 컨테이너에 모두 넘기는 것이 핵심입니다. 같은 디렉토리에 `.env` 파일을 만들어 두면 compose가 자동으로 읽어 들입니다.

```bash
# docker-compose.yml 과 같은 디렉토리에 .env 생성 (compose 전용, ~/.hermes/.env 와 다른 파일)
cat > .env <<EOF
HERMES_UID=$(id -u)
HERMES_GID=$(id -g)
EOF
```

```yaml
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    ports:
      - "8642:8642"
    volumes:
      - ~/.hermes:/opt/data
      - /srv/vault:/data/vault   # Obsidian vault (4장 참조)
    environment:
      - HERMES_UID=${HERMES_UID:-10000}
      - HERMES_GID=${HERMES_GID:-10000}
    networks: [hermes-net]

  dashboard:
    image: nousresearch/hermes-agent:latest
    container_name: hermes-dashboard
    restart: unless-stopped
    command: dashboard --host 0.0.0.0 --insecure
    ports:
      - "9119:9119"
    volumes:
      - ~/.hermes:/opt/data
    environment:
      - GATEWAY_HEALTH_URL=http://hermes:8642
      - HERMES_UID=${HERMES_UID:-10000}
      - HERMES_GID=${HERMES_GID:-10000}
    depends_on: [hermes]
    networks: [hermes-net]

networks:
  hermes-net:
    driver: bridge
```

> `${HERMES_UID:-10000}` 문법은 "환경변수가 비어 있으면 10000으로" 라는 fallback입니다. `.env`에 값을 넣어 두면 자동으로 호스트 UID로 치환됩니다.

### 1-3. 실행 & 접근

```bash
docker compose up -d
docker compose logs -f
```

> `.env` 파일을 안 쓰고 한 번만 임시로 띄우려면 다음처럼 prefix로 넘겨도 됩니다.  
> `HERMES_UID=$(id -u) HERMES_GID=$(id -g) docker compose up -d`

- 게이트웨이 API: `http://<서버IP>:8642`
- 대시보드: `http://<서버IP>:9119`
- 외부 노출 시 Cloudflare Tunnel·Tailscale 같은 보안 터널 권장.

## 2. LLM 설정 — OpenRouter / Anthropic / Claude Code

### 2-1. API 키 방식 (가장 간단)

`~/.hermes/.env`에 사용할 키만 적어 주면 됩니다.

```bash
# ~/.hermes/.env
OPENROUTER_API_KEY=sk-or-...
ANTHROPIC_API_KEY=sk-ant-...
```

### 2-2. 모델 지정
```bash
# 기본 모델 — Anthropic Native
docker compose exec hermes hermes config set model anthropic/claude-sonnet-4-6

# 또는 OpenRouter 경유로 여러 모델 라우팅
docker compose exec hermes hermes config set model openrouter/anthropic/claude-sonnet-4
```

> **추천 조합**: 일상 작업은 OpenRouter(가격·모델 다양성), 중요한 코딩·기획은 Anthropic Native(레이턴시·캐시 효율). `hermes model` 명령으로 대화형 전환도 가능합니다.

### 2-3. Claude Code OAuth로 붙이기 (Claude Max 구독자용)

API 키 대신 **Claude Code의 OAuth 자격증명을 hermes가 그대로 빌려 쓸 수 있습니다.** 이 경로의 장점은 **Claude Max 기본 할당량은 그대로 두고, 미리 충전한 추가 크레딧만** hermes 사용량으로 차감된다는 점이에요. 단, OAuth 흐름은 인터랙티브라 헤드리스 컨테이너에서 직접 못 도니, **호스트에서 한 번 로그인해 둔 자격증명 폴더를 컨테이너에 마운트**합니다.

**1단계 — 호스트에 Claude Code 설치 & 로그인**
```bash
npm install -g @anthropic-ai/claude-code
claude   # 첫 실행 시 브라우저 OAuth → ~/.claude/ 또는 ~/.config/claude/ 에 토큰 저장
```

**2단계 — `docker-compose.yml`에 자격증명 폴더 마운트** (hermes 서비스 `volumes:` 에 추가)
```yaml
    volumes:
      - ~/.hermes:/opt/data
      - /srv/vault:/data/vault
      - ~/.claude:/home/hermes/.claude:ro              # Claude Code 자격증명
      - ~/.config/claude:/home/hermes/.config/claude:ro # 백업 경로 (버전에 따라)
```

**3단계 — provider 지정**
```bash
docker compose up -d
docker compose exec hermes hermes model
# 메뉴에서 Anthropic OAuth (Claude Code) 선택 → 자격증명 자동 감지

# 또는 직접
docker compose exec hermes hermes config set model claude-code/claude-sonnet-4-6
```

> ⚠️ **주의사항**
> - `:ro`(read-only)로 마운트해 컨테이너가 토큰을 망치지 않게 합니다.
> - 토큰 갱신은 호스트 쪽 `claude` CLI가 담당하니, 가끔 호스트에서 `claude --version` 한 번씩 돌려 갱신을 트리거해 주세요.
> - 호스트 UID와 컨테이너 `HERMES_UID`가 같아야 read 권한이 정상입니다(1장 셋업 그대로면 OK).
> - `claude-code`, `claude` 둘 다 `anthropic` provider의 별칭입니다.

## 3. 구글 연동 — Workspace 스킬

### 3-1. GCP 프로젝트 & API 활성화
[Google Cloud Console](https://console.cloud.google.com/)에서:

1. 새 프로젝트 생성
2. **API 사용 설정** — Gmail, Calendar, Drive, Docs, Sheets, People (총 6개)
3. **OAuth 동의 화면** 구성 (외부, 본인 이메일을 테스트 사용자로 추가)
4. **사용자 인증 정보 → OAuth 2.0 클라이언트 ID → 데스크톱 앱**으로 발급, JSON 다운로드

### 3-2. 자격증명 등록 & 인증
다운로드한 JSON을 서버에 올린 뒤:

```bash
cp ~/Downloads/client_secret.json ~/.hermes/google_client_secret.json
docker compose exec hermes hermes
# 프롬프트에 "Set up Google Workspace" 라고 말하면
# 에이전트가 OAuth URL을 띄움 → 브라우저 승인 → 콜백 URL 붙여넣기
```

성공하면 `~/.hermes/google_token.json`에 토큰이 저장되고 이후 자동 갱신됩니다. 이때부터 자연어로 "내일 9시에 미팅 잡고 OOO한테 메일로 알려줘" 같은 요청이 통합니다.

> 메일만 필요하면 별도의 **himalaya 스킬**(앱 비밀번호 기반)이 2분이면 끝나서 더 가볍습니다.

## 4. 옵시디언 연동 — 서버·PC·폰 vault 동기화

### 4-1. 동기화 방식 비교

| 방식 | 비용 | 모바일 | 추천 시나리오 |
|------|------|--------|------|
| **Syncthing** | 무료 | Android (iOS는 우회) | 셀프호스팅 1순위 |
| **Git** | 무료 | iOS/Android 별도 앱 | 변경 이력이 필요할 때 |
| **Obsidian Sync** | 월 $4 | 공식 지원 | 가장 편하게 쓰고 싶을 때 |

### 4-2. 서버에 vault 두기 (Syncthing 기준)
1. PC와 서버 양쪽에 Syncthing 설치
2. PC의 Obsidian vault 폴더(`~/Documents/MyVault`)와 서버 `/srv/vault`를 페어링
3. 안드로이드 Obsidian 앱 → vault 위치를 동일 Syncthing 폴더로 지정

### 4-3. hermes-agent에 vault 경로 알리기
`docker-compose.yml`에 이미 `/srv/vault:/data/vault`를 마운트해 두었으니, `.env`에 한 줄만 추가합니다.

```bash
# ~/.hermes/.env
OBSIDIAN_VAULT_PATH=/data/vault
```

이제 "오늘 회의 메모를 vault에 정리해 줘" 같은 요청에 hermes가 마크다운을 읽고 새로 만들 수 있고, PC·폰 옵시디언 앱에도 곧바로 반영됩니다.

## 5. 안드로이드 폰에 설치 — Termux

### 5-1. Termux 설치
**Google Play 버전은 더 이상 업데이트되지 않습니다.** [F-Droid](https://f-droid.org/packages/com.termux/)에서 최신 Termux를 설치하세요.

### 5-2. 의존성 + 한 줄 설치
```bash
# Termux 안에서
pkg update && pkg upgrade -y
pkg install -y clang rust make pkg-config libffi openssl python nodejs git curl

curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc
hermes --tui
```

설치 스크립트가 Termux를 자동 감지해서 `python -m venv` + `pip install hermes-agent[termux]`로 셋업하고, `$PREFIX/bin`에 `hermes` 심볼릭 링크를 걸어 줍니다. 첫 실행 후 `hermes model`로 모델 선택, `~/.hermes/.env`에 API 키를 넣으면 끝납니다.

> 폰에서는 브라우저 자동화·WhatsApp 등 무거운 스킬은 자동으로 제외됩니다. 메모(Obsidian)·검색·일정 정리 정도가 쾌적합니다.

## 자주 묻는 트러블슈팅

- **포트 충돌**: 8642·9119가 이미 사용 중이면 `ports`를 `"18642:8642"`처럼 호스트 측만 바꿔 주세요.
- **헤드리스 서버 OAuth**: GUI 브라우저가 없는 서버라면 OAuth는 로컬 PC에서 한 번 인증해 `google_token.json`만 서버 `~/.hermes/`로 복사해도 됩니다.
- **컨테이너 중복 기동 금지**: 같은 `~/.hermes` 데이터 디렉토리로 게이트웨이를 둘 이상 띄우지 마세요. 메모리·세션이 깨집니다.

## 마무리

hermes-agent의 진짜 매력은 **세션이 쌓일수록 나를 더 잘 알게 된다**는 점입니다. Docker로 띄워둔 서버 인스턴스 하나만 잘 관리하면 PC·폰 어디서든 같은 메모리·같은 vault·같은 구글 계정에 닿는 개인 에이전트가 됩니다. 처음엔 단순한 비서로 시작하지만, 스킬을 늘려가다 보면 어느 순간 두 번째 두뇌처럼 작동할 거예요.

긴 글 읽어주셔서 감사합니다. 따라 하시다 막히는 부분이 있으면 댓글로 알려주세요. 🙂

## 참고 링크

- [hermes-agent 공식 문서](https://hermes-agent.nousresearch.com/docs)
- [GitHub: NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- [Docker 가이드](https://hermes-agent.nousresearch.com/docs/user-guide/docker)
- [Google Workspace 스킬](https://hermes-agent.nousresearch.com/docs/user-guide/skills/google-workspace)
- [Obsidian 스킬](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/note-taking/note-taking-obsidian)
- [Termux 설치 가이드](https://hermes-agent.nousresearch.com/docs/getting-started/termux)

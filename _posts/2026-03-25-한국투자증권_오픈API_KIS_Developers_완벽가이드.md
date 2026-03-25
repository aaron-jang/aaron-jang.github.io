---
layout: post
title: "한국투자증권 오픈API(KIS Developers) 완벽 가이드 — 국내 유일 REST API로 자동매매 시작하기"
subtitle: "계좌 개설부터 API 키 발급, Python 자동매매, 실시간 시세까지 한 번에 정리"
share-description: "한국투자증권 KIS Developers 오픈API의 가입 절차, 인증 방식, 주요 기능, Python 라이브러리, 증권사 API 비교까지. REST API로 주식 자동매매를 시작하는 완벽 가이드."
date: 2026-03-25T18:00:00+09:00
lastmod: 2026-03-25T18:00:00+09:00
author: 수수
tags: ["한국투자증권", "KIS Developers", "오픈API", "자동매매", "Python", "REST API", "주식API", "시스템트레이딩", "TQQQ", "해외주식"]
categories: ["투자"]
cover-img: /assets/images/kis_developers.jpg
thumbnail-img: /assets/images/kis_developers.jpg
share-img: /assets/images/kis_developers.jpg
---

안녕하세요. 수수입니다.

주식 자동매매를 하려면 증권사 API가 필요합니다. 그런데 국내 대부분의 증권사 API는 **Windows 전용**입니다. 키움증권의 Open API+는 OCX 모듈 기반이고, 대신증권의 CYBOS Plus는 COM 기반 — 맥북이나 리눅스 서버에서는 쓸 수 없습니다.

**한국투자증권 KIS Developers**는 국내에서 유일하게 **순수 REST API**를 제공하는 증권사 플랫폼입니다. 2022년 4월 출시 이후 꾸준히 기능이 확장되어, 지금은 국내주식·해외주식·채권·파생상품까지 API로 거래할 수 있고, 최근에는 **AI(LLM) 연동용 MCP 프로토콜**까지 지원합니다.

오늘은 KIS Developers의 가입부터 인증, 핵심 기능, Python 라이브러리, 그리고 다른 증권사 API와의 비교까지 깔끔하게 정리합니다.

## 목차
{: .no_toc}

* TOC
{:toc}

---

## 30초 핵심 요약

- **국내 유일 REST API**: Windows 종속 없이 macOS·Linux·클라우드 서버에서 개발 가능
- **제공 범위**: 국내주식, 해외주식(미국·일본·홍콩·중국·베트남), 채권, 선물옵션
- **인증 방식**: App Key + App Secret → OAuth Access Token (24시간 유효)
- **실시간 데이터**: WebSocket으로 실시간 체결가·호가·주문체결 통보 수신
- **Python 생태계**: 공식 샘플 + 커뮤니티 라이브러리(python-kis, pykis, mojito2)
- **최신 기능**: 전략 빌더, 백테스터, MCP(AI 연동) 프로토콜 지원

---

## KIS Developers란?

**KIS Developers**는 한국투자증권이 운영하는 오픈API 개발자 플랫폼입니다.

| 항목 | 내용 |
|------|------|
| **출시일** | 2022년 4월 |
| **포털 주소** | [apiportal.koreainvestment.com](https://apiportal.koreainvestment.com){:target="_blank"} |
| **GitHub** | [koreainvestment/open-trading-api](https://github.com/koreainvestment/open-trading-api){:target="_blank"} |
| **API 방식** | REST API + WebSocket |
| **핵심 차별점** | 국내 유일 순수 REST 기반 — OS 제약 없음 |
| **지원 상품** | 국내주식, 해외주식(9개 거래소), 채권, 선물옵션, ELW/ETF/ETN |

기존 증권사 API와 가장 큰 차이는 **HTS 접속이나 별도 프로그램 설치 없이**, HTTP 요청만으로 주식 매매가 가능하다는 점입니다.

---

## API 키 발급 절차 (5단계)

### Step 1: 한국투자증권 계좌 개설

실전투자를 하려면 한국투자증권 **종합 계좌**가 필요합니다. 모의투자만 할 경우 모의투자 전용 계좌를 별도로 신청합니다.

### Step 2: KIS Developers 서비스 신청

한국투자증권 홈페이지 > **서비스신청** > **Open API** > **KIS Developers** > **서비스 신청하기**

### Step 3: 본인 인증

인증서 로그인 + 휴대폰 인증을 진행합니다.

### Step 4: 계좌번호 선택

사용할 계좌번호를 선택하고 신청을 완료합니다.

### Step 5: App Key · App Secret 확인

신청 완료 후 **신청현황 테이블**에서 App Key와 App Secret을 확인할 수 있습니다.

> ⚠️ **보안 주의**: App Key와 App Secret은 계좌 접근 암호키입니다. **절대 타인에게 유출하지 마세요.** GitHub에 하드코딩하는 실수도 금물! 유출 시 즉시 재발급하세요.

---

## 인증 구조 (OAuth 2.0)

KIS API의 인증은 3단계로 구성됩니다.

```
App Key + App Secret
       │
       ▼
POST /oauth2/tokenP  ──→  access_token 발급 (24시간 유효)
       │
       ▼
REST API 호출 시 ──→  Authorization: Bearer {access_token}
       │
POST /oauth2/Approval  ──→  approval_key 발급 (WebSocket 전용)
       │
       ▼
WebSocket 연결 시 ──→  approval_key로 인증
```

| 인증 요소 | 용도 | 유효 기간 |
|----------|------|----------|
| **App Key / App Secret** | 토큰 발급용 자격 증명 | 영구 (재발급 가능) |
| **Access Token** | REST API 호출 인증 | 24시간 (재발급 1분/1회 제한) |
| **Approval Key** | WebSocket 실시간 접속 인증 | 세션 유지 동안 |
| **HashKey** | POST 요청 바디 무결성 검증 | 요청마다 생성 |

---

## REST API vs WebSocket — 언제 뭘 쓸까?

### REST API

**일회성 요청**에 사용합니다. 시세 조회, 주문 실행, 잔고 확인 등.

| 용도 | 메서드 | 예시 |
|------|--------|------|
| 현재가 조회 | GET | 삼성전자 현재가 확인 |
| 일별 시세 | GET | TQQQ 최근 30일 OHLCV |
| 매수/매도 주문 | POST | 삼성전자 10주 시장가 매수 |
| 정정/취소 | POST | 미체결 주문 취소 |
| 잔고 조회 | GET | 보유종목·평가금액·손익률 |

### WebSocket

**실시간 스트리밍**에 사용합니다. 체결가, 호가, 주문 체결 통보 등.

| 용도 | 설명 |
|------|------|
| 실시간 체결 | 종목별 체결 틱 데이터 수신 |
| 실시간 호가 | 10호가 실시간 업데이트 |
| 체결 통보 | 내 주문 체결 시 즉시 알림 |

> **팁**: 단순 조회는 REST, 실시간 모니터링은 WebSocket으로 나눠 설계하면 가장 효율적입니다.

---

## 주요 API 엔드포인트

### 인증

| 엔드포인트 | 메서드 | 용도 |
|-----------|--------|------|
| `/oauth2/tokenP` | POST | 접근토큰 발급 |
| `/oauth2/revokeP` | POST | 접근토큰 폐기 |
| `/oauth2/Approval` | POST | WebSocket 접속키 발급 |
| `/uapi/hashkey` | POST | 해시키 발급 |

### 국내주식

| 엔드포인트 | 메서드 | 용도 |
|-----------|--------|------|
| `.../quotations/inquire-price` | GET | 현재가 조회 |
| `.../quotations/inquire-daily-price` | GET | 일별 시세 (OHLCV) |
| `.../trading/order-cash` | POST | 현금 매수/매도 주문 |
| `.../trading/inquire-balance` | GET | 잔고 조회 |
| `.../trading/inquire-daily-ccld` | GET | 일별 체결내역 |

### 해외주식

| 엔드포인트 | 메서드 | 용도 |
|-----------|--------|------|
| `.../overseas-stock/.../order` | POST | 해외주식 주문 |
| `.../overseas-stock/.../quotations/price` | GET | 해외주식 현재가 |

**Base URL**:
- 실전: `https://openapi.koreainvestment.com:9443`
- 모의: `https://openapivts.koreainvestment.com:29443`

---

## 모의투자 vs 실전투자

처음 시작한다면 **반드시 모의투자부터** 테스트하세요.

| 항목 | 실전투자 | 모의투자 |
|------|---------|---------|
| **도메인** | `openapi.koreainvestment.com:9443` | `openapivts.koreainvestment.com:29443` |
| **코드 설정** | `svr="prod"` | `svr="vps"` |
| **API 호출 제한** | 약 20건/초 | 상대적으로 낮음 |
| **사용 가능 API** | 전체 | 일부 제한 |
| **계좌** | 기존 종합 계좌 | 별도 모의투자 계좌 |
| **거래 결과** | 실제 체결 · 실제 자산 변동 | 가상 체결 · 자산 변동 없음 |

> 코드에서 도메인과 `svr` 값만 바꾸면 모의 ↔ 실전 전환이 가능합니다.

---

## API 호출 제한 (Rate Limit)

| 항목 | 제한 |
|------|------|
| **초당 호출 수** | 약 20건/초 (실전 기준) |
| **제한 방식** | 슬라이딩 윈도우(Sliding Window) |
| **초과 시 에러** | `EGW00201` 반환 |
| **토큰 재발급** | 1분에 1회 제한 |
| **권장 설정** | 보수적으로 **15건/초** 이하 |

> **팁**: 슬라이딩 윈도우 경계에서 요청이 몰리면 제한에 걸릴 수 있습니다. `time.sleep(0.07)` 등으로 요청 간격을 두는 것이 안전합니다.

---

## Python 개발 환경

### 공식 샘플 코드

한국투자증권은 [공식 GitHub](https://github.com/koreainvestment/open-trading-api){:target="_blank"}에서 Python 샘플을 제공합니다.

| 디렉토리 | 내용 |
|----------|------|
| `examples_llm/` | LLM 연동용 단일 API 샘플 (함수 단위 분리) |
| `examples_user/` | 통합 실전 예제 |
| `strategy_builder/` | 시각적 매매 전략 설계 UI (80+ 기술 지표) |
| `backtester/` | QuantConnect Lean 기반 백테스팅 |
| `MCP/` | Claude·ChatGPT 등 AI 연동 MCP 프로토콜 |

**10가지 프리셋 전략** 포함: 골든크로스, 모멘텀, 52주 신고가, 평균회귀 등

### 커뮤니티 라이브러리

| 라이브러리 | Python | 특징 |
|-----------|--------|------|
| **[python-kis](https://github.com/Soju06/python-kis){:target="_blank"}** | 3.11+ | 완전한 타입 힌트, 자동 WebSocket 재연결, 가장 활발한 유지보수 |
| **[pykis](https://github.com/pjueon/pykis){:target="_blank"}** | 3.7+ | 국내외 주식 매매, 9개 해외 거래소 지원 |
| **[mojito2](https://pypi.org/project/mojito2/){:target="_blank"}** | 3.6+ | 경량 래퍼, 빠른 시작에 적합 |

> **추천**: 본격적인 자동매매 시스템을 만든다면 **python-kis**(Soju06)가 타입 안전성과 WebSocket 자동 복구 면에서 가장 안정적입니다.

---

## 실전 코드 예제: 현재가 조회

```python
import requests

# 설정
BASE_URL = "https://openapi.koreainvestment.com:9443"
APP_KEY = "your_app_key"
APP_SECRET = "your_app_secret"
ACCESS_TOKEN = "your_access_token"

# 삼성전자(005930) 현재가 조회
headers = {
    "content-type": "application/json; charset=utf-8",
    "authorization": f"Bearer {ACCESS_TOKEN}",
    "appkey": APP_KEY,
    "appsecret": APP_SECRET,
    "tr_id": "FHKST01010100",  # 국내주식 현재가 조회
}

params = {
    "FID_COND_MRKT_DIV_CODE": "J",   # 주식
    "FID_INPUT_ISCD": "005930",       # 삼성전자
}

res = requests.get(
    f"{BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-price",
    headers=headers,
    params=params,
)

data = res.json()
price = data["output"]["stck_prpr"]  # 현재가
print(f"삼성전자 현재가: {price}원")
```

---

## 실전 코드 예제: 주식 매수 주문

```python
# 삼성전자 10주 시장가 매수
headers = {
    "content-type": "application/json; charset=utf-8",
    "authorization": f"Bearer {ACCESS_TOKEN}",
    "appkey": APP_KEY,
    "appsecret": APP_SECRET,
    "tr_id": "TTTC0802U",  # 국내주식 매수 주문
    "hashkey": "your_hashkey",
}

body = {
    "CANO": "12345678",          # 계좌번호 앞 8자리
    "ACNT_PRDT_CD": "01",        # 계좌상품코드
    "PDNO": "005930",            # 종목코드 (삼성전자)
    "ORD_DVSN": "01",            # 주문구분 (01: 시장가)
    "ORD_QTY": "10",             # 주문수량
    "ORD_UNPR": "0",             # 주문단가 (시장가는 0)
}

res = requests.post(
    f"{BASE_URL}/uapi/domestic-stock/v1/trading/order-cash",
    headers=headers,
    json=body,
)

result = res.json()
print(f"주문 결과: {result['msg1']}")
```

---

## 국내 증권사 API 비교

| 증권사 | API | 방식 | 플랫폼 | 특징 |
|--------|-----|------|--------|------|
| **한국투자증권** | KIS Developers | REST + WebSocket | **크로스플랫폼** | 국내 유일 REST, Linux/Mac 개발 가능 |
| **키움증권** | Open API+ | OCX 모듈 | Windows 전용 | 자료·커뮤니티 풍부, 개인투자자 인기 |
| **대신증권** | CYBOS Plus | COM 기반 | Windows 전용 | Python/C#/C++ 지원 |
| **이베스트** | XingAPI | COM/DLL + REST | Windows (REST는 크로스) | REST 옵션 일부 제공 |
| **유진투자증권** | Champion | OCX/DLL | Windows 전용 | — |
| **유안타증권** | T-Trader | DLL/COM | Windows | Android API 제공 |
| **NH투자증권** | QV Open API | DLL | Windows 전용 | 문서 제한적 |

### 한국투자증권 API를 선택해야 하는 이유

1. **OS 자유**: macOS에서 개발하고 Linux 서버에 배포 가능
2. **클라우드 친화**: AWS·GCP·Azure 서버에서 바로 실행
3. **REST 표준**: HTTP 요청만 할 줄 알면 어떤 언어든 사용 가능
4. **해외주식 지원**: 미국(NYSE·NASDAQ·AMEX), 일본, 홍콩, 중국, 베트남 등 9개 거래소
5. **AI 연동**: MCP 프로토콜로 Claude·ChatGPT와 연동 가능

---

## 주요 활용 사례

### 1. 자동매매 시스템

가장 대표적인 활용입니다. 매매 조건을 프로그래밍하여 자동으로 주문을 실행합니다.

- **골든크로스 전략**: 5일선이 20일선을 돌파하면 매수
- **모멘텀 전략**: 최근 N일 수익률 상위 종목 교체 매수
- **무한매수법 자동화**: 라오어의 무한매수법을 API로 자동 실행

### 2. 실시간 모니터링 대시보드

WebSocket으로 실시간 체결가·호가를 수신하여 **나만의 HTS**를 만들 수 있습니다.

### 3. 포트폴리오 관리

잔고 조회 API로 보유종목·평가금액·손익률을 실시간으로 모니터링하고, 텔레그램이나 슬랙으로 알림을 보낼 수 있습니다.

### 4. 백테스팅 + 실전 배포

공식 `strategy_builder`로 전략을 설계하고, `backtester`(QuantConnect Lean)로 과거 데이터 검증 후, 검증된 전략을 실전 API에 연결하는 파이프라인을 구축할 수 있습니다.

### 5. AI 보조 매매

MCP 프로토콜을 통해 **Claude나 ChatGPT**에게 "삼성전자 현재가 알려줘", "TQQQ 10주 매수해줘" 같은 자연어 명령으로 매매를 요청할 수 있습니다.

---

## 시작하기 전 체크리스트

- [ ] 한국투자증권 계좌 개설 완료
- [ ] KIS Developers 서비스 신청 완료
- [ ] App Key · App Secret 발급 확인
- [ ] Python 3.11+ 환경 준비
- [ ] **모의투자 계좌로 충분히 테스트** 후 실전 전환
- [ ] App Key · App Secret **환경변수 또는 별도 설정파일**로 관리 (하드코딩 금지)
- [ ] API 호출 간격 설정 (0.07초 이상 권장)

---

## 2025~2026년 최신 업데이트

| 시기 | 내용 |
|------|------|
| **2025년 12월** | TLS 1.0/1.1 지원 종료 — TLS 1.2 이상 필수 |
| **2025~2026년** | `strategy_builder` 추가 — 시각적 UI로 매매 전략 설계 (80+ 기술 지표) |
| **2025~2026년** | `backtester` 추가 — QuantConnect Lean 기반 과거 데이터 검증 |
| **2025~2026년** | **MCP 프로토콜** 지원 — Claude·ChatGPT 등 LLM과 직접 연동 |
| **2025~2026년** | `examples_llm/` — AI 자동화 친화적 함수 단위 샘플 코드 제공 |

---

## 마치며

한국투자증권 KIS Developers는 **국내에서 유일하게 OS 제약 없이 사용할 수 있는 증권사 API**입니다. REST API 표준을 따르기 때문에 Python뿐 아니라 JavaScript, Go, Rust 등 어떤 언어로든 개발할 수 있고, 클라우드 서버에 배포하기도 쉽습니다.

특히 최근 추가된 **전략 빌더·백테스터·MCP 프로토콜**은 "코드를 짜서 자동매매를 하고 싶은데, 어디서부터 시작해야 할지 모르겠다"는 분들에게 좋은 출발점이 됩니다.

다만 API를 사용한 자동매매는 **버그 한 줄이 실제 손실**로 이어질 수 있습니다. 반드시 모의투자에서 충분히 테스트하고, 주문 로직에는 안전장치(최대 주문 금액 제한, 비정상 체결 알림 등)를 넣어두세요.

> **투자에 대한 최종 판단과 책임은 투자자 본인에게 있습니다. 이 글은 정보 제공 목적이며 특정 투자를 권유하지 않습니다.**

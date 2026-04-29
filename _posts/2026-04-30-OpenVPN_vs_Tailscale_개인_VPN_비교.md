---
layout: post
title: "OpenVPN vs Tailscale — 개인 VPN, 뭘 써야 할까?"
subtitle: "직접 구축하는 OpenVPN과 제로 설정 Tailscale, 목적별 완벽 비교"
share-description: "OpenVPN과 Tailscale의 구조, 설치, 보안, 속도, 비용을 비교합니다. 홈서버 접속, 원격 근무, NAS 연결 등 목적별로 어떤 VPN이 맞는지 정리합니다."
date: 2026-04-30T10:00:00+09:00
lastmod: 2026-04-30T10:00:00+09:00
author: 수수
tags: ["VPN", "OpenVPN", "Tailscale", "WireGuard", "홈서버", "네트워크", "보안", "셀프호스팅"]
categories: ["IT"]
---

안녕하세요. 수수입니다.

집에 NAS나 홈서버를 운영하거나, 외부에서 집 네트워크에 안전하게 접속하고 싶을 때 **개인 VPN**이 필요합니다. 상용 VPN(NordVPN, ExpressVPN 등)과는 다릅니다 — 내 장비끼리 안전하게 연결하는 게 목적이니까요.

이 분야의 양대 산맥이 바로 **OpenVPN**과 **Tailscale**입니다. 둘 다 써본 입장에서, 어떤 상황에 뭘 골라야 하는지 정리합니다.

---

* TOC
{:toc}

---

## 30초 요약 — 바쁜 분을 위해

| 항목 | OpenVPN | Tailscale |
|------|---------|-----------|
| **구조** | 클라이언트-서버 (중앙 서버 필요) | P2P 메시 네트워크 |
| **기반 프로토콜** | OpenVPN (자체) | WireGuard |
| **설치 난이도** | 높음 (서버 구축 필요) | 매우 낮음 (로그인만) |
| **속도** | 보통 | 빠름 (P2P 직접 연결) |
| **포트 포워딩** | 필요 | 불필요 |
| **무료 범위** | 완전 무료 (오픈소스) | 100대까지 무료 |
| **적합한 사람** | 네트워크를 완전히 제어하고 싶은 사람 | 빠르고 쉽게 연결하고 싶은 사람 |

**한 줄 정리**: 설정 자유도가 중요하면 OpenVPN, 편의성이 중요하면 Tailscale.

---

## 1. 구조부터 다르다

### OpenVPN — 전통적인 클라이언트-서버

```
[외부 기기] → 인터넷 → [OpenVPN 서버 (집/클라우드)] → [내부 네트워크]
```

- **중앙 서버**가 반드시 필요합니다. 집에 있는 리눅스 서버, NAS, 또는 클라우드 VPS에 설치합니다.
- 모든 트래픽이 서버를 경유합니다.
- **포트 포워딩**(보통 UDP 1194)을 공유기에서 열어야 합니다.
- 인증서(CA, 서버, 클라이언트)를 직접 생성·관리해야 합니다.

### Tailscale — P2P 메시 네트워크

```
[기기 A] ←── WireGuard 터널 ──→ [기기 B]
                  ↑
          [Tailscale 조정 서버]
          (연결 중개만, 데이터 안 지나감)
```

- **서버가 필요 없습니다**. 각 기기에 Tailscale 앱만 설치하면 됩니다.
- 기기끼리 **직접 연결**(P2P)을 시도하고, 안 되면 릴레이(DERP) 서버를 사용합니다.
- Tailscale의 조정 서버는 **연결을 중개**할 뿐, 실제 데이터는 지나가지 않습니다.
- 내부적으로 **WireGuard** 프로토콜을 사용합니다.

---

## 2. 설치 비교

### OpenVPN 설치 (우분투 기준)

직접 하면 꽤 복잡합니다. 다행히 자동 설치 스크립트가 있습니다.

```bash
# 자동 설치 스크립트 (Nyr의 openvpn-install)
curl -O https://raw.githubusercontent.com/Nyr/openvpn-install/master/openvpn-install.sh
chmod +x openvpn-install.sh
sudo ./openvpn-install.sh
```

그래도 해야 할 것들이 있습니다:
1. 서버에 고정 IP 또는 DDNS 설정
2. 공유기에서 포트 포워딩 설정
3. 클라이언트용 `.ovpn` 설정 파일 생성·배포
4. 방화벽(UFW/iptables) 규칙 추가
5. 인증서 만료 시 갱신

### Tailscale 설치

```bash
# 리눅스
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# macOS
brew install tailscale

# 또는 앱스토어에서 Tailscale 다운로드
```

끝입니다. 로그인하면 **100.x.x.x** 대역의 IP가 할당되고, 같은 계정의 기기끼리 바로 연결됩니다.

- 포트 포워딩? **필요 없습니다.**
- 인증서 관리? **필요 없습니다.**
- 방화벽 설정? **필요 없습니다.**

---

## 3. 공인 IP 없이도 되나? — CGNAT / 내부 IP 환경

아파트 인터넷, LTE/5G 테더링, 일부 저가 인터넷은 **공인 IP가 아닌 내부 IP**만 할당됩니다. 이걸 **CGNAT**(Carrier-Grade NAT)이라고 합니다.

내 IP가 `100.x.x.x`, `10.x.x.x`, `172.16~31.x.x` 대역이면 CGNAT일 가능성이 높습니다.

```bash
# 내 공인 IP 확인
curl ifconfig.me

# 공유기에 할당된 WAN IP 확인 → 위 결과와 다르면 CGNAT
```

### OpenVPN — 공인 IP 없으면 사실상 불가

| 환경 | 가능 여부 | 설명 |
|------|----------|------|
| 공인 IP + 포트포워딩 | **가능** | 정석적인 구성 |
| CGNAT (내부 IP만) | **불가** | 외부에서 서버로 접속할 방법이 없음 |
| 이중 NAT (공유기 2개) | **어려움** | 두 공유기 모두 포트포워딩 필요 |
| 클라우드 VPS 우회 | **가능** | VPS에 OpenVPN 서버를 두면 해결 |

OpenVPN 서버는 **외부에서 접속 가능한 IP와 열린 포트**가 필수입니다. CGNAT 환경에서는 포트 포워딩 자체가 불가능하므로, 별도 클라우드 VPS를 빌리거나 ISP에 공인 IP를 요청해야 합니다.

### Tailscale — 공인 IP 없어도 동작

| 환경 | 가능 여부 | 설명 |
|------|----------|------|
| 공인 IP | **가능** | P2P 직접 연결 |
| CGNAT (내부 IP만) | **가능** | NAT traversal 자동 처리 |
| 이중 NAT (공유기 2개) | **가능** | 알아서 뚫음 |
| 양쪽 다 CGNAT | **가능** | 최악의 경우 DERP 릴레이 사용 |

Tailscale이 CGNAT에서도 되는 이유:

1. **NAT traversal**: STUN/ICE 프로토콜로 NAT 뒤에 있는 기기끼리 직접 연결을 시도합니다.
2. **UDP hole punching**: 양쪽이 동시에 패킷을 보내 NAT 테이블에 구멍을 뚫습니다.
3. **DERP 릴레이 서버**: 직접 연결이 정말 안 되면, Tailscale이 운영하는 릴레이 서버를 통해 우회합니다. 속도는 약간 느려지지만 **항상 연결은 됩니다**.

```bash
# 현재 연결 상태 확인 — direct(직접) vs relay(릴레이)
tailscale status
tailscale ping my-nas
```

### 현실적인 상황 정리

```
                       OpenVPN    Tailscale
SK/KT/LG 가정용 인터넷     O          O
(공인 IP, 포트포워딩 가능)

아파트 단체 인터넷           X          O
(CGNAT, 포트포워딩 불가)

LTE/5G 테더링              X          O
(CGNAT)

해외 호텔/카페 와이파이       X          O
(NAT 뒤)
```

**이 차이가 Tailscale을 선택하는 가장 큰 이유 중 하나입니다.** 공유기 설정을 건드릴 수 없는 환경이라면 OpenVPN은 선택지에서 빠집니다.

---

## 4. 속도 비교

| 항목 | OpenVPN | Tailscale |
|------|---------|-----------|
| **프로토콜** | OpenVPN (TLS 기반) | WireGuard (커널 레벨) |
| **암호화 오버헤드** | 큼 | 작음 |
| **연결 방식** | 서버 경유 | P2P 직접 연결 |
| **핸드셰이크** | 느림 (TLS) | 빠름 (1-RTT) |
| **일반적인 속도 저하** | 20~40% | 5~15% |

**Tailscale이 빠릅니다.** 이유는 명확합니다:

1. **WireGuard**는 커널에서 동작해서 오버헤드가 적습니다. OpenVPN은 유저 스페이스에서 동작합니다.
2. **P2P 직접 연결**이므로 중앙 서버를 거치지 않습니다. 같은 카페에 있는 두 기기는 인터넷도 안 거칩니다.
3. WireGuard의 코드베이스는 약 **4,000줄**입니다. OpenVPN은 수십만 줄입니다. 간결할수록 빠릅니다.

---

## 5. 보안 비교

### OpenVPN

- **20년 이상** 검증된 프로토콜
- OpenSSL 기반 TLS 1.3 암호화
- 인증서 기반 상호 인증 (PKI)
- 완전한 오픈소스
- **모든 것을 직접 제어** — 암호화 알고리즘, 키 길이, 인증 방식 등

### Tailscale

- WireGuard 기반 — 현대적이고 간결한 암호화
- ChaCha20 + Poly1305 + Curve25519
- **SSO 연동** (Google, Microsoft, GitHub 등)
- ACL(접근 제어 목록)로 기기 간 접근 권한 세분화
- 클라이언트는 오픈소스, **조정 서버는 비공개**

### 보안 관점에서의 핵심 차이

```
OpenVPN:  내가 모든 걸 제어한다 → 내 실수도 내 책임
Tailscale: Tailscale이 관리한다 → Tailscale을 신뢰해야 한다
```

Tailscale의 조정 서버가 비공개라는 점이 불안하다면, **Headscale**이라는 오픈소스 대안이 있습니다. Tailscale 프로토콜을 사용하면서 조정 서버를 직접 운영할 수 있습니다.

```bash
# Headscale — 셀프호스팅 Tailscale 조정 서버
# https://github.com/juanfont/headscale
docker run -d --name headscale \
  -v /etc/headscale:/etc/headscale \
  -p 8080:8080 \
  headscale/headscale:latest serve
```

---

## 6. 비용 비교

### OpenVPN

| 항목 | 비용 |
|------|------|
| 소프트웨어 | **무료** (오픈소스) |
| 서버 (집) | 전기세만 |
| 서버 (클라우드 VPS) | 월 $3~10 |
| 도메인/DDNS | 무료~연 $10 |
| **총합** | **무료 ~ 월 $10** |

### Tailscale

| 플랜 | 가격 | 기기 수 | 사용자 수 |
|------|------|---------|----------|
| **Personal** | 무료 | 100대 | 3명 |
| **Personal Plus** | 월 $6 | 무제한 | 6명 |
| **Starter** | 사용자당 월 $6 | 무제한 | 무제한 |

개인 사용이라면 **무료 플랜**으로 충분합니다. 100대면 웬만한 홈랩은 다 커버합니다.

---

## 7. 기능 비교 심화

### Exit Node (출구 노드)

외부 인터넷 트래픽을 특정 기기를 통해 내보내는 기능입니다. 해외에서 한국 IP로 접속할 때 유용합니다.

| | OpenVPN | Tailscale |
|---|---------|-----------|
| 지원 여부 | 기본 지원 | 지원 (별도 설정) |
| 설정 난이도 | 서버 설정에 `push "redirect-gateway"` 추가 | `tailscale up --advertise-exit-node` |

### Subnet Router (서브넷 라우팅)

VPN에 연결된 기기뿐만 아니라, 그 기기가 속한 **내부 네트워크 전체**에 접근하는 기능입니다.

| | OpenVPN | Tailscale |
|---|---------|-----------|
| 지원 여부 | 기본 지원 | 지원 (Subnet Router) |
| 설정 | 서버에서 라우팅 설정 | `tailscale up --advertise-routes=192.168.1.0/24` |

### MagicDNS vs 수동 DNS

| | OpenVPN | Tailscale |
|---|---------|-----------|
| 기기 이름으로 접속 | Pi-hole/AdGuard 등 별도 설정 | **MagicDNS** 자동 지원 |
| 예시 | `ssh 10.8.0.5` | `ssh my-nas` |

Tailscale의 MagicDNS는 정말 편리합니다. `my-nas.tailnet-name.ts.net` 같은 도메인이 자동 생성됩니다.

### Taildrop (파일 전송)

Tailscale만의 기능입니다. AirDrop처럼 기기 간 파일을 직접 전송합니다.

```bash
# 파일 보내기
tailscale file cp ./report.pdf my-desktop:

# 파일 받기
tailscale file get ./downloads/
```

OpenVPN에는 이런 기능이 없습니다. SCP, rsync 등을 별도로 사용해야 합니다.

---

## 8. 시놀로지 NAS에 설치하기 (ARM CPU 포함)

홈 네트워크에서 VPN을 쓰는 가장 흔한 이유가 **외부에서 NAS 접속**입니다. 시놀로지 NAS에서 두 VPN 모두 설치할 수 있는지, 특히 저가형 ARM 모델에서도 되는지 정리합니다.

### 내 NAS가 ARM인지 확인하기

시놀로지 저가형 J 시리즈는 대부분 ARM CPU입니다.

| 모델 | CPU | 아키텍처 |
|------|-----|----------|
| DS120j | Marvell A3720 | ARMv8 (arm64) |
| DS220j | Realtek RTD1296 | ARMv8 (arm64) |
| DS223j | Realtek RTD1619B | ARMv8 (arm64) |
| DS220+ / DS720+ | Intel Celeron | x86_64 |
| DS920+ / DS1621+ | Intel Celeron / AMD Ryzen | x86_64 |

DSM에서 **제어판 → 정보 센터**에서 CPU 모델을 확인할 수 있습니다.

### Tailscale 설치 — ARM도 공식 지원

시놀로지 패키지 센터에서 바로 설치할 수 있습니다.

**방법 1: 패키지 센터 (가장 쉬움)**

1. DSM 웹 관리자 → **패키지 센터** 열기
2. "Tailscale" 검색 → **설치**
3. 설치 후 Tailscale 앱 실행 → 브라우저에서 **로그인**
4. 끝. NAS에 `100.x.x.x` IP가 할당됨

**방법 2: SPK 수동 설치 (최신 버전이 필요할 때)**

패키지 센터 버전이 오래된 경우, [pkgs.tailscale.com/stable](https://pkgs.tailscale.com/stable/)에서 직접 다운로드합니다.

```
# ARM NAS라면 이 파일을 다운로드
tailscale-armv8-x.xx.x-xxxxxxxx-dsm7.spk

# Intel NAS라면
tailscale-x86_64-x.xx.x-xxxxxxxx-dsm7.spk
```

DSM → 패키지 센터 → **수동 설치** → SPK 파일 업로드 → 완료.

**DSM 7 주의사항**

DSM 7에서는 보안 정책이 강화되어 몇 가지 제약이 있습니다:

- Tailscale 패키지가 **TUN 디바이스 생성 권한이 제한**됩니다
- 기본적으로 **인바운드 연결만** 허용 (외부에서 NAS로 접속하는 건 됨)
- **Subnet Router**나 **Exit Node**를 쓰려면 SSH 접속 후 추가 설정 필요:

```bash
# SSH로 NAS 접속 후
sudo tailscale up --advertise-routes=192.168.1.0/24 --advertise-exit-node
```

### OpenVPN 설치 — 내장 VPN Server 패키지

시놀로지는 자체적으로 **VPN Server** 패키지를 제공합니다. ARM 모델도 지원합니다.

**설치 방법:**

1. DSM → **패키지 센터** → "VPN Server" 검색 → **설치**
2. VPN Server 앱 실행 → 좌측 메뉴에서 **OpenVPN** 선택
3. **OpenVPN 서버 활성화** 토글 켜기
4. 설정:
   - 포트: UDP 1194 (기본값)
   - 서브넷: 10.8.0.0/24
   - 최대 접속 수: 10
5. **내보내기**를 눌러 `.ovpn` 설정 파일 다운로드
6. 클라이언트 기기에서 `.ovpn` 파일 임포트

**공유기 추가 설정 필수:**

```
공유기 관리자 페이지 → 포트 포워딩 설정
외부 포트: 1194 (UDP)  →  내부 IP: NAS IP  →  내부 포트: 1194 (UDP)
```

### ARM NAS에서의 성능 차이

ARM CPU는 암호화 연산 성능이 제한적입니다. 여기서 **프로토콜 차이가 크게 벌어집니다.**

| 항목 | OpenVPN (ARM) | Tailscale (ARM) |
|------|--------------|-----------------|
| **예상 속도** | 5~15 Mbps | 30~80 Mbps |
| **CPU 사용률** | 높음 (유저스페이스 암호화) | 낮음 (WireGuard 커널 레벨) |
| **파일 전송** | 느림 | 실용적 |
| **영상 스트리밍** | 버퍼링 가능 | 원활 |

WireGuard는 OpenVPN 대비 **암호화 오버헤드가 훨씬 적어서**, CPU가 약한 ARM NAS에서 차이가 더 극적으로 벌어집니다. DS220j 같은 저가형 NAS에서 OpenVPN으로 영상을 스트리밍하면 버퍼링이 걸릴 수 있지만, Tailscale은 대체로 원활합니다.

### 시놀로지 NAS 요약

| 판단 기준 | OpenVPN | Tailscale |
|----------|---------|-----------|
| ARM NAS 지원 | O | O |
| 설치 난이도 | 쉬움 (패키지 센터) | 쉬움 (패키지 센터) |
| 포트 포워딩 | **필요** | **불필요** |
| ARM 속도 | 느림 (5~15Mbps) | 빠름 (30~80Mbps) |
| 공유기 설정 | 필요 | 불필요 |
| CGNAT 환경 | 불가 | 가능 |

**ARM NAS 사용자라면 Tailscale을 강력 추천합니다.** 설치도 쉽고, ARM CPU에서의 성능도 압도적이며, 포트 포워딩 없이 바로 외부 접속이 가능합니다.

---

## 9. 실전 시나리오별 추천

### 시나리오 1: 외부에서 집 NAS 접속

**추천: Tailscale**

- NAS에 Tailscale 패키지 설치 (Synology, QNAP 공식 지원)
- 스마트폰에 Tailscale 앱 설치
- 끝. 어디서든 NAS에 접속 가능

### 시나리오 2: 해외에서 한국 넷플릭스 시청

**추천: OpenVPN (또는 Tailscale Exit Node)**

- 집에 OpenVPN 서버를 두고, 모든 트래픽을 집으로 라우팅
- Tailscale도 Exit Node로 가능하지만, OpenVPN이 이 용도에 더 성숙

### 시나리오 3: 여러 거점 연결 (집 + 사무실 + 클라우드)

**추천: Tailscale**

- 각 거점에 Tailscale만 설치하면 메시 네트워크 자동 구성
- ACL로 접근 권한 세분화 가능
- OpenVPN으로 하려면 사이트 간 VPN 설정이 복잡

### 시나리오 4: 보안이 최우선 (기업/민감 데이터)

**추천: OpenVPN 또는 Headscale**

- 제3자 서비스에 의존하지 않는 완전한 자체 운영
- 모든 트래픽 경로를 직접 제어
- Tailscale을 쓰되 Headscale로 조정 서버를 자체 운영하는 것도 방법

### 시나리오 5: 게임 서버/개발 서버 공유

**추천: Tailscale**

- 친구에게 Tailscale 초대만 보내면 끝
- 포트 포워딩 없이 내 PC의 마인크래프트 서버에 친구가 접속 가능
- Funnel 기능으로 Tailscale 없는 사람에게도 서비스 노출 가능

---

## 10. 둘 다 쓰는 하이브리드 구성

사실 **둘 다 같이 쓸 수 있습니다**. 제가 쓰는 구성입니다:

```
[일상 접속] → Tailscale (간편하게 NAS, 홈서버 접속)
[전체 트래픽 라우팅] → OpenVPN (해외 출장 시 한국 IP 필요할 때)
```

- Tailscale은 **항상 켜두고** 기기 간 연결에 사용
- OpenVPN은 **필요할 때만** 전체 트래픽을 집으로 보내는 용도

---

## 11. 마이그레이션 가이드 — OpenVPN에서 Tailscale로

기존에 OpenVPN을 쓰고 있다면, 병행하면서 천천히 전환할 수 있습니다.

### Step 1: Tailscale 설치

기존 OpenVPN 서버에 Tailscale을 **함께** 설치합니다. 충돌하지 않습니다.

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --advertise-routes=192.168.1.0/24
```

### Step 2: 클라이언트 전환

기기 하나씩 Tailscale로 전환합니다. 문제가 생기면 OpenVPN으로 돌아가면 됩니다.

### Step 3: OpenVPN 서버 종료

모든 기기가 Tailscale로 전환되면, OpenVPN 서버를 내립니다.

---

## 최종 정리

| 이런 사람이라면 | 이걸 쓰세요 |
|----------------|------------|
| 네트워크 지식이 있고, 모든 걸 직접 제어하고 싶다 | **OpenVPN** |
| 빠르게 설정하고 바로 쓰고 싶다 | **Tailscale** |
| 리눅스 서버 운영이 익숙하다 | **OpenVPN** |
| 가족/친구와 쉽게 공유하고 싶다 | **Tailscale** |
| 제3자 서비스를 신뢰하지 않는다 | **OpenVPN** 또는 **Headscale** |
| 여러 기기를 메시로 연결하고 싶다 | **Tailscale** |
| 상용 VPN 대체 (IP 우회) 용도다 | **OpenVPN** |

개인적으로는 **Tailscale을 먼저 써보시길 추천합니다**. 5분 만에 설치 끝나고, 무료 플랜으로 충분합니다. 그러다 더 세밀한 제어가 필요해지면 OpenVPN이나 Headscale을 고려하면 됩니다.

---

**참고 링크**
- [OpenVPN 공식 문서](https://openvpn.net/community-resources/)
- [Tailscale 공식 문서](https://tailscale.com/kb/)
- [WireGuard 공식 사이트](https://www.wireguard.com/)
- [Headscale GitHub](https://github.com/juanfont/headscale)
- [Nyr의 OpenVPN 자동 설치 스크립트](https://github.com/Nyr/openvpn-install)

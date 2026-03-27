---
layout: post
title: "CompTIA A+ / Network+ / Security+ 완벽 가이드"
subtitle: "시험 구성·도메인별 비중·공부법·추천 교재까지 — 3대 핵심 자격증 한 번에 정리"
share-description: "CompTIA A+, Network+, Security+ 시험의 도메인별 비중, 합격 점수, 추천 공부 순서, 무료·유료 교재, 합격 전략을 한 글로 정리했습니다. IT 자격증 시리즈 2편."
date: 2026-03-20T09:30:00+09:00
lastmod: 2026-03-20T11:14:20+09:00
author: 수수
tags: ["CompTIA", "A+", "Network+", "Security+", "IT자격증", "IT취업", "사이버보안", "공부법", "자격증시험", "커리어"]
categories: ["테크"]
cover-img: /assets/images/comptia_roadmap.webp
thumbnail-img: /assets/images/comptia_roadmap.thumb.webp
share-img: /assets/images/comptia_roadmap.png
---

안녕하세요. 수수입니다.

[CompTIA 자격증 로드맵 (시리즈 1편)]({% post_url 2026-03-20-CompTIA_자격증_로드맵_IT_커리어_시작하기 %})에서 전체 그림을 잡았다면, 이제 가장 많이 따는 **3대 핵심 자격증 — A+, Network+, Security+** 를 자세히 파헤쳐 보겠습니다.

각 시험의 도메인별 비중, 난이도, 공부 전략, 추천 교재·강의를 한 글에 정리했습니다.

---

## 목차
{: .no_toc}

* TOC
{:toc}

---

## 30초 핵심 요약

| 항목 | A+ | Network+ | Security+ |
|------|-----|----------|-----------|
| 시험 코드 | 220-1201 / 220-1202 | N10-009 | SY0-701 |
| 시험 수 | 2개 (Core 1 + Core 2) | 1개 | 1개 |
| 문항 | 최대 90문제 × 2 | 최대 90문제 | 최대 90문제 |
| 시간 | 90분 × 2 | 90분 | 90분 |
| 합격 점수 | 675 / 700 (900점 만점) | 720 (900점 만점) | 750 (900점 만점) |
| 비용 | $530 (2과목) | $369 | $425 |
| 추천 공부 기간 | 2~3개월 | 1~2개월 | 1.5~2개월 |
| 선수 지식 | 없음 | A+ 수준 권장 | Network+ 수준 권장 |

---

## CompTIA A+ — IT 커리어의 출발점

### 이 자격증은 누구를 위한 건가?

- IT 비전공자가 **첫 IT 직무**를 얻고 싶을 때
- 헬프데스크·IT 지원·기술 지원 엔지니어를 목표로 할 때
- IT 기본기를 체계적으로 정리하고 싶을 때

> 💡 A+는 **2개의 시험**을 모두 통과해야 자격증이 발급됩니다

---

### Core 1 (220-1201) — 하드웨어·네트워크

**"이 컴퓨터가 왜 안 되지?"를 해결하는 기술**

| 도메인 | 비중 | 핵심 내용 |
|--------|------|-----------|
| 하드웨어·장치 | 25% | CPU, RAM, 스토리지, 주변기기, 모바일 기기 |
| 네트워킹 | 23% | TCP/IP, DNS, DHCP, Wi-Fi, 네트워크 장비 |
| 문제 해결 | 29% | 하드웨어·네트워크·모바일 문제 진단 |
| 클라우드·가상화 | 12% | 클라우드 개념, 가상 머신, 컨테이너 |
| 직무 절차 | 11% | 안전 절차, 변경 관리, 문서화 |

**가장 비중 높은 도메인**: 문제 해결(29%) — 실제 IT 지원 현장에서 가장 많이 하는 일입니다.

---

### Core 2 (220-1202) — OS·보안·소프트웨어

**"이 프로그램이 왜 안 되지?"를 해결하는 기술**

| 도메인 | 비중 | 핵심 내용 |
|--------|------|-----------|
| 운영체제 | 28% | Windows, macOS, Linux 설치·설정·관리 |
| 보안 | 28% | 멀웨어, 사회공학, 접근 제어, 보안 설정 |
| 소프트웨어 문제 해결 | 23% | OS·앱 문제 진단, 명령줄 도구 |
| 직무 절차 | 21% | 백업, 재해 복구, 스크립팅 기초 |

**가장 비중 높은 도메인**: 운영체제(28%)와 보안(28%)이 동률 — Core 2는 소프트웨어와 보안에 집중합니다.

---

### A+ 공부 전략

#### 추천 순서

```
Core 1 먼저 → Core 1 합격 → Core 2 공부 → Core 2 합격
```

한 번에 두 시험을 준비하면 범위가 너무 넓습니다. **하나씩 끝내세요.**

#### 도메인별 공부 비중

| 우선순위 | 도메인 | 이유 |
|----------|--------|------|
| 1순위 | 문제 해결 (Core 1) | 비중 29%로 가장 높음 |
| 2순위 | 하드웨어 (Core 1) | 25%, 기초 중의 기초 |
| 3순위 | 운영체제 + 보안 (Core 2) | 각각 28%, 절반 이상 차지 |
| 4순위 | 나머지 도메인 | 고르게 학습 |

#### 실습이 필수인 영역

- **하드웨어**: 실제 PC 분해·조립을 해보세요 (중고 PC면 충분)
- **OS**: VirtualBox로 Windows, Linux 설치·설정 연습
- **명령줄**: cmd, PowerShell, 리눅스 터미널 기본 명령어

---

## CompTIA Network+ — 네트워크의 기본기

### 이 자격증은 누구를 위한 건가?

- 네트워크 관리자·엔지니어를 목표로 할 때
- Security+를 준비하기 전 네트워크 기초를 다지고 싶을 때
- A+ 이후 다음 단계를 밟고 싶을 때

---

### 시험 도메인 (N10-009)

| 도메인 | 비중 | 핵심 내용 |
|--------|------|-----------|
| 네트워킹 개념 | 24% | OSI 모델, TCP/IP, 서브넷팅, 포트, 프로토콜 |
| 네트워크 구현 | 19% | 라우팅, 스위칭, 무선, WAN 기술 |
| 네트워크 운영 | 16% | 모니터링, 문서화, 정책, 고가용성 |
| 네트워크 보안 | 20% | 방화벽, VPN, ACL, 인증, 공격 유형 |
| 네트워크 문제 해결 | 21% | 연결 문제, 성능 문제, 도구 사용법 |

**가장 비중 높은 도메인**: 네트워킹 개념(24%) — OSI 모델과 TCP/IP는 반드시 완벽하게 이해해야 합니다.

---

### Network+ 핵심 개념 미리보기

시험에서 **반드시** 나오는 개념들입니다:

| 개념 | 왜 중요한가 |
|------|-------------|
| OSI 7계층 | 네트워크 문제를 계층별로 분석하는 프레임워크 |
| TCP vs UDP | 신뢰성 vs 속도, 포트 번호까지 |
| 서브넷팅 | IP 주소 계산 — 시험에서 여러 문제 출제 |
| DNS / DHCP | 인터넷 동작의 핵심 |
| VLAN | 네트워크 분리와 보안 |
| VPN | 원격 접속 보안 |

> ⚠️ **서브넷팅**: 많은 수험생이 어려워하지만, 연습하면 기계적으로 풀 수 있습니다. 유튜브에서 "subnetting practice" 검색하세요

---

### Network+ 공부 전략

#### 도메인별 공부 비중

| 우선순위 | 도메인 | 이유 |
|----------|--------|------|
| 1순위 | 네트워킹 개념 (24%) | 모든 도메인의 기초 |
| 2순위 | 네트워크 문제 해결 (21%) | PBQ 출제 가능성 높음 |
| 3순위 | 네트워크 보안 (20%) | Security+ 연계 |
| 4순위 | 구현 + 운영 | 남은 도메인 고르게 |

#### 실습이 필수인 영역

- **서브넷 계산**: 반복 연습이 답 — [SubnettingPractice.com](https://subnettingpractice.com/) 활용
- **패킷 분석**: Wireshark 설치 후 기본 패킷 캡처 연습
- **네트워크 명령어**: ping, tracert, nslookup, netstat, ipconfig

---

## CompTIA Security+ — 보안 커리어의 관문

### 이 자격증은 누구를 위한 건가?

- 사이버보안 분야에 진입하고 싶을 때
- **미국 국방부(DoD) 인정 자격증**이 필요할 때
- 보안 분석가·보안 엔지니어·SOC 분석가를 목표로 할 때

> 💡 Security+는 미국 정부·군 IT 직무의 **기본 요구 자격**입니다 (DoD 8570)

---

### 시험 도메인 (SY0-701)

| 도메인 | 비중 | 핵심 내용 |
|--------|------|-----------|
| 일반 보안 개념 | 12% | CIA 트라이어드, 제로 트러스트, 암호화 기초 |
| 위협·취약점·완화 | 22% | 멀웨어, 피싱, 사회공학, 취약점 관리 |
| 보안 아키텍처 | 18% | 클라우드/하이브리드 보안, 네트워크 설계, 인증 |
| 보안 운영 | 28% | 로그 분석, 인시던트 대응, 포렌식, 모니터링 |
| 보안 프로그램 관리 | 20% | 거버넌스, 위험 관리, 컴플라이언스, 감사 |

**가장 비중 높은 도메인**: 보안 운영(28%) — 실제 보안 업무의 핵심인 로그 분석, 인시던트 대응이 여기 포함됩니다.

---

### Security+ 핵심 개념 미리보기

| 개념 | 설명 |
|------|------|
| CIA 트라이어드 | 기밀성(Confidentiality), 무결성(Integrity), 가용성(Availability) |
| 제로 트러스트 | "아무도 믿지 마라" — 모든 접근을 검증 |
| SIEM | 보안 이벤트 통합 모니터링 시스템 |
| 인시던트 대응 | 탐지 → 분석 → 격리 → 복구 → 교훈 |
| 암호화 | 대칭(AES) vs 비대칭(RSA), 해시(SHA), PKI |
| MFA | 다중 인증 (알고 있는 것 + 가지고 있는 것 + 본인인 것) |

---

### Security+ 공부 전략

#### 도메인별 공부 비중

| 우선순위 | 도메인 | 이유 |
|----------|--------|------|
| 1순위 | 보안 운영 (28%) | 비중 최대, PBQ 핵심 |
| 2순위 | 위협·취약점·완화 (22%) | 실무와 직결 |
| 3순위 | 보안 프로그램 관리 (20%) | 암기 비중 높음 |
| 4순위 | 보안 아키텍처 (18%) | 클라우드·네트워크 설계 |
| 5순위 | 일반 보안 개념 (12%) | 기초이므로 빠르게 정리 |

#### 실습이 필수인 영역

- **로그 분석**: Splunk Free 또는 ELK Stack 기본 사용법
- **네트워크 보안**: 방화벽 규칙 설정 (pfSense 추천)
- **취약점 분석**: TryHackMe 무료 모듈 활용
- **암호화**: OpenSSL로 키 생성·인증서 만들기 연습

---

## 3개 시험 난이도 비교

| 비교 항목 | A+ | Network+ | Security+ |
|-----------|-----|----------|-----------|
| 난이도 | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ |
| 암기 비중 | 높음 | 중간 | 높음 |
| 이해 비중 | 중간 | 높음 | 높음 |
| 실습 필요도 | 중간 | 높음 | 높음 |
| 합격률 (비공식) | ~70% | ~60% | ~50% |
| 합격 커트라인 | 675~700/900 | 720/900 | 750/900 |

> 💡 Security+는 합격 점수(750)가 가장 높고, 보안 개념의 깊이가 있어 세 시험 중 가장 어렵습니다

---

## 추천 학습 자료

### 무료 자료

| 자료 | 대상 시험 | 특징 |
|------|-----------|------|
| **[Professor Messer](https://www.professormesser.com/)** | A+, Network+, Security+ | 가장 인기 있는 무료 강의. 체계적이고 시험 범위에 정확히 맞춤 |
| **[CompTIA 공식 시험 목표](https://www.comptia.org/certifications/)** | 전체 | 시험 범위 체크리스트로 활용 — 반드시 다운로드 |
| **[TryHackMe](https://tryhackme.com/)** | Security+ | 무료 모듈로 보안 실습 가능 |
| **[SubnettingPractice.com](https://subnettingpractice.com/)** | Network+ | 서브넷 계산 반복 연습 |

**Professor Messer 강의 바로가기**:
- [A+ Core 1 (220-1201) 무료 강의](https://www.professormesser.com/free-a-plus-training/220-1201/220-1201-video/220-1201-training-course/)
- [Network+ (N10-009) 무료 강의](https://www.professormesser.com/network-plus/n10-009/n10-009-video/n10-009-training-course/)
- [Security+ (SY0-701) 무료 강의](https://www.professormesser.com/security-plus/sy0-701/sy0-701-video/sy0-701-comptia-security-plus-course/)

### 유료 자료

| 자료 | 대상 시험 | 가격대 | 특징 |
|------|-----------|--------|------|
| **Jason Dion (Udemy)** | A+, Network+, Security+ | ~$15 (할인 시) | 강의 + 모의시험 세트. 실제 시험과 유사한 문제 |
| **Mike Meyers (Udemy)** | A+, Network+ | ~$15 (할인 시) | 친근한 설명, 초보자에게 최적 |
| **[CompTIA CertMaster](https://www.comptia.org/en-us/resources/certmaster-training/learn/)** | 전체 | $149~$349 | 공식 교육 플랫폼 |
| **Exam Cram 시리즈 (책)** | 전체 | $30~$45 | 시험 직전 핵심 정리용 |

**Jason Dion Udemy 강의 바로가기**:
- [A+ Core 1 (220-1201) 강의](https://www.udemy.com/course/comptia-a-core-1/)
- [A+ Core 2 (220-1202) 강의](https://www.udemy.com/course/comptia-a-core-2/)
- [Network+ (N10-009) 강의](https://www.udemy.com/course/comptia-network-009/)
- [Security+ (SY0-701) 강의](https://www.udemy.com/course/securityplus/)

**Mike Meyers Udemy 강의 바로가기**:
- [A+ Core 1 (220-1201) 강의](https://www.udemy.com/course/comptia-aplus-core-1/)
- [A+ Core 2 (220-1202) 강의](https://www.udemy.com/course/comptia-aplus-core-2/)
- [Network+ (N10-009) 강의](https://www.udemy.com/course/comptia-networkplus-certification/)

> 💡 **최고의 조합**: Professor Messer(무료 강의) + Jason Dion(모의시험) — 이 조합으로 합격한 사람이 가장 많습니다

---

## 합격 전략 — 시험 당일 팁

### PBQ(실기형 문제) 대처법

1. PBQ는 **건너뛰고** 객관식부터 풀기
2. 객관식 완료 후 남은 시간으로 PBQ 돌아오기
3. PBQ에서 막히면 부분 점수라도 노리기 — **빈칸으로 두지 마세요**

### 시간 관리

| 전략 | 방법 |
|------|------|
| 1차 패스 (60분) | 쉬운 문제 먼저 풀기, 어려운 건 표시(flag) |
| 2차 패스 (20분) | 표시한 문제 재도전 |
| PBQ (10분) | 남은 시간에 PBQ 집중 |

### 오답 소거법

CompTIA 시험은 **가장 좋은 답**을 고르는 문제가 많습니다. 정답이 2개처럼 보일 때:

- 더 **포괄적인** 답이 정답일 가능성 높음
- "모두 해당" 옵션이 있으면 신중하게 검토
- 절대적 표현 ("항상", "절대")이 있는 선지는 오답 가능성 높음

---

## 현실적 공부 플랜

### 3개월 플랜 (하루 1~2시간)

| 기간 | 목표 | 할 일 |
|------|------|-------|
| 1~4주 | A+ Core 1 | Professor Messer 강의 + 모의시험 |
| 5~6주 | A+ Core 1 시험 | 모의시험 반복 → 시험 응시 |
| 7~10주 | A+ Core 2 | 강의 + 실습 + 모의시험 |
| 11~12주 | A+ Core 2 시험 | 모의시험 반복 → 시험 응시 |

### +2개월 추가 (Network+ → Security+)

| 기간 | 목표 | 할 일 |
|------|------|-------|
| 13~17주 | Network+ | 강의 + 서브넷팅 연습 + 모의시험 |
| 18주 | Network+ 시험 | 시험 응시 |
| 19~24주 | Security+ | 강의 + TryHackMe + 모의시험 |
| 25주 | Security+ 시험 | 시험 응시 |

> 💡 **모의시험 목표 점수**: 실제 합격 점수 + 50점 이상 꾸준히 나오면 응시 타이밍입니다

---

## 합격 후 다음 단계

A+ → Network+ → Security+를 모두 취득했다면, 이제 **전문 분야**를 선택할 차례입니다.

| 목표 | 다음 자격증 | 설명 |
|------|------------|------|
| 보안 분석가 (Blue Team) | CySA+ | 위협 탐지·분석·대응 |
| 침투 테스터 (Red Team) | PenTest+ | 모의 해킹·취약점 발견 |
| 클라우드 엔지니어 | Cloud+ 또는 AWS SAA | 클라우드 인프라 |
| 리눅스 관리자 | Linux+ | 리눅스 시스템 관리 |
| 시니어 보안 전문가 | SecurityX (CASP+) | 엔터프라이즈 보안 |

> 다음 시리즈 3편에서 **CySA+와 PenTest+**를 자세히 다룹니다

---

## 시리즈 안내

| 편 | 주제 | 상태 |
|----|------|------|
| 1편 | [CompTIA 자격증 로드맵]({% post_url 2026-03-20-CompTIA_자격증_로드맵_IT_커리어_시작하기 %}) | ✅ |
| **2편** | **A+ / Network+ / Security+ 완벽 가이드 (이 글)** | ✅ |
| 3편 | [CySA+ / PenTest+ 보안 심화 가이드]({% post_url 2026-03-20-CompTIA_CySA+_PenTest+_보안_심화_가이드 %}) | ✅ |

---

## 참고 자료

- [CompTIA 공식 — A+ 자격증](https://www.comptia.org/certifications/a)
- [CompTIA 공식 — Network+ 자격증](https://www.comptia.org/certifications/network)
- [CompTIA 공식 — Security+ 자격증](https://www.comptia.org/certifications/security)
- [Professor Messer — 무료 강의](https://www.professormesser.com/)
- [TryHackMe — 보안 실습](https://tryhackme.com/)

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "CompTIA A+는 시험이 몇 개인가요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A+는 Core 1(220-1201)과 Core 2(220-1202) 두 개의 시험을 모두 통과해야 자격증이 발급됩니다. 비용은 총 $530(시험당 $265)이며, Core 1을 먼저 합격한 후 Core 2를 응시하는 것을 추천합니다."
      }
    },
    {
      "@type": "Question",
      "name": "A+, Network+, Security+ 중 어떤 것이 가장 어렵나요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Security+가 가장 어렵습니다. 합격 점수가 750/900으로 가장 높고, 보안 개념의 깊이와 범위가 넓습니다. A+는 범위가 넓지만 난이도는 낮고, Network+는 서브넷팅 등 이해가 필요한 개념이 있어 중간 수준입니다."
      }
    },
    {
      "@type": "Question",
      "name": "CompTIA 시험 공부는 어떤 자료로 하나요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "가장 인기 있는 조합은 Professor Messer의 무료 유튜브 강의와 Jason Dion의 Udemy 모의시험입니다. Professor Messer는 시험 범위에 정확히 맞춘 체계적 강의를 제공하고, Jason Dion의 모의시험은 실제 시험과 유사한 난이도로 평가받습니다."
      }
    },
    {
      "@type": "Question",
      "name": "PBQ(Performance-Based Questions)는 어떻게 준비하나요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "PBQ는 가상 환경에서 실제 작업을 수행하는 문제입니다. 실습 경험이 핵심이므로 VirtualBox로 OS 설치, Wireshark로 패킷 분석, 명령줄 도구 연습 등을 해두세요. 시험 당일에는 PBQ를 건너뛰고 객관식을 먼저 푼 후, 남은 시간에 PBQ를 풀는 전략이 효과적입니다."
      }
    },
    {
      "@type": "Question",
      "name": "Security+ 공부 기간은 얼마나 필요한가요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "네트워크와 OS 기초가 있다면 주 10~15시간 기준 약 6~8주가 적당합니다. 기초가 없다면 A+와 Network+를 먼저 취득한 후 도전하는 것을 추천합니다. 모의시험에서 합격 점수+50점 이상 꾸준히 나오면 응시 타이밍입니다."
      }
    }
  ]
}
</script>

*면책 조항: 이 글은 정보 제공 목적이며, 시험 코드·비용·도메인 비중은 CompTIA의 공식 발표에 따라 변경될 수 있습니다. 최신 정보는 반드시 [CompTIA 공식 사이트](https://www.comptia.org/)에서 확인하세요.*

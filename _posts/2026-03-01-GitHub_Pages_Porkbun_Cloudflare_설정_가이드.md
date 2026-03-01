---
layout: post
title: "GitHub Pages + Porkbun + Cloudflare 설정 가이드"
subtitle: 커스텀 도메인 블로그에 Cloudflare CDN과 보안을 추가하는 방법
date: 2026-03-01T12:00:00+09:00
lastmod: 2026-03-01T23:44:21+09:00
author: 수수
tags: ["GitHub Pages", "Cloudflare", "Porkbun", "CDN", "DNS", "SSL", "커스텀도메인", "블로그"]
categories: ["테크"]
---

안녕하세요. 수수입니다. <br />

GitHub Pages와 Porkbun 도메인으로 블로그를 운영하고 계신가요? <br />

이 가이드에서는 여기에 **Cloudflare**를 추가해서 CDN, 보안, 성능 최적화까지 한 번에 챙기는 방법을 단계별로 정리합니다. <br />

실제로 이 블로그(soosoo.life)에 적용한 과정을 그대로 따라하시면 됩니다.

## 목차

* TOC
{:toc}

---

## 현재 구성과 왜 Cloudflare를 추가하는가

### 기존 구성

현재 구성은 단순합니다:

```
사용자 → Porkbun DNS → GitHub Pages 서버
```

- **GitHub Pages**: Jekyll 블로그 호스팅 (무료)
- **Porkbun**: 커스텀 도메인 등록 및 DNS 관리
- **SSL**: GitHub Pages가 제공하는 Let's Encrypt 인증서

이 구성만으로도 블로그 운영에는 문제가 없습니다. 하지만 CDN 캐싱, DDoS 방어, 세부 보안 설정 같은 부분은 직접 제어할 수 없습니다.

### Cloudflare를 추가하는 이유

- **CDN**: 전 세계 330개+ 데이터센터에서 콘텐츠를 캐싱하여 로딩 속도 향상
- **보안**: DDoS 방어, WAF(웹 애플리케이션 방화벽), Bot 차단
- **성능**: Brotli 압축, Auto Minify, Early Hints
- **분석**: 트래픽, 보안 위협, 성능 메트릭을 대시보드에서 확인
- **무료**: Free 플랜으로도 위 기능 대부분 사용 가능

---

## 전체 구조 비교

### 적용 전

```
사용자 브라우저
    ↓ DNS 조회
Porkbun DNS
    ↓ A 레코드 응답
GitHub Pages 서버 (185.199.108-111.153)
    ↓ HTML/CSS/JS 응답
사용자 브라우저
```

### 적용 후

```
사용자 브라우저
    ↓ DNS 조회
Cloudflare DNS (네임서버 변경됨)
    ↓ 프록시 (주황색 구름)
Cloudflare Edge (CDN + WAF + SSL)
    ↓ 캐시 HIT → 즉시 응답
    ↓ 캐시 MISS → GitHub Pages로 요청
GitHub Pages 서버
    ↓ 원본 응답
Cloudflare Edge (캐싱 + 압축)
    ↓ 최적화된 응답
사용자 브라우저
```

| 항목 | 적용 전 | 적용 후 |
|------|---------|---------|
| **DNS** | Porkbun | Cloudflare |
| **CDN** | 없음 | Cloudflare 글로벌 CDN |
| **SSL** | Let's Encrypt (GitHub) | Cloudflare + Let's Encrypt (이중) |
| **DDoS 방어** | GitHub 기본 | Cloudflare 전용 방어 |
| **WAF** | 없음 | Cloudflare WAF |
| **캐싱** | 브라우저 캐시만 | Edge 캐싱 + 브라우저 캐시 |
| **분석** | 없음 (GA만) | Cloudflare Analytics + GA |
| **비용** | 무료 | 무료 (Free 플랜) |

---

## Cloudflare가 주는 것

### CDN (Content Delivery Network)

Cloudflare는 전 세계 330개 이상의 데이터센터를 운영합니다. 한국 사용자가 접속하면 서울 데이터센터에서 캐싱된 콘텐츠를 바로 전달하고, 미국 사용자는 가까운 미국 데이터센터에서 응답합니다.

정적 사이트인 Jekyll 블로그는 CDN 효과가 특히 큽니다. HTML, CSS, JS, 이미지 파일 모두 Edge에서 캐싱되므로 원본 서버(GitHub Pages)까지 갈 필요가 없습니다.

### 보안

- **DDoS 방어**: Layer 3/4/7 DDoS 공격을 자동으로 감지하고 차단
- **WAF**: 일반적인 웹 공격(SQL Injection, XSS 등)을 필터링
- **Bot Fight Mode**: 악성 봇 트래픽 차단
- **이메일 난독화**: 페이지에 노출된 이메일 주소를 봇이 수집하지 못하도록 처리

### 성능 최적화

- **Brotli 압축**: gzip보다 효율적인 압축으로 전송 크기 감소
- **Auto Minify**: HTML, CSS, JS 파일 자동 경량화
- **Early Hints (103)**: 브라우저가 페이지를 더 빠르게 로드하도록 사전 힌트 전송
- **HTTP/2, HTTP/3**: 최신 프로토콜 자동 지원

### 분석

Cloudflare 대시보드에서 별도의 JavaScript 트래커 없이도 트래픽 패턴, 보안 위협, 성능 메트릭을 확인할 수 있습니다.

---

## Step 1: Cloudflare 계정 생성 & 사이트 추가

### 1.1 계정 가입

1. [Cloudflare 가입 페이지](https://dash.cloudflare.com/sign-up)에 접속
2. 이메일과 비밀번호로 계정 생성
3. 이메일 인증 완료

### 1.2 사이트 추가

1. 대시보드에서 **"Add a site"** 클릭
2. 도메인 입력: `soosoo.life` (자신의 도메인 입력)
3. **Free 플랜** 선택 → **Continue**

Cloudflare가 기존 DNS 레코드를 자동으로 스캔합니다. 스캔이 완료되면 기존 레코드 목록이 표시됩니다.

> 기존 레코드를 확인하되, 다음 단계에서 GitHub Pages에 맞게 수정할 것이므로 일단 넘어가도 됩니다.

---

## Step 2: Porkbun 네임서버 변경

Cloudflare가 DNS를 관리하려면 도메인의 네임서버를 Cloudflare 것으로 변경해야 합니다.

### 2.1 Cloudflare 네임서버 확인

사이트 추가 과정에서 Cloudflare가 할당한 네임서버 2개를 확인합니다. 예시:

```
aria.ns.cloudflare.com
jon.ns.cloudflare.com
```

> 실제 값은 계정마다 다릅니다. 반드시 Cloudflare 대시보드에서 확인하세요.

### 2.2 Porkbun에서 네임서버 변경

1. [Porkbun](https://porkbun.com) 로그인
2. **Domain Management** → 해당 도메인 선택
3. **Authoritative Nameservers** 섹션 찾기
4. 기존 Porkbun 네임서버 삭제:
   ```
   curitiba.ns.porkbun.com
   fortaleza.ns.porkbun.com
   maceio.ns.porkbun.com
   salvador.ns.porkbun.com
   ```
5. Cloudflare 네임서버 2개 입력:
   ```
   aria.ns.cloudflare.com
   jon.ns.cloudflare.com
   ```
6. **Save** 클릭

### 2.3 전파 대기

네임서버 변경은 보통 **수 분 ~ 24시간** 정도 걸립니다. 대부분 1시간 이내에 완료됩니다.

Cloudflare 대시보드에서 **"Check nameservers"** 버튼으로 상태를 확인할 수 있습니다. 완료되면 이메일 알림이 옵니다.

---

## Step 3: Cloudflare DNS 레코드 설정

네임서버 변경이 완료되면 Cloudflare DNS에서 GitHub Pages를 가리키는 레코드를 설정합니다.

### 3.1 A 레코드 (IPv4)

Cloudflare 대시보드 → **DNS** → **Records** 에서 다음 4개의 A 레코드를 추가합니다:

| Type | Name | Content | Proxy status |
|------|------|---------|-------------|
| A | `@` | `185.199.108.153` | Proxied (주황색) |
| A | `@` | `185.199.109.153` | Proxied (주황색) |
| A | `@` | `185.199.110.153` | Proxied (주황색) |
| A | `@` | `185.199.111.153` | Proxied (주황색) |

### 3.2 AAAA 레코드 (IPv6)

| Type | Name | Content | Proxy status |
|------|------|---------|-------------|
| AAAA | `@` | `2606:50c0:8000::153` | Proxied (주황색) |
| AAAA | `@` | `2606:50c0:8001::153` | Proxied (주황색) |
| AAAA | `@` | `2606:50c0:8002::153` | Proxied (주황색) |
| AAAA | `@` | `2606:50c0:8003::153` | Proxied (주황색) |

### 3.3 CNAME 레코드 (www)

| Type | Name | Content | Proxy status |
|------|------|---------|-------------|
| CNAME | `www` | `your-username.github.io` | Proxied (주황색) |

> `your-username.github.io` 부분은 자신의 GitHub Pages 도메인으로 변경하세요.

### 3.4 Proxy 상태 설명

- **Proxied (주황색 구름)**: 트래픽이 Cloudflare를 거침 → CDN, WAF, DDoS 방어 활성화
- **DNS only (회색 구름)**: 단순 DNS 해석만 → Cloudflare 기능 비활성화

GitHub Pages에서는 **Proxied** 상태를 사용합니다.

---

## Step 4: SSL/TLS 설정

### 4.1 SSL 모드 설정

Cloudflare 대시보드 → **SSL/TLS** → **Overview**

**Full (Strict)** 모드를 선택합니다.

| 모드 | 설명 | 권장 |
|------|------|------|
| Off | 암호화 없음 | ❌ |
| Flexible | 브라우저↔Cloudflare만 암호화 | ❌ |
| Full | 양쪽 암호화, 인증서 검증 안 함 | △ |
| **Full (Strict)** | **양쪽 암호화, 인증서 검증함** | **✅ 권장** |

GitHub Pages는 Let's Encrypt로 유효한 SSL 인증서를 제공하므로 **Full (Strict)** 를 사용할 수 있습니다.

### 4.2 Edge Certificates 설정

**SSL/TLS** → **Edge Certificates** 에서 다음을 확인합니다:

- **Always Use HTTPS**: `ON` — HTTP 요청을 자동으로 HTTPS로 리다이렉트
- **HTTP Strict Transport Security (HSTS)**: `Enable`
  - Max-Age: `6 months` (또는 `12 months`)
  - Include subdomains: `ON`
  - Preload: `ON`
  - No-Sniff Header: `ON`
- **Minimum TLS Version**: `TLS 1.2`
- **Automatic HTTPS Rewrites**: `ON` — 페이지 내 HTTP 링크를 HTTPS로 자동 변환

> **HSTS 주의사항**: HSTS를 활성화하면 브라우저가 해당 도메인을 HTTPS로만 접속하도록 기억합니다. HTTPS를 해제할 계획이 없다면 활성화하세요.

---

## Step 5: 성능 최적화

### 5.1 캐싱 설정

**Caching** → **Configuration**:

- **Caching Level**: `Standard`
- **Browser Cache TTL**: `Respect Existing Headers` 또는 `1 month`

**Caching** → **Tiered Cache**:

- **Tiered Cache Topology**: `Smart` — 요청을 가까운 Cloudflare 데이터센터를 통해 효율적으로 라우팅

### 5.2 속도 최적화

**Speed** → **Optimization**:

- **Auto Minify**: HTML, CSS, JavaScript 모두 `ON`
- **Brotli**: `ON` — gzip보다 15-20% 더 효율적인 압축
- **Early Hints**: `ON` — 서버가 응답을 준비하는 동안 브라우저에 리소스 힌트 전송
- **HTTP/2 to Origin**: `ON`

### 5.3 Page Rules (선택)

특정 URL 패턴에 대해 캐싱 정책을 세밀하게 조절할 수 있습니다:

**예시: 정적 자산 장기 캐싱**

```
URL: soosoo.life/assets/*
설정: Cache Level → Cache Everything, Edge Cache TTL → 1 month
```

> Free 플랜에서는 Page Rules를 3개까지 사용할 수 있습니다.

---

## Step 6: 보안 설정

### 6.1 WAF (Web Application Firewall)

**Security** → **WAF**:

- Cloudflare Free 플랜에서도 기본 관리형 규칙이 활성화됩니다
- 일반적인 웹 공격(SQL Injection, XSS 등)을 자동 차단

### 6.2 Bot Fight Mode

**Security** → **Bots**:

- **Bot Fight Mode**: `ON` — 알려진 악성 봇 트래픽을 자동 차단
- 정상적인 검색 엔진 봇(Googlebot 등)은 영향받지 않음

### 6.3 이메일 난독화

**Security** → **Settings**:

- **Email Address Obfuscation**: `ON` — 페이지에 표시된 이메일 주소를 봇이 수집할 수 없도록 난독화

### 6.4 Scrape Shield

**Security** → **Settings**:

- **Hotlink Protection**: `ON` — 다른 사이트에서 이미지를 직접 링크하는 것을 방지

---

## Step 7: GitHub Pages 확인

### 7.1 CNAME 파일

레포지토리 루트에 `CNAME` 파일이 있는지 확인합니다:

```
soosoo.life
```

파일 내용은 커스텀 도메인(서브도메인 없이)이어야 합니다.

### 7.2 GitHub 레포지토리 설정

GitHub 레포지토리 → **Settings** → **Pages**:

1. **Custom domain**: `soosoo.life` 입력 (또는 이미 설정되어 있으면 확인)
2. **Enforce HTTPS**: 체크 ✅

> Cloudflare를 통해 네임서버를 변경한 직후에는 GitHub에서 DNS 확인이 실패할 수 있습니다. 네임서버 전파가 완료될 때까지 기다린 후 다시 확인하세요.

### 7.3 DNS 확인 후 인증서 발급

GitHub Pages는 커스텀 도메인의 DNS가 올바르게 설정되면 자동으로 Let's Encrypt 인증서를 발급합니다.

Cloudflare Proxied 모드에서는 GitHub가 직접 도메인을 확인하는 방식이 약간 다를 수 있습니다. 만약 인증서 발급에 문제가 있다면:

1. 일시적으로 A 레코드를 **DNS only (회색 구름)** 로 변경
2. GitHub Pages에서 인증서 발급 완료 대기
3. 다시 **Proxied (주황색 구름)** 로 변경

---

## 검증 & 트러블슈팅

### DNS 확인

```bash
# A 레코드 확인 (Cloudflare IP가 응답되어야 함)
dig soosoo.life A +short

# Cloudflare 프록시를 사용하므로 GitHub IP 대신
# Cloudflare IP가 표시됩니다

# AAAA 레코드 확인
dig soosoo.life AAAA +short

# 네임서버 확인
dig soosoo.life NS +short
# aria.ns.cloudflare.com
# jon.ns.cloudflare.com
```

### HTTP 응답 헤더 확인

```bash
curl -I https://soosoo.life
```

Cloudflare가 정상 동작하면 응답 헤더에 다음이 포함됩니다:

```
server: cloudflare
cf-ray: xxxxxxxxx-ICN
cf-cache-status: HIT  (또는 MISS, DYNAMIC)
```

### 흔한 문제와 해결

**1. "DNS_PROBE_FINISHED_NXDOMAIN" 에러**
```
원인: 네임서버 변경이 아직 전파되지 않음
해결: 최대 24시간 대기. Cloudflare 대시보드에서 "Check nameservers" 클릭
```

**2. GitHub Pages에서 "Domain not properly configured" 경고**
```
원인: DNS 전파 미완료 또는 Cloudflare 프록시 설정 문제
해결:
- 네임서버 전파 대기
- CNAME 파일 확인
- 필요시 일시적으로 DNS only 모드로 전환 후 확인
```

**3. ERR_TOO_MANY_REDIRECTS (리다이렉트 루프)**
```
원인: SSL 모드가 "Flexible"로 설정됨
해결: SSL/TLS → Overview에서 "Full (Strict)" 선택
```

**4. 사이트는 열리지만 "Not Secure" 표시**
```
원인: Mixed Content (HTTP 리소스가 섞여 있음)
해결:
- "Automatic HTTPS Rewrites" 활성화
- 페이지 소스에서 http:// 링크를 https://로 수정
```

**5. 캐시가 업데이트되지 않음**
```
원인: Cloudflare Edge 캐시에 이전 버전이 남아 있음
해결: Cloudflare 대시보드 → Caching → Purge Cache → Purge Everything
```

---

## 정리

### 핵심 체크리스트

- [ ] Cloudflare 계정 생성 및 사이트 추가 (Free 플랜)
- [ ] Porkbun 네임서버를 Cloudflare 네임서버로 변경
- [ ] DNS에 GitHub Pages A/AAAA 레코드 4개씩 추가 (Proxied)
- [ ] www CNAME 레코드 추가 (Proxied)
- [ ] SSL/TLS → Full (Strict) 설정
- [ ] Always Use HTTPS 활성화
- [ ] HSTS 활성화
- [ ] Auto Minify, Brotli, Early Hints 활성화
- [ ] Bot Fight Mode 활성화
- [ ] GitHub Pages에서 Custom domain & Enforce HTTPS 확인
- [ ] `dig` 명령어로 DNS 전파 확인
- [ ] `curl -I`로 Cloudflare 헤더 확인

### 최종 구성 요약

| 서비스 | 역할 |
|--------|------|
| **Porkbun** | 도메인 등록 (소유권) |
| **Cloudflare** | DNS, CDN, SSL, WAF, 보안, 성능 |
| **GitHub Pages** | 원본 서버 (Jekyll 호스팅) |

세 서비스 모두 **무료**로 사용할 수 있어, 비용 부담 없이 전문적인 웹 인프라를 구성할 수 있습니다.

---

## 관련 포스팅

- [Hugo에서 Jekyll로 마이그레이션하기](/2025-12-16-Hugo에서_Jekyll로_마이그레이션하기/)

---

## 참고 자료

- [GitHub Pages 공식 문서 - 커스텀 도메인 설정](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [Cloudflare 공식 문서](https://developers.cloudflare.com/)
- [Porkbun 도움말 - 네임서버 변경](https://kb.porkbun.com/article/22-how-to-change-your-nameservers)

---

**면책 조항** <br />
본 가이드는 2026년 3월 기준 GitHub Pages, Cloudflare, Porkbun의 설정 방법을 소개합니다. <br />
각 서비스는 지속적으로 업데이트되므로, 최신 정보는 공식 문서를 참고하시기 바랍니다. <br />
DNS 설정 변경 시 기존 서비스 접근에 영향을 줄 수 있으니 신중하게 진행하세요.

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "GitHub Pages에 Cloudflare를 추가하면 비용이 드나요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "아니요. Cloudflare Free 플랜으로 CDN, DDoS 방어, WAF, SSL, 성능 최적화 기능을 무료로 사용할 수 있습니다. GitHub Pages와 Porkbun 도메인도 무료(도메인 등록비 제외)이므로 추가 비용 없이 전문적인 웹 인프라를 구성할 수 있습니다."
      }
    },
    {
      "@type": "Question",
      "name": "Cloudflare SSL 모드는 무엇을 선택해야 하나요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Full (Strict) 모드를 권장합니다. GitHub Pages는 Let's Encrypt를 통해 유효한 SSL 인증서를 제공하므로 Full (Strict) 모드를 사용할 수 있습니다. Flexible 모드를 사용하면 리다이렉트 루프(ERR_TOO_MANY_REDIRECTS)가 발생할 수 있으니 반드시 Full (Strict)를 선택하세요."
      }
    },
    {
      "@type": "Question",
      "name": "네임서버 변경 후 사이트에 접속이 안 되면 어떻게 하나요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "네임서버 변경은 전파(propagation)에 시간이 걸립니다. 보통 수 분에서 최대 24시간까지 소요될 수 있습니다. Cloudflare 대시보드에서 'Check nameservers' 버튼으로 상태를 확인하고, dig 명령어로 DNS 전파 여부를 확인할 수 있습니다. 전파가 완료될 때까지 기다려주세요."
      }
    },
    {
      "@type": "Question",
      "name": "Cloudflare를 추가하면 GitHub Pages의 HTTPS가 깨지나요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "아니요. Cloudflare를 Proxied 모드로 설정하면 SSL이 이중으로 적용됩니다(브라우저↔Cloudflare, Cloudflare↔GitHub Pages). Full (Strict) 모드를 사용하면 양쪽 모두 유효한 인증서로 암호화됩니다. 다만 Cloudflare 추가 직후 GitHub Pages에서 인증서 재발급이 필요할 수 있으니, 문제가 있으면 일시적으로 DNS only 모드로 전환 후 인증서 발급을 기다리세요."
      }
    },
    {
      "@type": "Question",
      "name": "Cloudflare에서 Porkbun으로 다시 되돌릴 수 있나요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "네, 언제든지 가능합니다. Porkbun 대시보드에서 네임서버를 원래 Porkbun 네임서버(curitiba.ns.porkbun.com 등)로 되돌리고, Porkbun DNS에서 GitHub Pages A/AAAA 레코드를 다시 설정하면 됩니다. 되돌리는 과정도 네임서버 전파 시간이 필요합니다."
      }
    }
  ]
}
</script>

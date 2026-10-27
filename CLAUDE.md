# 블로그 프로젝트 가이드

## 프로젝트 개요
- Jekyll 기반 블로그 (Chirpy 테마)
- GitHub Pages로 배포
- 저장소: aaron-jang/aaron-jang.github.io

## 블로그 포스트 작성 규칙

### Front Matter 형식 (Chirpy 테마)
```yaml
---
layout: post
title: "제목"
description: "1~2줄 설명"
date: 2026-01-01T00:00:00+09:00
author: 수수
tags: ["태그1", "태그2", "태그3"]
categories: ["카테고리"]
image:
  path: /assets/images/이미지명.jpg
---
```

### 주의사항
- **이미지 형식**: `cover-img`/`thumbnail-img` 사용 금지. 반드시 `image: path:` 형식 사용
- **태그**: 최대 3개, 중요도 순 (타이틀 포함 태그 > 한글 태그 > 유명 브랜드/인물)
- **이미지 파일**: 다운로드 후 `file` 명령어로 실제 포맷 확인 필수 (확장자와 실제 포맷 불일치 주의)
- **이미지 경로**: `/assets/images/` 하위에 저장
- **작성자**: 항상 "수수"
- **날짜 타임존**: +09:00 (KST)
- **FAQ**: SEO deprecated — front matter에 faq 섹션 넣지 않기

### 포스트 작성 워크플로우
1. 주제 웹 조사 (WebSearch)
2. 기존 포스트 포맷 참고 (`_posts/` 최신 파일)
3. 이미지 다운로드 → `assets/images/`에 저장 → `file` 명령어로 실제 포맷 확인
4. 포스트 마크다운 작성
5. 커밋 & 푸시

### 카테고리 목록
기존에 사용된 카테고리: AI, 개발, 투자, 자동차, 생활, 말레이시아, 영화, 리뷰 등

### 본문 구조
- `## 목차` + `{: .no_toc}` + `* TOC` + `{:toc}` 로 자동 목차 생성
- 섹션은 `## 1. 제목` 형식으로 번호 매기기
- 인사말: "안녕하세요. 수수입니다."로 시작
- 마무리 섹션과 참고 링크 섹션으로 끝내기

## Git 커밋 컨벤션
- `feat:` 새 포스트 추가
- `fix:` 오류 수정
- `refactor:` 구조/태그 정리
- Co-Authored-By 항상 포함

## GitHub Actions
- Build and Deploy: htmlproofer로 내부 링크 검증 — 존재하지 않는 앵커 링크 주의
- 실패 시: `gh run list` → `gh run view <id> --log-failed`로 원인 확인

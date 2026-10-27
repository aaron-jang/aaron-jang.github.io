# /blog-post — 블로그 포스트 작성

주제를 받아 웹 조사부터 커밋/푸시까지 블로그 포스트를 완성합니다.

## 입력
- 사용자가 주제 또는 키워드를 제공 (예: "Orca ADE", "피클 AI 앱")

## 워크플로우

### 1단계: 웹 조사
- WebSearch로 주제를 2~3회 검색
- 핵심 정보, 수치, 출처 URL 수집

### 2단계: 기존 포맷 확인
- `_posts/` 디렉토리의 최신 파일 1개를 읽어 front matter 형식 확인

### 3단계: 이미지 준비
- 공식 사이트, GitHub, App Store 등에서 대표 이미지 다운로드
- `assets/images/`에 저장
- `file` 명령어로 실제 포맷 확인 필수 (확장자와 실제 포맷 불일치 주의)
- 실제 포맷과 확장자가 다르면 ffmpeg 등으로 변환

### 4단계: 포스트 작성
Front Matter 규칙:
```yaml
---
layout: post
title: "제목"
description: "1~2줄 설명"
date: YYYY-MM-DDT00:00:00+09:00
author: 수수
tags: ["태그1", "태그2", "태그3"]
categories: ["카테고리"]
image:
  path: /assets/images/이미지명.jpg
---
```

절대 지켜야 할 것:
- `cover-img`/`thumbnail-img` 사용 금지 → 반드시 `image: path:` 형식
- 태그 최대 3개, 중요도 순 (타이틀 포함 > 한글 > 유명 브랜드/인물)
- 작성자 항상 "수수"
- 날짜 타임존 +09:00 (KST)
- FAQ front matter 넣지 않기 (SEO deprecated)

본문 구조:
- "안녕하세요. 수수입니다."로 시작
- `## 목차` + `{: .no_toc}` + `* TOC` + `{:toc}` 자동 목차
- 섹션 `## 1. 제목` 형식으로 번호 매기기
- 마무리 섹션 + 참고 링크 섹션으로 끝

카테고리: AI, 개발, 투자, 자동차, 생활, 말레이시아, 영화, 리뷰 등

### 5단계: 커밋 & 푸시
- `git add` → `git commit` → `git push`
- 커밋 메시지: `feat: 포스트 제목 요약`
- Co-Authored-By 항상 포함

### 6단계: 빌드 확인
- `gh run list`로 GitHub Actions 빌드 확인
- 실패 시 `gh run view <id> --log-failed`로 원인 파악
- htmlproofer 앵커 링크 오류 주의

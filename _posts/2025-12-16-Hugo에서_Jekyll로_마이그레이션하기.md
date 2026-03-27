---
layout: post
title: "Hugo에서 Jekyll로 마이그레이션하기"
date: 2025-12-16T13:30:00+09:00
lastmod: 2025-12-17T21:15:51+09:00
author: 수수
tags: ["Hugo", "Jekyll", "마이그레이션", "GitHub Pages", "정적 사이트 생성기", "블로그"]
categories: ["교육"]
subtitle: GitHub Pages로 블로그를 이전한 전체 과정
cover-img: ./assets/images/jekyll.webp
---

## 개요

안녕하세요. 수수입니다.

Hugo로 운영하던 블로그를 Jekyll로 마이그레이션한 전체 과정을 정리했습니다. GitHub Pages에서 Jekyll을 공식 지원하기 때문에 빌드 과정이 더 간단해지고, Beautiful Jekyll 같은 훌륭한 테마들도 많아서 이전을 결정했습니다.

## 1. 왜 Jekyll로 이전했나?

### Hugo의 장점
- ⚡ 빠른 빌드 속도
- 🎨 다양한 테마
- 📦 단일 바이너리로 설치 간편

### Jekyll을 선택한 이유
- ✅ **GitHub Pages 공식 지원** - 별도 빌드 없이 푸시만으로 배포
- ✅ **Ruby 생태계** - 풍부한 플러그인과 커뮤니티
- ✅ **Beautiful Jekyll** - 깔끔하고 반응형 테마
- ✅ **간단한 설정** - Hugo보다 설정이 직관적

## 2. 마이그레이션 준비

### 2.1 환경 설정

```bash
# Ruby 설치 확인
ruby --version

# Jekyll 및 Bundler 설치
gem install jekyll bundler

# 작업 디렉토리 생성
mkdir ~/workspace/soosoolife_jekyll
cd ~/workspace/soosoolife_jekyll
```

### 2.2 Beautiful Jekyll 테마 설치

```bash
# Beautiful Jekyll 클론
git clone https://github.com/daattali/beautiful-jekyll.git .

# 불필요한 Git 히스토리 제거
rm -rf .git
git init
```

## 3. 기본 설정

### 3.1 _config.yml 수정

```yaml
# 사이트 기본 정보
title: 수수라이프
author: 수수
url: "https://aaron-jang.github.io"
baseurl: "/blog"

# 네비게이션 메뉴
navbar-links:
  Posts: "/"
  Categories: "/categories"
  Tags: "/tags"
  About: "about"

# Google Analytics
gtag: "G-XXXXXXXXXX"

# 타임존 설정
timezone: "Asia/Seoul"

# RSS 피드
rss-description: 수수의 일상과 정보를 공유하는 블로그입니다
```

### 3.2 Gemfile 설정

```ruby
source "https://rubygems.org"

# Jekyll 및 기본 플러그인
gem "jekyll", "~> 3.9"
gem "jekyll-paginate"
gem "jekyll-sitemap"
gem "kramdown-parser-gfm"

# Ruby 3.4+ 호환성을 위한 라이브러리
gem "base64"
gem "logger"
gem "csv"
gem "bigdecimal"

# GitHub Pages 호환성을 위한 webrick
gem "webrick", "~> 1.8"
```

## 4. 포스트 마이그레이션

### 4.1 자동 변환 스크립트

Hugo 포스트를 Jekyll 형식으로 변환하는 Python 스크립트를 작성했습니다:

```python
#!/usr/bin/env python3
import os
import re
from pathlib import Path
from datetime import datetime

def convert_frontmatter(hugo_frontmatter):
    """Hugo frontmatter를 Jekyll 형식으로 변환"""
    jekyll_frontmatter = {
        'layout': 'post',
    }

    # 필드 매핑
    field_mapping = {
        'title': 'title',
        'date': 'date',
        'author': 'author',
        'tags': 'tags',
        'categories': 'categories',
        'featuredImage': 'cover-img',
        'description': 'subtitle',
    }

    for hugo_key, jekyll_key in field_mapping.items():
        if hugo_key in hugo_frontmatter:
            jekyll_frontmatter[jekyll_key] = hugo_frontmatter[hugo_key]

    return jekyll_frontmatter

def convert_image_paths(content):
    """Hugo 이미지 경로를 Jekyll 형식으로 변환"""
    # /images/ -> /assets/images/
    content = re.sub(r'/images/', '/assets/images/', content)
    return content

# 포스트 변환 실행
posts_dir = Path('content/posts')
output_dir = Path('_posts')

for post_file in posts_dir.glob('*.md'):
    # 포스트 읽기 및 변환
    # ... (변환 로직)
```

### 4.2 주요 변환 작업

**Frontmatter 변환**:
```yaml
# Hugo
+++
title = "제목"
date = 2024-01-01
featuredImage = "/images/cover.jpg"
+++

# Jekyll
---
layout: post
title: "제목"
date: 2024-01-01T00:00:00+09:00
cover-img: /assets/posts/포스트명/cover.jpg
---
```

**이미지 경로 변환**:
- Hugo: `/images/photo.jpg` → Jekyll: `/assets/images/photo.jpg`
- 포스트별 이미지: `/assets/posts/포스트명/` 구조로 정리

**Shortcode 변환**:
{% raw %}
```markdown
# Hugo
{{< ref "다른포스트.md" >}}

# Jekyll
{% post_url 2024-01-01-다른포스트 %}
```
{% endraw %}

## 5. 주요 이슈 해결

### 5.1 이미지 경로 문제

**문제**: baseurl이 `/blog`로 설정되어 있어 이미지가 안 보이는 현상

**해결**: `relative_url` 필터 사용

{% raw %}
```markdown
# Before (잘못된 경로)
![이미지](/assets/posts/example/image.jpg)

# After (올바른 경로)
![이미지]({{ "/assets/posts/example/image.jpg" | relative_url }})
```
{% endraw %}

### 5.2 Hugo Shortcode 제거

**admonition 블록 변환**:
{% raw %}
```markdown
# Hugo
{{< admonition title="중요" >}}
내용
{{< /admonition >}}

# Jekyll (blockquote 사용)
> **💡 중요**
>
> 내용
```
{% endraw %}

### 5.3 포스트 간 링크 수정

**내부 링크 매핑**:
{% raw %}
```python
LINK_MAPPING = {
    '어린이 체험관 - 1. 요리, 탈것': '2023-10-02-잡월드_1_요리_탈것',
    '한국잡월드 0. 개요': '2023-10-02-잡월드_0_개요',
    # ...
}

# Hugo ref를 Jekyll post_url로 변환
content = re.sub(
    r'\[([^\]]+)\]\(#\)',
    lambda m: f'[{m.group(1)}]({{{{ site.baseurl }}}}{{% post_url {LINK_MAPPING[m.group(1)]} %}})',
    content
)
```
{% endraw %}

## 6. 추가 설정

### 6.1 Google AdSense 추가

**Auto Ads 스크립트** (`_includes/google-adsense.html`):
```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXX"
     crossorigin="anonymous"></script>
```

**포스트 내 광고** (`_includes/adsense-in-article.html`):
```html
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-XXXXXXXX"
     data-ad-slot="AUTO"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

### 6.2 네이버 사이트 인증

루트 디렉토리에 인증 파일 생성:
```bash
# naverXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.html
naver-site-verification: naverXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.html
```

### 6.3 ads.txt 추가

```
google.com, pub-XXXXXXXX, DIRECT, XXXXXXXXXXXXXXXX
```

## 7. 로컬 테스트

### 7.1 의존성 설치 및 빌드

```bash
# Bundle 설치
bundle install

# Jekyll 빌드
bundle exec jekyll build

# 로컬 서버 실행
bundle exec jekyll serve
```

### 7.2 확인 사항

- ✅ http://localhost:4000/blog/ 접속 확인
- ✅ 모든 포스트가 정상적으로 보이는지 확인
- ✅ 이미지가 제대로 로드되는지 확인
- ✅ 내부 링크가 작동하는지 확인
- ✅ 카테고리/태그 페이지 확인

## 8. GitHub Pages 배포

### 8.1 저장소 설정

```bash
# GitHub 저장소 생성: username.github.io

# 원격 저장소 추가
git remote add origin https://github.com/username/username.github.io.git

# 커밋 및 푸시
git add .
git commit -m "Jekyll 블로그 초기 설정

- Beautiful Jekyll 테마 적용
- Hugo에서 29개 포스트 마이그레이션
- 이미지 경로 및 내부 링크 수정
- Google AdSense 추가"

git push -u origin main
```

### 8.2 GitHub Pages 설정

1. 저장소 Settings → Pages
2. Source: `Deploy from a branch`
3. Branch: `main` / `/ (root)`
4. Save

## 9. 도메인 설정 (선택사항)

### 9.1 CNAME 파일 생성

```bash
echo "soosoo.life" > CNAME
```

### 9.2 DNS 설정

```
# A 레코드
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153

# CNAME 레코드
www -> username.github.io
```

## 10. 마이그레이션 결과

### 통계
- ✅ **포스트**: 29개 완벽 마이그레이션
- ✅ **이미지**: 77개 경로 수정
- ✅ **내부 링크**: 8개 포스트, 시리즈 연결 유지
- ✅ **빌드 시간**: ~0.5초
- ✅ **경고/오류**: 0개

### 개선 사항
- 🚀 GitHub Pages 직접 배포 (빌드 과정 자동화)
- 📱 Beautiful Jekyll의 반응형 디자인
- 🎨 깔끔한 UI/UX
- 🔍 SEO 최적화 (sitemap, RSS 자동 생성)

## 11. 문제 해결 팁

### Ruby 3.4+ 호환성 이슈
```bash
# base64, logger 등 표준 라이브러리가 제거됨
# Gemfile에 명시적으로 추가 필요
gem "base64"
gem "logger"
gem "csv"
gem "bigdecimal"
```

### YAML 파싱 오류
```yaml
# 특수문자가 포함된 title은 따옴표로 감싸기
title: "[중고거래] 잘 판매하는 법"  # ✅
title: [중고거래] 잘 판매하는 법   # ❌
```

### 이미지 경로 디버깅
```bash
# 빌드된 HTML에서 이미지 경로 확인
grep -r "img src" _site/

# 실제 이미지 파일 확인
find assets/ -name "*.jpg" -o -name "*.png"
```

## 12. 참고 자료

- [Jekyll 공식 문서](https://jekyllrb.com/docs/)
- [Beautiful Jekyll GitHub](https://github.com/daattali/beautiful-jekyll)
- [GitHub Pages 문서](https://docs.github.com/en/pages)
- [Jekyll Liquid 필터](https://jekyllrb.com/docs/liquid/filters/)

## 마무리

Hugo에서 Jekyll로 마이그레이션하는 과정이 생각보다 순조로웠습니다. 특히 GitHub Pages와의 통합이 정말 편리했고, Beautiful Jekyll 테마도 마음에 듭니다.

마이그레이션을 고민 중이시라면 이 가이드가 도움이 되었으면 좋겠습니다. 궁금한 점이 있으시면 댓글로 남겨주세요!

## 체크리스트

마이그레이션 시 확인할 사항들:

- [ ] Jekyll 설치 및 환경 설정
- [ ] _config.yml 기본 설정
- [ ] 포스트 frontmatter 변환
- [ ] 이미지 경로 수정 (`relative_url` 적용)
- [ ] Hugo shortcode 제거
- [ ] 내부 링크 수정 (`post_url` 적용)
- [ ] 로컬에서 빌드 및 테스트
- [ ] Google Analytics 연동
- [ ] Google AdSense 추가
- [ ] 사이트 인증 (Naver, Google)
- [ ] GitHub 저장소 생성 및 푸시
- [ ] GitHub Pages 설정
- [ ] 커스텀 도메인 연결 (선택)
- [ ] 모든 페이지 동작 확인
- [ ] SEO 설정 확인 (sitemap, robots.txt)

감사합니다! 🎉

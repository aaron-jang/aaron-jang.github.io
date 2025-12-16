# Hugo → Jekyll 마이그레이션 노트

## 마이그레이션 완료 사항

### 1. Jekyll 블로그 생성
- **위치**: `~/workspace/soosoolife_jekyll`
- **테마**: Beautiful Jekyll
- **URL**: https://soosoo.life

### 2. 포스트 변환
- **총 포스트 수**: 29개
- **변환 방식**: Hugo frontmatter → Jekyll frontmatter
- **파일명 형식**: `YYYY-MM-DD-title.md`
- **위치**: `_posts/`

#### Frontmatter 변환
- `featuredImage` → `cover-img`
- 이미지 경로: `images/` → `/assets/posts/포스트명/`
- 기타 필드: `title`, `date`, `author`, `tags`, `categories` 유지

#### Hugo Shortcode 제거/변환
- `{{< ref "..." >}}` → `{% post_url YYYY-MM-DD-title %}` (Jekyll 내부 링크로 변환)
- `{{< admonition tip>}}` → blockquote 형식으로 변환
- `{{<figure src="...">}}` → `![](...)`  마크다운 이미지 형식으로 변환

#### 포스트 간 내부 링크 변환
- **잡월드 시리즈** (4개 포스트): 시리즈 간 연결 완료
- **테슬라모델Y 악세서리 시리즈** (2개 포스트): 1편 ↔ 2편 연결 완료
- **에버랜드 시리즈** (2개 포스트): 영유아 추천코스 ↔ 화장실/편의시설 연결 완료
- 총 8개 포스트의 내부 링크가 Jekyll `{% post_url %}` 형식으로 변환됨

### 3. Asset 구조 재편성

#### 포스트별 이미지
- **위치**: `assets/posts/포스트명/`
- **예시**:
  - `content/posts/how_to_use_ios_openvpn_app/images/`
  - → `assets/posts/how_to_use_ios_openvpn_app/`

#### 공용 이미지
- **위치**: `assets/images/`
- **원본**: `static/images/` → `assets/images/`

#### 경로 변환
- 포스트 내 `/images/` → `/assets/images/`
- 포스트별 `images/` → `/assets/posts/포스트명/`

### 4. 설정 파일

#### _config.yml
```yaml
title: 수수라이프
author: 수수
url: "https://soosoo.life"
baseurl: ""
timezone: "Asia/Seoul"
gtag: "G-FVWYZ3MFW9"
```

#### 네비게이션
- Posts: "/"
- Categories: "/categories"
- Tags: "/tags"
- About: "/about"

### 5. 추가 페이지
- `about.md`: About 페이지
- `categories.html`: 카테고리 페이지
- `tags.html`: 태그 페이지 (Beautiful Jekyll 기본 제공)

### 6. GitHub Pages 설정
- `CNAME`: soosoo.life
- Git 저장소 초기화 완료

## 다음 단계

### GitHub에 배포하기

1. **GitHub Repository 생성**
   ```bash
   # GitHub에서 새 repository 생성 (예: soosoolife.github.io)
   ```

2. **원격 저장소 연결 및 푸시**
   ```bash
   cd ~/workspace/soosoolife_jekyll
   git remote add origin https://github.com/[username]/[repository].git
   git commit -m "Initial Jekyll blog migration from Hugo"
   git branch -M main
   git push -u origin main
   ```

3. **GitHub Pages 활성화**
   - Repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: main / (root)
   - Custom domain: soosoo.life (이미 CNAME 파일에 설정됨)

4. **DNS 설정**
   - 도메인 등록업체에서 다음 레코드 추가:
     ```
     Type: A
     Host: @
     Value: 185.199.108.153
            185.199.109.153
            185.199.110.153
            185.199.111.153

     Type: CNAME
     Host: www
     Value: [username].github.io
     ```

### 로컬 테스트

```bash
cd ~/workspace/soosoolife_jekyll
bundle install
bundle exec jekyll serve
# http://localhost:4000 에서 확인
```

## 마이그레이션 스크립트

### migrate_to_jekyll.py
- Hugo 포스트를 Jekyll 형식으로 변환
- Frontmatter 변환
- 이미지 asset 복사

### fix_posts.py
- Hugo shortcode 제거/변환
- 이미지 경로 수정

### fix_internal_links.py
- 포스트 간 내부 링크를 Jekyll `{% post_url %}` 형식으로 변환
- 8개 포스트의 시리즈 연결 복구

## 확인 사항

- [x] 29개 포스트 변환 완료
- [x] 이미지 파일 복사 완료
- [x] Hugo shortcode 제거 완료
- [x] 포스트 간 내부 링크 변환 완료 (8개 포스트)
- [x] _config.yml 설정 완료
- [x] 카테고리/태그 페이지 생성
- [x] CNAME 파일 생성
- [x] Git 저장소 초기화
- [ ] 로컬 테스트
- [ ] GitHub에 배포
- [ ] DNS 설정
- [ ] 실제 사이트 확인

## 주의 사항

1. **Hugo shortcode 완전 제거되지 않은 부분**
   - 일부 복잡한 shortcode는 수동 확인 필요
   - 특히 ref 링크는 실제 포스트 URL로 수동 업데이트 권장

2. **이미지 경로**
   - 모든 이미지 경로가 올바르게 변환되었는지 확인 필요
   - 로컬 테스트 시 브라우저 개발자 도구로 404 에러 확인

3. **카테고리/태그**
   - 기존 Hugo의 카테고리와 태그 구조 유지됨
   - 필요시 정리 및 통합 권장

4. **GitHub Pages 제한사항**
   - Jekyll 플러그인은 GitHub Pages에서 제한적
   - Beautiful Jekyll은 GitHub Pages 호환 테마

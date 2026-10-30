# soosoo.life

**수수라이프** — 수수의 개인 블로그

## About

IT, AI, 반도체, 자동차, 말레이시아 생활, 재테크 등 다양한 주제를 다루는 블로그입니다.

- URL: [https://soosoo.life](https://soosoo.life)
- Author: 수수
- Framework: [Jekyll](https://jekyllrb.com/) + [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy)
- Hosting: GitHub Pages

## Tech Stack

| 항목 | 기술 |
|------|------|
| Static Site Generator | Jekyll |
| Theme | Chirpy (`jekyll-theme-chirpy`, `~> 7.6`) |
| Ruby | 로컬 3.4.1 (`.ruby-version`), CI 3.4 |
| Hosting | GitHub Pages (GitHub Actions 빌드·배포) |
| Domain | soosoo.life |
| Language | Korean (ko) |

## Local Development

```bash
# Ruby 3.4.1 및 Bundler가 설치된 환경에서 실행
# 의존성 설치
bundle install

# 로컬 서버 실행
bundle exec jekyll serve
```

`http://localhost:4000` 에서 확인할 수 있습니다.

```bash
# 초안 포함 미리보기
bundle exec jekyll serve --drafts

# 프로덕션 빌드 (결과: _site/)
JEKYLL_ENV=production bundle exec jekyll build
```

## Directory Structure

```
_posts/         # 블로그 포스트 (Markdown)
_drafts/        # 미발행 초안
_layouts/       # 페이지 레이아웃
_includes/      # 재사용 컴포넌트
_data/          # 데이터 파일
_tabs/          # 소개, 카테고리, 태그, 아카이브 페이지
assets/         # 이미지, CSS, JS 등 정적 파일
disney-adventure-decks/ # 다국어 디즈니 어드벤처호 시설 가이드 PWA
scripts/        # 가이드 생성, 이미지 최적화, 색인 요청 스크립트
.github/workflows/ # 빌드·배포 및 검색엔진 색인 자동화
_docs/          # 이전 마이그레이션·정리 기록
_site/          # Jekyll 빌드 결과 (Git 추적 제외)
```

사이트 설정은 `_config.yml`에서 관리합니다. 게시글 파일명은 `YYYY-MM-DD-title.md` 형식이며, 기본 URL은 `/:year-:month-:day-:title/`입니다.

## Deployment

`.github/workflows/pages-deploy.yml`이 `main` 또는 `master` 브랜치에 푸시할 때 실행됩니다. 프로덕션 빌드 후 HTMLProofer로 내부 링크 등을 검사하고 GitHub Pages에 배포합니다. Actions 탭에서 수동 실행도 가능합니다. README, LICENSE, `.gitignore`만 변경한 푸시는 배포를 실행하지 않습니다.

`main` 브랜치의 `_posts/` 변경 시 별도 워크플로가 Google Indexing API와 네이버 IndexNow에 색인 요청을 보냅니다. Google 요청에는 저장소 시크릿 `GOOGLE_SERVICE_ACCOUNT_JSON`이 필요합니다.

## Disney Adventure Guide

`disney-adventure-decks/`는 한국어, 영어, 일본어, 중국어 간체·번체를 지원하는 정적 가이드입니다. 즐겨찾기, 홈 화면 설치, 오프라인 기능을 제공합니다.

데이터와 번역은 `scripts/build-disney-guide.py`에서 관리하며, 수정 후 페이지를 재생성하고 생성된 파일도 함께 커밋합니다. 생성에는 Python 3와 `opencc-python-reimplemented`가 필요합니다.

```bash
# 별도 가상환경에서 의존성 설치
python3 -m venv ../soosoolife-guide-venv
../soosoolife-guide-venv/bin/python -m pip install opencc-python-reimplemented
../soosoolife-guide-venv/bin/python scripts/build-disney-guide.py
```

## License

MIT License

#!/usr/bin/env python3
"""
네이버 IndexNow - 새 포스트 자동 색인 요청 스크립트
GitHub Actions에서 push 이벤트 시 실행됩니다.

Google Indexing API(google-indexing.py)와 동일한 트리거/URL 추출 로직을 쓰되,
서비스 계정 인증 없이 IndexNow 키만으로 네이버 서치어드바이저에 색인을 요청합니다.
같은 IndexNow 키로 Bing/Yandex 등 다른 참여 검색엔진에도 함께 통보됩니다.

사용법:
  python3 scripts/naver-indexnow.py --file /tmp/changed_posts.txt
  python3 scripts/naver-indexnow.py file1.md file2.md

참고:
  키 파일은 사이트 루트에 호스팅되어야 합니다.
  https://soosoo.life/263e6540e0b242e681269fca80768c0e1ae103453d8c4c68acfae4c8633d99bf.txt
"""

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

SITE_URL = "https://soosoo.life"
HOST = "soosoo.life"
INDEXNOW_KEY = "263e6540e0b242e681269fca80768c0e1ae103453d8c4c68acfae4c8633d99bf"
KEY_LOCATION = f"{SITE_URL}/{INDEXNOW_KEY}.txt"
# 네이버 서치어드바이저 IndexNow 엔드포인트
INDEXNOW_ENDPOINT = "https://searchadvisor.naver.com/indexnow"


def extract_post_urls(changed_files):
    """변경된 파일 목록에서 _posts/*.md 파일의 URL을 추출 (한글 슬러그는 percent-encoding)"""
    urls = []
    for filepath in changed_files:
        # _posts/2026-06-21-AI버블_꺼져도_돈은_여기로_김학주_마벨_광통신.md 형태
        match = re.match(r"_posts/(\d{4})-(\d{2})-(\d{2})-(.+)\.md$", filepath)
        if match:
            year, month, day, slug = match.groups()
            # 슬러그(한글 포함)를 안전하게 URL 인코딩
            # permalink 형식: /:year-:month-:day-:title/ (sitemap canonical과 동일)
            slug_enc = urllib.parse.quote(slug, safe="")
            url = f"{SITE_URL}/{year}-{month}-{day}-{slug_enc}/"
            urls.append(url)
    return urls


def submit_indexnow(urls):
    """IndexNow에 URL 목록을 한 번에 POST로 제출"""
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
    }

    req = urllib.request.Request(INDEXNOW_ENDPOINT, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            text = response.read().decode("utf-8", errors="replace")
            print(f"  OK: HTTP {status}")
            if text.strip():
                print(f"      -> {text.strip()}")
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        # IndexNow 규약: 200/202 성공. 일부 엔드포인트는 202를 HTTPError로 올리지 않음.
        print(f"  FAIL: HTTP {e.code}")
        print(f"      -> {error_body.strip()}")
        # 200/202는 성공으로 간주
        return e.code in (200, 202)
    except urllib.error.URLError as e:
        print(f"  FAIL: 네트워크 오류 -> {e.reason}")
        return False


def main():
    # --file 옵션: 파일에서 목록 읽기 (한글 파일명 안전 처리)
    if len(sys.argv) >= 3 and sys.argv[1] == "--file":
        filepath = sys.argv[2]
        with open(filepath, "r", encoding="utf-8") as f:
            changed_files = [line.strip() for line in f if line.strip()]
    else:
        changed_files = sys.argv[1:]

    if not changed_files:
        print("변경된 파일이 없습니다.")
        return

    print(f"변경된 파일 {len(changed_files)}개 감지")
    urls = extract_post_urls(changed_files)

    if not urls:
        print("새로운/수정된 포스트가 없습니다. 스킵합니다.")
        return

    print(f"\nIndexNow 색인 요청할 URL {len(urls)}개:")
    for url in urls:
        print(f"  - {url}")

    print("\n네이버 IndexNow 요청 시작...\n")
    ok = submit_indexnow(urls)
    print(f"\n완료: {'성공' if ok else '실패'}")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()

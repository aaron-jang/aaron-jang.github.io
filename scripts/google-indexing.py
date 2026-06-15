#!/usr/bin/env python3
"""
Google Indexing API - 새 포스트 자동 인덱싱 요청 스크립트
GitHub Actions에서 push 이벤트 시 실행됩니다.

사용법:
  python3 scripts/google-indexing.py --file /tmp/changed_posts.txt
  python3 scripts/google-indexing.py file1.md file2.md

환경변수:
  GOOGLE_SERVICE_ACCOUNT_JSON: 서비스 계정 JSON 키 (GitHub Secret)
"""

import json
import os
import re
import sys

import google.auth.transport.requests
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/indexing"]
INDEXING_API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SITE_URL = "https://soosoo.life"


def get_credentials():
    """GitHub Secret에서 서비스 계정 JSON을 읽어 인증 객체 생성"""
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON 환경변수가 설정되지 않았습니다.")
        sys.exit(1)

    sa_info = json.loads(sa_json)
    credentials = service_account.Credentials.from_service_account_info(
        sa_info, scopes=SCOPES
    )
    return credentials


def extract_post_urls(changed_files):
    """변경된 파일 목록에서 _posts/*.md 파일의 URL을 추출"""
    urls = []
    for filepath in changed_files:
        # _posts/2026-06-15-레버리지_ETF_변동성_손실_녹는_이유.md 형태
        match = re.match(r"_posts/(\d{4})-(\d{2})-(\d{2})-(.+)\.md$", filepath)
        if match:
            year, month, day, slug = match.groups()
            url = f"{SITE_URL}/{year}/{month}/{day}/{slug}/"
            urls.append(url)
    return urls


def request_indexing(credentials, url, action="URL_UPDATED"):
    """Google Indexing API에 인덱싱 요청"""
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)

    import urllib.request

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {credentials.token}",
    }
    body = json.dumps({"url": url, "type": action}).encode("utf-8")

    req = urllib.request.Request(INDEXING_API_URL, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"  OK: {url}")
            print(f"      -> notifyTime: {result.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('notifyTime', 'N/A')}")
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"  FAIL: {url}")
        print(f"      -> {e.code}: {error_body}")
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

    print(f"\n인덱싱 요청할 URL {len(urls)}개:")
    for url in urls:
        print(f"  - {url}")

    credentials = get_credentials()

    print("\nGoogle Indexing API 요청 시작...\n")
    success = 0
    for url in urls:
        if request_indexing(credentials, url):
            success += 1

    print(f"\n완료: {success}/{len(urls)} 성공")


if __name__ == "__main__":
    main()

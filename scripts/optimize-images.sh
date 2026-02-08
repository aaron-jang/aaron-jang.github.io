#!/bin/bash
# WebP 이미지 변환 스크립트
# cwebp (libwebp) + sips (macOS 내장) 사용
# 용도: assets/ 하위 JPG/PNG → WebP 변환 + 480w 모바일 썸네일 생성

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

QUALITY_FULL=80
QUALITY_MOBILE=75
MOBILE_WIDTH=480

IMAGE_DIRS=(
  "$PROJECT_DIR/assets/images"
  "$PROJECT_DIR/assets/img"
  "$PROJECT_DIR/assets/posts"
)

converted=0
skipped=0
errors=0

convert_to_webp() {
  local src="$1"
  local basename="${src%.*}"
  local webp_full="${basename}.webp"
  local webp_mobile="${basename}-480w.webp"

  # 원본 해상도 WebP
  if [ -f "$webp_full" ]; then
    echo "  SKIP  $webp_full (exists)"
    skipped=$((skipped + 1))
  else
    if cwebp -q "$QUALITY_FULL" "$src" -o "$webp_full" -quiet 2>/dev/null; then
      local src_size=$(stat -f%z "$src" 2>/dev/null || stat -c%s "$src" 2>/dev/null)
      local webp_size=$(stat -f%z "$webp_full" 2>/dev/null || stat -c%s "$webp_full" 2>/dev/null)
      echo "  CONV  $webp_full (${src_size} → ${webp_size} bytes)"
      converted=$((converted + 1))
    else
      echo "  ERR   $src → WebP 변환 실패"
      errors=$((errors + 1))
    fi
  fi

  # 480w 모바일 썸네일
  if [ -f "$webp_mobile" ]; then
    echo "  SKIP  $webp_mobile (exists)"
    skipped=$((skipped + 1))
  else
    local tmp_resized="/tmp/resize_$(basename "$src")"
    # sips로 리사이즈 (macOS)
    if command -v sips &>/dev/null; then
      cp "$src" "$tmp_resized"
      sips --resampleWidth "$MOBILE_WIDTH" "$tmp_resized" --out "$tmp_resized" &>/dev/null
    else
      # Linux fallback: ImageMagick
      convert "$src" -resize "${MOBILE_WIDTH}x" "$tmp_resized" 2>/dev/null
    fi

    if [ -f "$tmp_resized" ]; then
      if cwebp -q "$QUALITY_MOBILE" "$tmp_resized" -o "$webp_mobile" -quiet 2>/dev/null; then
        local mobile_size=$(stat -f%z "$webp_mobile" 2>/dev/null || stat -c%s "$webp_mobile" 2>/dev/null)
        echo "  CONV  $webp_mobile (${mobile_size} bytes)"
        converted=$((converted + 1))
      else
        echo "  ERR   $src → 480w WebP 변환 실패"
        errors=$((errors + 1))
      fi
      rm -f "$tmp_resized"
    fi
  fi
}

echo "=== WebP 이미지 최적화 ==="
echo "Quality: full=${QUALITY_FULL}, mobile=${QUALITY_MOBILE}"
echo ""

for dir in "${IMAGE_DIRS[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "SKIP directory: $dir (not found)"
    continue
  fi

  echo "Processing: $dir"
  while IFS= read -r -d '' file; do
    ext="${file##*.}"
    ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

    case "$ext_lower" in
      jpg|jpeg|png)
        convert_to_webp "$file"
        ;;
    esac
  done < <(find "$dir" -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) -print0)
  echo ""
done

echo "=== 완료 ==="
echo "변환: ${converted}개 | 스킵: ${skipped}개 | 오류: ${errors}개"

#!/usr/bin/env python3
import os
import re
from pathlib import Path

posts_dir = Path('/Users/hyeongjinjang/workspace/soosoolife_jekyll/_posts')
assets_dir = Path('/Users/hyeongjinjang/workspace/soosoolife_jekyll/assets')

# Pattern to match incorrect cover-img paths
pattern = r'cover-img: (/assets/posts/[^/]+)/assets/images/(.+)'

fixed_count = 0
checked_count = 0

for post_file in posts_dir.glob('*.md'):
    checked_count += 1
    content = post_file.read_text(encoding='utf-8')

    # Check if this post has the problematic pattern
    match = re.search(pattern, content)
    if match:
        old_path = f"{match.group(1)}/assets/images/{match.group(2)}"
        new_path = f"{match.group(1)}/{match.group(2)}"

        # Verify the image file actually exists
        image_file = assets_dir / old_path.replace('/assets/', '')
        correct_image = assets_dir / new_path.replace('/assets/', '')

        if correct_image.exists():
            print(f"✓ {post_file.name}")
            print(f"  Old: {old_path}")
            print(f"  New: {new_path}")

            # Replace the path
            new_content = content.replace(old_path, new_path)
            post_file.write_text(new_content, encoding='utf-8')
            fixed_count += 1
        else:
            print(f"✗ {post_file.name} - Image not found: {correct_image}")

print(f"\n총 {checked_count}개 포스트 확인")
print(f"{fixed_count}개 포스트 수정 완료")

#!/usr/bin/env python3
import re
from pathlib import Path

posts_dir = Path('/Users/hyeongjinjang/workspace/soosoolife_jekyll/_posts')

# Pattern to match markdown images with absolute asset paths
pattern = r'!\[([^\]]*)\]\((/assets/[^)]+)\)'

fixed_count = 0
checked_count = 0

for post_file in posts_dir.glob('*.md'):
    content = post_file.read_text(encoding='utf-8')
    original_content = content

    # Find all matches
    matches = list(re.finditer(pattern, content))

    if matches:
        checked_count += 1
        print(f"\n📝 {post_file.name}")

        for match in matches:
            alt_text = match.group(1)
            old_path = match.group(2)

            # Create new path with relative_url filter
            new_image = f'![{alt_text}]({{{{ "{old_path}" | relative_url }}}})'
            old_image = match.group(0)

            print(f"  Old: {old_image}")
            print(f"  New: {new_image}")

            content = content.replace(old_image, new_image)

        # Write back if changed
        if content != original_content:
            post_file.write_text(content, encoding='utf-8')
            fixed_count += 1

print(f"\n총 {checked_count}개 포스트에서 이미지 발견")
print(f"{fixed_count}개 포스트 수정 완료")

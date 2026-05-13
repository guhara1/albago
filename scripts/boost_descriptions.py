#!/usr/bin/env python3
"""
description 길이가 50자 미만인 페이지에 컨텍스트 문구를 추가해
Google 권장 70~160자 범위로 보강.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SUFFIX = " 마사지알바고에서 검증된 사업자의 마사지·스파·테라피 채용 정보를 권역별로 확인하세요."


def main() -> int:
    count = 0
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        html = p.read_text(encoding="utf-8")
        m = re.search(r'(<meta name="description" content=")([^"]*)("[ /]*>)', html)
        if not m:
            continue
        existing = m.group(2)
        if len(existing) >= 50:
            continue
        # 이미 SUFFIX 포함이면 건너뜀 (idempotent)
        if "마사지알바고에서 검증된 사업자" in existing:
            continue
        boosted = existing.rstrip() + SUFFIX
        if len(boosted) > 170:
            boosted = boosted[:167] + "…"
        new_meta = m.group(1) + boosted + m.group(3)
        new_html = html[:m.start()] + new_meta + html[m.end():]

        # og:description 동일하게 갱신
        og_pattern = r'(<meta property="og:description" content=")([^"]*)("[ /]*>)'
        og_match = re.search(og_pattern, new_html)
        if og_match and og_match.group(2) == existing:
            new_og = og_match.group(1) + boosted + og_match.group(3)
            new_html = new_html[:og_match.start()] + new_og + new_html[og_match.end():]

        p.write_text(new_html, encoding="utf-8")
        count += 1
    print(f"boosted descriptions: {count} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

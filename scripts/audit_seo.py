#!/usr/bin/env python3
"""
albago 사이트 전체 SEO / E-E-A-T 감사 도구.
모든 *.html 파일을 스캔하여 Google 가이드라인 위반·약점을 보고.
"""

from __future__ import annotations
import re
import json
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parent.parent

# ===== 헬퍼 =====
def files():
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        yield p

def meta(html: str, name: str) -> str | None:
    m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', html)
    if m: return m.group(1)
    m = re.search(rf'<meta\s+property="{name}"\s+content="([^"]*)"', html)
    return m.group(1) if m else None

def get_title(html: str) -> str | None:
    m = re.search(r'<title>([^<]*)</title>', html)
    return m.group(1).strip() if m else None

def get_canonical(html: str) -> str | None:
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html)
    return m.group(1) if m else None

def get_h1s(html: str) -> list[str]:
    return re.findall(r'<h1[^>]*>([^<]*)</h1>', html)

def imgs(html: str) -> list[tuple[str, str]]:
    return re.findall(r'<img\s+[^>]*src="([^"]*)"[^>]*alt="([^"]*)"', html)

def imgs_missing_alt(html: str) -> list[str]:
    # <img> 태그 중 alt 속성이 없거나 비어있는 것
    bad = []
    for m in re.finditer(r'<img\s+([^>]*)>', html):
        attrs = m.group(1)
        src_m = re.search(r'src="([^"]*)"', attrs)
        alt_m = re.search(r'alt="([^"]*)"', attrs)
        if not alt_m or not alt_m.group(1).strip():
            bad.append(src_m.group(1) if src_m else "(no src)")
    return bad

def jsonld_blocks(html: str) -> list[str]:
    return re.findall(
        r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>',
        html, re.DOTALL
    )

def lang_attr(html: str) -> str | None:
    m = re.search(r'<html\s+lang="([^"]*)"', html)
    return m.group(1) if m else None

def has_viewport(html: str) -> bool:
    return 'name="viewport"' in html

def has_charset(html: str) -> bool:
    return 'charset="utf-8"' in html.lower() or 'charset=utf-8' in html.lower()


# ===== 본 감사 =====
def audit():
    titles = defaultdict(list)          # title → [paths]
    descriptions = defaultdict(list)
    canonicals = defaultdict(list)
    h1_counts = []                      # (path, count)
    page_records = []

    for f in files():
        rel = str(f.relative_to(ROOT))
        html = f.read_text(encoding="utf-8")
        t = get_title(html)
        d = meta(html, "description")
        c = get_canonical(html)
        h1s = get_h1s(html)
        og_title = meta(html, "og:title")
        og_image = meta(html, "og:image")
        og_url = meta(html, "og:url")
        kw = meta(html, "keywords")
        lang = lang_attr(html)
        vp = has_viewport(html)
        cs = has_charset(html)
        ld = jsonld_blocks(html)
        bad_alts = imgs_missing_alt(html)
        page_chars = len(re.sub(r'<[^>]+>', '', html))

        if t: titles[t].append(rel)
        if d: descriptions[d].append(rel)
        if c: canonicals[c].append(rel)
        h1_counts.append((rel, len(h1s), h1s[:1]))

        page_records.append({
            "path": rel,
            "title": t,
            "desc": d,
            "canonical": c,
            "h1_count": len(h1s),
            "og_title": og_title,
            "og_image": og_image,
            "og_url": og_url,
            "keywords": kw,
            "lang": lang,
            "viewport": vp,
            "charset": cs,
            "jsonld_count": len(ld),
            "bad_alts": bad_alts,
            "page_chars": page_chars,
        })

    # ===== 발견 =====
    print("=" * 70)
    print(" SEO / E-E-A-T 감사 결과 — 총 {} 페이지".format(len(page_records)))
    print("=" * 70)

    # 1. 중복 타이틀
    dup_titles = {t: paths for t, paths in titles.items() if len(paths) > 1}
    print(f"\n[1] 중복 <title> 그룹: {len(dup_titles)}개")
    for t, paths in list(dup_titles.items())[:10]:
        print(f"  • \"{t[:60]}\" → {len(paths)}개 파일")
        for p in paths[:3]:
            print(f"     - {p}")
        if len(paths) > 3: print(f"     - ... +{len(paths)-3}")

    # 2. 중복 description
    dup_desc = {d: paths for d, paths in descriptions.items() if len(paths) > 1}
    print(f"\n[2] 중복 <meta description> 그룹: {len(dup_desc)}개")
    for d, paths in list(dup_desc.items())[:10]:
        print(f"  • \"{d[:60]}…\" → {len(paths)}개 파일")
        for p in paths[:3]:
            print(f"     - {p}")
        if len(paths) > 3: print(f"     - ... +{len(paths)-3}")

    # 3. 중복 canonical (= 다른 페이지가 같은 URL 가리킴 - 큰 문제)
    dup_canonical = {c: paths for c, paths in canonicals.items() if len(paths) > 1}
    print(f"\n[3] 중복 canonical 그룹 (다른 페이지가 같은 URL 가리킴): {len(dup_canonical)}개")
    for c, paths in list(dup_canonical.items())[:10]:
        print(f"  • {c} → {len(paths)}개 파일")
        for p in paths[:3]:
            print(f"     - {p}")
        if len(paths) > 3: print(f"     - ... +{len(paths)-3}")

    # 4. canonical 미존재
    missing_canonical = [r for r in page_records if not r["canonical"]]
    print(f"\n[4] canonical 누락: {len(missing_canonical)}개")
    for r in missing_canonical[:8]:
        print(f"  • {r['path']}")

    # 5. title 누락
    missing_title = [r for r in page_records if not r["title"]]
    print(f"\n[5] <title> 누락: {len(missing_title)}개")
    for r in missing_title[:5]:
        print(f"  • {r['path']}")

    # 6. description 누락
    missing_desc = [r for r in page_records if not r["desc"]]
    print(f"\n[6] meta description 누락: {len(missing_desc)}개")
    for r in missing_desc[:5]:
        print(f"  • {r['path']}")

    # 7. h1 0개 또는 2개+
    bad_h1 = [r for r in page_records if r["h1_count"] != 1]
    print(f"\n[7] h1 개수 비정상 (0개 또는 2개+): {len(bad_h1)}개")
    for r in bad_h1[:8]:
        print(f"  • {r['path']} → h1 {r['h1_count']}개")

    # 8. 너무 짧은 title (<10자) 또는 너무 긴 (>70자)
    bad_title_len = [r for r in page_records if r["title"] and (len(r["title"]) < 10 or len(r["title"]) > 70)]
    print(f"\n[8] title 길이 비정상 (<10자 또는 >70자): {len(bad_title_len)}개")
    for r in bad_title_len[:8]:
        print(f"  • {r['path']} → {len(r['title'])}자: {r['title'][:50]}")

    # 9. description 길이 비정상 — Google 권장 50~160자 (한글 기준 안전 범위)
    bad_desc_len = [r for r in page_records if r["desc"] and (len(r["desc"]) < 50 or len(r["desc"]) > 170)]
    print(f"\n[9] description 길이 비정상 (<50 또는 >170): {len(bad_desc_len)}개")
    for r in bad_desc_len[:8]:
        print(f"  • {r['path']} → {len(r['desc'])}자")

    # 10. OG 누락
    missing_og = [r for r in page_records if not r["og_title"]]
    print(f"\n[10] og:title 누락: {len(missing_og)}개")
    for r in missing_og[:5]:
        print(f"  • {r['path']}")

    # 11. 이미지 alt 누락
    pages_with_bad_alt = [r for r in page_records if r["bad_alts"]]
    total_bad_alt = sum(len(r["bad_alts"]) for r in pages_with_bad_alt)
    print(f"\n[11] 이미지 alt 누락: {total_bad_alt}개 (페이지 {len(pages_with_bad_alt)}개)")
    for r in pages_with_bad_alt[:5]:
        print(f"  • {r['path']} → {len(r['bad_alts'])}개")

    # 12. lang 속성
    no_lang = [r for r in page_records if not r["lang"]]
    print(f"\n[12] <html lang> 누락: {len(no_lang)}개")

    # 13. viewport 누락
    no_vp = [r for r in page_records if not r["viewport"]]
    print(f"\n[13] viewport meta 누락: {len(no_vp)}개")

    # 14. JSON-LD 없는 페이지
    no_ld = [r for r in page_records if r["jsonld_count"] == 0]
    print(f"\n[14] JSON-LD 구조화 데이터 누락: {len(no_ld)}개")
    for r in no_ld[:8]:
        print(f"  • {r['path']}")

    # 15. 너무 짧은 페이지 (thin content, <2000자)
    thin = [r for r in page_records if r["page_chars"] < 2000]
    print(f"\n[15] thin content 의심 (전체 텍스트 <2000자): {len(thin)}개")
    for r in sorted(thin, key=lambda r: r["page_chars"])[:5]:
        print(f"  • {r['path']} → {r['page_chars']}자")

    # ===== 종합 점수 =====
    issues_count = (
        len(dup_titles) + len(dup_desc) + len(dup_canonical) +
        len(missing_canonical) + len(missing_title) + len(missing_desc) +
        len(bad_h1) + len(bad_title_len) + len(bad_desc_len) +
        len(missing_og) + len(pages_with_bad_alt) + len(no_lang) +
        len(no_vp) + len(no_ld) + len(thin)
    )
    print("\n" + "=" * 70)
    print(f" 총 이슈 발견: {issues_count}건")
    print("=" * 70)


if __name__ == "__main__":
    audit()

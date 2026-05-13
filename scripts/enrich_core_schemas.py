#!/usr/bin/env python3
"""
모든 페이지에 Google 핵심 스키마(BreadcrumbList + Organization + WebSite)
를 항상 제공하도록 보강.

전략:
- 페이지 path 에서 자동으로 브레드크럼 경로 추론
- 기존 JSON-LD 가 있으면 그 옆에 새 <script> 블록을 추가
- 이미 모든 핵심 스키마가 있으면 건너뜀
"""

from __future__ import annotations
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://massagealbago.kr"

# 디렉토리 → 카테고리 한글명
DIR_LABELS = {
    "jobs": "구인공고",
    "partner-stores": "제휴업소",
    "resumes": "이력서 등록",
    "partners": "업체 가입",
    "ads": "광고 상품안내",
    "guide": "시술별 가이드",
    "magazine": "매거진",
    "support": "고객지원",
    "about": "회사 소개",
    "inquiry": "광고 문의",
}

REGION_LABELS = {
    "seoul": "서울", "gyeonggi": "경기", "incheon": "인천", "busan": "부산",
    "daegu": "대구", "daejeon": "대전", "gwangju": "광주", "ulsan": "울산",
    "sejong": "세종", "gangwon": "강원", "chungbuk": "충북", "chungnam": "충남",
    "gyeongbuk": "경북", "gyeongnam": "경남", "jeonbuk": "전북", "jeonnam": "전남",
    "jeju": "제주",
}

ORG = {
    "@type": "Organization",
    "@id": f"{DOMAIN}/#org",
    "name": "마사지알바고",
    "alternateName": "MassageAlbaGo",
    "legalName": "YH LAB",
    "url": f"{DOMAIN}/",
    "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/images/logo/logo.png"},
    "telephone": "+82-508-202-4690",
    "email": "hello@massage-albago.kr",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "청석로 268",
        "addressLocality": "파주시",
        "addressRegion": "경기도",
        "addressCountry": "KR",
    },
    "founder": {"@type": "Person", "name": "김수환"},
    "areaServed": {"@type": "Country", "name": "대한민국"},
    "sameAs": [
        "https://www.linkedin.com/in/%EB%B0%B1%ED%98%B8-%EA%B0%95-a84273261/",
        "https://medium.com/@88smartbro88",
        "https://x.com/gugeulmake84173",
    ],
}

WEBSITE = {
    "@type": "WebSite",
    "@id": f"{DOMAIN}/#website",
    "url": f"{DOMAIN}/",
    "name": "마사지알바고",
    "inLanguage": "ko-KR",
    "publisher": {"@id": f"{DOMAIN}/#org"},
    "potentialAction": {
        "@type": "SearchAction",
        "target": {
            "@type": "EntryPoint",
            "urlTemplate": f"{DOMAIN}/jobs/?q={{search_term_string}}",
        },
        "query-input": "required name=search_term_string",
    },
}


def page_title_from_html(html: str) -> str:
    m = re.search(r"<title>([^<]*?)\s*(?:\|.*)?</title>", html)
    return m.group(1).strip() if m else ""


def page_h1_from_html(html: str) -> str:
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", html)
    return m.group(1).strip() if m else ""


def build_breadcrumb(rel_path: str, html: str) -> dict | None:
    """파일 경로에서 브레드크럼 자동 추론. 깊이 1~3 모두 지원."""
    page_url = f"{DOMAIN}/{rel_path}".replace("index.html", "")
    items = [{"name": "홈", "url": f"{DOMAIN}/"}]

    parts = rel_path.split("/")
    # 루트 index.html / 404.html — 브레드크럼 단일 항목
    if len(parts) == 1:
        if parts[0] in ("index.html", "404.html"):
            return None  # 루트엔 breadcrumb 불필요 (또는 짧음)

    # 첫 디렉토리 — 카테고리 허브
    if len(parts) >= 1:
        cat = parts[0]
        cat_label = DIR_LABELS.get(cat, cat)
        items.append({
            "name": cat_label,
            "url": f"{DOMAIN}/{cat}/",
        })

    # 두 번째 — sub-region 또는 sub-page
    if len(parts) >= 2:
        sub = parts[-1].replace(".html", "")
        # 17개 시도 sub-region
        if sub in REGION_LABELS:
            sub_label = REGION_LABELS[sub]
        else:
            # 시·도 + 자치구 형태: jobs/seoul/gangnam.html
            # html 의 h1 또는 title 에서 추출
            sub_label = page_h1_from_html(html) or page_title_from_html(html)
            if not sub_label:
                sub_label = sub
        # 3단계 (jobs/seoul/gangnam.html) 인 경우 시·도 중간 단계 추가
        if len(parts) == 3:
            region = parts[1]
            region_label = REGION_LABELS.get(region, region)
            items.append({
                "name": region_label,
                "url": f"{DOMAIN}/{parts[0]}/{region}.html",
            })
        items.append({
            "name": sub_label,
            "url": page_url,
        })

    if len(items) < 2:
        return None

    return {
        "@type": "BreadcrumbList",
        "@id": f"{page_url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": it["name"], "item": it["url"]}
            for i, it in enumerate(items)
        ],
    }


def build_supplement(rel_path: str, html: str) -> list[dict]:
    """현재 페이지에 빠진 핵심 스키마만 보충."""
    nodes = []
    has_org = '"@type": "Organization"' in html or '"@type":"Organization"' in html
    has_website = '"@type": "WebSite"' in html or '"@type":"WebSite"' in html
    has_breadcrumb = '"@type": "BreadcrumbList"' in html or '"@type":"BreadcrumbList"' in html

    if not has_breadcrumb:
        bc = build_breadcrumb(rel_path, html)
        if bc:
            nodes.append(bc)
    if not has_org:
        nodes.append(ORG)
    if not has_website:
        nodes.append(WEBSITE)
    return nodes


def main():
    enriched = 0
    skipped = 0
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        rel = str(p.relative_to(ROOT))
        html = p.read_text(encoding="utf-8")
        nodes = build_supplement(rel, html)
        if not nodes:
            skipped += 1
            continue
        block = (
            '<script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@graph": nodes},
                         ensure_ascii=False, indent=2)
            + '\n</script>'
        )
        new_html, n = re.subn(r'</body>', block + "\n</body>", html, count=1)
        if n == 1:
            p.write_text(new_html, encoding="utf-8")
            enriched += 1

    print(f"enriched: {enriched}")
    print(f"skipped (already complete): {skipped}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
JSON-LD 구조화 데이터 누락 페이지에 일괄 주입.
Google 권장 schema.org 타입을 페이지 성격별로 맞춤 부여.
"""

from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://albago.pages.dev"

# 공통 Organization 정의 - 모든 페이지가 참조
ORG = {
    "@type": "Organization",
    "@id": f"{DOMAIN}/#org",
    "name": "마사지알바고",
    "alternateName": "MassageAlbaGo",
    "legalName": "YH LAB",
    "url": f"{DOMAIN}/",
    "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/images/logo/logo.png"},
    "description": "전국 마사지·스파·테라피 업종 구인구직 플랫폼",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "청석로 268",
        "addressLocality": "파주시",
        "addressRegion": "경기도",
        "addressCountry": "KR",
    },
    "telephone": "+82-508-202-4690",
    "email": "hello@massage-albago.kr",
    "founder": {"@type": "Person", "name": "김수환"},
    "areaServed": {"@type": "Country", "name": "대한민국"},
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


def breadcrumb(items: list[tuple[str, str]], page_id: str) -> dict:
    return {
        "@type": "BreadcrumbList",
        "@id": f"{page_id}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": url,
            }
            for i, (name, url) in enumerate(items)
        ],
    }


# 페이지별 JSON-LD 정의
PAGE_GRAPHS: dict[str, list[dict]] = {
    "jobs/index.html": [
        breadcrumb([("홈", f"{DOMAIN}/"), ("구인공고", f"{DOMAIN}/jobs/")], f"{DOMAIN}/jobs/"),
        {
            "@type": "CollectionPage",
            "@id": f"{DOMAIN}/jobs/",
            "url": f"{DOMAIN}/jobs/",
            "name": "마사지 구인공고",
            "description": "전국 마사지·스파·테라피 채용 공고 모음. 사업자 인증을 마친 업체 공고만 노출됩니다.",
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "publisher": {"@id": f"{DOMAIN}/#org"},
            "breadcrumb": {"@id": f"{DOMAIN}/jobs/#breadcrumb"},
        },
        ORG,
        WEBSITE,
    ],
    "partner-stores/index.html": [
        breadcrumb([("홈", f"{DOMAIN}/"), ("제휴업소", f"{DOMAIN}/partner-stores/")], f"{DOMAIN}/partner-stores/"),
        {
            "@type": "CollectionPage",
            "@id": f"{DOMAIN}/partner-stores/",
            "url": f"{DOMAIN}/partner-stores/",
            "name": "제휴업소",
            "description": "마사지알바고 제휴 매장 안내",
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "publisher": {"@id": f"{DOMAIN}/#org"},
            "breadcrumb": {"@id": f"{DOMAIN}/partner-stores/#breadcrumb"},
        },
        ORG,
        WEBSITE,
    ],
    "magazine/index.html": [
        breadcrumb([("홈", f"{DOMAIN}/"), ("매거진", f"{DOMAIN}/magazine/")], f"{DOMAIN}/magazine/"),
        {
            "@type": "Blog",
            "@id": f"{DOMAIN}/magazine/",
            "url": f"{DOMAIN}/magazine/",
            "name": "마사지알바고 매거진",
            "description": "관리사·테라피스트를 위한 구직 노하우, 업계 인사이트, 현직자 이야기. 매주 월요일 한 편씩 업데이트.",
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "publisher": {"@id": f"{DOMAIN}/#org"},
            "breadcrumb": {"@id": f"{DOMAIN}/magazine/#breadcrumb"},
        },
        ORG,
        WEBSITE,
    ],
    "inquiry/index.html": [
        breadcrumb([("홈", f"{DOMAIN}/"), ("광고 문의", f"{DOMAIN}/inquiry/")], f"{DOMAIN}/inquiry/"),
        {
            "@type": "ContactPage",
            "@id": f"{DOMAIN}/inquiry/",
            "url": f"{DOMAIN}/inquiry/",
            "name": "광고·제휴 문의",
            "description": "마사지알바고 광고 상품 및 매장 제휴 문의 페이지",
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "publisher": {"@id": f"{DOMAIN}/#org"},
            "breadcrumb": {"@id": f"{DOMAIN}/inquiry/#breadcrumb"},
        },
        ORG,
        WEBSITE,
    ],
    "support/index.html": [
        breadcrumb([("홈", f"{DOMAIN}/"), ("고객지원", f"{DOMAIN}/support/")], f"{DOMAIN}/support/"),
        {
            "@type": "WebPage",
            "@id": f"{DOMAIN}/support/",
            "url": f"{DOMAIN}/support/",
            "name": "고객지원·이용 안내",
            "description": "마사지알바고 이용 안내, 안전 가이드, 자주 묻는 질문 모음",
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "publisher": {"@id": f"{DOMAIN}/#org"},
            "breadcrumb": {"@id": f"{DOMAIN}/support/#breadcrumb"},
        },
        ORG,
        WEBSITE,
    ],
    "partners/index.html": [
        breadcrumb([("홈", f"{DOMAIN}/"), ("업체 가입", f"{DOMAIN}/partners/")], f"{DOMAIN}/partners/"),
        {
            "@type": "Service",
            "@id": f"{DOMAIN}/partners/",
            "url": f"{DOMAIN}/partners/",
            "name": "마사지알바고 업체 가입",
            "description": "마사지·스파·테라피 업종 사업자 채용공고 게재 서비스. 사업자 인증 후 30일 무료 게재.",
            "provider": {"@id": f"{DOMAIN}/#org"},
            "areaServed": {"@type": "Country", "name": "대한민국"},
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "breadcrumb": {"@id": f"{DOMAIN}/partners/#breadcrumb"},
        },
        ORG,
        WEBSITE,
    ],
    "guide/index.html": [
        breadcrumb([("홈", f"{DOMAIN}/"), ("시술별 가이드", f"{DOMAIN}/guide/")], f"{DOMAIN}/guide/"),
        {
            "@type": "CollectionPage",
            "@id": f"{DOMAIN}/guide/",
            "url": f"{DOMAIN}/guide/",
            "name": "시술 분야별 마사지 관리사 채용 가이드",
            "description": "스웨디시·아로마·타이·1인샵·피부관리·체형관리·왁싱·카운터·토탈샵까지 14개 분야 가이드.",
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "publisher": {"@id": f"{DOMAIN}/#org"},
            "breadcrumb": {"@id": f"{DOMAIN}/guide/#breadcrumb"},
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": 14,
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": name, "url": f"{DOMAIN}/guide/{slug}"}
                    for i, (slug, name) in enumerate([
                        ("single-shop.html", "1인샵"),
                        ("swedish.html", "스웨디시"),
                        ("aroma.html", "아로마"),
                        ("sports.html", "스포츠·경락"),
                        ("spa.html", "스파·매니저"),
                        ("thai.html", "타이마사지"),
                        ("chinese.html", "중국마사지"),
                        ("lomi.html", "로미로미"),
                        ("skincare.html", "피부관리"),
                        ("body-shaping.html", "체형관리"),
                        ("waxing.html", "왁싱"),
                        ("counter.html", "카운터"),
                        ("total-shop.html", "토탈샵"),
                        ("homecare.html", "홈케어"),
                    ])
                ],
            },
        },
        ORG,
        WEBSITE,
    ],
    "about/index.html": [
        breadcrumb([("홈", f"{DOMAIN}/"), ("회사 소개", f"{DOMAIN}/about/")], f"{DOMAIN}/about/"),
        {
            "@type": "AboutPage",
            "@id": f"{DOMAIN}/about/",
            "url": f"{DOMAIN}/about/",
            "name": "마사지알바고 회사 소개",
            "description": "YH LAB 이 운영하는 전국 마사지 구인구직 플랫폼 마사지알바고의 회사 정보, 운영 원칙, 검증 시스템 안내",
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "mainEntity": {"@id": f"{DOMAIN}/#org"},
            "breadcrumb": {"@id": f"{DOMAIN}/about/#breadcrumb"},
        },
        ORG,
        WEBSITE,
    ],
    "resumes/index.html": [
        breadcrumb([("홈", f"{DOMAIN}/"), ("이력서 등록", f"{DOMAIN}/resumes/")], f"{DOMAIN}/resumes/"),
        {
            "@type": "Service",
            "@id": f"{DOMAIN}/resumes/",
            "url": f"{DOMAIN}/resumes/",
            "name": "관리사 이력서 등록",
            "description": "마사지·스파 관리사 이력서 무료 등록. 사업자 인증을 마친 업체에서 매칭 연락이 갑니다.",
            "provider": {"@id": f"{DOMAIN}/#org"},
            "areaServed": {"@type": "Country", "name": "대한민국"},
            "audience": {"@type": "Audience", "audienceType": "마사지·스파·테라피 관리사"},
            "inLanguage": "ko-KR",
            "isPartOf": {"@id": f"{DOMAIN}/#website"},
            "breadcrumb": {"@id": f"{DOMAIN}/resumes/#breadcrumb"},
        },
        ORG,
        WEBSITE,
    ],
}


# 시술 가이드 8개 — 동일 구조의 Article + Breadcrumb 자동 생성
_guide_meta = {
    "spa.html": ("스파·매니저 관리사 채용·구직 가이드", "스파·매니저"),
    "homecare.html": ("홈케어(출장) 관리사 채용·구직 가이드", "홈케어 출장"),
    "chinese.html": ("중국마사지 관리사 채용·구직 가이드", "중국마사지"),
    "lomi.html": ("로미로미 테라피스트 채용·구직 가이드", "로미로미"),
    "swedish.html": ("스웨디시 관리사 채용·구직 가이드", "스웨디시"),
    "sports.html": ("스포츠·경락 관리사 채용·구직 가이드", "스포츠·경락"),
    "thai.html": ("타이마사지 관리사 채용·구직 가이드", "타이마사지"),
    "aroma.html": ("아로마 테라피스트 채용·구직 가이드", "아로마"),
}
for fname, (title, category) in _guide_meta.items():
    url = f"{DOMAIN}/guide/{fname}"
    PAGE_GRAPHS[f"guide/{fname}"] = [
        breadcrumb([("홈", f"{DOMAIN}/"), ("시술별 가이드", f"{DOMAIN}/guide/"), (category, url)], url),
        {
            "@type": "Article",
            "@id": f"{url}#article",
            "headline": title,
            "description": f"{category} 분야 관리사·테라피스트 채용 정보. 자격 요건, 평균 급여, 채용 시장 현황 안내.",
            "author": {"@id": f"{DOMAIN}/#org"},
            "publisher": {"@id": f"{DOMAIN}/#org"},
            "mainEntityOfPage": {"@id": url},
            "inLanguage": "ko-KR",
            "articleSection": category,
            "image": f"{DOMAIN}/favicon.svg",
        },
        ORG,
        WEBSITE,
    ]


def build_jsonld_block(graph: list[dict]) -> str:
    payload = {"@context": "https://schema.org", "@graph": graph}
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + '\n</script>'
    )


def inject(path_str: str, graph: list[dict]) -> bool:
    p = ROOT / path_str
    if not p.exists():
        print(f"[skip] {path_str} not found")
        return False
    html = p.read_text(encoding="utf-8")
    if 'application/ld+json' in html:
        print(f"[skip] {path_str} already has JSON-LD")
        return False
    block = build_jsonld_block(graph)
    new_html, n = re.subn(r'</body>', block + "\n</body>", html, count=1)
    if n == 0:
        print(f"[warn] {path_str} has no </body>")
        return False
    p.write_text(new_html, encoding="utf-8")
    print(f"[ok] {path_str}")
    return True


def main() -> int:
    count = 0
    for path, graph in PAGE_GRAPHS.items():
        if inject(path, graph):
            count += 1
    print(f"\nTotal injected: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

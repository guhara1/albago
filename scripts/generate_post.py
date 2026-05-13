#!/usr/bin/env python3
"""
마사지알바고 매거진 자동 생성기.

- topic_queue.json 에서 used:false 인 다음 주제 1개 선택
- Anthropic API 로 사람 글 톤의 본문 생성 (AI 탐지 회피 강조)
- 품질 가드 (분량/구조/금지어/AI 정형구) 통과 후 HTML 저장
- /magazine/index.html 자동 갱신 블록 갱신
- /sitemap.xml 에 새 글 URL 추가
- topic 을 used:true 처리
- IndexNow / 사이트맵 ping
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from anthropic import Anthropic

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://albago.pages.dev"
KST = timezone(timedelta(hours=9))

POSTS_DIR = ROOT / "magazine" / "posts"
QUEUE_PATH = ROOT / "scripts" / "topic_queue.json"
MAGAZINE_INDEX = ROOT / "magazine" / "index.html"
SITEMAP = ROOT / "sitemap.xml"
MAGAZINE_RSS = ROOT / "magazine" / "rss.xml"

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-4-7")

BANNED_TERMS = [
    "1등", "최고의", "100%", "완벽", "보장", "베스트", "1위",
    "추천 1순위", "치료된다", "낫는다", "효과가 확실", "무조건",
    "절대적", "유일한",
]

AI_CLICHE = [
    "또한", "결론적으로", "정리하자면", "마지막으로", "다음과 같이",
    "특히 중요한 것은", "본 글에서는", "이 글에서는 다음과 같이",
    "여러분",
]


def load_queue() -> dict:
    return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))


def save_queue(q: dict) -> None:
    QUEUE_PATH.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")


def pick_topic(q: dict) -> dict | None:
    for t in q["topics"]:
        if not t.get("used"):
            return t
    return None


COMMON_BLOCK = """[분량]
한글 기준 본문 합계 2,500자 ± 150자.

[구조]
- 본문은 H2 다섯 개. 각 제목 앞에 "1. ", "2. ", "3. ", "4. ", "5. ".
- 각 H2 아래는 평문 문단만. 목록(불릿/번호), 표, 굵은체, 이탤릭, 강조부호, 코드블록 모두 금지.
- 각 H2 본문은 약 500자.

[톤 — AI 티가 나면 실패. 가장 중요한 항목.]
이 글은 "논리적 완성도"보다 "사람 말투의 혼란과 감정의 앞섬"이 먼저입니다. 잘 정리된 컨설팅 글이 아니라, 그 일을 직접 해 본 사람이 카페에 앉아 친한 후배에게 이야기를 풀어주는 톤이어야 합니다.

1. 자연스러운 한국어 구어체. 너무 매끄럽거나 정형적이지 않게.
2. 다음 AI 정형 표현 금지: "또한", "결론적으로", "정리하자면", "마지막으로", "다음과 같이", "본 글에서는", "여러분".
3. 사람다운 군더더기 표현을 군데군데 섞기: "솔직히", "사실", "근데 이게", "어쩌면", "그러니까", "말이 좀 이상한데", "음".
4. 종결어미를 한 패턴으로 통일하지 말 것. "~죠", "~거든요", "~잖아요", "~더라고요", "~합니다"를 한 글 안에 자연스럽게 섞으세요.
5. 문장 길이를 다양화 — 짧고 끊긴 문장과 약간 늘어진 문장을 한 문단 안에 섞으세요. 가끔 두세 글자짜리 짧은 문장을 일부러 넣으세요.
6. 결론을 단정짓지 말 것. "이게 정답이다" 대신 "이 정도가 적당하더라" 식 여운.
7. 한 단락 안에서 감정이 살짝 흔들려도 됩니다. 처음엔 단단하게 말하다가 끝에 가서 자기 의심이 한 줄 들어와도 좋습니다.
8. 가끔 비문에 가까운 짧은 회상을 끼워 넣어도 됩니다. 예: "그날따라 손이 떨렸어요." 이런 식.
9. 통계·수치는 1~2개만 사용하고 출처를 단정짓지 마세요 ("들리는 말로는", "현장에서 보면 대충" 같은 톤).
10. 광고·홍보 톤 절대 금지. "추천드립니다", "이용해 보세요" 같은 권유형 어미는 피하세요.

[E-E-A-T — 본문 흐름에 자연스럽게 녹이기]
- Experience: 1인칭 시점이거나, 적어도 한 명의 구체적 인물 시나리오 1회 이상.
- Expertise: 현장에서 자주 마주치는 구체 숫자 1~2개 (시간·금액·연차·근무일수).
- Authority: 법적·안전 관련 한 줄 짚기 (4대보험, 근로계약서, 직업정보제공사업, 산재 등).
- Trust: 합법적 정상 영업·허위 공고 거르기 같은 안전 원칙을 자연스럽게 한 번.
별도 섹션을 두지 말고, 다섯 H2 본문 전체에 흩뿌리세요.

[Helpful content / 검색의도 부합]
- 사용자가 [검색 의도]에 적힌 그 질문을 들고 들어왔다는 사실을 1번 H2가 끝나기 전에 반드시 짚어 주세요.
- 모호하게 일반론으로 흐르지 말고, 구체적 상황(시간대, 지역, 연차, 매장 형태)에 묶어서 답하세요.

[스팸 금지]
- 키워드 반복(같은 키워드 5회 이상) 금지.
- 외부 링크 권유, 전화번호, 가격표, 할인 코드, 쿠폰 코드 금지.
- "꼭 이용하세요", "지금 신청하세요" 같은 직접 행동 유도 문구 금지.

[금지어]
"1등", "최고의", "100%", "보장", "완벽", "베스트", "1위", "추천 1순위", "치료된다", "낫는다", "효과가 확실", "무조건", "절대적", "유일한" 사용 금지.

[출력 형식]
오직 JSON 한 덩어리만 출력하세요. JSON 앞뒤 어떤 설명·인사·코드블록 마크다운도 붙이지 마세요.

{{
  "title": "60자 이내 제목 (클릭 유도되되 과장 없이, 사람 말투)",
  "description": "140자 이내 메타 디스크립션",
  "h2_1": "1. 첫 H2 제목 (10~28자)",
  "p_1": "약 500자 본문",
  "h2_2": "2. 두 번째 H2 제목",
  "p_2": "약 500자 본문",
  "h2_3": "3. 세 번째 H2 제목",
  "p_3": "약 500자 본문",
  "h2_4": "4. 네 번째 H2 제목",
  "p_4": "약 500자 본문",
  "h2_5": "5. 다섯 번째 H2 제목",
  "p_5": "약 500자 본문"
}}
"""

PROMPT = """당신은 "마사지알바고" 매거진의 한국인 작성자입니다.
마사지·스파·테라피 업계에서 직접 일해 본 사람의 시점으로, 관리사 구직과 마사지샵 채용·근무 환경을 사람의 일기·에세이처럼 풀어내는 글을 씁니다.
글 톤의 핵심은 "정돈된 컨설팅"이 아니라 "오래 일해 본 선배가 카페에서 후배에게 진심으로 말해 주는 느낌"입니다.

[주제]
{title}

[카테고리]
{category}

[검색 의도]
"{intent}"

[배경 시나리오 — 본문 안에 자연스럽게 녹일 것]
{scenario}

[지역 디테일 — 본문에 한두 번 자연스럽게 녹일 것]
{region_hint}
지역명이 어색하면 억지로 끼우지 마세요. 다만 "어디서나 그렇겠지만"이라는 식의 무색무취 표현으로만 끝내지는 마세요.

[제목 만드는 법]
- "마사지 구인구직" 같은 키워드를 제목에 그대로 박지 마세요. AI 글로 인식됩니다.
- 사람 입에서 나오는 표현을 쓰세요. "솔직히", "아무도 안 알려주는", "현장에서 보면", "처음엔 몰랐던", "1년 해보고 알았는데" 같은 살아 있는 어휘.
- 의문형·고백형·회상형 중 한 가지를 선택하세요.
- 위 [주제]를 그대로 쓰지 말고 한 번 비틀어 주세요.

[꼭 지킬 것]
- 1인칭 시점이 자연스러우면 사용 (저는, 제 친구가, 우리 매장에서). 다만 매 문단을 1인칭으로 시작하지는 마세요.
- 5개 H2 사이에 시간 흐름이나 시점 변화를 살짝 두세요 (입사 전 → 입사 직후 → 1년 뒤, 이런 식). 모든 H2가 같은 시점의 정보 나열이면 AI 글입니다.
- 본문 어디엔가 작은 후회나 망설임 한 줄을 넣어 주세요. 사람 글에는 그게 들어갑니다.

""" + COMMON_BLOCK


def call_claude(topic: dict, retry_hint: str = "") -> dict:
    client = Anthropic()
    prompt = PROMPT.format(
        title=topic["title"],
        category=topic.get("category", "구인구직"),
        intent=topic["search_intent"],
        scenario=topic.get("scenario", "(시나리오 없음 — 자유롭게)"),
        region_hint=topic.get("region_hint", "") or "(특정 지역 없음)",
    )
    if retry_hint:
        prompt += f"\n\n[재시도 안내]\n이전 출력에서 다음 문제가 있었습니다. 수정해 주세요:\n{retry_hint}\n"

    msg = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    raw = "".join(b.text for b in msg.content if b.type == "text").strip()
    # ``` 또는 ```json 으로 감싸진 경우 제거
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    # 본문 안에서 첫 { 부터 마지막 } 까지 안전하게 추출
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        raise ValueError(f"응답에서 JSON 블록을 찾지 못했습니다: {raw[:300]}")
    return json.loads(m.group(0))


def validate(article: dict) -> str:
    required = ["title", "description", "h2_1", "p_1", "h2_2", "p_2",
                "h2_3", "p_3", "h2_4", "p_4", "h2_5", "p_5"]
    for k in required:
        if k not in article or not str(article[k]).strip():
            return f"필수 키 '{k}' 누락 또는 빈 값"

    for i in range(1, 6):
        h = article[f"h2_{i}"].strip()
        if not h.startswith(f"{i}. "):
            return f"h2_{i} 가 '{i}. '로 시작하지 않음: {h[:40]}"

    body = "".join(article[f"p_{i}"] for i in range(1, 6))
    n = len(body)
    if n < 2200 or n > 2900:
        return f"본문 분량 부적합: {n}자 (목표 2350~2650)"

    for i in range(1, 6):
        p = article[f"p_{i}"]
        if re.search(r"[*_`]{1,}|<[a-zA-Z]+|^[-•·]\s", p, re.MULTILINE):
            return f"p_{i} 안에 서식 흔적이 포함됨"

    full = " ".join([article["title"], article["description"], body])
    for t in BANNED_TERMS:
        if t in full:
            return f"금지어 사용: {t}"

    # AI 정형구 빈출 검사
    cliche_hits = sum(full.count(c) for c in AI_CLICHE)
    if cliche_hits >= 5:
        return f"AI 정형 표현 과다 사용({cliche_hits}회)"

    return ""


def generate(topic: dict) -> dict:
    last_err = ""
    for attempt in range(3):
        article = call_claude(topic, retry_hint=last_err)
        err = validate(article)
        if not err:
            return article
        last_err = err
        print(f"[validate] 시도 {attempt+1} 실패: {err}", file=sys.stderr)
    raise RuntimeError(f"품질 검증 실패: {last_err}")


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def build_jsonld(title: str, description: str, post_url: str, iso_date: str,
                 body_chars: int, keywords: list, category: str,
                 toc_items: list[tuple[int, str]] | None = None) -> str:
    base = DOMAIN
    graph = [
        {
            "@type": "Article",
            "@id": f"{post_url}#article",
            "headline": title,
            "description": description,
            "datePublished": iso_date,
            "dateModified": iso_date,
            "author": {"@id": f"{base}/#org"},
            "publisher": {"@id": f"{base}/#org"},
            "mainEntityOfPage": {"@id": post_url},
            "inLanguage": "ko-KR",
            "wordCount": body_chars,
            "articleSection": category or "Magazine",
            "keywords": keywords,
            "image": f"{base}/favicon.svg",
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{post_url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{base}/"},
                {"@type": "ListItem", "position": 2, "name": "매거진", "item": f"{base}/magazine/"},
                {"@type": "ListItem", "position": 3, "name": title, "item": post_url},
            ],
        },
        {
            "@type": "Organization",
            "@id": f"{base}/#org",
            "name": "마사지알바고",
            "url": f"{base}/",
            "logo": {"@type": "ImageObject", "url": f"{base}/favicon.svg"},
        },
        {
            "@type": "WebSite",
            "@id": f"{base}/#website",
            "url": f"{base}/",
            "name": "마사지알바고",
            "inLanguage": "ko-KR",
            "publisher": {"@id": f"{base}/#org"},
        },
        {
            "@type": "WebPage",
            "@id": post_url,
            "url": post_url,
            "name": title,
            "isPartOf": {"@id": f"{base}/#website"},
            "breadcrumb": {"@id": f"{post_url}#breadcrumb"},
            "inLanguage": "ko-KR",
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": [".article h2", ".article p"],
            },
        },
    ]
    if toc_items:
        graph.append({
            "@type": "ItemList",
            "@id": f"{post_url}#toc",
            "name": "이 글에서 짚는 다섯 가지",
            "itemListOrder": "https://schema.org/ItemListOrderAscending",
            "numberOfItems": len(toc_items),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": pos,
                    "name": name,
                    "url": f"{post_url}#h2-{pos}",
                }
                for pos, name in toc_items
            ],
        })
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=2)


def render_html(topic: dict, article: dict, slug: str, post_url: str) -> str:
    now = datetime.now(KST)
    iso = now.strftime("%Y-%m-%dT%H:%M:%S+09:00")
    date_korean = now.strftime("%Y년 %m월 %d일")

    related_label = topic.get("related_label", "구직 가이드")
    category = topic.get("category", "매거진")

    sections_html = "\n".join(
        f'  <section id="sec-{i}">\n'
        f'    <h2 id="h2-{i}">{esc(article[f"h2_{i}"])}</h2>\n'
        f'    <p>{esc(article[f"p_{i}"]).replace(chr(10), "</p><p>")}</p>\n'
        f'  </section>'
        for i in range(1, 6)
    )

    # 본문 상단 TL;DR 카드: 다섯 H2 제목에서 "N. " 접두사를 떼고 한 줄씩
    # 각 항목은 해당 H2 로 점프하는 앵커 — 가독성 + SERP jump-to 링크 노출 기대
    num_prefix = re.compile(r"^[0-9]+\.\s*")
    lead_items = "\n".join(
        f'      <li><a href="#h2-{i}">' + esc(num_prefix.sub("", article[f"h2_{i}"])) + '</a></li>'
        for i in range(1, 6)
    )
    body_chars_for_lead = sum(len(article[f"p_{i}"]) for i in range(1, 6))
    read_minutes = max(2, round(body_chars_for_lead / 500))
    lead_html = f'''  <aside class="post-lead">
    <span class="post-lead__title">한눈에 보기</span>
    <h2>이 글에서 짚는 다섯 가지</h2>
    <ul>
{lead_items}
    </ul>
  </aside>
  <div class="post-meta-strip">
    <span class="chip chip--cat">{esc(category)}</span>
    <span class="chip">읽는 데 약 {read_minutes}분</span>
    <span class="chip">{date_korean}</span>
  </div>'''

    # 관련 링크 카드 그리드 마크업 — href 패턴으로 카테고리/아이콘 자동 매핑
    def _classify(href: str) -> tuple[str, str, str]:
        h = href.lower()
        if "/jobs/" in h:
            return ("구인공고", "💼", "")
        if "/resumes/" in h:
            return ("이력서", "📝", "amber")
        if "/partners/" in h:
            return ("업체", "🏢", "slate")
        if "/partner-stores/" in h:
            return ("제휴업소", "🤝", "slate")
        if "/guide/swedish" in h: return ("시술 가이드", "🌿", "green")
        if "/guide/aroma" in h:   return ("시술 가이드", "🌸", "green")
        if "/guide/thai" in h:    return ("시술 가이드", "🌏", "green")
        if "/guide/lomi" in h:    return ("시술 가이드", "🌺", "green")
        if "/guide/spa" in h:     return ("시술 가이드", "💆", "green")
        if "/guide/sports" in h:  return ("시술 가이드", "🏋", "green")
        if "/guide/homecare" in h:return ("시술 가이드", "🏠", "green")
        if "/guide/chinese" in h: return ("시술 가이드", "🍀", "green")
        if "/guide/" in h:        return ("이용 안내", "📖", "")
        if "/support/" in h:      return ("안전·고객지원", "🛡", "rose")
        if "/about/" in h:        return ("회사 소개", "ℹ️", "slate")
        if "/ads/" in h:          return ("상품 안내", "🎯", "amber")
        if "/magazine/" in h:     return ("매거진", "📰", "")
        return ("바로 가기", "🔗", "slate")

    related_cards = "\n".join(
        (
            lambda c, i, tone: (
                f'      <a href="{esc(r["href"])}" class="related-card">\n'
                f'        <span class="related-card__icon {tone}" aria-hidden="true">{i}</span>\n'
                f'        <span class="related-card__body">\n'
                f'          <span class="related-card__cat">{esc(c)}</span>\n'
                f'          <span class="related-card__title">{esc(r["text"])}</span>\n'
                f'        </span>\n'
                f'        <span class="related-card__arrow" aria-hidden="true">→</span>\n'
                f'      </a>'
            )
        )(*_classify(r["href"]))
        for r in topic.get("related_links", [])
    )

    keywords = ["마사지 구인구직", "관리사 채용", "마사지알바고", category]
    if topic.get("region_hint"):
        keywords.append(topic["region_hint"])

    body_chars = sum(len(article[f"p_{i}"]) for i in range(1, 6))
    toc_items = [
        (i, num_prefix.sub("", article[f"h2_{i}"]))
        for i in range(1, 6)
    ]
    jsonld_str = build_jsonld(
        title=article["title"],
        description=article["description"],
        post_url=post_url,
        iso_date=iso,
        body_chars=body_chars,
        keywords=keywords,
        category=category,
        toc_items=toc_items,
    )

    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(article["title"])} | 마사지알바고 매거진</title>
<meta name="description" content="{esc(article["description"])}" />
<meta name="keywords" content="{esc(", ".join(keywords))}" />
<meta name="author" content="마사지알바고 편집팀" />
<meta name="theme-color" content="#1E40AF" />
<link rel="icon" type="image/svg+xml" href="../../favicon.svg" />
<link rel="apple-touch-icon" href="../../favicon.svg" />
<link rel="manifest" href="../../manifest.webmanifest" />
<link rel="canonical" href="{post_url}" />
<meta property="og:title" content="{esc(article["title"])}" />
<meta property="og:description" content="{esc(article["description"])}" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="마사지알바고" />
<meta property="og:url" content="{post_url}" />
<meta property="og:image" content="{DOMAIN}/favicon.svg" />
<meta property="article:section" content="{esc(category)}" />
<meta property="article:published_time" content="{iso}" />
<link rel="stylesheet" href="../../css/style.css" />
</head>
<body class="magazine-post-body">

<div class="topbar"><div class="container">
  <a href="../../guide/index.html">이용 안내</a>
  <a href="../../support/index.html#safety">안전 가이드</a>
  <a href="../../partners/index.html">제휴 문의</a>
</div></div>

<header class="site-header"><div class="container header-inner">
  <a href="../../index.html" class="brand"><img src="/images/logo/logo.png" alt="마사지알바GO" class="brand-img" /></a>
  <nav class="main-nav" aria-label="주메뉴">
    <a href="../../jobs/index.html">구인공고</a>
    <a href="../../partner-stores/index.html">제휴업소</a>
    <a href="../../ads/index.html">상품안내</a>
    <a href="../../resumes/index.html">이력서 등록</a>
    <a href="../../partners/index.html">업체 가입</a>
    <a href="../../guide/index.html">시술별 가이드</a>
    <a href="../index.html" class="active">매거진</a>
    <a href="../../about/index.html">소개</a>
  </nav>
  <div class="header-cta">
    <a href="../../jobs/index.html" class="btn btn-primary">구인공고 보기</a>
  </div>
  <button class="menu-toggle" aria-label="메뉴 열기" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
</div></header>

<section class="page-header"><div class="container">
  <div class="breadcrumb"><a href="../../index.html">홈</a><span class="sep">/</span><a href="../index.html">매거진</a><span class="sep">/</span><span>{esc(article["title"])}</span></div>
  <h1>{esc(article["title"])}</h1>
  <p class="post-meta">{date_korean} · 마사지알바고 매거진 · {esc(category)}</p>
</div></section>

<div class="container">
{lead_html}
  <article class="article">
{sections_html}
  </article>

  <aside class="callout" style="margin: 32px 0;">
    <strong>안전 안내</strong> 이 글은 합법적·정상 영업 매장과 정상 구직 활동을 전제로 작성되었습니다.
    선입금 요구, 신분증·통장 사본 요구, 비정상 야간 운영, 허위 채용 공고 등은
    <a href="../../support/index.html#safety">안전 가이드</a>를 참고해 거르세요. 4대보험·근로계약서 작성은 정상 매장에서 당연히 진행되는 절차입니다.
  </aside>

  <section class="related-section" aria-label="관련 정보">
    <div class="related-section__head">
      <span class="related-section__eyebrow">함께 보면 좋은 곳</span>
      <h2 class="related-section__title">사이트 둘러보기</h2>
      <span class="related-section__sub">{esc(related_label)}</span>
    </div>
    <div class="related-grid">
{related_cards}
    </div>
  </section>
</div>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand"><img src="/images/logo/logo-sm.png" alt="마사지알바GO" class="footer-logo-img" /></div>
        <p>전국 마사지·스파·테라피 구인구직 플랫폼.<br>검증된 사업자의 공고와 검증된 인재를 한곳에서.</p>
      </div>
      <nav class="footer-nav">
        <h4>구인·구직</h4>
        <ul>
          <li><a href="../../jobs/index.html">전체 구인공고</a></li>
          <li><a href="../../partner-stores/index.html">제휴업소</a></li>
          <li><a href="../../ads/index.html">상품안내</a></li>
          <li><a href="../../resumes/index.html">이력서 등록</a></li>
          <li><a href="../../partners/index.html">업체 가입</a></li>
          <li><a href="../../guide/index.html">시술별 가이드</a></li>
        </ul>
      </nav>
      <nav class="footer-nav">
        <h4>지역별</h4>
        <ul>
          <li><a href="../../jobs/seoul.html">서울</a></li>
          <li><a href="../../jobs/gyeonggi.html">경기</a></li>
          <li><a href="../../jobs/busan.html">부산</a></li>
          <li><a href="../../jobs/index.html">전체 지역</a></li>
        </ul>
      </nav>
      <nav class="footer-nav">
        <h4>고객지원</h4>
        <ul>
          <li><a href="../../guide/index.html">이용 안내</a></li>
          <li><a href="../../support/index.html#safety">안전 가이드</a></li>
          <li><a href="../index.html">매거진</a></li>
          <li><a href="../../about/index.html">회사 소개</a></li>
        </ul>
      </nav>
    </div>
    <div class="footer-bottom">
      <p class="footer-legal">상호: YH LAB · 대표: 김수환 · 사업자등록번호: 815-26-00585 · 직업정보제공사업신고번호: J1802020260002</p>
      <p class="footer-legal">사업장소재지: 경기도 파주시 청석로 268 · 고객센터: 0508-202-4690 (평일 10:00~19:00) · 이메일: hello@massage-albago.kr</p>
      <p>© 2026 마사지알바고. All rights reserved.</p>
    </div>
  </div>
</footer>

<script src="../../js/main.js"></script>

<script type="application/ld+json">
{jsonld_str}
</script>
</body></html>
'''


# ----- 매거진 인덱스 갱신 -----

INDEX_MARK_START = "<!-- AUTO_POSTS_START -->"
INDEX_MARK_END = "<!-- AUTO_POSTS_END -->"


def list_posts() -> list[dict]:
    posts = []
    if not POSTS_DIR.exists():
        return posts
    for p in sorted(POSTS_DIR.glob("*.html"), reverse=True):
        html = p.read_text(encoding="utf-8")
        title_m = re.search(r"<title>([^<|]+?)\s*\|", html)
        desc_m = re.search(r'<meta name="description" content="([^"]+)"', html)
        date_m = re.search(r'<p class="post-meta">([^<·]+?)\s*·', html)
        cat_m = re.search(r'<meta property="article:section" content="([^"]+)"', html)
        if not title_m:
            continue
        posts.append({
            "slug": p.stem,
            "title": title_m.group(1).strip(),
            "description": desc_m.group(1).strip() if desc_m else "",
            "date": date_m.group(1).strip() if date_m else "",
            "category": cat_m.group(1).strip() if cat_m else "매거진",
        })
    return posts


def _cat_slug(cat: str) -> str:
    """카테고리 이름을 CSS 클래스용 슬러그로 (공백 제거)."""
    return (cat or "default").replace(" ", "").replace("·", "").strip() or "default"


def _read_min(desc: str) -> int:
    """본문 분량에서 대략 읽기 시간(분) 추정. 인덱스에선 description 만 가지므로
    description 길이로 근사하지 않고 기본 5분 표기."""
    return 5


def update_magazine_index() -> None:
    posts = list_posts()

    # 큐에서 곧 발행될 토픽 / 남은 전체 토픽 수
    upcoming: list[dict] = []
    total_unused = 0
    try:
        queue = load_queue()
        unused_all = [t for t in queue.get("topics", []) if not t.get("used")]
        upcoming = unused_all[:3]
        total_unused = len(unused_all)
    except Exception:
        pass

    # 카테고리 칩 모음 (이미 발행된 글 + 예정 토픽에서 unique)
    cats_seen: list[str] = []
    for p in posts:
        c = p.get("category", "매거진")
        if c not in cats_seen:
            cats_seen.append(c)
    for t in upcoming:
        c = t.get("category", "매거진")
        if c not in cats_seen:
            cats_seen.append(c)
    chip_html = " ".join(
        f'<span class="mag-hero__chip">{esc(c)}</span>' for c in cats_seen[:8]
    )
    chips_block = f'<div class="mag-hero__chips">{chip_html}</div>' if chip_html else ''

    hero_html = f'''<section class="mag-hero">
  <div class="container">
    <div class="mag-hero__stats">
      <span><strong>{len(posts)}</strong>편 게시</span>
      <span class="dot"></span>
      <span>매주 월요일 1편 자동 업데이트</span>
      <span class="dot"></span>
      <span><strong>{total_unused}</strong>편 발행 예정</span>
    </div>
    {chips_block}
  </div>
</section>'''

    if not posts:
        # 글이 아예 없을 때: hero + coming만
        body_blocks = [hero_html]
    else:
        featured = posts[0]
        others = posts[1:13]
        f_cat = featured.get("category", "매거진")
        f_slug_cls = _cat_slug(f_cat)
        feat_html = f'''<section class="mag-section">
  <div class="container">
    <div class="mag-section__head">
      <span class="mag-section__eyebrow">📌 Featured</span>
      <h2 class="mag-section__title">가장 최근 글</h2>
      <span class="mag-section__sub">방금 올라온 따끈한 글</span>
    </div>
    <a href="posts/{featured["slug"]}.html" class="mag-featured">
      <div class="mag-featured__visual mag-bg--{f_slug_cls}">
        <span class="mag-featured__cat">{esc(f_cat)}</span>
        <h3>{esc(featured["title"])}</h3>
      </div>
      <div class="mag-featured__body">
        <p>{esc(featured["description"])}</p>
        <div class="mag-featured__meta">
          <span>{esc(featured["date"])}</span>
          <span class="dot"></span>
          <span>약 5분 읽기</span>
          <span class="mag-featured__cta">글 읽기 →</span>
        </div>
      </div>
    </a>
  </div>
</section>'''

        if others:
            cards = "\n".join(
                f'      <a href="posts/{p["slug"]}.html" class="mag-card">\n'
                f'        <div class="mag-card__visual mag-bg--{_cat_slug(p.get("category","매거진"))}">\n'
                f'          <span class="mag-card__cat">{esc(p.get("category","매거진"))}</span>\n'
                f'        </div>\n'
                f'        <div class="mag-card__body">\n'
                f'          <h3>{esc(p["title"])}</h3>\n'
                f'          <p>{esc(p["description"][:140])}</p>\n'
                f'          <div class="mag-card__meta">\n'
                f'            <span>{esc(p["date"])}</span>\n'
                f'            <span class="dot"></span>\n'
                f'            <span>약 5분 읽기</span>\n'
                f'          </div>\n'
                f'        </div>\n'
                f'      </a>'
                for p in others
            )
            grid_section = f'''
<section class="mag-section">
  <div class="container">
    <div class="mag-section__head">
      <span class="mag-section__eyebrow">Latest</span>
      <h2 class="mag-section__title">최근 매거진 글</h2>
      <span class="mag-section__sub">새 글은 매주 월요일 오전</span>
    </div>
    <div class="mag-card-grid">
{cards}
    </div>
  </div>
</section>'''
        else:
            grid_section = ""

        body_blocks = [hero_html, feat_html, grid_section]

    coming_section = ""
    if upcoming:
        coming_cards = "\n".join(
            f'      <div class="mag-card mag-card--coming">\n'
            f'        <div class="mag-card__visual mag-bg--{_cat_slug(t.get("category","매거진"))}">\n'
            f'          <span class="mag-card__cat">{esc(t.get("category","매거진"))}</span>\n'
            f'        </div>\n'
            f'        <div class="mag-card__body">\n'
            f'          <h3>{esc(t["title"])}</h3>\n'
            f'          <p>{esc((t.get("scenario") or t.get("search_intent", ""))[:140])}</p>\n'
            f'          <div class="mag-card__meta">\n'
            f'            <span>🗓 발행 예정</span>\n'
            f'          </div>\n'
            f'        </div>\n'
            f'      </div>'
            for t in upcoming
        )
        coming_section = f'''
<section class="mag-section mag-section--coming">
  <div class="container">
    <div class="mag-section__head">
      <span class="mag-section__eyebrow">🗓 Coming Soon</span>
      <h2 class="mag-section__title">곧 업데이트될 글</h2>
      <span class="mag-section__sub">다음 월요일 오전 09:00 KST</span>
    </div>
    <div class="mag-card-grid">
{coming_cards}
    </div>
  </div>
</section>'''

    block = f'''{INDEX_MARK_START}
{"".join(body_blocks)}{coming_section}
{INDEX_MARK_END}'''

    html = MAGAZINE_INDEX.read_text(encoding="utf-8")
    # body 에 magazine-index-page 클래스 추가 (없으면)
    if "<body class=\"magazine-index-page\">" not in html:
        html = html.replace("<body>", "<body class=\"magazine-index-page\">", 1)

    if INDEX_MARK_START in html and INDEX_MARK_END in html:
        html = re.sub(
            re.escape(INDEX_MARK_START) + r".*?" + re.escape(INDEX_MARK_END),
            block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    MAGAZINE_INDEX.write_text(html, encoding="utf-8")


# ----- 사이트맵 + RSS + 색인 ping -----

INDEXNOW_KEY = "albago1697b88e2c3b4f48a17e5d29c8a3e4b1"
INDEXNOW_KEY_LOCATION = f"{DOMAIN}/{INDEXNOW_KEY}.txt"
INDEXNOW_ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://yandex.com/indexnow",
]


def update_sitemap(post_url: str) -> None:
    today = datetime.now(KST).strftime("%Y-%m-%d")
    if not SITEMAP.exists():
        return
    text = SITEMAP.read_text(encoding="utf-8")
    if post_url in text:
        return
    entry = (
        f"  <url><loc>{post_url}</loc>"
        f"<lastmod>{today}</lastmod>"
        f"<changefreq>monthly</changefreq>"
        f"<priority>0.7</priority></url>\n"
    )
    text = text.replace("</urlset>", entry + "</urlset>")
    # /magazine/ lastmod 업데이트
    text = re.sub(
        r'(<loc>https://albago\.pages\.dev/magazine/</loc><lastmod>)[^<]+(</lastmod>)',
        rf'\g<1>{today}\g<2>',
        text,
    )
    SITEMAP.write_text(text, encoding="utf-8")


def update_rss() -> None:
    posts = list_posts()
    items = []
    for p in posts[:30]:
        url = f"{DOMAIN}/magazine/posts/{p['slug']}.html"
        pub_date = datetime.now(KST).strftime("%a, %d %b %Y %H:%M:%S +0900")
        items.append(
            f'    <item>\n'
            f'      <title><![CDATA[{p["title"]}]]></title>\n'
            f'      <link>{url}</link>\n'
            f'      <guid isPermaLink="true">{url}</guid>\n'
            f'      <description><![CDATA[{p["description"]}]]></description>\n'
            f'      <pubDate>{pub_date}</pubDate>\n'
            f'    </item>'
        )
    last_build = datetime.now(KST).strftime("%a, %d %b %Y %H:%M:%S +0900")
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        '  <channel>\n'
        '    <title>마사지알바고 매거진</title>\n'
        f'    <link>{DOMAIN}/magazine/</link>\n'
        f'    <atom:link href="{DOMAIN}/magazine/rss.xml" rel="self" type="application/rss+xml"/>\n'
        '    <description>마사지·스파·테라피 구인구직, 관리사 직업 정보, 업계 인사이트.</description>\n'
        '    <language>ko-KR</language>\n'
        f'    <lastBuildDate>{last_build}</lastBuildDate>\n'
        '    <generator>마사지알바고 Auto-Publisher</generator>\n'
        + "\n".join(items) + "\n"
        '  </channel>\n'
        '</rss>\n'
    )
    MAGAZINE_RSS.parent.mkdir(parents=True, exist_ok=True)
    MAGAZINE_RSS.write_text(rss, encoding="utf-8")


def ping_indexnow(post_url: str) -> None:
    payload = json.dumps({
        "host": "albago.pages.dev",
        "key": INDEXNOW_KEY,
        "keyLocation": INDEXNOW_KEY_LOCATION,
        "urlList": [post_url, f"{DOMAIN}/magazine/", f"{DOMAIN}/magazine/rss.xml", f"{DOMAIN}/sitemap.xml"],
    }).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    for ep in INDEXNOW_ENDPOINTS:
        try:
            req = urllib.request.Request(ep, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"[indexnow] {ep} → {resp.status}")
        except urllib.error.HTTPError as e:
            if e.code in (200, 202):
                print(f"[indexnow] {ep} → {e.code}")
            else:
                print(f"[indexnow] {ep} → {e.code}")
        except Exception as e:
            print(f"[indexnow] {ep} → 에러: {e}")


def ping_sitemap() -> None:
    sitemap_url = f"{DOMAIN}/sitemap.xml"
    for ping in [
        f"https://www.google.com/ping?sitemap={sitemap_url}",
        f"https://www.bing.com/ping?sitemap={sitemap_url}",
    ]:
        try:
            with urllib.request.urlopen(ping, timeout=10) as r:
                print(f"[sitemap-ping] {ping[:60]} → {r.status}")
        except Exception as e:
            print(f"[sitemap-ping] {ping[:60]} → 에러: {e}")


def main() -> int:
    queue = load_queue()
    topic = pick_topic(queue)
    if topic is None:
        print("[info] 모든 토픽이 소진되었습니다. topic_queue.json 에 새 토픽을 추가하세요.")
        return 0

    print(f"[info] 토픽 선택: {topic['slug']} - {topic['title']}")
    article = generate(topic)
    body_chars = sum(len(article[f'p_{i}']) for i in range(1, 6))
    print(f"[info] 본문 분량: {body_chars} 자")

    slug = topic["slug"]
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    post_path = POSTS_DIR / f"{slug}.html"
    post_url = f"{DOMAIN}/magazine/posts/{slug}.html"

    html = render_html(topic, article, slug, post_url)
    post_path.write_text(html, encoding="utf-8")
    print(f"[ok] 글 저장: {post_path.relative_to(ROOT)}")

    update_magazine_index()
    print(f"[ok] 매거진 인덱스 갱신")

    update_sitemap(post_url)
    print(f"[ok] 사이트맵 갱신")

    update_rss()
    print(f"[ok] RSS 피드 갱신")

    try:
        ping_indexnow(post_url)
        ping_sitemap()
    except Exception as e:
        print(f"[warn] 색인 ping 일부 실패: {e}")
    print(f"[ok] 색인 요청 ping 완료")

    topic["used"] = True
    topic["published_at"] = datetime.now(KST).strftime("%Y-%m-%d")
    save_queue(queue)
    print(f"[ok] 토픽 큐 갱신 (used: true)")

    return 0


if __name__ == "__main__":
    sys.exit(main())

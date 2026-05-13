#!/usr/bin/env python3
"""
모든 HTML 파일의 <footer class="site-footer"> 블록을 SEO/E-E-A-T 강화 푸터로 교체.

- 절대 경로(`/`) 사용 — 페이지 깊이 무관
- 시맨틱 HTML: <footer role="contentinfo"> / <address> / <time>
- Schema.org Microdata: Organization + PostalAddress
- NAP 명확 표기 (Name·Address·Phone) — 로컬 SEO
- 사업자 정보 + 직업정보제공사업 신고번호 (신뢰)
- 정책·약관·사이트맵·RSS 링크 (Discoverability)
- 카테고리 그룹 (구인구직 / 가이드 / 지역 / 정보)
"""

from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NEW_FOOTER = '''<footer class="site-footer" role="contentinfo">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand-col">
        <a href="/" class="footer-brand-link" aria-label="마사지알바고 홈으로 이동">
          <img src="/images/logo/logo-sm.png" alt="마사지알바GO 로고" class="footer-logo-img" width="160" height="40" />
        </a>
        <p class="footer-tagline">전국 마사지·스파·테라피 구인구직 플랫폼.<br>검증된 사업자의 공고와 검증된 인재를 한곳에서.</p>
        <ul class="footer-contact" aria-label="고객 연락처">
          <li>
            <a href="tel:+82-508-202-4690" rel="nofollow">
              <span aria-hidden="true">📞</span>
              <span>0508-202-4690</span>
            </a>
            <span class="footer-contact__hours">평일 10:00~19:00</span>
          </li>
          <li>
            <a href="mailto:hello@massage-albago.kr">
              <span aria-hidden="true">✉️</span>
              <span>hello@massage-albago.kr</span>
            </a>
          </li>
        </ul>
        <ul class="footer-social" aria-label="공식 SNS 채널">
          <li>
            <a href="https://www.linkedin.com/in/%EB%B0%B1%ED%98%B8-%EA%B0%95-a84273261/" target="_blank" rel="me noopener" aria-label="마사지알바고 LinkedIn">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.063 2.063 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
            </a>
          </li>
          <li>
            <a href="https://medium.com/@88smartbro88" target="_blank" rel="me noopener" aria-label="마사지알바고 Medium">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M13.54 12a6.8 6.8 0 01-6.77 6.82A6.8 6.8 0 010 12a6.8 6.8 0 016.77-6.82A6.8 6.8 0 0113.54 12zM20.96 12c0 3.54-1.51 6.42-3.38 6.42-1.87 0-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42 3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12z"/></svg>
            </a>
          </li>
          <li>
            <a href="https://x.com/gugeulmake84173" target="_blank" rel="me noopener" aria-label="마사지알바고 X (Twitter)">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </a>
          </li>
        </ul>
      </div>

      <nav class="footer-nav" aria-label="구인구직">
        <h3 class="footer-nav__title">구인·구직</h3>
        <ul>
          <li><a href="/jobs/">전체 구인공고</a></li>
          <li><a href="/partner-stores/">제휴업소</a></li>
          <li><a href="/resumes/">이력서 등록</a></li>
          <li><a href="/partners/">업체 가입</a></li>
          <li><a href="/ads/">광고 상품안내</a></li>
        </ul>
      </nav>

      <nav class="footer-nav" aria-label="시술별 가이드">
        <h3 class="footer-nav__title">시술별 가이드</h3>
        <ul>
          <li><a href="/guide/swedish.html">스웨디시</a></li>
          <li><a href="/guide/aroma.html">아로마</a></li>
          <li><a href="/guide/thai.html">타이</a></li>
          <li><a href="/guide/single-shop.html">1인샵</a></li>
          <li><a href="/guide/total-shop.html">토탈샵</a></li>
          <li><a href="/guide/">전체 가이드</a></li>
        </ul>
      </nav>

      <nav class="footer-nav" aria-label="지역별 채용공고">
        <h3 class="footer-nav__title">지역별</h3>
        <ul>
          <li><a href="/jobs/seoul.html">서울</a></li>
          <li><a href="/jobs/gyeonggi.html">경기</a></li>
          <li><a href="/jobs/incheon.html">인천</a></li>
          <li><a href="/jobs/busan.html">부산</a></li>
          <li><a href="/jobs/">전체 17개 시·도</a></li>
        </ul>
      </nav>

      <nav class="footer-nav" aria-label="정보 및 고객지원">
        <h3 class="footer-nav__title">정보·고객지원</h3>
        <ul>
          <li><a href="/guide/">이용 안내</a></li>
          <li><a href="/support/index.html#safety">안전 가이드</a></li>
          <li><a href="/magazine/">매거진</a></li>
          <li><a href="/magazine/rss.xml" rel="alternate" type="application/rss+xml">매거진 RSS</a></li>
          <li><a href="/about/">회사 소개</a></li>
          <li><a href="/sitemap.xml">사이트맵</a></li>
        </ul>
      </nav>
    </div>

    <address class="footer-business" itemscope itemtype="https://schema.org/Organization">
      <meta itemprop="name" content="마사지알바고" />
      <meta itemprop="alternateName" content="MassageAlbaGo" />
      <meta itemprop="url" content="https://massagealbago.kr/" />
      <meta itemprop="logo" content="https://massagealbago.kr/images/logo/logo.png" />
      <dl class="footer-business__info">
        <div class="footer-business__row"><dt>상호</dt><dd itemprop="legalName">YH LAB</dd></div>
        <div class="footer-business__row"><dt>대표자</dt><dd>김수환</dd></div>
        <div class="footer-business__row"><dt>사업자등록번호</dt><dd>815-26-00585</dd></div>
        <div class="footer-business__row"><dt>직업정보제공사업 신고번호</dt><dd>J1802020260002</dd></div>
        <div class="footer-business__row"><dt>사업장 주소</dt>
          <dd itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
            <span itemprop="streetAddress">청석로 268</span>,
            <span itemprop="addressLocality">파주시</span>,
            <span itemprop="addressRegion">경기도</span>
            <meta itemprop="addressCountry" content="KR" />
          </dd>
        </div>
        <div class="footer-business__row"><dt>고객센터</dt><dd><a href="tel:+82-508-202-4690" itemprop="telephone" rel="nofollow">0508-202-4690</a> <span class="footer-business__muted">(평일 10:00~19:00)</span></dd></div>
        <div class="footer-business__row"><dt>이메일</dt><dd><a href="mailto:hello@massage-albago.kr" itemprop="email">hello@massage-albago.kr</a></dd></div>
      </dl>
    </address>

    <div class="footer-bottom">
      <nav class="footer-legal-nav" aria-label="정책 및 약관">
        <a href="/support/index.html#privacy">개인정보처리방침</a>
        <span class="sep" aria-hidden="true">·</span>
        <a href="/support/index.html#terms">이용약관</a>
        <span class="sep" aria-hidden="true">·</span>
        <a href="/support/index.html#safety">안전 가이드</a>
        <span class="sep" aria-hidden="true">·</span>
        <a href="/about/">회사 소개</a>
      </nav>
      <p class="footer-trust-line">본 사이트는 직업정보제공사업 신고를 마친 검증된 채용 정보 플랫폼입니다.</p>
      <p class="footer-copyright">© <time datetime="2026">2026</time> 마사지알바고 · YH LAB. All rights reserved.</p>
    </div>
  </div>
</footer>'''

FOOTER_RE = re.compile(
    r'<footer[^>]*class="[^"]*site-footer[^"]*"[^>]*>.*?</footer>',
    re.DOTALL,
)


def find_html_files() -> list[Path]:
    return [
        p for p in ROOT.rglob("*.html")
        if ".git" not in p.parts and "node_modules" not in p.parts
    ]


def main() -> int:
    files = find_html_files()
    changed = 0
    skipped = 0
    no_footer = 0
    for f in files:
        html = f.read_text(encoding="utf-8")
        if 'class="site-footer"' not in html:
            no_footer += 1
            continue
        new_html, n = FOOTER_RE.subn(NEW_FOOTER, html, count=1)
        if n == 0:
            skipped += 1
            continue
        if new_html != html:
            f.write_text(new_html, encoding="utf-8")
            changed += 1
    print(f"changed: {changed}")
    print(f"skipped: {skipped}")
    print(f"no footer: {no_footer}")
    print(f"total scanned: {len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

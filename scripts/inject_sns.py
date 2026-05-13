#!/usr/bin/env python3
"""
모든 HTML 파일 푸터에 SNS 아이콘 행 추가 + 홈 Organization JSON-LD
에 sameAs 배열 추가 (E-E-A-T sameAs 시그널).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SNS_BLOCK = '''        <ul class="footer-social" aria-label="공식 SNS 채널">
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
        </ul>'''

# .footer-contact ul 의 닫는 </ul> 직후에 삽입
# 매처: </ul> 다음 줄에 </div> (footer-brand-col 닫기)
INSERT_RE = re.compile(
    r'(<ul class="footer-contact"[^>]*>.*?</ul>)(\s*</div>)',
    re.DOTALL
)


def inject_sns_to_html(html: str) -> tuple[str, bool]:
    if 'class="footer-social"' in html:
        return html, False
    new_html, n = INSERT_RE.subn(
        lambda m: m.group(1) + "\n" + SNS_BLOCK + m.group(2),
        html,
        count=1,
    )
    return new_html, n > 0


# 홈 index.html 의 Organization JSON-LD 에 sameAs 추가
SAMEAS_VALUE = [
    "https://www.linkedin.com/in/%EB%B0%B1%ED%98%B8-%EA%B0%95-a84273261/",
    "https://medium.com/@88smartbro88",
    "https://x.com/gugeulmake84173",
]


def inject_sameas_in_home(html: str) -> tuple[str, bool]:
    """홈 index.html 의 Organization JSON-LD 블록에 sameAs 배열 추가."""
    if '"sameAs"' in html:
        return html, False
    # "Organization" 블록 안에 telephone 또는 email 다음에 sameAs 추가
    # 우리 home jsonld 구조: telephone, email 라인 다음에 address...
    # 가장 안정적: "founder" 직후 또는 "telephone" 직후 삽입
    sameas_str = '      "sameAs": [\n        ' + ',\n        '.join(f'"{u}"' for u in SAMEAS_VALUE) + '\n      ],\n      '
    pattern = re.compile(r'(\s+)("telephone": "[^"]+",\n)', re.DOTALL)
    new_html, n = pattern.subn(
        lambda m: m.group(1) + m.group(2) + sameas_str.lstrip("\n"),
        html,
        count=1,
    )
    return new_html, n > 0


def main():
    sns_count = 0
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        html = p.read_text(encoding="utf-8")
        new_html, changed = inject_sns_to_html(html)
        if changed:
            p.write_text(new_html, encoding="utf-8")
            sns_count += 1
    print(f"SNS injected into {sns_count} files")

    # 홈 sameAs
    home = ROOT / "index.html"
    html = home.read_text(encoding="utf-8")
    new_html, changed = inject_sameas_in_home(html)
    if changed:
        home.write_text(new_html, encoding="utf-8")
        print("home Organization sameAs added")
    else:
        print("home sameAs not added (already present or pattern not matched)")


if __name__ == "__main__":
    main()

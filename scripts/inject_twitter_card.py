#!/usr/bin/env python3
"""모든 HTML 페이지에 Twitter Card meta 일괄 추가."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INSERT_BLOCK = (
    '<meta name="twitter:card" content="summary_large_image" />\n'
    '<meta name="twitter:site" content="@massagealba" />\n'
)


def main() -> int:
    count = 0
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        html = p.read_text(encoding="utf-8")
        if 'twitter:card' in html:
            continue
        # og:image 또는 stylesheet 직전에 삽입
        anchor = re.search(r'<meta property="og:image"[^>]*/?>', html)
        if anchor:
            insert_at = anchor.end()
            new_html = html[:insert_at] + "\n" + INSERT_BLOCK.rstrip() + html[insert_at:]
        else:
            # og:image 없으면 </head> 직전에 삽입
            new_html, n = re.subn(r'</head>', INSERT_BLOCK + "</head>", html, count=1)
            if n == 0:
                continue
        if new_html != html:
            p.write_text(new_html, encoding="utf-8")
            count += 1
    print(f"twitter:card meta injected: {count} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

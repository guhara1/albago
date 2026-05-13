# 매거진 자동 발행

`generate_post.py` 가 주 1회(매주 월요일 오전 9시 KST) GitHub Actions 에서 실행되어,
`topic_queue.json` 의 다음 주제 1개를 사람 톤의 SEO 본문으로 작성·게시합니다.

## 동작 흐름

1. `topic_queue.json` 에서 `used:false` 인 첫 번째 주제 선택
2. Anthropic API (`ANTHROPIC_API_KEY` secret) 호출 → JSON 출력
3. 품질 가드: 분량(2,200~2,900자) · H2 5개 구조 · 금지어 · AI 정형구 빈도 검사
4. 통과하면 `magazine/posts/{slug}.html` 로 저장
5. `magazine/index.html` 의 `<!-- AUTO_POSTS_START -->` 블록 자동 갱신
6. `sitemap.xml` 에 URL 추가, `magazine/rss.xml` 재생성
7. IndexNow · Google · Bing 사이트맵 ping
8. `topic` 을 `used:true` 처리 + `published_at` 기록

## SEO 정책 (Google 실제 평가 순서 기준)

- **노출 가능성**: 정적 HTML, canonical, og, sitemap, RSS, JSON-LD(@graph)
- **스팸 차단**: 금지어 리스트, 외부 행동유도/할인코드/번호 금지, 키워드 과반복 검사
- **검색 의도**: 토픽마다 `search_intent` / `scenario` 가 명시되어 첫 H2 안에 짚도록 프롬프트
- **도움됨 · 신뢰성 (E-E-A-T)**: 본문에 Experience(시나리오) · Expertise(숫자) · Authority(법규 한 줄) · Trust(안전 가이드 링크) 가 흩뿌려짐
- **페이지 경험**: `css/style.css` 기존 디자인 시스템, 모바일 viewport, 가벼운 정적 HTML
- **링크 · 신선도 · 원본성**: 주 1회 주기적 발행, 토픽별 내부 링크(`related_links`), 1인칭 회상 톤

## AI 탐지 회피

- "또한 / 결론적으로 / 정리하자면 / 마지막으로 / 본 글에서는 / 여러분" 금지
- 종결어미 한 패턴 통일 금지 — "~죠 / ~거든요 / ~잖아요 / ~더라고요" 혼용
- 작은 후회·자기 의심 한 줄 의무
- 비문에 가까운 짧은 회상 허용
- 통계는 1~2개, "들리는 말로는" 톤으로 단정 회피

## 로컬에서 한 번 돌려 보기

```bash
pip install -r scripts/requirements.txt
ANTHROPIC_API_KEY=sk-ant-... python scripts/generate_post.py
```

## 토픽 보충

`topic_queue.json` 의 `topics` 배열에 새 항목을 추가하기만 하면 됩니다. 모든 토픽이
`used:true` 가 되면 워크플로우는 "토픽 소진" 메시지를 남기고 종료합니다.

# 마사지알바고

전국 마사지·스파·테라피 구인구직 플랫폼.
관리사·테라피스트 채용 공고와 이력서를 한곳에서.

> 본 저장소는 `massage5`(전국 출장마사지 정보 플랫폼 `간다GO`)를 베이스로
> 마사지 구인구직 플랫폼 `마사지알바고`로 리뉴얼한 결과물입니다.
> 기존 region/services/magazine/reviews/support 페이지의 SEO 자산은 그대로
> 유지하고, 메인·메타·내비게이션·신규 핵심 페이지(jobs/resumes/partners)를
> 구인구직 흐름으로 재구성했습니다.

## 구조

```
.
├─ index.html              # 메인 (구인구직 랜딩)
├─ jobs/index.html         # 구인공고 전체 (NEW)
├─ resumes/index.html      # 이력서 등록·인재 검색 (NEW)
├─ partners/index.html     # 업체 가입·공고 등록 (NEW)
├─ css/style.css           # 공통 스타일
├─ js/main.js              # 모바일 메뉴 / 활성 메뉴 표시
├─ region/                 # 지역별 (전국 17개 시·도, 시·군·구 SEO 페이지)
├─ services/               # 업종/시술별 (스웨디시·아로마·타이 등)
├─ reviews/index.html      # 이용 후기
├─ support/index.html      # 고객지원·안전·FAQ·제휴
├─ magazine/               # 매거진 (직무 가이드·인터뷰·지역 트렌드)
├─ manifest.webmanifest    # PWA 매니페스트
├─ robots.txt
├─ sitemap.xml             # 사이트맵 인덱스
└─ sitemap-*.xml           # 카테고리별 sub-sitemap
```

## 핵심 페이지

- `/` — 메인 랜딩 (구직자/구인 업체 모두 대상)
- `/jobs/` — 채용 공고 (급구·신입 가능·일급·기숙사·정규직·출장)
- `/resumes/` — 이력서 등록, 업체용 인재 검색, 구직 가이드
- `/partners/` — 업체 회원 가입, 요금제, 공고 등록

## 미리보기

순수 정적 HTML/CSS/JS이므로 별도 빌드 없이 바로 열 수 있습니다.

```bash
python3 -m http.server 8080
# 또는
npx serve .
```

브라우저에서 `http://localhost:8080` 열기.

## GitHub Pages 배포

저장소의 Settings → Pages → Source = `Deploy from a branch`, Branch = 배포할
브랜치 → `/ (root)` 선택 후 저장하면 됩니다.

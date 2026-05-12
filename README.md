# 마사지알바고

전국 마사지·스파·테라피 구인구직 플랫폼.

## 구조

```
.
├── index.html                # 메인 (구인구직 랜딩)
├── css/style.css             # 디자인 시스템
├── js/main.js                # 모바일 메뉴 토글
├── favicon.svg
├── manifest.webmanifest
├── robots.txt
├── sitemap.xml
├── jobs/                     # 구인공고
│   ├── index.html            # 채용공고 허브
│   ├── seoul.html ~ jeju.html  # 17개 시·도 페이지
├── resumes/index.html        # 이력서 등록
├── partners/index.html       # 업체 가입·요금제
├── guide/                    # 시술별 가이드
│   ├── index.html            # 가이드 허브
│   ├── swedish/aroma/thai/lomi/chinese/homecare/spa/sports.html
├── magazine/index.html       # 매거진 (콘텐츠 곧 추가)
├── about/index.html          # 회사 소개
└── support/index.html        # 고객지원·안전
```

총 33개 페이지로 구성된 깔끔한 마사지 구인구직 플랫폼.

## 미리보기

```bash
python3 -m http.server 8080
```

브라우저에서 `http://localhost:8080` 열기.

## 배포 (Cloudflare Pages)

- 프로덕션 브랜치: `main`
- 빌드 명령: 없음
- 출력 디렉토리: `/`
- main 머지 시 자동 배포 (1~2분)

# Cloudflare Pages Functions

광고 문의 폼 → 텔레그램 알림 서버리스 함수.

## 파일 구조

```
functions/
└── api/
    └── inquiry.js   ← POST /api/inquiry 핸들러
```

배포 시 Cloudflare Pages가 자동으로 `/api/inquiry` 엔드포인트로 노출합니다.

## ⚠️ 환경변수 설정 (필수)

Cloudflare Pages 대시보드에서 4개 환경변수를 설정해야 텔레그램 알림이 전송됩니다.

### 설정 방법

1. https://dash.cloudflare.com → **Workers & Pages** → **albago** 프로젝트 선택
2. **Settings** 탭 → **Environment variables** → **Add variable**
3. **Production** 환경에 다음 4개 추가:

| 변수명 | 값 |
|---|---|
| `TG_TOKEN_OWNER` | 대표 봇 토큰 (BotFather 발급) |
| `TG_CHAT_OWNER` | 대표 텔레그램 chat_id (숫자) |
| `TG_TOKEN_FRIEND` | 보조 봇 토큰 (BotFather 발급) |
| `TG_CHAT_FRIEND` | 보조 텔레그램 chat_id (숫자) |

4. **Save** → 다음 배포부터 적용됨 (또는 **Deployments** → 마지막 배포 **Retry**)

### 🔐 보안 권고

대화 또는 PHP 코드 등에 토큰이 노출된 경우 **반드시 토큰을 재발급**하세요:

1. 텔레그램에서 `@BotFather` 검색
2. `/mybots` → 해당 봇 선택 → **API Token** → **Revoke current token**
3. 새 토큰을 받아 Cloudflare 환경변수에 업데이트

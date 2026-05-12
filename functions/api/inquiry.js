// Cloudflare Pages Function — POST /api/inquiry
// 광고 문의 폼 제출 시 텔레그램으로 즉시 알림 전송
//
// 환경변수 (Cloudflare Pages 대시보드에서 설정):
//   TG_TOKEN_OWNER  — 대표 봇 토큰
//   TG_CHAT_OWNER   — 대표 텔레그램 chat_id
//   TG_TOKEN_FRIEND — 보조 봇 토큰
//   TG_CHAT_FRIEND  — 보조 텔레그램 chat_id

export async function onRequestPost(context) {
  const { request, env } = context;

  if (!request.headers.get("content-type")?.includes("application/json")) {
    return jsonResponse({ ok: false, error: "Content-Type must be application/json" }, 400);
  }

  let data;
  try {
    data = await request.json();
  } catch (e) {
    return jsonResponse({ ok: false, error: "Invalid JSON" }, 400);
  }

  if (data.website) {
    return jsonResponse({ ok: true, skipped: true });
  }

  const required = ["companyName", "bizNumber", "managerName", "managerPhone", "tier"];
  for (const k of required) {
    if (!data[k] || String(data[k]).trim() === "") {
      return jsonResponse({ ok: false, error: `필수 항목 누락: ${k}` }, 400);
    }
  }

  const ts = new Date().toLocaleString("ko-KR", { timeZone: "Asia/Seoul" });
  const message =
    `📥 마사지알바고 광고 문의\n` +
    `━━━━━━━━━━━━━━━━━━\n` +
    `🏢 업소 정보\n` +
    `• 업체명: ${data.companyName || "-"}\n` +
    `• 사업자등록번호: ${data.bizNumber || "-"}\n` +
    `• 회사 주소: ${[data.zip, data.addr, data.addrDetail, data.addrRef].filter(Boolean).join(" / ")}\n` +
    `• 회사 전화: ${data.companyPhone || "-"}\n` +
    `\n` +
    `📢 광고 정보\n` +
    `• 광고 지역: ${data.region || "-"}\n` +
    `• 업종: ${data.category || "-"}\n` +
    `• 희망 티어: ${data.tier || "-"}\n` +
    `• 시작 희망일: ${data.startDate || "-"}\n` +
    `\n` +
    `👤 담당자\n` +
    `• 성함: ${data.managerName || "-"}\n` +
    `• 휴대폰: ${data.managerPhone || "-"}\n` +
    `• 이메일: ${data.managerEmail || "-"}\n` +
    `\n` +
    `📝 추가 요청\n` +
    `${data.note || "(없음)"}\n` +
    `\n` +
    `━━━━━━━━━━━━━━━━━━\n` +
    `🕒 접수: ${ts}`;

  const targets = [
    { token: env.TG_TOKEN_OWNER,  chat: env.TG_CHAT_OWNER,  label: "대표" },
    { token: env.TG_TOKEN_FRIEND, chat: env.TG_CHAT_FRIEND, label: "보조" },
  ];

  const results = [];
  for (const t of targets) {
    if (!t.token || !t.chat) {
      results.push({ label: t.label, ok: false, error: "env not set" });
      continue;
    }
    try {
      const tgRes = await fetch(`https://api.telegram.org/bot${t.token}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: t.chat,
          text: message,
          disable_web_page_preview: true,
        }),
      });
      const body = await tgRes.json();
      results.push({ label: t.label, ok: body.ok === true, body });
    } catch (e) {
      results.push({ label: t.label, ok: false, error: String(e) });
    }
  }

  const anyOk = results.some((r) => r.ok);
  return jsonResponse({ ok: anyOk, results }, anyOk ? 200 : 502);
}

function jsonResponse(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
    },
  });
}

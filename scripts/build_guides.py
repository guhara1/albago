#!/usr/bin/env python3
"""
분야별 채용 가이드 6개 페이지 생성기.

GUIDES 데이터 dict 를 받아 guide/{slug}.html 로 저장.
SEO/EEAT 강화 — Article + BreadcrumbList + FAQPage + Organization JSON-LD,
   풍부한 본문(직무·시장·자격·급여·신입팁·안전·FAQ), 카드 그리드 UI.
"""

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
GUIDE_DIR = ROOT / "guide"
DOMAIN = "https://massagealbago.kr"
KST = timezone(timedelta(hours=9))
TODAY_ISO = datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
TODAY = datetime.now(KST).strftime("%Y-%m-%d")

GUIDES = [
    {
        "slug": "single-shop",
        "category": "1인샵",
        "icon_letter": "1",
        "icon_tone": "blue",
        "h1": "1인샵 관리사 채용·구직 가이드 — 자유 출퇴근·높은 일급",
        "lead": "관리사 한 명이 운영하는 1인 마사지샵의 채용·근무 정보. 매니저 없는 자율 근무, 일급제 수익 구조, 콜수에 따른 변동까지 현장 톤으로 정리했습니다.",
        "stats": [
            ("평균 일급", "20~30만원"),
            ("경력 우대", "1년 이상"),
            ("주요 지역", "수도권·강남권"),
            ("근무 형태", "일급제·자유"),
        ],
        "keywords": "1인샵 구인, 1인샵 채용, 1인샵 관리사, 1인샵 일급, 강남 1인샵 채용, 마사지알바고",
        "overview_p": "1인샵은 관리사 한 명이 시술부터 예약 응대·매장 정리·결제·청소까지 전부 본인이 담당하는 소형 매장입니다. 매니저가 없는 만큼 자유롭지만, 매장 전체가 본인 책임이라는 무게가 따라옵니다. 강남·송파·분당 같은 인구 밀집 지역의 오피스텔 단위에 가장 많이 분포하고, 신규 오픈과 양도 매물이 끊임없이 도는 시장이에요.",
        "overview_tasks": [
            "예약 고객 응대 + 시술 진행 (60·90·120분 코스)",
            "본인 일정 관리, 콜 응답·예약 컨펌·노쇼 대응",
            "시술 전후 시트 교체·매장 청소·소모품 발주",
            "카드 결제기·현금 정산·매출 장부 관리",
            "매장 전기·수도·공조·소독 일상 점검",
        ],
        "market_p": "수도권을 중심으로 1인샵은 한 동네에 4~5곳씩 분포할 만큼 흔합니다. 강남·서초·송파·분당·일산 권역이 가장 활발하고, 부산·해운대·대전·세종 같은 대도시 중심에도 안정적인 수요가 있어요. 경력 1~3년차 관리사가 본인 페이스로 일하기 위해 1인샵으로 옮겨오는 흐름이 가장 큽니다.",
        "market_types": [
            "<strong>오피스텔형 1인샵</strong> — 가장 흔한 형태. 본사 없이 개인 사업자 단독 운영. 일급 25만 전후.",
            "<strong>아파트형 1인샵</strong> — 주거 권역 내 입지. 단골 비중 높고 콜수 안정적.",
            "<strong>본사 분점형 1인샵</strong> — 동일 브랜드 다점포 중 한 자리. 마케팅·콜센터 공유.",
        ],
        "qualification_must": [
            "기본 시술 경력 1년 이상 (스웨디시·아로마·타이 중 하나 이상 손에 익은 상태)",
            "예약 응대·카운터 응대·결제까지 단독 수행 가능",
            "차분한 응대 톤과 매장 청결 유지 습관",
        ],
        "qualification_plus": [
            "오일·아로마 트리트먼트 60·90·120분 코스 운영 경험",
            "단골 관리 노하우 — 카카오톡·문자 응대 기본",
            "위생 관련 자격(피부미용사 등) 보유자 우대",
        ],
        "salary_rows": [
            ("신입(1년 미만)", "일 15~18만원", "월 280~320만원"),
            ("경력 1~3년", "일 20~25만원", "월 330~420만원"),
            ("경력 3~5년", "일 25~30만원", "월 400~480만원"),
            ("실장급(5년+)", "일 28~35만원+", "월 450만원+"),
        ],
        "salary_note": "위 수치는 마사지알바고에 등록된 1인샵 공고 표본을 기반으로 한 업계 평균 추정치입니다. 콜수·지역·인센티브 구조에 따라 ±20% 변동 가능.",
        "tips_p": "1인샵은 매니저가 없으니 콜수가 적은 날이 본인 수익에 그대로 반영됩니다. 첫 1~2개월은 단골 형성 전이라 콜이 불안정할 수 있는데, 그 기간을 버틸 수 있는 매장 풀(콜수 보장)이 있는 곳을 고르는 게 좋아요. 본사 마케팅이 들어가는 분점형 1인샵이 신입에게 더 안정적입니다.",
        "safety_items": [
            "근로계약서 또는 위탁계약서를 입사 전 반드시 작성 — 일급·정산 주기·노쇼 책임 명시",
            "선입금·교육비·유니폼비 요구는 즉시 거절 (정상 매장은 안 받음)",
            "사업자등록증 사본 또는 매장 등록 확인. 미등록 매장은 거르세요",
            "야간 단독 근무 시 비상 연락처·CCTV 운영 여부 확인",
        ],
        "faq": [
            ("1인샵은 신입도 가능한가요?",
             "기본적으로 경력 1년 이상을 우대합니다. 매니저 없이 모든 응대를 단독으로 해야 하기 때문이에요. 다만 본사 마케팅·콜센터를 운영하는 분점형 1인샵은 신입 트레이니로 받기도 합니다."),
            ("일급제와 건당제 중 어떤 게 유리한가요?",
             "콜수가 안정적이라면 일급제가 예측 가능해 좋고, 콜이 많은 매장이라면 건당제가 수익이 큽니다. 입사 전 매장의 최근 30일 콜수 분포를 확인해 보시면 판단이 빠릅니다."),
            ("1인샵에서 4대보험 가입은 안 되는 경우가 많나요?",
             "1인샵 다수가 위탁 계약(프리랜서) 형태로 운영되어 4대보험이 적용되지 않는 경우가 있습니다. 이 경우 국민건강·국민연금은 본인이 지역가입자로 납부해야 하니 사전에 매장에 확인하세요."),
            ("콜수가 0인 날은 어떻게 정산하나요?",
             "보장제(보장 일급)·기본급+인센·순건당 등 매장마다 다릅니다. 보장제가 있는 매장은 신입에게 가장 안정적입니다. 계약서 작성 시 이 부분이 명시되어야 합니다."),
            ("이력서 등록은 어디서 하나요?",
             '마사지알바고 <a href="../resumes/index.html">이력서 등록</a> 페이지에서 무료로 등록 가능합니다. 사업자 인증을 마친 1인샵 매장에서만 연락이 갑니다.'),
        ],
        "related": [
            ("swedish.html", "스웨디시 가이드", "스", "blue", "1인샵에서 가장 많이 운영"),
            ("spa.html", "스파·매니저 가이드", "스", "indigo", "중대형 정규직 트랙"),
            ("homecare.html", "홈케어 출장 가이드", "홈", "teal", "자율 근무의 또 다른 형태"),
        ],
    },
    {
        "slug": "skincare",
        "category": "피부관리",
        "icon_letter": "피",
        "icon_tone": "rose",
        "h1": "피부관리사(에스테티션) 채용·구직 가이드",
        "lead": "피부미용사 국가자격증 보유자 중심의 안정적 정규직 시장. 페이셜·바디 관리, 기기 운영, 딥클렌징·필링까지 전문성이 핵심인 분야의 채용 정보를 정리했습니다.",
        "stats": [
            ("평균 월급", "280~400만원"),
            ("필수 자격", "피부미용사"),
            ("주요 형태", "월급제 정규직"),
            ("4대보험", "표준 적용"),
        ],
        "keywords": "피부관리사 채용, 에스테티션 구인, 피부관리실 알바, 피부미용사 채용, 페이셜 관리사 구인, 마사지알바고",
        "overview_p": "피부관리사(에스테티션)는 피부미용사 국가자격증을 기반으로 페이셜·바디 케어를 전문으로 합니다. 기기(고주파·RF·LED·갈바닉) 운영, 딥클렌징, 필링, 마스크 관리까지 표준화된 케어를 제공해요. 정규직 비중이 마사지 시술 분야 중 가장 높고, 4대보험·근로계약서가 거의 100% 표준화되어 있어 신입에게도 진입 장벽이 낮은 분야입니다.",
        "overview_tasks": [
            "페이셜 케어 진행 (60·90분 코스 단위, 클렌징·각질·마스크 패키지)",
            "피부 진단 — 유수분 밸런스·트러블·민감도 체크",
            "기기 운영 — 고주파·RF·LED·갈바닉·초음파",
            "고객 홈케어 제품 추천 및 매출 관리",
            "위생 관리 — 도구 소독·시트·타올 세탁 관리",
        ],
        "market_p": "피부관리 채용은 시술 분야 중 가장 안정적입니다. 에스테틱샵·피부관리실·종합 토탈샵·호텔 스파 모두 채용 수요가 꾸준해요. 신입은 사내 교육 후 단독 케어 진행, 경력자는 실장·매니저 트랙으로 올라가는 커리어 패스가 명확합니다. 전국에 고르게 분포하지만 특히 강남·압구정·분당·해운대 등 고급 권역에서 수요가 많아요.",
        "market_types": [
            "<strong>에스테틱샵·피부관리실</strong> — 페이셜·바디 전문. 정규직 다수.",
            "<strong>종합 토탈샵</strong> — 피부+체형+왁싱 등 멀티 케어. 시술 다양.",
            "<strong>호텔 스파</strong> — 고급 호텔 부설. 외국인 고객 응대 기회.",
            "<strong>의원·클리닉 부설</strong> — 시술 후 케어 보조. 의료 환경.",
        ],
        "qualification_must": [
            "피부미용사 국가자격증(필수)",
            "기본 페이셜·바디 케어 프로토콜 숙지",
            "기기 안전 사용법 이해 (고주파·RF·LED 등)",
            "고객 응대·홈케어 컨설팅 가능",
        ],
        "qualification_plus": [
            "기기 자격증 보유(RF·고주파 메이커별 교육 이수)",
            "두피·바디 트리트먼트 경력",
            "외국어(영어·중국어·일본어) 응대 가능자 호텔 스파 우대",
        ],
        "salary_rows": [
            ("신입(1년 미만)", "—", "월 240~280만원"),
            ("경력 1~3년", "—", "월 290~360만원"),
            ("경력 3~5년", "—", "월 350~450만원"),
            ("실장급(5년+)", "—", "월 450만원+"),
        ],
        "salary_note": "피부관리 분야는 일급제 비중이 낮고 월급제+인센티브 구조가 표준입니다. 매출 인센티브가 별도로 붙는 매장이 많아 경력자는 실수령이 더 클 수 있어요.",
        "tips_p": "피부미용사 자격증을 갓 취득한 신입은 대형 에스테틱이나 호텔 스파의 트레이니 채용을 노리면 좋습니다. 3~6개월 사내 교육 후 단독 케어를 맡게 되고, 그 기간 동안 기기 사용·고객 응대를 표준화된 매뉴얼로 익힐 수 있어요.",
        "safety_items": [
            "근로계약서·4대보험·연차 표준 적용 매장 선택",
            "고객 환불 책임이 본인에게 전가되는 계약서 조항 주의",
            "기기 운영 안전 교육이 입사 후 제공되는지 확인",
            "고가 화장품 판매 강요는 위법 소지 있음",
        ],
        "faq": [
            ("피부미용사 자격증 없이도 채용되나요?",
             "피부관리실·에스테틱 단독 운영은 자격증이 사실상 필수입니다. 일부 종합 토탈샵에서 '관리 보조' 형태로 무자격 채용도 있지만, 정식 케어 진행은 자격증 보유자만 가능합니다."),
            ("자격증 학원 추천 기준은?",
             "한국산업인력공단 시험 합격률, 실습 시간, 실제 기기 사용 비중을 비교하세요. 단기 속성 코스보다 6개월 이상 정규 과정이 현장 적응에 유리합니다."),
            ("호텔 스파 채용은 어떻게 준비하나요?",
             "기본 자격증 + 외국어 회화(영어 중급 이상) + 호텔 매너 교육을 함께 갖추면 유리합니다. 5성급 호텔 채용은 별도 면접·시범 케어 절차가 있습니다."),
            ("기기 운영 사고가 발생하면 책임은 누가 지나요?",
             "정상 매장은 매장 책임보험에 가입되어 있어 1차 책임은 매장이 집니다. 다만 본인의 명백한 과실(미숙련 운영)은 본인 책임이 될 수 있으니 입사 후 충분한 교육을 받고 단독 운영을 시작하세요."),
            ("이력서 등록은?",
             '마사지알바고 <a href="../resumes/index.html">이력서 등록</a>에서 자격증·기기 경력을 입력하시면 매칭이 빠릅니다.'),
        ],
        "related": [
            ("body-shaping.html", "체형관리 가이드", "체", "emerald", "함께 운영하는 매장 다수"),
            ("waxing.html", "왁싱 가이드", "왁", "amber", "토탈샵에서 같이 채용"),
            ("total-shop.html", "토탈샵 가이드", "토", "violet", "멀티 케어 정규직"),
        ],
    },
    {
        "slug": "body-shaping",
        "category": "체형관리",
        "icon_letter": "체",
        "icon_tone": "emerald",
        "h1": "체형관리 관리사 채용·구직 가이드 — 다이어트·림프 케어",
        "lead": "다이어트 마사지·셀룰라이트 케어·림프 드레나지 등 체형 변화 목적의 케어를 전문으로 하는 분야. 강도 있는 시술과 코스 컨설팅 능력이 핵심이며, 슬리밍 전문 매장과 종합 토탈샵에서 활발히 채용합니다.",
        "stats": [
            ("평균 일급", "18~25만원"),
            ("우대 자격", "피부미용사·림프 드레나지"),
            ("주요 형태", "정규직·일급제 혼합"),
            ("주요 지역", "수도권·해운대"),
        ],
        "keywords": "체형관리사 채용, 림프 드레나지 구인, 슬리밍 매장 알바, 다이어트 관리사 구인, 셀룰라이트 케어 채용, 마사지알바고",
        "overview_p": "체형관리는 림프 드레나지·셀룰라이트 케어·복부 관리·하체 케어를 중심으로 한 시술 분야입니다. 코스가 60~90분으로 길고 시술 강도가 있어 체력 요구가 큰 편이에요. 슬리밍 전문 매장·종합 에스테틱에서 활발하게 채용하며, 다이어트 시즌(3~6월, 11~12월)에는 수요가 폭증합니다.",
        "overview_tasks": [
            "림프 드레나지·셀룰라이트 케어·복부 관리 시술 진행",
            "기기 운영 — RF·캐비테이션·EMS·온열 기기",
            "고객 체형 측정 및 변화 추적 (입체 체크·둘레 측정)",
            "코스 컨설팅 — 회당·10회·20회 패키지 안내",
            "사후 관리 — 식이·홈케어 가이드 제공",
        ],
        "market_p": "체형관리 시장은 다이어트 시즌성에 영향을 받지만 사계절 모두 수요가 있습니다. 슬리밍 전문 매장은 전국 주요 도시에 분포하며, 종합 토탈샵 안에 체형관리 코스가 포함된 형태도 많아요. 경력 2~5년차가 실장·원장 트랙으로 가장 활발히 이동하는 분야입니다.",
        "market_types": [
            "<strong>슬리밍 전문샵</strong> — 체형관리만 전문. 강남·압구정 등 강세.",
            "<strong>종합 에스테틱(토탈샵)</strong> — 피부+체형+왁싱 통합. 정규직.",
            "<strong>한의원·의원 부설</strong> — 비만 클리닉 보조. 의료 매뉴얼.",
            "<strong>여성 전용 다이어트 케어</strong> — 1:1 컨설팅 중심.",
        ],
        "qualification_must": [
            "체형관리 코스 운영 경험 또는 림프 드레나지 교육 이수",
            "시술 강도 조절 능력 (강한 압부터 부드러운 압까지)",
            "코스 컨설팅·고객 추적 관리 가능",
        ],
        "qualification_plus": [
            "피부미용사 국가자격증 보유자 우대",
            "RF·캐비테이션·EMS 기기 운영 경험",
            "한방·아유르베다·림프 드레나지 전문 교육 이수자",
        ],
        "salary_rows": [
            ("신입(1년 미만)", "일 14~17만원", "월 250~290만원"),
            ("경력 1~3년", "일 18~22만원", "월 300~370만원"),
            ("경력 3~5년", "일 22~28만원", "월 370~450만원"),
            ("실장급(5년+)", "일 28만원+", "월 450만원+"),
        ],
        "salary_note": "체형관리 매장은 매출 인센티브 비중이 큽니다. 코스 판매 실적에 따라 월 100만원 이상 인센티브가 붙는 경우도 흔해요.",
        "tips_p": "체형관리는 손기술과 함께 코스 컨설팅 능력이 중요합니다. 신입은 매뉴얼 시술부터 익힌 뒤 6개월 정도 후에 고객 컨설팅 단계로 넘어가는 게 일반적이에요. 림프 드레나지 교육은 1~3개월 단기 과정이 많아 시술 경력 1년차에 보충하면 좋습니다.",
        "safety_items": [
            "강한 압 시술이 많은 분야 — 본인 손목·허리 보호 필수, 매장의 휴식 시간 보장 확인",
            "고객 부작용(멍·통증) 발생 시 매장 책임보험 적용 여부 확인",
            "기기 사용 전 충분한 교육 — 화상·전기 사고 방지",
            "근로계약서에 시술 코스별 수당 명확히 명시",
        ],
        "faq": [
            ("림프 드레나지 자격증이 따로 있나요?",
             "민간 자격으로 림프 드레나지·MLD(Manual Lymph Drainage) 교육 과정이 많습니다. 국가공인은 아니지만 실제 매장에서는 이수 여부를 우대 사항으로 봅니다."),
            ("다이어트 시즌과 비수기 차이가 큰가요?",
             "3~6월(여름 대비)과 11~12월(연말 대비)이 성수기, 1~2월과 7~8월이 상대적 비수기입니다. 정규직은 안정적이지만 일급제는 시즌 영향을 더 받습니다."),
            ("체형관리만 단독으로 하는 매장이 많나요?",
             "전문 슬리밍샵은 별도 시장으로 존재하고, 종합 에스테틱에서 체형관리를 한 코스로 운영하는 경우가 더 많습니다. 본인 진로(전문성·다양성)에 따라 선택하세요."),
            ("시술 강도가 강해 손목이 아픈데 어떻게 하나요?",
             "강한 압이 필요한 시술은 본인 자세와 기기 보조 활용으로 부담을 줄일 수 있습니다. 매장에서 RF·EMS 같은 기기 시술 비중이 높은 곳이 손에 부담이 덜해요."),
            ("이력서 등록은?",
             '<a href="../resumes/index.html">이력서 등록</a>에서 림프 드레나지·기기 경력을 입력하면 슬리밍 매장 매칭이 빠릅니다.'),
        ],
        "related": [
            ("skincare.html", "피부관리 가이드", "피", "rose", "함께 운영 매장 다수"),
            ("waxing.html", "왁싱 가이드", "왁", "amber", "여성 케어 토탈"),
            ("total-shop.html", "토탈샵 가이드", "토", "violet", "정규직 트랙"),
        ],
    },
    {
        "slug": "waxing",
        "category": "왁싱",
        "icon_letter": "왁",
        "icon_tone": "amber",
        "h1": "왁싱 관리사 채용·구직 가이드 — 위생·기술 중심의 1:1 케어",
        "lead": "브라질리언·바디·페이스 왁싱을 전문으로 하는 분야. 위생 관리와 기술 정확도가 핵심이며, 왁싱 전문샵과 종합 토탈샵에서 채용이 활발합니다. 강남·압구정·홍대 등 도심 권역에서 수요가 가장 큽니다.",
        "stats": [
            ("평균 월급", "250~350만원"),
            ("필수", "왁싱 전문 교육"),
            ("주요 형태", "정규직·일급제 혼합"),
            ("주요 지역", "강남·홍대·압구정"),
        ],
        "keywords": "왁싱 관리사 채용, 브라질리언 왁싱 구인, 왁싱샵 알바, 왁싱 전문 채용, 강남 왁싱 구인, 마사지알바고",
        "overview_p": "왁싱은 위생과 기술이 가장 직접적으로 평가되는 분야입니다. 한 번의 실수가 고객 피부 트러블로 이어지기 때문에, 매장마다 정해진 위생 매뉴얼을 엄격히 따라야 해요. 1:1 응대 비율이 100%라 고객과의 신뢰 형성이 중요하고, 단골 비중이 높아 안정적으로 일할 수 있는 분야이기도 합니다.",
        "overview_tasks": [
            "브라질리언·바디·페이스 왁싱 진행 (30분~1시간 코스)",
            "위생 관리 — 도구 1회용 사용, 베드 소독, 손 위생 철저",
            "고객 상담 — 통증 민감도·알러지·피부 상태 사전 확인",
            "왁스 온도·점도 관리 및 후처리 진정 케어",
            "재방문 주기 안내 (보통 4~6주)",
        ],
        "market_p": "왁싱 시장은 도심·번화가 권역에 집중되어 있습니다. 강남·압구정·홍대·잠실·해운대 같은 20~30대 여성 인구가 많은 지역이 핵심 시장이에요. 최근 5년 사이 왁싱 전문 프랜차이즈가 빠르게 늘었고, 종합 토탈샵 내 왁싱 코스도 일반화되었습니다.",
        "market_types": [
            "<strong>왁싱 전문 프랜차이즈</strong> — 표준화된 매뉴얼·교육·CI. 신입 트레이니 채용 많음.",
            "<strong>1인 운영 왁싱샵</strong> — 강남·압구정 오피스텔형. 단골 중심.",
            "<strong>종합 토탈샵 내 왁싱 코스</strong> — 다른 케어와 병행 운영.",
            "<strong>남성 전용 왁싱 매장</strong> — 최근 증가 추세.",
        ],
        "qualification_must": [
            "왁싱 전문 교육 이수 (보통 1~3개월 전문 과정)",
            "위생 관리 매뉴얼 숙지·준수",
            "고객 1:1 응대 및 통증 관리 가능",
            "왁스 종류별(스트립·하드·슈가) 사용법 이해",
        ],
        "qualification_plus": [
            "피부미용사 국가자격증 보유자 우대",
            "프랜차이즈 본사 교육 이수 경험",
            "브라질리언 왁싱 전문 교육 이수",
            "고객 응대 서비스 경력",
        ],
        "salary_rows": [
            ("신입(1년 미만)", "일 14~17만원", "월 230~270만원"),
            ("경력 1~3년", "일 18~22만원", "월 280~340만원"),
            ("경력 3~5년", "일 22~26만원", "월 340~420만원"),
            ("실장급(5년+)", "일 26만원+", "월 420만원+"),
        ],
        "salary_note": "왁싱은 시술 시간이 짧아 하루 처리 건수가 많고, 매출 인센티브 구조가 활발합니다. 단골이 쌓이면 본인 매출이 본인 급여에 직접 반영되는 구조가 일반적이에요.",
        "tips_p": "왁싱은 처음 1~3개월 사이에 기술 숙련도가 빠르게 올라가는 분야입니다. 본사 교육이 잘 되어 있는 프랜차이즈에서 시작해 표준 매뉴얼을 익힌 뒤, 본인 단골을 쌓아 1인샵으로 독립하는 커리어 패스가 일반적이에요. 위생 사고 한 건이 커리어에 큰 흠집이 되니, 본인 매뉴얼은 강박적으로 지키세요.",
        "safety_items": [
            "1회용 스파출라·장갑·시트 표준 사용 매장 선택",
            "왁스 온도계 사용으로 화상 예방 — 기준 온도 매뉴얼화 필수",
            "고객 피부 트러블 발생 시 매장 책임보험 적용 여부 확인",
            "근로계약서에 위생 사고 시 책임 분담 구조 명시",
        ],
        "faq": [
            ("왁싱 교육은 어디서 받나요?",
             "왁싱 전문 학원·아카데미에서 1~3개월 단기 과정으로 받을 수 있습니다. 메이저 왁스 브랜드(스트립·하드 왁스) 본사가 운영하는 교육 프로그램도 신뢰도가 높아요."),
            ("브라질리언 왁싱은 별도 교육이 필요한가요?",
             "기본 왁싱 교육과 별도로 브라질리언 전문 과정을 권합니다. 민감 부위 시술이라 통증 관리와 위생 매뉴얼이 더 엄격해요. 보통 1~2주 단기 집중 과정으로 운영됩니다."),
            ("남성 왁싱 시장은 어떤가요?",
             "최근 5년 사이 빠르게 성장 중입니다. 남성 전용 매장이 강남·홍대 중심으로 늘었고, 종합 매장에서도 남성 고객 비중이 30%를 넘는 곳이 있어요. 남성 응대 경험은 향후 커리어에 자산이 됩니다."),
            ("위생 사고가 발생하면 어떻게 되나요?",
             "정상 매장은 매장 책임보험에 가입되어 1차 책임은 매장이 집니다. 다만 본인의 매뉴얼 미준수가 명백한 경우 일부 책임이 발생할 수 있으니, 본인 매뉴얼을 항상 지키는 게 가장 큰 보호입니다."),
            ("이력서 등록은?",
             '<a href="../resumes/index.html">이력서 등록</a>에서 왁싱 교육 이수와 전문 분야(브라질리언/바디 등)를 입력하면 매칭이 빠릅니다.'),
        ],
        "related": [
            ("skincare.html", "피부관리 가이드", "피", "rose", "함께 운영 매장 다수"),
            ("total-shop.html", "토탈샵 가이드", "토", "violet", "왁싱 포함 종합샵"),
            ("body-shaping.html", "체형관리 가이드", "체", "emerald", "여성 케어 전문"),
        ],
    },
    {
        "slug": "counter",
        "category": "카운터",
        "icon_letter": "카",
        "icon_tone": "slate",
        "h1": "마사지샵 카운터(매니저) 채용·구직 가이드",
        "lead": "시술을 하지 않고 매장 카운터에서 예약·응대·결제·운영 보조를 담당하는 직무. 서비스직 첫 직장으로 인기가 높고, 자격증 없이 시작할 수 있으며 정규직·4대보험이 표준으로 적용되는 안정적인 자리입니다.",
        "stats": [
            ("평균 월급", "220~300만원"),
            ("필수 자격", "무관·신입 가능"),
            ("주요 형태", "정규직·4대보험"),
            ("근무 시간", "교대제·고정제"),
        ],
        "keywords": "마사지샵 카운터 구인, 마사지 매니저 채용, 스파 카운터 알바, 마사지샵 데스크 구인, 매장 운영 보조 채용, 마사지알바고",
        "overview_p": "카운터는 시술을 하지 않습니다. 대신 매장 전체 운영의 흐름을 컨트롤하는 자리예요. 예약 관리·고객 응대·결제 처리·시술 관리사 스케줄 조율·소모품 발주 등 매장의 흐름을 책임집니다. 자격증이 따로 필요 없고 친절한 응대 톤과 기본 컴퓨터 활용 능력이 가장 중요해요. 정규직·4대보험·연차가 표준으로 적용되는 안정적인 자리입니다.",
        "overview_tasks": [
            "예약 관리 — 전화·카톡·앱·홈페이지 통합 관리",
            "고객 체크인·체크아웃 응대 및 결제 처리",
            "시술 관리사 스케줄 조율 및 휴게 시간 관리",
            "매장 위생·소모품 관리 (오일·시트·일회용품 발주)",
            "POS·매출 보고·일일 정산",
            "신규 고객 상담 및 코스 안내",
        ],
        "market_p": "중대형 스파·종합 토탈샵·1인샵 분점형 매장에서 카운터 채용이 꾸준합니다. 강남·홍대·해운대 같은 번화가 매장은 응대 강도가 높은 대신 급여 수준도 높고, 주거 권역 매장은 차분한 단골 응대가 중심이에요. 서비스직 경력자나 매장 운영에 관심 있는 20~30대 여성에게 가장 적합한 자리입니다.",
        "market_types": [
            "<strong>중대형 스파·호텔 스파</strong> — 정규직·교대제. 외국어 응대 가능자 우대.",
            "<strong>종합 토탈샵</strong> — 코스 컨설팅 비중 큼. 상담력 중요.",
            "<strong>1인샵 분점형</strong> — 본사 카운터에서 여러 매장 예약 통합 관리.",
            "<strong>왁싱 전문샵</strong> — 1:1 응대 중심. 위생 매뉴얼 익숙해야.",
        ],
        "qualification_must": [
            "친절한 응대 톤·전화 응대 자신감",
            "POS·예약 시스템·기본 컴퓨터 활용",
            "근무 시간 준수 및 매장 운영 매뉴얼 이해",
        ],
        "qualification_plus": [
            "서비스직(카페·호텔·매장) 경력",
            "외국어 응대(영어 중급 이상) 가능자",
            "엑셀·매출 관리·재고 관리 경험",
            "코스·상품 컨설팅 영업 경력",
        ],
        "salary_rows": [
            ("신입(1년 미만)", "—", "월 210~240만원"),
            ("경력 1~3년", "—", "월 240~280만원"),
            ("경력 3~5년", "—", "월 280~340만원"),
            ("매니저·실장(5년+)", "—", "월 340만원+"),
        ],
        "salary_note": "카운터는 매출 인센티브가 별도로 붙는 매장이 늘고 있습니다. 코스 판매·신규 고객 유치 실적에 따라 월 30~80만원 추가 인센이 일반적이에요.",
        "tips_p": "카운터는 서비스직 첫 직장으로 가장 추천할 만합니다. 자격증 필요 없고, 사내 교육으로 1~2주 안에 업무를 익힐 수 있어요. 5년 이상 경력이 쌓이면 매니저·실장 트랙으로 올라가거나, 본인 매장 운영을 준비할 수 있는 좋은 출발점입니다.",
        "safety_items": [
            "근로계약서·4대보험 정상 가입 확인",
            "야간 단독 근무 시 CCTV·비상 호출 시스템 확인",
            "고객 정보 취급 관련 개인정보보호법 교육",
            "현금 정산 책임 분담 구조 사전 명시",
        ],
        "faq": [
            ("카운터 직무는 신입도 가능한가요?",
             "네, 카운터는 마사지 분야에서 신입 진입이 가장 쉬운 자리입니다. 자격증 무관, 사내 교육 1~2주 후 단독 운영 가능합니다. 친절한 응대 톤이 가장 중요한 요건이에요."),
            ("시술 관리사가 되고 싶다면 카운터부터 시작해도 되나요?",
             "좋은 출발점입니다. 매장 운영과 시술 흐름을 이해한 후 자격증 취득·시술 교육을 받으면, 매장 내에서 자연스럽게 시술 관리사로 전환되는 케이스가 많아요."),
            ("야간 근무가 있나요?",
             "매장에 따라 다르지만, 일반적으로 10:00~22:00 또는 14:00~02:00 같은 교대제 운영이 많습니다. 22:00 이후 단독 근무가 있다면 안전 시스템(CCTV·비상 호출) 확인 필수입니다."),
            ("외국어가 필요한가요?",
             "강남·압구정·이태원·해운대 같은 외국인 고객 비중이 높은 매장은 영어 응대가 사실상 필수입니다. 일반 주거 권역 매장은 외국어 없이도 충분합니다."),
            ("이력서 등록은?",
             '<a href="../resumes/index.html">이력서 등록</a>에서 서비스직 경력·외국어·POS 경험을 입력하면 매칭이 빠릅니다.'),
        ],
        "related": [
            ("spa.html", "스파 매니저 가이드", "스", "indigo", "매니저 트랙 경로"),
            ("total-shop.html", "토탈샵 가이드", "토", "violet", "복합 매장 운영"),
            ("single-shop.html", "1인샵 가이드", "1", "blue", "분점형 본사 카운터"),
        ],
    },
    {
        "slug": "total-shop",
        "category": "토탈샵",
        "icon_letter": "토",
        "icon_tone": "violet",
        "h1": "토탈샵(종합 에스테틱) 관리사 채용·구직 가이드",
        "lead": "스파·피부관리·체형관리·왁싱 등 여러 시술을 한 매장에서 통합 제공하는 종합 에스테틱. 멀티 케어 가능한 관리사를 우대하고 정규직·4대보험이 표준이며, 안정적인 커리어 패스를 원하는 경력자에게 가장 적합한 형태입니다.",
        "stats": [
            ("평균 월급", "280~450만원"),
            ("우대 자격", "복수 시술 가능자"),
            ("주요 형태", "정규직·4대보험"),
            ("커리어", "실장·원장 트랙"),
        ],
        "keywords": "토탈샵 채용, 종합 에스테틱 구인, 토탈샵 관리사 알바, 종합 마사지샵 채용, 멀티 케어 관리사 구인, 마사지알바고",
        "overview_p": "토탈샵(종합 에스테틱)은 페이셜·바디·체형·왁싱·스파 같은 여러 시술을 한 매장에서 통합 제공하는 형태입니다. 관리사 한 명이 2~3가지 시술을 다 다룰 수 있어야 하기 때문에 멀티 케어 가능자가 우대돼요. 매장 규모가 크고 정규직·4대보험·연차가 표준화되어 있어, 장기 근속·실장·원장 트랙으로 커리어를 쌓고 싶은 경력 관리사에게 가장 적합한 환경입니다.",
        "overview_tasks": [
            "복수 시술 운영 (페이셜+바디 / 체형+왁싱 등 조합)",
            "고객 통합 케어 — 코스 컨설팅·홈케어 가이드",
            "기기 운영 (RF·고주파·EMS·LED·캐비테이션)",
            "신규 고객 상담 및 패키지 안내",
            "매출 관리·매장 위생 관리 보조",
        ],
        "market_p": "토탈샵 시장은 안정적이고 큰 편입니다. 강남·분당·해운대·일산 같은 고급 권역에 가장 많이 분포하며, 신축 매장과 양도 매물이 꾸준해요. 단일 시술 전문 매장보다 매장 규모가 크고 직원 수가 많아 동료와의 협업이 중요한 환경입니다.",
        "market_types": [
            "<strong>대형 종합 에스테틱</strong> — 시술실 10개 이상·직원 15명+. 정규직·교대제.",
            "<strong>중형 종합샵</strong> — 시술실 4~8개·직원 6~10명. 가장 흔한 형태.",
            "<strong>피부+체형 결합형</strong> — 자매 매장 연계 운영 다수.",
            "<strong>호텔·리조트 부설 스파</strong> — 외국인 고객 비중 높음.",
        ],
        "qualification_must": [
            "2개 이상 시술 운영 가능 (페이셜+바디 / 체형+왁싱 등)",
            "고객 통합 컨설팅·코스 안내 가능",
            "장기 근속 의지 — 정규직 트랙",
        ],
        "qualification_plus": [
            "피부미용사 국가자격증 보유",
            "기기 운영 경험 — RF·EMS·LED·캐비테이션",
            "실장·원장 경력 또는 매장 운영 보조 경험",
            "외국어 응대 가능자 호텔 스파 우대",
        ],
        "salary_rows": [
            ("신입(1년 미만)", "—", "월 260~300만원"),
            ("경력 1~3년", "—", "월 300~370만원"),
            ("경력 3~5년", "—", "월 370~450만원"),
            ("실장·원장(5년+)", "—", "월 450~700만원+"),
        ],
        "salary_note": "토탈샵은 매출 인센티브가 별도로 붙는 매장이 표준이며, 코스 판매 실적에 따라 월 100~300만원 추가 인센이 일반적입니다. 실장·원장급은 매출 지분 형태로 운영되기도 합니다.",
        "tips_p": "토탈샵은 멀티 시술이 핵심이라 단일 분야만 깊게 파온 관리사보다 두 분야 이상을 어느 정도 다룰 줄 아는 관리사가 유리합니다. 신입은 페이셜 또는 체형 한 분야로 입사한 뒤 6~12개월 차에 두 번째 분야를 본격 배우는 흐름이 일반적이에요. 5년차 이후 실장·원장 트랙으로 가장 자연스럽게 올라갈 수 있는 환경입니다.",
        "safety_items": [
            "근로계약서·4대보험·연차 표준 적용 매장 선택",
            "매출 인센티브 구조 명확히 — 모호한 영업 분담 주의",
            "시술 강요·코스 끼워팔기 강제 압박 매장은 거르세요",
            "본인 손목·허리 보호 — 휴식 시간 보장 매장 확인",
        ],
        "faq": [
            ("토탈샵은 신입도 가능한가요?",
             "신입도 가능하지만 단일 분야 매장보다 진입 난이도가 살짝 높습니다. 페이셜 또는 체형 한 분야로 자격증·교육을 갖추고 입사한 뒤, 매장 내에서 두 번째 분야를 배우는 흐름이 일반적이에요."),
            ("실장·원장 트랙으로 가는 데 얼마나 걸리나요?",
             "보통 5~7년 경력 시 실장, 8~10년 경력 시 원장 또는 본인 매장 오픈으로 이어집니다. 토탈샵은 운영 흐름을 자연스럽게 익힐 수 있어 가장 빠른 트랙 중 하나예요."),
            ("매출 인센티브 구조가 어떻게 되나요?",
             "매장마다 다르지만 일반적으로 본인 매출의 5~15% 인센티브, 신규 고객 유치 시 1인당 보너스 1~3만원, 패키지 판매 시 별도 수당 구조가 흔합니다. 입사 전 구조를 명확히 확인하세요."),
            ("멀티 시술을 다 못해도 채용되나요?",
             "단일 분야 강자도 채용됩니다. 다만 6~12개월 내에 두 번째 분야를 익혀야 한다는 전제가 있는 경우가 많아요. 본인 의지가 있는지 확인하고 입사하시면 됩니다."),
            ("이력서 등록은?",
             '<a href="../resumes/index.html">이력서 등록</a>에서 운영 가능 시술 분야(2개 이상 체크), 기기 경력, 매출 관리 경험을 입력하면 매칭이 빠릅니다.'),
        ],
        "related": [
            ("skincare.html", "피부관리 가이드", "피", "rose", "토탈샵의 핵심 분야"),
            ("body-shaping.html", "체형관리 가이드", "체", "emerald", "함께 운영하는 코스"),
            ("waxing.html", "왁싱 가이드", "왁", "amber", "여성 케어 통합 라인"),
        ],
    },
]


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def render(g: dict) -> str:
    slug = g["slug"]
    url = f"{DOMAIN}/guide/{slug}.html"
    title = f"{g['h1']} - 마사지알바고"
    desc = g["lead"][:160]

    stats_html = "\n".join(
        f'      <div class="stat-box">\n'
        f'        <span class="stat-box__label">{esc(label)}</span>\n'
        f'        <strong class="stat-box__value">{esc(value)}</strong>\n'
        f'      </div>'
        for label, value in g["stats"]
    )

    tasks_html = "\n".join(f"    <li>{esc(t) if '<' not in t else t}</li>" for t in g["overview_tasks"])
    market_types_html = "\n".join(f"    <li>{t}</li>" for t in g["market_types"])
    qual_must_html = "\n".join(f"    <li>{esc(t)}</li>" for t in g["qualification_must"])
    qual_plus_html = "\n".join(f"    <li>{esc(t)}</li>" for t in g["qualification_plus"])

    salary_rows = "\n".join(
        f'      <tr>\n'
        f'        <td>{esc(career)}</td>\n'
        f'        <td><span class="salary-amount">{esc(daily)}</span></td>\n'
        f'        <td><span class="salary-amount">{esc(monthly)}</span></td>\n'
        f'      </tr>'
        for career, daily, monthly in g["salary_rows"]
    )

    safety_html = "\n".join(f"    <li>{esc(t)}</li>" for t in g["safety_items"])

    faq_items = "\n".join(
        f'    <details class="faq"{" open" if i == 0 else ""}>\n'
        f'      <summary>{esc(q)}</summary>\n'
        f'      <p>{a}</p>\n'
        f'    </details>'
        for i, (q, a) in enumerate(g["faq"])
    )

    related_cards = "\n".join(
        f'      <a href="{esc(href)}" class="guide-related-card">\n'
        f'        <span class="guide-related-card__icon gi-{tone}">{esc(icon)}</span>\n'
        f'        <span class="guide-related-card__body">\n'
        f'          <span class="guide-related-card__title">{esc(title)}</span>\n'
        f'          <span class="guide-related-card__sub">{esc(sub)}</span>\n'
        f'        </span>\n'
        f'      </a>'
        for href, title, icon, tone, sub in g["related"]
    )

    # JSON-LD
    faq_jsonld_items = ",\n        ".join(
        f'{{"@type":"Question","name":{json.dumps(q, ensure_ascii=False)},"acceptedAnswer":{{"@type":"Answer","text":{json.dumps(a, ensure_ascii=False)}}}}}'
        for q, a in g["faq"]
    )
    jsonld = f'''{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Article",
      "@id": "{url}#article",
      "headline": {json.dumps(g["h1"], ensure_ascii=False)},
      "description": {json.dumps(desc, ensure_ascii=False)},
      "datePublished": "{TODAY_ISO}",
      "dateModified": "{TODAY_ISO}",
      "author": {{"@id": "{DOMAIN}/#org"}},
      "publisher": {{"@id": "{DOMAIN}/#org"}},
      "mainEntityOfPage": {{"@id": "{url}"}},
      "inLanguage": "ko-KR",
      "articleSection": {json.dumps(g["category"], ensure_ascii=False)},
      "keywords": {json.dumps(g["keywords"], ensure_ascii=False)},
      "image": "{DOMAIN}/favicon.svg"
    }},
    {{
      "@type": "BreadcrumbList",
      "@id": "{url}#breadcrumb",
      "itemListElement": [
        {{"@type":"ListItem","position":1,"name":"홈","item":"{DOMAIN}/"}},
        {{"@type":"ListItem","position":2,"name":"시술별 가이드","item":"{DOMAIN}/guide/"}},
        {{"@type":"ListItem","position":3,"name":{json.dumps(g["category"], ensure_ascii=False)},"item":"{url}"}}
      ]
    }},
    {{
      "@type": "FAQPage",
      "@id": "{url}#faq",
      "mainEntity": [
        {faq_jsonld_items}
      ]
    }},
    {{
      "@type": "Organization",
      "@id": "{DOMAIN}/#org",
      "name": "마사지알바고",
      "url": "{DOMAIN}/",
      "logo": {{"@type":"ImageObject","url":"{DOMAIN}/favicon.svg"}}
    }}
  ]
}}'''

    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<meta name="keywords" content="{esc(g["keywords"])}" />
<meta name="author" content="마사지알바고 편집팀" />
<meta name="theme-color" content="#1E40AF" />
<link rel="icon" type="image/svg+xml" href="../favicon.svg" />
<link rel="apple-touch-icon" href="../favicon.svg" />
<link rel="manifest" href="../manifest.webmanifest" />
<link rel="canonical" href="{url}" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="마사지알바고" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{DOMAIN}/favicon.svg" />
<meta property="article:section" content="{esc(g["category"])}" />
<meta property="article:published_time" content="{TODAY_ISO}" />
<link rel="stylesheet" href="../css/style.css" />
</head>
<body class="guide-page">

<div class="topbar"><div class="container">
  <a href="../guide/index.html">이용 안내</a>
  <a href="../support/index.html#safety">안전 가이드</a>
  <a href="../partners/index.html">제휴 문의</a>
</div></div>

<header class="site-header"><div class="container header-inner">
  <a href="../index.html" class="brand"><img src="/images/logo/logo.png" alt="마사지알바GO" class="brand-img" /></a>
  <nav class="main-nav" aria-label="주메뉴">
    <a href="../jobs/index.html">구인공고</a>
    <a href="../partner-stores/index.html">제휴업소</a>
    <a href="../ads/index.html">상품안내</a>
    <a href="../resumes/index.html">이력서 등록</a>
    <a href="../partners/index.html">업체 가입</a>
    <a href="../guide/index.html" class="active">시술별 가이드</a>
    <a href="../magazine/index.html">매거진</a>
    <a href="../about/index.html">소개</a>
  </nav>
  <div class="header-cta">
    <a href="../jobs/index.html" class="btn btn-primary">구인공고 보기</a>
  </div>
  <button class="menu-toggle" aria-label="메뉴 열기" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
</div></header>

<section class="page-header"><div class="container">
  <div class="breadcrumb"><a href="../index.html">홈</a><span class="sep">/</span><a href="index.html">시술별 가이드</a><span class="sep">/</span><span>{esc(g["category"])}</span></div>
  <span class="guide-category-tag">{esc(g["category"])} 채용 가이드</span>
  <h1>{esc(g["h1"])}</h1>
  <p>{esc(g["lead"])}</p>
  <div class="guide-quick-stats">
{stats_html}
  </div>
  <nav class="anchor-nav">
    <a href="#overview">직무 개요</a>
    <a href="#market">채용 시장</a>
    <a href="#qualification">자격·요건</a>
    <a href="#salary">평균 급여</a>
    <a href="#tips">신입 팁</a>
    <a href="#safety">안전 가이드</a>
    <a href="#faq">FAQ</a>
  </nav>
</div></section>

<div class="article container">

  <div class="callout">
    <strong>검증된 업체만:</strong> 마사지알바고는 사업자 등록 인증을 마친 매장의 {esc(g["category"])} 채용 공고만 노출합니다. 선입금·교육비·유니폼비 요구는 즉시 거절하고 <a href="../support/index.html#safety">안전 가이드</a>를 참고하세요.
  </div>

  <section id="overview">
    <h2>{esc(g["category"])} 관리사 직무 개요</h2>
    <p>{esc(g["overview_p"])}</p>
    <h3>주요 업무</h3>
    <ul class="check-list">
{tasks_html}
    </ul>
  </section>

  <section id="market">
    <h2>{esc(g["category"])} 채용 시장 현황</h2>
    <p>{esc(g["market_p"])}</p>
    <h3>주요 매장 유형</h3>
    <ul class="check-list">
{market_types_html}
    </ul>
  </section>

  <section id="qualification">
    <h2>{esc(g["category"])} 관리사 자격·경력 요건</h2>
    <h3>필수 사항</h3>
    <ul class="check-list">
{qual_must_html}
    </ul>
    <h3>우대 사항</h3>
    <ul class="check-list">
{qual_plus_html}
    </ul>
  </section>

  <section id="salary">
    <h2>{esc(g["category"])} 평균 급여</h2>
    <p>마사지알바고에 등록된 {esc(g["category"])} 공고 표본을 기반으로 한 업계 평균 추정치입니다.</p>
    <table class="salary-table">
      <thead>
        <tr><th>경력</th><th>일급제</th><th>월급제</th></tr>
      </thead>
      <tbody>
{salary_rows}
      </tbody>
    </table>
    <p style="font-size:13.5px;color:#64748B;margin-top:10px;">※ {esc(g["salary_note"])}</p>
  </section>

  <section id="tips">
    <h2>{esc(g["category"])} 신입·이직 팁</h2>
    <p>{esc(g["tips_p"])}</p>
  </section>

  <section id="safety">
    <h2>안전·계약 가이드</h2>
    <ul class="check-list">
{safety_html}
    </ul>
  </section>

  <section id="faq">
    <h2>자주 묻는 질문</h2>
    <div class="faq-list">
{faq_items}
    </div>
  </section>

</div>

<section class="section">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Related</span>
      <h2>다른 시술 가이드</h2>
    </div>
    <div class="guide-related-grid">
{related_cards}
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Apply</span>
      <h2>지금 시작하세요</h2>
      <p>이력서 등록·채용 공고 검색 모두 무료입니다.</p>
    </div>
    <div style="text-align:center; display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
      <a href="../resumes/index.html" class="btn btn-primary btn-lg">이력서 등록</a>
      <a href="../jobs/index.html" class="btn btn-outline btn-lg">구인공고 보기</a>
    </div>
  </div>
</section>

<footer class="site-footer" role="contentinfo">
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
          <li><a href="/magazine/rss.xml" rel="alternate" type="application/rss+xml">RSS 피드</a></li>
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
</footer>

<script src="../js/main.js"></script>

<script type="application/ld+json">
{jsonld}
</script>
</body>
</html>
'''


def main():
    GUIDE_DIR.mkdir(parents=True, exist_ok=True)
    for g in GUIDES:
        path = GUIDE_DIR / f"{g['slug']}.html"
        path.write_text(render(g), encoding="utf-8")
        print(f"[ok] {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

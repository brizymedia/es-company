# -*- coding: utf-8 -*-
"""
큰길이벤트기획의 서류 3종(견적서 · 전자계약서 · 거래명세서)을 이에스컴퍼니용으로 옮긴다.

  python tools/port_docs.py [큰길이벤트 레포 경로]      (기본 ~/Documents/클로드코드)

원본(큰길이벤트)이 바뀌면 다시 돌리면 같은 규칙으로 다시 옮긴다. 이에스컴퍼니 쪽 손수정은 여기 규칙으로 넣을 것.
하는 일: 회사 정보 · 문구 · 예시 · 품목표(렌탈 품목 12종) 교체, 주황 → 이에스 파랑, 머리글 로고 · 메뉴를 이에스컴퍼니 것으로.
바로기획(baro-event/tools/port_docs.py)과 같은 틀.
"""
import os, re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Documents/클로드코드')
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = 'https://www.es-company.co.kr'   # 도메인이 정해지면 바꾸고 다시 돌린다

# 이에스컴퍼니 계약 서버(앱스 스크립트, apps-script/contract) — 형님이 배포하면 /exec 주소를 넣고 다시 돌린다. 비어 있으면 서버 없이 동작.
ES_CONTRACT = 'https://script.google.com/macros/s/AKfycbxPDFzWN8wIOGglva2vDkBDzv1ap8yyrEUmrHPwK5io1II4bYlSFp6kMZk5JjYm6OeO5Q/exec'
# 이에스컴퍼니 입금 계좌 — 박미배 대표에게 받아서 넣는다. 비어 있으면 계약서 제4조가 「을이 지정하는 계좌」로 나간다.
ES_BANK = ''

LOGO = '<img src="assets/img/logo-mark.svg" alt="" style="width:2.3rem;height:2.3rem;display:block">'
LOGO_S = '<img src="assets/img/logo-mark.svg" alt="" style="width:2.1rem;height:2.1rem;display:block">'
MAIL_LOGO = '<img src="' + HOME + '/assets/img/logo-h-white.png" height="32" alt="이에스컴퍼니" style="vertical-align:middle;">'

COMMON = [
    # ── 회사 정보 ──
    ('큰길이벤트기획 (주식회사 브리지미디어)', '이에스컴퍼니'),
    (' <span style="color:#9ca3af;">(주식회사 브리지미디어)</span>', ''),
    ('주식회사 브리지미디어 대표 직인', '이에스컴퍼니 대표 직인'),
    ('(예금주: 주식회사 브리지미디어)', ''),
    ('주식회사 브리지미디어', '이에스컴퍼니'),
    ('큰길이벤트기획', '이에스컴퍼니'),
    ('[큰길이벤트]', '[이에스컴퍼니]'),
    ('큰길이벤트.com/quote.html', 'www.es-company.co.kr/quote.html'),
    ('큰길이벤트.com', 'www.es-company.co.kr'),
    ('김동길', '박미배'),
    ('813-81-02252', '710-09-02317'),
    ("corp:'204611-0065269'", "corp:''"),
    ('전남광주통합특별시 광양시 광양읍 강변동길 1, 2층', '충청북도 청주시 흥덕구 옥산면 오산가좌로 110-13, 1동 1층'),
    ('전남광주통합특별시 광양시 광양읍 강변동길 1', '충청북도 청주시 흥덕구 옥산면 오산가좌로 110-13, 1동 1층'),
    ('1533-7295', '010-2084-0102'),
    ('gilcaro@naver.com', 'esgroup0102@naver.com'),
    ("'KB국민은행 788101-01-397776 '", repr(ES_BANK)),
    ("bank:'KB국민은행 788101-01-397776 '", 'bank:' + repr(ES_BANK)),
    ("'KG-'", "'ES-'"),
    ('data-site="keungil"', 'data-site="es"'),
    ('keungil-quote-box', 'es-quote-box'),
    ('keungil-contract', 'es-contract'),
    ('keungil-statement', 'es-statement'),
    ('우리(큰길)', '우리(이에스컴퍼니)'),
    # ── 예시 문구 ──
    ('예) 광양시청 / ○○총동문회', '예) 청주시 ○○동 주민자치회 / ○○초등학교'),
    ('예) 광양시 광양읍 일원', '예) 청주 ○○공원 (잔디 · 차량 진입 가능)'),
    ('예) 제25회 광양 매화축제', '예) 2026 ○○초등학교 가을 운동회'),
    ('예) 고흥군청 문화관광과', '예) 충주시 ○○동 행정복지센터'),
    ('고흥군 녹동항 일원', '충주 ○○공원 잔디광장'),
    ('2026 녹동바다불꽃축제 무대음향 운영', '2026 ○○ 가족행사 천막 · 테이블 · 음향 렌탈'),
    ('음향 · 조명 · LED · 무대', '천막 · 테이블 · 의자 · 무대 음향'),
    ("spec:'전남 외 지역'", "spec:'충북 · 충남 · 세종 · 대전 외 지역'"),
    # ── 아이콘 · 파비콘 ──
    ('<link rel="icon" href="/favicon.ico" sizes="32x32">\n', ''),
    ('href="/favicon.svg"', 'href="assets/img/favicon.svg"'),
    ('<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n', ''),
    ('  <link rel="alternate" type="application/rss+xml" title="이에스컴퍼니 소식" href="/rss.xml">\n', ''),
    ('src="logo-kgm-transparent.png"', 'src="assets/img/logo-mark.svg"'),
    # ── 색: 주황 → 이에스 파랑 (로고 #074EA2 · #002561) ──
    ('#F59E0B', '#074EA2'), ('#FBBF24', '#4A8FE7'), ('#D97706', '#063E82'), ('#B45309', '#002561'),
    ('#FCD34D', '#9CC3F5'), ('#a05c00', '#002561'), ('#09090b', '#0A1F45'), ('#0B0A10', '#0A1F45'),
    ('#16141C', '#102A5C'), ('#131317', '#102A5C'),
    ('rgba(245,158,11', 'rgba(7,78,162'), ('rgba(251,191,36', 'rgba(74,143,231'),
    ('rgba(9,9,11', 'rgba(10,31,69'), ('rgba(11,10,16', 'rgba(10,31,69'),
]

NAV = [
    ('href="index.html#services"', 'href="service.html"'),
    ('href="index.html#portfolio"', 'href="portfolio.html"'),
    ('href="index.html#gallery"', 'href="portfolio.html"'),
    ('href="index.html#contact"', 'href="contact.html"'),
    ('href="/blog/"', 'href="blog/index.html"'),
    ('href="/stories/"', 'href="blog/index.html"'),
    ('>행사이력</a>', '>현장사진</a>'),
    ('href="/quote.html', 'href="quote.html'), ('href="/contract.html', 'href="contract.html'), ('href="/"', 'href="index.html"'),
    ('>블로그</a>', '>행사 가이드</a>'),
    ('TOTAL EVENT AGENCY', 'ES COMPANY'),
    ('src="/quote-catalog.js"', 'src="quote-catalog.js"'),
]

# 렌탈 품목 — service.html 의 12개 카드와 같은 이름. 단가는 전부 협의(null)라 금액은 안 나오고 「협의」로 찍힌다.
CATALOG = """const CATALOG = [
  { group:'천막 · 텐트', items:[
    { id:'t1', name:'캐노피천막 3m×3m',  spec:'판매 · 체험 · 안내 부스 기본형 · 설치 · 철거 포함', unit:'동', price:null, qty:true },
    { id:'t2', name:'캐노피천막 3m×6m',  spec:'넓은 부스 · 본부석 · 급식 공간',              unit:'동', price:null, qty:true },
    { id:'t3', name:'몽골텐트',          spec:'운영본부 · 체험 프로그램 · 휴게 공간',          unit:'동', price:null, qty:true },
    { id:'t4', name:'부스천막',          spec:'박람회 · 설명회용 조립 부스 · 간판 · 칸막이',    unit:'동', price:null, qty:true },
    { id:'t5', name:'옆면 가림막',       spec:'햇빛 · 바람 · 비 가림',                        unit:'면', price:null, qty:true },
  ]},
  { group:'테이블 · 의자', items:[
    { id:'d1', name:'듀라테이블',        spec:'접이식 1800 · 진열 · 접수 · 체험 · 급식',        unit:'개', price:null, qty:true },
    { id:'d2', name:'테이블보 · 스커트', spec:'테이블 크기에 맞춰',                            unit:'장', price:null, qty:true },
    { id:'d3', name:'의자',              spec:'관람석 · 대기석 · 체육관 행사용',                unit:'개', price:null, qty:true },
    { id:'d4', name:'의자 커버',         spec:'협약식 · 기념식 · 내빈석',                      unit:'개', price:null, qty:true },
    { id:'d5', name:'파라솔세트',        spec:'파라솔 + 테이블 + 의자 · 휴게 · 먹거리 존',      unit:'세트', price:null, qty:true },
    { id:'d6', name:'캠핑세트',          spec:'캠핑의자 · 캠핑테이블 · 그늘막',                unit:'세트', price:null, qty:true },
    { id:'d7', name:'다과테이블',        spec:'다과 · 케이터링 세팅용',                        unit:'개', price:null, qty:true },
  ]},
  { group:'무대 · 음향', items:[
    { id:'s1', name:'무대 (덱 · 계단)',  spec:'크기 · 높이 협의 · 설치 · 철거 포함',           unit:'식', price:null },
    { id:'s2', name:'연단 (포디움)',     spec:'개회사 · 축사',                                unit:'개', price:null, qty:true },
    { id:'s3', name:'아크릴단상',        spec:'투명 아크릴 연단',                              unit:'개', price:null, qty:true },
    { id:'s4', name:'음향 세트',         spec:'스피커 · 무선 마이크 · 믹서 · 운영',            unit:'식', price:null },
    { id:'s5', name:'무선 마이크 추가',  spec:'핸드 / 핀 마이크',                             unit:'개', price:null, qty:true },
    { id:'s6', name:'포토존 트러스',     spec:'트러스 구조물 + 현수막 · 백월',                 unit:'식', price:null },
  ]},
  { group:'부스 · 안전 · 안내', items:[
    { id:'b1', name:'나무매대',          spec:'실내 축제 · 로비 판매 부스용 나무 프레임',       unit:'개', price:null, qty:true },
    { id:'b2', name:'하드펜스',          spec:'인파 통제 · 구역 구분',                        unit:'개', price:null, qty:true },
    { id:'b3', name:'줄 차단봉',         spec:'대기 줄 · 동선 구분',                          unit:'개', price:null, qty:true },
    { id:'b4', name:'일반배너 · X배너',  spec:'부스명 · 안내 문구 출력 포함',                  unit:'개', price:null, qty:true },
    { id:'b5', name:'자이언트배너',      spec:'대형 안내 · 행사명',                            unit:'개', price:null, qty:true },
    { id:'b6', name:'A보드 안내판',      spec:'입구 · 동선 안내',                             unit:'개', price:null, qty:true },
    { id:'b7', name:'태극기 · 기관기',   spec:'기념식 · 협약식 무대',                          unit:'식', price:null },
  ]},
  { group:'계절 · 기타 용품', items:[
    { id:'e1', name:'삿갓난로',          spec:'겨울 야외 행사',                               unit:'대', price:null, qty:true },
    { id:'e2', name:'대형 선풍기',       spec:'여름 야외 행사',                               unit:'대', price:null, qty:true },
    { id:'e3', name:'아이스박스 · 보온통', spec:'급수 · 음료 · 급식 공간',                    unit:'개', price:null, qty:true },
    { id:'e4', name:'케이블 프로텍터',   spec:'통로 가로지르는 전선 보호',                     unit:'개', price:null, qty:true },
  ]},
  { group:'기획 · 운영', items:[
    { id:'p1', name:'행사기획 · 배치도', spec:'공간 구성 · 품목 수량 산출 · 동선',             unit:'식', price:null },
    { id:'p2', name:'현장 운영 스태프',  spec:'설치 · 행사 중 대응 · 철거',                    unit:'명', price:null, qty:true },
    { id:'p3', name:'운반 · 설치 · 철거', spec:'상하차 · 설치 · 철수 인건비',                  unit:'식', price:null },
    { id:'p4', name:'출장비',            spec:'충북 · 충남 · 세종 · 대전 외 지역',             unit:'식', price:null },
  ]},
];"""


def dedupe_nav(s):
    # 큰길이벤트는 「행사이력」「갤러리」가 따로지만 이에스컴퍼니는 둘 다 현장사진 페이지 — 갤러리 줄은 뺀다
    s = re.sub(r'\s*<a href="portfolio\.html"[^>]*>갤러리</a>', '', s)
    return s


def rep_all(s, pairs):
    for a, b in pairs:
        s = s.replace(a, b)
    return s


def logo_fix(s):
    s = re.sub(r'<span style="display:grid;place-items:center;width:2\.3rem;height:2\.3rem;[^"]*">KG</span>', LOGO, s)
    s = re.sub(r'<span style="display:grid;place-items:center;width:2\.1rem;height:2\.1rem;[^"]*">KG</span>', LOGO_S, s)
    s = re.sub(r'<span style="display:inline-block;width:32px;height:32px;line-height:32px;text-align:center;\s*background:#074EA2;[^"]*">KG</span>\s*<span style="[^"]*">이에스컴퍼니</span>', MAIL_LOGO, s)
    s = s.replace('<a class="brand" href="index.html"><i>KG</i> 이에스컴퍼니</a>', '<a class="brand" href="index.html"><img src="assets/img/logo-mark.svg" alt="" style="width:26px;height:26px;vertical-align:-7px;margin-right:6px">이에스컴퍼니</a>')
    return s


def no_stamp(s):
    # 대표 인감(투명 PNG) = assets/img/stamp-es.png (2026-10-10 박 대표 전달분). 세 서류 모두 이 파일을 찍는다.
    s = s.replace('<img class="stamp" src="stamp-keungil.png" alt="이에스컴퍼니 대표 직인"',
                  '<img class="stamp" src="assets/img/stamp-es.png" alt="이에스컴퍼니 대표 직인"')
    s = s.replace("'stamp-keungil.png'", "'assets/img/stamp-es.png'")
    s = s.replace("'https://xn--wk0bn7yi8h24iszc.com/stamp-keungil.png'", "'" + HOME + "/assets/img/stamp-es.png'")
    s = s.replace('src="stamp-keungil\\.png', 'src="assets\\/img\\/stamp-es\\.png')
    return s


def servers(s):
    s = re.sub(r"'https://script\.google\.com/macros/s/AKfycbwgO5Ry[A-Za-z0-9_-]+/exec'", repr(ES_CONTRACT) if ES_CONTRACT else "''", s)
    return s


def port(name, extra=None):
    s = open(os.path.join(SRC, name), encoding='utf-8').read()
    s = rep_all(s, COMMON)
    s = rep_all(s, NAV)
    s = dedupe_nav(s)
    s = logo_fix(s)
    s = no_stamp(s)
    s = servers(s)
    if extra: s = extra(s)
    left = [w for w in ('큰길', '김동길', '광양', '브리지미디어', '788101', 'xn--wk0', 'keungil', 'KG<', '>KG', '바로기획') if w in s]
    open(os.path.join(SITE, name), 'w', encoding='utf-8', newline='\n').write(s)
    print(name, '남은 흔적:', left or '없음')


def quote_extra(s):
    # 큰길 바닥글의 「관리자(office.html)」 링크 — 이에스컴퍼니에는 그 페이지가 없다
    s = re.sub(r'\s*·\s*<a style="color:inherit;" href="/office\.html"[^>]*>.*?</a>', '', s, count=1, flags=re.S)
    if 'const CATALOG = [' in s:   # 옛 원본: 품목표가 quote.html 안에 있던 때
        a = s.index('const CATALOG = ['); b = s.index('];', a) + 2
        s = s[:a] + CATALOG + s[b:]
    s = re.sub(r'<title>.*?</title>', '<title>자동 견적서 — 천막 · 테이블 · 의자 · 무대 음향 렌탈 | 이에스컴퍼니</title>', s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="청주 · 충북 · 충남 · 세종 · 대전 행사용품 렌탈 견적을 품목만 골라 바로 문의하세요. 캐노피천막 · 몽골텐트 · 듀라테이블 · 의자 · 파라솔세트 · 무대 음향 · 포토존 트러스 · 하드펜스까지. 이에스컴퍼니 010-2084-0102">\n  <meta name="robots" content="noindex,nofollow">', s, count=1)
    return s


def contract_extra(s):
    s = s.replace('.brand img{ height:1.8rem;filter:brightness(0) invert(1) drop-shadow(0 0 6px rgba(7,78,162,.5)); }', '.brand img{ height:1.8rem; }')
    s = re.sub(r"const STAMP_SRC = 'assets/img/stamp-es\.png';[^\n]*", "const STAMP_SRC = 'assets/img/stamp-es.png';  // 대표 인감(투명 PNG)을 이 이름으로 넣으면 찍힌다. 없으면 「(인)」", s)
    s = s.replace('return `<div class="seal-css">${esc(C.co.brand||C.co.name)}<br>대표<br>인</div>`;', 'return `<div class="seal-none">(인)</div>`;')
    s = s.replace('<span class="stamp-flag ok">날인 완료</span>', "${stampOK?'<span class=\"stamp-flag ok\">날인 완료</span>':''}")
    s = s.replace('  #paper .stamp-flag.ok{', '  #paper .party .sig-slot .box .seal-none{ position:absolute;right:6mm;top:50%;transform:translateY(-50%);color:#9CA3AF;font-size:10pt; }\n  #paper .stamp-flag.ok{', 1)
    s = s.replace('<title>전자계약서 — 이에스컴퍼니</title>', '<title>전자계약서 — 이에스컴퍼니</title>\n<meta name="robots" content="noindex,nofollow">')
    return s


def statement_extra(s):
    s = s.replace("우리.name + ' (' + 우리.brand + ')'", "우리.name")
    s = s.replace("esc(우리.name) + ' (' + esc(우리.brand) + ')'", "esc(우리.name)")
    s = s.replace("esc(우리.name) + ' (' + esc(우리.brand) + ')</b>", "esc(우리.name) + '</b>")   # 바닥글 「이에스컴퍼니 (이에스컴퍼니)」 방지
    s = s.replace("우리.name + ' (' + 우리.brand + ') · ' + 우리.tel", "우리.name + ' · ' + 우리.tel")
    s = s.replace('alt="이에스컴퍼니 대표 직인">', 'alt="이에스컴퍼니 대표 직인" onerror="this.remove()">')
    s = s.replace('<title>거래명세서 — 이에스컴퍼니</title>', '<title>거래명세서 — 이에스컴퍼니</title>\n<meta name="robots" content="noindex,nofollow">')
    return s


def port_catalog():
    """quote-catalog.js — 원본은 큰길 품목표 + 견적 코드 읽기 함수. 품목표만 이에스컴퍼니 것으로 바꾸고 함수는 그대로."""
    src = os.path.join(SRC, 'quote-catalog.js')
    if not os.path.exists(src): print('quote-catalog.js 원본 없음 — 건너뜀'); return
    s = open(src, encoding='utf-8').read()
    s = rep_all(s, COMMON)
    a = s.index('const CATALOG = ['); b = s.index('\n];', a) + 3
    s = s[:a] + CATALOG + s[b:]
    open(os.path.join(SITE, 'quote-catalog.js'), 'w', encoding='utf-8', newline='\n').write(s)
    left = [w for w in ('큰길', '김동길', '광양', '브리지미디어', '전남') if w in s]
    print('quote-catalog.js 남은 흔적:', left or '없음')


if __name__ == '__main__':
    port_catalog()
    port('quote.html', quote_extra)
    port('contract.html', contract_extra)
    port('statement.html', statement_extra)

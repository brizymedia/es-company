# -*- coding: utf-8 -*-
"""
검색 노출 보강 (네이버 · AI 검색) — build_blog.py 가 끝난 뒤 실행된다 (build_blog 의 __main__ 이 부른다).

 1. 지역 페이지 14개 areas/<slug>.html + areas/index.html — 「청주 천막 대여」 같은 지역 검색용. 지역마다 다른 글 · 사례 · FAQ.
 2. 갤러리(대문 9장 · 현장사진 39장) · 블로그 글 목록을 HTML 로 미리 그려 넣는다 — 네이버 로봇은 JS 를 잘 안 돌린다.
 3. llms.txt — AI 검색(ChatGPT · Perplexity · 네이버 AI 브리핑 등)이 회사를 요약할 때 읽는 파일.
 4. rss.xml — 행사 가이드 피드 (네이버 서치어드바이저 「RSS 제출」용).
 5. robots.txt — AI 수집 로봇 명시 허용 · sitemap 에 지역 페이지 추가.
 6. service.html 에 렌탈 품목 ItemList 구조화 데이터, 전 페이지 바닥글에 지역 링크.
"""
import os, re, json, html
import build_blog as B

SITE, BASE = B.SITE, B.BASE
AREAS_DIR = os.path.join(SITE, 'areas')

# ------------------------------------------------------------------ 지역 14곳
REGIONS = [
 dict(slug='cheongju', name='청주', sido='충청북도', drive='본사가 있는 곳 — 옥산면 창고에서 시내 어디든 30분 안',
  intro='이에스컴퍼니 본사와 창고가 청주시 흥덕구 옥산면에 있습니다. 청주 시내 · 오창 · 오송 · 청원 · 상당 · 서원 어디든 당일 설치 · 당일 철거가 가능하고, 급한 추가 수량도 창고에서 바로 싣고 갑니다.',
  events=['한국와인데이 썸머페스티벌(8월) — 실내 아트리움 나무 프레임 부스 · 테이블 · 의자', '오스코(청주 전시장) 세미나 — 테이블 · 의자 수백 조 강의식 세팅', '충북 식품산업 상생협약식 — 의자 커버 · 배너 · 다과 테이블', '초록우산 충북 아이리더 발대식 — 라운드테이블 · 무대 · 음향'],
  tips=['청주 시내 축제는 실내 아트리움 · 로비에서 열리는 경우가 많아 천막 대신 나무매대 · 부스천막을 씁니다.', '학교 운동회는 흙 운동장이 많아 팩 고정, 트랙 옆은 웨이트 고정으로 나눕니다.', '오스코 · 호텔 연회장은 전날 저녁 세팅이 원칙입니다.'],
  faq=[('청주 시내 당일 추가 주문도 되나요?', '네. 옥산 창고에서 30분 안에 닿으니 행사 당일 테이블 · 의자 추가도 받습니다. 성수기에는 전날까지 알려 주시면 더 확실합니다.'), ('청주 어느 동네까지 가나요?', '청주 전역(상당 · 서원 · 흥덕 · 청원)과 오창 · 오송 · 내수 · 미원 등 읍면 모두 갑니다.'), ('설치만 하고 철거는 다음 날 해도 되나요?', '네. 장소 사용 조건에 맞춰 야간 철거 · 다음 날 아침 철거 모두 가능합니다.')]),
 dict(slug='chungju', name='충주', sido='충청북도', drive='청주 본사에서 1시간 안팎',
  intro='충주는 기업 가족행사와 학교 운동회, 봉숭아꽃잔치 같은 지역 축제 현장을 여러 차례 진행했습니다. 낮부터 밤까지 이어지는 행사가 많아 천막 · 테이블과 함께 야간 부스 구성까지 준비합니다.',
  events=['에코그린데이 기업 가족행사 — 야간 부스 천막 · 핑크 캐노피 · 테이블', '충주 고등학교 운동회 — 학년별 파란 천막 · 본부석', '충주 봉숭아꽃잔치 — 체험 대기줄과 공연 관람 동선 분리', '충주 체육행사 · 7월 여름행사 장비 구성'],
  tips=['탄금대 · 호암지 같은 공원 잔디밭은 팩 금지인 곳이 많아 물통 웨이트로 고정합니다.', '기업 가족행사는 체험 · 판매 · 운영 구역을 천막 색으로 나누면 안내가 쉽습니다.', '충주 시내 학교는 새벽 5시 30분 설치 기준으로 일정을 잡습니다.'],
  faq=[('충주까지 출장비가 따로 붙나요?', '충북 안은 기본 운반 · 설치비에 포함합니다. 견적서에 항목별로 적어 드리니 숨은 비용이 없습니다.'), ('밤 10시까지 하는 행사도 철거되나요?', '네. 야간 철거 또는 다음 날 아침 철거를 고르실 수 있습니다. 주택가 근처는 조용히 접어서 철수합니다.'), ('충주 공단 · 공장 마당 행사도 하나요?', '네. 아스팔트 바닥은 웨이트 고정으로 설치합니다.')]),
 dict(slug='jecheon', name='제천', sido='충청북도', drive='청주 본사에서 1시간 30분 안팎',
  intro='제천은 열대야 페스타 같은 여름 축제와 학교 운동회, 지역 축제 장비를 맡았습니다. 아스팔트 · 잔디 · 흙 등 바닥이 제각각이라 설치 방식을 현장에 맞춰 바꿉니다.',
  events=['제천 열대야 페스타 — 여름 축제 테이블 · 의자 · 천막', '제천 학교 운동회 — 운동장 트랙 옆 캐노피 천막 일렬 설치', '제천 축제 행사장비 — 수량 산출 기준', '제천 행사용 천막 — 아스팔트와 잔디밭 설치 방식'],
  tips=['의림지 · 청풍호 쪽 야외 행사는 바람이 있어 천막 웨이트를 한 동당 6개로 늘립니다.', '여름 축제는 대형 선풍기 · 아이스박스 · 파라솔세트를 같이 잡는 편이 좋습니다.', '먼 거리라 전날 설치가 기본이고, 새벽 출발 당일 설치도 가능합니다.'],
  faq=[('제천은 멀어서 설치가 늦지 않나요?', '전날 오후 설치를 기본으로 잡고, 당일 설치면 새벽 4시에 출발합니다. 행사 시작 2시간 전에는 끝냅니다.'), ('학교 운동회 천막은 몇 동 필요한가요?', '학급당 한 동을 기본으로 본부 · 급수 · 응급 · 내빈석을 더합니다. 학급 수를 알려 주시면 배치도와 함께 수량을 잡아 드립니다.'), ('축제 이틀 행사면 장비를 두고 가나요?', '네. 행사 기간 내내 두고 쓰고, 야간 보관 · 우천 대비를 같이 계획합니다.')]),
 dict(slug='jeungpyeong', name='증평', sido='충청북도', drive='청주 본사에서 30분 안팎',
  intro='증평은 청주에서 가까워 당일 설치 · 당일 철거가 가장 편한 지역입니다. 전통문화축제, 장뜰들노래축제, 주민행사처럼 체험과 공연이 함께 있는 야외행사를 여러 번 진행했습니다.',
  events=['증평 전통문화축제 — 체험 부스 천막 · 관람 의자 · 음향', '장뜰들노래축제 — 체험과 공연이 함께 있는 야외행사 구성', '증평 주민행사 — 장비 대여부터 빠른 세팅까지', '증평 행사장 천막 옆면 가림막 — 햇빛 · 바람 대비'],
  tips=['보강천 · 공원 행사는 통로를 먼저 그리고 테이블을 놓습니다.', '체험 부스는 캐노피, 운영본부는 몽골텐트로 나누면 안내가 쉽습니다.', '가까운 거리라 행사 중 추가 수량도 바로 가져갑니다.'],
  faq=[('증평 소규모 주민행사도 받나요?', '네. 천막 몇 동 · 테이블 몇 개 규모도 진행합니다. 품목만 골라 쓰셔도 됩니다.'), ('옆면 가림막은 언제 다나요?', '바람이 잦거나 햇빛이 한쪽으로 들어오는 자리에 한쪽만 다는 편이 좋습니다. 현장을 보고 정합니다.'), ('당일 설치가 가능한가요?', '네. 30분 거리라 아침 설치 · 저녁 철거가 기본입니다.')]),
 dict(slug='jincheon', name='진천', sido='충청북도', drive='청주 본사에서 30~40분',
  intro='진천은 산업단지 기업행사와 공원 야외행사, 대학입시박람회 같은 실내 행사까지 폭이 넓습니다. 공원 행사는 그늘 · 물 · 전기 세 가지를 저희가 만들어야 하므로 천막 · 급수대 · 발전기를 같이 잡습니다.',
  events=['진천 기업행사 — 공원 테이블 · 의자 · 급수 공간 구성', '진천 대학입시박람회 — 운영 공간에 맞는 장비 · 조립 부스', '진천 지역축제 — 작은 장비 차이가 분위기를 바꾸는 구성', '진천 여름 야외행사 — 부스와 그늘 공간'],
  tips=['공원 사용 허가 조건(팩 · 전기 · 차량 진입)을 미리 알려 주시면 그에 맞춰 준비합니다.', '산단 공장 마당 행사는 아스팔트 웨이트 고정, 테이블 다리 받침으로 바닥을 보호합니다.', '박람회는 부스명 사인과 안내 테이블을 부스마다 넣습니다.'],
  faq=[('진천 산업단지 안 공장 행사도 가능한가요?', '네. 공장 마당 · 주차장 행사도 많이 합니다. 차량 진입로와 전기 위치만 알려 주세요.'), ('공원 행사에 전기가 없으면요?', '발전기를 가져가고 케이블 프로텍터로 통로를 덮습니다.'), ('테이블보 · 의자 커버도 같이 되나요?', '네. 내빈석만 씌우거나 전체를 씌우거나 고르실 수 있습니다.')]),
 dict(slug='goesan', name='괴산', sido='충청북도', drive='청주 본사에서 1시간 안팎',
  intro='괴산은 고추축제 같은 농산물 축제와 장터 행사, 여름 야외행사, 문화공연 · 먹거리 부스 운영을 맡아 왔습니다. 판매 부스가 많은 축제라 천막 · 테이블 수량과 대기 줄 동선이 핵심입니다.',
  events=['괴산 고추축제 — 판매 부스 천막 · 테이블 · 차단봉', '괴산 천막 렌탈 — 농산물 축제와 장터 행사', '괴산 여름 야외행사 — 무더위 속 행사장 준비', '괴산 문화공연 · 먹거리 부스 운영'],
  tips=['농산물 판매 부스는 부스당 테이블 1.5개 기준으로 예비 수량을 가져갑니다.', '먹거리 존은 판매 부스 : 테이블 = 1 : 4 로 잡습니다.', '성수기(9~10월) 축제는 한 달 전 수량 확정을 권합니다.'],
  faq=[('괴산 고추축제 같은 큰 축제도 되나요?', '네. 부스 수십 동 · 테이블 수백 개 규모도 전날 설치로 진행합니다.'), ('장터 행사 셀러가 당일 테이블을 더 달라고 하면요?', '예비 수량을 가져가서 현장에서 바로 추가해 드리고, 쓴 만큼만 정산합니다.'), ('괴산 읍면 어디든 가나요?', '네. 괴산읍 · 청천 · 연풍 · 칠성 등 전 읍면 갑니다.')]),
 dict(slug='eumseong', name='음성', sido='충청북도', drive='청주 본사에서 40분 안팎',
  intro='음성은 품바축제처럼 공연이 많은 야외행사와 전통시장 이벤트, 소규모 공연, 야외 체육행사 장비를 진행했습니다. 공연 행사는 무대 · 음향과 관람 의자를, 시장 행사는 경품 · 홍보 부스 테이블을 중심으로 구성합니다.',
  events=['음성 품바축제 — 공연 많은 야외행사 음향 · 관람석', '음성 전통시장 이벤트 — 경품행사 · 홍보 부스', '음성 소규모 공연 — 합리적인 예산 구성', '음성 야외 체육행사 — 천막 · 테이블 공간'],
  tips=['공연 행사는 스피커를 좌우 2개 + 보조로 나누고, 관람 의자는 동시 체류 인원 기준으로 잡습니다.', '전통시장 행사는 통로가 좁아 접이식 테이블을 벽 쪽으로 붙입니다.', '소규모 공연은 음향 세트만으로도 가능합니다.'],
  faq=[('음성 공연 행사 음향만 빌릴 수 있나요?', '네. 스피커 · 무선 마이크 · 믹서 세트만 운영 스태프와 함께 갑니다.'), ('전통시장 안 행사도 설치되나요?', '네. 차량 진입 시간만 시장 상인회와 맞춰 주시면 됩니다.'), ('체육행사 천막은 몇 동이 필요한가요?', '팀당 한 동에 본부 · 급수 · 시상 공간을 더합니다. 팀 수를 알려 주시면 잡아 드립니다.')]),
 dict(slug='danyang', name='단양', sido='충청북도', drive='청주 본사에서 1시간 40분 안팎',
  intro='단양은 야외 플리마켓과 동문 체육대회, 캐노피 천막 설치 현장을 진행했습니다. 강바람이 있는 지역이라 천막 고정을 더 단단히 하고, 플리마켓은 핑크 캐노피처럼 색 천막으로 분위기를 살렸습니다.',
  events=['단양 야외 플리마켓 — 핑크 캐노피 천막 · 셀러 테이블', '단양 동문 체육대회 — 캐노피 천막 · 테이블 · 의자', '단양 야외행사 장비 — 천막과 테이블 설치까지 한 번에', '단양 캐노피 천막 대여 — 장비를 함께 빌릴 때 확인할 기준'],
  tips=['강변 보도블록은 팩을 못 박아 물통 웨이트 6개로 고정합니다.', '플리마켓은 같은 색 천막을 한 줄로 세우면 사진이 살아납니다.', '먼 거리라 새벽 출발 당일 설치 또는 전날 설치로 잡습니다.'],
  faq=[('단양까지 와 주시나요?', '네. 청주 옥산에서 1시간 40분 안팎입니다. 새벽 설치 기준으로 일정을 잡습니다.'), ('색 천막은 어떤 색이 있나요?', '흰색 · 파란색 · 핑크 등 몇 가지를 갖추고 있습니다. 행사 컨셉 색을 알려 주세요.'), ('바람이 세면 천막이 괜찮나요?', '웨이트를 늘리고 옆면 가림막은 바람길을 터서 답니다. 강풍 예보면 미리 협의합니다.')]),
 dict(slug='boeun', name='보은', sido='충청북도', drive='청주 본사에서 1시간 안팎',
  intro='보은은 가을 야외행사와 속리산 일대 지역 행사 장비를 준비합니다. 가을 행사는 아침 서리와 바람 변수가 있어 천막 고정과 난방 용품(삿갓난로)까지 같이 잡는 편이 좋습니다.',
  events=['보은 가을 야외행사 — 번거로운 준비 과정을 덜어내는 장비 구성', '지역 축제 · 주민 행사 천막 · 테이블 · 의자', '학교 운동회 · 체육대회 그늘 천막'],
  tips=['가을 · 겨울 야외 행사는 삿갓난로 · 보온통을 같이 준비합니다.', '산 쪽 행사장은 바람이 있어 웨이트를 늘립니다.', '행사 전날 설치를 기본으로 합니다.'],
  faq=[('보은 소규모 행사도 받나요?', '네. 천막 몇 동 규모도 진행합니다.'), ('가을 행사에 난로도 빌릴 수 있나요?', '네. 삿갓난로를 대여합니다. 수량과 연료는 상담 때 정합니다.'), ('보은 읍면 어디까지 가나요?', '보은읍 · 속리산 · 장안 · 마로 등 전 읍면 갑니다.')]),
 dict(slug='okcheon', name='옥천', sido='충청북도', drive='청주 본사에서 1시간 안팎',
  intro='옥천은 전국연극제 부대행사 · 플리마켓 천막, 텐트부터 무대까지 원스톱 행사 장비를 준비했습니다. 본 공연 무대 바깥의 부대행사 공간(판매 · 체험 · 안내)을 나눠 수량을 잡습니다.',
  events=['옥천 전국연극제 — 부대행사 · 플리마켓 천막 가이드', '옥천 행사 장비 — 텐트부터 무대까지 원스톱 준비'],
  tips=['판매 · 체험 · 안내 공간을 먼저 나눈 뒤 캐노피 · 몽골텐트를 섞어 구성합니다.', '부스 앞 대기 공간 1.5m, 통로 2.5m 를 확보합니다.', '행사 일정 · 장소 · 부스 수만 알려 주시면 수량을 잡아 드립니다.'],
  faq=[('옥천 연극제 같은 문화행사도 되나요?', '네. 본 공연 외 부대행사 공간의 천막 · 테이블 · 의자 · 배너를 준비합니다.'), ('무대까지 한 번에 맡길 수 있나요?', '네. 천막 · 테이블과 무대 · 음향을 한 팀이 세팅하면 동선이 겹치지 않습니다.'), ('옥천까지 설치는 언제 하나요?', '전날 오후 또는 당일 새벽에 합니다.')]),
 dict(slug='yeongdong', name='영동', sido='충청북도', drive='청주 본사에서 1시간 30분 안팎',
  intro='영동은 포도축제 몽골천막, 정원박람회 공간별 대여 품목, 전통시장 행사, 여름 축제 장비를 진행했습니다. 축제 규모가 커서 공간별(판매 · 체험 · 운영 · 휴게) 품목 정리가 중요합니다.',
  events=['영동 포도축제 — 몽골천막 · 부스 · 관람 의자', '영동 정원박람회 — 공간별 대여 품목 정리', '영동 전통시장 행사 — 토요장터 렌탈 장비 구성', '영동 여름 행사 — 8월 축제 장비 체크리스트'],
  tips=['대형 축제는 동시 체류 인원 기준으로 좌석을 잡습니다(방문객 수가 아니라).', '몽골텐트는 운영본부 · 체험, 캐노피는 판매 부스로 나눕니다.', '먼 거리라 전날 설치 · 다음 날 철거가 기본입니다.'],
  faq=[('영동 포도축제 규모도 가능한가요?', '네. 부스 수십 동, 테이블 · 의자 수백 개 규모를 전날 설치로 진행합니다.'), ('정원박람회처럼 며칠 하는 행사는요?', '행사 기간 내내 장비를 두고 쓰고, 야간 보관 · 우천 대비를 같이 계획합니다.'), ('전통시장 행사도 하나요?', '네. 토요장터 · 야간 장터 테이블 · 천막 · 음향을 준비합니다.')]),
 dict(slug='cheonan', name='천안', sido='충청남도', drive='청주 본사에서 1시간 안팎',
  intro='천안 · 아산 등 충남 북부는 청주에서 1시간 안팎이라 자주 갑니다. K컬처박람회처럼 수만 명이 오는 대형 박람회 장비와 안전 세팅, 기업 · 학교 행사 천막 · 테이블을 준비합니다.',
  events=['천안 K컬처박람회 — 대형 박람회 행사장비 · 안전 세팅', '천안 실내 · 야외 박람회 몽골텐트 · 테이블 · 음향', '충남 행사 몽골텐트 — 부스 용도별 준비'],
  tips=['대형 박람회는 차량 2.5톤 진입로와 하차 공간을 답사 때 먼저 확인합니다.', '인파 통제용 하드펜스 · 차단봉을 출입구와 무대 앞에 둡니다.', '실내 전시장은 바닥 보호 매트와 케이블 프로텍터를 기본으로 챙깁니다.'],
  faq=[('천안 · 아산 외 충남 다른 시군도 가나요?', '네. 공주 · 보령 · 서산 · 논산 · 당진 · 홍성 · 예산 · 청양 등 일정이 맞으면 갑니다.'), ('대형 박람회는 답사를 오시나요?', '네. 대형 행사는 답사를 먼저 가서 차량 동선과 전기를 확인합니다.'), ('천안 학교 운동회도 하나요?', '네. 학년별 천막 · 본부석 · 급수대를 준비합니다.')]),
 dict(slug='sejong', name='세종', sido='세종특별자치시', drive='청주 본사에서 30~40분',
  intro='세종은 청주에서 가까워 당일 설치가 편합니다. 학교 체육관 행사의 캠핑의자 · 좌식 테이블, 동문 체육대회, 조치원 복숭아축제 먹거리 존, 공연 행사 무대 · 관람 공간을 진행했습니다.',
  events=['세종 학교 체육관 행사 — 캠핑의자 · 좌식 테이블', '세종 동문 체육대회 — 캐노피천막 · 테이블 · 의자 기본 구성', '세종 먹거리 축제 — 조치원 복숭아축제 현장 준비', '세종 공연 행사 — 무대와 관람 공간 세팅'],
  tips=['체육관은 바닥 보호 매트 · 고무 캡 · 케이블 프로텍터를 기본으로 챙깁니다.', '먹거리 축제는 판매 부스 : 테이블 = 1 : 4 로 잡습니다.', '조치원 · 신도심 · 부강 · 전의 · 금남 모두 갑니다.'],
  faq=[('세종시 신도심 아파트 단지 행사도 되나요?', '네. 관리사무소와 차량 진입 · 설치 시간을 맞춰 주시면 됩니다.'), ('체육관 좌식 행사 캠핑의자는 몇 개까지 되나요?', '학교 한 학년부터 전교생 규모까지 준비합니다. 수량이 크면 미리 날짜를 잡아 주세요.'), ('당일 설치가 가능한가요?', '네. 30~40분 거리라 아침 설치 · 저녁 철거가 기본입니다.')]),
 dict(slug='daejeon', name='대전', sido='대전광역시', drive='청주 본사에서 50분 안팎',
  intro='대전은 기업 · 기관 기념식과 시상식, 세미나 · 박람회 테이블 세팅, 야외 광장 행사 천막을 준비합니다. 호텔 연회장은 라운드테이블 · 의자 커버 · 연단으로 격식을 맞추고, 야외는 천막 · 의자 · 음향으로 구성합니다.',
  events=['대전 · 세종 · 청주 기념식 · 시상식 — 라운드테이블 · 관람석 의자', '기업 · 기관 세미나 · 박람회 테이블 세팅', '야외 광장 행사 천막 · 음향'],
  tips=['연회장 라운드테이블은 8인 기준, 무대와 3m 를 띄웁니다.', '야외 기념식 관람석은 중앙 통로 2m + 좌우 1.5m 를 먼저 잡습니다.', '유성 · 서구 · 중구 · 동구 · 대덕구 전 지역 출장 설치합니다.'],
  faq=[('대전 호텔 연회장도 세팅하나요?', '네. 연회장 자체 테이블이 있으면 커버 · 테이블보 · 연단만도 가능합니다.'), ('의자 커버 색은 무엇이 있나요?', '블랙 · 화이트를 기본으로 하고 리본 색으로 포인트를 줄 수 있습니다.'), ('대전까지 당일 설치가 되나요?', '네. 50분 안팎이라 당일 새벽 설치 · 당일 철거가 가능합니다.')]),
]
BY_SLUG = {r['slug']: r for r in REGIONS}

# ------------------------------------------------------------------ app.js 자료 읽기 (WORKS · BLOG)
def read_js_array(src, name):
    m = re.search(r'var ' + name + r' = \[(.*?)\n  \];', src, re.S)
    body = m.group(1)
    body = re.sub(r'(\{|,)\s*([a-z]+):', r'\1 "\2":', body)   # i: → "i":
    body = re.sub(r"'((?:[^'\\]|\\.)*)'", lambda mm: json.dumps(mm.group(1).replace("\\'", "'"), ensure_ascii=False), body)
    return json.loads('[' + body + ']')

APP = open(os.path.join(SITE, 'assets/app.js'), encoding='utf-8').read()
WORKS = read_js_array(APP, 'WORKS')
BLOG = read_js_array(APP, 'BLOG')
GAL_IDX = [0, 3, 6, 11, 14, 20, 24, 26, 33]   # app.js 대문 9장과 같아야 한다

def work_card(w, k, R=''):
    return ('<figure data-k="%d" data-c="%s"><img src="%sassets/img/works/w%d.webp" alt="%s" loading="lazy" width="1400" height="1050"><figcaption><em>%s · %s</em><b>%s</b></figcaption></figure>'
            % (k, w['c'], R, w['i'], html.escape(w['t']), html.escape(w['o']), w['y'], html.escape(w['t'])))

def blog_row(b, k, limit=10):
    return ('<a href="%s" target="_blank" rel="noopener"%s><small>%s</small><b>%s</b><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M9 7h8v8"/></svg></a>'
            % (b['u'], ' class="hide"' if k >= limit else '', b['d'], html.escape(b['t'])))

def fill(s, open_tag, inner):
    """<div …id="gal"…>…</div> 안을 inner 로 갈아 끼운다 (안에 div 가 없는 경우에만 쓴다)"""
    pat = re.compile(r'(' + re.escape(open_tag) + r')(.*?)(</div>)', re.S)
    assert pat.search(s), open_tag
    return pat.sub(lambda m: m.group(1) + inner + m.group(3), s, count=1)

def prerender():
    p = os.path.join(SITE, 'index.html'); s = open(p, encoding='utf-8').read()
    s = fill(s, '<div class="gal reveal" id="gal">', ''.join(work_card(WORKS[k], k) for k in GAL_IDX))
    open(p, 'w', encoding='utf-8').write(s)
    p = os.path.join(SITE, 'portfolio.html'); s = open(p, encoding='utf-8').read()
    s = fill(s, '<div class="gal" id="pfGrid">', ''.join(work_card(w, k) for k, w in enumerate(WORKS)))
    s = fill(s, '<div class="bloglist reveal" id="blogList" data-limit="10">', ''.join(blog_row(b, k) for k, b in enumerate(BLOG)))
    open(p, 'w', encoding='utf-8').write(s)
    print('prerender: gallery %d/%d · blog %d' % (len(GAL_IDX), len(WORKS), len(BLOG)))

# ------------------------------------------------------------------ 지역 페이지
ITEMS12 = ['캐노피천막', '몽골텐트', '부스천막', '듀라테이블', '파라솔세트', '의자', '무대 음향', '포토존 트러스', '캠핑세트', '나무매대', '하드펜스 · 차단봉', '다과테이블 · 배너 · 삿갓난로 등']

def area_url(r): return BASE + 'areas/' + r['slug'] + '.html'

def render_area(r):
    R = '../'; url = area_url(r)
    title = '%s 행사용품 렌탈 · 천막 · 테이블 · 의자 · 무대 음향 — 이에스컴퍼니' % r['name']
    desc = '%s 행사 천막 · 테이블 · 의자 · 몽골텐트 · 무대 음향 렌탈, 설치 · 철거 포함. %s. 학교 운동회 · 체육대회 · 지역축제 · 기업행사 · 기념식. 이에스컴퍼니 010-2084-0102' % (r['name'], r['drive'])
    kw = ['%s 행사용품 렌탈' % r['name'], '%s 천막 대여' % r['name'], '%s 테이블 의자 대여' % r['name'], '%s 몽골텐트 대여' % r['name'], '%s 무대 음향 렌탈' % r['name'], '%s 운동회 천막' % r['name'], '%s 축제 장비 렌탈' % r['name'], '%s 행사 렌탈' % r['sido']]
    guides = [p for p in B.POSTS if r['name'] in p['title'] or r['name'] == p['region']]
    naver = [b for b in BLOG if b['t'].startswith(r['name'])][:8]
    ld_service = {"@context": "https://schema.org", "@type": "Service", "@id": url + "#service", "name": '%s 행사용품 · 시스템 렌탈' % r['name'], "serviceType": "행사용품 렌탈 · 무대 음향 렌탈 · 행사기획",
                  "provider": {"@id": BASE + "#business"}, "areaServed": {"@type": "Place", "name": r['name'], "containedInPlace": {"@type": "AdministrativeArea", "name": r['sido']}},
                  "description": desc, "url": url,
                  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "렌탈 품목", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Product", "name": n}} for n in ITEMS12]}}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in r['faq']]}
    extra = B.ld(ld_service) + B.ld(ld_faq) + B.breadcrumb([("홈", BASE), ("운영 지역", BASE + 'areas/index.html'), (r['name'], url)]) + B.ld(B.business_ld())
    ev = ''.join('<li>%s</li>' % html.escape(e) for e in r['events'])
    tips = ''.join('<li>%s</li>' % html.escape(t) for t in r['tips'])
    faq = ''.join('<details%s><summary><i>Q</i>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', html.escape(q), html.escape(a)) for i, (q, a) in enumerate(r['faq']))
    gcards = ''.join('<a class="pcard reveal" href="../blog/%s.html"><div class="img" style="background-image:url(../assets/img/blog/b%02d.webp)"><i>%s</i></div><div class="body"><small>%s · 행사 가이드</small><b>%s</b></div></a>' % (p['slug'], p['photos'][0][0], html.escape(p['region']), p['date'].replace('-', '.'), html.escape(p['title'])) for p in guides[:4])
    nrows = ''.join(blog_row(b, 0) for b in naver)
    others = ''.join('<a href="%s.html"%s>%s</a>' % (x['slug'], ' class="on"' if x is r else '', x['name']) for x in REGIONS)
    items = ''.join('<span>%s</span>' % n for n in ITEMS12)
    return f'''<!doctype html>
<html lang="ko">
<head>
{B.head(title, desc, url, BASE + 'assets/img/og.jpg', kw, extra).replace('og:type" content="article"', 'og:type" content="website"')}
</head>
<body>
{B.header(R)}
<main id="top">
<section class="pagehead">
  <div class="bg" style="background-image:url(../assets/img/sec/ph_works.webp)"></div>
  <div class="wrap">
    <div class="crumb"><a href="../index.html">HOME</a><span>›</span><a href="index.html">운영 지역</a><span>›</span><span>{html.escape(r['name'])}</span></div>
    <small>Service Area · {html.escape(r['sido'])}</small>
    <h1>{html.escape(r['name'])} 행사용품 렌탈 · 천막 · 테이블 · 의자 · 무대 음향</h1>
    <p>{html.escape(r['drive'])}. 설치 · 철거까지 이에스컴퍼니가 직접 합니다.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap post-wrap">
    <article class="post area">
      <p class="lead">{html.escape(r['intro'])}</p>
      <h2>{html.escape(r['name'])}에서 진행한 행사</h2>
      <ul>{ev}</ul>
      <h2>{html.escape(r['name'])} 현장에서 챙기는 것</h2>
      <ul>{tips}</ul>
      <h2>{html.escape(r['name'])}에서 자주 찾는 품목</h2>
      <p>캐노피천막 · 몽골텐트 · 부스천막, 듀라테이블 · 파라솔세트 · 의자, 무대 음향 · 포토존 트러스 · 캠핑세트, 나무매대 · 하드펜스 · 차단봉. 필요한 것만 골라 쓰셔도 되고, 기획부터 전부 맡기셔도 됩니다. 단가는 행사 조건에 따라 달라 <a href="../service.html#calc">견적 요청서</a>로 품목 · 수량을 보내 주시면 1영업일 안에 항목별로 답합니다.</p>
      <div class="tags">{items}</div>
      <h2>진행 순서</h2>
      <ul><li><b>상담 · 견적</b> — 날짜 · 장소 · 부스 수 · 인원을 듣고 1영업일 안에 항목별 견적.</li><li><b>현장 조건 확인</b> — 바닥(아스팔트 · 잔디 · 흙) · 차량 진입 · 전기 · 설치 가능 시간. {html.escape(r['name'])}은 {html.escape(r['drive'])}.</li><li><b>품목 · 수량 확정</b> — 공간별 배치와 수량, 세금계산서 · 정산 방식.</li><li><b>설치 → 행사 → 철거</b> — 전날 또는 당일 새벽 설치, 정해진 시간에 철거 · 주변 정리.</li></ul>
      <h2>자주 묻는 질문 — {html.escape(r['name'])}</h2>
      <div class="faq">{faq}</div>
      {('<h2>관련 행사 가이드</h2><div class="pgrid">' + gcards + '</div>') if gcards else ''}
      {('<h2>' + html.escape(r['name']) + ' 현장 이야기 (네이버 블로그)</h2><div class="bloglist">' + nrows + '</div>') if nrows else ''}
      <div class="cta-box">
        <div><b>{html.escape(r['name'])} 행사 준비 중이신가요?</b><span>날짜 · 장소 · 대략의 수량만 알려 주시면 1영업일 안에 항목별 견적과 배치 제안으로 답합니다. 청주 옥산에서 {html.escape(r['name'])}까지 직접 싣고 가서 설치 · 철거합니다.</span></div>
        <div class="btns"><a class="btn btn-pri" href="../contact.html">견적 문의하기{B.ARR}</a><a class="btn btn-white" href="../service.html#calc">품목 골라 요청서 만들기</a><a class="btn btn-white" href="tel:{B.TEL}">{B.TEL}</a></div>
      </div>
    </article>
    <aside class="side">
      <div class="box"><small>OTHER AREAS</small><b>다른 지역</b><div class="arealinks">{others}</div></div>
      <div class="box"><small>RENTAL ITEMS</small><b>렌탈 품목 보기</b><ul class="lnk"><li><a href="../service.html#items">품목 12종 사진 · 설명</a></li><li><a href="../service.html#calc">견적 요청서 만들기</a></li><li><a href="../portfolio.html">현장 사진 39장</a></li></ul></div>
      <div class="box dark"><small>CONTACT</small><b>{B.TEL}</b><p>평일 낮 시간 전화가 가장 빠릅니다. 현장에 있을 때는 문자 · 폼으로 남겨 주세요.</p><a class="btn btn-pri" href="../contact.html">견적 문의</a></div>
    </aside>
  </div>
</section>
</main>
{B.footer(R)}
<script src="../assets/app.js?v=4"></script>
</body>
</html>
'''

def render_areas_index():
    R = '../'; url = BASE + 'areas/index.html'
    title = '운영 지역 | 이에스컴퍼니 — 충북 · 충남 · 세종 · 대전 행사용품 렌탈 출장 설치'
    desc = '청주 · 충주 · 제천 · 증평 · 진천 · 괴산 · 음성 · 단양 · 보은 · 옥천 · 영동 · 천안 · 세종 · 대전. 지역별 행사 사례와 현장 준비 기준, 천막 · 테이블 · 의자 · 무대 음향 렌탈 안내.'
    kw = ['충북 행사 렌탈', '충남 행사 렌탈', '세종 행사 렌탈', '대전 행사 렌탈', '지역별 천막 대여', '이에스컴퍼니 운영 지역']
    cards = ''.join('<a class="pcard reveal" href="%s.html"><div class="img" style="background-image:url(../assets/img/blog/b%02d.webp)"><i>%s</i></div><div class="body"><small>%s</small><b>%s 행사용품 렌탈 · 천막 · 테이블 · 무대 음향</b><p>%s</p></div></a>' % (r['slug'], [20, 10, 21, 25, 4, 8, 9, 14, 26, 0, 27, 1, 3, 24][i], html.escape(r['name']), html.escape(r['sido']), html.escape(r['name']), html.escape(r['drive'])) for i, r in enumerate(REGIONS))
    extra = B.ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": "이에스컴퍼니 운영 지역", "url": url, "hasPart": [{"@type": "WebPage", "name": r['name'] + ' 행사용품 렌탈', "url": area_url(r)} for r in REGIONS]}) + B.breadcrumb([("홈", BASE), ("운영 지역", url)]) + B.ld(B.business_ld())
    return f'''<!doctype html>
<html lang="ko">
<head>
{B.head(title, desc, url, BASE + 'assets/img/og.jpg', kw, extra).replace('og:type" content="article"', 'og:type" content="website"')}
</head>
<body>
{B.header(R)}
<main id="top">
<section class="pagehead">
  <div class="bg" style="background-image:url(../assets/img/sec/ph_about.webp)"></div>
  <div class="wrap">
    <div class="crumb"><a href="../index.html">HOME</a><span>›</span><span>AREAS</span></div>
    <small>Service Area · 14 Regions</small>
    <h1>충북 · 충남 · 세종 · 대전, 청주에서 바로 갑니다.</h1>
    <p>지역마다 해 본 행사와 현장에서 챙기는 기준이 다릅니다. 우리 지역을 눌러 보세요.</p>
  </div>
</section>
<section class="sec"><div class="wrap"><div class="pgrid">{cards}</div></div></section>
</main>
{B.footer(R)}
<script src="../assets/app.js?v=4"></script>
</body>
</html>
'''

def build_areas():
    os.makedirs(AREAS_DIR, exist_ok=True)
    for r in REGIONS:
        open(os.path.join(AREAS_DIR, r['slug'] + '.html'), 'w', encoding='utf-8').write(render_area(r))
    open(os.path.join(AREAS_DIR, 'index.html'), 'w', encoding='utf-8').write(render_areas_index())
    print('areas', len(REGIONS))

# ------------------------------------------------------------------ 본문 페이지에 지역 링크 심기
def link_regions():
    # 대문 지역 띠
    p = os.path.join(SITE, 'index.html'); s = open(p, encoding='utf-8').read()
    ul = '<ul>' + ''.join('<li><a href="areas/%s.html">%s</a></li>' % (r['slug'], r['name']) for r in REGIONS) + '</ul>'
    s = re.sub(r'(<div class="regions" aria-label="운영 지역">.*?)<ul>.*?</ul>', lambda m: m.group(1) + ul, s, count=1, flags=re.S)
    s = s.replace('<a href="about.html#region">충북 · 충남 · 세종 · 대전 전 지역 →</a>', '<a href="areas/index.html">지역별 안내 보기 →</a>')
    open(p, 'w', encoding='utf-8').write(s)
    # 회사소개 지역 칩
    p = os.path.join(SITE, 'about.html'); s = open(p, encoding='utf-8').read()
    for r in REGIONS:
        s = s.replace('<li>%s</li>' % r['name'], '<li><a href="areas/%s.html">%s</a></li>' % (r['slug'], r['name']), 1)
    open(p, 'w', encoding='utf-8').write(s)
    # 바닥글 지역 링크 (정적 5장)
    row = '<p class="flinks">지역별 안내: ' + ' · '.join('<a href="areas/%s.html">%s</a>' % (r['slug'], r['name']) for r in REGIONS) + '</p>\n    '
    for fn in ('index.html', 'about.html', 'service.html', 'portfolio.html', 'contact.html'):
        p = os.path.join(SITE, fn); s = open(p, encoding='utf-8').read()
        s = re.sub(r'\s*<p class="flinks">.*?</p>\n\s*', '\n    ', s, count=1, flags=re.S)
        s = s.replace('    <div class="bot">', '    ' + row + '<div class="bot">', 1)
        open(p, 'w', encoding='utf-8').write(s)
    print('region links ok')

# ------------------------------------------------------------------ service.html 품목 ItemList
def item_list_ld():
    p = os.path.join(SITE, 'service.html'); s = open(p, encoding='utf-8').read()
    cards = re.findall(r'<article class="item reveal"><div class="img" style="background-image:url\((assets/img/sec/[^)]+)\)"></div><div class="body"><small>[^<]*</small><b>([^<]+)</b><p>([^<]+)</p>', s)
    items = [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Product", "name": n, "description": d, "image": BASE + img, "brand": {"@type": "Brand", "name": "이에스컴퍼니"}, "offers": {"@type": "Offer", "availability": "https://schema.org/InStock", "priceCurrency": "KRW", "priceSpecification": {"@type": "PriceSpecification", "description": "행사 조건에 따른 견적"}, "areaServed": "충북 · 충남 · 세종 · 대전", "url": BASE + "service.html#items"}}} for i, (img, n, d) in enumerate(cards)]
    block = '<!-- seo2:start -->\n' + B.ld({"@context": "https://schema.org", "@type": "ItemList", "name": "이에스컴퍼니 렌탈 품목", "numberOfItems": len(items), "itemListElement": items}) + '\n<!-- seo2:end -->\n'
    s = re.sub(r'<!-- seo2:start -->.*?<!-- seo2:end -->\n', '', s, flags=re.S)
    s = s.replace('<link rel="icon" href="assets/img/favicon.svg"', block + '<link rel="icon" href="assets/img/favicon.svg"', 1)
    open(p, 'w', encoding='utf-8').write(s); print('itemlist', len(items))

# ------------------------------------------------------------------ rss · llms · robots · sitemap
def write_rss():
    items = ''.join('<item><title>%s</title><link>%s</link><guid>%s</guid><description>%s</description><pubDate>%s</pubDate></item>\n' % (html.escape(p['title']), B.post_url(p), B.post_url(p), html.escape(p['desc']), p['date'] + 'T09:00:00+09:00') for p in B.POSTS)
    rss = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>이에스컴퍼니 행사 가이드</title><link>%s</link><description>청주 · 충북 · 충남 · 세종 · 대전 행사 준비 가이드 — 천막 · 테이블 · 의자 · 무대 음향 렌탈</description><language>ko</language>\n%s</channel></rss>\n' % (BASE + 'blog/index.html', items))
    open(os.path.join(SITE, 'rss.xml'), 'w', encoding='utf-8').write(rss); print('rss', len(B.POSTS))

def write_llms():
    lines = ['# 이에스컴퍼니 (ES COMPANY)', '', '> 충북 청주에 본사를 둔 행사 파트너. 캐노피천막 · 몽골텐트 · 부스천막 · 듀라테이블 · 파라솔세트 · 의자 · 무대 음향 · 포토존 트러스 · 캠핑세트 · 나무매대 · 하드펜스 · 차단봉 등 행사용품 렌탈과 설치 · 철거, 행사기획을 원스톱으로 제공한다. 충북 전역 · 충남(천안 등) · 세종 · 대전 출장.', '',
             '- 대표 박미배 · 사업자등록번호 710-09-02317 · 충청북도 청주시 흥덕구 옥산면 오산가좌로 110-13, 1동 1층', '- 전화 010-2084-0102 · 이메일 esgroup0102@naver.com · 네이버 블로그 https://blog.naver.com/esgroup0102', '- 견적 회신 1영업일 · 세금계산서 발행 · 설치 · 철거 포함 · 단가는 행사 조건(수량 · 거리 · 기간)에 따라 견적', '',
             '## 서비스', '- 행사기획: 공간 구성 · 품목 수량 산출 · 동선 · 설치 일정', '- 행사용품렌탈: 캐노피천막(3×3 · 3×6) · 몽골텐트 · 부스천막 · 듀라테이블 · 파라솔세트 · 의자 · 캠핑세트 · 나무매대 · 하드펜스 · 차단봉 · 다과테이블 · 아크릴단상 · 배너 · A보드 · 태극기 · 삿갓난로 · 아이스박스 · 보온통', '- 시스템렌탈: 무대(덱 · 계단 · 연단) · 음향(스피커 · 무선 마이크 · 믹서) · 포토존 트러스', '',
             '## 주요 페이지', '- 홈: %s' % BASE, '- 서비스 · 렌탈 품목 · 견적 요청서: %sservice.html' % BASE, '- 현장 사진: %sportfolio.html' % BASE, '- 견적 문의: %scontact.html' % BASE, '- 회사소개 · 운영 지역: %sabout.html' % BASE, '',
             '## 운영 지역 페이지'] + ['- %s: %s' % (r['name'], area_url(r)) for r in REGIONS] + ['', '## 행사 가이드 (지역 · 상황별 준비법)'] + ['- %s: %s' % (p['title'], B.post_url(p)) for p in B.POSTS] + ['', '## 자주 묻는 질문'] + ['- Q. %s\n  A. %s' % (q, a) for q, a in B.CONTACT_FAQ] + ['', '## 참고', '- 사이트맵 %ssitemap.xml · RSS %srss.xml' % (BASE, BASE), '- 홈페이지 제작: 큰길브리지 (주식회사 브리지미디어) https://www.ai-make.co.kr']
    open(os.path.join(SITE, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n'); print('llms.txt')

def write_robots_sitemap():
    bots = ['Googlebot', 'Yeti', 'Bingbot', 'GPTBot', 'ChatGPT-User', 'OAI-SearchBot', 'ClaudeBot', 'Claude-User', 'anthropic-ai', 'PerplexityBot', 'Google-Extended', 'Applebot', 'Amazonbot', 'DuckDuckBot', 'Daum', 'Kakaobot']
    txt = 'User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /apps-script/\n\n' + ''.join('User-agent: %s\nAllow: /\n\n' % b for b in bots) + 'Sitemap: %ssitemap.xml\n' % BASE
    open(os.path.join(SITE, 'robots.txt'), 'w', encoding='utf-8').write(txt)
    p = os.path.join(SITE, 'sitemap.xml'); s = open(p, encoding='utf-8').read()
    s = re.sub(r'  <url><loc>%sareas/.*?</url>\n' % re.escape(BASE), '', s)
    add = ''.join('  <url><loc>%s</loc><lastmod>2026-10-08</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n' % u for u in [BASE + 'areas/index.html'] + [area_url(r) for r in REGIONS])
    s = s.replace('</urlset>', add + '</urlset>')
    open(p, 'w', encoding='utf-8').write(s); print('robots · sitemap', s.count('<loc>'))

def main():
    prerender(); build_areas(); link_regions(); item_list_ld(); write_rss(); write_llms(); write_robots_sitemap()

if __name__ == '__main__':
    main()

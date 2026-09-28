# -*- coding: utf-8 -*-
"""
이에스컴퍼니 홈페이지 — 블로그 글 생성 + 검색 최적화(SEO) 주입
실행: python tools/build_blog.py   (Python 3, 외부 의존성 없음)

하는 일
 1. blog/<slug>.html 10편 + blog/index.html 생성 (사진 · FAQ · 구조화 데이터 포함)
 2. 다섯 본문 페이지에 canonical · og:url · og:image(절대 주소) · LocalBusiness JSON-LD 주입, noindex 제거
 3. sitemap.xml · robots.txt 생성
도메인이 바뀌면 BASE 만 고치고 다시 실행한다.
"""
import os, re, json, html

BASE = 'https://brizymedia.github.io/es-company/'   # ← 도메인 연결 뒤 https://도메인/ 으로 바꾸고 다시 실행
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEL = '010-2084-0102'
ADDR = '충청북도 청주시 흥덕구 옥산면 오산가좌로 110-13, 1동 1층'

# ------------------------------------------------------------------ 글 10편
POSTS = [
{
 'slug': 'cheongju-school-sports-day-tent', 'date': '2026-09-15', 'region': '청주', 'area': '충북',
 'title': '청주 학교 운동회 천막 대여, 학년별 그늘 천막은 몇 동이 필요할까?',
 'desc': '청주 · 충북 초중고 운동회 천막 렌탈 기준. 학년별 대기 천막 수량, 본부석 · 급수 · 응급 공간, 흙 운동장과 트랙 옆 고정 방법, 설치 · 철거 시간까지 이에스컴퍼니가 현장 기준으로 정리했습니다.',
 'kw': ['청주 운동회 천막 대여', '청주 학교 행사 천막 렌탈', '충북 운동회 천막', '학교 운동회 그늘막', '운동회 천막 수량', '청주 행사용품 렌탈'],
 'photos': [(20, '운동장 트랙 옆으로 캐노피 천막을 한 줄로 설치한 학교 운동회 현장'), (12, '충주 고등학교 운동회 — 학년별 파란 천막과 만국기'), (21, '잔디 운동장 둘레에 천막을 배치한 체육행사')],
 'lead': '운동회 준비를 맡은 선생님이 가장 먼저 묻는 질문은 "천막이 몇 동 필요하냐"입니다. 답은 학생 수가 아니라 <b>운동장에 학년이 어떻게 앉느냐</b>에 달려 있습니다. 청주와 충북 학교 운동회 현장에서 저희가 실제로 수량을 잡는 순서를 그대로 적습니다.',
 'sections': [
  ('학년별 대기 천막: 반 수가 아니라 "앉는 줄"로 셉니다', '<p>캐노피 천막 3×3m 한 동에는 학생이 의자 없이 돗자리로 앉을 때 20~25명, 의자를 놓으면 12~15명이 들어갑니다. 학급당 25명 안팎이면 <b>학급당 한 동</b>이 기본이고, 저학년은 학부모가 같이 앉는 경우가 많아 한 동을 더 잡습니다.</p><ul><li>초등 6학급 × 4반 = 24학급 → 천막 24~26동</li><li>중고등학교는 학년 단위로 3×6m 천막을 쓰면 줄이 덜 흐트러집니다</li><li>운동장이 좁으면 천막을 "ㄷ"자로 돌리고 본부석을 짧은 변에 둡니다</li></ul>'),
  ('본부석 · 급수 · 응급 공간은 따로 잡습니다', '<p>학년 천막만 세면 당일에 꼭 모자랍니다. 아래 네 곳은 별도 수량으로 잡아 두세요.</p><ul><li><b>본부석</b> 3×6m 1동 — 방송 장비 · 진행 테이블 2개 · 의자 6개</li><li><b>급수대</b> 3×3m 1~2동 — 접이식 테이블 2개, 얼음물 보관 공간</li><li><b>보건 · 응급</b> 3×3m 1동 — 그늘이 가장 짙은 자리(건물 옆)에</li><li><b>학부모 · 내빈석</b> 3×6m 1~2동 — 의자 커버를 씌우면 내빈석 티가 납니다</li></ul>'),
  ('흙 운동장과 트랙 옆, 고정 방법이 다릅니다', '<p>청주 시내 학교는 흙 운동장과 우레탄 트랙이 섞여 있습니다. 흙바닥은 팩을 박아 고정하고, 트랙 · 아스팔트는 팩을 박을 수 없어 <b>물통 · 모래주머니 웨이트</b>로 다리를 눌러 줍니다. 천막 한 동에 웨이트 4개가 기본이고, 바람이 잦은 봄 · 가을 운동회는 옆면 가림막을 한쪽만 달아 바람길을 터 줍니다.</p><p>설치는 전날 오후나 당일 새벽에 합니다. 학교는 보통 아침 7시부터 학생이 들어오니 <b>새벽 5시 30분 설치 시작</b>이 안전한 기준입니다. 철거는 폐회식 뒤 학생이 빠진 다음 30~40분이면 끝납니다.</p>'),
  ('같이 준비하면 편한 것', '<ul><li>접이식 테이블 — 본부 2 · 급수 2 · 학년 접수 각 1</li><li>플라스틱 의자 — 내빈 · 학부모석 인원 + 여유 10%</li><li>음향 세트(스피커 2 · 무선 마이크 2) — 운동장 크기에 맞춰 스피커 위치를 잡아 드립니다</li><li>줄 차단봉 — 경기 구역과 관람 구역 구분</li></ul>'),
 ],
 'faq': [
  ('청주 초등학교 운동회에 천막은 보통 몇 동 빌리나요?', '학급당 한 동을 기본으로 본부 · 급수 · 응급 · 내빈석을 더해 24학급 학교면 28~30동 정도가 나옵니다. 학급 수와 운동장 크기를 알려 주시면 배치도와 함께 수량을 다시 잡아 드립니다.'),
  ('설치는 언제 하나요? 학교 수업에 지장 없나요?', '전날 오후 수업이 끝난 뒤, 또는 당일 새벽 5시 30분부터 설치합니다. 학생 등교 전에 끝내는 것을 기준으로 일정을 잡습니다.'),
  ('흙 운동장에 팩을 박아도 되나요?', '학교마다 다릅니다. 팩을 박을 수 없으면 물통 · 모래주머니 웨이트로 고정하니 미리 알려 주세요. 트랙 위에는 팩을 쓰지 않습니다.'),
 ],
 'related': ['chungbuk-night-sports-tent', 'sejong-school-gym-camping-chair'],
},
{
 'slug': 'chungju-corporate-event-rental', 'date': '2026-09-14', 'region': '충주', 'area': '충북',
 'title': '충주 기업행사 장비 렌탈, 야간 부스 천막과 조명은 이렇게 준비합니다',
 'desc': '충주 기업행사 · 가족행사 장비 렌탈 가이드. 에코그린데이처럼 낮부터 밤까지 이어지는 행사의 부스 천막, 핑크 캐노피, 야간 조명 · 전력, 잔디 고정과 동선 구성을 이에스컴퍼니 현장 사진으로 설명합니다.',
 'kw': ['충주 기업행사 장비 렌탈', '충주 행사 천막 대여', '충주 야간 행사 조명', '충주 행사용품 렌탈', '기업 가족행사 부스', '충북 기업행사 렌탈'],
 'photos': [(10, '충주 기업행사 — 해가 진 뒤에도 부스가 보이도록 천막마다 조명을 넣은 야간 세팅'), (11, '잔디 위 핑크 캐노피 천막 — 체험 · 판매 부스 구역'), (25, '도심 공원 잔디밭에 천막과 테이블을 세팅한 기업 야외행사')],
 'lead': '기업 가족행사는 오후에 시작해 저녁 공연으로 끝나는 경우가 많습니다. 낮에는 그늘, 밤에는 조명이 필요하고, 잔디밭이라 고정도 다릅니다. 충주에서 진행한 기업행사 현장을 기준으로 <b>낮과 밤을 한 번에 준비하는 방법</b>을 정리했습니다.',
 'sections': [
  ('부스 구역을 색으로 나누면 안내가 쉬워집니다', '<p>체험 부스는 핑크 캐노피, 판매 · 먹거리 부스는 흰색, 운영본부는 파란색처럼 <b>천막 색으로 구역을 나누면</b> 안내 배너를 줄여도 참가자가 길을 찾습니다. 가족행사는 아이들이 뛰어다니니 체험 구역을 무대와 반대편에 두고, 그 사이에 휴게 테이블을 놓아 완충 공간을 만듭니다.</p>'),
  ('야간 행사의 핵심은 조명보다 전력 분배입니다', '<p>천막마다 작업등 하나씩 달면 부스 20동에 20개 전등이 필요합니다. 여기에 무대 조명과 음향까지 한 라인에 물리면 차단기가 내려갑니다. 저희는 <b>부스 조명 · 무대 · 먹거리(전기 조리기구)를 세 라인으로 분리</b>하고, 현장 전기가 부족하면 발전기를 붙입니다. 케이블은 통로를 가로지르지 않게 돌리고, 꼭 가로질러야 하는 곳은 케이블 프로텍터를 깝니다.</p><ul><li>부스 조명: 천막 1동당 LED 작업등 1~2개</li><li>무대 · 음향: 별도 라인 + 필요 시 발전기</li><li>먹거리 부스: 조리기구 용량을 미리 확인 (전기 그릴 · 온장고가 전력을 많이 씁니다)</li></ul>'),
  ('잔디밭 설치: 팩 대신 웨이트, 철거 뒤 잔디 정리까지', '<p>공원 · 회사 잔디밭은 관리 주체가 팩을 금지하는 곳이 많습니다. 물통 웨이트로 고정하고, 테이블 다리 밑에는 받침을 깔아 잔디가 눌리지 않게 합니다. 철거할 때는 케이블 타이 조각과 쓰레기까지 저희가 걷고 나옵니다. 다음 해에 같은 장소를 다시 쓰려면 이 마무리가 중요합니다.</p>'),
  ('충주 기업행사에 자주 나가는 구성', '<ul><li>캐노피 천막 3×3m 15~25동 (색상 2~3종)</li><li>접이식 테이블 30~50개 · 플라스틱 의자 100~200개</li><li>무대 덱 + 스피커 · 무선 마이크 + 조명</li><li>하드펜스 · 줄 차단봉 — 주차장과 행사장 경계</li><li>대형 선풍기 · 파라솔 — 여름 행사</li></ul>'),
 ],
 'faq': [
  ('충주 시내가 아닌 공장 부지에서도 진행하나요?', '네. 충주 시내 · 공단 · 교외 모두 갑니다. 차량 진입로와 전기 위치만 미리 알려 주시면 됩니다.'),
  ('밤 10시까지 하는 행사인데 철거는 언제 하나요?', '행사 종료 직후 야간 철거도 가능하고, 다음 날 아침 철거도 가능합니다. 장소 사용 조건에 맞춰 정합니다.'),
  ('비 예보가 있으면 어떻게 하나요?', '천막 옆면 가림막을 추가하고 웨이트를 늘려 진행하거나, 실내 대안으로 구성을 바꿉니다. 행사 3일 전까지 협의해 주시면 비용 없이 조정합니다.'),
 ],
 'related': ['jincheon-corporate-park-event', 'big-festival-quantity'],
},
{
 'slug': 'sejong-school-gym-camping-chair', 'date': '2026-09-13', 'region': '세종', 'area': '세종',
 'title': '세종 학교 체육관 행사, 캠핑의자 · 좌식 테이블로 바꾸면 달라지는 것',
 'desc': '세종 · 조치원 학교 체육관 행사 렌탈. 일반 의자 대신 캠핑의자와 낮은 테이블을 쓰면 좋은 경우, 체육관 바닥 보호, 좌석 배치와 수량, 음향 세팅을 이에스컴퍼니 현장 사진으로 설명합니다.',
 'kw': ['세종 학교 행사 렌탈', '세종 체육관 행사 의자 대여', '캠핑의자 렌탈', '조치원 학교 행사', '체육관 테이블 대여', '세종 행사용품 렌탈'],
 'photos': [(3, '학교 체육관 — 캠핑의자와 낮은 테이블로 조별 자리를 만든 행사'), (17, '체육관 좌식 긴 테이블 세팅 — 학년 전체가 한 방향을 보는 배치')],
 'lead': '체육관 행사는 의자를 줄 세우는 게 전부라고 생각하기 쉽습니다. 그런데 학생들이 두 시간 넘게 앉아 있는 행사라면 <b>캠핑의자 + 낮은 테이블</b>이 훨씬 편하고, 사진도 잘 나옵니다. 세종 학교 체육관에서 진행한 두 가지 배치를 비교해 드립니다.',
 'sections': [
  ('일반 의자 vs 캠핑의자, 언제 무엇을 쓰나', '<table><tr><th></th><th>일반 의자</th><th>캠핑의자</th></tr><tr><td>맞는 행사</td><td>입학식 · 졸업식 · 강연</td><td>조별 활동 · 축제 · 공연 관람</td></tr><tr><td>공간</td><td>좁게 많이</td><td>여유 있게, 조별로</td></tr><tr><td>분위기</td><td>격식</td><td>편안 · 친근</td></tr><tr><td>테이블</td><td>없거나 앞줄만</td><td>낮은 테이블과 세트</td></tr></table><p>학생 대상 축제나 동아리 발표회처럼 <b>서로 얼굴을 보며 앉는 행사</b>는 캠핑의자가 맞고, 학부모가 많이 오는 공식 행사는 일반 의자에 커버를 씌우는 편이 낫습니다.</p>'),
  ('체육관 바닥은 보호가 먼저입니다', '<p>세종 학교 체육관은 마루나 우레탄 바닥이 많습니다. 테이블 · 의자 다리에 고무 캡을 씌우고, 무대 덱을 놓을 자리에는 보호 매트를 깝니다. 음향 케이블은 벽을 따라 돌리고 출입구 앞은 케이블 프로텍터로 덮습니다. 이 준비를 안 하면 행사 뒤 바닥 긁힘으로 학교와 곤란해집니다.</p>'),
  ('수량 잡는 법: 조 단위로', '<ul><li>캠핑의자 — 학생 수 + 교사 · 진행 10%</li><li>낮은 테이블(좌식 긴 테이블) — 6~8명당 1개</li><li>무대 덱 — 체육관 폭의 1/3 정도, 높이 40~60cm</li><li>음향 — 체육관은 울림이 커서 스피커를 좌우 2개 + 뒤쪽 보조 1~2개로 나눕니다</li></ul>'),
  ('세팅 시간', '<p>학생 300명 규모 체육관은 캠핑의자 300개와 테이블 40개 기준으로 <b>세팅 2시간, 철거 1시간</b>이면 됩니다. 수업 뒤 오후에 설치하고 다음 날 행사 뒤 바로 철거하는 일정이 가장 흔합니다.</p>'),
 ],
 'faq': [
  ('세종시 안이면 어디든 오시나요?', '조치원 · 신도심 · 부강 · 전의 · 금남 모두 갑니다. 청주 옥산에서 30~40분 거리라 당일 설치도 가능합니다.'),
  ('캠핑의자는 몇 개까지 준비되나요?', '학교 한 학년~전교생 규모까지 준비합니다. 수량이 크면 미리 날짜를 잡아 주세요.'),
  ('체육관 바닥 보호 매트는 따로 비용이 드나요?', '무대 · 장비 밑 보호 매트와 케이블 프로텍터는 기본 세팅에 포함해 드립니다.'),
 ],
 'related': ['cheongju-school-sports-day-tent', 'daejeon-ceremony-round-table'],
},
{
 'slug': 'cheongju-festival-booth-setting', 'date': '2026-09-12', 'region': '청주', 'area': '충북',
 'title': '청주 축제 부스 세팅, 와인데이 썸머페스티벌처럼 실내 · 야간 부스 준비법',
 'desc': '청주 축제 부스 렌탈 사례. 2026 한국와인데이 썸머페스티벌 현장처럼 실내 아트리움에 나무 프레임 부스와 흰 테이블 · 의자를 세팅한 방법, 판매 부스 동선, 야간 조명, 배너 설치를 정리했습니다.',
 'kw': ['청주 축제 부스 렌탈', '청주 행사 부스 설치', '와인데이 썸머페스티벌', '청주 행사 테이블 의자 대여', '실내 축제 부스', '청주 행사용품 렌탈'],
 'photos': [(0, '2026 한국와인데이 썸머페스티벌 — 실내 아트리움에 세운 나무 프레임 판매 부스'), (1, '부스 옆 휴게 공간 — 흰 라탄 테이블과 의자'), (2, '부스 정면 — 배너와 테이블보로 통일한 판매 부스 열')],
 'lead': '축제 부스라고 하면 야외 천막을 떠올리지만, 청주 시내 축제는 <b>실내 아트리움이나 건물 로비</b>에서 열리는 경우도 많습니다. 천막 대신 부스 프레임, 바닥 고정 대신 무게추, 그늘 대신 조명이 필요합니다. 와인데이 썸머페스티벌 현장을 기준으로 실내 부스 준비 순서를 적습니다.',
 'sections': [
  ('실내 부스는 "프레임 + 테이블 + 배너" 세 가지로 끝납니다', '<p>실내에서는 천막 지붕이 필요 없으니 <b>나무 · 알루미늄 프레임</b>으로 부스 경계만 세우고, 접이식 테이블에 테이블보를 씌워 진열대를 만듭니다. 부스 이름은 프레임 상단 배너로 통일하면 멀리서도 읽힙니다. 이 구성은 설치가 빨라 부스 30개를 3시간 안에 세울 수 있습니다.</p>'),
  ('판매 부스 동선: 시음 · 결제 · 대기 줄을 나눕니다', '<p>와인 · 먹거리 축제는 시음 줄이 판매대를 막는 게 가장 흔한 문제입니다. 부스 앞 1.5m를 비워 대기 줄을 만들고, 부스 사이 통로는 최소 2.5m를 확보합니다. 줄 차단봉을 부스 3개마다 하나씩 두면 줄이 옆 부스로 넘어가지 않습니다.</p><ul><li>부스 앞 대기 공간 1.5m</li><li>통로 폭 2.5m 이상 (휠체어 · 유모차 교행)</li><li>휴게 테이블은 부스 열과 떨어진 곳에 모아서</li></ul>'),
  ('야간에는 조명이 부스 얼굴입니다', '<p>실내라도 저녁 행사는 천장 조명만으로 부스가 어둡습니다. 프레임 상단에 <b>스트링 라이트나 스팟 조명</b>을 달면 사진이 살고 상품이 보입니다. 전원은 부스 열마다 한 라인씩 돌리고, 바닥 케이블은 프로텍터로 덮습니다.</p>'),
  ('휴게 공간은 "앉고 싶은 자리"로', '<p>흰 라탄 테이블과 의자 세트는 사진 찍기 좋은 자리가 되어 참가자가 오래 머뭅니다. 부스 10개당 휴게 테이블 2~3세트가 기준입니다.</p>'),
 ],
 'faq': [
  ('실내 행사장 바닥에 손상이 가지 않나요?', '프레임과 테이블 다리에 보호 캡을 씌우고, 무게추로 고정해 바닥에 구멍을 내지 않습니다. 대리석 · 마루 바닥 모두 가능합니다.'),
  ('부스 프레임 대신 천막을 실내에 세울 수도 있나요?', '천장 높이가 3m 이상이면 캐노피 천막도 실내에 세울 수 있습니다. 다만 프레임 부스가 더 가볍고 통로를 덜 차지합니다.'),
  ('청주 시내 축제는 설치 시간이 제한되는데 가능한가요?', '실내 부스 30개 기준 3시간 안에 세팅합니다. 새벽 · 야간 설치 모두 가능하니 장소 사용 가능 시간을 알려 주세요.'),
 ],
 'related': ['big-festival-quantity', 'cheongju-seminar-expo-table'],
},
{
 'slug': 'danyang-flea-market-pink-tent', 'date': '2026-09-11', 'region': '단양', 'area': '충북',
 'title': '단양 야외 플리마켓 천막 대여, 핑크 캐노피로 부스 분위기 살리기',
 'desc': '단양 · 제천 야외 플리마켓 천막 렌탈. 흰 천막 대신 핑크 캐노피를 쓴 이유, 산책로를 따라 한 줄로 배치하는 방법, 파라솔 휴게 공간, 셀러 테이블 수량과 설치 시간을 이에스컴퍼니가 정리했습니다.',
 'kw': ['단양 플리마켓 천막 대여', '단양 행사 천막 렌탈', '핑크 천막 대여', '제천 단양 행사용품', '플리마켓 부스 천막', '충북 플리마켓 렌탈'],
 'photos': [(14, '단양 야외 플리마켓 — 산책로를 따라 핑크 캐노피 천막을 한 줄로'), (13, '노란 파라솔과 흰 의자로 만든 휴게 공간')],
 'lead': '플리마켓은 "예쁜 사진이 곧 홍보"인 행사입니다. 흰 천막 20동을 세우면 깔끔하지만, <b>핑크나 노랑처럼 색이 있는 천막</b>을 쓰면 SNS에 올라가는 사진이 달라집니다. 단양 야외 플리마켓 현장에서 색 천막을 어떻게 배치했는지 적습니다.',
 'sections': [
  ('색 천막은 한 줄로, 같은 색으로', '<p>색 천막을 섞어 놓으면 오히려 어수선합니다. 단양 현장은 <b>산책로를 따라 핑크 캐노피를 한 줄로</b> 세워 멀리서 보면 하나의 띠처럼 보이게 했습니다. 부스 사이 간격은 50cm를 띄워 옆 부스 손님과 부딪히지 않게 하고, 셀러가 뒤로 드나들 공간 1m를 남깁니다.</p>'),
  ('셀러 테이블 수량: 부스당 1.5개', '<p>플리마켓 셀러는 진열 테이블 하나로 부족한 경우가 많습니다. 부스당 접이식 테이블 1개를 기본으로 두고 <b>전체의 절반 수량을 예비</b>로 가져가면 현장에서 추가 요청을 바로 받을 수 있습니다. 의자는 부스당 2개.</p><ul><li>부스 20개 → 테이블 30개, 의자 40개</li><li>테이블보는 천막 색과 맞추거나 흰색으로 통일</li><li>운영본부 몽골텐트 1동 — 방송 · 안내 · 분실물</li></ul>'),
  ('휴게 공간은 파라솔로 가볍게', '<p>천막 대신 <b>대형 파라솔 + 흰 플라스틱 의자</b>로 휴게 공간을 만들면 설치가 10분이면 끝나고 사진도 잘 나옵니다. 먹거리 부스 근처에 파라솔 4~6개, 의자 20~30개가 기준입니다.</p>'),
  ('보도블록 · 잔디 설치와 철거', '<p>산책로 보도블록에는 팩을 박을 수 없어 물통 웨이트로 고정합니다. 단양은 강바람이 있어 천막 한 동당 웨이트를 4개 → 6개로 늘립니다. 오전 6시 설치 시작, 오후 6시 마감 뒤 1시간 철거가 보통입니다.</p>'),
 ],
 'faq': [
  ('핑크 말고 다른 색 천막도 있나요?', '흰색 · 파란색 · 핑크 등 몇 가지 색을 갖추고 있습니다. 행사 컨셉 색을 알려 주시면 맞는 색으로 제안해 드립니다.'),
  ('단양 · 제천은 청주에서 멀지 않나요?', '청주 옥산에서 1시간 30분 안팎입니다. 새벽 설치 기준으로 일정을 잡으니 부담 없이 문의해 주세요.'),
  ('셀러가 당일에 테이블을 더 달라고 하면요?', '예비 수량을 가져가기 때문에 현장에서 바로 추가해 드립니다. 예비분은 사용한 만큼만 정산합니다.'),
 ],
 'related': ['cheongju-festival-booth-setting', 'big-festival-quantity'],
},
{
 'slug': 'jincheon-corporate-park-event', 'date': '2026-09-10', 'region': '진천', 'area': '충북',
 'title': '진천 기업행사 장비 렌탈, 공원 행사 테이블 · 의자 · 급수 공간 구성',
 'desc': '진천 · 음성 기업행사 장비 렌탈. 공원 야외행사에서 접이식 테이블과 의자를 어떻게 놓는지, 급수 · 음료 공간, 잔디밭 천막 고정, 무대 · 음향 위치를 이에스컴퍼니 현장 사진으로 설명합니다.',
 'kw': ['진천 기업행사 장비 렌탈', '진천 행사 테이블 의자 대여', '진천 행사 천막', '음성 진천 행사용품', '공원 야외행사 세팅', '충북 기업행사 렌탈'],
 'photos': [(4, '진천 공원 기업행사 — 접이식 테이블과 의자를 통로 방향으로 배치'), (5, '급수 · 음료 공간 — 생수 보관 아이스박스와 테이블'), (26, '잔디밭 천막 · 테이블 세팅, 저녁 노을 무렵')],
 'lead': '진천 · 음성 산업단지 기업들이 임직원 행사를 공원에서 여는 경우가 늘었습니다. 공원 행사는 회사 강당과 달리 <b>그늘 · 물 · 전기</b> 세 가지를 저희가 만들어야 합니다. 진천 공원 기업행사 현장을 기준으로 구성 순서를 적습니다.',
 'sections': [
  ('테이블은 통로를 먼저 그리고 놓습니다', '<p>테이블부터 놓고 통로를 만들면 꼭 막히는 곳이 생깁니다. 먼저 <b>무대 → 급수 → 화장실</b>을 잇는 주 통로(폭 3m)를 그리고, 테이블은 통로 양쪽에 8명 단위로 놓습니다. 접이식 테이블 1개(1800mm)에 의자 6~8개가 기본입니다.</p><ul><li>임직원 200명 → 테이블 28~30개, 의자 220개</li><li>내빈석은 앞줄 2~3개 테이블에 테이블보 + 의자 커버</li><li>테이블 다리 밑 받침으로 잔디 보호</li></ul>'),
  ('급수 · 음료 공간은 그늘에, 무대에서 멀리', '<p>사람이 가장 많이 몰리는 곳이 급수대입니다. 무대 바로 옆에 두면 공연 중에 줄이 무대를 가립니다. <b>나무 그늘 아래 천막 1~2동</b>에 아이스박스와 테이블을 놓고, 쓰레기 분리함을 바로 옆에 둡니다.</p>'),
  ('무대 · 음향은 해 방향을 봅니다', '<p>오후 행사는 무대가 서쪽을 등지게 세워야 관객이 해를 안 봅니다. 스피커는 무대 좌우에 두고, 테이블 구역이 길면 중간에 보조 스피커를 하나 더 둡니다. 전기는 공원 관리사무소 분전반을 쓰거나 발전기를 가져갑니다.</p>'),
  ('저녁까지 이어지면', '<p>천막마다 조명 하나, 통로에 스트링 라이트를 걸면 저녁 사진이 살아납니다. 진천 현장은 오후 3시 시작 · 저녁 8시 마감으로, 설치 4시간 · 철거 1시간 30분이 걸렸습니다.</p>'),
 ],
 'faq': [
  ('공원 사용 허가는 누가 받나요?', '공원 사용 허가는 주최 측에서 받으셔야 합니다. 허가 조건(팩 사용 · 전기 · 차량 진입)을 알려 주시면 그에 맞춰 장비를 준비합니다.'),
  ('진천 · 음성 산업단지 내 행사도 가능한가요?', '네. 공장 마당 · 주차장 행사도 많이 합니다. 아스팔트 바닥은 웨이트 고정으로 진행합니다.'),
  ('테이블보 · 의자 커버도 같이 빌릴 수 있나요?', '네. 내빈석만 씌우거나 전체를 씌우거나 선택할 수 있습니다.'),
 ],
 'related': ['chungju-corporate-event-rental', 'daejeon-ceremony-round-table'],
},
{
 'slug': 'cheongju-seminar-expo-table', 'date': '2026-09-09', 'region': '청주', 'area': '충북',
 'title': '청주 세미나 · 박람회 테이블 렌탈, 전시장 수백 조 세팅 순서',
 'desc': '청주 오스코 · 전시장 세미나 테이블 렌탈. 강의식 배치와 테이블보 · 스커트, 접수대, 박람회 조립 부스, 케이블 정리, 400석 세팅 시간을 이에스컴퍼니 현장 사진으로 정리했습니다.',
 'kw': ['청주 세미나 테이블 렌탈', '청주 오스코 행사 장비', '박람회 부스 렌탈 청주', '세미나 의자 대여', '전시장 테이블 세팅', '청주 행사용품 렌탈'],
 'photos': [(6, '청주 오스코 세미나 — 네이비 테이블보 · 스커트로 통일한 강의식 배치'), (7, '전시장 400석 규모 테이블 · 의자 세팅'), (19, '박람회 조립 부스 — 부스명 사인과 안내 테이블'), (15, '전시장 통로 접수 · 안내 테이블')],
 'lead': '세미나 · 박람회는 "줄이 맞느냐"가 첫인상입니다. 테이블 400개를 눈대중으로 놓으면 사진에서 바로 티가 납니다. 청주 오스코와 전시장에서 진행한 세팅을 기준으로 <b>줄 맞추는 순서와 시간</b>을 적습니다.',
 'sections': [
  ('먼저 바닥에 기준선을 잡습니다', '<p>전시장은 넓어서 기준 없이 놓으면 뒤로 갈수록 틀어집니다. 무대 중심선과 첫 줄 위치를 <b>마스킹테이프로 바닥에 표시</b>한 뒤, 줄마다 앞 테이블 끝에 맞춰 놓습니다. 강의식은 테이블(1800mm) 1개에 의자 3개, 앞뒤 간격 1.2m가 기준입니다.</p><ul><li>400석 → 테이블 134개 · 의자 400개 · 통로 2~3개</li><li>테이블보 + 스커트로 다리를 가리면 사진이 정리됩니다</li><li>앞줄 내빈석은 의자 커버까지</li></ul>'),
  ('접수대 · 안내 사인은 입구 동선에', '<p>접수대는 입구에서 5m 안쪽, 줄이 문을 막지 않는 자리에 둡니다. 접수 테이블 2~3개, 명찰 · 자료 테이블 1개, 안내 배너 2개가 기본입니다. 박람회는 조립 부스에 부스명 사인을 달고 부스마다 테이블 1 · 의자 2를 넣습니다.</p>'),
  ('케이블은 보이지 않게', '<p>세미나는 노트북 · 마이크 · 프로젝터 케이블이 많습니다. 통로를 가로지르는 케이블은 프로텍터로 덮고, 테이블 밑으로 지나가는 선은 테이프로 고정합니다. 이 작업을 빼먹으면 행사 중 누군가 꼭 걸려 넘어집니다.</p>'),
  ('세팅 시간', '<p>400석 강의식은 <b>5명이 3시간</b>이면 테이블보까지 끝납니다. 전날 저녁 세팅이 가장 안전하고, 당일 아침 세팅이면 4시간 전에는 들어가야 합니다.</p>'),
 ],
 'faq': [
  ('오스코 외에 청주 시내 호텔 · 컨벤션도 가능한가요?', '네. 청주 시내 호텔 연회장, 대학 강당, 기업 강당 모두 세팅합니다.'),
  ('테이블보 색은 고를 수 있나요?', '네이비 · 블랙 · 화이트를 기본으로 갖추고 있고, 행사 색에 맞춰 준비할 수 있습니다.'),
  ('박람회 조립 부스는 몇 개까지 되나요?', '수십 개 규모 박람회까지 진행합니다. 부스 규격(2×2m · 3×2m)과 수량을 알려 주시면 도면과 함께 견적을 드립니다.'),
 ],
 'related': ['cheongju-festival-booth-setting', 'daejeon-ceremony-round-table'],
},
{
 'slug': 'chungbuk-night-sports-tent', 'date': '2026-09-08', 'region': '충북', 'area': '충북',
 'title': '충북 야간 체육행사 천막 · 조명 렌탈, 풋살장 · 잔디 운동장 설치 기준',
 'desc': '충북 청주 · 충주 · 제천 야간 체육대회 · 동문회 · 풋살 대회 장비 렌탈. 인조잔디 풋살장 천막 고정, 야간 조명 위치, 응원석 의자, 급수 공간, 새벽 설치 시간을 이에스컴퍼니 현장 사진으로 정리했습니다.',
 'kw': ['충북 체육대회 천막 대여', '야간 체육행사 조명 렌탈', '풋살장 행사 천막', '동문 체육대회 장비 렌탈', '청주 체육대회 의자 대여', '충북 행사용품 렌탈'],
 'photos': [(22, '야간 풋살장 — 인조잔디 옆으로 천막을 세우고 조명을 켠 체육행사'), (23, '천막 아래 응원석 의자, 경기장 조명과 함께'), (21, '잔디 운동장 둘레에 천막을 배치한 낮 체육대회')],
 'lead': '동문 체육대회 · 직장 풋살 대회는 퇴근 뒤 저녁에 열리는 경우가 많습니다. 낮 체육대회와 달리 <b>조명, 인조잔디 고정, 야간 철거</b> 세 가지를 따로 준비해야 합니다. 충북 풋살장과 잔디 운동장 현장을 기준으로 적습니다.',
 'sections': [
  ('인조잔디에는 팩을 절대 박지 않습니다', '<p>인조잔디는 밑에 배수층이 있어 팩을 박으면 시설 손상입니다. 천막은 <b>물통 웨이트 4~6개</b>로 고정하고, 천막 다리 밑에 고무판을 깔아 잔디를 보호합니다. 경기 라인 안쪽으로는 장비를 놓지 않고, 골대 뒤 · 사이드라인 바깥에 천막을 세웁니다.</p>'),
  ('조명은 경기장 조명 "빈 자리"를 채웁니다', '<p>풋살장에는 보통 경기장 조명이 있습니다. 문제는 천막 아래 응원석과 급수대가 그 조명의 그늘에 들어간다는 점입니다. 천막마다 LED 작업등 1개, 급수대 · 본부석에 2개를 달면 됩니다. 무대(시상식)가 있으면 스팟 조명 2개를 추가합니다.</p><ul><li>천막 1동당 LED 작업등 1개</li><li>본부 · 급수 · 시상 공간은 2개씩</li><li>전기는 경기장 콘센트 확인 → 부족하면 발전기</li></ul>'),
  ('응원석 의자 · 급수 · 본부', '<p>팀당 천막 1동(3×3m)에 의자 10~12개가 기본입니다. 팀이 8개면 천막 8동 + 본부 1동 + 급수 1동 + 시상 · 음향 1동으로 11동. 급수대는 경기장 출입구 옆, 본부는 경기장 전체가 보이는 자리에 둡니다.</p>'),
  ('야간 철거는 소음이 관건', '<p>밤 10시 마감 행사는 주변이 주택가인 경우가 많습니다. 철거 때 천막 프레임 소리를 줄이려고 <b>천막을 접어서 옮기고 차량에서 정리</b>합니다. 30분 안에 조용히 빠지는 게 목표입니다.</p>'),
 ],
 'faq': [
  ('낮 체육대회와 야간 행사 비용이 다른가요?', '조명 · 전력 장비가 추가되는 만큼만 차이가 납니다. 항목별로 견적을 드리니 필요 없는 항목은 빼셔도 됩니다.'),
  ('풋살장 관리자가 장비 반입을 제한하면요?', '반입 조건(차량 진입 · 시간 · 고정 방식)을 미리 확인해 주시면 그에 맞춰 준비합니다. 인조잔디 보호 자재는 기본으로 가져갑니다.'),
  ('제천 · 옥천 · 영동처럼 먼 곳도 야간 철거가 되나요?', '네. 야간 철거 뒤 복귀까지 일정에 넣어 진행합니다. 일정이 늦은 행사는 다음 날 아침 철거로 조정할 수도 있습니다.'),
 ],
 'related': ['cheongju-school-sports-day-tent', 'chungju-corporate-event-rental'],
},
{
 'slug': 'daejeon-ceremony-round-table', 'date': '2026-09-07', 'region': '대전', 'area': '대전',
 'title': '대전 · 청주 기념식 · 시상식 세팅, 라운드테이블과 관람석 의자 수량 잡는 법',
 'desc': '대전 · 세종 · 청주 기념식 · 시상식 · 협약식 장비 렌탈. 호텔 연회장 라운드테이블과 의자 커버, 야외 관람석 의자 수백 개 배치, 무대 · 연단 · 배너, 겨울 야외 행사 대비를 이에스컴퍼니가 현장 기준으로 정리했습니다.',
 'kw': ['대전 기념식 행사 렌탈', '대전 시상식 라운드테이블 대여', '의자 커버 렌탈 대전', '협약식 의자 배치', '세종 대전 행사용품 렌탈', '야외 기념식 의자 대여'],
 'photos': [(24, '호텔 연회장 — 라운드테이블과 검은 의자 커버로 세팅한 만찬 · 시상식'), (18, '야외 기념식 — 흰 의자 수백 개를 줄 맞춰 놓은 관람석')],
 'lead': '기념식 · 시상식은 "격식"이 보여야 하는 행사입니다. 같은 의자라도 커버를 씌우면 다르고, 같은 테이블이라도 라운드로 놓으면 다릅니다. 대전 · 세종 · 청주 기관 · 기업 행사에서 저희가 잡는 <b>좌석 구성과 수량 기준</b>을 적습니다.',
 'sections': [
  ('라운드테이블: 8인 기준, 무대와 3m', '<p>연회장 라운드테이블(1500~1800mm)은 8명이 기본, 10명이면 좁습니다. 무대 앞 첫 줄은 무대에서 3m 띄워 내빈이 사진 찍을 공간을 만들고, 테이블 사이는 1.5m를 확보해 서빙 동선을 냅니다.</p><ul><li>참석 160명 → 라운드 20개 · 의자 160개 + 여유 10개</li><li>테이블보 + 의자 커버 + 센터피스로 통일</li><li>내빈 테이블은 무대 정면 2~3개, 명패 준비</li></ul>'),
  ('야외 기념식 관람석: 줄과 통로가 전부입니다', '<p>야외에서 의자 300~500개를 놓을 때는 <b>중앙 통로 2m + 좌우 통로 1.5m</b>를 먼저 잡고 12~16개씩 줄을 만듭니다. 줄 간격은 90cm. 앞 3줄은 내빈석으로 커버를 씌우고 뒤는 흰 의자 그대로 두면 예산이 줄어듭니다.</p>'),
  ('무대 · 연단 · 배너', '<p>기념식 무대는 덱 높이 40~60cm, 연단(포디움) 1개, 국기 · 기관기 자리, 뒷막 배너가 기본입니다. 음향은 무선 마이크 2개(사회 · 축사)와 유선 1개(연단)로 구성하고, 시상식은 수상자 대기 동선을 무대 옆에 따로 만듭니다.</p>'),
  ('겨울 · 이른 봄 야외 행사', '<p>1~3월 야외 기념식은 의자에 서리가 내립니다. 행사 1시간 전 의자를 닦고, 내빈석에는 방석 · 무릎담요를 준비하면 좋습니다. 저희는 새벽 설치 뒤 행사 직전에 한 번 더 점검하고 나옵니다.</p>'),
 ],
 'faq': [
  ('대전 호텔 · 컨벤션 연회장도 세팅하나요?', '네. 대전 · 세종 · 청주 호텔 연회장, 기관 강당, 야외 광장 모두 갑니다. 연회장 자체 테이블이 있으면 커버 · 테이블보만도 가능합니다.'),
  ('의자 커버 색은 무엇이 있나요?', '블랙 · 화이트를 기본으로 하고, 리본 색으로 포인트를 줄 수 있습니다.'),
  ('당일 참석 인원이 늘면요?', '여유 수량을 10% 가져가고, 그 이상 늘어날 것 같으면 전날까지 알려 주시면 추가합니다.'),
 ],
 'related': ['cheongju-seminar-expo-table', 'sejong-school-gym-camping-chair'],
},
{
 'slug': 'big-festival-quantity', 'date': '2026-09-06', 'region': '충청권', 'area': '충북',
 'title': '수천 명 모이는 야외 축제, 테이블 · 의자 · 천막 수량은 어떻게 정할까 (충청권 대형 축제 준비)',
 'desc': '충북 · 충남 · 세종 · 대전 대형 야외 축제 장비 렌탈 가이드. 방문객 수가 아닌 동시 체류 인원으로 테이블 · 의자 수량 잡는 법, 먹거리 존 배치, 야간 조명, 대규모 설치 · 철거 인력과 시간을 이에스컴퍼니 현장 사진으로 설명합니다.',
 'kw': ['대형 축제 장비 렌탈', '축제 테이블 의자 대여 충북', '야외 축제 천막 수량', '먹거리 축제 테이블 렌탈', '충청권 축제 행사용품', '세종 청주 축제 장비'],
 'photos': [(27, '대형 야외 축제 — 광장 전체에 테이블 · 의자를 깔고 무대를 세운 저녁 풍경'), (28, '해질 무렵 축제장 전경 — 부스 열과 관람 테이블'), (8, '야간 먹거리 존 — 테이블마다 사람이 찬 시간대'), (9, '스트링 라이트 아래 먹거리 테이블 배치')],
 'lead': '"방문객 5,000명"이라고 해서 의자 5,000개를 빌리는 축제는 없습니다. 필요한 건 <b>같은 시간에 앉아 있는 사람 수</b>입니다. 충청권 대형 축제 현장에서 저희가 수량을 잡는 계산법을 공개합니다.',
 'sections': [
  ('동시 체류 인원 = 방문객 × 체류 비율', '<p>하루 방문객 5,000명, 행사 6시간, 평균 체류 1.5시간이면 같은 시간에 있는 사람은 약 1,250명입니다. 그중 앉아서 먹거나 공연을 보는 비율을 40~50%로 잡으면 <b>좌석 500~600석</b>이 나옵니다. 테이블은 6인 기준 100개 안팎.</p><ul><li>좌석 = 동시 체류 인원 × 0.4~0.5</li><li>테이블 = 좌석 ÷ 6</li><li>피크 시간(저녁 6~8시)이 뚜렷한 먹거리 축제는 0.5 이상</li></ul>'),
  ('먹거리 존은 "판매 부스 : 테이블 = 1 : 4"', '<p>먹거리 부스 20개면 테이블 80개 · 의자 480개가 기준입니다. 부스 열과 테이블 구역 사이에 3m 통로를 두고, 테이블은 부스에서 먼 쪽부터 채워지도록 배치합니다. 쓰레기 분리함은 테이블 20개당 1세트.</p>'),
  ('천막은 관람석이 아니라 "머무는 곳"에', '<p>대형 축제에서 관람석 전체에 천막을 치면 무대가 안 보입니다. 천막은 <b>먹거리 테이블 · 체험 · 안내 · 응급 · 운영본부</b>에만 두고, 관람 구역은 파라솔이나 그늘막으로 대신합니다. 야간에는 스트링 라이트를 테이블 구역 위로 걸면 조명과 분위기를 한 번에 해결합니다.</p>'),
  ('설치 · 철거 인력과 시간', '<p>테이블 100개 · 의자 600개 · 천막 30동 규모는 <b>8명이 6시간</b>이면 설치가 끝납니다. 전날 설치가 원칙이고, 철거는 다음 날 오전. 차량은 2.5톤 2대가 들어갈 진입로와 하차 공간이 필요하니 답사 때 가장 먼저 확인합니다.</p>'),
 ],
 'faq': [
  ('축제 이틀 · 사흘 행사는 어떻게 계산하나요?', '일별 피크 인원이 가장 큰 날을 기준으로 수량을 잡고, 행사 기간 내내 두고 씁니다. 야간 보관 · 우천 대비도 같이 계획합니다.'),
  ('천안 · 아산 같은 충남 지역 축제도 가능한가요?', '네. 충북 · 충남 · 세종 · 대전 전 지역 진행합니다. 대형 행사는 답사를 먼저 가서 차량 동선과 전기를 확인합니다.'),
  ('무대 · 음향까지 한 번에 맡길 수 있나요?', '네. 천막 · 테이블 · 의자와 무대 · 음향 · 조명을 한 팀이 세팅하면 동선이 겹치지 않아 설치가 빠릅니다.'),
 ],
 'related': ['cheongju-festival-booth-setting', 'chungju-corporate-event-rental'],
},
]

# ------------------------------------------------------------------ 공통 조각
LOGO_H = '<a class="logo" href="{R}index.html" aria-label="이에스컴퍼니 홈"><img src="{R}assets/img/logo-h.svg" alt="이에스컴퍼니 ES COMPANY"></a>'
LOGO_W = '<a class="logo" href="{R}index.html" aria-label="이에스컴퍼니 홈"><img src="{R}assets/img/logo-h-white.svg" alt="이에스컴퍼니 ES COMPANY"></a>'
PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'
ARR = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def nav(R):
    return f'''<a href="{R}about.html">회사소개</a>
      <a href="{R}service.html">서비스 · 렌탈품목</a>
      <a href="{R}portfolio.html">현장사진</a>
      <a href="{R}blog/index.html">행사 가이드</a>
      <a href="{R}contact.html">견적문의</a>'''

def header(R):
    return f'''<header class="top">
  <div class="wrap">
    {LOGO_H.format(R=R)}
    <div class="slogan"><b>“완벽을 만드는 작은 차이”</b>행사기획 · 시스템렌탈 · 행사용품렌탈 — 충북 · 충남 · 세종 · 대전</div>
    <div class="right">
      <a class="tel" href="tel:{TEL}"><span class="ic">{PHONE_SVG}</span><span><small>행사 상담 · 견적</small>{TEL}</span></a>
      <a class="btn btn-pri" href="{R}contact.html">견적 문의{ARR}</a>
    </div>
    <button class="burger" id="burger" aria-label="메뉴 열기" aria-expanded="false" aria-controls="sheet"><i></i></button>
  </div>
</header>
<div class="bar" id="bar">
  <div class="wrap">
    <a class="mini" href="{R}index.html"><img src="{R}assets/img/logo-h-white.svg" alt="이에스컴퍼니"></a>
    <nav class="menu" aria-label="주 메뉴">
      {nav(R)}
    </nav>
    <a class="cta" href="{R}contact.html">견적 문의 →</a>
  </div>
</div>
<div class="sheet" id="sheet" aria-label="모바일 메뉴">
  <div class="head">
    {LOGO_H.format(R=R)}
    <button class="x" aria-label="메뉴 닫기"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  </div>
  <nav>
    <a href="{R}index.html">홈<small>HOME</small></a>
    <a href="{R}about.html">회사소개<small>ABOUT</small></a>
    <a href="{R}service.html">서비스 · 렌탈품목<small>SERVICE</small></a>
    <a href="{R}portfolio.html">현장사진<small>WORKS</small></a>
    <a href="{R}blog/index.html">행사 가이드<small>GUIDE</small></a>
    <a href="{R}contact.html">견적문의<small>CONTACT</small></a>
  </nav>
  <div class="foot">대표 박미배 · {TEL}<br>충북 청주시 흥덕구 옥산면 오산가좌로 110-13<a class="btn btn-pri" href="tel:{TEL}">전화로 바로 상담</a></div>
</div>'''

def footer(R):
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="top-row">
      <div>
        {LOGO_W.format(R=R)}
        <p>“완벽을 만드는 작은 차이” 행사의 가치를 높이는 전문 행사 파트너 이에스컴퍼니입니다. 기획부터 무대 · 음향 · 조명 시스템, 천막 · 테이블 · 의자 행사용품 렌탈까지 원스톱으로 준비해 드립니다.</p>
      </div>
      <div><h4>OFFICE</h4><ul>
        <li><b>주소</b>충북 청주시 흥덕구 옥산면 오산가좌로 110-13, 1동 1층</li>
        <li><b>TEL</b>{TEL}</li>
        <li><b>E-MAIL</b>esgroup0102@naver.com</li>
        <li><b>BLOG</b><a href="https://blog.naver.com/esgroup0102" target="_blank" rel="noopener">blog.naver.com/esgroup0102</a></li></ul></div>
      <div><h4>COMPANY</h4><ul>
        <li><b>상호</b>이에스컴퍼니 (ES COMPANY)</li>
        <li><b>대표</b>박미배</li>
        <li><b>사업자등록번호</b>710-09-02317</li>
        <li><b>운영 지역</b>충북 · 충남 · 세종 · 대전</li></ul></div>
    </div>
    <div class="bot"><span>COPYRIGHT © 2026 이에스컴퍼니. ALL RIGHTS RESERVED.</span><span><a href="#top">맨 위로 ↑</a></span></div>
  </div>
</footer>
<div class="quick" aria-label="빠른 연락">
  <a href="tel:{TEL}">{PHONE_SVG}전화</a>
  <a href="sms:{TEL}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="M4 5h16v11H9l-5 4z"/></svg>문자</a>
  <a class="main" href="{R}contact.html">견적 문의</a>
</div>
<button class="totop" id="totop" aria-label="맨 위로"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>'''

AREAS = ['충청북도', '청주시', '충주시', '제천시', '증평군', '진천군', '괴산군', '음성군', '단양군', '보은군', '옥천군', '영동군', '충청남도', '천안시', '아산시', '세종특별자치시', '대전광역시']

def business_ld():
    return {
        "@context": "https://schema.org", "@type": "LocalBusiness", "@id": BASE + "#business",
        "name": "이에스컴퍼니", "alternateName": "ES COMPANY", "url": BASE,
        "logo": BASE + "assets/img/logo-mark.svg", "image": BASE + "assets/img/og.jpg",
        "description": "충북 청주 본사의 행사 파트너. 천막 · 테이블 · 의자 · 부스 행사용품 렌탈, 무대 · 음향 · 조명 시스템 렌탈, 행사기획을 설치 · 철거 포함 원스톱으로 제공합니다. 충북 · 충남 · 세종 · 대전 출장 설치.",
        "telephone": "+82-10-2084-0102", "email": "esgroup0102@naver.com", "priceRange": "₩₩",
        "founder": {"@type": "Person", "name": "박미배"},
        "address": {"@type": "PostalAddress", "streetAddress": "옥산면 오산가좌로 110-13, 1동 1층", "addressLocality": "청주시 흥덕구", "addressRegion": "충청북도", "addressCountry": "KR"},
        "geo": {"@type": "GeoCoordinates", "latitude": 36.6715486, "longitude": 127.3735257},
        "areaServed": [{"@type": "AdministrativeArea", "name": a} for a in AREAS],
        "sameAs": ["https://blog.naver.com/esgroup0102"],
        "knowsAbout": ["행사용품 렌탈", "천막 대여", "몽골텐트 대여", "테이블 의자 대여", "무대 음향 렌탈", "학교 운동회", "체육대회", "지역 축제", "기업행사", "협약식 기념식", "세미나 박람회 세팅", "하드펜스"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "이에스컴퍼니 서비스", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "행사기획", "description": "행사 목적 · 인원 · 장소 조건에 맞춘 공간 구성과 품목 · 수량 제안, 설치 · 철거 일정 조율"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "시스템렌탈", "description": "무대 · 연단 · 음향(스피커 · 마이크 · 믹서) 렌탈과 운영"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "행사용품렌탈", "description": "캐노피천막 · 몽골텐트 · 부스천막 · 듀라테이블 · 파라솔세트 · 의자 · 포토존 트러스 · 캠핑세트 · 나무매대 · 하드펜스 · 차단봉 · 다과테이블 · 아크릴단상 · 배너 렌탈, 설치 · 철거 포함"}},
        ]},
    }

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '</script>'

def breadcrumb(items):
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]})

def head(title, desc, url, image, kw, extra=''):
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="keywords" content="{html.escape(', '.join(kw))}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0A1F45">
<meta property="og:type" content="article">
<meta property="og:site_name" content="이에스컴퍼니">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="../assets/style.css?v=3">
{extra}'''

def post_url(p): return BASE + 'blog/' + p['slug'] + '.html'
def img_url(i): return BASE + f'assets/img/blog/b{i:02d}.webp'
BY = {p['slug']: p for p in POSTS}

def render_post(p, k):
    R = '../'
    url = post_url(p); img = img_url(p['photos'][0][0])
    body_text = re.sub(r'<[^>]+>', ' ', p['lead'] + ' '.join(s for _, s in p['sections']))
    ld_article = {"@context": "https://schema.org", "@type": "BlogPosting", "@id": url + "#article", "mainEntityOfPage": url,
        "headline": p['title'], "description": p['desc'], "image": [img_url(i) for i, _ in p['photos']],
        "datePublished": p['date'], "dateModified": p['date'], "inLanguage": "ko-KR",
        "author": {"@type": "Organization", "name": "이에스컴퍼니", "url": BASE},
        "publisher": {"@type": "Organization", "name": "이에스컴퍼니", "logo": {"@type": "ImageObject", "url": BASE + "assets/img/logo-mark.svg"}},
        "keywords": ', '.join(p['kw']), "articleSection": "행사 가이드",
        "spatialCoverage": {"@type": "Place", "name": p['region']},
        "about": {"@id": BASE + "#business"}, "wordCount": len(body_text.split())}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]}
    extra = ld(ld_article) + ld(ld_faq) + breadcrumb([("홈", BASE), ("행사 가이드", BASE + 'blog/index.html'), (p['title'], url)]) + ld(business_ld())
    photos = p['photos']
    figs = [f'<figure class="ph"><img src="../assets/img/blog/b{i:02d}.webp" alt="{html.escape(c)}" loading="{"eager" if n == 0 else "lazy"}" width="1600" height="1200"><figcaption>{html.escape(c)}</figcaption></figure>' for n, (i, c) in enumerate(photos)]
    # 사진을 본문 사이에 끼워 넣기: 첫 사진은 리드 뒤, 나머지는 섹션 사이
    parts = [f'<p class="lead">{p["lead"]}</p>', figs[0]]
    fi = 1
    for n, (h2, body) in enumerate(p['sections']):
        parts.append(f'<h2>{html.escape(h2)}</h2>{body}')
        if fi < len(figs) and n < len(p['sections']) - 1:
            parts.append(figs[fi]); fi += 1
    while fi < len(figs): parts.append(figs[fi]); fi += 1
    faq_html = ''.join(f'<details{" open" if i == 0 else ""}><summary><i>Q</i>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for i, (q, a) in enumerate(p['faq']))
    related = ''.join(f'<a href="{BY[s]["slug"]}.html"><small>{BY[s]["region"]} · {BY[s]["date"]}</small><b>{html.escape(BY[s]["title"])}</b></a>' for s in p['related'] if s in BY)
    prev_ = POSTS[k + 1] if k + 1 < len(POSTS) else None; next_ = POSTS[k - 1] if k > 0 else None
    tags = ''.join(f'<span>{html.escape(t)}</span>' for t in p['kw'])
    return f'''<!doctype html>
<html lang="ko">
<head>
{head(p['title'] + ' | 이에스컴퍼니 행사 가이드', p['desc'], url, img, p['kw'], extra)}
</head>
<body>
{header(R)}
<main id="top">
<section class="pagehead post-head">
  <div class="bg" style="background-image:url(../assets/img/blog/b{photos[0][0]:02d}.webp)"></div>
  <div class="wrap">
    <div class="crumb"><a href="../index.html">HOME</a><span>›</span><a href="index.html">행사 가이드</a><span>›</span><span>{html.escape(p['region'])}</span></div>
    <small>Guide · {html.escape(p['region'])} · {p['date'].replace('-', '.')}</small>
    <h1>{html.escape(p['title'])}</h1>
    <p>{html.escape(p['desc'])}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap post-wrap">
    <article class="post">
      <div class="meta"><span class="who"><i>ES</i>이에스컴퍼니 · 대표 박미배</span><time datetime="{p['date']}">{p['date'].replace('-', '.')}</time><span class="rg">{html.escape(p['area'])} · {html.escape(p['region'])}</span></div>
      {''.join(parts)}
      <h2>자주 묻는 질문</h2>
      <div class="faq">{faq_html}</div>
      <div class="tags">{tags}</div>
      <div class="cta-box">
        <div><b>{html.escape(p['region'])} 행사 준비 중이신가요?</b><span>날짜 · 장소 · 대략의 수량만 알려 주시면 1영업일 안에 항목별 견적과 배치 제안으로 답합니다. 청주 옥산에서 충북 · 충남 · 세종 · 대전 어디든 갑니다.</span></div>
        <div class="btns"><a class="btn btn-pri" href="../contact.html">견적 문의하기{ARR}</a><a class="btn btn-white" href="../service.html#calc">품목 골라 요청서 만들기</a><a class="btn btn-white" href="tel:{TEL}">{TEL}</a></div>
      </div>
    </article>
    <aside class="side">
      <div class="box"><small>RENTAL ITEMS</small><b>이 글에 나온 품목</b><ul class="lnk"><li><a href="../service.html#items">캐노피 천막 · 몽골텐트</a></li><li><a href="../service.html#items">접이식 · 원형 테이블</a></li><li><a href="../service.html#items">의자 · 캠핑의자 · 의자 커버</a></li><li><a href="../service.html#system">무대 · 음향 · 조명</a></li><li><a href="../service.html#items">하드펜스 · 차단봉 · 배너</a></li></ul></div>
      <div class="box"><small>RELATED</small><b>같이 읽으면 좋은 글</b><div class="rel">{related}</div></div>
      <div class="box dark"><small>SERVICE AREA</small><b>충북 · 충남 · 세종 · 대전</b><p>청주 · 충주 · 제천 · 증평 · 진천 · 괴산 · 음성 · 단양 · 보은 · 옥천 · 영동 · 천안 · 아산 · 세종 · 대전</p><a class="btn btn-pri" href="../about.html#region">운영 지역 보기</a></div>
    </aside>
  </div>
  <div class="wrap post-nav">{('<a class="pv" href="' + prev_['slug'] + '.html"><small>← 이전 글</small><b>' + html.escape(prev_['title']) + '</b></a>') if prev_ else '<span></span>'}{('<a class="nx" href="' + next_['slug'] + '.html"><small>다음 글 →</small><b>' + html.escape(next_['title']) + '</b></a>') if next_ else '<span></span>'}</div>
</section>
</main>
{footer(R)}
<script src="../assets/app.js?v=3"></script>
</body>
</html>
'''

def render_index():
    R = '../'; url = BASE + 'blog/index.html'
    cards = ''.join(f'''<a class="pcard reveal" href="{p['slug']}.html"><div class="img" style="background-image:url(../assets/img/blog/b{p['photos'][0][0]:02d}.webp)"><i>{html.escape(p['region'])}</i></div><div class="body"><small>{p['date'].replace('-', '.')} · {html.escape(p['area'])}</small><b>{html.escape(p['title'])}</b><p>{html.escape(p['desc'][:90])}…</p></div></a>''' for p in POSTS)
    ld_list = ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": "이에스컴퍼니 행사 가이드", "url": url, "hasPart": [{"@type": "BlogPosting", "headline": p['title'], "url": post_url(p), "datePublished": p['date']} for p in POSTS]})
    extra = ld_list + breadcrumb([("홈", BASE), ("행사 가이드", url)]) + ld(business_ld())
    title = '행사 가이드 | 이에스컴퍼니 — 청주 · 충주 · 세종 · 대전 행사 천막 · 테이블 · 무대 렌탈 준비법'
    desc = '충북 · 충남 · 세종 · 대전 지역별 행사 준비 가이드 10편. 학교 운동회 천막 수량, 기업행사 야간 조명, 체육관 캠핑의자, 축제 부스 세팅, 플리마켓 천막, 세미나 테이블, 기념식 라운드테이블, 대형 축제 수량 계산까지 이에스컴퍼니 현장 사진으로.'
    kw = ['행사 준비 가이드', '청주 행사 렌탈', '충주 행사 렌탈', '세종 행사 렌탈', '대전 행사 렌탈', '천막 대여', '테이블 의자 대여', '무대 음향 렌탈']
    return f'''<!doctype html>
<html lang="ko">
<head>
{head(title, desc, url, BASE + 'assets/img/og.jpg', kw, extra).replace('og:type" content="article"', 'og:type" content="website"')}
</head>
<body>
{header(R)}
<main id="top">
<section class="pagehead">
  <div class="bg" style="background-image:url(../assets/img/blog/b27.webp)"></div>
  <div class="wrap">
    <div class="crumb"><a href="../index.html">HOME</a><span>›</span><span>GUIDE</span></div>
    <small>Event Guide · By Region</small>
    <h1>지역별 행사 준비 가이드</h1>
    <p>청주 · 충주 · 세종 · 단양 · 진천 · 대전. 학교 운동회부터 대형 축제까지, 현장에서 수량과 배치를 잡는 기준을 사진과 함께 적었습니다.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="pgrid">{cards}</div>
    <div class="blogbox reveal" style="margin:40px 0 0">
      <div><b>더 많은 지역 · 행사 이야기는 네이버 블로그에</b><span>옥천 · 보은 · 영동 · 제천 · 증평 · 괴산 · 음성 · 천안 현장 글 50편 이상. 같은 지역 · 같은 행사 글부터 찾아보세요.</span></div>
      <a class="btn" href="../portfolio.html#blog">블로그 글 목록 보기 →</a>
    </div>
  </div>
</section>
</main>
{footer(R)}
<script src="../assets/app.js?v=3"></script>
</body>
</html>
'''

# ------------------------------------------------------------------ 본문 5페이지 SEO 주입
PAGES = {
    'index.html': {'kw': ['청주 행사용품 렌탈', '청주 천막 대여', '충북 행사 장비 렌탈', '세종 행사 렌탈', '대전 행사 렌탈', '충남 천안 행사 천막', '무대 음향 조명 렌탈', '테이블 의자 대여', '몽골텐트 대여', '행사기획', '이에스컴퍼니'],
                   'title': '이에스컴퍼니 | 청주 행사용품 렌탈 · 천막 · 테이블 · 의자 · 무대 음향 조명 — 충북 · 충남 · 세종 · 대전', 'crumb': None},
    'about.html': {'kw': ['이에스컴퍼니 소개', '청주 행사 렌탈 업체', '옥산면 행사용품', '충북 행사 파트너', '박미배'], 'title': None, 'crumb': [('회사소개', 'about.html')]},
    'service.html': {'kw': ['캐노피천막 대여', '몽골텐트 렌탈', '부스천막 대여', '듀라테이블 대여', '파라솔세트 렌탈', '의자 대여', '무대 음향 렌탈', '포토존 트러스 대여', '캠핑세트 렌탈', '나무매대 대여', '하드펜스 차단봉 대여', '청주 행사 견적'], 'title': None, 'crumb': [('서비스 · 렌탈품목', 'service.html')]},
    'portfolio.html': {'kw': ['행사 현장 사진', '청주 축제 부스', '학교 운동회 천막 사진', '기업행사 세팅 사례', '협약식 세팅', '세미나 테이블 세팅'], 'title': None, 'crumb': [('현장사진', 'portfolio.html')]},
    'contact.html': {'kw': ['청주 행사 렌탈 견적', '천막 대여 문의', '행사용품 렌탈 문의', '충북 행사 견적 문의'], 'title': None, 'crumb': [('견적문의', 'contact.html')]},
}
CONTACT_FAQ = [
    ('수량을 정확히 모르는데 문의해도 되나요?', '네. 예상 부스 수와 인원만 알려 주시면 판매 · 체험 · 운영 · 휴게 공간으로 나눠 필요한 천막 · 테이블 · 의자 수량을 저희가 다시 계산해 드립니다. 대략만 적어 주세요.'),
    ('설치와 철거도 해 주시나요?', '네, 설치 · 철거가 포함됩니다. 행사 전날이나 당일 새벽에 설치하고, 행사가 끝나면 정해진 시간에 철거해 주변까지 정리합니다. 바닥(아스팔트 · 잔디 · 흙)에 맞는 고정 방식을 씁니다.'),
    ('언제부터 알아보는 게 좋을까요?', '봄 · 가을 성수기에는 원하는 수량과 날짜가 먼저 빠집니다. 행사일이 정해지면 바로 연락 주시는 게 좋고, 최소 2~3주 전에는 수량을 확정하시길 권합니다.'),
    ('천막만, 또는 마이크만 빌릴 수도 있나요?', '네. 필요한 품목만 골라 쓰셔도 됩니다. 소규모 행사는 스피커 · 마이크 세트만, 학교 운동회는 천막만도 가능합니다.'),
    ('비가 오면 어떻게 되나요?', '천막 옆면 가림막과 고정을 강화해 진행하거나, 실내 대안으로 구성을 바꿀 수 있습니다. 일정 변경은 미리 협의해 주시면 최대한 맞춰 드립니다.'),
    ('세금계산서 발행이 되나요?', '네. 항목별 견적서를 드리고 세금계산서를 발행합니다. 학교 · 관공서 · 기업의 정산 서류도 요청하시면 바로 챙겨 드립니다.'),
    ('어느 지역까지 가시나요?', '청주 옥산 본사에서 충북 전 시 · 군, 충남, 세종, 대전까지 갑니다. 그 밖의 지역도 일정이 맞으면 상담해 드리니 문의해 주세요.'),
]

def inject_pages():
    for fn, cfg in PAGES.items():
        p = os.path.join(SITE, fn); s = open(p, encoding='utf-8').read()
        url = BASE if fn == 'index.html' else BASE + fn
        # 이전 주입분 제거
        s = re.sub(r'<!-- seo:start -->.*?<!-- seo:end -->\n?', '', s, flags=re.S)
        s = re.sub(r'<meta name="robots" content="[^"]*">\n', '', s)
        s = re.sub(r'<meta property="og:image" content="[^"]*">\n', '', s)
        s = re.sub(r'<meta name="keywords" content="[^"]*">\n', '', s)
        if cfg['title']:
            s = re.sub(r'<title>.*?</title>', '<title>' + html.escape(cfg['title']) + '</title>', s, count=1)
        lds = [ld(business_ld())]
        if cfg['crumb']:
            lds.append(breadcrumb([("홈", BASE)] + [(n, BASE + u) for n, u in cfg['crumb']]))
        if fn == 'contact.html':
            lds.append(ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in CONTACT_FAQ]}))
        if fn == 'index.html':
            lds.append(ld({"@context": "https://schema.org", "@type": "WebSite", "name": "이에스컴퍼니", "url": BASE, "inLanguage": "ko-KR"}))
        block = ('<!-- seo:start -->\n'
                 f'<meta name="robots" content="index,follow,max-image-preview:large">\n'
                 f'<meta name="keywords" content="{html.escape(", ".join(cfg["kw"]))}">\n'
                 f'<link rel="canonical" href="{url}">\n'
                 f'<meta property="og:url" content="{url}">\n'
                 f'<meta property="og:site_name" content="이에스컴퍼니">\n'
                 f'<meta property="og:locale" content="ko_KR">\n'
                 f'<meta property="og:image" content="{BASE}assets/img/og.jpg">\n'
                 f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
                 f'<meta name="twitter:card" content="summary_large_image">\n'
                 f'<meta name="geo.region" content="KR-43">\n<meta name="geo.placename" content="청주시">\n<meta name="geo.position" content="36.6715486;127.3735257">\n'
                 + '\n'.join(lds) + '\n<!-- seo:end -->\n')
        s = s.replace('<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">', block + '<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">', 1)
        # 메뉴: 행사이야기 → 행사 가이드
        s = s.replace('<a href="portfolio.html#blog">행사이야기</a>', '<a href="blog/index.html">행사 가이드</a>')
        s = s.replace('<a href="portfolio.html#blog">행사이야기<small>STORY</small></a>', '<a href="blog/index.html">행사 가이드<small>GUIDE</small></a>')
        s = s.replace('assets/style.css?v=2', 'assets/style.css?v=3').replace('assets/app.js?v=2', 'assets/app.js?v=3')
        open(p, 'w', encoding='utf-8').write(s)
        print('seo', fn)

def inject_index_guide():
    """대문에 행사 가이드 4편 띠 (후기 앞)"""
    p = os.path.join(SITE, 'index.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!-- ===== 행사 가이드 ===== -->.*?<!-- /행사 가이드 -->\n', '', s, flags=re.S)
    cards = ''.join(f'''<a class="pcard reveal" href="blog/{p_['slug']}.html"><div class="img" style="background-image:url(assets/img/blog/b{p_['photos'][0][0]:02d}.webp)"><i>{html.escape(p_['region'])}</i></div><div class="body"><small>{p_['date'].replace('-', '.')} · {html.escape(p_['area'])}</small><b>{html.escape(p_['title'])}</b></div></a>''' for p_ in POSTS[:4])
    sec = f'''<!-- ===== 행사 가이드 ===== -->
<section class="sec" id="guide">
  <div class="wrap">
    <div class="sec-head reveal">
      <div class="t"><span class="en-t">Event Guide · By Region</span><h2>지역별 행사 준비 가이드.</h2></div>
      <a class="more" href="blog/index.html">+ 가이드 10편 전체 보기<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div>
    <div class="pgrid four">{cards}</div>
  </div>
</section>
<!-- /행사 가이드 -->
'''
    s = s.replace('<!-- ===== 고객 후기 ===== -->', sec + '<!-- ===== 고객 후기 ===== -->', 1)
    open(p, 'w', encoding='utf-8').write(s); print('index guide section')

def write_sitemap():
    today = '2026-09-15'
    urls = [(BASE, '1.0', 'weekly'), (BASE + 'about.html', '0.8', 'monthly'), (BASE + 'service.html', '0.9', 'monthly'),
            (BASE + 'portfolio.html', '0.7', 'weekly'), (BASE + 'contact.html', '0.8', 'monthly'), (BASE + 'blog/index.html', '0.8', 'weekly')]
    urls += [(post_url(p), '0.7', 'monthly') for p in POSTS]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n' for u, pr, c in urls) + '</urlset>\n'
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8').write(xml)
    open(os.path.join(SITE, 'robots.txt'), 'w', encoding='utf-8').write(f'User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {BASE}sitemap.xml\n')
    print('sitemap', len(urls))

if __name__ == '__main__':
    os.makedirs(os.path.join(SITE, 'blog'), exist_ok=True)
    for k, p in enumerate(POSTS):
        open(os.path.join(SITE, 'blog', p['slug'] + '.html'), 'w', encoding='utf-8').write(render_post(p, k))
    open(os.path.join(SITE, 'blog', 'index.html'), 'w', encoding='utf-8').write(render_index())
    print('posts', len(POSTS))
    inject_pages(); inject_index_guide(); write_sitemap()

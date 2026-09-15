/* 이에스컴퍼니 홈페이지 — 공통 스크립트 (외부 라이브러리 없음) */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 회사 정보 · 문의 폼 전송처 ----------
     FORM_ENDPOINT 가 비어 있으면 휴대폰에서는 문자 앱이 열리고, PC 에서는 내용을 복사해 준다.
     Apps Script(문의 서버) 주소를 넣으면 그쪽으로 JSON 이 간다. */
  var FORM_ENDPOINT = '';
  var SMS_TO = '010-2084-0102';
  var COMPANY = '이에스컴퍼니';

  /* ---------- 공지사항 (여기만 고치면 대문에 반영) ---------- */
  var NOTICES = [
    { d: '2026.09.15', t: '이에스컴퍼니 홈페이지를 새로 열었습니다.', n: true },
    { d: '2026.09.10', t: '가을 축제 · 체육대회 · 운동회 시즌 천막 · 테이블 · 의자 예약을 받고 있습니다.', n: true },
    { d: '2026.09.01', t: '충북 · 충남 · 세종 · 대전 전 지역 설치 · 철거까지 직접 진행합니다.' },
    { d: '2026.08.20', t: '무대 · 음향 · 조명 시스템 렌탈, 장비만 대여도 가능합니다.' }
  ];

  /* ---------- 현장 사진 (assets/img/works/w1~w39 ↔ 제목) ----------
     c: school 학교행사 · sport 체육대회 · fest 축제·지역행사 · corp 기업행사 · gov 관공서·기관 · indoor 실내행사 */
  var WORKS = [
    { i: 1, t: '제천 학교 운동회 천막 · 테이블 설치', o: '학교행사 · 제천', c: 'school', y: '2026' },
    { i: 2, t: '운동장 트랙 옆 캐노피 천막 일렬 설치', o: '학교행사 · 제천', c: 'school', y: '2026' },
    { i: 3, t: '학교 운동회 본부석 · 학년별 천막', o: '학교행사 · 제천', c: 'school', y: '2026' },
    { i: 4, t: '충주 고등학교 운동회 천막 렌탈', o: '학교행사 · 충주', c: 'school', y: '2026' },
    { i: 5, t: '만국기 아래 운동장 천막 세팅', o: '학교행사 · 충주', c: 'school', y: '2026' },
    { i: 6, t: '학생 대기 공간 그늘 천막', o: '학교행사 · 충주', c: 'school', y: '2026' },
    { i: 7, t: '세종 동문 체육대회 장비 렌탈', o: '체육대회 · 세종', c: 'sport', y: '2026' },
    { i: 8, t: '운동장 둘레 캐노피 천막 배치', o: '체육대회 · 세종', c: 'sport', y: '2026' },
    { i: 9, t: '체육대회 응원석 천막 · 의자', o: '체육대회 · 세종', c: 'sport', y: '2026' },
    { i: 10, t: '단양 동문 체육대회 천막 · 테이블', o: '체육대회 · 단양', c: 'sport', y: '2026' },
    { i: 11, t: '잔디 운동장 캐노피 천막 설치', o: '체육대회 · 단양', c: 'sport', y: '2026' },
    { i: 12, t: '단양 야외 플리마켓 핑크 천막', o: '축제 · 단양', c: 'fest', y: '2026' },
    { i: 13, t: '산책로를 따라 이어진 부스 천막', o: '축제 · 단양', c: 'fest', y: '2026' },
    { i: 14, t: '플리마켓 셀러 테이블 세팅', o: '축제 · 단양', c: 'fest', y: '2026' },
    { i: 15, t: '충주 에코그린데이 기업행사', o: '기업행사 · 충주', c: 'corp', y: '2026' },
    { i: 16, t: '도심 공원 몽골텐트 · 안내 부스', o: '기업행사 · 충주', c: 'corp', y: '2026' },
    { i: 17, t: '호수 위 조형물과 행사장 구성', o: '기업행사 · 충주', c: 'corp', y: '2026' },
    { i: 18, t: '체험 부스 천막 · 테이블 배치', o: '기업행사 · 충주', c: 'corp', y: '2026' },
    { i: 19, t: '야간 행사장 천막 · 조명 세팅', o: '기업행사 · 충주', c: 'corp', y: '2026' },
    { i: 20, t: '진천 기업행사 장비 렌탈', o: '기업행사 · 진천', c: 'corp', y: '2026' },
    { i: 21, t: '야외 무대 · LED 스크린 · 음향', o: '기업행사 · 진천', c: 'corp', y: '2026' },
    { i: 22, t: '접이식 테이블 · 의자 일괄 세팅', o: '기업행사 · 진천', c: 'corp', y: '2026' },
    { i: 23, t: '공원 행사 캐노피 천막 · 안내 부스', o: '기업행사 · 진천', c: 'corp', y: '2026' },
    { i: 24, t: '청주 오스코 세미나 테이블 렌탈', o: '세미나 · 청주', c: 'indoor', y: '2026' },
    { i: 25, t: '전시장 세미나 테이블 · 의자 세팅', o: '세미나 · 청주', c: 'indoor', y: '2026' },
    { i: 26, t: '충북 식품산업 상생협약식', o: '관공서 · 충북', c: 'gov indoor', y: '2026' },
    { i: 27, t: '협약식 좌석 · 배너 · 무대 구성', o: '관공서 · 충북', c: 'gov indoor', y: '2026' },
    { i: 28, t: '협약식 다과 · 케이터링 테이블', o: '관공서 · 충북', c: 'gov indoor', y: '2026' },
    { i: 29, t: '의자 커버 · 좌석 배치', o: '관공서 · 충북', c: 'gov indoor', y: '2026' },
    { i: 30, t: '초록우산 충북 아이리더 발대식', o: '기관행사 · 청주', c: 'gov indoor', y: '2026' },
    { i: 31, t: '라운드 테이블 · 테이블보 세팅', o: '기관행사 · 청주', c: 'gov indoor', y: '2026' },
    { i: 32, t: '무대 · 연단 · 음향 · 스크린', o: '기관행사 · 청주', c: 'gov indoor', y: '2026' },
    { i: 33, t: '발대식 무대 정면 구성', o: '기관행사 · 청주', c: 'gov indoor', y: '2026' },
    { i: 34, t: '청주 와인데이 썸머페스티벌', o: '축제 · 청주', c: 'fest', y: '2026' },
    { i: 35, t: '축제 판매 부스 · 테이블 세팅', o: '축제 · 청주', c: 'fest', y: '2026' },
    { i: 36, t: '야외 휴게 테이블 · 의자', o: '축제 · 청주', c: 'fest', y: '2026' },
    { i: 37, t: '부스 배너 · 안내 사인 설치', o: '축제 · 청주', c: 'fest', y: '2026' },
    { i: 38, t: '세종 학교 체육관 행사 캠핑의자', o: '학교행사 · 세종', c: 'school indoor', y: '2026' },
    { i: 39, t: '체육관 좌식 테이블 · 캠핑의자 배치', o: '학교행사 · 세종', c: 'school indoor', y: '2026' }
  ];
  var IMG = 'assets/img/works/w';

  /* ---------- 행사 이야기 (네이버 블로그 글 — 새 글은 맨 앞에 추가) ---------- */
  var BLOG = [
    { d: "2026.09.14", t: "옥천 전국연극제 준비, 부대행사 및 플리마켓 운영을 위한 천막 대여 가이드", u: "https://blog.naver.com/esgroup0102/224408729638" },
    { d: "2026.09.11", t: "수만 명 몰리는 천안 K컬처박람회, 복잡한 행사장비 렌탈과 안전 세팅 노하우", u: "https://blog.naver.com/esgroup0102/224404652577" },
    { d: "2026.09.09", t: "보은 가을 야외 행사 장비 렌탈, 번거로운 준비 과정 덜어내는 업체 선택 팁", u: "https://blog.naver.com/esgroup0102/224404112722" },
    { d: "2026.09.07", t: "충남 행사 몽골텐트 대여, 부스 용도에 따라 준비가 달라집니다", u: "https://blog.naver.com/esgroup0102/224402255356" },
    { d: "2026.09.04", t: "영동 정원박람회 준비에 필요한 행사준비, 공간별 대여 품목 정리", u: "https://blog.naver.com/esgroup0102/224399946860" },
    { d: "2026.09.02", t: "단양 행사 캐노피 천막 대여업체, 장비를 함께 빌릴 때 확인할 기준", u: "https://blog.naver.com/esgroup0102/224396584251" },
    { d: "2026.08.31", t: "제천 축제 행사장비 대여, 필요한 수량은 어떻게 정해야 할까요?", u: "https://blog.naver.com/esgroup0102/224392474898" },
    { d: "2026.08.28", t: "진천 대학입시박람회 준비, 운영 공간에 맞는 장비 대여 기준", u: "https://blog.naver.com/esgroup0102/224392189451" },
    { d: "2026.08.26", t: "증평 행사장 천막 설치, 옆면 가림막은 언제 사용하는게 좋을까요?", u: "https://blog.naver.com/esgroup0102/224389569444" },
    { d: "2026.08.24", t: "괴산 고추축제 준비, 행사 장비 대여는 언제부터 알아봐야 할까요?", u: "https://blog.naver.com/esgroup0102/224385665795" },
    { d: "2026.08.21", t: "음성 야외 체육행사 준비, 천막과 테이블이 필요한 공간은 어디일까요?", u: "https://blog.naver.com/esgroup0102/224384407435" },
    { d: "2026.08.19", t: "세종 학교 체육관 행사, 일반 의자 대신 캠핑의자를 활용하면 좋은 경우", u: "https://blog.naver.com/esgroup0102/224383083672" },
    { d: "2026.08.17", t: "충북 행사장비 대여, 공식행사 무대와 원형테이블 준비 방법", u: "https://blog.naver.com/esgroup0102/224377897491" },
    { d: "2026.08.14", t: "충북 기업행사 장비 대여, 협약식 좌석부터 테이블 세팅까지", u: "https://blog.naver.com/esgroup0102/224376255205" },
    { d: "2026.08.12", t: "청주 축제 장비 대여, 와인데이 썸머페스티벌 행사장 세팅 후기", u: "https://blog.naver.com/esgroup0102/224374537137" },
    { d: "2026.08.10", t: "단양 행사 조명 대여, 전력 부담을 줄이면서 야간 현장을 밝히는 방법", u: "https://blog.naver.com/esgroup0102/224373383541" },
    { d: "2026.08.07", t: "제천 행사용 천막 대여, 아스팔트와 잔디밭 설치 방식의 차이점", u: "https://blog.naver.com/esgroup0102/224370345958" },
    { d: "2026.08.05", t: "충주 봉숭아꽃잔치 장비 구성, 체험 대기줄과 공연 관람객이 겹치지 않으려면", u: "https://blog.naver.com/esgroup0102/224367175223" },
    { d: "2026.08.03", t: "증평 주민행사 준비, 장비 대여부터 행사장 빠른 세팅 방법까지", u: "https://blog.naver.com/esgroup0102/224365253822" },
    { d: "2026.07.31", t: "음성 소규모 공연 장비 대여, 합리적인 예산으로 구성하려면", u: "https://blog.naver.com/esgroup0102/224363166076" },
    { d: "2026.07.29", t: "옥천 행사 장비 대여, 텐트부터 무대까지 원스톱 준비법", u: "https://blog.naver.com/esgroup0102/224360715648" },
    { d: "2026.07.27", t: "영동 야외행사 장비 대여, 포도축제에 몽골천막이 필요하다면", u: "https://blog.naver.com/esgroup0102/224358652499" },
    { d: "2026.07.24", t: "단양 야외행사 장비 대여하는 곳, 천막과 테이블 설치까지 한 번에", u: "https://blog.naver.com/esgroup0102/224354792426" },
    { d: "2026.07.22", t: "제천 열대야 페스타 축제 준비, 여름행사 장비 선택 기준", u: "https://blog.naver.com/esgroup0102/224353527588" },
    { d: "2026.07.20", t: "충주에서 체육행사 준비할 때 꼭 확인해야 할 현장 구성 기준", u: "https://blog.naver.com/esgroup0102/224350498698" },
    { d: "2026.07.17", t: "행사장비 대여 비용은 무엇에 따라 달라질까요? 견적을 정하는 기준", u: "https://blog.naver.com/esgroup0102/224348822310" },
    { d: "2026.07.15", t: "진천 기업행사 장비 렌탈, 테이블 천막 의자 음향까지 한 번에", u: "https://blog.naver.com/esgroup0102/224346281963" },
    { d: "2026.07.13", t: "청주 테이블렌탈, 오스코 세미나 행사장비 대여 준비법", u: "https://blog.naver.com/esgroup0102/224343802424" },
    { d: "2026.07.10", t: "증평 전통문화축제 장비 대여, 체험부스와 관람 공간 준비 기준", u: "https://blog.naver.com/esgroup0102/224337435652" },
    { d: "2026.07.08", t: "음성 전통시장 이벤트 장비 대여, 경품행사와 홍보부스 준비 방법", u: "https://blog.naver.com/esgroup0102/224335733840" },
    { d: "2026.07.06", t: "괴산 여름 야외행사 장비 대여, 무더위 속 행사장 준비 방법", u: "https://blog.naver.com/esgroup0102/224335709960" },
    { d: "2026.07.03", t: "세종 먹거리 축제 장비 대여, 조치원 복숭아축제 현장 준비는 어떻게 할까", u: "https://blog.naver.com/esgroup0102/224334171568" },
    { d: "2026.07.01", t: "충주 7월 여름행사 장비 대여, 행사 규모에 맞는 장비 구성", u: "https://blog.naver.com/esgroup0102/224331776899" },
    { d: "2026.06.29", t: "영동 여름 행사 렌탈, 8월 축제 현장에서 필요한 장비 체크리스트", u: "https://blog.naver.com/esgroup0102/224329149073" },
    { d: "2026.06.26", t: "증평 행사장비 대여, 무더운 야외행사에 필요한 천막 구성법", u: "https://blog.naver.com/esgroup0102/224326875460" },
    { d: "2026.06.24", t: "제천 행사장비 대여, 공연과 체험부스 세팅 기준", u: "https://blog.naver.com/esgroup0102/224324571370" },
    { d: "2026.06.22", t: "진천 행사장비 대여, 여름 야외행사 부스와 그늘 공간 준비법", u: "https://blog.naver.com/esgroup0102/224322594828" },
    { d: "2026.06.19", t: "괴산 행사 장비 대여, 문화공연과 먹거리 부스 운영 준비 방법", u: "https://blog.naver.com/esgroup0102/224320135128" },
    { d: "2026.06.17", t: "세종 공연 행사 준비, 보헤미안 스테이지 무대와 관람 공간 세팅 포인트", u: "https://blog.naver.com/esgroup0102/224318053791" },
    { d: "2026.06.15", t: "영동 전통시장 행사 준비, 야시장과 토요장터에 필요한 렌탈 장비 구성", u: "https://blog.naver.com/esgroup0102/224315735084" },
    { d: "2026.06.12", t: "단양 동문 체육대회 준비, 캐노피 천막과 테이블 의자렌탈로 한 번에", u: "https://blog.naver.com/esgroup0102/224312671652" },
    { d: "2026.06.10", t: "제천 학교 운동회 행사용품 렌탈, 체육대회 준비 전 확인할 장비 구성", u: "https://blog.naver.com/esgroup0102/224309974450" },
    { d: "2026.06.08", t: "충주 기업행사 장비렌탈, 에코그린데이 행사장 세팅 포인트", u: "https://blog.naver.com/esgroup0102/224308186695" },
    { d: "2026.06.05", t: "증평 행사장비 대여, 장뜰들노래축제처럼 체험과 공연이 함께 있는 야외행사 준비법", u: "https://blog.naver.com/esgroup0102/224305190775" },
    { d: "2026.06.03", t: "음성 음향 장비 렌탈, 품바축제처럼 공연 많은 야외행사 준비법", u: "https://blog.naver.com/esgroup0102/224303752210" },
    { d: "2026.06.01", t: "괴산 천막 렌탈, 농산물 축제와 장터 행사 준비는 이렇게", u: "https://blog.naver.com/esgroup0102/224300079931" },
    { d: "2026.05.30", t: "세종 동문 체육대회 장비 렌탈, 캐노피천막부터 테이블 의자까지 기본 장비 구성", u: "https://blog.naver.com/esgroup0102/224299499261" },
    { d: "2026.05.28", t: "단양 야외 플리마켓 천막 렌탈, 핑크 천막으로 야외부스 분위기 살리기", u: "https://blog.naver.com/esgroup0102/224297918598" },
    { d: "2026.05.26", t: "충주 고등학교 운동회 천막렌탈, 햇빛 걱정 줄이는 행사장 세팅", u: "https://blog.naver.com/esgroup0102/224296667194" },
    { d: "2026.05.15", t: "진천 지역축제 장비렌탈, 작은 장비 차이가 행사 분위기를 바꿉니다", u: "https://blog.naver.com/esgroup0102/224284667818" }
  ];

  function workCard(w, k) {
    return '<figure data-k="' + k + '" data-c="' + w.c + '">' +
      '<img src="' + IMG + w.i + '.webp" alt="' + w.t + '" loading="lazy">' +
      '<figcaption><em>' + w.o + ' · ' + w.y + '</em><b>' + w.t + '</b></figcaption></figure>';
  }

  /* ---------- 상단 띠 · 모바일 메뉴 · 맨 위로 ---------- */
  var bar = $('#bar'), totop = $('#totop');
  function onScroll() {
    var y = window.scrollY;
    if (bar) bar.classList.toggle('stuck', y > 10 && bar.getBoundingClientRect().top <= 0);
    if (totop) totop.classList.toggle('on', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (totop) totop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  // 현재 페이지 메뉴 표시
  var curPath = location.pathname.replace(/\/$/, '/index.html'), inBlog = curPath.indexOf('/blog/') >= 0;
  $$('.bar .menu a, .sheet nav a').forEach(function (a) {
    var u = new URL(a.getAttribute('href'), location.href), p = u.pathname.replace(/\/$/, '/index.html');
    if ((p === curPath && u.hash === location.hash) || (inBlog && /\/blog\/index\.html$/.test(p))) a.classList.add('act');
  });

  var burger = $('#burger'), sheet = $('#sheet');
  function closeSheet() { if (!sheet) return; sheet.classList.remove('on'); if (burger) { burger.classList.remove('x'); burger.setAttribute('aria-expanded', 'false'); } document.body.style.overflow = ''; }
  if (burger && sheet) {
    burger.addEventListener('click', function () {
      var on = sheet.classList.toggle('on'); burger.classList.toggle('x', on); burger.setAttribute('aria-expanded', on);
      document.body.style.overflow = on ? 'hidden' : '';
    });
    $$('a, .x', sheet).forEach(function (a) { a.addEventListener('click', closeSheet); });
  }

  /* ---------- 히어로 슬라이더 ---------- */
  var hero = $('#hero');
  if (hero) {
    var slides = $$('.slide', hero), dots = $('#dots'), cnt = $('#cnt'), cur = 0, timer = null, DUR = 6000;
    slides.forEach(function (s, i) { var b = document.createElement('button'); b.innerHTML = '<i></i>'; b.setAttribute('aria-label', (i + 1) + '번 슬라이드'); b.addEventListener('click', function () { go(i); restart(); }); dots.appendChild(b); });
    var dotBtns = $$('button', dots);
    function go(i) {
      cur = (i + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle('on', k === cur); });
      dotBtns.forEach(function (d, k) { d.classList.toggle('on', k === cur); });
      cnt.innerHTML = '<b>' + String(cur + 1).padStart(2, '0') + '</b> / ' + String(slides.length).padStart(2, '0');
    }
    function restart() { clearInterval(timer); if (!reduce) timer = setInterval(function () { go(cur + 1); }, DUR); }
    go(0); restart();
    $('#prev').addEventListener('click', function () { go(cur - 1); restart(); });
    $('#next').addEventListener('click', function () { go(cur + 1); restart(); });
    hero.addEventListener('pointerenter', function () { hero.classList.add('paused'); clearInterval(timer); });
    hero.addEventListener('pointerleave', function () { hero.classList.remove('paused'); restart(); });
    var sx = 0;
    hero.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (e) { var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) { go(dx < 0 ? cur + 1 : cur - 1); restart(); } }, { passive: true });
    document.addEventListener('visibilitychange', function () { if (document.hidden) clearInterval(timer); else restart(); });
    slides.forEach(function (s) { var im = new Image(); im.src = $('.img', s).getAttribute('data-src'); $('.img', s).style.backgroundImage = 'url(' + im.src + ')'; });
  }

  /* ---------- 핵심 가치 탭 ---------- */
  var tabs = $('#vtabs');
  if (tabs) {
    var tb = $$('button', tabs), panes = $$('#vpanes .pane');
    tb.forEach(function (b, i) { b.addEventListener('click', function () { tb.forEach(function (x) { x.classList.remove('on'); }); panes.forEach(function (p) { p.classList.remove('on'); }); b.classList.add('on'); panes[i].classList.add('on'); }); });
  }

  /* ---------- 등장 · 숫자 ---------- */
  var revealEls = $$('.reveal');
  function checkReveal() {
    var h = window.innerHeight;
    revealEls = revealEls.filter(function (el) { if (el.getBoundingClientRect().top < h * .95) { el.classList.add('in'); return false; } return true; });
  }
  window.addEventListener('scroll', checkReveal, { passive: true }); window.addEventListener('resize', checkReveal); window.addEventListener('load', checkReveal);
  checkReveal(); setTimeout(checkReveal, 600); setTimeout(checkReveal, 2000);
  var cio = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return; cio.unobserve(e.target);
      var el = e.target, to = +el.getAttribute('data-count'), t0 = null, dur = 1500;
      if (reduce) { el.textContent = to.toLocaleString('ko-KR'); return; }
      (function step(ts) { if (!t0) t0 = ts; var k = Math.min(1, (ts - t0) / dur); k = 1 - Math.pow(1 - k, 3); el.textContent = Math.round(to * k).toLocaleString('ko-KR'); if (k < 1) requestAnimationFrame(step); })(performance.now());
    });
  }, { threshold: .5 });
  $$('[data-count]').forEach(function (el) { cio.observe(el); });

  /* ---------- 갤러리 (대문 9장 · 현장사진 전체) ---------- */
  var gal = $('#gal'), pf = $('#pfGrid'), list = [];
  if (gal) { list = [0, 3, 6, 11, 14, 20, 24, 26, 33].map(function (k) { return WORKS[k]; }); gal.innerHTML = list.map(workCard).join(''); }
  if (pf) { list = WORKS; pf.innerHTML = list.map(workCard).join(''); }
  var grid = gal || pf;
  var lb = $('#lb');
  if (grid && lb) {
    var figs = $$('figure', grid), lbImg = $('#lbImg'), lbT = $('#lbTitle'), lbM = $('#lbMeta'), lbK = 0;
    function visible() { return figs.filter(function (f) { return !f.classList.contains('hide'); }).map(function (f) { return +f.getAttribute('data-k'); }); }
    function openLb(k) { var w = list[k]; lbK = k; lbImg.src = IMG + w.i + '.webp'; lbImg.alt = w.t; lbT.textContent = w.t; lbM.textContent = w.o + ' · ' + w.y; lb.classList.add('on'); document.body.style.overflow = 'hidden'; }
    function closeLb() { lb.classList.remove('on'); document.body.style.overflow = ''; }
    function stepLb(d) { var v = visible(), i = v.indexOf(lbK); openLb(v[(i + d + v.length) % v.length]); }
    grid.addEventListener('click', function (e) { var f = e.target.closest('figure'); if (f) openLb(+f.getAttribute('data-k')); });
    $('#lbX').addEventListener('click', closeLb); $('#lbPrev').addEventListener('click', function () { stepLb(-1); }); $('#lbNext').addEventListener('click', function () { stepLb(1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    document.addEventListener('keydown', function (e) { if (!lb.classList.contains('on')) return; if (e.key === 'Escape') closeLb(); if (e.key === 'ArrowLeft') stepLb(-1); if (e.key === 'ArrowRight') stepLb(1); });
    var filters = $('#filters');
    if (filters) filters.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      $$('button', filters).forEach(function (x) { x.classList.remove('act'); }); b.classList.add('act');
      var f = b.getAttribute('data-f');
      figs.forEach(function (fg) { fg.classList.toggle('hide', f !== 'all' && fg.getAttribute('data-c').split(' ').indexOf(f) < 0); });
    });
  }

  /* ---------- 행사 이야기 목록 ---------- */
  var bl = $('#blogList');
  if (bl) {
    var LIMIT = +bl.getAttribute('data-limit') || 10, shown = LIMIT;
    function blogRow(b, k) { return '<a href="' + b.u + '" target="_blank" rel="noopener"' + (k >= shown ? ' class="hide"' : '') + '><small>' + b.d + '</small><b>' + b.t + '</b><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M9 7h8v8"/></svg></a>'; }
    bl.innerHTML = BLOG.map(blogRow).join('');
    var more = $('#blogMore');
    if (more) {
      if (BLOG.length <= LIMIT) more.hidden = true;
      more.addEventListener('click', function () { shown += LIMIT; $$('a', bl).forEach(function (a, k) { a.classList.toggle('hide', k >= shown); }); if (shown >= BLOG.length) more.hidden = true; });
    }
  }

  /* ---------- 공지사항 ---------- */
  var nl = $('#noticeList');
  if (nl) nl.innerHTML = NOTICES.length ? NOTICES.slice(0, 5).map(function (n) { return '<li><b>' + n.t + (n.n ? '<span class="new">NEW</span>' : '') + '</b><small>' + n.d + '</small></li>'; }).join('') : '<li class="empty">등록된 공지가 없습니다.</li>';

  /* ---------- 문의 보내기 (폼 · 견적 요청서 공용) ---------- */
  function isMobile() { return /iPhone|iPad|Android/i.test(navigator.userAgent); }
  function send(text, data, done, service) {
    if (FORM_ENDPOINT) {
      data.at = new Date().toISOString(); data.page = location.href; data.service = service; data.message = text;
      fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(data) }).catch(function () {}).then(function () { done(true); });
      return;
    }
    if (isMobile()) { var ios = /iPhone|iPad/i.test(navigator.userAgent); location.href = 'sms:' + SMS_TO + (ios ? '&' : '?') + 'body=' + encodeURIComponent(text); done(true); return; }
    if (navigator.clipboard) navigator.clipboard.writeText(text).catch(function () {});
    done(false);
  }

  var form = $('#quoteForm');
  if (form) {
    var done = $('#formDone');
    // 견적 요청서에서 넘어온 내용 (#q=)
    var qm = location.hash.match(/^#q=(.+)$/);
    if (qm && form.elements.msg) { try { form.elements.msg.value = decodeURIComponent(qm[1]); form.elements.msg.scrollIntoView({ block: 'center' }); } catch (e) {} }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.elements.website && form.elements.website.value) return; // 스팸 봇 함정
      var d = {}; ['name', 'tel', 'org', 'type', 'date', 'place', 'people', 'msg'].forEach(function (k) { d[k] = form.elements[k] ? form.elements[k].value.trim() : ''; });
      if (!d.name || !d.tel) { alert('담당자 이름과 연락처는 꼭 적어 주세요.'); (d.name ? form.elements.tel : form.elements.name).focus(); return; }
      if (!$('#fAgree').checked) { alert('개인정보 수집·이용에 동의해 주세요.'); return; }
      var text = '[' + COMPANY + ' 견적문의]\n담당자: ' + d.name + '\n연락처: ' + d.tel + '\n기관: ' + (d.org || '-') + '\n행사: ' + d.type + '\n날짜: ' + (d.date || '-') + '\n장소: ' + (d.place || '-') + '\n인원: ' + (d.people || '-') + '\n내용: ' + (d.msg || '-');
      send(text, d, function (sent) {
        done.classList.add('on');
        if (!sent) $('p', done).innerHTML = '문의 내용을 복사해 두었습니다.<br><b>' + SMS_TO + '</b> 로 문자 · 전화 주시면 바로 상담됩니다.';
      }, '행사 견적문의');
    });
  }

  /* ---------- 견적 요청서 만들기 (service.html) ---------- */
  var calc = $('#calc');
  if (calc) {
    var rows = $$('.row', calc), sumList = $('#sumList'), sumCnt = $('#sumCnt'), out = $('#calcText'), basic = $('#calcBasic');
    function val(k) { var el = basic.elements[k]; return el ? el.value.trim() : ''; }
    function build() {
      var lines = [], n = 0;
      rows.forEach(function (r) {
        var q = +$('input', r).value || 0; r.classList.toggle('on', q > 0);
        if (q > 0) { n++; lines.push({ n: r.getAttribute('data-n'), q: q, u: r.getAttribute('data-u') }); }
      });
      sumCnt.innerHTML = n + '<small>개 품목</small>';
      sumList.innerHTML = lines.length ? lines.map(function (l) { return '<li><span>' + l.n + '</span><b>' + l.q + l.u + '</b></li>'; }).join('') : '<li class="empty">왼쪽에서 필요한 품목의 수량을 올리면 여기에 정리됩니다. 정확한 수량을 몰라도 괜찮습니다. 대략만 적어 주세요.</li>';
      var t = '[' + COMPANY + ' 견적 요청서]\n';
      t += '행사명: ' + (val('ev') || '-') + '\n행사 유형: ' + val('type') + '\n날짜: ' + (val('date') || '-') + '\n장소: ' + (val('place') || '-') + '\n예상 인원: ' + (val('people') || '-') + '\n실내/야외: ' + val('inout') + '\n';
      t += '\n[필요 품목]\n' + (lines.length ? lines.map(function (l) { return '- ' + l.n + ' ' + l.q + l.u; }).join('\n') : '- (품목 미정 · 상담 요청)') + '\n';
      if (val('memo')) t += '\n[요청 사항]\n' + val('memo') + '\n';
      t += '\n연락처: ' + (val('tel') || '-') + ' / ' + (val('name') || '-');
      out.value = t;
      return t;
    }
    calc.addEventListener('click', function (e) {
      var b = e.target.closest('.qty button'); if (!b) return;
      var inp = $('input', b.parentNode), v = (+inp.value || 0) + (+b.getAttribute('data-d')); inp.value = Math.max(0, v); build();
    });
    calc.addEventListener('input', build); build();
    var cs = $('#calcSend'), cc = $('#calcCopy'), cf = $('#calcForm');
    if (cs) cs.addEventListener('click', function () {
      var t = build();
      if (!val('tel') || !val('name')) { alert('연락처와 이름을 적어 주셔야 답을 드릴 수 있어요.'); basic.elements.name.focus(); return; }
      if (!$('#cAgree').checked) { alert('개인정보 수집·이용에 동의해 주세요.'); return; }
      send(t, { name: val('name'), tel: val('tel'), type: val('type'), date: val('date'), place: val('place'), people: val('people') }, function (sent) {
        alert(sent ? '견적 요청서를 보냈습니다. 확인 후 1영업일 안에 연락드립니다.' : '요청서 내용을 복사해 두었습니다. ' + SMS_TO + ' 로 문자 · 전화 주시면 바로 상담됩니다.');
      }, '렌탈 견적 요청서');
    });
    if (cc) cc.addEventListener('click', function () { var t = build(); if (navigator.clipboard) navigator.clipboard.writeText(t).then(function () { cc.textContent = '복사됨 ✓'; setTimeout(function () { cc.textContent = '요청서 내용 복사'; }, 1800); }); else { out.select(); document.execCommand('copy'); } });
    if (cf) cf.addEventListener('click', function () { location.href = 'contact.html#q=' + encodeURIComponent(build()); });
  }
})();

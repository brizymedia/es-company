/*
 * 이에스컴퍼니 — 견적 품목표와 견적 코드 읽기
 *
 * quote.html 과 schedule.html 이 함께 쓴다. 품목을 고칠 곳은 여기 하나뿐이다.
 * 견적서에는 서버가 없다 — 견적 하나가 주소 뒤 #q= 에 담기는 짧은 코드 하나다.
 * 그 코드를 푸는 규칙도 여기 둔다(두 화면이 같은 규칙으로 읽어야 하니까).
 */

const CATALOG = [
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
];
const BY_ID = {};
CATALOG.forEach(g => g.items.forEach(it => { BY_ID[it.id] = it; }));

const 견적정보칸 = ['org','name','tel','email','title','date','place','people','memo'];
const 견적정보짧게 = { org:'o', name:'n', tel:'t', email:'e', title:'m', date:'d', place:'p', people:'c', memo:'x' };

const 견적b64u   = (s) => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const 견적unb64u = (s) => {
  let t = String(s).replace(/-/g, '+').replace(/_/g, '/');
  while (t.length % 4) t += '=';
  return decodeURIComponent(escape(atob(t)));
};

/**
 * 견적 코드를 사람이 읽을 수 있는 모양으로 푼다.
 *   { 정보:{org,name,tel,…}, 줄:[{id,name,spec,qty,unit,days,price}], 할인 }
 * 못 읽으면 null.
 */
function 견적풀기(코드) {
  try {
    const s = JSON.parse(견적unb64u(코드));
    const 정보 = {};
    견적정보칸.forEach((k, idx) => {
      const i = s.i;
      if (!i) { 정보[k] = ''; return; }
      const v = Array.isArray(i) ? i[idx]
              : (i[견적정보짧게[k]] != null ? i[견적정보짧게[k]] : i[k]);
      정보[k] = v == null ? '' : String(v);
    });

    const 책 = (id) => BY_ID[id] || { name: '', spec: '', unit: '식' };
    const 줄 = (s.r || []).map((a) => {
      if (typeof a === 'string') {
        const c = 책(a);
        return { id: a, name: c.name, spec: c.spec, qty: 1, unit: c.unit, days: 1, price: null };
      }
      if (a.length <= 4) {
        const c = 책(a[0]);
        return { id: a[0], name: c.name, spec: c.spec,
                 qty: a[1] != null ? a[1] : 1, unit: c.unit,
                 days: a[2] != null ? a[2] : 1,
                 price: a[3] != null ? a[3] : null };
      }
      return { id: a[0], name: a[1], spec: a[2], qty: a[3], unit: a[4], days: a[5], price: a[6] };
    });

    return { 정보: 정보, 줄: 줄, 할인: +s.d || 0 };
  } catch (e) { return null; }
}

/* 견적 한 줄을 「300명 내외 · 스피커 4통 · 2개 · 2일」 같은 한 줄 설명으로 */
function 견적줄설명(r) {
  return [r.spec, (+r.qty > 1 ? r.qty + (r.unit || '') : ''), (+r.days > 1 ? r.days + '일' : '')]
    .filter(Boolean).join(' · ');
}

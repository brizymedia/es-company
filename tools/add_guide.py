# -*- coding: utf-8 -*-
"""이에스컴퍼니 사이트에 guide.html(홈페이지 활용 안내) 넣기 + 바닥글 링크 + robots + app.js 버전."""
import io, os, re, glob

SITE = os.path.expanduser('~/Documents/es-company')
SRC = r'C:\Users\gilau\Desktop\큰길브리지\이에스컴퍼니\이에스컴퍼니-홈페이지-활용안내-2026-10-13.html'
def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

# 1) guide.html — 주소를 눌러 열리게, 검색 제외, 파비콘, 홈으로 가는 줄
s = rd(SRC)
s = s.replace('<title>이에스컴퍼니 홈페이지 활용 안내</title>',
              '<title>홈페이지 활용 안내 — 이에스컴퍼니</title>\n<meta name="robots" content="noindex,nofollow">\n<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">', 1)
def linkify(html):
    out = []; pos = 0
    # 태그 밖 글자에서만 주소를 찾는다
    for m in re.finditer(r'<[^>]+>', html):
        out.append(_link(html[pos:m.start()])); out.append(m.group(0)); pos = m.end()
    out.append(_link(html[pos:]))
    return ''.join(out)
def _link(text):
    def rep(m):
        u = m.group(0)
        tail = ''
        while u and u[-1] in '.,)）': tail = u[-1] + tail; u = u[:-1]
        href = u if u.startswith('http') else 'https://' + u
        if '열쇠' in u: return m.group(0)
        return '<a href="' + href + '">' + u + '</a>' + tail
    return re.sub(r'(https?://[^\s<「」]+|www\.es-company\.co\.kr(?:/[^\s<「」]*)?)', rep, text)
head, body = s.split('<body>', 1)
body = linkify(body)
s = head + '<body>' + body
s = s.replace('<div class="wrap">\n<h1>', '<div class="wrap">\n<p style="margin:0 0 14px;font-size:13px"><a href="index.html" style="color:#6b7280;text-decoration:none">← 이에스컴퍼니 홈페이지로</a></p>\n<h1>', 1)
s = s.replace('a{', 'a{', 1)
s = s.replace('  .foot{', '  a{ color:var(--acc); }\n  .foot{', 1)
wr(os.path.join(SITE, 'guide.html'), s)
print('guide.html', len(s))

# 2) app.js — 바닥글 맨 끝에 「홈페이지 사용 안내」 작은 링크 (모든 페이지: blog · areas 포함)
a = rd(os.path.join(SITE, 'assets/app.js'))
if 'guide-entry' not in a:
    a = a.rstrip('\n') + '''

/* ---------- 홈페이지 사용 안내 — 바닥글 맨 끝 작은 링크 → guide.html (대표님용, 검색 제외) ---------- */
(function () {
  var cs = document.currentScript, base = cs && cs.src ? cs.src.replace(/assets\\/app\\.js(\\?.*)?$/, '') : '';
  function add() {
    var ft = document.querySelector('footer'); if (!ft || ft.querySelector('.guide-entry')) return;
    var d = document.createElement('div'); d.className = 'guide-entry';
    d.style.cssText = 'text-align:center;padding:10px 0 16px;font-size:12px;line-height:1';
    d.innerHTML = '<a href="' + base + 'guide.html" rel="nofollow" style="color:inherit;opacity:.55;text-decoration:none;display:inline-flex;align-items:center;gap:5px">' +
      '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H4z"/><path d="M20 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z"/></svg>홈페이지 사용 안내</a>';
    ft.appendChild(d);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', add); else add();
})();
'''
    wr(os.path.join(SITE, 'assets/app.js'), a)
    print('app.js 바닥글 링크 추가')

# 3) app.js?v=5 → v6 (캐시)
n = 0
for p in glob.glob(os.path.join(SITE, '**/*.html'), recursive=True) + [os.path.join(SITE, 'tools/build_blog.py'), os.path.join(SITE, 'tools/build_extra.py')]:
    t = rd(p)
    if 'app.js?v=5' in t: wr(p, t.replace('app.js?v=5', 'app.js?v=6')); n += 1
print('버전 올린 파일', n)

# 4) robots — guide.html 검색 제외
b = rd(os.path.join(SITE, 'tools/build_extra.py'))
old = "Disallow: /statement.html\\n\\n'"
if 'guide.html' not in b:
    assert old in b
    b = b.replace(old, "Disallow: /statement.html\\nDisallow: /guide.html\\n\\n'", 1); wr(os.path.join(SITE, 'tools/build_extra.py'), b); print('robots 규칙 추가')

# 5) README
r = rd(os.path.join(SITE, 'README.md'))
anchor = '- 직인: `assets/img/stamp-es.png`'
if 'guide.html' not in r:
    r = r.replace(anchor, "- 대표님용 활용 안내 `guide.html`(2026-10-13, 박 대표 질문 4가지 답 + 마케팅 월간 팩 제안) — 원본은 `Desktop\\큰길브리지\\이에스컴퍼니\\이에스컴퍼니-홈페이지-활용안내-2026-10-13.html`, 고치면 `tools/add_guide.py` 같은 방식으로 다시 복사(주소 링크화 · noindex · 파비콘). 모든 페이지 바닥글 맨 끝 「홈페이지 사용 안내」 링크는 `assets/app.js` 끝 블록. robots 에서 제외.\n" + anchor, 1)
    wr(os.path.join(SITE, 'README.md'), r); print('README 추가')

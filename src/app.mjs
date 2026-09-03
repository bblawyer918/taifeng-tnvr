/* ══════════════════════════════════════════════════════════════
   設定區：整份網頁只有這裡要改。把兩個 Google 表單網址貼進來。
   Google 表單 → 右上「傳送」→ 選鏈結圖示 🔗 → 複製網址
   ══════════════════════════════════════════════════════════════ */
var FORMS = {
  report:   "https://REPLACE-ME.example/通報表單",   // 「立即通報」：發現沒剪耳的浪貓
  complain: "https://REPLACE-ME.example/檢舉表單"    // 「我要檢舉」：餵食後沒整理環境
};

(function () {
  var links = document.querySelectorAll("[data-form]");
  for (var i = 0; i < links.length; i++) {
    var u = FORMS[links[i].getAttribute("data-form")];
    if (u) links[i].href = u;
  }
  if (/REPLACE-ME/.test(FORMS.report + FORMS.complain)) {
    console.warn("[台鳳里] 表單網址尚未填寫，請修改 index.html 最上方的 FORMS 設定區。");
  }
})();

(function () {
  var svg = document.getElementById('map');
  var pz = document.getElementById('pz');
  var wrap = document.getElementById('mapWrap');
  var hint = document.getElementById('mapHint');
  if (!svg || !pz) return;

  var MIN = 0.75, MAX = 4.5, HOME = { k: 1, tx: 0, ty: 0 };
  var view = { k: 1, tx: 0, ty: 0 };
  var markers = Array.prototype.slice.call(pz.querySelectorAll('.marker'));
  var cards = Array.prototype.slice.call(wrap.querySelectorAll('.cat-card'));

  function apply() {
    pz.setAttribute('transform', 'translate(' + view.tx.toFixed(2) + ' ' + view.ty.toFixed(2) +
      ') scale(' + view.k.toFixed(4) + ')');
    var inv = (1 / view.k).toFixed(4);
    for (var i = 0; i < markers.length; i++) {
      markers[i].firstElementChild.setAttribute('transform', 'scale(' + inv + ')');
    }
  }

  // 螢幕座標 → viewBox 座標
  function toUser(ev) {
    var m = svg.getScreenCTM();
    if (!m) return { x: 0, y: 0 };
    var p = svg.createSVGPoint();
    p.x = ev.clientX; p.y = ev.clientY;
    p = p.matrixTransform(m.inverse());
    return { x: p.x, y: p.y };
  }

  function clamp() {
    view.k = Math.min(MAX, Math.max(MIN, view.k));
    // 讓里界不會被拖出畫面：限制平移量
    var limX = 1000 * 0.55 * view.k, limY = 1250 * 0.55 * view.k;
    view.tx = Math.min(limX, Math.max(-limX, view.tx));
    view.ty = Math.min(limY, Math.max(-limY, view.ty));
  }

  function zoomAt(factor, ux, uy) {
    var k0 = view.k;
    view.k = Math.min(MAX, Math.max(MIN, k0 * factor));
    var r = view.k / k0;
    view.tx = ux - (ux - view.tx) * r;
    view.ty = uy - (uy - view.ty) * r;
    clamp(); apply();
  }

  // ── 拖曳與縮放 ──────────────────────────────────
  var pts = {}, last = null, pinch = null, moved = 0;

  svg.addEventListener('pointerdown', function (e) {
    svg.setPointerCapture(e.pointerId);
    pts[e.pointerId] = toUser(e);
    moved = 0;
    var ids = Object.keys(pts);
    if (ids.length === 1) { last = pts[e.pointerId]; svg.classList.add('dragging'); }
    else if (ids.length === 2) {
      var a = pts[ids[0]], b = pts[ids[1]];
      pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), cx: (a.x + b.x) / 2, cy: (a.y + b.y) / 2 };
    }
  });

  svg.addEventListener('pointermove', function (e) {
    if (!(e.pointerId in pts)) return;
    var now = toUser(e);
    var ids = Object.keys(pts);
    if (ids.length >= 2 && pinch) {
      pts[e.pointerId] = now;
      var a = pts[ids[0]], b = pts[ids[1]];
      var d = Math.hypot(a.x - b.x, a.y - b.y);
      if (pinch.d > 0.001) zoomAt(d / pinch.d, pinch.cx, pinch.cy);
      pinch.d = d;
      moved = 99;
      return;
    }
    if (!last) return;
    var dx = now.x - last.x, dy = now.y - last.y;
    moved += Math.abs(dx) + Math.abs(dy);
    view.tx += dx; view.ty += dy;
    clamp(); apply();
    pts[e.pointerId] = toUser(e);
    last = pts[e.pointerId];
  });

  function endPtr(e) {
    delete pts[e.pointerId];
    if (Object.keys(pts).length < 2) pinch = null;
    if (Object.keys(pts).length === 0) { last = null; svg.classList.remove('dragging'); }
  }
  svg.addEventListener('pointerup', endPtr);
  svg.addEventListener('pointercancel', endPtr);

  svg.addEventListener('wheel', function (e) {
    e.preventDefault();
    var u = toUser(e);
    zoomAt(e.deltaY < 0 ? 1.16 : 1 / 1.16, u.x, u.y);
  }, { passive: false });

  document.getElementById('zin').onclick = function () { zoomAt(1.35, 500, 625); };
  document.getElementById('zout').onclick = function () { zoomAt(1 / 1.35, 500, 625); };
  document.getElementById('zreset').onclick = function () {
    view = { k: HOME.k, tx: HOME.tx, ty: HOME.ty }; apply(); close();
  };

  // ── 貓咪資訊卡 ──────────────────────────────────
  function close() {
    cards.forEach(function (c) { c.hidden = true; });
    markers.forEach(function (m) { m.classList.remove('is-on'); });
    if (hint) hint.classList.remove('hide');
  }

  function open(i) {
    cards.forEach(function (c, j) { c.hidden = j !== i; });
    markers.forEach(function (m, j) { m.classList.toggle('is-on', j === i); });
    if (hint) hint.classList.add('hide');
  }

  markers.forEach(function (m, i) {
    m.addEventListener('pointerup', function (e) {
      if (moved > 12) return;
      e.stopPropagation();
      m.classList.contains('is-on') ? close() : open(i);
    });
    m.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); }
    });
  });

  cards.forEach(function (c) {
    c.querySelector('.cat-card-close').onclick = close;
  });

  svg.addEventListener('pointerup', function () { if (moved <= 12) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

  // ── 捲動後浮出通報鍵 ────────────────────────────
  var dock = document.querySelector('.dock');
  if (dock && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (rows) {
      dock.classList.toggle('show', !rows[0].isIntersecting);
    }, { threshold: 0 }).observe(wrap);
  }

  apply();
})();

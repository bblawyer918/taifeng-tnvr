/* ══════════════════════════════════════════════════════════════
   設定區：整份網頁只有這裡要改。
   把 Apps Script 的網頁應用程式網址貼進來（部署步驟見 apps-script/README.md）。
   ══════════════════════════════════════════════════════════════ */
var ENDPOINT = "https://REPLACE-ME.example/exec";

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

/* ── 站內表單 ────────────────────────────────────────────── */
(function () {
  var sheets = {};
  document.querySelectorAll('.form-sheet').forEach(function (el) {
    sheets[el.id.replace('form-', '')] = el;
  });
  if (!Object.keys(sheets).length) return;

  var open = null;

  function show(kind) {
    var el = sheets[kind];
    if (!el) return;
    el.hidden = false;
    open = el;
    document.body.style.overflow = 'hidden';
    var first = el.querySelector('.txt');
    if (first) setTimeout(function () { first.focus(); }, 260);
  }

  function hide() {
    if (!open) return;
    open.hidden = true;
    document.body.style.overflow = '';
    // 還原成可再次填寫的狀態
    open.querySelector('.form-body').hidden = false;
    open.querySelector('.form-done').hidden = true;
    open = null;
  }

  document.querySelectorAll('[data-open]').forEach(function (b) {
    b.addEventListener('click', function () { show(b.getAttribute('data-open')); });
  });
  document.querySelectorAll('[data-close]').forEach(function (b) {
    b.addEventListener('click', hide);
  });
  document.querySelectorAll('.form-sheet').forEach(function (el) {
    el.addEventListener('click', function (e) { if (e.target === el) hide(); });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') hide(); });

  // 目前位置
  document.querySelectorAll('[data-geo]').forEach(function (btn) {
    var id = btn.getAttribute('data-geo');
    var out = document.querySelector('[data-geo-out="' + id + '"]');
    btn.addEventListener('click', function () {
      if (!navigator.geolocation) {
        out.hidden = false; out.textContent = '這台裝置不支援定位，直接寫地點就好。';
        return;
      }
      btn.disabled = true; btn.textContent = '抓取中⋯⋯';
      navigator.geolocation.getCurrentPosition(function (p) {
        btn.dataset.lat = p.coords.latitude.toFixed(6);
        btn.dataset.lng = p.coords.longitude.toFixed(6);
        out.hidden = false;
        out.textContent = '✓ 已記錄位置（' + btn.dataset.lat + ', ' + btn.dataset.lng + '）';
        btn.textContent = '重新抓一次'; btn.disabled = false;
      }, function () {
        out.hidden = false;
        out.style.color = 'var(--ink-faint)';
        out.textContent = '抓不到位置，直接把地點寫在上面就可以。';
        btn.textContent = '再試一次'; btn.disabled = false;
      }, { enableHighAccuracy: true, timeout: 10000 });
    });
  });

  // 聯絡方式：換管道時同步換提示文字
  document.querySelectorAll('.form-body').forEach(function (form) {
    var box = form.querySelector('[name=contact]');
    if (!box) return;
    form.querySelectorAll('[name=contact_type]').forEach(function (r) {
      r.addEventListener('change', function () { box.placeholder = r.dataset.ph || ''; });
    });
  });

  // 上傳前先縮圖，避免佔使用者流量
  function shrink(file, cb) {
    if (!file) return cb('');
    var img = new Image(), url = URL.createObjectURL(file);
    img.onload = function () {
      var s = Math.min(1, 1400 / Math.max(img.width, img.height));
      var c = document.createElement('canvas');
      c.width = Math.round(img.width * s);
      c.height = Math.round(img.height * s);
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      URL.revokeObjectURL(url);
      try { cb(c.toDataURL('image/jpeg', 0.72)); } catch (err) { cb(''); }
    };
    img.onerror = function () { URL.revokeObjectURL(url); cb(''); };
    img.src = url;
  }

  document.querySelectorAll('.form-body').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('[data-msg]');
      var btn = form.querySelector('.submit');
      var place = form.querySelector('[name=place]');

      if (!place.value.trim()) {
        msg.textContent = '請先寫下你在哪裡看到的，這樣我們才找得到。';
        place.focus();
        return;
      }
      if (/REPLACE-ME/.test(ENDPOINT)) {
        msg.textContent = '表單後端還沒接上，請先完成 apps-script/README.md 的部署步驟。';
        return;
      }

      msg.textContent = '';
      btn.disabled = true;
      btn.textContent = '送出中⋯⋯';

      var geo = form.querySelector('[data-geo]');
      var data = { kind: form.getAttribute('data-kind') };
      new FormData(form).forEach(function (v, k) { if (k !== 'photo') data[k] = v; });
      if (geo && geo.dataset.lat) data.coords = geo.dataset.lat + ',' + geo.dataset.lng;
      data.contact = data.contact && data.contact.trim()
        ? (data.contact_type || '') + '：' + data.contact.trim() : '';
      delete data.contact_type;

      shrink(form.querySelector('[name=photo]').files[0], function (photo) {
        data.photo = photo;
        fetch(ENDPOINT, { method: 'POST', body: JSON.stringify(data) })
          .then(function (r) { return r.json(); })
          .then(function (r) {
            if (!r || !r.ok) throw new Error(r && r.error ? r.error : 'unknown');
            form.hidden = true;
            form.parentNode.querySelector('.form-done').hidden = false;
            form.reset();
          })
          .catch(function () {
            msg.textContent = '送不出去，可能是網路不穩。再按一次試試，或直接把照片和地點傳到里的群組。';
          })
          .then(function () {
            btn.disabled = false;
            btn.textContent = form.getAttribute('data-kind') === 'report' ? '送出通報' : '送出檢舉';
          });
      });
    });
  });
})();

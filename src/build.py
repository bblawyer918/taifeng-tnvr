# -*- coding: utf-8 -*-
import json, html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import art, forms

M = json.load(open(os.path.join(HERE, 'mapdata.json'), encoding='utf-8'))
F = M['frame']

LI      = "台鳳里"
CITY    = "彰化市"

# ⚠️ 示範資料 — 座標取自台鳳里實際街道，貓咪名稱與數量請換成里內實際紀錄
CATS = [
  dict(key="orange", name="橘貓小橘", lat=24.074471, lng=120.597780,
       area="一心南街、一德南路200巷", count="區域數量：統計中", note="怕生，看到人會先退兩步"),
  dict(key="calico", name="三花小花", lat=24.072634, lng=120.598425,
       area="一德南路254巷、互助一街3巷", count="區域數量：約 5 隻", note="常在騎樓下午睡"),
  dict(key="brown",  name="棕貓小棕", lat=24.072874, lng=120.600406,
       area="一心東街、互助二街", count="區域數量：約 8 隻", note="固定在同一處等餵食"),
  dict(key="tuxedo", name="賓士小黑", lat=24.071815, lng=120.600798,
       area="互助一街、互助一街1巷", count="區域數量：3 隻", note="夜間才會出現"),
]

def prj(lat, lng):
    x = (lng - F['lng0']) / (F['lng1'] - F['lng0']) * F['w']
    y = (F['lat0'] - lat) / (F['lat0'] - F['lat1']) * F['h']
    return round(x, 1), round(y, 1)

# ── 地圖 SVG ────────────────────────────────────────────────
def paths(cls, key):
    return "".join('<path class="%s" d="%s"/>' % (cls, d) for d in M['roads'][key])

NET = (
  '<g class="rd-case">' + paths('rc-major','major') + paths('rc-mid','mid') + '</g>'
  '<g class="rd-ink">'  + paths('r-minor','minor') + paths('r-foot','foot')
                        + paths('r-mid','mid') + paths('r-major','major') + '</g>'
)

lbls = []
for L in M['labels']:
    if not L['in']:
        continue
    lbls.append('<text class="st-label" x="%s" y="%s" transform="rotate(%s %s %s)">%s</text>'
                % (L['x'], L['y'], L['rot'], L['x'], L['y'], html.escape(L['name'])))
LABELS = "".join(lbls)

symbols = "".join(
    '<symbol id="cat-%s" viewBox="0 0 118 76">%s</symbol>'
    % (k, art.cat(v).split('>', 1)[1].rsplit('</svg>', 1)[0])
    for k, v in art.PALETTES.items()
)

markers = []
for i, c in enumerate(CATS):
    x, y = prj(c['lat'], c['lng'])
    markers.append(
      '<g class="marker" data-i="%d" transform="translate(%s %s)" tabindex="0" role="button" '
      'aria-label="%s">'
      '<g class="marker-scale">'
      '<ellipse class="pin-glow" cx="0" cy="30" rx="54" ry="16"/>'
      '<circle class="hit" cx="0" cy="8" r="62"/>'
      '<use href="#cat-%s" x="-59" y="-30" width="118" height="76"/>'
      '</g></g>' % (i, x, y, html.escape(c['name']), c['key']))
MARKERS = "".join(markers)

MAP_SVG = f'''<svg id="map" viewBox="0 0 {F['w']:.0f} {F['h']:.0f}" preserveAspectRatio="xMidYMid slice"
     xmlns="http://www.w3.org/2000/svg" aria-label="{LI}浪貓分布地圖">
  <defs>
    <g id="netw">{NET}</g>
    <mask id="inside">
      <rect x="0" y="0" width="{F['w']:.0f}" height="{F['h']:.0f}" fill="#000"/>
      <path d="{M['boundary']}" fill="#fff"/>
    </mask>
    {symbols}
  </defs>
  <g id="pz">
    <g class="layer-out">
      <rect x="-2000" y="-2000" width="5000" height="5000" class="ground"/>
      <use href="#netw"/>
    </g>
    <g class="layer-in" mask="url(#inside)">
      <rect x="-2000" y="-2000" width="5000" height="5000" class="ground"/>
      <use href="#netw"/>
      {LABELS}
    </g>
    <path class="boundary-glow" d="{M['boundary']}"/>
    <path class="boundary" d="{M['boundary']}"/>
    {MARKERS}
  </g>
</svg>'''

TILES = [
  ("T", "捕捉", "Trap",      art.ICON_T, "誘捕籠請向里辦公處或動保單位借用，捕捉後全程覆蓋布巾安撫。"),
  ("N", "絕育", "Neuter",    art.ICON_N, "由合作獸醫院執行結紮手術，術後留院觀察，母貓再多休養幾天。"),
  ("V", "施打疫苗", "Vaccinate", art.ICON_V, "同時完成狂犬病疫苗與必要防疫處置，降低疾病在社區流通。"),
  ("R", "原地放回", "Return", art.ICON_R, "回到原本熟悉的巷弄，牠會守住地盤，外來未絕育的貓就進不來。"),
]

tiles = "".join(f'''
      <li class="tile">
        <span class="tile-badge">{k}</span>
        <div class="tile-art">{svg}</div>
        <p class="tile-zh">{zh}</p>
        <p class="tile-en"><b>{en[0]}</b>{en[1:]}</p>
        <p class="tile-note">{note}</p>
      </li>''' for k, zh, en, svg, note in TILES)

catcards = "".join(f'''
    <article class="cat-card" data-card="{i}" hidden>
      <div class="cat-card-art">{art.cat(art.PALETTES[c['key']])}</div>
      <div class="cat-card-body">
        <h3>{html.escape(c['name'])}<span class="tnr-chip" title="已完成 TNVR">已剪耳</span></h3>
        <dl>
          <div><dt>經常活動區域</dt><dd>{html.escape(c['area'])}</dd></div>
          <div><dt>同區浪貓</dt><dd>{html.escape(c['count'])}</dd></div>
          <div><dt>相處提醒</dt><dd>{html.escape(c['note'])}</dd></div>
        </dl>
      </div>
      <button class="cat-card-close" type="button" aria-label="關閉">關閉</button>
    </article>''' for i, c in enumerate(CATS))

clouds = "".join(f'<span class="cloud c{i}">{art.CLOUD}</span>' for i in range(1, 7))

BODY = f'''
<a class="skip" href="#report">跳到通報表單</a>

<div class="phone">

  <header class="hero">
    <div class="map-wrap" id="mapWrap">
      {MAP_SVG}
      <p class="map-chip">{LI}浪貓地圖</p>
      <div class="map-hint" id="mapHint">
        <span class="hint-cat">{art.cat(art.PALETTES['calico'])}</span>
        <p><b>貓貓害羞，相遇時請溫柔一點唷</b><br>
        <span class="hint-sub">點地圖上的貓咪可以看牠的資訊</span></p>
      </div>
      <div class="map-tools">
        <button type="button" id="zin" aria-label="放大">＋</button>
        <button type="button" id="zout" aria-label="縮小">－</button>
        <button type="button" id="zreset" aria-label="回到{LI}">回正</button>
      </div>
      {catcards}
    </div>
    <button class="pill-cta" type="button" data-open="report">立即通報
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h12M12 6l6 6-6 6" fill="none"
        stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
  </header>

  <main>
    <section class="intro">
      <h1>看見浪貓請告訴我們！</h1>
      <p>{LI}透過 <b>TNVR</b> 行動及宣導正確觀念，打造人貓共好的友善生活圈 🪴</p>

      <section class="tnvr" aria-labelledby="tnvr-h">
        <h2 id="tnvr-h">TNVR 是什麼？</h2>
        <p class="tnvr-lead">四個步驟一次做完，才算完成一輪。順序不能跳。</p>
        <ol class="tiles">{tiles}
        </ol>
        <p class="tnvr-foot">現行能有效控制流浪動物數量的方式，並可降低干擾事件及掌握區域流浪動物狀況 🐱</p>
      </section>

      <p class="ask">若在{LI}發現<b>尚未絕育</b>的浪貓，請透過下方表單協助通報！</p>
    </section>

    <section class="eartip">
      <div class="sky">{clouds}</div>
      <div class="eartip-inner">
        <div class="bubble">
          <p>被<mark>剪耳</mark>就是<br>已絕育貓貓！</p>
        </div>
        <figure class="eartip-fig">
          {art.EARTIP}
          <figcaption>左耳剪一角＝已完成 TNVR，不用再通報</figcaption>
        </figure>
      </div>
      <div class="skyline">{art.SKYLINE}</div>
    </section>

    <section class="cta" id="report">
      <h2><span class="slash">＼</span>一起打造友善社區吧<span class="slash">／</span></h2>

      <button class="act act-report" type="button" data-open="report">
        <span class="act-q">在{LI}遇到<b>沒有剪耳</b>的浪貓？</span>
        <span class="act-btn">立即通報</span>
        <span class="act-art">{art.CAT_SILHOUETTE}</span>
      </button>

      <button class="act act-report act-complain" type="button" data-open="complain">
        <span class="act-q">在{LI}餵完浪貓<b>沒有整理環境</b>？</span>
        <span class="act-btn">我要檢舉</span>
        <span class="act-art">{art.FISHBONE}</span>
      </button>
    </section>
  </main>

  <footer>
    <p>© 2026 {CITY}{LI}浪貓通報站</p>
    <p class="foot-note">地圖里界資料來源：OpenStreetMap 貢獻者</p>
  </footer>

  <button class="dock" type="button" data-open="report">立即通報
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h12M12 6l6 6-6 6" fill="none"
      stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></button>

  {forms.ALL}
</div>
'''

CSS = open(os.path.join(HERE, 'style.css'), encoding='utf-8').read()
JS  = open(os.path.join(HERE, 'app.mjs'),  encoding='utf-8').read()

HEAD_BITS = f'''<title>{LI}浪貓通報站</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<style>{CSS}</style>'''

TAIL = f'<script>{JS}</script>'

# 1) Artifact 版本（不含 doctype/html/head/body）
open(os.path.join(HERE, 'artifact.html'), 'w', encoding='utf-8').write(HEAD_BITS + BODY + TAIL)

# 2) 可直接部署的獨立網頁
standalone = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{CITY}{LI}浪貓通報站：里內浪貓分布地圖、TNVR 說明與通報／檢舉表單。">
<meta name="theme-color" content="#2BA6DE">
{HEAD_BITS}
</head>
<body>
{BODY}
{TAIL}
</body>
</html>'''
out = os.path.join(ROOT, 'index.html')
open(out, 'w', encoding='utf-8').write(standalone)
print('index.html 已重新產生')
print(out, '%d KB' % (os.path.getsize(out)//1024))

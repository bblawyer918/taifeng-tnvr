# -*- coding: utf-8 -*-
"""自繪 SVG 插圖庫：躺姿貓咪、雲、天際線、TNVR 四格圖示、剪耳示意。"""

def cat(pal, ear_tip=True, uid="c"):
    """側躺貓，面向右。pal: dict(body, shade, belly, patch, ear, face)"""
    body, shade, belly = pal["body"], pal["shade"], pal["belly"]
    ear, face = pal.get("ear", "#E88FA0"), pal.get("face", "#2E2E38")
    patch = pal.get("patch")
    stripes = ""
    if pal.get("stripes"):
        stripes = f'''
    <g fill="{shade}" opacity=".85">
      <path d="M44 31c5-1 9 0 12 2l-3 5c-3-2-6-3-10-2z"/>
      <path d="M33 33c5-1 9 1 12 3l-3 5c-3-2-6-3-10-3z"/>
      <path d="M22 37c4-1 8 1 11 3l-3 5c-3-2-5-3-9-3z"/>
    </g>'''
    patches = ""
    if patch:
        patches = f'''
    <g>
      <path fill="{patch[0]}" d="M60 30c9-2 17 1 21 7-6 5-16 6-24 2z"/>
      <path fill="{patch[1]}" d="M20 34c8-2 14 0 18 5-6 5-14 6-21 3z"/>
    </g>'''
    tip = ""
    if ear_tip:
        # 左耳（畫面上貓的右耳）平切 = 已絕育標記
        tip = f'<path d="M84 15h11l2 5H82z" fill="{body}"/>'
    return f'''<svg viewBox="0 0 118 76" xmlns="http://www.w3.org/2000/svg" class="cat-svg">
  <ellipse cx="60" cy="70" rx="42" ry="5" fill="#0b1f2a" opacity=".13"/>
  <path d="M16 52C4 52 2 36 13 32" fill="none" stroke="{body}" stroke-width="9" stroke-linecap="round"/>
  <circle cx="30" cy="46" r="19" fill="{body}"/>
  <ellipse cx="56" cy="48" rx="38" ry="18" fill="{body}"/>
  <ellipse cx="60" cy="57" rx="30" ry="9" fill="{belly}" opacity=".9"/>
  {stripes}
  {patches}
  <g>
    {"" if ear_tip else f'<path d="M82 24 86 8l12 12z" fill="{body}"/>'}
    <path d="M82 24 86 9l12 11z" fill="{body}"/>
    <path d="M84.5 21 87 13l6.5 6z" fill="{ear}"/>
    <path d="M104 24 101 10l-9 9z" fill="{body}"/>
    <path d="M102.5 21.5 101 14l-5 5z" fill="{ear}"/>
    {tip}
  </g>
  <circle cx="93" cy="36" r="17" fill="{body}"/>
  <ellipse cx="95" cy="44" rx="10" ry="7" fill="{belly}"/>
  <g fill="{face}">
    <path d="M85 34c2.6 0 4 1.6 4 3s-1.4 3-4 3-4-1.6-4-3 1.4-3 4-3z" opacity="0"/>
    <path d="M82 35.5c1.8 0 3.2 1.2 3.2 2.6" fill="none" stroke="{face}" stroke-width="2" stroke-linecap="round"/>
    <path d="M99 35.5c1.8 0 3.2 1.2 3.2 2.6" fill="none" stroke="{face}" stroke-width="2" stroke-linecap="round"/>
    <path d="M93 43.5 91 41.5h4z"/>
  </g>
  <g fill="none" stroke="{face}" stroke-width="1.4" stroke-linecap="round" opacity=".75">
    <path d="M93 46.5c-1.6 1.8-4 1.6-5.2 0"/><path d="M93 46.5c1.6 1.8 4 1.6 5.2 0"/>
  </g>
  <g fill="{belly}">
    <rect x="72" y="56" width="17" height="9" rx="4.5"/>
    <rect x="53" y="57" width="17" height="9" rx="4.5"/>
  </g>
</svg>'''

PALETTES = {
  "orange": dict(body="#F2A344", shade="#D9822B", belly="#FCE3C0", stripes=True),
  "tuxedo": dict(body="#33333D", shade="#1E1E26", belly="#FFFFFF", face="#FFFFFF", ear="#C97F8E"),
  "calico": dict(body="#FFFFFF", shade="#E2E2E6", belly="#FFFFFF",
                 patch=("#F2A344", "#41414B"), face="#3A3A44"),
  "brown":  dict(body="#A5794E", shade="#7F5A38", belly="#EBD8BF", stripes=True),
}

CLOUD = '''<svg viewBox="0 0 120 46" xmlns="http://www.w3.org/2000/svg">
  <path fill="currentColor" d="M28 44c-12 0-20-7-20-16 0-8 6-14 14-15 2-8 10-13 19-13 10 0 18 6 20 15 9 0 16 6 16 14 0 9-8 15-19 15z"/>
</svg>'''

SKYLINE = '''<svg viewBox="0 0 390 92" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
  <g fill="#CFEBFA">
    <rect x="6" y="46" width="34" height="46" rx="3"/><rect x="46" y="60" width="26" height="32" rx="3"/>
    <rect x="78" y="34" width="30" height="58" rx="3"/><rect x="114" y="56" width="38" height="36" rx="3"/>
    <rect x="158" y="42" width="24" height="50" rx="3"/><rect x="188" y="64" width="34" height="28" rx="3"/>
    <rect x="228" y="38" width="30" height="54" rx="3"/><rect x="264" y="58" width="28" height="34" rx="3"/>
    <rect x="298" y="48" width="36" height="44" rx="3"/><rect x="340" y="62" width="30" height="30" rx="3"/>
  </g>
  <g fill="#EAF7FE">
    <rect x="12" y="54" width="6" height="7" rx="1"/><rect x="24" y="54" width="6" height="7" rx="1"/>
    <rect x="12" y="68" width="6" height="7" rx="1"/><rect x="24" y="68" width="6" height="7" rx="1"/>
    <rect x="86" y="44" width="6" height="7" rx="1"/><rect x="96" y="44" width="6" height="7" rx="1"/>
    <rect x="86" y="58" width="6" height="7" rx="1"/><rect x="96" y="58" width="6" height="7" rx="1"/>
    <rect x="236" y="48" width="6" height="7" rx="1"/><rect x="246" y="48" width="6" height="7" rx="1"/>
    <rect x="236" y="62" width="6" height="7" rx="1"/><rect x="246" y="62" width="6" height="7" rx="1"/>
    <rect x="306" y="58" width="6" height="7" rx="1"/><rect x="318" y="58" width="6" height="7" rx="1"/>
  </g>
  <g fill="#A9DDF5">
    <path d="M170 92V64c0-9 12-9 12 0v28z" opacity=".7"/>
    <path d="M356 92V68c0-8 11-8 11 0v24z" opacity=".7"/>
  </g>
</svg>'''

# ── TNVR 四格圖示 ──────────────────────────────────────────────
ICON_T = '''<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="20" width="92" height="66" rx="8" fill="#F7C873"/>
  <rect x="14" y="20" width="92" height="66" rx="8" fill="none" stroke="#4A4A52" stroke-width="4"/>
  <g stroke="#4A4A52" stroke-width="3.4" stroke-linecap="round">
    <path d="M32 22v62M50 22v62M68 22v62M86 22v62"/>
    <path d="M16 38h88M16 56h88M16 74h88"/>
  </g>
  <path d="M42 14h36l-4 8H46z" fill="#4A4A52"/>
  <circle cx="60" cy="10" r="6" fill="none" stroke="#4A4A52" stroke-width="4"/>
  <g opacity=".95">
    <ellipse cx="60" cy="66" rx="24" ry="13" fill="#F2A344"/>
    <circle cx="80" cy="56" r="12" fill="#F2A344"/>
    <path d="M72 47 74 38l8 7zM90 48l-2-9-7 7z" fill="#F2A344"/>
    <g stroke="#4A4A52" stroke-width="2" stroke-linecap="round" fill="none">
      <path d="M75 55c1.3 0 2.3.9 2.3 1.9M85 55c1.3 0 2.3.9 2.3 1.9"/>
    </g>
  </g>
</svg>'''

ICON_N = '''<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M18 96c0-20 12-31 27-31s27 11 27 31z" fill="#6FBF7F"/>
  <circle cx="45" cy="48" r="18" fill="#F6D2AE"/>
  <path d="M25 44c0-13 9-20 20-20s20 7 20 20l-4 2c-2-8-8-11-16-11s-14 3-16 11z" fill="#8A5A3B"/>
  <path d="M23 40c2-12 11-19 22-19s20 7 22 19c1-16-9-25-22-25S22 24 23 40z" fill="#4EA85F"/>
  <g stroke="#4A4A52" stroke-width="2.2" stroke-linecap="round" fill="none">
    <path d="M38 49c1.4 0 2.5 1 2.5 2.1M52 49c1.4 0 2.5 1 2.5 2.1"/>
  </g>
  <g>
    <ellipse cx="84" cy="72" rx="21" ry="12" fill="#F2A344"/>
    <circle cx="90" cy="56" r="13" fill="#F2A344"/>
    <path d="M81 47 83 37l9 8zM100 48l-2-10-8 8z" fill="#F2A344"/>
    <path d="M83.5 45 85 40l4.5 4zM97.5 45.5 96.5 41l-4 4z" fill="#E88FA0"/>
    <g stroke="#4A4A52" stroke-width="2" stroke-linecap="round" fill="none">
      <path d="M85 55c1.3 0 2.3.9 2.3 1.9M95 55c1.3 0 2.3.9 2.3 1.9"/>
    </g>
  </g>
  <path d="M60 66c6-4 13-4 18-1" fill="none" stroke="#F6D2AE" stroke-width="9" stroke-linecap="round"/>
</svg>'''

ICON_V = '''<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">
  <g>
    <ellipse cx="40" cy="74" rx="23" ry="13" fill="#F2A344"/>
    <circle cx="44" cy="55" r="15" fill="#F2A344"/>
    <path d="M34 46 36 34l10 9zM55 47l-2-11-9 9z" fill="#F2A344"/>
    <path d="M37 43.5 38.5 38l5 4.5zM52.5 44 51.5 39l-4.5 4.5z" fill="#E88FA0"/>
    <g stroke="#4A4A52" stroke-width="2.2" stroke-linecap="round" fill="none">
      <path d="M38 54c1.4 0 2.5 1 2.5 2.1M49 54c1.4 0 2.5 1 2.5 2.1"/>
    </g>
    <path d="M44 62.5 42.2 60.8h3.6z" fill="#4A4A52"/>
  </g>
  <g transform="rotate(38 86 52)">
    <rect x="76" y="30" width="20" height="42" rx="3" fill="#DCEEF7" stroke="#4A4A52" stroke-width="3"/>
    <rect x="79" y="44" width="14" height="28" rx="2" fill="#8ED1F0"/>
    <rect x="72" y="24" width="28" height="9" rx="3" fill="#4A4A52"/>
    <path d="M86 72v14" stroke="#4A4A52" stroke-width="3.4" stroke-linecap="round"/>
    <g stroke="#4A4A52" stroke-width="2" stroke-linecap="round">
      <path d="M92 40h4M92 48h4M92 56h4"/>
    </g>
  </g>
  <g fill="#6FBF7F"><circle cx="100" cy="16" r="5"/><circle cx="110" cy="24" r="3.4"/></g>
</svg>'''

ICON_R = '''<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg">
  <g fill="#6FBF7F">
    <path d="M6 96c0-9 4-15 9-15s9 6 9 15z" opacity=".9"/>
    <path d="M96 96c0-11 5-18 11-18s11 7 11 18z" opacity=".9"/>
    <path d="M26 96c0-6 3-10 6-10s6 4 6 10z" opacity=".7"/>
  </g>
  <path d="M0 96h120" stroke="#6FBF7F" stroke-width="6" stroke-linecap="round"/>
  <g>
    <path d="M40 78C26 78 24 60 36 55" fill="none" stroke="#F2A344" stroke-width="9" stroke-linecap="round"/>
    <ellipse cx="66" cy="72" rx="26" ry="15" fill="#F2A344"/>
    <circle cx="46" cy="68" r="14" fill="#F2A344"/>
    <circle cx="86" cy="54" r="16" fill="#F2A344"/>
    <path d="M74 44 77 30l12 12zM99 45l-3-14-9 9z" fill="#F2A344"/>
    <path d="M77 41 79 33l6.5 6.5z" fill="#E88FA0"/>
    <path d="M96 43h11l2 5H94z" fill="#F2A344"/>
    <g stroke="#4A4A52" stroke-width="2.2" stroke-linecap="round" fill="none">
      <path d="M79 53c1.4 0 2.5 1 2.5 2.1M92 53c1.4 0 2.5 1 2.5 2.1"/>
    </g>
    <path d="M86 61.5 84 59.5h4z" fill="#4A4A52"/>
  </g>
  <g fill="#F7C873"><circle cx="18" cy="20" r="9"/></g>
</svg>'''

# ── 剪耳示意（貓臉 + 左耳平切 + 紅圈）────────────────────────
EARTIP = '''<svg viewBox="0 0 160 150" xmlns="http://www.w3.org/2000/svg">
  <path d="M44 62 50 24l30 24z" fill="#8A6A4F"/>
  <path d="M48 57 52 34l19 15z" fill="#C99C86"/>
  <path d="M116 62 110 24 80 48z" fill="#8A6A4F"/>
  <path d="M112 57 108 34 89 49z" fill="#C99C86"/>
  <path d="M106 26h14l4 10h-19z" fill="#8A6A4F"/>
  <ellipse cx="80" cy="86" rx="42" ry="38" fill="#8A6A4F"/>
  <g fill="#6B513B" opacity=".55">
    <path d="M62 52c5 6 7 14 7 22h-6c0-8-2-15-6-20zM98 52c-5 6-7 14-7 22h6c0-8 2-15 6-20zM80 50c3 6 4 14 4 22h-8c0-8 1-16 4-22z"/>
  </g>
  <ellipse cx="80" cy="100" rx="21" ry="15" fill="#E8D5C2"/>
  <g fill="#3A2E24">
    <ellipse cx="64" cy="82" rx="7.5" ry="9"/><ellipse cx="96" cy="82" rx="7.5" ry="9"/>
  </g>
  <g fill="#FFF"><circle cx="66.5" cy="79" r="2.6"/><circle cx="98.5" cy="79" r="2.6"/></g>
  <path d="M80 98 75 93h10z" fill="#3A2E24"/>
  <g fill="none" stroke="#3A2E24" stroke-width="2.4" stroke-linecap="round">
    <path d="M80 98v4M80 102c-3 3.4-8 3-10 0M80 102c3 3.4 8 3 10 0"/>
  </g>
  <ellipse cx="114" cy="36" rx="26" ry="24" fill="none" stroke="#E5484D" stroke-width="4.5"/>
</svg>'''


CAT_SILHOUETTE = '''<svg viewBox="0 0 132 84" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M22 66C5 66 3 41 19 37" fill="none" stroke="currentColor" stroke-width="12" stroke-linecap="round"/>
  <g fill="currentColor">
    <ellipse cx="66" cy="58" rx="52" ry="22"/>
    <circle cx="34" cy="52" r="24"/>
    <circle cx="104" cy="34" r="22"/>
    <path d="M88 21 92 2l15 15zM122 22 118 3l-14 14z"/>
  </g>
</svg>'''

FISHBONE = '''<svg viewBox="0 0 132 60" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <g fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M22 15c10 5 15 10 17 15-2 5-7 10-17 15"/>
    <path d="M39 30h58"/>
    <path d="M52 14v32M66 17v26M80 20v20M91 23v14"/>
    <path d="M97 30 120 13v34z"/>
  </g>
  <circle cx="27" cy="25" r="3.4" fill="currentColor"/>
</svg>'''

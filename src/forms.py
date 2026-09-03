# -*- coding: utf-8 -*-
"""站內表單（不收集姓名、電話、email）"""

PRIVACY = "這張表單不會問你的名字、電話或 email。"

def radio(name, key, opts):
    return "".join(
        '<label class="opt"><input type="radio" name="%s" value="%s"%s><span>%s</span></label>'
        % (name, o, " checked" if i == 0 else "", o) for i, o in enumerate(opts))

def place_field(idp):
    return f'''
      <div class="fld">
        <label class="lbl" for="{idp}-place">在哪裡看到的？<i>必填</i></label>
        <input class="txt" id="{idp}-place" name="place" required
               placeholder="例：互助一街 3 巷口、一心南街公園旁" autocomplete="off">
        <button type="button" class="geo" data-geo="{idp}">用我目前的位置</button>
        <p class="geo-out" data-geo-out="{idp}" hidden></p>
        <p class="hint">按了才會抓位置，用來把貓標到地圖上。不按也可以送出。</p>
      </div>'''

def sheet(idp, title, sub, fields, submit):
    return f'''
  <div class="form-sheet" id="form-{idp}" hidden role="dialog" aria-modal="true"
       aria-labelledby="form-{idp}-h">
    <div class="form-card">
      <div class="form-head">
        <div>
          <h2 id="form-{idp}-h">{title}</h2>
          <p class="form-sub">{sub}</p>
        </div>
        <button type="button" class="form-x" data-close aria-label="關閉">✕</button>
      </div>
      <p class="privacy">🔒 {PRIVACY}</p>
      <form class="form-body" data-kind="{idp}" novalidate>
        {fields}
        <div class="fld">
          <label class="lbl" for="{idp}-photo">照片<i>可跳過</i></label>
          <input class="file" id="{idp}-photo" name="photo" type="file"
                 accept="image/*" capture="environment">
          <p class="hint">會自動縮小再上傳，不會佔你的流量。</p>
        </div>
        <button class="submit" type="submit">{submit}</button>
        <p class="form-msg" data-msg role="status"></p>
      </form>
      <div class="form-done" hidden>
        <div class="done-mark">✓</div>
        <h3>收到了，謝謝你</h3>
        <p>我們會去看看。台鳳里的浪貓會因為這一筆少一點。</p>
        <button type="button" class="submit ghost" data-close>關閉</button>
      </div>
    </div>
  </div>'''

REPORT = sheet(
    "report", "看到沒剪耳的浪貓", "四個問題，最快 20 秒",
    place_field("report") + f'''
      <div class="fld">
        <span class="lbl">有沒有剪耳？<i>必填</i></span>
        <div class="opts">{radio("eartip", "eartip", ["沒有剪耳", "有剪耳", "沒看清楚"])}</div>
        <p class="hint">剪耳＝已經結紮過了，不用再通報。不確定就選「沒看清楚」。</p>
      </div>
      <div class="fld">
        <label class="lbl" for="report-looks">貓長什麼樣子？<i>可跳過</i></label>
        <input class="txt" id="report-looks" name="looks"
               placeholder="例：橘白色，大概兩隻" autocomplete="off">
      </div>''',
    "送出通報")

COMPLAIN = sheet(
    "complain", "餵食後沒整理環境", "三個問題，不會問你是誰",
    place_field("complain") + f'''
      <div class="fld">
        <span class="lbl">是什麼狀況？<i>必填</i></span>
        <div class="opts">{radio("issue", "issue", ["剩食沒收", "容器留在原地", "環境髒亂", "其他"])}</div>
      </div>
      <div class="fld">
        <label class="lbl" for="complain-note">補充說明<i>可跳過</i></label>
        <textarea class="txt" id="complain-note" name="note" rows="3"
                  placeholder="例：每天早上都有，位置固定"></textarea>
      </div>''',
    "送出檢舉")

ALL = REPORT + COMPLAIN

# -*- coding: utf-8 -*-
"""站內表單（不收集姓名、電話、email）"""

PRIVACY = "聯絡方式可以不填。填了只會用來跟你確認這一筆，不會用在別的地方。"

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

def contact_field(idp):
    ways = ["LINE", "電話", "Email"]
    chips = "".join(
        '<label class="opt"><input type="radio" name="contact_type" value="%s"%s'
        ' data-ph="%s"><span>%s</span></label>'
        % (w, " checked" if i == 0 else "", ph, w)
        for i, (w, ph) in enumerate(zip(ways, ["你的 LINE ID", "09xx-xxx-xxx", "you@example.com"])))
    return f'''
      <div class="fld">
        <span class="lbl">方便的話留個聯絡方式<i>可跳過</i></span>
        <div class="opts">{chips}</div>
        <input class="txt" id="{idp}-contact" name="contact"
               placeholder="你的 LINE ID" autocomplete="off">
        <p class="hint">只有在需要跟你確認地點、或想告訴你處理結果時才會聯絡。不留也可以送出，通報一樣會收到。</p>
      </div>'''


NOTICE = '''
      <details class="notice">
        <summary>留了聯絡方式，我們會怎麼處理？</summary>
        <ul>
          <li><b>誰在蒐集</b>：台鳳探險隊（台鳳里浪貓通報站）</li>
          <li><b>做什麼用</b>：處理這筆浪貓通報或環境檢舉，必要時跟你確認細節、回報結果</li>
          <li><b>存哪裡</b>：本計畫的 Google 試算表，只有工作人員看得到</li>
          <li><b>會給誰</b>：本計畫工作人員，以及為了執行 TNVR 而配合的獸醫院</li>
          <li><b>存多久</b>：到這個計畫結束，或你要求刪除為止</li>
          <li><b>你的權利</b>：可以隨時要求查詢、更正或刪除你留下的聯絡方式</li>
          <li><b>不留會怎樣</b>：不影響通報，我們只是沒辦法回覆你</li>
        </ul>
      </details>'''


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
        {contact_field(idp)}
        <div class="fld">
          <label class="lbl" for="{idp}-photo">照片<i>可跳過</i></label>
          <input class="file" id="{idp}-photo" name="photo" type="file"
                 accept="image/*" capture="environment">
          <p class="hint">會自動縮小再上傳，不會佔你的流量。</p>
        </div>
        {NOTICE}
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

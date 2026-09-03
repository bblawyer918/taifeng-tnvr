# 台鳳里浪貓通報站

彰化市台鳳里的浪貓 TNVR 通報網站。一頁式、手機優先、沒有後端。

**這是一個 Build in Public 的專案**，現在還很粗糙，歡迎接手任何一塊。

## 現在的狀態

- [x] 里界地圖（資料來自 OpenStreetMap，非 Google Maps，不需要 API 金鑰）
- [x] TNVR 四步驟說明
- [x] 剪耳辨識說明
- [ ] **通報／檢舉表單還沒接**（見下方「要改什麼」）
- [ ] **地圖上的貓是示範資料**，不是真實通報紀錄
- [ ] 貓咪照片
- [ ] 通報進度回報

## 要改什麼

### 1. 表單網址

打開 `index.html`，找到最上面的設定區，只改這兩行：

```js
var FORMS = {
  report:   "https://REPLACE-ME.example/通報表單",   // 「立即通報」
  complain: "https://REPLACE-ME.example/檢舉表單"    // 「我要檢舉」
};
```

四個按鈕會一起換掉。

### 2. 貓咪資料

在 `src/build.py` 的 `CATS`。座標用 Google Maps 右鍵「這是哪裡？」複製。
改完重新產生：

```bash
python3 src/build.py
```

## 開發

沒有建置流程，沒有相依套件（Python 3 標準函式庫就夠）。

```
src/build.py    ← 把 HTML 組出來，改文案跟貓咪資料在這裡
src/style.css   ← 樣式
src/app.mjs     ← 地圖拖曳縮放、貓咪資訊卡、表單設定區
src/art.py      ← 所有插圖（手繪 SVG，可自由改）
src/mapdata.json← 里界與街道，由 tools/build_mapdata.py 產生
index.html      ← 產生出來的成品，就是部署的東西
```

本機預覽：

```bash
python3 -m http.server 8000
# 開 http://localhost:8000
```

## 想幫忙？

目前需要設計師、工程師、社區的愛媽們，還有後續可以配合的獸醫師。
開 issue 或直接發 PR 都可以。

## 授權

程式碼 MIT。地圖資料 © OpenStreetMap 貢獻者（ODbL）。插圖為本專案自繪。

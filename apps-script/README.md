# 表單後端

**已部署完成（2026-09-03）**，網址已寫進 `index.html`。以下步驟只有在要重建時才需要。

---

# 重建步驟（約 5 分鐘）

網站上的通報／檢舉表單會把資料送到這支 Apps Script，由它寫進 Google 試算表。
沒有第三方服務，資料只在你自己的 Google 帳號裡。

**回報紀錄試算表**：
https://docs.google.com/spreadsheets/d/1BxmHORen_jPpaWMIsfKKdvv_ZXe0n33GZ3RklUMQToI/edit

## 步驟

1. 打開上面那張試算表 →「擴充功能」→「Apps Script」
2. 把編輯器裡原本的 `function myFunction() {}` 全部刪掉，貼上 `Code.gs` 的完整內容
3. 按存檔（磁片圖示）
4. 右上角「部署」→「新增部署作業」
5. 左邊齒輪選「**網頁應用程式**」
6. 設定兩項：
   - 執行身分：**我**
   - 誰可以存取：**任何人**  ← 一定要選這個，里民才送得出表單
7. 按「部署」→ 第一次會要你授權，選你的 Google 帳號 →「進階」→「前往（不安全）」→「允許」
8. 複製最後給你的**網頁應用程式網址**（長得像 `https://script.google.com/macros/s/AKfy.../exec`）

## 確認有沒有成功

把那個網址直接貼到瀏覽器打開，看到這行就對了：

```json
{"ok":true,"service":"taifeng-tnvr"}
```

## 最後一步

把網址貼進 `index.html` 最上方的設定區：

```js
var ENDPOINT = "https://script.google.com/macros/s/你的網址/exec";
```

`git push` 之後網站就會自動更新。

## 之後改了 Code.gs 怎麼辦

「部署」→「管理部署作業」→ 鉛筆圖示 → 版本選「新版本」→ 部署。
**網址不會變**，不用再改網站。

## Apps Script 專案

https://script.google.com/home/projects/11RNJBlGI84q8WkWetYScw7_NaDiJJ9h84QcJpD4_iZmWjwQJl-NR2HVp/edit

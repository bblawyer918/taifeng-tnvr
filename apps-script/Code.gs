/**
 * 台鳳里浪貓通報站 — 表單後端
 * 收到網站送來的通報／檢舉，寫進 Google 試算表。
 * 不收集姓名、電話、email。
 */

const SHEET_ID = '1BxmHORen_jPpaWMIsfKKdvv_ZXe0n33GZ3RklUMQToI';
const PHOTO_FOLDER = '台鳳里浪貓通報－照片';

const SCHEMA = {
  report: {
    tab: '通報',
    cols: ['送出時間', '地點', '座標', '有沒有剪耳', '貓的樣子', '照片'],
    pick: d => [d.place || '', d.coords || '', d.eartip || '', d.looks || '']
  },
  complain: {
    tab: '檢舉',
    cols: ['送出時間', '地點', '座標', '狀況', '補充說明', '照片'],
    pick: d => [d.place || '', d.coords || '', d.issue || '', d.note || '']
  }
};

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    const s = SCHEMA[d.kind] || SCHEMA.report;
    const sheet = getTab(s.tab, s.cols);
    const photo = d.photo ? savePhoto(d.photo, s.tab) : '';
    sheet.appendRow([new Date()].concat(s.pick(d), [photo]));
    return reply({ ok: true });
  } catch (err) {
    return reply({ ok: false, error: String(err) });
  }
}

/** 讓你可以用瀏覽器打開網址，確認部署成功 */
function doGet() {
  return reply({ ok: true, service: 'taifeng-tnvr' });
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function getTab(name, cols) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.appendRow(cols);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, cols.length).setFontWeight('bold');
    sh.setColumnWidth(1, 150);
    sh.setColumnWidth(2, 220);
  }
  return sh;
}

function savePhoto(dataUrl, tab) {
  const m = /^data:([^;]+);base64,(.+)$/.exec(dataUrl);
  if (!m) return '';
  const stamp = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyyMMdd-HHmmss');
  const blob = Utilities.newBlob(Utilities.base64Decode(m[2]), m[1], tab + '-' + stamp + '.jpg');
  const it = DriveApp.getFoldersByName(PHOTO_FOLDER);
  const folder = it.hasNext() ? it.next() : DriveApp.createFolder(PHOTO_FOLDER);
  return folder.createFile(blob).getUrl();
}

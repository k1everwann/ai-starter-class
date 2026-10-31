# 測試與交付範圍

## 本機驗證

2026-10-31 重新執行：

- `tests/browser_check.py`：117 項通過，無未捕捉的 JavaScript 例外。
- `tests/standalone_check.py`：8 項通過，無未捕捉的 JavaScript 例外。

涵蓋四個任務的十二個步驟、提示詞組合、來源判斷、固定題目、紀錄與遊戲下載、重複點選不重複加分、重新開始、程式修改後讓舊預覽失效、十二張圖片的載入與關閉，以及 1240px、390px、360px 畫面。

## 遠端驗證

Actions 中的 **Prepare and check classroom site** 會重新跑相同檢查。以該次工作記錄與 `tests/results.json`、`tests/standalone-results.json` 的內容為準，不把尚未執行的測試寫成通過。

首次傳輸採兩個壓縮片段，總內容的 SHA-256 為：
`3c1137e620e91d7e80fdf0a2f92e2071962655dadae8cdf0a367d65934bdc41a`

工作流程驗證摘要後才還原來源；測試成功後將原始碼、實拍截圖與單檔版提交到根目錄，刪除傳輸片段。不會讀取或修改任何舊專案。

## 限制

瀏覽器測試用 set_content 載入真實原始碼，測互動與版面；它不是公開網站的完整端到端測試。
未驗證真實 ChatGPT、Codex 或 Google 帳號授權，未測 Safari、Firefox。一般網址上的 sessionStorage 重新整理恢復，以及真實外部服務，都不能僅因這些測試通過就宣稱已驗證。

截圖是本站練習畫面，不是官方 AI 介面。預備遊戲不是學生透過 AI 生成的作品。
首次開啟 GitHub Pages 需由專案擁有者設定，詳見 DEPLOY.md。

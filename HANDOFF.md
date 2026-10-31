# 交付狀態

更新日期：2026-10-31（台北時間）

## 已完成

網站已放進獨立的 `k1everwann/ai-starter-class` 專案，首頁直接使用根目錄 `index.html`。本次未改動 `ai-life-lab`。

- 四個短任務：問清楚、練英文、找通知、做遊戲。每個任務三步。
- 十二張本站實際操作截圖，保存在 `assets/screens/`，不引用舊站。
- 九份虛構練習資料、教師區、紀錄下載與可修改、預覽、下載的單字遊戲。
- `ai-starter-class-standalone.html`：完整內嵌教材與圖片的離線單檔版。
- 原始碼、測試程式與測試結果均已保存在本專案；初始傳輸片段已清除。

## 實際驗證

GitHub Actions 第 3 次執行已全部成功：
https://github.com/k1everwann/ai-starter-class/actions/runs/41158633728

- `tests/results.json`：117 項通過，未捕捉的 JavaScript 錯誤為 0。
- `tests/standalone-results.json`：8 項通過，未捕捉的 JavaScript 錯誤為 0。
- JavaScript 語法、圖片產生、單檔版建置、檔案提交與部署包產生均成功。

先前兩次失敗屬於測試環境：第一次是 Ubuntu 最新版本不相容；第二次使用了作業系統的 Chromium，遇到瀏覽器當機。已固定 Ubuntu 24.04，並明確選用對應 Playwright 版本的 Chromium。沒有刪除測試或放寬網站的 iframe 隔離來讓測試通過。

## 尚未完成：首次啟用公開網址

最後查核時 GitHub Pages 尚未啟用。上述成功結果只代表檔案上傳與測試完成，不代表網站已公開。

請專案擁有者開啟：
https://github.com/k1everwann/ai-starter-class/settings/pages

選擇 **Deploy from a branch → main → /(root) → Save**。

Pages 部署成功後，預定網址為：
https://k1everwann.github.io/ai-starter-class/

以 Settings → Pages 顯示的實際發布狀態為準。完整說明見 `DEPLOY.md`。

## 驗證界線

本次測試使用實際程式碼的瀏覽器互動，但以 inline set_content 載入。尚未完成公開網址的端到端測試，未驗證真實 AI／Google 帳號授權、Safari 或 Firefox，以及一般網址下的重新整理暫存恢復。

本站操作截圖不是 ChatGPT 或 Codex 的官方介面；固定練習與預備程式不是即時 AI 產出。

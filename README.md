# AI 動手做

給 14–18 歲的 90 分鐘現場實作課。**這是全新、獨立的網站，不放在舊專案裡。**

學生只做四件事：**問清楚、練英文、找通知、做遊戲**。
每個任務只有三個短步驟。長說明放在教師區，不擋住學生的操作。

## 網站入口

- `index.html`：網站首頁，直接放在本專案根目錄。
- `ai-starter-class-standalone.html`：可下載後直接開啟的單檔版。
- `STUDENT.md`：精簡學生講義。
- `scenario-data.txt`：九份完全虛構的練習資料。
- `assets/screens/`：十二張本站操作截圖，不是官方 ChatGPT 或 Codex 的介面截圖。

本專案為 `k1everwann/ai-starter-class`。程式、圖片和材料都在這裡，不依賴舊站。

## 第一次發布

請開啟 [Pages 設定](https://github.com/k1everwann/ai-starter-class/settings/pages)，選擇：

**Deploy from a branch → main → /(root) → Save**

設定完成、GitHub 的 Pages 部署成功後，網站預計位於：
`https://k1everwann.github.io/ai-starter-class/`

這是預定發布位置，不代表已啟用或已部署。實際狀態以 Settings → Pages 與 Actions 的結果為準。詳見 [DEPLOY.md](DEPLOY.md)。

## 網站裡有什麼

四格提問練習、單字練習、來源查證、可修改與下載的 HTML 遊戲。學生可以下載紀錄；教師區提供 90 分鐘帶課安排與示範說明。

本站不呼叫 AI、不讀取私人信箱、不需要 API key。不收集學生姓名或帳號。預備程式、固定題目、虛構資料都有標示。
輸入暫存在目前瀏覽器分頁的 sessionStorage；共用電腦離開前先下載，再清除紀錄。

## 本機開啟

下載整個專案，開啟 `index.html`。或執行：

```sh
python -m http.server 8000
```

再開啟 `http://localhost:8000`。網站不需要安裝 Node 套件。

## 修改與測試

- `content.js`：提示詞、模擬資料、教學內容。
- `app.js`：分步頁面與互動。
- `style.css`：白底、細線、少量藍色。
- `starter.js` / `example-game.html`：預先編寫的單字遊戲。
- `tests/`：瀏覽器檢查與結果。
- `scripts/build_standalone.py`：產生單檔版。

Actions 的「Prepare and check classroom site」會檢查程式、實際操作練習、重新擷取十二張操作圖、產生單檔版，並將成果保存在本專案。
這個流程準備檔案，不會代替你首次啟用 GitHub Pages。

測試範圍與限制見 [QA.md](QA.md)。

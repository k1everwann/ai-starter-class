# 發布這個新網站

這是獨立專案 `k1everwann/ai-starter-class`。首頁是根目錄的 `index.html`，不是舊專案的子頁面。

## 只需設定一次

1. 開啟 https://github.com/k1everwann/ai-starter-class/settings/pages 。
2. 在 Build and deployment 的 Source 選 **Deploy from a branch**。
3. Branch 選 **main**，資料夾選 **/(root)**，按 **Save**。

請不要選 GitHub Actions 作為 Pages Source；本專案使用分支發布，現有的自動化只負責檢查與產生圖片。

GitHub 的 Pages 部署成功後，在同一頁按 Visit site。預定位置是：
https://k1everwann.github.io/ai-starter-class/

如果仍出現 404，先檢查 Pages 是否已啟用，以及 Actions 中的 **pages build and deployment** 是否成功。
**Prepare and check classroom site 成功只代表檔案與測試準備完成，不代表公開網站已上線。**

本次工具連線可寫入網站檔案，但沒有首次建立 Pages 的管理操作。不需要把任何 token 或密碼貼給聊天機器人。

## 後續修改

直接修改新專案的檔案並提交。檢查流程會重新產生操作圖；以 Actions 的實際結果確認是否成功。
由 GitHub Actions 的 GITHUB_TOKEN 提交的檔案不會自行觸發另一個 Pages 建置。如果新版截圖尚未出現在網站，請在 main 提交另一個正常更新，或在 GitHub 的 Pages 建置介面重新執行。

官方參考：
https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
https://github.com/actions/configure-pages/blob/main/action.yml

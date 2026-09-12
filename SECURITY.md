# Security Policy

## 支援範圍

GPT Image 2.5 Prompt Migrator 維護最新的 v1.x 發布版本與 `main` 分支；較舊版本請先更新後再確認問題。自行修改的分支不承諾安全更新。

## 回報安全問題

若問題涉及敏感資訊、任意檔案存取、未預期的指令執行、安裝流程遭竄改，或可能危害使用者環境，請使用 GitHub 的私密漏洞回報：

[Privately report a security vulnerability](https://github.com/gd8455-create/image25-prompt-migrator/security/advisories/new)

請提供：

- 受影響的提交或版本。
- 可重現的最小步驟。
- 實際結果與預期結果。
- 已知影響，以及不含真實密鑰或個人資料的測試樣本。

請勿在公開 Issue 中貼出密碼、API key、token、私密圖片、個人資料或可直接利用的完整細節。若 GitHub 私密回報功能尚未啟用，可先建立不含敏感細節的 Issue，請維護者提供私密聯絡方式。

## 使用者內容

這個 Skill 會處理使用者提供的既有提示詞、來源工具資訊，以及可能描述參考圖片的文字。來源 prompt 可能包含客戶資料、未發布企劃、人物身分或第三方工具的私密設定；提交 Issue 或測試案例前，請移除身分資訊、帳號、檔案路徑、憑證及未獲授權公開的素材。

本專案不需要使用者在 Issue 中提供 API key，也不會把提示詞中的密鑰視為可遷移的 request setting。若發現範例、紀錄或安裝流程意外保存密鑰，請使用上方的私密漏洞回報管道。
